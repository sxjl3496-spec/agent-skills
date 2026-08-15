---
title: DeerFlow 2.0深度解读
tags: [AI技能, DeerFlow, 深度研究, 字节跳动, Super Agent]
created: 2026-08-05
source: github
license: MIT
---

# DeerFlow 2.0 深度解读

> 来源：stophobia/deerflow2.0-enhanced（★651，字节跳动 DeerFlow 2.0 中文本地化版）
> 用户指定安装，MIT 许可证。

## 1. 是什么

**DeerFlow**（Deep Exploration and Efficient Research Flow）是**字节跳动开源**的 **super agent harness**（超级agent框架）。它把 **sub-agents（子agent）**、**memory（记忆）** 和 **sandbox（沙箱）** 组织在一起，配合可扩展的 **skills**，让 agent 完成几乎任何事情。

- 2026年2月28日 DeerFlow 2 发布后登上 **GitHub Trending 第1名**
- 2.0 是彻底重写（与 v1 无共用代码）
- 官网：https://deerflow.tech

## 2. 为什么对用户有价值

DeerFlow 自带 **21个公开技能**，其中科研相关的极有价值：

| 技能 | 用途 |
|------|------|
| **deep-research** | 系统化多角度网络调研（替代单次浅层搜索） |
| **paper-research** | 论文研究（文献阅读/分析） |
| **data-analysis** | 数据分析 |
| **company-research** | 公司调研 |
| **consulting-analysis** | 咨询分析 |
| **ppt-generation** | 自动生成PPT |
| **report-to-ppt** | 报告转PPT |
| **image-generation** | 图片生成 |
| **video-generation** | 视频生成 |
| **podcast-generation** | 播客生成 |
| **skill-creator** | 技能创建 |
| **github-deep-research** | GitHub深度研究 |
| **frontend-design** | 前端设计 |
| **web-design-guidelines** | 网页设计指南 |
| **chart-visualization** | 图表可视化 |
| **multi-language** | 多语言 |
| **find-skills** | 技能查找 |
| **bootstrap** | 初始化 |
| **claude-to-deerflow** | Claude Code 迁移到 DeerFlow |
| **surprise-me** | 随机创意 |
| **vercel-deploy-claimable** | Vercel部署 |

## 3. 核心特性

### 3.1 Skills 与 Tools
- 可扩展技能体系，支持社区技能安装
- 与 Claude Code 集成（claude-to-deerflow 技能）

### 3.2 Sub-Agents
- 子agent编排：复杂任务分解给多个子agent并行执行
- 与 Hermes 的 delegate_task 理念一致

### 3.3 Sandbox 与文件系统
- 隔离的执行环境，agent 可以安全地读写文件、运行代码

### 3.4 Context Engineering
- 上下文工程：管理长对话上下文，避免token浪费

## 4. 技术栈

| 组件 | 要求 |
|------|------|
| 后端 | Python 3.12+（backend/） |
| 前端 | Node.js 22+（frontend/） |
| 运行方式 | Docker（推荐）或本地开发 |
| 推荐模型 | Doubao-Seed-2.0-Code、DeepSeek v3.2、Kimi 2.5 |
| 配置 | config.example.yaml（环境变量注入API key） |

## 5. 部署状态（2026-08-05）

- **技能**：21个公开技能已全部安装到 Hermes `development/deerflow-skills/`（纯SKILL.md，可直接调用）
- **应用本体**：已部署到 `<deerflow目录>\`（21M，含backend/frontend/docs）
- **运行方式**：需要时用 Docker 或本地启动（`make dev` / docker compose）
- **注意**：应用本体未配置API key（config.example.yaml 是示例），运行时需注入

## 6. 与 Hermes 现有 deep-research 的关系

Hermes 已有 deep-research 技能（Imbad0202/academic-research-skills ★40.8K），DeerFlow 的 deep-research 是补充视角：

| 维度 | Hermes deep-research | DeerFlow deep-research |
|------|---------------------|----------------------|
| 来源 | Imbad0202（学术向） | 字节DeerFlow（工程向） |
| 侧重点 | 学术文献综述 | 多角度网络调研方法论 |
| 集成 | 已装 | 本次新装 |

两者互补：学术论文调研用 Hermes 版，通用课题调研用 DeerFlow 版。

## 7. 开源合规确认

- ✅ MIT 许可证（字节跳动官方开源）
- ✅ 21个技能全部可自由使用/修改/分发
- ✅ 无敏感信息
- ✅ README 多语言（英/中/日），适合开源分享
- ✅ 附带 SECURITY.md、CONTRIBUTING.md（开源项目规范范例）

## 8. 后续操作

1. **运行应用**：`cd <deerflow目录> && docker compose up`（需配置API key）
2. **技能调用**：直接对 Hermes 说"用 deep-research 调研XXX"或"生成PPT"（deerflow-skills 已装）
3. **科研应用**：paper-research 技能可用于文献调研，与 literature-review 搭配
