---
name: arkcli-helper
version: 1.0.0
description: "arkcli helper:给 Claude Code / Codex / OpenCode / OpenClaw / Hermes Agent 配置火山方舟 Plan 或 Platform Endpoint 的 model/provider，或给支持的 Agent(含 MCP-only 的 Trae)注入 MCP。Platform 仅可选择本人创建、Running、已验证为文本输出的 Endpoint 作 model，不配 MCP/Supabase；Plan 路径保持原有模型、MCP 与 Supabase 能力。用户说给当前或某个 Agent 配 MCP、豆包搜索、联网搜索、dataPro、OpenViking 时,用 `arkcli helper mcp`(只注入 MCP,不改 model);要连 model/provider 一起配用 `helper configure`;查状态用 `helper list`;移除注入用 `helper reset`。"
metadata:
  requires:
    bins: ["arkcli"]
  cliHelp: "arkcli helper mcp --help"
---

# arkcli helper —— 给本机 AI Agent 配置 Plan / Platform Endpoint / 注入 MCP

**前置:** 先用 Read 读 [`../arkcli-shared/SKILL.md`](../arkcli-shared/SKILL.md) 获取共享安全规则与认证闸门。

## 命令选择（先选最具体的子命令）

- 用户要查看或配置 Agent 的 model/provider、Plan、Platform Endpoint，或核对 `--with-mcp` / `--with-supabase` 等非交互选项时，必须选择 `arkcli helper configure`；只查看用法也要运行 `arkcli helper configure --help`，不能退化成父级 `arkcli helper --help`。
- 用户明确只注入 MCP、不改 model/provider 时，才选择 `arkcli helper mcp [target]`；只查看用法时运行 `arkcli helper mcp --help`。
- `arkcli-auth` 只处理实际认证阻塞。用户仅要求查看 helper 的 `--help` 时，不要转去登录、`init-volc` 或其他认证命令。

把 Agent Plan 内置 MCP server 注入本机 AI Agent 的配置 —— 这正是 `arkcli helper` 交互向导里"注入 MCP"那一步,这里做成**非交互、可被 prompt 触发**。个人版 `agent-plan` 注入四台;团队版 `agent-plan-team` 与 OpenViking 无关,只注入豆包搜索 + dataPro 两台。

## Platform Endpoint 配置

Platform profile 只负责配置 Agent 的 model/provider：`model` 写为用户选择的 Endpoint ID，base URL 使用 Platform 的 `/api/v3`，协议继续由各 harness 保持现有行为（Chat 或 Responses）。

- 只展示**当前 SSO 子用户创建**、`Running`、模型被明确验证为**文本输出**的 Endpoint；VLM（图文输入、文本输出）可用。
- 生图、生视频、生 3D、音频、Embedding、内容生成或未知模型一律不展示，也不能通过 `--model` 绕过。
- Agent 配置中的 `model` 仍写 Endpoint ID；context window、max completion tokens、输入/输出模态按 Endpoint 绑定的基础模型名，复用 Agent Plan / Coding Plan 现有的 ArkModels 元数据富化规则。元数据查询失败时同样 best-effort 省略扩展字段，不阻断已通过资格校验的 Endpoint。
- Hermes Agent 支持把 Platform Endpoint 写成 `volcengine-platform` model/provider；仍不支持 MCP 注入。
- 该接入只为 Platform 增加元数据调用方，不修改 Plan 模型清单、默认模型、元数据查询、MCP 或 Supabase 行为。
- 没有自己创建的 Endpoint 时，向导打开 `https://ark.volcengine.com/region:cn-beijing/endpoint/create?agentMode=close`；创建完成后选择“刷新列表”。已有但未运行的 Endpoint 需先启动再刷新。
- Platform **不支持** MCP、OpenViking 或 Supabase；`--with-mcp`、`--with-supabase` 会报错。

非交互调用：

```bash
arkcli helper configure codex \
  --profile <platform-profile> \
  --endpoint <ep-id>
```

配置成功后，Endpoint 可按 OpenAI 兼容入口调用：`/responses` 或 `/chat/completions`，请求的 `model` 均使用该 `<ep-id>`。

