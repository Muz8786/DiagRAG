# %% [markdown]
# ## 14c. Composed-fault arm (v7), evaluation on held-out composed episodes. Descriptive targets only; no adoption gate. Pre-registered in docs/evidence/v7_composed_protocol.md.
# The diagnoser is the project's own dispatch_v3 (rules, family-first attribution, group fallbacks) with the attributor fitted on single-fault rows (ATT0, the v6 version) or on single-fault rows plus
# composed TRAIN rows (ATT, the v7 version). Nothing about the diagnoser or the repairs is new; only the attributor's training rows differ.

# %%
COMPRES = RES.get('COMPRES') or dict(rows={}, clean={})
def fam_cover(lab, f_): return (not lab.startswith('G')) and (lab == f_ or FAMILY[lab] == FAMILY[f_])      # primary: a non-fallback label that names the cause or its repair-equivalence family
def grp_cover(lab, f_): return lab_group(lab) == GROUP[f_]                                                  # secondary: the label is in the cause's group (letter), fallbacks included
def set_prf(labels, comps, cover):
    labs = list(dict.fromkeys(labels))
    rec = sum(any(cover(l_, f_) for l_ in labs) for f_ in comps) / len(comps)
    prec = (sum(any(cover(l_, f_) for f_ in comps) for l_ in labs) / len(labs)) if labs else 0.0
    return rec, prec, (2 * prec * rec / (prec + rec) if prec + rec else 0.0)
def static_labels(fe, att, cls, inone, mg):
    p = att.predict_proba(np.array([[fe[k_] for k_ in FEATS]], dtype=np.float32))[0]; reps, s = dispatch_v3(p, fe, cls, inone, mg); return [l_ for l_, _ in reps], float(s)
CLS0 = list(ATT0.classes_); iN0 = CLS0.index('NONE')
def static_old(fe):   # the v6 diagnoser: attributor fitted on single-fault rows only, with its own TAU_C2 (swapped in for the call)
    g_ = globals(); t_ = g_['TAU_C2']; g_['TAU_C2'] = TAU_C2_0
    try: return static_labels(fe, ATT0, CLS0, iN0, ATTG0)
    finally: g_['TAU_C2'] = t_
def seq_loop(e, rev=False):
    """repair -> re-run -> re-diagnose -> repair, at most 3 rounds. The loop never sees the gold: it stops when the diagnoser's score falls below the L1 threshold of the query's stratum
    (mondrian_crc_0.005, calibrated on clean TRAIN queries scored by the same attributor) or when the diagnosis repeats a label it already applied. rev=True forces the first repair to be the
    other cause's (second group if the diagnosis listed two, else the best label outside the top group); if none exists it falls back to the default and reports rev_applicable False."""
    st, fe, gold, k_ = e['st'], e['feats'], e['st']['gold'], e['k']; lam = LAMS[GATES['ALPHA']][stratum(fe, e['src'])]; applied = []; rev_ok = None; s0 = None
    for rd in range(3):
        p = proba(fe); reps, s = dispatch_v3(p, fe)
        if rd == 0: s0 = float(s)
        if s < lam: break
        pick = reps[0]
        if rd == 0 and rev:
            rev_ok = False
            if len(reps) >= 2: pick, rev_ok = reps[-1], True
            elif not [f_ for f_ in RULE_PRIO if RULE_FIRE[f_](fe)]:
                p2 = p.copy(); g0 = lab_group(reps[0][0])
                for j_, c_ in enumerate(CLS):
                    if c_ != 'NONE' and GROUP[c_] == g0: p2[j_] = 0.0
                if p2.sum() - p2[iN] > 1e-9:
                    reps2, _ = dispatch_v3(p2 / p2.sum(), fe)
                    if reps2[0][0] != reps[0][0]: pick, rev_ok = reps2[0], True
        lab, fn = pick
        if lab in applied: break
        st = fn(st, run(st)); applied.append(lab); fe = features(run(st))
    return dict(ok=bool(succ(run(st), gold, k_)), applied=applied, rounds=len(applied), s_first=s0, rev_applicable=rev_ok)

TEST_COMP = [(i_, e) for i_, e in enumerate(COMP) if e['split'] == 'test']
SUB_REV = {i_ for i_, e in TEST_COMP if int(hashlib.md5(f'{COMP_SEED}|rev|{e["bid"]}'.encode()).hexdigest()[:8], 16) / 2**32 < 0.25}   # the forced reverse-order subsample (fixed by the protocol)
for n_, (i_, e) in enumerate(TEST_COMP):
    if i_ in COMPRES['rows']: continue
    comps, fe, st = e['comps'], e['feats'], e['st']
    lab_n, s_n = static_labels(fe, ATT, CLS, iN, ATTG); lab_o, s_o = static_old(fe)
    r = dict(comps=comps, stratum=e['stratum'], bid=e['bid'], src=e['src'], alone_fails=e['alone_fails'], lab_new=lab_n, s_new=s_n, lab_old=lab_o, s_old=s_o, seq=seq_loop(e))
    if i_ in SUB_REV: r['seq_rev'] = seq_loop(e, rev=True)
    r['oracle_fwd'] = bool(succ(run(apply_repairs(st, comps)), st['gold'], e['k']))
    rv = st
    for f_ in sorted(comps, key=lambda f_: 'QKR'.index(f_[0]), reverse=True): rv = REP[f_](rv, run(rv))
    r['oracle_rev'] = bool(succ(run(rv), st['gold'], e['k'])); COMPRES['rows'][i_] = r
    if n_ % 6 == 0: maybe_stop('composed_eval')
