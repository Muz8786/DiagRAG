"""WORKSTREAM 1 (diagnosis only). Why did the C2 and Q03 detector gates flip across the seven judged runs?
NO code, bar or threshold is changed by this script. It re-fits each run's attributor from that run's own episodes.jsonl
(same HistGradientBoosting settings, same seed, same train/calibration split as the shipped code) and then asks four questions.

Q1  Does the offline re-fit reproduce the AUROC that the judged run reported?  (If not, nothing below is trusted for that run.)
Q2  C2: the attributor never trains on C2 episodes, so the 25 TRAIN-split C2 episodes are a second, equally held-out set of positives.
    Is the seed-48 failure a property of which 25 positives landed in the test split?
Q3  C2: does the test-split pair composition (12 fault pairs, ~2 episodes each) explain it?
Q4  Q03: pooled out-of-fold AUROC on all ~50 Q03 positives (train+test) per run, by construction era
    (v1/v2 synonym swap; v3/v4 real-user query pairs), and the probability of the observed pass/fail pattern under a fixed true AUROC.

Usage: python diagnose_gate_flips.py <dir containing judged_*/episodes.jsonl and *PROTOCOL.json> <out.json>
(the zip's `kaggle/` folder works). Only the read-only judged outputs are used."""
import collections, hashlib, json, math, os, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold

ROOT, OUT = sys.argv[1], sys.argv[2]
RUNS = [('seed42', 'judged_cpu_run_seed42', 'CPU', 'v1 (synonym-swap Q03)'), ('seed43', 'judged_cpu_run_seed43', 'CPU', 'v1 (synonym-swap Q03)'),
        ('seed44', 'judged_cpu_run_v2_seed44', 'CPU', 'v2 (synonym-swap Q03)'), ('seed45', 'judged_cpu_run_v3_seed45', 'CPU', 'v3 (real query-pair Q03)'),
        ('seed46', 'judged_gpu_v3_seed46', 'GPU', 'v3 (real query-pair Q03)'), ('seed47', 'judged_cpu_run_v4_seed47', 'CPU', 'v4 (real query-pair Q03)'),
        ('seed48', 'judged_gpu_v4_seed48', 'GPU', 'v4 (real query-pair Q03)')]
GROUP = lambda f: f[0]


def hgb(seed): return HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5,
                                                       l2_regularization=1.0, class_weight='balanced', random_state=seed)


def boot(y, s, n=1000, seed=0):
    r = np.random.default_rng(seed); a = roc_auc_score(y, s); bs = []
    for _ in range(n):
        i = r.integers(0, len(y), len(y))
        if len(set(y[i])) == 2: bs.append(roc_auc_score(y[i], s[i]))
    return float(a), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), float(np.std(bs))


def load(folder):
    f = os.path.join(ROOT, folder)
    rows = [json.loads(l) for l in open(os.path.join(f, 'episodes.jsonl'), encoding='utf-8')]
    prot = json.load(open([os.path.join(f, p) for p in os.listdir(f) if p.endswith('PROTOCOL.json')][0]))
    rep = {r['fault']: r for r in __import__('csv').DictReader(open(os.path.join(f, 'detector_gates.csv')))}
    return rows, int(prot['cfg']['SEED']), prot['gates'], rep


