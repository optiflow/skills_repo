---
name: create-skill
description: Create, review, improve, test, and package AI agent skills built around SKILL.md. Use when a user asks to turn a workflow into a reusable skill, assess or capture a lesson from difficult work, revise an existing skill, diagnose its behavior or triggering, or compare skill versions. Ordinary task execution and skill installation alone do not need this workflow.
compatibility: Instructions work across agents with skill support. Bundled helpers require Python 3.10+ and PyYAML; behavioral evaluations need a separate agent or host runner.
---

# Create Skill

Produce a skill that adds useful knowledge or a reliable method to the target agent, with evidence suited to the change. The required entrypoint is `SKILL.md`, singular.

## Working rules

- Treat an explicit request to create or update a skill as authorization for that work. Use the context already supplied and resolve routine choices. For a lesson noticed during other work, apply the capture gate below; propose it before writing unless the user has already authorized capturing qualifying lessons. Ask only for missing information that materially changes the result or for an action outside the user's authorization.
- A skill supplies task guidance. It does not override system or developer instructions, the user's current request, tool permissions, or approval controls. Keep genuine workflow constraints; distinguish requirements from defaults and examples.
- Describe the desired result, the evidence to use, and the constraints that matter. Give capable models room to choose the method. Use fixed steps where order or precision affects correctness. Remove generic tutorials, blanket approval pauses, repeated self-checks, and tool-use demands that do not help the task.
- Keep scope and names stable during an update. Inspect existing resources and their callers before removing them. Preserve unrelated metadata, invocation policy, dependencies, and user edits.

## Choose the amount of work

| Situation | Useful scope |
|---|---|
| A narrow correction | Make the focused edit; validate the changed contract and rerun the affected case. |
| A new, small skill with a known workflow | Write the smallest useful instructions; check realistic success and boundary cases; test any helper code. |
| Broad behavior changes, shared use, fragile actions, or a performance claim | Define cases early, compare independent runs, inspect artifacts, and check regressions. |

A short skill can be one file. Do not require a folder tree, benchmark, reviewer, or packaging step when it adds no value. Existing project requirements and the user's requested checks still apply.

## 1. Establish the contract and evidence

Infer from the request and current files:

- **Job and output:** The user task, inputs, result, and observable success criteria.
- **Routing:** Requests that need the skill and nearby requests that do not.
- **Environment:** Target hosts and models, available tools, file location, and any needed dependencies.
- **Constraints:** Required formats, permissions, irreversible actions, and failure or stopping conditions.

For updates, save or identify the original version and inspect the reported failure before rewriting. For new skills, look for information the base model lacks: local schemas, business rules, approved templates, or repeatable operations. A preference or stable workflow can justify a skill even if the base model can already do the task.

Before writing extensive instructions, define a small set of real tasks and what would count as success. Include a representative case and a plausible failure or boundary case; add cases for materially different modes. If making an improvement claim, establish the baseline early. Do not invent failures to justify more instructions.

### Capture a lesson from completed work

Use this gate when deciding whether a discovered lesson merits capture. It does not veto an explicit request for a skill, template, preference, or routine workflow just because the task was easy.

| Criterion | Evidence needed |
|---|---|
| **It was hard** | Failed approaches or a specific constraint or trade-off that required substantial reasoning. Time spent or tool-call count alone is insufficient. |
| **The move was not obvious** | A concrete method, constraint, or diagnostic step that another agent would otherwise need to rediscover. |
| **It will recur** | A plausible second feature, repo, or task with the same underlying failure and stated conditions where the lesson applies. |
| **It is testable** | A different instance of the problem, necessary inputs, and observable success criteria that check whether the known failure is avoided. |

Require evidence for all four; mark missing evidence as unknown. If any criterion fails or remains unknown, do not promote the lesson as qualifying. An assessment request authorizes an assessment; a qualifying lesson still needs permission to write unless that permission already exists.

Inspect relevant existing skills first. Update one when the lesson fits its job and trigger; create a new skill when it adds a distinct capability. Capture the general method and its limits, with the smallest useful change. See [lesson capture](references/lesson_capture.md) for evidence, overlap decisions, and fresh-context testing. A defined test makes a lesson testable; only an observed successful run validates it.

## 2. Write the smallest useful skill

Use valid YAML frontmatter with a short name and a discriminating description:

```yaml
---
name: reconcile-invoices
description: Reconcile invoice exports with payment records and report unmatched items. Use when comparing invoice and payment files or investigating a reconciliation mismatch.
---
```

For the portable core, names use 1-64 lowercase ASCII letters, digits, and single internal hyphens, and match the folder name. Descriptions are nonempty strings of at most 1,024 characters. Supported optional fields include `license`, `compatibility`, and string-valued `metadata`; tool and invocation extensions depend on the host.

Put the main capability and trigger early in the description: some hosts shorten discovery metadata. Add exclusions when they prevent a likely routing error. Keep detailed workflow branches and resource selection in the body. Do not use keyword stuffing or aggressive trigger language without evidence that it helps the target host.

