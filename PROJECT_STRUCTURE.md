# 项目结构说明

## 📁 目录结构

```
new-energy-carport-monitoring/
├── README.md                    # 项目主文档
├── PROJECT_STRUCTURE.md         # 本文档（项目结构说明）
│
├── docs/                        # 📚 文档目录
│   ├── README.md               # 文档索引
│   ├── deployment/             # 部署文档
│   │   ├── EDGE_DEPLOYMENT.md
│   │   └── PLATFORM_OPTIMIZATION_SUMMARY.md
│   ├── optimization/           # 优化文档
│   │   └── OPTIMIZATION_ANALYSIS.md
│   └── compatibility/         # 兼容性文档
│       ├── COMPATIBILITY_CHECK.md
│       └── COMPATIBILITY_FIXES.md
│
├── server/                     # 🔧 后端服务
│   ├── app.py                  # 原始版本
│   ├── app_optimized.py        # 通用优化版本
│   ├── app_edge.py             # 边缘设备优化版本（推荐）
│   ├── device_config.py        # 设备配置和检测
│   ├── requirements.txt        # Python依赖
│   ├── environment.yml         # Conda环境配置
│   │
│   ├── models/                 # 🤖 AI模型文件
│   │   ├── fire_m.pt           # 火焰检测模型（中等）
│   │   ├── fire.pt              # 火焰检测模型（备用）
│   │   └── yolov8n.pt          # YOLOv8 Nano模型（轻量）
│   │
│   └── scripts/                # 🚀 启动脚本
│       ├── start_auto.sh       # 自动检测设备类型
│       ├── start_raspberry_pi.sh
│       ├── start_jetson.sh
│       └── start_hisilicon.sh
│
├── src/                        # 🎨 前端源码
│   ├── components/            # Vue组件
│   │   ├── BatteryCard.vue
│   │   ├── ControlCard.vue
│   │   ├── EnvironmentCard.vue
│   │   ├── SolarPowerCard.vue
│   │   ├── TotalPowerCard.vue
│   │   ├── VideoMonitor.vue
│   │   └── WindPowerCard.vue
│   ├── views/                 # 页面视图
│   │   └── Dashboard.vue
│   ├── router/               # 路由配置
│   │   └── index.ts
│   ├── assets/               # 静态资源
│   │   └── styles/
│   │       └── main.css
│   ├── App.vue               # 根组件
│   └── main.ts               # 入口文件
│
├── package.json               # 前端依赖配置
├── vite.config.ts            # Vite构建配置
├── tsconfig.json             # TypeScript配置
├── vercel.json               # Vercel部署配置
└── index.html                # HTML入口
```

## 📋 文件说明

### 后端文件

| 文件 | 说明 | 使用场景 |
|------|------|---------|
| `app.py` | 原始版本 | 基础功能，参考用 |
| `app_optimized.py` | 通用优化版 | PC/服务器部署 |
| `app_edge.py` | 边缘设备版 | **推荐**，终端机部署 |
| `device_config.py` | 设备配置 | 自动检测和配置设备 |

### 启动脚本

| 脚本 | 说明 |
|------|------|
| `scripts/start_auto.sh` | 自动检测设备类型（推荐） |
| `scripts/start_raspberry_pi.sh` | 树莓派专用 |
| `scripts/start_jetson.sh` | Jetson设备（自动识别Nano/Xavier） |
| `scripts/start_hisilicon.sh` | 海思芯片 |

### 模型文件

| 模型 | 大小 | 适用场景 |
|------|------|---------|
| `yolov8n.pt` | 最小 | 低性能设备（树莓派等） |
| `fire_m.pt` | 中等 | 高性能设备（Jetson Xavier等） |

## 🎯 使用建议

### 开发环境
- 使用 `app.py` 或 `app_optimized.py` 进行开发测试

### 生产环境（终端机）
- 使用 `app_edge.py` + `scripts/start_auto.sh`

### 文档查阅
- 部署问题 → `docs/deployment/`
- 性能优化 → `docs/optimization/`
- 兼容性 → `docs/compatibility/`

## 📝 注意事项

1. **模型文件位置**: 模型文件应放在 `server/models/` 目录
2. **启动脚本**: 所有启动脚本都在 `server/scripts/` 目录
3. **文档**: 所有技术文档都在 `docs/` 目录，按分类组织

---

**最后更新**: 2024-11-22

