"""Generate kaggle/diagrag_v5.py from kaggle/diagrag_v4.py by exact, asserted replacements. Every edit maps to an item of
docs/evidence/v5_protocol.md (C1 floor, C2 policies, C3 deployed config, C5 accounting) and its amendments B1-B3.
Usage: python kaggle/mk_v5.py   (writes diagrag_v5.py and prints its SHA-256)"""
import hashlib, os

here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, 'diagrag_v4.py'), encoding='utf-8').read()


def sub(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:90])
    s = s.replace(old, new)


# ---- header
sub("# # DiagRAG v4 — v3 + a GROUP-level attributor (NONE/Q/K/R) for dispatch and a complete K fallback repair\n",
    "# # DiagRAG v5 — v4 + a 50-positive measurement floor, capped and two-stage dispatch policies, and a deployed-config correction\n"
    "# v5 changes are pre-registered in docs/evidence/v5_protocol.md (amendments B1-B3), committed before this file existed. Bars are unchanged from v4:\n"
    "# AUROC >= 0.70, rescue Wilson LB >= 0.50, harm <= 10%, adoption >= 27 detectors and >= 24 repairs, L1 0.005, L2 0.70, U1 0.50, N1 CI lower bound > 0.\n"
    "# C1 floor: >= 50 held-out positives per detector gate and >= 50 hard episodes per repair gate (else THIN); N_HARD 100, MAX_ATT 4000.\n"
    "# C2 policies: capped_crc_0.005 and two_stage_0.005 are added to the policy table, with four targets reported together.\n"
    "# C3 deployed config: natural-misspelling repair (rep_QLEX) is OFF on natural traffic; the v4 behaviour is kept as a counterfactual (h_loop_v4cfg).\n"
    "# C5 accounting: VERDICT.accounting reports (a) the core 28, (b) the grounded set, (c) the quarantine set; the headline is (a).\n"
    "# ---- v4 header, unchanged below ----\n"
    "# # DiagRAG v4 — v3 + a GROUP-level attributor (NONE/Q/K/R) for dispatch and a complete K fallback repair\n")

# ---- C1 floor
sub("N_HARD=int(os.environ.get('N_HARD', 80 if GPU else 10))", "N_HARD=int(os.environ.get('N_HARD', 100 if GPU else 10))")
sub("MAX_ATT=int(os.environ.get('MAX_ATT', 2500 if GPU else 70))", "MAX_ATT=int(os.environ.get('MAX_ATT', 4000 if GPU else 70))")
sub("    detector='held-out one-vs-rest AUROC >= 0.70 (point estimate) AND >= 20 held-out positives',",
    "    detector='held-out one-vs-rest AUROC >= 0.70 (point estimate) AND >= 50 held-out positives (v5 floor; fewer is THIN)',")
sub("    repair='>= 20 hard episodes AND Wilson", "    repair='>= 50 hard episodes (v5 floor; fewer is THIN) AND Wilson")
sub("AUROC_BAR=0.70, MIN_TEST_POS=20, RESCUE_BAR_LB=0.50, MIN_REPAIR_N=20,", "AUROC_BAR=0.70, MIN_TEST_POS=50, RESCUE_BAR_LB=0.50, MIN_REPAIR_N=50,")

# ---- C2 / C3 config
sub("    RAGLOG_COMMIT='7f7d0686cc69e00f3081369039ae1247878aa928',\n)",
    "    RAGLOG_COMMIT='7f7d0686cc69e00f3081369039ae1247878aa928',\n"
    "    CAP_FRAC=0.20, T_DISPATCH=0.25, T_COST=1.5, T_CLOSURE=0.80,   # v5 C2: clean-dispatch cap used by the capped policies; targets T2, T3, T4\n"
    "    DEPLOY=dict(natural_typo_repair=False, injected_typo_repair=True, date='2026-11-16',\n"
    "                evidence='natural-misspelling repair: negative point estimate in all 5 runs that measured it (-4.9 to -7.1 pts); 95% CI excludes 0 in GPU seeds 46 and 48 (-5.4 [-10.8, -0.5]); SymSpell worse. docs/evidence/v5_protocol.md C3, B3'),\n)")
