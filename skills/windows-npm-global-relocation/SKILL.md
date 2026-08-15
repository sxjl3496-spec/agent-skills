---
name: windows-npm-global-relocation
description: >
  将 Windows 上 npm 全局安装的命令行工具（claude、opencode、openclaw 等）从 C 盘迁移到 D 盘，
  释放 C 盘空间。当用户说"C 盘内存不够"、"程序装在 C 盘要搬走"、"npm 全局包迁移"时触发。
  包含 wrapper 改写（.cmd + bash 双版）、MSYS 路径坑、依赖归属判断、AionUi 间接调用、实测验证流程。
---

# Windows npm 全局工具跨盘迁移

## 触发场景
- 用户抱怨 C 盘空间不足，npm 全局安装的工具占用大（claude、opencode、openclaw 等，每个 300M-700M）
- 用户要求把命令行工具从 C 盘搬到 D 盘，且强调"非必要不装 C 盘"
- 本机已完成：OpenClaw、Claude Code、OpenCode 三例，可直接参照

## 核心原理
npm 全局包位于 `C:\Users\<user>\AppData\Roaming\npm\node_modules\<pkg>`，命令入口是：
- `C:\Users\<user>\AppData\Roaming\npm\<name>.cmd`（Windows 批处理，AionUi 和 cmd 用这个）
- `C:\Users\<user>\AppData\Roaming\npm\<name>`（无扩展名 bash wrapper，Git Bash 用这个）

迁移 = 移动包本体到 D 盘 + 改写两个 wrapper 指向新位置。**wrapper 文件本身留在 C 盘**（PATH 已含该目录，只改内容）。

## 步骤

### 1. 勘察现状
```bash
npm config get prefix            # 全局目录（通常 C:\Users\xxx\AppData\Roaming\npm）
npm root -g                      # node_modules 路径
du -sh ~/AppData/Roaming/npm/node_modules/*   # 各包大小，找出大头
ls ~/AppData/Roaming/npm/        # wrapper 文件清单（.cmd 版 + 无扩展名 bash 版）
```

### 2. 确认目标包自包含（决定能否独立搬迁）
```bash
# 检查包内部 node_modules 依赖是否完整
ls <pkg>/node_modules | wc -l
# package.json 的 dependencies 为空（deps=0）或全部依赖都在包内部 node_modules = 可独立搬迁
```
**scope 包注意**：`@anthropic-ai/claude-code` 这类要连 `@anthropic-ai` scope 目录一起搬。
**npm 临时目录**：原 node_modules 下可能有 `.pkg-xxx`（npm 安装残留临时目录），确认无关后随目录删除。

### 3. 移动包到 D 盘（遵循用户的目录偏好 ⭐）
```bash
mkdir -p <知识库根目录>/<ToolName>/app/node_modules
mv C盘node_modules/<pkg> D盘目标路径
```
**用户的目录偏好（2026.8.6 明确纠正）**：
- 每个工具必须**独立文件夹并列存放**，不要多个工具挤在一个文件夹（曾把 Claude Code 和 OpenCode 都放 OpenCodeAgent 里被用户纠正）
- 结构参照：`AIKnowledgeBase/` 下 `ClaudeCode/`、`OpenCode/`、`OpenClaw/`、`Hermesagent/` 并列
- 每个工具内部结构统一为 `<Tool>/app/node_modules/<pkg>`（与 OpenClaw 一致）
- 工具的插件跟主工具走（oh-my-opencode 是 OpenCode 插件 → 放 OpenCode 下）；独立工具单独处理（@electron/asar 是打包工具，不属于任何 agent，可跟主工具放一起但标注用途）

### 4. 改写 wrapper（关键步骤，两个都要改）
`.cmd` 版（`C:\Users\<user>\AppData\Roaming\npm\<name>.cmd`）：
```cmd
@ECHO off
REM 注释：指向 D 盘副本 + 日期
node "<知识库根目录>\\<Tool>\app\node_modules\<pkg>\<entry>" %*
```

