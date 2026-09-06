#!/usr/bin/env python3
"""
技能两阶段检索器 - 借鉴 Resource2Skill skill_retriever.py

阶段1: DashScope text-embedding-v2 向量检索 -> top-k 候选
阶段2: 火山方舟 LLM 重排序 -> top-n 最终选择
降级路径: 关键词匹配（无 API key 时）

用法:
  from skill_retriever import SkillRetriever

  retriever = SkillRetriever()
  results = retriever.retrieve("帮我优化一段文字的表达", top_k=5)
  # -> [{"skill_id": "polish", "skill_name": "表达优化", "score": 0.92, "reason": "..."}]
"""

import os
import sys
import json
import urllib.request
from pathlib import Path
from typing import Optional


# ============================================================
# 配置
# ============================================================

SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent  # skills/ 目录
EMBEDDING_CACHE = Path.home() / "AppData" / "Local" / "hermes" / "skill_embeddings.npz"

# DashScope Embedding 配置
DASHSCOPE_EMBED_MODEL = "text-embedding-v2"
DASHSCOPE_EMBED_DIM = 1536

# 火山方舟 LLM 重排序配置
VOLCANO_RERANK_MODEL = "deepseek-v4-flash"


# ============================================================
# 环境变量加载
# ============================================================

def _load_env():
    """从 ~/AppData/Local/hermes/.env 加载环境变量"""
    env_path = Path.home() / "AppData" / "Local" / "hermes" / ".env"
    if not env_path.exists():
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                if key and key not in os.environ:
                    os.environ[key] = val


def _get_dashscope_config():
    _load_env()
    key = os.environ.get("DASHSCOPE_API_KEY", "")
    base_url = os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    return key, base_url


def _get_volcano_config():
    _load_env()
    key = os.environ.get("ARK_API_KEY", "")
    base_url = os.environ.get("VOLCANO_BASE_URL", "https://ark.cn-beijing.volces.com/api/coding/v3")
    return key, base_url


# ============================================================
# 技能索引：扫描所有 SKILL.md 提取元数据
# ============================================================

