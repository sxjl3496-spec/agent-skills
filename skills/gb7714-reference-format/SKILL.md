---
name: gb7714-reference-format
description: "Generate and validate GB/T 7714-2015 compliant Chinese academic reference lists. Use when formatting references for Chinese academic papers, theses, or grant applications that require GB/T 7714 standard. Covers journal articles [J], books [M], book chapters [M]//, conference papers [C], reports [R], and online documents [EB/OL]. Includes author name normalization, punctuation rules, and cross-validation with Crossref/PDF metadata."
---

# GB/T 7714-2015 Reference Formatting Skill

## Purpose

Generate and validate reference lists in GB/T 7714-2015 format (中国国家标准·信息与文献 参考文献著录规则) for Chinese academic papers, theses, and grant applications.

## When to Use

- Formatting references for Chinese journals (CSSCI, 北大核心, CSCD)
- Grant applications requiring GB/T 7714 compliance
- Converting reference lists from other formats (APA, MLA, Chicago) to GB/T 7714
- Validating existing reference lists for GB/T 7714 compliance
- Chinese thesis/dissertation reference formatting

## Format Templates

### Journal Article [J]

```
作者. 题名[J]. 刊名, 年, 卷(期): 起止页码.
```

**English example:**
```
COASE R H. The Problem of Social Cost[J]. Journal of Law and Economics, 1960, 3(1): 1-44.
```

**Chinese example:**
```
马彦瑞. "双碳"目标下碳排放权交易的减排效应与作用机制[J]. 生态经济, 2025, 41(10): 24-32.
```

### Book [M]

```
作者. 书名[M]. 版次(第1版不标注). 出版地: 出版社, 出版年: 引用页码.
```

**Example:**
```
DALES J H. Pollution, Property and Prices[M]. Toronto: University of Toronto Press, 1968.
```

### Book Chapter [M]//

```
章节作者. 章节题名[M]//编者. 书名. 出版地: 出版社, 出版年: 起止页码.
```

**Example:**
```
TESFATSION L. Agent-based Computational Economics[M]//HANDBOOK OF COMPUTATIONAL ECONOMICS. Amsterdam: Elsevier, 2006, 2: 829-880.
```

### Conference Paper [C]

```
作者. 题名[C]//会议录名. 出版地: 出版者, 出版年: 起止页码.
```

### Report [R]

```
作者. 题名[R]. 出版地: 机构名, 出版年.
```

**Example:**
```
HOLT C A, SHOBE W M, BURTRAW D, et al. Auction Design for Selling CO2 Emission Allowances[R]. Washington, DC: Resources for the Future, 2007.
```

### Online Document [EB/OL]

```
作者. 题名[EB/OL]. (发布日期)[引用日期]. URL.
```

## Author Name Rules

1. **Chinese authors**: 姓在前名在后，如 `马彦瑞` → `马彦瑞`
2. **English authors**: 姓大写在前，名缩写在后，如 `Ronald Coase` → `COASE R H`
3. **3人以内**: 全部列出，用逗号分隔
4. **3人以上**: 列出前3人，后加 `, et al.`（英文）或 `, 等`（中文）
5. **机构作者**: 使用全称，如 `Resources for the Future`

## Punctuation Rules (GB/T 7714-2015)

| 元素 | 分隔符 | 说明 |
|:---|:---:|:---|
| 作者与题名 | `.` | 英文句点 |
| 题名与文献类型 | 无 | 紧接 `[J]`/`[M]` 等 |
| 刊名与年份 | `,` | 英文逗号 |
| 年份与卷号 | `,` | 英文逗号 |
| 卷号与期号 | `(` `)` | 期号用括号 |
| 期号与页码 | `:` | 英文冒号 |
| 起止页码 | `-` | 短横线 |

## Validation Checklist

Before finalizing a reference list, verify:

- [ ] All authors listed (3+ authors: first 3 + et al.)
- [ ] Author names in correct format (English: LASTNAME F M; Chinese: 全名)
- [ ] Journal name in correct case (usually Title Case)
- [ ] Volume and issue numbers present and correct
- [ ] Page range complete (start-end)
- [ ] Document type label correct ([J], [M], [C], [R], [EB/OL])
- [ ] Punctuation consistent throughout
- [ ] No missing commas, periods, or colons
- [ ] Reference numbers match in-text citations
- [ ] No duplicates in the list

## Common Mistakes to Avoid

1. **Missing page numbers**: GB/T 7714 requires complete page ranges
2. **Wrong document type**: Ensure [J] for journals, [M] for books
3. **Inconsistent author format**: All English authors should be LASTNAME F M
4. **Missing volume/issue**: Both volume and issue are required for journals
5. **Wrong punctuation**: Use GB/T 7714 punctuation, not APA/MLA style
6. **Incomplete book info**: Include publisher location and name

## Cross-Validation Sources

- **English references**: Crossref DOI lookup, publisher websites
- **Chinese references**: CNKI (知网), Wanfang (万方), VIP (维普), PDF metadata extraction
- **Never fabricate**: If metadata cannot be verified, mark for manual verification or remove
