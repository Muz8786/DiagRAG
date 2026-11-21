"""DiagRAG-Bench quickstart: build a Track-1 diagnoser on the PUBLIC dev split and score it. Works from the release package alone.
Usage:  python quickstart_dev_cv.py release_v1 my_dev_predictions.csv
Replace `fit_predict` with your own diagnoser: it receives dev telemetry + labels (train folds) and the telemetry to predict, and returns P(fault) and a family.
Cross-validation is grouped by nothing here because dev episodes carry no base-query id; expect a mildly optimistic dev score. The real test split has no public labels."""
import csv, json, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold

rel, outp = sys.argv[1], sys.argv[2]


def tel(p):
    rows = list(csv.DictReader(open(p, encoding='utf-8'))); keys = [k for k in rows[0] if k != 'episode_id']
    return [r['episode_id'] for r in rows], np.array([[float(r[k]) for k in keys] for r in rows], np.float32)


def fit_predict(Xtr, ytr_family, Xte):          # <- your diagnoser goes here
    m = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=0).fit(Xtr, ytr_family)
    P = m.predict_proba(Xte); cls = list(m.classes_); return 1 - P[:, cls.index('NONE')], [cls[int(i)] for i in P.argmax(1)]


ids, X = tel(f'{rel}/telemetry_dev.csv'); lab = {j['episode_id']: j for j in map(json.loads, open(f'{rel}/labels_dev.jsonl', encoding='utf-8'))}
y = np.array([lab[i]['family'] for i in ids]); p_fault = np.zeros(len(ids)); fam = [''] * len(ids)
for a, b in StratifiedKFold(5, shuffle=True, random_state=0).split(X, y):
    pf, fm = fit_predict(X[a], y[a], X[b]); p_fault[b] = pf
    for k, f in zip(b, fm): fam[k] = f
with open(outp, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['episode_id', 'p_fault', 'family'])
    for i, p, fm in zip(ids, p_fault, fam): w.writerow([i, float(p), fm])
print('wrote', outp, len(ids), 'dev predictions. Score them with:  python score.py --labels', f'{rel}/labels_dev.jsonl', '--track1', outp)
