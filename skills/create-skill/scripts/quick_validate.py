#!/usr/bin/env python3
"""Check portable metadata and resources; this is not a behavioral or security audit."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
try:
    import yaml
except ImportError:
    raise SystemExit('PyYAML is required. Install scripts/requirements.txt in your chosen Python environment.')

NAME_RE = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
TEXT_EXTS = {'.md', '.py', '.json', '.yaml', '.yml', '.txt', '.html', '.sh'}
ALLOWED_ROOT = {'SKILL.md', 'scripts', 'references', 'assets', 'agents', 'evals', 'LICENSE', 'LICENSE.txt', 'LICENSE.md', 'NOTICE'}
SECRET_PATTERNS = [re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{20,}"), re.compile(r'sk-(?:proj-)?[A-Za-z0-9_-]{20,}'), re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]
PLACEHOLDERS = ('[TODO:', 'Replace this description with', 'State the outcome this skill produces in one short paragraph.', 'Replace this section with direct links')

class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently overwriting them."""

def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError('YAML mapping keys must be strings')
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result

UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def load_yaml_mapping(text: str) -> dict:
    data = yaml.load(text, Loader=UniqueKeyLoader)
    if not isinstance(data, dict):
        raise ValueError('YAML must be a mapping')
    return data

def valid_name(name) -> bool:
    return isinstance(name, str) and 1 <= len(name) <= 64 and bool(NAME_RE.fullmatch(name))

def read_frontmatter(skill_md: Path) -> tuple[dict, str, list[str]]:
    try:
        text = skill_md.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as exc:
        return {}, '', [f'cannot read SKILL.md: {exc}']
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        return {}, text, ['SKILL.md must start with YAML frontmatter delimited by ---']
    end = next((i for i in range(1, len(lines)) if lines[i] == '---'), None)
    if end is None:
        return {}, text, ['SKILL.md frontmatter is missing closing ---']
    body = '\n'.join(lines[end + 1:])
    try:
        return load_yaml_mapping('\n'.join(lines[1:end])), body, []
    except (yaml.YAMLError, ValueError) as exc:
        return {}, body, [f'invalid frontmatter: {exc}']

def validate_evals(path: Path) -> list[str]:
    file = path / 'evals' / 'evals.json'
    if not file.exists():
        return []
    try:
        data = json.loads(file.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError) as exc:
        return [f'invalid evals/evals.json: {exc}']
    if not isinstance(data, dict) or data.get('skill_name') != path.name or not isinstance(data.get('evals'), list):
        return ['evals/evals.json needs a matching skill_name and an evals list']
    errors, ids = [], set()
    for i, item in enumerate(data['evals']):
        if not isinstance(item, dict):
            errors.append(f'evals[{i}] must be an object')
            continue
        ident = item.get('id')
        if not isinstance(ident, str) or not ident.strip() or ident in ids:
            errors.append(f'evals[{i}] needs a unique, nonempty string id')
        else:
            ids.add(ident)
        prompt = item.get('prompt')
        if not isinstance(prompt, str) or not prompt.strip() or prompt.startswith('Replace with') or '[TODO:' in prompt:
            errors.append(f'evals[{i}] needs a real, nonempty prompt')
        assertions = item.get('assertions', [])
        if not isinstance(assertions, list) or any(not isinstance(a, dict) or not isinstance(a.get('text'), str) or not a['text'].strip() for a in assertions):
            errors.append(f'evals[{i}].assertions must contain objects with nonempty text')
        files = item.get('files', [])
        if not isinstance(files, list) or any(not isinstance(f, str) for f in files):
            errors.append(f'evals[{i}].files must be a list of paths')
    return errors

