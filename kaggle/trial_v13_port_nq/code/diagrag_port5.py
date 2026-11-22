# %% [markdown]
# # DiagRAG portability arm v2 — second stack on two domains (SciFact = science, FiQA = finance)
# v2 fixes found by the v1 port run (judged_port_scifact/): query punctuation broke the Q01/Q04/Q05 injectors; R03 re-expressed
# as query truncation (sentence-transformers#4060); index-health probe depth 20; 50/50 hash split over ALL labelled queries so
# held-out positives are not capped by the 300-query official test split. Gates unchanged and frozen in PORT_PROTOCOL.json.
# Domain: BEIR SciFact (scientific claims, 5,183 abstracts, official train/test qrels).
# Stack 2: intfloat/e5-small-v2 ("query:"/"passage:" prefixes) + FAISS HNSW (M=32) + BM25 + min-max convex fusion
#          + ms-marco-MiniLM-L-6-v2 reranker, Hit@5.
# Faults: the 20 of core-28 + R25 that translate (docs/EVIDENCE_AND_NOVELTY_REPORT.md section 5), re-expressed on
# stack 2's own knobs. Gates are identical to core-28 and frozen in PORT_PROTOCOL.json before any result.

# %%
import os, sys, subprocess, json, re, time, math, random, hashlib, zipfile, csv, collections, pickle
ON_KAGGLE = os.path.exists('/kaggle')
WORK = '/kaggle/working' if ON_KAGGLE else os.environ.get('DIAGRAG_WORK', os.getcwd())
DATA = '/tmp/diagrag_port_data' if ON_KAGGLE else os.path.join(WORK, 'port_data'); OUT = os.path.join(WORK, f"port5_{os.environ.get('DATASET', 'scifact')}_out")
os.makedirs(DATA, exist_ok=True); os.makedirs(OUT, exist_ok=True)
for mod, pk in [('sentence_transformers', 'sentence-transformers'), ('faiss', 'faiss-cpu'), ('nltk', 'nltk'), ('tabulate', 'tabulate')]:
    try: __import__(mod)
    except ImportError: subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pk], check=False)
import numpy as np, pandas as pd, torch, faiss
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sentence_transformers import SentenceTransformer, CrossEncoder
DEV = 'cuda' if torch.cuda.is_available() else 'cpu'; GPU = DEV == 'cuda'
DATASET = os.environ.get('DATASET', 'scifact')
CFG = dict(DATASET=DATASET, N_QUERIES=int(os.environ.get('N_QUERIES', 2500)), SEED=int(os.environ.get('SEED', 7)), K_FINAL=5, DEPTH=25, CAND=100, FUSION_ALPHA=0.5, EF_CLEAN=128, HNSW_M=32,
           ENCODER='intfloat/e5-small-v2', ENCODER_OLD='intfloat/e5-small', RERANKER='cross-encoder/ms-marco-MiniLM-L-6-v2',
           CE_MAXLEN=256, N_HARD=int(os.environ.get('N_HARD', 50)), MAX_ATT=int(os.environ.get('MAX_ATT', 2500)),
           N_HARM=int(os.environ.get('N_HARM', 20)), PROBE_K=20, TIME_BUDGET=int(os.environ.get('TIME_BUDGET', 0)))
GATES = dict(detector='held-out one-vs-rest AUROC >= 0.70 AND >= 20 held-out positives',
             repair='>= 20 hard episodes AND Wilson 95% lower bound >= 0.50 AND <= 10% of clean successes lost',
             AUROC_BAR=0.70, MIN_TEST_POS=20, RESCUE_BAR_LB=0.50, MIN_REPAIR_N=20, MAX_HARM=0.10,
             summary='claim "the suite ports" only if >= 15 of the 20 ported faults pass both gates; report every fault either way',
             PORT_TARGET=15)
random.seed(CFG['SEED']); np.random.seed(CFG['SEED']); torch.manual_seed(CFG['SEED'])
if not GPU: torch.set_num_threads(int(os.environ.get('TORCH_THREADS', os.cpu_count() or 4)))
T0 = time.time()
def log(*a): print(f'[{time.time()-T0:7.0f}s]', *a, flush=True)
CKPT = os.path.join(OUT, 'checkpoint.pkl'); RES = pickle.load(open(CKPT, 'rb')) if os.path.exists(CKPT) else {}
def over_budget(): return CFG['TIME_BUDGET'] > 0 and time.time() - T0 > CFG['TIME_BUDGET']
def save_ckpt(stage):
    keep = {k: globals()[k] for k in ('CLEAN', 'EPIS', 'GEN', 'GSTATE', 'SEEN', 'HARM') if k in globals()}
    keep.update(stage=stage, caches=dict(QC=_QC, CEC=_CEC, DC=_DC))
    pickle.dump(keep, open(CKPT + '.tmp', 'wb'), protocol=4); os.replace(CKPT + '.tmp', CKPT); log('checkpoint saved:', stage)
def maybe_stop(stage):
    if over_budget(): save_ckpt(stage); log('TIME_BUDGET reached - run again to resume'); raise SystemExit(0)
PROTO = os.path.join(OUT, 'PORT_PROTOCOL.json')
if not os.path.exists(PROTO):
    json.dump(dict(created_utc=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()), gates=GATES, cfg=CFG, device=DEV,
                   code_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest() if '__file__' in globals() else 'notebook'),
              open(PROTO, 'w'), indent=1)

# %% [markdown]
# ## 1. Data (exact bytes + SHA-256) and corpus

# %%
BEIR = dict(scifact=(2816079, '536e14446a0ba56ed1398ab1055f39fe852686ecad24a6306c80c490fa8e0165'),
            fiqa=(17948027, '32c7df99ed21252fdfb2cf3f5673502a8d245ee0c44c4a133570d92ce2b3ad02'),
            nfcorpus=(2448432, 'efe5be03f8c5b86a5870102d0599d227c8c6e2484328e68c6522560385671b0b'),
            arguana=(3773617, 'cfdf79adce27a401b3cd3ea267903134dbfab2c6afeb95d7fe5724a00bf7557b'),
            scidocs=(142471588, '96640201687767c9b1fcc5af7a80b90fb325b37fa25329c2586c25edcfa17ef1'),
            nq=(498307926, '2553bf7bfbab47b1436ca00a34bce57320e18e611fd00999a2a3a1b4714be752'))
