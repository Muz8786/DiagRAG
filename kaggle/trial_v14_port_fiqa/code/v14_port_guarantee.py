"""v14 E4 (per-stratum conformal do-no-harm gate on the second stack) and E4b (real failures labelled by intervention) by replay of a judged port5 run.
docs/evidence/v14_flagship_protocol.md (E4, E4b, amendment A1).
usage: DATASET=<ds> python docs/evidence/v14_port_guarantee.py <work_dir> <code_file> <out_dir> [TRIAL]
<work_dir> must contain port5_<ds>_out/{checkpoint.pkl,corpus_e5.npy,PORT_PROTOCOL.json,port_detector_gates.csv} and the verified zips under the port data folder."""
import csv, glob, hashlib, json, math, os, pickle, re, sys, time
import numpy as np

work, code_file, outd = sys.argv[1:4]; TRIAL = len(sys.argv) > 4 and sys.argv[4] == '1'; ds = os.environ['DATASET']; os.makedirs(outd, exist_ok=True)
outdir = glob.glob(os.path.join(work, f'port*_{ds}_out'))[0]; prot = json.load(open(os.path.join(outdir, 'PORT_PROTOCOL.json'))); cfg = prot['cfg']
src = open(code_file, encoding='utf-8').read(); assert hashlib.sha256(src.encode('utf-8')).hexdigest() == prot['code_sha256'], 'code file is not the code that produced this run'
os.environ.update(DIAGRAG_WORK=work, SEED=str(cfg['SEED']), N_QUERIES=str(cfg['N_QUERIES']), N_HARD=str(cfg['N_HARD']), MAX_ATT=str(cfg['MAX_ATT']), N_HARM=str(cfg['N_HARM']), TIME_BUDGET='0')
cells = re.split(r'\n# %%(?: \[markdown\])?\n', src); last = max(i for i, c in enumerate(cells) if 'REP = dict(' in c)
g = {'__name__': '__replay__', '__file__': os.path.join(work, os.path.basename(code_file))}; t0 = time.time()
log = lambda *a: print(f'[{time.time() - t0:6.0f}s]', *a, flush=True)
for i, c in enumerate(cells[:last + 1]):
    if not c.lstrip().startswith('# '): exec(compile(c, f'cell{i}', 'exec'), g)
log('setup done')
run, features, succ, REP, FAULTS, CFG, with_cfg, mkcfg, qnorm = g['run'], g['features'], g['succ'], g['REP'], g['FAULTS'], g['CFG'], g['with_cfg'], g['mkcfg'], g['qnorm']
_ok = [b['clean_tr']['ce'].max() for b in g['BASE'] if b['split'] == 'train' and b['h5'] and len(b['clean_tr']['ce'])]; g['CE_FLOOR'][0] = float(np.percentile(_ok, 10))   # frozen formula (as v13 Idea 2)
_R = pickle.load(open(os.path.join(outdir, 'checkpoint.pkl'), 'rb')); EP = _R['EPIS']; CLN = _R['CLEAN']; seed = int(cfg['SEED'])
from sklearn.ensemble import HistGradientBoostingClassifier
FE = sorted(EP[0]['feats']); mat = lambda fs: np.array([[fe[k] for k in FE] for fe in fs], np.float32)
hgb = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=seed)
ALPHA, CAP_FRAC, N_CAL_EXTRA = 0.005, 0.20, 2000
INF = float('inf'); rng = np.random.default_rng(7)

def wilson(k, n, z=1.96):
    if n == 0: return [float('nan')] * 2
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return [(c - h) / d, (c + h) / d]
def boot(d, n=2000):
    d = np.asarray(d, float)
    if len(d) == 0: return dict(mean=float('nan'), ci=[float('nan')] * 2)
    bs = d[rng.integers(0, len(d), (n, len(d)))].mean(1); return dict(mean=float(d.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])
def auc(y, s):
    from scipy.stats import rankdata
    y = np.asarray(y, int); s = np.asarray(s, float)
    if y.sum() == 0 or y.sum() == len(y): return float('nan')
    r = rankdata(s); p_ = y == 1; return float((r[p_].sum() - p_.sum() * (p_.sum() + 1) / 2) / (p_.sum() * (~p_).sum()))
def auc_ci(y, s, n=1000):
    y = np.asarray(y, int); s = np.asarray(s, float); a = auc(y, s); bs = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if 0 < y[i].sum() < len(i): bs.append(auc(y[i], s[i]))
    return dict(auroc=a, ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if bs else [float('nan')] * 2, n_pos=int(y.sum()), n_neg=int(len(y) - y.sum()))
