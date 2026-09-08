# Back briefs for humans and AI agents

Research checked: 8 September 2026.

## Main finding

A back brief makes the receiver's interpretation and proposed approach available for correction before substantial execution. A useful plan-validation gate has three parts: the sender states intent, the receiver explains how it will meet that intent, and an authorized reviewer resolves mismatches and decides what work may proceed.

The military practice supplies the definition and purpose. Human communication and human–AI interaction research support feedback and correction. Agent research identifies relevant coordination failures, while current frameworks provide ways to pause and resume. These sources support the design rationale; they do not establish that this particular skill reduces task cost or error rates.

## Source register

All links below were inspected on 8 September 2026. Publication dates are distinct from the access date.

| Source and date | What it supports | Limit |
|---|---|---|
| U.S. Army Center for Army Lessons Learned, [Commander and Staff Guide to Rehearsals, No. 19-18](https://api.army.mil/e2/c/downloads/2023/01/19/48e6a637/19-18-commander-and-staff-guide-to-rehearsals-a-no-fail-approach-handbook-jul-19-public.pdf), July 2019, printed p. 5 and chapter 5 | A back brief follows planning, reviews how subordinates intend to accomplish the mission, checks intent, and exposes problems in the approach. | Military practice, not an AI experiment. This is a dated primary guide, not a claim about the latest doctrine edition. |
| AHRQ TeamSTEPPS, [Closed-Loop Communication](https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/loop.html), reviewed May 2023 | Sender initiates, receiver provides feedback, sender verifies. The sender has an active checking role. | Human teamwork guidance; no measured effect for LLM agents. |
| AHRQ TeamSTEPPS, [Teach-Back](https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/teachback.html), reviewed May 2023 | Explaining instructions in one's own words exposes understanding more usefully than merely asserting understanding. | A related communication method; it does not define backbriefing. |
| Amershi et al., [Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf), CHI 2019, guidelines 9, 10, and 12 | Make correction easy, handle uncertain user goals through clarification or reduced scope, and retain recent interaction context. | Design guidelines evaluated with practitioners and AI products; not a trial of modern agent back briefs. |
| Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), 13 June 2025, delegation section | Workers need objectives, output formats, source/tool guidance, and clear boundaries. Vague delegation produced overlap and missed requirements in the authors' system. | Engineering experience from one system; no isolated back-brief comparison. |
| Cemri et al., [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/html/2503.13657v3), v3, 26 October 2025, sections 3–4 and appendix A | Observed failures include wrong assumptions without clarification, lost context, ignored peer input, plan/action mismatch, and incomplete verification. | A failure taxonomy and dataset do not prove this proposed gate fixes those failures. |
| LangChain, [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts), live documentation | A host can persist a pause and resume with external input. Resuming reruns the interrupted node; side-effect placement and retry behavior matter. | A runtime building block, not semantic plan review or reviewer authorization. No LangGraph integration was run for this revision. |
| A2A Project, [Life of a Task](https://a2a-protocol.org/latest/topics/life-of-a-task/), live documentation | Task identity, context, input-required states, and completion states support tracked coordination. | The acceptance and plan-revision contract proposed here is application design, not a standard A2A feature. No A2A integration was run. |

The definition uses the directly inspected Army guide. The dated primary sources above support each additional research claim.

## Why the mechanism can help

A task request leaves choices unstated. The receiver must infer the desired outcome, what counts as success, and a path to get there. If the sender cannot see those choices, errors may become visible only after work has been spent. A brief moves a small part of that checking effort earlier.

The proposed gate tests the mapping from intent to outcome, then from outcome to plan and evidence. It also tests whether constraints and dependencies make the plan feasible. Distinguishing assumptions from facts allows a reviewer to correct a false premise without rewriting the entire request.

This is a design inference from the sources and the user's intended workflow. The gate is worthwhile when the expected avoided rework exceeds the cost of preparing, reading, and correcting the brief. No numeric threshold has been measured here. Use shorter briefs for routine work and fuller briefs where misunderstanding would be costly.

## Distinct checks

| Check | What it answers |
|---|---|
| Understanding | Does its own-word interpretation preserve the intended result and purpose? |
| Plan validation | Would the proposed approach meet the success criteria within constraints? |
| Authorization | May this actor perform these actions under the current instruction and permissions? |
| Completion validation | Does actual evidence show that the work met the criteria? |

These checks can occur in one short exchange, but one cannot substitute for another. A reviewer may accept a research plan while the human retains the decision to purchase. A good plan can still be executed incorrectly. A mistaken assumption remains uncertain even when both agents agree with it.

## Human-to-agent use

The human supplies intent. The agent should use available context, describe the result it believes the human wants, propose observable checks, and flag only decisions that affect execution. The human can correct the goal, tighten scope, change priorities, or accept the plan.

Example task: "Prepare a comparison of database options for our internal service. Back brief first and wait for my review."

Example receiver response:

> Understanding: You want a comparison that helps choose a database for the service.
>
> Success criteria: Each candidate is assessed against the same agreed workload and priorities, with official sources and material uncertainties.
>
> Constraints: This stage covers a comparison, with no procurement or implementation.
>
> Plan: Confirm the decision criteria, inspect the relevant official documentation, compare the options, and check each conclusion against its sources.
>
> Assumptions: This is a selection decision; I have not established the workload or preferred candidates.
>
> Open questions: Which options and workload should I compare, and which trade-offs matter most? These affect the research scope.
>
> Gate: Waiting for your review and those inputs before substantive research.

Where the human already gives complete requirements and says to proceed, the brief records the working interpretation without creating another approval round. If only an optional formatting detail is unknown, state a sensible default. If a missing fact changes the decision itself, pause the dependent work.

## Agent-to-agent use

The receiving agent must connect its task to the parent's purpose, retain limits and handoff expectations, and say how it will produce a verifiable result. The sender then compares that plan against the original task and the other workers' responsibilities.

Plan reviews should expose duplicated work, missing coverage, conflicting edits, unavailable inputs, and authority gaps. A versioned decision prevents an old approval from releasing changed work. The coordinator may accept within its delegated authority; human-reserved decisions remain with the human.

See [agent coordination](agent-coordination.md) for a concrete message contract and runtime boundaries. The contract is deliberately separate from a specific framework.

## Debrief and lesson handoff

A debrief compares observed results with the original intent and success criteria. It can expose a reusable method, but completion, effort, or a surprising outcome alone does not justify a skill change. The handoff to `$create-skill` follows the user's capture policy; it is not a finding established by the research sources above.

Example: an export passed its row-count check but duplicated records because different source systems reused the same local identifiers. Evidence shows that matching by source and local identifier fixed the error, another import has the same condition, and a separate fixture can test it. The debrief should explain the failed check, corrected method, recurrence conditions, and proposed test, then use the current `$create-skill` workflow to assess the lesson and inspect existing coverage.

If the user requested only an assessment, return the assessment and any supported capture proposal without editing a skill. If qualifying captures were already authorized, follow that authority and the capture workflow without repeating the permission request. When evidence is missing or no reusable lesson emerges, keep the findings in the debrief. Report a defined but unrun transfer test as untested.

## Failure modes and remedies

| Failure | What to change |
|---|---|
| Polished echo with no execution implications | Require a result, evidence of success, and credible approach. |
| Hidden assumptions or invented facts | Label material assumptions and identify how they will be checked. |
| Rubber-stamp review | Compare against the original intent and name mismatches. |
| Required review treated as satisfied by silence | Keep dependent work pending until an authorized current decision arrives. |
| Repeated approval requests despite clear authority | Preserve existing permission and ask only at an unresolved boundary. |
| All work stalls on one optional detail | Use a stated default or continue independent authorized work. |
| Preparation consumes the effort the gate was meant to protect | Limit pre-gate discovery to what makes the proposal reviewable. |
| Stale approval or lost handoff context | Bind the decision to the current task, plan, and relevant inputs. |
| Coordinators approve beyond their authority | Retain reserved decisions and escalate to the proper owner. |
| Agents agree on a false premise | Check sources and outputs; consensus is not proof. |
| A verbal gate is bypassed by tools or retries | Enforce state, authorization, and version checks in the host where required. |
| Plan accepted, work unfinished | Check outputs and required tests before reporting completion. |
| Every debrief creates another skill | Apply the current create-skill evidence, existing-coverage, permission, and validation rules. |

## Evaluation and limits

The revision's cases are in [evals.json](../evals/evals.json). They cover explicit human review, authorized continuation, agent delegation and sender review, material ambiguity, corrections, stale acceptance, reserved authority, critical constraints, trivial requests, completion evidence, and debrief handoffs to lesson assessment.

Assess actual responses and tool traces, not the presence of headings alone. Useful measures for a later deployment trial include critical requirements retained, material contradictions caught before execution, unauthorized actions, avoidable pauses, correction turns, rework, review time, and task cost. Compare matched tasks with the saved original and measure any added review overhead.

Text response cases show how an agent responds to supplied scenarios. An isolated multi-turn run can show whether it waits, incorporates a correction, and executes only the released scope. Neither establishes automatic discovery, production enforcement, cross-model gains, or reduced real-world rework. Keep those observations separate.
