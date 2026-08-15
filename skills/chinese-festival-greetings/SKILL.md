---
name: chinese-festival-greetings
description: Writing Chinese festival greetings (端午、中秋、春节等) tailored to different relationships and social contexts. Covers tone calibration, cultural nuance, and batch-generating greetings for multiple recipients.
triggers:
  - user asks to write festival greetings (端午、中秋、春节、元旦、国庆等)
  - user asks to write holiday messages for different people
  - user asks to send blessings in Chinese
  - user mentions 节日祝福/节日问候
---

# Chinese Festival Greetings

## Core Principle

**关系决定语气，场景决定内容。** Never write one-size-fits-all greetings. Always ask or infer the relationship before writing.

## Relationship Tiers and Tone

### 长辈 (Elders: 父母、叔伯姑姨、老师、导师、院长等)
- Use **您** (formal you)
- Keywords: 身体健康、阖家幸福、万事顺遂、平安如意
- Tone: respectful, warm, not overly stiff
- Mention specific context if available (e.g., their work, location)

### 平辈-亲近 (Close peers: 师兄师姐、好朋友、兄弟姐妹)
- Use **你**
- Tone: casual, warm, can use humor
- Emojis OK (🎉😄💪🎋)
- Can reference shared experiences or inside jokes

### 平辈-正式 (Professional peers: 学院院长、新领导、不太熟的同事)
- Use **您**
- More formal structure, but still warm
- Express gratitude or anticipation if context fits
- Emojis: 1-2 max, choose 🎉🎊 not 😄哈哈

### 晚辈/弟弟妹妹 (Younger: 表弟表妹、师弟师妹)
- Use **你**
- Tone: friendly, encouraging, like a caring older sibling
- Keywords: 学业顺利、天天开心、假期愉快

## Structure Templates

### Short (群聊/批量, 1-2 lines)
```
[称呼]，[节日名]安康/快乐！🎋 祝[祝福语]！[emoji]
```

### Medium (普通关系, 3-5 lines)
```
[称呼]，[节日名]安康！🎋
[1句关心/具体场景]
祝[2-3个四字祝福]！🎉
```

### Long (重要人物/有故事, 5-8 lines)
```
[称呼]，[节日名]安康！🎋
[感恩/回忆/具体事件]
[坦诚感受（遗憾、珍惜等）]
祝[祝福]！[emoji]
```

## Festival-Specific Notes

| 节日 | 标准祝词 | 注意事项 |
|------|---------|---------|
| 端午节 | 端午安康 (not 快乐，安康更主流) | 可提粽子、假期、龙舟 |
| 中秋节 | 中秋快乐/中秋团圆 | 可提月饼、月圆、团圆 |
| 春节 | 新春快乐/过年好 | 可提红包、年夜饭、拜年 |
| 国庆节 | 国庆快乐 | 可提假期、出游 |
| 元旦 | 元旦快乐/新年快乐 | 可提新年、展望 |

## Key Patterns from Practice

### 1. 多版本策略
Always offer 2-3 versions (克制版/得体版/轻松版), let user choose. Label each with a recommended one.

### 2. 有故事背景时的分寸
When the user shares backstory (e.g., "师兄帮了我很多但最后没去成"):
- **坦诚但不沉重**: mention the facts, express gratitude, don't wallow
- **主动权归对方**: "是我女朋友考虑到……" — framing shows honesty without blame
- **收在感恩上**: end on gratitude, not regret

### 3. 对方突然切语言时
If the recipient switches language (e.g., Chinese to English):
- Mirror the language switch naturally
- Keep length roughly equal to the incoming message
- Use appropriate titles (Prof., Dr., etc. in English; 老师/院长 in Chinese)

### 4. 批量群发优化
When writing for many people at once:
- Group by relationship tier
- Keep each greeting self-contained
- Vary the wording slightly to avoid sounding copy-paste
- Don't over-elaborate for casual relationships

### 5. 表情使用
- 长辈: 1-2 个, 选 🎉🎋🎊
- 同辈: 可以多用 😄💪😊🐧
- 群聊: 响应群内已有风格

## Pitfalls

- **不要过度客套**: 长辈面前不要写得像公文，平辈面前不要写得像求职信
- **不要主动提尴尬细节**: 生育问题、感情分手等，除非用户明确要求
- **不要写太长**: 除非有深仇大恩，5行以内足够
- **节日名+安康/快乐要准确**: 端午用"安康"更稳妥，中秋春节用"快乐"
- **英文称呼要地道**: 英文里用 Prof./Dr. 不用 Teacher
