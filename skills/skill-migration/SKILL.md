---
name: skill-migration
description: >
  从外部仓库（GitHub）导入/迁移 Agent 技能到 Hermes 技能库，并沉淀解读文档。
  适用场景：(1) 用户提供技能排行榜/技能列表截图要求"都装"或调研，(2) 用户要求从
  GitHub 克隆某个技能仓库安装，(3) 用户想了解某技能与 Hermes 现有技能的异同，
  (4) 用户要求建立技能解读文档体系方便学习和迁移。
  触发词："技能排行榜"、"装这个技能"、"迁移技能"、"从GitHub导入技能"、
  "这些技能看看哪几个是你没有的"、"技能详细解读"。
  与 skill-distiller 的区别：distiller 从教程/文档创建新技能；本技能导入现成技能仓库。
---

# 外部技能导入与迁移（GitHub → Hermes）

## 完整流程

```
[用户提供技能列表/排行榜/仓库名]
  ↓
1. 调研：克隆源仓库（git clone --depth 1）
  ↓
2. 定位：找到技能目录（各仓库结构不同，见下表）
  ↓
3. 对比：与 Hermes 现有技能对比（相同/不同/可借鉴）
  ↓
4. 安装：复制到 Hermes 技能库（带分类）
  ↓
5. 验证：frontmatter 检查 + hermes skills list 确认
  ↓
6. 沉淀：在技能库建立解读文档体系
```

## 步骤1：调研（克隆源仓库）

**不要用 GitHub API 搜索**（匿名限流 60 次/小时，批量调研必撞 403）。直接克隆：

```bash
mkdir skills_research && cd skills_research
git clone --depth 1 https://github.com/<org>/<repo>.git   # --depth 1 只拉最新，省时省流量
```

**仓库名冲突**：多个仓库都叫 skills → 克隆时指定目标目录：
```bash
git clone --depth 1 https://github.com/anthropics/skills.git
git clone --depth 1 https://github.com/openai/skills.git openai_skills
```

## 步骤2：定位技能目录（各仓库结构）

| 来源仓库 | 技能位置 | 示例 |
|---------|---------|------|
| anthropics/skills | `skills/skills/<name>/` | mcp-builder、frontend-design、skill-creator |
| openai/skills | `skills/.curated/<name>/` | figma-implement-design、figma-use |
| composio-community/awesome-codex-skills | 仓库根目录 `<name>/` | create-plan、gh-fix-ci、47个技能 |
| obra/superpowers | `skills/<name>/` | 14个子技能（本身是技能包） |
| VoltAgent/awesome-agent-skills | README 索引 | 指向各官方仓库链接 |

**技能包特殊处理**：Superpowers 是"方法论框架包"（14个子技能），整体复制为一个
新分类 `superpowers/`，每个子技能独立 SKILL.md 可独立触发。

## 步骤3：与现有技能对比

输出对比矩阵（用户明确要"了解相同/不同/可借鉴"）：
- 每个外部技能 vs Hermes 最近似的现有技能（用 skills_list 盘点）
- 维度：定位、流程、触发机制、输出格式
- 结论：✅完整引入 / 🔗补充现有 / 📚仅作索引

## 步骤4：安装（复制到技能库）

```bash
SKILLS_ROOT=<Hermes数据目录>/skills
# 单技能 → 按功能分类（development/、academic/ 等）
cp -r skills_research/skills/skills/mcp-builder "$SKILLS_ROOT/development/"
# 技能包 → 新建分类
mkdir -p "$SKILLS_ROOT/superpowers"
cp -r skills_research/superpowers/skills/* "$SKILLS_ROOT/superpowers/"
```

目录结构：`skills/<分类>/<技能名>/SKILL.md` + 可选 references/、scripts/、assets/

## 步骤5：验证

```bash
# frontmatter 完整性（Hermes 要求 name + description 必填）
for d in skills/development/mcp-builder; do
  head -5 "$d/SKILL.md" | grep -E "^(name|description):"
done
# Hermes 识别确认（应显示 enabled）
hermes skills list | grep <技能名>
```

**frontmatter 兼容性**：Claude/Codex 标准 SKILL.md 与 Hermes 完全兼容（name+description
必填，license/metadata 可选）。直接复制即可，无需转换。

## 步骤6：知识库沉淀（技能解读文档）

在 `技能开源仓库/技能解读/` 建立文档体系，方便学习和迁移：

