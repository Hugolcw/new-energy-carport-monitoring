# Git 推送指南

## 📋 当前状态

代码已经准备好推送到GitHub，但可能需要身份验证。

## 🚀 推送步骤

### 方式1: 使用HTTPS（推荐）

```bash
cd new-energy-carport-monitoring

# 检查远程仓库配置
git remote -v

# 如果还没有设置，添加远程仓库
git remote add origin https://github.com/Hugolcw/new-energy-carport-monitoring.git

# 推送代码
git push -u origin main
```

**注意**: 如果提示需要认证，GitHub现在要求使用Personal Access Token (PAT)而不是密码。

### 方式2: 使用SSH

```bash
# 如果已配置SSH密钥
git remote set-url origin git@github.com:Hugolcw/new-energy-carport-monitoring.git
git push -u origin main
```

## 🔐 GitHub认证设置

### 创建Personal Access Token

1. 访问: https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限: 至少需要 `repo` 权限
4. 生成并复制token

### 使用Token推送

```bash
# 推送时会提示输入用户名和密码
# 用户名: 你的GitHub用户名
# 密码: 使用刚才生成的Personal Access Token
git push -u origin main
```

## 📝 如果仓库已存在

如果远程仓库已经有内容，可能需要先拉取：

```bash
# 拉取远程内容（如果有）
git pull origin main --allow-unrelated-histories

# 解决可能的冲突后，再推送
git push -u origin main
```

## ✅ 验证推送

推送成功后，访问以下URL查看：
https://github.com/Hugolcw/new-energy-carport-monitoring

## 🎯 推送的文件

本次推送包含：

- ✅ 优化后的项目结构
- ✅ 边缘设备优化版本 (`app_edge.py`)
- ✅ 完整的文档 (`docs/`)
- ✅ 启动脚本 (`server/scripts/`)
- ✅ 项目结构说明文档
- ✅ 更新的README

## ⚠️ 注意事项

1. **模型文件**: `.pt` 文件可能很大，如果超过100MB，考虑使用Git LFS
2. **node_modules**: 已在 `.gitignore` 中排除
3. **敏感信息**: 确保没有提交 `.env` 等敏感文件

---

**提示**: 如果遇到问题，可以查看Git错误信息或联系GitHub支持。


