"""v17 summary: the A1 rule (S-1..S-5, S-5 as amended for the second stack) on one confirmation run. File reading and arithmetic only.
usage: python docs/evidence/v17_summary.py <run_dir> <out.json>"""
import json, os, sys
import numpy as np

d, out = sys.argv[1:3]; rng = np.random.default_rng(7)
rd = lambda f: [json.loads(l) for l in open(os.path.join(d, f))]
S, P = rd('S_single.jsonl'), rd('S_pairs.jsonl'); R0 = json.load(open(os.path.join(d, 'RESULT.json')))
m = lambda xs, k: float(np.mean([bool(x[k]) for x in xs])) if xs else None
def boot(vals, n=4000):
    v = np.asarray(vals, float)
    if len(v) == 0: return dict(mean=None, ci=[None, None])
    bs = v[rng.integers(0, len(v), (n, len(v)))].mean(1); return dict(mean=float(v.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])
HS = [r for r in S if r['harmful']]; HT = [r for r in HS if 'traffic' in r and r['traffic']['closure']['selftest'] is not None]
EP = [r for r in P if r['effective']]; EG = [r for r in EP if r['same_group']]; ET = [r for r in EP if r['traffic']['closure']['selftest'] is not None]
cl = lambda rows, who: [r['traffic']['closure'][who] for r in rows]
hm = lambda rows, who: [r['traffic']['harm'][who] for r in rows if r['traffic']['harm'][who] is not None]
d4 = boot([int(r['both_family']) - int(r['agg_dispatcher_both']) for r in EG])
dS = boot([a - b for a, b in zip(cl(HT, 'selftest'), cl(HT, 'loop'))]); dP = boot([a - b for a, b in zip(cl(ET, 'selftest'), cl(ET, 'loop'))])
c_s_inst, c_p_inst = float(np.mean(cl(HT, 'selftest'))) if HT else None, float(np.mean(cl(ET, 'selftest'))) if ET else None
pooled = lambda rows: (float(sum(r['traffic']['closure']['selftest'] * r['traffic']['broken'] for r in rows) / sum(r['traffic']['broken'] for r in rows)) if rows and sum(r['traffic']['broken'] for r in rows) else None)
c_s, c_p = pooled(HT), pooled(ET)   # A3: share of broken traffic queries restored
h_s, h_p = (float(np.mean(hm(HT, 'selftest'))) if hm(HT, 'selftest') else 0.0), (float(np.mean(hm(ET, 'selftest'))) if hm(ET, 'selftest') else 0.0)
rule = {'S-1 detection >= 0.95': bool(m(HS, 'detected') is not None and m(HS, 'detected') >= 0.95),
        'S-2 family >= 0.90': bool(m(HS, 'family') is not None and m(HS, 'family') >= 0.90),
        'S-3 verified >= 0.95 (singles, pairs)': bool(min(m(HS, 'verified') or 0, m(EP, 'verified') or 0) >= 0.95),
        'S-4 same-group pairs both named >= 0.70 and above aggregated (LB > 0)': bool(EG and m(EG, 'both_family') >= 0.70 and d4['ci'][0] > 0),
        'S-5 closure >= 0.95, harm <= 0.5%, pairs above loop (LB > 0), singles not below (LB > -0.05)': bool(None not in (c_s, c_p) and min(c_s, c_p) >= 0.95 and max(h_s, h_p) <= 0.005 and dP['ci'][0] > 0 and dS['ci'][0] > -0.05)}
R = dict(run=os.path.basename(d.rstrip('/')), role=R0['role'], dataset=R0['dataset'], battery=R0['battery'], harmful_singles=len(HS), singles=len(S),
         detected=m(HS, 'detected'), family=m(HS, 'family'), exact=m(HS, 'exact'), verified_singles=m(HS, 'verified'), effective_pairs=len(EP), same_group_pairs=len(EG),
         both_family_same_group=m(EG, 'both_family'), both_family_all=m(EP, 'both_family'), agg_same_group=m(EG, 'agg_dispatcher_both'), diff_vs_agg=d4, verified_pairs=m(EP, 'verified'),
         closure=dict(singles=dict(selftest=c_s, selftest_per_instance_mean=c_s_inst, broken_queries=sum(r['traffic']['broken'] for r in HT), loop=float(np.mean(cl(HT, 'loop'))) if HT else None, universal=float(np.mean(cl(HT, 'universal'))) if HT else None, diff=dS),
                      pairs=dict(selftest=c_p, selftest_per_instance_mean=c_p_inst, broken_queries=sum(r['traffic']['broken'] for r in ET), loop=float(np.mean(cl(ET, 'loop'))) if ET else None, universal=float(np.mean(cl(ET, 'universal'))) if ET else None, diff=dP)),
         harm=dict(singles=dict(selftest=h_s, loop=float(np.mean(hm(HT, 'loop'))) if hm(HT, 'loop') else None, universal=float(np.mean(hm(HT, 'universal'))) if hm(HT, 'universal') else None),
                   pairs=dict(selftest=h_p, loop=float(np.mean(hm(ET, 'loop'))) if hm(ET, 'loop') else None, universal=float(np.mean(hm(ET, 'universal'))) if hm(ET, 'universal') else None)),
         rule=rule, S_PASS=bool(all(rule.values())))
json.dump(R, open(out, 'w'), indent=1); print(json.dumps(R, indent=1))
