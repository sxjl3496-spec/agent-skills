# -*- coding: utf-8 -*-
"""Crossref 批量核实参考文献（英文部分）。
用法：编辑 REFS 字典（编号 -> (作者关键词, 标题关键词)），运行后逐条输出
     MATCH（含完整卷期页码+DOI）/ NO MATCH（疑似编造，需替换）。
依赖：pip install requests；需能直连 api.crossref.org（trust_env=False 绕代理）。
"""
import requests
import time

session = requests.Session()
session.trust_env = False  # 必须：绕过系统代理（Clash 未开时会 ProxyError）

# 示例：编号 -> (作者, 标题关键词)。按需替换为真实待核实列表。
REFS = {
    1: ("Coase", "The Problem of Social Cost"),
    2: ("Montgomery", "Markets in Licenses and Efficient Pollution Control"),
}

# 附带字段：DOI 反查用（验证已知 DOI 是否真实）
DOI_CHECKS = {
    # 编号: "10.xxxx/xxx"
}

def query_bibliographic(author, title_kw, rows=2):
    r = session.get("https://api.crossref.org/works", params={
        "query.bibliographic": title_kw,
        "query.author": author,
        "rows": rows,
        "select": "DOI,title,author,container-title,volume,issue,page,published",
    }, timeout=25)
    out = []
    for it in r.json().get("message", {}).get("items", []):
        yr = ""
        for k in ("published", "published-print", "published-online"):
            if it.get(k, {}).get("date-parts"):
                yr = it[k]["date-parts"][0][0]
                break
        au = ", ".join(f"{a.get('family','')}" for a in (it.get("author") or [])[:4])
        out.append({
            "title": (it.get("title") or [""])[0][:75],
            "authors": au,
            "journal": (it.get("container-title") or [""])[0][:40],
            "year": yr,
            "vol": it.get("volume", ""),
            "issue": it.get("issue", ""),
            "page": it.get("page", ""),
            "doi": it.get("DOI", ""),
        })
    return out

def check_doi(doi):
    r = session.get(f"https://api.crossref.org/works/{doi}", timeout=20)
    if r.status_code != 200:
        return None
    it = r.json()["message"]
    return (it.get("title") or [""])[0][:75], (it.get("container-title") or [""])[0][:40]

def main():
    for num, (author, title_kw) in REFS.items():
        print(f"\n=== [{num}] 原条目: {author} - {title_kw}")
        try:
            for hit in query_bibliographic(author, title_kw):
                print(f"  -> {hit['title']} | {hit['authors']} | {hit['journal']} | "
                      f"{hit['year']} | {hit['vol']}({hit['issue']}):{hit['page']} | DOI:{hit['doi']}")
        except Exception as e:
            print(f"  ERR: {e}")
        time.sleep(0.8)

    for num, doi in DOI_CHECKS.items():
        res = check_doi(doi)
        print(f"\n=== [{num}] DOI {doi}: " + (f"存在 -> {res[0]} | {res[1]}" if res else "不存在(404)"))
        time.sleep(0.5)

if __name__ == "__main__":
    main()
