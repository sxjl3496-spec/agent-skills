---
title: kepano Obsidian技能解读
tags: [AI技能, Obsidian, kepano, 知识管理]
created: 2026-08-05
source: https://github.com/kepano/obsidian-skills
---

# kepano/obsidian-skills 解读

## 基本信息

- **仓库**：[kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
- **Star**：★44,071
- **作者**：kepano（Obsidian CEO，Steph Ango）
- **定位**：教 agent 使用 Obsidian CLI 和开放协议——5个技能覆盖 Obsidian 的核心能力

## 设计哲学

Obsidian CEO 亲自编写，教 AI agent 如何与 Obsidian 交互。核心是 **Obsidian CLI**（官方命令行工具）+ **Obsidian 特有 Markdown 语法** + **Bases 数据库视图**。

## 5个技能详解

### 1. obsidian-cli（Obsidian CLI 交互）

- **触发**：用户要求与 Obsidian vault 交互、管理笔记、搜索vault内容、执行vault操作、开发调试Obsidian插件和主题
- **核心**：用 Obsidian CLI 读取、创建、搜索、管理笔记、任务、属性等
- **特色**：支持插件/主题开发——重载插件、运行JavaScript、捕获错误、截图、检查DOM

### 2. obsidian-markdown（Obsidian 特有Markdown）

- **触发**：在 Obsidian 中使用 .md 文件、用户提到 wikilinks/callouts/frontmatter/tags/embeds
- **核心**：创建和编辑 Obsidian Flavored Markdown——wikilinks、embeds、callouts、properties 等 Obsidian 特有语法

### 3. obsidian-bases（Obsidian Bases 数据库）

- **触发**：处理 .base 文件、创建笔记的数据库视图、用户提到 Bases/表格视图/卡片视图/过滤器/公式
- **核心**：创建和编辑 Obsidian Bases——视图、过滤器、公式、摘要的数据库功能

### 4. defuddle（网页内容净化）

- **核心**：把网页内容转换为干净的 Obsidian 笔记（提取正文、去除噪音）

### 5. json-canvas（JSON Canvas 格式）

- **核心**：Obsidian Canvas 的 JSON 格式支持——可视化笔记白板

## 与 Hermes 现有技能对比

| 维度 | obsidian-skills | Hermes现有 |
|------|----------------|-----------|
| 搜索 | obsidian-cli | vault-search（关键词搜索+双链追踪） |
| 归档 | obsidian-markdown | obsidian-vault-archiving（外部文档转笔记） |
| 数据库 | obsidian-bases | 无 |
| 网页净化 | defuddle | 无 |

**互补关系**：Hermes 的 vault-search 是轻量搜索，obsidian-cli 是完整 CLI 交互；obsidian-vault-archiving 侧重外部文档转结构化笔记，obsidian-markdown 侧重 Obsidian 特有语法的正确使用。

## 可借鉴的提升点

1. **Obsidian 特有语法规范**：wikilinks/callouts/properties 的正确用法——Hermes 写知识库笔记时可引用
2. **CLI 交互模式**：Obsidian CLI 的完整命令集（读/建/搜/管）比 Hermes 的 vault-search 更强大
3. **Bases 数据库视图**：Obsidian 的数据库能力（过滤器/公式/摘要）——Hermes 知识库可探索

## 收录状态

✅ 收录：obsidian-cli、obsidian-markdown、obsidian-bases
