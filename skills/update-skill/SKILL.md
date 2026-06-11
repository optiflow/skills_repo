---
name: update-skill
description: Update existing AI agent skills with evidence, version severity, evals, validation, and rollback. Use when the user asks to update, maintain, refresh, version, de-bloat, retest, roll back, or improve a skill; when evals, traces, logs, feedback, incidents, or observed behavior show repeat skill failures; or when the task, environment, risk, output contract, model, runtime, platform, or domain rules changed.
---

# Update Skill

Use this skill to update an existing skill only when evidence or real change shows the current skill no longer helps the agent do the right task reliably, safely, cheaply, and at the right time.

## Workflow

1. **Ground the update.** Inspect the current skill files, user request, available evidence, and repo rules before editing. Preserve the skill name unless the user asks for a rename.
2. **Snapshot the original.** Keep a copy or clear diff of the old skill so it can serve as the baseline and rollback path.
3. **Decide if an update is warranted.** Read `references/update-playbook.md` before choosing update, no-op, split, or tool fix.
4. **Set version severity.** Mark the change as patch, minor, or major before editing. Treat output schema, tool contract, permissions, safety behavior, core workflow, or scope changes as major.
5. **Make the smallest useful change.** Update only the skill surfaces tied to the evidence: description, scope, workflow steps, references, scripts, evals, validation, or safety gates.
6. **Validate against the baseline.** Run structural validation and the smallest realistic eval or reproduction that shows the update improves the old version.
7. **Report the change.** State severity, evidence, changed behavior, validation, rollback path, and remaining risk.

## Resources

- `references/update-playbook.md`: Read before deciding whether to update, assigning version severity, changing risky behavior, splitting bloated skills, or writing the final update report.

## Quality Checks

- Every changed line should trace to a task change, environment change, risk change, output contract change, or repeated failure evidence.
- Do not patch a skill after one odd failure unless the issue is reproduced with a small eval or clear trace.
- Do not add generic "be careful" text unless it changes behavior, validation, permissions, or human review.
- Prefer removing, narrowing, or splitting content over expanding a skill that covers too many jobs.
- Keep time-sensitive facts out of the skill when a current source of truth can be retrieved instead.
