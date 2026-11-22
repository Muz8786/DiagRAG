"""Brief section 3 (C2): decompose the seed-48 C2 detector failure from the shipped episodes. Read-only; no code, bar or threshold changes.
Usage: python c2_decomposition.py <judged_gpu_v4_seed48 folder> <out.json>

Questions asked, in the brief's terms:
 (a) how many seed-48 test positives are there;
 (b) their score distribution under the seed-48 head versus other heads (here: 40 cluster-bootstrap re-fits of the head, and the train-split positives scored by the same head);
 (c) whether the low-scoring positives share a construction feature (pair type, episode source, tenant, k, injector parameters).
C2's score is the second-largest group probability mass of the single-fault attributor, which never trains on C2 episodes (diagrag_v4.py section 12)."""
import collections, hashlib, json, os, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

folder, outp = sys.argv[1], sys.argv[2]
rows = [json.loads(l) for l in open(os.path.join(folder, 'episodes.jsonl'), encoding='utf-8')]
SEED = 48; GROUP = lambda f: f[0]
FE = sorted(rows[0]['feats']); mat = lambda es: np.array([[e['feats'][k] for k in FE] for e in es], np.float32)
sing = [e for e in rows if e['fault'] != 'C2']; TR = [e for e in sing if e['split'] == 'train']; TE = [e for e in sing if e['split'] == 'test']
C2te = [e for e in rows if e['fault'] == 'C2' and e['split'] == 'test']; C2tr = [e for e in rows if e['fault'] == 'C2' and e['split'] == 'train']
hg = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=SEED)
CAL = {e['bid'] for e in TR if e['fault'] == 'NONE' and int(hashlib.md5(('cal|' + e['bid']).encode()).hexdigest()[:8], 16) / 2**32 < 0.5}
keep = [e for e in TR if not (e['fault'] == 'NONE' and e['bid'] in CAL)]; Xk, yk = mat(keep), np.array([e['fault'] for e in keep])

def second_mass(att, es):
    p = att.predict_proba(mat(es)); cls = list(att.classes_); gm = np.zeros((len(es), 3))
    for j, c_ in enumerate(cls):
        if c_ != 'NONE': gm[:, 'QKR'.index(GROUP(c_))] += p[:, j]
    return np.sort(gm, 1)[:, -2]

att0 = hg().fit(Xk, yk)
neg = second_mass(att0, TE); pos_te = second_mass(att0, C2te); pos_tr = second_mass(att0, C2tr)
y1 = np.array([1] * len(pos_te) + [0] * len(neg)); auc_te = roc_auc_score(y1, np.concatenate([pos_te, neg]))
out = dict(a_n_test_positives=len(C2te), a_n_train_positives=len(C2tr), a_n_test_negatives=len(neg), auroc_test_refit=float(auc_te),
           auroc_train_positives_same_head=float(roc_auc_score(np.array([1] * len(pos_tr) + [0] * len(neg)), np.concatenate([pos_tr, neg]))))
# (b1) head variance: cluster-bootstrap re-fits of the head (resample base queries with replacement), same 25 test positives and same negatives
rng = np.random.default_rng(0); bids = sorted({e['bid'] for e in keep}); by = collections.defaultdict(list)
for i, e in enumerate(keep): by[e['bid']].append(i)
aucs = []
for b in range(40):
    pick = rng.choice(len(bids), len(bids), replace=True); idx = [i for j in pick for i in by[bids[j]]]
    try: m = hg().fit(Xk[idx], yk[idx])
    except Exception: continue
    aucs.append(roc_auc_score(y1, np.concatenate([second_mass(m, C2te), second_mass(m, TE)])))
aucs = np.array(aucs)
out['b1_head_variance'] = dict(n_heads=len(aucs), mean=float(aucs.mean()), sd=float(aucs.std()), min=float(aucs.min()), max=float(aucs.max()), frac_below_0p70=float((aucs < 0.70).mean()))
# (b2) are the test and train positives from the same score distribution under the same head?
def mwu(a, b):
    from itertools import product
    a, b = np.asarray(a), np.asarray(b); u = sum((x > y) + 0.5 * (x == y) for x, y in product(a, b)); n = len(a) * len(b)
    mu, sd = n / 2, np.sqrt(len(a) * len(b) * (len(a) + len(b) + 1) / 12); z = (u - mu) / sd
    from math import erf, sqrt; return float(u / n), float(2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2)))))
p_u, p_p = mwu(pos_te, pos_tr)
out['b2_test_vs_train_positives_same_head'] = dict(prob_test_greater=p_u, p_value_two_sided=p_p, test_median=float(np.median(pos_te)), train_median=float(np.median(pos_tr)),
                                                  test_frac_below_tau90_of_negatives=float(np.mean(pos_te < np.quantile(neg, 0.90))), train_frac_below_tau90=float(np.mean(pos_tr < np.quantile(neg, 0.90))))
# (c) construction features of the 50 positives
def src(e): return e['bid'].split(':')[0]
tab = []
for e, s, sp in [(e, s, 'test') for e, s in zip(C2te, pos_te)] + [(e, s, 'train') for e, s in zip(C2tr, pos_tr)]:
    cfg = {k: v for k, v in e['cfg'].items() if k != 'emb_override'}
    tab.append(dict(split=sp, pair='+'.join(e['meta']['combo']), source=src(e), tenant=e['tenant'], k=e['k'], score=float(s), q_len=len(e['query'].split()), cfg=cfg, n_injected_docs=len(e['injected_docs'])))
