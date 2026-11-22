"""v20 (docs/evidence/v20_protocol.md): feature-family ablations (A), same-supervision and same-information baselines (B1, B2) and
leave-one-mechanism-out detection and coarse localization (C2), from a judged run's saved episodes. No retrieval is run.
usage: python v20_ablation.py <run_dir> <out_dir> <manifest.json> [--lomo] [--trial]
<run_dir> holds episodes.jsonl, *PROTOCOL.json and (optionally) detection_baselines.csv of one judged run."""
import argparse, collections, csv, glob, hashlib, json, os, time
import numpy as np
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score

ap = argparse.ArgumentParser(); ap.add_argument('run'); ap.add_argument('out'); ap.add_argument('manifest'); ap.add_argument('--lomo', action='store_true'); ap.add_argument('--trial', action='store_true')
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); t0 = time.time(); log = lambda *x: print(f'[{time.time() - t0:6.0f}s]', *x, flush=True)
MAN = json.load(open(a.manifest)); FAM = MAN['families']
rows = [json.loads(l) for l in open(os.path.join(a.run, 'episodes.jsonl'), encoding='utf-8')]
prot = json.load(open(glob.glob(os.path.join(a.run, '*PROTOCOL.json'))[0])); seed = int(prot['cfg']['SEED']); CAL_FRAC = prot['cfg'].get('CAL_FRAC', 0.5)
FE = sorted(rows[0]['feats']); assert sorted(sum(FAM.values(), [])) == FE, 'manifest does not cover the 63 columns'
col = {k: i for i, k in enumerate(FE)}
X_of = lambda es: np.array([[e['feats'][k] for k in FE] for e in es], dtype=np.float64)
sing = [e for e in rows if e['fault'] != 'C2']; TR = [e for e in sing if e['split'] == 'train']; TE = [e for e in sing if e['split'] == 'test']
C2te = [e for e in rows if e['fault'] == 'C2' and e['split'] == 'test']
CALB = {e['bid'] for e in TR if e['fault'] == 'NONE' and int(hashlib.md5(('cal|' + e['bid']).encode()).hexdigest()[:8], 16) / 2**32 < CAL_FRAC}
TRA = [e for e in TR if not (e['fault'] == 'NONE' and e['bid'] in CALB)]
if a.trial: TRA = TRA[::4]; TE = TE[::4]
Xtr, Xte, Xc2 = X_of(TRA), X_of(TE), X_of(C2te); ytr = np.array([e['fault'] for e in TRA]); yte = np.array([e['fault'] for e in TE])
nan_tr, nan_te = int(np.isnan(Xtr).sum()), int(np.isnan(Xte).sum())
med = np.nanmedian(Xtr, axis=0); fill = lambda X: np.where(np.isnan(X), med, X)
FAMILY = {c: c for c in set(ytr)}; FAMILY.update(Q01='QLEX', Q03='QLEX', Q04='QLEX', Q05='QLEX', K04='STALE', R07='STALE', R03='ENC', R10='ENC', R11='ENC')
GROUP = lambda c: 'NONE' if c == 'NONE' else c[0]
hgb = lambda: HistGradientBoostingClassifier(max_iter=int(os.environ.get("V20_ITERS", 250)), learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=seed)
R = dict(run=os.path.basename(a.run.rstrip('/')), seed=seed, code_sha256=prot.get('code_sha256'), sklearn=sklearn.__version__, n_train=len(TRA), n_test=len(TE),
         n_test_faulted=int((yte != 'NONE').sum()), n_test_clean=int((yte == 'NONE').sum()), nan_cells=dict(train=nan_tr, test=nan_te), trial=a.trial)
log('run', R)

def prf_macro(y, pred, classes):
    f1s = []
    for c in classes:
        tp = int(((y == c) & (pred == c)).sum()); fp = int(((y != c) & (pred == c)).sum()); fn = int(((y == c) & (pred != c)).sum())
        if tp + fn == 0: continue
        p = tp / (tp + fp) if tp + fp else 0.0; r = tp / (tp + fn); f1s.append(0.0 if tp == 0 else 2 * p * r / (p + r))
    return float(np.mean(f1s)) if f1s else float('nan')
CLASSES = sorted(set(ytr))
def metrics(y, pc, pred, idx=None):
    if idx is not None: y, pc, pred = y[idx], pc[idx], pred[idx]
    yb = (y != 'NONE').astype(int); fm = y != 'NONE'; cm = ~fm
    out = dict(auroc=float(roc_auc_score(yb, 1 - pc)) if 0 < yb.sum() < len(yb) else float('nan'),
               auprc=float(average_precision_score(yb, 1 - pc)) if 0 < yb.sum() < len(yb) else float('nan'),
               exact_top1_faulted=float((pred[fm] == y[fm]).mean()) if fm.any() else float('nan'),
               family_acc_faulted=float(np.mean([FAMILY.get(p, p) == FAMILY.get(t, t) for p, t in zip(pred[fm], y[fm])])) if fm.any() else float('nan'),
               macro_f1=prf_macro(y, pred, CLASSES), clean_fpr=float((pred[cm] != 'NONE').mean()) if cm.any() else float('nan'))
    for f in ('Q03', 'K04', 'R24'):
        m_ = y == f; out[f'recall_{f}'] = float((pred[m_] == f).mean()) if m_.any() else float('nan')
    return out