V8_TRAIN_PIDS = {p_ for r_ in qg.itertuples() if r_.split == 'train' and CENS.get(r_.query, {}).get('fresh') for p_ in r_.product_id}
V8_TRAIN_GOLD = gold_set([i_ for p_ in V8_TRAIN_PIDS for i_ in BY_PKEY[p_]])
CLEAN_CANDIDATES = [x for x in EPIS if x['split'] == 'test' and x['fault'] == 'NONE' and not (set(x['st']['gold']) & V8_TRAIN_GOLD)]
CLEAN_SEQ = sorted(CLEAN_CANDIDATES, key=lambda x: hashlib.md5(f'{COMP_SEED}|v8-clean|{x["bid"]}'.encode()).hexdigest())[:1000]
assert len(CLEAN_SEQ) == 1000, f'only {len(CLEAN_SEQ)} eligible held-out clean queries remain'
for n_, x in enumerate(CLEAN_SEQ):
    if x['bid'] in COMPRES['clean']: continue
    ps = dict(st=dict(q=x['st']['q'], tenant=x['st']['tenant'], cfg=mkcfg(), ov=None, gold=x['st']['gold'], k=5, meta={}), feats=x['feats'], k=5, src=src_of(x['bid']))
    sq = seq_loop(ps); COMPRES['clean'][x['bid']] = dict(sq, clean_h=bool(x['clean_h5']), lost=bool(x['clean_h5'] and not sq['ok']))
    if n_ % 10 == 0: maybe_stop('composed_clean')
save_ckpt('composed_eval_done')

def _w(k_, n_): return dict(k=int(k_), n=int(n_), rate=(k_ / n_ if n_ else None), ci=(list(wilson(int(k_), int(n_))) if n_ else None))
def summarise(rs):
    n_ = len(rs)
    if not n_: return dict(n=0, note='EMPTY: no held-out composed episodes in this stratum')
    out = dict(n=n_)
    for tag, key in (('new', 'lab_new'), ('old', 'lab_old')):
        prf = [set_prf(r[key], r['comps'], fam_cover) for r in rs]; prg = [set_prf(r[key], r['comps'], grp_cover) for r in rs]
        out[f'both_causes_family_{tag}'] = _w(sum(p[0] == 1.0 for p in prf), n_); out[f'any_cause_family_{tag}'] = _w(sum(p[0] > 0 for p in prf), n_)
        out[f'both_causes_group_{tag}'] = _w(sum(p[0] == 1.0 for p in prg), n_)
        out[f'set_f1_family_{tag}'] = float(np.mean([p[2] for p in prf])); out[f'set_recall_family_{tag}'] = float(np.mean([p[0] for p in prf])); out[f'set_precision_family_{tag}'] = float(np.mean([p[1] for p in prf]))
        out[f'set_f1_group_{tag}'] = float(np.mean([p[2] for p in prg]))
    out['sequential_closure'] = _w(sum(r['seq']['ok'] for r in rs), n_); out['mean_rounds_applied'] = float(np.mean([r['seq']['rounds'] for r in rs]))
    out['dispatched_first_round'] = _w(sum(r['seq']['rounds'] >= 1 for r in rs), n_)
    out['oracle_forward_closure'] = _w(sum(r['oracle_fwd'] for r in rs), n_); out['oracle_reverse_closure'] = _w(sum(r['oracle_rev'] for r in rs), n_)
    sub = [r for r in rs if 'seq_rev' in r]; out['reverse_subsample_n'] = len(sub)
    if sub:
        app = [r for r in sub if r['seq_rev']['rev_applicable']]; out['reverse_subsample_applicable_n'] = len(app)
        out['reverse_default_closure_same_episodes'] = _w(sum(r['seq']['ok'] for r in sub), len(sub)); out['reverse_forced_closure'] = _w(sum(r['seq_rev']['ok'] for r in sub), len(sub))
        out['reverse_default_closure_applicable_only'] = _w(sum(r['seq']['ok'] for r in app), len(app)); out['reverse_forced_closure_applicable_only'] = _w(sum(r['seq_rev']['ok'] for r in app), len(app))
    af = [r['alone_fails'] for r in rs]
    out['alone_all_fail'] = _w(sum(all(v_ is True for v_ in a_.values()) for a_ in af), n_); out['alone_none_fail'] = _w(sum(all(v_ is False for v_ in a_.values()) for a_ in af), n_)
    out['alone_some_fail_not_all'] = _w(sum((any(v_ is True for v_ in a_.values()) and not all(v_ is True for v_ in a_.values())) for a_ in af), n_)
    out['alone_unknown'] = _w(sum(any(v_ is None for v_ in a_.values()) for a_ in af), n_)
    return out
