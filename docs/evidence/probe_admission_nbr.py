# PRE-REGISTERED probe admission test (docs/evidence/v5_protocol.md, item C4). Run ONCE. TRAIN split only, out-of-fold, grouped by base query.
# Executed through a harness that loads the v4 pipeline state (seed-47 checkpoint). No held-out (test-split) episode is read.
#
# Probe = one extra retrieval with the query-log nearest neighbour of the query (other users' queries; the same neighbour the Q03 repair uses):
#   nbr_cos      cosine similarity of the query to its nearest log neighbour
#   nbr_overlap  Jaccard overlap of the neighbour's top-5 with the original top-5
#   nbr_ce_gain  best cross-encoder score of the neighbour's retrieval minus the original's (ce1)
#
# Admission (all four): (a) mean pairwise OOF AUROC over the five least-separable pairs of IDENTIFIABILITY.md section 4 rises by >= 0.03;
# (b) Q03-vs-rest OOF AUROC rises by >= 0.03; (c) the mean over all pairs does not fall by more than 0.002; (d) fault-vs-clean OOF AUROC does not fall by more than 0.002.
import itertools, json, math, time
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold

EP = RES['EPIS']
TRN = [e for e in EP if e['split'] == 'train' and e['fault'] != 'C2']
assert all(e['split'] == 'train' for e in TRN)
t0 = time.time(); extra = {}
for n_, e in enumerate(TRN):
    st = e['st']; tr0 = run(st); qn, cs = qlog_neighbour(st['q'])
    tr1 = run(dict(st, q=qn)) if qn != st['q'] else tr0
    a, b = set(tr0['final'][:5]), set(tr1['final'][:5])
    extra[id(e)] = dict(nbr_cos=float(cs), nbr_overlap=len(a & b) / max(1, len(a | b)),
                        nbr_ce_gain=(float(np.max(tr1['ce'])) if len(tr1['ce']) else 0.0) - (float(np.max(tr0['ce'])) if len(tr0['ce']) else 0.0))
    if n_ % 400 == 0: print('probe features %d/%d %.0fs' % (n_, len(TRN), time.time() - t0), flush=True)
FE0 = sorted(TRN[0]['feats']); PK = ['nbr_cos', 'nbr_overlap', 'nbr_ce_gain']
X0 = np.array([[e['feats'][k] for k in FE0] for e in TRN], np.float32); XP = np.array([[extra[id(e)][k] for k in PK] for e in TRN], np.float32)
X1 = np.concatenate([X0, XP], 1); y = np.array([e['fault'] for e in TRN]); grp = [e['bid'] for e in TRN]
def hg(): return HistGradientBoostingClassifier(max_iter=150, min_samples_leaf=5, random_state=0)       # same settings as analysis_v3.py (pairwise)
def pair_auc(X, f1, f2):
    m = (y == f1) | (y == f2); Xa, ya, ga = X[m], (y[m] == f1).astype(int), [grp[k] for k in np.where(m)[0]]; s = np.zeros(len(ya))
    for a_, b_ in GroupKFold(5).split(Xa, ya, ga): s[b_] = hg().fit(Xa[a_], ya[a_]).predict_proba(Xa[b_])[:, 1]
    return max(roc_auc_score(ya, s), 1 - roc_auc_score(ya, s))
faults = sorted(set(y) - {'NONE'}); allf = sorted(set(y))
FIVE = [('K04', 'Q03'), ('Q03', 'R22'), ('K05', 'R11'), ('Q04', 'R13'), ('Q03', 'R24')]
res = dict(n_train_episodes=len(TRN), probe_features=PK, five={}, started_utc=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()))
for p_ in FIVE: res['five'][f'{p_[0]}|{p_[1]}'] = dict(base=pair_auc(X0, *p_), probe=pair_auc(X1, *p_)); print(p_, res['five'][f'{p_[0]}|{p_[1]}'], flush=True)
a_base = np.mean([v['base'] for v in res['five'].values()]); a_probe = np.mean([v['probe'] for v in res['five'].values()])
def ovr(X, f):
    yy = (y == f).astype(int); s = np.zeros(len(yy))
    for a_, b_ in GroupKFold(5).split(X, yy, grp): s[b_] = hg().fit(X[a_], yy[a_]).predict_proba(X[b_])[:, 1]
    return roc_auc_score(yy, s)
q3_base, q3_probe = ovr(X0, 'Q03'), ovr(X1, 'Q03')
def fvc(X):   # fault-vs-clean OOF AUROC (clean = NONE)
    yy = (y != 'NONE').astype(int); s = np.zeros(len(yy))
    for a_, b_ in GroupKFold(5).split(X, yy, grp): s[b_] = hg().fit(X[a_], yy[a_]).predict_proba(X[b_])[:, 1]
    return roc_auc_score(yy, s)
fv_base, fv_probe = fvc(X0), fvc(X1)
allp = list(itertools.combinations(allf, 2)); pb, pp = [], []
for n_, (f1, f2) in enumerate(allp):
    pb.append(pair_auc(X0, f1, f2)); pp.append(pair_auc(X1, f1, f2))
    if n_ % 60 == 0: print('all-pairs %d/%d %.0fs' % (n_, len(allp), time.time() - t0), flush=True)
res.update(five_mean_base=float(a_base), five_mean_probe=float(a_probe), five_gain=float(a_probe - a_base), q03_ovr_base=float(q3_base), q03_ovr_probe=float(q3_probe), q03_gain=float(q3_probe - q3_base),
           all_pairs_n=len(allp), all_pairs_mean_base=float(np.mean(pb)), all_pairs_mean_probe=float(np.mean(pp)), all_pairs_change=float(np.mean(pp) - np.mean(pb)),
           fault_vs_clean_base=float(fv_base), fault_vs_clean_probe=float(fv_probe), fault_vs_clean_change=float(fv_probe - fv_base))
cond = dict(a=res['five_gain'] >= 0.03, b=res['q03_gain'] >= 0.03, c=res['all_pairs_change'] >= -0.002, d=res['fault_vs_clean_change'] >= -0.002)
res['conditions'] = cond; res['ADMITTED'] = bool(all(cond.values())); res['finished_utc'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
json.dump(res, open('/projects/sandbox/_w3/probe_admission_result.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'five'}, indent=1))
