---
name: cnki-paper-download
description: >
  第三方文献平台（文献云 wxy88.top）自动化登录知网/万方/维普镜像，检索并限速下载CSSCI中文文献PDF。
  当少帅需要下载中文期刊文献（知网论文/CSSCI）且无机构访问权限，或需要批量下文献时触发。
  覆盖：平台登录（验证码识别）、知网镜像入口链路、KNS8检索接口（brief/grid）、CSSCI期刊过滤、
  限速规则（写死）、每日限额处理、断点续传、GB/T 7714文献清单生成。
  触发词：文献云、wxy88、ccki.top、知网账号、下载文献、下中文文献、CSSCI下载。
---

# 知网文献自动化下载（文献云平台）⭐ 2026.8.6 实战验证版

## 触发条件

- 少帅需要下载中文文献（知网/万方/维普），尤其是批量下载、按质量筛选
- 少帅提到"文献云"、"wxy88"、"ccki.top"、"知网账号"、"下载文献"等
- 文献综述/基金申报需要补中文核心文献时
- 已下载文献目录：`ObsidianVault\academia\文献库\<主题>\`（GB/T 7714清单同目录）

## 平台与账号（敏感信息不写入技能文件）

- 平台：文献云（wxy88.top，备用 lib.ccki.top）
- 账号/密码：存储在 memory 条目"文献云平台" + 本机 `D:\BaiduSyncdisk\知网查文献.txt`
- 平台性质：第三方文献代下服务（织网/万方/维普入口），登录后进入各数据库镜像

## ⚠️ 每日限额（2026.8.6 实测发现，最关键的坑）

```
镜像站有每日下载额度。用尽后页面显示：
"您今天的下载次数已用尽, 请明天再来"
```

**识别方法**：进入镜像后如果 `.search-input` 搜索框找不到/页面文本只有这句话 → **额度已用尽，非技术故障**。

**⚠️ 查询也不受额度豁免（2026.8.7 实测纠正）**：此前以为"下载受限但查询可用"，实测发现**额度用尽后 brief/grid 检索API也返回空**（39字节 `<html><head></head><body></body></html>`）。UI搜索框可能仍显示（input=68）但点击搜索后结果列表不渲染。**额度用尽 = 检索+下载全部不可用**，只能换入口或等明天。

**实测数据**：一天约可下载 18-20 篇 PDF 后触发限额（含检索和点击尝试均消耗额度）。

**处理**：
1. **先试换镜像入口**（见陷阱0c）：知网2额度尽→试知网10/12（id=1132/1765），其他入口有独立额度，可继续**查询**（下载是否可行待验证）
2. 所有入口都尽 → 立即停止下载，保存已下载文件
3. 整理当前成果（清单+验证），告知少帅"今日额度用尽，明日继续"
4. 明天（北京时间新一天）额度重置后可继续，脚本带断点续传（自动跳过已下载）

## 两套方案：requests（检索分析） vs Playwright（下载，推荐）

| 能力 | requests | Playwright |
|------|---------|-----------|
| 登录 | ✅ 可用 | ✅ 可用（更稳）|
| 进入镜像 | ✅ 可用 | ✅ 可用 |
| 检索接口 | ⚠️ 可调但易触发"检索模型参数错误" | ✅ 浏览器真实点击最可靠 |
| 下载PDF | ❌ 无法触发浏览器下载 | ✅ `expect_download` 捕获 |
| 结论 | 用于登录态保持/分析 | **下载必须用 Playwright** |

## 核心工作流

### 步骤0：登录（两种方式）

**方式A：requests + session（适合保持登录态）**

```python
import requests, pickle
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36"})
s.get("http://www.wxy88.top/", timeout=20)  # 建立cookie

# 获取验证码（必须与登录同一session！）
cap = s.get("http://www.wxy88.top/e/ShowKey/?v=login", timeout=20)
# 保存图片 -> vision_analyze 识别（提示词加"注意字母都是小写"）

login_data = {
    "enews": "login", "ecmsfrom": "/e/action/ListInfo/?classid=61",
    "username": "<账号>", "password": "<密码>",
    "key": "<验证码>", "ok": "立即登录"
}
r = s.post("http://www.wxy88.top/e/member/doaction.php", data=login_data, timeout=20)
# 成功标志：Set-Cookie 含 ujgpvmluserid / ujgpvmlauth
# 保存: pickle.dump(s.cookies, f) -> 存 TEMP/cnki_session.pkl
```

**方式B：Playwright 完整登录（推荐，cookie存 JSON）**

⚠️ **陷阱0**：登录页 `/e/member/login/` 的 id 与 name 反转！`id="password"` = 用户名框，`id="username"` = 密码框。详见陷阱0。

```python
from playwright.sync_api import sync_playwright
import json, time

TEMP = os.environ.get("TEMP", r"C:\Users\sxjl3\AppData\Local\Temp")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 ... Chrome/120.0")
    page = context.new_page()
    page.goto("http://www.wxy88.top/e/member/login/", timeout=45000, wait_until="domcontentloaded")
    time.sleep(5)
    # 陷阱0b：首次登录通常无验证码！只有失败后才出现。先检查再决定
    if page.locator("#code").count() > 0:
        cap_img = page.locator("img[src*='ShowKey']").first
        cap_img.screenshot(path=f"{TEMP}\\captcha.png")
        # vision_analyze 识别验证码（提示"注意字母都是小写"）
        page.fill("#code", "<验证码>")
    # 填表（注意id反转！）
    page.fill("#password", "<账号>")   # id=password 是用户名框！
    page.fill("#username", "<密码>")   # id=username 是密码框！
    # ⚠️ 提交按钮是 input[name=Submit]（type=submit），#ok 不存在！
    page.click("input[name=Submit]")
    time.sleep(4)
    cookies = context.cookies()
    json.dump(cookies, open(f"{TEMP}\\pw_cookies.json", "w"))
