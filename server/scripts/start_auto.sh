#!/bin/bash
# 自动检测设备类型启动脚本

cd "$(dirname "$0")/.." || exit 1
echo "自动检测设备类型..."
python3 app_edge.py

