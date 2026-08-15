# Agent 技能开源仓库（本地维护版）

> 版本：V3.4（2026-08-16，全库脱敏整改，总计 257 项）
> 来源：Hermes 本地技能库 + 太尉（Claude Code）~/.claude/skills/（含 arkcli 工具族）+ OpenCode ~/.config/opencode/skills/ + Aion CLI
> 定位：本地技能仓库维护中（用户指示：先本地完善，后择机开源）——给任意支持 SKILL.md 的 Agent 直接装配
> 排除项：敏感技能（铁粉厂/家庭工厂/银行战略）+ 平台绑定技能（hermes/claude/aionui/openclaw专属）

## 目录

```
技能开源仓库/
├── README.md                    # 本文件
├── skills/                      # 257 项可迁移技能（SKILL.md 格式）
├── 技能解读/                    # 29 份技能深度解读文档
├── academic-standards/          # 学术方法论文档（引用规范+写作流程）
└── carbon-market-abm-toolkit/   # 碳市场 ABM 论文配套可运行代码
```

## 一、技能分类统计（257 项）

### 🎓 学术科研（32 项）
academic-figure, academic-paper-composer, academic-paper-review, academic-paper-reviewer, academic-paper-strategist, academic-paper-skills, academic-reference-verification, academic-rewriter, aigc-check, cnki-paper-download, deep-research, drawio-scientific-illustrator, drawio-scientific-figure, evidence-gate, gb7714-reference-format, github-deep-research, grant-application-strategist, hermes-arxiv-agent, journal-adapt, latex-document-skill, literature-review, obsidian-literature-matrix, office-academic-skill, paper2code, paper-to-patent, paperjury, reference-verification, research-paper-writing, research-paper-writing-advanced, research-writing-skill, scientific-toolkit-skill, systematic-literature-review, systematic-literature-review-method, no-ai-slop, no-ai-slop-zh, simple-english

### ⚡ Superpowers 全流程方法论（14 项）
brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills

### 🎨 Taste-Skill 反Slop设计品味（16 项）
brandkit, brutalist-skill, design-taste-frontend, gpt-taste, gpt-tasteskill, image-to-code-skill, imagegen-frontend-mobile, imagegen-frontend-web, minimalist-skill, output-skill, redesign-skill, soft-skill, stitch-skill, taste-skill, taste-skill-official, taste-skill-v1

### 💎 Impeccable 前端设计（2 项）
impeccable, impeccable-cli

### 🧩 Better-UI-Kit（7 项）
better-accessibility, better-colors, better-interface, better-layout, better-typography, better-ui, better-writing

### 🌋 火山方舟 arkcli 工具族（24 项）
arkcli-agent, arkcli-api-explorer, arkcli-auth, arkcli-billing, arkcli-chat, arkcli-code-example, arkcli-config, arkcli-connect, arkcli-custommodel, arkcli-deploy, arkcli-doctor, arkcli-gen, arkcli-helper, arkcli-infer-endpoint, arkcli-models, arkcli-onboard, arkcli-plans, arkcli-pricing, arkcli-profile, arkcli-resources, arkcli-shared, arkcli-train-finetune, arkcli-understand, arkcli-usage

### 🔗 Letta 生态技能（10 项）
creating-letta-code-channels, fleet-management, letta-api-client, letta-configuration, letta-filesystem-to-memfs, letta-skills-letta, memfs-search, navigating-chatgpt-history, self-configuration, setting-profile-images

### 🔧 开发工程（42 项）
api-and-interface-design, bootstrap, ci-cd-and-automation, ci-fix-loop, code-documentation, code-review-and-quality, code-simplification, context-engineering, cron, debugging-and-error-recovery, deprecation-and-migration, doc, documentation-and-adrs, doubt-driven-development, figma-implement-design, gh-fix-ci, git-workflow-and-versioning, github, incremental-implementation, mcp-builder, multi-agent-collaboration, performance-optimization, planning-and-task-breakdown, security-and-hardening, shipping-and-launch, skill-creator, skill-distiller, skill-import, skill-migration, source-driven-development, spec-driven-development, create-plan, desktop-pet-creation, docx-template-fill, windows-launcher, windows-npm-global-relocation, windows-tool-relocation, datadog, linear, morph-warpgrep, observability-and-instrumentation, sentry

