"""v17: the diagnostic self-test (v15 S, unchanged algorithm) on the SECOND retrieval stack, by replay of a judged port5 run.
Development on FiQA, confirmation on NQ (docs/evidence/v17_port_selftest_protocol.md). Probes: train clean successes; traffic: test queries.
Per-query baseline: the second stack's attributor at its 5% false-positive threshold, dispatching the repair of its top fault class.
usage: DATASET=<ds> python docs/evidence/v17_port_selftest.py <work_dir> <code_file> <out_dir> <ROLE> [TRIAL]"""
import glob, hashlib, itertools, json, math, os, pickle, random, re, sys, time
import numpy as np

work, code_file, outd, ROLE = sys.argv[1:5]; TRIAL = len(sys.argv) > 5 and sys.argv[5] == '1'; ds = os.environ['DATASET']; os.makedirs(outd, exist_ok=True)
outdir = glob.glob(os.path.join(work, f'port*_{ds}_out'))[0]; prot = json.load(open(os.path.join(outdir, 'PORT_PROTOCOL.json'))); cfg = prot['cfg']
src = open(code_file, encoding='utf-8').read(); assert hashlib.sha256(src.encode('utf-8')).hexdigest() == prot['code_sha256'], 'code file is not the code that produced this run'
os.environ.update(DIAGRAG_WORK=work, SEED=str(cfg['SEED']), N_QUERIES=str(cfg['N_QUERIES']), N_HARD=str(cfg['N_HARD']), MAX_ATT=str(cfg['MAX_ATT']), N_HARM=str(cfg['N_HARM']), TIME_BUDGET='0')
cells = re.split(r'\n# %%(?: \[markdown\])?\n', src); last = max(i for i, c in enumerate(cells) if 'REP = dict(' in c)
g = {'__name__': '__replay__', '__file__': os.path.join(work, os.path.basename(code_file))}; t0 = time.time()
log = lambda *a: print(f'[{time.time() - t0:6.0f}s]', *a, flush=True)
for i, c in enumerate(cells[:last + 1]):
    if not c.lstrip().startswith('# '): exec(compile(c, f'cell{i}', 'exec'), g)
log('setup done')
_ok = [b['clean_tr']['ce'].max() for b in g['BASE'] if b['split'] == 'train' and b['h5'] and len(b['clean_tr']['ce'])]; g['CE_FLOOR'][0] = float(np.percentile(_ok, 10))
run, succ, mkcfg, with_cfg, REP, features, CFG, N, E = g['run'], g['succ'], g['mkcfg'], g['with_cfg'], g['REP'], g['features'], g['CFG'], g['N'], g['E']
_R = pickle.load(open(os.path.join(outdir, 'checkpoint.pkl'), 'rb')); EP = _R['EPIS']; seed = int(cfg['SEED'])
from sklearn.ensemble import HistGradientBoostingClassifier
FE = sorted(EP[0]['feats']); mat = lambda fs: np.array([[fe[k] for k in FE] for fe in fs], np.float32)
calb = lambda bid: int(hashlib.md5(('cal|' + bid).encode()).hexdigest()[:8], 16) / 2**32 < 0.5
TR = [e for e in EP if e['split'] == 'train']; TRA = [e for e in TR if not (e['fault'] == 'NONE' and calb(e['bid']))]; CALE = [e for e in TR if e['fault'] == 'NONE' and calb(e['bid'])]
ATT = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced',
                                     random_state=seed).fit(mat([e['feats'] for e in TRA]), np.array([e['fault'] for e in TRA])); CLS = list(ATT.classes_); iN = CLS.index('NONE')
def proba(fe): return ATT.predict_proba(mat([fe]))[0]
TAU = float(np.quantile([1 - proba(e['feats'])[iN] for e in CALE], 0.95))

SYS = ['R01', 'R03', 'R05', 'R07', 'R10', 'R11', 'R13', 'R15', 'R19', 'R22', 'R23', 'R24', 'R25', 'K04']
KNOBS = dict(R01={'mask'}, R03={'enc'}, R05={'ce'}, R07={'shift'}, R10={'q_noise'}, R11={'enc'}, R13={'sparse_shift'}, R15={'ef'}, R19={'depth'}, R22={'fusion'},
             R23={'result_cap'}, R24={'ce_trunc'}, R25={'nonfinite'}, K04={'emb_override'})
