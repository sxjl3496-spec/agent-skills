---
name: multi-agent-collaboration
description: >
  多 Agent 能力边界与协作路由。当用户需要的任务超出 Hermes Agent 能力边界时，
  主动建议切换到其他本机 Agent（OpenWorker/Claude Code/OpenCode/OpenClaw）。
  覆盖：能力对照、场景路由决策、多 Agent 协作方式、Hermes 调用其他 CLI Agent 的命令。
  触发条件：(1) 用户问"XX能不能做"涉及其他 Agent 能力时，
  (2) Hermes 遇到自身无法完成的任务时主动触发，
  (3) 用户要求对比 Agent 能力时，
  (4) 用户提到 OpenWorker/Claude Code/OpenCode/OpenClaw 时。
---

# 多 Agent 协作路由

## 核心原则

当 Hermes Agent 遇到自身无法完成的任务时，**主动告知用户**可用的替代 Agent，而不是沉默失败或勉强用不擅长的方式处理。

## 本机 Agent 清单

| Agent | 形态 | 模型 | 启动方式 | 安装位置 |
|-------|------|------|---------|---------|
| Hermes Agent | CLI | glm-5.2（火山方舟） | `hermes` 命令 | <知识库根目录>\\Hermesagent\ |
| OpenWorker | 桌面 GUI | BYO（12+厂商+Ollama） | 桌面双击 / openworker-desktop.exe | <AI软件目录>\OpenWorker\ |
| Claude Code | CLI | Claude（Anthropic） | `claude.cmd --print` | npm 全局 @anthropic-ai/claude-code |
| OpenCode | CLI | BYO | `opencode.cmd run` | npm 全局 opencode-ai |
| OpenClaw | CLI | BYO | `openclaw.cmd agent` | npm 全局 openclaw |

## 场景路由规则

### Hermes 做不了 → 主动建议 OpenWorker

| 场景 | 为什么 Hermes 做不了 | OpenWorker 能力 |
|------|---------------------|----------------|
| Slack @mention 触发 | 无 Slack 连接器 | Slack 连接器，@OpenWorker 触发桌面端任务 |
| Jira/Linear/Notion/HubSpot | 无项目管理集成 | 25+ 业务应用连接器 |
| Google Calendar 管理 | 无日历集成 | Calendar 连接器 |
| Gmail/Outlook 邮件 | 无邮件集成 | 邮件连接器 |
| 浏览器自动化 | 无 Playwright | Playwright 集成 |
| 语音输入 | 无 STT | Rust STT sidecar |
| 无人值守审批 | 同步审批阻塞 | Inbox 异步审批队列（跨会话持久化） |
| 需要 GUI 可视化 | 纯 CLI | Tauri + React 桌面应用 |
| MCP 协议工具 | 无 MCP 客户端 | MCP 客户端，per-tool 控制 |

### Hermes 独占场景（不需要建议切换）

- Obsidian 知识库读写（唯一直接读写 Vault 的 Agent）
- /plan 任务规划 + 双模型验证 + 出口检验
- 飞书 API 集成（发文件/消息）
- 学术写作/科研申报技能链（academic 技能组）
- 个人商业项目经营咨询
- 三层模型降级链（Coding Plan → 免费千问 → 按量付费）
- cron 定时任务（no_agent 脚本模式）
- Telegram/Discord 多平台消息
- 图片生成（DashScope qwen-image）
- TTS 语音输出

### 需要深度推理 → Hermes 调用 Claude Code

Claude Code 可通过 terminal 非交互调用：

```bash
# 基本调用（短 prompt）
claude.cmd --allowedTools "Read,WebSearch,WebFetch,Write" --print "分析任务"

# 长 prompt 写入文件让 Claude 自己读（避免参数截断）
echo "你的长 prompt" > /tmp/task.txt
claude.cmd --allowedTools "Read,WebSearch,WebFetch,Write" --print "读取 /tmp/task.txt 并执行"
```

### 其他 CLI Agent 调用

```bash
# OpenCode（需 cd 到工作目录，自动拒读外部目录）
opencode.cmd run --model volcano/glm-5.2 "任务描述"

# OpenClaw 非交互单次调用（长消息用 --message-file，tools.profile 须设 "full"）
openclaw.cmd agent --local --agent main --message-file msg.txt

# OpenClaw 交互式 TUI（用户自己操作终端时）
openclaw.cmd chat --local
# 等价别名：openclaw.cmd tui --local
```