## 注入的是哪几台 MCP(写死,勿幻觉)

| server | 传输 | key 来源 |
|--------|------|---------|
| `mcp-server-askecho-search-infinity`（豆包搜索） | stdio(`uvx`) | **Agent Plan 的 API Key**(env `ASK_ECHO_SEARCH_INFINITY_API_KEY`,与 dataPro / 控制面**同一把** plan key);取不到则写占位符 |
| `dataPro-search` | http(streamable) | **Agent Plan 的 API Key**(header `X-Agent-Plan-Key`,裸 key) |
| `openviking-dataplane`（**仅个人版 agent-plan**） | http(streamable) | **OpenViking 库的访问 key**（数据面；header `Authorization: Bearer <key>`）;经 vikingdb 两步取:列库 → 按库取 key。账号多库时要选库(见下)。账号下 0 个库时跳过 |
| `openviking-controlplane`（**仅个人版 agent-plan**） | stdio(`uvx`) | **Agent Plan 的 API Key**（控制面；env `AGENTPLAN_API_KEY`）;不依赖 OV 库列表,个人版有 Agent Plan 即注入 |

> **个人版 vs 团队版:** 上表 OpenViking 两台是**个人版 `agent-plan`** 专属。**团队版 `agent-plan-team` 与 OpenViking 无关** —— 只注入豆包搜索 + dataPro 两台,`openviking-dataplane` / `openviking-controlplane` 都不配,也不会去查 vikingdb。

## host ≠ target(最关键的概念)

- **host** = 你(这个 AI Agent)此刻跑在哪 —— 命令读环境变量自动检测,无需你判断。
- **target** = 要把 MCP 写进谁的配置 —— 可以是 host 自己,也可以是另一个 agent。
- 二者解耦:人在 OpenCode 里,也能给 Claude Code 配 MCP。

→ 用户在 prompt 里**点名了某个 agent**(如"给 opencode / codex 配"):跑 `arkcli helper mcp opencode` / `arkcli helper mcp codex`
→ 用户说"**当前 / 这个 Agent**"或没点名:跑 `arkcli helper mcp`(自动检测当前 host)

## 子命令穷举

| 调用 | 说明 |
|------|------|
| `arkcli helper mcp [target] [--ov-resource <库名>] [--scope project] [--codex-config-scope profile|global] [--codex-profile <name>]` | **只注入 MCP,不改 model**。不传 target 自动检测当前 agent;账号多个 OpenViking 库时用 `--ov-resource` 指定;`--scope project`(仅 Trae)写项目级 `./.trae/mcp.json`;Codex 默认写 profile `~/.codex/arkcli.config.toml` |
| `arkcli helper configure <harness> [--profile P] [--model M\|--endpoint ep-id] [--with-mcp] [--with-supabase] [--codex-config-scope profile\|global] [--codex-profile <name>]` | Plan 用 model/provider；Platform 必须用 `--endpoint` 选择文本 Endpoint。仅 Plan 可加 MCP/Supabase。 |
| `arkcli helper list` | 查支持的 agent + 安装/配置状态(只读) |
| `arkcli helper supabase [--profile P]` | **非 MCP**:装 byted-supabase-cli + skill + 注入火山登录态(打通 byted-supabase 数据库能力);跟 harness 无关。仅 Agent Plan(个人版全档 + 团队版全档) |
| `arkcli helper reset <harness>` | 移除 arkcli 注入的配置(含 MCP) |
| `arkcli helper` | TTY 交互向导(需终端;非交互场景改用上面的);进入向导前会检查登录态,未登录/SSO 过期时按当前登录上下文拉起 SSO(火山走 volc-sso;全新用户无明确上下文时走 auth login 菜单),成功后继续向导;末尾会问是否顺便配 byted-supabase |

