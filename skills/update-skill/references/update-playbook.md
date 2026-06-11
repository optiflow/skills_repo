# Update Playbook

Use this reference to decide whether an existing AI agent skill should change, how large the update is, and how to prove the new version is better.

## Update Gate

Update a skill only when the current skill no longer helps the agent do the right task reliably, safely, cheaply, and at the right time.

At least one condition must be true:

- **Task changed:** The skill must now support a new user job, output, workflow, or scope.
- **Environment changed:** A tool, API, MCP server, file format, template, package, CLI, database, source system, or runtime changed.
- **Risk changed:** The skill now handles more sensitive data or can write, delete, send, buy, prescribe, approve, commit, or expose private data.
- **Evidence shows failure:** Evals, traces, logs, user feedback, incident reviews, or observed behavior show the same failure pattern more than once.

If evidence is weak, write a small eval or reproduction first. Do not turn one odd run into permanent instructions.

## Do Not Update

Do not update the skill when:

- A one-off failure has not been reproduced.
- The tool is broken but the instruction is fine.
- The agent needs fresh data, not a larger prompt.
- A separate skill would be cleaner.
- The skill is trying to cover too many jobs.
- The update only adds "be careful" without changing behavior, validation, permissions, or review.

For bloated skills, prefer removing content, moving rare details into `references/`, or splitting the skill.

## Common Update Cases

- **Wrong trigger behavior:** Update the name, frontmatter description, trigger terms, or scope boundaries when the agent misses the skill, overuses it, chooses the wrong overlapping skill, or sees a vague description.
- **Repeated mistake:** Update when traces, evals, or feedback show the agent skips a required step, uses the wrong tool, misreads a policy, forgets validation, emits the wrong format, or asks for facts it could inspect.
- **Workflow or dependency change:** Update tool names, API endpoints, auth notes, schemas, field names, rate limits, table names, file formats, templates, package commands, or source-of-truth links.
- **Risk change:** Add guardrails, human review, narrower permissions, safer defaults, logging, or tool-level validation when the skill can cause more harm than before.
- **Output contract change:** Update JSON schemas, report templates, naming rules, citation rules, file structure, or acceptance criteria. Treat silent contract edits as unsafe.
- **Bloat:** Move long or rare material out of `SKILL.md`; replace prose with a checklist, template, or script where that reduces repeated errors.
- **Model, runtime, or platform change:** Re-test the skill when model family, context size, tool calling, local versus MCP tools, or deployment environment changes.
- **Domain knowledge change:** Update policy, clinical, brand, coding, compliance, product, or pricing rules. For fast-changing facts, teach the agent where to fetch the current source instead of burying stale facts.

## Version Severity

- **Patch:** Clarify wording, fix a bad example, improve trigger terms, fix a typo, or tighten one step without changing behavior.
- **Minor:** Add a supported case, reference file, script, eval, or validation step while keeping old behavior.
- **Major:** Change output schema, tool contract, permissions, safety behavior, core workflow, or scope.

Use the highest severity that applies. If in doubt between minor and major, choose major when another prompt, tool, user, or system may depend on the old behavior.

## Update Workflow

1. Capture the reason for change and the evidence.
2. Snapshot the original skill and keep a rollback path.
3. Reproduce the failure or define a baseline from the old skill.
4. Choose update, no-op, split, or tool fix.
5. Assign patch, minor, or major severity.
6. Edit the smallest useful surface.
7. Add or update evals that would have caught the issue.
8. Run validation and compare old versus new behavior where possible.
9. Report the result and any remaining risk.

## Update Report

Use this report shape after the update:

```text
Severity: patch | minor | major
Evidence: eval, trace, log, feedback, incident, observed behavior, or concrete change
Changed behavior: what the new skill does differently
Validation: commands, evals, manual checks, and comparison result
Rollback: original snapshot or commit path
Remaining risk: known gaps, follow-up evals, or limits
```

A strong skill library does not change daily. It has clear ownership, evals, version history, rollback, and measured improvement after each change.
