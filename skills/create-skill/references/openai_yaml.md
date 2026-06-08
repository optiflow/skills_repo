# OpenAI UI Metadata Reference

Some OpenAI skill environments can show UI-facing metadata from `agents/openai.yaml`. This file is optional and separate from trigger frontmatter.

## Recommended fields

```yaml
display_name: My Skill
short_description: Create and validate my kind of output
default_prompt: Use this skill to create a polished example from my source files.
```

## Field guidance

- `display_name`: Human-facing title. Use title case. Keep it short.
- `short_description`: One short sentence. Say the main value, not every feature.
- `default_prompt`: A useful starter prompt that shows the skill's purpose.
- `icon`: Include only if the user provides an allowed icon or asset.
- `brand_color`: Include only if the user provides a specific color.

Do not put trigger rules here. Trigger rules belong in `SKILL.md` frontmatter `description`.

## Regenerate

```bash
scripts/generate_openai_yaml.py path/to/skill \
  --interface display_name="My Skill" \
  --interface short_description="Create and validate my kind of output" \
  --interface default_prompt="Use this skill to create a polished example from my source files."
```

After updating `SKILL.md`, check whether this metadata still matches the skill.
