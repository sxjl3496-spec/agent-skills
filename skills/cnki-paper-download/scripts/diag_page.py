"""诊断：镜像页面实际加载状态"""
from playwright.sync_api import sync_playwright
import json, time, os

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
    time.sleep(6)

    body = page.inner_text("body")
    print(f"页面文本({len(body)}字符):")
    print(body[:800])
    print("\n---")
    for sel in [".search-input", "#search-input", "input", "iframe"]:
        count = page.locator(sel).count()
        print(f"元素 {sel}: {count}个")
    browser.close()
