#!/usr/bin/env python3
"""Initialize a skill draft without replacing an existing skill."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from generate_openai_yaml import build_metadata, dump_yaml
from quick_validate import valid_name

ALLOWED_RESOURCES = {'scripts', 'references', 'assets'}

def create_skill_md(name: str, description: str) -> str:
    frontmatter = dump_yaml({'name': name, 'description': description})
    title = ' '.join(part.capitalize() for part in name.split('-'))
    return f'---\n{frontmatter}---\n\n# {title}\n\n[TODO: Define the outcome, task-specific constraints, and the smallest useful workflow. Link only resources this skill needs.]\n'

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name')
    parser.add_argument('--path', required=True, help='Parent directory for the new skill')
    parser.add_argument('--description', help='What the skill does and when it applies')
    parser.add_argument('--resources', default='', help='Comma-separated scripts,references,assets; none by default')
    parser.add_argument('--evals', action='store_true')
    parser.add_argument('--openai-agent', action='store_true')
    parser.add_argument('--display-name')
    parser.add_argument('--short-description')
    parser.add_argument('--default-prompt')
    parser.add_argument('--force', action='store_true', help='Allow an existing empty directory; never overwrite files')
    args = parser.parse_args()
    name = args.name
    if not valid_name(name):
        parser.error('name must be 1-64 lowercase ASCII letters/digits with single internal hyphens')
    resources = {r.strip() for r in args.resources.split(',') if r.strip()}
    if resources - ALLOWED_RESOURCES:
        parser.error('unknown resource dirs: ' + ', '.join(sorted(resources - ALLOWED_RESOURCES)))
    description = args.description or '[TODO: Describe the capability and its main trigger.]'
    if not description.strip() or len(description) > 1024:
        parser.error('description must be 1-1024 characters')
    interface_args = {key: getattr(args, key) for key in ('display_name', 'short_description', 'default_prompt') if getattr(args, key) is not None}
    if interface_args and not args.openai_agent:
        parser.error('UI fields require --openai-agent')
    try:
        metadata = build_metadata(name, description, interface_args) if args.openai_agent else None
    except ValueError as exc:
        parser.error(str(exc))
    target = Path(args.path).expanduser().resolve() / name
    if target.is_symlink() or (target.exists() and (not target.is_dir() or not args.force or any(target.iterdir()))):
        parser.error('target exists; --force permits only an empty directory')
    target.mkdir(parents=True, exist_ok=args.force)
    (target / 'SKILL.md').write_text(create_skill_md(name, description), encoding='utf-8')
    for resource in sorted(resources):
        (target / resource).mkdir()
    if args.evals:
        (target / 'evals').mkdir()
        data = {'skill_name': name, 'evals': [{'id': 'core-workflow', 'prompt': '[TODO: Add a realistic request and input fixture.]', 'expected_output': '[TODO: Define observable success.]', 'files': [], 'assertions': []}]}
        (target / 'evals' / 'evals.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    if metadata:
        (target / 'agents').mkdir()
        (target / 'agents' / 'openai.yaml').write_text(dump_yaml(metadata), encoding='utf-8')
    print(f'Created draft: {target}\nReplace the TODO markers before validation or packaging.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
