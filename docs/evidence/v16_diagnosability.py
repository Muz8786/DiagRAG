"""v16 diagnosability (docs/evidence/v16_diagnosability_protocol.md). Executed INSIDE the Kaggle notebook after the frozen v6 code has run up to its
U1 stage on a resumed judged checkpoint; `G` is that namespace. Rebuilds the v15 self-test pool, dictionary and battery with the same random tags and
code (checked against EXPECT, the stored v15 battery), records probe outcomes and stage traces of the same evaluated fault instances, and decodes from
probe subsets. ROLE = 'dev' (seed 55, v15 'deveval' draws) or 'heldout' (v15 'heldout' draws). Measurements only."""
import collections, itertools, json, math, os, random, time
import numpy as np

SYS = ['R01', 'R03', 'R05', 'R06', 'R07', 'R10', 'R11', 'R13', 'R15', 'R19', 'R22', 'R23', 'R24', 'R25', 'K04']
KNOBS = dict(R01={'mask'}, R03={'enc'}, R05={'ce'}, R06={'route'}, R07={'shift'}, R10={'q_noise'}, R11={'enc'}, R13={'sparse_shift'}, R15={'nprobe'},
             R19={'depth'}, R22={'fusion'}, R23={'result_cap'}, R24={'ce_trunc'}, R25={'nonfinite'}, K04={'emb_override'})
RANDOM_FAULTS = {'R01', 'R07', 'R25', 'K04', 'R13', 'R06'}
P = dict(POOL=600, A=100, B=40, NDICT=2, NDICT_RANDOM=4, T=3, EPS=0.002, KAPPA=3.0)   # v15 values (A1)
D = dict(MS=[1, 2, 3, 5, 10, 20, 40, 60, 100], REPS=40, CLIP=0.01)
STG = ['D', 'S', 'F', 'O', 'V']


