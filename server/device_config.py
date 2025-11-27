"""
设备配置和性能预设
根据不同的终端机平台自动调整参数
"""
import platform
import os
import subprocess
import logging

# 延迟导入psutil（可选依赖）
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# 设备预设配置
DEVICE_PRESETS = {
    # 低性能ARM设备（树莓派4等）
    'raspberry_pi': {
        'name': 'Raspberry Pi 4',
        'resolution': (640, 480),  # 降低分辨率
        'target_fps': 10,  # 低帧率
        'frame_skip': 5,  # 每5帧推理一次
        'jpeg_quality': 70,  # 较低质量
        'detection_conf': 0.2,  # 稍高置信度减少误检
        'max_threads': 2,  # 限制线程数
        'use_gpu': False,
        'model_size': 'nano',  # 使用最小模型
    },
    
    # Jetson Nano（低端GPU）
    'jetson_nano': {
        'name': 'NVIDIA Jetson Nano',
        'resolution': (1280, 720),
        'target_fps': 20,
        'frame_skip': 2,
        'jpeg_quality': 80,
        'detection_conf': 0.15,
        'max_threads': 4,
        'use_gpu': True,
        'model_size': 'nano',
    },
    
    # Jetson Xavier/Orin（高端GPU）
    'jetson_xavier': {
        'name': 'NVIDIA Jetson Xavier/Orin',
        'resolution': (1920, 1080),
        'target_fps': 30,
        'frame_skip': 1,  # 几乎每帧都推理
        'jpeg_quality': 85,
        'detection_conf': 0.15,
        'max_threads': 8,
        'use_gpu': True,
        'model_size': 'medium',
    },
    
    # 海思芯片（常见于摄像头终端）
    'hisilicon': {
        'name': 'HiSilicon SoC',
        'resolution': (1280, 720),
        'target_fps': 15,
        'frame_skip': 3,
        'jpeg_quality': 75,
        'detection_conf': 0.18,
        'max_threads': 4,
        'use_gpu': False,  # 通常没有CUDA支持
        'model_size': 'nano',
    },
    
    # 瑞芯微芯片
    'rockchip': {
        'name': 'Rockchip SoC',
        'resolution': (1280, 720),
        'target_fps': 15,
        'frame_skip': 3,
        'jpeg_quality': 75,
        'detection_conf': 0.18,
        'max_threads': 4,
        'use_gpu': False,
        'model_size': 'nano',
    },
    
    # x86设备（中等性能）
    'x86_low': {
        'name': 'x86 Low-end',
        'resolution': (1280, 720),
        'target_fps': 20,
        'frame_skip': 3,
        'jpeg_quality': 80,
        'detection_conf': 0.15,
        'max_threads': 4,
        'use_gpu': False,
        'model_size': 'nano',
    },
    
    # x86高性能
    'x86_high': {
        'name': 'x86 High-end',
        'resolution': (1920, 1080),
        'target_fps': 30,
        'frame_skip': 1,
        'jpeg_quality': 85,
        'detection_conf': 0.15,
        'max_threads': 8,
        'use_gpu': True,  # 如果有GPU
        'model_size': 'medium',
    },
    
    # 默认配置（自动检测）
    'auto': {
        'name': 'Auto-detect',
        'resolution': (1280, 720),
        'target_fps': 20,
        'frame_skip': 3,
        'jpeg_quality': 80,
        'detection_conf': 0.15,
        'max_threads': 4,
        'use_gpu': False,
        'model_size': 'nano',
    },
}


def detect_device_type():
    """
    自动检测设备类型
    返回设备类型字符串
    """
    system = platform.system()
    machine = platform.machine().lower()
    
    # 检测Jetson设备
    try:
        if os.path.exists('/proc/device-tree/model'):
            with open('/proc/device-tree/model', 'r') as f:
                model = f.read().lower()
                if 'jetson' in model:
                    if 'nano' in model:
                        return 'jetson_nano'
                    elif 'xavier' in model or 'orin' in model:
                        return 'jetson_xavier'
                    return 'jetson_nano'  # 默认
    except:
        pass
    
    # 检测树莓派
    try:
        if os.path.exists('/proc/cpuinfo'):
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read().lower()
                if 'raspberry pi' in cpuinfo or 'bcm' in cpuinfo:
                    return 'raspberry_pi'
    except:
        pass
    
    # 检测海思芯片
    try:
        if os.path.exists('/proc/device-tree/compatible'):
            with open('/proc/device-tree/compatible', 'r') as f:
                compatible = f.read().lower()
                if 'hisilicon' in compatible or 'hi' in compatible:
                    return 'hisilicon'
    except:
        pass
    
    # 检测瑞芯微
    try:
        if os.path.exists('/proc/device-tree/compatible'):
            with open('/proc/device-tree/compatible', 'r') as f:
                compatible = f.read().lower()
                if 'rockchip' in compatible or 'rk' in compatible:
                    return 'rockchip'
    except:
        pass
    
    # 根据架构判断
    if 'arm' in machine or 'aarch64' in machine:
        # ARM设备，根据CPU核心数和频率判断性能
        if HAS_PSUTIL:
            try:
                cpu_count = psutil.cpu_count()
                cpu_freq = psutil.cpu_freq()
                if cpu_freq and cpu_freq.max:
                    if cpu_count <= 4 and cpu_freq.max < 2000:
                        return 'raspberry_pi'  # 低性能ARM
                    else:
                        return 'hisilicon'  # 中等性能ARM
            except:
                pass
        return 'raspberry_pi'  # 默认低性能
    elif 'x86' in machine or 'amd64' in machine:
        # x86设备，根据CPU核心数判断
        if HAS_PSUTIL:
            try:
                cpu_count = psutil.cpu_count()
                if cpu_count <= 4:
                    return 'x86_low'
                else:
                    return 'x86_high'
            except:
                pass
        return 'x86_low'
    
    return 'auto'


