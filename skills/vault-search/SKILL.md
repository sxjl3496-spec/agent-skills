---
name: vault-search
description: >
  Obsidian 知识库检索技能。在 Obsidian Vault 中搜索笔记内容，
  支持关键词搜索和双链追踪。
  触发词：搜索知识库、查笔记、vault search、在obsidian里找。
---

# Vault 检索 (vault-search)

## 何时使用

- 用户提到之前记录过的信息
- 需要查找 Obsidian Vault 中的笔记
- 需要验证知识库中是否已有某主题的笔记

## Vault 位置

```
<Obsidian库>\\
├── 🤖 AI Agent/          # AI工具相关
│   ├── 01-Hermes/
│   ├── 02-Claude Code/
│   ├── ...
│   └── 09-Agent工程方法论/
├── 🏭 铁粉厂/            # 工厂经营
├── 🏠 万楼装修/           # 装修
├── 📜 古今明鉴/           # 历史
└── AI Agent 知识总汇.md
```

## 搜索方式

### 1. 关键词搜索

```python
from hermes_tools import search_files

# 搜索内容
result = search_files(
    pattern="关键词",
    target="content",
    path="<Obsidian库>",
    limit=20
)

# 搜索文件名
result = search_files(
    pattern="*关键词*",
    target="files",
    path="<Obsidian库>",
    limit=20
)
```

### 2. 读取笔记

```python
from hermes_tools import read_file

content = read_file(
    path="<Obsidian库>/🤖 AI Agent/09-Agent工程方法论/01-Prompt Engineering.md"
)
```

### 3. 双链追踪

在笔记中搜索 `[[笔记名]]` 标记，找到关联笔记：
```python
from hermes_tools import search_files

# 搜索双链
result = search_files(
    pattern=r"\[\[.*目标笔记名.*\]\]",
    target="content",
    path="<Obsidian库>"
)
```

## 搜索策略

1. **先搜文件名**：用 target="files" 按文件名搜索
2. **再搜内容**：用 target="content" 在文件内容中搜索
3. **读回上下文**：找到文件后用 read_file 读取完整内容
4. **追踪双链**：从搜索结果中的 [[]] 标记追踪关联笔记

## 注意事项

- Vault 路径含 emoji（🤖🏭🏠📜），在终端中需正确处理编码
- D盘路径在写入时需管理员权限，但读取不需要
- 搜索结果按修改时间排序（search_files 默认行为）
- 大文件（>100K字符）会被 read_file 拒绝，需用 offset+limit 分段读取
