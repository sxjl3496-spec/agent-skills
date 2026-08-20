"""
CSSCI过滤测试 - 检索一页，打印每行的期刊名和CSSCI判断结果（不下载）
"""
from playwright.sync_api import sync_playwright
import json, time, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cssci_journals import is_cssci

TEMP = os.environ.get("TEMP", r"C:\Users\sxjl3\AppData\Local\Temp")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
    page = context.new_page()

    with open(f"{TEMP}\\pw_cookies.json", "r") as f:
        cookies = json.load(f)
    for c in cookies:
        try:
            context.add_cookies([{
                "name": c["name"], "value": c["value"],
                "domain": c.get("domain", ".wxy88.top"), "path": c.get("path", "/"),
            }])
        except Exception:
            pass

    page.goto("http://www.wxy88.top/e/action/ShowInfo.php?classid=62&id=1077", timeout=30000)
    time.sleep(2)
    page.goto("http://www.wxy88.top/cnkipdf.php", timeout=30000)
    time.sleep(5)
    if "您未登录" in page.content():
        print("❌ 未登录")
        browser.close()
        exit(1)

    page.goto("https://pdf.ccki.top/kns8s/defaultresult/index", timeout=30000)
    time.sleep(3)
    box = page.locator(".search-input").first
    box.fill("碳排放权交易")
    time.sleep(0.5)
    page.locator(".search-btn").first.click()
    time.sleep(8)
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    time.sleep(2)

    rows = page.locator("table.result-table-list tbody tr").all()
    print(f"结果行: {len(rows)}个\n")
    cssci_count = 0
    for i, row in enumerate(rows):
        try:
            journal = row.locator("td.source").first.inner_text().strip() if row.locator("td.source").first.count() > 0 else ""
            title_el = row.locator("td.name a").first
            title = title_el.inner_text().strip() if title_el.count() > 0 else ""
            is_c = is_cssci(journal)
            if is_c:
                cssci_count += 1
            mark = "✅CSSCI" if is_c else "❌非"
            print(f"  [{i+1}] {mark} [{journal}] {title[:45]}")
        except Exception as e:
            print(f"  [{i+1}] 提取失败: {e}")

    print(f"\nCSSCI占比: {cssci_count}/{len(rows)}")
    browser.close()