### 🖼️ 前端与设计（27 项）
architecture-diagram, ascii-art, ascii-video, baoyu-infographic, claude-design, comfyui, design-md, excalidraw, frontend-design, frontend-skill, frontend-ui-engineering, humanizer, image-generation, manim-video, p5js, playwright, popular-web-designs, pretext, screenshot, sketch, songwriting-and-ai-music, touchdesigner-mcp, visual-identity, web-design-guidelines, chart-visualization, archify, hallmark

### 📊 DeerFlow 技能（8 项）
claude-to-deerflow, company-research, find-skills, multi-language, paper-research, ppt-generation, report-to-ppt, vercel-deploy-claimable

### 📝 Obsidian 技能（8 项）
defuddle, json-canvas, obsidian, obsidian-bases, obsidian-cli, obsidian-markdown, obsidian-skills-official, obsidian-vault-archiving

### 📦 生产力办公（18 项）
airtable, docx, google-workspace, jupyter-notebook, maps, nano-pdf, notion, ocr-and-documents, officecli, pdf, pdf-hybrid-reader, powerpoint, ppt-generation, spreadsheet, teams-meeting-pipeline, xlsx, gog, 1password

### 💡 通用方法论（10 项）
agent-development, consulting-analysis, conversations, idea-refine, interview-me, prompt-optimizer, surprise-me, using-agent-skills, verify, bootstrap

### 🎬 媒体创作（14 项）
blogwatcher, gif-search, music-generation, newsletter-generation, podcast-generation, remotion, slides, songsee, speech, transcribe, video-generation, youtube-content, ai-news, spotify-player

### 💼 商业与社交（10 项）
ai-seo, cold-email, official-form-filling, renovation-advisory, chinese-festival-greetings, chinese-personal-letters, discord, slack, social-cli, yelp-search

### 🐙 GitHub 工作流（6 项）
codebase-inspection, github-auth, github-code-review, github-issues, github-pr-workflow, github-repo-management

### 🤖 MLOps（5 项）
evaluating-llms-harness, huggingface-hub, llama-cpp, serving-llms-vllm, weights-and-biases

### 📈 金融与研究（5 项）
a-share-stock-analysis, grounded-citations, llm-wiki, polymarket, wind-terminal-data-extraction

### 💻 软件开发（5 项）
dogfood, hermes-agent-skill-authoring, inspecting-hermes-desktop-dom, node-inspect-debugger, plan

### 🏠 其他（9 项）
debug-helper, hermes-hatch-pet, literature-review, polish, project-context, prompt-templates, research-offline-playbook, vault-search, openhue

## 二、装配方式

```bash
# Claude Code
cp -r skills/<技能名> ~/.claude/skills/
# OpenCode
cp -r skills/<技能名> ~/.config/opencode/skills/
# Hermes：复制到 hermes-data/skills/<分类>/
# 其他 Agent：按平台技能规范导入 skills/<名>/SKILL.md（frontmatter 含 name/description）
```

## 三、排除项（未入库）

| 类型 | 技能 | 原因 |
|------|------|------|
| 敏感 | iron-powder-business（铁粉厂） | 个人商业信息 |
| 敏感 | family-factory-advisory（家庭工厂） | 个人商业信息 |
| 敏感 | bank-strategic-research-report（银行战略） | 涉个人职业背景 |
| 平台绑定 | hermes-agent, hermes-windows, aionui-team-leadership, openclaw-ops 等 30 项 | 仅限特定平台运行 |

## 四、维护记录

- V3.3（2026-08-15）：全库敏感信息脱敏（真实身份证号/姓名/本机路径→占位符），14技能修订，重建干净git历史
- V3.4（2026-08-16）：全库脱敏整改（学号/姓名/路径/称谓→占位）+补MIT LICENSE，总计 275→257 项
- V3.1（2026-08-07）：太尉技能盘点入库 47 项（arkcli 工具族 24 + Letta 生态 10 + 独立工具 13），总计 226→273 项；OpenCode/Aion CLI 复核无新增；御史大夫 2 项平台绑定不入库
- V3.0（2026-08-07）：技能本体全量入库，从 Hermes 本地技能库同步 138 项缺失技能，总计 88→226 项
- V2.3（2026-08-07）：合并技能详细解读与构造（29份解读）+ 88项技能仓库
- V2.1（2026-08-07）：OpenCode 技能入库 3 项，总计 87 项
- V2.0（2026-08-07）：全量入库 84 项 + 分类清单 + 排除项说明
- V1.0（2026-08-07）：5 项自研技能 + 学术方法论文档 + 碳市场工具箱
- 待办：后续择机推送 GitHub（<GITHUB_USER>/agent-skills）