```

### 步骤1：进入知网镜像（必须按顺序 + 带cookie）

```
入口详情页: GET /e/action/ShowInfo.php?classid=62&id=1077   (知网2入口)
  ↓
跳转页: GET /cnkipdf.php   ← 必须带 Referer=入口页URL，且cookie已登录
  ↓
知网镜像: https://pdf.ccki.top/kns8s/defaultresult/index （已带登录态）
```

- **直接访问镜像首页会显示"您未登录"**——必须从 wxy88.top 的入口页 → cnkipdf.php 跳转
- 入口ID：知网2=id1077、知网12=id1765、万方6=id1774 等（在 `/e/action/ListInfo/?classid=61` 提取）
- Playwright 方式：`page.goto` 两次即可，cookie 自动带

### 步骤2：检索（KNS8接口已破解）

**真实接口**：`POST https://pdf.ccki.top/kns8s/brief/grid`

**真实 QueryJson 结构**（2026.8.6 从浏览器请求拦截验证）：

```json
{
  "Platform": "", "Resource": "CROSSDB", "Classid": "WD0FTY92", "Products": "",
  "QNode": {"QGroup": [{
    "Key": "Subject", "Title": "", "Logic": 0,
    "Items": [{"Field": "SU", "Value": "关键词", "Operator": "TOPRANK", "Logic": 0, "Title": "主题"}],
    "ChildItems": []
  }]},
  "ExScope": 1, "SearchType": 2, "Rlang": "BOTH",
  "KuaKuCode": "YSTT4HG0,LSTPFY1C,JUP3MUPD,MPMFIG1A,EMRPGLPA,WQ0UVIAA,BLZOG7CK,PWFIRAGL,NN3FJMUV,NLBO1Z6R",
  "Expands": {}, "SearchFrom": 1
}
```

**关键参数**（踩坑记录）：
- `Logic`: AND=0（数字不是字符串"AND"！）
- `Operator`: "TOPRANK"（不是0）
- `Resource`: "CROSSDB"（跨库）
- `Classid`: 页面里的 classid（WD0FTY92）
- `ExScope`: 1, `SearchType`: 2, `Rlang`: "BOTH"
- **`KuaKuCode` 必须有**（一堆库代码），缺失报"没有指定检索分类"
- 附带参数：`boolSearch=true`, `pageNum`, `pageSize=20`, `sortField=FFD`, `sortType=desc`, `dstyle=listmode`, `productStr`, `uniplatform=NZKPT`

**⚠️ requests 调接口风险**：即使参数全对也可能报"检索模型参数错误"或"您未登录"（cookie 与浏览器会话不一致）。**实际下载场景直接用 Playwright 点击搜索框+搜索按钮**最可靠。

### 步骤3：CSSCI 期刊过滤（写死名单）

```python
# 引入技能目录的 cssci_journals.py
from cssci_journals import is_cssci

# 每行结果：row.locator("td.source").first 提取期刊名
if not is_cssci(journal):
    continue  # 非CSSCI跳过，不消耗下载额度
```

- 名单：177 本 CSSCI（2025-2026）期刊，覆盖经济学/管理学/环境资源/综合社科/高校学报
- 匹配逻辑：精确匹配为主，**模糊匹配有已知bug（见陷阱10）**
- 名单文件：`scripts/cssci_journals.py`（可扩充）

### ⚠️ 陷阱10：is_cssci() 模糊匹配过松导致非CSSCI混入（2026.8.7 发现）⭐⭐⭐

**问题**：`cssci_journals.py` 中 `is_cssci()` 的模糊匹配逻辑 `name in j or j in name` 会将非CSSCI期刊误判为CSSCI：

| 非CSSCI文献 | 误匹配原因 |
|------------|-----------|
| 《国际金融》 | `"国际金融" in "国际金融研究"` → 误判CSSCI ✅ |
| 《重庆交通大学学报（社会科学版）` | `"社会科学" in name`（名单中有"社会科学"短词） → 误判CSSCI ✅ |
| 《江西师范大学学报（哲学社会科学版）` | 同上 → 误判CSSCI ✅ |
| 新闻稿（报纸类） | 若td.source为空或报纸名被部分匹配 → 可能绕过过滤 |

**根因**：子串匹配对短期刊名（如"社会科学""国际金融"）没有长度约束，任何包含这些词的期刊都会被误判。

**✅ 已修复（2026.8.7 实测）**：`cssci_journals.py` 的 `is_cssci()` 已改为**严格匹配**——①精确命中名单 → ②别名映射 `_ALIASES`（如"中国人口资源与环境"→"中国人口·资源与环境"）→ ③归一化匹配（去括号全角/半角变体、去标点空格，构建 `_NORM_JOURNALS` 集合）。**彻底移除了 `name in j or j in name` 子串模糊匹配**。修复后实测：`国际金融`→❌、`重庆交通大学学报（社会科学版）`→❌、`江西师范大学学报（哲学社会科学版）`→❌、`中国人口资源与环境`→✅（变体归一化仍能识别）、`经济研究`→✅。

**⚠️ 名单不全的保守策略**：177本名单是精选（经管/环境/综合社科/部分高校学报），**不在名单的高校学报会被严格模式拒绝**（如江西师范大学学报社科版）。宁可漏收不可错收——少帅确认某刊是CSSCI后可手动补进 `cssci_journals.py`。**每次新下载后仍必须抽查验证期刊**（脚本过滤防不了名单外的漏网），不能只靠脚本。

