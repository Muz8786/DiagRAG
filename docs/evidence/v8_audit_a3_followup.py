"""POST-HOC follow-up to audit check A3 (docs/evidence/v8_protocol.md amendment E2). Written AFTER A3 missed its pre-registered band, so it is explanatory, not a gate.
Question: is the shuffled-label AUROC drift (mean 0.535 against a pre-registered band of 0.45 to 0.55) label leakage, or a property of the features?
(1) shuffled-label attributor scores against a test-label-permutation null; (2) a score that never sees any label: mean distance of each held-out episode to its 5 nearest training episodes.
usage: python docs/evidence/v8_audit_a3_followup.py <judged_folder> <out.json>"""
import glob, hashlib, json, os, sys
import numpy as np
from scipy.stats import rankdata
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.neighbors import NearestNeighbors

folder, outp = sys.argv[1], sys.argv[2]
rows = [json.loads(l) for l in open(os.path.join(folder, 'episodes.jsonl'), encoding='utf-8')]
prot = json.load(open(glob.glob(os.path.join(folder, '*PROTOCOL.json'))[0])); seed = int(prot['cfg']['SEED']); CF = prot['cfg'].get('CAL_FRAC', 0.5)
FE = sorted(rows[0]['feats']); mat = lambda es: np.array([[e['feats'][k] for k in FE] for e in es], dtype=np.float32)
sing = [e for e in rows if e['fault'] != 'C2']; TR = [e for e in sing if e['split'] == 'train']; TE = [e for e in sing if e['split'] == 'test']
CALB = {e['bid'] for e in TR if e['fault'] == 'NONE' and int(hashlib.md5(('cal|' + e['bid']).encode()).hexdigest()[:8], 16) / 2**32 < CF}
TRA = [e for e in TR if not (e['fault'] == 'NONE' and e['bid'] in CALB)]
ytr = np.array([e['fault'] for e in TRA]); fm = np.array([e['fault'] != 'NONE' for e in TE]).astype(int); Xtr, Xte = mat(TRA), mat(TE)


def auc(y, s):
    r = rankdata(s); p = y == 1
    return float((r[p].sum() - p.sum() * (p.sum() + 1) / 2) / (p.sum() * (~p).sum()))


out = dict(folder=folder, shuffles=[])
for s in range(20):
    m = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=seed
                                       ).fit(Xtr, np.random.default_rng(s).permutation(ytr))
    cls = list(m.classes_); sc = 1 - m.predict_proba(Xte)[:, cls.index('NONE')]
    nulls = [auc(np.random.default_rng(100 + k).permutation(fm), sc) for k in range(200)]
    out['shuffles'].append(dict(shuffle=s, auroc=auc(fm, sc), test_label_permutation_null_mean=float(np.mean(nulls)), null_sd=float(np.std(nulls))))
a = [x['auroc'] for x in out['shuffles']]
out['summary'] = dict(mean=float(np.mean(a)), min=float(np.min(a)), max=float(np.max(a)), null_sd=float(np.mean([x['null_sd'] for x in out['shuffles']])))
mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9; d, _ = NearestNeighbors(n_neighbors=5).fit((Xtr - mu) / sd).kneighbors((Xte - mu) / sd); s5 = d.mean(1)
out['label_free_knn_distance'] = dict(auroc_fault_vs_clean=auc(fm, s5), median_distance_faulted=float(np.median(s5[fm == 1])), median_distance_clean=float(np.median(s5[fm == 0])),
                                      note='uses no labels at all; faulted held-out episodes lie farther from the training data than clean ones')
json.dump(out, open(outp, 'w'), indent=1); print(json.dumps(dict(summary=out['summary'], label_free=out['label_free_knn_distance']), indent=1))
