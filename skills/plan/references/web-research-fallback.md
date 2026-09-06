# 主 Agent Web 调研降级方案

## 适用场景

plan 执行中需要 web 调研，但以下条件同时成立：
- delegate_task 子agent 失败（API key 失效、模型限额、循环卡死等）
- 主 agent 没有加载 web/web_search 工具集
- 需要在主 agent 中直接用 HTTP 请求做搜索

## 技术方案：Python requests + 百度搜索

### 核心要点

1. **必须设置 `trust_env = False`**：Windows 上系统代理设置（HTTP_PROXY/HTTPS_PROXY）会导致 SSL 错误或连接失败。`requests.Session()` 默认读取系统代理，设 `trust_env = False` 可绕过。

2. **用百度而非 Bing**：从本机环境直连 Bing 会触发 SSL EOF 错误（`SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING]')`），百度搜索无此问题。

3. **百度搜索结果链接是重定向 URL**：格式为 `http://www.baidu.com/link?url=...`，需跟随重定向获取真实页面。

### 完整代码模板

```python
import requests
import re

session = requests.Session()
session.trust_env = False  # 关键：绕过系统代理

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
}

def baidu_search(keyword, num=10):
    """百度搜索，返回 (标题, 百度重定向URL) 列表"""
    resp = session.get("https://www.baidu.com/s",
                      params={"wd": keyword, "rn": num},
                      headers=headers, timeout=15)
    results = re.findall(
        r'<h3[^>]*>.*?<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
        resp.text, re.DOTALL
    )
    out = []
    for url, title in results[:num]:
        clean = re.sub(r'<[^>]+>', '', title).strip()
        if clean:
            out.append((clean, url))
    return out

def fetch_page(baidu_url):
    """跟随百度重定向，获取真实页面内容"""
    resp = session.get(baidu_url, headers=headers, timeout=15, allow_redirects=True)
    # 去掉 script/style
    text = re.sub(r'<script[^>]*>.*?</script>', '', resp.text, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    # 提取正文
    paragraphs = re.findall(
        r'<(?:p|div|li|td|span|article)[^>]*>(.*?)</(?:p|div|li|td|span|article)>',
        text, re.DOTALL
    )
    full = ' '.join(paragraphs)
    full = re.sub(r'<[^>]+>', ' ', full)
    full = re.sub(r'\s+', ' ', full).strip()
    return full

# 使用示例
results = baidu_search("你的搜索关键词")
for title, url in results:
    print(f"  {title}")
    content = fetch_page(url)
    print(content[:2000])
```

### 注意事项

- **百度图片搜索结果**返回的不是文章页，是图片聚合页，内容不可用。搜索结果中标题含"百度图片"的条目应跳过。
- **百度视频搜索**（`/sf/vsearch?...`）也不是文章页，跳过。
- **百度重定向有时很慢**（15秒超时可能不够），可适当调大 timeout。
- **编码问题**：部分百度重定向页面返回 GBK 编码，需检查 `resp.encoding`。
- **搜索结果质量**：百度搜索结果含大量百度自家产品（百度知道、百度文库、百度图片），需筛选。
- **多关键词搜索**：同一主题用 3-5 个不同关键词搜索，交叉比对结果，避免单一关键词的偏差。

### 在 execute_code 中使用

可以将上述代码写入 `.py` 文件用 `write_file` + `terminal` 运行，避免 `execute_code` 中的多行字符串转义问题。也可以直接在 `execute_code` 中内嵌，但注意 f-string 中不能含反斜杠（见陷阱7）。

### 在 plan 中的使用位置

1. **步骤3.1 补救**：delegate_task 返回后覆盖度检查发现缺口时，用此方法补充缺失信息
2. **陷阱2 处理**：delegate_task 子agent 卡死或失败后，用此方法替代
3. **阶段4 验证**：需要验证交付物中引用的事实时，用此方法快速查证

## 已知限制

- 无法搜索英文技术文档（百度对英文内容的索引不如 Google/Bing）
- 无法访问需要登录的页面（知乎、微信公众号等）
- 搜索结果可能过时或含 SEO 垃圾
- 如需更高质量的搜索，考虑安装 browser 工具集或配置可用的 web_search provider
