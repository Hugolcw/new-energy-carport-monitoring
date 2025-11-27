# 边缘设备部署指南

本文档说明如何在不同的摄像头终端机上部署和运行火焰识别系统。

## 📋 支持的设备平台

### 1. 树莓派系列（Raspberry Pi）
- **设备**: Raspberry Pi 4 / 3B+
- **性能**: 低性能ARM
- **配置**: 640x480, 10 FPS, 每5帧推理一次
- **适用场景**: 低功耗、低成本部署

### 2. NVIDIA Jetson系列
- **Jetson Nano**: 低端GPU，1280x720, 20 FPS
- **Jetson Xavier/Orin**: 高端GPU，1920x1080, 30 FPS
- **适用场景**: 需要GPU加速的高性能场景

### 3. 海思芯片（HiSilicon）
- **设备**: 海思SoC摄像头终端
- **配置**: 1280x720, 15 FPS
- **适用场景**: 工业摄像头设备

### 4. 瑞芯微（Rockchip）
- **设备**: RK系列开发板
- **配置**: 1280x720, 15 FPS
- **适用场景**: 通用ARM设备

### 5. x86设备
- **低端**: 4核以下CPU，1280x720, 20 FPS
- **高端**: 4核以上CPU，1920x1080, 30 FPS

## 🚀 快速开始

### 方式1: 自动检测（推荐）

```bash
cd server
chmod +x scripts/start_auto.sh
./scripts/start_auto.sh
```

系统会自动检测设备类型并应用相应配置。

### 方式2: 手动指定设备类型

```bash
cd server
# 树莓派
python3 app_edge.py raspberry_pi

# Jetson Nano
python3 app_edge.py jetson_nano

# Jetson Xavier/Orin
python3 app_edge.py jetson_xavier

# 海思芯片
python3 app_edge.py hisilicon
```

### 方式3: 使用环境变量

```bash
export DEVICE_TYPE=raspberry_pi
python3 app_edge.py
```

## 📦 安装依赖

### 基础依赖

```bash
cd server
pip install -r requirements.txt
```

### PyTorch安装（根据平台选择）

#### CPU版本（树莓派、海思等）
```bash
pip install torch torchvision
```

#### Jetson设备（CUDA）
```bash
# 根据JetPack版本安装对应的PyTorch
# 参考: https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
```

## ⚙️ 配置说明

系统会根据设备类型自动调整参数。如需自定义，可修改 `server/device_config.py`。

## 🔍 性能监控

访问 `http://localhost:5000/api/stats` 查看实时统计。

## 🎯 性能优化建议

详见 `docs/optimization/OPTIMIZATION_ANALYSIS.md`

## 🐛 故障排查

详见完整文档：`docs/deployment/EDGE_DEPLOYMENT.md`

---

**完整文档**: 查看 `docs/deployment/` 目录下的详细文档