def run_one(tag, folder, stack, era):
    rows, seed, gates, rep = load(folder)
    FE = sorted(rows[0]['feats']); mat = lambda es: np.array([[e['feats'][k] for k in FE] for e in es], dtype=np.float32)
    sing = [e for e in rows if e['fault'] != 'C2']; TR = [e for e in sing if e['split'] == 'train']; TE = [e for e in sing if e['split'] == 'test']
    C2tr = [e for e in rows if e['fault'] == 'C2' and e['split'] == 'train']; C2te = [e for e in rows if e['fault'] == 'C2' and e['split'] == 'test']
    out = dict(run=tag, folder=folder, stack=stack, era=era, seed=seed, n_C2_train=len(C2tr), n_C2_test=len(C2te), n_TE_singles=len(TE))
    Xtr, ytr = mat(TR), np.array([e['fault'] for e in TR]); Xte = mat(TE)
    # variant A: the v2+ code (calibration split of clean TRAIN queries excluded from the attributor fit)
    CAL = {e['bid'] for e in TR if e['fault'] == 'NONE' and int(hashlib.md5(('cal|' + e['bid']).encode()).hexdigest()[:8], 16) / 2**32 < 0.5}
    keepA = np.array([not (e['fault'] == 'NONE' and e['bid'] in CAL) for e in TR])
    variants = {'calsplit': keepA, 'all_train': np.ones(len(TR), bool)}
    ref = float(rep['C2']['auroc']) if 'C2' in rep else None
    # The variant is fixed by code era, NOT chosen to match the reported number: the calibration split of clean TRAIN queries was
    # introduced in v2 (seeds 44+); v1 (seeds 42, 43) fitted the attributor on all training episodes.
    era_variant = 'all_train' if era.startswith('v1') else 'calsplit'
    allv = {}
    for name, keep in variants.items():
        att = hgb(seed).fit(Xtr[keep], ytr[keep]); cls = list(att.classes_)
        def sec(es, att=att, cls=cls):
            p = att.predict_proba(mat(es)); gm = np.zeros((len(es), 3))
            for j, c_ in enumerate(cls):
                if c_ != 'NONE': gm[:, 'QKR'.index(GROUP(c_))] += p[:, j]
            return np.sort(gm, 1)[:, -2]
        y_te = np.array([1] * len(C2te) + [0] * len(TE)); allv[name] = (float(roc_auc_score(y_te, np.concatenate([sec(C2te), sec(TE)]))), name, att, sec)
    a, name, att, sec = allv[era_variant]
    out['C2_variant_aurocs'] = {k: v[0] for k, v in allv.items()}
    out.update(C2_reported_auroc=ref, C2_refit_auroc=float(a), C2_refit_variant=name, C2_replicates=bool(abs(a - ref) < 0.015))
    s_neg = sec(TE); s_te_pos, s_tr_pos = sec(C2te), sec(C2tr)
    y1 = np.array([1] * len(C2te) + [0] * len(TE)); r1 = boot(y1, np.concatenate([s_te_pos, s_neg]))
    y2 = np.array([1] * len(C2tr) + [0] * len(TE)); r2 = boot(y2, np.concatenate([s_tr_pos, s_neg]))
    pool = np.concatenate([s_te_pos, s_tr_pos]); r3 = boot(np.array([1] * len(pool) + [0] * len(TE)), np.concatenate([pool, s_neg]))
    out['_scores'] = dict(pos_test=[float(x) for x in s_te_pos], pos_train=[float(x) for x in s_tr_pos], neg=[float(x) for x in s_neg])
    out.update(C2_test25=dict(auroc=r1[0], ci=[r1[1], r1[2]], se=r1[3]), C2_train25_heldout_from_attributor=dict(auroc=r2[0], ci=[r2[1], r2[2]], se=r2[3]),
               C2_pooled50=dict(auroc=r3[0], ci=[r3[1], r3[2]], se=r3[3]),
               neg_score_quantiles={q: float(np.quantile(s_neg, q)) for q in (0.5, 0.9, 0.95)},
               pos_test_median=float(np.median(s_te_pos)), pos_train_median=float(np.median(s_tr_pos)))
    # pair composition
    pair = lambda e: '+'.join(e['meta']['combo'])
    comp = {}
    for e, sc in list(zip(C2te, s_te_pos)) + list(zip(C2tr, s_tr_pos)):
        comp.setdefault(pair(e), {'test': [], 'train': []})[e['split']].append(float(sc))
    out['C2_pairs'] = {k: dict(n_test=len(v['test']), n_train=len(v['train']), mean_test=(float(np.mean(v['test'])) if v['test'] else None),
                               mean_train=(float(np.mean(v['train'])) if v['train'] else None)) for k, v in sorted(comp.items())}
    # which pairs are 'low second-group mass' in this run (score below the 10th percentile of singles' 90th = TAU_C2-like level)
    tau = float(np.quantile(s_neg, 0.90)); out['C2_test_frac_below_tau90_of_singles'] = float(np.mean(s_te_pos < tau)); out['C2_train_frac_below_tau90_of_singles'] = float(np.mean(s_tr_pos < tau))
    # Q03: pooled out-of-fold head AUROC on train+test singles
    allx = np.concatenate([Xtr, Xte]); ally = np.concatenate([ytr, np.array([e['fault'] for e in TE])]); bids = [e['bid'] for e in TR + TE]
    yb = (ally == 'Q03').astype(int); oof = np.zeros(len(yb))
    for a_, b_ in GroupKFold(5).split(allx, yb, bids):
        oof[b_] = hgb(seed).fit(allx[a_], yb[a_]).predict_proba(allx[b_])[:, 1]
    r4 = boot(yb, oof)
    q = [e for e in rep if e == 'Q03'][0]
    out['Q03'] = dict(reported_auroc=float(rep['Q03']['auroc']), reported_ci=[float(rep['Q03']['ci_lo']), float(rep['Q03']['ci_hi'])], reported_status=rep['Q03']['status'],
                      n_pos_test=int(rep['Q03']['n_pos_test']), n_pos_pooled=int(yb.sum()), pooled_oof_auroc=r4[0], pooled_oof_ci=[r4[1], r4[2]], pooled_oof_se=r4[3])
    return out


