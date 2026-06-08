#!/usr/bin/env python3
"""Package a skill folder as a deterministic .skill zip archive."""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
EXCLUDE_FILES = {".DS_Store", "review.html", "benchmark.json", "benchmark.md"}


def should_skip(path: Path, root: Path, include_evals: bool) -> bool:
    rel_parts = path.relative_to(root).parts
    if any(part in EXCLUDE_DIRS for part in rel_parts):
        return True
    if any(part.endswith("-workspace") for part in rel_parts):
        return True
    if not include_evals and rel_parts and rel_parts[0] == "evals":
        return True
    if path.name in EXCLUDE_FILES:
        return True
    if path.suffix in {".pyc", ".pyo"}:
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path")
    parser.add_argument("--output", default=".", help="Output directory or .skill file path")
    parser.add_argument("--include-evals", action="store_true", help="Include evals/ in the package")
    args = parser.parse_args()

    skill_path = Path(args.skill_path).expanduser().resolve()
    if not (skill_path / "SKILL.md").exists():
        parser.error("SKILL.md not found in skill_path")

    output = Path(args.output).expanduser().resolve()
    if output.suffix == ".skill":
        package_path = output
        package_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output.mkdir(parents=True, exist_ok=True)
        package_path = output / f"{skill_path.name}.skill"

    files = [p for p in skill_path.rglob("*") if p.is_file() and not should_skip(p, skill_path, args.include_evals)]
    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(files, key=lambda p: str(p.relative_to(skill_path))):
            zf.write(file, arcname=str(Path(skill_path.name) / file.relative_to(skill_path)))
    print(package_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