rows_all = list(COMPRES['rows'].values()); BYS = {s_: summarise([r for r in rows_all if r['stratum'] == s_]) for s_ in COMP_QUOTA}
clean_rows = list(COMPRES['clean'].values())
COMPRES_SUMMARY = dict(
    seed=COMP_SEED, protocol='docs/evidence/v7_composed_protocol.md', n_train_kept=sum(1 for e in COMP if e['split'] == 'train'), n_test_kept=len(TEST_COMP),
    kept_by_split_stratum={f'{sp_}|{s_}': sum(1 for e in COMP if e['split'] == sp_ and e['stratum'] == s_) for sp_ in ('train', 'test') for s_ in COMP_QUOTA}, quota_per_split_stratum=COMP_QUOTA,
    empty_or_short_strata={f'{sp_}|{s_}': dict(kept=sum(1 for e in COMP if e['split'] == sp_ and e['stratum'] == s_), quota=COMP_QUOTA[s_]) for sp_ in ('train', 'test') for s_ in COMP_QUOTA
                           if sum(1 for e in COMP if e['split'] == sp_ and e['stratum'] == s_) < COMP_QUOTA[s_]},
    overall=summarise(rows_all), by_stratum=BYS, generation_log=COMPLOG,
    clean_loss=dict(single_round_L1_heldout=GUARANTEE['heldout_clean_loss'], single_round_policy='mondrian_crc_0.005, all held-out clean episodes',
                    sequential_loop_sample_n=len(CLEAN_SEQ), eligible_n=len(CLEAN_CANDIDATES),
                    sequential_loop_subsample=_w(sum(r['lost'] for r in clean_rows), len(clean_rows)), sequential_loop_dispatched=_w(sum(r['rounds'] >= 1 for r in clean_rows), len(clean_rows)),
                    sequential_loop_mean_rounds=float(np.mean([r['rounds'] for r in clean_rows])) if clean_rows else None, bar=GATES['ALPHA']))
def _headline(S):
    o = S['overall']
    if not o.get('n'): return 'No held-out composed episodes were generated, so no composed-arm result exists.'
    f = lambda w_: f"{100 * w_['rate']:.1f}% [{100 * w_['ci'][0]:.1f}, {100 * w_['ci'][1]:.1f}] ({w_['k']}/{w_['n']})"
    cl = S['clean_loss']; rv = o.get('reverse_forced_closure'); dv = o.get('reverse_default_closure_same_episodes')
    return (f"On {o['n']} held-out composed episodes (seed {S['seed']}; strata short of quota: {len(S['empty_or_short_strata'])}), the retrained attributor named every cause at the family level in {f(o['both_causes_family_new'])} "
            f"(the single-fault-trained attributor: {f(o['both_causes_family_old'])}), with mean set-F1 {o['set_f1_family_new']:.3f} (old {o['set_f1_family_old']:.3f}); "
            f"sequential repair closed {f(o['sequential_closure'])} against {f(o['oracle_forward_closure'])} for oracle-forward repairs"
            + (f"; in the forced reverse-order subsample (n = {o['reverse_subsample_n']}) closure was {f(rv)} against {f(dv)} for the default order on the same episodes" if rv and dv else '')
            + f". Held-out clean loss was {100 * cl['single_round_L1_heldout']:.2f}% under the single-round policy and {f(cl['sequential_loop_subsample'])} under the sequential loop on a fixed clean subsample (bar {100 * cl['bar']:.1f}%).")
COMPRES_SUMMARY['headline'] = _headline(COMPRES_SUMMARY)
json.dump(COMPRES_SUMMARY, open(os.path.join(OUT, 'COMPOSED_RESULT.json'), 'w'), indent=1, default=str)
with open(os.path.join(OUT, 'composed_episodes.jsonl'), 'w') as fh_:
    for e in COMP: fh_.write(json.dumps(dict(comps=e['comps'], stratum=e['stratum'], split=e['split'], bid=e['bid'], src=e['src'], k=e['k'], alone_fails=e['alone_fails'], clean_h=e['clean_h'], q=e['st']['q'],
                                              eval=COMPRES['rows'].get(next((i_ for i_, x_ in enumerate(COMP) if x_ is e), -1))), default=str) + '\n')
log('COMPOSED HEADLINE', COMPRES_SUMMARY['headline'])
