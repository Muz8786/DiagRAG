"""POST-HOC, DESCRIPTIVE (not pre-registered). Splits the natural-traffic result (1,648 never-examined queries) by whether the query's gold document has real content.
Why: the census found that the gold document is an empty placeholder ("nan") for many queries, and the placeholder document itself counts as a hit when it is retrieved,
so a gain on those queries may not mean a better answer. Reads a v6/v7 checkpoint (NAT3 rows: h0 = clean Hit@5, h_loop, h_univ, h_rules, h_clf; CENS rows: gold_is_nan).
usage: python natural_split_by_gold.py <checkpoint.pkl> <out.json>"""
import json, pickle, sys
import numpy as np
R = pickle.load(open(sys.argv[1], 'rb')); N = R['NAT3']; C = R['CENS']; ks = list(N)
def stats(keys):
    g = lambda f: np.array([N[k][f] for k in keys], int); h0 = g('h0'); n = len(keys); out = dict(n=n, baseline_hit5=float(h0.mean()), baseline_misses=int((h0 == 0).sum()))
    for arm in ('h_loop', 'h_rules', 'h_clf', 'h_univ', 'h_k12_always'):
        a = g(arm); d = a - h0; rng = np.random.default_rng(0); bs = [d[rng.integers(0, n, n)].mean() for _ in range(4000)]
        out[arm] = dict(delta_points=float(100 * d.mean()), ci_lo=float(100 * np.percentile(bs, 2.5)), ci_hi=float(100 * np.percentile(bs, 97.5)), fixed=int(((h0 == 0) & (a == 1)).sum()), broken=int(((h0 == 1) & (a == 0)).sum()))
    return out
ok = [k for k in ks if not C[k]['gold_is_nan']]; nan = [k for k in ks if C[k]['gold_is_nan']]
res = dict(post_hoc=True, all=stats(ks), gold_has_content=stats(ok), gold_is_placeholder=stats(nan))
json.dump(res, open(sys.argv[2], 'w'), indent=1)
for k in ('all', 'gold_has_content', 'gold_is_placeholder'):
    r = res[k]; print(f"{k:20s} n={r['n']:5d} baseline {r['baseline_hit5']:.3f} | loop {r['h_loop']['delta_points']:+.2f} [{r['h_loop']['ci_lo']:+.2f},{r['h_loop']['ci_hi']:+.2f}] fixed {r['h_loop']['fixed']} broken {r['h_loop']['broken']} | rules {r['h_rules']['delta_points']:+.2f} | clf-only {r['h_clf']['delta_points']:+.2f} | universal {r['h_univ']['delta_points']:+.2f} fixed {r['h_univ']['fixed']} broken {r['h_univ']['broken']}")