def _scan_all_skills() -> list[dict]:
    """扫描 skills/ 目录下所有技能，提取 name, description, path。"""
    skills = []
    for cat_dir in sorted(SKILLS_ROOT.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("."):
            continue
        for skill_dir in sorted(cat_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            content = skill_md.read_text(encoding="utf-8")
            # 提取 YAML frontmatter
            if content.startswith("---"):
                end = content.find("---", 3)
                if end > 0:
                    frontmatter = content[3:end].strip()
                    name = ""
                    desc = ""
                    for line in frontmatter.split("\n"):
                        line = line.strip()
                        if line.startswith("name:"):
                            name = line.split(":", 1)[1].strip()
                        elif line.startswith("description:"):
                            # description 可能跨行，取第一行
                            desc = line.split(":", 1)[1].strip().strip(">").strip()
                    if name:
                        skills.append({
                            "skill_id": name,
                            "skill_name": name,
                            "description": desc,
                            "category": cat_dir.name,
                            "path": str(skill_dir),
                            "full_text": content[:2000],  # 前2000字用于 embedding
                        })
    return skills


# ============================================================
# Embedding 向量检索（阶段1）
# ============================================================

def _get_embeddings(texts: list[str], api_key: str, base_url: str) -> list[list[float]]:
    """调用 DashScope text-embedding-v2 获取向量。"""
    url = f"{base_url.rstrip('/')}/embeddings"
    payload = json.dumps({
        "model": DASHSCOPE_EMBED_MODEL,
        "input": texts,
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    resp = urllib.request.urlopen(req, timeout=60)
    data = json.loads(resp.read())
    return [item["embedding"] for item in data["data"]]


def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """计算余弦相似度。"""
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _embed_retrieve(query: str, skills: list[dict], top_k: int = 10) -> list[dict]:
    """阶段1: Embedding 向量检索。"""
    api_key, base_url = _get_dashscope_config()
    if not api_key:
        return []

    # 获取 query embedding
    query_vec = _get_embeddings([query], api_key, base_url)[0]

    # 获取所有技能的 embedding
    texts = [s["full_text"] for s in skills]
    # 分批处理（DashScope embedding 限制每次最多25条）
    all_vecs = []
    batch_size = 20
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_vecs = _get_embeddings(batch, api_key, base_url)
        all_vecs.extend(batch_vecs)

    # 计算相似度并排序
    scored = []
    for skill, vec in zip(skills, all_vecs):
        score = _cosine_similarity(query_vec, vec)
        scored.append({**skill, "score": score})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


# ============================================================
# LLM 重排序（阶段2）
# ============================================================

def _llm_rerank(query: str, candidates: list[dict], top_n: int = 5,
                api_key: str = "", base_url: str = "") -> list[dict]:
    """阶段2: 用火山方舟 LLM 重排序。"""
    if not api_key:
        return candidates[:top_n]

    # 构建候选摘要
    candidate_lines = []
    for i, c in enumerate(candidates):
        candidate_lines.append(
            f"{i+1}. [{c['skill_id']}] {c.get('description', c.get('skill_name', ''))[:100]}"
        )
    candidates_text = "\n".join(candidate_lines)

    rerank_prompt = (
        f"你是技能选择专家。根据用户任务，从以下候选技能中选择最相关的 {top_n} 个。\n"
        f"要求：选择互补的技能组合，避免功能重叠。\n\n"
        f"## 用户任务\n{query}\n\n"
        f"## 候选技能\n{candidates_text}\n\n"
        f"## 输出格式\n"
        f"输出JSON数组，每项含 skill_id 和 reason：\n"
        f'[{{"skill_id": "...", "reason": "一句话理由"}}]'
    )

    payload = json.dumps({
        "model": VOLCANO_RERANK_MODEL,
        "messages": [{"role": "user", "content": rerank_prompt}],
        "temperature": 0.3,
        "max_tokens": 1000,
        "thinking": {"type": "disabled"},
    }).encode("utf-8")

    url = f"{base_url.rstrip('/')}/chat/completions"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read())
    content = data["choices"][0]["message"]["content"]

    # 解析 JSON 响应
    import re
    json_match = re.search(r'\[.*\]', content, re.DOTALL)
    if json_match:
        try:
            reranked = json.loads(json_match.group())
            # 映射回完整技能信息
            result = []
            for item in reranked:
                skill_id = item.get("skill_id", "")
                reason = item.get("reason", "")
                for c in candidates:
                    if c["skill_id"] == skill_id:
                        result.append({**c, "rerank_reason": reason})
                        break
            return result[:top_n]
        except json.JSONDecodeError:
            pass

    # 解析失败，返回原始排序
    return candidates[:top_n]


# ============================================================
# 关键词匹配（降级路径）
# ============================================================

def _keyword_match(query: str, skills: list[dict], top_k: int = 5) -> list[dict]:
    """降级路径: 关键词匹配。"""
    query_lower = query.lower()
    scored = []
    for skill in skills:
        text = (skill.get("full_text", "") + " " + skill.get("skill_name", "")).lower()
        score = sum(1 for word in query_lower.split() if word in text)
        if score > 0:
            scored.append({**skill, "score": score / 10})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k] if scored else skills[:top_k]


# ============================================================
# 核心类: SkillRetriever
# ============================================================

class SkillRetriever:
    """两阶段技能检索器。

    阶段1: DashScope text-embedding-v2 向量检索
    阶段2: 火山方舟 LLM 重排序
    降级: 关键词匹配
    """

    def __init__(self):
        self._skills = None
        self._embeddings = None

    @property
    def skills(self) -> list[dict]:
        if self._skills is None:
            self._skills = _scan_all_skills()
        return self._skills

    def retrieve(self, query: str, top_k: int = 5, top_n: int = None) -> list[dict]:
        """两阶段检索。

        Args:
            query: 用户任务描述
            top_k: 阶段1返回的候选数（默认10）
            top_n: 最终返回数（默认等于top_k）

        Returns:
            排序后的技能列表，每项含 skill_id, skill_name, score, reason
        """
        if top_n is None:
            top_n = top_k

        if not self.skills:
            return []

        # 阶段1: Embedding 检索
        try:
            ds_key, ds_base = _get_dashscope_config()
            if ds_key:
                candidates = _embed_retrieve(query, self.skills, top_k=max(top_k * 2, 10))
                # 阶段2: LLM 重排序
                try:
                    vol_key, vol_base = _get_volcano_config()
                    if vol_key:
                        return _llm_rerank(query, candidates, top_n=top_n,
                                           api_key=vol_key, base_url=vol_base)
                except Exception as e:
                    print(f"[skill_retriever] LLM rerank failed: {e}", file=sys.stderr)
                # 重排序失败，返回 embedding 排序结果
                return candidates[:top_n]
        except Exception as e:
            print(f"[skill_retriever] Embedding retrieval failed: {e}", file=sys.stderr)

        # 降级: 关键词匹配
        print("[skill_retriever] Falling back to keyword matching", file=sys.stderr)
        return _keyword_match(query, self.skills, top_k=top_n)

    def list_all(self) -> list[dict]:
        """列出所有已索引的技能。"""
        return [{"skill_id": s["skill_id"], "skill_name": s["skill_name"],
                 "category": s["category"]} for s in self.skills]

    def get_skill(self, skill_id: str) -> Optional[dict]:
        """获取指定技能的详情。"""
        for s in self.skills:
            if s["skill_id"] == skill_id:
                return s
        return None


# ============================================================
# 命令行接口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Hermes 技能两阶段检索器")
    parser.add_argument("query", help="搜索查询")
    parser.add_argument("--top-k", type=int, default=5, help="返回数量")
    parser.add_argument("--list", action="store_true", help="列出所有技能")

    args = parser.parse_args()

    retriever = SkillRetriever()

    if args.list:
        skills = retriever.list_all()
        print(f"共 {len(skills)} 个技能:")
        for s in skills:
            print(f"  [{s['category']}] {s['skill_id']}")
        return

    results = retriever.retrieve(args.query, top_k=args.top_k)
    print(f"查询: '{args.query}'\n")
    for i, r in enumerate(results, 1):
        score = r.get("score", 0)
        reason = r.get("rerank_reason", r.get("description", "")[:80])
        print(f"  {i}. [{r['skill_id']}] (score={score:.3f})")
        if reason:
            print(f"     {reason[:100]}")


if __name__ == "__main__":
    main()
