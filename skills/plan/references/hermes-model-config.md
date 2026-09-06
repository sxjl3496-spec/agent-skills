# Hermes 模型降级与子agent模型配置

本文档记录 config.yaml 中与模型切换相关的配置项。config 真实路径由 HERMES_HOME 环境变量决定（当前 D:\BaiduSyncdisk\AIKnowledgeBase\Hermesagent\hermes-data\config.yaml），不是 ~/AppData/Local/hermes/config.yaml。

## 1. fallback_providers -- 主模型降级链

当主模型失败时（429限额、529过载、503服务错误、402余额不足、连接失败），Hermes 按顺序尝试降级链中的模型。

**格式**：字典列表，每项含 provider + model + base_url。字符串列表会被静默跳过（降级链为空）。

```yaml
fallback_providers:
  - provider: deepseek
    model: deepseek-v4-flash
    base_url: https://api.deepseek.com/v1
  - provider: moonshot
    model: kimi-k2.6
    base_url: https://api.moonshot.cn/v1
  - provider: dashscope
    model: qwen3.7-flash
    base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
```

**验证命令**：`hermes fallback list`

**常见错误**：`fallback_providers: '["deepseek","moonshot"]'`（字符串列表）-- Hermes 的 get_fallback_chain() 要求每项是 dict 含 provider+model 字段，字符串会被跳过。降级链实际为空但无报错。

## 2. delegation.model -- 子agent模型

控制 delegate_task 派出的子agent使用哪个模型。为空时继承主agent模型（无模型隔离）。

```yaml
delegation:
  model: deepseek-v4-flash
  provider: deepseek
  base_url: https://api.deepseek.com/v1
```

设置后 delegate_task 子agent使用指定模型，与主agent不同。这对 plan 技能的验证层至关重要：验证子agent用不同模型审查交付物，消除同模型确认偏差。

**API key 解析**：delegation 段**不设 `api_key`**。⭐ 原因：当 `base_url` 也设置时，`api_key: ${VAR}` 不会做环境变量展开，字面量 `"${VAR}"` 被当作 API key 使用，必然 401（详见陷阱19 Bug A）。省略 `api_key` 后，子agent 继承父 agent 已解析的 API key。

**推荐写法**（优先级从高到低）：
```yaml
# ① 最佳：只设 model+provider，走 resolve_runtime_provider 完整解析
delegation:
  model: deepseek-v4-flash
  provider: deepseek

# ② 可接受：设 base_url 但不设 api_key
delegation:
  model: deepseek-v4-flash
  provider: volcano
  base_url: https://ark.cn-beijing.volces.com/api/coding/v3

# ❌ 错误：base_url + api_key: ${VAR}（VAR不展开，401）
```

**credential pool 跨provider降级bug**（v0.16.0）：当子agent首选模型429降级到不同provider的fallback模型时，credential pool 用父agent的key调新provider，导致401。详见陷阱19 Bug B。临时方案：delegation 用与主模型相同的provider避开跨provider降级。

## 3. auxiliary.vision.fallback_chain -- 视觉模型降级链

辅助任务（如视觉分析）有独立的降级链，配置在 auxiliary.<task>.fallback_chain 下。

当前生效配置（2026.7.30 更新，优先换通道策略）：

```yaml
auxiliary:
  vision:
    provider: volcano
    model: kimi-k2.6
    base_url: https://ark.cn-beijing.volces.com/api/coding/v3
    api_key: ark-xxxxx
    fallback_chain:
      - provider: moonshot           # 备1: 换通道（月之暗面直连）
        model: kimi-k2.6
        base_url: https://api.moonshot.cn/v1
      - provider: dashscope          # 备2: 换通道（DashScope直连）
        model: qwen3.5-omni-plus
        base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
      - provider: volcano            # 备3: 同通道兜底（火山方舟换模型）
        model: doubao-seed-2.1-turbo
        base_url: https://ark.cn-beijing.volces.com/api/coding/v3
```

fallback_chain 中每项支持 provider、model、base_url、api_key 字段。provider 字段必填，其余可选。

> **换通道优先原则（2026.7.30）**：fallback 链优先切换 API 提供商（换通道），而非在同提供商上换模型。这样避免同一提供商的限额/故障同时影响主模型和备用模型。同通道换模型仅作为最后兜底。

## 4. providers -- Provider 定义

每个 provider 需要在 providers 段注册，包含 base_url、api_key_env（环境变量名）、models（可用模型列表）。

```yaml
providers:
  dashscope:
    base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
    api_key_env: DASHSCOPE_API_KEY
    models: '["qwen3.7-flash", "qwen3.7-max"]'
```

**API key 存放**：环境变量定义在 ~/AppData/Local/hermes/.env 文件中（不是 bashrc，因为 Windows Scheduled Task 启动的 gateway 不 source bashrc）。

## 5. CLI 管理命令

| 命令 | 作用 |
|------|------|
| `hermes fallback list` | 查看当前降级链 |
| `hermes fallback add` | 交互式添加降级条目（需 TTY） |
| `hermes fallback remove` | 交互式删除降级条目 |
| `hermes fallback clear` | 清空降级链 |

**注意**：`hermes fallback add` 需要交互式终端，无法在 execute_code 中调用。直接编辑 config.yaml 更可靠。

## 6. 当前配置状态（2026.7.30）

