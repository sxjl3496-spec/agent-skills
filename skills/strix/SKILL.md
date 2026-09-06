---
name: strix
description: >
  AI渗透测试工具：自动发现+修复应用漏洞，集成CI/CD。
  开源免费，支持Web/API/移动应用安全测试。适用于需要自动化安全审计的项目。
triggers:
  - 用户需要"安全测试"、"渗透测试"、"漏洞扫描"
  - 项目需要CI/CD集成安全检查
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, penetration-testing, vulnerability, ci-cd]
    source: https://github.com/usestrix/strix
    stars: 60767
---

# Strix

AI渗透测试工具：自动发现+修复应用漏洞，CI/CD集成。

## 安装

```bash
# Docker方式
docker pull usestrix/strix
docker run -it usestrix/strix

# 或pip安装
pip install strix-ai
```

## 使用方式

```bash
# 扫描Web应用
strix scan https://example.com

# 扫描API
strix scan --api https://api.example.com

# CI/CD集成
strix scan --format json --output results.json
```

## 适用场景

- 上线前安全审计
- CI/CD管道自动安全检查
- 定期漏洞扫描