res = [run_one(*r) for r in RUNS]
# --- era summary and the binomial/normal consistency check for Q03
def pnorm(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))
summ = {}
for era_key, sel in (('v1_v2_synonym_swap', lambda r: r['era'].startswith(('v1', 'v2'))), ('v3_v4_real_query_pairs', lambda r: r['era'].startswith(('v3', 'v4')))):
    rr = [r for r in res if sel(r)]; a = np.array([r['Q03']['reported_auroc'] for r in rr]); se = np.array([(r['Q03']['reported_ci'][1] - r['Q03']['reported_ci'][0]) / 3.92 for r in rr])
    w = 1 / se**2; mu = float((a * w).sum() / w.sum()); se_mu = float(1 / math.sqrt(w.sum()))
    p_pass = [1 - pnorm((0.70 - mu) / s_) for s_ in se]; passes = [r['Q03']['reported_status'] == 'PASS' for r in rr]
    het = float(((a - mu)**2 * w).sum())   # Cochran Q, df = k-1
    # probability of >= observed number of passes if each run independently passes with p_pass[i]
    summ[era_key] = dict(runs=[r['run'] for r in rr], aurocs=[float(x) for x in a], inverse_variance_mean=mu, se_of_mean=se_mu, mean_ci=[mu - 1.96 * se_mu, mu + 1.96 * se_mu],
                         p_pass_each_if_true_equals_mean=[float(p) for p in p_pass], passes=int(sum(passes)), expected_passes=float(sum(p_pass)), cochran_Q=het, df=len(rr) - 1,
                         pooled_oof_aurocs=[r['Q03']['pooled_oof_auroc'] for r in rr])
a_all = np.array([r['Q03']['reported_auroc'] for r in res]); se_all = np.array([(r['Q03']['reported_ci'][1] - r['Q03']['reported_ci'][0]) / 3.92 for r in res])
w = 1 / se_all**2; mu_all = float((a_all * w).sum() / w.sum()); summ['all_seven_one_population'] = dict(inverse_variance_mean=mu_all, cochran_Q=float(((a_all - mu_all)**2 * w).sum()), df=6,
                                                                                                         note='Q > 12.6 (chi2 df=6, p<0.05) means the seven runs are NOT draws from one true AUROC')

# --- Q3 (C2): split-luck permutation. Pool each run's 50 C2 scores, draw 25 at random as "test", repeat; how often does the draw FAIL the 0.70 bar?
rng = np.random.default_rng(0)
for r in res:
    sc = r['_scores']; pos = np.array(sc['pos_test'] + sc['pos_train']); neg = np.array(sc['neg']); nt = len(sc['pos_test'])
    y = np.array([1] * nt + [0] * len(neg)); aucs = []
    for _ in range(4000):
        i = rng.permutation(len(pos))[:nt]; aucs.append(roc_auc_score(y, np.concatenate([pos[i], neg])))
    aucs = np.array(aucs); obs = r['C2_test25']['auroc']
    r['C2_split_luck'] = dict(pooled50=r['C2_pooled50']['auroc'], draw_mean=float(aucs.mean()), draw_sd=float(aucs.std()), p_fail_by_split_alone=float((aucs < 0.70).mean()),
                              observed_test_auroc=obs, observed_percentile=float((aucs <= obs).mean()))
    print(r['run'], 'C2 split-luck: pooled50 %.3f | random 25-of-50 draws mean %.3f sd %.3f | P(fail 0.70 by split alone) %.3f | observed %.3f is at percentile %.0f'
          % (r['C2_split_luck']['pooled50'], aucs.mean(), aucs.std(), r['C2_split_luck']['p_fail_by_split_alone'], obs, 100 * r['C2_split_luck']['observed_percentile']))