| 配置项 | 值 |
|--------|-----|
| 主模型 | glm-5.2 (volcano/火山方舟) |
| 文本降级链 | deepseek-v4-flash -> kimi-k2.6 -> qwen3.7-flash |
| 视觉主模型 | kimi-k2.6 (volcano) |
| 视觉降级链 | kimi-k2.6(moonshot换通道) -> qwen3.5-omni-plus(dashscope换通道) -> doubao-seed-2.1-turbo(volcano同通道兜底) |
| 子agent模型 | qwen3.7-flash (dashscope) -- 临时方案，规避 credential pool 跨provider bug（v0.16.0）。原配置 deepseek-v4-flash (volcano) 因 Bug B 降级401，改为同provider避开 |
| 第一层验证模型 | qwen3.7-flash (dashscope) |
| 图片生成 | wanx2.1-t2i-turbo (dashscope), 插件内 fallback: turbo->plus->v1 |
| 图生图 | qwen-image-edit-plus (dashscope), 无备用模型 |
| 视频生成 | wanx2.1-i2v-turbo (dashscope), 插件内 fallback: i2v-turbo->i2v-plus, t2v-turbo->t2v-plus |
| STT | faster-whisper small (本地), wrapper: small->base->tiny->paraformer-v2 |
| TTS | SAPI Huihui (本地), wrapper: Huihui->any Chinese->CosyVoice预留 |
| API监控cron | bb0ad2ee5962，每天8/14/20点检查4个API |

三者（主agent、第一层验证、第二层验证）使用三个不同厂商的模型，最大程度消除确认偏差。

## 7. Gateway 重启要求 -- CLI_CONFIG 模块级快照 ⭐

修改 config.yaml 后必须重启 gateway 进程才能生效。

**根因**：`cli.py:701` 执行 `CLI_CONFIG = load_cli_config()` -- 这是模块级变量，在 gateway 进程启动时加载一次，之后不再刷新。即使 `load_config()` 有 mtime 缓存机制（文件改动时自动重读），`cli.py` 中的 `CLI_CONFIG` 不会再次调用它。

**影响链路**：
- `cli.py:3343`: `self._fallback_model = get_fallback_chain(CLI_CONFIG)` 使用启动时快照
- 如果 gateway 启动时 fallback_providers 是旧的字符串列表格式，`get_fallback_chain()` 返回空列表
- `chat_completion_helpers.py:1026-1027`: `if agent._fallback_index >= len(agent._fallback_chain): return False` -- 空链直接跳过
- 结果：主模型 429 时不切换备用，静默失败无报错

**验证方法**：
```python
# 确认运行中的 gateway 已加载正确的降级链
from hermes_cli.config import load_config
from hermes_cli.fallback_config import get_fallback_chain
cfg = load_config()  # 这个会读最新 config（有 mtime 缓存）
chain = get_fallback_chain(cfg)
print(f"Chain length: {len(chain)}")  # 应 > 0
```

**注意**：上述验证用的是 `load_config()`（有 mtime 缓存），不能代表运行中 gateway 的 `CLI_CONFIG`（无缓存）。真正的验证是重启 gateway 后触发一次 429 看是否切换。

**修复步骤**：修改 config.yaml 后，重启 Hermes gateway（关闭旧进程 + 启动新进程）。

## 9. 环境变量名不匹配 — Coding Plan 静默 401 ⭐

**问题**：config.yaml 中 `providers.volcano.api_key: ${VOLCANO_API_KEY}` 但 .env 文件中对应的环境变量名为 `ARK_API_KEY`。Hermes 解析 `${VOLCANO_API_KEY}` 拿到空字符串，所有 Coding Plan API 调用用空 key 发出，全部 401 失败。

**排查方法**：
```bash
# 检查 config 引用的变量是否实际存在
echo "length=${#VOLCANO_API_KEY}"
# 检查 .env 中的实际变量名
grep -E "VOLCANO|ARK|volcano|coding" ~/AppData/Local/hermes/.env
```

**修复**：
1. 将所有 `${VOLCANO_API_KEY}` 引用改为 `.env` 中实际存在的变量名（如 `${ARK_API_KEY}`）
2. 同步更新 `providers.volcano.api_key_env: ARK_API_KEY`（原来是空字符串）
3. 重启 gateway 生效

**关键**：Hermes 配置中 `${VAR_NAME}` 直接按字面量在进程环境中查找，不校验环境变量是否存在。不存在的变量名静默解析为空字符串，无报错、无日志。这是一个静默故障模式。需要在两个位置保持一致：
- `providers.<name>.api_key_env` — 指定从哪个环境变量读取
- `api_key: ${VAR_NAME}` — inline 引用（与 api_key_env 使用相同变量名）

DashScope 文本模型（qwen3.7-flash/max）正常可用。视觉模型全部不可用（2026.7.29 测试8个模型）：

| 模型 | HTTP | 错误 |
|------|------|------|
| qwen-vl-max | 403 | Free quota exhausted |
| qwen-vl-plus | 403 | Free quota exhausted |
| qwen-vl-max-latest | 403 | Access denied |
| qwen-vl-plus-latest | 403 | Access denied |
| qwen2.5-vl-72b-instruct | 403 | Access denied |
| qwen2.5-vl-7b-instruct | 403 | Access denied |
| qwen2-vl-72b-instruct | 404 | Model does not exist |
| qwen2-vl-7b-instruct | 404 | Model does not exist |

需在阿里云控制台充值或开通付费后才可用。qwen3.7-flash 不支持视觉输入（多模态），仅支持纯文本。