**验证抽查流程**：
```python
# 批量检查新下载PDF的期刊
python check_new10.py  # 对比 PDF首页+CSSCI名单
# 或手动：
# 1. 用 fitz 渲染首页 → vision_analyze 看期刊名
# 2. 检查是否在 CSSCI_JOURNALS 精确命中（不允许子串）
```

### 步骤4：限速下载（写死的规则，不可绕过）

```
⏱️ 下载节流（硬约束，写进脚本，任何情况不违反）：
   - 每篇下载间隔 ≥ 3 秒（RateLimiter.wait()）
   - 1 分钟最多 20 篇
   - 3 分钟最多 50 篇
   - 每 5 篇下载后额外休息 10 秒（防触发限流）
   - 下载超时：等待 60 秒后重试 1 次
```

**Playwright 下载核心**：

```python
# 每行结果内找下载按钮（PDF）
dl_btn = row.locator("a.downloadlink").first
with page.expect_download(timeout=30000) as dl_info:
    dl_btn.click()
download = dl_info.value
if download.suggested_filename.endswith(".pdf"):
    download.save_as(os.path.join(output_dir, download.suggested_filename))
```

- 按钮 `a.downloadlink` 的 href 带 `file-type=pdf`（CAJ 是 file-type=caj，跳过）
- **按钮可能显示"未登录"（icon-notlogged 类），但点击实际能下载**（2026.8.6 验证）
- 已下载文件去重：`existing_files = set(os.listdir(output_dir))`，同名跳过（断点续传）

### 步骤5：文献清单（GB/T 7714-2015 顺序编码制）

```python
# 从PDF首页提取元数据（PyPDF2）或从文件名解析
# 文件名格式: "标题-作者1作者2.pdf"
title, authors = fname.rsplit("-", 1)
# GB/T 7714: 作者. 题名[J]. 刊名, 年, 卷(期): 页码.
entry = f"{authors}. {title}[J]. {journal}, {year}."
```

- 清单写入文献库目录 `文献清单_GB7714.md`
- 结构：编号列表 + 按序编码引用段 `[1] 作者. 题名[J]...`
- 期刊/年份从PDF首页元数据核对（`extract_meta.py` 辅助）
- ⚠️ **标题前缀匹配（2026.8.6 实测修复）**：知网文件名标题常含副标题（如 `碳交易与企业数字创新——基于全国碳交易市场启动的准自然实验`），用 `JOURNAL_YEAR.get(title)` 精确匹配必然落空 → 必须双向 `startswith` 前缀匹配：`title.startswith(key) or key.startswith(title)`。否则清单出现"未知期刊"（实测4篇落空）。`gen_list.py` 已内置此逻辑。

### 步骤6：领域学者名单（可选）

- 从已下载文献中统计高频作者（高产）+ 交叉引用（高被引）
- 输出：学者名 + 所属机构 + 代表文献

## 选文标准（少帅定义，2026.8.6）

1. **级别门槛**：全部为 CSSCI（含扩展版）及以上
2. **级别配比**：顶刊+一区论文占比 ≥ 50%（如《经济研究》《管理世界》、SCI Q1等）
3. **时效配比**：近5年（2021-2026）文献占比 ≥ 50%
4. **经典兜底**：超过5年的必须是经典文献（一区以上或高被引）
5. **相关度**：主题相关（碳交易机制/市场设计）+ 方法相关（ABM/仿真/计量评估）优先

## 入库铁律（2026.8.6 写死，2026.8.7 升级，任何情况不违反）

**入库门槛（少帅2026-08-07指令，写死）**：文献写入文献库（PDF目录/主矩阵库/GB/T 7714清单）前，必须满足以下任一条件：
1. **CSSCI来源期刊**（经 `is_cssci()` 严格校验，177本名单精确/归一化匹配）
2. **SCI/SSCI**（英文文献，凭PDF首页期刊名+数据库确认）
3. **少帅本人论文**（作者含"冯泽宇"豁免，无论期刊级别，标注"本人论文"）

**未验证不入库**：期刊名称必须通过以下至少一种方式验证：
1. **PDF首页/页眉明确显示**：期刊名+卷期号在PDF可见文字中直接出现（如"《生态经济》第32卷第11期"）
2. **DOI反查**：PDF内嵌DOI可查证期刊归属（如ISSN 1674-6252 = 中国环境管理）
3. **CSSCI名单精确匹配**：期刊名在 `cssci_journals.py` 的177本名单中精确命中

**禁止入库的情况**：
- 凭正文关键词猜测（如正文出现"改革"不代表期刊是《改革》）
- 编码乱码推测（GBK乱码不可作为验证依据）
- 新闻稿/报纸文章/非学术论文（如"双碳聚焦"栏目文章，雷英杰2026.8.7案例）
- 期刊名"未知"或未通过 `is_cssci()` 校验的（matrix_ingest.py 已写死校验，未知期刊一律拒绝入库）
- 未验证的文献只能放在 `_非CSSCI待清理/` 或待验证区，不写入主矩阵

**PDF页码坐标提取法（2026.8.7 实战突破，申报书参考文献核实核心）⭐⭐**：

中文期刊PDF的页码格式多样，逐条提取技巧（配合 GB/T 7714 清单生成）：

