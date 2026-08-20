# Playwright 自动化完整方案

> 来源：文献云平台自动化下载（2026.8.6 验证通过）
> 优势：真实浏览器环境，登录态稳定，验证码可自动识别

## 安装

### 首次安装

```bash
# 安装playwright + chromium（国内镜像加速）
export PLAYWRIGHT_DOWNLOAD_HOST=https://cdn.npmmirror.com/binaries/playwright
python -m playwright install chromium
```

### 常见问题

**360安全卫士阻止安装**：
- 错误：`EPERM: operation not permitted, open 'D3DCompiler_47.dll'`
- 原因：360锁住系统DLL文件
- 修复：**完全退出360**（包括托盘图标），重新安装

**安装后验证**：
```python
from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    exe = p.chromium.executable_path
    print(f"chromium路径: {exe}")
    print(f"浏览器存在: {os.path.exists(exe)}")
    browser.close()
```

## 完整流程

### 1. 登录文献云

```python
from playwright.sync_api import sync_playwright
import json, time, os

TEMP = os.environ.get("TEMP", r"C:\Users\sxjl3\AppData\Local\Temp")
USERNAME = "418710404"
PASSWORD = "434501"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
    page = context.new_page()

    # 1. 打开首页
    page.goto("http://www.wxy88.top/", timeout=30000)
    print(f"首页: {page.title()}")

    # 2. 截图验证码
    cap = page.locator("img[src*='ShowKey']")
    cap.screenshot(path=f"{TEMP}\\captcha.png")
    print(f"验证码已截图: {TEMP}\\captcha.png")

    # 3. 用 vision_analyze 识别验证码
    # 提示词："这是一个网站登录验证码图片，请只输出验证码中的字符，注意字母都是小写。"

    # 4. 填表提交
    page.fill("#user_name", USERNAME)
    page.fill("#password", PASSWORD)
    page.fill("#code", CAPTCHA)  # 识别出的验证码
    page.click("#ok")
    time.sleep(3)

    # 5. 检查登录成功
    cookies = context.cookies()
    has_auth = any("auth" in c["name"].lower() or "userid" in c["name"].lower() for c in cookies)
    print(f"cookies: {len(cookies)}个, 有认证cookie: {has_auth}")

    # 6. 保存cookie
    with open(f"{TEMP}\\pw_cookies.json", "w") as f:
        json.dump(cookies, f)
    print(f"✅ cookies已保存")
```

### 2. 进入知网镜像（关键！必须按顺序）

```python
# 入口详情页
page.goto("http://www.wxy88.top/e/action/ShowInfo.php?classid=62&id=1077", timeout=30000)
time.sleep(2)

# 跳转知网镜像（必须经过cnkipdf.php）
page.goto("http://www.wxy88.top/cnkipdf.php", timeout=30000)
time.sleep(6)

# 验证
title = page.title()
content = page.content()
if "您未登录" in content:
    print("❌ 未登录！")
else:
    print(f"✅ 已登录: {title}")
```

**入口ID对照表**：
| 入口名 | ID | 数据库 |
|--------|-----|--------|
| 知网2 | id=1077 | 学术期刊（默认） |
| 知网33 | id=1076 | 学术期刊 |
| 知网12 | id=1765 | 国外数据库 |
| 万方6 | id=1774 | 万方数据 |

### 3. 检索+CSSCI过滤+下载

