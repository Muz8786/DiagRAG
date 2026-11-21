# %% [markdown]
# ## 11b. Composed-fault arm (v7), generation. Pre-registered in docs/evidence/v7_composed_protocol.md.
# Pairs (within-family, cross-family same letter, cross-letter) and triples of faults from the grounded and solved set are injected into base queries that NO single-fault episode uses.
# An episode is kept only if the clean pipeline succeeds and the composed state fails. For every kept episode each component is also run ALONE. The list COMP is separate from EPIS: the single-fault arms and their gates never see it.

# %%
COMP_SEED = int(os.environ.get('COMP_SEED', 51))   # fixed by the protocol; the override exists only for disposable development smoke tests
COMP_QUOTA = {'WITHIN_FAMILY': 20, 'QQ': 20, 'KK': 20, 'RR': 20, 'QK': 20, 'QR': 20, 'KR': 20, 'TRIPLE': 15}   # kept episodes per split and stratum
if os.environ.get('COMP_QUOTA_SCALE'): COMP_QUOTA = {k_: max(1, int(v_ * float(os.environ['COMP_QUOTA_SCALE']))) for k_, v_ in COMP_QUOTA.items()}   # development smoke tests only
COMP_SOLVED = [f_ for f_ in GROUNDED if f_ not in ('Q03', 'R26')]   # grounded (tier S or M) and solved in the v6 judged runs; Q03 (detector and repair FAIL) and R26 (THIN) are not
assert len(COMP_SOLVED) == 20, COMP_SOLVED
COMP_EXCL_FAULTS = {f_: ('quarantine tier N or P (not grounded)' if TIER[f_] in 'NP' else 'grounded but not solved in the v6 judged runs') for f_ in FAULTS if f_ not in COMP_SOLVED}
COMP_EXCL_FAULTS['C2'] = 'a composed fault itself (the single-fault arm of the original suite), not a component'
K_COMP = lambda comps: min(K_OF.get(f_, 5) for f_ in comps)
def comp_stratum(comps):
    if len(comps) == 3: return 'TRIPLE'
    a_, b_ = comps
    if FAMILY[a_] == FAMILY[b_]: return 'WITHIN_FAMILY'
    return a_[0] * 2 if a_[0] == b_[0] else ''.join(sorted((a_[0], b_[0]), key='QKR'.index))
def comp_pool(comps):
    s_ = set(POOL[comps[0]])
    for f_ in comps[1:]: s_ &= set(POOL[f_])
    return s_
COMP_PAIRS, COMP_PAIR_EXCL = collections.defaultdict(list), []
for i_, a_ in enumerate(COMP_SOLVED):
    for b_ in COMP_SOLVED[i_ + 1:]:
        if not comp_pool((a_, b_)): COMP_PAIR_EXCL.append(dict(comps=[a_, b_], stratum=comp_stratum((a_, b_)), reason=f'no common base-query source ({POOL[a_]} against {POOL[b_]})'))
        else: COMP_PAIRS[comp_stratum((a_, b_))].append((a_, b_))
for q_ in [f_ for f_ in COMP_SOLVED if f_[0] == 'Q']:
    for k_ in [f_ for f_ in COMP_SOLVED if f_[0] == 'K']:
        for r_ in [f_ for f_ in COMP_SOLVED if f_[0] == 'R']:
            if not comp_pool((q_, k_, r_)): COMP_PAIR_EXCL.append(dict(comps=[q_, k_, r_], stratum='TRIPLE', reason='no common base-query source'))
            else: COMP_PAIRS['TRIPLE'].append((q_, k_, r_))
COMP_EMPTY = {s_: 'no eligible pair in the grounded and solved set' for s_ in COMP_QUOTA if not COMP_PAIRS[s_]}
log('composed arm: eligible faults', COMP_SOLVED, '| eligible combinations per stratum', {s_: len(COMP_PAIRS[s_]) for s_ in COMP_QUOTA}, '| empty strata', COMP_EMPTY, '| combinations excluded for pool', len(COMP_PAIR_EXCL))

