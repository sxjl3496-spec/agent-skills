---
title: Superpowers全流程方法论解读
tags: [AI技能, Superpowers, TDD, 方法论]
created: 2026-08-05
source: https://github.com/obra/superpowers
---

# Superpowers 全流程方法论解读

## 基本信息

- **仓库**：[obra/superpowers](https://github.com/obra/superpowers)
- **Star**：★266,304（排行榜第1，生态顶流）
- **定位**：完整的软件工程方法论，基于14个可组合技能 + 初始化指令
- **核心卖点**：强制 agent 走 TDD+代码审查，坚决不偷懒

## 设计哲学

> Superpowers 是"完整的软件开发方法论"，不是单个技能。它从你启动 coding agent 那一刻就开始工作：不直接写代码，而是先问清楚你要做什么，把规格拆成小块给你确认，然后生成一份"足够让一个热情但没品味、没判断力、没项目背景、讨厌测试的初级工程师"也能执行的实现计划，强调真正的红/绿 TDD、YAGNI（You Aren't Gonna Need It）、DRY。然后启动子agent驱动开发，让agent逐任务执行、检查、审查、继续。agent 可以自主工作数小时不偏离计划。

## 14个子技能详解

### 1. using-superpowers（总入口）
- **触发**：任何对话开始
- **核心**：<EXTREMELY-IMPORTANT> 只要有1%可能某个技能适用，就必须调用技能。技能适用时你没有选择，必须用。
- **关键**：Red Flags 表格列出"这是简单问题"等合理化借口，帮助 agent 识别自己在偷懒

### 2. brainstorming（头脑风暴→设计）
- **触发**：任何创意工作前（建功能、改行为）**必须**使用
- **HARD-GATE**：未经用户批准设计前，禁止写任何代码、脚手架、实施动作。适用于每个项目，无论多简单
- **反模式**："这太简单不需要设计"——简单项目恰恰是未检查假设浪费最多工作的地方
- **流程**：探索项目上下文 → 逐个问澄清问题 → 提出2-3个方案带权衡 → 分段展示设计并逐个获批 → 写设计文档 → 规格自审

### 3. writing-plans（写计划）
- **触发**：有规格或需求、多步任务、碰代码之前
- **核心**：假设工程师对代码库零背景、品味可疑。记录所有必要信息：任务对应的文件、代码、测试、文档、如何测试。整份计划拆成 bite-sized 任务。
- **原则**：DRY、YAGNI、TDD、频繁提交
- **文件结构**：先映射文件职责，再分解任务。任务是最小可独立测试单元，值得新鲜审查者把关

### 4. executing-plans（执行计划）
- **触发**：计划已批准，开始实施
- **核心**：按计划逐任务执行，每个任务自带测试周期

### 5. test-driven-development（TDD铁律）
- **触发**：实现任何功能或 bugfix 前
- **铁律**："如果你没看到测试失败，你就不知道测试是否正确。违反规则的文字就是违反规则的精神。"
- **适用**：新功能、bug修复、重构、行为变更（始终）
- **例外（问人类伙伴）**：一次性原型、生成代码、配置文件

### 6. systematic-debugging（系统化调试）
- **触发**：任何 bug、测试失败、意外行为
- **铁律**：**没有根因调查就不准修复。症状修复就是失败。**
- **Iron Law**：NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
- **流程**：Phase 1 根因调查完成前，禁止提出修复方案

### 7. verification-before-completion（完成前验证）
- **触发**：声称工作完成/修复/通过前，提交或建PR前
- **铁律**：**永远证据先行。** 没有新鲜的验证证据就不能声称完成。
- **Gate Function**：声称任何状态或表达满意之前，必须先运行验证命令并确认输出

### 8. subagent-driven-development（子agent驱动开发）
- **触发**：计划批准后，逐任务实施
- **核心**：agent 为每个工程任务派发子agent，子agent执行、审查其工作、继续前进
- **配套**：implementer-prompt.md、task-reviewer-prompt.md、re-review-prompt.md

### 9. dispatching-parallel-agents（并行agent调度）
- **触发**：多个独立任务可并行
- **核心**：在隔离的 git worktree 中并行派发 agent

### 10. requesting-code-review / receiving-code-review（代码审查）
- **触发**：完成开发后请求审查 / 收到审查反馈
- **核心**：code-reviewer.md 提供审查者提示词；接收审查时如何吸收反馈

### 11. using-git-worktrees（git worktree 隔离）
- **触发**：子agent开发前
- **核心**：每个子agent在隔离 worktree 工作，避免互相污染

### 12. finishing-a-development-branch（收尾分支）
- **触发**：功能完成后合并分支
- **核心**：清理 worktree、确认测试通过、合并

### 13. writing-skills（写技能）
- **触发**：为 superpowers 体系编写新技能
- **核心**：技能要描述"动作"而非"特定工具"，保持 harness 无关

## 与 Hermes 现有技能的对比

| 维度 | Superpowers | Hermes现有 |
|------|-------------|-----------|
| 计划 | writing-plans：零上下文工程师视角 | plan：阶段0-4+模型路由+审批 |
| 验证 | verification-before-completion：证据先行铁律 | verify：cross_model_verify跨模型验证 |
| 调试 | systematic-debugging：无根因不修复 | debug-helper：错误分类、日志分析 |
| 审查 | requesting/receiving-code-review | 无对应 |
| 开发 | TDD铁律+子agent驱动+worktree隔离 | 无对应 |

## 可借鉴的提升点（⭐重点）

1. **HARD-GATE 机制**：设计未批准不实现。Hermes 的 plan 技能已有"等待确认"环节，但可强化为"任何规模项目都必须先设计后实施"
2. **证据先行铁律**：verification-before-completion 的"本消息内没跑过验证就不能声称通过"，比 Hermes verify 更严格
3. **子agent驱动开发**：Hermes 的 delegate_task 可借鉴"逐任务派发+审查+继续"模式（注：v0.16.0 credential pool bug 限制可用性）
4. **1%规则**：只要有1%可能技能适用就必须调用——可强化 Hermes 技能的触发纪律
5. **TDD 铁律**：Hermes 无 TDD 技能，test-driven-development 可直接补位

## 安装状态

✅ 已安装到 Hermes 技能库 `superpowers\` 分类（14个子技能全部识别启用）
