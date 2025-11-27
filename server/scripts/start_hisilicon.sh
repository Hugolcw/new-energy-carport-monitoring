#!/bin/bash
# 海思芯片启动脚本

cd "$(dirname "$0")/.." || exit 1
echo "启动海思芯片优化版本..."
export DEVICE_TYPE=hisilicon
python3 app_edge.py hisilicon


