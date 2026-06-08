# Workflow Modes Reference

Use this when the ideal evaluation loop is not fully available.

## Full mode

Use when you have independent agent runs, filesystem access, and can create review artifacts.

1. Draft or edit the skill.
2. Create eval prompts.
3. Run with-skill and baseline runs independently.
4. Grade objective assertions.
5. Aggregate benchmark results.
6. Generate a review page.
7. Improve from scores and human feedback.
8. Repeat until gains are clear or progress stalls.

## Single-agent mode

Use when there are no subagents.

1. Read the skill as the tested agent would.
2. Run each test prompt inline.
3. Save outputs under an iteration directory when a filesystem is available.
4. Skip formal baseline claims unless you can run a fair baseline.
5. Ask for human review or compare outputs manually.
6. State that this is a sanity check, not a rigorous benchmark.

## No-browser or headless mode

Generate static files instead of opening a server:

```bash
scripts/generate_review.py my-skill-workspace/iteration-1 --static review.html
```

Provide the HTML file as an artifact or path.

## No filesystem mode

Keep the loop in the conversation:

- Show the draft `SKILL.md`.
- Show 2-5 test prompts.
- Summarize expected outputs and likely assertions.
- Ask for feedback on the draft and test set.
- Do not claim scripts were tested or benchmarks were run.

## Updating installed or read-only skills

If the source skill cannot be edited directly:

1. Copy it to a writable folder.
2. Preserve the original folder name and frontmatter name unless the user asks for a rename.
3. Snapshot the original before changing it.
4. Use the snapshot as the baseline.
5. Package from the writable copy.

## Lightweight mode

For small private skills, it is acceptable to skip full benchmarking when the user wants speed. Still do these minimum checks:

- Valid frontmatter.
- Clean folder structure.
- No surprise files or secrets.
- Important scripts run on representative inputs.
- At least two realistic usage prompts are written down.
