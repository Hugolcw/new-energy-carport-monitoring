"""
边缘设备优化版本 - 针对终端机部署
支持多平台自动检测和性能自适应
"""
import cv2
import threading
import platform
import signal
import sys
import time
import logging
import numpy as np
import os
from collections import deque
from queue import Queue, Empty
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from ultralytics import YOLO

# 导入设备配置
from device_config import get_device_config, get_model_path, print_device_info

app = Flask(__name__)
CORS(app)

# --- 从环境变量或命令行参数获取设备类型 ---
DEVICE_TYPE = os.getenv('DEVICE_TYPE', None)
if len(sys.argv) > 1:
    DEVICE_TYPE = sys.argv[1]

# 获取设备配置
CONFIG, detected_device_type = get_device_config(DEVICE_TYPE)

# 获取模型路径并检查
try:
    MODEL_PATH = get_model_path(CONFIG['model_size'])
    if not os.path.exists(MODEL_PATH):
        logging.error(f"❌ 模型文件不存在: {MODEL_PATH}")
        logging.error("请确保模型文件在 server/ 目录下")
        logging.error("可用模型: fire_m.pt, yolov8n.pt, yolov8s.pt")
        sys.exit(1)
except FileNotFoundError as e:
    logging.error(f"❌ {e}")
    logging.error("请确保模型文件存在")
    sys.exit(1)