def comp_build(b, comps, seed_key):
    """Compose faults on base query b. Query faults chain on the evolving query (Q first); K and R faults act on the original base; two faults that set the same
    configuration knob to different values are a conflict and the combination is excluded. Returns (state, None, singles) or (None, reason, None)."""
    order = sorted(comps, key=lambda f_: 'QKR'.index(f_[0])); cur = b; st = S(b); knobs, docs, singles = {}, [], {}
    for f_ in order:
        sf = INJ[f_](cur if f_[0] == 'Q' else b, random.Random(f'{seed_key}|{f_}'))
        if sf is None: return None, f'injector not applicable: {f_}', None
        if f_[0] == 'Q': cur = dict(cur, q=sf['q']); st['q'] = sf['q']
        for k_, v_ in sf['cfg'].items():
            if v_ != DEFAULT[k_]:
                if k_ in knobs and knobs[k_] != v_: return None, f'configuration knob conflict: {k_}', None
                knobs[k_] = v_
        if sf['tenant'] != b['tenant']:
            if st['tenant'] != b['tenant'] and st['tenant'] != sf['tenant']: return None, 'tenant conflict', None
            st['tenant'] = sf['tenant']
        if sf['ov']: docs += list(sf['ov']['docs'])
        st['k'] = min(st['k'], sf['k']); singles[f_] = INJ[f_](b, random.Random(f'{seed_key}|{f_}'))
    c_ = dict(st['cfg']); c_.update(knobs); st['cfg'] = c_; st['ov'] = make_overlay(docs) if docs else None; st['meta'] = dict(combo=list(order), arm='composed')
    return st, None, singles

COMPST = RES.get('COMPST') or dict(ptr={'train': 0, 'test': 0}, done=False, COMP=[], acc=collections.Counter(), att=collections.Counter(), pair_acc=collections.Counter(),
                                   pair_att=collections.Counter(), log=collections.defaultdict(collections.Counter), seen=set(), n_overlap={}, n_cleanfail={})