# --- all 28 faults: AUROC across the seven runs (reported values only), margin to the bar, and a model-based planning calculation
import csv
per = collections.defaultdict(list)
for tag, folder, stack, era in RUNS:
    for row in csv.DictReader(open(os.path.join(ROOT, folder, 'detector_gates.csv'))):
        if row['auroc'] not in ('', 'nan'):
            per[row['fault']].append((tag, float(row['auroc']), (float(row['ci_hi']) - float(row['ci_lo'])) / 3.92, int(row['n_pos_test']), row['status']))
tab = {}
for f, v in sorted(per.items()):
    a = np.array([x[1] for x in v]); se = np.array([x[2] for x in v]); st = [x[4] for x in v]
    tab[f] = dict(n_runs=len(v), min=float(a.min()), median=float(np.median(a)), max=float(a.max()), fails=int(sum(x == 'FAIL' for x in st)), thin=int(sum(x == 'THIN' for x in st)),
                  mean_se=float(se.mean()), runs=[dict(run=x[0], auroc=x[1], n_pos_test=x[3], status=x[4]) for x in v])
# --- What the record implies for the 27-detector rule. CORE 28 only (R25/R26/K11/K12 are outside the adoption count).
# 25 of the 28 never fail and never drop below 0.80 in any of the seven runs, so the whole risk sits in Q03 and C2 (need >= 27 of 28: at most ONE fail).
core = {f: t for f, t in tab.items() if f not in ('R25', 'R26', 'K11', 'K12')}
stable = [f for f, t in core.items() if t['fails'] == 0 and t['min'] >= 0.80]
risky = [f for f in core if f not in stable]
def p_fail_empirical(f): t = core[f]; return t['fails'] / t['n_runs']
# Empirical (frequency) estimates are used rather than a distributional model, because the Q03/C2 run-to-run variance is larger than their
# within-run standard error (Cochran Q for Q03 = 68 on 6 df): a model built on the within-run SE would be over-confident.
# Q03 is estimated on the v3/v4 era only (its construction changed at v3); C2 on all seven runs.
q3_era = [r for r in tab['Q03']['runs'] if r['run'] in ('seed45', 'seed46', 'seed47', 'seed48')]
pq = sum(r['status'] == 'FAIL' for r in q3_era) / len(q3_era); pc = core['C2']['fails'] / core['C2']['n_runs']
# add-one (Laplace) smoothing so that 0 observed fails of n is not read as probability 0
sm = lambda k, n: (k + 1) / (n + 2)
pq_s, pc_s = sm(sum(r['status'] == 'FAIL' for r in q3_era), len(q3_era)), sm(core['C2']['fails'], core['C2']['n_runs'])
p_adopt_det = 1 - pq_s * pc_s      # fails the 27-detector rule only if BOTH fail (>= 2 fails among the 28), assuming independence of Q03 and C2
plan = dict(stable_faults=len(stable), risky_faults=risky, q03_fail_rate_v3v4_raw=pq, c2_fail_rate_raw=pc, q03_fail_rate_smoothed=pq_s, c2_fail_rate_smoothed=pc_s,
            p_detector_rule_met_if_independent=p_adopt_det, observed_detector_counts_per_run={'seed42': 28, 'seed43': 28, 'seed44': 28, 'seed45': 27, 'seed46': 27, 'seed47': 28, 'seed48': 26},
            reading='The seven-run record has ONE run (seed48) with both Q03 and C2 failing, i.e. 1 of 7 below the 27-detector bar. The model above gives its chance as pq*pc. '
                    'These are frequencies from 7 runs of one codebase family and are planning aids, not guarantees.')
print('PLAN:', json.dumps(plan))
json.dump(dict(runs=[{k: v for k, v in r.items() if k != '_scores'} for r in res], q03_summary=summ, per_fault_detector_stability=tab, planning_model=plan), open(OUT, 'w'), indent=1)
print(json.dumps(summ, indent=1))
for r in res:
    print(r['run'], r['stack'], 'C2 rep %.3f refit %.3f (%s, replicates=%s) | test25 %.3f [%.2f,%.2f] | train25(held-out) %.3f [%.2f,%.2f] | pooled50 %.3f | Q03 rep %.3f pooledOOF %.3f'
          % (r['C2_reported_auroc'], r['C2_refit_auroc'], r['C2_refit_variant'], r['C2_replicates'], r['C2_test25']['auroc'], *r['C2_test25']['ci'],
             r['C2_train25_heldout_from_attributor']['auroc'], *r['C2_train25_heldout_from_attributor']['ci'], r['C2_pooled50']['auroc'], r['Q03']['reported_auroc'], r['Q03']['pooled_oof_auroc']))