## OpenClaw 使用与配置

### 两种运行模式

| 模式 | 命令 | Gateway 要求 | 适用场景 |
|------|------|-------------|---------|
| 本地嵌入模式 | `openclaw chat --local` 或 `openclaw agent --local` | 不需要 | 单独使用、终端交互、单次 agent 调用 |
| Gateway 模式 | `openclaw chat` 或 `openclaw agent` | 需要运行 Gateway | AionUi 集成、ACP 桥接、多设备配对 |

关键区别：`--local` 标志让 OpenClaw 走本地 embedded runtime，直接调用模型 API，不需要 Gateway 进程。不加 `--local` 时需要 Gateway 在 `127.0.0.1:18789` 监听。

### 交互式 TUI 模式

用户自己在终端中使用 OpenClaw 时：

```bash
# 在 Git Bash 中（需先在 .bashrc 中配置 PATH）
openclaw chat --local

# 在 PowerShell 中（需先在 PowerShell profile 中添加函数）
openclaw chat --local
```

`chat` 和 `tui` 是同一个命令的别名，都打开终端 UI。

### Gateway 配置与 AionUi 集成

AionUi 通过 ACP（Agent Client Protocol）连接 OpenClaw，**需要 Gateway 运行**。Gateway 不会自动启动，需要手动安装和启动：

**第一步：安装为开机自启服务**
```bash
openclaw daemon install
```

**第二步：启动 Gateway**
```bash
openclaw daemon start
# 或前台运行（调试用）：
openclaw gateway
```

**第三步：验证**
```bash
openclaw daemon status    # 检查服务状态和端口监听
openclaw health           # 检查 Gateway 连通性
```

Gateway 配置在 `~/.openclaw/openclaw.json` 中：
- `gateway.mode: "local"` + `gateway.bind: "loopback"` = 仅本机可连（127.0.0.1:18789）
- `gateway.auth.token` = ACP 连接需要此 token 认证（loopback 模式下明文可接受，见安全加固章节）

### 安全加固（实战修订）⭐

首次配置 OpenClaw 后需要完成安全加固。`openclaw doctor` 会报 3 个安全问题，但实际操作中需注意 Windows 环境的陷阱：

1. **明文密钥 -> SecretRef（Windows 上有陷阱）**：
   - 理论上应将 `gateway.auth.token` 和 `models.providers.<name>.apiKey` 改为 env 引用（`{"source":"env","provider":"openclaw","id":"..."}`），环境变量写入 `~/.bashrc`
   - **Windows 陷阱**：SecretRef 需要 env var 在系统级别可见（注册表 HKEY_CURRENT_USER\Environment）。但 `setx`、PowerShell `SetEnvironmentVariable`、Python `winreg` 都可能被权限拒绝。即使 `.bashrc` 中有 env var，Gateway 进程（通过 `cmd.exe` 启动）不读 `.bashrc`，导致报错 `Secret provider "openclaw" is not configured`，Gateway 启动失败
   - **实际方案**：在 `bind: loopback`（仅 127.0.0.1）+ token 认证 + ownerAllowFrom 的多层防护下，保留明文密钥是可接受的安全折衷。安全审计仍为 0 critical

2. **Command owner**：`commands.ownerAllowFrom` 设为 `["cli:ACP"]`
   - **不要过度禁用特权命令**：`/config`、`/bash`、`/mcp`、`/plugins`、`/debug` 等命令本身需要 owner 权限才能触发。本地单用户场景下，用户就是 owner，过度禁用反而影响使用。只保留 `ownerAllowFrom` 即可

3. **Memory search**：`agents.defaults.memorySearch.enabled` 设为 `false`（无 OpenAI key 时必做）

完成后运行 `openclaw security audit` 确认：预期 0 critical（1 warn about trusted_proxies 在 loopback 模式下可忽略）。

详细步骤见 `references/openclaw-setup.md`「安全加固」章节。

### 配置验证流程

当 OpenClaw 出现问题时，按以下顺序排查：

