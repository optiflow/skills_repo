import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
SCRIPTS = Path(__file__).resolve().parents[2] / 'skills/create-skill/scripts'
sys.path.insert(0, str(SCRIPTS))
from aggregate_benchmark import find_runs, summarize_config, make_deltas
from score_trigger_evals import load_items

class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data))

    def add_run(self, case, config, passed=True, graded=True, duration=0, model='fixture-model'):
        run = self.root / case / config
        run.mkdir(parents=True)
        self.write(run.parent / 'eval_metadata.json', {'eval_id': case, 'eval_name': case, 'prompt': 'Draft the report.'})
        if graded:
            self.write(run / 'grading.json', {'expectations': [{'text': 'Keeps all rows', 'passed': passed, 'evidence': 'Checked fixture rows.'}]})
        self.write(run / 'timing.json', {'total_duration_seconds': duration, 'total_tokens': 0})
        self.write(run / 'run_metadata.json', {'model': model, 'runtime': 'synthetic-test', 'settings': {}, 'tools': []})
        (run / 'outputs').mkdir()
        (run / 'outputs/result.md').write_text('Report <script>alert(1)</script>')
        return run

    def summaries(self):
        return [summarize_config(k, v) for k, v in find_runs(self.root).items()]

    def cli(self, name, *args):
        return subprocess.run([sys.executable, '-B', str(SCRIPTS / name), *map(str, args)], cwd=self.root, capture_output=True, text=True)

    def test_trigger_rejects_truthy_strings_and_bad_rows(self):
        file = self.root / 'results.json'
        for items in ([{'should_trigger': False, 'triggered': 'false'}], [{'should_trigger': 'false', 'triggered': False}], [12]):
            self.write(file, items)
            with self.assertRaises(ValueError):
                load_items(file)

    def test_trigger_scores_missing_observations_as_missing(self):
        file = self.root / 'results.json'
        self.write(file, [{'should_trigger': True, 'triggered': True}, {'should_trigger': False, 'triggered': False}, {'should_trigger': True, 'triggered': None}])
        result = self.cli('score_trigger_evals.py', file)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data['accuracy'], 1)
        self.assertEqual(data['coverage'], 0.6667)
        self.assertEqual(data['total_scored'], 2)

    def test_trigger_empty_set_has_no_scores(self):
        file = self.root / 'results.json'
        self.write(file, {'evals': []})
        result = self.cli('score_trigger_evals.py', file)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsNone(json.loads(result.stdout)['accuracy'])

    def test_preserve_zero_and_pair_valid_observations(self):
        self.add_run('a', 'with_skill')
        self.add_run('a', 'old_skill', passed=False)
        configs = self.summaries()
        self.assertEqual(configs[0]['duration_seconds_mean'], 0)
        self.assertEqual(make_deltas(configs)[0]['pass_rate_delta'], 1)

    def test_missing_or_unpaired_grading_suppresses_deltas(self):
        self.add_run('a', 'with_skill')
        self.add_run('a', 'old_skill', graded=False)
        self.assertFalse(make_deltas(self.summaries()))
        self.add_run('b', 'with_skill')
        self.assertFalse(make_deltas(self.summaries()))

    def test_assertion_or_runtime_mismatch_suppresses_deltas(self):
        self.add_run('a', 'with_skill')
        old = self.add_run('a', 'old_skill', model='different-model')
        self.assertFalse(make_deltas(self.summaries()))
        self.write(old / 'run_metadata.json', {'model': 'fixture-model', 'runtime': 'synthetic-test', 'settings': {}, 'tools': []})
        self.write(old / 'grading.json', {'expectations': [{'text': 'Different check', 'passed': True, 'evidence': 'Checked.'}]})
        self.assertFalse(make_deltas(self.summaries()))

    def test_missing_provenance_suppresses_deltas(self):
        self.add_run('a', 'with_skill')
        old = self.add_run('a', 'old_skill')
        (old / 'run_metadata.json').unlink()
        self.assertFalse(make_deltas(self.summaries()))

    def test_null_provenance_suppresses_deltas(self):
        for config in ("with_skill", "old_skill"):
            run = self.add_run("a", config)
            self.write(run / "run_metadata.json", {"model": None, "runtime": None, "settings": {}, "tools": []})
        self.assertFalse(make_deltas(self.summaries()))

    def test_malformed_grades_and_invalid_measurements_fail(self):
        run = self.add_run('a', 'with_skill')
        (run / 'grading.json').write_text('{broken')
        self.assertNotEqual(self.cli('aggregate_benchmark.py', self.root).returncode, 0)
        self.write(run / 'grading.json', {'expectations': [{'text': 'Check', 'passed': 'false', 'evidence': 'Fixture'}]})
        self.assertNotEqual(self.cli('aggregate_benchmark.py', self.root).returncode, 0)
        self.write(run / 'grading.json', {'expectations': []})
        self.write(run / 'timing.json', {'total_tokens': -1})
        self.assertNotEqual(self.cli('aggregate_benchmark.py', self.root).returncode, 0)

    def test_end_to_end_aggregate_and_render_observed_data(self):
        self.add_run('a', 'with_skill')
        self.add_run('a', 'old_skill', passed=False)
        result = self.cli('aggregate_benchmark.py', self.root, '--skill-name', 'fixture-skill')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((self.root / 'benchmark.json').read_text())
        self.assertEqual(data['deltas'][0]['pass_rate_delta'], 1)
        result = self.cli('generate_review.py', self.root, '--skill-name', 'fixture-skill')
        self.assertEqual(result.returncode, 0, result.stderr)
        page = (self.root / 'review.html').read_text()
        self.assertIn('100.0%', page)
        self.assertIn('Descriptive paired differences', page)
        self.assertIn('&lt;script&gt;', page)
        self.assertNotIn('<script>alert(1)</script>', page)

if __name__ == '__main__':
    unittest.main()
