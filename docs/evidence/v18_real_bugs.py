"""v18: retrieval bugs reproduced from public issue reports, on the main stack (docs/evidence/v18_real_bugs_protocol.md).
Executed INSIDE the Kaggle notebook after the frozen v6 code has run up to its U1 stage on a resumed judged checkpoint; `G` is that namespace.
Each bug is a patch of the frozen retrieval code (code bugs) or a configuration (config bugs), applied system-wide, then measured on natural traffic:
self-test detection and stage localization (100 random probes with known answers), verified rollback of the localized component, per-query telemetry
alarm, the frozen deployed loop and the universal repair. The original code is restored after every bug. TRIAL=1 limits the work."""
import collections, hashlib, json, math, os, random, time
import numpy as np

BUGS = [
    dict(id='B1', src='langgenius/dify#6097; intfloat/e5 model card FAQ', what='query instruction prefix not sent to the encoder', stage='DENSE', fn='enc_q',
         patch=[("s = CFG['QPROMPT'] + q", "s = q")]),
    dict(id='B2', src='dorianbrown/rank_bm25#50; mem0ai/mem0#4884; mastra-ai/mastra#25928', what='query tokenized differently from the index (whitespace split, no normalization)',
         stage='BM25', fn='q_terms', patch=[("ids = [VOC[t] for t in tok(q) if t in VOC]", "ids = [VOC[t] for t in q.split() if t in VOC]")]),
    dict(id='B3', src='langchain-ai/langchain#37046', what='rank fusion accumulates the scores of chunks sharing one source id', stage='FUSION', fn='run',
         patch=[("fs = collections.defaultdict(float)\n        for lst in (dtop, stop):\n            for r_, i in enumerate(lst): fs[int(i)] += 1.0 / (CFG['RRF_K'] + r_ + 1)",
                 "fs = collections.defaultdict(float); _src = {}\n        for lst in (dtop, stop):\n            for r_, i in enumerate(lst): fs[_src.setdefault(dparent(int(i), ov), int(i))] += 1.0 / (CFG['RRF_K'] + r_ + 1)")]),
    dict(id='B4', src='milvus-io/milvus#53672', what='reranker scores assigned to the wrong documents when one document is not answered', stage='RERANK', fn='run',
         patch=[("ce = ce_scores(q, [dkey(i, ov) for i in depth], texts, c['ce_trunc'])",
                 "ce = ce_scores(q, [dkey(i, ov) for i in depth], texts, c['ce_trunc']); ce = np.concatenate([ce[:len(ce) // 2], ce[len(ce) // 2 + 1:], ce[-1:] * 0 + ce.min() - 1]) if len(ce) > 1 else ce")]),
    dict(id='B5', src='getzep/graphiti#1720', what='reranked list sorted ascending instead of descending', stage='RERANK', fn='run',
         patch=[("order = [depth[j] for j in np.argsort(-ce, kind='stable')]", "order = [depth[j] for j in np.argsort(ce, kind='stable')]")]),
    dict(id='B6', src='castorini/pygaggle#67', what='reranker runs but its order is not applied', stage='RERANK', fn='run',
         patch=[("order = [depth[j] for j in np.argsort(-ce, kind='stable')]", "order = list(depth)")]),
    dict(id='B7', src='run-llama/llama_index QueryFusionRetriever cache issue (reported 2026-10-03)', what='shared state: scores of the previous query reused by the next query',
         stage='DENSE', fn='run', patch=[("ds = dense_all(qv)", "ds = _V18_LAST.get('ds', dense_all(qv)); _V18_LAST['ds'] = dense_all(qv)")]),
    dict(id='B8', src='facebookresearch/faiss#600', what='IVF index searched with the default nprobe = 1', stage='DENSE', cfg=dict(nprobe=1), designed='R15'),
    dict(id='B9', src='jenkinsci/resources-ai-chatbot-plugin#542', what='BM25 and cosine scores added on their raw scales', stage='FUSION', cfg=dict(fusion='raw'), designed='R22'),
]
STAGE_KNOBS = dict(DENSE=['nprobe', 'enc', 'q_noise', 'mask', 'shift', 'emb_override', 'nonfinite'], BM25=['sparse_shift'], FUSION=['fusion'],
                   RERANK=['depth', 'ce', 'ce_trunc'], SERVING=['result_cap'], FILTERS=['route', 'tenant_filter', 'validity', 'post_filter'])
STG = ['D', 'S', 'F', 'O', 'V']


