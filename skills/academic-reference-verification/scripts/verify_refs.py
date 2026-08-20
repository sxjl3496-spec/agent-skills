# -*- coding: utf-8 -*-
"""参考文献批量核实脚本（Crossref）
用法: python verify_refs.py <文献列表文件> [起始编号]
输入: 每行 "[N] 作者. 题名. 刊名, 年, 卷(期): 页码." 格式
输出: 每篇的 Crossref 最佳匹配（标题/作者/刊名/年/卷/期/页/DOI）+ 匹配判定
"""
import requests, re, sys, time, json

session = requests.Session()
session.trust_env = False  # 必须：绕过系统代理

def crossref_by_doi(doi):
    try:
        r = session.get(f"https://api.crossref.org/works/{doi}", timeout=20)
        if r.status_code == 200:
            return r.json()["message"]
    except Exception:
        pass
    return None

def crossref_search(author, title_kw, rows=3):
    try:
        r = session.get("https://api.crossref.org/works", params={
            "query.bibliographic": title_kw,
            "query.author": author,
            "rows": rows,
            "select": "DOI,title,author,container-title,volume,issue,page,published",
        }, timeout=25)
        return r.json().get("message", {}).get("items", [])
    except Exception:
        return []

def fmt(it):
    if not it:
        return "  ❌ 无匹配"
    t = (it.get("title") or [""])[0][:60]
    ct = (it.get("container-title") or [""])[0][:35]
    yr = ""
    for k in ("published-print", "published", "published-online"):
        if it.get(k, {}).get("date-parts"):
            yr = it[k]["date-parts"][0][0]
            break
    au = ", ".join(f"{a.get('family','')}" for a in (it.get("author") or [])[:4])
    return (f"  → {t}\n     {au} | {ct} | {yr} | "
            f"vol={it.get('volume','')} iss={it.get('issue','')} pg={it.get('page','')} | DOI:{it.get('DOI','')}")

def main():
    if len(sys.argv) < 2:
        print("用法: python verify_refs.py <文献列表文件> [起始编号]")
        return
    path = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        m = re.match(r"^\[(\d+)\]\s*(.+)", line.strip())
        if not m:
            continue
        num = int(m.group(1))
        if num < start:
            continue
        entry = m.group(2)
        # 粗略解析：作者(第一个.前) 和 标题关键词(第二个.后 前50字)
        parts = entry.split(". ")
        author = parts[0] if parts else ""
        title_kw = parts[1][:60] if len(parts) > 1 else ""
        # 尝试 DOI
        doi_m = re.search(r"10\.\d{4,9}/[^\s,\]]+", entry)
        print(f"\n[{num}] {author} - {title_kw}")
        if doi_m:
            it = crossref_by_doi(doi_m.group(0).rstrip('.'))
            if it:
                print(fmt(it))
                time.sleep(0.6)
                continue
        items = crossref_search(author, title_kw)
        for it in items[:2]:
            print(fmt(it))
        time.sleep(0.8)

if __name__ == "__main__":
    main()