RANDOM_FAULTS = {'R01', 'R07', 'R25', 'K04', 'R13'}
FAMILY = {f: f for f in SYS}; FAMILY.update(R03='ENC', R10='ENC', R11='ENC', K04='STALE', R07='STALE')
P = dict(POOL=300, A=80, B=20, NDICT=2, NDICT_RANDOM=3, T=3, EPS=0.002, KAPPA=3.0, NI=2, NPAIR=30, TRAFFIC=50, PAIR_TRAFFIC=25)
if TRIAL: P.update(POOL=40, A=10, B=4, NI=1, NPAIR=3, TRAFFIC=6, PAIR_TRAFFIC=4)
rnd = lambda *tag: random.Random('|'.join(map(str, tag)))
def sys_cfg(f, r):
    if f == 'R01': return dict(mask=(0.3, r.randrange(10**6), ()))
    if f == 'R03': return dict(enc='trunc')
    if f == 'R05': return dict(ce='random')
    if f == 'R07': L = int(0.2 * N); a = r.randrange(0, N - L - 4); return dict(shift=(a, a + L, r.choice([1, 2, 3])))
    if f == 'R10': return dict(q_noise=r.uniform(2.0, 3.5))
    if f == 'R11': return dict(enc='old')
    if f == 'R13': return dict(sparse_shift=r.randint(1, 3000))
    if f == 'R15': return dict(ef=r.choice([3, 5, 8]))
    if f == 'R19': return dict(depth=5)
    if f == 'R22': return dict(fusion='raw')
    if f == 'R23': return dict(result_cap=r.choice([1, 2]))
    if f == 'R24': return dict(ce_trunc=24)
    if f == 'R25': return dict(nonfinite=('top', tuple(r.sample(range(N), 40))))
    if f == 'K04': return dict(emb_override={i: E[r.randrange(N)] for i in r.sample(range(N), min(int(0.05 * N), 20000))})
def rollback(st): return dict(st, cfg=mkcfg(refresh=True))   # pinned configuration, dense view rebuilt from text
def st_of(b, over, reps=()):
    st = dict(q=b['q'], cfg=mkcfg(**over), ov=None, gold=b['gold'], k=5)
    for f in reps: st = rollback(st) if f == 'GR' else REP[f](st, run(st))
    return st
ok = lambda b, over, reps=(): bool(succ(run(st_of(b, over, reps)), b['gold']))
def universal(st):   # as v14 E4
    for f in ('Q01', 'Q03', 'Q04', 'Q05'): st = REP[f](st, None)
    st = with_cfg(st, refresh=True, dedup=True, quality=True, mask=None, enc='v2', q_noise=0.0, ce='ok', shift=None, sparse_shift=0, ef=CFG['EF_CLEAN'], fusion='minmax',
                  result_cap=None, ce_trunc=None, nonfinite=None)
    return REP['R19'](st, None)
B = g['BASE']; tr_ok = [b for b in B if b['split'] == 'train' and b['h5']]; te = [b for b in B if b['split'] == 'test']
pool = [b for b in rnd('pool').sample(tr_ok, min(len(tr_ok), P['POOL'])) if ok(b, {})]; traffic = rnd('traffic').sample(te, min(len(te), P['TRAFFIC']))
R = dict(trial=TRIAL, role=ROLE, dataset=ds, seed=seed, code_sha256=prot['code_sha256'], P=dict(P), TAU=TAU)
log('pool', len(pool), 'traffic', len(traffic), 'TAU', TAU)
DI = {f: [sys_cfg(f, rnd('dict', f, j)) for j in range(P['NDICT_RANDOM'] if f in RANDOM_FAULTS else P['NDICT'])] for f in SYS}
Q = {f: np.mean([[not ok(b, over) for b in pool] for over in DI[f]], axis=0) for f in SYS}
log('dictionary', {f: round(float(Q[f].mean()), 3) for f in SYS})
idx = list(range(len(pool))); A_idx = sorted(rnd('batteryA').sample(idx, min(P['A'], len(idx)))); rest = [i for i in idx if i not in set(A_idx)]
det = {f: sum(Q[f][i] >= 0.5 for i in A_idx) for f in SYS}; pairs_all = list(itertools.combinations(SYS, 2))
sep = {pg: sum(abs(Q[pg[0]][i] - Q[pg[1]][i]) >= 0.5 for i in A_idx) for pg in pairs_all}
def gain(i): return (sum(max(0, P['T'] - det[f]) for f in SYS if Q[f][i] >= 0.5) + sum(max(0, P['T'] - sep[pg]) for pg in pairs_all if abs(Q[pg[0]][i] - Q[pg[1]][i]) >= 0.5))
B_idx = []
for _ in range(P['B']):
    if not rest: break
    bi = max(rest, key=gain)
    if gain(bi) == 0: break
    B_idx.append(bi); rest.remove(bi)
    for f in SYS: det[f] += Q[f][bi] >= 0.5
    for pg in pairs_all: sep[pg] += abs(Q[pg[0]][bi] - Q[pg[1]][bi]) >= 0.5
