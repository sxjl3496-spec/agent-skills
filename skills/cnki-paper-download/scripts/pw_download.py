"""
知网镜像批量下载脚本 v3 - 限速规则写死 + CSSCI过滤 + 每日限额自动停止
- 每篇间隔 ≥ 3秒
- 1分钟 ≤ 20篇
- 3分钟 ≤ 50篇
- 默认上限 18篇/次（每日限额约18-20篇，少帅2026.8.6设定）
- 只下载CSSCI来源期刊论文（少帅2026.8.6要求）
- 检测到"下载次数已用尽"立即停止
- 断点续传：已存在的PDF自动跳过

用法: python pw_download.py [--max 18] [--output 目录]
"""
from playwright.sync_api import sync_playwright
import json, time, os, sys, re, threading, pickle, argparse

# 引入CSSCI名单
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cssci_journals import is_cssci

TEMP = os.environ.get("TEMP", r"C:\Users\sxjl3\AppData\Local\Temp")
OUTPUT_DIR = r"D:\BaiduSyncdisk\AIKnowledgeBase\ObsidianVault\academia\文献库\碳排放权交易"
MAX_PAPERS = 18  # 每次运行默认下载上限（每日限额约18-20篇）

# ========== 限速规则（写死，任何情况不绕过）==========
MIN_INTERVAL = 3.0      # 每篇最小间隔（秒）
MAX_PER_MIN = 20        # 每分钟上限
MAX_PER_3MIN = 50       # 每3分钟上限

# 限速状态
class RateLimiter:
    def __init__(self):
        self.timestamps = []
        self.lock = threading.Lock()

    def wait(self):
        """在下载前调用，确保符合限速规则"""
        with self.lock:
            now = time.time()
            # 清理超过3分钟的记录
            self.timestamps = [t for t in self.timestamps if now - t < 180]
            # 检查3分钟窗口
            if len(self.timestamps) >= MAX_PER_3MIN:
                sleep_time = 180 - (now - self.timestamps[0]) + 1
                print(f"⏳ 3分钟窗口已达{MAX_PER_3MIN}篇，等待{sleep_time:.0f}秒...")
            else:
                # 检查1分钟窗口
                last_60s = [t for t in self.timestamps if now - t < 60]
                if len(last_60s) >= MAX_PER_MIN:
                    sleep_time = 60 - (now - last_60s[0]) + 1
                    print(f"⏳ 1分钟窗口已达{MAX_PER_MIN}篇，等待{sleep_time:.0f}秒...")
                else:
                    # 最小间隔
                    if self.timestamps:
                        sleep_time = MIN_INTERVAL - (now - self.timestamps[-1])
                        if sleep_time > 0:
                            print(f"⏳ 间隔等待{sleep_time:.1f}秒...")
                            time.sleep(sleep_time)
                            return
                        sleep_time = 0
                    else:
                        sleep_time = 0
            if sleep_time > 0:
                time.sleep(sleep_time)
            self.timestamps.append(time.time())

KEYWORDS = ["碳排放权交易", "碳交易", "碳市场", "碳配额", "碳价", "碳排放交易", "排污权交易", "碳交易政策", "碳中和", "碳排放权"]

