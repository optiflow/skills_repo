---
name: back-brief
description: Create a concise execution-focused understanding check before material action. Use when a task is ambiguous, risky, multi-step, file-changing, high-cost, delegated, incident-related, handoff-heavy, or when the user asks to back-brief, confirm understanding, read back critical items, restate requirements, summarize the mission, or say the task back before executing.
---

# Back Brief

Use this skill to expose your execution model before material work. Do not simply summarize the request. State what you think the user wants, how you plan to act, what you assume, and what must be confirmed before you proceed.

## Material Task Gate

Use this skill for material tasks:

- Ambiguous or incomplete requirements.
- Multi-step implementation, research, analysis, or planning.
- File edits, code changes, migrations, deploys, purchases, messages, or other side effects.
- Incident response, handoffs, async coordination, delegated work, or work with unclear owners.
- Work that could waste time, money, or user trust if misunderstood.
- Any request to back-brief, confirm understanding, read back critical items, restate requirements, or summarize the mission.

Do not use this skill for trivial one-step read-only requests unless the user asks for it.

## Brief Type

Classify the exchange before writing:

- `Confirmation brief`: use right after tasking when the user only needs a receipt and intent check.
- `Back brief`: use after minimal planning, before material action, to show how you intend to execute.
- `Readback`: use for exact critical items such as commands, dates, amounts, destructive actions, permissions, stop conditions, or safety limits.
- `Debrief`: use after action for learning; do not treat it as approval to execute new work.

If the request is broad or risky, a short confirmation brief can come before the back brief. If exact critical items matter, include a readback inside `Open points`.

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
- `Open points`: Assumptions, risks, dependencies, authority, decisions, contradictions, or missing details that could change the work.

Ask only for missing context that could change execution. Useful checks include audience, desired end state, constraints, dependencies, approval authority, sensitivity, and stop conditions. Label inferred facts as assumptions.

## Stop Rule

After the back-brief, stop and wait for the user to explicitly confirm, correct, or escalate before material execution. Do not treat silence as approval.

Do not edit files, run mutating commands, deploy, spend money, send messages, or call side-effect tools until the user confirms or corrects the back-brief.

If the user corrects the task and the change is material, treat the correction as the source of truth. Send a revised back brief and call out what changed before execution.

## Source Notes

Read `references/backbriefing.md` when you need the source-backed rationale, scenario templates, failure modes, metrics, or wording guardrails for back-briefing.
