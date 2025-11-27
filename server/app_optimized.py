"""
优化版本的后端服务
主要优化点：
1. 帧跳跃机制（每N帧推理一次）
2. 帧率控制
3. JPEG质量优化
4. 模型预热
5. 摄像头断线重连
6. 改进异常处理
7. 资源清理
8. 统计信息
"""
import cv2
import threading
import platform
import signal
import sys
import time
import logging
import numpy as np
from collections import deque
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

# --- 配置参数 ---
CONFIG = {
    'DETECTION_CONF': 0.15,  # 检测置信度阈值
    'FRAME_SKIP': 3,  # 每3帧推理一次（1=每帧都推理，3=每3帧推理一次）
    'TARGET_FPS': 30,  # 目标帧率
    'JPEG_QUALITY': 85,  # JPEG压缩质量 (0-100)
    'CAMERA_WIDTH': 1280,
    'CAMERA_HEIGHT': 720,
    'RECONNECT_THRESHOLD': 10,  # 连续失败多少次后重连
}

# --- 日志配置 ---
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- 全局统计 ---
stats = {
    'total_frames': 0,
    'detected_fires': 0,
    'detected_smoke': 0,
    'current_fps': 0.0,
    'last_detection_time': None,
}

# --- 加载模型 ---
logging.info("正在加载 YOLO 模型 (fire_m.pt)...")
try:
    model = YOLO('fire_m.pt')
    logging.info("模型加载成功，正在预热...")
    
    # 模型预热：使用虚拟帧进行推理
    dummy_frame = np.zeros((CONFIG['CAMERA_HEIGHT'], CONFIG['CAMERA_WIDTH'], 3), dtype=np.uint8)
    _ = model(dummy_frame, conf=CONFIG['DETECTION_CONF'], verbose=False)
    logging.info("✅ 模型预热完成")
except Exception as e:
    logging.error(f"❌ 模型加载失败! 请检查文件名是否正确: {e}")
    sys.exit(1)

# 检查 CUDA 状态
try:
    import torch
    if torch.cuda.is_available():
        logging.info(f"🚀 CUDA 就绪! 使用显卡: {torch.cuda.get_device_name(0)}")
        device = 'cuda'
    else:
        logging.warning("⚠️ CUDA 不可用! 正在使用 CPU")
        device = 'cpu'
except Exception as e:
    logging.info(f"无法确定 torch/cuda 状态: {e}")
    device = 'cpu'


