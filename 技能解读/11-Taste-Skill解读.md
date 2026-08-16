---
title: Taste-Skill解读
tags: [AI技能, 前端设计, 反Slop, 设计流程]
created: 2026-08-05
source: https://github.com/Leonxlnx/taste-skill
---

# Taste-Skill 解读

## 基本信息

- **仓库**：[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
- **Star**：★71,765（反Slop前端框架顶流）
- **定位**：The Anti-Slop Frontend Framework for AI Agents——让 AI 有"品味"，停止生成无聊、通用的 UI
- **兼容**：Codex、Cursor、Claude Code（Agent Skills 标准格式，与 Hermes 兼容）

## 核心机制：三拨盘配置

主技能 `design-taste-frontend`（v2，1206行）的核心是**三个拨盘**，所有布局/动效/密度决策都由它们门控：

| 拨盘 | 范围 | 含义 |
|------|------|------|
| `DESIGN_VARIANCE` | 1-10 | 1=完美对称，10=艺术混乱 |
| `MOTION_INTENSITY` | 1-10 | 1=静态，10=电影级/物理 |
| `VISUAL_DENSITY` | 1-10 | 1=艺术画廊/空灵，10=驾驶舱/数据密集 |

**基线**：`8 / 6 / 4`，除非设计读取覆盖。

### 拨盘推断（信号→值）

| 信号 | VARIANCE | MOTION | DENSITY |
|------|----------|--------|---------|
| "minimalist / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury" | 7-8 | 5-7 | 3-4 |
| "playful / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing / portfolio / marketing (默认)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector / regulated" | 3-4 | 2-3 | 4-5 |

## 核心流程

### 0. 简报推断（先读房间，再动手）

LLM 设计输出差的最大原因：跳过简报推断直接跳到默认美学。

**读取信号**：页面类型 → 用户的氛围词 → 参考信号（URL/截图/竞品）→ 受众 → 已有品牌资产 → 隐性约束（无障碍/公共部门/监管行业——这些覆盖美学偏好）

**输出一行"Design Read"**：
> "Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities + Geist + restrained motion."

**模糊时只问一个问题**，能推断就不问。

### 反默认纪律（Anti-Default Discipline）

禁止默认：AI紫色渐变、深色网格上的居中hero、三个等大特性卡片、到处玻璃拟态、无限循环微动画、Inter + slate-900。

### 2. 简报→设计系统映射

需要真实设计系统时用官方包，不发明 CSS：

| 简报像... | 用... |
|----------|-------|
| Microsoft/企业SaaS | `@fluentui/react-components` |
| Google风格 | `@material/web` + Material 3 tokens |
| IBM企业分析 | `@carbon/react` |
| Shopify | Polaris |
| Atlassian/Jira | `@atlaskit/*` |
| GitHub风格 | `@primer/css` |
| 英国公共服务 | `govuk-frontend` |
| 美国公共服务 | `uswds` |
| 现代React基础 | `@radix-ui/themes` |
| 自有组件SaaS | shadcn/ui |
| Tailwind SaaS | Tailwind v4 + dark: |

## 13个子技能

| 子技能 | 定位 |
|--------|------|
| taste-skill | 主技能：着陆页/作品集/改版（v2实验版） |
| taste-skill-v1 | v1保留版 |
| gpt-taste | Awwwards级 + GSAP动效 |
| image-to-code-skill | 图片参考→代码 |
| imagegen-frontend-web | 生成网页设计参考图（不写代码） |
| imagegen-frontend-mobile | 生成移动端概念图（不写代码） |
| brandkit | 生成品牌套件参考图 |
| redesign-skill | 升级现有项目（审计+修复设计问题） |
| soft-skill | 昂贵软性UI：高级字体、留白、深度、平滑动画 |
| output-skill | 防AI偷懒：省略代码块、占位注释 |
| minimalist-skill | 编辑式干净界面（Notion/Linear风格） |
| brutalist-skill | 原始机械界面、瑞士排版、极端尺度对比 |
| stitch-skill | Google Stitch语义设计规则 |

## 与仓库现有技能对比

| 维度 | Taste-Skill | 本仓库 frontend-design（Anthropic 来源） |
|------|-------------|-----------------------------------|
| 定位 | 完整流程（三拨盘+流程） | 设计原则 |
| 风格流派 | soft/minimalist/brutalist 多流派 | 单一 |
| 图片生成 | imagegen系列（参考图） | 无 |
| 防Slop | 反默认纪律+AI Slop测试 | 三个默认外观清单 |
| 改版 | redesign-skill 专门改版流程 | 提及但不系统 |

**相同点**：都强调反AI模板、设计读取、克制
**不同点**：Taste-Skill 是**可配置流程**（拨盘系统），frontend-design 是**原则集**；Taste-Skill 有风格流派和图片生成，frontend-design 没有

## 可借鉴的提升点

1. **三拨盘系统**：把"设计变体/动效强度/视觉密度"三个可调参数引入前端工作流，让设计有梯度而非一刀切
2. **Design Read 一行声明**：动手前先声明"我在做什么"，防止默认美学
3. **反默认纪律清单**：比 frontend-design 的三个默认外观更全（紫色渐变/网格hero/三卡片/玻璃拟态/无限动画/Inter+slate）
4. **真实设计系统映射表**：简报像什么→用什么官方包，避免发明CSS
5. **output-skill**：防AI省略代码块/占位注释——与 verify 证据先行呼应

## 收录状态

✅ 已收录至本仓库技能库（对应 `skills/` 下的 taste-skill-v1、design-taste-frontend、gpt-taste 等子技能目录）
