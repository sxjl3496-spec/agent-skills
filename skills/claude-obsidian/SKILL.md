---
name: claude-obsidian
description: >
  自组织AI第二大脑：让Claude Code/Codex拥有Obsidian知识图谱持久记忆。
  支持任意资料导入，自动整理为结构化笔记。适用于需要跨会话记忆的Agent工作流。
triggers:
  - 用户要求"整理笔记"、"建立知识库"、"记忆管理"
  - 需要Agent持久化存储研究笔记
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [memory, knowledge-management, obsidian, claude-code]
    source: https://github.com/AgriciDaniel/claude-obsidian
    stars: 14661
---

# Claude Obsidian

自组织AI第二大脑：把任意资料扔进去，自动整理为Obsidian知识图谱。

## 安装

```bash
git clone https://github.com/AgriciDaniel/claude-obsidian.git
cd claude-obsidian
# 按README安装依赖
```

## 使用方式

1. 将资料（PDF、网页、笔记）放入指定目录
2. Claude Code自动识别并分类整理
3. 生成Obsidian兼容的Markdown笔记+双链

## 适用场景

- 研究笔记自动整理
- 文献阅读后自动归档
- 跨会话知识积累
