"""v14 E2 (U1 ceiling), E2b (verify-then-escalate) and E3 (real failures labelled by intervention) on ESCI; docs/evidence/v14_flagship_protocol.md.
Executed INSIDE the Kaggle notebook after the frozen v6 code has run up to its U1 stage on a resumed judged checkpoint; `G` is that namespace.
TRIAL=1 limits the work (numbers are not results). Writes <OUT>/RESULT.json and per-item jsonl files. Measurements only: nothing in the frozen run is changed."""
import json, math, os, time
import numpy as np

INF = float('inf')


def main(G, OUT, TRIAL, CEILING=True):
    os.makedirs(OUT, exist_ok=True); t0 = time.time(); log = lambda *a: print(f'[{time.time() - t0:6.0f}s]', *a, flush=True)
    EPIS, FEATS, CFG, GATES = G['EPIS'], G['FEATS'], G['CFG'], G['GATES']
    run, succ, features, apply_v3, fam_repair, dispatch_v3, proba = G['run'], G['succ'], G['features'], G['apply_v3'], G['fam_repair'], G['dispatch_v3'], G['proba']
    SINGLE, RULE_PRIO, REP, GROUP_REPAIR, universal, FAMILY, GROUP = G['SINGLE'], G['RULE_PRIO'], G['REP'], G['GROUP_REPAIR'], G['universal'], G['FAMILY'], G['GROUP']
    Xtra, ytra, hgb, to_group, LOFO, ATT = G['Xtra'], G['ytra'], G['hgb'], G['to_group'], G['LOFO'], G['ATT']
    COST, lab_group, STRATA, LAMS, crc_lambda, cap_lambda = G['COST'], G['lab_group'], G['STRATA'], G['LAMS'], G['crc_lambda'], G['cap_lambda']
    vec = lambda fe: np.array([[fe[k] for k in FEATS]], dtype=np.float32)
    rng = np.random.default_rng(7)
    def boot(d, n=2000):
        d = np.asarray(d, float)
        if len(d) == 0: return dict(mean=float('nan'), ci=[float('nan')] * 2)
        bs = d[rng.integers(0, len(d), (n, len(d)))].mean(1); return dict(mean=float(d.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])
    def wilson(k, n, z=1.96):
        if n == 0: return [float('nan')] * 2
        p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return [(c - h) / d, (c + h) / d]
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
    def uniq(pairs):
        out = []
        for l, fn in pairs:
            if all(fn is not g for _, g in out): out.append((l, fn))
        return out
    CAT = uniq([(c, fam_repair(c)) for c in SINGLE] + [(r, REP[r]) for r in RULE_PRIO] + [('G' + g, GROUP_REPAIR[g]) for g in 'QKR'] + [('UNIV', universal)])
    R = dict(trial=bool(TRIAL), seed=str(CFG['SEED']), code_note='frozen v6 executed on a judged checkpoint; this file adds measurements only', catalogue=[l for l, _ in CAT])
    log('catalogue', len(CAT), [l for l, _ in CAT])
    def cost_esc(reps, esc): return sum(COST[lab_group(l)] for l, _ in reps) + (12 if esc else 0)

    # ---------------- E2 + E2b in LOFO: ceiling decomposition and U1 of the escalation policies
    faults = [f for f in SINGLE if f not in RULE_PRIO and LOFO.get(f)]
    if TRIAL: faults = faults[:2]
    rowsU, agree, tot = [], 0, 0; fU = open(os.path.join(OUT, 'E2_lofo.jsonl'), 'w')
    for f in faults:
        keep_ = ytra != f; mf = hgb().fit(Xtra[keep_], ytra[keep_]); clf = list(mf.classes_); inf_ = clf.index('NONE')
        mgf = hgb().fit(Xtra[keep_], to_group(ytra[keep_])); gcf = list(mgf.classes_)
        thr_f = float(np.quantile(1 - mgf.predict_proba(Xtra[(ytra == 'NONE')])[:, gcf.index('NONE')], 1 - CFG['CLEAN_FPR']))
        reach = uniq([(c, fam_repair(c)) for c in SINGLE if c != f] + [(r, REP[r]) for r in RULE_PRIO if r != f] + [('G' + g, GROUP_REPAIR[g]) for g in 'QKR'] + [('UNIV', universal)])
        own = fam_repair(f); own_reachable = any(fn is own for _, fn in reach)
        es = [x for x in EPIS if x['fault'] == f and x['split'] == 'test']; stored = LOFO[f]
        if TRIAL: es, stored = es[:3], stored[:3]
        sc = lambda fe: dispatch_v3(mf.predict_proba(vec(fe))[0], fe, clf, inf_, mgf)[1]
        for e, srow in zip(es, stored):
            st = e['st']; gold, k = st['gold'], st['k']; tr0 = run(st)
            reps, s = dispatch_v3(mf.predict_proba(vec(e['feats']))[0], e['feats'], clf, inf_, mgf); fl = bool(s >= thr_f)
            tr1 = run(apply_v3(st, reps)); ok_rep = bool(succ(tr1, gold, k)); s1 = float(sc(features(tr1)))
            tru = run(universal(st, tr0)); ok_univ = bool(succ(tru, gold, k)); su = float(sc(features(tru)))
            P0 = fl and ok_rep; tot += 1; agree += int(P0 == bool(srow['ok']))
            esc = fl and s1 >= thr_f
            r = dict(fault=f, flagged=fl, P0=P0, ok_rep=ok_rep, ok_univ=ok_univ, s=float(s), s1=s1, su=su, thr=thr_f, escalated=bool(esc),
                     F_esc=bool(fl and (ok_univ if esc else ok_rep)), F_keep=bool(fl and ((ok_rep if s1 <= su else ok_univ) if esc else ok_rep)), F_univ=bool(fl and ok_univ))
            if CEILING:
                outc = {l: bool(succ(run(fn(st, tr0)), gold, k)) for l, fn in reach}
                r.update(own_ok=bool(succ(run(own(st, tr0)), gold, k)), own_reachable=own_reachable, reach_any=any(outc.values()), reach_fixers=[l for l, v in outc.items() if v])
            rowsU.append(r); fU.write(json.dumps(r) + '\n'); fU.flush()
        xs = [r for r in rowsU if r['fault'] == f]
        log('E2', f, 'P0', round(np.mean([r['P0'] for r in xs]), 3), 'F_esc', round(np.mean([r['F_esc'] for r in xs]), 3), 'F_keep', round(np.mean([r['F_keep'] for r in xs]), 3),
            'C_any', round(np.mean([r.get('reach_any', 0) for r in xs]), 3) if CEILING else '-')
    R['E2_reproduction'] = dict(agree=agree, n=tot, rate=agree / max(1, tot))
    if R['E2_reproduction']['rate'] >= 0.995:
        pf = {}
        for f in faults:
            xs = [r for r in rowsU if r['fault'] == f]; m = lambda key: float(np.mean([bool(r.get(key)) for r in xs]))
            pf[f] = dict(n=len(xs), flagged=m('flagged'), P0=m('P0'), F_esc=m('F_esc'), F_keep=m('F_keep'), F_univ=m('F_univ'), escalated=m('escalated'),
                         ok_univ_unflagged_too=m('ok_univ'))
            if CEILING: pf[f].update(own=m('own_ok'), own_reachable=bool(xs[0]['own_reachable']) if xs else None, C_any=m('reach_any'),
                                     C_flag=float(np.mean([r['flagged'] and r['reach_any'] for r in xs])))
        mean = lambda key: float(np.mean([pf[f][key] for f in faults]))
        U = dict(n_faults=len(faults), U1_bar=0.50, U1_P0=mean('P0'), U1_F_esc=mean('F_esc'), U1_F_keep=mean('F_keep'), U1_F_univ=mean('F_univ'), flagged=mean('flagged'),
                 F_esc_minus_P0=boot([pf[f]['F_esc'] - pf[f]['P0'] for f in faults]), F_keep_minus_P0=boot([pf[f]['F_keep'] - pf[f]['P0'] for f in faults]), per_fault=pf)
        if CEILING:
            U.update(C_any=mean('C_any'), C_flag=mean('C_flag'), own=mean('own'), U1_over_C_flag=(mean('P0') / mean('C_flag')) if mean('C_flag') > 0 else None,
                     faults_C_any_below_bar=[f for f in faults if pf[f]['C_any'] < 0.5], faults_C_flag_below_bar=[f for f in faults if pf[f]['C_flag'] < 0.5],
                     bar_reachable_with_this_flagger=bool(mean('C_flag') >= 0.5))
        R['E2'] = U
    else: R['E2'] = 'NOT REPORTED: reproduction gate failed'
    log('E2 done', R['E2_reproduction'], {k: v for k, v in R['E2'].items() if k != 'per_fault'} if isinstance(R['E2'], dict) else R['E2'])

    # ---------------- E2b in deployment: CRC recalibrated for the escalation policies; held-out clean loss and in-distribution closure
    CAL, cal_items, mkcfg = G['CAL'], G['cal_items'], G['mkcfg']
    items = cal_items[:40] if TRIAL else cal_items
    cal, agc = [], 0; fC = open(os.path.join(OUT, 'E2b_calibration.jsonl'), 'w')
    for n_, (bid, x) in enumerate(items):
        fe = x['feats']; st = dict(q=x['q'], tenant=x['tenant'], cfg=mkcfg(), ov=None, gold=x['gold'], k=5, meta={}); h5 = bool(x['h5'])
        reps, s = dispatch_v3(proba(fe), fe); tr1 = run(apply_v3(st, reps)); fe1 = features(tr1); s1 = float(dispatch_v3(proba(fe1), fe1)[1])
        l_rep = int(h5 and not succ(tr1, x['gold'], 5)); tru = run(universal(st)); l_univ = int(h5 and not succ(tru, x['gold'], 5)); feu = features(tru); su = float(dispatch_v3(proba(feu), feu)[1])
        c0 = CAL[bid]; agc += int(abs(float(c0[0]) - float(s)) < 1e-9 and int(c0[1]) == l_rep)
        r = dict(bid_n=n_, s=float(s), s1=s1, su=su, l_rep=l_rep, l_univ=l_univ, strat=c0[2]); cal.append(r); fC.write(json.dumps(r) + '\n')
        if n_ % 400 == 0: log('E2b calibration', n_, 'of', len(items))
    R['E2b_cal_reproduction'] = dict(agree=agc, n=len(items), rate=agc / max(1, len(items)))
    def crc_esc(rows, alpha):
        s = np.array([r['s'] for r in rows]); s1 = np.array([r['s1'] for r in rows]); lr = np.array([r['l_rep'] for r in rows]); lu = np.array([r['l_univ'] for r in rows]); n = len(rows)
        if n == 0: return INF
        for lam in sorted(set(s.tolist()) | set(s1.tolist())) + [INF]:
            if n / (n + 1) * np.mean((s >= lam) * np.maximum(lr, (s1 >= lam) * lu)) + 1 / (n + 1) <= alpha: return lam
        return INF
    A = GATES['ALPHA']
    LAM_E = {sn: crc_esc([r for r in cal if r['strat'] == sn], A) for sn in STRATA}
    LAM_EC = {sn: max(LAM_E[sn], cap_lambda(np.array([r['s'] for r in cal if r['strat'] == sn]), CFG['CAP_FRAC'])) for sn in STRATA}
    R['E2b_lambdas'] = dict(escalation_mondrian=LAM_E, escalation_capped=LAM_EC, frozen_mondrian=LAMS[A], calibration_n={sn: sum(r['strat'] == sn for r in cal) for sn in STRATA})
    log('E2b lambdas', R['E2b_lambdas'])
    TE = [e for e in EPIS if e['split'] == 'test']
    if TRIAL: TE = [e for e in TE if e['fault'] == 'NONE'][:40] + [e for e in TE if e['fault'] != 'NONE'][:40]
    rowsT, agt = [], 0; fT = open(os.path.join(OUT, 'E2b_test.jsonl'), 'w')
    for n_, e in enumerate(TE):
        L3 = e['loop3']; st = e['st']; k = 5 if e['fault'] == 'NONE' else st['k']; gold = st['gold']; fe = e['feats']
        reps, s = dispatch_v3(proba(fe), fe); tr1 = run(apply_v3(st, reps)); ok_rep = bool(succ(tr1, gold, k)); fe1 = features(tr1); s1 = float(dispatch_v3(proba(fe1), fe1)[1])
        tru = run(universal(st)); ok_univ = bool(succ(tru, gold, k)); feu = features(tru); su = float(dispatch_v3(proba(feu), feu)[1])
        agt += int(abs(float(L3['s']) - float(s)) < 1e-9 and bool(L3['ok_rep']) == ok_rep and bool(L3['ok_univ']) == ok_univ)
        r = dict(n=n_, fault=e['fault'], strat=L3['strat'], s=float(s), s1=s1, su=su, ok_rep=ok_rep, ok_univ=ok_univ, ok_none=bool(L3['ok_none']),
                 clean_h5=bool(e.get('clean_h5', False)), cost_rep=sum(COST[lab_group(l)] for l, _ in reps)); rowsT.append(r); fT.write(json.dumps(r) + '\n')
        if n_ % 500 == 0: log('E2b test', n_, 'of', len(TE))
    R['E2b_test_reproduction'] = dict(agree=agt, n=len(TE), rate=agt / max(1, len(TE)))
    def evalpol(lam, mode):
        per, clean = {}, []
        for r in rowsT:
            lm = lam[r['strat']]; d = r['s'] >= lm; esc = d and mode != 'base' and r['s1'] >= lm
            if not d: ok = r['ok_none']
            elif not esc: ok = r['ok_rep']
            else: ok = r['ok_univ'] if mode == 'esc' else (r['ok_rep'] if r['s1'] <= r['su'] else r['ok_univ'])
            cost = (r['cost_rep'] + (12 if esc else 0)) if d else 0
            if r['fault'] == 'NONE': clean.append((r['clean_h5'] and not ok, d, esc, cost))
            else: per.setdefault(r['fault'], []).append(ok)
        nl = sum(c[0] for c in clean); n = len(clean)
        return dict(clean_loss=nl / max(1, n), clean_loss_wilson=wilson(nl, n), clean_n=n, clean_dispatch=float(np.mean([c[1] for c in clean])) if clean else None,
                    clean_escalation=float(np.mean([c[2] for c in clean])) if clean else None, clean_mean_cost=float(np.mean([c[3] for c in clean])) if clean else None,
                    mean_closure=float(np.mean([np.mean(v) for v in per.values()])) if per else None, per_fault_closure={f: float(np.mean(v)) for f, v in per.items()})
    LAMS_CAP = G['LAMS_CAP']
    P = {'mondrian_crc_0.005 (frozen)': evalpol(LAMS[A], 'base'), 'capped_crc_0.005 (frozen)': evalpol(LAMS_CAP, 'base'),
         'F_esc mondrian': evalpol(LAM_E, 'esc'), 'F_keep mondrian': evalpol(LAM_E, 'keep'), 'F_esc capped': evalpol(LAM_EC, 'esc'), 'F_keep capped': evalpol(LAM_EC, 'keep')}
    for v in P.values(): v.pop('per_fault_closure') if TRIAL else None
    R['E2b_policies'] = P
    stored = {p['policy']: p for p in G['POLICY']}
    R['E2b_base_matches_stored'] = dict(mondrian=[P['mondrian_crc_0.005 (frozen)']['mean_closure'], stored['mondrian_crc_0.005']['mean_closure'], P['mondrian_crc_0.005 (frozen)']['clean_loss'], stored['mondrian_crc_0.005']['clean_loss']],
                                        capped=[P['capped_crc_0.005 (frozen)']['mean_closure'], stored['capped_crc_0.005']['mean_closure'], P['capped_crc_0.005 (frozen)']['clean_loss'], stored['capped_crc_0.005']['clean_loss']])
    log('E2b policies', {k: {kk: vv for kk, vv in v.items() if kk != 'per_fault_closure'} for k, v in P.items()})
    if isinstance(R.get('E2'), dict):
        dev = {}
        for var in ('F_esc', 'F_keep'):
            dev[var] = dict(U1=R['E2']['U1_' + var], clean_loss=P[f'{var} mondrian']['clean_loss'])
        ok_ = [v for v in ('F_esc', 'F_keep') if dev[v]['clean_loss'] <= A]
        primary = 'F_esc' if not ok_ else max(ok_, key=lambda v: (dev[v]['U1'], v == 'F_esc'))
        R['E2b_selection_rule_output'] = dict(dev=dev, primary=primary,
                                              confirm_conditions=dict(U1_ge_bar=bool(R['E2']['U1_' + primary] >= 0.5), clean_loss_le_alpha=bool(P[f'{primary} mondrian']['clean_loss'] <= A),
                                                                      closure_not_below_base_minus_0p02=bool(P[f'{primary} mondrian']['mean_closure'] >= P['mondrian_crc_0.005 (frozen)']['mean_closure'] - 0.02)))

    # ---------------- E3: real failures in natural traffic, labelled by intervention
    NAT3, CENS, gold_set, BY_PKEY, NAT_RULES, rep_QLEX, stratum = G['NAT3'], G['CENS'], G['gold_set'], G['BY_PKEY'], G['NAT_RULES'], G['rep_QLEX'], G['stratum']
    qpp, iN = G['qpp'], list(ATT.classes_).index('NONE')
    qs = list(NAT3)
    fails = [q for q in qs if not NAT3[q]['h0'] and not CENS[q]['gold_is_nan']]; oks = [q for q in qs if NAT3[q]['h0'] and not CENS[q]['gold_is_nan']]
    if TRIAL: fails, oks = fails[:10], oks[:10]
    allow = (lambda fn: True) if CFG['DEPLOY']['natural_typo_repair'] else (lambda fn: fn is not rep_QLEX)
    rowsR = []; fR = open(os.path.join(OUT, 'E3_natural.jsonl'), 'w'); agn = 0
    for n_, q in enumerate(fails + oks):
        r0 = CENS[q]; gold = gold_set([j for p_ in r0['pids'] for j in BY_PKEY[p_]]); st = dict(q=q, tenant='ALL', cfg=mkcfg(), ov=None, gold=gold, k=5, meta={})
        tr0 = run(st); fe = r0['feats']; h0 = bool(succ(tr0, gold, 5)); agn += int(h0 == bool(NAT3[q]['h0']))
        Q = qpp(tr0); x = dict(q_n=n_, real_failure=not h0, h0=h0, h_loop=bool(NAT3[q]['h_loop']), h_univ=bool(NAT3[q]['h_univ']), s_att=float(1 - proba(fe)[iN]), nqc=Q['nqc'], wig=Q['wig'])
        # escalation on top of the deployed loop (descriptive): classifier at the escalation threshold, natural rules as deployed
        reps, s = dispatch_v3(proba(fe), fe); lam = LAM_E[stratum(fe, 'esci')]
        nat = [(f_, REP[f_]) for f_, cond in NAT_RULES if cond(fe)]; clf_reps = [(l, fn) for l, fn in (reps if s >= lam else []) if allow(fn)]
        if nat or clf_reps:
            tr1 = run(apply_v3(st, nat + clf_reps)); fe1 = features(tr1); s1 = float(dispatch_v3(proba(fe1), fe1)[1])
            x['h_esc'] = bool(succ(run(universal(st)), gold, 5)) if (clf_reps and s1 >= lam) else bool(succ(tr1, gold, 5)); x['escalated'] = bool(clf_reps and s1 >= lam)
        else: x['h_esc'] = h0; x['escalated'] = False
        if not h0:
            outc = {l: bool(succ(run(fn(st, tr0)), gold, 5)) for l, fn in CAT}; x['fixers'] = [l for l, v in outc.items() if v]; x['random_success'] = float(np.mean(list(outc.values())))
        rowsR.append(x); fR.write(json.dumps(x) + '\n'); fR.flush()
        if n_ % 200 == 0: log('E3', n_, 'of', len(fails) + len(oks))
    R['E3_reproduction'] = dict(agree=agn, n=len(rowsR), rate=agn / max(1, len(rowsR)))
    F = [x for x in rowsR if x['real_failure']]; RF = [x for x in F if x['fixers']]; UF = [x for x in F if not x['fixers']]; S = [x for x in rowsR if not x['real_failure']]
    lab = {}
    for x in RF:
        for l in x['fixers']: lab[l] = lab.get(l, 0) + 1
    def det(pos):
        out = {}
        for name, key, sign in [('attributor', 's_att', 1), ('qpp_neg_nqc', 'nqc', -1), ('qpp_neg_wig', 'wig', -1)]:
            y = [1] * len(pos) + [0] * len(S); sc_ = [sign * x[key] for x in pos + S]; out[name] = auc_ci(y, sc_)
        return out
    E3 = dict(n_natural=len(qs), n_nonplaceholder=len(fails) + len(oks), real_failures=len(F), repairable=len(RF), coverage=len(RF) / max(1, len(F)), unrepairable=len(UF),
              label_counts=dict(sorted(lab.items(), key=lambda kv: -kv[1])),
              success_on_repairable=dict(loop=float(np.mean([x['h_loop'] for x in RF])) if RF else None, loop_wilson=wilson(sum(x['h_loop'] for x in RF), len(RF)),
                                         universal=float(np.mean([x['h_univ'] for x in RF])) if RF else None, random_catalogue_repair=float(np.mean([x['random_success'] for x in RF])) if RF else None,
                                         escalation=float(np.mean([x['h_esc'] for x in RF])) if RF else None, oracle=1.0 if RF else None,
                                         loop_minus_random=boot([x['h_loop'] - x['random_success'] for x in RF]), loop_minus_universal=boot([x['h_loop'] - x['h_univ'] for x in RF]),
                                         escalation_minus_loop=boot([x['h_esc'] - x['h_loop'] for x in RF])),
              detection_repairable_vs_success=det(RF), detection_unrepairable_vs_success=det(UF), detection_all_failures_vs_success=det(F),
              harm_on_real_successes=dict(n=len(S), loop_broken=int(sum(not x['h_loop'] for x in S)), loop_rate=float(np.mean([not x['h_loop'] for x in S])) if S else None,
                                          loop_wilson=wilson(int(sum(not x['h_loop'] for x in S)), len(S)), universal_rate=float(np.mean([not x['h_univ'] for x in S])) if S else None,
                                          escalation_rate=float(np.mean([not x['h_esc'] for x in S])) if S else None, escalated_share=float(np.mean([x['escalated'] for x in S])) if S else None))
    E3['claims'] = dict(detects_repairable_real_failures=bool(RF and E3['detection_repairable_vs_success']['attributor']['auroc'] >= 0.70),
                        diagnosis_beats_chance=bool(RF and E3['success_on_repairable']['loop_minus_random']['ci'][0] > 0),
                        no_harm_on_real_traffic=bool(S and E3['harm_on_real_successes']['loop_rate'] <= 0.005))
    R['E3'] = E3; log('E3', {k: v for k, v in E3.items() if k not in ('label_counts',)})
    json.dump(R, open(os.path.join(OUT, 'RESULT.json'), 'w'), indent=1, default=str)
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk not in ('per_fault', 'per_fault_closure')}) for k, v in R.items()}, indent=1, default=str)[:20000])
