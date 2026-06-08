---
name: back-brief
description: Confirm task intent before material execution. Use when a task is ambiguous, risky, multi-step, file-changing, high-cost, or when the user asks to back-brief, confirm understanding, restate requirements, summarize the mission, or say the task back before executing.
---

# Back Brief

Use this skill to prove understanding before doing material work. Back-brief the task in your own words, translate the user's intent into concrete action, then wait for confirmation or correction.

## Material Task Gate

Use this skill for material tasks:

- Ambiguous or incomplete requirements.
- Multi-step implementation, research, analysis, or planning.
- File edits, code changes, migrations, deploys, purchases, messages, or other side effects.
- Work that could waste time, money, or user trust if misunderstood.
- Any request to back-brief, confirm understanding, restate requirements, or summarize the mission.

Do not use this skill for trivial one-step read-only requests unless the user asks for it.

## Back-Brief Format

Keep the back-brief short and concrete:

```text
Goal: ...
Done when: ...
Constraints: ...
Plan: ...
Open points: ...
```

- `Goal`: What you think the user wants.
- `Done when`: Concrete success checks.
- `Constraints`: Files, scope, non-goals, style, safety limits, and user preferences.
- `Plan`: Short execution steps.
- `Open points`: Assumptions, risks, and questions that could change the work.

## Stop Rule

After the back-brief, stop and wait for the user to confirm or correct it before material execution.

Do not edit files, run mutating commands, deploy, spend money, send messages, or call side-effect tools until the user confirms or corrects the back-brief.

If the user corrects the task and the change is material, treat the correction as the source of truth and back-brief the corrected task before execution.

## Source Notes

Read `references/backbriefing.md` when you need the source-backed rationale, wording, or guardrails for back-briefing.
