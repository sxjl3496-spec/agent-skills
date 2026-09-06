# delegation.api_key `${VAR}` 不解析 + credential pool 跨provider降级401

Hermes v0.16.0 确认的两个关联 bug。详见 plan SKILL.md 陷阱19。

## Bug A：delegation.api_key: ${VAR} 不被解析

### 根因

`delegate_tool.py` 的 `_resolve_delegation_credentials()` 有两条路径：

1. **base_url 路径**（当 `delegation.base_url` 设置时）：
   - 直接读 `cfg.get("api_key")`，**不做 `${VAR}` 展开**
   - `configured_api_key = str(cfg.get("api_key") or "").strip() or None`
   - 如果 config.yaml 写 `api_key: ${ARK_API_KEY}`，读到的字面量是 `"${ARK_API_KEY}"`
   - 这个字面量被当作 API key 使用，API 返回 401

2. **provider 路径**（当只设 `delegation.provider`，不设 `base_url` 时）：
   - 走 `resolve_runtime_provider()`，完整解析 provider 凭据
   - api_key 从 `providers.<name>.api_key_env` 指定的环境变量中读取
   - **这条路径正确**

### 对比：providers 段和 fallback_providers 段

`load_config()` 对 `providers` 段和 `fallback_providers` 段做 `${VAR}` 展开，但 `delegation` 段**不在展开范围内**（可能是 bug 或设计遗漏）。

```python
# 验证方法
from hermes_cli.config import load_config
cfg = load_config()
# providers 段：api_key 已解析为实际值
print(cfg['providers']['volcano']['api_key'])  # ark-ccaa1a...
# fallback_providers 段：api_key 已解析
print(cfg['fallback_providers'][0]['api_key'])  # ark-ccaa1a...
# delegation 段：api_key 是字面量 ${ARK_API_KEY}（如果设了的话）
print(cfg.get('delegation', {}).get('api_key'))  # '${ARK_API_KEY}'
```

### 修复

从 delegation 段移除 `api_key` 行。省略后 `_resolve_delegation_credentials()` 返回 `api_key: None`，子agent 通过 `_build_child_agent()` 继承父 agent 已解析的 API key：

```python
# delegate_tool.py:1027
effective_api_key = override_api_key or parent_api_key
```

或更优：同时移除 `base_url`，只保留 `model` + `provider`，走 `resolve_runtime_provider` 路径。

## Bug B：credential pool 跨provider降级 401

### 根因

子agent 首选模型（如 `deepseek-v4-flash` on volcano）429 限额后，降级到 fallback 链中不同 provider 的模型（如 `dashscope/qwen3.7-flash`）。但 credential pool 仍用父 agent 的 API key（ARK_API_KEY）调 DashScope API，导致 401。

### 错误日志

```
WARNING run_agent: Credential pool provider mismatch: pool=custom:volcano, agent=custom - skipping pool mutation to avoid cross-provider contamination
```

这条 WARNING 说明 credential pool 检测到了 provider 不匹配，但选择"跳过"而不是切换 key，导致用错误的 key 调用 API。

### 排查方法

```python
# 在 execute_code 中验证凭据解析是否正确
import sys, os
sys.path.insert(0, r'D:\BaiduSyncdisk\AIKnowledgeBase\Hermesagent\.venv\Lib\site-packages')

# Load .env
env_path = os.path.expanduser('~/AppData/Local/hermes/.env')
with open(env_path) as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            os.environ[k] = v

from tools.delegate_tool import _load_config, _resolve_delegation_credentials

cfg = _load_config()
print("delegation config:", cfg)

class FakeParent:
    model = "glm-5.2"
    provider = "volcano"
    base_url = "https://ark.cn-beijing.volces.com/api/coding/v3"
    api_key = os.environ.get('ARK_API_KEY', '')
    api_mode = "chat_completions"

creds = _resolve_delegation_credentials(cfg, FakeParent())
for k, v in creds.items():
    if k == 'api_key' and v:
        print(f"  {k}: {v[:15]}...{v[-5:]} (len={len(v)})")
    else:
        print(f"  {k}: {repr(v)}")
```

### 区分 Bug A 和 Bug B

| 症状 | Bug A | Bug B |
|------|-------|-------|
| 子agent 用的模型 | delegation 配置的模型 | fallback 链最后的模型（如 qwen3.7-flash） |
| 401 错误的 API | 首选模型的 provider | fallback 模型的 provider（不同provider） |
| errors.log | 无特殊日志 | 有 `Credential pool provider mismatch` |
| _resolve_delegation_credentials 返回的 api_key | 字面量 `${...}` 或 None | 正确的 API key |
| 修复方法 | 移除 delegation.api_key | 升级 Hermes 或用同provider规避 |

### 当前临时方案

delegate_task 在 v0.16.0 上**完全不可用**。测试了4种配置全部 401：

| 配置 | 结果 | 原因 |
|------|------|------|
| volcano/deepseek-v4-flash + base_url + api_key: ${ARK_API_KEY} | 401 | Bug A（api_key 字面量） |
| volcano/deepseek-v4-flash + base_url（移除 api_key） | 401 | Bug B（降级到 dashscope 时用错 key） |
| volcano/deepseek-v4-flash（移除 base_url 和 api_key） | 401 | Bug B（同上，_resolve_delegation_credentials 返回正确 key 但 AIAgent 构造时被 credential pool 覆盖） |
| dashscope/qwen3.7-flash（完全不同 provider） | 401 | credential pool 仍用父 agent 的 volcano key（ARK_API_KEY）调 dashscope API |

`_resolve_delegation_credentials()` 在第4种配置下返回了正确的 DASHSCOPE_API_KEY（116字符，验证可用），但 AIAgent 构造时 credential pool 机制覆盖了正确的 key，改用父 agent 的 volcano key。

**实际降级方案**：跳过 delegate_task，用以下替代：
1. 第二层验证：用 cross_model_verify + 硬验证（对文本类交付物足够）
2. 并行调研：在主 agent 中用 terminal + curl 直接搜索（见 `references/github-api-research.md`）

### 根本方案

升级 Hermes 到 v0.19.0 **不能修复此 bug**。

已确认的 GitHub issues/PRs（2026.7.31 验证）：

| 编号 | 标题 | 状态 | 说明 |
|------|------|------|------|
| PR #41730 | fix(delegate): resolve custom-endpoint subagent pools by endpoint identity | ✅ 已合并入 v0.17.0 | 部分修复：不同 custom 端点不再被误判为相同。但不修复 credential pool key 泄漏 |
| Issue #68237 | Delegated Azure child can lease public OpenAI pool and send credential to wrong endpoint | ❌ OPEN (P2) | 核心问题：子agent credential pool 泄漏到错误端点 |
| PR #68240 | fix(delegation): keep credential pools endpoint-coherent | ❌ OPEN (P2) | 完整修复：阻止 credential pool 跨端点共享。截至 v0.19.1 未合并 |
| Issue #71410 | fix(hermes_cli): stop /model aliases from leaking the prior provider API key | ❌ OPEN | 相关：模型切换时 API key 泄漏 |

升级评估（依赖兼容性、config 迁移、技能影响）详见 `references/hermes-upgrade-impact.md`。
