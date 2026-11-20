"""v13 Idea 2 (docs/evidence/v13_idea2_protocol.md): probe-and-verify under leave-one-fault-out, by CPU replay of a judged port run.
usage: DATASET=<ds> python docs/evidence/v13_idea2.py <work_dir> <code_file> <eval_split: train|test> <out.jsonl>    (resumable; writes one line per episode)
<work_dir> must contain port*_<ds>_out/{checkpoint.pkl,corpus_e5.npy,PORT_PROTOCOL.json} and port_data/ with the verified zips."""
import glob, hashlib, json, os, pickle, re, sys, time
import numpy as np

work, code_file, split, outp = sys.argv[1:5]; ds = os.environ['DATASET']
outdir = glob.glob(os.path.join(work, f'port*_{ds}_out'))[0]; prot = json.load(open(os.path.join(outdir, 'PORT_PROTOCOL.json'))); cfg = prot['cfg']
src = open(code_file, encoding='utf-8').read(); assert hashlib.sha256(src.encode('utf-8')).hexdigest() == prot['code_sha256'], 'code file is not the code that produced this run'
os.environ.update(DIAGRAG_WORK=work, SEED=str(cfg['SEED']), N_QUERIES=str(cfg['N_QUERIES']), N_HARD=str(cfg['N_HARD']), MAX_ATT=str(cfg['MAX_ATT']), N_HARM=str(cfg['N_HARM']), TIME_BUDGET='0')
cells = re.split(r'\n# %%(?: \[markdown\])?\n', src); last = max(i for i, c in enumerate(cells) if 'REP = dict(' in c)
g = {'__name__': '__replay__', '__file__': os.path.join(work, os.path.basename(code_file))}; t0 = time.time()
for i, c in enumerate(cells[:last + 1]):
    if not c.lstrip().startswith('# '): exec(compile(c, f'cell{i}', 'exec'), g)
print(f'setup {time.time() - t0:.0f}s', flush=True)
run, features, succ, REP = g['run'], g['features'], g['succ'], g['REP']
# the R19 repair reads CE_FLOOR, which the frozen code fits in a later cell; set it with the frozen code's own formula (10th percentile of clean-train top CE score)
_ok = [b['clean_tr']['ce'].max() for b in g['BASE'] if b['split'] == 'train' and b['h5'] and len(b['clean_tr']['ce'])]; g['CE_FLOOR'][0] = float(np.percentile(_ok, 10))
_R = pickle.load(open(os.path.join(outdir, 'checkpoint.pkl'), 'rb')); EP = _R['EPIS']; CLN = _R['CLEAN']; seed = int(cfg['SEED'])
from sklearn.ensemble import HistGradientBoostingClassifier
FE = sorted(EP[0]['feats'])
INV = {'QUERY': [('q_oov', '+'), ('q_correctable', '+'), ('q_segmentable', '+'), ('q_prefix', '+'), ('q_synlow', '+')], 'ENCODER': [('q_probe_cos', '-'), ('d_null10', '+')],
       'ANN': [('ann_probe', '-')], 'VECTORS': [('align_probe', '-'), ('stale_sparse', '+'), ('stale_min', '-'), ('nonfinite', '+'), ('cov', '-'), ('sparse_absent_dense', '+')],
       'BM25': [('s_lex5', '-')], 'RERANK': [('ce_fuse_rho', '-'), ('ce_dense_rho', '-'), ('n_depth', '-')], 'FUSION': [('dep_dense', '-')], 'SERVING': [('n_final', '-')],
       'CONTENT': [('dup5', '+'), ('red_cos5', '+'), ('thin5', '+')]}
COMP = {**{f: 'QUERY' for f in 'Q01 Q03 Q04 Q05'.split()}, 'K04': 'VECTORS', 'K05': 'CONTENT', 'K08': 'CONTENT', **{f: 'VECTORS' for f in 'R01 R07 R25'.split()},
        **{f: 'ENCODER' for f in 'R03 R10 R11'.split()}, **{f: 'RERANK' for f in 'R05 R19 R24'.split()}, 'R13': 'BM25', 'R15': 'ANN', 'R22': 'FUSION', 'R23': 'SERVING'}
