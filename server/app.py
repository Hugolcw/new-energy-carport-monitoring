import cv2
import threading
import platform
import signal
import sys
import time
import logging
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)  # 允许前端跨域访问 API

# --- 日志配置 ---
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# --- 加载模型 ---
logging.info("正在加载 YOLO 模型 (fire_m.pt)...")
try:
    # 确保 fire_m.pt 文件在当前目录下
    model = YOLO('fire_m.pt')
    # 预热一下模型 (可选)
    logging.info("模型加载成功，正在预热...")
except Exception as e:
    logging.error(f"模型加载失败! 请检查文件名是否正确: {e}")
    sys.exit(1)

# 检查 CUDA 状态
try:
    import torch
    if torch.cuda.is_available():
        logging.info(f"🚀 CUDA 就绪! 使用显卡: {torch.cuda.get_device_name(0)}")
    else:
        logging.warning("⚠️ CUDA 不可用! 正在使用 CPU (可能会卡顿)")
except Exception:
    logging.info("无法确定 torch/cuda 状态")


# --- 摄像头管理类 ---
class Camera:
    def __init__(self, source=0):
        self.current_source = source
        self.video = None
        self.lock = threading.Lock()
        self.open_camera(source)

    def _choose_backend(self):
        """根据系统选择最佳的摄像头后端"""
        system = platform.system()
        if system == 'Windows':
            return cv2.CAP_DSHOW
        elif system == 'Linux':
            return cv2.CAP_V4L2 # Linux 首选 V4L2
        else:
            return 0

    def open_camera(self, source):
        """切换摄像头的核心逻辑（线程安全）"""
        with self.lock:
            if self.video is not None:
                try:
                    self.video.release()
                except Exception:
                    pass
                time.sleep(0.5) # 给硬件一点喘息时间

            backend = self._choose_backend()
            
            # 尝试 1: 带后端参数启动
            try:
                if backend:
                    self.video = cv2.VideoCapture(source, backend)
                else:
                    self.video = cv2.VideoCapture(source)
            except Exception:
                self.video = cv2.VideoCapture(source)

            # 尝试 2: 如果刚才没打开，尝试默认方式
            if not self.video.isOpened():
                logging.warning(f"带后端参数打开失败，尝试默认方式打开索引 {source}...")
                self.video = cv2.VideoCapture(source)

            # 设置高清分辨率 (1280x720) - 这对识别远距离火焰很重要
            try:
                self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            except Exception:
                pass

            if self.video.isOpened():
                self.current_source = source
                logging.info(f"📷 摄像头已切换至索引: {source}")
            else:
                logging.error(f"❌ 无法打开摄像头索引: {source}")

    def get_frame(self):
        with self.lock:
            if not self.video or not self.video.isOpened():
                return None
            success, frame = self.video.read()
            if not success or frame is None:
                return None

        # --- AI 推理 (核心修改) ---
        try:
            # 关键修改：将置信度 conf 降低到 0.15
            # 理由：打火机的火特征不明显，降低门槛能大幅提高检出率
            results = model(frame, conf=0.15)
            
            # 调试日志：如果有检测到东西，在终端打印出来
            if len(results[0].boxes) > 0:
                # 获取检测到的类别名称
                detected_cls = [results[0].names[int(cls)] for cls in results[0].boxes.cls]
                logging.info(f"🔥 检测到: {detected_cls} | 置信度: {results[0].boxes.conf.cpu().numpy()}")
        
            # 获取检测结果
            if len(results[0].boxes) > 0:
                detected_cls_ids = results[0].boxes.cls.cpu().numpy() # 获取类别ID
                names = results[0].names
            
                is_danger = False
                for cls_id in detected_cls_ids:
                    class_name = names[int(cls_id)]
                
                # 关键点：把 smoke 也纳入“火情”范畴
                    if class_name == 'fire' or class_name == 'smoke':
                        is_danger = True
                        logging.info(f"🚨 警报！检测到危险源: {class_name} (已触发火情逻辑)")
            
        except Exception as e:
            logging.error(f"模型推理出错: {e}")
            return None

        # 绘制和编码
        # try:
            # 原代码：annotated_frame = results[0].plot()
            
            # 修改为：显式传入 conf=False (或者 conf=0.1)
            # conf=False 表示：直接画出 results 里包含的所有结果，不要再做二次过滤
            #annotated_frame = results[0].plot(conf=False, labels=True, boxes=True)
            
            #ret, jpeg = cv2.imencode('.jpg', annotated_frame)
            #return jpeg.tobytes()
        #except Exception as e:
            #return None# 绘制和编码
        try:
            # --- 修改开始 ---
            
            # 1. 去掉 conf=False (先让它显示数字，确保逻辑没问题)
            # 2. 加上 line_width=5 (画一个超级粗的框，绝对能看见)
            # 3. 加上 font_size=2 (让字也大一点)
            annotated_frame = results[0].plot(line_width=5, font_size=2)
            
            # --- 修改结束 ---
            
            ret, jpeg = cv2.imencode('.jpg', annotated_frame)
            return jpeg.tobytes()
        except Exception as e:
            # 最好把错误打印出来，万一 plot 真的报错了呢
            logging.error(f"绘图失败: {e}")
            return None

# 全局摄像头实例
global_camera = Camera()


def generate_frames():
    while True:
        frame = global_camera.get_frame()
        if frame is None:
            time.sleep(0.01)
            continue
        # MJPEG 格式流
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# --- API 路由 ---

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/cameras')
def get_cameras():
    """扫描可用摄像头"""
    available_cameras = []
    # 简单扫描前 5 个索引
    for i in range(5):
        try:
            # Linux 下仅做快速探测
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # 读取一帧验证是否真的可用
                ret, _ = cap.read()
                if ret:
                    available_cameras.append({"id": i, "name": f"摄像头 {i}"})
                cap.release()
        except:
            pass
    return jsonify(available_cameras)

@app.route('/api/switch_camera', methods=['POST'])
def switch_camera():
    data = request.json
    new_index = int(data.get('index', 0))
    try:
        global_camera.open_camera(new_index)
        return jsonify({"status": "success", "message": f"已切换到 {new_index}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 调试接口：查看原始检测数据
@app.route('/api/debug_frame')
def debug_frame():
    # ... (保持原有的调试逻辑，为了简洁这里省略，上面的代码已经包含了核心功能) ...
    return jsonify({"message": "请查看终端日志输出"})

# 优雅退出
def _cleanup_and_exit(signum, frame):
    logging.info('👋 服务正在停止...')
    sys.exit(0)

signal.signal(signal.SIGINT, _cleanup_and_exit)
signal.signal(signal.SIGTERM, _cleanup_and_exit)

if __name__ == '__main__':
    # 监听所有 IP，允许局域网访问
    app.run(host='0.0.0.0', port=5000, debug=False)