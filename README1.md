# 🌟 风光互补太阳能充电车棚监控系统 (AI 增强版)

✨ 版本特性：本项目在原有的 Vue 3 可视化大屏基础上，全新集成了 Python Flask 后端与 YOLOv8 深度学习模型，实现了基于计算机视觉的实时火情与烟雾监测功能，并支持 CUDA 显卡加速。

一个现代化的风光互补太阳能充电车棚管理系统，采用 Vue 3 + TypeScript + Python 全栈开发，融合了实时数据监控、智能硬件控制、科技风格 UI 设计以及 AI 安全预警能力。

## 🚀 在线演示

**前端演示地址**: https://traenewenergywebc261.vercel.app
(注：在线演示仅包含前端静态页面布局，AI 视觉流与硬件控制功能需在本地运行 Python 后端服务)

## ✨ 核心功能

### 🔥 AI 智能视觉 (核心升级)

- **实时火情/烟雾监测**: 集成 YOLOv8m (Medium) 深度学习模型，能够实时、精准地识别视频流中的火焰与烟雾。

- **智能预警逻辑**: 针对微弱火源（如打火机、初期火苗）进行了低阈值灵敏度优化，结合多类别（Fire & Smoke）联合判断逻辑，大幅降低漏报率。

- **高性能流媒体**: 基于 OpenCV + Flask 实现 MJPEG 视频流传输，在 RTX 5060 等显卡上支持 CUDA 加速，实现 60FPS+ 丝滑体验。

- **硬件兼容性**: 底层封装了通用摄像头接口，支持笔记本自带摄像头、USB 外接相机，并提供 API 接口进行设备热切换。

### 📊 实时监控数据

- **风力发电功率**: 实时显示风力发电功率（kW），带动态风机图标。

- **太阳能发电功率**: 实时显示太阳能发电功率（kW），带动态太阳图标。

- **电池电量**: 可视化电池电量显示，支持颜色渐变和状态指示。

- **总功率统计**: 综合功率显示和效率分析。

- **环境数据**: 温度、湿度、风速实时监测。

### 📹 视频监控系统

- **实时视频流**: 无缝接入 Python 后端 AI 处理后的视频流，包含自动绘制的识别框与置信度。

- **交互控制**: 支持播放/暂停、录制、截图以及远程切换摄像头设备。

- **视觉特效**: 叠加了科技感 CSS3 扫描线动画与动态 HUD 界面。

### ⚡ 智能控制系统

- **主电源控制**: 一键开启/关闭整个系统。

- **设备控制**: 独立控制风机启停、紧急停止功能。

### 🛠️ 技术栈

前端 (Frontend)

框架: Vue 3.5.12

语言: TypeScript

构建工具: Vite 5.4.10

状态管理: Pinia 2.2.6

路由: Vue Router 4.4.5

样式: CSS3 Variables + Flex/Grid Layout

后端 (Backend & AI)

语言: Python 3.9+

Web 框架: Flask (RESTful API + 视频流服务)

计算机视觉: OpenCV (cv2)

AI 模型: Ultralytics YOLOv8 (PyTorch)

加速技术: NVIDIA CUDA (可选)

📦 安装与运行指南

为了体验完整功能，请分别启动后端和前端服务。

1. 克隆项目

git clone [https://github.com/Hugolcw/new-energy-carport-monitoring.git](https://github.com/Hugolcw/new-energy-carport-monitoring.git)
cd new-energy-carport-monitoring


2. 后端环境配置 (Python)

推荐使用 Conda 来管理 Python 环境，以避免依赖冲突。

# 1. 进入后端目录
cd server

# 2. 创建并激活虚拟环境
conda create -n fire_detect python=3.10 -y
conda activate fire_detect

# 3. 安装依赖库
# 注意：如果是 Windows 且需要显卡加速，请参考 PyTorch 官网安装对应的 CUDA 版本
pip install flask flask-cors opencv-python ultralytics

# 4. 下载 AI 模型 (关键步骤！)
# 由于模型文件(50MB)未上传至 Git，请运行此脚本自动下载 YOLOv8m 权重
python download_model.py


启动后端服务：

python app.py


终端显示 Running on http://0.0.0.0:5000 即代表启动成功。

3. 前端环境配置 (Vue)

确保本地已安装 Node.js 18+。

# 1. 打开新的终端窗口，回到项目根目录
cd .. 

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev


访问 http://localhost:5173 即可进入系统。视频监控卡片将自动连接本地后端，并在识别到火情时触发警报。

🎯 项目结构

new_energy_carport_monitoring/
├── server/                # [Backend] Python 后端与 AI 核心
│   ├── app.py            # Flask 启动入口 / 摄像头管理 / AI 推理逻辑
│   ├── download_model.py # 模型自动下载工具
│   └── fire_m.pt         # YOLOv8m 权重文件 (需运行脚本下载)
├── src/                   # [Frontend] Vue 3 源码
│   ├── api/              # 接口请求封装
│   ├── assets/           # 静态资源 (CSS, Images)
│   ├── components/       # 业务组件
│   │   ├── VideoMonitor.vue  # 视频流与控制组件 (核心)
│   │   └── ...
│   ├── views/            # 页面视图 (Dashboard)
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── public/                # 公共静态资源
├── vite.config.ts         # Vite 配置
├── tsconfig.json          # TypeScript 配置
└── README.md              # 项目文档


⚠️ 常见问题 (FAQ)

Q1: 启动后端时提示 ModuleNotFoundError？

A: 请确保你已经执行了 conda activate fire_detect 进入了正确的虚拟环境，并且在该环境下执行了 pip install。

Q2: 画面能显示，但帧率很低（卡顿）？

A: 默认情况下 PyTorch 可能使用 CPU 运行。如果你有 NVIDIA 显卡，请卸载当前的 torch，并去 PyTorch官网 下载对应 CUDA 版本的 torch（例如 pip install torch --index-url https://download.pytorch.org/whl/cu121）。

Q3: 为什么画面上没有识别框？

A:

确认后端终端是否显示 正在加载 YOLO 模型...。

确认 fire_m.pt 文件是否存在且完整（约 50MB）。

尝试调低环境光线或使用更明显的火源测试（系统已针对打火机做了低阈值优化）。

📞 技术支持

本项目由 岚曦智枢 (Lanxi Intelligent Hub) 团队开发。
如有问题或建议，欢迎提交 Issue 或联系维护者。

📄 许可证

MIT License - 详见 LICENSE 文件

⭐ Star us on GitHub if you like this project!