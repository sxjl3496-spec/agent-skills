---
name: skill-import
description: >
  从 GitHub 调研并导入现成 Agent 技能（Claude Code/Codex/Cursor 生态）到 Hermes 技能库。
  覆盖：排行榜/截图技能识别 → GitHub 仓库定位与克隆 → SKILL.md 兼容性检查 →
  安装到 skills/ 目录 → hermes skills list 验证 → 知识库沉淀解读文档 →
  借鉴点提炼并回写现有技能。
  触发词：导入技能、安装技能、迁移技能、技能调研、排行榜技能、GitHub技能、
  克隆技能仓库、外部技能、技能解读。
---

# 技能导入 (skill-import)

从 GitHub 导入现成 Agent 技能到 Hermes 技能库的完整流程。
与 skill-distiller（从教程/文档蒸馏新技能）互补：本技能处理**已存在的现成技能**的调研、安装、沉淀、借鉴。

## 触发场景

- 用户提供技能排行榜/截图，要求"都值得装"、"去github调查了解"、"写入知识库方便迁移"
- 用户点名某技能（如 Superpowers、Taste-Skill、Impeccable）要求引入
- 需要从 anthropics/skills、openai/skills 等官方仓库取技能

## 完整流程（5步）

> **⭐ 用户要求的顺序**（2026-08-05 两轮明确指示"解析好放在知识库再安装，再借鉴改进"）：调研 → 知识库解读文档 → 安装 → 借鉴回写。即**先写解读文档、后安装**。但实际执行中"对比现状"（步骤3前半）需在写文档前完成以确定安装清单，故流程为：调研 → 对比现状定安装清单 → 写解读文档 → 安装验证 → 借鉴回写。解读文档必须先于安装产出，不能装完再补文档。

### 步骤1：GitHub 调研（定位仓库）

**先精确搜索，再批量确认**：

```python
# GitHub API 搜索（匿名限流 60次/小时，注意节奏）
https://api.github.com/search/repositories?q=<关键词>&sort=stars&per_page=5
```

**⚠️ 匿名 API 限流**：连续搜索约 10 次后触发 `403 rate limit exceeded`。
**绕过方法：直接 git clone 仓库到本地调研，不受 API 限流影响**：

```bash
mkdir -p <hermes-data>/skills_research && cd skills_research
git clone --depth 1 https://github.com/<org>/<repo>.git
```

**已知官方/顶级技能仓库**（2026.8 验证）：

