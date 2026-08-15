---
title: GitHub AI Agent项目监控部署记录
tags: [AI监控, GitHub, MCP, Skills, 飞书推送]
created: 2026-08-05
---

# GitHub AI Agent 项目监控部署记录

## 背景（2026-08-05）

用户指示：hermes-arxiv-agent **不再抓取 arXiv 论文**，改为监控 **GitHub 上 AI Agent / AI 大模型相关的开源项目**（skills、MCP、工具、框架等）。

原 arXiv 论文监控 cron 已**暂停**（保留恢复能力），新增 GitHub 项目监控 cron。

## 监控方案

### 数据源：GitHub Search API
- 未认证限流 60次/小时，本脚本每次运行用4次搜索，完全够用
- 认证方式：无需 token（公开搜索 API）

### 4路搜索（合并去重）

| 路 | 查询 | 分类 |
|----|------|------|
| 1 | `AI agent created:>30d` | agent |
| 2 | `agent skills created:>30d` | skill |
| 3 | `MCP created:>30d` | mcp |
| 4 | `agent framework created:>30d` | framework |

**为什么用 `created:>30d` 而不是 stars 排序**：stars 排序永远返回同一批老项目（superpowers、langchain 等），无法发现新东西。按创建时间过滤才能发现近30天的新项目。

### 过滤规则
- 去重：seen_projects.json（脚本维护）+ projects_record.xlsx（历史记录）
- 最低星标：30（过滤水货）
- 每路取前10，合并去重后按 stars 降序，取前12

## 核心文件

| 文件 | 作用 |
|------|------|
| github_monitor.py | 主监控脚本（4路搜索+去重+输出JSON） |
| new_projects.json | 待 LLM 补全的项目列表（含 summary_cn/recommendation 空字段） |
| seen_projects.json | 已见过项目ID去重缓存 |
| projects_record.xlsx | 历史记录（LLM 回填中文介绍） |

## 每日工作流（cron 25f62b982e50，每天8点）

```
github_monitor.py 4路搜索近30天新项目
  → 去重+星标过滤 → 最多12个
  → 写 new_projects.json
  → LLM补全：中文介绍(summary_cn 60-120字) + 推荐度判断(recommendation)
  → 回填 projects_record.xlsx
  → 推送飞书Markdown日报
```

### 飞书日报格式
```
🤖 **AI Agent 开源项目日报** | YYYY-MM-DD
共发现 N 个新项目

⭐ 值得关注 | ★stars | 项目名
中文介绍
🔗 链接
[按推荐度排序：⭐ → 👍 → 👀]
```

### 推荐度标准
| 级别 | 条件 |
|------|------|
| ⭐ 值得关注 | stars≥1000，或技术独特 |
| 👍 可关注 | stars 500-1000，或有特色 |
| 👀 一般 | stars<500，或方向小众 |

## 实测验证（2026-08-05）

**dry-run 测试**：4路搜索收集到12个新项目，全部近30天创建：
- ★3049 [skill] jakubkrehel/skills（agent技能集合）
- ★1950 [mcp] AlephAITech/WorkBuddyGuide
- ★1887 [agent] QwenAudio/qwen-audio-agent（音频agent）
- ★1260 [mcp] icebird1998/drawio-scientific-illustrator（绘图MCP）
- ★1025 [framework] XYZ-AI-Lab/axrl（新框架）

**正式运行**：12个项目写入 new_projects.json + seen_projects.json（35个已记录），去重正常。

**API通道验证**：volcano Coding Plan（deepseek-v4-flash）可用；DashScope 文本API 403（与视觉一致，已知问题）。

## 与旧 arXiv 监控的对比

| 维度 | arXiv论文监控（已暂停） | GitHub项目监控（新） |
|------|----------------------|-------------------|
| 数据源 | export.arxiv.org | api.github.com |
| 内容 | 学术论文 | 开源项目（skills/MCP/框架/工具） |
| 补充信息 | 作者单位+中文摘要 | 中文介绍+推荐度 |
| 去重 | papers_record.xlsx | seen_projects.json + projects_record.xlsx |
| cron | 12ad7a78fa62（暂停） | 25f62b982e50（启用） |
| 状态字段 | journal_status/journal_name | category/recommendation |

## 后续操作

1. 用户想调整监控方向：改 github_monitor.py 中的 `queries` 列表（第4路搜索关键词）
2. 想恢复 arXiv 论文监控：cronjob resume 12ad7a78fa62
3. 调整每日推送量：改 MAX_PROJECTS（默认12）
4. 调整星标门槛：改 MIN_STARS（默认30）
