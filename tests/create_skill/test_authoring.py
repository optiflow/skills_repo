"""Observable authoring behavior, including a real scaffold/edit/validate workflow."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / 'skills/create-skill/scripts'
sys.path.insert(0, str(SCRIPTS))
from quick_validate import read_frontmatter, validate_skill, valid_name, load_yaml_mapping
from generate_openai_yaml import build_metadata, dump_yaml

class AuthoringTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.skill = self.root / 'weekly-report'
        self.skill.mkdir()
        self.write_skill()

    def write_skill(self, frontmatter=None, body='Write a report with the supplied figures and flag missing data.'):
        fm = frontmatter or 'name: weekly-report\ndescription: Summarize weekly results when the user requests a weekly business report.'
        (self.skill / 'SKILL.md').write_text('---\n' + fm + '\n---\n\n' + body + '\n')

    def cli(self, script, *args):
        return subprocess.run([sys.executable, '-B', str(SCRIPTS / script), *map(str, args)], text=True, capture_output=True, cwd=self.root)

    def test_portable_names(self):
        for name in ('a', 'weekly-report', 'a' * 64):
            self.assertTrue(valid_name(name))
        for name in ('A', '-a', 'a-', 'a--b', 'a' * 65, '', True, 12):
            self.assertFalse(valid_name(name))

    def test_folded_yaml_and_optional_fields(self):
        self.write_skill('name: weekly-report\ndescription: >-\n  Summarize weekly results\n  when asked for a business report.\nlicense: MIT\nmetadata:\n  version: "1.0"\nallowed-tools: Read')
        fm, _, errors = read_frontmatter(self.skill / 'SKILL.md')
        self.assertFalse(errors)
        self.assertEqual(fm['description'], 'Summarize weekly results when asked for a business report.')
        self.assertEqual(validate_skill(self.skill), ([], []))

    def test_reject_malformed_yaml_and_duplicate_keys(self):
        for fm in ('name: weekly-report\ndescription: bad: yaml', 'name: weekly-report\nname: other\ndescription: report', 'name: weekly-report\ndescription: [bad', 'name: weekly-report\ndescription: !!python/object:thing {}'):
            self.write_skill(fm)
            self.assertTrue(validate_skill(self.skill)[0])

    def test_description_type_length_and_folder_match(self):
        for fm in ('name: weekly-report\ndescription: false', 'name: weekly-report\ndescription: ""', 'name: weekly-report\ndescription: ' + 'x' * 1025, 'name: other\ndescription: Make weekly reports'):
            self.write_skill(fm)
            self.assertTrue(validate_skill(self.skill)[0])

    def test_syntax_check_does_not_write_cache(self):
        scripts = self.skill / 'scripts'
        scripts.mkdir()
        (scripts / 'helper.py').write_text('print("ok")\n')
        self.assertEqual(validate_skill(self.skill), ([], []))
        self.assertFalse(list(self.skill.rglob('__pycache__')))
        (scripts / 'helper.py').write_text('def broken(\n')
        self.assertTrue(validate_skill(self.skill)[0])

    def test_real_broken_links_but_not_examples(self):
        self.write_skill(body='```markdown\n[Example](references/example.md)\n```\nWrite the report.')
        self.assertFalse(validate_skill(self.skill)[0])
        self.write_skill(body='Read [the schema](references/missing.md).')
        self.assertTrue(validate_skill(self.skill)[0])

    def test_secret_findings_report_path_without_exposing_value(self):
        value = "example" * 5
        (self.skill / "assets").mkdir()
        (self.skill / "assets/config.txt").write_text("api_key=" + value)
        errors, _ = validate_skill(self.skill)
        self.assertTrue(any("assets/config.txt" in error for error in errors))
        self.assertNotIn(value, " ".join(errors))

    def test_metadata_merge_preserves_unrelated_fields(self):
        existing = {'interface': {'display_name': 'Existing', 'short_description': 'Write concise weekly business reports', 'default_prompt': 'Use $weekly-report for my report.', 'icon_small': './assets/icon.svg'}, 'policy': {'allow_implicit_invocation': False}, 'dependencies': {'tools': [{'type': 'mcp', 'value': 'drive'}]}, 'custom': {'enabled': True}}
        got = build_metadata('weekly-report', 'Description', {'display_name': 'New'}, existing)
        self.assertEqual(got['policy'], existing['policy'])
        self.assertEqual(got['dependencies'], existing['dependencies'])
        self.assertEqual(got['custom'], existing['custom'])
        self.assertEqual(got['interface']['icon_small'], './assets/icon.svg')
        self.assertEqual(existing['interface']['display_name'], 'Existing')
        self.assertEqual(load_yaml_mapping(dump_yaml(got)), got)

    def test_metadata_rejects_bad_fields_before_writing(self):
        self.assertNotEqual(self.cli('generate_openai_yaml.py', self.skill, '--interface', 'typo=Bad').returncode, 0)
        self.assertFalse((self.skill / 'agents').exists())
        with self.assertRaises(ValueError):
            build_metadata('weekly-report', 'description', {'default_prompt': 'Use $weekly-report-extra.'})

    def test_initializer_refuses_nonempty_even_with_force(self):
        before = (self.skill / 'SKILL.md').read_bytes()
        result = self.cli('init_skill.py', 'weekly-report', '--path', self.root, '--force')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.skill / 'SKILL.md').read_bytes(), before)

    def test_initializer_checks_options_before_any_write(self):
        result = self.cli('init_skill.py', 'new-report', '--path', self.root, '--resources', 'invalid')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / 'new-report').exists())

    def test_evals_reject_duplicate_ids_and_placeholder_prompts(self):
        (self.skill / 'evals').mkdir()
        item = {'id': 'one', 'prompt': 'Replace with a test', 'assertions': []}
        (self.skill / 'evals/evals.json').write_text(json.dumps({'skill_name': 'weekly-report', 'evals': [item, item]}))
        self.assertGreaterEqual(len(validate_skill(self.skill)[0]), 2)

    def test_end_to_end_authoring_from_an_unrelated_cwd(self):
        desc = 'Draft weekly reports: preserve "quoted" text and paths.\nUse supplied figures.'
        result = self.cli('init_skill.py', 'new-report', '--path', self.root, '--description', desc, '--openai-agent')
        self.assertEqual(result.returncode, 0, result.stderr)
        target = self.root / 'new-report'
        self.assertEqual(read_frontmatter(target / 'SKILL.md')[0]['description'], desc)
        self.assertTrue(validate_skill(target)[0], 'unfinished draft must not pass validation')
        text = (target / 'SKILL.md').read_text()
        text = text[:text.index('[TODO:')] + 'Use the supplied figures to write the weekly report.\n'
        (target / 'SKILL.md').write_text(text)
        self.assertEqual(self.cli('quick_validate.py', target, '--strict').returncode, 0)
        metadata = load_yaml_mapping((target / 'agents/openai.yaml').read_text())
        metadata['policy'] = {'allow_implicit_invocation': False}
        (target / 'agents/openai.yaml').write_text(dump_yaml(metadata))
        result = self.cli('generate_openai_yaml.py', target, '--interface', 'display_name=New Weekly Report')
        self.assertEqual(result.returncode, 0, result.stderr)
        final = load_yaml_mapping((target / 'agents/openai.yaml').read_text())
        self.assertFalse(final['policy']['allow_implicit_invocation'])
        self.assertEqual(self.cli('quick_validate.py', target, '--strict').returncode, 0)

if __name__ == '__main__':
    unittest.main()
