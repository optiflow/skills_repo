# Evaluation Schemas

Use these shapes for test prompts, run metadata, grading, timing, and benchmark files.

## `evals/evals.json`

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": "extract-table-edge-case",
      "prompt": "The realistic user task prompt.",
      "expected_output": "What a good result should contain or do.",
      "files": [],
      "assertions": [
        {
          "text": "Output includes a CSV file with headers patient_id, age, score.",
          "type": "manual_or_script",
          "evidence_hint": "Check generated CSV header row."
        }
      ]
    }
  ]
}
```

`id` should be descriptive and stable. Avoid `eval-0` as the only name.

`files` may contain paths to input files used by the prompt. Keep test files small and safe to share.

`assertions` should be objective. Do not force assertions onto writing taste, visual design, or strategy advice unless the user gives clear criteria.

## `eval_metadata.json`

Save one file per eval directory.

```json
{
  "eval_id": "extract-table-edge-case",
  "eval_name": "extract-table-edge-case",
  "prompt": "The exact task prompt used for this run.",
  "expected_output": "What good looks like.",
  "assertions": [
    {"text": "The output preserves all rows from the source table."}
  ]
}
```

## Workspace layout

```text
my-skill-workspace/
└── iteration-1/
    ├── benchmark.json
    ├── benchmark.md
    └── extract-table-edge-case/
        ├── eval_metadata.json
        ├── with_skill/
        │   ├── outputs/
        │   ├── timing.json
        │   └── grading.json
        └── without_skill/
            ├── outputs/
            ├── timing.json
            └── grading.json
```

For updates to an existing skill, use `old_skill/` or `previous_skill/` instead of `without_skill/`.

## `timing.json`

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.332
}
```

When token or timing data is unavailable, omit the file or set values to `null`. Do not invent measurements.

## `grading.json`

```json
{
  "run_id": "extract-table-edge-case-with_skill",
  "expectations": [
    {
      "text": "Output includes a CSV file with headers patient_id, age, score.",
      "passed": true,
      "evidence": "outputs/result.csv starts with patient_id,age,score."
    }
  ]
}
```

Use exactly `text`, `passed`, and `evidence` for each expectation. This keeps aggregation and review tooling simple.

## `benchmark.json`

```json
{
  "skill_name": "my-skill",
  "iteration": "iteration-1",
  "configs": [
    {
      "name": "with_skill",
      "runs": 3,
      "assertions_passed": 8,
      "assertions_total": 9,
      "pass_rate": 0.8889,
      "duration_seconds_mean": 21.4,
      "duration_seconds_stddev": 4.2,
      "tokens_mean": 70000,
      "tokens_stddev": 5000
    }
  ],
  "deltas": [
    {
      "from": "without_skill",
      "to": "with_skill",
      "pass_rate_delta": 0.2222,
      "duration_seconds_delta": -3.1,
      "tokens_delta": -4000
    }
  ]
}
```

## Good evals

Good evals are realistic, discriminating, and stable.

- Realistic: They look like real user tasks.
- Discriminating: A weak skill or baseline can fail them.
- Stable: A good run should usually pass for the same reason.
- Covering: They include common cases, edge cases, and near-misses.

A tiny eval set is useful for fast iteration. A larger held-out set is useful before wide rollout.
