---
name: obsidian-vault-archiving
description: >
  将外部文档（txt/pdf/html/大段文本）转化为结构化 Obsidian 知识库笔记。
  适用场景：(1) 用户提供一份大型文档文件路径，要求"存档/归档/方便检索"，
  (2) 将 API 文档/模型列表/技术手册压缩为 AI 可快速检索的 Markdown 笔记，
  (3) 用户问"以后能否从网上搜集信息更新"时，评估和执行 web 更新。
  不适用：用户只要求总结一段文字（直接回复即可，无需写入 Vault）。
---

# Obsidian 知识库归档

## 触发条件

**场景A（文档归档）**：用户提供文档文件路径 + 要求"存档/归档/方便检索/做成知识库"时触发。
典型输入格式：`polish "D:\...\xxx.txt" 这是...需要你做成方便你检索的知识库形式`

**场景B（研究入库）**：用户要求调研某主题 + 将结果"做成文档存入知识库/Obsidian"时触发。
典型输入格式：`/plan auto 帮我详细调查XX，做成文档存放在obsidian知识库中`
此场景下，先调研（GitHub API + Google 搜索，详见 plan 技能 `references/github-api-research.md`），再按下面的多文档入库流程写入 Vault。

> **⭐ 调研类任务默认沉淀知识库（2026.8.6 用户纠正）**：调研/调查类任务（含 /plan 制定的调研计划）**默认**要把详细结果写入知识库，不能只输出在对话里。用户原话："调查的详细信息要总结到AI知识库中的hermes里面呀"。制定调研计划时就把"写入知识库"列为独立步骤，先 `search_files` 查 Vault 对应分类目录（如 `🤖 AI Agent/01-Hermes/`）沿用现有命名，对话里只发摘要+文件路径。除非用户明确说不用写。

> **注意**：用户使用 "polish" 一词时，不是触发 expression-polish 技能，而是"处理/加工这份文档"的意思。仅在 `\polish：` 前缀（反斜杠+冒号）时才触发 expression-polish。

## Vault 结构

```
<Obsidian库>\\
├── 🤖 AI Agent/          # AI 相关文档
│   ├── 07-API与配置/     # API 文档、模型计费、配置说明
│   ├── 01-Hermes/        # Hermes Agent 使用说明
│   ├── 02-Claude Code/
│   ├── 03-Codex/
│   ├── 04-OpenCode/
│   └── 05-OpenClaw/
└── 🏭 铁粉厂/            # 工厂经营相关
    ├── 经营/
    ├── 原料/
    ├── 客户/
    └── 环保脱硫方案/
```

**路径注意**：D 盘写操作需管理员权限。如遇权限问题，用 `write_file` 工具（非 terminal echo/cat）。

## 归档流程

### 步骤1：源文件分析

1. 用 `terminal` 检查文件大小（`ls -la` 或 `wc -l`）
2. 用 `read_file` 读取前 100 行了解文档头部和格式
3. 用 `execute_code` 扫描全部标题行（`#`、`##`、`###`），构建目录树
4. 统计总行数，判断是否需要分段读取

**判断标准**：
- <500行：一次 read_file 读完
- 500-5000行：分段读取关键章节
- >5000行：只读标题 + 定位关键章节读取（如定价表、模型列表、API 示例）

### 步骤2：内容提取

按文档类型提取关键内容：

| 文档类型 | 提取重点 | 可丢弃 |
|---------|---------|--------|
| API 文档 | 模型ID、端点URL、参数表、代码示例 | Node.js 代码（保留 Python）、HTML 标签、截图 URL |
| 模型计费 | 定价表（主地域）、免费额度、计费规则 | 国际/美国/欧盟地域的重复定价表（保留北京+全球） |
| 技术手册 | 架构图、配置项、命令列表 | 冗余说明、营销文案 |
| 通用文档 | 关键概念、流程步骤、结论 | 重复段落、过渡语句 |

**核心原则**：保留"AI 检索时有用的信息"（模型ID、价格、代码、参数），丢弃"只有人类阅读时才需要的格式"（多语言重复、HTML 标记、截图链接）。

### 步骤3：结构化重组

按以下模板组织内容：

