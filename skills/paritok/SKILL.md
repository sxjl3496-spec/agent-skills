---
name: paritok
description: >
  编码Agent专用压缩模型：无损压缩token 25%，省85%成本。
  4B参数量，专为代码任务优化。适用于高频调用LLM的编码场景。
triggers:
  - 用户需要"压缩token"、"降低LLM成本"
  - 编码Agent需要节省API费用
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [compression, token-optimization, cost-saving, coding]
    source: https://github.com/Paritok-official/paritok-4b-v1
    stars: 1449
---

# Paritok

编码Agent专用压缩模型：无损压缩token 25%，省85%成本。

## 安装

```bash
# 通过HuggingFace下载
huggingface-cli download Paritok-official/paritok-4b-v1

# 或用vLLM部署
vllm serve Paritok-official/paritok-4b-v1
```

## 使用方式

1. 部署Paritok作为中间层
2. 编码Agent的输入/输出经过Paritok压缩
3. 压缩后token数减少25%，成本降低85%

## 适用场景

- 高频调用GPT-4/Claude的编码项目
- 预算有限的AI编码团队
- 需要批量处理代码的场景