FILES = {DATASET: dict(name=f'{DATASET}.zip', size=BEIR[DATASET][0], url=f'https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{DATASET}.zip',
                       sha=BEIR[DATASET][1]),
         'qspell': dict(name='corpus-webis-qspell-17.zip', size=2285705, url='https://zenodo.org/api/records/3570912/files/corpus-webis-qspell-17.zip/content',
                        sha='f13bd165544ab2ac75d63de4334feb86d74d1b3dfbe48d79423133552b5054e4')}
def sha256(p):
    h = hashlib.sha256(); h.update(open(p, 'rb').read()); return h.hexdigest()
VERIFY = {}
for k, f in FILES.items():
    p = os.path.join(DATA, f['name']); f['path'] = p
    if not (os.path.exists(p) and os.path.getsize(p) == f['size']): subprocess.run(['curl', '-sL', '--retry', '3', '-o', p, f['url']], check=True)
    VERIFY[k] = dict(bytes=os.path.getsize(p), sha256=sha256(p)); assert VERIFY[k]['bytes'] == f['size'] and VERIFY[k]['sha256'] == f['sha'], k
zf = zipfile.ZipFile(FILES[DATASET]['path'])
rd = lambda n: zf.read(n).decode('utf-8')
DOCS = [json.loads(l) for l in rd(f'{DATASET}/corpus.jsonl').splitlines()]; N = len(DOCS)
TEXT = [(d.get('title') or '') + '. ' + d['text'] for d in DOCS]; ID2I = {d['_id']: i for i, d in enumerate(DOCS)}
QUERIES = {j['_id']: j['text'] for j in map(json.loads, rd(f'{DATASET}/queries.jsonl').splitlines())}
QRELS, _qr = {}, collections.defaultdict(set)
for split in [n.split('/')[-1][:-4] for n in zf.namelist() if '/qrels/' in n and n.endswith('.tsv')]:
    for row in list(csv.reader(rd(f'{DATASET}/qrels/{split}.tsv').splitlines(), delimiter='\t'))[1:]:
        if row[1] in ID2I and int(row[2]) > 0: _qr[row[0]].add(ID2I[row[1]])
def hsplit(qid): return 'test' if int(hashlib.md5(f'port2|{DATASET}|{qid}'.encode()).hexdigest()[:8], 16) % 2 else 'train'   # 50/50 by query id
for qid in sorted(_qr, key=lambda x: hashlib.md5(x.encode()).hexdigest())[:CFG['N_QUERIES']]:
    QRELS[(hsplit(qid), qid)] = _qr[qid]
CH = [hashlib.md5(re.sub(r'\s+', ' ', t.lower()).encode()).hexdigest() for t in TEXT]
PUR = dict(docs=N, unique_ids=len(ID2I), empty=sum(not d['text'].strip() for d in DOCS),
           exact_dup_rows=N - len(set(CH)), queries_with_qrels=collections.Counter(s for s, _ in QRELS))
log('verify', VERIFY, 'purity', PUR)

# %% [markdown]
# ## 2. Stack 2: BM25 + e5-small-v2 dense in FAISS HNSW + min-max convex fusion + MiniLM reranker

# %%
TOKRE = re.compile(r'[a-z0-9]+')
def tok(s): return TOKRE.findall(s.lower())
CV = CountVectorizer(token_pattern=r'[a-z0-9]+', lowercase=True, dtype=np.float32); TF = CV.fit_transform(TEXT).tocsr()
VOC = CV.vocabulary_; V = len(VOC); DF = np.bincount(TF.indices, minlength=V)
IDF = np.log(1 + (N - DF + 0.5) / (DF + 0.5)).astype(np.float32); DL = np.asarray(TF.sum(1)).ravel(); AVGDL = DL.mean(); K1, B = 0.9, 0.4
def bm25_weight(tf, dl):
    tf = tf.tocsr(copy=True); rows = np.repeat(np.arange(tf.shape[0]), np.diff(tf.indptr)); t = tf.data
    tf.data = IDF[tf.indices] * t * (K1 + 1) / (t + K1 * (1 - B + B * dl[rows] / AVGDL)); return tf
BM = bm25_weight(TF, DL).tocsc(); del TF
def df_of(w): return int(DF[VOC[w]]) if w in VOC else 0
def bm25_scores(q, shift=0, extra=None):
    ids = [(VOC[t] + shift) % V for t in tok(q) if t in VOC]
    s = np.asarray(BM[:, ids].sum(1)).ravel() if ids else np.zeros(N, np.float32)
    if extra is not None and extra.shape[0]:
        s = np.concatenate([s, np.asarray(extra[:, ids].sum(1)).ravel() if ids else np.zeros(extra.shape[0], np.float32)])
    return s.astype(np.float32)
ENC = SentenceTransformer(CFG['ENCODER'], device=DEV); ENC_OLD = SentenceTransformer(CFG['ENCODER_OLD'], device=DEV)
CE = CrossEncoder(CFG['RERANKER'], max_length=CFG['CE_MAXLEN'], device=DEV)
_QC, _CEC, _DC = RES.get('caches', {}).get('QC', {}), RES.get('caches', {}).get('CEC', {}), RES.get('caches', {}).get('DC', {})
def enc_docs(texts):
    miss = [t for t in dict.fromkeys(texts) if t not in _DC]
    if miss:
        for t, v in zip(miss, ENC.encode(['passage: ' + t for t in miss], normalize_embeddings=True, batch_size=64)): _DC[t] = np.asarray(v, np.float32)
    return np.stack([_DC[t] for t in texts]) if texts else np.zeros((0, 384), np.float32)
def enc_q(q, mode='v2'):
    k = (q, mode)
    if k not in _QC:
        if mode == 'v2': v = ENC.encode(['query: ' + q], normalize_embeddings=True)[0]
        elif mode == 'noprefix': v = ENC.encode([q], normalize_embeddings=True)[0]          # v1 R03 (kept for reference)
        elif mode == 'trunc':                                                                # v2 R03: max_seq_length misconfig (sentence-transformers#4060)
            ml = ENC.max_seq_length; ENC.max_seq_length = 6
            try: v = ENC.encode(['query: ' + q], normalize_embeddings=True)[0]
            finally: ENC.max_seq_length = ml
        elif mode == 'old': v = ENC_OLD.encode(['query: ' + q], normalize_embeddings=True)[0]  # R11 on stack 2: e5-small v1 vs v2 index
        _QC[k] = np.asarray(v, np.float32)
    return _QC[k]
