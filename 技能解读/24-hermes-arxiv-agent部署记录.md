---
title: hermes-arxiv-agent部署记录
tags: [AI技能, arXiv, 飞书推送, 科研, 部署]
created: 2026-08-05
source: https://github.com/genggng/hermes-arxiv-agent
---

# hermes-arxiv-agent 部署记录

## 基本信息

- **仓库**：[genggng/hermes-arxiv-agent](https://github.com/genggng/hermes-arxiv-agent)（★107，Hermes 专属）
- **定位**：每天自动检索 arXiv 论文、补全中文摘要和作者单位、推送飞书日报 + 本地网页阅读站
- **部署模式**：本地/飞书模式（默认）

## 部署结构

- **项目目录**：`<hermes-arxiv-agent目录>\`
- **技能**：`academic\hermes-arxiv-agent\SKILL.md`（hermes-arxiv-agent-deploy，部署/维护技能）
- **cron**：job_id `12ad7a78fa62`「arxiv论文日报」，每天 08:00，deliver=origin（推飞书）

## 核心文件

| 文件 | 作用 |
|------|------|
| monitor.py | 主监控脚本：arXiv检索→下载PDF→记录Excel |
| search_keywords.txt | 搜索关键词（本次已按用户方向修改） |
| cronjob_prompt.txt | cron提示词模板（`/path/to`占位） |
| prepare_deploy.sh | 部署脚本（生成cron prompt） |
| viewer/ | 本地静态阅读网站（run_viewer.py启动） |
| reextract_affiliations.py | 作者单位重新提取 |

## ⚠️ 关键修正（2026-08-05）

### 教训1：关键词必须按用户科研方向定制

**上游默认关键词**：`all:quantization+AND+all:large+AND+all:language+AND+all:model`（量化+大语言模型）

**用户方向**：碳排放权交易（省自科基金申报方向，ABM省级碳市场模拟）

**修正后关键词**（search_keywords.txt）：
```
all:"carbon emission trading" OR all:"emissions trading" OR all:"carbon market" OR all:"cap-and-trade" OR all:"carbon allowance" OR all:"emission trading scheme" OR all:"carbon trading mechanism" OR all:"carbon pricing"
```

**验证结果**：检索到182篇论文，前5篇全部高度相关（碳价预测、cap-and-trade、EU碳市场尾部依赖、气候政策与能源转型）✅

### 教训2：首次运行会按旧关键词下载论文

首次测试运行时（关键词未改前），monitor.py 下载了33篇量化LLM论文PDF到 papers/。**必须清理**：删除 papers/、new_papers.json、papers_record.xlsx、pending_llm_ids.txt 及上游示例数据（excel_data.json、feishu_msg.md 等），让 cron 从干净状态用新关键词开始。

### 教训3：本机环境差异

- 本机无 `python3` 命令（只有 `python`）→ 生成的 cron prompt 需把 `python3` 替换为 `python`
- `prepare_deploy.sh` 需用 `bash` 运行（不是 python）
- arXiv API 用 HTTPS（`https://export.arxiv.org/api/query`），HTTP 返回空

## 期刊回溯功能（OpenAlex，2026-08-05 升级）⭐

**背景**：arXiv 是预印本服务器（非期刊、不经过同行评审、几乎全英文），论文本身不标注期刊档次。用户需要日报显示期刊信息。

**方案**：新建 `journal_lookup.py`，用 OpenAlex API（免费、无key）按标题反查论文是否已正式发表。

**工作原理**：
1. monitor.py 抓取新论文后，自动调用 `lookup_journal(title)` 
2. OpenAlex 按标题模糊匹配（`filter=title.search`）
3. 从 `locations` 中优先找 type=journal 的来源（论文可能有 arXiv 预印本 + 正式期刊两个位置）
4. 结果写入 Excel 新字段：journal_status / journal_name / cited_by_count

**状态分类**：
| journal_status | 含义 | 飞书显示 |
|---------------|------|---------|
| published | 已正式发表 | 📄 已发表于《期刊名》（被引N次） |
| repository | 工作论文（SSRN/arXiv等） | 📚 工作论文（来源名） |
| unpublished | 未检索到发表记录 | 🔍 预印本 |
| error | API调用失败 | 不显示 |

**实测验证**：
- "Carbon trading in China" → 📄 《Technological Forecasting and Social Change》被引254 ✅
- 最新 arXiv 论文多数显示"预印本"（因为确实还没发表，符合实际）

**踩坑记录**：
1. OpenAlex `search=` 参数对长标题/含标点标题报 400（"Wildcards require exact search"）→ 改用 `filter=title.search:` 解决
2. 单篇论文在 OpenAlex 有多个 locations（预印本+期刊版）→ 需遍历 locations 优先取 journal 类型
3. 需带 User-Agent + mailto 参数（OpenAlex 礼貌使用要求）

## 工作流（每日cron自动执行）

```
monitor.py 检索新论文（按search_keywords.txt，碳交易方向8个短语）
  → OpenAlex 期刊回溯（journal_lookup.py，标注发表期刊/被引数）
  → 下载PDF到papers/
  → 生成new_papers.json（含journal_status/journal_name/cited_by_count）
  → LLM补全：提取作者单位(affiliations) + 生成中文总结(summary_cn 90-150字)
  → 回填papers_record.xlsx（含期刊字段）
  → viewer/build_data.py 更新网站数据
  → 推送飞书Markdown日报（含期刊档次标注）
```

## 验证证据

- ✅ monitor.py 用新关键词检索成功（3篇测试，全部碳交易相关）
- ✅ cron 配置正确（每天8点、deliver=origin、enabled）
- ✅ 依赖齐全（pdfplumber/openpyxl/requests/PyMuPDF 均已装）

## 后续操作

1. 用户可随时改 `search_keywords.txt` 调整监控方向（无需改cron）
2. 本地网页阅读：`cd <hermes-arxiv-agent目录> && python viewer/run_viewer.py`
3. 每日8点自动推送论文日报到飞书
