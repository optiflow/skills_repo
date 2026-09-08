# Adapting skills to newer models

Keep the reusable workflow stable and test the instructions whose effect may change. A model upgrade can make a useful old instruction redundant or counterproductive; a shorter prompt is not automatically better either.

## What to inspect

| Observed issue | Candidate correction | Evidence to check |
|---|---|---|
| Pauses before already-requested work | Remove blanket confirmation gates; identify the actual action that needs authorization. | The task finishes within scope and still respects real permission boundaries. |
| Excessive steps, tool calls, or repeat verification | Replace general demands for thoroughness with the required outcome and checks. | Required checks run; latency or tool use falls without a regression. |
| Missing constraints after simplification | Restore the specific invariant at the decision where it matters. | The result preserves the needed format, rule, or action boundary. |
| Too much or too little skill invocation | Make the trigger and adjacent boundary precise; avoid model-independent claims about undertriggering. | Observed host decisions on positive and near-miss cases. |
| Unnecessary delegation | Use independent workers where isolation or separate work adds value. | Better quality or elapsed time after accounting for coordination. |
| Repeated rediscovery or long context loads | Add a focused reference or a tested helper and a clear routing condition. | The agent finds the right resource and uses less irrelevant context. |

These are hypotheses to test, not mandatory additions to every skill. Keep API model settings, effort levels, context management, and installed-tool configuration in the host when that is where they are controlled. A portable skill should not hard-code a new model ID merely because it is newer.

## Model-specific notes checked 2026-09-08

OpenAI's GPT-6 Astra guide flags sensitivity to skill instructions, extra clarification, and excessive testing on small changes. The current Claude Fable 5.1 guide also addresses incomplete follow-through, unsolicited expansion, and scope of tests. These support an audit of permission and process wording before adding more instructions.

Anthropic's Opus 5 guide describes over-verification caused by old self-check prompts. Its general prompting guide warns that aggressive tool-use language can overtrigger some Claude models. Those are model-specific observations; do not assume the same correction is optimal for every host or smaller model.

For each intended model, record the model version, host, settings, tools, task outcomes, and measured cost or time when available. Keep the skill's benefits bounded to the tested cases. Recheck after a material model, host, or tool change; a documentation review is not a runtime benchmark.

See [source notes](source_notes.md) for primary sources and the revisions reviewed.
