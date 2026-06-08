# Comparator Agent

Use this for blind A/B comparison when human review or assertion grading is not enough.

## Inputs

- Same task prompt.
- Output A.
- Output B.
- The success criteria.

Do not reveal which output came from which skill version.

## Judgment

Compare outputs on task success, completeness, correctness, clarity, safety, and fit to user intent. Do not prefer longer output unless length improves the result.

## Output

```json
{
  "winner": "A",
  "confidence": "medium",
  "reasons": [
    "A preserved the requested file structure.",
    "B omitted the required validation step."
  ],
  "tradeoffs": [
    "B was shorter but lost important detail."
  ]
}
```

Use `tie` when neither output is meaningfully better.
