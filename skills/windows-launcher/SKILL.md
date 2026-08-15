---
name: windows-launcher
description: >
  Creating reliable Windows desktop shortcuts and launchers for CLI tools (Hermes, etc.).
  Covers WScript.Shell encoding pitfalls, PowerShell SxS errors, TERM variable
  inheritance, and Defender false-positive workarounds. Trigger when the user needs
  a double-clickable desktop icon for any CLI tool on Windows.
---

# Windows Desktop Launcher

## When to use

User asks to create a desktop shortcut / icon / launcher for a CLI tool on Windows,
or a previously working shortcut stopped working.

## Core workflow

1. **Diagnose first** — don't create files blindly. Check:
   - Is the target executable accessible from the Desktop context? Test with `cmd //c "tool --version"`
   - Is Windows Defender active? `Get-Service WinDefend`
   - Is TERM set in the environment? `echo %TERM%`
   - Is OneDrive syncing Desktop?

2. **Choose the right architecture:**
   ```
   .lnk → cmd.exe (inline args)  (BEST — no intermediate files, no encoding risk)
   .lnk → .cmd → tool.exe         (OK — for complex multi-line scripts)
   .lnk → tool.exe                (only if tool has no env requirements)
   .lnk → .vbs → tool.exe         (AVOID — Defender kills .vbs files)
   ```

   The inline-args pattern is simplest and most reliable:
   ```
   TargetPath: C:\Windows\System32\cmd.exe
   Arguments:  /c set TERM=&& set ENV_VAR=...&& C:\path\to\tool.exe
   WorkDir:    C:\Users\<user>
   ```

3. **Use pure ASCII filenames and paths** — see `references/encoding-pitfall.md`

4. **Clear TERM in the launcher** — see `references/term-inheritance.md`

5. **Verify** — read back the .lnk TargetPath to confirm it's not garbled

## .cmd template

```cmd
@echo off
set TERM=
set HERMES_HOME=D:\path\to\hermes-data
"D:\path\to\tool.exe"
```

## 后台守护进程开机自启（免管理员）⭐

CLI 工具的常驻进程（如 OpenClaw gateway）要开机自启且**不弹控制台窗口**时的方案：

1. **schtasks 会被拒**：`schtasks /create /tn X /tr "..." /sc onlogon /f` 普通用户
   报"拒绝访问"（onlogon 任务需管理员）——不要走这条路
2. **正确方案：VBS 静默启动器 + HKCU Run 键**（免管理员、登录即生效）：
   ```vbs
   Set WshShell = CreateObject("WScript.Shell")
   WshShell.Run """C:\...\tool.cmd"" daemon", 0, False   ' 0=隐藏窗口, False=不等待
   ```
   ```bash
   reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v <Name> \
     /t REG_SZ /d "wscript.exe \"D:\...\autostart.vbs\"" /f
   ```
3. **验证自启脚本本身**（不能只验证手动启动）：杀现有进程 → `wscript.exe <vbs>` →
   sleep 35 → netstat 确认新 PID 监听
4. **进程独立性验证**：`wmic process where "ProcessId=<pid>" get ParentProcessId`
   逐级上查，确认顶层是 wscript/cmd 而非 Hermes 终端的 bash（否则会随会话结束而死）
5. **taskkill 在 Git Bash 的坑**：`//F` 会被 MSYS 转义报"无效参数/选项"，
   必须用 `MSYS_NO_PATHCONV=1 taskkill /F /PID <pid>` 或单斜杠写法

## npm 全局包 C→D 盘迁移（释放 C 盘空间）

当 C 盘 npm 全局目录（`~/AppData/Roaming/npm/node_modules/`）过大、需要把某个 CLI 工具包（claude-code、opencode-ai 等）搬到 D 盘时使用。完整步骤见 `references/npm-global-migration.md`。核心要点：

