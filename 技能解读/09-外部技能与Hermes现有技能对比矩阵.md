---
title: 外部技能与Hermes现有技能对比矩阵
tags: [AI技能, 对比分析, 技能体系]
created: 2026-08-05
---

# 外部技能与 Hermes 现有技能对比矩阵

## 总览表

| 外部技能 | 来源 | Hermes对应技能 | 相同点 | 不同点 | 借鉴价值 |
|---------|------|---------------|--------|--------|---------|
| **Superpowers** | obra ★266K | plan、verify、debug-helper | 计划→执行→验证三段式 | 4个硬门禁+子agent驱动+worktree隔离+TDD铁律 | ⭐⭐⭐⭐⭐ |
| **figma-implement-design** | openai官方 | 无 | - | 完全新增（设计转代码） | ⭐⭐⭐（需Figma MCP） |
| **mcp-builder** | anthropics ★166K | 无 | - | 完全新增（MCP开发） | ⭐⭐⭐⭐ |
| **frontend-design** | anthropics ★166K | 无 | - | 完全新增（差异化UI设计） | ⭐⭐⭐⭐ |
| **create-plan** | Composio社区 | plan | 任务规划、防跑偏 | create-plan极简模板 vs plan重型全流程 | ⭐⭐⭐ |
| **gh-fix-ci** | Composio社区 | debug-helper | 都是排查问题 | gh-fix-ci专精GitHub CI+脚本化 | ⭐⭐⭐ |
| **skill-creator** | anthropics ★166K | skill-distiller | 都创建技能 | creator有评测循环，distiller无 | ⭐⭐⭐⭐ |
| **awesome-codex-skills** | Composio索引 | 无（索引非技能） | - | 47技能索引+评级体系 | ⭐⭐⭐ |

## 深度对比

### 1. Superpowers vs (plan + verify + debug-helper)

| 能力 | Superpowers | Hermes组合 | 差距 |
|------|-------------|-----------|------|
| 需求澄清 | brainstorming（HARD-GATE：未批准不实施） | plan阶段0表达优化 | Hermes无强制设计门禁 |
| 计划 | writing-plans（零上下文工程师视角） | plan阶段1（模型路由+审批） | Hermes更重但缺任务粒度指导 |
| 调试 | systematic-debugging（无根因不修复） | debug-helper（错误分类） | Hermes无"根因铁律" |
| 验证 | verification-before-completion（证据先行） | verify（cross_model_verify） | Hermes已有跨模型验证，更强 |
| TDD | test-driven-development（铁律） | 无 | ❌ 完全缺失 |
| 代码审查 | requesting/receiving-code-review | 无 | ❌ 完全缺失 |
| 并行开发 | dispatching-parallel-agents + worktree | delegate_task（v0.16.0受限） | Hermes有基础但受限 |
| 分支管理 | finishing-a-development-branch | 无 | ❌ 缺失 |

### 2. create-plan vs plan

| 维度 | create-plan | Hermes plan |
|------|-------------|-------------|
| 输出 | 单条消息内模板化计划 | 全流程（阶段0-4） |
| 提问 | 最多1-2个，多选题 | 完整表达优化+逐项确认 |
| 模式 | 只读 | 边规划边执行 |
| 模板 | Scope In/Out + checklist + Open questions | 复杂度评估+模型路由+审批+陷阱库 |
| 适用 | 快速编码任务计划 | 复杂多步任务 |

**结论**：互补关系。create-plan 适合快速轻量计划；plan 适合重型全流程。可将 create-plan 的模板要素（Scope In/Out、动词开头checklist、Open questions）吸收进 plan 的阶段1。

### 3. skill-creator vs skill-distiller

| 维度 | skill-creator | skill-distiller |
|------|--------------|-----------------|
| 输入 | 从零创建/改进现有技能 | 外部教程/文档 |
| 评测 | 测试prompts + 量化benchmark + 方差分析 | 无 |
| 迭代 | 循环直到满意 | 单次提取 |
| 触发优化 | description improver 脚本 | 无 |

**结论**：可串联使用——distiller 从资料提取草稿，creator 流程评测迭代。建议把 creator 的"测试prompts+量化评测"环节引入 distiller 作为质量门控。

### 4. gh-fix-ci vs debug-helper

| 维度 | gh-fix-ci | debug-helper |
|------|-----------|-------------|
| 领域 | GitHub Actions CI 专用 | 通用调试 |
| 工具 | gh CLI + inspect_pr_checks.py 脚本 | 日志分析、API诊断 |
| 协作 | 显式依赖 plan 技能 | 独立 |