def extract_paper_info(row_html):
    """从结果行提取论文信息（标题/作者/期刊/年份）"""
    title_m = re.search(r'title="([^"]*)"|data-filename="([^"]*)"', row_html)
    return title_m.group(1) if title_m else ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=MAX_PAPERS, help="本次下载上限")
    parser.add_argument("--output", type=str, default=OUTPUT_DIR, help="输出目录")
    args = parser.parse_args()

    max_papers = args.max
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    rate = RateLimiter()
    downloaded = []
    errors = []
    quota_exhausted = False  # 每日额度用尽标记

    # 收集已存在的PDF（断点续传：已下载的文件不再重复下）
    existing_files = set(os.listdir(output_dir)) if os.path.isdir(output_dir) else set()
    print(f"📁 已存在文件: {len(existing_files)}个，将跳过重复下载")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            accept_downloads=True
        )
        page = context.new_page()

        # 加载cookie
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

        # 进入镜像
        page.goto("http://www.wxy88.top/e/action/ShowInfo.php?classid=62&id=1077", timeout=30000)
        time.sleep(2)
        page.goto("http://www.wxy88.top/cnkipdf.php", timeout=30000)
        time.sleep(5)
        if "您未登录" in page.content():
            print("❌ 未登录！需要重新登录")
            browser.close()
            sys.exit(1)
        print("✅ 已登录镜像")

        # 遍历关键词
        for kw_idx, kw in enumerate(KEYWORDS):
            if len(downloaded) >= max_papers:
                print(f"\n✅ 已达上限 {max_papers} 篇，停止")
                break
            if quota_exhausted:
                print(f"\n⚠️ 每日额度已用尽，停止")
                break

            print(f"\n=== [{kw_idx+1}/{len(KEYWORDS)}] 关键词: {kw} ===")
            try:
                # 强制刷新页面（重置状态，避免搜索框找不到）
                page.goto("https://pdf.ccki.top/kns8s/defaultresult/index", timeout=30000)
                time.sleep(4)
                # 确保搜索框存在（等待最多20秒）
                box = page.locator(".search-input").first
                box.wait_for(state="visible", timeout=20000)
                box.fill(kw)
                time.sleep(0.5)
                page.locator(".search-btn").first.click()
                time.sleep(7)
                try:
                    page.wait_for_load_state("networkidle", timeout=12000)
                except Exception:
                    pass
                time.sleep(2)
            except Exception as e:
                # 检查是否每日额度用尽（页面文本判断）
                try:
                    page_text = page.inner_text("body")[:500]
                    if "下载次数已用尽" in page_text or "请明天再来" in page_text:
                        print(f"⚠️ 每日额度已用尽！停止本次下载")
                        quota_exhausted = True
                        break
                except Exception:
                    pass
                print(f"  检索失败: {e}，等待60秒重试...")
                time.sleep(60)
                try:
                    page.goto("https://pdf.ccki.top/kns8s/defaultresult/index", timeout=30000)
                    time.sleep(4)
                    box = page.locator(".search-input").first
                    box.wait_for(state="visible", timeout=20000)
                    box.fill(kw)
                    time.sleep(0.5)
                    page.locator(".search-btn").first.click()
                    time.sleep(7)
                    try:
                        page.wait_for_load_state("networkidle", timeout=12000)
                    except Exception:
                        pass
                    time.sleep(2)
                except Exception as e2:
                    # 重试仍失败：检查额度
                    try:
                        page_text = page.inner_text("body")[:500]
                        if "下载次数已用尽" in page_text or "请明天再来" in page_text:
                            print(f"⚠️ 每日额度已用尽！停止本次下载")
                            quota_exhausted = True
                            break
                    except Exception:
                        pass
                    print(f"  重试仍失败: {e2}，跳过该词")
                    continue

            # 翻页下载
            page_num = 1
            while len(downloaded) < max_papers:
                print(f"\n  -- 第{page_num}页 --")
                # 获取本页所有结果行（每行包含标题/作者/期刊/下载按钮）
                rows = page.locator("table.result-table-list tbody tr").all()
                print(f"  本页结果行: {len(rows)}个")

                if len(rows) == 0:
                    break

                for row_idx, row in enumerate(rows):
                    if len(downloaded) >= max_papers:
                        break
                    # 每行处理前检查额度（若已用尽立即停止）
                    if quota_exhausted:
                        break
                    try:
                        # 提取期刊名（td.source 内的文本）
                        journal = ""
                        src_td = row.locator("td.source").first
                        if src_td.count() > 0:
                            journal = src_td.inner_text().strip()
                        # 提取标题（td.name 或 title属性）
                        title = ""
                        title_el = row.locator("td.name a, td a.fz14").first
                        if title_el.count() > 0:
                            title = title_el.inner_text().strip()

                        # CSSCI过滤：非CSSCI期刊跳过（不消耗下载）
                        if not is_cssci(journal):
                            print(f"  ⏭️ 非CSSCI跳过: [{journal}] {title[:30]}")
                            continue

                        print(f"  📖 CSSCI确认: [{journal}] {title[:40]}")

                        # 限速等待（固定3秒，即使前面都是跳过也等）
                        rate.wait()

                        # 每5篇下载后额外休息10秒（防限流）
                        if len(downloaded) > 0 and len(downloaded) % 5 == 0:
                            print(f"  💤 每5篇防限流休息10秒...")
                            time.sleep(10)

                        # 在行内找下载按钮（PDF优先）
                        dl_btn = row.locator("a.downloadlink").first
                        if dl_btn.count() == 0:
                            print(f"  ⏭️ 无下载按钮: {title[:30]}")
                            continue

                        # 点击下载（失败自动重试1次，超时等待更长）
                        download = None
                        for attempt in range(2):
                            try:
                                with page.expect_download(timeout=30000) as dl_info:
                                    dl_btn.click()
                                download = dl_info.value
                                break
                            except Exception as e:
                                if attempt == 0:
                                    print(f"  ⚠️ 下载超时，等待60秒后重试...")
                                    time.sleep(60)
                                else:
                                    raise e
                        if download is None:
                            raise Exception("下载两次失败")

                        fname = download.suggested_filename
                        # 过滤：只要PDF，跳过CAJ
                        if not fname.lower().endswith(".pdf"):
                            print(f"  ⏭️ 跳过非PDF: {fname[:40]}")
                            continue
                        # 已存在文件跳过（断点续传）
                        if fname in existing_files:
                            print(f"  ⏭️ 已下载过，跳过: {fname[:45]}")
                            continue
                        save_path = os.path.join(output_dir, fname)
                        # 避免重名
                        if os.path.exists(save_path):
                            save_path = os.path.join(output_dir, f"{int(time.time())}_{fname}")
                        download.save_as(save_path)
                        size = os.path.getsize(save_path)
                        if size > 10000:
                            downloaded.append({"file": fname, "path": save_path, "kw": kw,
                                               "journal": journal, "title": title, "size": size})
                            existing_files.add(fname)
                            print(f"  ✅ [{len(downloaded)}/{max_papers}] [{journal}] {fname[:45]} ({size//1024}KB)")
                        else:
                            os.remove(save_path)
                            print(f"  ⚠️ 文件过小已删除: {fname[:40]}")
                            errors.append(fname)
                        # 额外防抖（下载本身耗时也算间隔）
                        time.sleep(1)
                    except Exception as e:
                        print(f"  ❌ 行{row_idx}下载失败: {e}")
                        errors.append(f"row{row_idx}: {e}")
                        # 连续下载失败可能是额度用尽，检查页面
                        try:
                            page_text = page.inner_text("body")[:500]
                            if "下载次数已用尽" in page_text or "请明天再来" in page_text:
                                print(f"⚠️ 每日额度已用尽！停止本次下载")
                                quota_exhausted = True
                                break
                        except Exception:
                            pass
                        time.sleep(5)

                # 下一页
                if len(downloaded) >= max_papers:
                    break
                next_btn = page.locator("a.next, .next, .page-next, [class*='next']").first
                if next_btn.count() > 0:
                    try:
                        next_btn.click()
                        time.sleep(5)
                        try:
                            page.wait_for_load_state("networkidle", timeout=12000)
                        except Exception:
                            pass
                        time.sleep(2)
                        page_num += 1
                    except Exception as e:
                        print(f"  翻页失败: {e}")
                        break
                else:
                    print(f"  没有下一页（本词结束）")
                    break

        browser.close()

    # 汇总
    print(f"\n{'='*50}")
    print(f"✅ 下载完成: {len(downloaded)}/{max_papers} 篇")
    print(f"❌ 失败: {len(errors)} 个")
    print(f"📁 目录: {output_dir}")

    # 保存记录
    record = {
        "downloaded": downloaded,
        "errors": errors,
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "rate_limit": {"min_interval": MIN_INTERVAL, "max_per_min": MAX_PER_MIN, "max_per_3min": MAX_PER_3MIN}
    }
    with open(os.path.join(output_dir, "_download_record.json"), "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"📋 记录: {output_dir}\\_download_record.json")

if __name__ == "__main__":
    main()