```markdown
---
title: [文档标题]
tags:
  - [主题标签1]
  - [主题标签2]
  - API/hermes/参考文档  # 按需选择
source: [原始来源URL或说明]
archived: [YYYY-MM-DD]
---

# [文档标题]

> 来源：[说明]
> 原始文件：`[路径]`（[行数]行，[大小]）
> 本笔记为 AI 优化版：[压缩说明]

## 快速导航

| 主题 | 章节 |
|------|------|
| ... | [[#章节名]] |

---

## [按主题组织的章节...]

## 关于自动更新

[如果用户问能否更新，在此说明能力和限制]

## 相关笔记

- [[相关笔记1]] - 简要说明
- [[相关笔记2]] - 简要说明
```

### 步骤4：写入与验证

1. 用 `write_file` 写入目标路径（选择正确的 Vault 子目录）
2. 验证：`terminal` 检查文件大小和行数
3. 确认 YAML frontmatter 格式正确（tags 列表）
4. 确认 Obsidian wiki-links `[[笔记名]]` 指向已存在的笔记

**目标大小**：压缩后 15-25KB（原始文件可能 200KB-4MB）。过大会降低 AI 检索效率，过小会丢失关键信息。

### 已归档文档清单

| 文档 | 原始大小 | 归档大小 | 路径 |
|------|---------|---------|------|
| Kimi API 使用手册 | 210KB/4401行 | 18KB/591行 | `07-API与配置/Kimi API 完整使用手册.md` |
| 阿里百炼模型总览 | 4.2MB/91054行 | 21KB/582行 | `07-API与配置/阿里百炼模型总览与计费手册.md` |
| MiniMax API 使用手册 | 506KB/20434行 | 12KB/37章节 | `07-API与配置/MiniMax API 使用手册.md` |

> MiniMax API 端点实测验证：2026.8.4 进一步验证了图片识别（M3通过`/anthropic/v1/messages`传image类型）和图片生成（`/v1/image_generation`同步返回URL）均可用。MiniMax base_url必须用`/v1`（OpenAI兼容）而非`/anthropic`（Anthropic兼容），后者会导致Hermes和AionUi请求格式不匹配。查询端点为`GET /v2/query/video_generation/{task_id}`（非直觉路径）。MiniMax-H3视频生成按次计费较贵，路由中放DashScope wanx2.1之后作兜底。

> MiniMax API 端点实测验证结果（含图片识别/图片生成/视频生成的代码示例和错误端点列表）见 `references/minimax-api-verified-endpoints.md`
> MiniMax + AionUi 多provider配置（含127模型污染修复）见 `ai-app-provider-config` 技能 `references/minimax-aionui-multi-provider.md`

### 陷阱6：API 文档中查询端点路径与实际不符 -- 需获取 OpenAPI Spec 验证 ⭐

从官网复制的 API 文档可能不包含所有端点的完整路径，或者路径有误。**不要靠猜，去取 OpenAPI Spec**。

**真实案例（2026.8.3）**：MiniMax H3 视频生成任务创建成功（`POST /v2/video_generation` 返回 task_id），但查询端点路径不确定。文档中只写了"查询任务"接口，没有明确路径。尝试了 6 种猜测路径全部 404：
- `/v2/video_generation/{task_id}` ❌
- `/v2/video_generation?task_id=xxx` ❌
- `/v2/query` ❌
- `/v2/video_generation/query` ❌

**解决方法**：从官方文档的 llms.txt 索引找到 API 文档的 markdown 文件 URL，获取 OpenAPI YAML spec：
```python
import requests
session = requests.Session()
session.trust_env = False

# 1. 获取文档索引
resp = session.get("https://platform.minimaxi.com/docs/llms.txt", timeout=15)
# 在返回内容中搜索 video-generation-v2-query.md 的 URL

# 2. 获取该接口的 markdown 文档（含 OpenAPI YAML spec）
resp = session.get("https://platform.minimaxi.com/docs/api-reference/video-generation-v2-query.md", timeout=15)
# 在返回的 YAML 中找到正确路径：GET /v2/query/video_generation/{task_id}
```

**通用模式**：当 API 端点路径不确定时：
1. 查找官方文档站点的 `llms.txt` 或 `docs/llms.txt` 索引文件
2. 从索引中找到对应接口的 `.md` 文件 URL
3. 获取该 `.md` 文件，其中通常包含 OpenAPI YAML spec，有完整的 `paths:` 定义
4. 从 YAML 的 `paths:` 字段提取正确的端点路径和 HTTP 方法