if not COMPST['done']:
    USED_SINGLE = {e['bid'] for e in EPIS if e['fault'] != 'NONE'}
    for sp_ in ('train', 'test'):
        allb = [b for b in BASE if b['split'] == sp_]
        COMPST['n_overlap'][sp_] = sum(1 for b in allb if b['bid'] in USED_SINGLE)
        free = [b for b in allb if b['bid'] not in USED_SINGLE]; COMPST['n_cleanfail'][sp_] = sum(1 for b in free if not (b['h5'] or b['h1']))
        cand = sorted([b for b in free if b['h5'] or b['h1']], key=lambda b: hashlib.md5(f'{COMP_SEED}|order|{b["bid"]}'.encode()).hexdigest())
        L = COMPST['log'][sp_]
        while COMPST['ptr'][sp_] < len(cand) and any(COMPST['acc'][(sp_, s_)] < COMP_QUOTA[s_] and COMP_PAIRS[s_] for s_ in COMP_QUOTA):
            if COMPST['ptr'][sp_] % 15 == 0: maybe_stop('composed_generation')   # checked BEFORE the pointer moves, so a resumed run processes exactly the same base queries as an uninterrupted one
            b = cand[COMPST['ptr'][sp_]]; COMPST['ptr'][sp_] += 1
            opts = []
            for i_, s_ in enumerate(COMP_QUOTA):
                if COMPST['acc'][(sp_, s_)] >= COMP_QUOTA[s_]: continue
                pl = [p_ for p_ in COMP_PAIRS[s_] if b['src'] in comp_pool(p_) and (b['h1'] if K_COMP(p_) == 1 else b['h5'])]
                if pl: opts.append((COMPST['acc'][(sp_, s_)] / COMP_QUOTA[s_], i_, s_, pl))
            if not opts: L['skipped base query: no open stratum has a combination for source ' + b['src'] + ' and its clean outcome'] += 1; continue
            _, _, s_, pl = min(opts, key=lambda o_: o_[:2])
            live = [p_ for p_ in pl if not (COMPST['pair_att'][(sp_, p_)] >= 12 and COMPST['pair_acc'][(sp_, p_)] == 0)]   # a combination with 12 attempts and no kept episode is stuck
            comps = min(live or pl, key=lambda p_: (COMPST['pair_acc'][(sp_, p_)], COMPST['pair_att'][(sp_, p_)], pl.index(p_)))
            COMPST['pair_att'][(sp_, comps)] += 1; COMPST['att'][(sp_, s_)] += 1; k_ = K_COMP(comps)
            st, why, singles = comp_build(b, comps, f'{COMP_SEED}|{b["bid"]}')
            if st is None: L[f'excluded [{s_}]: {why}'] += 1; continue
            sig = hashlib.md5(repr((b['bid'], st['q'], sorted((k2, str(v2)) for k2, v2 in st['cfg'].items() if k2 != 'emb_override'), st['ov']['text'] if st['ov'] else None)).encode()).hexdigest()
            if sig in COMPST['seen']: L[f'excluded [{s_}]: duplicate state'] += 1; continue
            COMPST['seen'].add(sig); tr = run(st)
            if succ(tr, st['gold'], k_): L[f'excluded [{s_}]: composed state does not fail (easy)'] += 1; continue
            alone = {f_: (None if singles[f_] is None else (not succ(run(singles[f_]), singles[f_]['gold'], k_))) for f_ in comps}   # True means the fault ALONE also fails
            COMPST['acc'][(sp_, s_)] += 1; COMPST['pair_acc'][(sp_, comps)] += 1
            COMPST['COMP'].append(dict(arm='composed', comps=list(comps), stratum=s_, bid=b['bid'], split=sp_, src=b['src'], st=st, feats=features(tr), k=k_, alone_fails=alone,
                                       clean_h=bool(b['h1'] if k_ == 1 else b['h5'])))
    COMPST['done'] = True; save_ckpt('composed_done')
COMP = COMPST['COMP']
COMPLOG = dict(seed=COMP_SEED, quota=COMP_QUOTA, eligible_faults=COMP_SOLVED, excluded_faults=COMP_EXCL_FAULTS, empty_strata=COMP_EMPTY, combinations_per_stratum={s_: [list(p_) for p_ in COMP_PAIRS[s_]] if s_ != 'TRIPLE' else len(COMP_PAIRS[s_]) for s_ in COMP_QUOTA},
               combinations_excluded_pool=COMP_PAIR_EXCL, base_queries_overlapping_single_fault_arms=COMPST['n_overlap'], base_queries_clean_fails=COMPST['n_cleanfail'],
               attempts={f'{k_[0]}|{k_[1]}': v_ for k_, v_ in COMPST['att'].items()}, kept={f'{k_[0]}|{k_[1]}': v_ for k_, v_ in COMPST['acc'].items()},
               exclusion_reasons={sp_: dict(c_) for sp_, c_ in COMPST['log'].items()}, kept_per_combination={f'{k_[0]}|{"+".join(k_[1])}': v_ for k_, v_ in COMPST['pair_acc'].items()})
log('composed episodes kept', collections.Counter((e['split'], e['stratum']) for e in COMP)); log('composed exclusions', COMPLOG['exclusion_reasons'])

def comp_rows(split):
    """Composed TRAIN rows for the retrained attributor: each kept episode contributes one row per component, labelled with that component's fault. Never called for the test split."""
    assert split == 'train'
    rows = [(e['feats'], f_) for e in COMP if e['split'] == 'train' for f_ in e['comps']]
    nf_ = len(sorted(EPIS[0]['feats']))
    return np.array([[fe[k_] for k_ in sorted(EPIS[0]['feats'])] for fe, _ in rows], dtype=np.float32).reshape(len(rows), nf_), np.array([f_ for _, f_ in rows], dtype=object)
