---
title: Hermes核心技能解析-根目录篇
tags: [Hermes技能, 技能解析, 核心技能]
created: 2026-08-05
---

# Hermes 核心技能解析（根目录篇）

> 本篇解析 Hermes 技能库根目录下的核心技能，涵盖基础工作流能力。

## 1. plan（任务规划器）

- **触发**：`/plan 你的任务` 或 `/plan auto 你的任务`
- **核心**：全流程任务规划——表达优化（调polish）→ 复杂度评估 → 模型路由 → 执行计划 → 等待确认 → 逐步执行 → 两层验证 → 检验报告
- **特色**：模型路由矩阵（L/M/H/H+四级）、三层降级链（Coding Plan→免费千问→按量付费）、并行执行、中断处理、跨会话恢复
- **出口**：任务完成检验（cross_model_verify跨模型验证 + delegate_task隔离验证 + 硬验证）
- **借鉴来源**：已融入 Superpowers HARD-GATE、create-plan Scope模板（2026-08-05）
- **文档**：`<Hermes技能目录>\plan\SKILL.md`（971行，含19个陷阱+模型路由矩阵）

## 2. polish（表达优化器）

- **触发**：`/polish`、`\polish：`、`\优化：`、`\youhua：` 开头
- **核心**：将用户表达优化为逻辑清晰的版本，等待确认后再执行
- **与no-ai-slop分工**：polish做加法（提升表达），no-ai-slop做减法（去AI痕迹）

## 3. verify（通用验证器）

- **触发**：验证、verify、检查质量、审查、validate、质检
- **核心**：三层验证——硬验证（运行/读取/测试）→ 跨模型验证（cross_model_verify，qwen3.7-flash）→ 验证报告
- **铁律**：证据先行（Evidence Before Claims）——声称完成前必须本回合内运行验证命令并确认输出（2026-08-05借鉴Superpowers）
- **前端反模式检测**：集成 Impeccable CLI（`npx impeccable detect`，2026-08-05），前端交付物零token客观检测25+反模式

## 4. debug-helper（调试助手）

- **触发**：调试、debug、排查、为什么报错、报错了、出错
- **核心**：错误分类表（API 401/403/429/超时、ModuleNotFound、SSL等）→ API诊断流程 → 网络诊断 → Hermes特有诊断 → Python代码调试
- **铁律**：无根因不修复（Root Cause First）——Phase 1根因调查（复现→证据→缩小范围→确认根因）完成前禁止修复（2026-08-05借鉴Superpowers）

## 5. no-ai-slop（去AI痕迹）

- **触发**：`/no-ai-slop` 斜杠命令
- **核心**：从写作中移除AI生成痕迹，保留作者个人声音和学术表达规范
- **模式**：编辑模式（默认，去AI化重写）+ 检测模式（仅标记）
- **特色**：内置学术写作白名单，避免误删标准学术术语；与polish串联使用

## 6. literature-review（文献综述）

- **触发**：文献综述、literature review、帮我搜集文献、综述写作
- **核心**：端到端文献综述——文献搜集（OpenAlex/arXiv/Crossref/Semantic Scholar多源聚合）→ 筛选去重 → 综述撰写（主题/时间/方法论维度）→ 格式化输出（GB/T 7714-2015 + APA 7th）
- **特色**：支持导入CNKI导出文件（.ris/.enw/.nbib）、生成PRISMA检索流程报告

## 7. pdf-hybrid-reader（PDF混合读取）

- **触发**：读取/分析/总结PDF文件、PDF书籍、课程资料
- **核心**：混合策略——文字页直接提取文本，含图片页渲染为PNG后调用视觉模型识别
- **价值**：解决PDF图片页（图表/扫描页）无法提取文本的问题

## 8. research-offline-playbook（离线调研）

- **触发**：网络不可达时的调研任务（行业分析、政策研究、文献综述）
- **核心**：系统化降级到本地资源——文件系统搜索、PDF/CAJ文档提取、session历史检索、专家知识合成
- **场景**：判断可能涉及在线搜索但环境无网络时立即启动

## 9. vault-search（知识库检索）

- **触发**：搜索知识库、查笔记、vault search、在obsidian里找
- **核心**：Obsidian Vault关键词搜索 + 双链追踪

## 10. prompt-templates（Prompt模板库）

- **触发**：prompt模板、template、参考模板、用模板
- **核心**：通用prompt模板库——调研、代码审查、文档写作、数据分析、方案评估、翻译润色

## 11. project-context（项目上下文）

- **触发**：项目状态、保存进度、恢复任务、project state、跨会话
- **核心**：在当前工作目录维护 `.hermes/project-state.md`，记录任务/进度/决策/待办，支持跨会话状态恢复

## 12. hermes-hatch-pet（桌宠精灵图集生成）

- **触发**：桌面宠物、桌宠、精灵图集、sprite atlas
- **核心**：从文本提示/参考照片/图片编辑生成动画宠物精灵图集，3种生成模式（t2i/edit/ref）+ 照片转宠物工作流 + DyberPet格式转换
- **特色**：纯Python/Pillow管道，确定性步骤无外部AI依赖