```python
import fitz, re
doc = fitz.open(pdf_path)
# 1. 首页文本找刊名/卷期/年份："第X卷第X期"、"202X年X月"
p1 = doc[0].get_text()
# 2. 页码：按坐标取页面底部70px内的数字token（页脚页码）
for i in range(doc.page_count):
    page = doc[i]
    h = page.rect.height
    words = page.get_text("words")  # (x0,y0,x1,y1,word,...)
    bottom = [w[4] for w in words if w[1] > h - 70 and re.fullmatch(r"[0-9０-９]{1,4}", w[4])]
# 3. "引用本文"/"引用格式"行（部分期刊首页自带规范引用，最可靠）
```

**页码格式大全（血泪汇总）**：
- `·N·`（生态经济等）、`-- N` / `— — N`（上海大学学报等）、全角数字、页眉页脚混合
- **反序页码**：左右分列数字按"个位 十位 百位"排列——如 `７ １ １` = 117（西南民族大学学报），逐页 +1 验证
- **文章编号解析**：`1004-8308（2024）01-0040-13` = 期01、起始页0040、13页 → 页码 40-52
- 递增序列（120,121,...,135）→ 页码范围 = min-max；PDF 页数=页码范围差+1 可交叉验证
- 无卷号期刊（科技管理研究/重庆社会科学）→ 只标 年(期): 页码；增刊/合刊 → "年, 卷(增刊): 页码"
- 卷号合理性：按创刊年推算（科技管理研究1981创刊→2024年44卷；南开管理评论1998→2024年27卷）
- **±1页码争议裁决**：以 PDF 页码序列（谁有连续序列证据）为准

**铁律**：页码必须从 PDF/知网题录获取，**禁止 AI 凭记忆/推测补写**（2026.8.7 教训：某队友"补全"的 18 篇中文文献页码 16 篇编造，如曹辰实为165-173 被写成 1-12）。

## 三层保障机制：如何确保规则每次都被执行

用户曾问"你如何确保你每次都会遵循这个规则呢"——AI每次会话都是全新状态，靠"记得"不可靠。真正的保障是把规则写进**持久化的文件/代码**，不依赖模型自觉：

| 层级 | 载体 | 可靠性 | 说明 |
|------|------|--------|------|
| **代码层** | `matrix_ingest.py` 入库铁律 | ★★★ | 入库前强制 `is_cssci()` 校验，非CSSCI/未知期刊直接拒绝，模型没有机会跳过 |
| **技能层** | `cnki-paper-download/SKILL.md` | ★★☆ | 每次触发技能时加载规则，模型读到后执行 |
| **调度层** | cron prompt（72bf13a254cb） | ★★☆ | 每日01:00自动执行，prompt写死只准CSSCI，--max 10 |

**核心原则**：代码强制 > 技能提醒 > 记忆依赖。如果只靠LLM记得遵守，早晚会出错（2026.8.7 就出过一次：旧is_cssci子串匹配bug导致非CSSCI混入，是代码层bug不是模型遗忘）。修复代码（严格匹配+变体归一化）才是根本解。

**乱码PDF的期刊验证法（2026.8.7 实战突破）⭐⭐**：

PyPDF2/PdfReader 提取乱码（GBK编码错乱）时，**不能放弃也不能猜**，用 PyMuPDF 渲染首页+视觉识别：

```python
import fitz  # PyMuPDF: pip install pymupdf
doc = fitz.open(pdf_path)
page = doc[0]  # 首页
pix = page.get_pixmap(dpi=150)
pix.save(f"{TEMP}\\p1.png")
# 然后 vision_analyze 看图片：提示"这是学术论文PDF首页，页眉期刊名是什么？"
```

**实战效果（2026.8.7）**：
- 涂正革《排污权交易机制…波特效应？》PyPDF2全乱码 → 渲染首页 → vision识别 **《经济研究》第50卷第4期2015**（此前误判为《改革》，因为正文有"新改革"字样——**正是"凭正文关键词猜测"的陷阱实例**）
- 吴文娟郭树龙SO2双倍差分 → vision识别 **《上海经济研究》**
- **⚠️ 视觉模型可能识别错误**：常杪那篇 vision 报"中国环境管理"，但页内 DOI `10.14026/j.cnki.0253-9705` 的 ISSN 0253-9705 实为《环境保护》——**必须同时核验DOI/ISSN**，视觉结果与DOI冲突时以DOI为准
- 多页交叉验证：乱码页眉的页面（第2/4页）也渲染出来再问一次，增强置信度

## 交付物与目录

```
ObsidianVault\academia\文献库\<主题>\
├── <标题>-<作者>.pdf        # 下载的论文（命名: 标题-作者）
├── 文献清单_GB7714.md        # GB/T 7714 引用清单
└── _download_record.json    # 下载记录（含限速参数、错误列表）
```

## 常用脚本（hermes-data/scripts/）

| 脚本 | 功能 |
|------|------|
| `cnki_search.py` / `cnki_search_v2.py` | requests 调 brief/grid 检索（分析用）|
| `pw_login_full.py` | Playwright 登录+保存cookie |
| `pw_search2.py` | Playwright 检索+提取结果（带cookie复用）|
| `pw_download.py` | ⭐ 批量下载 v3（CSSCI过滤+限速+断点续传+防限流+重试+额度自动停止+`--max`参数）|
| `cssci_journals.py` | CSSCI期刊名单 + is_cssci() 判断 |
| `gen_list.py` | 生成 GB/T 7714 清单 |
| `extract_meta.py` | 提取PDF首页元数据 |
| `diag_page.py` | 诊断镜像页状态（额度/登录）|

## 常见陷阱

### 陷阱0：登录页表单字段ID与name完全相反（2026.8.6实测确认）⭐⭐⭐