**已验证的 MiniMax API 端点**（2026.8.3 实测）：
| 接口 | 正确端点 | 方法 |
|:---|:---|:---:|
| 创建视频任务 | `/v2/video_generation` | POST |
| 查询视频任务 | `/v2/query/video_generation/{task_id}` | GET |
| 语言模型（推荐） | `/anthropic/v1/messages` | POST |
| 语言模型（OpenAI兼容） | `/v1/chat/completions` | POST |

> 注意：MiniMax API 的查询端点用的是 `/v2/query/video_generation/{task_id}` 而非直觉上的 `/v2/video_generation/{task_id}`。这种"查询端点不在资源路径下"的设计模式在其他 API 中也可能出现。

## 关于自动更新

用户可能问"以后信息更新了，你能否从网上搜集来更新知识库"。

**能做到的**：
1. 用 `web_search` 搜索官方文档页面，抓取最新模型列表和定价
2. 用 `browser` 工具访问动态渲染页面（如百炼文档）
3. 对比现有笔记内容，发现新增/下线/调价的模型
4. 更新 Obsidian 笔记

**限制**：
1. 动态渲染页面可能需要 browser 工具而非简单 HTTP 请求
2. "限时折扣"变化频繁，需定期核对
3. 无法查询用户私有数据（余额、用量）

**建议方案**：
1. 手动触发：用户说"更新XX模型库"时执行
2. 定时 cron：每月1日自动抓取对比，有变化时通知用户
3. 即时查询：需要某模型参数时直接搜索补充

## 多文档研究入库流程

当任务是"调研某主题 -> 写入 Vault"时（场景B），使用以下流程：

### 步骤1：调研

1. 用 GitHub API 搜索相关仓库（`curl -s "https://api.github.com/search/repositories?q=KEYWORDS&sort=stars"`）
2. 获取关键仓库的 README（`curl -s "https://api.github.com/repos/OWNER/REPO/readme"` + base64 解码）
3. **获取仓库内特定文件**（Contents API）：README 之外的文件（如 SKILL.md、eval.md、配置文件、源码）可通过 Contents API 获取。研究 Agent Skill / 技术项目时，README 通常只有安装说明，真正的规则逻辑在仓库内部文件中。完整方法和代码模板见 `references/github-contents-api.md`（含模糊名称恢复策略、Raw API、限流管理、execute_code+requests 批量搜索模式）。
4. **多源整合**：深度调研时不应只依赖 GitHub，还需从 ArXiv（论文摘要）、项目主页（性能数据）、HuggingFace（数据集元信息）获取互补信息。完整的多源获取流程、限流管理、数据完整度评估清单见 `references/multi-source-research-integration.md`。
5. **学术论文文献检索**：使用 Crossref API（`api.crossref.org/works`）搜索期刊论文，无 token 无限流，适合批量搜索。Semantic Scholar 限流严格（429 频发），Crossref 作为首选。详见 `references/academic-and-github-research.md`。
6. **GitHub 项目批量调研**：用 execute_code 中的 `fetch_github_repo()` 函数一次获取仓库基本信息+README+文件结构+package.json+commits+releases，比 terminal curl 批量调用更可靠。详见 `references/academic-and-github-research.md`。
   ```bash
   curl -s "https://api.github.com/repos/OWNER/REPO/contents/path/to/file.ext" \
     | python -c "
   import sys, json, base64
   d = json.load(sys.stdin)
   if 'content' in d:
       content = base64.b64decode(d['content']).decode('utf-8', errors='ignore')
       print(content[:8000])
   else:
       print('Not found:', d.get('message', 'error'))
   "
   ```
   - 先用 README 中的 "Files" 或 "Repo layout" 章节定位文件路径
   - 可在一个 terminal 调用中并行获取多个文件（多个 curl 用 `&` 连接）
   - 如果路径是目录而非文件，API 返回该目录下的文件列表 JSON 数组
4. 如需 Google 搜索，走 Clash 代理（`curl -s -x http://127.0.0.1:<代理端口> "https://www.google.com/search?q=QUERY"`）
5. 批量搜索：一个 terminal 调用中 for 循环搜索多个子主题
6. **并行获取多仓库数据**：在同一个回复中发出多个 terminal 调用（每个获取不同仓库的 README/内部文件），结果并行返回。典型模式：5个仓库 = 5个 terminal 调用并行，约10秒完成全部获取

