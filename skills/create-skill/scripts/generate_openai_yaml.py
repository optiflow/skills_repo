#!/usr/bin/env python3
"""Merge OpenAI interface fields, preserving policy, dependencies, and other settings."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from quick_validate import load_yaml_mapping, read_frontmatter, valid_name, yaml

INTERFACE_FIELDS = {'display_name', 'short_description', 'default_prompt', 'icon_small', 'icon_large', 'brand_color'}
class Quoted(str):
    pass
class ValueDumper(yaml.SafeDumper):
    pass
ValueDumper.add_representer(Quoted, lambda dumper, value: dumper.represent_scalar('tag:yaml.org,2002:str', value, style='"'))

def dump_yaml(data: dict) -> str:
    def quote_values(value):
        if isinstance(value, dict):
            return {k: quote_values(v) for k, v in value.items()}
        if isinstance(value, list):
            return [quote_values(v) for v in value]
        return Quoted(value) if isinstance(value, str) else value
    return yaml.dump(quote_values(data), Dumper=ValueDumper, sort_keys=False, allow_unicode=True)

def build_metadata(name: str, description: str, overrides: dict, existing: dict | None = None) -> dict:
    unknown = set(overrides) - INTERFACE_FIELDS
    if unknown:
        raise ValueError('unknown interface fields: ' + ', '.join(sorted(unknown)))
    data = dict(existing or {})
    interface = data.get('interface', {})
    if not isinstance(interface, dict):
        raise ValueError('existing interface must be a mapping')
    interface = dict(interface)
    for key in INTERFACE_FIELDS:
        if key in data:
            interface.setdefault(key, data.pop(key))
    if 'icon' in data or 'icon' in interface:
        raise ValueError('legacy icon is ambiguous; choose icon_small or icon_large in the existing file')
    display = ' '.join(part.capitalize() for part in name.split('-'))
    short = ' '.join(description.split())[:64].rstrip()
    if len(short) < 25:
        short = f'Use {display} for its defined workflow'[:64]
    defaults = {'display_name': display, 'short_description': short, 'default_prompt': f'Use ${name} to complete this task.'}
    for key, value in defaults.items():
        interface.setdefault(key, value)
    interface.update(overrides)
    if any(not isinstance(v, str) or not v.strip() for v in interface.values()):
        raise ValueError('interface values must be nonempty strings')
    if not 25 <= len(interface['short_description']) <= 64:
        raise ValueError('short_description must be 25-64 characters')
    if not re.search(r'\$' + re.escape(name) + r'(?![a-z0-9-])', interface['default_prompt']):
        raise ValueError('default_prompt must mention $' + name)
    return {'interface': interface, **{k: v for k, v in data.items() if k != 'interface'}}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill_path')
    parser.add_argument('--interface', action='append', default=[], help='key=value; only supplied fields change in existing metadata')
    args = parser.parse_args()
    path = Path(args.skill_path).expanduser().resolve()
    try:
        fm, _, errors = read_frontmatter(path / 'SKILL.md')
        if errors or not valid_name(fm.get('name')) or not isinstance(fm.get('description'), str):
            raise ValueError('valid SKILL.md name and description required: ' + '; '.join(errors))
        overrides = {}
        for pair in args.interface:
            if '=' not in pair:
                raise ValueError('--interface must be key=value')
            key, value = pair.split('=', 1)
            overrides[key.strip()] = value
        out = path / 'agents' / 'openai.yaml'
        existing = load_yaml_mapping(out.read_text(encoding='utf-8')) if out.exists() else None
        data = build_metadata(fm['name'], fm['description'], overrides, existing)
        out.parent.mkdir(exist_ok=True)
        out.write_text(dump_yaml(data), encoding='utf-8')
    except (ValueError, OSError, yaml.YAMLError) as exc:
        parser.error(str(exc))
    print(out)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