1. **检查配置文件**：`cat ~/.openclaw/openclaw.json` -- 确认 provider/apiKey/baseUrl 正确
2. **检查 agent 列表**：`openclaw agents list` -- 确认有 main agent，模型配置正确
3. **运行 doctor**：`openclaw doctor` -- 自动检查配置完整性、状态一致性
4. **测试本地调用**：`openclaw agent --local --agent main --message "test"` -- 验证模型 API 可达
5. **检查 Gateway**：`openclaw daemon status` + `netstat -ano | grep 18789`

### PowerShell 中使用 OpenClaw

npm 全局安装的 CLI 工具（openclaw 等）在 PowerShell 中默认不在 PATH。需要在 PowerShell profile 中添加函数：

```powershell
# 在 $PROFILE 中添加
function openclaw {
    & "$env:USERPROFILE\AppData\Roaming\npm\openclaw.cmd" @args
}
```

详见 `references/openclaw-setup.md`（完整安装、配置、Gateway 启动、AionUi 集成步骤）

## 主动提示规则

当 Hermes 在执行任务时发现以下情况，**必须主动告知用户**（不要沉默失败）：

1. 用户要求操作 Hermes 无连接器的平台（Jira/Notion/Slack/Calendar/Gmail/HubSpot）
   → "这个我做不了，OpenWorker 有 XXX 连接器，请在 OpenWorker 中操作"
2. 用户要求浏览器操作网页
   → "我无法操控浏览器，OpenWorker 有 Playwright 集成"
3. 用户要求语音输入
   → "我没有 STT，OpenWorker 支持语音输入"
4. 任务需要 GUI 可视化
   → "我是 CLI，OpenWorker 是桌面应用，可以可视化操作"
5. 用户需要无人值守自动化+审批
   → "我是同步审批，无人值守时操作会失败。OpenWorker 的 Inbox 队列更适合"

## 多 Agent 协作模式

### 模式 A：Hermes 为主，CLI Agent 为辅（已验证可用）

Hermes 通过 terminal 调用其他 CLI Agent，适合需要不同模型能力的场景：

```
Hermes → terminal → claude.cmd --print "深度分析任务"
Hermes ← 读取 Claude 输出 → 综合回复用户
```

### 模式 B：Hermes 为主，OpenWorker 为辅（手动切换）

Hermes 做不了的事情，告诉用户切到 OpenWorker：

```
Hermes: "这个 Jira 追踪我做不到，请打开 OpenWorker，在里面输入'检查 PROJ-123 的状态'"
```

### 模式 C：并行调研（受限）

Hermes 通过 terminal(background=true) 启动多个后台 Agent 进程实现伪并行。
delegate_task 在 v0.16.0 有 credential pool bug，暂不可用。

## AionUi Team 模式（与小队协作）⭐

当 Hermes 运行在 AionUi Team 模式下时，Hermes 是 Team Lead，可以通过 AionCore Team CLI 向小队成员（teammates）发消息、分配任务。

### 关键技术要点

1. **`$AIONUI_HELPER_BIN` 环境变量**：在 `terminal` 工具上下文中可用（指向 `<AI软件目录>\AionUi\resources\bundled-aioncore\win32-x64\aioncore.exe`），但在 `execute_code` 中**不可用**（缺 `AIONUI_BASE_URL` 等运行时环境变量）。所有 team CLI 调用必须通过 `terminal` 工具。

2. **stdin JSON 模式**：`team send-message` 不接受 `--to` 等 CLI 标志参数，必须通过 stdin 传入 JSON：

```bash
# ✅ 正确：echo JSON | pipe to CLI
echo '{"to":"019fcb33-xxxx","message":"任务描述"}' | "$AIONUI_HELPER_BIN" team send-message

# ❌ 错误：CLI 标志参数
"$AIONUI_HELPER_BIN" team send-message --to "019fcb33-xxxx" --message "任务描述"  # 报错
```

3. **其他 team 命令同样用 stdin JSON**：
   - `team members`：无参数，直接 `"$AIONUI_HELPER_BIN" team members`
   - `team task create`：`echo '{"subject":"任务标题","description":"描述"}' | "$AIONUI_HELPER_BIN" team task create`
   - `team task list`：`echo '{}' | "$AIONUI_HELPER_BIN" team task list`

4. **异步消息**：发送消息后队友状态为 `blocked` / `runtime_starting`，消息是异步的。队友处理完后会发回 idle 通知。

5. **获取 slot_id**：首次调用 `team members` 获取花名册，其中包含每个成员的 `slot_id`（用于 `to` 参数）、`name`、`role`、`status`、`model`。

