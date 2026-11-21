"""Summarise v13_idea2.py output: macro closure per policy, paired bootstrap over faults, mean cost. usage: python v13_idea2_summary.py <out.jsonl> [<out.json>]"""
import collections, json, sys
import numpy as np
R = [json.loads(l) for l in open(sys.argv[1])]; F = sorted({r['fault'] for r in R})
pf = {f: {k: float(np.mean([r[k] for r in R if r['fault'] == f])) for k in ('P0', 'P2_ok', 'P12_ok', 'oracle', 'P2_cost', 'P12_cost')} for f in F}
mac = {k: float(np.mean([pf[f][k] for f in F])) for k in ('P0', 'P2_ok', 'P12_ok', 'oracle')}
rng = np.random.default_rng(7); B = [rng.integers(0, len(F), len(F)) for _ in range(2000)]
def diff(a): x = np.array([pf[f][a] - pf[f]['P0'] for f in F]); bs = [x[i].mean() for i in B]; return dict(mean=float(x.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])
out = dict(n_episodes=len(R), n_faults=len(F), macro=mac, P2_minus_P0=diff('P2_ok'), P12_minus_P0=diff('P12_ok'),
           mean_cost=dict(P0=1.0, P2=float(np.mean([r['P2_cost'] for r in R])), P12=float(np.mean([r['P12_cost'] for r in R]))), per_fault=pf)
print(json.dumps({k: v for k, v in out.items() if k != 'per_fault'}, indent=1))
for f in F: print(f"  {f}: P0 {pf[f]['P0']:.2f}  P2 {pf[f]['P2_ok']:.2f}  P12 {pf[f]['P12_ok']:.2f}  oracle {pf[f]['oracle']:.2f}  cost P2 {pf[f]['P2_cost']:.1f} P12 {pf[f]['P12_cost']:.1f}")
if len(sys.argv) > 2: json.dump(out, open(sys.argv[2], 'w'), indent=1)
