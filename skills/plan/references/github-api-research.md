# GitHub API + Google 搜索技术

当 delegate_task 不可用时，在主 agent 中用 terminal + curl 直接搜索。

## GitHub API 搜索（无需 token，直连可用）

### 搜索仓库

```bash
curl -s "https://api.github.com/search/repositories?q=KEYWORDS&sort=stars&per_page=5" \
  | python -c "
import sys,json
d=json.load(sys.stdin)
for r in d.get('items',[])[:5]:
    print(f'  {r[\"full_name\"]} | ⭐{r[\"stargazers_count\"]} | {r.get(\"description\",\"\")[:80]}')
"
```

**搜索技巧**：
- 关键词用 `+` 连接：`prompt+engineering+agent`
- `sort=stars` 按星数排序
- `per_page=5` 限制返回数量
- 多个主题用 for 循环批量搜索（见下文）

### 获取仓库详情

```bash
curl -s "https://api.github.com/repos/OWNER/REPO" \
  | python -c "
import sys,json
d=json.load(sys.stdin)
print(f'  ⭐{d.get(\"stargazers_count\",0)} | {d.get(\"description\",\"\")[:120]}')
print(f'  Topics: {d.get(\"topics\",[])}')
print(f'  Updated: {d.get(\"updated_at\",\"\")}')
"
```

### 获取 README 内容

```bash
curl -s "https://api.github.com/repos/OWNER/REPO/readme" \
  | python -c "
import sys, json, base64
d = json.load(sys.stdin)
content = base64.b64decode(d.get('content','')).decode('utf-8', errors='ignore')
lines = content.split('\n')
for line in lines[20:80]:  # 跳过 header badges
    print(line)
"
```

**注意**：README 的 `content` 字段是 base64 编码的，需要解码。跳过前 20 行通常是 badge 图片。

### 批量搜索多个主题

```bash
for topic in "prompt+engineering+agent" "context+engineering+agent" "agentic+loop"; do
  echo "=== $topic ==="
  curl -s "https://api.github.com/search/repositories?q=${topic}&sort=stars&per_page=5" \
    | python -c "
import sys,json
d=json.load(sys.stdin)
for r in d.get('items',[])[:5]:
    print(f'  {r[\"full_name\"]} | ⭐{r[\"stargazers_count\"]} | {r.get(\"description\",\"\")[:80]}')
"
  echo ""
done
```

**经验**：一次 terminal 调用搜索 5 个主题，约 15 秒完成。比 delegate_task 更快更可靠。

## Google 搜索（需 Clash 代理）

Clash Verge 默认 HTTP 代理端口为 7897（非标准 7890）。

```bash
curl -s -x http://127.0.0.1:7897 "https://www.google.com/search?q=QUERY&num=5" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  --max-time 15
```

**注意**：Google HTML 搜索结果的链接解析不稳定（页面结构经常变化）。如果只需要确认"能不能连上"，检查 HTTP 状态码即可：
```bash
curl -s -x http://127.0.0.1:7897 "https://www.google.com/search?q=test" \
  -o /dev/null -w "Google: HTTP %{http_code}"
```

## 并行搜索策略

在同一个回复中发出多个 terminal 调用：
1. 一个 terminal 调用做 GitHub API 搜索
2. 另一个 terminal 调用做 Google 搜索
3. 两者并行执行，结果一起返回

## 代理端口检测

```bash
# 检测 Clash 是否在运行及端口
for port in 7890 7891 7892 7893 7897 1080; do
    result=$(curl -s -x http://127.0.0.1:$port "https://www.google.com" --max-time 5 -o /dev/null -w "%{http_code}" 2>&1)
    echo "Port $port: $result"
done
```

当前已知：Clash Verge 端口 7897，github.com/api.github.com 直连可用（不需代理）。