def main(G, OUT, TRIAL):
    os.makedirs(OUT, exist_ok=True); t0 = time.time(); log = lambda *a: print(f'[{time.time() - t0:6.0f}s]', *a, flush=True)
    import ast
    run0, succ, features, mkcfg, CFG = G['run'], G['succ'], G['features'], G['mkcfg'], G['CFG']
    dispatch_v3, proba, apply_v3, REP, NAT_RULES, LAMS, GATES, stratum, universal = G['dispatch_v3'], G['proba'], G['apply_v3'], G['REP'], G['NAT_RULES'], G['LAMS'], G['GATES'], G['stratum'], G['universal']
    rep_QLEX, CENS, NAT3, gold_set, BY_PKEY, BASE, TAU = G['rep_QLEX'], G['CENS'], G['NAT3'], G['gold_set'], G['BY_PKEY'], G['BASE'], G['TAU_NONE_G']
    rnd = lambda *tag: random.Random('|'.join(map(str, tag)))
    SRC = open(G['__file__'], encoding='utf-8').read(); tree = ast.parse(SRC); FN = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    ORIG = {n: G[n] for n in ('run', 'enc_q', 'q_terms', 'dense_all', 'bm25_scores')}; G['_V18_LAST'] = {}
    R = dict(trial=bool(TRIAL), seed=str(CFG['SEED']), bugs=[{k: v for k, v in b.items() if k != 'patch'} for b in BUGS])
    # natural traffic (never-examined ESCI queries, as N1), probes (train clean successes), telemetry traffic (test queries)
    nat = sorted(NAT3, key=lambda q: hashlib.md5(('v18|' + q).encode()).hexdigest())[:(30 if TRIAL else 600)]
    def nat_st(q, over):
        r = CENS[q]; return dict(q=q, tenant='ALL', cfg=mkcfg(**over), ov=None, gold=gold_set([j for p_ in r['pids'] for j in BY_PKEY[p_]]), k=5, meta={})
    esci_tr = [b for b in BASE if b['src'] == 'esci' and b['split'] == 'train' and b['h5']]; te = [b for b in BASE if b['src'] == 'esci' and b['split'] == 'test']
    probes = rnd('v18probes').sample(esci_tr, 20 if TRIAL else 100); traffic = rnd('v18traffic').sample(te, 20 if TRIAL else 100)
    pst = lambda b, over: dict(q=b['q'], tenant=b['tenant'], cfg=mkcfg(**over), ov=None)
    def sig(tr):
        out = {}
        for key, fn in (('D', lambda t: t['dtop'][:20]), ('S', lambda t: t['stop'][:20]), ('F', lambda t: t['fused'][:CFG['DEPTH']]), ('O', lambda t: t['order'][:10]), ('V', lambda t: t['final'])):
            try: out[key] = tuple(int(i) for i in fn(tr))
            except Exception: out[key] = None
        return out
    REF = [sig(G['run'](pst(b, {}))) for b in probes]
    CLEAN_NAT = {q: bool(succ(G['run'](nat_st(q, {})), nat_st(q, {})['gold'], 5)) for q in nat}
    CV = {}
    for b in traffic:
        fe = features(G['run'](pst(b, {}))); CV[b['bid']] = float(dispatch_v3(proba(fe), fe)[1])
    log('natural', len(nat), 'probes', len(probes), 'traffic', len(traffic), 'clean natural Hit@5', round(float(np.mean(list(CLEAN_NAT.values()))), 4))
    allow = (lambda fn: True) if CFG['DEPLOY']['natural_typo_repair'] else (lambda fn: fn is not rep_QLEX)
    def loop_ok(q, over):   # the frozen deployed loop (natural rules + classifier at the Mondrian thresholds), on the current code
        st = nat_st(q, over); tr = G['run'](st); fe = features(tr); reps, s = dispatch_v3(proba(fe), fe); lam = LAMS[GATES['ALPHA']][stratum(fe, 'esci')]
        rs = [(f, REP[f]) for f, cond in NAT_RULES if cond(fe)] + [(l, fn) for l, fn in (reps if s >= lam else []) if allow(fn)]
        return bool(succ(G['run'](apply_v3(st, rs)), st['gold'], 5)) if rs else bool(succ(tr, st['gold'], 5))
    def localize(cnt):
        ch = {k: cnt[k] > 0 for k in STG}
        if ch['D'] and ch['S']: return 'FILTERS'
        for k, c_ in (('D', 'DENSE'), ('S', 'BM25'), ('F', 'FUSION'), ('O', 'RERANK'), ('V', 'SERVING')):
            if ch[k]: return c_
        return 'NONE'
    def signp(bm, cm):
        n = bm + cm
        return 1.0 if n == 0 else float(sum(math.comb(n, i) for i in range(bm, n + 1)) / 2 ** n)
    rows = []; fB = open(os.path.join(OUT, 'B_bugs.jsonl'), 'w')
    for bug in BUGS:
        over = dict(bug.get('cfg', {})); state = dict(code=False)
        def apply_code():
            if 'patch' in bug:
                seg = ast.get_source_segment(SRC, FN[bug['fn']])
                for a, b2 in bug['patch']:
                    assert seg.count(a) == 1, (bug['id'], a); seg = seg.replace(a, b2)
                exec(compile(seg, f"bug:{bug['id']}", 'exec'), G); state['code'] = True
        def restore_code():
            for nm, fn in ORIG.items(): G[nm] = fn
            G['_V18_LAST'].clear(); state['code'] = False
        def rollback(stage, cur):
            if 'patch' in bug and stage == bug['stage']: restore_code()
            return {k: v for k, v in cur.items() if k not in STAGE_KNOBS.get(stage, [])}
        r = dict(id=bug['id'], stage=bug['stage'], designed=bug.get('designed'))
        try:
            apply_code()
            h_bug = {q: bool(succ(G['run'](nat_st(q, over)), nat_st(q, over)['gold'], 5)) for q in nat}
            work = [q for q in nat if CLEAN_NAT[q]]; broke = [q for q in work if not h_bug[q]]
            r.update(nat_hit_clean=float(np.mean(list(CLEAN_NAT.values()))), nat_hit_bug=float(np.mean(list(h_bug.values()))), nat_broken=len(broke), nat_working=len(work),
                     harmful=bool(len(broke) >= max(1, 0.01 * len(work))))
            trs = [G['run'](pst(b, over)) for b in probes]; y = [not bool(succ(t, b['gold'], 5)) for t, b in zip(trs, probes)]
            cnt = {k: sum(a[k] != b2[k] for a, b2 in zip([sig(t) for t in trs], REF)) for k in STG}
            r.update(selftest_alarm=any(y), probe_fail=float(np.mean(y)), stage_changes=cnt, stage_comp=localize(cnt), localized_ok=localize(cnt) == bug['stage'])
            bm = cm = 0
            for b in traffic:
                fe = features(G['run'](pst(b, over))); f1 = float(dispatch_v3(proba(fe), fe)[1]) >= TAU; f0 = CV[b['bid']] >= TAU; bm += f1 and not f0; cm += f0 and not f1
            r.update(telemetry_p=signp(bm, cm), telemetry_alarm=bool(signp(bm, cm) < 0.01))
            h_loop = {q: loop_ok(q, over) for q in broke}; h_univ = {q: bool(succ(G['run'](universal(nat_st(q, over))), nat_st(q, over)['gold'], 5)) for q in broke}
            r.update(loop_fixes=sum(h_loop.values()), universal_fixes=sum(h_univ.values()))
            # self-test repair: roll back the localized stage, retest; if probes still fail, roll back everything; accept only if every probe passes
            cur = dict(over); steps = []
            if any(y):
                cur = rollback(r['stage_comp'], cur); steps.append(r['stage_comp'])
                if any(not bool(succ(G['run'](pst(b, cur)), b['gold'], 5)) for b in probes):
                    restore_code(); cur = {}; steps.append('ALL')
            verified = not any(not bool(succ(G['run'](pst(b, cur)), b['gold'], 5)) for b in probes)
            h_fix = {q: bool(succ(G['run'](nat_st(q, cur)), nat_st(q, cur)['gold'], 5)) for q in nat}
            r.update(rollback_steps=steps, verified=verified, nat_hit_after=float(np.mean(list(h_fix.values()))), nat_restored=sum(h_fix[q] for q in broke),
                     nat_broken_after_repair=sum(CLEAN_NAT[q] and not h_fix[q] for q in nat), gain_points=100 * (float(np.mean(list(h_fix.values()))) - r['nat_hit_bug']))
        except Exception as ex: r['error'] = repr(ex)[:200]
        finally: restore_code()
        rows.append(r); fB.write(json.dumps(r, default=str) + '\n'); fB.flush(); log('bug', {k: r.get(k) for k in ('id', 'harmful', 'nat_broken', 'selftest_alarm', 'stage_comp', 'localized_ok', 'telemetry_alarm', 'verified', 'gain_points', 'loop_fixes', 'error')})
    H = [r for r in rows if r.get('harmful')]
    m = lambda xs, k: (float(np.mean([bool(x[k]) for x in xs])) if xs else None)
    R['summary'] = dict(bugs=len(rows), harmful=len(H), detected=m(H, 'selftest_alarm'), localized=m(H, 'localized_ok'), verified=m(H, 'verified'), telemetry=m(H, 'telemetry_alarm'),
                        broken=sum(r['nat_broken'] for r in H), restored=sum(r['nat_restored'] for r in H), loop_fixed=sum(r['loop_fixes'] for r in H), universal_fixed=sum(r['universal_fixes'] for r in H),
                        harm_after_repair=sum(r['nat_broken_after_repair'] for r in H))
    json.dump(R, open(os.path.join(OUT, 'RESULT.json'), 'w'), indent=1, default=str); log('summary', R['summary'])
