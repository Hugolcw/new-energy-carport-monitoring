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
# 树莓派
python3 app_edge.py raspberry_pi

# Jetson Nano
python3 app_edge.py jetson_nano

# Jetson Xavier/Orin
python3 app_edge.py jetson_xavier

# 海思芯片
python3 app_edge.py hisilicon

# 瑞芯微
python3 app_edge.py rockchip

# x86低端
python3 app_edge.py x86_low

# x86高端
python3 app_edge.py x86_high
```

### 方式3: 使用环境变量

```bash
export DEVICE_TYPE=raspberry_pi
python3 app_edge.py
```

## 📦 安装依赖

### 基础依赖

```bash
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

#### x86设备（可选CUDA）
```bash
# CPU版本
pip install torch torchvision

# CUDA版本（如果有NVIDIA GPU）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

## ⚙️ 配置说明

### 设备配置参数

系统会根据设备类型自动调整以下参数：

| 参数 | 说明 | 范围 |
|------|------|------|
| `resolution` | 视频分辨率 | (640,480) ~ (1920,1080) |
| `target_fps` | 目标帧率 | 8 ~ 30 FPS |
| `frame_skip` | 帧跳跃（每N帧推理一次） | 1 ~ 5 |
| `jpeg_quality` | JPEG压缩质量 | 65 ~ 85 |
| `detection_conf` | 检测置信度阈值 | 0.15 ~ 0.2 |
| `max_threads` | 最大线程数 | 2 ~ 8 |
| `use_gpu` | 是否使用GPU | True/False |
| `model_size` | 模型大小 | nano/small/medium |

### 自定义配置

如果需要自定义配置，可以修改 `device_config.py` 中的 `DEVICE_PRESETS` 字典。

## 🔍 性能监控

### API接口

访问 `http://localhost:5000/api/stats` 查看实时统计：

```json
{
  "total_frames": 1234,
  "detected_fires": 5,
  "detected_smoke": 2,
  "current_fps": 18.5,
  "inference_fps": 6.2,
  "cpu_usage": 45.3,
  "memory_usage": 62.1,
  "device_config": {
    "name": "Raspberry Pi 4",
    "resolution": "640x480",
    "target_fps": 10,
    "frame_skip": 5
  }
}
```

### 健康检查

访问 `http://localhost:5000/api/health` 检查服务状态。

## 🎯 性能优化建议

### 1. 树莓派优化

```bash
# 增加GPU内存分配（在/boot/config.txt中）
gpu_mem=128

# 使用SSD而非SD卡
# 关闭不必要的服务
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon
```

### 2. Jetson优化

```bash
# 设置最大性能模式
sudo nvpmodel -m 0
sudo jetson_clocks

# 设置GPU频率
sudo jetson_clocks --show
```

### 3. 内存优化

- 如果内存 < 2GB，系统会自动降低分辨率和帧率
- 建议至少 2GB 内存用于稳定运行
- 4GB+ 内存可获得更好性能

### 4. 模型选择

- **nano**: 最小模型，适合低性能设备
- **small**: 中等模型，平衡精度和速度
- **medium**: 当前使用的模型，精度较高

## 🐛 故障排查

### 问题1: 摄像头无法打开

```bash
# 检查摄像头设备
ls -l /dev/video*

# 测试摄像头
v4l2-ctl --list-devices
```

### 问题2: CUDA不可用（Jetson设备）

```bash
# 检查CUDA
python3 -c "import torch; print(torch.cuda.is_available())"

# 检查JetPack版本
cat /etc/nv_tegra_release
```

### 问题3: 内存不足

- 降低分辨率：修改 `device_config.py` 中的 `resolution`
- 增加帧跳跃：增大 `frame_skip` 值
- 使用更小的模型：设置 `model_size` 为 `nano`

### 问题4: 帧率过低

- 检查CPU使用率：`top` 或 `htop`
- 减少帧跳跃：减小 `frame_skip` 值
- 降低分辨率
- 使用GPU加速（如果支持）

## 📊 性能基准

### 树莓派4 (4GB)
- 分辨率: 640x480
- 实际FPS: 8-10 FPS
- CPU使用率: 60-80%
- 内存使用: 1.5-2GB

### Jetson Nano
- 分辨率: 1280x720
- 实际FPS: 18-22 FPS
- GPU使用率: 40-60%
- 内存使用: 2-3GB

### Jetson Xavier
- 分辨率: 1920x1080
- 实际FPS: 28-30 FPS
- GPU使用率: 30-50%
- 内存使用: 3-4GB

## 🔧 高级配置

### 环境变量

```bash
# 设置设备类型
export DEVICE_TYPE=raspberry_pi

# 启用调试模式
export DEBUG=1

# 自定义模型路径
export MODEL_PATH=./custom_model.pt
```

### 系统服务（systemd）

创建 `/etc/systemd/system/fire-detection.service`:

```ini
[Unit]
Description=Fire Detection Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/fire-detection/server
ExecStart=/usr/bin/python3 app_edge.py raspberry_pi
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl enable fire-detection
sudo systemctl start fire-detection
```

## 📝 注意事项

1. **首次运行**: 模型加载和预热需要一些时间，请耐心等待
2. **网络带宽**: 确保网络带宽足够传输视频流
3. **温度监控**: 长时间运行注意设备温度，必要时添加散热
4. **电源**: 确保电源供应充足，特别是Jetson设备
5. **存储**: 建议使用SSD而非SD卡，提升IO性能

## 🆘 获取帮助

- 查看日志: 程序运行时会输出详细日志
- API文档: 访问 `/api/health` 和 `/api/stats` 获取状态
- 设备信息: 访问 `/api/config` 查看当前配置

