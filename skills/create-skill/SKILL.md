---
name: create-skill
description: Create new AI agent skills from explicit user requests or confirmed repeated workflows. Use when the user asks to create, design, scaffold, validate, or package a new skill; asks whether a recurring workflow should become a skill; or approves turning a repeated workflow into a skill. If repeated work is only observed, suggest a brief skill proposal and ask before creating files. Do not use for maintenance of already-created skills; use update-skill instead.
---

# Create Skill

Create skills that are small enough to load well and measured enough to trust.

Use the full loop for important, broad, fragile, or user-facing skills. Use the light loop for small private skills, but still validate the folder and test any scripts.

## Core principles

- **Lean context:** Treat every token as a shared cost. Keep `SKILL.md` focused on the core workflow and navigation. Move details into `references/`.
- **Right freedom:** Use prose for flexible judgment, pseudocode for stable patterns, and scripts for fragile or repeated work.
- **Progressive disclosure:** Put trigger logic in frontmatter, core operating steps in `SKILL.md`, and optional depth in bundled resources.
- **Evidence first:** Do not rely on a skill because it sounds good. Test it on realistic prompts and compare against a baseline when the environment allows.
- **Generalize from feedback:** Improve the reusable method, not only the example that failed.
- **No surprises:** Do not create skills for malware, hidden data access, deception, or actions the user would not expect from the skill description.

## Resource map

Read these files only when needed:

- `references/resource_design.md`: Decide what belongs in `SKILL.md`, `scripts/`, `references/`, `assets/`, `agents/`, and `evals/`.
- `references/eval_schemas.md`: Write `evals.json`, `eval_metadata.json`, `grading.json`, `timing.json`, and `benchmark.json`.
- `references/trigger_optimization.md`: Build should-trigger and should-not-trigger query sets and score trigger descriptions.
- `references/workflow_modes.md`: Adapt the workflow when there are no subagents, no browser, read-only installed skills, or limited tools.
- `references/openai_yaml.md`: Create optional `agents/openai.yaml` UI metadata.
- `agents/grader.md`: Use when grading assertions against outputs.
- `agents/analyzer.md`: Use when interpreting benchmark results.
- `agents/comparator.md`: Use when doing blind A/B comparison between two skill versions.

## Skill anatomy

A normal skill folder should look like this:

```text
skill-name/
├── SKILL.md              # required: frontmatter + concise instructions
├── scripts/              # optional: deterministic or repeated code
├── references/           # optional: detailed docs loaded only when useful
├── assets/               # optional: templates, icons, boilerplate, sample files
├── evals/evals.json      # optional: test prompts and assertions
└── agents/               # optional: UI metadata or specialist agent instructions
```

Keep the root clean. Avoid extra `README.md`, changelog, install guide, and similar files unless the user explicitly needs them as part of the skill output.

## Workflow

Start with the right level of permission:

- If the user explicitly asks for a new skill, proceed with this creation workflow.
- If repeated work is only inferred, propose a one-paragraph skill brief first: job, trigger, output, likely resources, and why it is worth capturing.
- Do not scaffold files until the user confirms.

### 1. Capture intent

Extract what the user has already said before asking anything. Fill these fields:

- **Job:** What should the skill help an agent do?
- **Trigger:** What user requests or contexts should activate it?
- **Output:** What should the final answer, file, code, or artifact look like?
- **Inputs:** What files, APIs, tools, dependencies, or domain rules matter?
- **Success:** How will a human or script know the skill worked?
- **Risk:** What could fail, leak, surprise the user, or cause harm?

Ask at most the few questions that block safe progress. When the user has provided enough detail, continue.

### 2. Decide the skill shape

Classify the task before writing:

- **High freedom:** Many good outputs exist. Use compact principles, examples, and selection rules.
- **Medium freedom:** A preferred pattern exists. Use a checklist, pseudocode, or parameterized scripts.
- **Low freedom:** Small mistakes break the result. Use tested scripts with narrow inputs.

Then map repeated work to resources:

- Use `scripts/` when the same code would be rewritten often or precision matters.
- Use `references/` for detailed domain knowledge, schemas, policies, examples, and API notes.
- Use `assets/` for templates, images, boilerplate, fonts, and files that the agent copies or edits.
- Use `evals/` for test prompts, expected results, and assertions.
- Use `agents/` for optional reviewer, grader, comparator, analyzer, or UI metadata instructions.

### 3. Initialize the folder

For a new skill, run:

