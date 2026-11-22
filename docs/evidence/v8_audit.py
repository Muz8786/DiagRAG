"""v8 data-hygiene audit (docs/evidence/v8_protocol.md section 4 and amendment E1). DESCRIPTIVE: nothing here changes a verdict.
Checks A1 split leakage, A2 exact duplicates, A3 label-permutation control, A4 single-feature leakage scan, A5 bootstrap re-fit stability (E1), A6 query-text-only baseline.
Re-fits the multi-class attributor from the shipped episodes.jsonl exactly as docs/evidence/diagnosis_confusion.py does (same settings, same calibration split).
usage: python docs/evidence/v8_audit.py <judged_folder> <out.json>   (use scikit-learn 1.6.1, the version recorded in the v6 run)"""
import glob, hashlib, json, os, sys, time
import numpy as np
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

folder, outp = sys.argv[1], sys.argv[2]
rows = [json.loads(l) for l in open(os.path.join(folder, 'episodes.jsonl'), encoding='utf-8')]
prot = json.load(open(glob.glob(os.path.join(folder, '*PROTOCOL.json'))[0])); seed = int(prot['cfg']['SEED']); CAL_FRAC = prot['cfg'].get('CAL_FRAC', 0.5)
FE = sorted(rows[0]['feats']); mat = lambda es: np.array([[e['feats'][k] for k in FE] for e in es], dtype=np.float32)
sing = [e for e in rows if e['fault'] != 'C2']; TR = [e for e in sing if e['split'] == 'train']; TE = [e for e in sing if e['split'] == 'test']
CALB = {e['bid'] for e in TR if e['fault'] == 'NONE' and int(hashlib.md5(('cal|' + e['bid']).encode()).hexdigest()[:8], 16) / 2**32 < CAL_FRAC}
TRA = [e for e in TR if not (e['fault'] == 'NONE' and e['bid'] in CALB)]
hgb = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=seed)


def auroc(y, s):
    """Rank-based AUROC with ties averaged (Mann-Whitney)."""
    y = np.asarray(y, int); s = np.asarray(s, float); pos = y == 1
    if pos.sum() == 0 or (~pos).sum() == 0: return float('nan')
    order = np.argsort(s, kind='mergesort'); ss = s[order]; ranks = np.empty(len(s)); i = 0
    while i < len(ss):
        j = i
        while j + 1 < len(ss) and ss[j + 1] == ss[i]: j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1; i = j + 1
    return float((ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum()))


def fit_eval(tr, te, cols=None, shuffle_seed=None, boot_seed=None):
    Xtr = mat(tr); Xte = mat(te); ytr = np.array([e['fault'] for e in tr])
    if cols is not None: Xtr, Xte = Xtr[:, cols], Xte[:, cols]
    if boot_seed is not None:
        r = np.random.default_rng(boot_seed); i = r.integers(0, len(ytr), len(ytr)); Xtr, ytr = Xtr[i], ytr[i]
    if shuffle_seed is not None: ytr = np.random.default_rng(shuffle_seed).permutation(ytr)
    m = hgb().fit(Xtr, ytr); cls = list(m.classes_); P = m.predict_proba(Xte); pred = np.array([cls[i] for i in P.argmax(1)])
    yt = np.array([e['fault'] for e in te]); fm = yt != 'NONE'
    score = 1.0 - P[:, cls.index('NONE')] if 'NONE' in cls else P.max(1)
    return dict(auroc=auroc(fm.astype(int), score), exact_faulted=float((pred[fm] == yt[fm]).mean()), pred=pred, score=score)


t0 = time.time(); res = dict(folder=folder, sklearn=sklearn.__version__, seed=seed, n_train_fit=len(TRA), n_test=len(TE), n_test_faulted=int(sum(e['fault'] != 'NONE' for e in TE)),
                             n_test_clean=int(sum(e['fault'] == 'NONE' for e in TE)), n_features=len(FE))
base = fit_eval(TRA, TE); res['reference'] = dict(auroc_fault_vs_clean=base['auroc'], exact_fault_accuracy_on_faulted=base['exact_faulted'])
print('reference', res['reference'], f'{time.time() - t0:.0f}s', flush=True)
yte = np.array([e['fault'] for e in TE]); fm = yte != 'NONE'

# ---- A1 split leakage
norm = lambda q: ' '.join(q.strip().lower().split())
tr_q = {norm(e['query']) for e in TR}; tr_b = {e['bid'] for e in TR}
ov = [i for i, e in enumerate(TE) if norm(e['query']) in tr_q]
keep = np.array([i not in set(ov) for i in range(len(TE))])
res['A1_split_leakage'] = dict(bid_overlap_train_test=len({e['bid'] for e in TE} & tr_b), query_string_overlap_test_episodes=len(ov),
                               overlap_by_fault=dict(sorted({f: int(sum(1 for i in ov if TE[i]['fault'] == f)) for f in {TE[i]['fault'] for i in ov}}.items())),
                               exact_faulted_all=base['exact_faulted'],
                               exact_faulted_without_overlap=float((base['pred'][fm & keep] == yte[fm & keep]).mean()),
                               auroc_without_overlap=auroc(fm[keep].astype(int), base['score'][keep]), n_removed=len(ov))
