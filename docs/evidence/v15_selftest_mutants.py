"""v15 S (diagnostic self-test) and M (blind code-mutant faults); docs/evidence/v15_selftest_mutants_protocol.md.
Executed INSIDE the Kaggle notebook after the frozen v6 code has run up to its U1 stage on a resumed judged checkpoint; `G` is that namespace.
ROLE = 'dev' (seed 55, development draws, dev mutant half) or 'heldout' (seeds 71-73, held-out draws, held-out mutant half). TRIAL=1 limits the work.
Nothing in the frozen pipeline is changed except, temporarily and one at a time, the mutated retrieval function (restored after each mutant)."""
import ast, collections, hashlib, itertools, json, math, os, random, signal, time
import numpy as np

RANDOM_FAULTS = {'R01', 'R07', 'R25', 'K04', 'R13', 'R06'}   # faults whose affected documents/terms change from draw to draw
SYS = ['R01', 'R03', 'R05', 'R06', 'R07', 'R10', 'R11', 'R13', 'R15', 'R19', 'R22', 'R23', 'R24', 'R25', 'K04']
COMP = dict(R01='DENSE', R03='DENSE', R07='DENSE', R10='DENSE', R11='DENSE', R15='DENSE', R25='DENSE', K04='DENSE', R13='BM25', R22='FUSION',
            R05='RERANK', R19='RERANK', R24='RERANK', R23='SERVING', R06='FILTERS')
KNOBS = dict(R01={'mask'}, R03={'enc'}, R05={'ce'}, R06={'route'}, R07={'shift'}, R10={'q_noise'}, R11={'enc'}, R13={'sparse_shift'}, R15={'nprobe'},
             R19={'depth'}, R22={'fusion'}, R23={'result_cap'}, R24={'ce_trunc'}, R25={'nonfinite'}, K04={'emb_override'})
P = dict(POOL=600, A=100, B=40, NDICT=2, NDICT_RANDOM=4, T=3, EPS=0.002, KAPPA=3.0, TRAFFIC=100, PAIR_TRAFFIC=40, SCREEN=40, HARM_FRAC=0.10, ALARM_P=0.01, MAXM=400, TIMEOUT=90)
TARGETS = ['run', 'bm25_scores', 'q_terms', 'topn', 'dense_all', 'ce_scores', 'enc_q']
FCOMP = dict(bm25_scores='BM25', q_terms='BM25', dense_all='DENSE', enc_q='DENSE', ce_scores='RERANK', topn='SHARED')
RUN_MARKERS = [('m = M(ov)', 'DENSE'), ('ok = np.ones', 'FILTERS'), ("if c['mask'] is not None", 'DENSE'), ('ss = bm25_scores', 'BM25'),
               ("if c['pfilter'] is not None and c['post_filter']", 'FILTERS'), ("if c['refresh']", 'DENSE'), ("if c['fusion'] == 'rrf'", 'FUSION'),
               ("if c['quality']", 'CONTENT'), ("depth = fused[:c['depth']]", 'RERANK'), ("final = order[:CFG['K_FINAL']]", 'SERVING'), ('return dict(', 'TELEMETRY')]
CMP = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt, ast.Eq: ast.NotEq, ast.NotEq: ast.Eq}
BIN = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Div, ast.Div: ast.Mult}


class _TO(Exception): pass
def _alarm(*a): raise _TO()


