# Agent Skills 开源技能库

> **250+ 个即装即用的 AI Agent 技能（SKILL.md），支持 Claude Code / OpenCode / Hermes / Cursor 等任意支持技能规范的 Agent**
>
> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
> [![Skills](https://img.shields.io/badge/Skills-250%2B-blue)](CATALOG.md)
> [![Version](https://img.shields.io/badge/Version-V3.9-green)]()

一套覆盖**学术科研、软件开发、前端设计、生产力办公、媒体创作、金融研究、商业社交**等 17 大类的 Agent 技能集合。每个技能是一个标准化的 `SKILL.md`（YAML frontmatter + Markdown 正文），Agent 加载后即可获得该领域的专业工作流、命令模板与质量门控。

## ✨ 特性

- **🧩 即装即用**：复制技能目录即可装配，零依赖、零配置
- **📚 250+ 技能**：从论文写作到代码审查，从数据可视化到智能家居，覆盖主流 Agent 工作场景
- **✅ 质量门控**：每个技能内置验证/复核流程，减少 AI 输出"看起来对但实际错"
- **🌐 中英双语**：大量技能提供中文版本，适配中文学术与办公场景
- **📖 深度解读**：附 29 份技能解读文档 + 分类目录（CATALOG.md），快速定位所需能力

## 🚀 快速开始

### 装配方式

```bash
# Claude Code
cp -r skills/<技能名> ~/.claude/skills/

# OpenCode
cp -r skills/<技能名> ~/.config/opencode/skills/

# Hermes
# 复制到 hermes-data/skills/<分类>/

# 其他 Agent
# 按平台技能规范导入 skills/<名>/SKILL.md（frontmatter 含 name/description）
```

### 查看目录

- [📇 CATALOG.md](CATALOG.md) —— 250 项技能分类总目录（含逐项描述）
- [📂 skills/](skills/) —— 技能本体（每项一个目录）
- [📖 技能解读/](技能解读/) —— 29 份深度解读文档
- [📐 academic-standards/](academic-standards/) —— 学术方法论文档（引用规范 + 写作流程）

## 📊 技能分类总览

| 分类 | 数量 | 分类 | 数量 |
|------|------|------|------|
| 🎓 学术科研 | 31 | 🧩 Better-UI-Kit | 7 |
| ⚡ Superpowers 方法论 | 14 | 🌋 arkcli 工具族 | 24 |
| 🎨 反Slop设计品味 | 13 | 🔗 Letta 生态 | 2 |
| 💎 Impeccable 前端 | 1 | 🔧 开发工程 | 46 |
| 🖼️ 前端与设计 | 26 | 📝 Obsidian | 8 |
| 📦 生产力办公 | 22 | 💡 通用方法论 | 16 |
| 🎬 媒体创作 | 14 | 💼 商业与社交 | 10 |
| 🐙 GitHub 工作流 | 6 | 🤖 MLOps | 5 |
| 📈 金融与研究 | 5 | | |

**合计：250 项**（另有 11 项随主包分发的子技能）

## 📁 目录结构

```
agent-skills/
├── README.md                    # 本文件
├── CATALOG.md                   # 技能分类目录（250 项，逐项带描述）
├── LICENSE                      # MIT License
├── skills/                      # 250 项可迁移技能（SKILL.md 格式）
├── 技能解读/                    # 29 份技能深度解读文档
└── academic-standards/          # 学术方法论文档（引用规范+写作流程）
```

## 🤝 贡献指南

欢迎通过以下方式贡献：

1. **提交技能**：将技能目录放入 `skills/<分类>/`，确保包含完整 `SKILL.md`（frontmatter 含 `name` / `description`）
2. **改进现有技能**：修复描述、补充步骤、增加示例
3. **提交 Issue**：报告技能缺陷、提出新技能需求

> 说明：本仓库为**通用技能集合**，不含任何个人/商业敏感信息与平台专属技能（如特定 Agent 的内部配置）。个人工作流技能与平台绑定技能按开源合规要求保留在私有仓库。

## 📄 许可

[MIT License](LICENSE) © 2026 Hermes Agent Community