| 仓库 | 内容 | 备注 |
|------|------|------|
| `obra/superpowers` | ★266K 全流程方法论，14子技能 | skills/ 下每个子目录独立 SKILL.md |
| `anthropics/skills` | ★166K mcp-builder/frontend-design/skill-creator 等 | skills/skills/ 下 |
| `openai/skills` | figma-implement-design 等 | 在 `.curated/` 子目录 |
| `composio-community/awesome-codex-skills` | ★15.5K 47个技能 | 仓库根目录即技能目录 |
| `Leonxlnx/taste-skill` | ★71.8K 反Slop前端框架 | skills/ 下13个子技能 |
| `DevvGwardo/impeccable` | 23命令前端设计 | **Hermes原生移植版**，天然兼容 |
| `addyosmani/agent-skills` | ★81.6K 生产级工程技能23个 | 谷歌Chrome团队；skills/ 下，spec/source/doubt-driven 等最值得引入 |
| `kepano/obsidian-skills` | ★44K Obsidian CLI+Markdown+Bases | Obsidian CEO 出品；skills/ 下 |
| `Imbad0202/academic-research-skills` | ★40.8K 学术研究流水线 | 13-agent deep-research、5审稿人 reviewer |
| `coreyhaines31/marketingskills` | ★43K 营销技能30+ | skills/ 下，ai-seo(AEO/GEO/LLMO)/cold-email 等 |
| `K-Dense-AI/scientific-agent-skills` | ★32.6K 科学家技能2383文件 | 每个科学库一个SKILL.md，体量大 |
| `Master-cai/Research-Paper-Writing-Skills` | ★5.8K ML/CV/NLP论文写作 | research-paper-writing（段落清晰度/反向提纲/9条全局原则） |
| `zLanqing/codex-claude-academic-skills` | ★2.6K 中文优先学术技能 | 3技能：office-academic(Word/PPT)、research-writing(含rebuttal)、scientific-toolkit(243文件科学计算) |
| `PrathamLearnsToCode/paper2code` | ★1.5K arXiv论文转代码 | 5阶段pipeline + guardrails防幻觉；skills/paper2code/ 下 |
| `u7079256/paperjury` | ★875 CS会议投稿前审稿 | CVPR/ACL/NeurIPS；DIRECT-EDIT/REVIEW/AUTO三模式，共识门控修改 |
| `WantongC/journal-adapt-writing-skill` | ★738 期刊惯例学习 | 动态写作技能生成器；skill/SKILL.md；HARD RULES不添事实/不转述文献 |
| `ndpvt-web/latex-document-skill` | ★681 通用LaTeX | 27模板+27脚本+26参考；CJK自动XeLaTeX；单agent 1-10页经验 |
| `delibae/claude-prism` | ★1.7K 离线科学写作 | 重依赖本地工具链，暂缓安装 |
| `lishix520/academic-paper-skills` | ★1.1K 系统写作框架 | 与Hermes现有composer/strategist重复，仅对照 |
| `bytedance/deer-flow` | 字节DeerFlow 2.0 super agent harness | **`skills/public/` 下21个公开技能**：deep-research/paper-research/data-analysis/ppt-generation/skill-creator/github-deep-research 等，科研+通用全覆盖；MIT；应用本体35M(backend+frontend+Docker)单独部署，技能部分纯SKILL.md直接可装（中文本地化镜像 `stophobia/deerflow2.0-enhanced`） |
| `jakubkrehel/skills` | ★3K better-UI系列7子技能 | accessibility/colors/interface/layout/typography/ui/writing；与taste-skill(审美)+impeccable(反模式)组成UI质量三件套 |
| `AminBlg/SimpleEnglish` | ★1.6K ASD-STE100简化技术英语 | **自带evals/评测**（pressure-tests+RESULTS.md）——开源技能"有评测有结果"范例，借鉴点回写verify技能 |
| `icebird1998/drawio-scientific-illustrator` | ★1.3K draw.io科研绘图MCP | 实时操控draw.io画布画科研图；需要draw.io桌面版+MCP插件（运行时依赖，装技能前标注） |
| `Intuition-Lab/personal-model` | ★1.3K AI记忆档案(Persome) | **macOS守护进程依赖，Windows无法安装**——仅借鉴理念（可审计记忆/Point-Line-Face-Volume分层/HUMAN.md），不装为技能 |

**GitHub API 高星搜索技巧**：`api.github.com/search/repositories?q=<关键词>&sort=stars&per_page=10` 一次性可搜多组关键词（"agent skill"、"claude code skill"、"awesome agent skills"），去重后按 star 筛选候选。

**⚠️ 发现"新项目"不要用 sort=stars**（⭐ 2026.8.5 实测）：`sort=stars` 永远返回同一批头部老项目（superpowers ★266K、langchain ★143K 等霸榜），无法发现近期新冒出来的项目。要发现近30天的新仓库，用**时间过滤 + stars 排序**组合：

```python
since = (date.today() - timedelta(days=30)).isoformat()
# 4路并行搜索不同类别（agent/skill/mcp/framework），各自取前10
queries = [
    (f"AI agent created:>{since}", "agent"),
    (f"agent skills created:>{since}", "skill"),
    (f"MCP created:>{since}", "mcp"),
    (f"agent framework created:>{since}", "framework"),
]
# 合并去重（seen JSON + Excel 双缓存）→ 按 stars 降序 → 取前 MAX（如12）
# 实测效果：QwenAudio/qwen-audio-agent ★1887、drawio-scientific-illustrator(MCP) ★1260 等全是近30天新项目
```

