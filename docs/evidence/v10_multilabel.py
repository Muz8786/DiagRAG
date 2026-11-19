"""Multi-label dispatcher study (docs/evidence/v10_multilabel_protocol.md). Order is fixed: (1) re-derive the stored v7 naming figures to validate the metric code, (2) choose tau by grouped 5-fold CV on
composed TRAIN episodes only, (3) score the 155 held-out composed episodes ONCE with that tau. Run: python docs/evidence/v10_multilabel.py <out.json>   (scikit-learn 1.6.1)"""
import collections, glob, hashlib, json, math, os, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GroupKFold

D = 'kaggle/judged_cpu_run_v7_seed50'; SEED = 50; TAUS = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40]; CAP = 3
FAMILY = dict(Q01='QLEX', Q03='QLEX', Q04='QLEX', Q05='QLEX', K04='STALE', R07='STALE', R03='ENC', R10='ENC', R11='ENC'); fam = lambda f: FAMILY.get(f, f)
wilson = lambda k, n, z=1.96: [float('nan')] * 2 if n == 0 else [((k / n + z * z / (2 * n)) - z * math.sqrt(k / n * (1 - k / n) / n + z * z / (4 * n * n))) / (1 + z * z / n),
                                                                  ((k / n + z * z / (2 * n)) + z * math.sqrt(k / n * (1 - k / n) / n + z * z / (4 * n * n))) / (1 + z * z / n)]
rows = [json.loads(l) for l in open(os.path.join(D, 'episodes.jsonl'), encoding='utf-8')]
prot = json.load(open(os.path.join(D, 'JUDGED_PROTOCOL.json'))); CF = prot['cfg'].get('CAL_FRAC', 0.5)
FE = sorted(rows[0]['feats']); vec = lambda f: [f[k] for k in FE]
sing = [e for e in rows if e['fault'] != 'C2']; TR = [e for e in sing if e['split'] == 'train']; TE = [e for e in sing if e['split'] == 'test']
CALB = {e['bid'] for e in TR if e['fault'] == 'NONE' and int(hashlib.md5(('cal|' + e['bid']).encode()).hexdigest()[:8], 16) / 2**32 < CF}
TRA = [e for e in TR if not (e['fault'] == 'NONE' and e['bid'] in CALB)]
CE = [json.loads(l) for l in open(os.path.join(D, 'composed_episodes.jsonl'), encoding='utf-8')]; CFt = [json.loads(l) for l in open(os.path.join(D, 'composed_features.jsonl'), encoding='utf-8')]
assert len(CE) == len(CFt) == 310 and all((a['split'], a['stratum']) == (b['split'], b['stratum']) for a, b in zip(CE, CFt)), 'composed files are not aligned'
for a, b in zip(CE, CFt): a['feats'] = b['feats']
CTR = [e for e in CE if e['split'] == 'train']; CTE = [e for e in CE if e['split'] == 'test']; assert len(CTR) == len(CTE) == 155
Xs = np.array([vec(e['feats']) for e in TRA], np.float32); ys = np.array([e['fault'] for e in TRA])
hgb = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=SEED)


def fit(comp_eps):
    X = [Xs]; y = [ys]
    if comp_eps: X.append(np.array([vec(e['feats']) for e in comp_eps for _ in e['comps']], np.float32)); y.append(np.array([c for e in comp_eps for c in e['comps']]))
    return hgb().fit(np.vstack(X), np.concatenate(y))


def rule(p, cls, tau, ni):   # multi-label set (protocol section 2)
    order = [i for i in np.argsort(-p) if i != ni]; S = [i for i in order if p[i] >= tau][:CAP]
    if not S and p[ni] < 0.5 and order: S = [order[0]]
    return [cls[i] for i in S]


def top2(p, cls, ni): return [cls[i] for i in [j for j in np.argsort(-p) if j != ni][:2]]


def single(p, cls, ni):
    i = int(np.argmax(p)); return [] if i == ni else [cls[i]]


def metrics(labels, comps):   # family level; precision = share of emitted labels whose family is a true cause's; recall = share of true causes whose family is emitted
    L = [l for l in labels if not l.startswith('G')]; tf = {fam(c) for c in comps}; fl = {fam(l) for l in L}
    rec = sum(fam(c) in fl for c in comps) / len(comps); prec = (sum(fam(l) in tf for l in L) / len(L)) if L else 0.0
    f1 = 0.0 if (prec + rec) == 0 else 2 * prec * rec / (prec + rec)
    return dict(both=all(fam(c) in fl for c in comps), any=any(fam(c) in fl for c in comps), prec=prec, rec=rec, f1=f1, size=len(L))


# ---- (1) validate the metric code against the stored v7 numbers (stored labels; no re-fit)
st = [e['eval'] for e in CTE]; m_old = [metrics(e['lab_new'], e['comps']) for e in st]
chk = dict(both=sum(m['both'] for m in m_old), f1=float(np.mean([m['f1'] for m in m_old])), rec=float(np.mean([m['rec'] for m in m_old])), prec=float(np.mean([m['prec'] for m in m_old])))
print('stored v7 reproduced:', chk, flush=True)
assert chk['both'] == 62, 'metric code does not reproduce the stored 62/155'
V7_F1, V7_REC, V7_PREC = 0.770, 0.697, 0.923
drift = {k: abs(chk[k] - v) for k, v in (('f1', V7_F1), ('rec', V7_REC), ('prec', V7_PREC))}
print('abs difference from the stored v7 F1/recall/precision (3 d.p.):', drift, flush=True)