> ⚠️ 想"只加 MCP" → `helper mcp`;想"把 agent 接到 plan、连模型一起" → `helper configure --with-mcp`。别用 `configure` 去只加 MCP(它会一并(重)写 model)。
>
> 🎯 用户说"**把(我 plan 的)全套 harness 工具都配上 / 都给我 set 好**"(MCP + Supabase 一次到位)→ `arkcli helper configure <harness> --with-mcp --with-supabase`。这是 agent 唯一能一条命令配齐 MCP 三件套 + Supabase 的路径(交互向导 `arkcli helper` 要 TTY、agent 跑不了;它的自动 SSO 只服务真人终端);`--with-mcp` 只配 MCP、不含 Supabase,想带 Supabase **必须显式加 `--with-supabase`**(资格不够 / 失败只 warn,不阻断 harness 配置)。

## byted-supabase 数据库能力(`helper supabase`;**非 MCP**)

`arkcli helper supabase` 跟上面的 MCP 注入是**两类能力**:它**不写** agent 的 mcp.json,而是**装 byted-supabase-cli + skill** 并用当前火山 Agent Plan 登录态**注入登录态**(打通 byted-supabase / Volcengine Supabase 数据库平台)。**跟选哪个 harness 无关** —— 它配的是 byted-supabase-cli 这个独立工具本身。

- **门槛**:仅 Agent Plan —— 个人版 `agent-plan` **全档**支持(含 small/medium/large/max),团队版 `agent-plan-team` **全档**支持。不合格命令直接报错说明。
- **动作**:装 CLI(`npx -y @byted-supabase/cli@latest install`,连匹配的 byted-supabase agent skill 一起)→ 用所选 Agent Plan 身份的 STS + refresh_token 组装 Console Login 凭证 → `byted-supabase-cli login --credential-file`(个人版带 `--is-agent-plan`,团队版额外 `--agent-plan-seat-id <实时反查>`)注入到固定 profile `ark_login`。
- **触发**:用户说『配 byted-supabase / 打通数据库 / 装 supabase cli / 连接 supabase / 用我的 plan 连数据库』。
- **三条配置入口**(同一内核 `supabase.Configure`):① 专配 `arkcli helper supabase`;② 非交互/agent 顺带配 `arkcli helper configure <h> --with-supabase`(无确认框、失败只 warn,不阻断 harness 配置);③ 交互向导 `arkcli helper` 末尾可选步骤(仅合格 plan)。`helper mcp` / `configure --with-mcp` **不含** Supabase —— 想顺带配必须显式 `--with-supabase`。
- ⚠️ **v3 ve handoff 身份 (source=ve) 不能配 supabase**: `helper supabase` 内核 `gatherInputs` 强依赖 `LoadIdentityTokenFull(key)` 读 identity_store `token.json` 里的 refresh_token 组装 Console Login 凭证; 而 source=ve 身份**不落 token.json** (refresh_token 由 volcengine-go-sdk 内部管, arkcli 侧拿不到明文), 会报 `读 identity token: ...`。命中该报错时告诉用户: 想配 supabase 需要走 arkcli 原生 SSO 登录一次 (跳过 ve handoff), 具体做法是先 `ve logout` (或让 `ve` 处于未登录态) 再跑 `arkcli auth login` 拿到 `source="arkcli"` 的 identity。

## 范围边界(管好,别越界)

- **model/provider 可配置 target**:`claude-code` / `codex` / `opencode` / `openclaw` / `hermes`。其中 Hermes 支持 Plan 和 Platform Endpoint，但不支持 MCP。
- **可注入 target 有 5 个**:`claude-code` / `codex` / `opencode` / `openclaw` / `trae`。
- 本 skill 会被 `arkcli +connect` 装进很多 agent(cursor / gemini-cli / codex …40+),但 **MCP 注入只支持上一条列出的 5 个 target**。host 是其它 agent 时:要么用户点名其一作 target,要么命令会报"请显式指定" —— **绝不静默配错对象**。
- `codex` 支持 model/provider + MCP。默认 **profile 模式**写 `~/.codex/arkcli.config.toml`,需用 `codex --profile arkcli` 启动 terminal/TUI 才生效;传 `--codex-config-scope global` 才写 `~/.codex/config.toml`,该范围可能被 Codex CLI/TUI、Codex App、IDE extension 共享读取。
- `trae`(AI IDE)是 MCP-only:只注入 MCP、不配 model/provider;**无运行态宿主检测**(不会被自动当成 host),只能显式 `arkcli helper mcp trae`。默认写用户级 `~/.trae/mcp.json`,加 `--scope project` 写项目级 `./.trae/mcp.json`(项目级需在 Trae「设置 → MCP」开启「启用项目级 MCP」开关 + 重开项目)。
- `hermes` 支持 Plan / Platform Endpoint 的 model/provider 配置，但暂不支持 MCP 注入 → MCP 请求命中就直说"暂不支持"。

