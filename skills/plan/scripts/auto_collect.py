#!/usr/bin/env python3
"""
技能自动收集守护进程 - 借鉴 Resource2Skill auto_collect.py

定期从指定来源（GitHub trending / 技术博客 / ArXiv）搜索 AI Agent 相关资源，
用 skill-distiller 蒸馏成新技能候选。

运行方式:
  python auto_collect.py --dry-run    # 仅搜索，不蒸馏
  python auto_collect.py --collect     # 搜索+蒸馏
  python auto_collect.py --status      # 查看收集状态
"""

import json
import time
import os
import sys
import urllib.request
from pathlib import Path
from datetime import datetime


STATE_DIR = Path.home() / "AppData" / "Local" / "hermes" / "auto_collect"
SKILLS_DIR = Path(__file__).resolve().parent.parent.parent  # skills/

# 搜索关键词池
QUERY_POOL = [
    "AI agent skill framework",
    "claude code skills tutorial",
    "agent tool use pattern",
    "MCP model context protocol",
    "multi-agent collaboration",
    "agent memory system",
    "prompt engineering best practices",
    "agent evaluation benchmark",
]


def _load_state() -> dict:
    """加载收集状态。"""
    state_path = STATE_DIR / "state.json"
    if state_path.exists():
        return json.loads(state_path.read_text(encoding="utf-8"))
    return {
        "total_collected": 0,
        "last_run": None,
        "processed_urls": [],
        "collected_skills": [],
    }


def _save_state(state: dict):
    """保存收集状态。"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_path = STATE_DIR / "state.json"
    state["last_run"] = datetime.now().isoformat()
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def search_github_trending(query: str, max_results: int = 5) -> list[dict]:
    """搜索 GitHub trending 仓库。"""
    import urllib.parse
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&per_page={max_results}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        results = []
        for item in data.get("items", [])[:max_results]:
            results.append({
                "type": "github_repo",
                "url": item["html_url"],
                "title": item["full_name"],
                "description": item.get("description", ""),
                "stars": item["stargazers_count"],
                "query": query,
            })
        return results
    except Exception as e:
        print(f"  [search] GitHub error: {e}", file=sys.stderr)
        return []


def collect_once(dry_run: bool = True) -> dict:
    """执行一次收集周期。"""
    state = _load_state()
    processed = set(state.get("processed_urls", []))

    new_candidates = []
    for query in QUERY_POOL:
        print(f"  Searching: {query}")
        results = search_github_trending(query, max_results=3)
        for r in results:
            if r["url"] not in processed:
                new_candidates.append(r)
                processed.add(r["url"])

    report = {
        "timestamp": datetime.now().isoformat(),
        "queries_run": len(QUERY_POOL),
        "new_candidates": len(new_candidates),
        "candidates": new_candidates[:10],  # 限制输出
        "dry_run": dry_run,
    }

    if not dry_run and new_candidates:
        # 保存候选列表（蒸馏由 skill-distiller 技能处理）
        candidates_path = STATE_DIR / "candidates.json"
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        existing = []
        if candidates_path.exists():
            existing = json.loads(candidates_path.read_text(encoding="utf-8"))
        existing.extend(new_candidates)
        candidates_path.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        state["total_collected"] += len(new_candidates)
        state["processed_urls"] = list(processed)
        _save_state(state)
    else:
        # dry-run 也保存已处理URL
        state["processed_urls"] = list(processed)
        _save_state(state)

    return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Hermes 技能自动收集守护进程")
    parser.add_argument("--dry-run", action="store_true", help="仅搜索，不保存候选")
    parser.add_argument("--collect", action="store_true", help="搜索并保存候选")
    parser.add_argument("--status", action="store_true", help="查看收集状态")

    args = parser.parse_args()

    if args.status:
        state = _load_state()
        print(f"总收集: {state.get('total_collected', 0)}")
        print(f"上次运行: {state.get('last_run', '从未')}")
        print(f"已处理URL: {len(state.get('processed_urls', []))}")
        candidates_path = STATE_DIR / "candidates.json"
        if candidates_path.exists():
            candidates = json.loads(candidates_path.read_text(encoding="utf-8"))
            print(f"待蒸馏候选: {len(candidates)}")
            for c in candidates[:5]:
                print(f"  - [{c['type']}] {c['title']}: {c['description'][:60]}")
        return

    report = collect_once(dry_run=not args.collect)
    print(f"\n收集报告:")
    print(f"  查询数: {report['queries_run']}")
    print(f"  新候选: {report['new_candidates']}")
    for c in report["candidates"]:
        print(f"  - [{c['type']}] {c['title']} ({c.get('stars', '?')}*)")
        print(f"    {c['description'][:80]}")


if __name__ == "__main__":
    main()
