"""Reference Track 1 baseline: HistGB on the public dev telemetry, predicting the test episodes.
Usage: python baseline_track1.py release_v1 out.csv
Uses only public files (telemetry_dev.csv, labels_dev.jsonl, telemetry_test.csv, families.json)."""
import csv, json, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
rel, outp = sys.argv[1], sys.argv[2]
def tel(p):
    rows = list(csv.DictReader(open(p))); return [r['episode_id'] for r in rows], np.array([[float(r[k]) for k in rows[0] if k != 'episode_id'] for r in rows], np.float32)
ids_d, Xd = tel(f'{rel}/telemetry_dev.csv'); ids_t, Xt = tel(f'{rel}/telemetry_test.csv')
lab = {j['episode_id']: j for j in map(json.loads, open(f'{rel}/labels_dev.jsonl'))}
y = np.array([lab[i]['family'] for i in ids_d])
m = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0,
                                   class_weight='balanced', random_state=0).fit(Xd, y)
P = m.predict_proba(Xt); cls = list(m.classes_); iN = cls.index('NONE')
with open(outp, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['episode_id', 'p_fault', 'family'])
    for i, p in zip(ids_t, P): w.writerow([i, float(1 - p[iN]), cls[int(np.argmax(p))]])
print('wrote', outp, len(ids_t))
