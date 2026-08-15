---
name: simple-english
description: 简化英语写作自查——借鉴 ASD-STE100（AminBlg/SimpleEnglish ★1.6K 航空航天写作标准）的简明原则，适配中英文学术/技术写作：短句、单义、主动语态、术语统一。
---

# Simple English（简化英语写作）

## 核心原则（改编自 ASD-STE100）

1. **一句一信息**：每句只表达一个主张；长句拆短（目标 ≤25 词/句）
2. **主动语态优先**：`We calibrated the model` 优于 `The model was calibrated`
3. **单义词**：一个术语一个含义，全文统一（如 model/agent 不混用）
4. **移除冗余**：删 "in order to"→"to"、"very significant"→"significant"、"it should be noted that"→删除
5. **具体数字**：不用 vague（"significantly higher"），用可复核值（"1.70×, t = −49.7"）

## 学术写作自查清单

| 检查项 | 反例 → 正例 |
|---|---|
| 被动滥用 | "was conducted by us" → "we conducted" |
| 空洞强调 | "highly significant" → "p < 0.001" |
| 名词化 | "give consideration to" → "consider" |
| 模糊量词 | "a number of" → 具体数或删 |
| 重复主语 | 段落内同一主语连续句 → 合并 |

## 与去 AI 化配合

AI 生成文本的典型痕迹：过度连接词（furthermore/moreover 连发）、空泛总结句、每段三句式模板——用本清单逐句过，配合 no-ai-slop-zh 使用。

## 实战案例

本团队论文 Abstract 润色：丞相版采用"信息流重排+对比对象补全"（46.5-fold difference between grandfathering and benchmarking），全稿负号/符号统一（t = −49.7）——正是简化原则的落地。
