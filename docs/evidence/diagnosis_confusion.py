"""POST-HOC, DESCRIPTIVE analysis (not pre-registered; written after a reviewer-style objection that fault-vs-clean AUROC is not fault-type identification).
Question: on the held-out test episodes of a judged run, how accurately does the system identify WHICH fault is present?

Two things are measured.
 (A) The multi-class ATTRIBUTOR: re-fitted from the shipped episodes.jsonl with the run's own settings (train split minus the clean calibration split, class_weight balanced,
     seed from the protocol). Its top-1 class on each held-out test episode (32 classes: 31 single faults + NONE; C2 is a composition and is never a training class).
     A sanity check compares its p(NONE) with the per-episode score stored by the run (needs --checkpoint).
 (B) The END-TO-END DISPATCHER output stored by the run for each test episode (loop3['lab'], needs --checkpoint): the label(s) the loop would dispatch, including group fallbacks "G<letter>".
Reported: exact-fault top-1 accuracy, macro-F1, per-fault precision / recall / F1 / support, the confusion matrix, the most frequent confusions, and accuracy at the repair-family and
letter-group level. Held-out = split 'test'. Faults with fewer than 50 test positives are flagged THIN.
usage: python diagnosis_confusion.py <judged_folder> <out_prefix> [--checkpoint checkpoint.pkl]"""
import argparse, collections, csv, glob, hashlib, json, os, pickle, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier

ap = argparse.ArgumentParser(); ap.add_argument('folder'); ap.add_argument('out'); ap.add_argument('--checkpoint'); a = ap.parse_args()
rows = [json.loads(l) for l in open(os.path.join(a.folder, 'episodes.jsonl'), encoding='utf-8')]
prot = json.load(open(glob.glob(os.path.join(a.folder, '*PROTOCOL.json'))[0])); seed = int(prot['cfg']['SEED']); CAL_FRAC = prot['cfg'].get('CAL_FRAC', 0.5)
FE = sorted(rows[0]['feats']); mat = lambda es: np.array([[e['feats'][k] for k in FE] for e in es], dtype=np.float32)
sing = [e for e in rows if e['fault'] != 'C2']; TR = [e for e in sing if e['split'] == 'train']; TE = [e for e in sing if e['split'] == 'test']
CALB = {e['bid'] for e in TR if e['fault'] == 'NONE' and int(hashlib.md5(('cal|' + e['bid']).encode()).hexdigest()[:8], 16) / 2**32 < CAL_FRAC}
TRA = [e for e in TR if not (e['fault'] == 'NONE' and e['bid'] in CALB)]
hgb = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=seed)
ATT = hgb().fit(mat(TRA), np.array([e['fault'] for e in TRA])); CLS = list(ATT.classes_)
P = ATT.predict_proba(mat(TE)); pred = np.array([CLS[i] for i in P.argmax(1)]); y = np.array([e['fault'] for e in TE])
FAMILY = {c: c for c in CLS}; FAMILY.update(Q01='QLEX', Q03='QLEX', Q04='QLEX', Q05='QLEX', K04='STALE', R07='STALE', R03='ENC', R10='ENC', R11='ENC')
GROUP = {c: ('NONE' if c == 'NONE' else c[0]) for c in CLS}
res = dict(folder=a.folder, n_train=len(TRA), n_test=len(TE), classes=CLS, post_hoc=True)

def prf(y, pred, c):
    tp = int(((y == c) & (pred == c)).sum()); fp = int(((y != c) & (pred == c)).sum()); fn = int(((y == c) & (pred != c)).sum())
    p = tp / (tp + fp) if tp + fp else float('nan'); r = tp / (tp + fn) if tp + fn else float('nan')   # precision is undefined if the class is never predicted
    f = 0.0 if (tp == 0 and tp + fn > 0) else (2 * p * r / (p + r) if p == p and r == r and p + r else float('nan'))   # F1 = 0 when the class is present but never found (NOT dropped from the macro average)
    return dict(support=int((y == c).sum()), precision=p, recall=r, f1=f)