**结论**：互补。gh-fix-ci 专精 GitHub CI，debug-helper 通用排查。gh-fix-ci 的"技能显式依赖其他技能"协作模式值得推广。

### 5. frontend-design / figma-implement-design / mcp-builder

三者均为 Hermes 完全缺失的能力：
- **frontend-design**：差异化视觉设计方法论（反AI模板）
- **figma-implement-design**：Figma→代码 1:1 还原（需Figma MCP）
- **mcp-builder**：MCP server 开发四阶段指南

## 借鉴优先级排序

| 优先级 | 借鉴点 | 来源 | 落地对象 | 状态 |
|--------|--------|------|---------|------|
| P0 | 证据先行铁律（验证命令+确认输出才能声称完成） | Superpowers | verify技能 | ✅ 已落地(2026-08-05) |
| P0 | TDD铁律（先写测试看失败再实现） | Superpowers | 新增development技能 | ✅ 已安装test-driven-development |
| P0 | 无根因不修复（Phase 1调查完成前禁止修复） | Superpowers | debug-helper | ✅ 已落地(2026-08-05) |
| P1 | Scope In/Out + Open questions 模板 | create-plan | plan技能阶段1 | ✅ 已落地(2026-08-05) |
| P1 | 测试prompts+量化评测循环 | skill-creator | skill-distiller | ✅ 已落地(2026-08-05) |
| P1 | description improver 触发优化 | skill-creator | 全部Hermes技能 | ✅ 已写入distiller步骤4.3 |
| P2 | 反AI模板清单（三个默认外观） | frontend-design | 前端任务 | 📋 待实战验证 |
| P2 | 技能显式依赖协作模式 | gh-fix-ci | 技能间引用 | ✅ 已写入distiller模板 |
| P2 | HARD-GATE 设计批准门禁 | Superpowers | plan技能 | ✅ 已落地(2026-08-05) |

## 改进落地详情（2026-08-05）

### 已落地改进（7项）

**1. verify 技能：证据先行门禁**
- 修改：`skills/verify/SKILL.md` 新增"铁律：证据先行"章节
- 核心：声称完成前必须本回合内运行验证命令并确认输出（NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE）
- 提升：交付质量——每个"完成"都附带实测证据，杜绝假阳性

**2. debug-helper 技能：根因调查门禁**
- 修改：`skills/debug-helper/SKILL.md` 新增"铁律：无根因不修复"章节
- 核心：Phase 1 根因调查（复现→证据→缩小范围→确认根因）完成前禁止修复
- 提升：排查效率——一次定位根因，避免症状修复反复复发

**3. plan 技能：HARD-GATE + Scope/Open questions**
- 修改：`skills/plan/SKILL.md` 步骤1.3 计划模板
- 新增：设计批准门禁（任何规模必须确认）+ 范围In/Out标注 + 最多3条待确认事项
- 提升：方向把控——防跑偏、范围清晰、未知项提前暴露

**4. skill-distiller 技能：评测循环**
- 修改：`skills/development/skill-distiller/SKILL.md` 新增步骤4
- 新增：触发测试（正/边界/负面）+ 效果评测 + description优化 + 迭代
- 提升：技能质量——蒸馏出的技能经过触发验证才交付

**5. skill-distiller 模板：依赖声明**
- 修改：SKILL.md 生成模板新增"## 依赖技能"章节
- 提升：技能组合有迹可循，复杂任务自动串联

**6. TDD 铁律技能**
- 已安装：`skills/superpowers/test-driven-development/`
- 提升：代码质量——先测试后实现，bug率下降

**7. 反AI模板清单（frontend-design）**
- 已安装：`skills/development/frontend-design/`
- 提升：视觉质量——避免AI默认模板外观

### 待实战验证（2项）

- **figma-implement-design**：需先配置 Figma MCP server 才能实战
- **gh-fix-ci**：需 gh CLI 认证（`gh auth login`）后实战

## Impeccable CLI 集成记录（2026-08-05）

- **集成对象**：verify 技能
- **内容**：新增「前端反模式检测」章节——前端交付物验证时自动跑 `npx impeccable detect`
- **实测**：测试HTML检测出3个反模式（side-tab侧边条、cramped-padding内边距、ai-color-palette紫色调），CLI 完全可用
- **注意**：CLI 路径参数必须用 Windows 路径（`C:\...`），不能用 MSYS 路径（`/tmp/...`）
- **提升**：前端交付物验证从"AI主观审查"升级为"代码级客观检测"，且零token消耗
