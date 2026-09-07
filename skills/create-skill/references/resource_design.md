# Resource design

Start with the freedom the task allows. Add precision where a wrong choice has a concrete cost.

| Need | Place | Include when |
|---|---|---|
| Capability and trigger | Frontmatter description | Required for discovery; lead with the main job. |
| Shared outcome, decisions, constraints | `SKILL.md` body | Required task guidance; keep conditional detail elsewhere. |
| Domain rules, schemas, substantial examples | `references/` | The agent needs information it would otherwise have to rediscover. |
| Repeated transformation or fragile operation | `scripts/` | Running maintained code improves reliability or avoids repeated code generation. |
| Template, image, font, starter project | `assets/` | A file is copied or adapted into the result. |
| Prompts, fixtures, expected outcomes | `evals/` | Maintainers will test behavior again. Keep results outside the skill. |
| Host metadata or independent review role | `agents/` | The target host uses it, or the evaluation needs a separate role. |

## Instructions and context

One file is enough for a simple skill. Use prose and decision criteria for open work; examples or configurable scripts for a preferred pattern; exact steps and tested code for fragile operations. A universal checklist is rarely the right starting point.

Link resources at the decision where they become useful and say whether to read, run, or copy them. Keep each important rule in one maintained location. Short references need no contents page; add one or search terms when navigation becomes hard. Avoid chains that require loading many irrelevant files before reaching the needed rule.

A file can be large without being loaded, but reading it still consumes context. Include maintained, task-specific information rather than copied manuals. Record source dates for facts that can drift and provide an official refresh route when needed.

## Helpers and assets

Accept paths and options as arguments. Resolve bundled resources relative to the script or skill, not an assumed project directory. Declare dependencies. Report actionable errors with nonzero exit codes; do not silently fabricate a successful result after an operation fails.

Test the actual input-to-output operation, including a likely invalid input. For mutating helpers, preserve user inputs and define the required confirmation, retry, and stopping behavior for that operation. Prose about permission does not grant tool access.

Keep secrets and private client data out of distributable fixtures. Keep needed licenses and notices. Extra root documentation is acceptable when required for licensing, packaging, or the user's deliverable; otherwise keep maintainer review notes outside the installed skill.

## Packaging details

The package helper validates before writing and preserves an existing archive if validation fails. Output belongs outside the skill directory. It normalizes timestamps and file modes for reproducible bytes while preserving whether a file is executable. Nested symlinks are rejected because they can include files outside the intended package.

By default it excludes hidden files, common credential filenames and key extensions, caches, environments, build folders, previous skill archives, eval workspaces, and `evals/`. Use `--include-evals` to include shareable maintainer cases. The exclusions are not a proof that other files contain no private data. Review the actual archive manifest, licensing, and intended assets before sharing.

`init_skill.py --force` permits an existing empty directory; it never overwrites a populated skill. Unknown resource arguments are rejected before writing. Input and output paths supplied to helpers follow the caller's current directory; bundled helper paths follow the loaded skill's directory.