6. **批量发送**：可以在一个回复中发多个 `terminal` 调用（每个发一条消息），实现并行通知所有小队成员。

### Team 模式 vs CLI 委派模式

| 维度 | AionUi Team 模式 | CLI 委派模式 |
|------|-----------------|-------------|
| 调用方式 | `$AIONUI_HELPER_BIN` team CLI | terminal 调用 claude.cmd/opencode.cmd 等 |
| Agent 隔离 | 每个 teammate 独立会话+终端 | 共享 Hermes terminal 会话 |
| 适用场景 | 多 Agent 持续协作、任务分解分配 | 单次深度推理/代码分析 |
| 消息传递 | 异步 team_send_message | 同步 terminal 输出 |
| 任务追踪 | team task board | 无（靠对话记忆） |

两种模式可以并存：Team 模式用于协调，CLI 委派用于特定深度任务。

**Team CLI 完整使用手册**：见 `references/aionui-team-cli.md`（命令清单、stdin JSON 格式、常见陷阱）

**交叉验证报告验证模式**：见 `references/cross-validation-verification.md`（外部审查报告的验证流程、临时脚本模板、真实案例）

**中文文献搜索能力调研**：见 `references/chinese-literature-search.md`（百度学术/Crossref/OpenLex/Semantic Scholar 中文搜索实测、反爬调研、最佳实践）

## 详细能力矩阵

完整的 5 Agent 能力对照表（含 6 个维度 26 个表格项）见：
`references/agent-capability-matrix.md`

Obsidian 中的完整报告：`🤖 AI Agent\多Agent能力边界与协作矩阵.md`

OpenWorker 配置管理详见：`references/openworker-config.md`（配置文件结构、火山方舟接入方法、Coding Plan 模型清单、修改流程）

## 常见陷阱

### 陷阱1：OpenWorker 安装被 360 安全卫士拦截

OpenWorker Windows 版未签名（SmartScreen 也会警告），360 安全卫士会锁定 `ucrtbase.dll` 阻止安装。

**解决**：安装前临时退出 360 安全卫士，安装完成后再重新打开。

### 陷阱2：OpenWorker 不可被 Hermes 直接调用

OpenWorker 是独立桌面应用，不是库或 API。从源码运行时有 HTTP API（端口 8765），但无公开文档，API 随时变化。不要试图用 curl 调用 OpenWorker API 来"自动化"它——那是内部接口。

### 陷阱3：Claude Code 长 prompt 截断

`claude.cmd --print "很长的prompt"` 会截断长参数。解决方案：将 prompt 写入文件，让 Claude 自己读文件。

### 陷阱4：OpenCode 拒读外部目录

OpenCode 自动拒绝读取工作目录之外的文件。调用前需 `cd` 到材料所在目录。

### 陷阱5：火山方舟 API /models 返回的不是 Coding Plan 模型

火山方舟 `GET /api/coding/v3/models` 返回 127 个全平台模型（含旧版 doubao、embedding 等），**不是** Coding Plan 包月可用的 13 个模型。Coding Plan 模型清单须从 Coding Plan 控制台 UI 获取，不能从 API /models 拉取。用户已纠正过此错误。

### 陷阱5.5：OfficeCLI 安装到 D 盘 + PATH 配置 ⭐

OfficeCLI 是单一二进制文件（~32MB），从 GitHub Releases 下载 `officecli-win-x64.exe`。安装到 D 盘时：

1. 下载到 `<OfficeCLI目录>\officecli.exe`
2. 验证：直接运行 `officecli.exe --version` 确认可执行
3. **PATH 写入问题**：Windows 用户级 PATH 环境变量可能被安全策略阻止写入（PowerShell `[Environment]::SetEnvironmentVariable` 和 `setx` 都可能失败）。解决方法：
   - 创建 `officecli.bat` 包装文件（内容：`@echo off\n"D:\...\officecli.exe" %*`）在同目录
   - 或让用户手动通过 `sysdm.cpl` -> 高级 -> 环境变量 -> 用户变量 Path -> 新建添加目录
4. 安装到 AI 知识库目录下（不装 C 盘）

**AionUi 配合**：AionUi 是 Electron 桌面应用（~290MB exe安装包），安装时在安装向导中选择 D 盘路径即可，不需要命令行配置。下载 `AionUi-x.x.x-win-x64.exe`（不是 arm64 版本）。