## 前提

- **必须有 Agent Plan 订阅**(豆包搜索 / dataPro 要 Agent Plan 的 key;OpenViking 两台是个人版专属)。命令自动定位账号下的 Agent Plan profile,**与当前 active profile 无关**;个人版 `agent-plan` 与团队版 `agent-plan-team` 都能注入,但**两者不等价**:个人版注入四台,**团队版 `agent-plan-team` 与 OpenViking 无关,只注入豆包搜索 + dataPro 两台**。没有就引导 `arkcli auth login` 开通;账号同时有多个 Agent Plan profile(如个人版 + 团队版)时让用户用 `--profile` 指定。
- 注入后 **agent 需重启**才会加载新 MCP。Codex profile 模式还需用 `codex --profile <name>` 启动;Trae 还需去「设置 → MCP」面板确认 MCP 已启用(项目级文件额外要开「启用项目级 MCP」开关)后重开项目。

## OpenViking 库的选择(openviking-dataplane 专属;**仅个人版 agent-plan**)

> 本节只适用于**个人版 `agent-plan`**。**团队版 `agent-plan-team` 与 OpenViking 无关**,命令对团队版直接跳过下面整套列库/选库流程,只注入豆包搜索 + dataPro。

`openviking-dataplane` 的 key 绑定到某个 OpenViking 库(库名 ↔ ResourceID 1:1)。命令先列账号下的库,按数量分流:

- **0 个库** → 自动跳过 openviking-dataplane(仍注入另三台,包括 openviking-controlplane),并提示去 `https://console.volcengine.com/vikingdb/openviking/region:openviking+cn-beijing/create` 建库后重跑。可直接接受跳过。
- **1 个库** → 直接用,无需选择。
- **多个库** → 命令报错并列出所有库名(形如 `检测到多个 OpenViking 库,请用 --ov-resource <库名> 指定其一:[a, b, c]`)。**此时用 AskUserQuestion 把这些库名作为选项让用户选**,拿到选定库名后带 `--ov-resource <库名>` 重跑同一条命令。
- 取 key 失败(非 0 库)→ openviking-dataplane 写占位符 `Bearer <OPENVIKING_KEY>`,提示用户手动替换。
- `openviking-controlplane` 不受上述影响:个人版只要有 Agent Plan 就始终注入(团队版不注入,见上)。

## 路由判断 / 反触发

- "给 Agent 配 MCP / 豆包搜索 / 联网搜索 / dataPro / web search" → `arkcli helper mcp`
- "把 agent 指向我的 plan(连模型一起)" → `arkcli helper configure`
- "把全套 harness 工具都配上 / 一次配齐 MCP + Supabase" → `arkcli helper configure <h> --with-mcp --with-supabase`
- "配 byted-supabase / 打通数据库 / 装 supabase cli / 连接 supabase" → `arkcli helper supabase`(非 MCP,装 CLI+skill+注入登录态);或在配 harness 时顺带 `configure --with-supabase`
- 把 arkcli skills **安装**进 agent → 走 [arkcli-connect](../arkcli-connect/SKILL.md),与本 skill 无关
- 401 / 登录 / 鉴权失败 → 走 [arkcli-auth](../arkcli-auth/SKILL.md)
- 生图 / 生视频 → 走 [arkcli-gen](../arkcli-gen/SKILL.md)

详细 flag、输出样例、错误码、边界 case 见 [`references/arkcli-helper.md`](references/arkcli-helper.md)。
