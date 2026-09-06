---
name: officecli
description: >
  AI Agent专用Office套件：一键操控Word/Excel/PPT，单文件零依赖。
  支持读取、创建、编辑、转换Office文档。适用于Agent自动化办公场景。
triggers:
  - 用户需要"操作Word"、"读取Excel"、"生成PPT"
  - Agent需要自动化处理Office文档
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [office, word, excel, ppt, document-automation]
    source: https://github.com/iOfficeAI/OfficeCLI
    stars: 30058
---

# OfficeCLI

AI Agent专用Office套件：单文件零依赖操控Word/Excel/PPT。

## 安装

```bash
# npm安装
npm install -g officecli

# 或直接下载二进制
# https://github.com/iOfficeAI/OfficeCLI/releases
```

## 使用方式

```bash
# 读取Word文档
officecli read document.docx

# 创建Excel
officecli create spreadsheet.xlsx --data "Name,Age\nAlice,30"

# 转换格式
officecli convert input.docx output.pdf
```

## 适用场景

- Agent自动填充合同模板
- 批量处理Excel数据
- 自动生成PPT报告