完整实现见 `references/hermes-arxiv-agent-deployment.md` 的 GitHub 监控节（github_monitor.py 模式：4路搜索/去重缓存/星标门槛/推荐度分级⭐👍👀）。此模式同样适用于任何"发现新开源项目"的监控/调研场景。

**URL 编码**：GitHub Search API 查询串含空格时，用 `urllib.parse.quote()` 编码后再拼 URL，否则 `urlopen` 报 "URL can't contain control characters"。requests 库则自动处理。

**GitHub 仓库名冲突**：多个仓库都叫 skills → 克隆时指定目标目录 `git clone ... openai_skills`。

### 步骤2：读取核心文件（评估价值）

```bash
# 看技能清单和定位
ls <repo>/skills/ 或 ls <repo>/
cat <repo>/skills/llms.txt 2>/dev/null   # 部分仓库有技能索引
head -80 <repo>/skills/<name>/SKILL.md   # 看 frontmatter + 核心方法
```

评估要点：定位、触发条件、方法论核心、附属资源（references/scripts）、依赖（Figma MCP、gh CLI 等）。

### 步骤3：对比现状 + 安装

**先检查 Hermes 是否已有**：
```bash
hermes skills list | grep -iE "<关键词>"
```

**安装 = 复制目录**（Claude/Codex 标准 SKILL.md 与 Hermes 兼容，无需转换）：
```bash
SKILLS_ROOT=<hermes-data>/skills
# 单个技能 → 分类目录
cp -r <repo>/skills/<name> "$SKILLS_ROOT/<category>/"
# 技能包（多子技能）→ 新建分类
mkdir -p "$SKILLS_ROOT/<package-name>"
cp -r <repo>/skills/* "$SKILLS_ROOT/<package-name>/"
```

**frontmatter 兼容性检查**（必做）：
```bash
head -5 <技能>/SKILL.md | grep -E "^(name|description):"
```
name + description 必须有；license/metadata 可选兼容。

### 步骤4：验证识别 + 知识库沉淀

```bash
hermes skills list | grep <技能名>   # 应显示 enabled
```

**知识库沉淀**（用户要求，方便迁移教学）：写入
`ObsidianVault/🤖 AI Agent/09-Agent工程方法论/技能详细解读与构造/`：
- 每技能一篇 `NN-<技能名>解读.md`：基本信息(仓库/Star/定位) → 核心机制 → 与现有技能对比 → 可借鉴提升点 → 安装状态
- 更新 `技能详细解读与构造-总览.md` 的技能解读表 + 安装位置
- 更新 `NN-外部技能与Hermes现有技能对比矩阵.md` 的借鉴优先级表（标状态）

**⚠️ 开源敏感技能排除**（用户 2026-08-05 指示，技能库准备开源）：写入知识库的技能解析**必须排除**涉及个人信息/家庭经营/职业背景的技能——`iron-powder-business`（铁粉厂）、`family-factory-advisory`（家庭工厂）、`bank-strategic-research-report`（银行战略）可安装使用，但**不得**写入知识库解读文档。仅可在"排除声明"中列出名称说明为何不收录。筛选规则：技能描述含家庭经营、个人职业、亲属、财务细节的→不写入知识库。

### 步骤5：借鉴点回写（把价值留在技能库）

从解读中提炼的借鉴点**不能只写文档**，要回写到目标技能：
- 门禁/铁律类 → 补进对应技能（如 verify 加证据先行、debug-helper 加根因不修复）
- 模板类 → 补进生成模板（如 plan 加 Scope/Open questions、skill-distiller 加依赖声明）
- 回写后验证：`grep -c "<关键词>" <技能>/SKILL.md`

## 常见陷阱