```bash
scripts/init_skill.py my-skill --path skills --resources scripts,references --evals --openai-agent
```

Use lowercase letters, digits, and hyphens only. Keep names short, action-led, and under 64 characters. The folder name should match the `name` field.

### 4. Draft `SKILL.md`

Write frontmatter first:

```yaml
---
name: my-skill
description: What the skill does. Use when the user asks for X, works with Y files, needs Z workflow, or describes related real-world cases even if they do not name the skill.
---
```

Put all trigger rules in `description`. The body is loaded only after the skill triggers, so body-level trigger guidance arrives too late.

In the body:

- Start with the outcome the skill produces.
- Give the smallest workflow that works.
- Link every reference file from `SKILL.md` and say when to read it.
- Explain why important choices matter instead of using rigid rules everywhere.
- Include short examples when they prevent likely mistakes.
- Remove generic advice the base model already knows.

### 5. Validate and test scripts

Run:

```bash
scripts/quick_validate.py path/to/my-skill
```

Fix errors before packaging. Run every important script with representative inputs. If there are many similar scripts, test a representative sample and note any limits.

### 6. Create evals

Create 2-5 realistic prompts in `evals/evals.json`. Use prompts a real user would type, including messy details, file names, edge cases, and partial context.

Add assertions only when they can be checked objectively. For subjective work, use human review and optional blind comparison.

### 7. Run with-skill and baseline tests

When the environment supports independent runs, test each prompt twice:

- **With skill:** use the candidate skill.
- **Baseline:** use no skill.

Save outputs under a sibling workspace:

```text
my-skill-workspace/
└── iteration-1/
    └── eval-name/
        ├── with_skill/outputs/
        └── without_skill/outputs/
```

Save `eval_metadata.json`, `timing.json`, and `grading.json` where available. See `references/eval_schemas.md` for exact shapes.

When the environment cannot run independent agents, run the test prompts inline, state the limit, and still collect outputs for review.

### 8. Grade, review, and analyze

Grade objective assertions with scripts when possible. Otherwise, use `agents/grader.md`.

Aggregate results:

```bash
scripts/aggregate_benchmark.py my-skill-workspace/iteration-1 --skill-name my-skill
```

Create a static review page:

```bash
scripts/generate_review.py my-skill-workspace/iteration-1 --skill-name my-skill --benchmark my-skill-workspace/iteration-1/benchmark.json
```

Use `agents/analyzer.md` to look for:

- Assertions that pass both skill and baseline.
- Flaky prompts or high variance.
- Token or time cost that outweighs gains.
- Repeated helper code that belongs in `scripts/`.
- Missing references or unclear trigger wording.

### 9. Improve without overfitting

Read transcripts or outputs, not just final scores. Improve the reusable method:

- Remove text that did not help.
- Add scripts for repeated fragile work.
- Add references for stable domain knowledge.
- Clarify choices the agent misunderstood.
- Replace brittle “always/never” rules with the reason behind the rule unless the output format truly requires them.
- Keep failures from becoming one-off patches.

Rerun the same evals after each meaningful revision. Add new evals only after the current ones no longer reveal useful failures.

### 10. Optimize the trigger description

After the skill works on task quality, tune the `description` field.

Create a trigger eval set with realistic should-trigger and should-not-trigger prompts. Include near-misses. Split into train and held-out test cases. Choose the description that performs best on held-out cases, not the one that only fits the training examples.

Use:

```bash
scripts/score_trigger_evals.py trigger_results.json --output trigger_score.json
```

Then update the frontmatter and show the user the before/after description and scores.

### 11. Package and present

Package only after validation passes:

```bash
scripts/package_skill.py path/to/my-skill --output dist
```

By default, exclude eval workspaces, caches, and test review pages. Include evals only when the user wants future maintainers to rerun them:

```bash
scripts/package_skill.py path/to/my-skill --output dist --include-evals
```

## Quality gates

A skill is ready when all applicable gates pass:

- **Trigger gate:** The `description` states what the skill does and where it applies, including realistic adjacent contexts.
- **Context gate:** `SKILL.md` is lean, and all extra detail is discoverable from direct links.
- **Resource gate:** Scripts, references, and assets each have a clear reason to exist.
- **Execution gate:** Important scripts run on representative inputs.
- **Evidence gate:** Realistic tests show better quality, speed, cost, consistency, or safety than baseline.
- **Review gate:** Human feedback has been addressed or clearly marked as out of scope.
- **Package gate:** The package contains no secrets, caches, workspaces, or surprise files.