bids = np.array([e['bid'] for e in TE]); ub = np.unique(bids); bidx = {b: np.where(bids == b)[0] for b in ub}
rng = np.random.default_rng(7); NB = 100 if a.trial else 500
BOOT = [np.concatenate([bidx[b] for b in rng.choice(ub, len(ub), replace=True)]) for _ in range(NB)]
def boot_diff(ref, cur, keys=('auroc', 'exact_top1_faulted', 'macro_f1', 'clean_fpr')):
    out = {k: [] for k in keys}
    for idx in BOOT:
        m0, m1 = metrics(yte, ref[0], ref[1], idx), metrics(yte, cur[0], cur[1], idx)
        for k in keys: out[k].append(m1[k] - m0[k])
    return {k: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))] for k, v in out.items()}
def fit_predict(model, cols, X_tr=None, X_te=None, impute=False):
    X1 = (Xtr if X_tr is None else X_tr)[:, cols]; X2 = (Xte if X_te is None else X_te)[:, cols]
    if impute: X1, X2 = np.where(np.isnan(X1), med[cols], X1), np.where(np.isnan(X2), med[cols], X2)
    lab = np.unique(ytr); yint = np.searchsorted(lab, ytr)   # integer labels for every estimator (sklearn MLP early stopping fails on strings)
    a_ = time.time(); model.fit(X1, yint); ft = time.time() - a_
    P = model.predict_proba(X2); cls = [str(lab[i]) for i in model.classes_]; pc = P[:, cls.index('NONE')]; pred = np.array([cls[i] for i in P.argmax(1)])
    return model, pc, pred, ft, cls
fams = ['QUERY', 'SCORE', 'AGREEMENT', 'INTEGRITY', 'PROBE']; ALL = list(range(len(FE))); idx_of = lambda names: sorted(col[k] for k in names)
ARMS = {'F0_all': ALL}
for i, f in enumerate(fams): ARMS[f'F{i + 1}_minus_{f}'] = [j for j in ALL if FE[j] not in FAM[f]]
for i, f in enumerate(fams): ARMS[f'F{i + 6}_only_{f}'] = idx_of(FAM[f])
ARMS['F11_query_score'] = idx_of(FAM['QUERY'] + FAM['SCORE']); ARMS['F12_query_score_agreement'] = idx_of(FAM['QUERY'] + FAM['SCORE'] + FAM['AGREEMENT'])
res, PRED = {}, {}
for name, cols in ARMS.items():
    m_, pc, pred, ft, cls = fit_predict(hgb(), cols); PRED[name] = (pc, pred)
    res[name] = dict(n_features=len(cols), fit_seconds=ft, **metrics(yte, pc, pred))
    if name == 'F0_all':
        F0 = m_; F0cls = cls
        if len(C2te):   # reproduction check: the run's stored detection AUROC was computed on all test episodes, C2 included
            Pc = F0.predict_proba(Xc2); pall = np.concatenate([pc, Pc[:, cls.index('NONE')]]); yall = np.concatenate([(yte != 'NONE').astype(int), np.ones(len(C2te), int)])
            R['F0_auroc_including_C2'] = float(roc_auc_score(yall, 1 - pall))
    log(name, {k: round(v, 4) if isinstance(v, float) else v for k, v in res[name].items()})
for name in ARMS:
    if name != 'F0_all': res[name]['diff_ci_vs_F0'] = boot_diff(PRED['F0_all'], PRED[name])
# F14: probe columns permuted jointly across test episodes (F0 model, no refit)
pcols = idx_of(FAM['PROBE']); perm = []
for r_ in range(5):
    Xp = Xte.copy(); pi = np.random.default_rng(100 + r_).permutation(len(Xte)); Xp[:, pcols] = Xte[pi][:, pcols]
    P = F0.predict_proba(Xp); pc = P[:, F0cls.index('NONE')]; pred = np.array([F0cls[i] for i in P.argmax(1)]); perm.append(metrics(yte, pc, pred))
    if r_ == 0: PRED['F14_probe_permuted'] = (pc, pred)
