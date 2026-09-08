# Agent coordination and plan gates

Read this when a coordinating agent delegates work, reviews a worker's plan, or resumes an asynchronous task. This is a proposed application protocol for this skill, not an A2A standard or a supplied runtime implementation.

## Minimum exchange

1. **Sender tasks receiver:** purpose, worker scope, expected output and evidence, inputs, constraints, dependencies, authority, and review requirement.
2. **Receiver back briefs:** interpretation, success checks, plan, assumptions, questions, and pending status.
3. **Authorized reviewer decides:** accept with released scope, request specific revisions, or hold/escalate.
4. **Receiver executes released work:** retain the accepted record and check outputs against success criteria.
5. **Receiver reports:** evidence of completion, gaps, and deviations. A plan decision is not a completion decision.

The sender checks the worker's plan against the parent task, not just the worker's own restatement. A set of individually reasonable briefs can still duplicate work or leave a gap. Assign each shared artifact an owner and make dependency order explicit. Keep child review loops within the coordinator's authority; involve the human for a human-owned decision.

## Optional record for asynchronous systems

Use the host's schema where one exists. A small local record can carry the following fields; the field names are illustrative.

```yaml
task_id: REF-12
plan_revision: 2
sender: coordinator
receiver: storage-researcher
reviewer: coordinator
intent: Support the parent architecture decision with sourced storage facts.
scope: Compare access patterns and recovery options; pricing belongs to another worker.
input_refs:
  - service-requirements@revision-3
success_criteria:
  - Claim table covers each requested capability with an official source and uncertainty note.
plan:
  - Inspect requirements and select relevant official pages.
  - Compare the requested capabilities and verify claim-to-source support.
  - Return the table and unresolved trade-offs.
assumptions:
  - belief: Managed services are allowed.
    check: Coordinator must confirm this before source selection.
open_questions:
  - question: Are managed services allowed?
    blocking: true
authority:
  allowed: Read public sources after plan acceptance; at most five source pages.
  reserved: Purchases and architecture selection.
gate_status: pending
execution_status: not_started
```

The reviewer returns a decision referring to the same task and current plan:

```yaml
task_id: REF-12
plan_revision: 2
decision: accept
reviewer: coordinator
resolved_questions:
  managed_services_allowed: true
released_scope: Read up to five official source pages and return the comparison table.
conditions: []
```

The authenticated reviewer, decision, scope, and revision must come from the host's trusted channel. A model-supplied `reviewer` string is not proof of identity or authority. Store references or versions for inputs that affect the decision; avoid copying secrets into the record.

## Gate behavior

| Event | Result |
|---|---|
| Current plan accepted by an authorized reviewer; blockers resolved | Release only the accepted scope. |
| Accepted with a condition | Execute permitted preparation; release the dependent step only after evidence satisfies the condition. |
| Revision requested | Update the plan and keep affected execution pending. |
| Clear correction plus explicit permission to proceed | Record the corrected current plan and release that scope. |
| Missing, stale, ambiguous, or unauthorized decision | Keep affected work pending; request the current authorized decision. |
| Material change to scope, input, or assumption | Invalidate the affected acceptance and return for review unless already covered by explicit authority. |
| Task canceled or review rejected without revision | Do not execute; retain the status required by the host. |
| Accepted work finishes | Verify success evidence before reporting complete. |

Avoid duplicate execution when messages retry. Use the host's existing task and event identifiers to deduplicate decisions and bind execution to the accepted version. A retry should not silently start the same external action twice.

## Runtime implementation boundary

For a gate that must be enforced, separate plan preparation and execution in the host. Persist the brief and a pending state; validate the reviewer, task, revision, scope, conditions, and current inputs before resuming tools. Make action retries safe. Test both the permitted path and attempts to execute with no decision, a stale decision, or a decision outside the reviewer's authority.

[LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) provide persistence-backed pauses and resume input; a resumed node runs again from its start, so placement of side effects matters. The application still supplies the authorization and plan checks. This reference documents a possible mechanism, not an integration tested by this skill.

[A2A's task lifecycle](https://a2a-protocol.org/latest/topics/life-of-a-task/) distinguishes messages, tracked tasks, interrupted states such as `input-required`, and terminal states. Map a pending review to the host's supported nonterminal waiting state. The custom revision and acceptance contract above must be carried by the application; it is not a standard A2A back-brief field set.

## Example review that catches misalignment

Parent intent: update the local sign-in screen to match the supplied mockup while preserving authentication and password reset; verify the user flow.

Worker plan: replace authentication, remove password reset, and approve the result from screenshots.

Reviewer decision: **Revise.** The proposed actions conflict with two fixed requirements. Keep the existing authentication and password-reset behavior, describe how the screen will match the mockup, and include behavior and end-to-end checks. Execution remains pending for this revision.

The review names a concrete mismatch and a repair. General praise, a matching goal sentence, or a plan that sounds plausible would not close this gap.