# --- 摄像头管理类（优化版）---
class Camera:
    def __init__(self, source=0):
        self.current_source = source
        self.video = None
        self.lock = threading.Lock()
        self.fail_count = 0
        self.last_frame = None  # 缓存最后一帧
        self.frame_counter = 0  # 帧计数器（用于帧跳跃）
        self.open_camera(source)

    def _choose_backend(self):
        """根据系统选择最佳的摄像头后端"""
        system = platform.system()
        if system == 'Windows':
            return cv2.CAP_DSHOW
        elif system == 'Linux':
            return cv2.CAP_V4L2
        else:
            return 0

    def open_camera(self, source):
        """切换摄像头的核心逻辑（线程安全）"""
        with self.lock:
            if self.video is not None:
                try:
                    self.video.release()
                except Exception as e:
                    logging.warning(f"释放摄像头时出错: {e}")
                time.sleep(0.5)  # 给硬件一点喘息时间

            backend = self._choose_backend()
            
            # 尝试打开摄像头
            try:
                if backend:
                    self.video = cv2.VideoCapture(source, backend)
                else:
                    self.video = cv2.VideoCapture(source)
            except Exception as e:
                logging.warning(f"使用后端参数打开失败: {e}，尝试默认方式...")
                self.video = cv2.VideoCapture(source)

            # 如果还没打开，再试一次默认方式
            if not self.video.isOpened():
                logging.warning(f"带后端参数打开失败，尝试默认方式打开索引 {source}...")
                self.video = cv2.VideoCapture(source)

            # 设置分辨率
            if self.video.isOpened():
                try:
                    self.video.set(cv2.CAP_PROP_FRAME_WIDTH, CONFIG['CAMERA_WIDTH'])
                    self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, CONFIG['CAMERA_HEIGHT'])
                    # 设置缓冲区大小（减少延迟）
                    self.video.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                except Exception as e:
                    logging.warning(f"设置摄像头参数时出错: {e}")

            if self.video.isOpened():
                self.current_source = source
                self.fail_count = 0
                logging.info(f"📷 摄像头已切换至索引: {source}")
            else:
                logging.error(f"❌ 无法打开摄像头索引: {source}")

    def get_frame(self, skip_inference=False):
        """
        获取帧并进行AI推理
        
        Args:
            skip_inference: 是否跳过推理（用于快速获取原始帧）
        
        Returns:
            tuple: (jpeg_bytes, has_detection) 或 (None, False)
        """
        frame = None
        
        # 读取帧（线程安全）
        with self.lock:
            if not self.video or not self.video.isOpened():
                # 尝试重连
                if self.fail_count == 0:
                    logging.warning("摄像头断开，尝试重连...")
                self.fail_count += 1
                if self.fail_count >= CONFIG['RECONNECT_THRESHOLD']:
                    self.open_camera(self.current_source)
                return None, False
            
            success, frame = self.video.read()
            if not success or frame is None:
                self.fail_count += 1
                if self.fail_count >= CONFIG['RECONNECT_THRESHOLD']:
                    logging.warning("连续读取失败，尝试重连摄像头...")
                    self.open_camera(self.current_source)
                return None, False
            
            self.fail_count = 0  # 成功则重置计数

        # 帧跳跃：每N帧才推理一次
        should_infer = (self.frame_counter % CONFIG['FRAME_SKIP'] == 0) and not skip_inference
        self.frame_counter += 1
        
        # 如果不需要推理，直接返回原始帧（使用上次的检测结果）
        if not should_infer and self.last_frame is not None:
            # 使用缓存的最后一帧（已标注）
            return self.last_frame, False

        # --- AI 推理 ---
        has_danger = False
        try:
            results = model(frame, conf=CONFIG['DETECTION_CONF'], verbose=False)
            
            # 检查检测结果
            if len(results[0].boxes) > 0:
                detected_cls_ids = results[0].boxes.cls.cpu().numpy()
                confidences = results[0].boxes.conf.cpu().numpy()
                names = results[0].names
                detected_classes = []
                
                for cls_id, conf in zip(detected_cls_ids, confidences):
                    class_name = names[int(cls_id)]
                    detected_classes.append((class_name, float(conf)))
                    
                    # 检查是否为危险源
                    if class_name == 'fire':
                        has_danger = True
                        stats['detected_fires'] += 1
                        stats['last_detection_time'] = time.time()
                        logging.warning(f"🔥 检测到火焰! 置信度: {conf:.2f}")
                    elif class_name == 'smoke':
                        has_danger = True
                        stats['detected_smoke'] += 1
                        stats['last_detection_time'] = time.time()
                        logging.warning(f"💨 检测到烟雾! 置信度: {conf:.2f}")
                
                if detected_classes:
                    logging.info(f"检测到: {detected_classes}")
        
        except Exception as e:
            logging.error(f"模型推理出错: {e}", exc_info=True)
            # 推理失败时返回原始帧
            ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, CONFIG['JPEG_QUALITY']])
            if ret:
                return jpeg.tobytes(), False
            return None, False

        # 绘制检测框
        try:
            annotated_frame = results[0].plot(line_width=5, font_size=2)
            
            # JPEG编码（优化质量）
            encode_params = [cv2.IMWRITE_JPEG_QUALITY, CONFIG['JPEG_QUALITY']]
            ret, jpeg = cv2.imencode('.jpg', annotated_frame, encode_params)
            
            if ret:
                jpeg_bytes = jpeg.tobytes()
                # 缓存这一帧（用于帧跳跃时复用）
                self.last_frame = jpeg_bytes
                return jpeg_bytes, has_danger
            else:
                logging.error("JPEG编码失败")
                return None, False
                
        except Exception as e:
            logging.error(f"绘图失败: {e}", exc_info=True)
            # 绘图失败时返回原始帧
            ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, CONFIG['JPEG_QUALITY']])
            if ret:
                return jpeg.tobytes(), False
            return None, False

    def release(self):
        """释放摄像头资源"""
        with self.lock:
            if self.video is not None:
                try:
                    self.video.release()
                    logging.info("摄像头资源已释放")
                except Exception as e:
                    logging.warning(f"释放摄像头时出错: {e}")