out['c_table'] = tab
def kruskal(groups):
    from math import erf, sqrt
    allv = np.concatenate([g for g in groups if len(g)]); ranks = {}; order = np.argsort(allv, kind='mergesort'); r = np.empty(len(allv)); r[order] = np.arange(1, len(allv) + 1)
    for v in np.unique(allv): r[allv == v] = r[allv == v].mean()
    i = 0; H = 0.0
    for g in groups:
        if not len(g): continue
        H += r[i:i + len(g)].sum() ** 2 / len(g); i += len(g)
    N = len(allv); H = 12 / (N * (N + 1)) * H - 3 * (N + 1); k = sum(1 for g in groups if len(g)) - 1
    from scipy.stats import chi2; return float(H), int(k), float(chi2.sf(H, k)) if k > 0 else float('nan')
for feat in ('pair', 'source', 'tenant', 'k'):
    for scope, sel in (('all50', lambda t: True), ('test25', lambda t: t['split'] == 'test')):
        groups = collections.defaultdict(list)
        for t in tab:
            if sel(t): groups[t[feat]].append(t['score'])
        H, k, p = kruskal([np.array(v) for v in groups.values()]); out.setdefault('c_kruskal', {})[f'{feat}|{scope}'] = dict(H=H, df=k, p=p, n_levels=len(groups), level_sizes={a: len(b) for a, b in groups.items()})
low = [t for t in tab if t['split'] == 'test' and t['score'] < float(np.quantile(neg, 0.90))]
out['c_low_scoring_test_positives'] = dict(n=len(low), pairs=collections.Counter(t['pair'] for t in low), sources=collections.Counter(t['source'] for t in low), tenants=collections.Counter(t['tenant'] for t in low),
                                           all_test_sources=collections.Counter(t['source'] for t in tab if t['split'] == 'test'), all_train_sources=collections.Counter(t['source'] for t in tab if t['split'] == 'train'))
# which pair types are low in BOTH splits (a property of the pair) versus only in one split (a property of the episodes)
pp = collections.defaultdict(lambda: {'test': [], 'train': []})
for t in tab: pp[t['pair']][t['split']].append(t['score'])
out['c_pair_by_split'] = {k: dict(n_test=len(v['test']), n_train=len(v['train']), mean_test=(float(np.mean(v['test'])) if v['test'] else None), mean_train=(float(np.mean(v['train'])) if v['train'] else None)) for k, v in sorted(pp.items())}
# within-pair split: for pair types with >=2 episodes in each split, is |mean_test - mean_train| larger than the within-split spread?
# (d) composition test. The C2 generator draws one of 12 fault pairs at random per episode (about 4 per pair type per run), so the pair-type mix of a 25-episode split is random.
from sklearn.metrics import roc_auc_score as _auc
rng2 = np.random.default_rng(1); te_t = [t for t in tab if t['split'] == 'test']; tr_t = [t for t in tab if t['split'] == 'train']
_a = lambda pos: _auc(np.array([1] * len(pos) + [0] * len(neg)), np.concatenate([pos, neg]))
obs = _a(np.array([t['score'] for t in te_t])); bypair = collections.defaultdict(list)
for t in tab: bypair[t['pair']].append(t)
nt = collections.Counter(t['pair'] for t in te_t); fixed = []
for _ in range(4000):
    pos = []
    for pr, ts in bypair.items():
        sc = np.array([t['score'] for t in ts]); pos += list(sc[rng2.permutation(len(sc))[:nt[pr]]])
    fixed.append(_a(np.array(pos)))
fixed = np.array(fixed); pm = {pr: float(np.mean([t['score'] for t in ts])) for pr, ts in bypair.items()}
cm = np.array([np.mean(np.array([pm[t['pair']] for t in tab])[rng2.permutation(50)[:25]]) for _ in range(4000)]); comp_te = float(np.mean([pm[t['pair']] for t in te_t]))
p_fixed = float((fixed <= obs).mean())
out['d_composition'] = dict(observed_test_auroc=float(obs), within_pair_permutation_mean=float(fixed.mean()), within_pair_permutation_sd=float(fixed.std()), p_draw_le_observed=p_fixed,
    p_after_choosing_worst_of_7_runs=float(1 - (1 - p_fixed) ** 7), composition_only_mean_test=comp_te, composition_only_mean_train=float(np.mean([pm[t['pair']] for t in tr_t])),
    observed_mean_test=float(np.mean([t['score'] for t in te_t])), observed_mean_train=float(np.mean([t['score'] for t in tr_t])),
    random_split_composition_mean=float(cm.mean()), random_split_composition_sd=float(cm.std()), test_composition_percentile=float(100 * (cm <= comp_te).mean()),
    masked_pair_types_mean_score_below_0p05=sorted(pr for pr, v in pm.items() if v < 0.05), pair_mean_scores={pr: round(v, 3) for pr, v in sorted(pm.items())})
json.dump(out, open(outp, 'w'), indent=1, default=lambda o: dict(o) if isinstance(o, collections.Counter) else str(o))
print(json.dumps({k: v for k, v in out.items() if k not in ('c_table', 'c_pair_by_split')}, indent=1, default=lambda o: dict(o) if isinstance(o, collections.Counter) else str(o))[:5500])
