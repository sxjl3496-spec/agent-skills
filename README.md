# Agent Skills — Open Source Skill Library

> **250+ ready-to-use AI Agent skills (SKILL.md) for Claude Code / OpenCode / Hermes / Cursor and any Agent that supports the skill spec**
>
> [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
> [![Skills](https://img.shields.io/badge/Skills-250%2B-blue)](CATALOG.md)
> [![Version](https://img.shields.io/badge/Version-V3.11-green)]()
>
> **[中文版](README.zh-CN.md)** | English

A collection of **250+ Agent skills** across 17 categories — academic research, software development, frontend design, productivity, media creation, finance research, business & social. Each skill is a standardized `SKILL.md` (YAML frontmatter + Markdown body). Once loaded, your Agent gains professional workflows, command templates, and quality gates for that domain.

## ✨ Features

- **🧩 Plug & Play**: Copy a skill folder and it's ready — zero dependencies, zero config
- **📚 250+ Skills**: From paper writing to code review, data visualization to smart home, covering mainstream Agent workflows
- **✅ Quality Gates**: Each skill embeds verification/check flows to reduce AI "looks right but is wrong" outputs
- **🌐 Bilingual**: Many skills provide Chinese versions for Chinese academic & office scenarios
- **📖 Deep Reads**: 25 in-depth skill guides + a categorized catalog (CATALOG.md) for quick discovery

## 🚀 Quick Start

### Install

```bash
# Claude Code
cp -r skills/<skill-name> ~/.claude/skills/

# OpenCode
cp -r skills/<skill-name> ~/.config/opencode/skills/

# Hermes
# Copy to hermes-data/skills/<category>/

# Other Agents
# Import skills/<name>/SKILL.md per your platform's skill spec (frontmatter has name/description)
```

### Browse

- [📇 CATALOG.md](CATALOG.md) — Full categorized catalog of all 250 skills (with descriptions)
- [📂 skills/](skills/) — Skill bodies (one folder per skill)
- [📖 技能解读/](技能解读/) — 25 in-depth skill guides (Chinese)
- [📐 academic-standards/](academic-standards/) — Academic writing standards (citation rules + writing workflows)

## 📊 Category Overview

| Category | Count | Category | Count |
|----------|-------|----------|-------|
| 🎓 Academic & Research | 31 | 🧩 Better-UI-Kit | 7 |
| ⚡ Superpowers Methodology | 14 | 🌋 arkcli Tool Family | 24 |
| 🎨 Anti-Slop Design Taste | 13 | 🔗 Letta Ecosystem | 2 |
| 💎 Impeccable Frontend | 1 | 🔧 Development Engineering | 46 |
| 🖼️ Frontend & Design | 26 | 📝 Obsidian | 8 |
| 📦 Productivity & Office | 22 | 💡 General Methodology | 16 |
| 🎬 Media Creation | 14 | 💼 Business & Social | 10 |
| 🐙 GitHub Workflows | 6 | 🤖 MLOps | 5 |
| 📈 Finance & Research | 5 | | |

**Total: 250 skills** (+ 11 sub-skills shipped with parent packages)

## 📁 Repository Layout

```
agent-skills/
├── README.md                    # This file (English)
├── README.zh-CN.md              # Chinese version
├── CATALOG.md                   # Full skill catalog (250 items with descriptions)
├── LICENSE                      # MIT License
├── skills/                      # 250 migratable skills (SKILL.md format)
├── 技能解读/                    # 25 in-depth skill guides
└── academic-standards/          # Academic writing standards (citation rules + workflows)
```

## 🤝 Contributing

We welcome contributions in many ways:

1. **Submit a skill**: Put a skill folder under `skills/<category>/` with a complete `SKILL.md` (frontmatter includes `name` / `description`)
2. **Improve existing skills**: Fix descriptions, add steps, add examples
3. **Open an Issue**: Report skill bugs, request new skills

> Note: This repository is a **general-purpose skill collection** — it contains no personal/business-sensitive information and no platform-specific internals. Personal workflow skills and platform-bound skills are kept in private repositories per open-source compliance.

## 📄 License

[MIT License](LICENSE) © 2026 Hermes Agent Community