# 全局摄像头实例
global_camera = Camera()


def generate_frames():
    """生成视频流（带帧率控制）"""
    target_fps = CONFIG['TARGET_FPS']
    frame_time = 1.0 / target_fps
    last_time = time.time()
    
    # FPS计算
    fps_buffer = deque(maxlen=30)  # 保存最近30帧的时间戳
    
    while True:
        current_time = time.time()
        
        # 帧率控制
        elapsed = current_time - last_time
        if elapsed < frame_time:
            time.sleep(frame_time - elapsed)
        
        last_time = time.time()
        fps_buffer.append(last_time)
        
        # 计算实际FPS
        if len(fps_buffer) > 1:
            stats['current_fps'] = len(fps_buffer) / (fps_buffer[-1] - fps_buffer[0])
        
        # 获取帧
        frame_data, has_danger = global_camera.get_frame()
        stats['total_frames'] += 1
        
        if frame_data is None:
            time.sleep(0.01)
            continue
        
        # MJPEG 格式流
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')


# --- API 路由 ---

@app.route('/video_feed')
def video_feed():
    """视频流接口"""
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/api/cameras')
def get_cameras():
    """扫描可用摄像头（优化：添加超时）"""
    available_cameras = []
    for i in range(5):
        cap = None
        try:
            cap = cv2.VideoCapture(i)
            # 设置超时（快速检测）
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if cap.isOpened():
                # 尝试读取一帧（带超时）
                ret, _ = cap.read()
                if ret:
                    available_cameras.append({"id": i, "name": f"摄像头 {i}"})
        except Exception as e:
            logging.debug(f"检测摄像头 {i} 时出错: {e}")
        finally:
            if cap is not None:
                cap.release()
    
    return jsonify(available_cameras)

@app.route('/api/switch_camera', methods=['POST'])
def switch_camera():
    """切换摄像头"""
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "请求体为空"}), 400
        
        new_index = int(data.get('index', 0))
        global_camera.open_camera(new_index)
        return jsonify({"status": "success", "message": f"已切换到 {new_index}"})
    except ValueError as e:
        return jsonify({"status": "error", "message": f"无效的摄像头索引: {e}"}), 400
    except Exception as e:
        logging.error(f"切换摄像头失败: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """获取统计信息"""
    return jsonify({
        "total_frames": stats['total_frames'],
        "detected_fires": stats['detected_fires'],
        "detected_smoke": stats['detected_smoke'],
        "current_fps": round(stats['current_fps'], 2),
        "last_detection_time": stats['last_detection_time'],
        "config": {
            "detection_conf": CONFIG['DETECTION_CONF'],
            "frame_skip": CONFIG['FRAME_SKIP'],
            "target_fps": CONFIG['TARGET_FPS'],
        }
    })

@app.route('/api/health')
def health_check():
    """健康检查接口"""
    camera_status = "ok" if (global_camera.video and global_camera.video.isOpened()) else "error"
    return jsonify({
        "status": "ok",
        "camera": camera_status,
        "model_loaded": model is not None,
        "device": device
    })

@app.route('/api/debug_frame')
def debug_frame():
    """调试接口：查看原始检测数据"""
    return jsonify({
        "message": "请查看终端日志输出",
        "stats": stats,
        "config": CONFIG
    })


# --- 优雅退出 ---
def _cleanup_and_exit(signum, frame):
    """清理资源并退出"""
    logging.info('👋 服务正在停止...')
    global_camera.release()
    sys.exit(0)

signal.signal(signal.SIGINT, _cleanup_and_exit)
signal.signal(signal.SIGTERM, _cleanup_and_exit)

if __name__ == '__main__':
    logging.info(f"🚀 启动服务器 (端口: 5000)")
    logging.info(f"📊 配置: 帧跳跃={CONFIG['FRAME_SKIP']}, 目标FPS={CONFIG['TARGET_FPS']}, 置信度={CONFIG['DETECTION_CONF']}")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

