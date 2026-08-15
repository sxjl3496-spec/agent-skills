# Agent 技能开源仓库（本地维护版）

> 版本：V3.7（2026-08-16，分类开源处理：CATALOG 生成 + 257 项逐项核验唯一归类）
> 来源：Hermes 本地技能库 + 太尉（Claude Code）技能目录（含 arkcli 工具族）+ OpenCode 技能目录 + Aion CLI
> 定位：本地技能仓库维护中（用户指示：先本地完善，后择机开源）——给任意支持 SKILL.md 的 Agent 直接装配
> 排除项：敏感技能（铁粉厂/家庭工厂/银行战略）+ 平台绑定技能（hermes/claude/aionui/openclaw专属）

## 目录

```
技能开源仓库/
├── README.md                    # 本文件
├── CATALOG.md                   # 技能分类目录（257 项，逐项带描述，自动核验）
├── skills/                      # 257 项可迁移技能（SKILL.md 格式）
├── 技能解读/                    # 29 份技能深度解读文档
├── academic-standards/          # 学术方法论文档（引用规范+写作流程）
└── carbon-market-abm-toolkit/   # 碳市场 ABM 论文配套可运行代码
```

## 一、技能分类统计（257 项，逐项核验）

> 本清单由脚本对照 `skills/*/SKILL.md` 逐项生成，每项唯一归类；含描述版本见 [CATALOG.md](CATALOG.md)。
> 修订说明：V3.7 起移除清单中不存在的技能名（如 academic-paper-skills、cnki-paper-download、taste-skill-official 等占位/幽灵条目），并消除重复归类（bootstrap/github 等只入一类）。

### 🎓 学术科研（35 项）
academic-figure, academic-paper-composer, academic-paper-composer-zh, academic-paper-review, academic-paper-reviewer, academic-paper-strategist, academic-paper-strategist-zh, academic-reference-verification, academic-rewriter, aigc-check, arxiv, deep-research, drawio-scientific-figure, evidence-gate, gb7714-reference-format, github-deep-research, grant-application-strategist, hermes-arxiv-agent, journal-adapt, latex-document-skill, literature-review, no-ai-slop, no-ai-slop-zh, office-academic-skill, paper-research, paper-to-patent, paper2code, paperjury, reference-verification, research-paper-writing, research-writing-skill, scientific-toolkit-skill, simple-english, systematic-literature-review, systematic-literature-review-method

### ⚡ Superpowers 全流程方法论（14 项）
brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills

### 🎨 Taste-Skill 反Slop设计品味（13 项）
brandkit, brutalist-skill, design-taste-frontend, gpt-taste, hallmark, image-to-code-skill, imagegen-frontend-mobile, imagegen-frontend-web, minimalist-skill, redesign-skill, soft-skill, stitch-skill, taste-skill-v1

### 💎 Impeccable 前端设计（1 项）
impeccable

### 🧩 Better-UI-Kit（7 项）
better-accessibility, better-colors, better-interface, better-layout, better-typography, better-ui, better-writing

### 🌋 火山方舟 arkcli 工具族（24 项）
arkcli-agent, arkcli-api-explorer, arkcli-auth, arkcli-billing, arkcli-chat, arkcli-code-example, arkcli-config, arkcli-connect, arkcli-custommodel, arkcli-deploy, arkcli-doctor, arkcli-gen, arkcli-helper, arkcli-infer-endpoint, arkcli-models, arkcli-onboard, arkcli-plans, arkcli-pricing, arkcli-profile, arkcli-resources, arkcli-shared, arkcli-train-finetune, arkcli-understand, arkcli-usage

### 🔗 Letta 生态技能（2 项）
letta-skills-letta, memfs-search
（注：creating-letta-code-channels / fleet-management / letta-api-client 等 11 项为 letta-skills-letta 的子技能，随主包分发）

### 🔧 开发工程（47 项）
api-and-interface-design, browser-testing-with-devtools, ci-cd-and-automation, ci-fix-loop, code-documentation, code-review-and-quality, code-simplification, codebase-inspection, context-engineering, create-plan, cron, datadog, debug-helper, debugging-and-error-recovery, deprecation-and-migration, desktop-pet-creation, doc, documentation-and-adrs, dogfood, doubt-driven-development, gh-fix-ci, git-workflow-and-versioning, incremental-implementation, linear, mcp-builder, morph-warpgrep, multi-agent-collaboration, observability-and-instrumentation, performance-optimization, plan, planning-and-task-breakdown, project-context, security-and-hardening, sentry, shipping-and-launch, simplify-code, skill-creator, skill-distiller, skill-import, skill-migration, source-driven-development, spec-driven-development, spike, vercel-deploy-claimable, windows-launcher, windows-npm-global-relocation, windows-tool-relocation