### 陷阱6：AionUi 连接 Hermes 后报 "supported model names are deepseek-v4-pro or deepseek-v4-flash, but you passed glm-5.2" ⭐

**根因**：火山方舟 Coding Plan 的 5 小时用量限制是**所有模型共用**的（glm-5.2、deepseek-v4-pro、doubao-seed-2.0-lite 等共享同一额度池）。当 5 小时额度耗尽时，主模型 glm-5.2 返回 429，Hermes 自动降级到 fallback 链中的 deepseek-v4-pro（同属 volcano provider）-> 也 429 -> 继续降级到 doubao-seed-2.0-lite -> 也 429。此时 AionUi 前端显示的是降级过程中的错误信息，看起来像"模型名不匹配"，实际是**额度用完**。

**诊断方法**：
1. 看 AionUi 右上角模型选择器是否显示了一个非预期的模型（如 `doubao-lite-4k-240328`）-> 说明 Hermes 正在尝试 fallback
2. 用 `hermes config show` 检查当前主模型和 fallback 链配置
3. 直接 curl 测试主模型：`curl -s https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions -H "Authorization: Bearer $ARK_KEY" -d '{"model":"glm-5.2",...}'` -> 如果返回 429 就是额度耗尽
4. 去火山方舟控制台查看 5 小时额度：https://console.volcengine.com/ark/region:ark+cn-beijing/quota

**修复方案**：
- 短期：等待 5 小时窗口重置（额度按滑动窗口计算）
- 或：在 AionUi 模型选择器中手动切换到非火山方舟模型（如 DashScope 千问）
- 长期：确保 fallback 链中有跨 provider 的模型（DashScope/Moonshot/DeepSeek），这样 volcano 额度耗尽时能自动降级到其他 provider

**注意**：Hermes gateway 进程启动时加载了 fallback 配置快照（CLI_CONFIG 模块级变量），修改 config.yaml 后需重启 gateway 才能更新降级链。详见 `plan` 技能 `references/hermes-model-config.md` 第7节。

### 陷阱7：Windows 环境变量在 Hermes terminal 中不可见

用户在 Windows 系统设置中创建了环境变量（如 `MINIMAX_API_KEY`），但 Hermes 的 terminal 工具（Git Bash）无法直接读取。原因是 Hermes 的 terminal 继承的是 gateway 启动时的 shell 环境，不自动加载后续新增的系统环境变量。

**解决方法**：用 PowerShell 读取用户级环境变量并写入 Hermes 的 `.env` 文件：

```python
import subprocess, os
result = subprocess.run(
    ["powershell.exe", "-NoProfile", "-Command",
     "[Environment]::GetEnvironmentVariable('VAR_NAME', 'User')"],
    capture_output=True, text=True
)
api_key = result.stdout.strip()

env_path = os.path.expanduser("~/AppData/Local/hermes/.env")
# 追加到 .env 文件
with open(env_path, "a") as f:
    f.write(f"\nVAR_NAME={api_key}\n")
```

### 陷阱8：对用户必须用尊称"用户"

对用户一律用尊称"用户"，禁止用"你"。所有回复与委派模板中的指令均须遵循此规范。

### 陷阱9：Team 模式下长消息通过 stdin JSON 传输 ⭐

当消息内容较长（如完整计划文档、详细调研指令）时，直接用 `echo '{"to":"...","message":"很长的内容"}'` 会在 shell 中遇到引号转义问题（消息中含双引号、换行、特殊字符）。

**正确做法**：用 `write_file` 将消息写入临时文件，再用 Python 生成 JSON payload 写入另一个临时文件，最后通过管道传入：

```bash
# 步骤1：write_file 写消息内容到 /tmp/plan_review.md
# 步骤2：用 Python 生成 JSON payload（自动处理转义）
python3 -c "
import json
with open('/tmp/plan_review.md', 'r', encoding='utf-8') as f:
    msg = f.read()
payload = json.dumps({'to': '019fcb33-xxxx', 'message': msg}, ensure_ascii=False)
with open('/tmp/plan_review_cc.json', 'w', encoding='utf-8') as f:
    f.write(payload)
"
# 步骤3：管道传入 team CLI
"$AIONUI_HELPER_BIN" team send-message < /tmp/plan_review_cc.json
```

