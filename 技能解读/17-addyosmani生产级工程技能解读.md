---
title: addyosmani生产级工程技能解读
tags: [AI技能, 工程技能, addyosmani, 开发方法论]
created: 2026-08-05
source: https://github.com/addyosmani/agent-skills
---

# addyosmani/agent-skills 生产级工程技能解读

## 基本信息

- **仓库**：[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- **Star**：★81,620
- **作者**：Addy Osmani（Google Chrome 团队工程经理）
- **定位**：Production-grade engineering skills for AI coding agents——把资深工程师的工作流、质量门禁、最佳实践编码为技能，让 AI agent 在开发全阶段一致遵循

## 设计哲学

**6阶段开发生命周期**（DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP）：

```
  DEFINE          PLAN           BUILD          VERIFY         REVIEW          SHIP
 ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐      ┌──────┐
 │ Idea │ ───▶ │ Spec │ ───▶ │ Code │ ───▶ │ Test │ ───▶ │  QA  │ ───▶ │  Go  │
 │Refine│      │  PRD │      │ Impl │      │Debug │      │ Gate │      │ Live │
 └──────┘      └──────┘      └──────┘      └──────┘      └──────┘      └──────┘
  /spec          /plan          /build        /test         /review       /ship
```

**8个斜杠命令**映射生命周期：

| 命令 | 做什么 | 核心原则 |
|------|--------|---------|
| `/spec` | 定义要构建什么 | 先规格后代码 |
| `/plan` | 规划怎么构建 | 小原子任务 |
| `/build` | 增量构建 | 一次一片 |
| `/test` | 证明能工作 | 测试即证明 |
| `/review` | 合并前审查 | 提升代码健康 |
| `/webperf` | 审计web性能 | 先测量后优化 |
| `/code-simplify` | 简化代码 | 清晰胜于聪明 |
| `/ship` | 发布到生产 | 更快更安全 |

## 23个技能详解（选取6个核心）

### 1. spec-driven-development（规格驱动开发）

- **触发**：新项目/功能/重大变更且无规格、需求模糊不清时
- **不适用**：单行修复、拼写纠正、需求明确且自包含
- **门禁工作流**：SPECIFY→PLAN→TASKS→IMPLEMENT 四阶段，每阶段必须人类审查通过才能进入下一阶段
- **核心**：写代码前先写结构化规格——定义建什么、为什么、怎么知道完成了。立即暴露假设
- **与plan技能关系**：spec是plan的上游——spec定义"建什么"，plan定义"怎么建"

### 2. source-driven-development（源码驱动开发）

- **触发**：构建框架特定代码、样板代码、需要权威/正确实现时
- **核心**：**每个框架特定代码决策必须由官方文档支撑**。不从记忆实现——验证、引用、让用户看到来源
- **流程**：DETECT（检测技术栈和版本）→ FETCH（获取相关文档）→ IMPLEMENT（遵循文档化模式）→ CITE（展示来源）
- **反模式**：从训练数据记忆写框架代码（API会过时、最佳实践会演变）
- **价值**：代码可溯源，用户可验证

### 3. doubt-driven-development（怀疑驱动开发）

- **触发**：正确性比速度重要、在陌生代码中工作、高风险（生产/安全敏感/不可逆操作）时
- **核心**：**自信的答案≠正确的答案**。长会话积累上下文会把假设悄悄变成"事实"。本技能强制在非平凡输出定稿前，物化一个"新鲜上下文审查者"——偏向**证伪**而非批准
- **与/review区别**：/review是对已完成成品的裁决；doubt是进行中的姿态——非平凡决策在纠偏还便宜时交叉审查
- **流程**：CLAIM（写下主张+为何重要）→ EXTRACT（隔离工件+契约，剥离推理）→ DOUBT（新鲜上下文审查者+对抗性提示）→ RECONCILE（逐条分类发现）→ STOP（停止条件：琐碎发现/3轮/用户覆盖）
- **非平凡判定**：引入分支逻辑、跨模块边界、断言类型系统无法验证的属性、正确性依赖未来读者看不到的上下文、爆炸半径不可逆

### 4. context-engineering（上下文工程）

- **触发**：新会话开始、agent输出质量下降、任务切换、需要配置规则文件和项目上下文时
- **核心**：优化agent上下文设置——配置规则文件（AGENTS.md/CLAUDE.md）、管理上下文占用
- **价值**：与Hermes的 AGENTS.md 体系直接呼应

### 5. idea-refine（想法精炼）

- **触发**：想法模糊、需要从概念到清晰规格时
- **核心**：把粗糙想法精炼成可执行的规格——DEFINE阶段的第一步

### 6. incremental-implementation（增量实现）

- **触发**：从规格/计划开始逐步实现时
- **核心**：一次实现一片，每片可测试可提交——BUILD阶段的核心纪律
- **价值**：与plan技能的"小原子任务"原则一致

## 其余17个技能速览

| 技能 | 定位 |
|------|------|
| api-and-interface-design | API和接口设计 |
| browser-testing-with-devtools | 浏览器DevTools测试 |
| ci-cd-and-automation | CI/CD自动化 |
| code-review-and-quality | 代码审查和质量 |
| code-simplification | 代码简化 |
| debugging-and-error-recovery | 调试和错误恢复 |
| deprecation-and-migration | 弃用和迁移 |
| documentation-and-adrs | 文档和ADR |
| frontend-ui-engineering | 前端UI工程 |
| git-workflow-and-versioning | Git工作流 |
| interview-me | 面试模拟 |
| observability-and-instrumentation | 可观测性 |
| performance-optimization | 性能优化 |
| planning-and-task-breakdown | 规划和任务分解 |
| security-and-hardening | 安全和加固 |
| shipping-and-launch | 发布 |
| test-driven-development | TDD |
| using-agent-skills | 使用技能指引 |

## 与 Hermes 现有技能对比

| 维度 | addyosmani | Hermes现有 |
|------|-----------|-----------|
| 规格 | spec-driven-development | plan（任务规划）——缺spec环节 |
| 验证 | doubt-driven-development | verify（证据先行）——互补 |
| 溯源 | source-driven-development | 无——Hermes缺"官方文档溯源"纪律 |
| 上下文 | context-engineering | AGENTS.md体系 |
| TDD | test-driven-development | superpowers/test-driven-development |

**互补关系**：spec-driven 是 plan 的上游（先规格后规划）；doubt-driven 是 verify 的进行中版本（先怀疑后验证）；source-driven 是 Hermes 缺失的"官方文档溯源"纪律。

## 可借鉴的提升点

1. **spec驱动**：Hermes plan 缺"规格先行"环节——spec定义建什么，plan定义怎么建。可把 spec-driven 的四阶段门禁引入 plan
2. **doubt对抗审查**：verify 是事后验证，doubt 是事中对抗——"新鲜上下文审查者偏向证伪"的机制值得引入
3. **source溯源**：Hermes 写框架代码时缺乏"必须引用官方文档"的强制纪律
4. **8斜杠命令体系**：/spec /plan /build /test /review /ship 的生命周期映射清晰

## 收录状态

✅ 收录6个核心技能：spec-driven-development、source-driven-development、doubt-driven-development、context-engineering、idea-refine、incremental-implementation
