#!/usr/bin/env python3
"""Create or update agents/openai.yaml for a skill."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def yaml_quote(value: str) -> str:
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{value}"'


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}
    out: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            out[key.strip()] = val.strip().strip('"').strip("'")
    return out


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_path")
    parser.add_argument("--interface", action="append", default=[], help="key=value. Common keys: display_name, short_description, default_prompt, icon, brand_color")
    args = parser.parse_args()

    skill_path = Path(args.skill_path).expanduser().resolve()
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        parser.error("SKILL.md not found")

    fm = parse_frontmatter(skill_md)
    values: dict[str, str] = {}
    for pair in args.interface:
        if "=" not in pair:
            parser.error(f"--interface must be key=value: {pair}")
        key, value = pair.split("=", 1)
        values[key.strip()] = value.strip()

    name = fm.get("name", skill_path.name)
    description = fm.get("description", "")
    values.setdefault("display_name", title_from_name(name))
    values.setdefault("short_description", (description.split(".")[0] or f"Use {title_from_name(name)}")[:100])
    values.setdefault("default_prompt", f"Use the {title_from_name(name)} skill to complete this task.")

    allowed = ["display_name", "short_description", "default_prompt", "icon", "brand_color"]
    lines = []
    for key in allowed:
        if key in values and values[key]:
            lines.append(f"{key}: {yaml_quote(values[key])}")
    (skill_path / "agents").mkdir(exist_ok=True)
    out = skill_path / "agents" / "openai.yaml"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