**问题**：文献云登录页 `/e/member/login/` 的表单字段**id和name是反的**：
- `input id="password" name="username"` ← 这是**用户名输入框**（id叫password！）
- `input id="username" name="password"` ← 这是**密码输入框**（id叫username！）
- `input id="code"` ← 验证码（这个正确）

如果用 `#user_name`（不存在）或按id直觉填反了，必然登录失败或超时。

**根因**：文献云网站前端表单字段命名错误（id和name颠倒），不是Hermes的问题。

**修复**：登录脚本必须用**正确的id映射 + 正确的提交按钮**：
```python
page.goto("http://www.wxy88.top/e/member/login/", timeout=45000, wait_until="domcontentloaded")
time.sleep(5)
page.fill("#password", USERNAME)  # 用户名框（id叫password，name才叫username）
page.fill("#username", PASSWORD)  # 密码框（id叫username，name才叫password）
# ⚠️ 提交按钮是 input[name=Submit]，#ok 不存在！
page.click("input[name=Submit]")
```

**附加发现**：
1. 首页 `wxy88.top/` **没有登录表单**（登录入口在 `/e/member/login/`），直接在首页找 `#user_name` 会超时
2. `pw_login_full.py`（旧脚本）用 `#user_name` + `#password` + `#ok` 定位是**全错的**（id字段不存在、按钮也不存在），`pw_login_v4.py` 已全部修正
3. 验证码图片在登录页 `img[src*='ShowKey']`，需先截图 → vision_analyze 识别 → 再填表

**完整正确流程**：
```
1. goto('/e/member/login/') → 检查 #code 是否存在（首次通常无验证码，见陷阱0b）
2. fill("#password",用户名) → fill("#username",密码) → 若有验证码则 fill("#code",验证码)
3. click("input[name=Submit]")  ← 不是 #ok！
4. 验证: goto('ShowInfo.php?classid=62&id=1077') → goto('cnkipdf.php') → 确认"您未登录"不出现
5. 保存: context.cookies() → JSON → TEMP/pw_cookies.json
```

### 陷阱0b：首次登录通常无验证码（2026.8.6 实测）⭐⭐

登录页 `/e/member/login/` **首次访问没有验证码**（截图确认表单区只有用户名/密码/登录按钮，无验证码图）——验证码**只在登录失败后才出现**（防爆破）。

**处理**：填表前先 `page.locator("#code").count() > 0` 判断，有才走截图识别流程；没有直接填用户名密码提交。旧流程"必须先截图验证码"会因元素不存在而卡死。

### 陷阱0c：每日限额可换镜像入口绕过（2026.8.6 实测突破）⭐⭐⭐

**知网2入口（id=1077，pdf.ccki.top）额度用尽 ≠ 平台不可用！** 文献云有**多个知网镜像入口，每个入口独立额度**：

| 入口 | id | 跳转域名 | 状态(2026.8.6) |
|------|----|---------|--------------|
| 知网33 | 1076 | - | 额度尽 |
| 知网2 | 1077 | pdf.ccki.top | 额度尽 |
| 知网4 | 1084 | - | 额度尽 |
| 知网5 | 1086 | - | 额度尽 |
| 知网6 | 1087 | - | 额度尽 |
| **知网10** | **1132** | **180.76.181.155:9188** | ✅ 可用（68个input）|
| **知网12** | **1765** | **180.76.102.59:9299** | ✅ 可用（68个input）|

**流程**：`/e/action/ListInfo/?classid=62` 列出入口 → 逐个测试 ShowInfo.php?id=X 跳转后是否有 input 框 → 可用入口做检索/查询。**下载额度尽的入口，查询页面也会被"下载次数已用尽"拦截**（连搜索框都没有），但换入口即可。

**⚠️ 注意**：即使入口跳转成功，也可能显示"您未登录，请从图书馆入口处重新点击入口进去"——必须走 wxy88.top 的 ShowInfo 页跳转（带 referer+cookie 链），不能直接访问跳转域名。

### 陷阱0d：平台502宕机是瞬时的——cron报"宕机"后要重试验证（2026.8.9 实测）⭐⭐

**症状**：每日01:00 cron 报告"文献云平台全线宕机（wxy88.top / pdf.ccki.top 均 HTTP 502），今日无法下载，新增0篇"。cron 依据规则"连续失败3次停止并汇报异常"直接放弃。

**真相**：平台502是**瞬时故障**——当天晚上 curl 验证 `wxy88.top` 已恢复 HTTP 200、`pdf.ccki.top` 302。cron 在凌晨恰好撞上宕机窗口，但**当天后续时间平台是好的**。

**处理流程（少帅说"今天的下载任务还没完成"时）**：
1. **先 curl 验证平台是否已恢复**（不要信 cron 的"宕机"结论）：
   ```bash
   curl -s -o /dev/null -w "wxy88.top: %{http_code}\n" --max-time 15 "http://www.wxy88.top/"
   curl -s -o /dev/null -w "pdf.ccki.top: %{http_code}\n" --max-time 15 "https://pdf.ccki.top/"
   ```
   200/302 = 已恢复，可补跑；仍5xx = 真宕机，等明天。
