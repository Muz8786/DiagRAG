"""v19: unseen-fault closure (U1) of the two-channel system: per-query telemetry loop + diagnostic self-test (docs/evidence/v19_two_channel_u1_protocol.md).
Executed INSIDE the Kaggle notebook after the frozen v6 code has run up to its U1 stage on a resumed judged checkpoint; `G` is that namespace.
For each of the 25 leave-one-fault-out (LOFO) faults and each of its held-out episodes: if the fault is a system fault, the self-test (v15 algorithm,
dictionary WITHOUT the fault, random probes only) runs on the faulted system; if it detects a fault, its verified repair is applied to the episode;
otherwise the stored per-query LOFO outcome stands. Non-system faults keep the stored per-query outcome. Measurements only; nothing frozen changes."""
import hashlib, itertools, json, os, random, time
import numpy as np

SYS = ['R01', 'R03', 'R05', 'R06', 'R07', 'R10', 'R11', 'R13', 'R15', 'R19', 'R22', 'R23', 'R24', 'R25', 'K04']   # v15 system faults (dictionary)
RANDOM_FAULTS = {'R01', 'R07', 'R25', 'K04', 'R13', 'R06'}
P = dict(POOL=600, A=100, B=40, NDICT=2, NDICT_RANDOM=4, T=3, EPS=0.002)   # v15 A1 values


