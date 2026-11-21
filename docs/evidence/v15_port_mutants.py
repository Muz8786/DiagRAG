"""v15 A7: blind code mutants of the SECOND retrieval stack (frozen diagrag_port5.py), by replay of its judged FiQA run.
Same operators, coverage rule, harm definition, stage-trace localization and alarms as the main-stack M part (v15_selftest_mutants.py), with the
second stack's own probes (train clean successes) and its own attributor for the telemetry alarm. ROLE = dev | heldout (halves by md5 of the point id).
usage: DATASET=fiqa python docs/evidence/v15_port_mutants.py <work_dir> <code_file> <out_dir> <ROLE> [TRIAL]"""
import ast, collections, glob, hashlib, json, math, os, pickle, random, re, signal, sys, time
import numpy as np

work, code_file, outd, ROLE = sys.argv[1:5]; TRIAL = len(sys.argv) > 5 and sys.argv[5] == '1'; ds = os.environ['DATASET']; os.makedirs(outd, exist_ok=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import v15_selftest_mutants as V
outdir = glob.glob(os.path.join(work, f'port*_{ds}_out'))[0]; prot = json.load(open(os.path.join(outdir, 'PORT_PROTOCOL.json'))); cfg = prot['cfg']
src = open(code_file, encoding='utf-8').read(); assert hashlib.sha256(src.encode('utf-8')).hexdigest() == prot['code_sha256'], 'code file is not the code that produced this run'
os.environ.update(DIAGRAG_WORK=work, SEED=str(cfg['SEED']), N_QUERIES=str(cfg['N_QUERIES']), N_HARD=str(cfg['N_HARD']), MAX_ATT=str(cfg['MAX_ATT']), N_HARM=str(cfg['N_HARM']), TIME_BUDGET='0')
cells = re.split(r'\n# %%(?: \[markdown\])?\n', src); last = max(i for i, c in enumerate(cells) if 'REP = dict(' in c)
g = {'__name__': '__replay__', '__file__': os.path.join(work, os.path.basename(code_file))}; t0 = time.time()
log = lambda *a: print(f'[{time.time() - t0:6.0f}s]', *a, flush=True)
for i, c in enumerate(cells[:last + 1]):
    if not c.lstrip().startswith('# '): exec(compile(c, f'cell{i}', 'exec'), g)
log('setup done')
_ok = [b['clean_tr']['ce'].max() for b in g['BASE'] if b['split'] == 'train' and b['h5'] and len(b['clean_tr']['ce'])]; g['CE_FLOOR'][0] = float(np.percentile(_ok, 10))
_R = pickle.load(open(os.path.join(outdir, 'checkpoint.pkl'), 'rb')); EP = _R['EPIS']; seed = int(cfg['SEED'])
from sklearn.ensemble import HistGradientBoostingClassifier
FE = sorted(EP[0]['feats']); mat = lambda fs: np.array([[fe[k] for k in FE] for fe in fs], np.float32)
calb = lambda bid: int(hashlib.md5(('cal|' + bid).encode()).hexdigest()[:8], 16) / 2**32 < 0.5
TR = [e for e in EP if e['split'] == 'train']; TRA = [e for e in TR if not (e['fault'] == 'NONE' and calb(e['bid']))]; CALE = [e for e in TR if e['fault'] == 'NONE' and calb(e['bid'])]
ATT = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced',
                                     random_state=seed).fit(mat([e['feats'] for e in TRA]), np.array([e['fault'] for e in TRA])); iN = list(ATT.classes_).index('NONE')
score = lambda fe: float(1 - ATT.predict_proba(mat([fe]))[0][iN])
TAU = float(np.quantile([score(e['feats']) for e in CALE], 0.95))   # 5% false-positive threshold on clean calibration queries
P = dict(V.P); P.update(SCREEN=40, TRAFFIC=100, A=100, MAXM=400, HARM_FRAC=0.10, ALARM_P=0.01, TIMEOUT=90)
if TRIAL: P.update(SCREEN=8, TRAFFIC=8, A=10, MAXM=6)
rnd = lambda *tag: random.Random('|'.join(map(str, tag)))
B = g['BASE']; tr_ok = [b for b in B if b['split'] == 'train' and b['h5']]; te = [b for b in B if b['split'] == 'test']; te_ok = [b for b in te if b['h5']]
probes = rnd('p5probes').sample(tr_ok, min(P['A'], len(tr_ok))); screen = rnd('p5screen').sample(te_ok, P['SCREEN']); traffic = rnd('p5traffic').sample(te, P['TRAFFIC'])
qrun = lambda b: g['run'](dict(q=b['q'], cfg=g['mkcfg'](), ov=None)); succ = g['succ']
R = dict(trial=TRIAL, role=ROLE, dataset=ds, seed=seed, code_sha256=prot['code_sha256'], probes=len(probes), screen=len(screen), traffic=len(traffic), TAU=TAU)
log('probes', len(probes), 'screen', len(screen), 'traffic', len(traffic), 'TAU', TAU)