bash 版（`C:\Users\<user>\AppData\Roaming\npm\<name>`，无扩展名）：
```sh
#!/bin/sh
exec node "<知识库根目录>/<Tool>/app/node_modules/<pkg>/<entry>" "$@"
```

**关联 wrapper 一起改**：如果工具带插件（如 oh-my-opencode）或配套工具（如 asar），其 wrapper 也要指向新位置，否则插件命令失效。

### 5. 验证（必须实测，不能只看 --version）⭐
```bash
<tool> --version                      # 版本
echo "请只回复:测试通过" | claude -p --model sonnet    # Claude Code 真实对话
echo "请只回复:测试通过" | opencode run                # OpenCode 真实对话
```
工具类验证：`asar --version` 等。

### 6. 删除 C 盘原包 + 清缓存
```bash
rm -rf ~/AppData/Roaming/npm/node_modules/<pkg>
npm cache clean --force   # 或直接删 ~/AppData/Local/npm-cache（本机曾达 1.5G）
```

## 陷阱

### 陷阱1：MSYS 路径转义（node.exe 是 Windows 程序）⭐
bash wrapper 中：
```sh
# ❌ exec node "<知识库根目录>/..."    # MSYS 路径，node.exe 不认（报 C:\d\...）
# ❌ exec node "<知识库根目录>\\..."    # \ 被 shell 当转义符
# ✅ exec node "<知识库根目录>/..." "$@"   # 正斜杠 Windows 路径
```
`.cmd` 版里用 `D:\...` 反斜杠没问题（批处理不转义）。

### 陷阱2：只改 .cmd 不改 bash wrapper
AionUi 用 .cmd（Windows 批处理），Git Bash 终端用无扩展名 wrapper。**两者都要改**，只改一个会导致另一侧失效。

### 陷阱3：AionUi 无需改动配置
AionUi 通过 PATH 解析命令名（agent_metadata 的 `binary_name: claude` / `command: opencode` 字段）间接调用 wrapper。改 wrapper 内容即生效，**不需要**改 AionUi 数据库或配置。验证方法：查 agent_metadata 确认 command/command_override 无硬编码 C 盘路径。

### 陷阱4：迁移后验证进程用的是新路径
用 `wmic process where "name='node.exe'" get ProcessId,CommandLine` 确认运行中进程的 ExecutablePath/CommandLine 指向 D 盘，而不是旧 C 盘路径残留（旧进程可能还挂着）。

## 验证清单
- [ ] `<tool> --version` 正常（.cmd 和 bash 两个入口都测）
- [ ] 真实对话测试通过（不只 --version）
- [ ] C 盘 npm 全局变小（du 对比迁移前后）
- [ ] 关联插件（oh-my-opencode 等）路径已更新且可运行
- [ ] 若涉及 AionUi：health-check 刷新确认 online

## 本机迁移记录（2026-08-06）
| 工具 | D 盘位置 | 入口文件 |
|------|---------|---------|
| OpenClaw | `OpenClaw\app\node_modules\openclaw\openclaw.mjs` | openclaw.cmd + openclaw |
| Claude Code | `ClaudeCode\app\node_modules\@anthropic-ai\claude-code\cli.js` | claude.cmd + claude |
| OpenCode | `OpenCode\app\node_modules\opencode-ai\bin\opencode` | opencode.cmd + opencode |
| oh-my-opencode | `OpenCode\app\node_modules\oh-my-opencode\...` | oh-my-opencode |
| asar | `OpenCode\app\node_modules\@electron\asar\...` | asar.cmd + asar |

结果：C 盘 npm 全局 1.2G → 45M（剩 @volcengine + pnpm 两个小工具），npm-cache 1.5G 已清空。所有 agent 实测对话正常，AionUi 连接不受影响。