### 陷阱10：队友 runtime 启动失败时 Leader 自行接管 ⭐

队友状态显示 `error`，消息返回 `Agent runtime failed to start`。常见原因及诊断：

**原因A：Node.js 版本不兼容**（如 OpenClaw 要求 >=25.9.0，系统是 v25.2.1）
- 诊断：`openclaw --version` 在 terminal 中报 Node.js 版本错误
- 修复：见 `hermes-windows` 技能陷阱 #12/#13（bash wrapper PATH 格式修正）

**原因B：CLI 后端 Gateway 未运行** ⭐⭐（实战）

OpenClaw 在 AionUi Team 模式下以 ACP（Agent Client Protocol）模式运行，需要 OpenClaw Gateway 在 `127.0.0.1:18789` 监听。Gateway 未运行时：
- aioncore 日志反复出现 `ACP bridge failed: connect ECONNREFUSED 127.0.0.1:18789`
- 紧接着 `Failed to establish ACP protocol connection`
- 团队槽位状态变为 `Failed: Agent runtime failed to start`
- AionUi 反复重试 spawn openclaw.cmd 进程（每次约10秒后失败）

**诊断方法**：
1. 在 aioncore 日志中 grep `ECONNREFUSED` -- 如果指向 18789 端口，就是 Gateway 未运行
2. `netstat -ano | grep 18789` -- 端口未监听 = Gateway 没启动
3. `openclaw agent --message "test" --agent main` 在 terminal 中直接运行 -- 如果成功返回结果（嵌入模式），说明 CLI 本身正常，只是 Gateway 未启动

**修复方法**：
- 启动 OpenClaw Gateway：`openclaw gateway start`（在 terminal 中执行）
- 或在 AionUi Team 设置中移除 OpenClaw 槽位（如果暂时不需要）
- **注意**：OpenClaw 的 bash wrapper（`~/AppData/Roaming/npm/openclaw`）可能有 PATH 格式问题导致 node 版本错误（见 `hermes-windows` 陷阱12），AionUi 调用的是 `.cmd` 版本（Windows 路径格式，通常正常），但手动测试时用 bash 版本可能报错

**原因C：其他 CLI 后端配置错误**
- 用 `openclaw doctor` 诊断 OpenClaw 配置完整性
- 检查 `~/.openclaw/openclaw.json` 中 provider/apiKey/baseUrl 是否正确

**处理**：
1. 用 `team describe-assistant` 检查队友的 assistant 配置（backend 类型）
2. 在 `terminal` 中直接运行该 CLI 工具验证是否可启动
3. 如果是 Node.js 版本问题，见 `hermes-windows` 技能陷阱 #12/#13
4. 如果是 Gateway 未运行，启动 Gateway 或移除该队友槽位
5. **Leader 自己接管该队友的任务**（不要等修复完了才推进）。原则：Leader 先完成失败队友的任务，然后继续推进计划。

### Team 模式下 Leader 履职纪律 ⭐

Team 模式下 Leader 必须遵守以下纪律：

1. **/plan 前缀必须走 plan 流程，团队模式不豁免**：用户发 `/plan` 指令（即使任务看似明确），Leader 必须先走 plan 技能流程（阶段0 表达优化 → 阶段1 计划 → 阶段2 等待用户确认 → 执行），不能当普通任务直接执行。已直接执行后的补救：补展示"表达优化+执行计划（含已完成步骤）+待确认"。

2. **按能力分配任务 + 管理表格**：任务分配必须依据每位队友的能力与技能（参考《团队能力矩阵》），不能凭印象乱派。

3. **Leader 亲自把控质量，不当甩手掌柜**：申请书/论文/综述等核心文档，Leader 是最终质量把控者——必须**亲自通读全文、亲自把关、亲自终审**（给独立评分），不能只转述队友评价。其他成员只是辅助写作与审查。文献类任务 Leader 亲办（文献核验流程见 academic 技能组）。

4. **装配/确认类结论必须有实战验证**：队友"确认已具备技能/已装配"是口头自报，Leader 必须发**功能测试任务**（如真实调用 Crossref 验证文献、真实从 PDF 提取元数据）验证后才算数。

### 陷阱11：Team 模式下的计划评审工作流 ⭐

当用户要求在 Team 模式下制定计划并让队员评审时，正确流程：

