---
name: debug-helper
description: >
  调试助手技能。封装常见调试模式，提升排查效率。
  涵盖：错误分类、日志分析、变量追踪、API诊断、网络排查。
  触发词：调试、debug、排查、为什么报错、报错了、出错。
---

# 调试助手 (debug-helper)

## 何时使用

- 执行命令报错，需要排查原因
- 配置不生效，需要诊断
- API 调用失败，需要定位
- 网络连接问题

## 铁律：无根因不修复（Root Cause First）⭐

**来源**：Superpowers systematic-debugging（obra/superpowers ★266K，2026-08-05 借鉴引入）

**核心原则**：**没有完成根因调查之前，禁止提出任何修复方案。症状修复（看到报错就改，不追根因）就是失败。**

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

**Phase 1：根因调查（必须先完成）**

1. **复现**：实际重现问题，记录触发条件（输入、环境、步骤）
2. **收集证据**：错误日志、traceback、配置值、环境变量、版本信息
3. **缩小范围**：二分法/隔离法定位问题层（环境→配置→代码→依赖→网络）
4. **确认根因**：能解释"为什么这个症状出现"的底层原因，不满足于"表面报错"

**Phase 1 完成前禁止**：
- 提出修复方案
- 猜测性修改代码/配置
- "应该是XX问题，改一下试试"

**正确做法**：
- ❌ "报错了，可能是超时，把timeout调大试试"
- ✅ "复现成功：调用X API时返回429。检查限额→确认Coding Plan额度耗尽→根因是降级链未生效（CLI_CONFIG快照），修复：重启gateway加载新配置"

**与用户的排查要求一致**：逐层深入排除（查prefs→查DB→strings搜exe→asar extract→curl后端端口），不跳步给结论（2026.8.4 用户纠正）。

## 调试模式

### 1. 错误分类（先判断错误类型）

| 错误类型 | 特征 | 第一步 |
|---------|------|--------|
| API 401 | 认证失败 | 检查 API key 环境变量 |
| API 403 | 权限不足/模型不可用 | 检查模型名称和权限 |
| API 429 | 限流 | 检查限额，切换备用模型 |
| API 超时 | 网络问题 | 检查代理/网络 |
| ModuleNotFoundError | Python 包缺失 | pip install |
| FileNotFoundError | 路径错误 | 检查绝对路径 |
| SSL Error | 代理/证书 | session.trust_env=False |
| Permission Denied | 权限 | 检查文件权限 |
| SyntaxError | 语法错误 | 检查 Python 版本兼容 |

### 2. API 诊断流程

```bash
# Step 1: 检查环境变量
echo "${API_KEY:+set}"           # 输出set则有值
echo "length=${#API_KEY}"        # 长度应为30-60

# Step 2: 检查 .env 文件
grep "API_KEY" ~/AppData/Local/hermes/.env

# Step 3: 直接 curl 测试
curl -s "ENDPOINT_URL" \
  -H "Authorization: Bearer $API_KEY" \
  --max-time 10 | python -c "import sys,json; print(json.load(sys.stdin))"

# Step 4: 检查 config.yaml 中的变量名匹配
grep "api_key" config.yaml
```

### 3. 网络诊断流程

```bash
# 直连测试
curl -s -o /dev/null -w "%{http_code}" URL --max-time 10

# 代理测试（Clash 7897）
curl -s -x http://127.0.0.1:<代理端口> -o /dev/null -w "%{http_code}" URL --max-time 10

# DNS 检查
nslookup DOMAIN

# 端口检查
curl -s http://127.0.0.1:<代理端口> -o /dev/null -w "%{http_code}"
```

### 4. Hermes 特有诊断

```bash
# Gateway 状态
hermes gateway status

# 降级链检查
hermes fallback list

# 配置验证
hermes config show

# 进程检查
tasklist | grep -i "hermes\|python"

# Gateway 日志（最近50行）
tail -50 ~/AppData/Local/hermes/logs/gateway.log
```

### 5. Python 代码调试

```python
# 变量检查
import inspect, traceback

# 函数源码检查
print(inspect.getsource(function_name))

# 完整 traceback
import traceback
traceback.print_exc()

# 模块路径
import module
print(module.__file__)
```

### 6. 文件搜索

```bash
# 搜索配置项
grep -rn "关键词" /path/to/search/

# 搜索文件
find /path -name "*.py" -newer reference_file

# 检查文件修改时间
ls -la --time-style=full-iso /path/to/file
```

## 常见陷阱

1. **环境变量未传递**：Windows Scheduled Task 启动的 gateway 不 source ~/.bashrc
2. **CLI_CONFIG 快照**：gateway 启动时加载配置，修改 config.yaml 后需重启
3. **f-string 反斜杠**：Python 3.11 中 f-string 内不能用反斜杠
4. **代理端口**：Clash Verge 端口可能是 7897 而非 7890
5. **thinking 模式**：Coding Plan 模型默认 thinking，需关闭
