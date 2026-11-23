import unittest
import tempfile
import json
from pathlib import Path
from demo import run

class ExperimentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.output=Path(cls.temp.name)/'results.json'
        cls.r=run(cls.output)
    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()
    def test_output_matches_returned_result(self):
        self.assertEqual(json.loads(self.output.read_text()),self.r)
    def test_action_counts(self):
        from demo import simulate
        self.assertEqual(sum(simulate('ucb1',0,100)['arm_counts']),100)
    def test_reward_limits(self):
        self.assertTrue(all(0<=r['reward']<=3000 for p in self.r['policies'].values() for r in p['per_seed']))
    def test_seeds_complete(self):
        self.assertTrue(all(len(p['per_seed'])==20 for p in self.r['policies'].values()))

if __name__ == "__main__":
    unittest.main()