res['A1_split_leakage']['drop_points'] = 100 * (res['A1_split_leakage']['exact_faulted_all'] - res['A1_split_leakage']['exact_faulted_without_overlap'])
res['A1_split_leakage']['flag_leak_effect_over_0.5pt'] = bool(abs(res['A1_split_leakage']['drop_points']) > 0.5)
print('A1', res['A1_split_leakage'], flush=True)

# ---- A2 exact duplicates
h = lambda e: hashlib.md5(np.array([e['feats'][k] for k in FE], dtype=np.float32).tobytes()).hexdigest()
trh = {h(e) for e in TR}; dup_te = sum(1 for e in TE if h(e) in trh)
qf_tr = {(norm(e['query']), e['fault']) for e in TR}; qf_dup = sum(1 for e in TE if (norm(e['query']), e['fault']) in qf_tr)
res['A2_duplicates'] = dict(test_episodes_with_identical_feature_vector_in_train=int(dup_te), test_episodes_with_identical_query_and_fault_in_train=int(qf_dup),
                            note='identical feature vectors can be legitimate for clean queries that return the same documents; reported, not removed')
print('A2', res['A2_duplicates'], flush=True)

# ---- A3 label permutation control
perm = [fit_eval(TRA, TE, shuffle_seed=s)['auroc'] for s in range(20)]
res['A3_label_permutation'] = dict(n=20, auroc_mean=float(np.mean(perm)), auroc_min=float(np.min(perm)), auroc_max=float(np.max(perm)), band=[0.45, 0.55],
                                   pass_in_band=bool(0.45 <= np.min(perm) and np.max(perm) <= 0.55))
print('A3', res['A3_label_permutation'], f'{time.time() - t0:.0f}s', flush=True)

# ---- A4 single-feature leakage scan
Xte = mat(TE); sf = {k: auroc(fm.astype(int), Xte[:, j]) for j, k in enumerate(FE)}
sf_dir = {k: max(v, 1 - v) if v == v else float('nan') for k, v in sf.items()}   # direction-free
top = sorted(sf_dir.items(), key=lambda kv: -(kv[1] if kv[1] == kv[1] else 0))[:10]; flagged = [k for k, v in sf_dir.items() if v == v and v >= 0.99]
a4 = dict(top10_single_feature_auroc=[dict(feature=k, auroc_direction_free=v) for k, v in top], flagged_ge_0_99=flagged)
if flagged:
    cols = [j for j, k in enumerate(FE) if k not in flagged]; r = fit_eval(TRA, TE, cols=cols)
    a4['refit_without_flagged'] = dict(auroc=r['auroc'], exact_faulted=r['exact_faulted'], delta_auroc=r['auroc'] - base['auroc'], delta_exact_points=100 * (r['exact_faulted'] - base['exact_faulted']))
res['A4_single_feature_scan'] = a4; print('A4', json.dumps(a4)[:600], flush=True)

# ---- A5 bootstrap re-fit stability (amendment E1)
bs = [fit_eval(TRA, TE, boot_seed=s) for s in range(20)]
res['A5_bootstrap_stability'] = dict(n=20, auroc=dict(mean=float(np.mean([b['auroc'] for b in bs])), min=float(np.min([b['auroc'] for b in bs])), max=float(np.max([b['auroc'] for b in bs]))),
                                     exact_faulted=dict(mean=float(np.mean([b['exact_faulted'] for b in bs])), min=float(np.min([b['exact_faulted'] for b in bs])), max=float(np.max([b['exact_faulted'] for b in bs]))))
print('A5', res['A5_bootstrap_stability'], f'{time.time() - t0:.0f}s', flush=True)

# ---- A6 query-text-only supervised baseline (same train split, same held-out episodes, same classes)
vec = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), min_df=2, sublinear_tf=True); Xq = vec.fit_transform([e['query'] for e in TRA]); ytr = np.array([e['fault'] for e in TRA])
lr = LogisticRegression(max_iter=300, C=3.0, class_weight='balanced').fit(Xq, ytr); cls = list(lr.classes_); P = lr.predict_proba(vec.transform([e['query'] for e in TE]))
pred = np.array([cls[i] for i in P.argmax(1)]); sc = 1.0 - P[:, cls.index('NONE')]
grp = lambda f: f[0]; by_group = {}
for g in ('Q', 'K', 'R'):
    m_ = np.array([f.startswith(g) for f in yte]); by_group[g] = dict(n=int(m_.sum()), query_text_only_exact=float((pred[m_] == yte[m_]).mean()), telemetry_exact=float((base['pred'][m_] == yte[m_]).mean()))
res['A6_query_text_only'] = dict(auroc_fault_vs_clean=auroc(fm.astype(int), sc), exact_fault_accuracy_on_faulted=float((pred[fm] == yte[fm]).mean()),
                                 telemetry_auroc=base['auroc'], telemetry_exact=base['exact_faulted'], by_group=by_group,
                                 note='query text only; top-5 document text is not stored in episodes.jsonl, so a document-text baseline needs a re-run and is not part of v8')
print('A6', json.dumps(res['A6_query_text_only'])[:700], flush=True)
res['runtime_s'] = round(time.time() - t0); json.dump(res, open(outp, 'w'), indent=1); print('wrote', outp)
