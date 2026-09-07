#!/usr/bin/env python3
"""Generate a static HTML review page for one skill eval iteration."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any, Optional

TEXT_EXTS = {".txt", ".md", ".json", ".csv", ".py", ".yaml", ".yml", ".html", ".xml", ".log"}


def read_json(path: Path) -> Optional[dict[str, Any]]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def render_file(path: Path, root: Path) -> str:
    rel = html.escape(str(path.relative_to(root)))
    if path.suffix.lower() in TEXT_EXTS and path.stat().st_size <= 200_000:
        text = path.read_text(encoding="utf-8", errors="replace")
        return f"<details open><summary>{rel}</summary><pre>{html.escape(text)}</pre></details>"
    return f"<p><code>{rel}</code> ({path.stat().st_size} bytes)</p>"


def render_outputs(outputs: Path, run_root: Path) -> str:
    if not outputs.exists():
        return "<p><em>No outputs directory found.</em></p>"
    files = [p for p in sorted(outputs.rglob("*")) if p.is_file()]
    if not files:
        return "<p><em>No output files found.</em></p>"
    return "\n".join(render_file(p, run_root) for p in files)


def render_grading(run_dir: Path) -> str:
    grading = read_json(run_dir / "grading.json")
    if not grading:
        return "<p><em>Ungraded run; no pass rate is implied.</em></p>"
    rows = []
    for item in grading.get("expectations", []):
        status = "PASS" if item.get("passed") is True else "FAIL"
        rows.append(
            "<tr>"
            f"<td>{html.escape(status)}</td>"
            f"<td>{html.escape(str(item.get('text','')))}</td>"
            f"<td>{html.escape(str(item.get('evidence','')))}</td>"
            "</tr>"
        )
    return "<table><tr><th>Status</th><th>Assertion</th><th>Evidence</th></tr>" + "".join(rows) + "</table>"


def render_benchmark(path: Optional[Path]) -> str:
    if not path or not path.exists():
        return "<p><em>No benchmark file supplied.</em></p>"
    data = read_json(path)
    if not data:
        return "<p><em>Benchmark file could not be parsed.</em></p>"
    rows = []
    for c in data.get("configs", []):
        pr = c.get("pass_rate")
        pass_rate = "n/a" if pr is None else f"{pr*100:.1f}%"
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(c.get('name')))}</td>"
            f"<td>{html.escape(str(c.get('runs')))}</td>"
            f"<td>{pass_rate}</td>"
            f"<td>{html.escape(str(c.get('assertions_passed')))}/{html.escape(str(c.get('assertions_total')))}</td>"
            f"<td>{html.escape(str(c.get('duration_seconds_mean')))}</td>"
            f"<td>{html.escape(str(c.get('tokens_mean')))}</td>"
            "</tr>"
        )
    note = html.escape(str(data.get("comparison_note", "Inspect run provenance before comparing results.")))
    return f"<p>{note}</p>" + "<table><tr><th>Config</th><th>Runs</th><th>Pass rate</th><th>Assertions</th><th>Duration mean</th><th>Tokens mean</th></tr>" + "".join(rows) + "</table>"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("iteration_dir")
    parser.add_argument("--skill-name", default="skill")
    parser.add_argument("--benchmark", help="Path to benchmark.json")
    parser.add_argument("--static", help="Output HTML path. Defaults to iteration_dir/review.html")
    args = parser.parse_args()

    iteration_dir = Path(args.iteration_dir).expanduser().resolve()
    benchmark_path = Path(args.benchmark).expanduser().resolve() if args.benchmark else iteration_dir / "benchmark.json"
    out = Path(args.static).expanduser().resolve() if args.static else iteration_dir / "review.html"

    sections = []
    for eval_dir in sorted(p for p in iteration_dir.iterdir() if p.is_dir()):
        meta = read_json(eval_dir / "eval_metadata.json") or {}
        sections.append(f"<section><h2>{html.escape(meta.get('eval_name') or eval_dir.name)}</h2>")
        if meta.get("prompt"):
            sections.append(f"<h3>Prompt</h3><pre>{html.escape(meta['prompt'])}</pre>")
        for run_dir in sorted(p for p in eval_dir.iterdir() if p.is_dir()):
            sections.append(f"<h3>{html.escape(run_dir.name)}</h3>")
            sections.append(render_grading(run_dir))
            sections.append(render_outputs(run_dir / "outputs", run_dir))
        sections.append("</section>")

    doc = f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><title>Skill Review - {html.escape(args.skill_name)}</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:1200px;margin:2rem auto;padding:0 1rem;line-height:1.45}}
section{{border:1px solid #ddd;border-radius:10px;padding:1rem;margin:1.25rem 0}}
pre{{white-space:pre-wrap;background:#f6f6f6;padding:1rem;border-radius:8px;overflow:auto}}
table{{border-collapse:collapse;width:100%;margin:.75rem 0}} th,td{{border:1px solid #ddd;padding:.5rem;vertical-align:top}} th{{background:#f6f6f6}}
summary{{cursor:pointer;font-weight:600}}
</style></head><body>
<h1>Skill Review: {html.escape(args.skill_name)}</h1>
<p>Iteration: <code>{html.escape(iteration_dir.name)}</code></p>
<h2>Benchmark</h2>
{render_benchmark(benchmark_path)}
<h2>Outputs</h2>
{''.join(sections) if sections else '<p><em>No eval directories found.</em></p>'}
</body></html>
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