### 步骤2：规划文档结构

- 每个子主题一篇独立文档
- 加一篇综述文档（对比表 + 关系图 + 交叉引用）
- 文档命名：`01-主题A.md`、`02-主题B.md`、`综述.md`（数字前缀控制排序）
- 在 Vault 中创建新子目录（如 `09-新分类/`）

### 步骤3：写入文档

每篇文档包含：
- YAML frontmatter（tags、created、updated、sources）
- **数据完整性声明**（见下方"数据完整性声明"小节）-- 用户明确要求：研究入库时必须标注哪些资料已获取、哪些未获取，以及后续补充路径
- 定义与核心理念
- 技术架构
- 代表项目（含 GitHub 链接、star 数）
- 应用场景
- 优缺点对比
- Obsidian 双链 `[[]]` 交叉引用

#### 数据完整性声明（研究入库必须项）

当笔记基于在线调研（而非用户提供的一手文档）时，必须在笔记开头（YAML frontmatter 之后、正文之前）加入数据完整性声明。用户原话："因为你拿到的不是详细完整的数据，你需要强调这样一点，后续需要补充详细数据的时候应该去哪搜索，这不要漏掉了"。

声明包含两部分：

**1. 已获取资料表**（标注完整度）：
```
| 资料 | 来源 | 完整度 |
|------|------|--------|
| README.md | GitHub API | 完整（5207字符） |
| core/analyzer.py | GitHub API | 完整（9.2KB） |
| 论文全文PDF | 未获取 | 需代理下载 |
```

**2. 未获取资料及补充路径表**（标注获取方法+优先级）：
```
| 待补充资料 | 获取路径 | 优先级 |
|-----------|---------|--------|
| 论文全文PDF | https://arxiv.org/pdf/XXXX （需Clash代理） | 高 |
| 某核心源码 | git clone 后本地阅读 | 高 |
| 数据集完整内容 | huggingface-cli download | 中 |
```

**3. 后续补充操作步骤**（具体命令，可直接复制执行）：
```bash
# 方法1：完整克隆仓库
git clone https://github.com/OWNER/REPO.git

# 方法2：GitHub API 单文件获取
# 格式: https://api.github.com/repos/OWNER/REPO/contents/{path}

# 方法3：下载论文PDF（需代理）
curl -x http://127.0.0.1:<代理端口> -L -o paper.pdf https://arxiv.org/pdf/XXXX
```

**关键原则**：
- 声明的目的是让未来打开笔记的人（或AI）立即知道数据边界在哪、去哪补全
- 优先级标注帮助判断哪些补充最有价值
- 操作步骤必须具体可执行（含URL、代理端口、命令），不能只写"去GitHub上看"
1. 硬验证：检查每个文件存在、行数、维度覆盖（5维度齐全）
2. 交叉验证：双链指向的文件是否存在
3. 跨模型验证（plan 技能的 cross_model_verify.py）

### 已入库研究文档

| 主题 | 文档数 | 路径 |
|------|--------|------|
| Agent 工程方法论 | 6篇（综述+5篇专题） | `🤖 AI Agent/09-Agent工程方法论/` |
| No-AI-Slop 生态调研 | 1篇（364行/18KB） | `🤖 AI Agent/No-AI-Slop 生态调研.md` |
| Resource2Skill 调研 | 1篇（29413字符/42KB） | `🤖 AI Agent/Resource2Skill - 微软多模态资源蒸馏Agent技能框架.md` |
| OfficeCLI + AionUi 技术文档 | 2篇（17KB+12KB） | `🤖 AI Agent/OfficeCLI技术文档.md` + `AionUi技术文档.md` |
| OfficeCLI + AionUi GitHub调研 | 原始数据+README+SKILL.md | `hermes-data/cache/` 下 `ocli_readme_zh.md`、`ocli_skill.md`、`aionui_readme.md` |

---

## 常见陷阱

### 陷阱1：用户记错项目名导致搜索 0 结果

用户提供的项目名可能不准确（如将"Resource2Skill"记成"Resource25Skill"）。当 GitHub 精确搜索返回 0 结果时，不要直接告诉用户"找不到"。应逐步放宽搜索：拆分关键词、去掉数字、用连字符变体做宽泛搜索。详见 `references/github-contents-api.md` 中的"模糊名称恢复策略"。

