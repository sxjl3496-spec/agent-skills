# Hermes Agent 升级影响评估

评估 Hermes Agent 版本升级的安全性和影响。适用于任何 v0.16.0+ 的升级决策。

## 评估方法论

### 1. 依赖兼容性检查

对比当前安装版本和目标版本的 `pyproject.toml` 中的 `dependencies` 段。

```bash
# 当前安装版本和依赖
pip show hermes-agent | grep -E "^(Version|Requires):"
pip list | grep -iE "openai|pydantic|httpx|pyyaml|requests|jinja|dotenv|tenacity|fire|fastapi|uvicorn|croniter"

# 目标版本的依赖（从 GitHub 获取 pyproject.toml）
curl -s "https://api.github.com/repos/NousResearch/hermes-agent/contents/pyproject.toml?ref=v2026.7.20" | python -c "
import sys, json, base64
d = json.load(sys.stdin)
content = base64.b64decode(d['content']).decode('utf-8')
in_deps = False
for line in content.split('\n'):
    if 'dependencies' in line: in_deps = True; continue
    if in_deps:
        if line.startswith(']'): break
        line = line.strip()
        if any(k in line.lower() for k in ['openai','httpx','pydantic','pyyaml','rich','requests','jinja','dotenv','tenacity','fire']):
            print(f'  {line}')
"
```

**判断标准**：如果所有核心依赖（openai, pydantic, httpx, pyyaml）版本完全一致，升级不会破坏 Python 环境。

### 2. config.yaml 迁移影响

对比当前 `_config_version` 和目标版本的 `_config_version`。

```bash
# 当前版本
grep "_config_version" "D:/BaiduSyncdisk/AIKnowledgeBase/Hermesagent/.venv/Lib/site-packages/hermes_cli/config.py" | head -1

# 目标版本（从 GitHub 获取）
curl -s "https://api.github.com/repos/NousResearch/hermes-agent/contents/hermes_cli/config.py?ref=v2026.7.20" | python -c "
import sys, json, base64
d = json.load(sys.stdin)
content = base64.b64decode(d['content']).decode('utf-8')
for line in content.split('\n'):
    if '_config_version' in line.lower() and 'CONFIG_VERSION' in line:
        print(line)
"
```

然后检查每个版本的迁移逻辑（搜索 `current_ver < N` 的条件块）。

**判断标准**：迁移步骤只增不减已有字段、不删除用户配置。v27->v33 的迁移都是安全的（加字段、改名、改默认值）。

### 3. 技能兼容性

SKILL.md 格式（YAML frontmatter + markdown body）在 v0.16.0->v0.19.0 间未变。所有技能向后兼容。

### 4. GitHub Issue/PR 状态检查

搜索 Hermes GitHub 仓库中与待修复 bug 相关的 issue 和 PR：

```bash
# 搜索相关 issue
curl -s "https://api.github.com/search/issues?q=repo:NousResearch/hermes-agent+credential+pool+delegate+subagent&per_page=5&sort=updated" | python -c "
import sys, json
d = json.load(sys.stdin)
for item in d.get('items', [])[:5]:
    print(f'  #{item[\"number\"]}: {item[\"title\"][:100]}')
    print(f'    State: {item[\"state\"]}, Updated: {item[\"updated_at\"][:10]}')
"
```

### 5. 回退方案

```bash
# 回退到旧版本
pip install hermes-agent==0.16.0
```

## v0.16.0 -> v0.19.0 评估结果（2026.7.31）

### 依赖兼容性

所有核心依赖版本完全一致（openai==2.24.0, pydantic==2.13.4, httpx==0.28.1 等）。升级不会破坏 Python 环境。

### config.yaml 迁移（v27 -> v33）

| 版本 | 迁移内容 | 影响当前配置？ |
|------|---------|---------------|
| v27->v28 | (未文档化) | 否 |
| v28->v29 | memory/skills write_mode -> write_approval | 否（未设 write_mode） |
| v29->v30 | verify_on_stop 新增 | 否（新字段） |
| v30->v31 | verify_on_stop 非明确设为 false | 否（未设此字段） |
| v31->v32 | 强制 verify_on_stop=true 改为 false | 否（未设此字段） |
| v32->v33 | delegation.max_async_children -> max_concurrent_children | 否（未设此字段） |

结论：config.yaml 迁移安全，不破坏现有配置。

### delegate_task credential pool bug

- Issue #71424：在 v0.19.0 中仍然 OPEN
- PR #71454（修复）：未合并
- 升级到 v0.19.0 不修复 delegate_task 401 问题

### 升级收益（v0.17.0-v0.19.0 新功能）

- v0.17.0：Bitwarden/1Password 密钥管理、provider enabled:false
- v0.18.0：/learn 自动生成技能、/journey 学习时间线、gateway 空闲休眠、verify-on-stop
- v0.19.0：堆叠斜杠技能调用、/subscription、多 profile 路由、reasoning max/ultra、技能发现缓存5x

### 风险评估

| 风险 | 概率 | 缓解 |
|------|------|------|
| config.yaml 迁移异常 | 极低 | 已备份 |
| 自定义 provider 不兼容 | 极低 | 依赖版本一致 |
| 技能格式不兼容 | 极低 | 格式未变 |
| gateway 启动失败 | 低 | 可 pip install 回退 |

### 结论

升级本身安全（依赖一致、config 迁移无破坏），但升级不解决 delegate_task 问题。新功能（/learn、gateway 休眠、技能缓存）有价值但非急需。