per = {c: prf(y, pred, c) for c in CLS}; faults = [c for c in CLS if c != 'NONE']
macro_all = float(np.nanmean([per[c]['f1'] for c in CLS])); macro_fault = float(np.nanmean([per[c]['f1'] for c in faults]))
fm = y != 'NONE'
res['A_attributor'] = dict(
    top1_accuracy_all_32_classes=float((pred == y).mean()), macro_f1_all=macro_all, macro_f1_faults_only=macro_fault,
    exact_fault_accuracy_on_faulted=float((pred[fm] == y[fm]).mean()), n_faulted=int(fm.sum()),
    faulted_called_clean=float((pred[fm] == 'NONE').mean()), clean_called_fault=float((pred[~fm] != 'NONE').mean()), n_clean=int((~fm).sum()),
    family_accuracy_on_faulted=float(np.mean([FAMILY[p] == FAMILY[t] for p, t in zip(pred[fm], y[fm])])),
    group_accuracy_on_faulted=float(np.mean([GROUP[p] == GROUP[t] for p, t in zip(pred[fm], y[fm])])),
    exact_fault_accuracy_among_detected=float((pred[fm & (pred != 'NONE')] == y[fm & (pred != 'NONE')]).mean()),
    n_thin_faults=[c for c in faults if per[c]['support'] < 50], per_fault=per)
