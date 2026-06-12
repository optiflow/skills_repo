# Back-Briefing Notes

Use this reference when you need the rationale, scenario patterns, failure checks, or wording guardrails for the `back-brief` workflow.

## Source Basis

- U.S. Army FM 6-0 defines a back brief as a subordinate briefing the commander on how they intend to accomplish the mission. The useful point for agents: it checks execution understanding, not just receipt.
- FM 6-0 distinguishes a confirmation brief from a back brief. A confirmation brief verifies receipt and intent right after tasking. A back brief follows enough planning to show the intended approach.
- ADP 6-0 frames shared understanding as essential and perishable. Agents should expose assumptions early because users cannot correct hidden task models.
- FAA Order JO 7110.65BB supplies the readback pattern: exact critical items must be acknowledged and checked, especially when safety, dates, amounts, permissions, or stop conditions matter.
- Human-AI and team research on shared mental models and closed-loop communication supports the same rule: teams fail when people think they agree but hold different plans, constraints, or facts.

Older public explanations from Fivecoat Consulting Group and Workz also describe back-briefing as saying the task and plan back in the receiver's own words so the leader can correct gaps before work starts.

## Concepts

| Concept | Timing | Main check | Best use |
|---|---|---|---|
| Confirmation brief | Right after tasking | Did I receive the task, intent, and key constraints? | Fast alignment before planning |
| Back brief | After minimal planning, before execution | How do I intend to do the work? | Material tasks, handoffs, project kickoff |
| Readback | During live or risky instruction exchange | Did I get the exact critical item right? | Commands, dates, money, deletion, stop conditions |
| Debrief | After action | What happened and what should change? | Learning, not pre-action approval |

Use the lightest form that controls the risk. A risky task may need all three pre-action moves: confirmation brief, back brief, and readback of the critical item.

## Core Model

1. The requester gives intent, task, or direction.
2. The receiver checks whether the task type and risk are clear.
3. The receiver asks only for missing context that could change execution.
4. The receiver states the execution model: goal, success, constraints, plan, and open points.
5. The requester confirms, corrects, or escalates.
6. If corrected, the receiver revises the brief and marks what changed.
7. Material action starts only after explicit closure.

## Output Contract

Keep the default format stable:

```text
Goal: ...
Done when: ...
Constraints: ...
Plan: ...
Open points: ...
```

Use `Open points` for:

- assumptions,
- risks,
- dependencies,
- approval authority,
- sensitivity or audience limits,
- decisions needed,
- critical readback items,
- contradictions,
- missing details that could change the work.

Do not turn every back brief into a long template. Add detail only when it changes safety, quality, or approval.

## Scenario Guidance

| Scenario | Emphasize | Avoid |
|---|---|---|
| Code or file changes | files, scope, tests, rollback, non-goals | editing before confirmation |
| Project kickoff | purpose, success criteria, deliverables, tradeoffs, owners | building from vague intent |
| Incident response | immediate goal, stop condition, escalation path, authority, logs | broad remediation without approval |
| Async handoff | owners, dates, unresolved questions, sensitivity, action record | stale context or hidden assumptions |
| Executive alignment | decision needed, material risk, owner, date | deep implementation detail |
| Technical alignment | interfaces, constraints, failure modes, test plan | vague strategic restatement |

## Wording Patterns

- Initiate: `I can back brief this. To avoid guessing, I need the audience, success criteria, constraints, and approval authority.`
- Confirm receipt: `My understanding of the assignment is: ... Please confirm or correct before I plan execution.`
- Back brief: `Here is my execution back brief: goal, done when, constraints, plan, and open points.`
- Close loop: `Please reply with confirm, correct, or escalate. I will not treat silence as approval.`
- Revise: `Updated back brief. Changes since last version: ...`

## Failure Modes

| Failure mode | What it looks like | Mitigation |
|---|---|---|
| Unsupported belief | Agent states a fact not given or verified | Label as assumption or ask |
| False belief | Agent repeats a wrong item confidently | Read back critical items |
| Contradiction | Two parts of the brief disagree | Scan before sending |
| Omission | Owner, deadline, stop condition, or dependency is missing | Put it in `Open points` |
| Confirmation/back-brief confusion | Agent repeats the task but gives no execution plan | Classify the brief type first |
| Premature closure | Agent acts as if silence means approval | Require confirm, correct, or escalate |
| Security leakage | Sensitive details are restated in a broad channel | Check audience and sensitivity |
| Async drift | Later work continues from stale assumptions | Version or restate changed points |

## Metrics

Useful evals should check alignment, not prose quality:

- Critical-item recall: required items captured / required items.
- Critical-item precision: correct critical items / asserted critical items.
- Contradiction rate: briefs with internal or source contradiction / total briefs.
- Omission severity: weighted misses for owner, deadline, stop condition, dependency, authority, or safety limit.
- Time-to-confirm: turns or time until explicit confirmation or correction closure.
- Revision turns to closure: correction cycles until the user confirms.
- Audience fit: whether the brief foregrounds the right details for the audience.
- Escalation appropriateness: risky cases paused instead of executed.

## Guardrails

- Use back-briefing to align, not to add process for its own sake.
- Ask only questions that could change the task, plan, approval, or success checks.
- For trivial one-step read-only requests, answer directly unless the user asks for a back brief.
- For high-risk, destructive, external, regulated, or costly actions, require explicit approval.
- Separate facts from assumptions.
- If corrected, restate the corrected task before material action when the correction changes scope, risk, output, authority, or success checks.
