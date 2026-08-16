---
title: 科研绘图MCP与Personal-Model解读
tags: [AI技能, MCP, 科研绘图, drawio, 记忆]
created: 2026-08-05
source: github
license: MIT
---

# drawio 科研绘图 与 personal-model 解读

> 来源：GitHub AI Agent 项目日报（2026-08-05）。

## 1. drawio-scientific-illustrator（科研绘图MCP，★1,260，MIT）

- **仓库**：https://github.com/icebird1998/drawio-scientific-illustrator
- **技能名**：recreate-scientific-figure-in-drawio
- **许可证**：MIT
- **安装位置**：`development/drawio-scientific-figure/`

### 是什么
通过 **MCP（Model Context Protocol）** 实时操控 **draw.io**（免费开源绘图软件）桌面版画布，让 AI 一步步重建/修改科研示意图。

### 核心能力
- 用视觉模型分析参考图（PNG/JPEG/SVG/PDF）
- 分解图为可编辑图元：画布/面板/容器/节点/文字/箭头/图例/配色/描边/字体/z-order
- 通过 draw.io 的 graph API 实时添加形状、连线、更新单元格
- 输出 .drawio/PNG/SVG/PDF/JPG 交付物

### MCP 工具集
| 工具 | 作用 |
|------|------|
| drawio_live_launch | 启动draw.io画布 |
| drawio_live_add_shape | 添加形状 |
| drawio_live_add_edge | 添加连线 |
| drawio_live_draw_sequence | 绘制序列 |
| drawio_live_fit | 自适应 |
| drawio_live_screenshot | 截图检查 |
| drawio_live_inspect | 检查元素 |
| drawio_live_save_snapshot | 保存快照 |
| drawio_validate | 验证 |
| drawio_export | 导出 |

### 硬边界（HARD BOUNDARY）
- 只通过 draw.io 内部 graph/model API 控制
- **禁止**操作系统级鼠标/键盘/窗口自动化
- **禁止**先构建XML再打开（必须实时绘制）
- 渲染截图仅用于检查画布本身

### 对用户的价值
写论文需要**机制图/流程图/框架图**（<某研究机制>、<某模型框架>）——AI 直接操作 draw.io 画布画出可编辑矢量图，比静态生成图更专业。

### 使用前提
- 安装 draw.io 桌面版（https://draw.io）
- 配置 MCP 插件（plugins/drawio-scientific-illustrator）

## 2. personal-model（AI记忆档案，★1,336，Apache-2.0）

- **仓库**：https://github.com/Intuition-Lab/personal-model
- **许可证**：Apache-2.0
- **收录状态**：仅作理念借鉴（见下方说明）

### 是什么
**Persome**（personal-model 的运行时）：一个本地优先的 macOS 守护进程，观察真实用户屏幕上下文，形成持久状态，构建**可审计的个人模型**，通过 MCP 提供给客户端。

### 核心概念（Point/Line/Face/Volume 几何模型）
- **Point**：单点观察
- **Line**：时间线上的会话
- **Face**：个人模型快照
- **Volume**：累积的个人数据
- **Root**：最多一个根模型

### 技术栈
- macOS 13+（实时捕获）
- Python 3.12-3.13（uv 管理）
- Markdown/SQLite/evomem 存储
- REST + MCP 服务

### ⚠️ 为什么未直接收录为技能
1. **依赖 macOS**（Persome 运行时是 macOS 守护进程），不适合 Windows 环境
2. 是**完整应用**（安装脚本+守护进程+模型快照），不是 SKILL.md
3. 与 Hermes 现有**记忆体系**（MEMORY.md/USER.md）功能重叠

### 借鉴价值（重点）
即使不安装，它的**设计理念**值得学习：
1. **可审计记忆**：记忆可以查看、修正、遗忘（Hermes 记忆是黑盒）
2. **分层模型**：Point→Line→Face→Volume 的渐进式记忆沉淀
3. **本地优先+隐私**：数据在本地，不依赖云
4. **HUMAN.md 概念**：把"关于人的档案"做成标准文件