# ---- (2) choose tau on composed TRAIN only (grouped 5-fold CV by base query)
grp = [e['bid'] for e in CTR]; cv = {t: [] for t in TAUS}
for k, (a, b) in enumerate(GroupKFold(n_splits=5).split(CTR, groups=grp)):
    m = fit([CTR[i] for i in a]); cls = list(m.classes_); ni = cls.index('NONE'); P = m.predict_proba(np.array([vec(CTR[i]['feats']) for i in b], np.float32))
    for t in TAUS:
        for p, i in zip(P, b): cv[t].append(metrics(rule(p, cls, t, ni), CTR[i]['comps'])['f1'])
    print('cv fold', k, flush=True)
cvm = {t: float(np.mean(v)) for t, v in cv.items()}; best = max(cvm.values()); TAU = max(t for t, v in cvm.items() if abs(v - best) < 1e-12)
print('cv mean set-F1 by tau', cvm, '-> tau', TAU, flush=True)

# ---- (3) score held-out ONCE
m = fit(CTR); cls = list(m.classes_); ni = cls.index('NONE'); P = m.predict_proba(np.array([vec(e['feats']) for e in CTE], np.float32))
res = {}
for name, fn in (('multilabel', lambda p: rule(p, cls, TAU, ni)), ('top2_always', lambda p: top2(p, cls, ni)), ('single_label_argmax', lambda p: single(p, cls, ni))):
    ms = [metrics(fn(p), e['comps']) for p, e in zip(P, CTE)]; n = len(ms); k = sum(x['both'] for x in ms)
    by = {s: dict(n=sum(1 for e in CTE if e['stratum'] == s), both=sum(x['both'] for x, e in zip(ms, CTE) if e['stratum'] == s)) for s in sorted({e['stratum'] for e in CTE})}
    res[name] = dict(both_named=dict(k=k, n=n, rate=k / n, wilson95=wilson(k, n)), at_least_one=float(np.mean([x['any'] for x in ms])), set_f1=float(np.mean([x['f1'] for x in ms])), precision=float(np.mean([x['prec'] for x in ms])),
                     recall=float(np.mean([x['rec'] for x in ms])), mean_labels_per_episode=float(np.mean([x['size'] for x in ms])), by_stratum=by)
Pc = m.predict_proba(np.array([vec(e['feats']) for e in TE if e['fault'] == 'NONE'], np.float32)); nc = len(Pc)
clean = dict(n_clean_test=nc, multilabel_nonempty=float(np.mean([len(rule(p, cls, TAU, ni)) > 0 for p in Pc])), single_label_argmax_not_none=float(np.mean([len(single(p, cls, ni)) > 0 for p in Pc])),
             top2_always_nonempty=1.0)
# ---- POST-HOC block (added after the first run; NOT in the pre-registration): what the same rule does to SINGLE-fault held-out episodes, and the stored v7 labels re-scored with THIS metric (like for like)
sf = [e for e in TE if e['fault'] != 'NONE']; Psf = m.predict_proba(np.array([vec(e['feats']) for e in sf], np.float32))
def agg(fn):
    ms = [metrics(fn(p), [e['fault']]) for p, e in zip(Psf, sf)]
    return dict(n=len(ms), cause_family_named=float(np.mean([x['both'] for x in ms])), mean_labels_per_episode=float(np.mean([x['size'] for x in ms])), precision=float(np.mean([x['prec'] for x in ms])), share_with_a_wrong_label=float(np.mean([x['size'] > 0 and x['prec'] < 1.0 for x in ms])))
posthoc = dict(note='post-hoc, not pre-registered; single-fault held-out episodes (C2 excluded)', multilabel=agg(lambda p: rule(p, cls, TAU, ni)), single_label_argmax=agg(lambda p: single(p, cls, ni)),
               v7_stored_labels_rescored_with_this_metric=dict(both=sum(x['both'] for x in m_old), f1=float(np.mean([x['f1'] for x in m_old])), precision=float(np.mean([x['prec'] for x in m_old])), recall=float(np.mean([x['rec'] for x in m_old])),
                                                               mean_labels=float(np.mean([x['size'] for x in m_old]))))
print('POST-HOC', json.dumps(posthoc)[:1400], flush=True)
out = dict(protocol='docs/evidence/v10_multilabel_protocol.md', tau_grid=TAUS, cv_mean_set_f1=cvm, tau=TAU, metric_validation=dict(reproduced=chk, stored=dict(both=62, f1=V7_F1, rec=V7_REC, prec=V7_PREC), abs_diff=drift),
           stored_v7_dispatcher=dict(both_named=62, n=155, rate=62 / 155), heldout=res, heldout_clean_false_labels=clean, posthoc=posthoc, n_train_composed=len(CTR), n_test_composed=len(CTE), sklearn_note='1.6.1 expected')
json.dump(out, open(sys.argv[1], 'w'), indent=1)
for k, v in res.items(): print(f"{k:22s} both {v['both_named']['k']:3d}/155 ({100 * v['both_named']['rate']:.1f}%, CI {100 * v['both_named']['wilson95'][0]:.0f}-{100 * v['both_named']['wilson95'][1]:.0f})  F1 {v['set_f1']:.3f}  prec {v['precision']:.3f}  rec {v['recall']:.3f}  labels {v['mean_labels_per_episode']:.2f}  by stratum {v['by_stratum']}")
print('clean false-label check:', clean)
