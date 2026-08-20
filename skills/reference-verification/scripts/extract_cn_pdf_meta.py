# -*- coding: utf-8 -*-
"""中文期刊 PDF 元数据提取：刊名/卷期/年份 + 6种页码格式探测。
用法：编辑 TARGETS（键名 -> PDF 文件名），脚本遍历 base 目录下每篇 PDF，
输出每篇的刊名行、卷/期/年、页码候选与连续段。适用于知识库已下载文献。
依赖：pip install pymupdf（import fitz）。
"""
import fitz
import os
import re
from collections import Counter

BASE = r"D:\BaiduSyncdisk\AIKnowledgeBase\ObsidianVault\academia\文献库\碳排放权交易"

# 键名 -> 文件名。按需替换。
TARGETS = {
    "35_示例": "示例-作者.pdf",
}

def extract_pages(doc):
    """多策略页码提取，返回 (页码数字列表, 说明)"""
    nums = []
    n = doc.page_count
    for i in range(n):
        page = doc[i]
        t = page.get_text()
        h = page.rect.height
        cands = []
        # 策略1: ·N·
        cands += re.findall(r"·\s*(\d{1,4})\s*·", t)
        # 策略2: 页脚数字（y > h-70）
        for w in page.get_text("words"):
            if w[1] > h - 70 and re.fullmatch(r"[0-9０-９]{1,4}", w[4].strip()):
                cands.append(w[4].translate(str.maketrans("０１２３４５６７８９", "0123456789")))
        # 策略3: 反序数字（"个 十 百" 倒序，如 "７ １ １" = 117）
        rev = re.findall(r"([０-９])\s*\n?\s*([０-９])\s*\n?\s*([０-９])", t)
        for triple in rev:
            digits = "".join(
                c.translate(str.maketrans("０１２３４５６７８９", "0123456789")) for c in triple)
            cands.append(digits)
        if cands:
            nums.append(cands[0])
    return nums

def main():
    for key, fn in TARGETS.items():
        path = os.path.join(BASE, fn)
        if not os.path.exists(path):
            print(f"◆ [{key}] 文件不存在: {fn}")
            continue
        doc = fitz.open(path)
        first = doc[0].get_text()
        vol = re.search(r"第\s*(\d+)\s*卷", first)
        iss = re.search(r"第\s*(\d+)\s*期", first)
        yr = re.search(r"(20\d{2})\s*年", first)
        jname = ""
        for line in first.split("\n"):
            line = line.strip()
            if 4 <= len(line) <= 30 and re.search(
                r"(学报|评论|研究|经济|管理|科学|生态|社会|保护|税务|人口|资源|能源|金融|科技|实践|理论)", line
            ) and re.search(r"(第|Vol|No|20\d{2}|卷|期|总)", line):
                jname = line
                break
        pages = extract_pages(doc)
        print(f"◆ [{key}] {fn[:25]}... 页数{doc.page_count}")
        print(f"   刊名行: {jname[:45]}")
        print(f"   卷:{vol.group(1) if vol else '-'} 期:{iss.group(1) if iss else '-'} 年:{yr.group(1) if yr else '-'}")
        print(f"   页码候选: {pages[:15]}{'...' if len(pages) > 15 else ''}")
        if pages:
            pnums = sorted(set(int(p) for p in pages if p.isdigit() and 100 <= int(p) <= 9999))
            print(f"   有效页码序列: {pnums}")
        doc.close()

if __name__ == "__main__":
    main()