2. **cookie 已过期（8.7后未登录）→ 重新登录**：`python pw_login_v4.py`——首次登录通常无验证码（陷阱0b），直登成功打印"cookies: 5个, 认证cookie: True"；末尾"验证步骤异常: Page.goto Timeout"是页面加载慢，**不影响登录成功**，忽略。
3. **补跑下载**：`python pw_download.py --max 10`（后台跑，`terminal(background=true, notify_on_complete=true)`，单篇下载超时30s+重试60s，10篇全流程可能5-10分钟）。
4. **TEMP路径**：登录/下载脚本都读 `os.environ["TEMP"]`——bash 里 `TEMP=/tmp` 但 MSYS 会把 `/tmp` 映射到 `C:\Users\<user>\AppData\Local\Temp`，**两者是同一个物理路径**，cookie 能找到，无需改脚本。

### 陷阱0e：下载报"0/10 新增"≠ 失败——搜索词已耗尽（2026.8.9 实测）⭐⭐

**症状**：重新登录+补跑后，`pw_download.py --max 10` 输出 `✅ 下载完成: 0/10 篇`，日志全是"⏭️ 已下载过，跳过"+"⏭️ 非CSSCI跳过"。第二关键词直接报"⚠️ 每日额度已用尽！停止本次下载"。

**真相**：这不是故障，是**当前搜索词（碳排放权交易/碳交易）下的CSSCI文献已基本下完**——34篇存量覆盖了搜索词的全部CSSCI论文，断点续传全部识别跳过；非CSSCI也被过滤。**"每日额度已用尽"是脚本逻辑触发的停止条件，不是平台额度真尽**（当天还能访问）。

**处理**：
- 0/10 新增 + 全是跳过 = 换**新搜索词**（如"碳市场""碳排放权""绿色金融"）扩大覆盖面，而不是重跑同词
- 2篇下载超时失败的（如科技管理研究/科学学与科学技术管理）可单独重试（加长超时）
- 向少帅汇报时明确："今日新增0篇，原因=存量已覆盖搜索词，需换词或暂停"——不要含糊带过

### 陷阱0f：切换镜像入口必须保留 cnkipdf.php 中转（2026.8.9 实测，Codex委托踩坑）⭐⭐

**症状**：把 `pw_download.py` 改成知网10入口（ShowInfo.php?id=1132 → 直接 goto 180.76.181.155:9188）后，运行报"❌ 未登录！需要重新登录"——即使 cookie 有效（主站5个cookie正常）。

**根因**：镜像入口跳转必须经过 `cnkipdf.php` 中转（带Referer链），**不能直接从 ShowInfo 页跳到镜像域名**。原脚本是 `ShowInfo.php?id=1077 → cnkipdf.php → pdf.ccki.top` 三步。改成知网10时若把中间 `cnkipdf.php` 一步漏掉，镜像不认主站cookie → 未登录。

**✅ 正确跳转链（任何入口都适用）**：
```python
page.goto("http://www.wxy88.top/e/action/ShowInfo.php?classid=62&id=1132", ...)  # 入口页(改id)
time.sleep(2)
page.goto("http://www.wxy88.top/cnkipdf.php", ...)   # ← 必须保留的中转！带Referer
time.sleep(3)
page.goto("http://180.76.181.155:9188/kns8s/defaultresult/index", ...)  # 镜像检索页(改域名)
```
会话建立后检索页刷新可直接 goto 镜像域名，无需再走中转。

**⚠️ 委托其他agent（Codex/太尉）改此脚本的教训**：agent 会"聪明地"把中间中转步骤当作冗余省略，导致未登录。**收到改好的脚本必须核对：①入口ShowInfo id ②cnkipdf.php 中转保留 ③镜像域名正确**，三处缺一不可。

### 陷阱0g：matrix_ingest 期刊映射缺失导致"未知期刊"拒绝入库（2026.8.9 实测）⭐⭐

**症状**：新下载的5篇PDF（经济研究/中国管理科学/中国软科学/经济管理/吉林大学社会科学学报——全是CSSCI）跑 `matrix_ingest.py` 全部报 `⛔ 拒绝入库（非CSSCI或期刊未验证）: [期刊=未知期刊]`。但用 `cssci_journals.py` 的 `is_cssci()` 抽查这些期刊名明明都返回CSSCI✅。

**根因**：`matrix_ingest.py` 的期刊识别**不直接用 is_cssci 的名单**，而是先查内置硬编码映射 `KNOWN_JOURNALS`（标题前缀→期刊名）。新下载的标题不在映射表里 → 期刊解析为"未知期刊" → 下一步 is_cssci("未知期刊") 校验失败拒绝。**是映射表缺失，不是期刊非CSSCI**。

**处理**：把新下载文献的 `标题前缀: (期刊, 年, 卷期)` 补进 `matrix_ingest.py` 的 `KNOWN_JOURNALS` 字典（期刊名从 pw_download 的"CSSCI确认"日志取），再重跑入库。补前先 `--dry-run` 确认"新增X篇"且不再报"未知期刊"。已补映射后重跑即重新识别并入库。

### 陷阱0h：跨天额度≠立即重置——凌晨cron撞上"额度延续"（2026.8.9-10 实测，少帅批评事件）⭐⭐

**症状**：8/9深夜23:33下载5篇后，8/10凌晨01:27 cron自动运行，登录后页面显示"您今天的下载次数已用尽"——**新的一天额度没"满血"**。少帅8/10问"今天才开始怎么就没额度"，一度误以为丞相没干活。

**根因**：文献云账号额度是**账号全局限制**（约18-20篇/天），且**额度用尽状态跨天不立即清零**（按24h滚动窗口或延迟重置）。凌晨01:00 cron最容易撞上"昨日已尽"窗口——登录+探测+搜索这些操作**本身也消耗额度**，cron空跑一轮反而把当天额度进一步耗掉。

