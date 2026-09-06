#!/usr/bin/env python3
"""
技能溯源清单（Skill Grounding Provenance）脚本

借鉴 Resource2Skill 的 skill_grounding.py 设计，为 Hermes 的 plan 技能
提供交付物溯源能力。每次 Agent 使用技能创建产出物时，记录：
- 使用了哪个技能（from_skill_ids）
- 应用到哪个交付物（target_artifact）
- 做了什么适配修改（adaptation_notes）

实现交付物使用的可审计性。

用法:
  from skill_grounding import SkillGrounding

  sg = SkillGrounding()
  sg.record(
      from_skill_ids=["plan", "polish"],
      target_artifact="D:/path/to/note.md",
      adaptation_notes="使用plan的阶段4验证流程+polish的表达优化原则"
  )
  sg.save()
  report = sg.report()
"""

import json
import time
from pathlib import Path
from datetime import datetime


# 溯源清单默认路径
DEFAULT_GROUNDING_DIR = Path.home() / "AppData" / "Local" / "hermes" / "groundings"
MANIFEST_FILENAME = "skill_trace_manifest.json"
SCHEMA_VERSION = 1


class SkillGrounding:
    """技能溯源清单管理器。

    记录 Agent 在执行任务时使用了哪些技能、产出物是什么、做了什么适配。
    溯源清单存储为 JSON sidecar 文件（与产出物同目录）。
    """

    def __init__(self, base_dir: Path | str | None = None):
        self.base_dir = Path(base_dir) if base_dir else DEFAULT_GROUNDING_DIR
        self.groundings: list[dict] = []
        self._load()

    def _manifest_path(self) -> Path:
        return self.base_dir / MANIFEST_FILENAME

    def _load(self):
        """加载已有的溯源清单。"""
        path = self._manifest_path()
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    self.groundings = data.get("groundings", [])
            except Exception:
                pass

    def record(
        self,
        from_skill_ids: str | list[str],
        target_artifact: str,
        adaptation_notes: str = "",
        task_context: str = "",
        extra: dict | None = None,
    ) -> dict:
        """记录一条溯源条目。

        Args:
            from_skill_ids: 使用的技能名（单个字符串或列表）
            target_artifact: 产出物路径或标识
            adaptation_notes: 对技能做了什么适配/修改
            task_context: 任务上下文（简述任务目标）
            extra: 额外元数据

        Returns:
            创建的溯源条目 dict
        """
        if isinstance(from_skill_ids, str):
            skill_ids = [from_skill_ids]
        else:
            skill_ids = list(from_skill_ids)

        entry = {
            "schema_version": SCHEMA_VERSION,
            "from_skill_ids": skill_ids,
            "target_artifact": str(target_artifact),
            "adaptation_notes": str(adaptation_notes or "").strip(),
            "task_context": str(task_context or "").strip(),
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
        }
        if extra:
            entry.update(extra)

        self.groundings.append(entry)
        return entry

    def save(self) -> Path:
        """保存溯源清单到磁盘。

        Returns:
            保存的文件路径
        """
        self.base_dir.mkdir(parents=True, exist_ok=True)
        path = self._manifest_path()
        data = {
            "schema_version": SCHEMA_VERSION,
            "total": len(self.groundings),
            "groundings": self.groundings,
        }
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    def report(self) -> str:
        """生成溯源报告（人类可读文本）。

        Returns:
            格式化的溯源报告字符串
        """
        if not self.groundings:
            return "无溯源记录。"

        lines = [f"技能溯源报告（共 {len(self.groundings)} 条记录）\n"]
        lines.append("=" * 60)

        # 按产出物分组
        by_artifact: dict[str, list[dict]] = {}
        for g in self.groundings:
            artifact = g.get("target_artifact", "unknown")
            by_artifact.setdefault(artifact, []).append(g)

        for artifact, entries in by_artifact.items():
            lines.append(f"\n产出物: {artifact}")
            for e in entries:
                skills = ", ".join(e.get("from_skill_ids", []))
                notes = e.get("adaptation_notes", "（无适配说明）")
                dt = e.get("datetime", "unknown")
                lines.append(f"  [{dt}] 技能: {skills}")
                lines.append(f"    适配: {notes}")
                ctx = e.get("task_context", "")
                if ctx:
                    lines.append(f"    上下文: {ctx}")

        # 统计
        lines.append("\n" + "=" * 60)
        all_skills = set()
        for g in self.groundings:
            all_skills.update(g.get("from_skill_ids", []))
        lines.append(f"使用技能: {sorted(all_skills)}")
        lines.append(f"产出物数: {len(by_artifact)}")
        lines.append(f"溯源条目: {len(self.groundings)}")

        return "\n".join(lines)

    def get_groundings_for_artifact(self, artifact_path: str) -> list[dict]:
        """获取指定产出物的所有溯源条目。"""
        return [
            g for g in self.groundings
            if g.get("target_artifact") == str(artifact_path)
        ]

    def get_groundings_for_skill(self, skill_id: str) -> list[dict]:
        """获取使用指定技能的所有溯源条目。"""
        return [
            g for g in self.groundings
            if skill_id in g.get("from_skill_ids", [])
        ]

    def clear(self):
        """清空溯源记录。"""
        self.groundings = []


# ============================================================
# 命令行接口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="技能溯源清单工具 - 记录和查询技能使用溯源"
    )
    sub = parser.add_subparsers(dest="command")

    # report 子命令
    report_parser = sub.add_parser("report", help="生成溯源报告")
    report_parser.add_argument(
        "--dir", default=None,
        help="溯源清单目录（默认: ~/AppData/Local/hermes/groundings）",
    )

    # record 子命令
    record_parser = sub.add_parser("record", help="记录一条溯源")
    record_parser.add_argument(
        "--skills", required=True,
        help="使用的技能名（逗号分隔）",
    )
    record_parser.add_argument(
        "--artifact", required=True,
        help="产出物路径",
    )
    record_parser.add_argument(
        "--notes", default="",
        help="适配说明",
    )
    record_parser.add_argument(
        "--context", default="",
        help="任务上下文",
    )

    args = parser.parse_args()

    if args.command == "report" or args.command is None:
        sg = SkillGrounding(base_dir=args.dir) if hasattr(args, "dir") and args.dir else SkillGrounding()
        print(sg.report())
    elif args.command == "record":
        sg = SkillGrounding()
        sg.record(
            from_skill_ids=args.skills.split(","),
            target_artifact=args.artifact,
            adaptation_notes=args.notes,
            task_context=args.context,
        )
        path = sg.save()
        print(f"溯源记录已保存到: {path}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
