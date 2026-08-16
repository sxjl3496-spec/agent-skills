---
title: UI技能包与SimpleEnglish解读
tags: [AI技能, UI设计, 写作, 开源]
created: 2026-08-05
source: github
license: MIT
---

# jakubkrehel/skills 与 SimpleEnglish 技能解读

> 来源：GitHub AI Agent 项目日报（2026-08-05）。

## 1. jakubkrehel/skills（UI技能百宝箱，★3,049，MIT）

- **仓库**：https://github.com/jakubkrehel/skills
- **定位**：7个"更好UI"系列技能包，覆盖界面构建的各个维度
- **许可证**：MIT（可自由使用/修改/商用，适合开源）
- **安装位置**：`development/better-ui-kit/`（7个子技能）

### 7个子技能一览

| 技能 | 作用 |
|------|------|
| better-accessibility | 无障碍优化（对比度/键盘导航/ARIA） |
| better-colors | 色彩方案优化（可访问配色/主题） |
| better-interface | 跨学科界面审查（协调其他better-*技能） |
| better-layout | 布局优化（间距/对齐/层级） |
| better-typography | 字体排印优化（字号/行高/字重） |
| better-ui | UI整体质量提升 |
| better-writing | UX文案写作（按钮标签/错误消息/界面文案） |

### 使用场景
- 用户做**桌面宠物界面**、**网页/工具前端**时，让 Hermes 用这些技能审查和优化UI
- 与 taste-skill（审美）、impeccable（反模式检测）形成**UI质量三件套**：
  - taste-skill：审美方向
  - impeccable：代码级反模式检测
  - better-ui-kit：功能/无障碍/文案维度

## 2. SimpleEnglish（简化技术英语，★1,611，MIT）

- **仓库**：https://github.com/AminBlg/SimpleEnglish
- **技能名**：simple-english
- **许可证**：MIT
- **安装位置**：`development/simple-english/`

### 是什么
基于 **ASD-STE100** 航空航天简化技术英语标准的写作技能。STE 是航空/国防工业写维护手册用的受控语言，规则保证"疲惫且非英语母语的读者也不会误读指令"。

### 53条规则核心
- 句子 20/25 词上限
- 一词一义（禁止同义词轮换）
- 只用简单时态
- 主动语态
- 条件先于命令

### 与 no-ai-slop 的关系
STE 规则**顺带消灭AI味**（长句、同义词轮换、hedges模糊语、填充词、装饰从句）——与 Hermes 现有 no-ai-slop 技能互补但更严格：no-ai-slop 是"别写AI味"，simple-english 是"按航空标准写"。

### 两种模式
- **pragmatic（务实）**：日常技术文档
- **strict（严格）**：航空手册级

### 附带的评测（evals/）
仓库自带压力测试（evals/pressure-tests.md）和结果（evals/results/RESULTS.md）——开源项目做质量评测的范例，值得借鉴。

## 使用建议

- 写英文论文摘要/引言 → simple-english（务实模式）
- 写 API 文档/README/操作手册 → simple-english（严格模式）
- 做桌宠界面 → better-ui-kit 全家桶
- 界面文案（按钮/提示）→ better-writing