1. Leader 先完成失败队友的任务（如有）
2. Leader 综合所有队员的调研结果，制定完整计划
3. **依次**提交给每个可用队员评审（不是同时发送，是顺序评审）
4. 每轮评审后根据反馈修改计划，再提交下一位
5. 直到所有成员都认可没有可改进的地方为止
6. 最后提交给用户确认

### 陷阱12.5：bash wrapper 中 Windows 路径格式在 Git Bash 不生效 ⭐

npm 全局安装的 CLI 工具（openclaw 等）有 bash wrapper 脚本（`~/AppData/Roaming/npm/openclaw`），其中用 `export PATH="<知识库根目录>/..."` 设置自带 Node.js 路径。但 Git Bash（MSYS）**不认识 `D:/` 格式的路径**，导致 PATH 不生效，openclaw 报 Node.js 版本错误。

**修复**：将 bash wrapper 中的 `D:/...` 改为 `/d/...`（MSYS 路径格式）：

```bash
# 修复前（不生效）：
export PATH="<OpenClaw目录>/node/node-v25.9.0-win-x64:$PATH"

# 修复后（生效）：
export PATH="<知识库根目录>/OpenClaw/node/node-v25.9.0-win-x64:$PATH"
```

可用 sed 一键修复：
```bash
sed -i 's|<知识库根目录>|<知识库根目录>|' ~/AppData/Roaming/npm/openclaw
```

**注意**：`.cmd` 版本（PowerShell/cmd 用）不需要修改，Windows 路径格式在 cmd.exe 中正常工作。只有 bash wrapper 需要修。此问题也存在于 OpenCode 等其他 npm 全局安装的 CLI 工具中。

### 陷阱12：Gateway 启动慢，health 检查需等待 ⭐

OpenClaw Gateway 启动需要 30-35 秒（加载配置、解析认证、初始化插件、绑定端口）。启动后立即运行 `openclaw health` 会报 `gateway closed (1006 abnormal closure)`，让人误以为启动失败。

**正确做法**：
1. 用 `terminal(background=true)` 启动 Gateway，必须 export ARK_API_KEY 环境变量：
   ```bash
   export ARK_API_KEY="ark-xxx" && cmd.exe /c "%USERPROFILE%\AppData\Roaming\npm\openclaw.cmd gateway --verbose" 2>&1
   ```
2. 等待至少 15 秒后再检查端口：`netstat -ano | grep 18789`
3. 如果端口未出现，再等 15-20 秒重试
4. 端口监听后 `openclaw health` 才会返回正常

**Gateway 启动失败的诊断**：
- 如果 30 秒后端口仍未监听，检查 Gateway 进程的 stdout 输出（`process action='log'`）
- 常见失败原因：SecretRef 环境变量不可用（见安全加固章节）、配置文件 JSON 格式错误、Node.js 版本不兼容
- 稳定性日志路径：`~/.openclaw/logs/stability/openclaw-stability-*.json`
- **SecretRef 失败的具体错误**：`SecretProviderResolutionError: Secret provider "openclaw" is not configured (ref: env:openclaw:ARK_API_KEY)` -- 意味着 Gateway 进程上下文中找不到环境变量。修复：将 config 中 SecretRef 改回明文（loopback 模式下可接受），或确保环境变量在 Windows 注册表级别可用

### 陷阱13：AionUi 中 OpenClaw 的 ACP 连接配置 ⭐

AionUi 在 SQLite 数据库 `~/AppData/Roaming/AionUi/aionui/aionui-backend.db` 的 `agent_metadata` 表中管理 ACP 后端。OpenClaw 有两条记录：

| agent_id | agent_type | command | args | 用途 |
|----------|-----------|---------|------|------|
| `f9f61666` | `openclaw-gateway` | `openclaw` | `[]` | Gateway 直连模式（少用） |
| `b7e8a9c4` | `acp` | `openclaw` | `["acp"]` | ACP 桥接模式（常用） |

ACP 模式下 AionUi 执行 `openclaw acp`，该命令连接本地 Gateway 的 WebSocket（ws://127.0.0.1:18789）。

**连接失败的诊断**：
1. 检查 `last_check_error_message` 字段 -- 如果是 `ACP initialize failed: Incoming transport closed`，说明 Gateway 未运行
2. 检查 Gateway 端口：`netstat -ano | findstr 18789`
3. 检查 aioncore 日志中的 `ECONNREFUSED` 错误

