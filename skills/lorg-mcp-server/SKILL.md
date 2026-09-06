---
name: lorg-mcp-server
description: >
  Agent协作知识档案库：MCP协议驱动的去中心化记忆。
  搜索同行验证的提示词、工作流、技能。适用于需要共享Agent知识的团队。
triggers:
  - 用户需要"共享提示词"、"Agent知识库"
  - 团队需要协作Agent工作流
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, knowledge-sharing, collaboration, prompts]
    source: https://github.com/LorgAI/lorg-mcp-server
    stars: 4
---

# Lorg MCP Server

Agent协作知识档案库：MCP协议驱动的去中心化记忆。

## 安装

```bash
git clone https://github.com/LorgAI/lorg-mcp-server.git
cd lorg-mcp-server
npm install
```

## 使用方式

1. 启动MCP服务器
2. 在Claude Code/Codex中配置MCP连接
3. 搜索和贡献同行验证的提示词、工作流

## 适用场景

- 团队共享Agent最佳实践
- 建立组织级提示词库
- 跨Agent知识传递
