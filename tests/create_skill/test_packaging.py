import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
SCRIPTS = Path(__file__).resolve().parents[2] / 'skills/create-skill/scripts'
sys.path.insert(0, str(SCRIPTS))
from package_skill import package_skill
from quick_validate import validate_skill

class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.skill = self.root / 'small-skill'
        self.skill.mkdir()
        (self.skill / 'SKILL.md').write_text('---\nname: small-skill\ndescription: Produce small reports when a user asks for a compact status report.\n---\nWrite a report using the supplied source.\n')
        self.archive = self.root / 'dist/small-skill.skill'

    def test_invalid_source_cannot_create_or_replace_package(self):
        (self.skill / 'SKILL.md').write_text('Not a valid skill')
        self.archive.parent.mkdir()
        self.archive.write_bytes(b'existing archive')
        with self.assertRaises(ValueError):
            package_skill(self.skill, self.archive)
        self.assertEqual(self.archive.read_bytes(), b'existing archive')

    def test_nested_symlink_cannot_leak_files(self):
        external = self.root / 'private.txt'
        external.write_text('private fixture')
        (self.skill / 'data.txt').symlink_to(external)
        with self.assertRaises(ValueError):
            package_skill(self.skill, self.archive)
        self.assertFalse(self.archive.exists())

    def test_output_cannot_be_inside_source(self):
        with self.assertRaises(ValueError):
            package_skill(self.skill, self.skill / 'dist/out.skill')
        self.assertFalse((self.skill / 'dist').exists())

    def test_reproducible_archive_exclusions_and_executable_mode(self):
        (self.skill / 'scripts').mkdir()
        script = self.skill / 'scripts/helper.py'
        script.write_text('print("hello")\n')
        script.chmod(0o755)
        (self.skill / '.env').write_text('private fixture')
        (self.skill / 'scripts/__pycache__').mkdir()
        (self.skill / 'scripts/__pycache__/helper.pyc').write_bytes(b'cache')
        (self.skill / 'evals').mkdir()
        (self.skill / 'evals/evals.json').write_text(json.dumps({'skill_name': 'small-skill', 'evals': []}))
        package_skill(self.skill, self.archive)
        before = self.archive.read_bytes()
        os.utime(script, (2000000000, 2000000000))
        package_skill(self.skill, self.archive)
        self.assertEqual(before, self.archive.read_bytes())
        with zipfile.ZipFile(self.archive) as archive:
            self.assertEqual(archive.namelist(), ['small-skill/SKILL.md', 'small-skill/scripts/helper.py'])
            self.assertEqual(archive.getinfo('small-skill/scripts/helper.py').external_attr >> 16 & 0o777, 0o755)
        package_skill(self.skill, self.archive, include_evals=True)
        with zipfile.ZipFile(self.archive) as archive:
            self.assertIn('small-skill/evals/evals.json', archive.namelist())

    def test_cli_package_extract_and_validate(self):
        result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'package_skill.py'), str(self.skill), '--output', str(self.archive)], capture_output=True, text=True, cwd=self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        with zipfile.ZipFile(self.archive) as archive:
            self.assertIsNone(archive.testzip())
            archive.extractall(self.root / 'unpacked')
        self.assertEqual(validate_skill(self.root / 'unpacked/small-skill'), ([], []))

if __name__ == '__main__':
    unittest.main()
