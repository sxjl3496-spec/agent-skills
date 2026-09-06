# 模型隔离验证方案

## 问题

plan 技能阶段4的验证与执行可能使用同一模型，存在确认偏差。
delegate_task 工具本身不接受 model 参数，但子agent模型由 config.yaml 的 `delegation.model`/`delegation.provider` 控制。

**根因**：config.yaml 中 `delegation.model` 为空时，子agent继承主agent模型（无模型隔离）。
**修复**：显式设置 `delegation.model` 为不同模型（当前 deepseek-v4-flash via DeepSeek），子agent即获得模型隔离。

## 方案对比（2026.7.28 验证，2026.7.28 更新）

| 路径 | 原理 | 前置条件 | 模型隔离 | Agent能力 | 成本 | 状态 |
|------|------|----------|----------|----------|------|------|
| 1. execute_code + API | Python 直接调其他模型 API | API key（已有3个） | ✅ 完全 | ❌ 无工具 | 极低 | ✅ 可用 |
| 2. delegate_task agent隔离 | 独立子agent，模型由 delegation.model 控制 | config.yaml 设置 delegation.model | ✅ 不同模型 | ✅ 完整 | 正常 | ✅ 已配置 |
| 3. Claude Code --print | 调 claude -p 命令 | Claude Code + 认证 | 部分* | ✅ 完整 | 高** | ✅ 已安装 |
| 4. Copilot ACP | acp_command 切 Copilot 后端 | Copilot CLI + 订阅 | ✅ 完全 | ✅ 完整 | $10/月 | ❌ 未安装 |

\* Claude Code 底层用 DeepSeek V4 Pro（本机配置），非 Claude 原生
\** 每次调用系统提示词 23K tokens，简单验证约 $0.12

## 推荐方案：两层串行验证

```
路径1（execute_code 跨模型验证：模型隔离）
  ↓ 发现问题 -> 修复
路径2（delegate_task agent 隔离验证：模型+上下文双重隔离）
  ↓ 发现问题 -> 修复
终验（硬验证：实际运行/读取/测试）
  ↓ 通过
交付最终完成品
```

当前配置下两层验证使用不同模型：
- 第一层：qwen3.7-flash（DashScope/阿里）
- 第二层：deepseek-v4-flash（DeepSeek）via delegation.model
- 主agent：glm-5.2（火山方舟）

三者为三个不同厂商的模型，最大程度消除同模型确认偏差。

### 路径1：execute_code + 跨模型 API

**原理**：在 execute_code 中 import cross_model_verify.py，用不同模型的 API 审查交付物。

**可用 API（2026.7.28 验证通过）**：

| API | 环境变量 | Base URL | 默认模型 | 与 glm-5.2 不同厂商 |
|-----|---------|----------|----------|-------------------|
| DashScope | DASHSCOPE_API_KEY | https://dashscope.aliyuncs.com/compatible-mode/v1 | qwen3.7-flash | ✅ 阿里通义 |
| Moonshot | MOONSHOT_API_KEY | https://api.moonshot.cn/v1 | moonshot-v1-8k | ✅ 月之暗面 |
| DeepSeek | DEEPSEEK_API_KEY | https://api.deepseek.com/v1 | deepseek-chat | ✅ DeepSeek |

**推荐默认**：DashScope qwen3.7-flash（快、便宜、与 glm-5.2 完全不同厂商）

**注意**：DashScope 视觉模型（qwen-vl-max 等）免费额度已用完，需充值才可用。文本模型 qwen3.7-flash 正常可用。

**用法示例**：
```python
import sys
sys.path.insert(0, r"D:\BaiduSyncdisk\AIKnowledgeBase\Hermesagent\hermes-data\skills\plan\scripts")
from cross_model_verify import cross_model_verify

result = cross_model_verify(
    prompt="验证以下技能文件的步骤4.0是否包含两层验证机制...",
    content=open(r"path/to/deliverable.md").read(),
    api="dashscope",
    model="qwen3.7-flash",
)
if result["success"]:
    print(result["content"])
else:
    print(f"验证失败: {result['error']}")
```

**优点**：零安装、成本极低（只付 API token 费）、3+ 模型可选、完全可控
**缺点**：验证模型无自主工具能力（不能自己 read_file/跑命令），需主 agent 先把交付物内容塞进 prompt

### 路径2：delegate_task agent 隔离

**原理**：派独立子agent审查交付物，子agent有完整工具能力但看不到执行过程。

**模型控制**：子agent模型由 config.yaml delegation 段控制：
```yaml
delegation:
  model: deepseek-v4-flash
  provider: deepseek
  base_url: https://api.deepseek.com/v1
```
为空时继承主agent模型（无模型隔离）；设置后使用指定模型（模型隔离 + 上下文隔离）。

**用法示例**：
```
delegate_task(
    goal="你是独立审查员。验证以下交付物...",
    context="[原始需求]\n[交付物路径]\n[验收标准]",
    toolsets=["file", "terminal"]
)
```

**优点**：子agent有完整工具能力，能自己 read_file/跑命令；设置 delegation.model 后同时获得模型隔离
**缺点**：需在 config.yaml 显式配置 delegation.model，否则同主模型

### 路径3：Claude Code --print

**原理**：通过 terminal 调用 `claude -p "验证提示词"`，Claude Code 作为独立 agent。

**前置条件**：
- Claude Code CLI 已安装 ✅（@anthropic-ai/claude-code@2.1.78）
- 已认证 ✅（OAuth token）
- 注意：当前配置底层用 DeepSeek V4 Pro，非 Claude 原生

**用法示例**：
```bash
~/AppData/Roaming/npm/claude -p --output-format json "验证以下文件..." --allowedTools "Read,Bash"
```

**优点**：完整 agent 能力（read_file/terminal），独立上下文
**缺点**：系统提示词 23K tokens，单次验证约 $0.12，成本高；路径2 已实现模型隔离后通常不需要

### 路径4：Copilot ACP

**原理**：delegate_task 传 acp_command="copilot"，子agent切到 Copilot ACP 后端。

**前置条件**：
- @github/copilot CLI ❌ 未安装
- Copilot 订阅 ❌ 未购买

**优点**：完整 agent 能力 + 不同模型（Claude/GPT-4）
**缺点**：需 $10/月订阅，安装配置复杂；路径2 已满足需求

## 环境验证记录

```
验证时间: 2026.7.28
DeepSeek:    ✅ deepseek-v4-flash
DashScope:   ✅ qwen3.7-flash, qwen3.7-max (文本模型正常; 视觉模型 qwen-vl-max 免费额度已用完)
Moonshot:    ✅ kimi-k2.6 等
Ark:         ❌ 404 (需端点ID非模型名)
Xiaomi:      ❌ DNS解析失败
Claude Code: ✅ 已认证 (OAuth, 底层DeepSeek V4 Pro)
Copilot ACP: ❌ 未安装
```
