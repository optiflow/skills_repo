#!/usr/bin/env python3
"""Aggregate grading and timing files from a skill eval iteration."""
from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any, Dict, List, Optional


def read_json(path: Path) -> Optional[dict[str, Any]]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def mean(values: List[float]) -> Optional[float]:
    values = [v for v in values if v is not None]
    return round(statistics.mean(values), 4) if values else None


def stddev(values: List[float]) -> Optional[float]:
    values = [v for v in values if v is not None]
    if len(values) < 2:
        return 0.0 if values else None
    return round(statistics.stdev(values), 4)


def pct(value: Optional[float]) -> str:
    return "n/a" if value is None else f"{value * 100:.1f}%"


def find_runs(iteration_dir: Path) -> Dict[str, list[dict[str, Any]]]:
    configs: Dict[str, list[dict[str, Any]]] = {}
    for eval_dir in sorted(p for p in iteration_dir.iterdir() if p.is_dir()):
        metadata = read_json(eval_dir / "eval_metadata.json") or {}
        for run_dir in sorted(p for p in eval_dir.iterdir() if p.is_dir()):
            grading = read_json(run_dir / "grading.json") or {}
            timing = read_json(run_dir / "timing.json") or {}
            expectations = grading.get("expectations") or []
            total = len(expectations)
            passed = sum(1 for item in expectations if item.get("passed") is True)
            configs.setdefault(run_dir.name, []).append(
                {
                    "eval_id": metadata.get("eval_id") or eval_dir.name,
                    "eval_name": metadata.get("eval_name") or eval_dir.name,
                    "run_dir": str(run_dir.relative_to(iteration_dir)),
                    "assertions_passed": passed,
                    "assertions_total": total,
                    "pass_rate": (passed / total) if total else None,
                    "duration_seconds": timing.get("total_duration_seconds") or (timing.get("duration_ms") / 1000 if timing.get("duration_ms") else None),
                    "tokens": timing.get("total_tokens"),
                }
            )
    return configs


def summarize_config(name: str, runs: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(r["assertions_passed"] for r in runs)
    total = sum(r["assertions_total"] for r in runs)
    pass_rates = [r["pass_rate"] for r in runs if r["pass_rate"] is not None]
    durations = [r["duration_seconds"] for r in runs if r["duration_seconds"] is not None]
    tokens = [r["tokens"] for r in runs if r["tokens"] is not None]
    return {
        "name": name,
        "runs": len(runs),
        "assertions_passed": passed,
        "assertions_total": total,
        "pass_rate": round(passed / total, 4) if total else None,
        "per_eval_pass_rate_mean": mean(pass_rates),
        "per_eval_pass_rate_stddev": stddev(pass_rates),
        "duration_seconds_mean": mean(durations),
        "duration_seconds_stddev": stddev(durations),
        "tokens_mean": mean(tokens),
        "tokens_stddev": stddev(tokens),
        "details": runs,
    }


def make_deltas(configs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_name = {c["name"]: c for c in configs}
    target = by_name.get("with_skill")
    if not target:
        return []
    baseline = None
    for candidate in ["without_skill", "old_skill", "previous_skill", "baseline"]:
        if candidate in by_name:
            baseline = by_name[candidate]
            break
    if not baseline:
        return []

    def diff(field: str):
        a = target.get(field)
        b = baseline.get(field)
        if a is None or b is None:
            return None
        return round(a - b, 4)

    return [
        {
            "from": baseline["name"],
            "to": target["name"],
            "pass_rate_delta": diff("pass_rate"),
            "duration_seconds_delta": diff("duration_seconds_mean"),
            "tokens_delta": diff("tokens_mean"),
        }
    ]


def write_markdown(path: Path, benchmark: dict[str, Any]) -> None:
    lines = [f"# Benchmark: {benchmark['skill_name']}", "", f"Iteration: `{benchmark['iteration']}`", ""]
    lines.append("| Config | Runs | Pass rate | Assertions | Duration mean | Tokens mean |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for c in benchmark["configs"]:
        assertions = f"{c['assertions_passed']}/{c['assertions_total']}" if c["assertions_total"] else "n/a"
        duration = "n/a" if c["duration_seconds_mean"] is None else f"{c['duration_seconds_mean']:.2f}s"
        tokens = "n/a" if c["tokens_mean"] is None else f"{c['tokens_mean']:.0f}"
        lines.append(f"| {c['name']} | {c['runs']} | {pct(c['pass_rate'])} | {assertions} | {duration} | {tokens} |")
    if benchmark["deltas"]:
        lines.extend(["", "## Deltas", ""])
        for d in benchmark["deltas"]:
            lines.append(f"- `{d['to']}` vs `{d['from']}`: pass rate {d['pass_rate_delta']}, duration {d['duration_seconds_delta']}, tokens {d['tokens_delta']}.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("iteration_dir")
    parser.add_argument("--skill-name", default="skill")
    args = parser.parse_args()

    iteration_dir = Path(args.iteration_dir).expanduser().resolve()
    if not iteration_dir.exists():
        parser.error(f"not found: {iteration_dir}")

    runs_by_config = find_runs(iteration_dir)
    configs = [summarize_config(name, runs) for name, runs in sorted(runs_by_config.items())]
    order = {"with_skill": 0, "without_skill": 1, "old_skill": 1, "previous_skill": 1, "baseline": 1}
    configs.sort(key=lambda c: (order.get(c["name"], 9), c["name"]))

    benchmark = {
        "skill_name": args.skill_name,
        "iteration": iteration_dir.name,
        "configs": configs,
        "deltas": make_deltas(configs),
    }
    (iteration_dir / "benchmark.json").write_text(json.dumps(benchmark, indent=2), encoding="utf-8")
    write_markdown(iteration_dir / "benchmark.md", benchmark)
    print(iteration_dir / "benchmark.json")
    print(iteration_dir / "benchmark.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