| 文档 | 内容 |
|------|------|
| 总览.md | 目录导航 + 数据完整性声明 |
| 01~08-<技能名>解读.md | 每个技能一篇：来源/核心机制/工作流/与Hermes对比/可借鉴点 |
| 09-对比矩阵.md | 外部技能 vs Hermes 现有技能逐项对比 + 借鉴优先级 |
| 10-安装与迁移指南.md | 完整迁移流程 + 常见坑 |

每篇解读必须含：**数据完整性声明**（已获取/未获取/待补充/获取路径，见 obsidian-vault-archiving 技能）。

## 步骤7：开源仓库同步与维护审计

技能开源仓库（`<技能开源仓库路径>`）结构：
```
技能开源仓库/
├── README.md               # 项目简介+版本+技能清单+装配指南
├── CATALOG.md              # 技能分类目录（逐项带描述）
├── skills/                 # 可迁移技能本体（SKILL.md）
├── 技能解读/               # 解读文档
└── academic-standards/     # 学术方法论文档
```

**核心陷阱——"有解读、没本体"**：技能本体装进 Hermes 技能库（步骤4）≠ 同步进开源仓库 `skills/`。
常见问题：解读文档已入库，但对应技能本体缺失在 `skills/` 里——仓库"能看解读、不能装配"。

**维护审计 checklist（每次版本更新后必做）**：
```bash
# 1. 交叉比对：解读提到的技能名 vs skills/ 实际入库
cd "<技能开源仓库>"
grep -ohE '\[\[[A-Za-z][A-Za-z-]+' "技能解读/"*.md | sed 's/\[\[//' | sort -u
for s in superpowers taste-skill impeccable create-plan gh-fix-ci; do
  ls skills/ | grep -qi "$s" && echo "✓ $s 已入库" || echo "✗ $s 缺失"
done
# 2. 核对 Hermes 技能库有但开源仓库没有的技能（本地方有=未同步）
ls <Hermes数据目录>/skills/development/ | grep -iE "taste|impeccable"
ls <Hermes数据目录>/skills/superpowers/  # 14子技能
# 3. 敏感技能红线：涉及个人商业/职业背景的技能不纳入开源仓库
```

**审计时的坑**：
- README.md 是 CRLF+长行，read_file 会误判为 binary → 用 `cat` 或 `file README.md` 先确认
- 统计口径要分清：README 里的技能数量按分类清单统计，`ls skills | wc -l` 才是实际文件数，两者要核对
- 远端已配 origin 但从未 push → `git log origin/master` 报 fatal 是正常现象，说明本地未推送；push 前需用户确认

## 常见陷阱

1. **GitHub API 匿名限流**：批量调研用 `git clone --depth 1`，不要逐个 curl API。限流报错 `HTTP 403: rate limit exceeded`
2. **仓库名冲突**：多个官方仓库都叫 `skills`，克隆时指定 `openai_skills` 等目标目录
3. **--depth 1 限制**：看不到历史、分支；需要对比版本时用完整克隆
4. **依赖未配置**：部分技能依赖外部工具（figma-implement-design 需 Figma MCP server、gh-fix-ci 需 gh CLI 认证），安装时在解读文档标注清楚"⚠️ 实战需先配置 XX"
5. **分类选择**：技能库按分类组织，新技能放 development/ 或新建分类（如 superpowers）
6. **版本更新**：定期 `hermes skills check` 检查官方技能更新（本地复制不受 hub 更新管理，需手动 pull）
7. **目录名必须与 frontmatter name 一致（实测）**：Hermes 按 SKILL.md 里的 `name:` 注册技能，不看目录名。若目录名 ≠ 声明名（如目录 `expression-polish/` 内声明 `name: polish`），会导致按目录检索的工具困惑，甚至触发工具循环保护。**改名技能时必须同步重命名目录**：`mv skills/<旧目录名> skills/<新name>`。排查技能重名/加载异常时先做两步：(1) `find skills -name SKILL.md | xargs grep -l "name: X"` 找同名声明；(2) 对比目录名与声明名。注意多分类同技能名歧义（如 `development/skill-creator` 与 `development/deerflow-skills/skill-creator` 并存时，skill_view 会报 Ambiguous 需按分类路径加载）。

## 参考

- `references/top-skills-leaderboard.md` - 调研的8个顶级技能（来源/Star/结构/核心机制），含排行榜背景
- 关联技能：skill-distiller（从教程创建技能）、skill-creator（技能评测迭代循环）、obsidian-vault-archiving（知识库笔记规范）
