# 🌟 风光互补太阳能充电车棚监控系统（整合版）

**文档入口**：项目文档整合请从 `docs/CONSOLIDATED.md` 开始阅读（包含部署、优化与兼容性要点）。

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

# 安装依赖
pip install -r requirements.txt

# 启动后端服务（推荐使用边缘设备优化版）
# 方式1: 自动检测设备类型
./scripts/start_auto.sh

# 方式2: 直接运行
python app_edge.py

# 方式3: 使用原始版本
python app.py
```

**边缘设备部署**: 查看 [docs/deployment/EDGE_DEPLOYMENT.md](docs/deployment/EDGE_DEPLOYMENT.md)

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
- 模型文件：应放在 `server/models/` 目录（如 `fire_m.pt`、`yolov8n.pt`）
- **边缘设备优化**: 使用 `app_edge.py` 可自动检测设备类型并优化性能

## 项目结构

```
.
├── server/                # 后端：Flask 服务与模型
│   ├── app.py             # 原始版本
│   ├── app_edge.py        # 边缘设备优化版本（推荐）
│   ├── app_optimized.py   # 通用优化版本
│   ├── device_config.py   # 设备配置和检测
│   ├── models/            # AI模型文件目录
│   │   ├── fire_m.pt
│   │   └── yolov8n.pt
│   └── scripts/           # 启动脚本
│       ├── start_auto.sh
│       └── ...
├── src/                   # 前端：Vue 应用
│   ├── components/        # 关键组件（VideoMonitor 等）
│   └── views/Dashboard.vue
├── docs/                  # 文档目录
│   ├── deployment/        # 部署文档
│   ├── optimization/      # 优化文档
│   └── compatibility/     # 兼容性文档
├── package.json
└── vite.config.ts
```

**详细结构说明**: 查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

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
# 🌟 风光互补太阳能充电车棚监控系统

一个现代化的风光互补太阳能充电车棚用户端展示页面，采用Vue 4 + TypeScript技术栈开发，具有实时监控、智能控制和科技风格UI设计。

## 🚀 在线演示

**访问地址**: https://traenewenergywebc261.vercel.app

## ✨ 核心功能

### 📊 实时监控数据
- **风力发电功率**: 实时显示风力发电功率（kW），带动态风机图标
- **太阳能发电功率**: 实时显示太阳能发电功率（kW），带动态太阳图标  
- **电池电量**: 可视化电池电量显示，支持颜色渐变和状态指示
- **总功率统计**: 综合功率显示和效率分析
- **环境数据**: 温度、湿度、风速实时监测

### 📹 视频监控系统
- **实时视频流**: 支持播放/暂停控制
- **录制功能**: 可开始/停止录制监控视频
- **截图功能**: 支持快速截图保存
- **扫描线效果**: 科技感视频扫描动画

### ⚡ 智能控制系统
- **主电源控制**: 一键开启/关闭整个系统
- **风力发电控制**: 独立控制风机启停
- **紧急停止**: 紧急情况下的快速停止功能
- **系统重置**: 系统状态重置功能

### 🎨 科技风格UI
- **深色主题**: 专业的深色背景，适合监控场景
- **渐变色彩**: 使用蓝紫色渐变营造科技感
- **发光效果**: 卡片发光和脉冲动画
- **响应式设计**: 适配各种屏幕尺寸
- **流畅动画**: 丰富的过渡效果和微交互

## 🛠️ 技术栈

- **前端框架**: Vue 3.5.12
- **编程语言**: TypeScript
- **路由管理**: Vue Router 4.4.5
- **状态管理**: Pinia 2.2.6
- **构建工具**: Vite 5.4.10
- **样式**: CSS3 + 动画效果
- **部署平台**: Vercel

## 📦 安装环境要求

### 必需环境
- **Node.js**: 18.0.0 或更高版本
- **npm**: 9.0.0 或更高版本

### 推荐环境
- **Node.js**: 22.0.0 LTS (长期支持版本)
- **npm**: 10.0.0 或更高版本

## 🔧 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/HuaHungy/new-energy-carport-monitoring.git
cd new_energy_web
```

### 2. 安装依赖
```bash
npm install
```

### 3. 开发环境启动
```bash
npm run dev
```

访问 http://localhost:5173 查看应用

### 4. 构建生产版本
```bash
npm run build
```

构建产物将生成在 `dist/` 目录中

