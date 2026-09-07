#!/usr/bin/env python3
"""Validate and package a skill as a reproducible .skill ZIP archive."""
from __future__ import annotations
import argparse
import os
import stat
import tempfile
import zipfile
from pathlib import Path
from quick_validate import validate_skill

EXCLUDE_DIRS = {'__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build'}
EXCLUDE_FILES = {'review.html', 'benchmark.json', 'benchmark.md', 'credentials.json'}

def should_skip(path: Path, root: Path, include_evals: bool) -> bool:
    parts = path.relative_to(root).parts
    return (any(p.startswith('.') or p in EXCLUDE_DIRS or p.endswith('-workspace') for p in parts)
            or (not include_evals and parts[0] == 'evals')
            or path.name in EXCLUDE_FILES
            or path.suffix.lower() in {'.pyc', '.pyo', '.skill', '.pem', '.key', '.p12', '.pfx'})

def package_skill(skill_path: Path, package_path: Path, include_evals: bool = False) -> list[str]:
    skill_path, package_path = skill_path.resolve(), package_path.resolve()
    if package_path.is_relative_to(skill_path):
        raise ValueError('output must be outside the skill directory')
    errors, warnings = validate_skill(skill_path)
    if errors:
        raise ValueError('skill validation failed: ' + '; '.join(errors))
    files = sorted((p for p in skill_path.rglob('*') if p.is_file() and not should_skip(p, skill_path, include_evals)), key=lambda p: p.relative_to(skill_path).as_posix())
    package_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.skill-', suffix='.tmp', dir=package_path.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for file in files:
                info = zipfile.ZipInfo((Path(skill_path.name) / file.relative_to(skill_path)).as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                mode = 0o755 if file.stat().st_mode & 0o111 else 0o644
                info.external_attr = (stat.S_IFREG | mode) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, file.read_bytes())
        os.replace(temporary, package_path)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return warnings

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill_path')
    parser.add_argument('--output', default='.', help='Output directory or .skill file outside the skill')
    parser.add_argument('--include-evals', action='store_true')
    args = parser.parse_args()
    source = Path(args.skill_path).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    package = output if output.suffix == '.skill' else output / f'{source.name}.skill'
    try:
        warnings = package_skill(source, package, args.include_evals)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    for warning in warnings:
        print(f'WARNING: {warning}')
    print(package)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