def main(G, OUT, TRIAL, ROLE):
    assert ROLE in ('dev', 'heldout'); os.makedirs(OUT, exist_ok=True); t0 = time.time(); log = lambda *a: print(f'[{time.time() - t0:6.0f}s]', *a, flush=True)
    if TRIAL: P.update(POOL=40, A=10, B=6, NDICT_RANDOM=2, TRAFFIC=8, PAIR_TRAFFIC=4, SCREEN=8, MAXM=6)
    run, succ, features, dispatch_v3, proba, apply_v3 = G['run'], G['succ'], G['features'], G['dispatch_v3'], G['proba'], G['apply_v3']
    REP, GROUP, GROUP_REPAIR, universal, FAMILY = G['REP'], G['GROUP'], G['GROUP_REPAIR'], G['universal'], G['FAMILY']
    LAMS, GATES, stratum, mkcfg, N, E, BASE, TAU = G['LAMS'], G['GATES'], G['stratum'], G['mkcfg'], G['N'], G['E'], G['BASE'], G['TAU_NONE_G']
    A_ = GATES['ALPHA']; ESCI_PART, PARTS = G['ESCI_PART'], G['PARTS']
    rnd = lambda *tag: random.Random('|'.join(map(str, tag)))
    R = dict(trial=bool(TRIAL), role=ROLE, seed=str(G['CFG']['SEED']), params=dict(P), note='frozen v6 executed on a judged checkpoint; measurements only')

    def sys_cfg(f, r):
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
    def st_of(b, over, reps=()):
        st = dict(q=b['q'], tenant=b['tenant'], cfg=mkcfg(**over), ov=None, gold=b['gold'], k=5, meta={})
        for g in sorted(reps, key=lambda g: 'QKR'.index('R' if g == 'GR' else GROUP[g])):
            st = (GROUP_REPAIR['R'] if g == 'GR' else REP[g])(st, run(st))
        return st
    ok = lambda b, over, reps=(): bool(succ(run(st_of(b, over, reps)), b['gold'], 5))

    esci_tr = [b for b in BASE if b['src'] == 'esci' and b['split'] == 'train' and b['h5']]
    esci_te = [b for b in BASE if b['src'] == 'esci' and b['split'] == 'test']
    pool = rnd('pool').sample(esci_tr, min(len(esci_tr), P['POOL']))
    pool = [b for b in pool if ok(b, {})]   # clean pass check on this pipeline
    traffic = rnd('traffic').sample(esci_te, min(len(esci_te), P['TRAFFIC']))
    screen = rnd('screen').sample([b for b in esci_te if b['h5']], P['SCREEN'])
    log('pool', len(pool), 'traffic', len(traffic), 'screen', len(screen))

    # ---- dictionary (always from 'dict' draws, never the evaluated draws) and battery selection
    DI = {f: [sys_cfg(f, rnd('dict', f, j)) for j in range(P['NDICT_RANDOM'] if f in RANDOM_FAULTS else P['NDICT'])] for f in SYS}
    Q = {f: np.mean([[not ok(b, over) for b in pool] for over in DI[f]], axis=0) for f in SYS}
    log('dictionary built', {f: round(float(Q[f].mean()), 3) for f in SYS})
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
    BAT = A_idx + B_idx; probes = [pool[i] for i in BAT]; posA = list(range(len(A_idx))); posAll = list(range(len(BAT)))
    QB = {f: np.clip(Q[f][BAT], 0.01, 0.99) for f in SYS}
    R['battery'] = dict(size=len(BAT), random_part=len(A_idx), diagnostic_part=len(B_idx), undetected_faults=[f for f in SYS if det[f] == 0],
                        indistinct_pairs=[list(pg) for pg in pairs_all if sep[pg] == 0])
    log('battery', R['battery'])

    def decode(y, faults, pos):
        y = np.asarray(y, bool)
        def ll(H):
            pk = np.full(len(pos), 1 - P['EPS'])
            for f in H: pk = pk * (1 - QB[f][pos])
            pf = 1 - pk; return float(np.sum(np.where(y, np.log(pf), np.log(1 - pf)))) - P['KAPPA'] * len(H)
        hyps = ([] if y.any() else [()]) + [(f,) for f in faults] + [pg for pg in itertools.combinations(faults, 2)]
        return max(hyps, key=ll) if hyps else ()
    def selftest(over, faults, pos, max_tries=5):
        """Repair and retest: decode, apply the decoded repairs to the probes, keep them only if fewer probes fail; at most max_tries decodes, then rollback."""
        pr = [probes[k] for k in pos]; a = time.time(); nruns = len(pr)
        y = [not ok(b, over) for b in pr]; detected = any(y); named, excluded, tries = [], set(), 0
        while any(y) and tries < max_tries:
            H = decode(y, [f for f in faults if f not in named and f not in excluded], pos); tries += 1
            if not H: break
            y2 = [not ok(b, over, named + list(H)) for b in pr]; nruns += len(pr)
            if sum(y2) < sum(y): named, y = named + list(H), y2
            else: excluded |= set(H)
        if not any(y): return dict(named=named, verified=True, fallback=False, detected=detected, rounds=tries, runs=nruns, sec=time.time() - a)
        y = [not ok(b, over, named + ['GR']) for b in pr]; nruns += len(pr)
        return dict(named=named, verified=not any(y), fallback=True, detected=detected, rounds=tries, runs=nruns, sec=time.time() - a)
    fam = lambda l: FAMILY.get(l, l)
    def traffic_eval(over, res, qs):
        reps_b = list(res['named']) + (['GR'] if res['fallback'] else []); rows = []
        for b in qs:
            stf = st_of(b, over); trf = run(stf); hf = bool(succ(trf, b['gold'], 5))
            hb = ok(b, over, reps_b) if (reps_b and res['detected']) else hf
            fe = features(trf); reps, s = dispatch_v3(proba(fe), fe); lam = LAMS[A_][stratum(fe, 'esci')]
            hl = bool(succ(run(apply_v3(stf, reps)), b['gold'], 5)) if s >= lam else hf
            hu = bool(succ(run(universal(stf)), b['gold'], 5))
            rows.append(dict(h0=bool(b['h5']), hf=hf, hb=hb, hl=hl, hu=hu, labs=[l for l, _ in reps] if s >= lam else []))
        br = [r for r in rows if r['h0'] and not r['hf']]; it = [r for r in rows if r['h0'] and r['hf']]
        cl = lambda k: (float(np.mean([r[k] for r in br])) if br else None); hm = lambda k: (float(np.mean([not r[k] for r in it])) if it else None)
        labs = collections.Counter(fam(l) for r in rows for l in r['labs'])
        return dict(n=len(rows), broken=len(br), intact=len(it), closure=dict(selftest=cl('hb'), loop=cl('hl'), universal=cl('hu')),
                    harm=dict(selftest=hm('hb'), loop=hm('hl'), universal=hm('hu')), top_families=[l for l, _ in labs.most_common(2)])

    # ---- S1: single system faults (evaluated draws), with and without the fault in the dictionary
    tagE = 'deveval' if ROLE == 'dev' else 'heldout'; nI = 1 if TRIAL else 3
    rowsS = []; fS = open(os.path.join(OUT, 'S_single.jsonl'), 'w')
    for f in (SYS[:3] if TRIAL else SYS):
        for j in range(nI):
            over = sys_cfg(f, rnd(tagE, f, j)); res = selftest(over, SYS, posAll); lofo = selftest(over, [g for g in SYS if g != f], posA)
            r = dict(fault=f, inst=j, detected=res['detected'], named=res['named'], exact=f in res['named'], family=FAMILY[f] in {FAMILY[g] for g in res['named']}, component=COMP[f] in {COMP[g] for g in res['named']},
                     verified=res['verified'], fallback=res['fallback'], rounds=res['rounds'], runs=res['runs'], sec=res['sec'],
                     lofo_named=lofo['named'], lofo_family=FAMILY[f] in {FAMILY[g] for g in lofo['named']}, lofo_component=COMP[f] in {COMP[g] for g in lofo['named']}, lofo_verified=lofo['verified'], lofo_fallback=lofo['fallback'])
            if j == 0:
                r['traffic'] = traffic_eval(over, res, traffic); r['traffic_lofo'] = traffic_eval(over, lofo, traffic)
                r['agg_dispatcher_named'] = bool(r['traffic']['top_families'][:1] == [fam(f)])
            rowsS.append(r); fS.write(json.dumps(r, default=str) + '\n'); fS.flush()
        log('S single', f, {k: rowsS[-1][k] for k in ('detected', 'named', 'verified', 'lofo_named', 'lofo_verified')})
    # ---- S2: pairs of system faults (all pairs that do not set the same knob)
    prs = [pg for pg in pairs_all if not (KNOBS[pg[0]] & KNOBS[pg[1]])]
    if TRIAL: prs = prs[:3]
    rowsP = []; fP = open(os.path.join(OUT, 'S_pairs.jsonl'), 'w')
    for (f, g) in prs:
        over = dict(sys_cfg(f, rnd(tagE + 'pair', f, g, 0)), **sys_cfg(g, rnd(tagE + 'pair', f, g, 1)))
        res = selftest(over, SYS, posAll); tv = traffic_eval(over, res, traffic[:P['PAIR_TRAFFIC']])
        r = dict(pair=[f, g], same_group=GROUP[f] == GROUP[g], detected=res['detected'], named=res['named'], both_exact=f in res['named'] and g in res['named'],
                 both_component={COMP[f], COMP[g]} <= {COMP[h] for h in res['named']}, both_family={FAMILY[f], FAMILY[g]} <= {FAMILY[h] for h in res['named']}, verified=res['verified'], fallback=res['fallback'], runs=res['runs'],
                 traffic=tv, agg_dispatcher_both=set(tv['top_families']) >= {fam(f), fam(g)})
        rowsP.append(r); fP.write(json.dumps(r, default=str) + '\n'); fP.flush()
    log('S pairs done', len(rowsP))
    m = lambda xs, k: (float(np.mean([bool(x[k]) for x in xs])) if xs else None)
    tr0 = [r for r in rowsS if 'traffic' in r]
    def tmean(rows, key, sub, who): v = [r[key][sub][who] for r in rows if r[key][sub][who] is not None]; return float(np.mean(v)) if v else None
    R['S'] = dict(single=dict(n=len(rowsS), detected=m(rowsS, 'detected'), exact=m(rowsS, 'exact'), family=m(rowsS, 'family'), component=m(rowsS, 'component'), verified=m(rowsS, 'verified'),
                              fallback=m(rowsS, 'fallback'), agg_dispatcher_named=m(tr0, 'agg_dispatcher_named'),
                              mean_runs=float(np.mean([r['runs'] for r in rowsS])), median_sec=float(np.median([r['sec'] for r in rowsS])),
                              traffic_closure={w: tmean(tr0, 'traffic', 'closure', w) for w in ('selftest', 'loop', 'universal')},
                              traffic_harm={w: tmean(tr0, 'traffic', 'harm', w) for w in ('selftest', 'loop', 'universal')}),
                unseen=dict(family=m(rowsS, 'lofo_family'), component=m(rowsS, 'lofo_component'), verified=m(rowsS, 'lofo_verified'), fallback=m(rowsS, 'lofo_fallback'),
                            traffic_closure={w: tmean(tr0, 'traffic_lofo', 'closure', w) for w in ('selftest', 'loop', 'universal')},
                            traffic_harm={w: tmean(tr0, 'traffic_lofo', 'harm', w) for w in ('selftest', 'loop', 'universal')}),
                pairs=dict(n=len(rowsP), n_same_group=sum(r['same_group'] for r in rowsP), detected=m(rowsP, 'detected'), both_exact=m(rowsP, 'both_exact'),
                           both_component=m(rowsP, 'both_component'), both_family=m(rowsP, 'both_family'), both_family_same_group=m([r for r in rowsP if r['same_group']], 'both_family'), both_exact_same_group=m([r for r in rowsP if r['same_group']], 'both_exact'),
                           verified=m(rowsP, 'verified'), agg_dispatcher_both=m(rowsP, 'agg_dispatcher_both'),
                           traffic_closure={w: tmean(rowsP, 'traffic', 'closure', w) for w in ('selftest', 'loop', 'universal')},
                           traffic_harm={w: tmean(rowsP, 'traffic', 'harm', w) for w in ('selftest', 'loop', 'universal')}))
    log('S', R['S'])

    # ---- M: blind code mutants of the retrieval path
    SRC = open(G['__file__'], encoding='utf-8').read(); tree = ast.parse(SRC)
    FN = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in TARGETS}
    def pts_of(ft):
        out = []
        for node in ast.walk(ft):
            if isinstance(node, ast.Compare):
                out += [('cmp', node, k) for k, op in enumerate(node.ops) if type(op) in CMP]
            elif isinstance(node, ast.BinOp) and type(node.op) in BIN: out.append(('bin', node, 0))
            elif isinstance(node, ast.Constant) and not isinstance(node.value, str):
                v = node.value
                if isinstance(v, bool): out.append(('bool', node, 0))
                elif isinstance(v, int) and abs(v) < 10**6: out += [('int+', node, 0), ('int-', node, 0)]
                elif isinstance(v, float): out += [('fhalf', node, 0), ('fdouble', node, 0)]
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub): out.append(('neg', node, 0))
            elif isinstance(node, ast.If): out.append(('ifnot', node, 0))
            elif isinstance(node, ast.BoolOp): out.append(('andor', node, 0))
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('min', 'max'): out.append(('minmax', node, 0))
            elif isinstance(node, ast.Slice) and node.upper is not None and not isinstance(node.upper, ast.Constant): out += [('slice+', node, 0), ('slice-', node, 0)]
        return out
    MUT = []
    for name, node in FN.items():
        seg = ast.get_source_segment(SRC, node); base_line = node.lineno
        marks = []
        if name == 'run':
            for k, ln in enumerate(seg.splitlines()):
                for mk, cp in RUN_MARKERS:
                    if mk in ln: marks.append((base_line + k, cp))
        for k, (kind, nd, sub) in enumerate(pts_of(ast.parse(seg))):
            line = base_line + nd.lineno - 1; pid = f'{name}|{line}|{nd.col_offset}|{kind}|{sub}|{k}'
            half = 'dev' if int(hashlib.md5(pid.encode()).hexdigest()[0], 16) < 8 else 'heldout'
            comp = FCOMP.get(name) or next((cp for ml, cp in sorted(marks, reverse=True) if ml <= line), 'OTHER')
            MUT.append(dict(pid=pid, fn=name, k=k, kind=kind, line=line, half=half, comp=comp, seg=seg))
    R['M_points'] = dict(total=len(MUT), by_half=dict(collections.Counter(x['half'] for x in MUT)), by_fn=dict(collections.Counter(x['fn'] for x in MUT)))
    mine = sorted([x for x in MUT if x['half'] == ROLE], key=lambda x: hashlib.md5(x['pid'].encode()).hexdigest())[:P['MAXM']]
    log('mutation points', R['M_points'], 'evaluated', len(mine))
    def mutant_src(x):
        t = ast.parse(x['seg']); kind, nd, sub = pts_of(t)[x['k']]
        if kind == 'cmp': nd.ops[sub] = CMP[type(nd.ops[sub])]()
        elif kind == 'bin': nd.op = BIN[type(nd.op)]()
        elif kind == 'bool': nd.value = not nd.value
        elif kind == 'int+': nd.value = nd.value + 1
        elif kind == 'int-': nd.value = nd.value - 1
        elif kind == 'fhalf': nd.value = nd.value * 0.5
        elif kind == 'fdouble': nd.value = nd.value * 2.0
        elif kind == 'neg': nd.op = ast.UAdd()
        elif kind == 'ifnot': nd.test = ast.UnaryOp(op=ast.Not(), operand=nd.test)
        elif kind == 'andor': nd.op = ast.Or() if isinstance(nd.op, ast.And) else ast.And()
        elif kind == 'minmax': nd.func = ast.Name(id='max' if nd.func.id == 'min' else 'min', ctx=ast.Load())
        elif kind in ('slice+', 'slice-'): nd.upper = ast.BinOp(left=nd.upper, op=ast.Add() if kind == 'slice+' else ast.Sub(), right=ast.Constant(1))
        return ast.unparse(ast.fix_missing_locations(t))
    ORIG = {n: G[n] for n in TARGETS}; CACHES = {'enc_q': '_QC', 'ce_scores': '_CEC'}
    def clean_view(b):
        tr = run(dict(q=b['q'], tenant=b['tenant'], cfg=mkcfg(), ov=None)); fe = features(tr); s = dispatch_v3(proba(fe), fe)[1]
        return dict(s=float(s), ce1=float(np.max(tr['ce'])) if len(tr['ce']) else 0.0)
    CV = {b['bid']: clean_view(b) for b in traffic}
    def signp(bm, cm):
        n = bm + cm
        return 1.0 if n == 0 else float(sum(math.comb(n, i) for i in range(bm, n + 1)) / 2 ** n)
    rowsM = []; fM = open(os.path.join(OUT, 'M_mutants.jsonl'), 'w'); signal.signal(signal.SIGALRM, _alarm)
    for n_, x in enumerate(mine):
        r = dict(pid=x['pid'], fn=x['fn'], kind=x['kind'], comp=x['comp'])
        saved = {}
        try:
            code_ = compile(mutant_src(x), f"mutant:{x['pid']}", 'exec')
            if x['fn'] in CACHES: saved[CACHES[x['fn']]] = G[CACHES[x['fn']]]; G[CACHES[x['fn']]] = {}
            exec(code_, G); signal.alarm(P['TIMEOUT'])
            fails = sum(not bool(succ(run(dict(q=b['q'], tenant=b['tenant'], cfg=mkcfg(), ov=None)), b['gold'], 5)) for b in screen); signal.alarm(0)
            r['screen_fail'] = fails / len(screen); r['status'] = 'harmful' if r['screen_fail'] >= P['HARM_FRAC'] else 'harmless'
            if r['status'] == 'harmful':
                signal.alarm(P['TIMEOUT'] * 6)
                y = [not bool(succ(run(dict(q=b['q'], tenant=b['tenant'], cfg=mkcfg(), ov=None)), b['gold'], 5)) for b in probes]
                H = decode(y, SYS, posAll); r.update(selftest_alarm=any(y), probe_fail=float(np.mean(y)), decoded=list(H), decoded_comp=sorted({COMP[h] for h in H}))
                bm = cm = bce = cce = 0; tel_err = False
                for b in traffic:
                    tr = run(dict(q=b['q'], tenant=b['tenant'], cfg=mkcfg(), ov=None))
                    try: fe = features(tr); s = float(dispatch_v3(proba(fe), fe)[1])
                    except Exception: tel_err = True; continue
                    f1, f0 = s >= TAU, CV[b['bid']]['s'] >= TAU; bm += f1 and not f0; cm += f0 and not f1
                    c1 = float(np.max(tr['ce'])) if len(tr['ce']) else 0.0; bce += c1 < CV[b['bid']]['ce1'] - 1e-6; cce += c1 > CV[b['bid']]['ce1'] + 1e-6
                signal.alarm(0)
                r.update(telemetry_p=signp(bm, cm), telemetry_alarm=bool(tel_err or signp(bm, cm) < P['ALARM_P']), telemetry_error=tel_err,
                         ce_drop_p=signp(bce, cce), ce_drop_alarm=bool(signp(bce, cce) < P['ALARM_P']))
                r['either_alarm'] = bool(r['selftest_alarm'] or r['telemetry_alarm'])
                r['component_ok'] = (x['comp'] in r['decoded_comp']) if x['comp'] in ('DENSE', 'BM25', 'FUSION', 'RERANK', 'SERVING', 'FILTERS') else None
        except _TO: r['status'] = 'timeout'
        except Exception as ex: r['status'] = 'crash'; r['error'] = repr(ex)[:120]
        finally:
            signal.alarm(0)
            for nm, fn in ORIG.items(): G[nm] = fn
            for k_, v_ in saved.items(): G[k_] = v_
        rowsM.append(r); fM.write(json.dumps(r, default=str) + '\n'); fM.flush()
        if n_ % 25 == 0: log('M', n_, 'of', len(mine), collections.Counter(z['status'] for z in rowsM))
    H_ = [r for r in rowsM if r['status'] == 'harmful']; cmp_ = [r for r in H_ if r.get('component_ok') is not None]
    R['M'] = dict(evaluated=len(rowsM), status=dict(collections.Counter(r['status'] for r in rowsM)), harmful=len(H_),
                  detected_selftest=m(H_, 'selftest_alarm'), detected_telemetry=m(H_, 'telemetry_alarm'), detected_either=m(H_, 'either_alarm'),
                  detected_ce_drop_baseline=m(H_, 'ce_drop_alarm'), component_ok=m(cmp_, 'component_ok'), n_component_scored=len(cmp_),
                  by_component={c: dict(n=sum(r['comp'] == c for r in H_), selftest=m([r for r in H_ if r['comp'] == c], 'selftest_alarm'),
                                        telemetry=m([r for r in H_ if r['comp'] == c], 'telemetry_alarm')) for c in sorted({r['comp'] for r in H_})},
                  median_probe_fail=float(np.median([r['probe_fail'] for r in H_])) if H_ else None,
                  acceptance_sampling_bound=f"a fault breaking a share h of working queries is missed by all {len(posA)} random probes with probability (1-h)^{len(posA)}")
    log('M', R['M'])
    json.dump(R, open(os.path.join(OUT, 'RESULT.json'), 'w'), indent=1, default=str)
    print(json.dumps({k: v for k, v in R.items()}, indent=1, default=str)[:15000])