### 5. 预览生产版本
```bash
npm run preview
```

## 📋 可用脚本

| 脚本命令 | 功能描述 |
|---------|---------|
| `npm run dev` | 启动开发服务器，支持热重载 |
| `npm run build` | 构建生产版本，优化代码 |
| `npm run preview` | 预览生产构建结果 |
| `npm run lint` | 运行ESLint代码检查和修复 |

## 🎯 项目结构

```
new_energy_web/
├── public/                 # 静态资源
├── src/
│   ├── assets/            # 资源文件
│   │   └── styles/        # 全局样式
│   ├── components/        # Vue组件
│   │   ├── BatteryCard.vue       # 电池电量组件
│   │   ├── ControlCard.vue       # 系统控制组件
│   │   ├── EnvironmentCard.vue   # 环境数据组件
│   │   ├── SolarPowerCard.vue    # 太阳能功率组件
│   │   ├── TotalPowerCard.vue    # 总功率统计组件
│   │   ├── VideoMonitor.vue      # 视频监控组件
│   │   └── WindPowerCard.vue     # 风力功率组件
│   ├── router/            # 路由配置
│   ├── views/             # 页面组件
│   │   └── Dashboard.vue  # 主仪表板页面
│   ├── App.vue            # 根组件
│   └── main.ts            # 应用入口
├── dist/                  # 构建产物（构建后生成）
├── vercel.json            # Vercel部署配置
├── vite.config.ts         # Vite配置
├── tsconfig.json          # TypeScript配置
└── package.json           # 项目配置
```

## 🎨 设计特色

### 颜色系统
- **主色调**: 蓝紫色渐变 (#06b6d4 → #8b5cf6)
- **成功色**: 绿色 (#10b981)
- **警告色**: 橙色 (#f59e0b)
- **危险色**: 红色 (#ef4444)
- **背景色**: 深蓝黑色渐变 (#0f172a → #1e293b)

### 动画效果
- **脉冲发光**: 关键数据卡片的发光效果
- **旋转动画**: 风机和太阳图标的动态效果
- **扫描线**: 视频监控的科技感扫描效果
- **过渡动画**: 平滑的状态切换和悬停效果

## 📱 响应式设计

### 桌面端 (≥1024px)
- 多列网格布局，信息展示丰富
- 完整的功能面板和数据展示

### 平板端 (768px-1023px)
- 自适应布局，保持良好的可读性
- 优化的触摸交互体验

### 手机端 (<768px)
- 单列布局，操作便捷
- 精简的界面元素，专注核心功能

## ⚠️ 注意事项

### 开发环境
1. **Node.js版本**: 确保使用推荐的Node.js版本，避免兼容性问题
2. **依赖安装**: 首次运行前必须执行 `npm install` 安装依赖
3. **端口占用**: 默认端口为5173，如被占用会自动寻找其他端口

### 代码规范
1. **TypeScript**: 项目使用TypeScript，请确保类型定义正确
2. **组件规范**: 遵循Vue 3 Composition API规范
3. **样式规范**: 使用CSS变量和模块化样式

### 性能优化
1. **图片资源**: 建议使用SVG或WebP格式的图片
2. **组件拆分**: 保持组件职责单一，避免过大的组件
3. **状态管理**: 合理使用Pinia进行状态管理

### 部署配置
1. **构建配置**: 已配置Vercel部署，支持SPA路由
2. **环境变量**: 如需后端API，请配置相应的环境变量
3. **CDN加速**: 部署后自动启用全球CDN加速

### 浏览器兼容性
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ⚠️ IE 11 (不支持)

## 🔧 常见问题

### Q: 项目启动失败怎么办？
A: 检查Node.js版本是否符合要求，删除node_modules重新安装依赖

### Q: 构建失败怎么办？
A: 运行 `npm run lint` 检查代码规范，确保TypeScript类型正确

### Q: 如何修改监控数据？
A: 在 `src/views/Dashboard.vue` 中修改模拟数据逻辑

### Q: 如何添加新的监控指标？
A: 创建新的组件并在仪表板中引入，参考现有组件结构

## 📞 技术支持

如有问题或建议，欢迎通过以下方式联系：
- 项目Issues: 提交GitHub Issue
- 功能建议: 欢迎提出新的功能需求

## 📄 许可证

MIT License - 详见LICENSE文件

---

**⭐ 如果这个项目对你有帮助，请给个Star支持一下！**