res['F14_probe_permuted'] = dict(n_features=63, permutations=5, **{k: float(np.mean([p[k] for p in perm])) for k in perm[0]}, diff_ci_vs_F0=boot_diff(PRED['F0_all'], PRED['F14_probe_permuted']))
log('F14', {k: round(v, 4) for k, v in res['F14_probe_permuted'].items() if isinstance(v, float)})
R['A_ablation'] = res
# B1: same supervision, same features
B1 = {}
for name, mk in [('logistic_regression', lambda: make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000, class_weight='balanced'))),
                 ('random_forest', lambda: RandomForestClassifier(n_estimators=int(os.environ.get("V20_TREES", 500)), min_samples_leaf=2, class_weight='balanced', n_jobs=-1, random_state=seed)),
                 ('mlp', lambda: make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(128, 64), early_stopping=True, max_iter=500, random_state=seed)))]:
    try:
        _, pc, pred, ft, _ = fit_predict(mk(), ALL, impute=True); B1[name] = dict(fit_seconds=ft, **metrics(yte, pc, pred), diff_ci_vs_F0=boot_diff(PRED['F0_all'], (pc, pred)))
    except Exception as ex: B1[name] = dict(error=repr(ex)[:200])
    log('B1', name, {k: round(v, 4) if isinstance(v, float) else v for k, v in B1[name].items() if k != 'diff_ci_vs_F0'})
B1['hgb_attributor'] = {k: v for k, v in res['F0_all'].items()}
R['B1_same_supervision'] = B1
# B2: same information, no learned classifier over features (detection only)
yb_tr = (ytr != 'NONE').astype(int); yb_te = (yte != 'NONE').astype(int)
best = max(ALL, key=lambda j: abs(roc_auc_score(yb_tr, fill(Xtr)[:, j]) - 0.5)); sgn = 1 if roc_auc_score(yb_tr, fill(Xtr)[:, best]) >= 0.5 else -1
det = lambda s: dict(auroc=float(roc_auc_score(yb_te, s)), auprc=float(average_precision_score(yb_te, s)))
R['B2_same_information'] = dict(best_single_feature=dict(feature=FE[best], sign=sgn, chosen_on='train', **det(sgn * fill(Xte)[:, best])),
                                neg_top_reranker_score=det(-fill(Xte)[:, col['ce1']]), neg_top_dense_score=det(-fill(Xte)[:, col['d1']]),
                                hgb_attributor=dict(auroc=res['F0_all']['auroc'], auprc=res['F0_all']['auprc']))
log('B2', R['B2_same_information'])
dbp = os.path.join(a.run, 'detection_baselines.csv')
if os.path.exists(dbp):
    R['stored_detection_baselines'] = {r_.get('method') or r_.get(list(r_)[0]): r_ for r_ in csv.DictReader(open(dbp))}
# C2: leave-one-mechanism-out
if a.lomo:
    L = {}; faults = sorted(set(ytr) - {'NONE'})
    if a.trial: faults = faults[:2]
    clean_te = yte == 'NONE'
    for f in faults:
        keep = ytr != f; m_ = hgb().fit(Xtr[keep], ytr[keep]); cls = list(m_.classes_); P = m_.predict_proba(Xte); pc = P[:, cls.index('NONE')]
        sel = (yte == f) | clean_te
        top = np.array([cls[i] for i in P.argmax(1)]); fault_cols = [i for i, c in enumerate(cls) if c != 'NONE']
        topf = np.array([cls[fault_cols[i]] for i in P[:, fault_cols].argmax(1)])
        fm = yte == f
        L[f] = dict(n_test=int(fm.sum()), auroc_vs_clean=float(roc_auc_score((yte[sel] == f).astype(int), 1 - pc[sel])) if fm.any() else float('nan'),
                    flagged=float((top[fm] != 'NONE').mean()) if fm.any() else float('nan'),
                    group_of_top_fault_class=float(np.mean([GROUP(c) == f[0] for c in topf[fm]])) if fm.any() else float('nan'),
                    flagged_and_right_group=float(np.mean([(t != 'NONE') and GROUP(t) == f[0] for t in top[fm]])) if fm.any() else float('nan'))
        log('LOMO', f, {k: round(v, 3) if isinstance(v, float) else v for k, v in L[f].items()})
    agg = lambda k: float(np.nanmean([v[k] for v in L.values()]))
    R['C2_leave_one_mechanism_out'] = dict(per_fault=L, mean_auroc_vs_clean=agg('auroc_vs_clean'), mean_flagged=agg('flagged'), mean_group_of_top_fault_class=agg('group_of_top_fault_class'),
                                           mean_flagged_and_right_group=agg('flagged_and_right_group'),
                                           chance_group=float(np.mean([1 / 3] * len(L))), note='exact identification of an unseen label is undefined and not reported')
json.dump(R, open(os.path.join(a.out, f"RESULT_{R['run']}.json"), 'w'), indent=1, default=str); log('done', R['run'])
