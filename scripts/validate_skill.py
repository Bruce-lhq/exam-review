#!/usr/bin/env python3
"""Validate the exam-review skill package before submission."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "metadata.json",
    "requirements.txt",
    "scripts/extract.py",
    "scripts/validate_skill.py",
    "templates/_template/README.md",
    "templates/math/README.md",
    "templates/physics/README.md",
    "resources/example-math-review.html",
    "resources/example-math-exam.html",
    "resources/example-physics-review.html",
    "resources/example-physics-exam.html",
    "tests/example-usage.md",
]

README_RESOURCE_RE = re.compile(r"resources/[A-Za-z0-9._/-]+")
SKILL_VERSION_RE = re.compile(r'^version:\s*"([^"]+)"\s*$', re.MULTILINE)
README_VERSION_RE = re.compile(r"版本 v([0-9]+\.[0-9]+\.[0-9]+)")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files(errors: list[str]) -> None:
    for file_name in REQUIRED_FILES:
        path = ROOT / file_name
        if not path.is_file():
            errors.append(f"缺少必需文件：{file_name}")


def load_metadata(errors: list[str]) -> dict:
    path = ROOT / "metadata.json"
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        errors.append(f"metadata.json 不是合法 JSON：第 {exc.lineno} 行第 {exc.colno} 列")
    except OSError as exc:
        errors.append(f"无法读取 metadata.json：{exc}")
    return {}


def check_versions(errors: list[str]) -> None:
    skill_text = read_text(ROOT / "SKILL.md")
    readme_text = read_text(ROOT / "README.md")

    skill_match = SKILL_VERSION_RE.search(skill_text)
    readme_match = README_VERSION_RE.search(readme_text)

    if not skill_match:
        errors.append('SKILL.md 缺少 YAML version: "x.y.z"')
        return
    if not readme_match:
        errors.append("README.md 缺少末尾版本号，例如：版本 v1.3.1")
        return

    skill_version = skill_match.group(1)
    readme_version = readme_match.group(1)
    if skill_version != readme_version:
        errors.append(
            f"版本不一致：SKILL.md={skill_version}，README.md=v{readme_version}"
        )


def check_metadata(metadata: dict, errors: list[str]) -> None:
    if metadata.get("name") != "exam-review":
        errors.append('metadata.json 中 name 应为 "exam-review"')
    if metadata.get("document_type") != "agent-skill":
        errors.append('metadata.json 中 document_type 应为 "agent-skill"')

    description = metadata.get("description", "")
    use_cases = " ".join(metadata.get("use_cases", []))
    for keyword in ["Auto Mode", "Template Studio"]:
        if keyword not in description and keyword not in use_cases:
            errors.append(f"metadata.json 未覆盖关键能力：{keyword}")


def check_readme_resource_links(errors: list[str]) -> None:
    readme_text = read_text(ROOT / "README.md")
    for match in sorted(set(README_RESOURCE_RE.findall(readme_text))):
        path = ROOT / match
        if not path.is_file():
            errors.append(f"README.md 引用了不存在的资源文件：{match}")


def check_keyword_coverage(errors: list[str]) -> None:
    files = [
        ROOT / "SKILL.md",
        ROOT / "README.md",
        ROOT / "tests/example-usage.md",
    ]
    combined = "\n".join(read_text(path) for path in files)
    for keyword in ["Auto Mode", "Template Studio", "增量更新"]:
        if keyword not in combined:
            errors.append(f"文档未覆盖关键能力：{keyword}")
    if "templates/_template/README.md" not in combined:
        errors.append("文档未说明 Template Studio 标准模板包骨架：templates/_template/README.md")


def check_requirements(errors: list[str]) -> None:
    requirements = read_text(ROOT / "requirements.txt").lower()
    if "markitdown" not in requirements:
        errors.append("requirements.txt 缺少核心依赖 markitdown")


def check_extract_help(errors: list[str]) -> None:
    extract_text = read_text(ROOT / "scripts/extract.py")
    if "argparse.ArgumentParser" not in extract_text:
        errors.append("scripts/extract.py 缺少 argparse 帮助入口")


def main() -> int:
    errors: list[str] = []

    check_required_files(errors)
    if errors:
        print("❌ exam-review skill validation failed")
        for error in errors:
            print(f"  - {error}")
        return 1

    metadata = load_metadata(errors)
    check_versions(errors)
    check_metadata(metadata, errors)
    check_readme_resource_links(errors)
    check_keyword_coverage(errors)
    check_requirements(errors)
    check_extract_help(errors)

    if errors:
        print("❌ exam-review skill validation failed")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("✅ exam-review skill validation passed")
    print(f"Checked {len(REQUIRED_FILES)} required files under {ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