TARGETS = ['run', 'bm25_scores', 'topn', 'enc_q', 'ce_scores']
FCOMP = dict(bm25_scores='BM25', enc_q='DENSE', ce_scores='RERANK', topn='SHARED')
MARKERS = [('m = M(ov)', 'DENSE'), ('dok = np.ones(NT, bool)', 'DENSE'), ('ss = bm25_scores(', 'BM25'), ('n_stale = 0', 'DENSE'),
           ('fs = collections.defaultdict(float)', 'FUSION'), ("depth = fused[:c['depth']]", 'RERANK'), ('return dict(', 'TELEMETRY')]
V.INTKEYS = {k for k, v in g['CFG'].items() if isinstance(v, int) and not isinstance(v, bool)}
SRC = src; tree = ast.parse(SRC); FN = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in TARGETS}
assert set(FN) == set(TARGETS), FN.keys()
CACHES = {'enc_q': '_QC', 'ce_scores': '_CEC'}; ORIG = {n: g[n] for n in TARGETS}
codes = {g[f].__code__: f for f in TARGETS}; off = {f: FN[f].lineno - g[f].__code__.co_firstlineno for f in TARGETS}; COV = set()
def tracer(frame, event, arg):
    f = codes.get(frame.f_code)
    if f is None: return None
    COV.add((f, frame.f_lineno + off[f]))
    def lt(fr, ev, ar):
        if ev == 'line': COV.add((f, fr.f_lineno + off[f]))
        return lt
    return lt
saved_c = {v: g[v] for v in CACHES.values()}
for v in CACHES.values(): g[v] = {}
sys.settrace(tracer)
try:
    for b in screen: qrun(b)
finally:
    sys.settrace(None)
    for v, d_ in saved_c.items(): g[v] = d_
MUT = []
for name, node in FN.items():
    seg = ast.get_source_segment(SRC, node); base_line = node.lineno; marks = []
    if name == 'run':
        for k, ln in enumerate(seg.splitlines()):
            for mk, cp in MARKERS:
                if mk in ln: marks.append((base_line + k, cp))
    for k, (kind, nd, sub) in enumerate(V.pts_of(ast.parse(seg))):
        line = base_line + nd.lineno - 1; pid = f'p5|{name}|{line}|{nd.col_offset}|{getattr(nd, "end_col_offset", -1)}|{kind}|{sub}'
        half = 'dev' if int(hashlib.md5(pid.encode()).hexdigest()[0], 16) < 8 else 'heldout'
        comp = FCOMP.get(name) or next((cp for ml, cp in sorted(marks, reverse=True) if ml <= line), 'OTHER')
        MUT.append(dict(pid=pid, fn=name, k=k, kind=kind, line=line, half=half, comp=comp, seg=seg, covered=(name, line) in COV))
R['M_points'] = dict(total=len(MUT), covered=sum(x['covered'] for x in MUT), covered_by_half=dict(collections.Counter(x['half'] for x in MUT if x['covered'])),
                     by_fn=dict(collections.Counter(x['fn'] for x in MUT if x['covered'])))
mine = sorted([x for x in MUT if x['half'] == ROLE and x['covered']], key=lambda x: hashlib.md5(x['pid'].encode()).hexdigest())[:P['MAXM']]
log('mutation points', R['M_points'], 'evaluated', len(mine))
STG = ['D', 'S', 'F', 'O', 'V']
def sig(tr):
    out = {}
    for key, fn in (('D', lambda t: t['dtop'][:20]), ('S', lambda t: t['stop'][:20]), ('F', lambda t: t['fused'][:g['CFG']['DEPTH']]),
                    ('O', lambda t: t['order'][:10]), ('V', lambda t: t['final'])):
        try: out[key] = tuple(int(i) for i in fn(tr))
        except Exception: out[key] = None
    return out
