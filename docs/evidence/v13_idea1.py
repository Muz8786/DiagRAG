"""v13 Idea 1 (docs/evidence/v13_idea1_protocol.md): invariant-based component isolation vs the leave-one-fault-out attributor.
usage: python docs/evidence/v13_idea1.py <judged_folder> <eval_split: train|test> <out.json> [--composed <v7 folder>]     (scikit-learn 1.6.1)
eval_split=train is the DEVELOPMENT run (v8 only); eval_split=test is the held-out run, run once."""
import collections, glob, hashlib, json, os, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier

INV = {'QUERY': [('q_oov', '+'), ('q_oov_long', '+'), ('q_correctable', '+'), ('q_segmentable', '+'), ('q_prefix', '+'), ('q_filler', '+'), ('q_conj', '+'), ('q_code_oov', '+'), ('q_synlow', '+')],
       'ENCODER': [('q_probe_cos', '-'), ('d_null10', '+')], 'ANN': [('ann_probe', '-')],
       'VECTORS': [('align_probe', '-'), ('stale_sparse20', '+'), ('stale_min', '-'), ('nonfinite', '+'), ('cov', '-'), ('sparse_absent_dense', '+')],
       'BM25': [('s_lex5', '-')], 'RERANK': [('ce_rrf_rho', '-'), ('ce_dense_rho', '-'), ('n_depth', '-')], 'FUSION': [('dep_dense', '-')],
       'SERVING': [('n_final', '-'), ('deleted5', '+')], 'FILTERS': [('tenant_mis5', '+'), ('expired5', '+'), ('filter_survival', '-'), ('part_top', '2')],
       'CONTENT': [('dup5', '+'), ('red_cos5', '+'), ('thin5', '+'), ('unver5', '+'), ('ident5', '+'), ('chunk_crowd5', '+')]}
COMP = {**{f: 'QUERY' for f in 'Q01 Q02 Q03 Q04 Q05 Q07 Q09'.split()}, **{f: 'CONTENT' for f in 'K03 K05 K06 K08 K12'.split()}, **{f: 'VECTORS' for f in 'K04 R01 R07 R25'.split()},
        **{f: 'FILTERS' for f in 'K07 K09 R06 R26'.split()}, **{f: 'SERVING' for f in 'K11 R23'.split()}, **{f: 'ENCODER' for f in 'R03 R10 R11'.split()},
        **{f: 'RERANK' for f in 'R05 R19 R24'.split()}, 'R13': 'BM25', 'R15': 'ANN', 'R22': 'FUSION'}
LIST = [(c, f, d) for c, v in INV.items() for f, d in v]; J = len(LIST); ALPHA = 0.05; THR = ALPHA / J
folder, split, outp = sys.argv[1], sys.argv[2], sys.argv[3]; comp_dir = sys.argv[sys.argv.index('--composed') + 1] if '--composed' in sys.argv else None
rows = [json.loads(l) for l in open(os.path.join(folder, 'episodes.jsonl'), encoding='utf-8')]
prot = json.load(open(glob.glob(os.path.join(folder, '*PROTOCOL.json'))[0])); seed = int(prot['cfg']['SEED']); CF = prot['cfg'].get('CAL_FRAC', 0.5)
FE = sorted(rows[0]['feats']); assert all(f in FE for _, f, _ in LIST), [f for _, f, _ in LIST if f not in FE]
sing = [e for e in rows if e['fault'] != 'C2']; TR = [e for e in sing if e['split'] == 'train']
CALB = {e['bid'] for e in TR if e['fault'] == 'NONE' and int(hashlib.md5(('cal|' + e['bid']).encode()).hexdigest()[:8], 16) / 2**32 < CF}
TRA = [e for e in TR if not (e['fault'] == 'NONE' and e['bid'] in CALB)]
CAL = [e for e in TR if e['fault'] == 'NONE']   # every clean training episode: invariants use no fault label
EV = [e for e in sing if e['split'] == split and e['fault'] in COMP or (e['split'] == split and e['fault'] == 'NONE')]
if split == 'train': EV = [e for e in EV if e['fault'] != 'NONE' or e['bid'] in CALB]   # development: clean evaluation rows = the calibration-held part is not used for p-values below
cal_vals = {f: np.array([e['feats'][f] for e in CAL], float) for _, f, _ in LIST}


def pvals(feats, cal=cal_vals):
    out = []
    for c, f, d in LIST:
        x = float(feats[f]); v = cal[f]; n = len(v)
        if d == '+': p = (1 + (v >= x).sum()) / (n + 1)
        elif d == '-': p = (1 + (v <= x).sum()) / (n + 1)
        else: p = min(1.0, 2 * min((1 + (v >= x).sum()) / (n + 1), (1 + (v <= x).sum()) / (n + 1)))
        out.append((c, f, p))
    return out