### 🖼️ 前端与设计（26 项）
archify, architecture-diagram, ascii-art, ascii-video, baoyu-infographic, chart-visualization, claude-design, comfyui, design-md, excalidraw, figma, figma-implement-design, frontend-design, frontend-skill, frontend-ui-engineering, image-generation, manim-video, p5js, playwright, popular-web-designs, pretext, screenshot, sketch, touchdesigner-mcp, visual-identity, web-design-guidelines

### 📝 Obsidian 技能（8 项）
defuddle, json-canvas, obsidian, obsidian-bases, obsidian-cli, obsidian-markdown, obsidian-vault-archiving, vault-search

### 📦 生产力办公（24 项）
1password, airtable, data-analysis, docx, docx-template-fill, gog, google-workspace, jupyter-notebook, maps, nano-pdf, notion, ocr-and-documents, officecli, official-form-filling, openhue, pdf, pdf-hybrid-reader, powerpoint, ppt-generation, report-to-ppt, slides, spreadsheet, teams-meeting-pipeline, xlsx

### 💡 通用方法论（16 项）
bootstrap, claude-to-deerflow, consulting-analysis, find-skills, humanizer, idea-refine, interview-me, multi-language, output-skill, polish, prompt-optimizer, prompt-templates, research-offline-playbook, surprise-me, using-agent-skills, verify

### 🎬 媒体创作（14 项）
ai-news, blogwatcher, gif-search, music-generation, newsletter-generation, podcast-generation, remotion, songsee, songwriting-and-ai-music, speech, spotify-player, transcribe, video-generation, youtube-content

### 💼 商业与社交（10 项）
ai-seo, chinese-festival-greetings, chinese-personal-letters, cold-email, company-research, discord, renovation-advisory, slack, social-cli, yelp-search

### 🐙 GitHub 工作流（6 项）
github, github-auth, github-code-review, github-issues, github-pr-workflow, github-repo-management

### 🤖 MLOps（5 项）
evaluating-llms-harness, huggingface-hub, llama-cpp, serving-llms-vllm, weights-and-biases

### 📈 金融与研究（5 项）
a-share-stock-analysis, grounded-citations, llm-wiki, polymarket, wind-terminal-data-extraction

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

- V3.7（2026-08-16）：分类开源处理——生成 CATALOG.md（257 项含描述），对照 `skills/` 目录逐项核验唯一归类；README 分类清单校正（移除 academic-paper-skills / cnki-paper-download / taste-skill-official / hermes-hatch-pet 等幽灵条目，消除 bootstrap/github 重复归类，合并 DeerFlow/软件开发/其他 三个失真分类），版本号与 git 历史同步
- V3.6（2026-08-16）：太尉语境型身份信息清理（院校/人名/申报细节→占位，14 文件）+ README 本机路径清理；收紧半身份证区域码脱敏示例（430302→占位）
- V3.5（2026-08-16）：移除内部诊断文档，重建干净 git 历史（健康复检后整改）
- V3.4（2026-08-16）：全库脱敏整改（学号/姓名/路径/称谓→占位）+ 补 MIT LICENSE，总计 275→257 项
- V3.3（2026-08-15）：全库敏感信息脱敏（真实身份证号/姓名/本机路径→占位符），14 技能修订
- V3.1（2026-08-07）：太尉技能盘点入库 47 项（arkcli 工具族 24 + Letta 生态 10 + 独立工具 13），总计 226→273 项；OpenCode/Aion CLI 复核无新增；御史大夫 2 项平台绑定不入库
- V3.0（2026-08-07）：技能本体全量入库，从 Hermes 本地技能库同步 138 项缺失技能，总计 88→226 项
- V2.3（2026-08-07）：合并技能详细解读与构造（29 份解读）+ 88 项技能仓库
- V2.1（2026-08-07）：OpenCode 技能入库 3 项，总计 87 项
- V2.0（2026-08-07）：全量入库 84 项 + 分类清单 + 排除项说明
- V1.0（2026-08-07）：5 项自研技能 + 学术方法论文档 + 碳市场工具箱
- 待办：后续择机推送 GitHub（<GITHUB_USER>/agent-skills）