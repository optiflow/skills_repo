# Create-skill regression checks

Use Python 3.10+ in an isolated environment. Install `skills/create-skill/scripts/requirements.txt`, then run from the repository root:

```bash
python -B -m unittest discover -s tests/create_skill -v
python -B skills/create-skill/scripts/quick_validate.py skills/create-skill --strict
```

The suite covers authoring, metadata preservation, validation, evaluation records, aggregation, packaging, and the command-line workflows that connect them. Synthetic fixtures test the helpers; they do not measure model quality or host triggering.

The trigger-review template also needs browser checks when its behavior changes: edit a query, toggle its label, add and remove cases, export the JSON, and verify the downloaded values. Include literal HTML in one query to check safe rendering. The live behavior prompts in `skills/create-skill/evals/evals.json` are separate from these deterministic tests.

## Test provenance

The original 28 tests were authored for this repository during the create-skill review and first committed in `f1b016a` (Improve create-skill guidance and validation tools). They are not an OpenAI or Anthropic test suite. They check local helper contracts and demonstrated failure cases: authoring and metadata (13), evaluation data and reporting (10), and packaging (5). The source notes identify official guidance that informed the implementation.

A 29th test was added after the installed host exposed a nested evaluation fixture as a real skill. It packages this skill with maintainer evals, checks that only the intended entrypoint is discoverable, and verifies that fixture copies can still become valid runnable skills. Stored fixture entrypoints use `SKILL.md.fixture`; rename them to `SKILL.md` only in isolated evaluation copies.

These deterministic checks do not establish model behavior, automatic discovery quality, or cross-model performance. The separate behavioral cases and fresh-agent runs provide different evidence.