BAT = A_idx + B_idx; probes = [pool[i] for i in BAT]; posAll = list(range(len(BAT))); QB = {f: np.clip(Q[f][BAT], 0.01, 0.99) for f in SYS}
R['battery'] = dict(size=len(BAT), random_part=len(A_idx), diagnostic_part=len(B_idx), undetected_faults=[f for f in SYS if det[f] == 0])
log('battery', R['battery'])
def post_rank(y, faults, pos):
    y = np.asarray(y, bool)
    def ll(f):
        pf = 1 - (1 - P['EPS']) * (1 - QB[f][pos]); return float(np.sum(np.where(y, np.log(pf), np.log(1 - pf))))
    return sorted(faults, key=ll, reverse=True)
def selftest(over, faults, pos, K=6, max_rounds=4):   # identical to v15 (A1)
    pr = [probes[k] for k in pos]; a = time.time(); nruns = len(pr)
    y = [not ok(b, over) for b in pr]; detected = any(y); named, rounds = [], 0
    while any(y) and rounds < max_rounds:
        rounds += 1; fail_i = [i for i, v in enumerate(y) if v]
        top = post_rank(y, [f for f in faults if f not in named], pos)[:K]
        fixes = lambda H: sum(ok(pr[i], over, named + list(H)) for i in fail_i)
        best, gn = None, 0
        for f in top:
            g_ = fixes((f,)); nruns += len(fail_i)
            if g_ > gn: best, gn = (f,), g_
        if best is None:
            for H in itertools.combinations(top, 2):
                g_ = fixes(H); nruns += len(fail_i)
                if g_ > gn: best, gn = H, g_
        if best is None: break
        y2 = [not ok(b, over, named + list(best)) for b in pr]; nruns += len(pr)
        if sum(y2) >= sum(y): break
        named, y = named + list(best), y2
    if not any(y): return dict(named=named, verified=True, fallback=False, detected=detected, rounds=rounds, runs=nruns, sec=time.time() - a)
    y = [not ok(b, over, named + ['GR']) for b in pr]; nruns += len(pr)
    return dict(named=named, verified=not any(y), fallback=True, detected=detected, rounds=rounds, runs=nruns, sec=time.time() - a)
fam = lambda l: FAMILY.get(l, l)
def traffic_eval(over, res, qs):
    reps_b = list(res['named']) + (['GR'] if res['fallback'] else []); rows = []
    for b in qs:
        stf = st_of(b, over); trf = run(stf); hf = bool(succ(trf, b['gold']))
        hb = ok(b, over, reps_b) if (reps_b and res['detected']) else hf
        p = proba(features(trf)); s = 1 - p[iN]; top = max((j for j, c in enumerate(CLS) if c != 'NONE'), key=lambda j: p[j])
        hl = bool(succ(run(REP[CLS[top]](stf, trf)), b['gold'])) if s >= TAU else hf
        hu = bool(succ(run(universal(stf)), b['gold']))
        rows.append(dict(h0=bool(b['h5']), hf=hf, hb=hb, hl=hl, hu=hu, lab=fam(CLS[top]) if s >= TAU else None))
    br = [r for r in rows if r['h0'] and not r['hf']]; it = [r for r in rows if r['h0'] and r['hf']]
    cl = lambda k: (float(np.mean([r[k] for r in br])) if br else None); hm = lambda k: (float(np.mean([not r[k] for r in it])) if it else None)
    labs = {}
    for r in rows:
        if r['lab']: labs[r['lab']] = labs.get(r['lab'], 0) + 1
    return dict(n=len(rows), broken=len(br), intact=len(it), closure=dict(selftest=cl('hb'), loop=cl('hl'), universal=cl('hu')),
                harm=dict(selftest=hm('hb'), loop=hm('hl'), universal=hm('hu')), top_families=[l for l, _ in sorted(labs.items(), key=lambda kv: -kv[1])[:2]])
