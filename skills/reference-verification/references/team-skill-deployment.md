# 团队 Agent 科研技能装配：三层核查法（2026-08-07 实战）

> 背景：少帅督办"给4个agent装配学术科研技能"。假文献危机（Aion CLI 编造30处页码、OpenCode 综述13重复+7编造）根因是队友无学术技能。装配前先核查三层，避免"以为装了其实没装"。

## 三层核查法

| 层 | 查什么 | 命令/位置 | 实测结果（2026-08-07） |
|---|---|---|---|
| ① AionUi 配置层 | agent 技能列表是否非空 | `aionui-backend.db` → `conversation_assistant_snapshots.resolved_skill_ids` / `agent_metadata.native_skills_dirs` | bare 型队友 `resolved_skill_ids` 恒为空；`native_skills_dirs` 列：Claude Code=`.claude/skills`、OpenCode=`.opencode/skills`、Aion CLI=`.aionrs/skills` |
| ② 后端文件层 | 原生技能目录实际内容 | `ls ~/.claude/skills/`、`ls ~/.config/opencode/skills/`（⚠️ 见下）、`ls ~/.aionrs/skills/`、`ls ~/.openclaw/plugin-skills/` | 太尉天然 80+ 技能（含 academic-paper-review/systematic-literature-review/deep-research）；OpenCode/Aion CLI 目录为空；OpenClaw 仅 browser/canvas |

> **⚠️ OpenCode 技能目录错位教训（2026-08-07 实战修正）**：OpenCode（v1.2.26）的实际技能库是 `~/.config/opencode/skills/`（已含 arkcli-* 等 20+ 活跃技能），**不是** `~/.opencode/skills/`。装错位置=白装（运行时不会加载）。判断各后端真实技能目录的方法：查该后端配置文件/已存在技能示例（`ls ~/.config/<tool>/skills/`、看 `opencode.json`），不要凭 `agent_metadata.native_skills_dirs` 的声明值盲信。Aion CLI 的 `~/.aionrs/skills/` 经文件验证有效。
| ③ 文档层 | 技能包/总包是否送达并确认 | 队友回执 | 全员确认（消息回执） |

## 装配动作（文件层才是有效装配）

bare 型队友在 AionUi 会话层技能永远为空，**必须写入后端原生技能目录**：

```python
# 写入 SKILL.md 到各后端目录（新会话/重启后生效）
targets = [
    (r"C:\Users\sxjl3\.opencode\skills\reference-verification\SKILL.md", content),
    (r"C:\Users\sxjl3\.aionrs\skills\reference-verification\SKILL.md", content),
    (r"C:\Users\sxjl3\.openclaw\plugin-skills\reference-verification\SKILL.md", content),
]
```

SKILL.md 格式：YAML frontmatter（name/description）+ 正文（触发条件/步骤/红线）。装配内容按角色裁剪：
- 写作主力（Claude Code）：+ research-paper-writing 方法、journal-adapt
- 审核（OpenClaw）：+ academic-review-checklist（一票否决+10项清单+多审稿人视角）
- 综述/检索（OpenCode）：+ systematic-literature-review-method（系统综述7步含来源验证）
- 文献/格式（Aion CLI）：+ gb7714-reference-format

## 配套管理表格

少帅要求"制作管理表格列出每个 agent 的强项和技能"——标准位置：
`ObsidianVault/🤖 AI Agent/团队科研能力矩阵.md`
含：五维能力打分表（Crossref验证/PDF提取/GB7714/综述写作/审核等）、任务-能力匹配表（首选/次选/理由）、短板与防范表（血泪教训）、三层装配状态记录。
**委派任务前先对照此矩阵选人**，只派"能干好"的活（教训：把页码补全派给无技能的 Aion CLI = 编造30处）。

## 装配验证（少帅 2026.8.7 追问后补强：三层缺一不可）

- 文件存在性：`os.path.exists` 逐个确认
- **内容完整性：验证文件大小 > 500 字节**（教训：OpenClaw 技能曾写入 0 字节空文件——execute_code 写 ~/.openclaw 路径可能静默失败，必须重写并复核大小）
- 目录正确性：确认写入的是后端**真实加载目录**（见上文 OpenCode 错位教训）
- 生效确认：通知队友（"新会话/重启后生效"）+ 回执
- 矩阵更新：第七节"三层装配状态"记录在案

**⚠️ 功能验证（最关键，少帅："你有没有进行确认，它们确实具备这些技能了？"）**：
口头回执（"已确认装入"）≠ 技能可用——agent 可能只是读了消息就回复。必须**实战测试**验证其真实执行技能核心操作：

| 将 | 验证测试任务（2026-08-07 实测通过） |
|---|---|
| OpenCode | 用 reference-verification 真实调用 Crossref API 验证 2 篇文献（DOI 直查+输出 GB/T 7714）——检查返回字段/格式 |
| Aion CLI | 从知识库 PDF 真实提取元数据（刊名/卷期/页码/文章编号）并输出 GB/T 7714 |
| OpenClaw | 审核任务中标注使用 academic-review-checklist 的清单项（一票否决/重点/多审稿人）+ 三件套输出格式 |

验证标准：任务结果必须**包含技能核心动作的证据**（Crossref 返回的字段、PDF 提取的页码、清单项的引用），而非泛泛"已完成"。全部通过后才可向用户复命"技能确认可用"。

## 本地技能开源仓库（2026-08-07 少帅阶段指示）

**位置**：`ObsidianVault/🤖 AI Agent/技能开源仓库/`（git 仓库，太尉构建）
**结构**：`README.md`（总览+装配说明+实战验证记录）/ `skills/<技能名>/SKILL.md`（可复制装配）/ `academic-standards/`（引用规范+写作流程实战方法论）/ `carbon-market-abm-toolkit/`（可运行代码+实验数据）
**阶段定位（少帅原话）**："技能仓库还没有完善好，先等技能仓库完善好，再去开源不迟。现在还是在本地完善技能仓库的阶段"——**本地完善优先，push 开源延后**（太尉曾因 push 凭据问题请示，少帅直接定"暂不推送"）。

**可迁移技能入库流程**（少帅要求"太尉把他具备可迁移的技能也开源到本地技能仓库"）：
1. 扫描源技能库（如 `~/.claude/skills/` 全部技能）
2. 筛选**可迁移**技能：通用方法论/学术科研/开发工程类（不依赖专属环境/API）；排除：强依赖某后端专属环境的、涉密的；与现有库重复的可标注
3. 复制 SKILL.md 到 `技能开源仓库/skills/<技能名>/`
4. 更新 README（技能清单+来源+适用 agent）
5. 报告：仓库最终技能总数（`find ... -name SKILL.md | wc -l`）——少帅会直接问"仓库有多少技能了"，须用真实文件数回答（实测首版仅 5 个自研技能，140 个中的可迁移部分未入库，被少帅追问后补令全量入库）