```python
def search_and_download(page, keyword, output_dir, max_papers=80):
    """搜索关键词，CSSCI过滤后下载"""
    import re
    from cssci_journals import is_cssci

    downloaded = []
    rate = RateLimiter()

    # 搜索
    page.goto("https://pdf.ccki.top/kns8s/defaultresult/index", timeout=30000)
    time.sleep(3)
    box = page.locator(".search-input").first
    box.wait_for(state="visible", timeout=20000)
    box.fill(keyword)
    time.sleep(0.5)
    page.locator(".search-btn").first.click()
    time.sleep(8)
    page.wait_for_load_state("networkidle", timeout=12000)
    time.sleep(2)

    # 逐页下载
    page_num = 1
    while len(downloaded) < max_papers:
        # 提取结果行
        rows = page.locator("table.result-table-list tbody tr").all()
        if len(rows) == 0:
            break

        for row in rows:
            if len(downloaded) >= max_papers:
                break

            # 提取期刊名
            journal = row.locator("td.source").first.inner_text().strip()
            title = row.locator("td.name a").first.inner_text().strip()

            # CSSCI过滤
            if not is_cssci(journal):
                time.sleep(3)  # ⭐ 跳过也要等3秒！
                print(f"⏭️ 非CSSCI: [{journal}] {title[:30]}")
                continue

            # 限速等待
            rate.wait()

            # 每5篇额外休息
            if len(downloaded) > 0 and len(downloaded) % 5 == 0:
                print(f"💤 每5篇休息10秒...")
                time.sleep(10)

            # 下载
            dl_btn = row.locator("a.downloadlink").first
            try:
                with page.expect_download(timeout=30000) as dl_info:
                    dl_btn.click()
                download = dl_info.value
                fname = download.suggested_filename

                if fname.lower().endswith(".pdf"):
                    save_path = os.path.join(output_dir, fname)
                    download.save_as(save_path)
                    downloaded.append({"file": fname, "journal": journal, "title": title})
                    print(f"✅ [{len(downloaded)}/{max_papers}] [{journal}] {fname[:45]}")
                else:
                    print(f"⏭️ 跳过非PDF: {fname[:40]}")
                time.sleep(1)
            except Exception as e:
                print(f"❌ 下载失败: {e}")
                time.sleep(5)

        # 翻页
        next_btn = page.locator("a.next, [class*='next']").first
        if next_btn.count() > 0:
            next_btn.click()
            time.sleep(5)
            page.wait_for_load_state("networkidle", timeout=12000)
            time.sleep(2)
            page_num += 1
        else:
            break

    return downloaded
```

### 4. 完整调用

```python
import json

OUTPUT_DIR = r"D:\BaiduSyncdisk\AIKnowledgeBase\academia\文献库\碳排放权交易"
KEYWORDS = ["碳排放权交易", "碳交易", "碳市场", "碳配额", "碳价", "排污权交易"]

all_downloaded = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(...)
    page = context.new_page()

    # 登录
    login(page)
    # 进入镜像
    goto_mirror(page)

    for kw in KEYWORDS:
        if len(all_downloaded) >= 80:
            break
        downloaded = search_and_download(page, kw, OUTPUT_DIR, max_papers=80-len(all_downloaded))
        all_downloaded.extend(downloaded)

    browser.close()

# 保存记录
with open(f"{OUTPUT_DIR}\\_download_record.json", "w", encoding="utf-8") as f:
    json.dump(all_downloaded, f, ensure_ascii=False, indent=2)
print(f"✅ 下载完成: {len(all_downloaded)}篇")
```

## 复用登录状态

### 保存Cookie

```python
cookies = context.cookies()
with open(f"{TEMP}\\pw_cookies.json", "w") as f:
    json.dump(cookies, f)
```

### 加载Cookie

```python
with open(f"{TEMP}\\pw_cookies.json", "r") as f:
    cookies = json.load(f)
for c in cookies:
    try:
        context.add_cookies([{
            "name": c["name"], "value": c["value"],
            "domain": c.get("domain", ".wxy88.top"),
            "path": c.get("path", "/"),
        }])
    except Exception:
        pass
```

## 常见问题

### 1. 搜索框超时（页面状态损坏）

**表现**：
```
Locator.fill: Timeout 30000ms exceeded
waiting for locator(".search-input").first
```

**原因**：多次检索后页面状态损坏，或每日额度用尽

**修复**：
1. 强制刷新页面
2. 等待元素可见再操作
3. 检测每日额度
4. 失败重试（等待60秒）

### 2. 下载超时（平台限流）

**表现**：点击下载按钮后20秒无响应

**修复**：
1. 固定3秒间隔
2. 每5篇休息10秒
3. 超时重试（等待60秒）
4. 错误重试间隔5秒

### 3. 验证码识别失败

**表现**：登录后仍在首页，或提示"验证码错误"

**修复**：
1. 验证码每次刷新，需重新截图
2. 提示词加"字母都是小写"
3. 识别失败重新拉取验证码

### 4. 登录态失效

**表现**：页面显示"您未登录"

**修复**：
1. 确认走了完整链路：入口页 → cnkipdf.php → 知网镜像
2. 确认cookie已加载
3. 重新登录

## 参考

- `references/cssci_journals.py` - CSSCI过滤名单
- `references/kns8_queryjson.md` - QueryJson结构
- `references/rate_limit_rules.md` - 限速规则
- `scripts/pw_download.py` - 完整下载脚本
