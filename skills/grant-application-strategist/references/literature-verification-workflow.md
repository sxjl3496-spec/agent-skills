# 参考文献真实性核实全流程（Crossref + PDF 双重验证）

> 来源：2026-08-07 省自科申报假文献危机实战（少帅定性"重大学术问题"）
> 背景：申报书52篇参考文献查出7篇疑似编造+30余处卷期页码错误。根源=OpenAlex/二手元数据标题失真 + AI 补写卷期页码（=编造）。

## 一、铁律

1. 禁止编造：查不到 → 删除或替换为可查证文献，绝不臆造
2. 禁止"待核实"字样残留最终交付物
3. 禁止"标题+期刊+年份"简化条目（GB/T 7714 必须完整：作者. 题名. 刊名, 年, 卷(期): 页码.）
4. 双重验证：英文 Crossref（DOI 或标题检索）、中文 PDF 原文/知网题录
5. 编号与正文引用一一对应（无悬空、无跳号、无未引）

## 二、英文文献：Crossref 验证（标准代码）

```python
import requests
session = requests.Session()
session.trust_env = False  # 必须：绕过系统代理

# 方式1：按DOI精确验证（最可靠）
r = session.get(f"https://api.crossref.org/works/{doi}", timeout=20)
# 200=存在（读 title/container-title/volume/issue/page/author），404=疑似编造

# 方式2：按标题+作者检索
r = session.get("https://api.crossref.org/works", params={
    "query.bibliographic": "标题关键词",
    "query.author": "作者姓",
    "rows": 3,
    "select": "DOI,title,author,container-title,volume,issue,page,published",
}, timeout=25)
```

**判定**：完全匹配→采用 Crossref 信息（卷期页码以官方为准）；无匹配→疑似编造（删除/替换）；部分不符→以 Crossref 修正。

**关键坑**：
- **作者名一律以 Crossref family 字段为准**（教训：WebSearch 摘要显示"Zhou Yan and Zhao Yuan"→推断 ZHOU Y 错误，实测 family=Yan/Yuan。搜索结果只作线索不作依据）
- 经典文献（Coase 1960 JLE 3:1-44 / Kahneman 1979 Econometrica 47(2):263-291 / Simon 1955 QJE 69(1):99-118）Crossref 收录不全 → 用公认标准信息
- 区分正式版 vs 预印本（SSRN/arXiv 第一条可能是预印本，翻到正式期刊版）
- 中文期刊 Crossref 覆盖不全 → 走 PDF 验证

## 三、中文文献：PDF 坐标提取（标准流程）

```python
import fitz  # PyMuPDF
doc = fitz.open(pdf_path)
# 1. 首页文本：刊名/卷期/年份（"第X卷第X期"、"202X年X月"）
p1 = doc[0].get_text()
# 2. 页码：页眉页脚数字，按坐标取页面底部70px内的数字token
for i in range(doc.page_count):
    page = doc[i]
    h = page.rect.height
    words = page.get_text("words")  # x0,y0,x1,y1,word,...
    bottom = [w[4] for w in words if w[1] > h - 70 and re.fullmatch(r"[0-9０-９]{1,4}", w[4])]
# 3. "引用本文"格式行（部分期刊首页自带规范引用，最可靠）
```

**页码提取技巧（血泪汇总）**：
- 页脚格式多样：`·N·`、`-- N`、`— — N`、全角数字、左右分列**反序**（"７ １ １"=个位7十位1百位1=117，注意 [个十百] 反序）
- 每页递增序列（如 120,121,...,135）→ 页码范围 = min-max
- 文章编号解析：`1004-8308（2024）01-0040-13` = 期01、起始页0040、页数13 → 40-52
- 无卷号期刊（科技管理研究/重庆社会科学）→ 只标 年(期): 页码
- 增刊/合刊 → 标"年, 卷(增刊): 页码"
- 卷号合理性可用创刊年推算（如科技管理研究1981创刊→2024年44卷；南开管理评论1998创刊→2024年27卷）
- ±1页码争议 → 以 PDF 页码序列为准（谁有连续序列证据谁对）

**判定**：PDF 首页显示刊名/卷期 → 以此为准（可能推翻原条目）；PDF 无页码 → 知网题录/期刊官网；仍无 → 替换或删除。

## 四、审核10项清单（交付前逐项核对）

1. 编号连续、无跳号、无重复
2. 正文引用与列表一一对应（含反向：列表是否全被引用——申报书可策略性保留完整文献库，但要少帅知晓）
3. 每篇有完整作者名（无"et al."代替全部作者）
4. 英文文献 Crossref/DOI 可验证
5. 中文文献与 PDF/知网一致
6. 卷/期/页码完整正确
7. 刊名正确（警惕张冠李戴：如[49]实际发上海大学学报却标中国人口·资源与环境）
8. 年份正确（如[45]实为2024却标2025）
9. 无"待核实"字样
10. 引用语境与文献主题匹配（正文引用位置与该文献内容相符）

## 五、教训沉淀（2026-08-07 案例）

| 问题 | 根源 | 防范 |
|---|---|---|
| 7篇英文疑似编造 | OpenAlex 二手元数据标题失真 | Crossref 逐条验证 |
| AI 补写卷期页码（30+处错） | agent 凭记忆/推测补全 | 页码必须 PDF/知网来源 |
| 综述13重复+7编造+15错位 | 引用编号未规划+元数据未验证 | 先规划编号再写，逐条 Crossref |
| 替换文献作者名错误 | 凭搜索摘要推断 | family 字段为准 |
| 中文页码系统性错误 | 沿用主稿/二手数据 | 每篇 PDF 坐标提取 |
