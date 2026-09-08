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

Install `update-skill` with the skills CLI:

```bash
npx skills add optiflow/skills_repo --skill update-skill
```

If the shorthand has not appeared on skills.sh yet, install from the direct GitHub path:

```bash
npx skills add https://github.com/optiflow/skills_repo/tree/main/skills/update-skill
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

### update-skill

Update existing skills with evidence, version severity, evals, validation, and rollback.

### back-brief

Validate task understanding and proposed plans for human-to-agent and agent-to-agent work. Make success criteria, assumptions, and open questions explicit, and use scoped review gates before execution.

### spec-driven-dev

Guide spec-driven development for AI-assisted software work. Use this for feature specs, project constitutions, validation scorecards, and structured implementation plans.

## Directory Listing

Repo pages on skills.sh are telemetry-driven. After someone installs from this repo with `npx skills`, skills.sh should pick up `skills.sh.json` and refresh the repository page after its cache updates.
