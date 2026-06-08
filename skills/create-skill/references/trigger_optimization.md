# Trigger Optimization Reference

The `description` field is the main trigger surface for most skill systems. Optimize it after the skill's task behavior is good.

## Description pattern

A strong description says:

1. What the skill does.
2. What inputs or contexts it handles.
3. What phrases, file types, workflows, or user intents should trigger it.
4. What adjacent cases should still use it even if the user does not name the skill.

Avoid a vague description such as:

```text
Helps with documents.
```

Prefer a concrete description such as:

```text
Create, edit, inspect, and transform professional .docx documents. Use when the user asks to draft, revise, preserve formatting, add comments, handle tracked changes, extract text or tables, or fix Word document structure.
```

## Trigger eval set

Create 16-24 realistic queries:

- 8-12 should-trigger cases.
- 8-12 should-not-trigger cases.
- Include near-misses, not only obvious negatives.
- Include messy real prompts with filenames, partial context, typos, and casual wording.
- Include cases where the user does not name the skill but clearly needs the workflow.

Schema:

```json
[
  {
    "id": "casual-docx-edit",
    "query": "my manager sent me the board paper in /downloads/final_draft.docx and I need the tracked changes accepted but comments kept",
    "should_trigger": true,
    "triggered": true
  },
  {
    "id": "pdf-near-miss",
    "query": "can you summarize this PDF contract and flag risky clauses",
    "should_trigger": false,
    "triggered": false
  }
]
```

The `triggered` field is filled after testing a description.

## Train and held-out split

Use about 60% of cases for improving the description and 40% as held-out tests. Choose the final description by held-out score. This reduces overfitting.

## Metrics

Use `scripts/score_trigger_evals.py` to compute:

- Accuracy: all correct trigger decisions.
- Precision: when it triggered, how often it should have triggered.
- Recall: when it should trigger, how often it did.
- Specificity: when it should not trigger, how often it stayed off.
- F1: balance of precision and recall.

For narrow skills, favor precision. For high-value helper skills where missing the skill is costly, favor recall, but still protect near-miss negatives.

## Iteration rules

When the skill undertriggers, add concrete contexts and common user phrasing.

When the skill overtriggers, add sharper boundaries by naming adjacent tasks that should use a different skill or normal tools.

Do not stuff the description with every keyword. A long, noisy description can harm routing. Use compact clusters of intent.

## Before applying

Show the user:

- Old description.
- New description.
- Trigger eval score changes.
- Any remaining failure cases.
