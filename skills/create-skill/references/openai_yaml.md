# OpenAI metadata

Use this only for hosts that consume `agents/openai.yaml`. It is an optional host extension, separate from portable frontmatter.

```yaml
interface:
  display_name: "Reconcile Invoices"
  short_description: "Reconcile invoice exports and payment records"
  default_prompt: "Use $reconcile-invoices to check these invoice and payment files."
```

Put UI values under `interface`. `short_description` is 25-64 characters. `default_prompt` should mention the exact `$skill-name`. Optional `icon_small`, `icon_large`, and `brand_color` belong under `interface`; add them only when supplied or requested.

Preserve an existing `policy`, `dependencies`, and unrelated interface fields. For example, an existing explicit-only policy is:

```yaml
policy:
  allow_implicit_invocation: false
```

Do not infer this policy from sensitive operations. Keep automatic selection as the default for new skills unless the user requests explicit-only invocation; describe any actual approval requirement at the operation that needs it.

## Create or update

Run the bundled helper from the create-skill directory, or use its absolute path:

```bash
python -B scripts/generate_openai_yaml.py /path/to/reconcile-invoices \
  --interface 'display_name=Reconcile Invoices' \
  --interface 'short_description=Reconcile invoice exports and payment records' \
  --interface 'default_prompt=Use $reconcile-invoices to check these files.'
```

Single quotes protect the dollar sign from shell expansion. This helper merges supplied fields and fills missing required UI defaults. It preserves policy, dependencies, and other settings as data, but YAML comments and layout may change. Review the diff if comments matter.

Earlier create-skill versions wrote flat UI fields. This helper can move supported flat fields under `interface`; supply a valid default prompt if the old one lacks the skill mention. An old `icon` field needs a choice between `icon_small` and `icon_large`; the helper reports it rather than guessing.

Field support and discovery paths can vary by host version. Check the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) and [OpenAI's field reference](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.system/skill-creator/references/openai_yaml.md) for the target environment.
