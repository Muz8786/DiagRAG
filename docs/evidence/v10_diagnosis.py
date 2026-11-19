"""v10 diagnosis (DESCRIPTIVE, post-hoc, read-only; no gate, bar or code is changed). Why do C2 and Q03 sit near or under the 0.70 detector bar in the v6 and v8 GPU runs?
(1) Is the C2 change 0.751 -> 0.681 distinguishable from sampling noise? Two-sample z test from the stored AUROCs and their stored 95% CIs (SE = CI width / 3.92).
(2) What does the multi-class attributor predict for Q03 and C2 held-out episodes? (top predicted classes, share called clean).
(3) How many held-out positives does each have, and what is the width of a 95% interval at that n?
usage: python docs/evidence/v10_diagnosis.py <out.json>   (scikit-learn 1.6.1)"""
import collections, csv, glob, hashlib, json, math, os, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier

out = {}
runs = {'v6_gpu_seed50': 'kaggle/judged_gpu_v6_seed50', 'v8_gpu_seed52': 'kaggle/judged_gpu_v8_seed52'}
gate = {}
for tag, d in runs.items():
    for r in csv.DictReader(open(os.path.join(d, 'detector_gates.csv'))):
        if r['fault'] in ('Q03', 'C2'): gate[(tag, r['fault'])] = dict(auroc=float(r['auroc']), lo=float(r['ci_lo']), hi=float(r['ci_hi']), n_pos_test=int(r['n_pos_test']), status=r['status'])
out['stored_detector_gates'] = {f'{t}|{f}': v for (t, f), v in gate.items()}
for f in ('C2', 'Q03'):
    a, b = gate[('v6_gpu_seed50', f)], gate[('v8_gpu_seed52', f)]; se = lambda g: (g['hi'] - g['lo']) / 3.92
    z = (a['auroc'] - b['auroc']) / math.sqrt(se(a) ** 2 + se(b) ** 2); p = math.erfc(abs(z) / math.sqrt(2))
    out[f'{f}_v6_vs_v8'] = dict(auroc_v6=a['auroc'], auroc_v8=b['auroc'], diff=a['auroc'] - b['auroc'], z=z, two_sided_p_normal_approx=p,
                                 half_width_95_v6=(a['hi'] - a['lo']) / 2, half_width_95_v8=(b['hi'] - b['lo']) / 2, n_pos_test=(a['n_pos_test'], b['n_pos_test']),
                                 reading='difference is within sampling noise' if p > 0.05 else 'difference is NOT explained by sampling noise alone')

for tag, d in runs.items():
    rows = [json.loads(l) for l in open(os.path.join(d, 'episodes.jsonl'), encoding='utf-8')]
    prot = json.load(open(glob.glob(os.path.join(d, '*PROTOCOL.json'))[0])); seed = int(prot['cfg']['SEED']); CF = prot['cfg'].get('CAL_FRAC', 0.5)
    FE = sorted(rows[0]['feats']); mat = lambda es: np.array([[e['feats'][k] for k in FE] for e in es], dtype=np.float32)
    sing = [e for e in rows if e['fault'] != 'C2']; TR = [e for e in sing if e['split'] == 'train']; TE = [e for e in sing if e['split'] == 'test']
    CALB = {e['bid'] for e in TR if e['fault'] == 'NONE' and int(hashlib.md5(('cal|' + e['bid']).encode()).hexdigest()[:8], 16) / 2**32 < CF}
    TRA = [e for e in TR if not (e['fault'] == 'NONE' and e['bid'] in CALB)]
    m = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=seed
                                       ).fit(mat(TRA), np.array([e['fault'] for e in TRA]))
    cls = list(m.classes_); P = m.predict_proba(mat(TE)); pred = np.array([cls[i] for i in P.argmax(1)]); y = np.array([e['fault'] for e in TE])
    q = y == 'Q03'; tgt = collections.Counter(pred[q]).most_common(6)
    # C2 has no training class: report how the attributor scores the C2 test episodes (all rows with fault C2 in the held-out split)
    C2 = [e for e in rows if e['fault'] == 'C2' and e['split'] == 'test']; P2 = m.predict_proba(mat(C2)); pr2 = np.array([cls[i] for i in P2.argmax(1)])
    out[tag] = dict(n_train_fit=len(TRA), Q03_n_test=int(q.sum()), Q03_predicted_as=tgt, Q03_called_clean=float((pred[q] == 'NONE').mean()), Q03_exact=float((pred[q] == 'Q03').mean()),
                    Q03_mean_p_of_true_class=float(P[q][:, cls.index('Q03')].mean()), C2_n_test=len(C2), C2_attributor_top_classes=collections.Counter(pr2).most_common(6), C2_called_clean=float((pr2 == 'NONE').mean()))
    print(tag, json.dumps(out[tag])[:700], flush=True)
for f in ('C2', 'Q03'): print(f, json.dumps(out[f'{f}_v6_vs_v8']))
json.dump(out, open(sys.argv[1], 'w'), indent=1)