log('embedding corpus'); _ef = os.path.join(OUT, 'corpus_e5.npy'); _ep = _ef + '.partial.npy'
if os.path.exists(_ef): E = np.load(_ef)
else:   # checkpointed batches so a time-limited session can resume a large corpus
    _mm, _pc = _ef + '.partial.f32', _ef + '.partial.n'   # v13 execution fix: same chunks and encode calls, written into a preallocated on-disk array
    done_ = int(open(_pc).read()) if (os.path.exists(_pc) and os.path.exists(_mm)) else 0
    Em = np.memmap(_mm, dtype=np.float32, mode='r+' if done_ else 'w+', shape=(N, 384))
    while done_ < N:
        a_ = done_; Em[a_:a_ + 2048] = np.asarray(ENC.encode(['passage: ' + t for t in TEXT[a_:a_ + 2048]], normalize_embeddings=True, batch_size=64), np.float32)
        done_ = min(N, a_ + 2048)
        if (done_ // 2048) % 50 == 0 or done_ >= N: Em.flush(); open(_pc, 'w').write(str(done_)); log('embedded', done_, 'of', N)
        if over_budget(): Em.flush(); open(_pc, 'w').write(str(done_)); log('TIME_BUDGET reached during corpus embedding - run again to resume', done_); raise SystemExit(0)
    Em.flush(); E = np.array(Em); del Em; np.save(_ef, E); os.remove(_mm); os.remove(_pc)
_DC.update({t: E[i] for i, t in enumerate(TEXT)})
HN = faiss.IndexHNSWFlat(E.shape[1], CFG['HNSW_M'], faiss.METRIC_INNER_PRODUCT); HN.hnsw.efConstruction = 200; HN.add(E)
log('HNSW built', HN.ntotal)
def ce_scores(q, keys, texts, trunc=None):
    out = np.empty(len(keys), np.float32); todo = []
    for j, (k, t) in enumerate(zip(keys, texts)):
        if (q, k, trunc) in _CEC: out[j] = _CEC[(q, k, trunc)]
        else: todo.append((j, (q, k, trunc), t if trunc is None else t[:trunc]))
    if todo:
        for (j, ck, _), v in zip(todo, np.atleast_1d(CE.predict([(q, t) for _, _, t in todo], batch_size=64, show_progress_bar=False))):
            out[j] = v; _CEC[ck] = float(v)
    return out
def make_overlay(docs):
    if not docs: return None
    texts = [d['text'] for d in docs]; tf = CV.transform(texts).astype(np.float32)
    return dict(docs=docs, text=texts, E=enc_docs(texts), BMX=bm25_weight(tf, np.asarray(tf.sum(1)).ravel()).tocsr(),
                thin=np.array([bool(d.get('thin')) for d in docs]))
M = lambda ov: 0 if ov is None else len(ov['docs'])
def dtext(i, ov): return TEXT[i] if i < N else ov['text'][i - N]
def dkey(i, ov): return i if i < N else ('ov', hashlib.md5(ov['text'][i - N].encode()).hexdigest())
def dthin(i, ov, q):
    t = dtext(i, ov); body = t.split('. ', 1)[1] if '. ' in t else ''
    return len(body.strip()) < 60 and len(set(tok(t)) & set(tok(q))) / max(1, len(set(tok(q)))) >= 0.6
DEFAULT = dict(enc='v2', q_noise=0.0, mask=None, emb_override=None, shift=None, ef=CFG['EF_CLEAN'], sparse_shift=0, fusion='minmax',
               depth=CFG['DEPTH'], ce='ok', ce_trunc=None, result_cap=None, dedup=False, quality=False, refresh=False, nonfinite=None)
def mkcfg(**kw): c = dict(DEFAULT); c.update(kw); return c
def served_vec(i, c, ov):
    if c['emb_override'] and i in c['emb_override']: return c['emb_override'][i]
    if c['shift'] and c['shift'][0] <= i < c['shift'][1]: return E[i + c['shift'][2]]
    return E[i] if i < N else ov['E'][i - N]
def topn(s, n):
    n = min(n, int(np.isfinite(s).sum()))
    if n <= 0: return np.array([], dtype=np.int64)
    idx = np.argpartition(-s, n - 1)[:n]; return idx[np.argsort(-s[idx])]
def shingles(t, n=4):
    w = tok(t); return {' '.join(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}
def jacc(a, b): return len(a & b) / max(1, len(a | b))

def run(st):
    c, ov, q = st['cfg'], st.get('ov'), st['q']; m = M(ov); NT = N + m
    qv = enc_q(q, c['enc'])
    if c['q_noise']:
        r = np.random.default_rng(int(hashlib.md5(q.encode()).hexdigest()[:8], 16))
        qv = qv + c['q_noise'] * r.standard_normal(qv.shape).astype(np.float32) / math.sqrt(qv.size); qv = qv / np.linalg.norm(qv)
    ds = E @ qv
    if c['emb_override']:
        for i, v in c['emb_override'].items(): ds[i] = float(v @ qv)
    if c['shift']: a, b, s = c['shift']; ds[a:b] = ds[a + s:b + s].copy()
    nf = 0
    if c['nonfinite']:
        mode, idx = c['nonfinite']; nf = len(idx)
        if mode == 'top': ds[list(idx)] = 1e9
    if m: ds = np.concatenate([ds, ov['E'] @ qv])
    dok = np.ones(NT, bool); cov = 1.0
    if c['mask'] is not None:
        r = np.random.default_rng(c['mask'][1]); mk = r.random(N) < c['mask'][0]; mk[list(c['mask'][2])] = True; dok[:N] &= ~mk; cov = 1 - mk.mean()
    if c['nonfinite'] and c['nonfinite'][0] == 'drop': dok[list(c['nonfinite'][1])] = False
    dsm = np.where(dok, ds, -np.inf); exact_top = topn(dsm, 10)
    if c['ef'] < CFG['EF_CLEAN']:
        # R15 on stack 2, as pgvector documents it: "Results are limited by the size of the dynamic candidate list
        # (hnsw.ef_search)". The real FAISS HNSW is searched with ef_search = k = the misconfigured value.
        HN.hnsw.efSearch = c['ef']; _, I = HN.search(qv[None, :], c['ef']); HN.hnsw.efSearch = CFG['EF_CLEAN']
        dtop = np.array([i for i in I[0] if i >= 0 and dok[i]], dtype=np.int64)
    else: dtop = topn(dsm, CFG['CAND'])
    ss = bm25_scores(q, c['sparse_shift'], ov['BMX'] if m else None); ssm = np.where(ss > 0, ss, -np.inf); stop = topn(ssm, CFG['CAND'])
    n_stale = 0
    if c['refresh']:
        dset = set(dtop.tolist()); miss = [int(i) for i in stop[:50] if i not in dset]
        if miss:
            for i, v in zip(miss, enc_docs([dtext(i, ov) for i in miss])):
                if dok[i] or (c['nonfinite'] and i in c['nonfinite'][1]):
                    if float(v @ served_vec(i, c, ov)) < 0.98 or (c['nonfinite'] and i in c['nonfinite'][1]): dsm[i] = float(v @ qv); n_stale += 1
            if c['nonfinite'] and c['nonfinite'][0] == 'top': dsm[list(c['nonfinite'][1])] = -np.inf
            dtop = topn(dsm, CFG['CAND'])
    fs = collections.defaultdict(float)
    if c['fusion'] == 'minmax':                         # stack 2 fusion: min-max normalised convex combination
        for lst, sc, w in ((dtop, dsm, CFG['FUSION_ALPHA']), (stop, ss, 1 - CFG['FUSION_ALPHA'])):
            if len(lst):
                v = np.array([sc[i] for i in lst], float); lo, hi = v.min(), v.max()
                for i, x in zip(lst, v): fs[int(i)] += w * ((x - lo) / (hi - lo) if hi > lo else 1.0)
    else:                                               # R22 on stack 2: raw scores added without normalisation
        for i in dtop: fs[int(i)] += float(dsm[i])
        for i in stop: fs[int(i)] += float(ss[i])
    fused = sorted(fs, key=lambda i: -fs[i])
    if c['quality']: fused = [i for i in fused if not dthin(i, ov, q)] + [i for i in fused if dthin(i, ov, q)]
    if c['dedup']:
        kept, sh, rest = [], [], []
        for i in fused[:150]:
            s_ = shingles(dtext(i, ov))
            if any(jacc(s_, s2) >= 0.8 for s2 in sh): rest.append(i); continue
            kept.append(i); sh.append(s_)
        fused = kept + fused[150:] + rest
    depth = fused[:c['depth']]
    if c['result_cap'] is not None: depth = depth[:c['result_cap']]
    if c['ce'] == 'random':
        ce = np.random.default_rng(int(hashlib.md5(q.encode()).hexdigest()[:8], 16)).standard_normal(len(depth)).astype(np.float32)
    else: ce = ce_scores(q, [dkey(i, ov) for i in depth], [dtext(i, ov) for i in depth], c['ce_trunc'])
    order = [depth[j] for j in np.argsort(-ce, kind='stable')]; cmap = {i: float(s) for i, s in zip(depth, ce)}
    if c['quality']: order = [i for i in order if not dthin(i, ov, q)] + [i for i in order if dthin(i, ov, q)]
    return dict(q=q, qv=qv, dtop=dtop, dsc=dsm[dtop] if len(dtop) else np.zeros(0), stop=stop, ssc=ss[stop], fused=fused, depth=depth,
                ce=ce, cmap=cmap, order=order, final=order[:CFG['K_FINAL']], cov=cov, exact_top=exact_top, nf=nf, ov=ov, st=st)
def succ(tr, gold, k=5): return any(i in gold for i in tr['final'][:k])

# %% [markdown]
# ## 3. Lexical tools from the SciFact corpus (no query log exists for SciFact, so Q01/Q03 repairs use corpus co-occurrence)

# %%
import bisect, functools, nltk
nltk.download('wordnet', quiet=True); nltk.download('omw-1.4', quiet=True)
from nltk.corpus import wordnet as wn
FREQ = {w: int(DF[j]) for w, j in VOC.items() if DF[j] >= 2 and w.isalpha() and 3 <= len(w) <= 20}
def deletes1(w): return {w[:i] + w[i + 1:] for i in range(len(w))}
DEL = collections.defaultdict(list)
for w in FREQ:
    for d in deletes1(w): DEL[d].append(w)
def dl_dist(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1): d[i][0] = i
    for j in range(len(b) + 1): d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]: d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[-1][-1]
@functools.lru_cache(maxsize=None)
def spell_cands(w):
    if not w.isalpha() or len(w) < 3: return ()
    keys = {w} | deletes1(w)
    if len(w) >= 6: keys |= {d2 for d in list(keys) for d2 in deletes1(d)}
    cand = {c_ for k in keys for c_ in DEL.get(k, [])} | {k for k in keys if k in FREQ}; base = df_of(w); out = []
    for c_ in cand:
        dd = dl_dist(w, c_) if c_ != w else 99
        if dd <= (1 if len(w) < 5 else 2) and FREQ[c_] >= (2 if base == 0 else 10 * base): out.append(((dd, -FREQ[c_]), c_))
    return tuple(c_ for _, c_ in sorted(out)[:8])
SEGW = {w: math.log(N / FREQ[w]) for w in FREQ}
@functools.lru_cache(maxsize=None)
def segment(w):
    if len(w) < 7 or (w in VOC and df_of(w) >= 3): return None
    best = [(0.0, [])] + [(1e9, None)] * len(w)
    for i in range(1, len(w) + 1):
        for j in range(max(0, i - 20), i):
            p = w[j:i]
            if p in SEGW and best[j][1] is not None and best[j][0] + SEGW[p] + 2 < best[i][0]: best[i] = (best[j][0] + SEGW[p] + 2, best[j][1] + [p])
    s = best[-1][1]; return tuple(s) if s and len(s) >= 2 else None
PREF = sorted(FREQ)
@functools.lru_cache(maxsize=None)
def completions(p, n=60):
    i = bisect.bisect_left(PREF, p); out = []
    while i < len(PREF) and PREF[i].startswith(p):
        if PREF[i] != p: out.append(PREF[i])
        i += 1
    return tuple(sorted(out, key=lambda w: -FREQ[w])[:n])
@functools.lru_cache(maxsize=None)
def synonyms(w, first=False):
    ss = wn.synsets(w); return tuple(sorted({l.name().lower() for s in (ss[:1] if first else ss) for l in s.lemmas()
                                             if l.name().lower() != w and l.name().isalpha()}))
def docs_with(w): return set(BM[:, VOC[w]].indices.tolist()) if w in VOC else set()
def cooc_rank(cands, ctx, n):
    cs = [docs_with(t) for t in ctx if t in VOC and df_of(t) < N // 3]; joint = set.intersection(*cs) if cs else set()
    return sorted(cands, key=lambda w: (len(docs_with(w) & joint), sum(len(docs_with(w) & c_) for c_ in cs), FREQ.get(w, 0)), reverse=True)[:n]
WOPS = collections.Counter()
with zipfile.ZipFile(FILES['qspell']['path']) as z_:
    nm = [n for n in z_.namelist() if n.endswith('error-annotations.csv')][0]
    rows_ = csv.reader(z_.read(nm).decode('utf-8', 'replace').splitlines(), delimiter=';'); hdr = next(rows_)
    for row in rows_:
        if len(row) >= 9:
            for k_, v_ in zip(hdr[5:9], row[5:9]):
                if v_.isdigit(): WOPS[k_] += int(v_)
KEYB = 'qwertyuiop asdfghjkl zxcvbnm'.split()
def near_key(ch, rng):
    for row in KEYB:
        if ch in row: j = row.index(ch); return rng.choice([row[k] for k in (j - 1, j + 1) if 0 <= k < len(row)])
    return ch
def webis_edit(w, rng):
    ops, wt = zip(*WOPS.items()); op = rng.choices(ops, weights=wt)[0]; i = rng.randrange(1, len(w) - 1)
    if op == 'Deletion': return w[:i] + w[i + 1:]
    if op == 'Insertion': return w[:i] + near_key(w[i], rng) + w[i:]
    if op == 'Substitution': return w[:i] + near_key(w[i], rng) + w[i + 1:]
    return w[:i] + w[i + 1] + w[i] + w[i + 2:]

# %% [markdown]
# ## 4. Telemetry features (same definitions as core-28 where the signal exists on stack 2)

# %%
def spearman(a, b):
    if len(a) < 3: return 0.0
    v = np.corrcoef(np.argsort(np.argsort(a)), np.argsort(np.argsort(b)))[0, 1]; return 0.0 if np.isnan(v) else float(v)
NULL_TOP = None
def features(tr):
    global NULL_TOP
    q, st, ov = tr['q'], tr['st'], tr['ov']; qt = tok(q); f = {}; inv = [t for t in qt if t in VOC]; oov = [t for t in qt if t not in VOC]
    f['q_len'] = len(qt); f['q_oov'] = len(oov) / max(1, len(qt)); f['q_lowdf'] = sum(df_of(t) < 2 for t in qt) / max(1, len(qt))
    idf = [IDF[VOC[t]] for t in inv]; f['q_idf_mean'] = float(np.mean(idf)) if idf else 0.0; f['q_idf_max'] = float(max(idf)) if idf else 0.0
    f['q_correctable'] = sum(df_of(t) < 2 and len(spell_cands(t)) > 0 for t in qt); f['q_segmentable'] = sum(segment(t) is not None for t in oov)
    f['q_prefix'] = int(bool(qt) and df_of(qt[-1]) < 3 and len(completions(qt[-1])) > 0)
    f['q_synlow'] = sum(t.isalpha() and df_of(t) < 5 and any(df_of(s) >= 50 for s in synonyms(t)) for t in qt)
    d, s_ = tr['dsc'], tr['ssc']
    f['d1'] = float(d[0]) if len(d) else 0.0; f['d_gap'] = float(d[0] - d[1]) if len(d) > 1 else 0.0
    f['d_m5'] = float(np.mean(d[:5])) if len(d) else 0.0; f['d_std20'] = float(np.std(d[:20])) if len(d) > 1 else 0.0; f['d_n'] = len(d)
    f['s1'] = float(s_[0]) if len(s_) else 0.0; f['s_gap'] = float(s_[0] - s_[1]) if len(s_) > 1 else 0.0
    qs = set(inv); lex = lambda L: float(np.mean([len(qs & set(tok(dtext(i, ov)))) / max(1, len(qs)) for i in L[:5]])) if len(L) else 0.0
    f['s_lex5'] = lex(tr['stop']); f['d_lex5'] = lex(tr['dtop'])
    dt, stp = set(tr['dtop'][:10].tolist()), set(tr['stop'][:10].tolist()); f['ov_ds10'] = len(dt & stp) / 10
    dall, sall = set(tr['dtop'].tolist()), set(tr['stop'].tolist()); dep = tr['depth']
    f['dep_dense'] = sum(i in dall for i in dep) / max(1, len(dep)); f['dep_sparse'] = sum(i in sall for i in dep) / max(1, len(dep))
    ce = tr['ce']; srt = np.sort(ce)[::-1] if len(ce) else ce
    f['ce1'] = float(srt[0]) if len(ce) else 0.0; f['ce_gap'] = float(srt[0] - srt[1]) if len(ce) > 1 else 0.0
    f['ce_std'] = float(ce.std()) if len(ce) > 1 else 0.0; f['ce_mean'] = float(ce.mean()) if len(ce) else 0.0
    f['ce_fuse_rho'] = spearman(-np.arange(len(dep)), ce)
    dmap = {int(i): float(v) for i, v in zip(tr['dtop'], tr['dsc'])}; both = [(dmap[i], tr['cmap'][i]) for i in dep if i in dmap]
    f['ce_dense_rho'] = spearman([a for a, _ in both], [b for _, b in both]) if len(both) >= 3 else 0.0
    f['n_depth'] = len(dep); fin = tr['final']; f['n_final'] = len(fin)
    if len(fin) >= 2:
        em = np.stack([served_vec(i, st['cfg'], ov) for i in fin]); cs = em @ em.T; f['red_cos5'] = float((cs.sum() - len(fin)) / (len(fin) * (len(fin) - 1)))
        sh = [shingles(dtext(i, ov)) for i in fin]; f['dup5'] = sum(jacc(sh[a], sh[b]) >= 0.8 for a in range(len(fin)) for b in range(a + 1, len(fin)))
    else: f['red_cos5'] = f['dup5'] = 0.0
    f['thin5'] = sum(dthin(i, ov, q) for i in fin)
    f['cov'] = tr['cov']; f['ann_probe'] = len(set(tr['dtop'][:10].tolist()) & set(tr['exact_top'].tolist())) / max(1, len(tr['exact_top']))
    f['align_probe'] = float(enc_docs([dtext(int(tr['dtop'][0]), ov)])[0] @ served_vec(int(tr['dtop'][0]), st['cfg'], ov)) if len(tr['dtop']) else 1.0
    sp = [int(i) for i in tr['stop'][:CFG['PROBE_K']]]
    if sp:
        cs_ = [float(v @ served_vec(i, st['cfg'], ov)) for i, v in zip(sp, enc_docs([dtext(i, ov) for i in sp]))]
        f['stale_sparse'] = sum(c_ < 0.98 for c_ in cs_); f['stale_min'] = float(min(cs_)); f['sparse_absent_dense'] = sum(i not in dall for i in sp) / len(sp)
    else: f['stale_sparse'] = 0; f['stale_min'] = 1.0; f['sparse_absent_dense'] = 0.0
    f['q_probe_cos'] = float(tr['qv'] @ enc_q(q, 'v2'))
    if NULL_TOP is None: NULL_TOP = set(topn(E @ enc_q('', 'v2'), 10).tolist())
    f['d_null10'] = len(set(tr['dtop'][:10].tolist()) & NULL_TOP) / 10; f['nonfinite'] = tr['nf']
    return f

# %% [markdown]
# ## 5. Base queries (official BEIR train/test split), clean runs, injectors and repairs for the 20 ported faults

# %%
def qnorm(q): return ' '.join(re.sub(r"[^\w\s'-]", ' ', q.lower()).split())   # v2: punctuation stripped (v1 injector bug)
BASE = [dict(bid=f'{s}:{qid}', q=qnorm(QUERIES[qid]), split=s, gold=g) for (s, qid), g in sorted(QRELS.items()) if qid in QUERIES]
CLEAN = RES.get('CLEAN', {})
log('clean runs', len(BASE))
for n_, b in enumerate(BASE):
    if b['bid'] not in CLEAN:
        tr = run(dict(q=b['q'], cfg=mkcfg(), ov=None)); CLEAN[b['bid']] = dict(clean_tr=tr, h5=succ(tr, b['gold']))
        if n_ % 50 == 0: maybe_stop('clean_runs')
    b.update(CLEAN[b['bid']])
CLEAN_HIT = {s: float(np.mean([b['h5'] for b in BASE if b['split'] == s])) for s in ('train', 'test')}
hn = []
for b in BASE[:200]:
    HN.hnsw.efSearch = CFG['EF_CLEAN']; _, I = HN.search(enc_q(b['q'])[None, :], 10); hn.append(len(set(I[0]) & set(topn(E @ enc_q(b['q']), 10).tolist())) / 10)
PUR['hnsw_ef128_recall10_vs_exact'] = float(np.mean(hn)); log('clean Hit@5', CLEAN_HIT, 'HNSW@128 recall@10 vs exact', PUR['hnsw_ef128_recall10_vs_exact'])
def S(b, **kw):
    st = dict(q=b['q'], cfg=mkcfg(), ov=None, gold=b['gold'], k=5, bid=b['bid'], split=b['split'], meta={}); st.update(kw); return st
def content_toks(q): return [t for t in q.split() if t.isalpha() and len(t) >= 4]
def by_idf(ts): return sorted(ts, key=lambda t: -(IDF[VOC[t]] if t in VOC else 0))
def best_gold(b): return next((i for i in b['clean_tr']['order'] if i in b['gold']), min(b['gold']))
def inj_Q01(b, rng):
    ws = b['q'].split()
    if not ws or not (ws[-1].isalpha() and len(ws[-1]) >= 5): return None
    p = ws[-1][:max(3, len(ws[-1]) // 2)]; return S(b, q=' '.join(ws[:-1] + [p])) if df_of(p) < 3 else None
def inj_Q03(b, rng):
    q, n = b['q'], 0
    for t in by_idf(content_toks(q))[:3]:
        sy = [s for s in synonyms(t, True) if df_of(s) < 3] if df_of(t) >= 20 else []
        if sy: q = re.sub(rf'\b{t}\b', rng.choice(sy), q, count=1); n += 1
        if n == 2: break
    return S(b, q=q) if n else None
def inj_Q04(b, rng):
    q, n = b['q'], 0
    for t in by_idf(content_toks(q))[:2]:
        for _ in range(5):
            w = webis_edit(t, rng)
            if df_of(w) < 2 and w != t: q = re.sub(rf'\b{t}\b', w, q, count=1); n += 1; break
    return S(b, q=q) if n else None
def inj_Q05(b, rng):
    ws = b['q'].split(); idx = [i for i in range(len(ws) - 1) if ws[i].isalpha() and ws[i + 1].isalpha() and len(ws[i]) >= 3 and len(ws[i + 1]) >= 3]
    if not idx: return None
    i = rng.choice(idx); mg = ws[i] + ws[i + 1]; return S(b, q=' '.join(ws[:i] + [mg] + ws[i + 2:])) if df_of(mg) < 3 else None
def inj_K04(b, rng): return S(b, cfg=mkcfg(emb_override={i: E[rng.randrange(N)] for i in b['gold']}))
def inj_K05(b, rng):
    x = next((i for i in b['clean_tr']['order'] if i not in b['gold']), None)
    if x is None: return None
    return S(b, ov=make_overlay([dict(text=(TEXT[x] if k % 2 else b['q'] + '. ' + TEXT[x]) + f' Ref {rng.randint(1000, 9999)}.') for k in range(7)]))
def inj_K08(b, rng): return S(b, ov=make_overlay([dict(text=f"{b['q'].capitalize()} {rng.choice(['', 'review', 'study', 'notes'])}. ", thin=True) for _ in range(6)]))
def inj_R01(b, rng): return S(b, cfg=mkcfg(mask=(0.3, rng.randrange(10**6), tuple(b['gold']))))
def inj_R03(b, rng): return S(b, cfg=mkcfg(enc='trunc'))
def inj_R05(b, rng): return S(b, cfg=mkcfg(ce='random'))
def inj_R07(b, rng):
    g = best_gold(b); a = max(0, g - 1000); return S(b, cfg=mkcfg(shift=(a, min(N - 4, a + 2000), rng.choice([1, 2, 3]))))
def inj_R10(b, rng): return S(b, cfg=mkcfg(q_noise=rng.uniform(2.0, 3.5)))
def inj_R11(b, rng): return S(b, cfg=mkcfg(enc='old'))
def inj_R13(b, rng): return S(b, cfg=mkcfg(sparse_shift=rng.randint(1, 3000)))
def inj_R15(b, rng): return S(b, cfg=mkcfg(ef=rng.choice([3, 5, 8])))
def inj_R19(b, rng): return S(b, cfg=mkcfg(depth=5))
def inj_R22(b, rng): return S(b, cfg=mkcfg(fusion='raw'))
def inj_R23(b, rng): return S(b, cfg=mkcfg(result_cap=rng.choice([1, 2])))
def inj_R24(b, rng): return S(b, cfg=mkcfg(ce_trunc=24))
def inj_R25(b, rng):
    if rng.random() < 0.5: return S(b, cfg=mkcfg(nonfinite=('drop', tuple(b['gold']))))
    return S(b, cfg=mkcfg(nonfinite=('top', tuple(rng.sample(range(N), 40)))))
FAULTS = ['Q01', 'Q03', 'Q04', 'Q05', 'K04', 'K05', 'K08', 'R01', 'R03', 'R05', 'R07', 'R10', 'R11', 'R13', 'R15', 'R19', 'R22', 'R23', 'R24', 'R25']
INJ = {f: globals()[f'inj_{f}'] for f in FAULTS}; assert len(FAULTS) == 20
def with_q(st, q): return dict(st, q=q)
def with_cfg(st, **kw): c = dict(st['cfg']); c.update(kw); return dict(st, cfg=c)
def rep_Q01(st, tr):
    ws = st['q'].split()
    if not ws or df_of(ws[-1]) >= 3: return st
    cs = cooc_rank(list(completions(ws[-1])), ws[:-1], 1); return with_q(st, ' '.join(ws[:-1] + cs)) if cs else st
def rep_Q03(st, tr):
    cur = st
    for w in st['q'].split():
        sy = [s for s in synonyms(w) if df_of(s) >= 20] if w.isalpha() and df_of(w) < 5 else []
        if sy: cur = with_q(cur, re.sub(rf'\b{w}\b', cooc_rank(sy, [t for t in cur['q'].split() if t != w], 1)[0], cur['q'], count=1))
    return cur
def rep_Q04(st, tr):
    cur = st
    for w in st['q'].split():
        cs = list(spell_cands(w)) if df_of(w) < 2 else []
        if cs:
            d0 = dl_dist(w, cs[0]); best = cooc_rank([c_ for c_ in cs if dl_dist(w, c_) == d0], [t for t in cur['q'].split() if t != w], 1)[0]
            cur = with_q(cur, re.sub(rf'\b{re.escape(w)}\b', best, cur['q'], count=1))
    return cur
def rep_Q05(st, tr): return with_q(st, ' '.join(' '.join(segment(w)) if (w not in VOC and segment(w)) else w for w in st['q'].split()))
CE_FLOOR = [None]
def ann_probe(tr): return len(set(tr['dtop'][:10].tolist()) & set(tr['exact_top'].tolist())) / max(1, len(tr['exact_top']))
def rep_R15(st, tr):
    for ef in (32, CFG['EF_CLEAN']):
        s2 = with_cfg(st, ef=ef)
        if ef == CFG['EF_CLEAN'] or ann_probe(run(s2)) >= 0.999: return s2
def rep_R19(st, tr):
    for dp in (50, 100):
        s2 = with_cfg(st, depth=dp); t2 = run(s2)
        if len(t2['ce']) and float(t2['ce'].max()) >= CE_FLOOR[0]: return s2
    return s2
REP = dict(Q01=rep_Q01, Q03=rep_Q03, Q04=rep_Q04, Q05=rep_Q05,
           K04=lambda st, tr: with_cfg(st, refresh=True), K05=lambda st, tr: with_cfg(st, dedup=True), K08=lambda st, tr: with_cfg(st, quality=True),
           R01=lambda st, tr: with_cfg(st, mask=None) if tr['cov'] < 0.999 else st, R03=lambda st, tr: with_cfg(st, enc='v2', q_noise=0.0),
           R05=lambda st, tr: with_cfg(st, ce='ok'), R07=lambda st, tr: with_cfg(st, shift=None, refresh=True),
           R10=lambda st, tr: with_cfg(st, enc='v2', q_noise=0.0), R11=lambda st, tr: with_cfg(st, enc='v2', q_noise=0.0),
           R13=lambda st, tr: with_cfg(st, sparse_shift=0), R15=rep_R15, R19=rep_R19, R22=lambda st, tr: with_cfg(st, fusion='minmax'),
           R23=lambda st, tr: with_cfg(st, result_cap=None), R24=lambda st, tr: with_cfg(st, ce_trunc=None),
           R25=lambda st, tr: with_cfg(st, nonfinite=None, refresh=True))
assert set(REP) == set(FAULTS)
RULE = {'Q04': lambda f: f['q_correctable'], 'R15': lambda f: 1 - f['ann_probe'], 'R23': lambda f: CFG['K_FINAL'] - f['n_final'], 'R25': lambda f: f['nonfinite']}

# %% [markdown]
# ## 6. Hard episodes (clean succeeds, faulted fails), split quotas, detectors, repair gates, verdict

# %%
EPIS, GEN, SEEN, GSTATE = RES.get('EPIS', []), RES.get('GEN', {}), RES.get('SEEN', set()), RES.get('GSTATE', {})
QUOTA = CFG['N_HARD'] // 2
for f in FAULTS:
    if GSTATE.get(f, {}).get('done'): continue
    rng = random.Random(f'{CFG["SEED"]}-{f}'); pool = [b for b in BASE if b['h5']]; rng.shuffle(pool)
    gs = GSTATE.get(f) or dict(ptr=0, per=collections.Counter(), g=dict(pool=len(pool), attempts=0, not_applicable=0, easy=0, hard=0, hard_train=0, hard_test=0))
    if 'rng' in gs: rng.setstate(gs['rng'])
    g_ = gs['g']
    while g_['attempts'] < CFG['MAX_ATT'] and gs['ptr'] < 4 * len(pool) and (g_['hard_train'] < QUOTA or g_['hard_test'] < QUOTA):
        b = pool[gs['ptr'] % len(pool)]; gs['ptr'] += 1
        if g_['hard_' + b['split']] >= QUOTA or gs['per'][b['bid']] >= 2: continue
        g_['attempts'] += 1
        if g_['attempts'] % 25 == 0 and over_budget(): gs['rng'] = rng.getstate(); GSTATE[f] = gs; maybe_stop(f'generation:{f}')
        st = INJ[f](b, rng)
        if st is None: g_['not_applicable'] += 1; continue
        sig = hashlib.md5(repr((b['bid'], st['q'], sorted((k, str(v)) for k, v in st['cfg'].items() if k != 'emb_override'),
                                st['ov']['text'] if st['ov'] else None)).encode()).hexdigest()
        if sig in SEEN: g_['not_applicable'] += 1; continue
        SEEN.add(sig); tr = run(st)
        if succ(tr, st['gold']): g_['easy'] += 1; continue
        g_['hard'] += 1; g_['hard_' + b['split']] += 1; gs['per'][b['bid']] += 1
        EPIS.append(dict(fault=f, bid=b['bid'], split=b['split'], st=st, feats=features(tr)))
    tried = g_['attempts'] - g_['not_applicable']; g_['hard_yield'] = round(g_['hard'] / tried, 3) if tried else 0.0
    GEN[f] = g_; gs['done'] = True; GSTATE[f] = gs; log(f, g_)
if not GSTATE.get('_none'):
    for b in BASE:
        EPIS.append(dict(fault='NONE', bid=b['bid'], split=b['split'], st=dict(q=b['q'], cfg=mkcfg(), ov=None, gold=b['gold'], k=5),
                         feats=features(b['clean_tr']), clean_h5=b['h5']))
    GSTATE['_none'] = True
save_ckpt('generation_done')

FEATS = sorted(EPIS[0]['feats']); mat = lambda es: np.array([[e['feats'][k] for k in FEATS] for e in es], dtype=np.float32)
TR = [e for e in EPIS if e['split'] == 'train']; TE = [e for e in EPIS if e['split'] == 'test']
Xtr, Xte = mat(TR), mat(TE); ytr, yte = np.array([e['fault'] for e in TR]), np.array([e['fault'] for e in TE])
def boot_auc(y, s, n=500):
    if len(set(y)) < 2: return (float('nan'),) * 3
    r = np.random.default_rng(0); a = roc_auc_score(y, s); bs = [roc_auc_score(y[i], s[i]) for i in (r.integers(0, len(y), len(y)) for _ in range(n)) if len(set(y[i])) == 2]
    return a, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
hgb = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0,
                                             class_weight='balanced', random_state=CFG['SEED'])
DET = []
for f in FAULTS:
    npt, npe = int((ytr == f).sum()), int((yte == f).sum())
    row = dict(fault=f, detector='tier0_rule' if f in RULE else 'histgb_head', n_pos_train=npt, n_pos_test=npe)
    s = np.array([RULE[f](e['feats']) for e in TE]) if f in RULE else (hgb().fit(Xtr, (ytr == f).astype(int)).predict_proba(Xte)[:, 1] if npt >= 3 else None)
    if s is None: row['status'] = 'UNTRAINED'
    else:
        a, lo, hi = boot_auc((yte == f).astype(int), s); row.update(auroc=a, ci_lo=lo, ci_hi=hi)
        row['status'] = 'THIN' if npe < GATES['MIN_TEST_POS'] else 'PASS' if a >= GATES['AUROC_BAR'] else 'FAIL'
    DET.append(row); log('detector', row)
ok_ = [b['clean_tr']['ce'].max() for b in BASE if b['split'] == 'train' and b['h5'] and len(b['clean_tr']['ce'])]
CE_FLOOR[0] = float(np.percentile(ok_, 10))
def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),) * 2
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return (c - h) / d, (c + h) / d
HARM = RES.get('HARM', {}); REPG = []
for f in FAULTS:
    es = [e for e in EPIS if e['fault'] == f]
    for n_, e in enumerate(es):
        if 'rescued' not in e: e['rescued'] = bool(succ(run(REP[f](e['st'], run(e['st']))), e['st']['gold']))
        if n_ % 10 == 0: maybe_stop(f'repair:{f}')
    if f not in HARM:
        cl = [b for b in BASE if b['split'] == 'test' and b['h5']][:CFG['N_HARM']]
        HARM[f] = (len(cl), sum(not succ(run(REP[f](dict(q=b['q'], cfg=mkcfg(), ov=None), b['clean_tr'])), b['gold']) for b in cl))
    k = sum(e['rescued'] for e in es); lo, hi = wilson(k, len(es)); cn, lost = HARM[f]
    st_ = 'THIN' if len(es) < GATES['MIN_REPAIR_N'] else 'PASS' if lo >= GATES['RESCUE_BAR_LB'] and lost / max(1, cn) <= GATES['MAX_HARM'] else 'FAIL'
    REPG.append(dict(fault=f, n_hard=len(es), rescued=k, rescue_rate=k / len(es) if es else float('nan'), ci_lo=lo, ci_hi=hi, clean_n=cn, clean_lost=lost, status=st_))
    log('repair', REPG[-1])
save_ckpt('repair_done')
ds_, rs_ = {r['fault']: r['status'] for r in DET}, {r['fault']: r['status'] for r in REPG}
SOLVED = [dict(fault=f, detector=ds_[f], repair=rs_[f], solved=ds_[f] == 'PASS' and rs_[f] == 'PASS') for f in FAULTS]
n_sol = sum(r['solved'] for r in SOLVED)
VERDICT = dict(domain=f'BEIR {DATASET}', stack='e5-small-v2 + FAISS HNSW + BM25 + min-max fusion + MiniLM-L6 reranker', clean_hit5=CLEAN_HIT,
               detectors_pass=sum(v == 'PASS' for v in ds_.values()), repairs_pass=sum(v == 'PASS' for v in rs_.values()), solved_both=n_sol,
               of=len(FAULTS), suite_ports=n_sol >= GATES['PORT_TARGET'], not_solved=[r['fault'] for r in SOLVED if not r['solved']],
               purity=PUR, verify=VERIFY, protocol=json.load(open(PROTO)))
for name, rows in [('port_episodes_summary', [dict(fault=f, **g) for f, g in GEN.items()]), ('port_detector_gates', DET),
                   ('port_repair_gates', REPG), ('port_solved', SOLVED)]:
    pd.DataFrame(rows).to_csv(os.path.join(OUT, f'{name}.csv'), index=False)
json.dump(VERDICT, open(os.path.join(OUT, 'PORT_VERDICT.json'), 'w'), indent=1, default=str)
md = [f'# DiagRAG portability arm v2 ({DATASET}) — judged run', '', '```', json.dumps({k: v for k, v in VERDICT.items() if k != 'protocol'}, indent=1, default=str), '```', '',
      '## Episodes', '', pd.DataFrame([dict(fault=f, **g) for f, g in GEN.items()]).to_markdown(index=False), '',
      '## Detector gates', '', pd.DataFrame(DET).to_markdown(index=False, floatfmt='.4f'), '',
      '## Repair gates', '', pd.DataFrame(REPG).to_markdown(index=False, floatfmt='.3f'), '']
open(os.path.join(OUT, 'PORT_REPORT.md'), 'w').write('\n'.join(md)); log('PORT VERDICT', {k: v for k, v in VERDICT.items() if k not in ('protocol', 'purity', 'verify')})
log('done. outputs in', OUT)