sub("    U1_BAR=0.50)\n",
    "    U1_BAR=0.50)\n"
    "GATES.update(\n"
    "    v5_policies=('capped_crc_0.005: Mondrian CRC threshold, raised per stratum to the 80th percentile of the calibration clean score so classifier dispatch on clean is <= 20%; '\n"
    "                 'two_stage_0.005: precise rules (alone) or natural rules K12/K05 (additive) then the attributor at a capped threshold, calibrated on the combined loss. '\n"
    "                 'Targets reported together: T1 clean loss <= 0.005, T2 total clean dispatch <= 0.25, T3 clean mean cost <= 1.5, T4 mean closure >= 0.80. '\n"
    "                 'L1 and L2 stay defined on mondrian_crc_0.005 (L2 bar 0.70).'),\n"
    "    v5_accounting='VERDICT.accounting: (a) core 28 under the original rule [headline], (b) grounded set, (c) quarantine set',\n"
    "    v5_deploy=('deployed config: natural-misspelling repair OFF on natural traffic (rep_QLEX not applied); injected-typo repair stays on; '\n"
    "               'counterfactual v4 behaviour reported as h_loop_v4cfg, arms NA1c, NA1d, N1v4'))\n")

# ---- calibration: also store the natural-rule loss and the combined loss (needed for the two-stage policy)
sub("""    lost = int(bool(x['h5']) and not succ(run(apply_v3(st, reps)), x['gold'], 5))
    CAL[bid] = (s, lost, stratum(x['feats'], x['src']))""",
    """    lost = int(bool(x['h5']) and not succ(run(apply_v3(st, reps)), x['gold'], 5))
    nat_r = [(f_, REP[f_]) for f_, cond_ in NAT_RULES if cond_(x['feats'])]   # v5: natural rules are additive in the two-stage policy
    lost_nat = int(bool(x['h5']) and bool(nat_r) and not succ(run(apply_v3(st, nat_r)), x['gold'], 5))
    lost_comb = int(bool(x['h5']) and not succ(run(apply_v3(st, nat_r + reps)), x['gold'], 5)) if nat_r else lost
    CAL[bid] = (s, lost, stratum(x['feats'], x['src']), lost_nat, lost_comb)""")

# ---- lambdas for the new policies
sub("LAM_GLOBAL = crc_lambda(*cal_arr(), GATES['ALPHA'])\n",
    "LAM_GLOBAL = crc_lambda(*cal_arr(), GATES['ALPHA'])\n"
    "def crc_lambda_ts(s_arr, ln_arr, lc_arr, alpha):\n"
    "    \"\"\"Two-stage CRC: per-query loss is lost_nat if the classifier does not dispatch (s < lam), else max(lost_nat, lost_comb). Non-increasing in lam.\"\"\"\n"
    "    n = len(s_arr)\n"
    "    if n == 0: return float('inf')\n"
    "    for lam in sorted(set(s_arr.tolist())) + [float('inf')]:\n"
    "        if n / (n + 1) * np.mean(np.where(s_arr >= lam, np.maximum(ln_arr, lc_arr), ln_arr)) + 1 / (n + 1) <= alpha: return lam\n"
    "    return float('inf')\n"
    "def cap_lambda(s_arr, frac):\n"
    "    \"\"\"Smallest lam with at most `frac` of the calibration clean scores >= lam (caps clean classifier dispatch).\"\"\"\n"
    "    if len(s_arr) == 0: return float('inf')\n"
    "    for lam in sorted(set(s_arr.tolist())) + [float('inf')]:\n"
    "        if np.mean(s_arr >= lam) <= frac: return lam\n"
    "    return float('inf')\n"
    "def cal_arr5(sname):\n"
    "    rows_ = [v for v in cv if v[2] == sname]; return np.array([v[0] for v in rows_]), np.array([v[3] for v in rows_]), np.array([v[4] for v in rows_])\n"
    "LAMS_CAP = {sn: max(LAMS[GATES['ALPHA']][sn], cap_lambda(cal_arr(sn)[0], CFG['CAP_FRAC'])) for sn in STRATA}\n"
    "LAMS_TS = {sn: max(crc_lambda_ts(*cal_arr5(sn), GATES['ALPHA']), cap_lambda(cal_arr5(sn)[0], CFG['CAP_FRAC'])) for sn in STRATA}\n")
