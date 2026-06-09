# Skills Repo

[![skills.sh](https://skills.sh/b/optiflow/skills_repo)](https://skills.sh/optiflow/skills_repo)

Reusable agent skills for skill authoring, task alignment, and spec-driven development.

## Quick Install

Install `create-skill` with the skills CLI:

```bash
npx skills add optiflow/skills_repo --skill create-skill
```

If the shorthand has not appeared on skills.sh yet, install from the direct GitHub path:

```bash
npx skills add https://github.com/optiflow/skills_repo/tree/main/skills/create-skill
```

Install `back-brief` with the skills CLI:

```bash
npx skills add optiflow/skills_repo --skill back-brief
```

If the shorthand has not appeared on skills.sh yet, install from the direct GitHub path:

```bash
npx skills add https://github.com/optiflow/skills_repo/tree/main/skills/back-brief
```

List all skills in this repo:

```bash
npx skills add optiflow/skills_repo --list
```

## Skills

### create-skill

Create, update, validate, evaluate, optimize, and package AI agent skills.

### back-brief

Confirm task intent before material execution. Use this when a task is ambiguous, risky, multi-step, file-changing, high-cost, or when the user asks the agent to restate the requirement before acting.

### spec-driven-dev

Guide spec-driven development for AI-assisted software work. Use this for feature specs, project constitutions, validation scorecards, and structured implementation plans.

## Directory Listing

Repo pages on skills.sh are telemetry-driven. After someone installs from this repo with `npx skills`, skills.sh should pick up `skills.sh.json` and refresh the repository page after its cache updates.
