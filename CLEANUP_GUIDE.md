# 项目清理指南

## 📋 需要清理的文件

项目结构优化后，以下文件可以删除或移动到合适位置：

### 1. 重复的文档文件（server目录下）

以下文件已移动到 `docs/` 目录，可以删除：

```bash
server/COMPATIBILITY_CHECK.md          # → docs/compatibility/
server/COMPATIBILITY_FIXES.md          # → docs/compatibility/
server/EDGE_DEPLOYMENT.md              # → docs/deployment/
server/PLATFORM_OPTIMIZATION_SUMMARY.md # → docs/deployment/
server/OPTIMIZATION_ANALYSIS.md        # → docs/optimization/
```

### 2. 重复的启动脚本（server目录下）

以下文件已移动到 `server/scripts/` 目录，可以删除：

```bash
server/start_auto.sh
server/start_raspberry_pi.sh
server/start_jetson.sh
server/start_hisilicon.sh
```

### 3. 重复的README文件（根目录）

以下文件可以删除或合并：

```bash
README_GENERATED.md  # 内容已合并到 README.md
README1.md           # 内容已合并到 README.md
README.md.bak        # 备份文件，可删除
```

### 4. 模型文件位置（建议移动）

建议将模型文件移动到 `server/models/` 目录：

```bash
# 根目录下的模型文件
yolov8n.pt  # → server/models/

# server目录下的模型文件（如果存在）
server/fire_m.pt  # → server/models/
server/fire.pt    # → server/models/
```

## 🧹 清理命令（Linux/Mac）

```bash
cd new-energy-carport-monitoring

# 删除重复的文档文件
rm server/COMPATIBILITY_CHECK.md
rm server/COMPATIBILITY_FIXES.md
rm server/EDGE_DEPLOYMENT.md
rm server/PLATFORM_OPTIMIZATION_SUMMARY.md
rm server/OPTIMIZATION_ANALYSIS.md

# 删除重复的启动脚本
rm server/start_auto.sh
rm server/start_raspberry_pi.sh
rm server/start_jetson.sh
rm server/start_hisilicon.sh

# 删除重复的README文件
rm README_GENERATED.md
rm README1.md
rm README.md.bak

# 移动模型文件（如果存在）
mkdir -p server/models
mv yolov8n.pt server/models/ 2>/dev/null || true
mv server/*.pt server/models/ 2>/dev/null || true
```

## 🧹 清理命令（Windows PowerShell）

```powershell
cd new-energy-carport-monitoring

# 删除重复的文档文件
Remove-Item server\COMPATIBILITY_CHECK.md -ErrorAction SilentlyContinue
Remove-Item server\COMPATIBILITY_FIXES.md -ErrorAction SilentlyContinue
Remove-Item server\EDGE_DEPLOYMENT.md -ErrorAction SilentlyContinue
Remove-Item server\PLATFORM_OPTIMIZATION_SUMMARY.md -ErrorAction SilentlyContinue
Remove-Item server\OPTIMIZATION_ANALYSIS.md -ErrorAction SilentlyContinue

# 删除重复的启动脚本
Remove-Item server\start_auto.sh -ErrorAction SilentlyContinue
Remove-Item server\start_raspberry_pi.sh -ErrorAction SilentlyContinue
Remove-Item server\start_jetson.sh -ErrorAction SilentlyContinue
Remove-Item server\start_hisilicon.sh -ErrorAction SilentlyContinue

# 删除重复的README文件
Remove-Item README_GENERATED.md -ErrorAction SilentlyContinue
Remove-Item README1.md -ErrorAction SilentlyContinue
Remove-Item README.md.bak -ErrorAction SilentlyContinue

# 移动模型文件（如果存在）
New-Item -ItemType Directory -Force -Path server\models | Out-Null
Move-Item yolov8n.pt server\models\ -ErrorAction SilentlyContinue
Get-ChildItem server\*.pt -ErrorAction SilentlyContinue | Move-Item -Destination server\models\ -ErrorAction SilentlyContinue
```

## ✅ 清理后的结构

清理完成后，项目结构应该是：

```
new-energy-carport-monitoring/
├── README.md                    # 主文档
├── PROJECT_STRUCTURE.md
├── REORGANIZATION_SUMMARY.md
├── CLEANUP_GUIDE.md            # 本文档
│
├── docs/                        # 所有文档
│   ├── deployment/
│   ├── optimization/
│   └── compatibility/
│
├── server/
│   ├── app*.py
│   ├── device_config.py
│   ├── models/                  # 模型文件
│   └── scripts/                 # 启动脚本
│
└── src/                         # 前端
```

## ⚠️ 注意事项

1. **备份**: 清理前建议先备份整个项目
2. **模型文件**: 模型文件移动后，系统会自动查找新位置（已更新路径逻辑）
3. **Git**: 如果使用Git，删除文件后记得提交更改

## 🎯 验证清理

清理后，检查以下内容：

- ✅ `server/` 目录下没有 `.md` 文件（除了可能的环境说明）
- ✅ `server/` 目录下没有 `start_*.sh` 文件
- ✅ 根目录下只有一个 `README.md` 文件
- ✅ 所有模型文件都在 `server/models/` 目录

---

**提示**: 如果不确定某个文件是否可以删除，可以先移动到备份目录。


