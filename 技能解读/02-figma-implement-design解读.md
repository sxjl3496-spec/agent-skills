---
title: figma-implement-design解读
tags: [AI技能, Figma, 设计转代码, OpenAI]
created: 2026-08-05
source: https://github.com/openai/skills/tree/main/skills/.curated/figma-implement-design
---

# figma-implement-design 解读

## 基本信息

- **来源**：OpenAI 官方技能仓库 `openai/skills`（.curated 目录）
- **官方描述**：Translates Figma designs into production-ready application code with 1:1 visual fidelity
- **排行**：第2名（银牌，"官方 curated"标签）
- **定位**：Figma 设计稿 → 生产级代码，1:1 视觉保真

## 核心机制

通过 **Figma MCP server** 获取设计上下文，将设计 token、布局、资源映射到项目现有组件库和约定，实现像素级还原。

### 技能边界（Skill Boundaries）

| 用户需求 | 用哪个技能 |
|---------|-----------|
| 交付物是仓库里的代码 | **figma-implement-design** |
| 在Figma内创建/编辑/删除节点 | figma-use |
| 从代码/描述构建整页Figma | figma-generate-design |
| 只要 Code Connect 映射 | figma-code-connect-components |
| 写可复用的agent规则(CLAUDE.md/AGENTS.md) | figma-create-design-system-rules |

## 必备工作流（Required Workflow）

### Step 1: 获取 Node ID
- **URL解析**：`https://figma.com/design/:fileKey/:fileName?node-id=1-2` → 提取 fileKey 和 node-id
- **桌面MCP**：figma-desktop MCP 自动使用当前打开文件的选择节点（无需URL）

### Step 2: 获取设计上下文
- 调用 `get_design_context(fileKey, nodeId)` 获取结构化数据：
  - 布局属性（Auto Layout、约束、尺寸）
  - 排版规格
  - 颜色值和设计token
  - 组件结构和变体
  - 间距和padding值
- **响应过大/截断**：先用 `get_metadata` 获取高层节点映射 → 定位子节点 → 单独获取

### Step 3: Token 映射与代码生成
- 将设计 token 映射到项目现有组件库和约定
- 从 Figma 框架下载 SVG 资源并接线（无需引入 icon 包）

### Step 4: 视觉一致性检查清单
- 完成后对照 Figma 截图审计实现，捕捉间距或颜色漂移

## 适用场景（When to use it）

1. 将 Figma 组件 URL 转为带匹配 token 的 React 组件
2. 从 Figma 文件重建仪表盘布局（无需手动计算间距）
3. 用 Figma 定义的新变体扩展现有按钮组件
4. 下载并接线 Figma 框架的 SVG 资源
5. 对照 Figma 截图审计已实现 UI 捕捉漂移

## 依赖

- **Figma MCP server**（远程或 figma-desktop 本地）必须连接可用
- 用户提供 Figma URL（`figma.com/design/:fileKey/:fileName?node-id=x-x`）
- 项目已有设计系统或组件库（首选）

## 与 Hermes 现有技能对比

**Hermes 无对应技能**。这是完全新增的能力，属于"设计转代码"垂直领域。

## 可借鉴的提升点

1. **结构化工作流**：获取设计上下文 → token映射 → 生成 → 审计的强制顺序
2. **技能边界矩阵**：用表格清晰划分5个相邻技能的适用场景，避免触发混乱
3. **截断处理策略**：大响应时用 metadata → 子节点逐级获取的分层方法

## 安装状态

✅ 已安装到 Hermes 技能库 `development\figma-implement-design\`
⚠️ 注意：实战需要先配置 Figma MCP server（Hermes 尚未配置），未配置前技能作为方法论参考
