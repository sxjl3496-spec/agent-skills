"""
知网镜像检索（复用登录cookie）- 检索 → 提取结果列表 → 支持翻页
用法: python pw_search2.py "关键词" --page 1 --size 20
"""
from playwright.sync_api import sync_playwright
import json, time, os, sys, argparse, re

TEMP = os.environ.get("TEMP", r"C:\Users\sxjl3\AppData\Local\Temp")
COOKIES_FILE = os.path.join(TEMP, "pw_cookies.json")

def load_cookies(context):
    with open(COOKIES_FILE, "r") as f:
        cookies = json.load(f)
    # 转换playwright cookie格式
    for c in cookies:
        try:
            context.add_cookies([{
                "name": c["name"], "value": c["value"],
                "domain": c.get("domain", ".wxy88.top"),
                "path": c.get("path", "/"),
            }])
        except Exception:
            pass
    print(f"✅ 已加载 {len(cookies)} 个cookie")

def goto_mirror(page):
    """进入知网镜像"""
    page.goto("http://www.wxy88.top/e/action/ShowInfo.php?classid=62&id=1077", timeout=30000)
    time.sleep(2)
    page.goto("http://www.wxy88.top/cnkipdf.php", timeout=30000)
    time.sleep(5)
    return page.url

def search_and_extract(page, keyword, page_num=1):
    """搜索并提取结果"""
    page.goto("https://pdf.ccki.top/kns8s/defaultresult/index", timeout=30000)
    time.sleep(3)

    # 输入关键词
    box = page.locator(".search-input").first
    box.fill(keyword)
    time.sleep(0.5)

    # 搜索
    btn = page.locator(".search-btn").first
    btn.click()
    time.sleep(8)
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    time.sleep(2)

    # 保存HTML
    for _ in range(5):
        try:
            html = page.content()
            break
        except Exception:
            time.sleep(2)
    out = os.path.join(TEMP, f"pw2_{keyword}_p{page_num}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    # 提取论文列表（知网结果表格）
    papers = []
    try:
        rows = page.locator("table.result-table-list tbody tr, #gridTable tr.result-table-list, .result-table-list tbody tr").all()
        for row in rows:
            txt = row.inner_text().strip()
            if txt and len(txt) > 20:
                papers.append(txt)
    except Exception as e:
        print(f"提取表格失败: {e}")

    # 总数
    total = ""
    m = re.search(r'共\s*<[^>]*>?(\d+)', html) or re.search(r'(\d+)\s*条结果', html) or re.search(r'共\s*(\d+)\s*条', html)
    if m:
        total = m.group(1)

    return {"keyword": keyword, "page": page_num, "total": total, "papers": papers, "html_file": out}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword")
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        )
        load_cookies(context)
        page = context.new_page()

        url = goto_mirror(page)
        print(f"镜像: {url}")
        title = page.title()
        content = page.content()
        if "您未登录" in content:
            print("❌ 未登录！cookie过期，需要重新登录")
            browser.close()
            sys.exit(1)
        print(f"✅ 已登录: {title}")

        result = search_and_extract(page, args.keyword, args.page)
        print(f"\n=== 检索结果 ===")
        print(f"关键词: {result['keyword']}, 页码: {result['page']}")
        print(f"总数: {result['total']}, 提取论文: {len(result['papers'])}")
        for i, paper in enumerate(result['papers'][:5]):
            print(f"  [{i+1}] {paper[:120]}")

        browser.close()

if __name__ == "__main__":
    main()
