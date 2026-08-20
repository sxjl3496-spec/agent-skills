#!/usr/bin/env python3
"""
文献自动入库脚本 - 将文献目录中的PDF自动增量接入碳交易研究文献矩阵库

功能：
1. 扫描文献目录中的PDF，与已入库记录(_matrix_ingested.json)比对，找出新增文献
2. 提取新增PDF的标题/作者/期刊/年份 + 摘要/研究方法/核心结论
3. 按关键词规则自动分类研究主题
4. 追加到《碳交易研究文献矩阵库.md》（主矩阵 + 主题分类索引 + GB/T 7714引用）
5. 更新《文献清单_GB7714.md》
6. 记录已入库文件，下次运行时增量去重

用法：
  python matrix_ingest.py            # 正常入库
  python matrix_ingest.py --dry-run  # 仅扫描预览，不写入
"""
import os, re, json, sys, warnings
from datetime import datetime

warnings.filterwarnings("ignore")

DIR = r"D:\BaiduSyncdisk\AIKnowledgeBase\ObsidianVault\academia\文献库\碳排放权交易"
MATRIX_PATH = os.path.join(DIR, "碳交易研究文献矩阵库.md")
LIST_PATH = os.path.join(DIR, "文献清单_GB7714.md")
STATE_PATH = os.path.join(DIR, "_matrix_ingested.json")

# 期刊级别表（已知的CSSCI期刊统一标注，可扩展）
TOP_JOURNALS = {"南开管理评论", "管理世界", "经济研究", "中国工业经济"}
CSSCI_EXPANDED = set()  # 扩展版名单暂空

# 已知期刊映射（标题前缀 -> (期刊, 年份, 卷期)）
# 来源于 gen_list.py 人工核对结果；新增文献未命中时标注"未知期刊"
KNOWN_JOURNALS = {
    "“双碳”目标下碳排放权交易的减排效应与作用机制": ("生态经济", "2025", "41(10)"),
    "“双碳”背景下碳排放权交易行政监管的体制构建与机制创新": ("华中农业大学学报（社会科学版）", "2026", "(2)"),
    "中国碳市场一体化的动态测度与阻碍因素研究": ("运筹与管理", "2026", "35(2)"),
    "国内外碳市场与原油期货市场、股票市场的时频联动分析": ("系统工程理论与实践", "2025", "37(12)"),
    "基于《中华人民共和国生态环境法典》的碳交易市场规范续造": ("中国人口·资源与环境", "2025", ""),
    "市场激励型环境政策促进城市绿色创新的": ("重庆社会科学", "2025", "(10)"),
    "新质生产力视域下碳排放权交易对绿色高质量发展的影响研究": ("科技管理研究", "2024", "44(14)"),
    "碳交易、碳排放权配额与绿色转型风险": ("南开管理评论", "2024", ""),
    "碳交易与企业数字创新": ("财经研究", "2025", "51(12)"),
    "碳交易市场对农业绿色低碳发展的影响机理与协同增效路径": ("资源科学", "2025", "47(12)"),
    "碳交易税务处理与会计处理差异问题研析": ("税务研究", "2025", "(12)"),
    "碳排放权交易中行政处罚的适用困境及其纾解": ("社会科学家", "2025", "(5)"),
    "碳排放权交易如何影响企业全要素生产率": ("管理评论", "2025", "37(2)"),
    "碳排放权交易政策能够提升企业ESG表现吗": ("科学学与科学技术管理", "2024", "45(10)"),
    "碳排放权交易监管手段的优化与阶梯式构建": ("环境保护", "2024", "增刊5"),
    "碳排放权交易驱动城市绿色高质量发展的影响研究": ("西南民族大学学报（人文社会科学版）", "2025", "(5)"),
    "策略性回应还是实质性响应": ("南开管理评论", "2024", "27(3)"),
    "近朱者赤": ("研究与发展管理", "2024", "36(1)"),
}


def norm_title(t):
    """规范化标题用于匹配：统一标点（下划线/破折号/空格/书名号）"""
    t = t.replace("_", "").replace("——", "").replace("—", "").replace(" ", "")
    t = t.replace("《", "").replace("》", "").replace("？", "").replace("？", "")
    t = t.replace("“", "").replace("”", "")
    return t


def lookup_journal(title):
    """从已知映射查期刊，前缀匹配"""
    for key, val in KNOWN_JOURNALS.items():
        if title.startswith(key) or key.startswith(title):
            return val
    return ("未知期刊", "未知", "")