sub("log('Mondrian CRC lambdas', LAMS, 'calibration', CALN, 'global lambda', LAM_GLOBAL); save_ckpt('calibration_done')",
    "log('Mondrian CRC lambdas', LAMS, 'calibration', CALN, 'global lambda', LAM_GLOBAL, 'capped', LAMS_CAP, 'two-stage', LAMS_TS); save_ckpt('calibration_done')")

# ---- per-episode loop outcomes for the natural rules
sub("""        reps, s = dispatch_v3(proba(e['feats']), e['feats']); k_ = 5 if e['fault'] == 'NONE' else e['st']['k']
        e['loop3'] = dict(lab=[l for l, _ in reps], s=s, cost=cost_of(reps), ok_rep=bool(succ(run(apply_v3(e['st'], reps)), e['st']['gold'], k_)),""",
    """        reps, s = dispatch_v3(proba(e['feats']), e['feats']); k_ = 5 if e['fault'] == 'NONE' else e['st']['k']
        nat_r = [(f_, REP[f_]) for f_, cond_ in NAT_RULES if cond_(e['feats'])]   # v5: for the two-stage policy
        e['loop3'] = dict(nat=[f_ for f_, _ in nat_r], cost_nat=cost_of(nat_r), cost_comb=cost_of(nat_r + reps),
                          ok_nat=(bool(succ(run(apply_v3(e['st'], nat_r)), e['st']['gold'], k_)) if nat_r else None),
                          ok_comb=(bool(succ(run(apply_v3(e['st'], nat_r + reps)), e['st']['gold'], k_)) if nat_r else None),
                          lab=[l for l, _ in reps], s=s, cost=cost_of(reps), ok_rep=bool(succ(run(apply_v3(e['st'], reps)), e['st']['gold'], k_)),""")

# ---- policies
sub("    if pol == 'global_crc_0.005': return LAM_GLOBAL\n",
    "    if pol == 'global_crc_0.005': return LAM_GLOBAL\n    if pol == 'capped_crc_0.005': return LAMS_CAP[strat]\n    if pol == 'two_stage_0.005': return LAMS_TS[strat]\n")
sub("POLS = ['tau_none_5pct_fpr', 'global_crc_0.005'] + [f'mondrian_crc_{a}' for a in GATES['ALPHAS']]",
    "POLS = ['tau_none_5pct_fpr', 'global_crc_0.005'] + [f'mondrian_crc_{a}' for a in GATES['ALPHAS']] + ['capped_crc_0.005', 'two_stage_0.005']")
sub("""        if pol == 'diagnosis_free_universal':
            disp = [True] * len(es); ok = [e['loop3']['ok_univ'] for e in es]; costs = [12] * len(es)
            fa = ga = [False] * len(es)
        else:""",
    """        cd = None
        if pol == 'diagnosis_free_universal':
            disp = [True] * len(es); ok = [e['loop3']['ok_univ'] for e in es]; costs = [12] * len(es)
            fa = ga = [False] * len(es)
        elif pol == 'two_stage_0.005':   # v5: natural rules additive, classifier at the capped two-stage threshold
            cd = [e['loop3']['s'] >= thr_of(pol, e['loop3']['strat']) for e in es]; nt = [bool(e['loop3']['nat']) for e in es]
            disp = [c_ or n_ for c_, n_ in zip(cd, nt)]
            ok = [e['loop3']['ok_comb'] if (c_ and n_) else e['loop3']['ok_rep'] if c_ else e['loop3']['ok_nat'] if n_ else e['loop3']['ok_none'] for e, c_, n_ in zip(es, cd, nt)]
            costs = [e['loop3']['cost_comb'] if (c_ and n_) else e['loop3']['cost'] if c_ else e['loop3']['cost_nat'] if n_ else 0 for e, c_, n_ in zip(es, cd, nt)]
            labs = [e['loop3']['lab'] if c_ else e['loop3']['nat'] for e, c_ in zip(es, cd)]
            fa = [(not d) if f == 'NONE' else (d and fam_ok(l_, truth(e))) for e, d, l_ in zip(es, disp, labs)]
            ga = [(not d) if f == 'NONE' else (d and grp_ok(l_, truth(e))) for e, d, l_ in zip(es, disp, labs)]
        else:""")
