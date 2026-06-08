#!/usr/bin/env python3
"""Validate an AI-agent skill folder for structure, frontmatter, resources, evals, and common leaks."""
from __future__ import annotations

import argparse
import json
import py_compile
import re
from pathlib import Path
from typing import Dict, List, Tuple

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$|^[a-z0-9]$")
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"sk-proj-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}"),
]
TEXT_EXTS = {".md", ".py", ".json", ".yaml", ".yml", ".txt", ".html", ".sh"}
ALLOWED_ROOT = {"SKILL.md", "scripts", "references", "assets", "agents", "evals"}
DISCOURAGED_ROOT_FILES = {"README.md", "CHANGELOG.md", "INSTALL.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md"}


def read_frontmatter(skill_md: Path) -> Tuple[Dict[str, str], str, List[str]]:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: List[str] = []
    if not lines or lines[0].strip() != "---":
        return {}, text, ["SKILL.md must start with YAML frontmatter delimited by ---"]
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, text, ["SKILL.md frontmatter is missing closing ---"]
    data: Dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#") or raw.startswith(" "):
            continue
        if ":" not in raw:
            errors.append(f"frontmatter line is not key: value format: {raw}")
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    body = "\n".join(lines[end + 1 :])
    return data, body, errors


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS


def validate_evals(path: Path) -> List[str]:
    errors: List[str] = []
    evals_path = path / "evals" / "evals.json"
    if not evals_path.exists():
        return errors
    try:
        data = json.loads(evals_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"evals/evals.json is not valid JSON: {exc}"]
    if not isinstance(data, dict):
        return ["evals/evals.json must be a JSON object"]
    if not data.get("skill_name"):
        errors.append("evals/evals.json missing skill_name")
    evals = data.get("evals")
    if not isinstance(evals, list):
        errors.append("evals/evals.json field 'evals' must be a list")
        return errors
    for i, item in enumerate(evals):
        if not isinstance(item, dict):
            errors.append(f"evals[{i}] must be an object")
            continue
        if not item.get("id"):
            errors.append(f"evals[{i}] missing id")
        if not item.get("prompt"):
            errors.append(f"evals[{i}] missing prompt")
        if "assertions" in item and not isinstance(item["assertions"], list):
            errors.append(f"evals[{i}].assertions must be a list")
    return errors


def scan_secrets(path: Path) -> List[str]:
    findings: List[str] = []
    for file in path.rglob("*"):
        if not file.is_file() or not is_text_file(file):
            continue
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(f"possible secret in {file.relative_to(path)}")
                break
    return findings


def compile_python(path: Path) -> List[str]:
    errors: List[str] = []
    scripts = path / "scripts"
    if not scripts.exists():
        return errors
    for script in scripts.rglob("*.py"):
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"Python syntax error in {script.relative_to(path)}: {exc.msg}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path", help="Path to a skill folder")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    path = Path(args.skill_path).expanduser().resolve()
    errors: List[str] = []
    warnings: List[str] = []

    if not path.exists() or not path.is_dir():
        print(f"ERROR: not a directory: {path}")
        return 1

    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        print("ERROR: SKILL.md is required")
        return 1

    frontmatter, body, fm_errors = read_frontmatter(skill_md)
    errors.extend(fm_errors)

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not name:
        errors.append("frontmatter missing name")
    elif not NAME_RE.fullmatch(name):
        errors.append("frontmatter name must use lowercase letters, digits, and hyphens and be under 64 characters")
    elif path.name != name:
        warnings.append(f"folder name '{path.name}' does not match frontmatter name '{name}'")

    if not description:
        errors.append("frontmatter missing description")
    elif len(description.split()) < 8:
        warnings.append("description is very short; include what the skill does and when to use it")

    unknown_fm = set(frontmatter) - {"name", "description", "metadata", "compatibility"}
    if unknown_fm:
        warnings.append("unusual frontmatter fields: " + ", ".join(sorted(unknown_fm)))

    if "when to use" in body.lower():
        warnings.append("body contains 'when to use'; trigger rules usually belong in frontmatter description")

    for child in path.iterdir():
        if child.name in DISCOURAGED_ROOT_FILES:
            warnings.append(f"discouraged root file: {child.name}")
        elif child.name.startswith("."):
            continue
        elif child.name not in ALLOWED_ROOT:
            warnings.append(f"unexpected root item: {child.name}")

    refs = path / "references"
    if refs.exists():
        body_text = skill_md.read_text(encoding="utf-8")
        for ref in refs.rglob("*"):
            if ref.is_file() and not ref.name.startswith("."):
                rel = str(ref.relative_to(path))
                if ref.name not in body_text and rel not in body_text:
                    warnings.append(f"reference file not linked from SKILL.md: {rel}")

    errors.extend(validate_evals(path))
    errors.extend(compile_python(path))
    errors.extend(scan_secrets(path))

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors or (args.strict and warnings):
        print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"Validation passed: {path}")
    if warnings:
        print(f"Warnings: {len(warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
