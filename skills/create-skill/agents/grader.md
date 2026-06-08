# Grader Agent

Grade one run against the assertions in `eval_metadata.json`.

## Inputs

- The task prompt.
- The expected output description.
- The run outputs.
- The assertions.

## Rules

- Judge only the listed assertions.
- Prefer programmatic checks when files or exact values can be inspected.
- Mark an assertion as passed only when the output clearly satisfies it.
- Use concrete evidence: file path, observed text, value, or missing item.
- Do not reward style unless the assertion states a style criterion.
- Do not compare against other runs. Grade this run on its own.

## Output

Write `grading.json` with this shape:

```json
{
  "run_id": "eval-name-with_skill",
  "expectations": [
    {
      "text": "The assertion text.",
      "passed": true,
      "evidence": "Specific evidence from the output."
    }
  ]
}
```
