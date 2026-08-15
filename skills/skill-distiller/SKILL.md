---
name: skill-distiller
description: >
  从教程文章/技术文档/执行记录中蒸馏出可复用 Agent 技能（SKILL.md）。
  借鉴 Resource2Skill 的 distiller_prompt.md 设计模式。
  触发词：蒸馏技能、提取技能、从文章中提取技能、distill skill。
---

# 技能蒸馏器

从人类编写的教程、技术文档、Agent 执行记录中提取可复用的结构化技能。

## 核心理念

借鉴 Resource2Skill 的蒸馏提示词设计：
- 可复现性优先（"如果提取的技能描述不能让人复现方法，就是无用的"）
- 风格优于细节（提取方法论和设计模式，不是逐字复制）
- 强制结构化输出（固定模板，可验证）

## 蒸馏流程

### 步骤1：输入分析

用户提供：
- 文章/文档 URL 或文本
- 或 Agent 执行记录（session_search 找到的会话）

分析内容：
1. 识别核心方法论/工作流
2. 提取关键步骤和决策点
3. 标记可复用的工具调用模式
4. 识别适用的触发条件和场景

### 步骤2：结构化输出

按以下固定模板生成 SKILL.md：

```markdown
---
name: <skill-name>
description: >
  <一句话描述，含触发条件和核心能力>
---

# <技能标题>

## 依赖技能（⭐ 借鉴 gh-fix-ci 协作模式，2026-08-05 引入）
- [依赖技能A]：本技能在<什么环节>调用它（如"修复计划草拟依赖 plan 技能"）
- [依赖技能B]：本技能在<什么环节>调用它
- 无依赖则写：本技能独立运行，不依赖其他技能

## 核心原理
- 解决什么问题？
- 核心方法论/工作流概述
- 与已有技能的关系（互补/替代/增强）

## 使用场景
- 触发条件（用户说什么时触发）
- 适用任务类型
- 不适用场景（明确边界）

## 执行步骤
1. **步骤1**: 具体操作 -> 预期输出
2. **步骤2**: 具体操作 -> 预期输出
3. ...

## 关键决策点
- 决策点A：如果X则选方案1，如果Y则选方案2
- 决策点B：...

## 常见陷阱
- 陷阱1：描述 + 规避方法
- 陷阱2：描述 + 规避方法

## 验证标准
- 如何验证执行成功？
- 交付物质量标准
```

### 步骤3：关联文件生成

根据技能类型，生成配套文件：
- T2+：生成 references/ 参考文档
- T3+：生成 scripts/ 可执行脚本（从执行记录中提取代码模式）
- T4+：生成 SKILL_GROUNDING.md 溯源模板

### 步骤4：评测与迭代（⭐ 借鉴 skill-creator，Anthropic ★166K，2026-08-05 引入）

蒸馏出的技能**不能直接交付**，必须先过评测循环：

**4.1 触发测试**：写3-5个覆盖不同场景的测试prompts，检查技能的 description 能否正确触发：
- 正面测试：典型触发场景（应触发）
- 边界测试：模糊表述（应正确判断）
- 负面测试：无关任务（不应误触发）

**4.2 效果评测**：用测试prompts跑一遍技能流程，验证执行步骤可复现：
- 步骤是否可执行（不依赖蒸馏者隐性知识）
- 关键决策点是否覆盖主要分支
- 输出是否达到"可复现"标准（步骤不能复现=无用）

**4.3 description 优化**：根据测试结果调整 description：
- 触发不足 → 补充触发词和场景描述
- 误触发 → 收紧描述，明确边界（"不适用于..."）
- 参考 skill-creator 的"四问澄清法"：做什么/何时触发/输出格式/是否要测试

**4.4 迭代**：测试发现问题 → 修改 SKILL.md → 重新测试，直到全部通过。

**简化版**（轻量技能可跳过4.2）：至少执行4.1触发测试 + 4.3 description自查，确保技能能被正确触发。

## 蒸馏示例

### 输入：OpenAI API 调用经验

```
用户问：帮我总结一下用OpenAI API调用的最佳实践
执行记录：多次尝试 function calling、streaming、error handling 后的经验
```

### 输出：SKILL.md

```markdown
---
name: openai-api-best-practices
description: OpenAI API 调用最佳实践（function calling / streaming / error handling）
---

# OpenAI API 调用最佳实践

## 核心原理
- 解决：API 调用不稳定、超时、限流等问题
- 方法：三层降级 + 重试 + 流式响应

## 执行步骤
1. 设置重试机制（max_retries=3, exponential backoff）
2. 检测限流（429）-> 等待 Retry-After 秒
3. 检测超时 -> 缩短 prompt 重试
4. 流式输出时处理截断（拼接 chunk）
```

## 与 Resource2Skill distiller_prompt 的对齐

| 维度 | Resource2Skill | Skill Distiller |
|------|---------------|-----------------|
| 输入 | YouTube视频 + Gemini多模态 | 文本/文章 + LLM分析 |
| 输出格式 | 固定Markdown结构 | 固定YAML+Markdown |
| 可复现性 | 可执行代码（html/css/js） | 可执行步骤+工具调用 |
| 质量门控 | "代码不能复现=无用" | "步骤不能复现=无用" |
| 多模态 | 视频帧+代码+文字 | 文本+执行记录+脚本 |

## 参考

- Resource2Skill 论文: https://arxiv.org/abs/2606.29538
- distiller_prompt.md 原始设计: https://github.com/microsoft/Resource2Skill