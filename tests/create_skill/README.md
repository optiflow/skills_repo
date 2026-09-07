# Create-skill regression checks

Use Python 3.10+ in an isolated environment. Install `skills/create-skill/scripts/requirements.txt`, then run from the repository root:

```bash
python -B -m unittest discover -s tests/create_skill -v
python -B skills/create-skill/scripts/quick_validate.py skills/create-skill --strict
```

The suite covers authoring, metadata preservation, validation, evaluation records, aggregation, packaging, and the command-line workflows that connect them. Synthetic fixtures test the helpers; they do not measure model quality or host triggering.

The trigger-review template also needs browser checks when its behavior changes: edit a query, toggle its label, add and remove cases, export the JSON, and verify the downloaded values. Include literal HTML in one query to check safe rendering. The live behavior prompts in `skills/create-skill/evals/evals.json` are separate from these deterministic tests.
