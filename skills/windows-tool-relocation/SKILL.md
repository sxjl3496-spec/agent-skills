---
name: windows-tool-relocation
description: >
  将已安装的工具/Agent（npm 全局包、node 程序等）从 C 盘迁移到 D 盘，释放系统盘空间。
  适用场景：(1) 用户 C 盘空间不足、要求"非必要不装 C 盘"；(2) 迁移 OpenClaw/Claude Code/OpenCode
  等 npm 安装的 CLI 工具；(3) D 盘已有完整副本、C 盘只有冗余 npm 全局副本时的清理。
  核心：验证 D 盘副本完整性 → 重写 npm wrapper（.cmd + bash 双版本）→ 重启长驻进程 → 删 C 盘冗余 → 实测验证。
---

# Windows 工具 C 盘 → D 盘迁移

## 触发条件

- 用户说"C盘内存不够"、"不希望非必要在C盘运行的东西装在C盘"
- 工具安装位置偏好：`<知识库根目录>\\` 下，与 `Hermesagent/`、`OpenClaw/` 并列的**独立文件夹**
- 每个 Agent 必须有自己独立的文件夹（`ClaudeCode/`、`OpenCode/`、`OpenClaw/` 并列），**不要**多个工具混在一个共享目录（如曾出现的 `OpenCodeAgent/`，用户明确纠正过）

## 前置检查（先看是否已迁移过）

1. 查 D 盘现有目录：`ls <知识库根目录>/` — 往往已有完整副本（`app/node_modules/...`）
2. 对比版本：C 盘与 D 盘 package.json 的 version 是否一致
3. 查 C 盘 npm 全局实际残留：`du -sh ~/AppData/Roaming/npm/node_modules/*`
4. 看 wrapper 是否已被改写（`cat ~/AppData/Roaming/npm/<tool>.cmd`，注释里的日期可判断是否迁移过）
5. 注意：Claude/OpenCode 曾出现"C 盘已删、wrapper 已指向 D 盘但被误以为没迁"的情况——先查再动

## 迁移流程

1. **确认 D 盘副本自包含**：包自带 node_modules（claude-code 19M、opencode-ai 283M、openclaw 362M），不依赖顶层共享。检查：`ls <D>/app/node_modules/<pkg>/node_modules/ | wc -l` + package.json 的 deps
2. **重写 npm wrapper**（`%APPDATA%\npm\` 下，每个工具两个文件）：
   - `.cmd` 版（AionUi 和 Windows 原生调用）：直接 `node "D:\...\cli.js" %*`
   - bash 版（无扩展名，Git Bash 调用）：`exec node "D:/..." "$@"`
3. **重启长驻进程**：gateway 等已加载旧代码的进程必须 kill + 重启（kill 后先确认端口已清空再拉起）
4. **删 C 盘冗余包**：`rm -rf ~/AppData/Roaming/npm/node_modules/<pkg>`
5. **清理 npm 缓存**：`npm cache clean --force`（或删 `~/AppData/Local/npm-cache`，常可省 1.5G）
6. **实测**：版本命令 + 真实对话测试（`echo 消息 | <tool> ...`）+ AionUi health-check

## 路径格式陷阱（重点，踩过两次）

- node.exe 是 Windows 程序：bash wrapper 写 MSYS 路径 `<知识库根目录>/...` 会被 node 解析成 `C:\d\BaiduSyncdisk\...` → MODULE_NOT_FOUND
- bash wrapper 写 `D:\...` 反斜杠会被 sh 转义吞掉
- ✅ bash wrapper 正确写法：**正斜杠** `<知识库根目录>/...`
- ✅ .cmd wrapper 正确写法：反斜杠 `<知识库根目录>\\...`
- `openclaw agent --message-file /tmp/xxx` 会把 `/tmp` 解析成 `C:\tmp` → 传 `C:\Users\...` 绝对路径

## Windows 命令陷阱

- `taskkill` 在 git bash 下：`MSYS_NO_PATHCONV=1 taskkill /F /PID <pid>`（`//F` 会报"无效参数/选项"）
- `schtasks /create` 普通用户被拒（拒绝访问）→ 自启用改用注册表 Run 键（免管理员）：
  ```
  reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v <Name> /t REG_SZ /d "wscript.exe \"D:\...\autostart.vbs\"" /f
  ```
- VBS 静默启动（无控制台窗口）：`WshShell.Run """...\tool.cmd"" gateway", 0, False`

## 自启与持久化

- VBS + 注册表 Run 键：登录自动拉起，免管理员，适用于 gateway 等需要常驻的服务
- 验证进程独立性：`wmic process where "ProcessId=<pid>" get ParentProcessId` 追父进程链，确认不挂在 Hermes 终端会话下（wscript 异步拉起后自行退出，服务进程由 cmd 直接持有——这样终端关闭也不掉）
- AionUi 的 agent 状态检查是**手动触发**（界面 Test Connection），不是自动轮询；用 `POST http://127.0.0.1:<port>/api/agents/<id>/health-check` 可远程刷新，数据库 `agent_metadata.last_check_status` 确认结果

## 验证清单

- [ ] `openclaw --version` / `claude --version` / `opencode --version` 正常
- [ ] 真实对话测试通过（版本命令不够，必须实测对话）
- [ ] `du -sh ~/AppData/Roaming/npm` 大幅下降
- [ ] AionUi health-check → online（数据库 last_check_status）
- [ ] 长驻进程（gateway）重启后确认由 D 盘代码运行（wmic 看 CommandLine）

## 参考实例（2026-08-06）

- `<OpenClaw目录>\` — openclaw（app/node_modules + node 运行时）
- `<知识库根目录>\\ClaudeCode\app\node_modules\@anthropic-ai\claude-code\`
- `<知识库根目录>\\OpenCode\app\node_modules\` — opencode-ai + oh-my-opencode + @electron/asar
- 自启 VBS 实例：`hermes-data\scripts\openclaw-gateway-autostart.vbs`