sub("group_attribution=float(np.mean(ga)), mean_cost=float(np.mean(costs)))\n        if f == 'NONE':",
    "group_attribution=float(np.mean(ga)), mean_cost=float(np.mean(costs)),\n                   clf_dispatch_rate=float(np.mean(cd)) if cd is not None else float(np.mean(disp)))\n        if f == 'NONE':")
sub("clean_dispatch_rate=nr['dispatch_rate'], clean_mean_cost=nr['mean_cost'],",
    "clean_dispatch_rate=nr['dispatch_rate'], clean_clf_dispatch_rate=nr['clf_dispatch_rate'], clean_mean_cost=nr['mean_cost'],")
sub("    log('policy', POLICY[-1])\n",
    "    p_ = POLICY[-1]\n"
    "    p_.update(T1_loss=bool(p_['clean_loss'] <= GATES['ALPHA']), T2_dispatch=bool(p_['clean_dispatch_rate'] <= CFG['T_DISPATCH']),\n"
    "              T3_cost=bool(p_['clean_mean_cost'] <= CFG['T_COST']), T4_closure=bool(p_['mean_closure'] >= CFG['T_CLOSURE']))\n"
    "    p_['all_targets_met'] = bool(p_['T1_loss'] and p_['T2_dispatch'] and p_['T3_cost'] and p_['T4_closure'])\n"
    "    log('policy', POLICY[-1])\n")

# ---- C3 deployed config on natural traffic
sub("    clf_reps = reps if s >= lam else []\n",
    "    clf_full = reps if s >= lam else []\n"
    "    clf_reps = clf_full if CFG['DEPLOY']['natural_typo_repair'] else [(l_, fn_) for l_, fn_ in clf_full if fn_ is not rep_QLEX]   # v5 deployed config (C3, B3)\n")
sub("clf=[l for l, _ in clf_reps], h_loop=h(nat_reps + clf_reps),",
    "clf=[l for l, _ in clf_reps], h_loop=h(nat_reps + clf_reps), clf_v4cfg=[l for l, _ in clf_full],\n"
    "               h_loop_v4cfg=(h(nat_reps + clf_full) if len(clf_full) != len(clf_reps) else h(nat_reps + clf_reps)),")
sub("N1 = [r for r in NAT if r['arm'] == 'N1'][0]\n",
    "xs_c = [r for r in rows_ if 'NA1' in r['sel']]\n"
    "nat_row('NA1c', 'DEPLOYED LOOP, v5 config (natural typo repair OFF), on natural queries with q_correctable >= 1', xs_c, lambda r: r['h_loop'])\n"
    "nat_row('NA1d', 'counterfactual: same loop with the v4 config (natural typo repair ON), same queries', xs_c, lambda r: r['h_loop_v4cfg'])\n"
    "nat_row('N1v4', 'counterfactual: DEPLOYED LOOP with the v4 config on all natural queries', rows_, lambda r: r['h_loop_v4cfg'])\n"
    "N1 = [r for r in NAT if r['arm'] == 'N1'][0]\n")

# ---- B5: record the software environment in the protocol (no gate or computation changes)
sub("                   code_sha256=_code_sha), open(PROTO, 'w'), indent=1)",
    "                   code_sha256=_code_sha, env=ENV_VERSIONS), open(PROTO, 'w'), indent=1)")