def main(G, OUT, TRIAL, ROLE, EXPECT):
    os.makedirs(OUT, exist_ok=True); t0 = time.time(); log = lambda *a: print(f'[{time.time() - t0:6.0f}s]', *a, flush=True)
    run, succ, mkcfg, N, E, BASE, FAMILY, GROUP = G['run'], G['succ'], G['mkcfg'], G['N'], G['E'], G['BASE'], G['FAMILY'], G['GROUP']
    ESCI_PART, PARTS, CFG = G['ESCI_PART'], G['PARTS'], G['CFG']
    rnd = lambda *tag: random.Random('|'.join(map(str, tag)))
    R = dict(trial=bool(TRIAL), role=ROLE, seed=str(CFG['SEED']), P=dict(P), D=dict(D))

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
    trace = lambda b, over: run(dict(q=b['q'], tenant=b['tenant'], cfg=mkcfg(**over), ov=None, gold=b['gold'], k=5, meta={}))
    def sig(tr):
        out = {}
        for key, fn in (('D', lambda t: t['dtop'][:20]), ('S', lambda t: t['stop'][:20]), ('F', lambda t: t['fused'][:CFG['DEPTH']]),
                        ('O', lambda t: t['order'][:10]), ('V', lambda t: t['final'])):
            try: out[key] = tuple(int(i) for i in fn(tr))
            except Exception: out[key] = None
        return out

    esci_tr = [b for b in BASE if b['src'] == 'esci' and b['split'] == 'train' and b['h5']]
    pool = rnd('pool').sample(esci_tr, min(len(esci_tr), P['POOL']))
    pool = [b for b in pool if bool(succ(trace(b, {}), b['gold'], 5))]
    if TRIAL: pool = pool[:60]
    REF = [sig(trace(b, {})) for b in pool]
    log('pool', len(pool))
    def observe(over, idx):
        y, st = [], []
        for i in idx:
            b = pool[i]; tr = trace(b, over); y.append(not bool(succ(tr, b['gold'], 5))); s_ = sig(tr); st.append([s_[k] != REF[i][k] for k in STG])
        return np.array(y, bool), np.array(st, bool)
    # ---- dictionary (v15 'dict' draws) on the whole pool, with stage traces
    DI = {f: [sys_cfg(f, rnd('dict', f, j)) for j in range(P['NDICT_RANDOM'] if f in RANDOM_FAULTS else P['NDICT'])] for f in SYS}
    allidx = list(range(len(pool))); Q, QS = {}, {}
    for f in SYS:
        obs = [observe(over, allidx) for over in DI[f]]
        Q[f] = np.mean([o[0] for o in obs], axis=0); QS[f] = np.mean([o[1] for o in obs], axis=0)
    log('dictionary', {f: round(float(Q[f].mean()), 3) for f in SYS})
    # ---- battery, identical to v15
    idx = list(range(len(pool))); A_idx = sorted(rnd('batteryA').sample(idx, min(P['A'], len(idx)))); rest = [i for i in idx if i not in set(A_idx)]
    det = {f: sum(Q[f][i] >= 0.5 for i in A_idx) for f in SYS}; pairs_all = list(itertools.combinations(SYS, 2))
    sep = {pg: sum(abs(Q[pg[0]][i] - Q[pg[1]][i]) >= 0.5 for i in A_idx) for pg in pairs_all}
    def gain(i): return (sum(max(0, P['T'] - det[f]) for f in SYS if Q[f][i] >= 0.5)
                         + sum(max(0, P['T'] - sep[pg]) for pg in pairs_all if abs(Q[pg[0]][i] - Q[pg[1]][i]) >= 0.5))
    B_idx = []
    for _ in range(P['B']):
        if not rest: break
        bi = max(rest, key=gain)
        if gain(bi) == 0: break
        B_idx.append(bi); rest.remove(bi)
        for f in SYS: det[f] += Q[f][bi] >= 0.5
        for pg in pairs_all: sep[pg] += abs(Q[pg[0]][bi] - Q[pg[1]][bi]) >= 0.5
    BAT = A_idx + B_idx; nA = len(A_idx)
    bat = dict(size=len(BAT), random_part=len(A_idx), diagnostic_part=len(B_idx), undetected_faults=[f for f in SYS if det[f] == 0])
    R['battery'] = bat; R['battery_matches_v15'] = bool(all(bat[k] == EXPECT.get(k) for k in ('size', 'random_part', 'diagnostic_part', 'undetected_faults')))
    log('battery', bat, 'matches v15:', R['battery_matches_v15'], EXPECT)
    # ---- noisy-OR likelihood tables over all hypotheses
    HYP = [()] + [(f,) for f in SYS] + list(itertools.combinations(SYS, 2)); pen = np.array([P['KAPPA'] * len(h) for h in HYP])
    QB = {f: np.clip(Q[f][BAT], D['CLIP'], 1 - D['CLIP']) for f in SYS}; QSB = {f: np.clip(QS[f][BAT], D['CLIP'], 1 - D['CLIP']) for f in SYS}
    def tables(Qd, shape):
        p = []
        for h in HYP:
            k = np.full(shape, 1 - P['EPS'])
            for f in h: k = k * (1 - Qd[f])
            p.append(1 - k)
        p = np.array(p); return np.log(p), np.log(1 - p), p
    L1, L0, PP = tables(QB, (len(BAT),)); M1, M0, PS = tables(QSB, (len(BAT), len(STG)))
    fams = [frozenset(FAMILY[f] for f in h) for h in HYP]
    def decode(y, S, ch):
        ys = y[S].astype(float)
        if ch == 'pf': ll = (L1[:, S] * ys + L0[:, S] * (1 - ys)).sum(1)
        else: ll = (M1[:, S, :] * ys + M0[:, S, :] * (1 - ys)).sum((1, 2))
        ll = ll - pen
        if y[S].any(): ll[0] = -np.inf
        return int(np.argmax(ll)), ll
    def kl(p, q): return float(np.sum(p * np.log(p / q) + (1 - p) * np.log((1 - p) / (1 - q))))
    def separability(T, ch):
        ti = HYP.index(tuple(T)) if tuple(T) in HYP else HYP.index(tuple(sorted(T, key=SYS.index)))
        need = frozenset(FAMILY[f] for f in T); pT = PP[ti] if ch == 'pf' else PS[ti]
        best = min((kl(pT, PP[j] if ch == 'pf' else PS[j]), HYP[j]) for j in range(len(HYP)) if not need <= fams[j])
        return dict(D=best[0], per_probe=best[0] / len(BAT), nearest=list(best[1]))
    rng = np.random.default_rng(7); SUB = {m: [np.sort(rng.choice(nA, min(m, nA), replace=False)) for _ in range(D['REPS'])] for m in D['MS'] if m <= nA}
    full = np.arange(len(BAT))
    def evaluate(T, y, st):
        need = frozenset(FAMILY[f] for f in T); out = dict(any_fail=bool(y.any()), any_stage_change=bool(st.any()))
        for ch, obs in (('pf', y), ('st', st)):
            acc = {}
            for m, subs in SUB.items(): acc[m] = float(np.mean([need <= fams[decode(obs, S, ch)[0]] for S in subs]))
            j, ll = decode(obs, full, ch); acc['all'] = bool(need <= fams[j])
            good = max(ll[k] for k in range(len(HYP)) if need <= fams[k]); bad = max(ll[k] for k in range(len(HYP)) if not need <= fams[k])
            out[ch] = dict(acc=acc, decoded=list(HYP[j]), margin=float(good - bad), **separability(T, ch))
        return out
    # ---- evaluated instances (v15 draws)
    tagE = 'deveval' if ROLE == 'dev' else 'heldout'
    rowsS, rowsP = [], []; fS = open(os.path.join(OUT, 'D_single.jsonl'), 'w'); fP = open(os.path.join(OUT, 'D_pairs.jsonl'), 'w')
    for f in (SYS[:3] if TRIAL else SYS):
        for j in range(1 if TRIAL else 3):
            y, st = observe(sys_cfg(f, rnd(tagE, f, j)), BAT); r = dict(fault=f, inst=j, **evaluate((f,), y, st)); rowsS.append(r); fS.write(json.dumps(r) + '\n'); fS.flush()
    log('singles done', len(rowsS))
    prs = [pg for pg in pairs_all if not (KNOBS[pg[0]] & KNOBS[pg[1]])]
    if TRIAL: prs = prs[:4]
    for (f, g) in prs:
        over = dict(sys_cfg(f, rnd(tagE + 'pair', f, g, 0)), **sys_cfg(g, rnd(tagE + 'pair', f, g, 1)))
        y, st = observe(over, BAT); r = dict(pair=[f, g], same_group=GROUP[f] == GROUP[g], **evaluate((f, g), y, st)); rowsP.append(r); fP.write(json.dumps(r) + '\n'); fP.flush()
    log('pairs done', len(rowsP))
    curve = lambda rows, ch: {str(m): float(np.mean([r[ch]['acc'][m] for r in rows])) for m in list(SUB) + ['all']}
    sg = [r for r in rowsP if r['same_group']]
    R['curves'] = dict(singles=dict(pf=curve(rowsS, 'pf'), st=curve(rowsS, 'st')), pairs=dict(pf=curve(rowsP, 'pf'), st=curve(rowsP, 'st')),
                       pairs_same_group=dict(pf=curve(sg, 'pf'), st=curve(sg, 'st')))
    R['n'] = dict(singles=len(rowsS), pairs=len(rowsP), same_group=len(sg))
    log('curves', R['curves'])
    json.dump(R, open(os.path.join(OUT, 'RESULT.json'), 'w'), indent=1, default=str); print(json.dumps(R, indent=1, default=str)[:8000])