def isolate(feats, cal=cal_vals):
    pv = pvals(feats, cal); viol = [(c, f, p) for c, f, p in pv if p <= THR]
    if not viol: return None, set()
    best = min(viol, key=lambda t: t[2]); return best[0], {c for c, _, _ in viol}


if split == 'train':   # development only: p-values for training episodes must not use the same clean rows, so calibrate on the non-held clean training rows
    cal_dev = {f: np.array([e['feats'][f] for e in TR if e['fault'] == 'NONE' and e['bid'] not in CALB], float) for _, f, _ in LIST}
else: cal_dev = cal_vals
mat = lambda es: np.array([[e['feats'][k] for k in FE] for e in es], np.float32)
hgb = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=seed)
faults = sorted({e['fault'] for e in EV} - {'NONE'}); res = dict(folder=folder, split=split, seed=seed, J=J, alpha=ALPHA, n_cal=len(CAL), per_fault={})
Xtr = mat(TRA); ytr = np.array([e['fault'] for e in TRA]); full = hgb().fit(Xtr, ytr); fcls = list(full.classes_)
for f in faults:
    es = [e for e in EV if e['fault'] == f]; truth = COMP[f]; Xe = mat(es)
    inv = [isolate(e['feats'], cal_dev)[0] for e in es]
    keep = ytr != f; m = hgb().fit(Xtr[keep], ytr[keep]); cl = list(m.classes_); pr = [cl[i] for i in m.predict_proba(Xe).argmax(1)]
    lofo = [COMP.get(p) for p in pr]; seen = [COMP.get(fcls[i]) for i in full.predict_proba(Xe).argmax(1)]
    res['per_fault'][f] = dict(n=len(es), true=truth, inv_correct=float(np.mean([x == truth for x in inv])), lofo_correct=float(np.mean([x == truth for x in lofo])),
                               seen_correct=float(np.mean([x == truth for x in seen])), inv_flagged=float(np.mean([x is not None for x in inv])),
                               inv_top=collections.Counter(str(x) for x in inv).most_common(3), lofo_top=collections.Counter(str(x) for x in lofo).most_common(3))
    print(f"{f} {truth:8s} n={len(es):3d} inv {res['per_fault'][f]['inv_correct']:.2f} lofo {res['per_fault'][f]['lofo_correct']:.2f} seen {res['per_fault'][f]['seen_correct']:.2f}  inv picks {res['per_fault'][f]['inv_top']}", flush=True)
PF = res['per_fault']; a = np.array([PF[f]['inv_correct'] for f in faults]); b = np.array([PF[f]['lofo_correct'] for f in faults])
rng = np.random.default_rng(7); bs = [float((a[i] - b[i]).mean()) for i in (rng.integers(0, len(a), len(a)) for _ in range(2000))]
clean = [e for e in sing if e['split'] == split and e['fault'] == 'NONE' and (split == 'test' or e['bid'] in CALB)]
res['M1'] = dict(n_faults=len(faults), inv_macro=float(a.mean()), lofo_macro=float(b.mean()), seen_macro=float(np.mean([PF[f]['seen_correct'] for f in faults])),
                 diff=float((a - b).mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])
res['M2'] = dict(n_clean=len(clean), false_alarm=float(np.mean([isolate(e['feats'], cal_dev)[0] is not None for e in clean])))
res['by_group'] = {g: dict(inv=float(np.mean([PF[f]['inv_correct'] for f in faults if f[0] == g])), lofo=float(np.mean([PF[f]['lofo_correct'] for f in faults if f[0] == g]))) for g in 'QKR'}
if comp_dir and split == 'test':
    CE = [json.loads(l) for l in open(os.path.join(comp_dir, 'composed_episodes.jsonl'))]; CFt = [json.loads(l) for l in open(os.path.join(comp_dir, 'composed_features.jsonl'))]
    assert all((x['split'], x['stratum']) == (y['split'], y['stratum']) for x, y in zip(CE, CFt))
    vr = [json.loads(l) for l in open(os.path.join(comp_dir, 'episodes.jsonl'))]; vcal = {f: np.array([e['feats'][f] for e in vr if e['split'] == 'train' and e['fault'] == 'NONE'], float) for _, f, _ in LIST}
    by = collections.defaultdict(lambda: [0, 0])
    for x, y in zip(CE, CFt):
        if x['split'] != 'test': continue
        _, S = isolate(y['feats'], vcal); need = {COMP[c] for c in x['comps']}; by[x['stratum']][1] += 1; by[x['stratum']][0] += int(need <= S)
    res['M3'] = dict(by_stratum={k: dict(all_components_flagged=v[0], n=v[1]) for k, v in sorted(by.items())}, total=dict(k=sum(v[0] for v in by.values()), n=sum(v[1] for v in by.values())))
json.dump(res, open(outp, 'w'), indent=1); print('M1', res['M1']); print('M2', res['M2']); print('by group', res['by_group']); print('M3', res.get('M3'))