**处理规范**：
1. **cron/代跑先探测额度再干活**：登录后先看页面文本（"您今天的下载次数已用尽"→直接停，不跑搜索/下载），`diag_page.py` 可用
2. **cron撞墙后白天主动补一次**：01:00 cron报"额度尽"后，丞相当天稍晚（上午/下午）应主动重试——额度可能已重置（8/9就是深夜23:33才下成功的）
3. **汇报优先讲成果**：先报"已累计X篇+昨日新增Y篇"，再解释今日额度状态，**不要把"额度用尽"当标题**（少帅2026.8.10明确不满："你都没有帮助我下载一篇论文"——实际已下5篇，是汇报顺序误导了他）
4. **跨天边界主动检查**：零点过后主动验证额度是否重置、是否可续跑，不要等少帅来问

### 陷阱1：验证码需与登录同session
每次 `s.get("/e/ShowKey/")` 生成的验证码绑定当前session，换session必失败。Playwright 方式则是先截图验证码元素 → vision_analyze → 填表。

### 陷阱2：镜像站"未登录"提示
直接访问 pdf.ccki.top 显示"您未登录"——必须从 wxy88.top 的入口页 → cnkipdf.php 跳转，带 Referer。

### 陷阱3：登录后确认
登录响应是JS倒计时跳转页（3秒），无明确"成功"字样。判断标准是 Set-Cookie 中是否有 ujgpvmluserid 和 ujgpvmlauth。

### 陷阱4：vision_analyze 识别验证码
提示词加"只输出验证码中的字符，注意字母都是小写"。识别失败重新拉取（验证码每次刷新）。

### 陷阱5：每日限额（最坑）⭐
见上方"每日限额"章节。**搜索框找不到 ≠ 技术故障，先检查额度**。用 `diag_page.py` 诊断页面文本。

### 陷阱6：下载按钮"未登录"但能下载
`a.downloadlink` 带 `icon-notlogged` 类/title="未登录"是误导，点击实际能下载成功（2026.8.6 验证）。

### 陷阱7：requests 调 brief/grid 易失败
即使参数正确也可能"检索模型参数错误"或"您未登录"。原因：cookie 会话与镜像站校验不一致 + 可能有 AES 签名（vv 参数）。**下载一律走 Playwright 浏览器点击**。

### 陷阱8：连续快速点击触发限流
不等待直接连点下载按钮 → 后续点击全部超时（20秒无响应）。必须固定3秒间隔 + 每5篇休息10秒。

### 陷阱9：360安全卫士锁文件
Playwright 安装浏览器时 360 会导致 `EPERM` 解压失败（D3DCompiler_47.dll 被锁）。**先退出360再装**。下载运行期间360也可能拦截。

## 验证

- 登录成功：cookies 含 ujgpvmluserid/ujgpvmlauth
- 镜像可检索：访问 cnkipdf.php 后能加载检索界面（非"未登录"提示）
- CSSCI过滤：日志中非CSSCI行显示"⏭️ 非CSSCI跳过"
- 下载完整：文件存在且大小>10KB，数量与清单一致
- 限速合规：日志中时间戳间隔≥3秒
- PDF有效：文件头 `%PDF`（1MB+ 正常）

## 交付语言与自动化产出处理 ⭐

**翻译技术内容为白话（2026.8.7 少帅纠正）**：回复用户时先用大白话解释结论，技术细节作为补充。少帅是学术研究者不是程序员，优先用人话+比喻（如用"安检机"比喻三层保障机制），避免连续大段英文技术描述。

**自动化工具产出必须解释（2026.8.7 少帅纠正）**：cron/脚本/监控产出的报告，不能一句话"无需操作"带过。必须提取关键发现、解释价值、说明是否需要用户决策。即使是"正常"状态也要说清楚发现了什么。

## 定时自动下载（每日cron工作流，2026.8.6 创建，2026.8.7 更新）⭐

少帅要求**每天自动下载10篇，直到喊"暂停"为止**。已创建 cron job：

- **任务名**：`每日CSSCI文献自动下载`（job_id: `72bf13a254cb`）
- **调度**：每天 **01:00**（`0 1 * * *`），无限重复——⚠️ **凌晨1点是少帅指定**（该时段API最便宜），不要改回10:00（曾误改被纠正）
- **下载量**：`pw_download.py --max 10`——⚠️ **从18改到10是少帅指定**（预留8篇额度给手动下载补充文献），不要改回18
- **⚠️ 批次计数区分**：cron每次运行是一批（本次10篇），之前累积的存量（如昨天18篇）是另一批。汇报时**明确标注"本次下载X篇"+"累计Y篇"**，不要混为一谈——2026.8.7 少帅纠正过一次（我说"18篇全部达标"实际是指存量而非本次新下载的10篇）
- **工作流**：diag_page.py 检查登录/额度 → 未登录则走验证码流程重新登录 → `pw_download.py --max 10` → 验证PDF + 重新生成GB/T 7714清单 → 向少帅汇报
- **关键设计**：cron 是 LLM 驱动（非纯脚本），因为登录可能需要 vision_analyze 识别验证码；enabled_toolsets 限定为 terminal+file+vision
- **停止方法**：少帅喊"暂停"→ `cronjob action=list` 找到 `72bf13a254cb` → `cronjob action=remove`（或 pause）
- **每日限额交互**：若当天额度已用尽（diag_page 显示"请明天再来"），cron 直接结束并汇报，不硬撑
- 完整 prompt 与重建指引：`references/daily_cron_job.md`

## 文献矩阵库（下载后下一步）⭐ 2026.8.6 完整工作流

