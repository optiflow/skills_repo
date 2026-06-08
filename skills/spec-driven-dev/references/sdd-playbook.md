# SDD Playbook

Use this reference for spec-driven development templates and review gates. Keep specs practical: enough structure to guide the agent, not so much process that the project stalls.

## Source Ideas

- SDD makes a versioned spec the source of truth for requirements, constraints, and validation.
- The useful loop is constitution -> feature spec -> implementation -> validation -> replanning.
- Specs preserve project context across sessions and agents.
- SDD fits larger or longer-lived work better than one-off scripts and open-ended experiments.

## Constitution Template

Create these files when no project-level spec exists:

```text
docs/specs/constitution/
|-- mission.md
|-- tech-stack.md
`-- roadmap.md
```

`mission.md`:

```markdown
# Mission

## Goal
[What the product or system must achieve.]

## Users
[Primary users and their concrete needs.]

## Scope
[What this project includes.]

## Non-Goals
[What this project will not solve now.]

## Success Criteria
[Observable outcomes that prove the mission is met.]
```

`tech-stack.md`:

```markdown
# Tech Stack

## Runtime and Frameworks
[Languages, frameworks, versions, and package managers.]

## Data and Integrations
[Databases, APIs, queues, files, auth, and external systems.]

## Engineering Rules
[Testing, type safety, security, performance, accessibility, and style rules.]

## Known Constraints
[Hosted limits, compatibility needs, migration limits, and forbidden changes.]
```

`roadmap.md`:

```markdown
# Roadmap

## Current Phase
[The next meaningful delivery slice.]

## Planned Phases
1. [Phase name] - [outcome and key checks]
2. [Phase name] - [outcome and key checks]

## Backlog
[Ideas to revisit later, with links to research or notes.]
```

## Feature Spec Template

Default path: `docs/specs/features/<feature-slug>/`.

`plan.md`:

```markdown
# Feature Plan: [Name]

## Goal
[User-facing outcome.]

## Approach
[Main design choice and why it fits the constitution.]

## Task Groups
1. [Task group] - [expected files or subsystem]
2. [Task group] - [expected files or subsystem]

## Dependencies
[Libraries, services, migrations, feature flags, or upstream work.]

## Out of Scope
[Work that must not be bundled into this feature.]
```

`requirements.md`:

```markdown
# Requirements: [Name]

## User Scenarios
- As a [user], I can [action], so that [outcome].

## Functional Requirements
- WHEN [trigger], the system SHALL [response].
- IF [error or edge case], THEN the system SHALL [safe response].

## Interfaces
[Routes, CLI commands, schemas, props, events, files, or API contracts.]

## Constraints
[Version pins, compatibility rules, security limits, performance budgets.]

## Assumptions and Questions
- Assumption: [Fact inferred from repo or user prompt.]
- Question: [Only ask if it can change the design.]
```

`validation.md`:

```markdown
# Validation: [Name]

## Automated Checks
- [Command] - [what it proves]

## Manual Checks
- [User flow or review step] - [expected result]

## Diff Review
- [High-level behavior or architecture concern to inspect]

## Done When
- [Observable acceptance criterion]
```

## Brownfield Discovery

Before changing an existing repo, inspect:

- Agent instructions: `AGENTS.md`, `.agents/`, `.codex/`, or tool-specific rules.
- Project docs: `README`, `docs/`, design notes, PRDs, TODO files.
- Entry points: package manifests, build configs, routing files, server files.
- Tests and checks: unit, integration, end-to-end, lint, typecheck, CI configs.
- Domain clues: schemas, API types, migrations, fixtures, seed data.

Then draft a constitution that separates confirmed facts from assumptions.

## Replanning Checklist

Use this after each feature or when validation finds drift:

- Did implementation match the feature spec?
- Did any spec assumption prove false?
- Did the roadmap order change?
- Did the tech stack gain a new rule, dependency, or constraint?
- Should a follow-up become its own feature spec instead of being added now?

## When Not to Use Full SDD

Use a short plan instead of the full artifact set when:

- The task is a tiny one-file fix or script.
- The work is a throwaway prototype.
- Requirements are still being discovered through research or design exploration.
- The user asks for a quick answer, review, or command output, not a build.

Even then, keep a small validation check: what will prove the change worked?