### 陷阱2：GitHub API 限流导致深度调研中断

无 token 的 GitHub API 限流为 60 请求/小时。深度调研一个项目（README + 15个源文件 + 目录结构）会快速耗尽。策略：优先获取目录结构（1次调用返回全部文件列表），用 `Accept: application/vnd.github.raw` header 直接获取文件原文（跳过 base64），限流后切换到 Google 搜索 + 项目主页 HTML 解析。详见 `references/github-contents-api.md` 中的"GitHub API 限流管理"。

### 陷阱3：README 只覆盖安装说明，核心逻辑在仓库内部文件中

研究技术项目时，README 通常只有安装和快速开始说明，真正的架构设计、核心逻辑、配置规则在仓库内部文件中（如 `core/*.py`、`domains/*/domain.yaml`、`SKILL.md`）。获取 README 后应继续获取目录结构，定位核心文件再逐个获取。详见 `references/github-contents-api.md`。

### 陷阱4：网页复制文档的转义符、HTML 标签和重复段落

用户从官方文档网站直接复制粘贴的大段文本（如 API 文档、模型介绍）通常包含三类问题：

1. **Markdown 转义符**：`\*`、`\#`、`\[`、`\]`、`\_`、`\\` 等。网站渲染器需要这些转义符，但存入 Obsidian 后显示为乱码。
2. **HTML 自定义标签**：`<Accordion title="历史模型">`、`<Card title=...>`、`<Columns cols={2}>`、`<Note>`、`&#x20;` 等。这些是文档站框架组件，Obsidian 不识别。
3. **大段重复**：用户可能多次复制不同页面，但每个页面都包含相同的导航/概览段落。真实案例：MiniMax 文档 20,434 行中"接口概览"段落重复了 4 次，"语言模型"出现 13 次。

**清理流程**：
1. 用 `execute_code` 扫描全部标题行（`#{1,3}`），构建目录树
2. 统计每个关键章节出现的次数（如 `content.count('接口概览')`），识别重复
3. 取每个唯一标题的**第一次出现**的内容，丢弃后续重复
4. 清理转义符：`clean = content.replace('\\*', '*').replace('\\#', '#').replace('\\_', '_').replace('&#x20;', ' ')`
5. 清理 HTML 标签：替换或删除 `<Accordion>`、`<Card>`、`<Columns>` 等
6. 重组为结构化手册格式（表格+代码块+章节层级）

**压缩比参考**：MiniMax 文档从 506KB/20,434 行 → 12KB/37 章节，压缩比 2.4%。关键是丢弃了 4 次重复的概览段落和大段 OpenAPI YAML 定义。

### 陷阱5：跨模型验证截断导致假阴性（长笔记验证时）

当 Obsidian 笔记较长（>8000字符）时，cross_model_verify 传入的 content 会被 API token 限制截断。验证器只看到笔记前半部分，报告"维度X缺失"或"迁移路径不足"，但实际该内容在笔记后半部分是完整的。

**真实案例（2026.8.3）**：Resource2Skill 笔记（29413字符）用 moonshot-v1-8k 验证，迁移路径维度评3/5分称"缺少优先级排序"。实际笔记第8节有完整的"短期/中期/长期"三级表格+优先级总览矩阵，只是排在8000字符截断点之后。

**预防**：
1. 验证前预估笔记长度，超过8000字符时只传关键段落（如章节标题+首段），不要传全文
2. 如果验证报告"XX缺失"但你在撰写时确认写过该内容，先怀疑截断，用 read_file 确认内容存在
3. 可将关键内容（如优先级矩阵）前移到笔记前半部分，提高验证可见性
4. 硬验证（execute_code 脚本检查章节存在性+关键内容标记）不受截断影响，应作为最终判断依据

---

## 注意事项

- **D盘权限**：Vault 在 D 盘，写操作需管理员权限。`write_file` 工具可处理，但 terminal 直接写可能失败
- **中文路径**：Git Bash 中中文路径需用引号包裹，如 `"<知识库根目录>/.../🤖 AI Agent/..."`
- **现有笔记检查**：归档前先检查 Vault 中是否已有同主题笔记（用 `search_files` 搜索关键词），避免重复
- **用户偏好**：用户通过飞书沟通时，任何 AI 工具相关问题都应主动检索 Vault