broken_by = lambda over, qs: sum(bool(b['h5']) and not ok(b, over) for b in qs)
tagE = 'deveval' if ROLE == 'dev' else 'heldout'
rowsS, rowsP = [], []; fS = open(os.path.join(outd, 'S_single.jsonl'), 'w'); fP = open(os.path.join(outd, 'S_pairs.jsonl'), 'w')
for f in (SYS[:3] if TRIAL else SYS):
    for j in range(P['NI']):
        over = sys_cfg(f, rnd(tagE, f, j)); res = selftest(over, SYS, posAll); nb = broken_by(over, traffic)
        r = dict(fault=f, inst=j, harmful=nb > 0, traffic_broken=nb, detected=res['detected'], named=res['named'], exact=f in res['named'],
                 family=FAMILY[f] in {FAMILY[h] for h in res['named']}, verified=res['verified'], fallback=res['fallback'], rounds=res['rounds'], runs=res['runs'], sec=res['sec'])
        if j == 0: r['traffic'] = traffic_eval(over, res, traffic); r['agg_dispatcher_named'] = bool(r['traffic']['top_families'][:1] == [fam(f)])
        rowsS.append(r); fS.write(json.dumps(r) + '\n'); fS.flush()
    log('single', f, {k: rowsS[-1][k] for k in ('harmful', 'detected', 'named', 'verified')})
prs = sorted([pg for pg in pairs_all if not (KNOBS[pg[0]] & KNOBS[pg[1]])], key=lambda pg: hashlib.md5(('pair|' + '|'.join(pg)).encode()).hexdigest())[:P['NPAIR']]
for (f, h) in prs:
    of, oh = sys_cfg(f, rnd(tagE + 'pair', f, h, 0)), sys_cfg(h, rnd(tagE + 'pair', f, h, 1)); over = dict(of, **oh)
    eff = broken_by(of, traffic) > 0 and broken_by(oh, traffic) > 0
    res = selftest(over, SYS, posAll); tv = traffic_eval(over, res, traffic[:P['PAIR_TRAFFIC']])
    r = dict(pair=[f, h], effective=eff, same_group=f[0] == h[0], detected=res['detected'], named=res['named'], both_exact=f in res['named'] and h in res['named'],
             both_family={FAMILY[f], FAMILY[h]} <= {FAMILY[x] for x in res['named']}, verified=res['verified'], fallback=res['fallback'], runs=res['runs'],
             traffic=tv, agg_dispatcher_both=set(tv['top_families']) >= {fam(f), fam(h)})
    rowsP.append(r); fP.write(json.dumps(r) + '\n'); fP.flush()
    log('pair', f, h, {k: r[k] for k in ('effective', 'named', 'both_family', 'verified')})
m = lambda xs, k: (float(np.mean([bool(x[k]) for x in xs])) if xs else None)
HS = [r for r in rowsS if r['harmful']]; EPR = [r for r in rowsP if r['effective']]
R['summary'] = dict(singles=len(rowsS), harmful_singles=len(HS), detected=m(HS, 'detected'), family=m(HS, 'family'), verified=m(HS, 'verified'),
                    effective_pairs=len(EPR), pairs_both_family=m(EPR, 'both_family'), pairs_verified=m(EPR, 'verified'), agg_both=m(EPR, 'agg_dispatcher_both'))
json.dump(R, open(os.path.join(outd, 'RESULT.json'), 'w'), indent=1, default=str); log('summary', R['summary']); log('done')
