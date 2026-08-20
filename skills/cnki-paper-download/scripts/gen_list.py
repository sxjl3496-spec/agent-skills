"""
生成 GB/T 7714-2015 格式文献清单（从PDF元数据+文件名提取）
输出：清单MD

v2 (2026.8.6): 前缀匹配期刊映射键 —— 文件名标题常含副标题（如"——基于..."），
精确匹配 JOURNAL_YEAR.get(title) 会漏判导致"未知期刊"。改用 startswith 双向匹配，
并在末尾提示未匹配项，方便补充映射。
"""
import os, json

DIR = r"D:\BaiduSyncdisk\AIKnowledgeBase\ObsidianVault\academia\文献库\碳排放权交易"

# 从文件名提取标题和作者
def parse_filename(fname):
    name = fname.replace(".pdf", "")
    # 格式: "标题-作者1作者2作者3"
    # 用最后一个"-"分割（标题可能含"-"）
    parts = name.rsplit("-", 1)
    if len(parts) == 2:
        title, authors = parts[0], parts[1]
    else:
        title, authors = name, ""
    return title, authors

# 人工核对的期刊/年份映射（基于PDF首页元数据）
JOURNAL_YEAR = {
    "“双碳”目标下碳排放权交易的减排效应与作用机制": ("生态经济", "2025", "41(10)"),
    "“双碳”背景下碳排放权交易行政监管的体制构建与机制创新": ("华中农业大学学报（社会科学版）", "2026", "(2)"),
    "中国碳市场一体化的动态测度与阻碍因素研究": ("运筹与管理", "2026", "35(2)"),
    "国内外碳市场与原油期货市场、股票市场的时频联动分析": ("系统工程理论与实践", "2025", ""),
    "基于《中华人民共和国生态环境法典》的碳交易市场规范续造": ("中国人口·资源与环境", "2025", ""),
    "市场激励型环境政策促进城市绿色创新的“量质双升”": ("重庆社会科学", "2025", ""),
    "新质生产力视域下碳排放权交易对绿色高质量发展的影响研究": ("科技管理研究", "2024", "44(14)"),
    "碳交易、碳排放权配额与绿色转型风险": ("南开管理评论", "2024", "(11)"),
    "碳交易与企业数字创新": ("中国工业经济", "2024", ""),
    "碳交易市场对农业绿色低碳发展的影响机理与协同增效路径": ("中国农业资源与区划", "2025", "47(12)"),
    "碳交易税务处理与会计处理差异问题研析": ("税务研究", "2025", "(12)"),
    "碳排放权交易中行政处罚的适用困境及其纾解": ("社会科学家", "2025", ""),
    "碳排放权交易如何影响企业全要素生产率？": ("管理评论", "2025", "37(2)"),
    "碳排放权交易政策能够提升企业ESG表现吗？": ("科学学与科学技术管理", "2024", ""),
    "碳排放权交易监管手段的优化与阶梯式构建": ("环境保护", "2024", ""),
    "碳排放权交易驱动城市绿色高质量发展的影响研究": ("西南民族大学学报（人文社会科学版）", "2025", ""),
    "策略性回应还是实质性响应？碳排放权交易政策的企业绿色创新效应": ("南开管理评论", "2024", ""),
    "近朱者赤_被纳入碳排放权交易试点的客户能否影响企业ESG表现？": ("研究与发展管理", "2024", "36(1)"),
}

# 生成GB/T 7714条目
entries = []
for fname in sorted(os.listdir(DIR)):
    if not fname.endswith(".pdf"):
        continue
    title, authors = parse_filename(fname)
    # 前缀匹配：文件名标题含副标题（如"——基于..."），用 startswith 双向匹配
    journal, year, vol = "未知期刊", "未知", ""
    for key, val in JOURNAL_YEAR.items():
        if title.startswith(key) or key.startswith(title):
            journal, year, vol = val
            break
    # 作者格式：中文用逗号分隔，最多列3人加"等"
    author_list = authors if authors else "佚名"
    # GB/T 7714: 作者. 题名[J]. 刊名, 年, 卷(期): 页码.
    vol_part = f", {vol}" if vol else ""
    entry = f"{author_list}. {title}[J]. {journal}{vol_part}, {year}."
    entries.append({"file": fname, "title": title, "authors": author_list,
                    "journal": journal, "year": year, "entry": entry})

# 写入MD清单
md_lines = ["# 碳排放权交易文献库清单", "",
            "> 来源：知网（文献云平台），下载日期：2026-08-06", "",
            "> 说明：全部为CSSCI来源期刊论文，共{}篇".format(len(entries)), ""]
for i, e in enumerate(entries, 1):
    md_lines.append(f"{i}. {e['entry']}")
    md_lines.append(f"   📎 `{e['file']}`")
md_lines.append("")
md_lines.append("---")
md_lines.append("## GB/T 7714-2015 引用格式（按序编码）")
md_lines.append("")
for i, e in enumerate(entries, 1):
    md_lines.append(f"[{i}] {e['entry']}")

out_md = os.path.join(DIR, "文献清单_GB7714.md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print(f"✅ 清单已生成: {out_md}")
print(f"共 {len(entries)} 篇")
unknown = [e for e in entries if e["journal"] == "未知期刊"]
if unknown:
    print(f"⚠️ {len(unknown)} 篇期刊未匹配（需补 JOURNAL_YEAR 映射）:")
    for e in unknown:
        print(f"  - {e['title'][:40]}")
