# 中文文献真实性验证路径与期刊官网清单

> 来源：2026-08-14 省自科申报书文献战役实测
> 核心认知：**中文期刊DOI不在Crossref注册**（注册于中文DOI系统 chndoi.org），Crossref查中文DOI必404 ≠ 文献不存在。用 doi.org 全局解析验证。

## 一、验证路径选择

| 文献类型 | 首选验证 | 备选 |
|---|---|---|
| 英文SSCI/SCI | Crossref API 按DOI反查（题名/期刊/年/卷期页/作者全字段） | OpenAlex |
| 中文DOI（有DOI的） | **doi.org全局解析**（302重定向到chndoi.org/万方=有效） | 期刊官网 |
| 中文CSSCI刊（无DOI或Crossref查不到） | 期刊官网目录/文章页 | 知网CNKI、万方 |
| 中文新刊（2025-2026） | web_search定位 → 浏览器访问期刊官网 | 官网文章详情页 |

## 二、doi.org 全局解析验证（中文DOI）

```python
import urllib.request
# 302重定向到 chndoi.org 或万方 = DOI有效
req = urllib.request.Request(f"https://doi.org/{doi}", method="HEAD")
# 或 https://doi.org/api/handles/{doi} → responseCode==1 即有效
```

实测：10/10 中文DOI（宋德勇2024、斯丽娟2021、孙晓华2024、刘金科2022、王娟2025等）全部可解析，而 Crossref 查同一批 DOI 全部 404。

## 三、期刊官网验证（中文CSSCI）

以下官网已验证可访问且含完整元数据（卷期页码+DOI+作者）：

| 期刊 | 官网 | 备注 |
|---|---|---|
| 中国人口·资源与环境 | geores.com.cn/zgrkzyyhj | 文章页含作者/摘要/引用格式/参考文献全文 |
| 财经研究 | qks.sufe.edu.cn | 文章详情页含卷期页码+DOI+引用格式 |
| 税务研究 | 税务研究官网 | 目录页可核卷期页码 |
| 宏观经济研究 | 官网/知网 | DOI格式 10.16304/j.cnki.11-3952/f... |
| 中国管理科学 | 官网 | DOI格式 10.16381/j.cnki.issn1003-207x... |

验证技巧：浏览器访问文章详情页（如 geores.com.cn 的 DOI 链接页）能一次性拿到：作者全名、期刊、年卷期、页码、DOI、"引用本文"GB/T 7714格式、基金信息——比知网更权威（官网一手数据）。

## 四、期刊级别核实（CSSCI 2025-2026 官方目录）

- xlsx 来源：南财图书馆 `http://lib.nufe.edu.cn/2025/0902/c463a11884/page.htm`（页面内 xlsx 附件）
- 解析结构：每个 sheet=一个学科，**4列**（序号|期刊|序号|期刊）：
  - row[1] = CSSCI 来源期刊
  - row[3] = CSSCI 扩展版期刊
  - （注意：不是 row[0]/row[2]！第1列是"序号"）
- 2025-2026版已实测的变化：科技管理研究/湖北社会科学/中国环境管理/环境经济研究/工业技术经济/北京理工大学学报(社科版) 均转入 **CSSCI扩展版**
- 认定规则：按**发表当年**目录认定——2016年发在科技管理研究的论文（当时是CSSCI来源）仍可按CSSCI引用，标注"发表时CSSCI/现扩展版"；2026年发表的按最新目录=扩展版

## 五、英文近两年文献检索（2025-2026）

- Crossref 期刊定向：`query.bibliographic` + `filter=from-pub-date:2025-01-01`
- ⚠️ 返回的 container-title 可能为空 → 按期刊名硬过滤会**误杀全部**（实测92条候选变0条）→ 改用标题关键词强过滤
- 新文献（2025-2026）Semantic Scholar/OpenAlex 摘要常为空 → 用标题+期刊+领域知识做摘要级解读，标注⚠️，正文不引用未证实数值
- 高质量来源刊：JEEM / Energy Economics / Energy Policy / EJOR / EIA Review / Energy Efficiency / Applied Energy / Nature Climate Change

## 六、零编造红线要点

1. 检索候选的作者名可能不准 → 必须 Crossref 按DOI反查替换为真实作者
2. 页码缺失 → 标注"（页码待核，网络首发）"或官网核实，**绝不编造**
3. 无法验证期刊级别的文献 → 宁可弃用（实测：1篇建议文献因期刊无法确认被弃）
4. 摘要级解读的文献 → 正文不引用未证实的具体系数/数值