cm = collections.Counter(zip(y, pred)); labels = CLS
with open(a.out + '_confusion.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['true\\pred'] + labels)
    for t in labels: w.writerow([t] + [cm.get((t, p), 0) for p in labels])
conf = sorted(((n, t, p) for (t, p), n in cm.items() if t != p), reverse=True)
res['A_attributor']['top_confusions'] = [dict(n=n, true=t, predicted=p, true_family=FAMILY[t], pred_family=FAMILY[p], same_family=FAMILY[t] == FAMILY[p]) for n, t, p in conf[:20]]
res['A_attributor']['confusions_into_NONE_total'] = int(sum(n for n, t, p in conf if p == 'NONE')); res['A_attributor']['confusions_between_faults_total'] = int(sum(n for n, t, p in conf if p != 'NONE' and t != 'NONE'))

if a.checkpoint:
    R = pickle.load(open(a.checkpoint, 'rb')); E = [e for e in R['EPIS'] if e['split'] == 'test' and e['fault'] != 'C2']
    # sanity: the re-fit models reproduce the run's stored per-episode score s = 1.0 if a precise rule fires, else 1 - p(NONE) from the GROUP attributor (ATTG, letters Q/K/R/NONE)
    RULE_PRIO = ['R26', 'R25', 'K11', 'R23', 'R15', 'K07']
    RULE_FIRE = {'K07': lambda f: f['tenant_mis5'] >= 1, 'R15': lambda f: f['ann_probe'] < 0.9, 'R23': lambda f: f['n_final'] < 5, 'R25': lambda f: f['nonfinite'] >= 1,
                 'R26': lambda f: f['filter_survival'] < 0.5, 'K11': lambda f: f['deleted5'] >= 1}
    grp = lambda yy: np.array(['NONE' if v == 'NONE' else v[0] for v in yy])
    ATTG = hgb().fit(mat(TRA), grp([e['fault'] for e in TRA])); gcl = list(ATTG.classes_); PG = ATTG.predict_proba(mat(TE)); key = {(e['fault'], e['bid']): e for e in E}; d = []
    for e, pg in zip(TE, PG):
        k = (e['fault'], e['bid'])
        if k in key and 'loop3' in key[k]:
            sh = 1.0 if any(RULE_FIRE[r](e['feats']) for r in RULE_PRIO) else float(1 - pg[gcl.index('NONE')]); d.append(abs(sh - key[k]['loop3']['s']))
    d = np.array(d); res['sanity_refit_vs_stored_score'] = dict(n=int(len(d)), max_abs_diff=float(d.max()), mean_abs_diff=float(d.mean()), fraction_within_1e_6=float((d < 1e-6).mean()))
    FAM = lambda l: ('G' + l[1]) if str(l).startswith('G') else FAMILY[str(l)]; GRP = lambda l: l[1] if str(l).startswith('G') else GROUP[str(l)]
    fl = [e for e in E if e['fault'] != 'NONE' and 'loop3' in e]; ok_exact = ok_fam = ok_grp = fb = n_nolab = 0
    conf2 = collections.Counter(); per2 = collections.defaultdict(lambda: collections.Counter())
    for e in fl:
        lab = [str(x) for x in e['loop3']['lab']]; t = e['fault']
        if not lab: n_nolab += 1; per2[t]['none'] += 1; continue
        top = lab[0]; ex = top == t; fa = all(not l.startswith('G') for l in lab) and {FAMILY[l] for l in lab} == {FAMILY[t]}; gr = {GRP(l) for l in lab} == {GROUP[t]}
        ok_exact += ex; ok_fam += fa; ok_grp += gr; fb += any(l.startswith('G') for l in lab)
        per2[t]['n'] += 1; per2[t]['exact'] += ex; per2[t]['family'] += fa; per2[t]['group'] += gr; per2[t]['fallback'] += any(l.startswith('G') for l in lab)
        if not ex: conf2[(t, top)] += 1
    n = len(fl)
    res['B_dispatcher_end_to_end'] = dict(n_faulted_test=n, label_exact_top1=ok_exact / n, family_level_correct=ok_fam / n, group_level_correct=ok_grp / n, used_group_fallback=fb / n, no_label=n_nolab / n,
        note='labels the dispatcher would output before the do-no-harm gate; family_level_correct = all labels are non-fallback and name the true repair family; group_level_correct = the labels name the true letter group',
        per_fault={t: dict(n=int(c['n'] + c['none']), exact=c['exact'] / max(c['n'] + c['none'], 1), family=c['family'] / max(c['n'] + c['none'], 1), group=c['group'] / max(c['n'] + c['none'], 1), fallback=c['fallback'] / max(c['n'] + c['none'], 1)) for t, c in sorted(per2.items())},
        top_confusions=[dict(n=n_, true=t, dispatched=p) for (t, p), n_ in conf2.most_common(15)])
json.dump(res, open(a.out + '.json', 'w'), indent=1, default=float)

A = res['A_attributor']
print(f"held-out test: {res['n_test']} episodes ({A['n_faulted']} faulted, {A['n_clean']} clean), {len(CLS)} classes")
print(f"(A) attributor top-1 accuracy, all classes: {A['top1_accuracy_all_32_classes']:.3f} | macro-F1 all {A['macro_f1_all']:.3f}, faults only {A['macro_f1_faults_only']:.3f}")
print(f"    faulted episodes: exact fault {A['exact_fault_accuracy_on_faulted']:.3f}, repair-family {A['family_accuracy_on_faulted']:.3f}, letter-group {A['group_accuracy_on_faulted']:.3f}; called clean {A['faulted_called_clean']:.3f}")
print(f"    among faulted episodes called a fault: exact {A['exact_fault_accuracy_among_detected']:.3f} | clean called faulty {A['clean_called_fault']:.3f}")
print('    errors: %d into NONE, %d between faults' % (A['confusions_into_NONE_total'], A['confusions_between_faults_total']))
if a.checkpoint:
    B = res['B_dispatcher_end_to_end']; S = res['sanity_refit_vs_stored_score']
    print(f"    sanity: re-fit score vs the run's stored per-episode score: n={S['n']}, max |diff| {S['max_abs_diff']:.2e}, within 1e-6: {S['fraction_within_1e_6']:.3f}")
    print(f"(B) dispatcher end to end, n={B['n_faulted_test']}: exact top-1 {B['label_exact_top1']:.3f} | family-level {B['family_level_correct']:.3f} | group-level {B['group_level_correct']:.3f} | fallback used {B['used_group_fallback']:.3f}")
