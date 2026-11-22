"""v13 Ideas 1 + 2 on ESCI (docs/evidence/v13_esci_ideas_protocol.md). Executed INSIDE the Kaggle notebook after the frozen v6 code has been run up to its U1 stage
on the resumed v11.a checkpoint; `G` is that namespace. TRIAL=1 limits the work (numbers are not results). Writes <OUT>/RESULT.json and per-item jsonl files."""
import collections, json, os, time
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
    LIST = [(c, f, d) for c, v in INV.items() for f, d in v]; J = len(LIST); THR = 0.05 / J
    CAL = {f: np.array([e['feats'][f] for e in EPIS if e['split'] == 'train' and e['fault'] == 'NONE'], float) for _, f, _ in LIST}
    def pv(fe):
        out = []
        for c, f, d in LIST:
            x = float(fe[f]); v = CAL[f]; n = len(v)
            hi_, lo_ = (1 + (v >= x).sum()) / (n + 1), (1 + (v <= x).sum()) / (n + 1)
            out.append((c, hi_ if d == '+' else lo_ if d == '-' else min(1.0, 2 * min(hi_, lo_))))
        return out
    flagged = lambda fe: {c for c, p in pv(fe) if p <= THR}
    vec = lambda fe: np.array([[fe[k] for k in FEATS]], dtype=np.float32)
    def candidates(order, S0, f=None, allow=lambda fn: True):
        rank = {c: i for i, c in enumerate(order)}
        lib = sorted([c for c in LIB if COMP[c] in S0 and c != f], key=lambda c: rank.get(c, 99))
        if f is not None and COMP.get(f) in S0:
            pos = min([i for i, c in enumerate(lib) if COMP[c] == COMP[f]] or [len(lib)]); lib.insert(pos, f)
        out, seen = [], set()
        for c in lib + [c for c in order if c in G['SINGLE']]:
            fn = fam_repair(c)
            if id(fn) in seen or not allow(fn): continue
            seen.add(id(fn)); out.append((c, fn))
            if len(out) == 3: break
        return out
    R = dict(trial=bool(TRIAL), code_note='frozen v6 executed on the v11.a checkpoint; this file adds measurements only')

    # ---------------- Part A: U1 with Ideas 1 + 2
    Xtra, ytra, hgb, to_group, dispatch_v3 = G['Xtra'], G['ytra'], G['hgb'], G['to_group'], G['dispatch_v3']
    faults = [f for f in G['SINGLE'] if f not in G['RULE_PRIO'] and G['LOFO'].get(f)]
    if TRIAL: faults = faults[:2]
    rowsA, agree, tot = [], 0, 0; fA = open(os.path.join(OUT, 'partA.jsonl'), 'w')
    for f in faults:
        keep_ = ytra != f; mf = hgb().fit(Xtra[keep_], ytra[keep_]); clf = list(mf.classes_); inf_ = clf.index('NONE')
        mgf = hgb().fit(Xtra[keep_], to_group(ytra[keep_])); gcf = list(mgf.classes_)
        thr_f = float(np.quantile(1 - mgf.predict_proba(Xtra[(ytra == 'NONE')])[:, gcf.index('NONE')], 1 - CFG['CLEAN_FPR']))
        es = [x for x in EPIS if x['fault'] == f and x['split'] == 'test']; stored = G['LOFO'][f]
        if TRIAL: es, stored = es[:5], stored[:5]
        for e, srow in zip(es, stored):
            st = e['st']; gold, k = st['gold'], st['k']; p = mf.predict_proba(vec(e['feats']))[0]
            reps, s = dispatch_v3(p, e['feats'], clf, inf_, mgf); fl = s >= thr_f
            ok0 = fl and bool(succ(run(apply_v3(st, reps)), gold, k)); tot += 1; agree += int(ok0 == srow['ok'])
            ok12, pick, ncost = False, None, 0
            if fl:
                order = [clf[i] for i in np.argsort(-p) if clf[i] != 'NONE']; tr0 = run(st); best = None
                for c, fn in candidates(order, flagged(e['feats']), f):
                    tr2 = run(fn(st, tr0)); d = float(mf.predict_proba(vec(features(tr2)))[0][inf_] - p[inf_]); ncost += 1
                    if best is None or d > best[0]: best = (d, c, bool(succ(tr2, gold, k)))
                if best: ok12, pick = best[2], best[1]
            r = dict(fault=f, flagged=bool(fl), P0=bool(ok0), P0_stored=bool(srow['ok']), P12=bool(ok12), pick=pick, probes=ncost); rowsA.append(r); fA.write(json.dumps(r) + '\n'); fA.flush()
        log('A', f, 'P0', np.mean([r['P0'] for r in rowsA if r['fault'] == f]).round(3), 'P12', np.mean([r['P12'] for r in rowsA if r['fault'] == f]).round(3))
    gateA = agree / max(1, tot); R['A_reproduction'] = dict(agree=agree, n=tot, rate=gateA)
    if gateA >= 0.995:
        pf = {f: dict(P0=float(np.mean([r['P0'] for r in rowsA if r['fault'] == f])), P12=float(np.mean([r['P12'] for r in rowsA if r['fault'] == f])),
                      P0_stored=float(np.mean([r['P0_stored'] for r in rowsA if r['fault'] == f]))) for f in faults}
        d = np.array([pf[f]['P12'] - pf[f]['P0'] for f in faults]); rng = np.random.default_rng(7); bs = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(2000)]
        u0, u12 = float(np.mean([pf[f]['P0'] for f in faults])), float(np.mean([pf[f]['P12'] for f in faults]))
        R['A'] = dict(n_faults=len(faults), U1_P0=u0, U1_P0_stored=float(np.mean([pf[f]['P0_stored'] for f in faults])), U1_P12=u12, diff=float(d.mean()),
                      ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], U1_bar=0.50, U1_P12_meets_bar=bool(u12 >= 0.50),
                      mean_probes=float(np.mean([r['probes'] for r in rowsA if r['flagged']] or [0])), per_fault=pf)
    else: R['A'] = 'NOT RUN: reproduction gate failed'
    log('A done', R['A_reproduction'])

    # ---------------- Part B: real failures, detection
    ATT = G['ATT']; cls = list(ATT.classes_); iN = cls.index('NONE'); NAT3, CENS = G['NAT3'], G['CENS']
    qs = list(NAT3); y, sa, si, gn = [], [], [], []
    for q in qs:
        r = CENS[q]; fe = r['feats']; y.append(int(not r['h5'])); sa.append(1 - float(ATT.predict_proba(vec(fe))[0][iN])); si.append(-min(p for _, p in pv(fe))); gn.append(bool(r.get('gold_is_nan', False)))
    y, sa, si, gn = map(np.array, (y, sa, si, gn))
    def auc(yy, s):
        from scipy.stats import rankdata
        if yy.sum() == 0 or yy.sum() == len(yy): return float('nan')
        rr = rankdata(s); p_ = yy == 1; return float((rr[p_].sum() - p_.sum() * (p_.sum() + 1) / 2) / (p_.sum() * (~p_).sum()))
    keep = ~gn
    R['B'] = dict(n=len(qs), real_failures=int(y.sum()), attributor_auroc=auc(y, sa), invariant_auroc=auc(y, si),
                  n_excl_empty_gold=int(keep.sum()), failures_excl_empty_gold=int(y[keep].sum()), attributor_auroc_excl_empty_gold=auc(y[keep], sa[keep]), invariant_auroc_excl_empty_gold=auc(y[keep], si[keep]))
    log('B', R['B'])

    # ---------------- Part C: real failures, repair (Ideas 1 + 2 inside the deployed loop)
    LAMS, GATES, stratum, NAT_RULES, REP, rep_QLEX, gold_set, BY_PKEY, mkcfg, proba = G['LAMS'], G['GATES'], G['stratum'], G['NAT_RULES'], G['REP'], G['rep_QLEX'], G['gold_set'], G['BY_PKEY'], G['mkcfg'], G['proba']
    allow = (lambda fn: True) if CFG['DEPLOY']['natural_typo_repair'] else (lambda fn: fn is not rep_QLEX)
    qC = qs[:30] if TRIAL else qs; rowsC, agC = [], 0; fC = open(os.path.join(OUT, 'partC.jsonl'), 'w')
    for n_, q in enumerate(qC):
        r = CENS[q]; gold = gold_set([j for p_ in r['pids'] for j in BY_PKEY[p_]]); st = dict(q=q, tenant='ALL', cfg=mkcfg(), ov=None, gold=gold, k=5, meta={})
        tr = run(st); fe = r['feats']; h0 = bool(succ(tr, gold, 5)); p = proba(fe)
        reps, s = dispatch_v3(p, fe); lam = LAMS[GATES['ALPHA']][stratum(fe, 'esci')]
        nat = [(f, REP[f]) for f, cond in NAT_RULES if cond(fe)]; clf_reps = [(l, fn) for l, fn in (reps if s >= lam else []) if allow(fn)]
        h = lambda rs: bool(succ(run(apply_v3(st, rs)), gold, 5)) if rs else h0
        hl = h(nat + clf_reps); agC += int(hl == bool(NAT3[q]['h_loop'])); hn, pick, cost = hl, None, 0
        if clf_reps:
            order = [cls[i] for i in np.argsort(-p) if cls[i] != 'NONE']; best = None
            for c, fn in candidates(order, flagged(fe), None, allow):
                tr2 = run(apply_v3(st, nat + [(c, fn)])); d = float(proba(features(tr2))[iN] - p[iN]); cost += 1
                if best is None or d > best[0]: best = (d, c, bool(succ(tr2, gold, 5)))
            if best: hn, pick = best[2], best[1]
        x = dict(q_id=n_, h0=h0, h_loop=hl, h_loop_stored=bool(NAT3[q]['h_loop']), h_ideas=bool(hn), pick=pick, probes=cost); rowsC.append(x); fC.write(json.dumps(x) + '\n'); fC.flush()
        if n_ % 200 == 0: log('C', n_, 'of', len(qC))
    gateC = agC / max(1, len(qC)); R['C_reproduction'] = dict(agree=agC, n=len(qC), rate=gateC)
    if gateC >= 0.995:
        a = np.array([[x['h0'], x['h_loop'], x['h_ideas']] for x in rowsC], float); rng = np.random.default_rng(7); n = len(a)
        def bt(u, v):
            dd = a[:, u] - a[:, v]; bs = [dd[rng.integers(0, n, n)].mean() for _ in range(2000)]; return dict(mean=float(dd.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])
        R['C'] = dict(n=n, hit_none=float(a[:, 0].mean()), hit_loop=float(a[:, 1].mean()), hit_ideas=float(a[:, 2].mean()), ideas_minus_none=bt(2, 0), ideas_minus_loop=bt(2, 1), loop_minus_none=bt(1, 0),
                      fixed_vs_none=int(((a[:, 2] - a[:, 0]) > 0).sum()), broken_vs_none=int(((a[:, 2] - a[:, 0]) < 0).sum()), changed_vs_loop=int((a[:, 2] != a[:, 1]).sum()),
                      mean_extra_probes=float(np.mean([x['probes'] for x in rowsC])))
        R['C']['passes'] = bool(R['C']['ideas_minus_loop']['ci'][0] > -0.005 and R['C']['ideas_minus_none']['ci'][0] > 0)
    else: R['C'] = 'NOT RUN: reproduction gate failed'
    log('C done', R['C_reproduction'])
    if isinstance(R.get('A'), dict): R['A']['passes'] = bool(R['A']['ci'][0] > 0)
    json.dump(R, open(os.path.join(OUT, 'RESULT.json'), 'w'), indent=1, default=str)
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != 'per_fault'}) for k, v in R.items()}, indent=1, default=str))
