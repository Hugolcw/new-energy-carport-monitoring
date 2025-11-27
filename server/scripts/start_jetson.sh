#!/bin/bash
# Jetson设备启动脚本

cd "$(dirname "$0")/.." || exit 1
echo "检测Jetson设备类型..."
if [ -f /proc/device-tree/model ]; then
    MODEL=$(cat /proc/device-tree/model | tr -d '\0')
    echo "检测到设备: $MODEL"
    
    if echo "$MODEL" | grep -qi "nano"; then
        DEVICE_TYPE="jetson_nano"
    elif echo "$MODEL" | grep -qi "xavier\|orin"; then
        DEVICE_TYPE="jetson_xavier"
    else
        DEVICE_TYPE="jetson_nano"
    fi
else
    DEVICE_TYPE="jetson_nano"
fi

echo "使用设备配置: $DEVICE_TYPE"
export DEVICE_TYPE=$DEVICE_TYPE
python3 app_edge.py $DEVICE_TYPE