# --- 日志配置 ---
log_level = logging.DEBUG if os.getenv('DEBUG', '0') == '1' else logging.INFO
logging.basicConfig(
    level=log_level,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 打印设备信息
print_device_info(CONFIG, detected_device_type)

# --- 全局统计 ---
stats = {
    'total_frames': 0,
    'detected_fires': 0,
    'detected_smoke': 0,
    'current_fps': 0.0,
    'inference_fps': 0.0,
    'last_detection_time': None,
    'cpu_usage': 0.0,
    'memory_usage': 0.0,
}

# --- 加载模型 ---
logging.info(f"正在加载 YOLO 模型 ({MODEL_PATH})...")
try:
    model = YOLO(MODEL_PATH)
    
    # 设置设备
    device = 'cuda' if CONFIG['use_gpu'] else 'cpu'
    if device == 'cuda':
        try:
            import torch
            if torch.cuda.is_available():
                logging.info(f"🚀 CUDA 就绪! 使用显卡: {torch.cuda.get_device_name(0)}")
            else:
                logging.warning("⚠️ CUDA 不可用! 切换到 CPU")
                device = 'cpu'
        except:
            device = 'cpu'
    
    if device == 'cpu':
        logging.info("💻 使用 CPU 模式")
    
    # 模型预热
    logging.info("正在预热模型...")
    warmup_resolution = CONFIG['resolution']
    dummy_frame = np.zeros((warmup_resolution[1], warmup_resolution[0], 3), dtype=np.uint8)
    _ = model(dummy_frame, conf=CONFIG['detection_conf'], verbose=False, device=device)
    logging.info("✅ 模型预热完成")
    
except Exception as e:
    logging.error(f"❌ 模型加载失败! 错误: {e}", exc_info=True)
    sys.exit(1)


# --- 摄像头管理类（边缘设备优化版）---
class EdgeCamera:
    def __init__(self, source=0):
        self.current_source = source
        self.video = None
        self.lock = threading.Lock()
        self.fail_count = 0
        self.last_frame = None
        self.last_results = None  # 缓存检测结果
        self.frame_counter = 0
        self.inference_times = deque(maxlen=30)  # 推理时间统计
        
        # 多线程推理队列
        self.frame_queue = Queue(maxsize=2)  # 限制队列大小避免内存溢出
        self.result_queue = Queue(maxsize=2)
        self.inference_thread = None
        self.running = True
        
        self.open_camera(source)
        self.start_inference_thread()

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
        """切换摄像头"""
        with self.lock:
            if self.video is not None:
                try:
                    self.video.release()
                except Exception as e:
                    logging.warning(f"释放摄像头时出错: {e}")
                time.sleep(0.5)

            backend = self._choose_backend()
            
            try:
                if backend:
                    self.video = cv2.VideoCapture(source, backend)
                else:
                    self.video = cv2.VideoCapture(source)
            except Exception as e:
                logging.warning(f"使用后端参数打开失败: {e}")
                self.video = cv2.VideoCapture(source)

            if not self.video.isOpened():
                logging.warning(f"带后端参数打开失败，尝试默认方式...")
                self.video = cv2.VideoCapture(source)

            # 设置分辨率和缓冲区
            if self.video.isOpened():
                try:
                    width, height = CONFIG['resolution']
                    self.video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                    self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                    self.video.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 最小缓冲区减少延迟
                    # 设置帧率（如果支持）
                    self.video.set(cv2.CAP_PROP_FPS, CONFIG['target_fps'])
                except Exception as e:
                    logging.warning(f"设置摄像头参数时出错: {e}")

            if self.video.isOpened():
                self.current_source = source
                self.fail_count = 0
                logging.info(f"📷 摄像头已切换至索引: {source}")
            else:
                logging.error(f"❌ 无法打开摄像头索引: {source}")

    def start_inference_thread(self):
        """启动推理线程（异步处理）"""
        def inference_worker():
            while self.running:
                try:
                    # 从队列获取帧（带超时）
                    frame_data = self.frame_queue.get(timeout=1.0)
                    if frame_data is None:
                        continue
                    
                    frame, frame_id = frame_data
                    
                    # 执行推理
                    start_time = time.time()
                    results = model(
                        frame,
                        conf=CONFIG['detection_conf'],
                        verbose=False,
                        device=device
                    )
                    inference_time = time.time() - start_time
                    self.inference_times.append(inference_time)
                    
                    # 计算推理FPS
                    if len(self.inference_times) > 1:
                        stats['inference_fps'] = 1.0 / (sum(self.inference_times) / len(self.inference_times))
                    
                    # 处理检测结果
                    has_danger = False
                    if len(results[0].boxes) > 0:
                        detected_cls_ids = results[0].boxes.cls.cpu().numpy()
                        confidences = results[0].boxes.conf.cpu().numpy()
                        names = results[0].names
                        
                        for cls_id, conf in zip(detected_cls_ids, confidences):
                            class_name = names[int(cls_id)]
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
                    
                    # 绘制检测框
                    annotated_frame = results[0].plot(line_width=3, font_size=1)
                    
                    # JPEG编码
                    encode_params = [cv2.IMWRITE_JPEG_QUALITY, CONFIG['jpeg_quality']]
                    ret, jpeg = cv2.imencode('.jpg', annotated_frame, encode_params)
                    
                    if ret:
                        # 将结果放入结果队列
                        self.result_queue.put((jpeg.tobytes(), frame_id, has_danger))
                    
                except Empty:
                    continue
                except Exception as e:
                    logging.error(f"推理线程出错: {e}", exc_info=True)
        
        self.inference_thread = threading.Thread(target=inference_worker, daemon=True)
        self.inference_thread.start()
        logging.info("✅ 推理线程已启动")

    def get_frame(self):
        """
        获取帧（异步推理版本）
        
        Returns:
            tuple: (jpeg_bytes, has_danger) 或 (None, False)
        """
        frame = None
        
        # 读取帧
        with self.lock:
            if not self.video or not self.video.isOpened():
                self.fail_count += 1
                if self.fail_count >= 10:
                    logging.warning("摄像头断开，尝试重连...")
                    self.open_camera(self.current_source)
                return None, False
            
            success, frame = self.video.read()
            if not success or frame is None:
                self.fail_count += 1
                if self.fail_count >= 10:
                    self.open_camera(self.current_source)
                return None, False
            
            self.fail_count = 0

        # 帧跳跃：每N帧才推理一次
        should_infer = (self.frame_counter % CONFIG['frame_skip'] == 0)
        self.frame_counter += 1
        
        if should_infer:
            # 需要推理：将帧放入队列
            try:
                self.frame_queue.put_nowait((frame.copy(), self.frame_counter))
            except:
                # 队列满，跳过这一帧
                pass
        
        # 尝试从结果队列获取最新结果
        latest_result = None
        latest_id = -1
        
        # 清空旧结果，只保留最新的
        while True:
            try:
                result = self.result_queue.get_nowait()
                if result[1] > latest_id:
                    latest_result = result
                    latest_id = result[1]
            except Empty:
                break
        
        if latest_result:
            jpeg_bytes, _, has_danger = latest_result
            self.last_frame = jpeg_bytes
            return jpeg_bytes, has_danger
        elif self.last_frame:
            # 使用缓存的最后一帧
            return self.last_frame, False
        else:
            # 没有结果，返回原始帧
            encode_params = [cv2.IMWRITE_JPEG_QUALITY, CONFIG['jpeg_quality']]
            ret, jpeg = cv2.imencode('.jpg', frame, encode_params)
            if ret:
                return jpeg.tobytes(), False
            return None, False

    def release(self):
        """释放资源"""
        self.running = False
        with self.lock:
            if self.video is not None:
                try:
                    self.video.release()
                    logging.info("摄像头资源已释放")
                except Exception as e:
                    logging.warning(f"释放摄像头时出错: {e}")


# 全局摄像头实例
global_camera = EdgeCamera()


def generate_frames():
    """生成视频流（带帧率控制和资源监控）"""
    target_fps = CONFIG['target_fps']
    frame_time = 1.0 / target_fps
    last_time = time.time()
    fps_buffer = deque(maxlen=30)
    
    # 资源监控间隔
    last_stats_time = time.time()
    stats_interval = 5.0  # 每5秒更新一次统计
    
    while True:
        current_time = time.time()
        
        # 帧率控制
        elapsed = current_time - last_time
        if elapsed < frame_time:
            time.sleep(frame_time - elapsed)
        
        last_time = time.time()
        fps_buffer.append(last_time)
        
        # 计算FPS
        if len(fps_buffer) > 1:
            stats['current_fps'] = len(fps_buffer) / (fps_buffer[-1] - fps_buffer[0])
        
        # 定期更新资源使用情况
        if current_time - last_stats_time > stats_interval:
            try:
                import psutil
                stats['cpu_usage'] = psutil.cpu_percent(interval=0.1)
                stats['memory_usage'] = psutil.virtual_memory().percent
            except ImportError:
                pass
            except Exception:
                pass
            last_stats_time = current_time
        
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
    """扫描可用摄像头"""
    available_cameras = []
    for i in range(5):
        cap = None
        try:
            cap = cv2.VideoCapture(i)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if cap.isOpened():
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
        "inference_fps": round(stats['inference_fps'], 2),
        "cpu_usage": round(stats['cpu_usage'], 1),
        "memory_usage": round(stats['memory_usage'], 1),
        "last_detection_time": stats['last_detection_time'],
        "device_config": {
            "name": CONFIG['name'],
            "resolution": f"{CONFIG['resolution'][0]}x{CONFIG['resolution'][1]}",
            "target_fps": CONFIG['target_fps'],
            "frame_skip": CONFIG['frame_skip'],
            "detection_conf": CONFIG['detection_conf'],
            "use_gpu": CONFIG['use_gpu'],
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
        "device": device,
        "device_type": detected_device_type,
    })

@app.route('/api/config')
def get_config():
    """获取当前配置"""
    return jsonify(CONFIG)

@app.route('/api/debug_frame')
def debug_frame():
    """调试接口（兼容原版）"""
    return jsonify({
        "message": "请查看终端日志输出",
        "stats": stats,
        "config": CONFIG,
        "device_type": detected_device_type
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
    logging.info(f"🚀 启动边缘设备服务器 (端口: 5000)")
    logging.info(f"📊 设备: {CONFIG['name']}")
    logging.info(f"📊 模型: {MODEL_PATH}")
    
    # 导入psutil用于资源监控
    try:
        import psutil
    except ImportError:
        logging.warning("psutil 未安装，资源监控功能将不可用")
        logging.warning("建议安装: pip install psutil")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

