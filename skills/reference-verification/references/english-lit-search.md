# 英文SSCI/SCI文献检索策略（2026-08 文献战役实测）

## 结论：检索效率排序

1. **Crossref 期刊定向检索（首选，一次可得数十条高质量候选）**
2. OpenAlex `search` 参数（全文搜索，噪声极大，需强过滤）
3. Semantic Scholar（无 API key 限流严重，2秒/次，结果参差，仅补充）

## Crossref 期刊定向检索（最有效）

```python
params = {
    "query.bibliographic": keyword,          # 主题关键词
    "query.container-title": journal,        # 期刊名（可部分匹配）
    "filter": f"from-pub-date:{year_from}-01-01,type:journal-article",
    "rows": 12,
    "select": "DOI,title,container-title,issued,volume,issue,page,is-referenced-by-count",
}
url = "https://api.crossref.org/works?" + urlencode(params)
```

实测：对 JEEM/Energy Economics/Energy Policy/Nature Climate Change/China Economic Review 等 10 个核心期刊 × 关键词组合，一次拿到 **101 条近5年高质量SSCI候选**（全部真实DOI可查）。

**推荐期刊组合**（排放权/环境经济方向）：
JEEM、Energy Economics、Energy Policy、Nature Climate Change、China Economic Review、Ecological Economics、Journal of Cleaner Production、Resource and Energy Economics、Applied Energy、Computational Economics

## OpenAlex 的坑

- `search=` 参数是**全文搜索**，匹配正文含关键词的高引文献（实测返回糖尿病指南、药物递送纳米粒等完全无关的医学文献）
- `filter=title_and_abstract.search:` 可改善但仍需程序内标题关键词强过滤
- 正确姿势：`search + filter(from_publication_date,type:article) + 标题正则过滤`（排除 medicine/wireless/deep-learning 等噪声词）

## Semantic Scholar 的坑

- 无 API key 限流严重（约2秒/请求），15个查询要1分钟+
- 相关性排序尚可但候选质量波动大，且 publicationTypes 过滤易误伤
- 用途：单篇已知文献的摘要获取（`graph/v1/paper/DOI:xxx?fields=title,abstract`），不做批量检索

## 流程建议

1. 期刊定向检索 → 候选池（按被引降序）
2. 标题关键词强过滤（TITLE_OK/TITLE_BAD 正则）
3. **Crossref DOI 直查逐篇核实**（不信任 query.bibliographic 首结果——见 SKILL.md 陷阱）
4. 第二 agent 独立复核（双 agent 交叉验证）
5. 摘要获取：Semantic Scholar API 或期刊页面（付费墙文献标注"摘要级解读"）
