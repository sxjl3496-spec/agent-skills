---
title: Hermes技能解析-hermes篇
tags: [Hermes技能, 技能解析, hermes配置]
created: 2026-08-05
---

# Hermes 技能解析（hermes 篇）

> 本篇解析 Hermes 自身的配置与管理技能。安全等级：通用配置技能，不涉及个人信息（API Key 均以环境变量引用，不硬编码）。

## 1. hermes-provider-config（模型provider配置）

- **触发**：增加一个提供商、添加provider、接入XX模型、新增API、配置XX的API Key
- **核心**：向 Hermes config.yaml 添加新的文本模型 provider
- **覆盖**：provider注册、降级链插入、API Key环境变量设置、连通性测试
- **经验**：OpenCode Go、MiniMax 等接入案例

## 2. hermes-multimodal-setup（五感觉醒配置）

- **触发**：配置视觉、语音识别(STT)、语音合成(TTS)、图片生成(image_gen)等多模态能力
- **核心**：Hermes五感觉醒配置指南——火山方舟/DashScope/Windows SAPI/faster-whisper等服务配置
- **覆盖**：视觉（vision_analyze）、STT、TTS、图片生成的模型路由和已知限制

## 3. hermes-vision-config（视觉模型配置）

- **触发**：设置/切换/调试视觉模型、vision_analyze失败排查
- **核心**：Hermes视觉（辅助）模型配置与故障排查——provider选择、API key管理、配额问题、图片传递失败的workaround

## 4. hermes-messaging-setup（消息平台配置）

- **触发**：配置消息平台（Telegram、Discord、飞书、钉钉等）
- **核心**：Hermes gateway 消息平台配置——查找hermes CLI、运行gateway setup、配置凭据、连接问题排查

## 5. hermes-windows（Windows环境适配）

- **触发**：Hermes在Windows上运行的问题
- **核心**：Windows运行适配——launcher设置、Git Bash路径怪癖、gateway Scheduled Task配置、prompt_toolkit console修复、Clash Verge代理诊断

## 6. complex-task-router（复杂任务路由）

- **触发**：复杂、困难、深度分析、系统设计、架构、综合方案、帮我梳理
- **核心**：复杂困难任务的模型路由/升级机制——5步以上推理链、3+文件交叉分析、系统设计、跨域综合时切换到更强思维模式

## 7. multi-agent-delegation（主Agent委派）

- **触发**：所有任务接收时自动加载
- **核心**：多Agent委派——Hermes 评估能力边界，能做的自己做，做不到的委派给助手（OpenWorker/Claude Code/OpenCode/OpenClaw）
- **流程**：自包含上下文委派 → 返回后验证质量 → 发现短板主动升级

## 8. aionui-team-leadership（AionUi队长工作流）

- **触发**：AionUi Team模式下分配任务、计划需队友评审、队友启动失败
- **核心**：AionUi Team模式下的队长工作流——任务分配、计划串行评审、队员失败接管、Team CLI命令用法
- **互补**：与multi-agent-delegation互补（后者是CLI直接调用，本技能是Team模式）
