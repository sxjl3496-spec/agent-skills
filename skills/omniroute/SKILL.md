---
name: omniroute
description: >
  免费开源AI网关：一个端点接入350+供应商（含150+免费），内置token压缩和自动故障回退。
  MIT协议。适用于需要多模型切换、成本优化的AI应用。
triggers:
  - 用户需要"多模型网关"、"AI代理"、"成本优化"
  - 需要统一接口调用多个LLM
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gateway, llm, multi-provider, cost-optimization]
    source: https://github.com/diegosouzapw/OmniRoute
    stars: 61660
---

# OmniRoute

免费开源AI网关：一个端点接入350+供应商，MIT协议。

## 安装

```bash
# Docker方式
docker pull omniroute/omniroute
docker run -p 8080:8080 omniroute/omniroute

# 或源码安装
git clone https://github.com/diegosouzapw/OmniRoute.git
cd OmniRoute && npm install && npm start
```

## 使用方式

1. 启动服务后，所有LLM调用统一走 `http://localhost:8080/v1/chat/completions`
2. 在配置中添加API key（支持OpenAI、Anthropic、Google等）
3. 自动故障回退：主模型不可用时自动切换备用

## 核心优势

- 350+供应商，150+免费模型
- 内置token压缩，节省成本
- MIT协议，可自托管