def crc_lambda(s, l, alpha):
    n = len(s)
    if n == 0: return INF
    for lam in sorted(set(s.tolist())) + [INF]:
        if n / (n + 1) * np.mean((s >= lam) * l) + 1 / (n + 1) <= alpha: return lam
    return INF
def cap_lambda(s, frac):
    if len(s) == 0: return INF
    for lam in sorted(set(s.tolist())) + [INF]:
        if np.mean(s >= lam) <= frac: return lam
    return INF
def universal(st):
    """Diagnosis-free: every repair of the catalogue at once (query repairs, then every configuration repair, then the R19 depth repair)."""
    for f in ('Q01', 'Q03', 'Q04', 'Q05'): st = REP[f](st, None)
    st = with_cfg(st, refresh=True, dedup=True, quality=True, mask=None, enc='v2', q_noise=0.0, ce='ok', shift=None, sparse_shift=0, ef=CFG['EF_CLEAN'], fusion='minmax',
                  result_cap=None, ce_trunc=None, nonfinite=None)
    return REP['R19'](st, None)
def qpp(tr):
    s_ = np.sort(np.asarray(tr['ssc'], float))[::-1][:100]; ql = max(1, len(tr['q'].split())); mu = max(float(s_.mean()) if len(s_) else 0.0, 1e-6)
    return dict(nqc=float(np.std(s_) / mu) if len(s_) else 0.0, wig=float(np.mean(s_[:5] - mu) / math.sqrt(ql)) if len(s_) else 0.0, ce1=float(np.max(tr['ce'])) if len(tr['ce']) else 0.0)

R = dict(trial=TRIAL, dataset=ds, seed=seed, code_sha256=prot['code_sha256'], alpha=ALPHA, cap_frac=CAP_FRAC)
# replay check (as v13 Idea 2)
cl = [e for e in EP if e['split'] == 'test' and e['fault'] == 'NONE' and e['bid'] in CLN][:200]; mism = sum(bool(succ(run(e['st']), e['st']['gold'])) != bool(CLN[e['bid']]['h5']) for e in cl)
R['replay_check'] = dict(mismatches=mism, n=len(cl)); log('replay check', mism, 'of', len(cl)); assert mism <= 0.005 * len(cl), 'replay not trusted'

calb = lambda bid: int(hashlib.md5(('cal|' + bid).encode()).hexdigest()[:8], 16) / 2**32 < 0.5
TR = [e for e in EP if e['split'] == 'train']; TE = [e for e in EP if e['split'] == 'test']
TRA = [e for e in TR if not (e['fault'] == 'NONE' and calb(e['bid']))]; CALE = [e for e in TR if e['fault'] == 'NONE' and calb(e['bid'])]
ATT = hgb().fit(mat([e['feats'] for e in TRA]), np.array([e['fault'] for e in TRA])); CLS = list(ATT.classes_); iN = CLS.index('NONE')
def dispatch(fe):
    p = ATT.predict_proba(mat([fe]))[0]; j = max((j for j, c in enumerate(CLS) if c != 'NONE'), key=lambda j: p[j]); return CLS[j], float(1 - p[iN])
strat = lambda fe: 'rare' if fe['q_lowdf'] > 0 else 'common'
STRATA = ['common', 'rare']
log('attributor fitted on', len(TRA), 'episodes; calibration clean train', len(CALE))

# ---- calibration: clean train half + extra clean queries outside the run's sample (A1)
sample = {qid for (_, qid) in g['QRELS']}
extra = [q for q in sorted(g['_qr'], key=lambda x: hashlib.md5(x.encode()).hexdigest()) if q not in sample and q in g['QUERIES']][:N_CAL_EXTRA]
if TRIAL: CALE, extra = CALE[:15], extra[:15]
cal = []; fC = open(os.path.join(outd, 'calibration.jsonl'), 'w')
for n_, item in enumerate([('ep', e) for e in CALE] + [('extra', q) for q in extra]):
    if item[0] == 'ep': e = item[1]; st = dict(e['st']); h5 = bool(e['clean_h5']); fe = e['feats']; tr0 = run(st)
    else:
        q = item[1]; st = dict(q=qnorm(g['QUERIES'][q]), cfg=mkcfg(), ov=None, gold=g['_qr'][q], k=5); tr0 = run(st); h5 = bool(succ(tr0, st['gold'])); fe = features(tr0)
    top, s = dispatch(fe); tr1 = run(REP[top](st, tr0)); l_rep = int(h5 and not succ(tr1, st['gold']))
    r = dict(src=item[0], s=s, l_rep=l_rep, strat=strat(fe), h5=h5, top=top); cal.append(r); fC.write(json.dumps(r) + '\n')
    if n_ % 250 == 0: log('calibration', n_)
