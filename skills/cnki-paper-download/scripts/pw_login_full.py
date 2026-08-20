"""
Playwright 登录文献云 + 保存cookie（供后续复用）
用法: python pw_login_full.py <验证码>
成功后：cookie 存 TEMP/pw_cookies.json，可用于后续脚本
"""
from playwright.sync_api import sync_playwright
import json, time, os, sys

TEMP = os.environ.get("TEMP", r"C:\Users\sxjl3\AppData\Local\Temp")
USERNAME = "418710404"
PASSWORD = "434501"
CAPTCHA = sys.argv[1] if len(sys.argv) > 1 else ""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
    page = context.new_page()

    # 打开首页
    page.goto("http://www.wxy88.top/", timeout=30000)
    print(f"首页: {page.title()}")

    # 填表
    page.fill("#user_name", USERNAME)
    page.fill("#password", PASSWORD)
    page.fill("#code", CAPTCHA)
    print("表单已填写")
    time.sleep(1)

    # 提交
    page.click("#ok")
    time.sleep(3)
    print(f"登录后URL: {page.url}")

    # 检查登录是否成功（是否有用户cookie）
    cookies = context.cookies()
    has_auth = any("auth" in c["name"].lower() or "userid" in c["name"].lower() for c in cookies)
    print(f"cookies: {len(cookies)}个, 有认证cookie: {has_auth}")

    # 保存cookie
    with open(f"{TEMP}\\pw_cookies.json", "w") as f:
        json.dump(cookies, f)
    print(f"✅ cookies已保存: {TEMP}\\pw_cookies.json")

    # 验证：进入知网入口
    page.goto("http://www.wxy88.top/e/action/ShowInfo.php?classid=62&id=1077", timeout=30000)
    time.sleep(2)
    page.goto("http://www.wxy88.top/cnkipdf.php", timeout=30000)
    time.sleep(6)
    print(f"镜像页URL: {page.url}")
    print(f"标题: {page.title()}")
    content = page.content()
    if "您未登录" in content:
        print("❌ 未登录！")
    elif len(content) > 5000:
        print("✅ 已登录，检索界面加载成功！")

    browser.close()