def get_device_config(device_type=None):
    """
    获取设备配置
    
    Args:
        device_type: 设备类型，如果为None则自动检测
    
    Returns:
        dict: 设备配置字典
    """
    if device_type is None:
        device_type = detect_device_type()
    
    if device_type not in DEVICE_PRESETS:
        logging.warning(f"未知设备类型: {device_type}，使用默认配置")
        device_type = 'auto'
    
    config = DEVICE_PRESETS[device_type].copy()
    
    # 检查GPU可用性
    if config['use_gpu']:
        try:
            import torch
            if not torch.cuda.is_available():
                logging.warning("配置要求GPU但CUDA不可用，切换到CPU模式")
                config['use_gpu'] = False
                # 降低性能参数
                config['target_fps'] = max(10, config['target_fps'] // 2)
                config['frame_skip'] = config['frame_skip'] * 2
        except:
            config['use_gpu'] = False
    
    # 根据实际CPU核心数调整线程数
    if HAS_PSUTIL:
        try:
            cpu_count = psutil.cpu_count()
            config['max_threads'] = min(config['max_threads'], cpu_count)
        except:
            pass
    
    # 根据内存调整
    if HAS_PSUTIL:
        try:
            memory = psutil.virtual_memory()
            total_gb = memory.total / (1024**3)
            if total_gb < 2:
                # 内存小于2GB，进一步降低参数
                config['resolution'] = (640, 480)
                config['target_fps'] = max(8, config['target_fps'] // 2)
                config['frame_skip'] = config['frame_skip'] * 2
                config['jpeg_quality'] = 65
            elif total_gb < 4:
                # 内存小于4GB，适度降低
                if config['resolution'][0] > 1280:
                    config['resolution'] = (1280, 720)
        except:
            pass
    
    return config, device_type


def get_model_path(model_size='nano'):
    """
    根据模型大小获取模型路径
    
    Args:
        model_size: 'nano', 'small', 'medium'
    
    Returns:
        str: 模型文件路径
    """
    model_map = {
        'nano': 'yolov8n.pt',  # 最小模型
        'small': 'yolov8s.pt',
        'medium': 'fire_m.pt',  # 当前使用的模型
    }
    
    model_file = model_map.get(model_size, model_map['nano'])
    
    # 检查文件是否存在（按优先级顺序）
    # 1. 检查 models/ 目录（推荐位置）
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    model_path_in_models = os.path.join(models_dir, model_file)
    if os.path.exists(model_path_in_models):
        return model_path_in_models
    
    # 2. 检查当前目录
    if os.path.exists(model_file):
        return model_file
    
    # 3. 检查 server/ 目录（向后兼容）
    server_path = os.path.join(os.path.dirname(__file__), model_file)
    if os.path.exists(server_path):
        return server_path
    
    # 4. 如果指定模型不存在，尝试其他模型
    for size in ['nano', 'small', 'medium']:
        alt_file = model_map[size]
        # 检查 models/ 目录
        alt_path = os.path.join(models_dir, alt_file)
        if os.path.exists(alt_path):
            logging.warning(f"模型 {model_file} 不存在，使用 {alt_file}")
            return alt_path
        # 检查当前目录
        if os.path.exists(alt_file):
            logging.warning(f"模型 {model_file} 不存在，使用 {alt_file}")
            return alt_file
    
    # 5. 最后尝试默认模型 fire_m.pt
    default_models = ['fire_m.pt', 'yolov8n.pt']
    for default_model in default_models:
        # 检查 models/ 目录
        default_path = os.path.join(models_dir, default_model)
        if os.path.exists(default_path):
            return default_path
        # 检查当前目录
        if os.path.exists(default_model):
            return default_model
        # 检查 server/ 目录
        server_default = os.path.join(os.path.dirname(__file__), default_model)
        if os.path.exists(server_default):
            return server_default
    
    # 所有尝试都失败
    raise FileNotFoundError(
        f"找不到模型文件: {model_file}\n"
        f"请将模型文件放在以下位置之一:\n"
        f"  - {models_dir}/\n"
        f"  - {os.path.dirname(__file__)}/\n"
        f"可用模型: {', '.join(model_map.values())}"
    )


def print_device_info(config, device_type):
    """打印设备信息"""
    logging.info("=" * 60)
    logging.info(f"设备类型: {config['name']} ({device_type})")
    logging.info(f"分辨率: {config['resolution'][0]}x{config['resolution'][1]}")
    logging.info(f"目标帧率: {config['target_fps']} FPS")
    logging.info(f"帧跳跃: 每 {config['frame_skip']} 帧推理一次")
    logging.info(f"JPEG质量: {config['jpeg_quality']}")
    logging.info(f"检测置信度: {config['detection_conf']}")
    logging.info(f"最大线程数: {config['max_threads']}")
    logging.info(f"使用GPU: {config['use_gpu']}")
    logging.info(f"模型大小: {config['model_size']}")
    logging.info("=" * 60)

