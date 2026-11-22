"""Route B of the U1 analysis (docs/evidence/v5_protocol.md amendment B8). TRAIN split only. Read-only.
Usage: python route_b.py <episodes.jsonl of a judged run> <unseen_faults.csv files...> --out result.json
Part 1: pairwise out-of-fold AUROC for all pairs of the 31 single faults, cluster-bootstrap CI, certified TV lower bound 1 - sqrt(2 - 2a).
Part 2: nearest-confusable-partner diagnostic (NOT a proved ceiling; see B8 item 2).
Part 3: oracle-group closure from unseen_faults.csv files: mean of min(1, closure / right_group)."""
import argparse, collections, csv, itertools, json, math, os
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold

ap = argparse.ArgumentParser(); ap.add_argument('episodes'); ap.add_argument('unseen', nargs='*'); ap.add_argument('--out', required=True); ap.add_argument('--boot', type=int, default=500); a = ap.parse_args()
rows = [json.loads(l) for l in open(a.episodes, encoding='utf-8')]
TR = [e for e in rows if e['split'] == 'train' and e['fault'] not in ('C2', 'NONE')]
FE = sorted(TR[0]['feats']); X = np.array([[e['feats'][k] for k in FE] for e in TR], np.float32); y = np.array([e['fault'] for e in TR]); g = np.array([e['bid'] for e in TR])
faults = sorted(set(y)); assert len(faults) == 31, len(faults)
GROUP = lambda f: f[0]; rng = np.random.default_rng(0)
tv = lambda auc: max(0.0, 1 - math.sqrt(max(0.0, 2 - 2 * auc)))
pairs = {}
for f1, f2 in itertools.combinations(faults, 2):
    m = (y == f1) | (y == f2); Xa, ya, ga = X[m], (y[m] == f1).astype(int), g[m]; s = np.zeros(len(ya))
    for tr_i, te_i in GroupKFold(5).split(Xa, ya, ga):
        s[te_i] = HistGradientBoostingClassifier(max_iter=150, min_samples_leaf=5, random_state=0).fit(Xa[tr_i], ya[tr_i]).predict_proba(Xa[te_i])[:, 1]
    auc = roc_auc_score(ya, s); flip = auc < 0.5; auc = max(auc, 1 - auc); sc = s if not flip else 1 - s
    ug = np.unique(ga); idx = {u: np.where(ga == u)[0] for u in ug}; bs = []
    for _ in range(a.boot):
        pick = rng.choice(len(ug), len(ug), replace=True); ii = np.concatenate([idx[ug[j]] for j in pick])
        if len(set(ya[ii])) == 2: bs.append(roc_auc_score(ya[ii], sc[ii]))
    lo, hi = float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
    pairs[f'{f1}|{f2}'] = dict(auroc=float(auc), ci=[lo, hi], tv_lb=tv(auc), tv_lb_at_ci_lo=tv(lo), n=int(m.sum()))
low = sorted(pairs.items(), key=lambda kv: kv[1]['auroc'])
out = dict(n_pairs=len(pairs), n_train_episodes=len(TR), pairs=pairs, least_separable_20=[(k, round(v['auroc'], 3), [round(x, 3) for x in v['ci']], round(v['tv_lb'], 3)) for k, v in low[:20]],
           share_auroc_ge_0p95=float(np.mean([v['auroc'] >= 0.95 for v in pairs.values()])), share_auroc_lt_0p80=float(np.mean([v['auroc'] < 0.80 for v in pairs.values()])),
           median_tv_lb=float(np.median([v['tv_lb'] for v in pairs.values()])))
# part 2: nearest confusable partner
part = {}
for f in faults:
    cand = [(v['auroc'], (k.split('|')[1] if k.split('|')[0] == f else k.split('|')[0])) for k, v in pairs.items() if f in k.split('|')]
    au, partner = min(cand); part[f] = dict(partner=partner, auroc=float(au), same_group=GROUP(partner) == GROUP(f))
out['nearest_partner'] = part; out['share_nearest_partner_same_group'] = float(np.mean([v['same_group'] for v in part.values()]))
out['share_nearest_partner_other_group'] = 1 - out['share_nearest_partner_same_group']
out['diagnostic_note'] = 'NOT a proved ceiling: a pairwise AUROC does not say where an attributor trained without f routes f (B8 item 2).'
# part 3: oracle-group closure
og = {}
for p in a.unseen:
    rr = list(csv.DictReader(open(p))); c = np.array([float(r['closure']) for r in rr]); rg = np.array([float(r['right_group']) for r in rr])
    cond = np.where(rg > 0, np.minimum(1.0, c / np.maximum(rg, 1e-9)), 0.0)
    og[p] = dict(n_faults=len(rr), U1=float(c.mean()), mean_right_group=float(rg.mean()), oracle_group_closure=float(cond.mean()),
                 zero_closure_faults=sorted(r['fault'] for r, x in zip(rr, c) if x <= 0.08))
out['oracle_group_closure'] = og
json.dump(out, open(a.out, 'w'), indent=1)
print('pairs', len(pairs), '| AUROC>=0.95: %.3f | <0.80: %.3f | median certified TV lower bound %.3f' % (out['share_auroc_ge_0p95'], out['share_auroc_lt_0p80'], out['median_tv_lb']))
print('least separable 8:', out['least_separable_20'][:8])
print('nearest confusable partner in the SAME group: %.2f, OTHER group: %.2f' % (out['share_nearest_partner_same_group'], out['share_nearest_partner_other_group']))
for p, v in og.items(): print(os.path.basename(os.path.dirname(p)), 'U1 %.3f right_group %.3f oracle-group closure %.3f' % (v['U1'], v['mean_right_group'], v['oracle_group_closure']))
