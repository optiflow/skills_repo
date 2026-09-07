# Trigger testing

The description is a discovery interface. Lead with the capability and main context. Add a boundary when it prevents a plausible wrong match. Test actual host behavior before making a claim about routing accuracy.

## Cases and measurements

Use real user language, file names, and partial context. Cover positive requests, requests that never name the skill, competing skills, and close negatives. A few cases are enough for a focused correction; wider release needs enough varied cases to expose missed and unwanted activations.

Keep expected labels separate from observations:

```json
[
  {"id": "invoice-match", "query": "Match July invoices to these payment exports and list the gaps.", "should_trigger": true},
  {"id": "invoice-writing", "query": "Write a polite note asking a customer to pay an invoice.", "should_trigger": false}
]
```

Run each query in the target host with the candidate discoverable and without forcing its invocation. Record whether the host actually loaded it, using the host's invocation or file-read trace. Add `triggered: true` or `triggered: false` only for observed results. Use null or omit the field for unrun or missing observations. A tool error is not automatically a negative decision.

Keep the surrounding skills catalogue stable between descriptions. Explicit mentions such as `$skill-name` check availability and invocation; they do not establish implicit matching quality. Asking an LLM whether a description matches a query is a useful design check, but it is a proxy for host selection.

For manual query editing, an optional [review template](../assets/trigger_eval_review.html) is included. Escape the skill name and description as HTML. Replace its data placeholder with JSON whose `<`, `>`, and `&` characters are escaped as Unicode sequences so query text cannot close the script element. Save the filled template outside the skill. The exported file contains labels and queries, not observed trigger results.

## Avoid test-set leakage

Use development cases to revise descriptions. If comparing several candidates, use separate validation cases to select one. Freeze that description before looking at final test cases. Do not repeatedly choose the highest score on the final test set and still call it held out. If the test set informs another revision, treat it as development evidence and obtain fresh test cases.

Keep duplicate prompts and close paraphrases in the same split. With a tiny set, report it as exploratory rather than implying a reliable estimate. Repeat borderline cases when the host's choices vary.

## Score observations

Run from the create-skill directory, or use the helper's absolute path:

```bash
python -B scripts/score_trigger_evals.py /path/to/trigger-results.json \
  --output /path/to/trigger-score.json
```

The helper scores existing observations; it does not invoke a model, run the host, or optimize descriptions. JSON booleans are required; the strings `"true"` and `"false"` are invalid.

Report coverage with accuracy, precision, recall, specificity, and F1. Missing observations reduce coverage and are excluded from scored outcomes. Undefined metrics are null. Show false positives and false negatives so the user can judge the tradeoff; a high score with low coverage is weak evidence.

Choose a description for the actual task's error costs. More keywords can raise recall while drawing the skill into unrelated tasks. Explain the change and any observed differences; if no host test ran, say the description was reviewed but its routing was not measured.
