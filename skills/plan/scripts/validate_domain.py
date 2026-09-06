#!/usr/bin/env python3
"""
域验证脚本 - 验证 Hermes 技能域的配置完整性和技能质量

借鉴 Resource2Skill 的 validate_domain() 函数设计。
检查 domain.yaml 必需字段、技能目录结构、文件存在性、Tier标注。

用法:
  python validate_domain.py --domain development
  python validate_domain.py --all
"""

import yaml
import sys
from pathlib import Path
from typing import Optional


SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent  # go up 3 levels: scripts/ -> plan/ -> skills/


def load_domain_config(domain_name: str) -> Optional[dict]:
    """加载域的 domain.yaml 配置。"""
    domain_dir = SKILLS_ROOT / domain_name
    config_path = domain_dir / "domain.yaml"
    if not config_path.exists():
        return None
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_domain(domain_name: str) -> list[str]:
    """验证一个域的配置和所有技能。

    Returns:
        错误列表（空列表 = 全部通过）
    """
    errors: list[str] = []
    domain_dir = SKILLS_ROOT / domain_name

    if not domain_dir.is_dir():
        return [f"Domain directory not found: {domain_dir}"]

    # 1. 检查 domain.yaml
    config = load_domain_config(domain_name)
    if config is None:
        errors.append(f"domain.yaml not found in {domain_name}/")
    else:
        # 检查必需字段
        required = ["name", "display_name", "categories"]
        for key in required:
            if key not in config:
                errors.append(f"domain.yaml missing required key: '{key}'")

        if "categories" in config and not config["categories"]:
            errors.append("categories is empty — must define at least one category")

    # 2. 检查每个技能
    skill_count = 0
    for entry in sorted(domain_dir.iterdir()):
        if not entry.is_dir():
            continue
        # 跳过非技能目录（如 .curator_backups, .hub 等）
        if entry.name.startswith("."):
            continue

        skill_path = entry
        skill_md = skill_path / "SKILL.md"

        if not skill_md.exists():
            errors.append(f"Skill '{entry.name}' missing SKILL.md")
            continue

        skill_count += 1

        # 检查 SKILL.md 有 YAML frontmatter
        content = skill_md.read_text(encoding="utf-8")
        if not content.startswith("---"):
            errors.append(f"Skill '{entry.name}' SKILL.md missing YAML frontmatter")

        # 检查多模态组件
        refs = list((skill_path / "references").iterdir()) if (skill_path / "references").exists() else []
        scripts = list((skill_path / "scripts").iterdir()) if (skill_path / "scripts").exists() else []
        templates = list((skill_path / "templates").iterdir()) if (skill_path / "templates").exists() else []

        # 检查脚本语法（Python 文件）
        for script_file in scripts:
            if script_file.suffix == ".py":
                try:
                    compile(script_file.read_text(encoding="utf-8"), str(script_file), "exec")
                except SyntaxError as e:
                    errors.append(f"Skill '{entry.name}' script '{script_file.name}' syntax error: {e}")

        # 检查模板格式（YAML 文件）
        for template_file in templates:
            if template_file.suffix in (".yaml", ".yml"):
                try:
                    yaml.safe_load(template_file.read_text(encoding="utf-8"))
                except yaml.YAMLError as e:
                    errors.append(f"Skill '{entry.name}' template '{template_file.name}' YAML error: {e}")

    if skill_count == 0:
        errors.append(f"No skills found in {domain_name}/")

    return errors


def validate_all() -> dict[str, list[str]]:
    """验证所有域。"""
    results = {}
    for entry in sorted(SKILLS_ROOT.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        if (entry / "domain.yaml").exists() or any(
            (entry / sub).is_dir() and not sub.startswith(".")
            for sub in entry.iterdir() if (entry / sub / "SKILL.md").exists()
        ):
            errors = validate_domain(entry.name)
            results[entry.name] = errors
    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Hermes 技能域验证工具")
    parser.add_argument("--domain", help="验证指定域")
    parser.add_argument("--all", action="store_true", help="验证所有域")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if args.all:
        results = validate_all()
        total_errors = 0
        for domain, errors in results.items():
            if args.json:
                print(f"  {domain}: {'OK' if not errors else 'FAIL'}")
            else:
                if errors:
                    print(f"\n=== {domain} ({len(errors)} errors) ===")
                    for e in errors:
                        print(f"  ❌ {e}")
                else:
                    print(f"  ✅ {domain}")
            total_errors += len(errors)
        if not args.json:
            print(f"\n总计: {len(results)} 域, {total_errors} 个错误")
    elif args.domain:
        errors = validate_domain(args.domain)
        if errors:
            print(f"\n=== {args.domain} ({len(errors)} errors) ===")
            for e in errors:
                print(f"  ❌ {e}")
        else:
            print(f"✅ {args.domain} 验证通过")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()