#!/usr/bin/env python3
"""Aggregate grading and timing files from a skill eval iteration."""
from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any, Dict, List, Optional


def read_json(path: Path) -> Optional[dict[str, Any]]:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return data


def number(value, label: str):
    if value is None:
        return None
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{label}: expected a nonnegative finite number or null")
    return value



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
    allowed = {"with_skill", "without_skill", "old_skill", "previous_skill", "baseline"}
    for eval_dir in sorted(p for p in iteration_dir.iterdir() if p.is_dir()):
        metadata = read_json(eval_dir / "eval_metadata.json") or {}
        for run_dir in sorted(p for p in eval_dir.iterdir() if p.is_dir() and p.name in allowed):
            grading = read_json(run_dir / "grading.json")
            timing = read_json(run_dir / "timing.json") or {}
            provenance = read_json(run_dir / "run_metadata.json") or {}
            expectations = grading.get("expectations") if grading is not None else []
            if not isinstance(expectations, list) or any(not isinstance(item, dict) or type(item.get("passed")) is not bool or not isinstance(item.get("text"), str) or not item["text"].strip() or not isinstance(item.get("evidence"), str) or not item["evidence"].strip() for item in expectations):
                raise ValueError(f"{run_dir}: expectations require text, boolean passed, and evidence")
            texts = [item["text"] for item in expectations]
            if len(texts) != len(set(texts)):
                raise ValueError(f"{run_dir}: duplicate assertions")
            duration = number(timing.get("total_duration_seconds"), "duration")
            if duration is None:
                milliseconds = number(timing.get("duration_ms"), "duration_ms")
                duration = milliseconds / 1000 if milliseconds is not None else None
            runs = configs.setdefault(run_dir.name, [])
            eval_id, trial_id = metadata.get("eval_id", eval_dir.name), metadata.get("trial_id", "1")
            if any(r["eval_id"] == eval_id and r["trial_id"] == trial_id for r in runs):
                raise ValueError(f"{run_dir}: duplicate eval_id/trial_id; give repeats distinct trial_id values")
            total = len(expectations)
            passed = sum(item["passed"] for item in expectations)
            runs.append({
                "eval_id": eval_id, "trial_id": trial_id,
                "eval_name": metadata.get("eval_name", eval_dir.name),
                "run_dir": str(run_dir.relative_to(iteration_dir)),
                "graded": grading is not None, "assertion_texts": sorted(texts),
                "provenance": provenance,
                "assertions_passed": passed, "assertions_total": total,
                "pass_rate": passed / total if total else None,
                "duration_seconds": duration,
                "tokens": number(timing.get("total_tokens"), "total_tokens"),
            })
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
        "ungraded_runs": sum(not r["graded"] for r in runs),
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
    for candidate in ["old_skill", "previous_skill", "baseline", "without_skill"]:
        if candidate in by_name:
            baseline = by_name[candidate]
            break
    if not baseline:
        return []

    def paired(config):
        return {(r["eval_id"], r["trial_id"]): r for r in config["details"]}
    candidate_runs, baseline_runs = paired(target), paired(baseline)
    if candidate_runs.keys() != baseline_runs.keys():
        return []
    for key, candidate in candidate_runs.items():
        previous = baseline_runs[key]
        if not candidate["graded"] or not previous["graded"] or candidate["assertion_texts"] != previous["assertion_texts"]:
            return []
        for field in ("model", "runtime", "settings", "tools"):
            left, right = candidate["provenance"], previous["provenance"]
            if field not in left or field not in right or left[field] is None or right[field] is None or left[field] != right[field]:
                return []
        if any(not isinstance(candidate["provenance"][field], str) or not candidate["provenance"][field].strip() for field in ("model", "runtime")):
            return []
        if not isinstance(candidate["provenance"]["settings"], dict) or not isinstance(candidate["provenance"]["tools"], list):
            return []
        # Cost/time means also need observations from the same paired runs.
        if any((candidate[field] is None) != (previous[field] is None) for field in ("duration_seconds", "tokens")):
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
    lines.extend(["", benchmark["comparison_note"], ""])
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

    try:
        runs_by_config = find_runs(iteration_dir)
        if not runs_by_config:
            raise ValueError("no recognized eval run directories found")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    configs = [summarize_config(name, runs) for name, runs in sorted(runs_by_config.items())]
    order = {"with_skill": 0, "without_skill": 1, "old_skill": 1, "previous_skill": 1, "baseline": 1}
    configs.sort(key=lambda c: (order.get(c["name"], 9), c["name"]))

    benchmark = {
        "skill_name": args.skill_name,
        "iteration": iteration_dir.name,
        "configs": configs,
        "deltas": make_deltas(configs),
    }
    benchmark["comparison_note"] = ("Descriptive paired differences only; inspect artifacts and repeated runs before claiming improvement." if benchmark["deltas"] else "No comparable delta: require paired cases/trials, grading, identical assertions, matched model/runtime/settings/tools, and paired timing/token coverage.")
    (iteration_dir / "benchmark.json").write_text(json.dumps(benchmark, indent=2), encoding="utf-8")
    write_markdown(iteration_dir / "benchmark.md", benchmark)
    print(iteration_dir / "benchmark.json")
    print(iteration_dir / "benchmark.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
