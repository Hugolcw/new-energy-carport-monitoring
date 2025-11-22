# 🌟 风光互补太阳能充电车棚监控系统（整合版 README）

简体中文 | 本仓库包含前端（Vue 3 + TypeScript）和后端（Flask + YOLOv8）两部分，提供实时监控、AI 火情/烟雾检测与可视化控制面板。

---

**在线演示**: https://traenewenergywebc261.vercel.app

---

## 一句话简介

一个现代化的风光互补太阳能充电车棚监控面板，集成实时数据展示、视频监控与基于 YOLOv8 的火/烟检测后端。前端用于展示与交互，后端负责视频采集、AI 推理与告警。

## 核心功能
- **实时发电与电池监控**：风力、太阳能发电功率、电池电量与总功率统计。
- **环境数据**：温度、湿度、风速等监测指标。
- **视频监控**：前端展示后端 MJPEG/流媒体，支持播放/暂停、录制与截图。
- **AI 火/烟检测**：基于 YOLOv8 模型，实时标注识别框并触发预警。
- **智能控制**：主电源与风机开关、紧急停止与系统重置。

## 主要设计目标
- 可视化与可操作性：前端以仪表盘形式聚合关键指标并提供快捷操作控件。
- 实时性与稳定性：视频与数据流分离，后端优化推理性能（支持 CUDA）。
- 易部署：前后端分离，后端在 `server/`，前端在 `src/`，清晰的启动步骤。

## 技术栈
- 前端：Vue 3 + TypeScript、Vite、Pinia、Vue Router
- 后端：Python 3.9+、Flask、OpenCV（cv2）、Ultralytics YOLOv8
- AI：YOLOv8 权重文件（`fire_m.pt` 或 `yolov8n.pt`）

## 快速开始（开发）

前提：系统已安装 Node.js (>=18) 与 Python (>=3.9)。如果需要 GPU 加速，按 PyTorch 官网安装对应 CUDA 的 `torch`。

1. 克隆仓库

```bash
git clone https://github.com/Hugolcw/new-energy-carport-monitoring.git
cd new-energy-carport-monitoring
```

2. 启动后端（AI 推理服务）

```bash
# 进入后端目录
cd server

# 建议使用 conda（可选）
conda create -n fire_detect python=3.10 -y
conda activate fire_detect

# 安装依赖
pip install -r requirements.txt  # 若项目无 requirements.txt，请手动 pip install flask flask-cors opencv-python ultralytics

# （如需）下载模型权重（项目可能提供脚本或将权重置于 server/ 目录）
python download_model.py

# 启动后端服务
python app.py
```

默认后端服务地址：`http://0.0.0.0:5000`，视频流或 API 会在该地址暴露相应路由。

3. 启动前端（开发模式）

```bash
# 回到项目根目录
cd ..
npm install
npm run dev
```

前端默认访问：`http://localhost:5173`。如果前端看不到视频，请确认后端已启动且前端 Video 卡片中的流地址指向本地后端。

## 模型与加速说明
- 默认使用 CPU 运行 YOLOv8（兼容性好），但如需更高帧率请安装对应 CUDA 版本的 `torch`。参考 PyTorch 官网获取适配命令。
- 模型文件：`server/fire_m.pt`（若缺失，请运行 `download_model.py` 或从项目文档指定 URL 下载）。

## 项目结构（重要文件）

```
.
├── server/                # 后端：Flask 服务与模型
│   ├── app.py
│   ├── download_model.py
│   └── fire_m.pt
├── src/                   # 前端：Vue 应用
│   ├── components/        # 关键组件（VideoMonitor 等）
│   └── views/Dashboard.vue
├── package.json
├── vite.config.ts
└── README_GENERATED.md    # （本文件）
```

## 常见问题
- Q: 后端启动失败提示缺少模块？
  - A: 请激活正确的 Python 环境并 `pip install` 所需包，或使用 `requirements.txt`。
- Q: 画面能显示但很卡？
  - A: 检查后端是否在 CPU 模式，若有 NVIDIA 显卡请安装支持的 `torch` + CUDA 版本。
- Q: 为什么没有检测框？
  - A: 确认模型权重存在，且后端加载模型没有错误；可通过后端日志检查。

## 开发与贡献
- 若要修改前端，请在 `src/components` 中新增或调整组件，使用 Pinia 管理全局状态。
- 若要改进后端推理或模型，修改 `server/app.py` 中的推理逻辑，并在本地测试再发 PR。

## 许可与致谢
- 本项目遵循 MIT 许可证（见仓库 LICENSE）。
- 感谢 Ultralytics YOLOv8 与开源社区提供的计算机视觉工具链。

---

## 我怎么组织这个 README（思路说明）

1. 目标读者：开发者或运维工程师，既需要快速上手（安装/运行）也需要了解系统架构与模型依赖。
2. 结构设计：先给出简介与核心功能，让阅读者快速判断项目用途；随后给出分步的“快速开始”，细分后端与前端启动步骤，减少上手成本。
3. 模型与性能提示：把 GPU 加速与模型位置等常见阻塞点单列出来，便于排障。
4. 项目结构与常见问题：帮助开发者快速定位代码并解决常见错误。
5. 可扩展性考虑：提示在哪里修改推理或前端组件，以便贡献者快速上手。

如果你愿意，我可以：
- 1) 将此文件合并为仓库根目录的 `README.md`（覆盖或追加），
- 2) 生成 `requirements.txt`（从现有代码推断常用依赖），
- 3) 运行本地 lint / 启动脚本并验证前端/后端是否能在当前环境启动（需要你允许我执行终端命令）。

请告诉我接下来希望我做哪一步。🙋
