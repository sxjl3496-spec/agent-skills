---
name: literature-review
description: >
  端到端文献综述技能。输入研究主题即可完成：
  文献搜集（中英文双语，OpenAlex/arXiv/Crossref/Semantic Scholar多源聚合）
  -> 筛选去重 -> 综述撰写（主题/时间/方法论维度）
  -> 格式化输出（GB/T 7714-2015 顺序编码制/著者-出版年制 + APA 7th）。
  支持导入CNKI导出文件(.ris/.enw/.nbib)。生成PRISMA检索流程报告。
  触发词："文献综述"、"literature review"、"帮我搜集文献"、"综述写作"。
---

# 文献综述技能 (Literature Review)

## 概述

端到端文献搜集与综述生成技能。支持中英文双语文献检索、多维度综述组织、
GB/T 7714-2015 和 APA 7th 引用格式化。

## 何时使用

- 需要系统化搜集某研究主题的文献
- 需要撰写文献综述（论文/基金申请/学位论文）
- 需要格式化参考文献（GB/T 7714 或 APA 7th）
- 需要导入已下载的 CNKI/万方文献元数据

## 工作流程

```
[用户输入研究主题]
  ↓
[1 主题解析] 提取中英文关键词、时间窗、输出格式偏好
  ↓
[2 并行检索]
  ├─ OpenAlex (主数据源，覆盖中文期刊)
  └─ arXiv (预印本)
  ↓ 可选导入
  ├─ 用户提供的 .ris/.enw/.nbib 文件
  ↓
[3 元数据补全] Crossref(补DOI) + Semantic Scholar(引用网络，可选)
  ↓
[4 去重与筛选] DOI精确匹配 + 标题模糊匹配 + arXiv->DOI映射
  ↓
[5 主题聚类] LLM提取研究问题/方法/发现/局限，按维度聚类
  ↓
[6 综述生成] 按维度生成Markdown综述（含引用存在性校验）
  ↓
[7 引用格式化] citeproc-py + CSL样式 -> 正文引用 + 参考文献列表
  ├─ GB/T 7714-2015 顺序编码制 [1]
  ├─ GB/T 7714-2015 著者-出版年制 (作者, 年份)
  └─ APA 7th (Author, Year)
  ↓
[8 输出] Markdown综述 + PRISMA报告 + 参考文献列表 + BibTeX
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| query | (必填) | 研究主题/关键词 |
| max_results | 50 | 每数据源最大检索数 |
| year_from | 2000 | 起始年份 |
| year_to | (当前年) | 截止年份 |
| sources | [openalex, arxiv] | 检索源列表（crossref/semantic_scholar为可选补全源） |
| import_file | None | 导入文件路径(.ris/.enw/.nbib) |
| structure | theme | 综述维度: theme/chronology/methodology |
| citation_style | gb7714-numeric | 引用格式: gb7714-numeric/gb7714-author-date/apa |
| language | zh | 综述输出语言: zh/en |
| output_format | markdown | 输出格式: markdown（docx/bibtex为TODO） |

## 依赖

```
pip install pyalex arxiv habanero semanticscholar citeproc-py rapidfuzz langdetect rispy pymupdf requests
```

## 环境变量（可选）

| 变量 | 说明 |
|------|------|
| SEMANTIC_SCHOLAR_API_KEY | Semantic Scholar API密钥（提升限流额度） |
| RESEARCHER_EMAIL | polite mailto（OpenAlex/Crossref/Unpaywall） |

## 脚本说明

| 脚本 | 职责 |
|------|------|
| utils.py | Paper/SearchLogEntry数据模型 + 缓存 + 去重 + retry |
| search_papers.py | 并行搜索(OpenAlex+arXiv) + 中文导入 |
| csl_adapter.py | Paper->CSL-JSON转换（含中文作者处理） |
| format_citations.py | citeproc-py渲染 + locale后处理 |
| generate_review.py | LLM综述生成 + 引用存在性校验 |
| pdf_fetcher.py | 惰性PDF下载+全文提取 |
| prisma_report.py | PRISMA检索流程报告 |
| validator.py | CSL-JSON校验 + 必填字段 + 引用键唯一 |

## 引用格式说明

### GB/T 7714-2015 顺序编码制
正文标注：`[1]`、`[2-4]`（上标）
参考文献：`[1] 作者. 题名[J]. 刊名, 年, 卷(期): 页码.`

### GB/T 7714-2015 著者-出版年制
正文标注：`(张三, 2023)`
参考文献：`张三. 2023. 题名[J]. 刊名, 卷(期): 页码.`

### APA 7th
正文标注：`(Smith, 2020)` 或 `Smith (2020)`
参考文献：`Smith, J. (2020). Title. Journal, 12(3), 45-67.`

### 中英文混排处理
citeproc-py 用 en-US locale 渲染全部文献，
然后对 language=="zh" 的文献后处理替换：
- "et al." -> "等"
- "and" -> "、"

## LLM调用说明

`generate_review.py` 支持三种模式：
- `api='none'`（默认）：生成prompt，由上层agent或用户手动发给LLM
- `api='dashscope'`：直接调用阿里百炼API（需设DASHSCOPE_API_KEY）
- `api='moonshot'`：直接调用Moonshot API（需设MOONSHOT_API_KEY）

## 常见陷阱

1. **citeproc-py 的 author 字段必须是结构化对象**：不能是字符串，必须是 `[{family: "张", given: "三"}]` 结构。csl_adapter 已处理。
2. **OpenAlex 中文覆盖不完整**：OpenAlex 收录了大量中文期刊，但覆盖不如知网全面。建议同时使用导入功能补充中文文献。OpenAlex 的 language 字段不可靠（常将中文误标为 "ja"），代码用 CJK 字符检测标题来纠正。
3. **Crossref 支持中文搜索**：Crossref 收录了大量有 DOI 的中文期刊论文。搜索时用中文关键词即可返回中文结果。摘要可能含 JATS XML 标签，代码已自动清理。language 通过 CJK 检测标题 + Crossref language 字段双重判断。
4. **百度学术不可用**：百度学术有严格的反爬验证（百度安全验证 CAPTCHA），HTTP 请求和 headless Chrome 均被拦截，无公开 API。中文文献搜索请用 OpenAlex + Crossref 在线搜索，或导入 CNKI/万方导出文件。
5. **Semantic Scholar 无 Key 时限流严重**：建议配置 `SEMANTIC_SCHOLAR_API_KEY`，否则该源会被跳过。
6. **arXiv 与正式发表版去重**：同一研究可能同时有 arXiv ID 和 DOI，去重时以 DOI 为权威标识。
7. **PDF 全文提取质量不稳定**：扫描版 PDF、含公式较多的 PDF 可能提取出乱码。pdf_fetcher 有质量评估，低质量时回退到摘要。
8. **CSL 样式文件首次运行自动下载**：需要网络连接。下载后缓存在 csl/ 目录。
9. **缓存 TTL 30天**：学术论文元数据相对静态，但新发表的论文可能需要清缓存重新检索。

## 参考

- `references/api_sources.md` - 各API端点、限流、认证说明
- `references/gb7714_guide.md` - GB/T 7714-2015格式指南
- `references/apa7_guide.md` - APA 7th格式指南
- `templates/review_thematic.md` - 主题维度综述模板
- `templates/review_chronological.md` - 时间维度综述模板
- `csl/` - CSL样式文件（自动下载）
