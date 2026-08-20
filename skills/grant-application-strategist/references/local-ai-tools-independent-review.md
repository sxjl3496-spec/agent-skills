# 本地AI工具独立评审模式

> 来源：2026年8月2日会话（多轮迭代）
> 场景：用户要求将评审材料分发给多个AI工具做独立基金评审，用不同模型最大化模型多样性

## 一、概述

当用户要求用多个外部AI工具做独立评审时，需要：
1. 将客观材料写入一个Markdown文件（纯事实，不预设结论，见SKILL.md陷阱31）
2. PDF申报指南用PyMuPDF解析为Markdown存入Obsidian，路径在评审材料中标注
3. 多个工具并行执行（`terminal background=true`）
4. 每个工具的prompt相同，包含材料文件路径+评审问题清单
5. 等待全部完成后汇总报告

## 二、6模型并行评审模式（⭐ 2026.8.2 最终方案）

用户要求6种不同模型做最大模型隔离评审。最终方案：

| # | 执行通道 | 模型 | API来源 | 文件读取 |
|:---:|:---|:---|:---|:---|
| 1 | Claude Code (--print) | deepseek-v4-pro | DeepSeek API | ✅ 有 |
| 2 | OpenCode (run) | glm-5.2 | 火山方舟 | ✅ 有（仅当前目录） |
| 3 | OpenClaw (agent) | kimi-k2.6 | 火山方舟 | ❌ 需内嵌材料 |
| 4 | execute_code + requests | qwen3.7-max | DashScope | ❌ 材料作prompt传入 |
| 5 | execute_code + requests | qwen3.7-flash | DashScope | ❌ 材料作prompt传入 |
| 6 | execute_code + requests | kimi-k3 | Moonshot | ❌ 材料作prompt传入 |

### 关键设计原则

- 3个本地工具（1-3）有文件读取能力，可直接读取评审材料文件
- 3个API调用（4-6）用execute_code，材料作为prompt传入
- 6种模型来自4个不同厂商，实现最大模型隔离
- 所有agent用同一份材料、同一份prompt

## 三、三个本地工具的正确启动命令

### Claude Code

**关键**：`CLAUDE_CODE_GIT_BASH_PATH` 必须用 **Windows双反斜杠** 格式。

```bash
export CLAUDE_CODE_GIT_BASH_PATH="D:\\Redmi_Book14_software\\Git\\bin\\bash.exe"
cd /d/.../评审材料目录
/c/Users/sxjl3/AppData/Roaming/npm/claude.cmd --print "你的prompt"
```

**已知问题**：
- `claude` 命令不在PATH中，必须用完整npm路径
- **`--print` 传长prompt（>2000字符）会被静默截断**：Claude Code只收到部分内容，回复"没收到具体方向"。修复：将prompt写入文件，用 `PROMPT=$(cat file.txt)` 读取后传给 `--print "$PROMPT"`
- **`--allowedTools "Read,WebSearch,WebFetch,Write"` 参数**：不指定时Claude Code请求文件读取权限但无人交互时自动拒绝并退出。需要文件读取/搜索能力时必须显式声明此参数
- Claude Code会自动扫描工作目录，如果目录下有其他文件可能读取到错误文件。在目标目录运行，prompt中明确指定"请阅读文件 XXX.md"

### OpenCode

**关键**：用 `run` 子命令，不是 `--print` 参数。model参数格式 `--model "volcano/glm-5.2"`，model ID必须与opencode.json中models段的key完全一致。

```bash
cd /d/.../评审材料目录
/c/Users/sxjl3/AppData/Roaming/npm/opencode.cmd run --model "volcano/glm-5.2" "你的prompt"
```

**已知问题**：
- 外部目录读取需权限批准会自动拒绝，只能读当前目录文件。在prompt中明确告知"不需要读取其他文件"
- 火山方舟的model ID：配置文件中的key（如`glm-5.2`）可用，但底层ID（如`glm-5-2-260617`）报`ProviderModelNotFoundError`。API别名（kimi-k2.6、minimax-m2.7、glm-5.2等）可在curl中直接使用，但OpenCode的`--model`参数必须与opencode.json中models段的key完全一致
- **glm-5.2的thinking模式导致空回复**：API返回200但content为空，内容在reasoning_content中。需在请求中传`thinking: {"type": "disabled"}`关闭
- **火山方舟Coding Plan的`/models`端点只返回doubao系列模型**，不返回glm-5.2/minimax-m2.7/kimi-k2.6等别名。验证模型可用性需直接用curl调chat/completions测试

### OpenClaw

**关键**：`.bin/openclaw` 是shell脚本，不能直接 `node` 执行。用 `.cmd` 版本。长文本用 `--message-file` 避免参数过长。

```bash
export PATH="/d/.../OpenClaw/node/node-v25.9.0-win-x64:$PATH"
cd /d/.../OpenClaw/app

# 长文本用 --message-file（支持！--help 可查）
./node_modules/.bin/openclaw.cmd agent --local --agent main --message-file msg.txt
```

**已知问题**：
- `tools.profile="messaging"` 移除read/exec等20个工具，需改为 `"full"`。但即使改为full，agent仍可能报告"没有文件读取工具"（可能需要重启gateway）
- `.cmd`文件不展开bash的`$(...)`变量，用Python写临时文件再传
- `--message` 参数过长报"Argument list too long"，用 `--message-file <path>` 替代
- **`--message-file` 路径问题**：绝对路径（如`C:/Users/...`）可能找不到文件（ENOENT），建议用相对路径（在app目录下运行时用`msg.txt`）。先用Python将message文件写到app目录下
- kimi-k2-250905底层model ID有5小时配额限流（429），用别名kimi-k2.6不受此限
- **OpenClaw配置修改不即时生效**：修改`openclaw.json`后，正在运行的gateway可能仍用旧配置（类似Hermes的CLI_CONFIG模块级快照问题）。需重启OpenClaw进程

