"""PRE-REGISTERED analysis of the v3 GPU flagship run (seed 46). Written and committed BEFORE that run produced results.
Input: the run's checkpoint.pkl + VERDICT.json. Output: JSON with the verdict for every criterion below.

G  replication of the v3 loop gates on the GPU stack: L1, L2, U1, N1 exactly as frozen in diagrag_v3.py (read from VERDICT).
D1 diagnosis vs diagnosis-free, injected held-out: mean closure(mondrian_crc_0.005) - mean closure(universal) >= 0.05
   AND clean loss(mondrian) < clean loss(universal).
D2 diagnosis vs diagnosis-free, natural traffic: paired delta Hit@5 (deployed loop - universal), 95% bootstrap CI lower
   bound > -0.005 (non-inferiority margin 0.5 points) AND mean loop cost <= 0.6 x 12.
D3 detection gating, natural traffic (confirmatory replication of the exploratory v3 CPU finding): paired delta
   (natural rules gated - K12 always on), 95% CI lower bound > 0.
Bootstrap: 4000 resamples, seed 46."""
import json, pickle, sys
import numpy as np
R = pickle.load(open(sys.argv[1], 'rb')); V = json.load(open(sys.argv[2])); rng = np.random.default_rng(46)
rows = list(R['NAT3'].values())
def paired(a, b):
    d = np.array([int(x) - int(y) for x, y in zip(a, b)], float); bs = d[rng.integers(0, len(d), (4000, len(d)))].mean(1)
    return dict(mean=float(d.mean()), ci_lo=float(np.percentile(bs, 2.5)), ci_hi=float(np.percentile(bs, 97.5)), n=len(d))
pol = {p['policy']: p for p in V['policies']}; m, u = pol['mondrian_crc_0.005'], pol['diagnosis_free_universal']
d2 = paired([r['h_loop'] for r in rows], [r['h_univ'] for r in rows]); cost = float(np.mean([r['cost_loop'] for r in rows]))
d3 = paired([r['h_rules'] for r in rows], [r['h_k12_always'] for r in rows])
out = dict(
    G=dict(V['loop_gates'], solved_28=f"{V['solved_both']}/{V['of']}", grounded=f"{V['grounded']['solved_both']}/{V['grounded']['of']}"),
    D1=dict(closure_loop=m['mean_closure'], closure_universal=u['mean_closure'], clean_loss_loop=m['clean_loss'], clean_loss_universal=u['clean_loss'],
            verdict='PASS' if m['mean_closure'] - u['mean_closure'] >= 0.05 and m['clean_loss'] < u['clean_loss'] else 'FAIL'),
    D2=dict(paired_loop_minus_universal=d2, mean_cost_loop=cost, verdict='PASS' if d2['ci_lo'] > -0.005 and cost <= 0.6 * 12 else 'FAIL'),
    D3=dict(paired_rules_minus_k12_always=d3, verdict='PASS' if d3['ci_lo'] > 0 else 'FAIL'))
json.dump(out, open(sys.argv[3], 'w'), indent=1); print(json.dumps(out, indent=1))