sa = lambda sn: np.array([r['s'] for r in cal if sn is None or r['strat'] == sn]); la = lambda sn: np.array([r['l_rep'] for r in cal if sn is None or r['strat'] == sn])
LAM = {sn: crc_lambda(sa(sn), la(sn), ALPHA) for sn in STRATA}; LAM_CAP = {sn: max(LAM[sn], cap_lambda(sa(sn), CAP_FRAC)) for sn in STRATA}
LAM_G = crc_lambda(sa(None), la(None), ALPHA); TAU5 = float(np.quantile(sa(None), 0.95)) if len(cal) else INF
R['calibration'] = dict(n={sn: int(len(sa(sn))) for sn in STRATA}, n_from_run=len(CALE), n_extra=len(extra), losses_if_all_dispatched={sn: int(la(sn).sum()) for sn in STRATA},
                        lambdas=dict(mondrian=LAM, capped=LAM_CAP, global_=LAM_G, tau_5pct_fpr=TAU5))
log('calibration', R['calibration'])

# ---- held-out test split: clean and faulted episodes
DET = {r['fault']: float(r['auroc']) for r in csv.DictReader(open(os.path.join(outdir, 'port_detector_gates.csv'))) if r.get('auroc') not in (None, '', 'nan')}
NONCEIL = sorted(f for f, a in DET.items() if a < 0.995); R['non_ceiling_faults'] = NONCEIL
tests = [e for e in TE if e['fault'] == 'NONE'] + [e for e in TE if e['fault'] != 'NONE']
if TRIAL: tests = [e for e in TE if e['fault'] == 'NONE'][:20] + [e for e in TE if e['fault'] != 'NONE'][:20]
rows = []; fT = open(os.path.join(outd, 'test.jsonl'), 'w'); tim = dict(clean=[], rep=[], univ=[])
for n_, e in enumerate(tests):
    st = e['st']; gold = st['gold']; fe = e['feats']; a_ = time.perf_counter(); tr0 = run(st); tim['clean'].append(time.perf_counter() - a_)
    top, s = dispatch(fe); a_ = time.perf_counter(); tr1 = run(REP[top](st, tr0)); tim['rep'].append(time.perf_counter() - a_)
    a_ = time.perf_counter(); tru = run(universal(st)); tim['univ'].append(time.perf_counter() - a_)
    x = dict(fault=e['fault'], strat=strat(fe), s=s, top=top, ok_rep=bool(succ(tr1, gold)), ok_univ=bool(succ(tru, gold)), h5=bool(succ(tr0, gold)))
    if e['fault'] == 'NONE' and not x['h5']:   # E4b: a real failure; run every repair of the catalogue
        outc = {f: bool(succ(run(REP[f](st, tr0)), gold)) for f in FAULTS}; outc['UNIV'] = x['ok_univ']
        x['fixers'] = [k for k, v in outc.items() if v]; x['random_success'] = float(np.mean(list(outc.values())))
    if e['fault'] == 'NONE': x.update(qpp(tr0)); x['s_att'] = s
    rows.append(x); fT.write(json.dumps(x) + '\n'); fT.flush()
    if n_ % 250 == 0: log('test', n_, 'of', len(tests))
med = {k: float(np.median(v)) if v else None for k, v in tim.items()}
def evalpol(name):
    per, clean = {}, []
    for x in rows:
        if name == 'universal': d, ok, cost = True, x['ok_univ'], len(FAULTS)
        elif name == 'none': d, ok, cost = False, (x['h5'] if x['fault'] == 'NONE' else False), 0
        else:
            lam = {'mondrian_crc_0.005': LAM, 'capped_crc_0.005': LAM_CAP}.get(name)
            th = lam[x['strat']] if lam else (LAM_G if name == 'global_crc_0.005' else TAU5)
            d = x['s'] >= th; ok = x['ok_rep'] if d else (x['h5'] if x['fault'] == 'NONE' else False); cost = 1 if d else 0
        if x['fault'] == 'NONE': clean.append((x['h5'] and not ok, d, cost))
        else: per.setdefault(x['fault'], []).append(ok)
    nl, n = sum(c[0] for c in clean), len(clean); pc = {f: float(np.mean(v)) for f, v in per.items()}
    sec = med['clean'] + (med['univ'] if name == 'universal' else med['rep'] * float(np.mean([c[1] for c in clean])) if clean and name != 'none' else 0.0)
    return dict(clean_loss=nl / max(1, n), clean_loss_wilson=wilson(nl, n), clean_n=n, clean_dispatch=float(np.mean([c[1] for c in clean])) if clean else None,
                repairs_per_clean_query=float(np.mean([c[2] for c in clean])) if clean else None, est_median_seconds_per_clean_query=sec,
                mean_closure=float(np.mean(list(pc.values()))) if pc else None, closure_non_ceiling=float(np.mean([pc[f] for f in NONCEIL if f in pc])) if any(f in pc for f in NONCEIL) else None,
                per_fault=pc)