REF = [sig(qrun(b)) for b in probes]; REF2 = [sig(qrun(b)) for b in probes]
clean_chg = {k: sum(a[k] != b2[k] for a, b2 in zip(REF, REF2)) for k in STG}; R['clean_stage_changes'] = clean_chg
def localize(cnt):
    ch = {k: cnt[k] > clean_chg[k] for k in STG}
    if ch['D'] and ch['S']: return 'FILTERS'
    for k, c_ in (('D', 'DENSE'), ('S', 'BM25'), ('F', 'FUSION'), ('O', 'RERANK'), ('V', 'SERVING')):
        if ch[k]: return c_
    return 'NONE'
CV = {b['bid']: score(g['features'](qrun(b))) for b in traffic}
def signp(bm, cm):
    n = bm + cm
    return 1.0 if n == 0 else float(sum(math.comb(n, i) for i in range(bm, n + 1)) / 2 ** n)
SCORED = ('DENSE', 'BM25', 'FUSION', 'RERANK', 'SERVING', 'FILTERS')
class _TO(Exception): pass
def _alarm(*a): raise _TO()
signal.signal(signal.SIGALRM, _alarm)
rows = []; fM = open(os.path.join(outd, 'M_mutants.jsonl'), 'w')
for n_, x in enumerate(mine):
    r = dict(pid=x['pid'], fn=x['fn'], kind=x['kind'], comp=x['comp'], order=1, line=x['line'], code_base='port5_' + ds); saved = {}
    try:
        code_ = compile(V.mutant_src(x), f"mutant:{x['pid']}", 'exec')
        if x['fn'] in CACHES: saved[CACHES[x['fn']]] = g[CACHES[x['fn']]]; g[CACHES[x['fn']]] = {}
        exec(code_, g); signal.alarm(P['TIMEOUT'])
        fails = sum(not bool(succ(qrun(b), b['gold'])) for b in screen); signal.alarm(0)
        r['screen_fail'] = fails / len(screen); r['status'] = 'harmful' if r['screen_fail'] >= P['HARM_FRAC'] else ('subtle' if fails > 0 else 'harmless')
        if r['status'] in ('harmful', 'subtle'):
            signal.alarm(P['TIMEOUT'] * 8)
            trs = [qrun(b) for b in probes]; y = [not bool(succ(t, b['gold'])) for t, b in zip(trs, probes)]
            sg = [sig(t) for t in trs]; cnt = {k: sum(a[k] != b2[k] for a, b2 in zip(sg, REF)) for k in STG}
            r.update(selftest_alarm=any(y), probe_fail=float(np.mean(y)), stage_changes=cnt, stage_comp=localize(cnt), decoded=None)
            bm = cm = 0; tel_err = False
            for b in traffic:
                tr = qrun(b)
                try: s_ = score(g['features'](tr))
                except Exception: tel_err = True; continue
                f1, f0 = s_ >= TAU, CV[b['bid']] >= TAU; bm += f1 and not f0; cm += f0 and not f1
            signal.alarm(0)
            r.update(telemetry_p=signp(bm, cm), telemetry_alarm=bool(tel_err or signp(bm, cm) < P['ALARM_P']), telemetry_error=tel_err, ce_drop_alarm=None)
            r['either_alarm'] = bool(r['selftest_alarm'] or r['telemetry_alarm'])
            r['component_ok'] = (r['stage_comp'] == x['comp']) if x['comp'] in SCORED else None
            r['component_ok_decode'] = None
    except _TO: r['status'] = 'timeout'
    except Exception as ex: r['status'] = 'crash'; r['error'] = repr(ex)[:120]
    finally:
        signal.alarm(0)
        for nm, fn in ORIG.items(): g[nm] = fn
        for k_, v_ in saved.items(): g[k_] = v_
    rows.append(r); fM.write(json.dumps(r, default=str) + '\n'); fM.flush()
    if n_ % 25 == 0: log('M', n_, 'of', len(mine), collections.Counter(z['status'] for z in rows))
H = [r for r in rows if r['status'] == 'harmful']; C = [r for r in H if r.get('component_ok') is not None]
m = lambda xs, k: (float(np.mean([bool(x[k]) for x in xs])) if xs else None)
R['M'] = dict(evaluated=len(rows), status=dict(collections.Counter(r['status'] for r in rows)), harmful=len(H), detected_selftest=m(H, 'selftest_alarm'),
              detected_telemetry=m(H, 'telemetry_alarm'), component_ok=m(C, 'component_ok'), n_component_scored=len(C))
json.dump(R, open(os.path.join(outd, 'RESULT.json'), 'w'), indent=1, default=str); log('M', R['M']); log('done')
