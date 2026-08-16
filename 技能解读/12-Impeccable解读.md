---
title: Impeccable解读
tags: [AI技能, 前端设计, 23命令, Hermes原生]
created: 2026-08-05
source: https://github.com/DevvGwardo/impeccable
---

# Impeccable 解读

## 基本信息

- **仓库**：[DevvGwardo/impeccable](https://github.com/DevvGwardo/impeccable)
- **原版**：pbakaus/impeccable（Apache 2.0），构建于 Anthropic frontend-design 之上
- **关键**：**专门为 Hermes Agent 移植**（README 明确 "ported to Hermes Agent"）
- **定位**：23个命令的前端设计技能——塑造、审计、打磨、精炼 UI

## 核心机制：5阶段23命令

| 阶段 | 命令 | 类别 |
|------|------|------|
| **Learn** | teach（一次性设置：PRODUCT.md/DESIGN.md）、document（从代码生成DESIGN.md） | Build |
| **Shape** | shape（UX/UI规划）、craft（完整塑造+构建流程）、extract（提取组件到设计系统） | Build |
| **Evaluate** | critique（UX设计评审）、audit（技术质量检查：a11y/性能/响应式） | Evaluate |
| **Enhance** | colorize（战略色彩）、animate（刻意动效）、typeset（字体修复）、layout（布局间距）、delight（愉悦时刻）、overdrive（技术非凡效果） | Enhance |
| **Ship** | polish（最终打磨）、harden（错误处理/i18n/溢出）、onboard（首次运行/空状态）、optimize（性能）、adapt（设备适配）、clarify（UX文案）、bolder（放大平淡）、quieter（收敛过度）、distill（剥离本质） | Refine/Fix |
| **Iterate** | live（浏览器可视化变体迭代） | Iterate |

**路由**：用户说 `impeccable:<command> [target]` → 加载对应 reference 文件执行。无匹配但设计相关 → 直接应用共享设计法则。

## Setup 三步

1. **读上下文**：检查 PROJECT.md/DESIGN.md，缺失则建议先 `impeccable:teach`
2. **识别 register**：每个设计任务是 **brand**（营销/着陆/作品集：设计即产品）或 **product**（应用UI/管理后台：设计服务产品）
3. **加载对应 register reference**

## 共享设计法则（适用于所有设计）

### 色彩
- 用 OKLCH，接近0或100的亮度时降低chroma（极端高chroma刺眼）
- **绝不用 `#000` 或 `#fff`**：每个中性色都向品牌色相偏移（chroma 0.005-0.01即可）
- 先选**色彩策略**再选颜色（克制≤10%点缀 / 承诺30-60%主色 / 全调色板3-4角色 / 浸透=表面即颜色）

### 主题
- 深/浅色**永远不是默认**。选之前写一句物理场景："谁用、在哪、什么环境光、什么心情"。句子不能强制答案就是不够具体。
- "可观测性dashboard"不强制答案；"凌晨2点在昏暗房间盯着27寸显示器看告警严重性的SRE"强制。

### 排版
- 正文行长 65-75ch
- 层级靠字号+字重对比（步间≥1.25比例）

### 布局
- 变化间距制造节奏（处处相同padding=单调）
- 卡片是懒惰答案（嵌套卡片永远错）
- 不是什么都包container

### 动效
- 不动画CSS布局属性
- 指数缓出（ease-out-quart/quint/expo），无弹跳无弹性

### 绝对禁令（反模式）
1. 侧条边框（border-left/right彩色点缀）
2. 渐变文字（background-clip: text）
3. 玻璃拟态作为默认
4. hero指标模板（大数字+小标签+渐变）
5. 相同卡片网格
6. 模态框作为第一想法

### 文案
- 每个词都要有价值，无重复标题
- **禁用破折号（em dash）**——用逗号/冒号/分号/句号/括号

### AI Slop 测试
> 如果有人看这个界面能毫不犹豫说"AI做的"，它就失败了。

**一阶反射检查**：光看品类就能猜到主题+调色板（"可观测性→深蓝"、"医疗→白+青"、"金融→藏青+金"、"加密→霓虹黑"）→ 训练数据反射，重做场景句和色彩策略。

**二阶反射检查**：光看品类+反例就能猜到美学家族（"不是SaaS奶油色的AI工作流工具→编辑排版风"）→ 更深一层的陷阱。

## CLI 工具（独立反模式检测）

```bash
npx impeccable detect src/                   # 扫描目录
npx impeccable detect index.html             # 扫描HTML文件
npx impeccable detect https://example.com    # 扫描URL（需Puppeteer）
npx impeccable detect --fast --json .        # 纯正则+JSON输出
```

- 扫描 HTML/CSS/JSX/TSX/Vue/Svelte 的 **25+反模式**
- 退出码：0=干净，2=发现问题
- 需 Node.js 18+
- **无需AI harness**——可独立用于CI/验证

## 38个reference文件

```
reference/
├── 设计域（11个）: brand, product, typography, color-and-contrast, spatial-design,
│                   motion-design, interaction-design, responsive-design, ux-writing,
│                   cognitive-load, heuristics-scoring
├── 命令实现（23个）: craft, shape, teach, document, extract, critique, audit, polish,
│                   bolder, quieter, distill, harden, onboard, animate, colorize,
│                   typeset, layout, delight, overdrive, clarify, adapt, optimize, live
└── 其他: codex, personas, product
```

## 与仓库现有技能对比

| 维度 | Impeccable | 本仓库 frontend-design | Taste-Skill |
|------|-----------|----------------------|-------------|
| 形式 | 23命令体系 | 原则集 | 三拨盘流程 |
| 命令式交互 | ✅ `impeccable:audit` | ❌ | ❌ |
| CLI检测器 | ✅ npx impeccable detect | ❌ | ❌ |
| register区分 | ✅ brand/product | ❌ | 部分 |
| 设计域深度 | 38个reference | 单文件 | 单文件 |

**关系**：三者互补——Anthropic frontend-design 提供设计原则，Taste-Skill 提供流程配置（拨盘），Impeccable 提供命令体系和验证工具（CLI）。

## 可借鉴的提升点（⭐重点）

1. **CLI 反模式检测器**（最高价值）：`npx impeccable detect` 可独立运行——直接用于前端交付物的硬验证（类似 verify 技能的证据先行），且不消耗AI token
2. **命令体系设计**：23个命令分5阶段，用户可用 `impeccable:xxx` 精确触发——技能命令化设计范式
3. **AI Slop 测试**（一阶/二阶反射检查）：比 frontend-design 的三个默认外观更系统——与 no-ai-slop 呼应
4. **register 区分**（brand vs product）：设计前先判断"设计即产品"还是"设计服务产品"，影响整个设计决策
5. **物理场景句**：主题选择前写一句物理场景，强制具体化（"SRE凌晨2点看告警"vs"可观测性dashboard"）

## 收录状态

✅ 已收录至本仓库技能库（对应 `skills/impeccable/`，69 个文件：SKILL.md + 38 个 reference）
⭐ 特别说明：该技能为 Hermes Agent 原生移植，frontmatter 含 `metadata.hermes` 字段，天然兼容