def validate_openai(path: Path, name: str) -> list[str]:
    file = path / 'agents' / 'openai.yaml'
    if not file.exists():
        return []
    try:
        data = load_yaml_mapping(file.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        return [f'invalid agents/openai.yaml: {exc}']
    errors = []
    if set(data) & {'display_name', 'short_description', 'default_prompt', 'icon', 'brand_color'}:
        errors.append('OpenAI UI fields belong under interface; use icon_small/icon_large for icons')
    interface = data.get('interface', {})
    if not isinstance(interface, dict):
        return errors + ['openai.yaml interface must be a mapping']
    for key, value in interface.items():
        if not isinstance(value, str) or not value.strip():
            errors.append(f'interface.{key} must be a nonempty string')
    short = interface.get('short_description')
    if isinstance(short, str) and not 25 <= len(short) <= 64:
        errors.append('interface.short_description must be 25-64 characters')
    prompt = interface.get('default_prompt')
    if isinstance(prompt, str) and not re.search(r'\$' + re.escape(name) + r'(?![a-z0-9-])', prompt):
        errors.append('interface.default_prompt must mention $' + name)
    policy = data.get('policy', {})
    if not isinstance(policy, dict) or ('allow_implicit_invocation' in policy and type(policy['allow_implicit_invocation']) is not bool):
        errors.append('policy.allow_implicit_invocation must be a YAML boolean')
    return errors

def validate_skill(path: Path) -> tuple[list[str], list[str]]:
    path = Path(path).resolve()
    if not path.is_dir() or not (path / 'SKILL.md').is_file():
        return ['a skill directory containing SKILL.md is required'], []
    links = [str(p.relative_to(path)) for p in path.rglob('*') if p.is_symlink()]
    if links:
        return ['nested symlinks are not validated; copy intended files: ' + ', '.join(links)], []
    fm, body, errors = read_frontmatter(path / 'SKILL.md')
    warnings = []
    name, description = fm.get('name'), fm.get('description')
    if not valid_name(name):
        errors.append('name must be 1-64 lowercase ASCII letters/digits with single internal hyphens')
    elif name != path.name:
        errors.append('folder name must match frontmatter name')
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append('description must be a nonempty string of at most 1024 characters')
    if 'compatibility' in fm and (not isinstance(fm['compatibility'], str) or not 1 <= len(fm['compatibility'].strip()) <= 500):
        errors.append('compatibility must be a nonempty string of at most 500 characters')
    for field in ('license', 'allowed-tools'):
        if field in fm and not isinstance(fm[field], str):
            errors.append(f'{field} must be a string')
    metadata = fm.get('metadata', {})
    if not isinstance(metadata, dict) or any(not isinstance(v, str) for v in metadata.values()):
        errors.append('metadata must map string keys to string values')
    unknown = set(fm) - {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
    if unknown:
        warnings.append('host-specific frontmatter needs target-host review: ' + ', '.join(sorted(unknown)))
    if not body.strip():
        errors.append('SKILL.md needs instructions after frontmatter')
    if any(marker in body or (isinstance(description, str) and marker in description) for marker in PLACEHOLDERS):
        errors.append('SKILL.md contains unfinished scaffold placeholders')
    if len(body.splitlines()) > 500:
        warnings.append('body exceeds the 500-line guidance; consider moving conditional detail')
    for child in path.iterdir():
        if child.name not in ALLOWED_ROOT and not child.name.startswith('.'):
            warnings.append(f'review purpose of root item: {child.name}')
    for file in path.rglob('*.md'):
        contents = file.read_text(encoding='utf-8')
        contents = re.sub(r'(?ms)^\s*(```|~~~).*?^\s*\1[^\n]*$', '', contents)
        for target in re.findall(r'\]\(([^\s)]+)\)', contents):
            parsed = urlsplit(target.strip('<>'))
            if parsed.scheme or not parsed.path:
                continue
            dest = (file.parent / unquote(parsed.path)).resolve()
            if not dest.is_relative_to(path) or not dest.exists():
                errors.append(f'broken or external local link in {file.relative_to(path)}: {target}')
    scripts = path / 'scripts'
    for script in scripts.rglob('*.py') if scripts.exists() else []:
        try:
            compile(script.read_bytes(), str(script), 'exec')
        except (SyntaxError, OSError) as exc:
            errors.append(f'Python syntax/read error in {script.relative_to(path)}: {exc}')
    for file in path.rglob('*'):
        if file.is_file() and file.suffix.lower() in TEXT_EXTS:
            text = file.read_text(encoding='utf-8', errors='replace')
            if any(pattern.search(text) for pattern in SECRET_PATTERNS):
                errors.append(f'possible secret in {file.relative_to(path)}')
    errors.extend(validate_evals(path))
    errors.extend(validate_openai(path, name if isinstance(name, str) else path.name))
    return errors, warnings

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill_path')
    parser.add_argument('--strict', action='store_true', help='Treat review warnings as errors')
    args = parser.parse_args()
    try:
        errors, warnings = validate_skill(Path(args.skill_path).expanduser())
    except (OSError, UnicodeError) as exc:
        errors, warnings = [str(exc)], []
    for warning in warnings:
        print(f'WARNING: {warning}')
    for error in errors:
        print(f'ERROR: {error}')
    failed = bool(errors or (args.strict and warnings))
    print(f"Validation {'failed' if failed else 'passed'}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return int(failed)

if __name__ == '__main__':
    raise SystemExit(main())