## 四、API直接调用评审模式（⭐ 关键：不要用cross_model_verify！）

### ⚠️ cross_model_verify 是"验证员"不是"评审员"

**严重陷阱**：用 `cross_model_verify` 脚本调DashScope API做评审，两个API都把评审材料当作"交付物"来检查质量，输出的是"材料完整性审查报告"而非"评审意见"。

**根因**：`cross_model_verify` 的system prompt隐含"你是验证员"角色，把content当作待验证的交付物处理。

**正确做法**：需要模型"基于材料做分析/评审"时，用 execute_code + requests 直接调API：

```python
import requests, os

session = requests.Session()
session.trust_env = False  # 关键：绕过系统代理

resp = session.post(
    "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "model": "qwen3.7-max",
        "messages": [{"role": "user", "content": f"你是评审专家。以下是材料：\n\n{material}\n\n请回答：..."}],
        "temperature": 0.7,
        "max_tokens": 8000
    },
    timeout=180
)
content = resp.json()["choices"][0]["message"]["content"]
```

### Moonshot kimi-k3 调用注意事项

- 必须设 `session.trust_env = False` 绕过代理，否则ProxyError
- `temperature` 必须为 `1`（其他值报400）
- `max_tokens` 建议8000（输出含reasoning_tokens）
- 可加 `"thinking": {"type": "disabled"}` 关闭推理模式

## 五、与delegate_task的降级关系

| 优先级 | 方案 | 模型隔离 | 上下文隔离 | 备注 |
|:---:|:---|:---:|:---:|:---|
| 1 | 本地AI工具（3种不同模型） | ✅ 完全 | ✅ 完全 | 三个不同AI工具，天然隔离 |
| 2 | execute_code + API直调（3种不同模型） | ✅ 完全 | ✅ 完全 | 3个不同厂商API |
| 3 | delegate_task 派子agent | ✅（需config配置） | ✅ | 同一Hermes框架 |
| 4 | cross_model_verify | ✅ | ❌ | ⚠️ 只能验证交付物，不能做评审 |

**降级触发条件**：本地工具启动失败时，降级到API直调或delegate_task。

## 六、评审材料文件制作要求

### 纯客观原则（⭐ 关键，见SKILL.md陷阱31）

1. **所有候选方向平等列出**，不标注任何主观标签
2. **即使之前已讨论过并达成共识，材料中也不能预设结论**
3. **逐条核对用户提及的所有方向是否全部包含**
4. **允许agent自提课题**："基于申请人的学术背景，你认为有没有比A-F更好的课题方向？"

### PDF解析存入Obsidian

```python
import fitz  # PyMuPDF
doc = fitz.open(pdf_path)
full_text = ""
for page in doc:
    full_text += page.get_text() + "\n"
# 写入Obsidian academia/目录
```

## 七、Claude Code长prompt传参修复（⭐ 2026.8.2 实测）

**问题**：通过 `--print "很长的prompt"` 传递超过约2000字符的prompt时，Claude Code可能只收到部分内容，回复"没收到具体方向"或列出方向让用户选择。

**修复**：将prompt写入文件，用bash变量读取后传入：

```bash
# 1. 将prompt写入文件
cat > /tmp/prompt.txt << 'EOF'
你是碳排放权交易领域的学术研究助手。请搜索最新文献...
（完整prompt内容）
EOF

# 2. 用变量读取后传给claude
PROMPT=$(cat /tmp/prompt.txt)
/c/Users/sxjl3/AppData/Roaming/npm/claude.cmd --allowedTools "Read,WebSearch,WebFetch,Write" --print "$PROMPT"
```

**适用场景**：调研任务、评审任务等prompt较长的场景。短prompt（<1000字符）直接用 `--print "..."` 即可。

## 八、已知问题汇总

| 问题 | 影响工具 | 解决方案 |
|:---|:---|:---|
| git-bash路径正斜杠 vs 双反斜杠 | Claude Code | 必须用`D:\\\\...\\\\bash.exe`格式 |
| `--print` 参数不存在 | OpenCode | 用`run`子命令 |
| shell脚本不能node执行 | OpenClaw | 用`.cmd`文件或`npx` |
| 参数过长 | OpenClaw | 用`--message-file <path>` |
| messaging profile移除read工具 | OpenClaw | 改profile为`"full"` |
| 火山方舟模型ID找不到 | OpenCode | API别名(如glm-5.2)可用，底层ID(如glm-5-2-260617)不可用 |
| Python代理失败 | execute_code | `session.trust_env = False` |
| cross_model_verify当评审员用 | execute_code | 用requests直接调API，不用cross_model_verify |
| kimi-k2-250905配额限流 | OpenClaw | 用别名kimi-k2.6 |
| Claude Code读取错误文件 | Claude Code | 在目标目录运行，prompt明确指定文件名 |
| **Claude Code长prompt被截断** | Claude Code | **将prompt写入文件，用`PROMPT=$(cat file.txt)`读取后传入** |
| **glm-5.2 thinking模式空回复** | OpenCode/火山方舟API | **请求中传`thinking: {"type": "disabled"}`关闭** |
| **OpenClaw --message-file绝对路径ENOENT** | OpenClaw | **用相对路径（在app目录下运行时用`msg.txt`）** |
| **OpenClaw配置修改不即时生效** | OpenClaw | **需重启OpenClaw进程** |
