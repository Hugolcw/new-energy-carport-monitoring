import cv2
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from ultralytics import YOLO
import time

app = Flask(__name__)
CORS(app)  # 允许前端跨域访问 API

# 加载模型
print("正在加载 YOLOv8-Medium 模型...")
model = YOLO('fire_m.pt') # 确保这里是你最新的模型文件名

# --- 摄像头管理类 (核心升级) ---
class Camera:
    def __init__(self):
        self.current_source = 0
        self.video = None
        self.open_camera(0)

    def open_camera(self, source):
        """切换摄像头的核心逻辑"""
        if self.video is not None:
            self.video.release() # 先释放旧的
            time.sleep(0.5)      # 稍微等一下，防止硬件占用冲突
        
        # 尝试打开新设备
        self.video = cv2.VideoCapture(source)
        
        # 强制 720P 高清
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.current_source = source
        print(f"📷 摄像头已切换至索引: {source}")

    def get_frame(self):
        if not self.video or not self.video.isOpened():
            return None
        
        success, frame = self.video.read()
        if not success:
            return None
            
        # AI 识别
        results = model(frame, conf=0.25)
        annotated_frame = results[0].plot()
        
        ret, jpeg = cv2.imencode('.jpg', annotated_frame)
        return jpeg.tobytes()

# 全局摄像头单例
global_camera = Camera()

def generate_frames():
    while True:
        frame = global_camera.get_frame()
        if frame is None:
            continue # 如果切换中获取失败，就跳过这一帧
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# --- API 接口区域 ---

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 新增：扫描可用摄像头 API
@app.route('/api/cameras')
def get_cameras():
    available_cameras = []
    # 简单粗暴地扫描前 3 个索引，看看哪个能开
    for i in range(3):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW) 
        if cap.isOpened():
            available_cameras.append({"id": i, "name": f"摄像头 {i}"})
            cap.release()
    return jsonify(available_cameras)

# 新增：切换摄像头 API
@app.route('/api/switch_camera', methods=['POST'])
def switch_camera():
    data = request.json
    new_index = int(data.get('index', 0))
    try:
        global_camera.open_camera(new_index)
        return jsonify({"status": "success", "message": f"已切换到摄像头 {new_index}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)