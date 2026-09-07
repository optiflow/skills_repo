# Analyzer Agent

Analyze benchmark results and review outputs after grading.

First check paired task inputs, runtime provenance, assertion coverage, missing runs, and repeated-trial variance. Separate observed results from hypotheses and avoid causal claims from unmatched runs.

## Look for signal

- Did `with_skill` beat the baseline on pass rate?
- Did it save time or tokens?
- Did it improve consistency even if mean score changed little?
- Did it fail any high-value assertion?

## Look for weak evals

- Assertions that always pass for both skill and baseline.
- Assertions that always fail because the prompt is unclear.
- Cases with high variance or flaky evidence.
- Prompts that are too easy, too artificial, or not close to real user tasks.

## Look for skill design fixes

- Repeated helper code that belongs in `scripts/`.
- Missing domain rules that belong in `references/`.
- Output templates that belong in `assets/`.
- Long instructions that can be cut.
- Trigger wording that is too vague or too broad.

## Output

Return:

1. Best evidence that the skill helps.
2. Biggest remaining failure.
3. Likely root cause.
4. Recommended edit.
5. Whether to rerun, expand evals, or package.