# 主题分类关键词规则（按命中数取最高）
TOPIC_RULES = {
    "减排效应与政策评估": ["减排效应", "减排效果", "碳减排", "政策评估", "政策效应", "试点政策", "减污降碳", "排放效应"],
    "企业行为与创新/ESG": ["企业", "创新", "ESG", "全要素生产率", "TFP", "数字创新", "绿色创新", "上市公司", "企业价值", "经营决策"],
    "市场机制与碳金融": ["市场一体化", "时频联动", "小波", "Granger", "碳价", "价格", "联动", "一体化", "风险溢出", "DSGE", "配额", "碳金融", "市场机制"],
    "绿色高质量发展": ["绿色高质量", "新质生产力", "高质量发展", "农业绿色", "绿色低碳发展", "绿色转型"],
    "法律与政策监管": ["行政监管", "监管", "行政处罚", "法律", "法规", "法典", "法治", "立法", "监管手段", "体制构建"],
    "金融财税": ["税务", "会计", "企业所得税", "增值税", "税收", "财税"],
}


def parse_filename(fname):
    """从文件名提取标题和作者：'标题-作者1作者2'"""
    name = fname.replace(".pdf", "")
    parts = name.rsplit("-", 1)
    if len(parts) == 2 and parts[1].strip():
        return parts[0].strip(), parts[1].strip()
    return name, ""


def extract_pdf_text(path):
    """提取PDF全文（页列表）"""
    from PyPDF2 import PdfReader
    reader = PdfReader(path)
    return [p.extract_text() or "" for p in reader.pages]


def find_section(pages, keywords, max_len=2000):
    for page in pages:
        for kw in keywords:
            idx = page.find(kw)
            if idx >= 0:
                start = max(0, idx - 30)
                return page[start:start + max_len]
    return ""


def extract_meta(fname, path):
    """提取单篇文献的元数据+摘要+方法+结论"""
    pages = extract_pdf_text(path)
    first = pages[0] if pages else ""
    full = "\n".join(pages)

    # 摘要
    abstract = ""
    for kw in ["摘要", "摘 要", "Abstract", "ABSTRACT"]:
        idx = first.find(kw)
        if idx >= 0:
            abstract = first[idx:idx + 1200]
            break
    if not abstract:
        abstract = first[:900]

    # 结论
    conclusion = find_section(pages, ["结论与建议", "研究结论", "结  论", "结论", "四、结论", "五、结论"], 1800)
    if not conclusion:
        conclusion = pages[-1][-1800:] if pages else ""

    # 方法
    method = find_section(pages, ["研究方法", "模型设定", "模型构建", "实证模型", "计量模型"], 1500)
    if not method:
        method = find_section(pages, ["研究设计", "模型与方法", "方法"], 1200)

    return {"file": fname, "abstract": abstract.strip(),
            "method": method.strip(), "conclusion": conclusion.strip()}


def classify_topic(text):
    """按关键词规则分类主题，返回(主题, 命中数)"""
    best_topic, best_score = "待人工确认", 0
    for topic, kws in TOPIC_RULES.items():
        score = sum(1 for kw in kws if kw in text)
        if score > best_score:
            best_topic, best_score = topic, score
    return best_topic, best_score


def parse_meta_from_pdf(pages):
    """尝试从PDF首页提取期刊/年份（识别'文章编号'等模式）"""
    first = pages[0] if pages else ""
    journal, year = "未知期刊", "未知"
    # 年份：找 20xx 模式（收稿/出版年）
    years = re.findall(r"20[12]\d", first)
    if years:
        year = years[0]
    return journal, year


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"ingested": []}


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def build_gbt7714(entry, authors):
    """构建GB/T 7714引用条目：作者. 标题[J]. 期刊, 年, 卷(期)."""
    journal, year = entry.get("journal", "未知期刊"), entry.get("year", "未知")
    vol = entry.get("vol", "")
    vol_part = f", {vol}" if vol else ""
    return f"{authors}. {entry['title']}[J]. {journal}{vol_part}, {year}."


