---
title: Hermes技能解析-development篇
tags: [Hermes技能, 技能解析, development]
created: 2026-08-05
---

# Hermes 技能解析（development 篇）

> 本篇解析 Hermes development 分类下的自有技能（外部引入的技能见 01-08 篇解读）。
> 安全等级：均为通用技术技能，不涉及个人信息，可开源分享。

## 1. skill-import（技能导入器）

- **触发**：排行榜/截图技能识别、从GitHub导入技能
- **核心**：从 GitHub 调研并导入现成 Agent 技能（Claude Code/Codex/Cursor 生态）到 Hermes 技能库
- **流程**：排行榜/截图技能识别 → GitHub 仓库定位与克隆 → SKILL.md 兼容性检查 → 安装落地
- **价值**：把"调研→导入→落地"流程固化为可复用技能

## 2. skill-migration（技能迁移器）

- **触发**：技能迁移、从外部仓库导入技能并沉淀文档
- **核心**：从外部仓库导入/迁移 Agent 技能到 Hermes 技能库，并沉淀解读文档
- **适用**：(1) 用户提供技能排行榜截图要求"都装"或调研，(2) 从外部仓库迁移技能
- **价值**：覆盖"导入+文档沉淀"完整闭环，比 skill-import 多文档环节

## 3. skill-distiller（技能蒸馏器）

- **触发**：蒸馏技能、提取技能、从文章中提取技能、distill skill
- **核心**：从教程文章/技术文档/执行记录中蒸馏出可复用 Agent 技能（SKILL.md）
- **借鉴**：Resource2Skill 的 distiller_prompt.md 设计模式
- **流程**：输入分析 → 结构化输出（固定模板）→ 关联文件生成 → **评测与迭代**（触发测试/效果评测/description优化，2026-08-05借鉴skill-creator）
- **铁律**：可复现性优先（"步骤不能复现=无用"）

## 4. desktop-pet-creation（桌宠制作全流程）

- **触发**：桌面宠物、桌宠、desktop pet、Hatch Pet、sprite atlas、DyberPet、Shimeji
- **核心**：AI生成角色图制作桌面宠物全流程——工具选型、精灵图集生成、DyberPet/Shimeji框架配置
- **特色**：适配OpenAI Hatch Pet技能到Hermes、照片转桌宠

## 5. ai-app-provider-config（AI应用provider配置）

- **触发**：配置XX的模型、AionUi配置provider、添加模型、接入火山方舟
- **核心**：配置桌面AI应用（AionUi等Electron应用）的LLM模型提供方，通过应用本地后端REST API添加provider
- **流程**：定位后端端口 → 探测REST路由 → 最小payload创建 → 逐模型验证

## 6. claude-code-custom-provider（Claude Code自定义provider）

- **触发**：Claude Code配置非Anthropic provider
- **核心**：Anthropic-to-OpenAI 代理模式、settings.json配置、模型名约定、故障排查

## 7. multi-agent-collaboration（多Agent协作路由）

- **触发**：问"XX能不能做"、Hermes能力不足时、对比Agent能力时
- **核心**：多Agent能力边界与协作路由——能力对照、场景路由决策、协作方式、调用其他CLI Agent的命令
- **覆盖**：OpenWorker/Claude Code/OpenCode/OpenClaw

## 8. windows-launcher（Windows启动器）

- **触发**：创建Windows桌面快捷方式/启动器
- **核心**：CLI工具的Windows快捷方式创建——WScript.Shell编码陷阱、PowerShell SxS错误、TERM变量继承、Defender误报处理

## 9. domain.yaml（领域路由配置）

- **说明**：development 分类下的配置文件，用于领域路由（非独立技能）
