---
title: create-plan解读
tags: [AI技能, 任务规划, Composio]
created: 2026-08-05
source: https://github.com/composio-community/awesome-codex-skills/tree/main/create-plan
---

# create-plan 解读

## 基本信息

- **来源**：Composio 社区 `composio-community/awesome-codex-skills`（★15.5K）
- **排行榜标签**：Matt Pocock 出品（社区爆款）
- **官方描述**：Create a concise plan. Use when a user explicitly asks for a plan related to a coding task.
- **排行**：第5名
- **定位**：动手前先逼你把方案问清楚，防跑偏

## 核心机制

将用户 prompt 转成**单条最终消息中交付的、可执行的简洁计划**。

### 最小工作流（全程只读模式）

1. **快速扫描上下文**
   - 读 README.md 和明显文档（docs/、CONTRIBUTING.md、ARCHITECTURE.md）
   - 浏览最可能触及的相关文件
   - 识别约束（语言、框架、CI/测试命令、部署形态）

2. **仅在阻塞时提问**
   - 最多问 1-2 个问题
   - 只有无法负责任地规划时才问；优先给多选题
   - 不确定但不阻塞 → 做合理假设继续

3. **用模板创建计划**
   - 1段短文：意图+方法
   - 明确标注 In scope / Not in scope
   - 6-10条原子化、有序的checklist（发现→变更→测试→发布）
   - 动词开头："Add…" "Refactor…" "Verify…" "Ship…"
   - 至少一条测试/验证项 + 一条边界/风险项
   - 未知项 → 最多3条的 Open questions

4. **不输出元解释，直接按模板输出计划**

## 计划模板（严格遵循）

```markdown
# Plan

<1-3句：做什么、为什么、高层方法>

## Scope
- In:
- Out:

## Action items
[ ] <Step 1>
[ ] <Step 2>
[ ] <Step 3>
[ ] <Step 4>
[ ] <Step 5>
[ ] <Step 6>

## Open questions
- <Question 1>
- <Question 2>
- <Question 3>
```

## Checklist 条目指南

**好的条目**：
- 指向可能的文件/模块：src/...、app/...、services/...
- 指名具体验证："Run npm test"、"Add unit tests for X"
- 涉及安全发布：功能开关、迁移计划、回滚说明

**避免**：
- 模糊步骤（"handle backend"、"do auth"）
- 过多微步骤
- 写代码片段（保持计划与实现无关）

## 与仓库 plan 技能的对比

| 维度 | create-plan | 本库 plan |
|------|-------------|-------------|
| 定位 | 单条消息输出简洁计划 | 全流程任务规划器（阶段0-4） |
| 模式 | 全程只读 | 边规划边执行 |
| 提问 | 最多1-2个，多选题优先 | 完整表达优化+需求确认 |
| 格式 | 固定模板（Scope+checklist+Open questions） | 复杂度评估+模型路由+审批 |
| 重量 | 极简 | 重型（含成本估算、陷阱库） |

**相同点**：都是任务规划；都强调先理解需求再动手；都有"防跑偏"目标

**不同点**：create-plan 是轻量模板（适合快速产出计划文本），本库 plan 是完整方法论（含模型路由、交叉验证、质量门控）。create-plan 更像 plan 技能中"阶段1输出计划"这一步的极简版。

## 可借鉴的提升点

1. **Scope In/Out 显式标注**：本库 plan 可加入明确的"范围内/范围外"清单
2. **checklist 动词开头**：可强化 plan 执行步骤的可操作性
3. **Open questions 小节**：计划中明确列出未知项（最多3条）
4. **只读模式**：规划阶段不写文件，本库 plan 阶段1可借鉴
5. **提问克制**：最多1-2个问题，不确定但不阻塞就合理假设