1. **GitHub API 匿名限流**（403）：不要死磕 API 搜索，改用 git clone 直接拉仓库
2. **仓库名冲突**：clone 时显式指定目标目录名
3. **依赖标注**：部分技能依赖外部工具（Figma MCP、gh CLI 认证），安装时在解读文档中标注清楚，未配置前作为方法论参考
4. **改动触发词需重载**：修改技能 name/description 后需 `/reload-skills` 或新会话才重新注册斜杠命令；只改正文则实时生效
5. **知识库目录已固定**：技能解读体系在 `09-Agent工程方法论/技能详细解读与构造/`（2026.8.5 从顶层移入），不要另建位置
6. **Node CLI 的 MSYS vs Windows 路径**（⭐ 2026.8.5 impeccable 实测）：从 Git Bash 调用外部技能的 Node CLI（如 `npx impeccable detect`）时，路径参数必须是 Windows 路径（`C:\...` 或 `C:/...`），不能用 MSYS 路径（`/tmp/...`、`/c/...`），否则报 `cannot access`。先 cd 到包目录再用 `node cli/bin/cli.js` 调用；首次 `npx --yes` 会下载包约30-60秒
7. **execute_code 可能被审批拦截**：批量文件操作（复制/验证）优先用 terminal，不要在 execute_code 里做递归删除等敏感操作
8. **部署含默认配置的开源项目前必须先校准**（⭐ 2026.8.5 hermes-arxiv-agent 教训）：引入的不只是纯 SKILL.md 技能，还有带脚本/配置/cron 的完整项目（如 hermes-arxiv-agent：monitor.py + search_keywords.txt + cron）。**上游默认配置往往匹配作者自己的场景，不匹配用户**——hermes-arxiv-agent 默认关键词是 `quantization+large+language+model`（量化LLM），而用户方向是碳排放权交易，首次测试运行下载了33篇无关论文，用户提醒才修正。**正确顺序**：部署前先查 memory/现有技能确认用户研究方向（碳排放权交易/ABM省级碳市场模拟）→ 修改项目配置文件（search_keywords.txt）→ 再首次运行。若已误跑：清理旧数据（papers/、new_papers.json、papers_record.xlsx、pending_llm_ids.txt 及上游示例数据 excel_data.json/feishu_msg.md 等），保持干净状态待 cron 首跑。cron prompt 一般无硬编码关键词（monitor.py 运行时读配置文件），改配置即可生效，无需动 cron
9. **预印本 vs 期刊的档次查询**（⭐ 2026.8.5 用户问"arXiv论文是什么期刊档次"）：arXiv 是预印本服务器——不经过同行评审、论文不标注期刊档次（实测10篇 0/10 有 journal_ref）、几乎全英文无中文期刊。要回答"发表在哪、什么档次"，用 OpenAlex API 按标题反查（`filter=title.search:` 避免 search= 对长标题/标点报400；遍历 locations 优先取 type=journal；带 User-Agent+mailto；批量间隔0.4s防限流）。完整实现见 `references/hermes-arxiv-agent-deployment.md` 的 OpenAlex 节。注意：OpenAlex 能查期刊名+被引数，但**查不到中科院分区/影响因子**（中文评价体系增值数据）——如需分区需另建 ISSN 映射表
10. **给用户列候选清单必须用大白话+类比，禁止术语表**（⭐⭐ 2026.8.5 用户明确纠正"你列给我，我哪里看得懂"）：调研出候选技能/项目后，呈现决策表时**每条都要有通俗解释**——"它是啥（一句人话）+ 对用户有啥用（结合其场景：科研/论文/桌宠/基金申报）+ 装不装建议"。术语（MCP/SKILL.md/evals/许可证）必须翻译成生活类比：MCP→"让AI直接操控软件的接口"、SKILL.md→"教AI做一件事的技能包"、许可证→"能不能白嫖/商用"。**句式模板**：`**是啥**：...一句话。**对用户有啥用**：...结合科研/桌宠/基金场景。**建议**：✅装/⚠️暂缓(理由)/❌不装(理由)。` 用户认可这种"大白话解释版"（2026.8.5 实测：术语表版被拒→类比版被"认可，装这五个"）。技术细节留给知识库文档，聊天里只给人话
11. **技能安装目录扫描是两层深度，容器目录不显示**（⭐ 2026.8.5 实测）：Hermes 识别 `分类/<技能名>/SKILL.md`，即 `development/better-ui-kit/better-ui/SKILL.md` 会被识别为独立技能 better-ui，但**容器目录本身（better-ui-kit，无自己的SKILL.md）不出现在技能列表**。验证时按子技能名 grep，不要找容器名。多子技能包安装模式：`mkdir -p <分类>/<包名>` + 把每个子技能目录复制进去
12. **`hermes skills list` 长技能名显示截断**（⭐ 2026.8.5 实测）：超长技能名（如 recreate-scientific-figure-in-drawio）在列表中被截断为 `recreate-scientific-figu…`，用完整名 grep 会漏判"未识别"。验证用前缀或部分名 grep，或 `grep -c` 后人工确认
13. **完整应用类仓库（非纯技能）拆成"技能部分+应用本体"**（⭐ 2026.8.5 DeerFlow 教训）：DeerFlow 这类仓库=应用(backend/frontend 35M)+skills/ 技能目录。**只装技能部分**进 Hermes（纯SKILL.md直接可用），应用本体单独部署到独立目录（如 `hermes-data/../deerflow`）留待以后运行，知识库文档中说明"应用需Docker/Node/Python运行，未配置API key前不可用"。不要把35M应用拷进技能库
14. **已有文献综述的升级 vs 从零生成是两套流程**（⭐ 2026.8.5 省自科基金综述实战）：`literature-review` 技能管从零生成；**已有综述优化**走"诊断量化→方案审核→补文献→消模糊引用→统一格式→验证"流程，完整套路见 `references/literature-review-upgrade-playbook.md`。关键步骤：正则扫`有研究`模糊引用（实测9处比自认8处多）、OpenAlex多轮检索补2024-2026文献（避开纯电力调度邻域噪声）、格式少数迁就多数、时间范围写"至检索日"不写未来日期、跨模型验证报"摘要不完整"先核对原文（可能是截断误判）
15. **cross_model_verify 对"生成"类任务语义错位**（⭐ 2026.8.5 实测）：cross_model_verify 的定位是**审查验证**，若用其 prompt 要求"生成中文介绍/写文案"（非审查指令），它会按验证框架输出"未通过/缺信息"的审查报告而不是生成内容。**只用于审查验证**；生成类任务直接调 API 或让主 agent 写。涉及 Coding Plan 模型时注意：`cross_model_verify(api="volcano", model="deepseek-v4-flash")` 可用；DashScope 文本 API 403 时换 volcano 通道

## 参考

- `references/skill-repo-inventory.md` - 已调研技能仓库清单、各自子技能结构与安装状态（2026.8.5 四轮调研完整快照：97技能/24文档）
- `references/academic-skill-ecosystem.md` - 学术研究技能生态速查（6维度矩阵/候选清单/核心方法论/回写记录，用户吉首大学科研场景专项）
- `references/hermes-arxiv-agent-deployment.md` - hermes-arxiv-agent 完整部署记录（关键词校准/环境适配/清理清单/验证方法/OpenAlex期刊回溯，含 cron job 12ad7a78fa62）
- `references/literature-review-upgrade-playbook.md` - 已有文献综述的升级流程（诊断量化/OpenAlex补文献/消模糊引用/格式统一/跨模型验证，2026.8.5 省自科基金综述实战）
- skill-distiller（兄弟技能）：从教程/文档蒸馏新技能
- ai-app-provider-config：配置桌面 AI 应用接入 provider（技能导入不涉及 provider）