0. **目录布局（用户明确要求，2026.8.6 纠正）**：每个 agent 独立文件夹，并列在 `<知识库根目录>\\` 下（`ClaudeCode\` / `OpenCode\` / `OpenClaw\` / `Hermesagent\`），包放 `D:\...\<AgentName>\app\node_modules\<pkg>`。**禁止把多个 agent 合并进一个目录**（曾用 OpenCodeAgent 合并 Claude+OpenCode，被用户纠正拆分）；合并目录里的包自包含（claude-code 自带 node_modules、opencode-ai 自带二进制），拆开互不影响
1. **复制而非移动**：`cp -r` 包到上述 D 盘目标目录（如 `D:\...\ClaudeCode\app\node_modules\@anthropic-ai\claude-code`），保持原有 node_modules 内部结构
2. **必须改两个 wrapper**：`.cmd`（Windows/`cmd.exe` 调用方用）和 bash 无扩展名版（Git Bash 用），都改为硬编码 D 盘绝对路径
3. **⚠️ MSYS 路径陷阱**：bash wrapper 里 `exec node "/d/..."` 会被 node 当成 `C:\d\...` 报 Cannot find module —— 必须用 `D:/...`（正斜杠 Windows 路径）
4. **包内不一定有 node.exe**：先 `ls <pkg>/node.exe` 确认，没有就用系统 `node` 而非包内 node
5. **验证顺序（关键）**：先直接 `node "D:/.../cli.js" --version` 测 D 盘副本 → 再测 wrapper（bash+.cmd）→ **删 C 盘包后必须复测**（确认无 C 盘依赖）→ 真实对话测试（`claude -p "..."` / `opencode run "..."`）而非只测 --version
6. **gateway/守护进程残留陷阱**：如果该工具有常驻 gateway 进程（如 OpenClaw），且进程在删包前启动，其命令行仍指向 C 盘旧路径 —— 必须 `taskkill /F /PID` 杀掉后用 D 盘副本重启，否则运行时按需加载模块报 `Cannot find module`（`wmic process where "ProcessId=X" get CommandLine` 可验证进程实际用的路径）
7. **清理 npm-cache**：`npm cache clean --force` 后可能仍有残留（121M），直接 `rm -rf "C:/Users/<user>/AppData/Local/npm-cache/"*` 清到 0（npm 需要时会重建）
8. 用户配置（`~/.claude/`、`~/.config/opencode/` 等）都在用户目录，搬包不影响配置
9. **AionUi 调用链洞察（迁移安全的关键）**：AionUi 的 agent 槽位通过 **PATH wrapper 间接调用**（Claude Code 走 `binary_name: claude`、OpenCode 走 `command: opencode`，见 AionUi 数据库 agent_metadata 表），**没有硬编码 C 盘路径** —— 只要改 wrapper 指向 D 盘，AionUi 无需任何改动、连接不受影响。迁移后验证 AionUi 侧状态：`POST /api/agents/{id}/health-check`（见 `references/aionui-agent-healthcheck.md`）
10. **拆分已合并目录**：若发现多个 agent 被合并在一个目录（如 OpenCodeAgent），按"自包含包移动到各自独立文件夹 → 更新全部 wrapper → 删空壳目录 → 复测 --version + 真实对话 + 查进程 CommandLine 无旧路径残留"执行；拆分后 AionUi 调用链不变（仍走 wrapper）

## AionUi agent 连接运维

AionUi 中外部 agent 槽位（OpenClaw/Claude Code/OpenCode/Hermes）的状态检查是**手动触发**的（health-check API），不是自动轮询。gateway 重启或电脑重启后，AionUi 里的状态可能残留 offline，需要主动刷新。完整排查流程见 `references/aionui-agent-healthcheck.md`。核心：`POST http://127.0.0.1:<aioncore端口>/api/agents/<agent_id>/health-check` → 查数据库 `agent_metadata.last_check_status` 确认 online；aioncore 端口是动态的，用 `netstat -ano | grep <aioncore PID>` 找。**AionUi 未运行时 health-check 返回 502 属正常**，不代表连接坏了。

## Key pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Chinese filename in .lnk TargetPath | Double-click does nothing, no error; terminal tests may pass! | Use ASCII-only filenames or inline-args pattern; always read-back TargetPath to verify |
| Terminal verification misses .lnk bugs | `start` / `cmd //c` test passes, but Explorer double-click fails | Mandatory: read back TargetPath with WScript.Shell after creation |
| .lnk targets powershell.exe directly | SxS error popup ("并行配置不正确") | Use inline-args cmd.exe pattern, never target powershell.exe directly |
| TERM=xterm-256color inherited | NoConsoleScreenBufferError, tool crashes | `set TERM=` in .cmd before calling tool |
| Files on Desktop disappear | .lnk/.vbs gone after creation | Move .cmd to user home; Desktop may have sync/cleanup tools |
| .vbs files deleted | File vanishes immediately | Don't use .vbs; Windows Defender or antimalware kills them |

## References

- `references/encoding-pitfall.md` — WScript.Shell Chinese encoding corruption
- `references/sxs-error.md` — PowerShell Side-by-Side configuration error
- `references/term-inheritance.md` — TERM variable inheritance from Git Bash
- `references/npm-global-migration.md` — npm 全局包 C→D 盘迁移完整流程（复制→双wrapper→MSYS路径陷阱→删包复测→gateway残留陷阱→清cache）
- `references/aionui-agent-healthcheck.md` — AionUi agent 连接运维（手动 health-check 刷新、动态端口发现、数据库状态验证、502=AionUi未运行、gateway 重启后的残留状态清理）

## Templates

- `templates/hermes-launcher.cmd` — proven working .cmd launcher (copy to Desktop or user home)