下载文献→生成引用清单→**下一步是创建文献矩阵库**（研究方法/结论/期刊级别/主题分类），为文献综述做铺垫。完整工作流见 `obsidian-literature-matrix` 技能。实操案例：18篇碳交易CSSCI文献→`市场化环境治理研究文献矩阵库.md`（27篇：碳18+排污9，含"子方向"列+SSCI英文文献2篇）。排污权文献来自 D 盘毕业论文/考博资料目录（`排污权正在写\参考文献\`、`排污权抵押贷款\`等），非CSSCI文献按少帅规则不入库。

**矩阵库→基金申报综述补充**（2026.8.7 新增）：少帅有自科基金申报综述（`碳排放权交易文献综述_ABM方法论_改进版.md`，参考文献曾全英文无中文），用矩阵库已入库文献按 GB/T 7714 追加+正文插入引用+更新数据完整性声明。完整流程、筛选原则、验证清单、cross_model_verify 降级链见 `references/review_supplement_workflow.md`。⚠️ 少帅有两个基金材料（碳排放ABM综述 vs 交通出行权交易申报书），动手前先读文件确认目标。

**跨机制文献借鉴**（2026.8.7 少帅纠正）：碳交易综述补充时不要只看碳交易子方向——排污权交易12篇文献中的制度设计/定价/波特效应检验/法律制度等研究方法和结论，可直接迁移到碳交易综述（二者都是"污染品交易权"）。筛选综述补充文献时，**先跨子方向找已有文献的可迁移价值，再决定是否需要新检索**，避免重复劳动。

### 首次创建矩阵库

1. **提取PDF关键内容**：`scripts/extract_pdf_matrix.py` → 输出 `_matrix_extract.json`（摘要+方法+结论）
2. **生成矩阵库**：`scripts/gen_matrix.py` → 输出 `碳交易研究文献矩阵库.md`（主矩阵+主题分类+期刊级别+GB/T 7714+方法统计）
3. **补充标题列**：gen_matrix.py 输出默认无标题列，需用Python脚本从 titles dict 补充到主矩阵表的第4列（`[新增] 2026.8.6 补标题列的逻辑在 plan 会话中手工完成`）

### 增量自动入库（每日cron流程）⭐ 核心新增

下载完成后自动将新文献接入矩阵库（不再手动操作）：

```
pw_download.py --max 18  →  下载新文献到文献库目录
      ↓
matrix_ingest.py          →  自动增量入库（核心脚本）
      ↓
向少帅汇报新增X篇+累计Y篇+主题分布
```

**matrix_ingest.py 用法**：
- `python matrix_ingest.py` — 增量入库（只处理新增）
- `python matrix_ingest.py --init` — 首次部署：将当前所有PDF标记为已入库（不追加）
- `python matrix_ingest.py --dry-run` — 仅扫描预览，不写入

**关键机制**：
- **去重权威**：`_matrix_ingested.json` 记录已入库PDF文件名（**唯一去重依据，不靠标题匹配**）
- **首次自动检测**：脚本检测矩阵库已有内容但状态文件为空 → 自动标记全部PDF为已入库，不重复追加
- **入库动作**：提取PDF→关键词规则自动分类主题→追加主矩阵→更新分类索引→更新GB/T 7714引用→更新文献清单

**⚠️ 已知限制（2026.8.6 实测）**：
- `gen_matrix.py` 输出的矩阵库默认**无标题列**（标题在 titles dict 中但未写入表格），需额外补标题列脚本
- `matrix_ingest.py` 的期刊识别依赖内置映射表 `KNOWN_JOURNALS`（前18篇硬编码），新增文献未命中时标注"未知期刊"（需后续补充）
- 主题分类用关键词规则，分类不准时标"待人工确认"，cron LLM可补充

### cron集成prompt模板

在每日CSSCI下载cron（72bf13a254cb）的prompt中，第4步后追加入库步骤：

```
### 4. 自动入库文献矩阵库
下载完成后，运行入库脚本：
python "D:/BaiduSyncdisk/AIKnowledgeBase/Hermesagent/hermes-data/scripts/matrix_ingest.py"
- 正常输出"无新增文献"或"自动标记X篇为已入库"→属正常（额度用尽或首次同步）
- 若报错→用 read_file 查看 _matrix_ingested.json 和矩阵库文件确认状态
```

### ⚠️ 陷阱：标题匹配去重不可靠

**2026.8.6 实测踩坑**：最初用矩阵库主矩阵中的标题列做 `startswith` 匹配去重，但PDF文件名与矩阵库标题有**标点差异**（下划线`_` vs 破折号`——`），导致 `近朱者赤_被纳入` 与 `近朱者赤——被纳入` 无法匹配，误判为"新增"重复入库。

**正确设计**：去重必须依赖 `_matrix_ingested.json` 状态文件（记录已入库的完整文件名），而非矩阵库中的标题文本。状态文件是唯一权威，标题匹配仅作辅助。

## 实操记录（2026.8.6 第一次执行）

## 实操记录（2026.8.6 第一次执行）

- 检索词：碳排放权交易/碳交易/碳市场/碳配额/碳价/碳排放交易/排污权交易/碳交易政策/碳中和/碳排放权（多词并集）
- 每词第一页20条满载 → CSSCI占比约55%（11/20）
- 实际下载：18篇有效CSSCI PDF → 触发每日限额
- 输出目录：`ObsidianVault\academia\文献库\碳排放权交易\`
- 清单：`文献清单_GB7714.md`（18篇）
- 教训：额度有限，**优先下载高级别期刊**（经济研究/管理世界/中国工业经济等顶刊），避免浪费额度在普通CSSCI上
