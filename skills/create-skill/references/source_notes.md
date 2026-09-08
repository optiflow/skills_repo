# Source notes

Reviewed on 2026-09-07. These sources informed the workflow; their platform-specific instructions are not a combined universal specification. Resolve changing format or host behavior against the relevant current official source.

## Reviewed sources

| Source | Revision or scope | Use in this skill |
|---|---|---|
| [Original create-skill](https://github.com/optiflow/skills_repo/tree/c737122d37d9cccd9ad7e0984b880ce0f2bee9ed/skills/create-skill) | Repository HEAD matched local main on review date. | Retain portable resources, realistic evals, and packaging; correct conflicting gates and helper behavior. |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/41bbe19d1a1a7eaab5e7bb9050a417e5c6cffc8f/skills/skill-creator/SKILL.md) | Repository revision 41bbe19d, dated 2026-09-03. | Keep artifact review, baseline comparison, and iteration from observed failures. Use its Claude-specific runner only in a suitable host. |
| [OpenAI skill-creator](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/SKILL.md) | Repository revision 49f948fa, dated 2026-06-24. | Keep concise instructions, appropriate freedom, progressive disclosure, and optional resources. |
| [Open Agent Skills specification](https://agentskills.io/specification) | Live specification checked on review date. | Portable name, description, optional metadata, resource conventions, and YAML validation. |
| [OpenAI build skills](https://learn.chatgpt.com/docs/build-skills) | Live host documentation; the old Codex skills URL redirects here. | Concise discovery metadata, host-specific UI layout and invocation policy, and distinction between authoring and installation. |
| [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model) | The live page selected GPT-6 Astra on review date. | Audit permission pauses, instruction conflicts, and unnecessary testing before adding more process. |
| [Anthropic authoring practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Live skill authoring guidance. | Identify gaps and evaluation cases early; test the actual models; keep instructions concise and usable. |
| [Anthropic prompting practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Live general guidance with model-specific exceptions. | Adjust aggressive tool-use language and delegation to observed behavior. |
| [Claude Fable 5.1 prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) | Current model-specific guide. | Complete authorized tasks, keep changes and tests within scope, and test effort settings rather than transferring them blindly. |
| [Claude Opus 5 prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) | Current model-specific guide. | Remove redundant verification instructions when they cause excess work. |

The repository revisions above pin the snapshots inspected; a repository commit date is not necessarily the date of a change to SKILL.md itself. The locally bundled OpenAI system skill was also inspected and differs from the public GitHub snapshot: it gives stronger emphasis to scope, preserving existing metadata, and proportional testing. This review does not represent the installed copy as the public upstream version.

## Synthesis decisions

- Keep the task-based evaluation loop, but make its cost proportional to the change. Small edits do not need a mandatory browser review and another permission pause.
- Prefer precise discovery boundaries over a blanket rule to make descriptions more aggressive. Host and model behavior can differ.
- Respect optional fields supported by the open specification, even where an older creator paragraph suggests only two fields. Validate host extensions against the host.
- Treat final held-out cases as release evidence. Repeatedly selecting descriptions on their final test scores leaks test information into selection, even if a runner calls them held out.
- Keep field structure checks, code tests, artifact review, and runtime comparisons distinct. Passing one does not establish the others.

These are review decisions, not claims that this revision has been benchmarked on every named model. Retain a model-specific rule only when the target environment and observed outcome justify it.

## Lesson-capture update checked 2026-09-08

The four criteria (hard, non-obvious, recurring, testable) are the user's policy for lessons discovered during work, not a requirement published by either provider. They do not restrict explicit requests for simple skills. Existing authorization permits capture; qualification alone does not authorize changing files.

Rechecked both upstream creator files and their main revisions above; the revisions were unchanged. Rechecked Anthropic's authoring guidance and the three model guides linked above. The update follows OpenAI's concise, scoped instructions and proportional checks, and Anthropic's method of identifying a reusable pattern, defining evaluations, and testing on related tasks with a fresh agent. It preserves required validation while avoiding a compulsory verifier for every edit.

The capture gate, choosing an existing skill before creating a duplicate, and the separate "testable" and "transfer validated" statuses are synthesis choices. The new reference routes this extra detail only to lesson-capture tasks. Runtime evidence must still be reported separately from this documentation review.

A follow-up installation check found that the host exposed a nested payout fixture as a selectable skill. Fixture entrypoints now use `SKILL.md.fixture` and become `SKILL.md` only in isolated runs. A package-and-materialize regression check covers this distinction; structural validation alone had not caught it.
