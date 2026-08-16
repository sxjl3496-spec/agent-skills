---
title: mcp-builder解读
tags: [AI技能, MCP, 工具开发, Anthropic]
created: 2026-08-05
source: https://github.com/anthropics/skills/tree/main/skills/mcp-builder
---

# mcp-builder 解读

## 基本信息

- **来源**：Anthropic 官方技能仓库 `anthropics/skills`（★166K）
- **官方描述**：Guide for creating high-quality MCP (Model Context Protocol) servers
- **排行**：第3名（铜牌，"社区精选"标签）
- **定位**：一句话让 agent 生成一个 MCP server

## 核心机制

MCP server 开发完整指南。衡量一个 MCP server 质量的标准是：**它让 LLM 完成真实世界任务的能力有多强**。

## 四阶段工作流

### Phase 1: 深度调研与规划（Deep Research and Planning）

**1.1 理解现代 MCP 设计：**
- **API覆盖 vs 工作流工具**：平衡全面API端点覆盖与专用工作流工具。不确定时优先全面API覆盖
- **工具命名与可发现性**：清晰描述性名称，一致前缀（`github_create_issue`、`github_list_repos`），动作导向命名
- **上下文管理**：简洁工具描述、支持过滤/分页、返回聚焦数据
- **可操作错误消息**：错误消息应引导agent走向解决方案

**1.2 研究 MCP 协议文档：**
- sitemap: `https://modelcontextprotocol.io/sitemap.xml`
- 关键页面：规范概览与架构、传输机制（streamable HTTP、stdio）、工具/资源/prompt定义

**1.3 研究框架文档：**
- Python: FastMCP
- Node/TypeScript: MCP SDK

### Phase 2: 设计（后续阶段）
- 工具设计：名称、描述、参数
- 错误处理设计

### Phase 3: 实现（后续阶段）
- Python (FastMCP) 或 Node/TS (MCP SDK) 具体实现

### Phase 4: 测试与评估（后续阶段）
- 评估脚本：`scripts/evaluation.py`
- 连接测试：`scripts/connections.py`

## 附属资源

```
mcp-builder/
├── SKILL.md
├── reference/
│   ├── evaluation.md          # 评估方法
│   ├── mcp_best_practices.md  # MCP最佳实践
│   ├── node_mcp_server.md     # Node实现指南
│   └── python_mcp_server.md   # Python实现指南
└── scripts/
    ├── connections.py         # 连接测试
    ├── evaluation.py          # 评估脚本
    ├── example_evaluation.xml # 评估示例
    └── requirements.txt
```

## 与仓库现有技能对比

**本库无对应技能**。完全新增的 MCP 开发能力。
相关但不同：模型 provider 配置类技能是配置消费方，mcp-builder 是开发 MCP server 本身。

## 可借鉴的提升点

1. **工具命名规范**：动作导向+一致前缀（直接可用到任何工具开发）
2. **评估驱动开发**：evaluation.py 量化评估 MCP server 质量
3. **错误消息设计**："引导agent走向解决方案"的错误设计原则
4. **资源组织**：reference/ 与 scripts/ 分离的清晰结构
