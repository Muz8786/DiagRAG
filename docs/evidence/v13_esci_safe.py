"""v13 K04-safe probing on ESCI (docs/evidence/v13_safe_protocol.md). Executed INSIDE the Kaggle notebook after the frozen v6 code has been run up to its U1 stage
on a resumed checkpoint (seed 52 = confirmation C1, seed 55 = reference R); `G` is that namespace. TRIAL=1 limits the work (numbers are not results).
Reports, for the same held-out leave-one-fault-out episodes: P0 (old method), P12 (the earlier probing rule), P-safe (old repair first; probe only flagged components; switch only to a healthy result)."""
import json, os, time
import numpy as np


def main(G, OUT, TRIAL):
    os.makedirs(OUT, exist_ok=True); t0 = time.time(); log = lambda *a: print(f'[{time.time() - t0:6.0f}s]', *a, flush=True)
    EPIS, FEATS, CFG = G['EPIS'], G['FEATS'], G['CFG']; run, succ, features, apply_v3, fam_repair = G['run'], G['succ'], G['features'], G['apply_v3'], G['fam_repair']
    INV = {'QUERY': [('q_oov', '+'), ('q_oov_long', '+'), ('q_correctable', '+'), ('q_segmentable', '+'), ('q_prefix', '+'), ('q_filler', '+'), ('q_conj', '+'), ('q_code_oov', '+'), ('q_synlow', '+')],
           'ENCODER': [('q_probe_cos', '-'), ('d_null10', '+')], 'ANN': [('ann_probe', '-')],
           'VECTORS': [('align_probe', '-'), ('stale_sparse20', '+'), ('stale_min', '-'), ('nonfinite', '+'), ('cov', '-'), ('sparse_absent_dense', '+')],
           'BM25': [('s_lex5', '-')], 'RERANK': [('ce_rrf_rho', '-'), ('ce_dense_rho', '-'), ('n_depth', '-')], 'FUSION': [('dep_dense', '-')],
           'SERVING': [('n_final', '-'), ('deleted5', '+')], 'FILTERS': [('tenant_mis5', '+'), ('expired5', '+'), ('filter_survival', '-'), ('part_top', '2')],
           'CONTENT': [('dup5', '+'), ('red_cos5', '+'), ('thin5', '+'), ('unver5', '+'), ('ident5', '+'), ('chunk_crowd5', '+')]}
    COMP = {**{f: 'QUERY' for f in 'Q01 Q02 Q03 Q04 Q05 Q07 Q09'.split()}, **{f: 'CONTENT' for f in 'K03 K05 K06 K08 K12'.split()}, **{f: 'VECTORS' for f in 'K04 R01 R07 R25'.split()},
            **{f: 'FILTERS' for f in 'K07 K09 R06 R26'.split()}, **{f: 'SERVING' for f in 'K11 R23'.split()}, **{f: 'ENCODER' for f in 'R03 R10 R11'.split()},
            **{f: 'RERANK' for f in 'R05 R19 R24'.split()}, 'R13': 'BM25', 'R15': 'ANN', 'R22': 'FUSION'}
    LIB = [c for c in sorted(COMP) if c in G['SINGLE']]
    LIST = [(c, f, d) for c, v in INV.items() for f, d in v]; THR = 0.05 / len(LIST)
    CAL = {f: np.array([e['feats'][f] for e in EPIS if e['split'] == 'train' and e['fault'] == 'NONE'], float) for _, f, _ in LIST}
    def flagged(fe):
        S = set()
        for c, f, d in LIST:
            x = float(fe[f]); v = CAL[f]; n = len(v); hi_, lo_ = (1 + (v >= x).sum()) / (n + 1), (1 + (v <= x).sum()) / (n + 1)
            p = hi_ if d == '+' else lo_ if d == '-' else min(1.0, 2 * min(hi_, lo_))
            if p <= THR: S.add(c)
        return S
    vec = lambda fe: np.array([[fe[k] for k in FEATS]], dtype=np.float32)
    Xtra, ytra, hgb, to_group, dispatch_v3 = G['Xtra'], G['ytra'], G['hgb'], G['to_group'], G['dispatch_v3']
    faults = [f for f in G['SINGLE'] if f not in G['RULE_PRIO'] and G['LOFO'].get(f)]
    if TRIAL: faults = faults[:2]
    rows, agree, tot = [], 0, 0; fh = open(os.path.join(OUT, 'partA_safe.jsonl'), 'w')
    for f in faults:
        keep_ = ytra != f; mf = hgb().fit(Xtra[keep_], ytra[keep_]); clf = list(mf.classes_); inf_ = clf.index('NONE')
        mgf = hgb().fit(Xtra[keep_], to_group(ytra[keep_])); gcf = list(mgf.classes_)
        thr_f = float(np.quantile(1 - mgf.predict_proba(Xtra[(ytra == 'NONE')])[:, gcf.index('NONE')], 1 - CFG['CLEAN_FPR']))
        es = [x for x in EPIS if x['fault'] == f and x['split'] == 'test']; stored = G['LOFO'][f]
        if TRIAL: es, stored = es[:5], stored[:5]
        for e, srow in zip(es, stored):
            st = e['st']; gold, k = st['gold'], st['k']; p = mf.predict_proba(vec(e['feats']))[0]
            reps, s = dispatch_v3(p, e['feats'], clf, inf_, mgf); fl = bool(s >= thr_f)
            tr_old = run(apply_v3(st, reps)) if fl else None; ok0 = bool(fl and succ(tr_old, gold, k)); tot += 1; agree += int(ok0 == srow['ok'])
            r = dict(fault=f, flagged=fl, P0=ok0, P0_stored=bool(srow['ok']), P12=False, SAFE=False, P12_pick=None, SAFE_pick=None, SAFE_switched=False, old_healthy=None, probes12=0, probes_safe=0)
            if fl:
                order = [clf[i] for i in np.argsort(-p) if clf[i] != 'NONE']; S0 = flagged(e['feats']); tr0 = run(st); rank = {c: i for i, c in enumerate(order)}
                def healthy(fe): q = mf.predict_proba(vec(fe))[0]; return bool(clf[int(np.argmax(q))] == 'NONE' and not flagged(fe)), float(q[inf_])
                lib = sorted([c for c in LIB if COMP[c] in S0 and c != f], key=lambda c: rank.get(c, 99))
                if COMP.get(f) in S0: lib.insert(min([i for i, c in enumerate(lib) if COMP[c] == COMP[f]] or [len(lib)]), f)
                # ---- P12: the earlier rule (up to 3 candidates, keep the largest increase in P(NONE))
                cand, seen = [], set()
                for c in lib + [c for c in order if c in G['SINGLE']]:
                    fn = fam_repair(c)
                    if id(fn) in seen: continue
                    seen.add(id(fn)); cand.append((c, fn))
                    if len(cand) == 3: break
                best = None
                for c, fn in cand:
                    tr2 = run(fn(st, tr0)); d = float(mf.predict_proba(vec(features(tr2)))[0][inf_] - p[inf_])
                    if best is None or d > best[0]: best = (d, c, bool(succ(tr2, gold, k)))
                r['P12'], r['P12_pick'], r['probes12'] = best[2], best[1], len(cand)
                # ---- P-safe: old repair first; probe at most 2 flagged-component repairs; switch only to a healthy result
                h_old, pn_old = healthy(features(tr_old)); r['old_healthy'] = h_old; chosen = (ok0, 'OLD')
                if not h_old:
                    olds = {id(fn) for _, fn in reps}; extra, sn = [], set()
                    for c in lib:
                        fn = fam_repair(c)
                        if id(fn) in olds or id(fn) in sn: continue
                        sn.add(id(fn)); extra.append((c, fn))
                        if len(extra) == 2: break
                    res = []
                    for c, fn in extra:
                        tr2 = run(fn(st, tr0)); h2, pn2 = healthy(features(tr2)); res.append((h2, pn2, c, bool(succ(tr2, gold, k))))
                    healthy_ = [x for x in res if x[0]]
                    if healthy_: b = max(healthy_, key=lambda x: x[1]); chosen = (b[3], b[2]); r['SAFE_switched'] = True
                    r['probes_safe'] = len(extra)
                r['SAFE'], r['SAFE_pick'] = bool(chosen[0]), chosen[1]
            rows.append(r); fh.write(json.dumps(r) + '\n'); fh.flush()
        log(f, 'P0', round(float(np.mean([x['P0'] for x in rows if x['fault'] == f])), 3), 'P12', round(float(np.mean([x['P12'] for x in rows if x['fault'] == f])), 3), 'SAFE', round(float(np.mean([x['SAFE'] for x in rows if x['fault'] == f])), 3))
    R = dict(trial=bool(TRIAL), reproduction=dict(agree=agree, n=tot, rate=agree / max(1, tot)), n_faults=len(faults), seed=int(CFG['SEED']))
    if R['reproduction']['rate'] >= 0.995:
        pf = {f: {k: float(np.mean([x[k] for x in rows if x['fault'] == f])) for k in ('P0', 'P12', 'SAFE', 'P0_stored')} for f in faults}; rng = np.random.default_rng(7); B = [rng.integers(0, len(faults), len(faults)) for _ in range(2000)]
        def diff(a, b): d = np.array([pf[f][a] - pf[f][b] for f in faults]); bs = [d[i].mean() for i in B]; return dict(mean=float(d.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])
        fl_ = [x for x in rows if x['flagged']]
        R.update(U1={k: float(np.mean([pf[f][k] for f in faults])) for k in ('P0', 'P0_stored', 'P12', 'SAFE')}, SAFE_minus_P0=diff('SAFE', 'P0'), P12_minus_P0=diff('P12', 'P0'), SAFE_minus_P12=diff('SAFE', 'P12'),
                 flagged=len(fl_), switched=int(sum(x['SAFE_switched'] for x in fl_)), old_already_healthy=int(sum(bool(x['old_healthy']) for x in fl_)),
                 wins_vs_P0=int(sum(x['SAFE'] and not x['P0'] for x in fl_)), losses_vs_P0=int(sum(x['P0'] and not x['SAFE'] for x in fl_)),
                 mean_probes_safe=float(np.mean([x['probes_safe'] for x in fl_] or [0])), per_fault=pf)
        R['SAFE_passes_lower_bound_above_0'] = bool(R['SAFE_minus_P0']['ci'][0] > 0)
    else: R['note'] = 'NOT RUN: reproduction gate failed'
    json.dump(R, open(os.path.join(OUT, 'RESULT_safe.json'), 'w'), indent=1, default=str)
    print(json.dumps({k: v for k, v in R.items() if k != 'per_fault'}, indent=1, default=str))
