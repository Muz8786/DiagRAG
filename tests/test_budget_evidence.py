"""Check the audit against raw records, including the corrected 100-probe row."""
import json, pathlib, subprocess, sys, tempfile, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
class BudgetEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as d:
            out = pathlib.Path(d)/'audit.json'
            subprocess.run([sys.executable, str(ROOT/'docs/evidence/v20_budget_audit.py'), str(ROOT/'kaggle'), str(out)], check=True, stdout=subprocess.DEVNULL)
            cls.audit = json.loads(out.read_text())['B3_budget_frontier']
        cls.records=[]
        for seed in (71,72,73):
            active={tuple(r['pair']):r for r in map(json.loads,(ROOT/f'kaggle/heldout_v15_S_seed{seed}/S_pairs.jsonl').read_text().splitlines())}
            for p in map(json.loads,(ROOT/f'kaggle/heldout_v16_seed{seed}/D_pairs.jsonl').read_text().splitlines()):
                a=active[tuple(p['pair'])]
                if a['effective'] and a['same_group']: cls.records.append((a,p))
    def test_population(self):
        self.assertEqual(len(self.records),238)
        self.assertEqual(self.audit['n_pairs'],len(self.records))
    def test_hundred_uses_prefix(self):
        row=next(r for r in self.audit['rows'] if r['budget_executions']==100)
        expected=sum(p['pf']['acc']['100'] for a,p in self.records)/len(self.records)
        self.assertAlmostEqual(row['passive_pass_fail'],expected)
        self.assertIn('100 random probes',row['passive_basis'])
    def test_completed_success_denominator(self):
        for row in self.audit['rows']:
            expected=sum(bool(a['both_family']) and a['runs']<=row['budget_executions'] for a,p in self.records)/len(self.records)
            self.assertAlmostEqual(row['active_named_within_budget'],expected)
    def test_no_causal_or_exact_cost_claim(self):
        self.assertFalse(self.audit['exact_cost_matched'])
        self.assertFalse(self.audit['causal_intervention_effect_identified'])
        self.assertIn('interruption',self.audit['reading'])
if __name__=='__main__': unittest.main()