**如果需要通过 env_override 注入环境变量**（例如 AionUi 启动 openclaw 进程时需要传 token）：
```python
# 更新 agent_metadata 表的 env_override 字段
import sqlite3, json
conn = sqlite3.connect(r'C:\Users\<user>\AppData\Roaming\AionUi\aionui\aionui-backend.db')
cur = conn.cursor()
env_override = json.dumps([
    {"name": "OPENCLAW_GATEWAY_TOKEN", "value": "oc-xxx"},
    {"name": "ARK_API_KEY", "value": "ark-xxx"}
])
cur.execute('UPDATE agent_metadata SET env_override = ? WHERE agent_id = ? AND agent_type = ?',
    (env_override, 'b7e8a9c4', 'acp'))
conn.commit()
```

注意：如果 openclaw.json 中密钥保留明文（SecretRef 在 Windows 不可用时的折衷），则不需要 env_override。

### 陷阱14：交叉验证报告可能基于旧代码 -- 先读代码再改 ⭐

**问题**：收到外部 Agent（如 AionUi Team 成员）产出的交叉验证报告，报告列出若干问题和修复建议。但报告可能基于旧版本代码快照，问题在审查时已经修复。盲目按报告修改可能引入回退。

**真实案例**：literature-review 技能的交叉验证报告列出 5 个问题（中文作者名逗号、venue字段名、DOI/URL重复、title_zh映射、APA标点）。经实际代码验证，5 个问题在代码中均已修复。报告审查的是修复前的代码快照。

**正确流程**：
1. 通读报告，提取问题清单（每个问题对应一个文件+函数+预期行为）
2. **先读当前代码确认状态**：用 `skill_view(file_path=...)` 或 `read_file` 读取报告指向的文件
3. **写临时验证脚本**：用 `write_file` 写 .py 脚本，针对每个问题写 assert 语句
4. **运行脚本**：一次运行确认全部问题的 PASS/FAIL 状态
5. **清理**：删除临时脚本
6. 只对实际 FAIL 的问题进行修复

**关键原则**：
- **报告可能基于旧版本代码**：审查者可能审查的是修复前的快照。先读代码再下结论
- **用 assert 而非 print**：`assert actual == expected` 比 `print(actual)` 更明确
- **bash 引号嵌套陷阱**：Python 代码内嵌在 `terminal(command='python -c "..."')` 中时引号极易出错。改用 `write_file` 写临时 .py 文件再运行
- **一个脚本覆盖所有问题**：避免逐个手动检查，减少遗漏

## OpenWorker 配置管理

### 配置文件位置

- prefs.json: `~/AppData/Roaming/coworker/prefs.json` — 模型列表（models数组）、默认模型（default_model）
- secrets.json: `~/AppData/Roaming/coworker/secrets.json` — provider API key + base_url
- coworker.db: `~/AppData/Roaming/coworker/coworker.db` — 会话/审计/记忆（SQLite）
- 日志: `~/AppData/Roaming/coworker/logs/openworker-server.log`

### 火山方舟 Coding Plan 配置方法

OpenWorker 没有内置火山方舟 provider，通过 openai provider + custom base_url 实现：

1. secrets.json 中添加 `provider:openai`：`{"api_key": "ark-xxx", "base_url": "https://ark.cn-beijing.volces.com/api/coding/v3"}`
2. prefs.json 中设 `default_model`: `"openai:glm-5.2"`，`models` 数组每项为 `"openai:模型名"`
3. 模型字符串格式: `openai:glm-5.2`（ProviderRouter 按前缀路由到 openai provider）

### Coding Plan 13 个可用模型

auto, doubao-seed-2.1-turbo, doubao-seed-2.0-code, doubao-seed-2.0-pro,
doubao-seed-2.0-lite, doubao-seed-code, glm-5.2, kimi-k2.7-code,
minimax-m3, deepseek-v4-flash, deepseek-v4-pro, minimax-m2.7, kimi-k2.6

注意：glm-5.2、deepseek-v4-pro、kimi-k2.6 默认开启 thinking 模式，需关闭。

### 修改配置流程

1. taskkill 关闭 openworker-desktop.exe 和 openworker-server.exe
2. 修改 prefs.json 和/或 secrets.json
3. 用 PowerShell `Start-Process` 重启 openworker-desktop.exe
