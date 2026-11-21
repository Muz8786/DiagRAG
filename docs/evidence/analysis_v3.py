"""Post-run analyses of the v3 seed-45 judged run (checkpoint). Labelled EXPLORATORY where not pre-registered.
(1) paired comparisons on natural traffic (held-out natural queries, already scored inside the run)
(2) identifiability: out-of-fold pairwise AUROC on the TRAIN split only, certified TV lower bounds (IDENTIFIABILITY.md)."""
import json, pickle, sys, math, collections
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score
R = pickle.load(open(sys.argv[1], 'rb')); out = {}
rows = list(R['NAT3'].values()); rng = np.random.default_rng(45)
def paired(a, b):
    d = np.array([int(x) - int(y) for x, y in zip(a, b)], float); bs = d[rng.integers(0, len(d), (4000, len(d)))].mean(1)
    return dict(mean=float(d.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], n=len(d))
out['exploratory_natural'] = dict(
    rules_gated_vs_k12_always=paired([r['h_rules'] for r in rows], [r['h_k12_always'] for r in rows]),
    deployed_loop_vs_universal=paired([r['h_loop'] for r in rows], [r['h_univ'] for r in rows]),
    deployed_loop_vs_rules_only=paired([r['h_loop'] for r in rows], [r['h_rules'] for r in rows]),
    cost=dict(deployed_loop=float(np.mean([r['cost_loop'] for r in rows])), universal=12.0,
              rules_only=float(np.mean([3 * len(r['nat']) for r in rows]))))
TR = [e for e in R['EPIS'] if e['split'] == 'train' and e['fault'] not in ('C2', 'NONE')]
FE = sorted(TR[0]['feats']); X = np.array([[e['feats'][k] for k in FE] for e in TR], np.float32); y = np.array([e['fault'] for e in TR]); g = [e['bid'] for e in TR]
faults = sorted(set(y)); pair = {}
for i, a in enumerate(faults):
    for b in faults[i + 1:]:
        m = (y == a) | (y == b); Xa, ya, ga = X[m], (y[m] == a).astype(int), [g[k] for k in np.where(m)[0]]; s = np.zeros(len(ya))
        for tr_i, te_i in GroupKFold(5).split(Xa, ya, ga):
            s[te_i] = HistGradientBoostingClassifier(max_iter=150, min_samples_leaf=5, random_state=0).fit(Xa[tr_i], ya[tr_i]).predict_proba(Xa[te_i])[:, 1]
        auc = float(roc_auc_score(ya, s)); auc = max(auc, 1 - auc)
        pair[f'{a}|{b}'] = dict(oof_auroc=round(auc, 3), tv_lower_bound=round(max(0.0, 1 - math.sqrt(max(0.0, 2 - 2 * auc))), 3))
out['pairwise'] = pair
low = sorted(pair.items(), key=lambda kv: kv[1]['oof_auroc'])
out['least_separable_15'] = low[:15]
out['n_pairs'] = len(pair); out['pairs_auroc_ge_0.95'] = sum(v['oof_auroc'] >= 0.95 for v in pair.values())
out['pairs_auroc_lt_0.80'] = [k for k, v in pair.items() if v['oof_auroc'] < 0.80]
parent = {f: f for f in faults}                                  # classes = connected components of pairs with AUROC < 0.80
def find(x):
    while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
    return x
for k in out['pairs_auroc_lt_0.80']:
    a, b = k.split('|'); parent[find(a)] = find(b)
cls = collections.defaultdict(list)
for f in faults: cls[find(f)].append(f)
out['induced_classes_auroc_lt_0.80'] = sorted([v for v in cls.values() if len(v) > 1], key=len, reverse=True)
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'pairwise'}, indent=1)[:3500])
