#!/bin/bash
# 树莓派启动脚本

cd "$(dirname "$0")/.." || exit 1
echo "启动树莓派优化版本..."
export DEVICE_TYPE=raspberry_pi
python3 app_edge.py raspberry_pi


