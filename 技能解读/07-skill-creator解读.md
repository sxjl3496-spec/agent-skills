---
title: skill-creator解读
tags: [AI技能, 技能创建, 评测, Anthropic]
created: 2026-08-05
source: https://github.com/anthropics/skills/tree/main/skills/skill-creator
---

# skill-creator 解读

## 基本信息

- **来源**：Anthropic 官方技能仓库 `anthropics/skills`（★166K）；Composio 社区有简化版
- **官方描述**：Create new skills, modify and improve existing skills, and measure skill performance
- **排行**：第7名
- **定位**：教你写出能被正确触发的 SKILL.md

## 核心机制

技能创建 + 迭代改进 + **性能量化评测**的完整循环。

### 高层流程（迭代循环）

1. 决定技能要做什么、大致怎么做
2. 写技能草稿
3. 创建几个测试 prompts，用"带技能访问权的 agent"跑它们
4. 帮用户定性+定量评估结果
   - 后台运行期间，起草量化评测（没有的话）；有则直接用或修改
   - 用 `eval-viewer/generate_review.py` 展示结果给用户看
5. 根据用户评估反馈重写技能（也从量化 benchmark 暴露的明显缺陷中学习）
6. 重复直到满意
7. 扩大测试集，更大规模再试

### 技能完成后

运行 **description improver**（独立脚本）优化技能 description，提高触发准确性。

## 创建技能四问（Capture Intent）

1. 这个技能应该让 agent 能做什么？
2. 何时触发？（用户什么话/上下文）
3. 期望输出格式？
4. 是否设置测试用例验证？（客观可验证输出的技能受益于测试用例；主观输出如写作风格通常不需要——但让用户决定）

## 与用户沟通

- 受众跨技术熟练度光谱（水管工到程序员）
- "evaluation" "benchmark" 是边界词，"JSON" "assertion" 要看到用户熟悉信号才用
- 不确定就简要解释

## 附属资源

```
skill-creator/
├── agents/
│   ├── analyzer.md      # 分析 agent 提示词
│   ├── comparator.md    # 对比 agent 提示词
│   └── grader.md        # 评分 agent 提示词
├── assets/
│   └── eval_review.html
├── eval-viewer/
│   ├── generate_review.py
│   └── viewer.html
├── references/
│   └── schemas.md
└── scripts/
    ├── aggregate_benchmark.py
    └── generate_report.py
```

## Composio 版 skill-creator 要点（补充）

- **Concise is Key**：上下文窗口是公共资源。默认假设 agent 已经很聪明，只添加它没有的上下文。挑战每条信息："agent 真的需要这个解释吗？"
- **Set Appropriate Degrees of Freedom**：自由度匹配任务的脆弱性和变异性
  - 高自由度（文本指令）：多种方法都有效时用
  - 低自由度（严格流程）：步骤必须明确时用
- **Skills 提供什么**：专用工作流、工具集成、领域专长、捆绑资源

## 与 Hermes skill-distiller 的对比

| 维度 | skill-creator | Hermes skill-distiller |
|------|--------------|------------------------|
| 流程 | 创建→测试→评测→迭代循环 | 从教程/文档蒸馏技能 |
| 评测 | 量化 benchmark + 方差分析 + description优化 | 无评测环节 |
| 侧重 | 技能全生命周期管理 | 单次提取 |
| 输入 | 从零创建或改进现有 | 已有外部文档 |

**相同点**：都创建/改进 SKILL.md；都强调 description 触发优化

**不同点**：skill-creator 有完整测试-评测-迭代循环（agent 级 eval），skill-distiller 是单次转换（无验证）

**互补关系**：distiller 负责"从资料提取"，creator 负责"创建后验证优化"。可串联：distiller 产出草稿 → creator 流程评测迭代。

## 可借鉴的提升点

1. **测试 prompts + 量化评测循环**：Hermes 的 skill-distiller 缺评测环节，可引入
2. **description improver**：独立脚本优化技能触发准确性——Hermes 技能描述也可定期优化
3. **四问澄清法**：创建技能前先问清做什么/何时触发/输出格式/是否要测试
4. **上下文公共资源原则**：技能写作要精简，不重复 agent 已知内容
5. **分级自由度**：根据任务脆弱性决定指令的具体程度

## 安装状态

✅ 已安装到 Hermes 技能库 `development\skill-creator\`（Anthropic 完整版，含 agents/、eval-viewer/、scripts/）
