"""Re-derive a judged run's DETECTOR table from its shipped episodes.jsonl and compare it with the table the run recorded. CPU only, about 1 to 3 minutes.
Works for v3, v4 and v5 judged folders (those use one gradient-boosted head per fault and the rules RULE/TIER0 below).

Usage:  python reproduce_tables.py <judged_folder> [--max-diff 0.005]
Exit code 0 if every fault's AUROC matches the recorded one within --max-diff, else 1.

What this does and does not show. It re-fits the detectors from the recorded telemetry with the shipped settings and seed, so it checks that the recorded table follows from the
recorded episodes. It does NOT regenerate the episodes (that needs the full run, 2 to 4 hours on a GPU) and it cannot catch an error made before the telemetry was written.
Runs executed on Kaggle's library stack can differ from this re-fit in the third decimal or more (see docs/ROADMAP_V4.md section 2); the tolerance is a parameter, and the differences are printed."""
import argparse, csv, glob, json, os, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

ap = argparse.ArgumentParser(); ap.add_argument('folder'); ap.add_argument('--max-diff', type=float, default=0.005); a = ap.parse_args()
rows = [json.loads(l) for l in open(os.path.join(a.folder, 'episodes.jsonl'), encoding='utf-8')]
prot = json.load(open(glob.glob(os.path.join(a.folder, '*PROTOCOL.json'))[0])); seed = int(prot['cfg']['SEED'])
rec = {r['fault']: r for r in csv.DictReader(open(os.path.join(a.folder, 'detector_gates.csv')))}
K_FINAL = 5
RULE = {'Q04': lambda f: f['q_correctable'], 'K07': lambda f: f['tenant_mis5'], 'R15': lambda f: 1 - f['ann_probe'], 'R23': lambda f: K_FINAL - f['n_final'],
        'R25': lambda f: f['nonfinite'], 'R26': lambda f: 1 - f['filter_survival'], 'K11': lambda f: f['deleted5']}
sing = [e for e in rows if e['fault'] != 'C2']; TR = [e for e in sing if e['split'] == 'train']; TE = [e for e in sing if e['split'] == 'test']
FE = sorted(rows[0]['feats']); mat = lambda es: np.array([[e['feats'][k] for k in FE] for e in es], dtype=np.float32)
Xtr, Xte = mat(TR), mat(TE); ytr = np.array([e['fault'] for e in TR]); yte = np.array([e['fault'] for e in TE])
hgb = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=seed)
worst, n_ok, n_cmp = 0.0, 0, 0
print('%-6s %8s %8s %8s  %s' % ('fault', 'recorded', 're-fit', 'diff', 'head'))
for f in sorted(rec):
    if f == 'C2' or rec[f]['auroc'] in ('', 'nan') or int((yte == f).sum()) == 0: continue
    if f in RULE: s = np.array([RULE[f](e['feats']) for e in TE]); head = 'rule'
    elif int((ytr == f).sum()) >= 3: s = hgb().fit(Xtr, (ytr == f).astype(int)).predict_proba(Xte)[:, 1]; head = 'hgb'
    else: continue
    ref = float(rec[f]['auroc']); new = float(roc_auc_score((yte == f).astype(int), s)); d = new - ref; worst = max(worst, abs(d)); n_cmp += 1; n_ok += abs(d) <= a.max_diff
    print('%-6s %8.4f %8.4f %+8.4f  %s%s' % (f, ref, new, d, head, '' if abs(d) <= a.max_diff else '   <-- differs'))
print('\n%d of %d detector AUROCs reproduced within %.3f; largest difference %.4f' % (n_ok, n_cmp, a.max_diff, worst))
print('(C2 is scored from the attributor and is covered by docs/evidence/diagnose_gate_flips.py)')
sys.exit(0 if n_ok == n_cmp else 1)
