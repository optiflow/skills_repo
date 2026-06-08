#!/usr/bin/env python3
"""Initialize a lean, testable AI-agent skill folder."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$|^[a-z0-9]$")
ALLOWED_RESOURCES = {"scripts", "references", "assets"}


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def yaml_quote(value: str) -> str:
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{value}"'


def create_skill_md(name: str, description: str) -> str:
    return f"""---
name: {name}
description: {description}
---

# {title_from_name(name)}

State the outcome this skill produces in one short paragraph.

## Workflow

1. Confirm the user's goal, inputs, output format, and constraints from the conversation.
2. Use the bundled resources listed below only when they match the task.
3. Produce the requested output and call out any limits or assumptions.

## Bundled resources

Replace this section with direct links to any files you add.

- `scripts/`: Use for deterministic or repeated operations.
- `references/`: Read for detailed domain rules, schemas, examples, or API notes.
- `assets/`: Use for templates or files copied into outputs.

## Quality checks

- Validate inputs before transforming files or data.
- Preserve user-provided constraints and formats.
- Test important scripts with representative inputs.
"""


def create_evals_json(name: str) -> str:
    return """{
  "skill_name": "%s",
  "evals": [
    {
      "id": "core-workflow",
      "prompt": "Replace with a realistic user request that should use this skill.",
      "expected_output": "Describe what a good result should contain.",
      "files": [],
      "assertions": [
        {"text": "Replace with an objective assertion when possible."}
      ]
    },
    {
      "id": "edge-case",
      "prompt": "Replace with a realistic edge case or messy user request.",
      "expected_output": "Describe what a good result should contain.",
      "files": [],
      "assertions": []
    }
  ]
}
""" % name


def create_openai_yaml(display_name: str, short_description: str, default_prompt: str) -> str:
    return (
        f"display_name: {yaml_quote(display_name)}\n"
        f"short_description: {yaml_quote(short_description)}\n"
        f"default_prompt: {yaml_quote(default_prompt)}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Skill name, lower-case letters/digits/hyphens only")
    parser.add_argument("--path", required=True, help="Parent directory where the skill folder will be created")
    parser.add_argument("--description", help="Frontmatter description. Include what the skill does and when to use it.")
    parser.add_argument("--resources", default="", help="Comma-separated resource dirs: scripts,references,assets")
    parser.add_argument("--evals", action="store_true", help="Create evals/evals.json scaffold")
    parser.add_argument("--openai-agent", action="store_true", help="Create agents/openai.yaml UI metadata")
    parser.add_argument("--display-name", help="Display name for agents/openai.yaml")
    parser.add_argument("--short-description", help="Short description for agents/openai.yaml")
    parser.add_argument("--default-prompt", help="Default prompt for agents/openai.yaml")
    parser.add_argument("--force", action="store_true", help="Allow writing into an existing empty directory")
    args = parser.parse_args()

    name = args.name.strip()
    if not NAME_RE.fullmatch(name):
        parser.error("name must use lowercase letters, digits, and hyphens; keep it under 64 characters")

    parent = Path(args.path).expanduser().resolve()
    skill_dir = parent / name
    if skill_dir.exists() and any(skill_dir.iterdir()) and not args.force:
        parser.error(f"target already exists and is not empty: {skill_dir}")
    skill_dir.mkdir(parents=True, exist_ok=True)

    description = args.description or (
        f"Use this skill to perform the {name.replace('-', ' ')} workflow. "
        "Replace this description with concrete trigger contexts, file types, user phrases, and expected tasks."
    )
    (skill_dir / "SKILL.md").write_text(create_skill_md(name, description), encoding="utf-8")

    resources = {r.strip() for r in args.resources.split(",") if r.strip()}
    unknown = resources - ALLOWED_RESOURCES
    if unknown:
        parser.error(f"unknown resource dirs: {', '.join(sorted(unknown))}")
    for resource in sorted(resources):
        (skill_dir / resource).mkdir(exist_ok=True)

    if args.evals:
        (skill_dir / "evals").mkdir(exist_ok=True)
        (skill_dir / "evals" / "evals.json").write_text(create_evals_json(name), encoding="utf-8")

    if args.openai_agent:
        display = args.display_name or title_from_name(name)
        short = args.short_description or description.split(".")[0][:90]
        default = args.default_prompt or f"Use the {title_from_name(name)} skill to complete this task."
        (skill_dir / "agents").mkdir(exist_ok=True)
        (skill_dir / "agents" / "openai.yaml").write_text(create_openai_yaml(display, short, default), encoding="utf-8")

    print(skill_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