def main(G, OUT, TRIAL):
    os.makedirs(OUT, exist_ok=True); t0 = time.time(); log = lambda *a: print(f'[{time.time() - t0:6.0f}s]', *a, flush=True)
    run, succ, mkcfg, N, E, BASE, REP, GROUP, GROUP_REPAIR, DEFAULT = G['run'], G['succ'], G['mkcfg'], G['N'], G['E'], G['BASE'], G['REP'], G['GROUP'], G['GROUP_REPAIR'], G['DEFAULT']
    ESCI_PART, PARTS, CFG, EPIS, LOFO, SINGLE, RULE_PRIO = G['ESCI_PART'], G['PARTS'], G['CFG'], G['EPIS'], G['LOFO'], G['SINGLE'], G['RULE_PRIO']
    rnd = lambda *tag: random.Random('|'.join(map(str, tag)))
    def sys_cfg(f, r):   # identical to v15
        if f == 'R01': return dict(mask=(0.3, r.randrange(10**6), ()))
        if f == 'R03': return dict(enc='v15_trunc')
        if f == 'R05': return dict(ce='random')
        if f == 'R06': return dict(route=[r.choice([p for p in range(len(PARTS)) if p != ESCI_PART])])
        if f == 'R07': a = r.randrange(0, N - 20004); return dict(shift=(a, a + 20000, r.choice([1, 2, 3])))
        if f == 'R10': return dict(q_noise=r.uniform(2.0, 3.5))
        if f == 'R11': return dict(enc=r.choice(['v1', 'swap']))
        if f == 'R13': return dict(sparse_shift=r.randint(1, 5000))
        if f == 'R15': return dict(nprobe=1)
        if f == 'R19': return dict(depth=5)
        if f == 'R22': return dict(fusion='raw')
        if f == 'R23': return dict(result_cap=r.choice([1, 2]))
        if f == 'R24': return dict(ce_trunc=24)
        if f == 'R25': return dict(nonfinite=('top', tuple(r.sample(range(N), 40))))
        if f == 'K04': return dict(emb_override={i: E[r.randrange(N)] for i in r.sample(range(N), int(0.05 * N))})
    def apply_reps(st, reps):
        for g in sorted(reps, key=lambda g: 'QKR'.index('R' if g == 'GR' else GROUP[g])):
            st = (GROUP_REPAIR['R'] if g == 'GR' else REP[g])(st, run(st))
        return st
    st_of = lambda b, over, reps=(): apply_reps(dict(q=b['q'], tenant=b['tenant'], cfg=mkcfg(**over), ov=None, gold=b['gold'], k=5, meta={}), reps)
    ok = lambda b, over, reps=(): bool(succ(run(st_of(b, over, reps)), b['gold'], 5))
    esci_tr = [b for b in BASE if b['src'] == 'esci' and b['split'] == 'train' and b['h5']]
    pool = [b for b in rnd('pool').sample(esci_tr, min(len(esci_tr), P['POOL'])) if ok(b, {})]
    if TRIAL: pool = pool[:60]
    DI = {f: [sys_cfg(f, rnd('dict', f, j)) for j in range(P['NDICT_RANDOM'] if f in RANDOM_FAULTS else P['NDICT'])] for f in SYS}
    Q = {f: np.mean([[not ok(b, over) for b in pool] for over in DI[f]], axis=0) for f in SYS}
    idx = list(range(len(pool))); A_idx = sorted(rnd('batteryA').sample(idx, min(P['A'], len(idx))))
    probes = [pool[i] for i in A_idx]; QB = {f: np.clip(Q[f][A_idx], 0.01, 0.99) for f in SYS}; pos = list(range(len(A_idx)))
    log('pool', len(pool), 'random probes', len(probes))
    def post_rank(y, faults):
        y = np.asarray(y, bool)
        def ll(f):
            pf = 1 - (1 - P['EPS']) * (1 - QB[f]); return float(np.sum(np.where(y, np.log(pf), np.log(1 - pf))))
        return sorted(faults, key=ll, reverse=True)
    def selftest(over, faults, K=6, max_rounds=4):   # v15 A1 algorithm
        y = [not ok(b, over) for b in probes]; detected = any(y); named, rounds = [], 0
        while any(y) and rounds < max_rounds:
            rounds += 1; fail_i = [i for i, v in enumerate(y) if v]; top = post_rank(y, [f for f in faults if f not in named])[:K]
            fixes = lambda H: sum(ok(probes[i], over, named + list(H)) for i in fail_i)
            best, gn = None, 0
            for f in top:
                g_ = fixes((f,))
                if g_ > gn: best, gn = (f,), g_
            if best is None:
                for H in itertools.combinations(top, 2):
                    g_ = fixes(H)
                    if g_ > gn: best, gn = H, g_
            if best is None: break
            y2 = [not ok(b, over, named + list(best)) for b in probes]
            if sum(y2) >= sum(y): break
            named, y = named + list(best), y2
        if not any(y): return dict(named=named, fallback=False, detected=detected, verified=True)
        y = [not ok(b, over, named + ['GR']) for b in probes]
        return dict(named=named, fallback=True, detected=detected, verified=not any(y))
    R = dict(trial=bool(TRIAL), seed=str(CFG['SEED']))
    R['clean_false_alarm'] = selftest({}, SYS)['detected']; log('clean system: self-test detects a fault?', R['clean_false_alarm'])
    faults = [f for f in SINGLE if f not in RULE_PRIO and LOFO.get(f)]
    cache = {}; rows = []; fh = open(os.path.join(OUT, 'U1_two_channel.jsonl'), 'w')
    for f in faults:
        es = [x for x in EPIS if x['fault'] == f and x['split'] == 'test']; stored = LOFO[f]
        if TRIAL: es, stored = es[:3], stored[:3]
        for e, srow in zip(es, stored):
            p0 = bool(srow['ok']); r = dict(fault=f, system=f in SYS, P0=p0)
            if f in SYS:
                over = {k: v for k, v in e['st']['cfg'].items() if v != DEFAULT[k]}
                key = hashlib.md5(repr(sorted((k, repr(v)) for k, v in over.items())).encode()).hexdigest()
                if key not in cache: cache[key] = selftest(over, [g for g in SYS if g != f])
                res = cache[key]; reps = list(res['named']) + (['GR'] if res['fallback'] else [])
                if res['detected']:
                    st = e['st']; ok_st = bool(succ(run(apply_reps(st, reps)), st['gold'], st['k']))
                    r.update(detected=True, named=res['named'], fallback=res['fallback'], verified=res['verified'], two=ok_st)
                else: r.update(detected=False, two=p0)
            else: r['two'] = p0
            rows.append(r); fh.write(json.dumps(r) + '\n'); fh.flush()
        xs = [r for r in rows if r['fault'] == f]; log(f, 'P0', round(np.mean([r['P0'] for r in xs]), 3), 'two-channel', round(np.mean([r['two'] for r in xs]), 3))
    pf = {f: dict(P0=float(np.mean([r['P0'] for r in rows if r['fault'] == f])), two=float(np.mean([r['two'] for r in rows if r['fault'] == f])), system=f in SYS,
                  detected=float(np.mean([r.get('detected', False) for r in rows if r['fault'] == f])) if f in SYS else None) for f in faults}
    d = np.array([pf[f]['two'] - pf[f]['P0'] for f in faults]); rng = np.random.default_rng(7); bs = d[rng.integers(0, len(d), (4000, len(d)))].mean(1)
    R['U1'] = dict(n_faults=len(faults), U1_per_query=float(np.mean([pf[f]['P0'] for f in faults])), U1_two_channel=float(np.mean([pf[f]['two'] for f in faults])),
                   diff=float(d.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                   system_faults=dict(n=sum(pf[f]['system'] for f in faults), per_query=float(np.mean([pf[f]['P0'] for f in faults if pf[f]['system']])),
                                      two=float(np.mean([pf[f]['two'] for f in faults if pf[f]['system']]))),
                   other_faults=dict(n=sum(not pf[f]['system'] for f in faults), per_query=float(np.mean([pf[f]['P0'] for f in faults if not pf[f]['system']]))),
                   per_fault=pf, selftests_run=len(cache))
    json.dump(R, open(os.path.join(OUT, 'RESULT.json'), 'w'), indent=1, default=str); log('U1', {k: v for k, v in R['U1'].items() if k != 'per_fault'})