Write the body around the task's outcome and decisions. Preserve non-obvious constraints and explain their purpose briefly. Use examples for likely ambiguity, not to prescribe the wording of every result. Do not demand a visible chain of thought; ask for concise reasons, evidence, or intermediate artifacts only when useful to the task.

Keep shared guidance in the entrypoint. Link optional detail with a clear reading condition. The 500-line guidance is an upper bound to watch, not an authoring target. See [resource design](references/resource_design.md) for file placement and [model guidance](references/model_guidance.md) when revising instructions for a new model or runtime.

## 3. Add resources only when they earn their place

Choose instruction-only authoring unless another resource improves the work. Use scripts for repeated or fragile operations, references for conditional knowledge, and assets for files copied into output. Avoid depending on another skill unless it exists in the target environment and is needed for this workflow.

Resolve helper paths from this `SKILL.md`, not the caller's project. The examples run from the create-skill directory; use absolute helper paths elsewhere. Helpers require Python 3.10+ and [PyYAML](scripts/requirements.txt) in an available or isolated environment.

For a new skill, the initializer is optional:

```bash
python -B scripts/init_skill.py my-skill --path /path/to/skills \
  --description "Describe the actual capability and its trigger."
```

Add resource, eval, or OpenAI metadata flags only when needed. Replace scaffold TODO markers before validation. Edit existing skills directly or in a writable copy; do not initialize them again.

For Codex UI metadata, read [OpenAI metadata](references/openai_yaml.md). Keep UI fields under `interface` and preserve existing policy and dependencies. Automatic selection is the normal default; retain an existing explicit-only setting unless the user asks to change it.

## 4. Validate structure and behavior

```bash
python -B scripts/quick_validate.py /path/to/my-skill
```

Fix structural errors and review warnings; `--strict` also fails on warnings. Validation checks metadata, scaffolds, local links, eval structure, and Python syntax. Its secret scan is a heuristic. Passing does not prove behavior or installation.

Run each new or changed helper with representative input and a meaningful failure case. Check integrations and the complete workflow when a change crosses components. Inspect rendered results when appearance is part of success. Once applicable checks pass, repeat or broaden them only for a new change, failure, or unresolved concern.

For behavioral tests, use realistic prompts and observable outcomes. Keep instructions and outputs separate from the evaluator's expected answers. New skills compare against no skill; updates compare against the saved original, with an optional no-skill check to see whether the skill is still needed. Use fresh runs with the same task, input files, model, settings, tools, and permissions. Explicit invocation tests task execution; it does not measure automatic discovery.

For a captured lesson, use a fresh context with a different instance of the same problem, supplying only the candidate skill and necessary task inputs. Keep the earlier conversation, failed attempts, and expected answer out of that run. Check the result and whether the known failure recurs. If no independent run is available, deliver a draft labelled "transfer untested"; do not equate a structural pass or author walkthrough with successful transfer.

Read [workflow modes](references/workflow_modes.md) for independent runs and limited environments, and [evaluation schemas](references/eval_schemas.md) when saving results. An author walking through their own draft is a useful smoke check, not an independent benchmark. Record missing observations as missing, and state which hosts and models were actually tested.

## 5. Review results and make supported changes

Inspect outputs and relevant tool traces, not scores alone. Check whether a failure came from routing, missing instructions, a broken helper, unavailable inputs, or the test itself. Fix the cause, retain working constraints, and rerun affected cases. For repeated or uncertain results, add trials before concluding that a change helped.

For a recorded evaluation, the optional helpers are:

```bash
python -B scripts/aggregate_benchmark.py /path/to/iteration-1 --skill-name my-skill
python -B scripts/generate_review.py /path/to/iteration-1 --skill-name my-skill
```

The aggregator reports descriptive comparisons only for matched cases, assertions, settings, and observation coverage. Inspect the evidence. Use the static page for artifact review; pending user feedback is not acceptance, but does not prevent delivery of an accurately labelled draft.

Use [grader](agents/grader.md), [analyzer](agents/analyzer.md), or [comparator](agents/comparator.md) instructions only when those roles help and independent agents are available and permitted. Do not spawn a reviewer for every small edit.

For discovery problems or wider release, read [trigger testing](references/trigger_optimization.md). Tune on development cases, select on validation cases, and keep a final test set untouched until release assessment. If you revise after seeing that test set, it is no longer held out. Do not present classifier judgments or synthetic fixture results as measured host triggering.

## 6. Deliver with an accurate status

Return the revised skill and a short account of what changed, why, what ran, and what remains untested. Separate structural validation, behavioral observations, and measured comparisons. Do not promise improvement across untested models.

Package when the user asks or an archive makes the handoff useful:

```bash
python -B scripts/package_skill.py /path/to/my-skill --output /path/to/dist
```

The helper validates the source and writes a reproducible ZIP with a `.skill` extension outside the skill folder. Inspect the archive before sharing; see [packaging details](references/resource_design.md). Include evals only when maintainers need them. Follow the target host's installation method: a `.skill` archive is a transport option, and editing source does not install or publish it.

The dated sources and decisions behind this workflow are in [source notes](references/source_notes.md). Read them when checking upstream changes or resolving a conflict between authoring guides.