def main():
    dry_run = "--dry-run" in sys.argv
    init_mode = "--init" in sys.argv

    # 1. 扫描PDF，比对已入库
    state = load_state()
    ingested = set(state["ingested"])
    pdfs = sorted([f for f in os.listdir(DIR) if f.endswith(".pdf")])

    # --init 模式：将当前全部PDF标记为已入库（首次部署用，避免重复入库）
    if init_mode:
        state["ingested"] = pdfs
        state["last_ingest"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_state(state)
        print(f"✅ 初始化完成：{len(pdfs)} 篇现有文献已标记为已入库（后续只处理新增）")
        return

    # 首次运行但矩阵库已有内容且状态为空 → 自动全量标记（防重复）
    if not ingested and os.path.exists(MATRIX_PATH):
        with open(MATRIX_PATH, encoding="utf-8") as f:
            mtext = f.read()
        if "## 一、文献主矩阵" in mtext and "| 1 |" in mtext:
            state["ingested"] = pdfs
            state["last_ingest"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_state(state)
            print(f"✅ 检测到矩阵库已有内容且状态为空：自动标记 {len(pdfs)} 篇为已入库，不重复写入")
            return

    # 正常增量：只处理状态文件中没有的
    new_pdfs = [f for f in pdfs if f not in ingested]

    print(f"文献目录共 {len(pdfs)} 篇PDF，已入库 {len(ingested)} 篇，新增 {len(new_pdfs)} 篇")

    if not new_pdfs:
        print("✅ 无新增文献，跳过入库")
        return

    if dry_run:
        print("\n【DRY RUN】将入库以下文献：")
        for f in new_pdfs:
            print(f"  - {f}")
        return

    # 2. 逐个提取+分类
    new_entries = []
    for fname in new_pdfs:
        path = os.path.join(DIR, fname)
        try:
            meta = extract_meta(fname, path)
            title, authors = parse_filename(fname)

            # 期刊识别：优先已知映射，回退PDF文本提取
            journal, year, vol = lookup_journal(title)
            if journal == "未知期刊":
                pages = extract_pdf_text(path)
                j2, y2 = parse_meta_from_pdf(pages)
                if y2 != "未知":
                    year = y2
                journal = j2

            text = meta["abstract"] + meta["conclusion"] + meta["method"]
            topic, score = classify_topic(text)

            entry = {
                "file": fname, "title": title, "authors": authors,
                "journal": journal, "year": year, "vol": vol,
                "method": meta["method"][:80], "conclusion": meta["conclusion"][:80],
                "topic": topic, "topic_score": score,
            }
            new_entries.append(entry)
            print(f"  ✅ 提取: {title[:30]}... 期刊={journal} 主题={topic}(score={score})")
        except Exception as e:
            print(f"  ❌ 提取失败 {fname[:40]}: {str(e)[:60]}")
            new_entries.append({"file": fname, "title": fname, "authors": "",
                                "journal": "未知期刊", "year": "未知", "vol": "",
                                "method": "", "conclusion": "", "topic": "待人工确认", "topic_score": 0})

    if not new_entries:
        print("❌ 无有效新文献可入库")
        return

    # 3. 追加到矩阵库
    with open(MATRIX_PATH, encoding="utf-8") as f:
        matrix = f.read()

    # 在"## 二、主题分类索引"之前插入新行到主矩阵
    # 找到主矩阵表末尾（在"---"和"## 二"之间）
    idx = matrix.find("## 二、主题分类索引")
    if idx == -1:
        print("❌ 矩阵库结构异常：找不到主题分类索引")
        return

    # 构建新矩阵行
    new_rows = []
    for e in new_entries:
        # 提取作者首作者（去掉"等"）
        author_short = e["authors"].split("等")[0][:10] if e["authors"] else "佚名"
        new_rows.append(f"| {e['file'][:15]} | {author_short} | {e['year']} | {e['title'][:25]} | {e['journal'][:10]} | CSSCI来源 | {e['method'][:40]} | {e['conclusion'][:50]} | {e['topic']} |")

    # 在"---\n\n## 二、"前插入新行
    insertion = "\n".join(new_rows) + "\n"
    matrix = matrix.replace("---\n\n## 二、主题分类索引", insertion + "---\n\n## 二、主题分类索引")

    # 更新主题分类索引：在对应主题小节追加
    for e in new_entries:
        topic = e["topic"]
        pattern = f"### {topic}（"
        if topic in matrix:
            # 在主题小节末尾（下一个"### "或"---"前）追加条目
            t_start = matrix.find(pattern)
            t_end = matrix.find("\n### ", t_start + 1)
            if t_end == -1:
                t_end = matrix.find("\n---", t_start + 1)
            if t_end > t_start:
                author_short = e["authors"].split("等")[0][:10] if e["authors"] else "佚名"
                new_item = f"- **[新增] {author_short}（{e['year']}）** — {e['journal']}：{e['conclusion'][:60]}"
                matrix = matrix[:t_end] + new_item + "\n" + matrix[t_end:]
            # 更新数量统计
            m = re.search(rf"(### {re.escape(topic)}（)(\d+)(篇）)", matrix)
            if m:
                matrix = matrix[:m.start(2)] + str(int(m.group(2)) + 1) + matrix[m.end(2):]
        else:
            # 新主题：在"## 三、"前插入新小节
            marker = "## 三、期刊级别图例"
            if marker in matrix:
                author_short = e["authors"].split("等")[0][:10] if e["authors"] else "佚名"
                new_section = (f"### {topic}（1篇）\n> 新增主题分类\n\n"
                               f"- **[新增] {author_short}（{e['year']}）** — {e['journal']}：{e['conclusion'][:60]}\n\n")
                matrix = matrix.replace(marker, new_section + marker)

    # 更新GB/T 7714引用段：在最后一个[18]后追加
    gbt_marker = "## 四、GB/T 7714-2015 引用格式"
    if gbt_marker in matrix:
        # 找到引用列表末尾
        last_ref = max(matrix.rfind("[1]"), matrix.rfind("[2]"), matrix.rfind("[3]"),
                       matrix.rfind("[4]"), matrix.rfind("[5]"), matrix.rfind("[6]"),
                       matrix.rfind("[7]"), matrix.rfind("[8]"), matrix.rfind("[9]"),
                       matrix.rfind("[10]"), matrix.rfind("[11]"), matrix.rfind("[12]"),
                       matrix.rfind("[13]"), matrix.rfind("[14]"), matrix.rfind("[15]"),
                       matrix.rfind("[16]"), matrix.rfind("[17]"), matrix.rfind("[18]"))
        if last_ref > gbt_marker.find("GB"):
            # 找到该行的结尾
            line_end = matrix.find("\n", last_ref)
            next_section = matrix.find("\n## ", line_end)
            if next_section == -1:
                next_section = len(matrix)
            # 计算当前引用数
            ref_count = len(re.findall(r"^\[\d+\]", matrix[matrix.find(gbt_marker):], re.M))
            for i, e in enumerate(new_entries, ref_count + 1):
                authors_full = e["authors"] if e["authors"] else "佚名"
                gbt = build_gbt7714(e, authors_full)
                matrix = matrix[:next_section] + f"[{i}] {gbt}\n" + matrix[next_section:]
                next_section = matrix.find("\n## ", matrix.find(f"[{i}]") + len(f"[{i}]"))
                if next_section == -1:
                    next_section = len(matrix)

    with open(MATRIX_PATH, "w", encoding="utf-8") as f:
        f.write(matrix)
    print(f"✅ 矩阵库已更新: {MATRIX_PATH}")

    # 4. 更新文献清单（GB/T 7714清单）
    if os.path.exists(LIST_PATH):
        with open(LIST_PATH, encoding="utf-8") as f:
            lst = f.read()
        new_lines = []
        for e in new_entries:
            authors_full = e["authors"] if e["authors"] else "佚名"
            gbt = build_gbt7714(e, authors_full)
            new_lines.append(f"{gbt}")
            new_lines.append(f"   📎 `{e['file']}`")
        if new_lines:
            # 在"---\n## GB/T"前插入编号条目
            insert_text = "\n".join(f"{i}. {l}" if i <= 50 else l for i, l in enumerate(new_lines, 1))
            lst = lst.replace("---\n## GB/T 7714-2015", insert_text + "\n\n---\n## GB/T 7714-2015")
        with open(LIST_PATH, "w", encoding="utf-8") as f:
            f.write(lst)
        print(f"✅ 文献清单已更新: {LIST_PATH}")

    # 5. 记录已入库
    state["ingested"] = sorted(ingested | {e["file"] for e in new_entries})
    state["last_ingest"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_state(state)
    print(f"✅ 状态已记录: {len(state['ingested'])} 篇已入库")

    # 6. 汇报摘要
    topics = {}
    for e in new_entries:
        topics[e["topic"]] = topics.get(e["topic"], 0) + 1
    print(f"\n📊 本次入库 {len(new_entries)} 篇，累计 {len(state['ingested'])} 篇")
    for t, c in sorted(topics.items(), key=lambda x: -x[1]):
        print(f"   {t}: {c}篇")
    print(f"   主题分布详见矩阵库")


if __name__ == "__main__":
    main()