POL = {p: evalpol(p) for p in ('none', 'tau_5pct_fpr', 'global_crc_0.005', 'mondrian_crc_0.005', 'capped_crc_0.005', 'universal')}
fx = [x for x in rows if x['fault'] != 'NONE']
R['identification_top1_on_faulted'] = float(np.mean([x['top'] == x['fault'] for x in fx])) if fx else None
R['median_seconds'] = dict(clean_run=med['clean'], dispatched_repair_and_run=med['rep'], universal_and_run=med['univ'])
R['policies'] = POL
R['pass'] = dict(mondrian_loss_ok=bool(POL['mondrian_crc_0.005']['clean_loss'] <= ALPHA), capped_loss_ok=bool(POL['capped_crc_0.005']['clean_loss'] <= ALPHA),
                 capped_closure_ok=bool((POL['capped_crc_0.005']['mean_closure'] or 0) >= 0.70))
R['pass']['E4_PASS'] = bool(all(R['pass'].values()))
log('policies', {k: {kk: vv for kk, vv in v.items() if kk != 'per_fault'} for k, v in POL.items()}, R['pass'])

# ---- E4b: real failures (clean test queries that miss the gold), labelled by intervention
F = [x for x in rows if x['fault'] == 'NONE' and not x['h5']]; RF = [x for x in F if x['fixers']]; UF = [x for x in F if not x['fixers']]; S = [x for x in rows if x['fault'] == 'NONE' and x['h5']]
lab = {}
for x in RF:
    for l in x['fixers']: lab[l] = lab.get(l, 0) + 1
def det(pos):
    return {nm: auc_ci([1] * len(pos) + [0] * len(S), [sg * x[k] for x in pos + S]) for nm, k, sg in [('attributor', 's_att', 1), ('qpp_neg_nqc', 'nqc', -1), ('qpp_neg_wig', 'wig', -1), ('neg_top_ce', 'ce1', -1)]}
loop_ok = lambda x: bool(x['s'] >= LAM[x['strat']] and x['ok_rep'])
E4b = dict(real_failures=len(F), repairable=len(RF), coverage=len(RF) / max(1, len(F)), unrepairable=len(UF), label_counts=dict(sorted(lab.items(), key=lambda kv: -kv[1])),
           success_on_repairable=dict(loop_mondrian=float(np.mean([loop_ok(x) for x in RF])) if RF else None, universal=float(np.mean([x['ok_univ'] for x in RF])) if RF else None,
                                      random_catalogue_repair=float(np.mean([x['random_success'] for x in RF])) if RF else None, oracle=1.0 if RF else None,
                                      loop_minus_random=boot([loop_ok(x) - x['random_success'] for x in RF]), loop_minus_universal=boot([loop_ok(x) - x['ok_univ'] for x in RF])),
           detection_repairable_vs_success=det(RF), detection_unrepairable_vs_success=det(UF), detection_all_failures_vs_success=det(F),
           harm_on_real_successes=dict(n=len(S), mondrian_broken=int(sum(x['s'] >= LAM[x['strat']] and not x['ok_rep'] for x in S)),
                                       capped_broken=int(sum(x['s'] >= LAM_CAP[x['strat']] and not x['ok_rep'] for x in S)), universal_broken=int(sum(not x['ok_univ'] for x in S))))
h = E4b['harm_on_real_successes']; h['mondrian_rate'] = h['mondrian_broken'] / max(1, h['n']); h['mondrian_wilson'] = wilson(h['mondrian_broken'], h['n']); h['universal_rate'] = h['universal_broken'] / max(1, h['n'])
E4b['claims'] = dict(detects_repairable_real_failures=bool(RF and E4b['detection_repairable_vs_success']['attributor']['auroc'] >= 0.70),
                     diagnosis_beats_chance=bool(RF and E4b['success_on_repairable']['loop_minus_random']['ci'][0] > 0), no_harm_on_real_traffic=bool(S and h['mondrian_rate'] <= 0.005))
R['E4b'] = E4b; log('E4b', {k: v for k, v in E4b.items() if k != 'label_counts'})
json.dump(R, open(os.path.join(outd, 'RESULT.json'), 'w'), indent=1, default=str); log('done')