LIST = [(c, f, d) for c, v in INV.items() for f, d in v if f in FE]; THR = 0.05 / len(LIST)
TR = [e for e in EP if e['split'] == 'train']; cal = {f: np.array([e['feats'][f] for e in TR if e['fault'] == 'NONE'], float) for _, f, _ in LIST}
def flagged(fe):
    S = set()
    for c, f, d in LIST:
        x = float(fe[f]); v = cal[f]; p = (1 + ((v >= x) if d == '+' else (v <= x)).sum()) / (len(v) + 1)
        if p <= THR: S.add(c)
    return S
mat = lambda fs: np.array([[fe[k] for k in FE] for fe in fs], np.float32)
hgb = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=seed)
Xtr = mat([e['feats'] for e in TR]); ytr = np.array([e['fault'] for e in TR])
# replay check: clean episodes of the evaluated split must reproduce the stored clean result
cl = [e for e in EP if e['split'] == split and e['fault'] == 'NONE' and e['bid'] in CLN][:200]; mism = sum(bool(succ(run(e['st']), e['st']['gold'])) != bool(CLN[e['bid']]['h5']) for e in cl)   # replay must reproduce the stored clean Hit@5
print(f'replay check: {mism} mismatches of {len(cl)} clean episodes', flush=True); assert mism <= 0.005 * len(cl), 'replay not trusted'
done = set()
if os.path.exists(outp): done = {json.loads(l)['n'] for l in open(outp)}
fh = open(outp, 'a'); models = {}
for n, e in enumerate(EP):
    if e['split'] != split or e['fault'] not in COMP or n in done: continue
    f = e['fault']
    if f not in models: keep = ytr != f; models[f] = hgb().fit(Xtr[keep], ytr[keep])
    m = models[f]; cls = list(m.classes_); iN = cls.index('NONE'); st = e['st']; gold = st['gold']; k = st['k']
    tr0 = run(st); p = m.predict_proba(mat([e['feats']]))[0]
    order = [cls[i] for i in np.argsort(-p) if cls[i] != 'NONE']; S0 = flagged(e['feats'])
    rank = {c: i for i, c in enumerate(order)}; LIB = sorted(COMP)   # component-indexed repair library (D1)
    comp_lib = [c for c in LIB if COMP[c] in S0 and c != f]; comp_lib = sorted(comp_lib, key=lambda c: rank.get(c, 99))
    if COMP[f] in S0: pos = min([i for i, c in enumerate(comp_lib) if COMP[c] == COMP[f]] or [len(comp_lib)]); comp_lib.insert(pos, f)
    o12 = list(dict.fromkeys(comp_lib + order))
    cache = {}
    def probe(c):
        if c not in cache:
            tr2 = run(REP[c](st, tr0)); fe2 = features(tr2); q = m.predict_proba(mat([fe2]))[0]
            cache[c] = dict(ok=bool(succ(tr2, gold, k)), healthy=bool(cls[int(np.argmax(q))] == 'NONE' and not flagged(fe2)), pnone=float(q[iN]), flagged=sorted(flagged(fe2)), top=cls[int(np.argmax(q))])
        return cache[c]
    def policy(cands):   # D1: probe up to 3 candidates, keep the largest increase in P(NONE)
        tried = cands[:3]
        for c in tried: probe(c)
        best = max(tried, key=lambda c: cache[c]['pnone'] - float(p[iN])); return cache[best]['ok'], len(tried), best
    p0 = probe(order[0])['ok']; p2 = policy(order); p12 = policy(o12)
    for c in list(dict.fromkeys(order[:3] + o12[:3])): probe(c)   # raw outcomes of every candidate either ordering could try, so stopping rules can be evaluated offline
    fh.write(json.dumps(dict(n=n, fault=f, comp=COMP[f], flagged=sorted(S0), P0=p0, P2_ok=p2[0], P2_cost=p2[1], P2_pick=p2[2], P12_ok=p12[0], P12_cost=p12[1], P12_pick=p12[2],
                             oracle=bool(e.get('rescued')), top3=order[:3], o12=o12[:3], p_orig_none=float(p[iN]), probes=cache)) + '\n'); fh.flush()
    if len(done) % 25 == 0: print(f'{n} {f} {time.time() - t0:.0f}s', flush=True)
    done.add(n)
print('done', len(done), 'episodes', f'{time.time() - t0:.0f}s')