sub("PROTO = os.path.join(OUT, 'JUDGED_PROTOCOL.json')\n",
    "PROTO = os.path.join(OUT, 'JUDGED_PROTOCOL.json')\n"
    "def _env_versions():   # v5 B5: a re-fit of the detectors from shipped episodes differed on Kaggle's stack, and the library versions were not recorded\n"
    "    import importlib.metadata as _im, platform\n"
    "    v = dict(python=platform.python_version(), platform=platform.platform(), cpu_count=os.cpu_count())\n"
    "    for n_ in ('numpy', 'pandas', 'scipy', 'scikit-learn', 'torch', 'transformers', 'sentence-transformers', 'faiss-cpu', 'faiss-gpu', 'rank-bm25', 'nltk', 'threadpoolctl'):\n"
    "        try: v[n_] = _im.version(n_)\n"
    "        except Exception: pass\n"
    "    try: v['cuda'] = torch.version.cuda; v['gpu'] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None\n"
    "    except Exception: pass\n"
    "    return v\n"
    "ENV_VERSIONS = _env_versions()\n")

# ---- C5 accounting and cheap-guarantee summary
sub("gsol = sol_df[sol_df.grounded]\n",
    "gsol = sol_df[sol_df.grounded]\n"
    "qsol = sol_df[~sol_df.grounded]\n"
    "_ver = 'ADOPTED' if n_rep >= GATES['REPAIR_TARGET'] and n_det >= GATES['DETECT_TARGET'] else 'NOT_ADOPTED'\n"
    "ACCT = dict(headline='a_core28',\n"
    "            a_core28=dict(detectors_pass=n_det, repairs_pass=n_rep, solved_both=n_sol, of=len(V1_FAULTS), verdict=_ver, not_solved=v1s[~v1s.solved].fault.tolist(),\n"
    "                          thin=v1s[(v1s.detector == 'THIN') | (v1s.repair == 'THIN')].fault.tolist()),\n"
    "            b_grounded=dict(faults=GROUNDED, detectors_pass=int((gsol.detector == 'PASS').sum()), repairs_pass=int((gsol.repair == 'PASS').sum()),\n"
    "                            solved_both=int(gsol.solved.sum()), of=len(gsol), not_solved=gsol[~gsol.solved].fault.tolist(), v4_baseline='20/22 (Q03, R26)'),\n"
    "            c_quarantine=dict(faults=QUARANTINE, detectors_pass=int((qsol.detector == 'PASS').sum()), repairs_pass=int((qsol.repair == 'PASS').sum()),\n"
    "                              solved_both=int(qsol.solved.sum()), of=len(qsol), not_solved=qsol[~qsol.solved].fault.tolist()))\n"
    "_has_guarantee = lambda p_: p_['policy'].startswith(('mondrian_crc', 'global_crc', 'capped_crc', 'two_stage'))\n"
    "_meets = [p_ for p_ in POLICY if p_['all_targets_met'] and _has_guarantee(p_)]\n"
    "CHEAP = dict(targets=dict(T1='held-out clean loss <= 0.005', T2='total clean dispatch <= 0.25', T3='clean mean cost <= 1.5', T4='mean closure >= 0.80'),\n"
    "             table=[{k_: p_[k_] for k_ in ('policy', 'clean_loss', 'clean_dispatch_rate', 'clean_clf_dispatch_rate', 'clean_mean_cost', 'mean_closure', 'T1_loss', 'T2_dispatch', 'T3_cost', 'T4_closure', 'all_targets_met')} for p_ in POLICY],\n"
    "             guaranteed_policies_meeting_all_four=[p_['policy'] for p_ in _meets], no_guarantee_policies_meeting_all_four=[p_['policy'] for p_ in POLICY if p_['all_targets_met'] and not _has_guarantee(p_)],\n"
    "             claim=(min(_meets, key=lambda p_: p_['clean_mean_cost'])['policy'] if _meets else None),\n"
    "             claim_rule='the guarantee claim is as strong as the best CRC-based policy meeting T1-T4 together, and no stronger; None means no CRC-based policy met all four')\n")
sub("               quarantine=QUARANTINE, U1=U1,", "               quarantine=QUARANTINE, accounting=ACCT, cheap_guarantee=CHEAP, U1=U1,")
sub("md = ['# DiagRAG v4 judged run report',", "md = ['# DiagRAG v5 judged run report',")

out = os.path.join(here, 'diagrag_v5.py')
open(out, 'w', encoding='utf-8').write(s)
print('wrote', out, hashlib.sha256(s.encode('utf-8')).hexdigest())
