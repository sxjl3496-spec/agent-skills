---
name: docx-template-fill
description: Fill Chinese official docx form templates that use XXX/XX placeholder tokens (专业一致性说明、政审公函、报名表、在编证明 etc.) by editing the OOXML directly. Use when the user sends a docx template with blanks marked as XXX/XX/XXXXXXXXXX and asks to 填写/填好, when a plain-text find fails to match, or when placeholder text is split across XML runs. Preserves original formatting, fonts, and structure.
---

# DOCX Template Fill (XXX placeholder tokens)

## When To Use

- User sends a `.docx` template with blanks marked `XXX` / `XX` / `XXXXXXXXXX` / `20XX年` and asks to fill it (填写/填好).
- Typical for 用户: 政审公函, 专业一致性说明, 招聘报名表, 不在校证明, 专家评阅书 — official forms whose blanks must be filled WITHOUT breaking the original layout/fonts.
- Also use when you need to fill a docx programmatically but `python-docx` paragraph text matching fails.

## HARD RULE: Replace placeholders ONLY — never alter template wording ⭐

User explicitly corrected (2026-08-05): "你不要修改模板，那是人家给过来的模板，你把那个信息填进去可以了，不要修改它的模板" — official templates are fixed formats from the issuing authority. Replace ONLY the `XXX`/`XX`/`XXXX` placeholder tokens with real values; the template's own phrasing, sentence structure, and words must remain byte-for-byte identical.

- ✅ Replace `XXX一级学科（代码XXX）` → `应用经济学一级学科（代码0202）` (placeholder → value only)
- ❌ Do NOT restructure: e.g. rewriting "隶属于XXX一级学科" into a longer clause, injecting extra codes (like 0202Z1) the template never asked for, or adding honorifics like "同志" to a placeholder replacement
- If real data has no corresponding placeholder in the template, TELL the user "模板没有该字段位置" — do not modify the template to accommodate it
- Verify by re-reading: template text (non-placeholder parts) should be unchanged; only the tokens differ

## Core Insight

**Never match against rendered paragraph text.** Word stores text in `<w:t>` elements and splits phrases across MULTIPLE runs (`<w:t>就读于</w:t>...<w:t>XXX 大学</w:t>`). A whole-sentence search in the extracted text will NOT locate the XML to replace. Edit `word/document.xml` directly inside the zip.

## Workflow (verified 2026-08-05)

1. **Read the template first** (`read_file` on the docx auto-extracts text). Identify every placeholder token and its surrounding context sentence.
2. **Extract `word/document.xml`** from the docx zip via `zipfile`. Work on the raw XML string.
3. **Plain global `str.replace(old, new)` on the whole XML**, ordered most-specific-first:
   - Replace complete placeholder phrases WITH their context, e.g.
     `"XXX（男 / 女，身份证号：XXXXXXXXXX）"` → `"申请人（男，身份证号：430302XXXXXXXXXXXX）"`
     `"20XX 年 XX 月至 20XX 年 XX 月"` → `"2021 年 9 月至 2026 年 6 月"`
     `"XXX一级学科（代码XXX）"` → `"应用经济学一级学科（代码0202）"`
   - **Short generic tokens (`XXX`, `XX学院`) LAST, and only with enough context** — bare `XXX` appears in the title too and would over-replace. Handle the title first with full phrase: `"关于XXX专业一致性的说明"` → `"关于申请人同志专业一致性的说明"`.
   - Print ✅/⚠️ per replacement (⚠️ = no match → must investigate, don't deliver silently).
4. **If a phrase spans a run boundary** (`</w:t><w:t>` between words), plain replace misses it. Fix: replace the XML fragment including the boundary tags, or regex tolerant of tag characters between words. Verify by re-extracting text.
5. **Write a NEW zip** with all original entries + patched `document.xml`. Save as a NEW file — never overwrite the template. Good home: user's Obsidian folder or a versioned copy.
6. **Verify by re-reading the patched zip**: parse XML with ElementTree, join `<w:t>` per paragraph, print full document text, assert **0 residual `XX+` tokens**, assert each key field present (name, ID number, dates, institution, code). Report results explicitly.
7. **Leave genuinely unfillable fields blank** (e.g. signature date `2026年 月 日`, seal) and TELL the user — don't invent them. Flag fields needing user confirmation (e.g. discipline code inferred, not from the recruitment notice).

## Gathering the Values

Before filling, collect the person's real data from the best available source, in priority order:
1. 用户口述 / 消息中的信息
2. 报名表 / 考核表 / 简历 / 证明材料 PDF (search Desktop, Obsidian Vault, Feishu chat)
3. Ask the user for anything still missing — do not guess ID numbers or dates.

## Pitfalls

- **`XXX` over-replacement**: a bare `"XXX"` replace hits the title AND every occurrence. Always replace context phrases first, bare tokens last.
- **Run-split phrases**: the first attempt may fail with "未匹配" because the placeholder text is split across `<w:t>` elements. Don't give up — replace at the XML-fragment level.
- **Don't use python-docx paragraph matching** for placeholders; it flattens runs and loses the split structure.
- **Formatting preservation**: editing only `<w:t>` text keeps all original fonts/sizes/bold — this is the whole point vs. rebuilding the document.
- **After filling, re-download source vs. use prior output**: if an earlier session already filled the docx (check Obsidian/session history), verify the existing output before redoing the work. Verify = re-read + assert no residual tokens + assert key fields, then deliver.

## Support Files

- `references/docx-placeholder-fill.md` — full working Python script pattern (extract, replace, verify, write).
