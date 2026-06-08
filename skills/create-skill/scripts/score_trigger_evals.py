#!/usr/bin/env python3
"""Score should-trigger / should-not-trigger eval results."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List


def load_items(path: Path) -> List[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("evals") or data.get("items") or data.get("queries")
    if not isinstance(data, list):
        raise ValueError("input must be a list, or an object with evals/items/queries")
    return data


def safe_div(a: int, b: int):
    return round(a / b, 4) if b else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_json", help="JSON list with query, should_trigger, and triggered fields")
    parser.add_argument("--output", help="Optional output JSON path")
    args = parser.parse_args()

    path = Path(args.results_json).expanduser().resolve()
    try:
        items = load_items(path)
    except Exception as exc:
        parser.error(str(exc))

    tp = fp = tn = fn = missing = 0
    failures = []
    for item in items:
        if "should_trigger" not in item or "triggered" not in item:
            missing += 1
            continue
        should = bool(item["should_trigger"])
        got = bool(item["triggered"])
        if should and got:
            tp += 1
        elif should and not got:
            fn += 1
            failures.append({"id": item.get("id"), "query": item.get("query"), "expected": True, "observed": False})
        elif not should and got:
            fp += 1
            failures.append({"id": item.get("id"), "query": item.get("query"), "expected": False, "observed": True})
        else:
            tn += 1

    total = tp + fp + tn + fn
    score = {
        "total_scored": total,
        "missing_triggered_or_should_trigger": missing,
        "true_positive": tp,
        "false_positive": fp,
        "true_negative": tn,
        "false_negative": fn,
        "accuracy": safe_div(tp + tn, total),
        "precision": safe_div(tp, tp + fp),
        "recall": safe_div(tp, tp + fn),
        "specificity": safe_div(tn, tn + fp),
        "f1": round(2 * tp / (2 * tp + fp + fn), 4) if (2 * tp + fp + fn) else None,
        "failures": failures,
    }

    text = json.dumps(score, indent=2)
    if args.output:
        out = Path(args.output).expanduser().resolve()
        out.write_text(text + "\n", encoding="utf-8")
        print(out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
