# Capturing lessons from completed work

Read this when evaluating a lesson discovered while solving a task, or when the user has authorized capturing such lessons. Apply the four criteria in `SKILL.md` to the available evidence. A direct request for a simple skill remains valid without a history of failure.

## Establish the evidence

Keep a short note in the task output or evaluation workspace: what failed or demanded substantial reasoning, what changed the outcome, where the same problem could recur, and how to test the lesson. Reuse available logs, artifacts, or user reports and identify their source. Do not manufacture extra failed attempts, claim access to hidden reasoning, or treat effort alone as proof of value.

An expired credential, transient outage, typo, or long download does not by itself justify a skill. A demonstrated way to distinguish an outage from a configuration error might qualify if the other criteria also hold. Generalize the cause and the useful decision, not the accidental details of a single run.

If a criterion is false or unknown, say which one and keep useful findings in the task summary. Do not write a skill under an authorization limited to qualifying lessons. If the user expressly asks to capture it anyway, follow that request and state the evidence limits.

Qualification and permission are separate. Honor existing session authorization to capture qualifying lessons; do not ask again. If only assessment is authorized, give a short proposal naming the destination, reusable method, and test. Do not modify a skill yet. This workflow does not install a background watcher or change project instructions to inspect every completed task.

## Choose the destination and content

Inspect the relevant installed or project skills and their resources. Compare their jobs and triggers with the lesson rather than matching names alone.

| Finding | Action |
|---|---|
| An existing skill already covers the lesson correctly | Reuse it; diagnose discovery, unavailable inputs, or execution before adding duplicate instructions. |
| The lesson fits an existing skill but a useful decision or constraint is missing or wrong | Update the relevant instructions, reference, or helper, preserving unrelated behavior. |
| No existing skill fits and the lesson has a distinct reusable job and trigger | Create a focused skill. |

Write the condition that activates the method, the method itself, why it prevents the observed failure, and its limits. Include necessary schemas or examples, using safe substitutes for task-specific data. Store detailed incident history and test observations outside the skill; another agent should need the reusable method, not the original chat. Avoid turning a version-specific workaround into an unconditional rule; recheck the underlying behavior when the runtime changes.

## Test transfer to another task

Before editing, choose a related instance with different inputs or a different feature or repo. It must preserve the underlying failure conditions; changing a filename alone is not evidence of generalization. Define success and the known failure before the execution run. Select a plausible boundary case when needed to check that the method is not applied outside its scope.

Use a fresh agent or session with the candidate skill and only the raw task inputs it needs. Do not give it the original conversation, failed attempts, expected answer, or author's explanation of the fix outside the skill. Keep evaluator notes separate and use isolated folders for outputs. A fresh subagent may inherit host rules or a global skill catalogue; record those limits and do not call a contaminated run fully isolated.

For a claim that the skill improved the result, give the same task and inputs to an independent baseline under matching model, host, settings, tools, and permissions. Use the saved original for an update or no skill for a new capability. Keep the baseline from reading the candidate. Count avoidable failed attempts only when a trace supports that count; fewer tool calls alone do not show better reasoning.

Check the resulting artifact against the success criteria, inspect whether the known failure recurred, and record any prompting or recovery required. A correct final answer after repeating the same old errors does not establish that the lesson prevented them. Retain actual outputs and record which task, model, and environment were tested. One successful case establishes that observation, not reliability on every future task.

Use an available, permitted independent runner when this transfer claim is being tested. If none is available, finish the supported structural and author checks and deliver the requested draft with "transfer untested" and the unrun test. Do not invent a baseline or turn the author replaying their own instructions into independent evidence. See [workflow modes](workflow_modes.md) for runner limits and [evaluation schemas](eval_schemas.md) for saved observations.

Once the required checks pass, stop. Repeat or expand the evaluation only for a failure, meaningful change, uncertain result, or broader claim. The four criteria are this user's capture policy; the source notes explain how the authoring and evaluation method draws on official guidance.
