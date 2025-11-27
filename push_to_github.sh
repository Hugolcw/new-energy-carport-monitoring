#!/bin/bash
# GitHub推送脚本

echo "========================================"
echo "准备推送到GitHub仓库"
echo "========================================"
echo

# 检查是否在正确的目录
if [ ! -d ".git" ]; then
    echo "初始化Git仓库..."
    git init
fi

# 检查远程仓库
if ! git remote | grep -q "origin"; then
    echo "添加远程仓库..."
    git remote add origin https://github.com/Hugolcw/new-energy-carport-monitoring.git
else
    echo "更新远程仓库URL..."
    git remote set-url origin https://github.com/Hugolcw/new-energy-carport-monitoring.git
fi

echo
echo "添加所有文件..."
git add .

echo
echo "提交更改..."
git commit -m "项目结构优化：重新组织文件结构，添加边缘设备优化版本

- 创建docs目录，分类整理所有文档
- 创建server/scripts目录，集中管理启动脚本
- 创建server/models目录，统一模型文件位置
- 添加边缘设备优化版本(app_edge.py)，支持多平台自动检测
- 更新device_config.py，支持模型文件多路径查找
- 添加完整的部署文档和优化文档
- 更新README，添加项目结构说明"

echo
echo "设置主分支..."
git branch -M main

echo
echo "========================================"
echo "准备推送到远程仓库..."
echo "========================================"
echo
echo "注意: 如果提示需要认证，请使用GitHub Personal Access Token"
echo "获取Token: https://github.com/settings/tokens"
echo
echo "正在推送..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo
    echo "========================================"
    echo "推送成功！"
    echo "查看仓库: https://github.com/Hugolcw/new-energy-carport-monitoring"
    echo "========================================"
else
    echo
    echo "========================================"
    echo "推送失败！可能的原因："
    echo "1. 需要GitHub认证（使用Personal Access Token）"
    echo "2. 远程仓库已有内容，需要先拉取"
    echo "3. 网络连接问题"
    echo
    echo "请查看上面的错误信息，或参考 GIT_PUSH_GUIDE.md"
    echo "========================================"
fi


