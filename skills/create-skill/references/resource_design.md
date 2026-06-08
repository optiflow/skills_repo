# Resource Design Reference

Use this when deciding what belongs inside a skill.

## Decision table

| Need | Best place | Why |
|---|---|---|
| Trigger matching | `SKILL.md` frontmatter `description` | Always visible before the skill loads. |
| Core workflow | `SKILL.md` body | Loaded after trigger; should be short and actionable. |
| Detailed domain knowledge | `references/` | Loaded only when useful. |
| Deterministic or repeated code | `scripts/` | Reliable and token efficient. |
| Templates or files copied into outputs | `assets/` | Used without loading all content into the model. |
| Test prompts and assertions | `evals/` | Lets maintainers measure improvement. |
| Specialist review instructions | `agents/` | Keeps grader, analyzer, and comparator roles separate. |

## Degree of freedom

| Freedom | Use when | Skill form |
|---|---|---|
| High | Multiple outputs can be good; judgment matters. | Principles, examples, selection rules. |
| Medium | A stable method exists, but cases vary. | Checklist, pseudocode, parameterized scripts. |
| Low | Fragile steps, strict formats, or repeated transforms. | Tested scripts and narrow instructions. |

Start with the lowest freedom needed for reliability, then loosen only where the task needs judgment.

## Context hygiene

Keep `SKILL.md` under 500 lines when possible. Move details out when they are optional, domain-specific, long, or only relevant to one branch of the workflow.

Do not duplicate the same rule in `SKILL.md` and a reference file. Duplication makes later updates unsafe because one copy will become stale.

Every reference file should be linked from `SKILL.md`. For files over 100 lines, add a short table of contents near the top.

Avoid deep trees. One level below `references/` is usually enough.

## Script design

Write scripts when the agent would otherwise repeat brittle code. Good scripts are:

- Narrow: one clear job.
- Parameterized: file paths and options come from arguments.
- Safe: no hidden network calls, credential use, or destructive defaults.
- Testable: include a simple example command or representative test input.
- Transparent: print useful errors and exit non-zero on failure.

Do not hide important reasoning inside scripts. The skill should explain when and why to use the script.

## Asset design

Use assets for files that are copied, filled, edited, or used as output material. Do not use assets as a dumping ground for documentation. If the model should read a file for knowledge, put it under `references/`.

Never package private credentials, proprietary files, or fonts unless the user has the right to share and use them in the skill.

## Root-folder hygiene

A clean root helps the agent see what matters. In most skills, the root should contain only `SKILL.md` and known resource folders.

Avoid extra files such as `README.md`, `CHANGELOG.md`, `INSTALL.md`, and informal notes unless they are part of the task itself.
