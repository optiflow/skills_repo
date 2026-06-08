---
name: spec-driven-dev
description: Guide spec-driven development for AI-assisted software work. Use when the user asks for SDD, project constitutions, feature specs, AI coding plans, validation scorecards, replanning, brownfield SDD adoption, or moving beyond vibe coding.
---

# Spec-Driven Dev

Use this skill to turn non-trivial AI-assisted software work into durable specs before code changes. The output should make intent, constraints, tests, and review gates explicit enough for a coding agent to implement without guessing.

## Fit Gate

Use the full SDD flow for work that is multi-step, long-lived, risky, shared by a team, or likely to span agent sessions. Use a light plan for tiny scripts, throwaway experiments, or highly exploratory work where a full spec would cost more than the code.

Respect the active execution mode. If file edits are not allowed, produce spec text or a proposed plan. If edits are allowed, write or update spec files before implementation unless the user has already approved a clear plan.

## Workflow

1. **Ground first.** Inspect repo instructions, docs, tests, package configs, existing specs, and relevant code before asking questions. Resolve discoverable facts locally.
2. **Choose the spec location.** Reuse an existing spec/docs convention. If none exists, use `docs/specs/constitution/` for project-level docs and `docs/specs/features/<feature-slug>/` for feature docs.
3. **Create or update the constitution.** Define `mission.md`, `tech-stack.md`, and `roadmap.md`. Keep them short, versioned, and specific enough to guide later agent runs.
4. **Write the feature spec before code.** Produce `plan.md`, `requirements.md`, and `validation.md` for each feature. Cover user flows, interfaces, constraints, task order, acceptance checks, and manual or automated verification.
5. **Implement from the spec.** Treat the spec as the source of truth. If implementation reveals a wrong assumption, update the spec and call out the change before continuing.
6. **Validate and replan.** Compare behavior and diffs against `validation.md`. After each feature, update the roadmap, constitution, or future specs if the project direction changed.

## Brownfield Adoption

For existing codebases, do not invent a constitution from the prompt alone. Reverse-engineer it from current docs, code structure, tests, configs, and commit clues. Mark uncertain claims as assumptions or questions, then use the normal feature loop for new work.

## Reference

Read `references/sdd-playbook.md` when you need templates, brownfield discovery prompts, validation scorecards, or guidance on when SDD is too heavy.
