# %% [markdown]
# # DiagRAG framework-stack arm v2 — LangChain pipeline, fixes from the v1 judged run (judged_langchain_scifact/)
# Fixes: K08 repair removes thin docs BEFORE the cross-encoder (v1 only reordered them, CrossEncoderReranker re-sorted);
# R23 detected from the dense leg's own result count (v1 used the final count, which EnsembleRetriever keeps at 5);
# K05 = re-ingestion with different chunk boundaries (exact copies are collapsed by EnsembleRetriever's own dedup, a v1 finding),
# repaired by one-chunk-per-source dedup; K11 deleted versions made distinct for the same reason. Gates unchanged.
# Stack 3 is built only from LangChain components with their documented defaults or tutorial values:
#   RecursiveCharacterTextSplitter(1000, 200) -> HuggingFaceBgeEmbeddings(bge-small-en-v1.5) -> FAISS vector store
#   + BM25Retriever -> EnsembleRetriever (weighted RRF) -> CrossEncoderReranker(ms-marco-MiniLM-L-6-v2, top_n=5).
# Faults are injected through the framework's own knobs and objects (k, weights, query_instruction, embedding model,
# preprocess_func, score_threshold, cross-encoder max_length, add_documents re-ingestion, FAISS vectors), each tied to a
# field report in docs/EVIDENCE_AND_NOVELTY_REPORT.md. Same domain as port2 SciFact, so stack 2 vs stack 3 differ only
# in the stack. Gates identical to core-28, frozen in LC_PROTOCOL.json before any result.

# %%
import os, sys, subprocess, json, re, time, math, random, hashlib, zipfile, csv, collections, pickle
ON_KAGGLE = os.path.exists('/kaggle')
WORK = '/kaggle/working' if ON_KAGGLE else os.environ.get('DIAGRAG_WORK', os.getcwd())
DATA = '/tmp/diagrag_lc_data' if ON_KAGGLE else os.path.join(WORK, 'port_data'); OUT = os.path.join(WORK, 'langchain2_out')
os.makedirs(DATA, exist_ok=True); os.makedirs(OUT, exist_ok=True)
for mod, pk in [('langchain_community', 'langchain-community'), ('langchain_text_splitters', 'langchain-text-splitters'), ('rank_bm25', 'rank_bm25'),
                ('faiss', 'faiss-cpu'), ('sentence_transformers', 'sentence-transformers'), ('tabulate', 'tabulate')]:
    try: __import__(mod)
    except ImportError: subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pk], check=False)
import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, torch, faiss
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
try:
    from langchain_classic.retrievers import EnsembleRetriever
    from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
except ImportError:
    from langchain.retrievers import EnsembleRetriever
    from langchain.retrievers.document_compressors import CrossEncoderReranker
DEV = 'cuda' if torch.cuda.is_available() else 'cpu'
if DEV == 'cpu': torch.set_num_threads(int(os.environ.get('TORCH_THREADS', os.cpu_count() or 4)))
CFG = dict(SEED=int(os.environ.get('SEED', 11)), K=25, TOP_N=5, W=[0.5, 0.5], THRESH=None, N_HARD=int(os.environ.get('N_HARD', 50)),
           MAX_ATT=int(os.environ.get('MAX_ATT', 2500)), N_HARM=int(os.environ.get('N_HARM', 20)), TIME_BUDGET=int(os.environ.get('TIME_BUDGET', 0)),
           EMB='BAAI/bge-small-en-v1.5', EMB_SWAP='sentence-transformers/all-MiniLM-L6-v2', CE='cross-encoder/ms-marco-MiniLM-L-6-v2',
           INSTR='Represent this sentence for searching relevant passages: ')
GATES = dict(detector='held-out one-vs-rest AUROC >= 0.70 AND >= 20 held-out positives',
             repair='>= 20 hard episodes AND Wilson 95% lower bound >= 0.50 AND <= 10% of clean successes lost',
             AUROC_BAR=0.70, MIN_TEST_POS=20, RESCUE_BAR_LB=0.50, MIN_REPAIR_N=20, MAX_HARM=0.10,
             summary='claim "the suite runs on a framework stack" only if >= 11 of the 15 framework-expressible faults pass both gates', TARGET=11)
random.seed(CFG['SEED']); np.random.seed(CFG['SEED'])
T0 = time.time()
def log(*a): print(f'[{time.time()-T0:7.0f}s]', *a, flush=True)
CKPT = os.path.join(OUT, 'checkpoint.pkl'); RES = pickle.load(open(CKPT, 'rb')) if os.path.exists(CKPT) else {}
def over_budget(): return CFG['TIME_BUDGET'] > 0 and time.time() - T0 > CFG['TIME_BUDGET']
def save_ckpt(stage):
    keep = {k: globals()[k] for k in ('CLEAN', 'EPIS', 'GEN', 'GSTATE', 'SEEN', 'HARM') if k in globals()}; keep['stage'] = stage
    pickle.dump(keep, open(CKPT + '.tmp', 'wb'), protocol=4); os.replace(CKPT + '.tmp', CKPT); log('checkpoint saved:', stage)
def maybe_stop(stage):
    if over_budget(): save_ckpt(stage); log('TIME_BUDGET reached - run again to resume'); raise SystemExit(0)
PROTO = os.path.join(OUT, 'LC2_PROTOCOL.json')
if not os.path.exists(PROTO):
    import langchain_community, langchain_core
    json.dump(dict(created_utc=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()), gates=GATES, cfg=CFG, device=DEV,
                   versions=dict(langchain_core=langchain_core.__version__, langchain_community=langchain_community.__version__, faiss=faiss.__version__),
                   code_sha256=hashlib.sha256(open(__file__, 'rb').read()).hexdigest() if '__file__' in globals() else 'notebook'), open(PROTO, 'w'), indent=1)

# %% [markdown]
# ## 1. Data, chunking, and the clean LangChain pipeline

# %%
F = dict(name='scifact.zip', size=2816079, url='https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scifact.zip',
         sha='536e14446a0ba56ed1398ab1055f39fe852686ecad24a6306c80c490fa8e0165')
p = os.path.join(DATA, F['name'])
if not (os.path.exists(p) and os.path.getsize(p) == F['size']): subprocess.run(['curl', '-sL', '--retry', '3', '-o', p, F['url']], check=True)
assert os.path.getsize(p) == F['size'] and hashlib.sha256(open(p, 'rb').read()).hexdigest() == F['sha']
zf = zipfile.ZipFile(p); rd = lambda n: zf.read(n).decode('utf-8')
RAW = [json.loads(l) for l in rd('scifact/corpus.jsonl').splitlines()]
QUERIES = {j['_id']: j['text'] for j in map(json.loads, rd('scifact/queries.jsonl').splitlines())}
qrels = collections.defaultdict(set)
for split in ('train', 'test'):
    for row in list(csv.reader(rd(f'scifact/qrels/{split}.tsv').splitlines(), delimiter='\t'))[1:]:
        if int(row[2]) > 0: qrels[row[0]].add(row[1])
SPLITTER = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
CHUNKS = SPLITTER.split_documents([Document(page_content=(d.get('title') or '') + '. ' + d['text'], metadata=dict(doc_id=d['_id'])) for d in RAW])
for k, c in enumerate(CHUNKS): c.metadata['cid'] = k
log('docs', len(RAW), 'chunks', len(CHUNKS))
EMB = HuggingFaceBgeEmbeddings(model_name=CFG['EMB'], encode_kwargs=dict(normalize_embeddings=True), query_instruction=CFG['INSTR'])
EMB_NOINSTR = HuggingFaceBgeEmbeddings(model_name=CFG['EMB'], encode_kwargs=dict(normalize_embeddings=True), query_instruction='')
EMB_SWAP = HuggingFaceBgeEmbeddings(model_name=CFG['EMB_SWAP'], encode_kwargs=dict(normalize_embeddings=True), query_instruction='')
_vf = os.path.join(OUT, 'chunk_vectors.npy')
if os.path.exists(_vf): VEC = np.load(_vf)
else: VEC = np.asarray(EMB.embed_documents([c.page_content for c in CHUNKS]), np.float32); np.save(_vf, VEC)
TEXTS = [c.page_content for c in CHUNKS]
def make_store(vec, chunks):
    return FAISS.from_embeddings(list(zip([c.page_content for c in chunks], [list(map(float, v)) for v in vec])), EMB, metadatas=[c.metadata for c in chunks])
STORE = make_store(VEC, CHUNKS)
BASE_MAP = dict(STORE.index_to_docstore_id); BASE_DOCS = dict(STORE.docstore._dict)
from langchain_community.docstore.in_memory import InMemoryDocstore
def lower_pre(t): return re.findall(r'[a-z0-9]+', t.lower())
BM25 = BM25Retriever.from_documents(CHUNKS, k=CFG['K'], preprocess_func=lower_pre)
BM25_DEFAULT = BM25Retriever.from_documents(CHUNKS, k=CFG['K'])           # framework default preprocess: str.split(), no lowercasing
CEM = HuggingFaceCrossEncoder(model_name=CFG['CE'])
CEM_TRUNC = HuggingFaceCrossEncoder(model_name=CFG['CE'], model_kwargs=dict(max_length=16))
VOCDF = collections.Counter(w for t in TEXTS for w in set(lower_pre(t)))
def df_of(w): return VOCDF.get(w, 0)

# %% [markdown]
# ## 2. One pipeline run through LangChain objects; faults are changes to those objects

# %%
from langchain_community.document_transformers import EmbeddingsRedundantFilter
REDUNDANT = EmbeddingsRedundantFilter(embeddings=EMB, similarity_threshold=0.98)   # LangChain's own dedup component (K05 repair)
DEFAULT = dict(emb='ok', bm25='ok', k=CFG['K'], w=tuple(CFG['W']), thresh=None, ce='ok', vec=None, drop=None, extra=None, registry=False,
               dedup=False, thin_filter=False)
def mkcfg(**kw): c = dict(DEFAULT); c.update(kw); return c
_STORES, _BM, _CEC = {}, {}, {}
def store_for(c):
    """FAISS store as configured: optionally with corrupted vectors (vec), dropped rows (drop) and re-ingested extra docs."""
    key = (c['emb'], c['vec'] is not None and hash(str(sorted(c['vec'].items())) if isinstance(c['vec'], dict) else c['vec']), c['drop'], c['extra'] and tuple(d['text'] for d in c['extra']))
    if key in _STORES: return _STORES[key]
    emb = dict(ok=EMB, noinstr=EMB_NOINSTR, swap=EMB_SWAP)[c['emb']]
    # Same LangChain FAISS store as FAISS.from_embeddings (IndexFlatL2 + InMemoryDocstore + id map), assembled directly from the
    # numpy vectors so a per-episode store costs milliseconds; NaN rows go into the real faiss index exactly as before.
    V = VEC.copy() if c['vec'] else VEC
    if c['vec']:
        for i, v in c['vec'].items(): V[i] = v
    dropset = set(c['drop'] or ()); rows = [i for i in range(len(CHUNKS)) if i not in dropset]
    ids = [BASE_MAP[i] for i in rows]; ch = [CHUNKS[i] for i in rows]; ds = {k: BASE_DOCS[k] for k in ids}; Vall = V[rows]
    if c['extra']:
        xd = [Document(page_content=d['text'], metadata=dict(doc_id=d.get('doc_id', 'ov'), cid=-1, deleted=d.get('deleted', False), thin=d.get('thin', False))) for d in c['extra']]
        xv = np.asarray(EMB.embed_documents([d.page_content for d in xd]), np.float32)
        for k, d in enumerate(xd): ds[f'extra-{k}'] = d; ids.append(f'extra-{k}')
        Vall = np.concatenate([Vall, xv]); ch = ch + xd
    index = faiss.IndexFlatL2(VEC.shape[1]); index.add(np.ascontiguousarray(Vall, dtype=np.float32))
    st = FAISS(embedding_function=emb, index=index, docstore=InMemoryDocstore(ds), index_to_docstore_id=dict(enumerate(ids)))
    if len(_STORES) > 64: _STORES.clear()
    _STORES[key] = (st, ch); return _STORES[key]
def bm25_for(c, ch):
    key = (c['bm25'], c['extra'] and tuple(d['text'] for d in c['extra']), c['drop'], c['k'])
    if key not in _BM:
        if len(_BM) > 32: _BM.clear()
        _BM[key] = BM25Retriever.from_documents(ch, k=c['k'], **({} if c['bm25'] == 'default' else dict(preprocess_func=lower_pre)))
    return _BM[key]
def ce_score(q, docs, model):
    out = []
    for d in docs:
        k = (q, d.page_content, id(model))
        if k not in _CEC: _CEC[k] = None
        out.append(k)
    todo = [k for k in out if _CEC[k] is None]
    if todo:
        for k, s in zip(todo, model.score([(k[0], k[1]) for k in todo])): _CEC[k] = float(s)
    return np.array([_CEC[k] for k in out], np.float32)
def run(st):
    c, q = st['cfg'], st['q']; store, ch = store_for(c)
    sk = dict(k=c['k']) if c['thresh'] is None else dict(k=c['k'], score_threshold=c['thresh'])
    dense = store.as_retriever(search_type='similarity' if c['thresh'] is None else 'similarity_score_threshold', search_kwargs=sk)
    ens = EnsembleRetriever(retrievers=[dense, bm25_for(c, ch)], weights=list(c['w']))
    dense_leg = dense.invoke(q); cand = ens.invoke(q)[:CFG['K']]
    if c['registry']: cand = [d for d in cand if not d.metadata.get('deleted')]                       # K11 repair: reconcile with source
    if c['thin_filter']: cand = [d for d in cand if len(d.page_content.split('. ', 1)[-1].strip()) >= 60]   # v2: removed, not reordered
    if c['dedup'] and len(cand) > 1:                                                                   # v2 K05 repair: one chunk per source doc
        seen_, kept_ = set(), []
        for d in cand:
            if d.metadata.get('doc_id') not in seen_: kept_.append(d); seen_.add(d.metadata.get('doc_id'))
        cand = kept_
    model = CEM_TRUNC if c['ce'] == 'trunc' else CEM
    final = list(CrossEncoderReranker(model=model, top_n=CFG['TOP_N']).compress_documents(cand, q)) if cand else []
    qv = np.asarray(dict(ok=EMB, noinstr=EMB_NOINSTR, swap=EMB_SWAP)[c['emb']].embed_query(q), np.float32)
    dd = store.similarity_search_with_score_by_vector(list(map(float, qv)), k=c['k'])
    D, I = store.index.search(qv[None, :], c['k'])
    return dict(dense_leg_n=len(dense_leg), q=q, cfg=c, cand=cand, final=final, ce=ce_score(q, cand, model) if cand else np.zeros(0), dense=dd, qv=qv, store=store, raw_minus1=int((I[0] < 0).sum()),
                bm=bm25_for(c, ch).invoke(q))
def doc_ids(docs): return [d.metadata.get('doc_id') for d in docs]
def succ(tr, gold): return any(d in gold for d in doc_ids(tr['final'][:CFG['TOP_N']]))

# %% [markdown]
# ## 3. Telemetry an application can read from its own LangChain objects

# %%
def spearman(a, b):
    if len(a) < 3: return 0.0
    v = np.corrcoef(np.argsort(np.argsort(a)), np.argsort(np.argsort(b)))[0, 1]; return 0.0 if np.isnan(v) else float(v)
def shingle(t, n=4):
    w = lower_pre(t); return {' '.join(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}
def features(tr):
    q = tr['q']; qt = lower_pre(q); f = {}
    f['q_len'] = len(qt); f['q_oov'] = sum(df_of(t) == 0 for t in qt) / max(1, len(qt)); f['q_lowdf'] = sum(df_of(t) < 2 for t in qt) / max(1, len(qt))
    f['q_last_lowdf'] = int(bool(qt) and df_of(qt[-1]) < 2); f['q_long_oov'] = sum(df_of(t) == 0 and len(t) >= 9 for t in qt)
    ds = np.array([s for _, s in tr['dense']], float) if tr['dense'] else np.zeros(1)
    f['d_best'] = float(ds.min()); f['d_gap'] = float(ds[1] - ds[0]) if len(ds) > 1 else 0.0; f['d_n'] = len(tr['dense']); f['raw_minus1'] = tr['raw_minus1']
    dn, bn = set(doc_ids([d for d, _ in tr['dense']][:10])), set(doc_ids(tr['bm'][:10])); f['ov_db10'] = len(dn & bn) / 10
    qs = set(qt); lex = lambda L: float(np.mean([len(qs & set(lower_pre(d.page_content))) / max(1, len(qs)) for d in L[:5]])) if L else 0.0
    f['bm_lex5'] = lex(tr['bm']); f['d_lex5'] = lex([d for d, _ in tr['dense']])
    ce = tr['ce']; srt = np.sort(ce)[::-1] if len(ce) else np.zeros(1)
    f['ce1'] = float(srt[0]); f['ce_gap'] = float(srt[0] - srt[1]) if len(srt) > 1 else 0.0; f['ce_std'] = float(ce.std()) if len(ce) > 1 else 0.0
    f['ce_ens_rho'] = spearman(-np.arange(len(ce)), ce); f['n_cand'] = len(tr['cand']); f['n_final'] = len(tr['final'])
    fin = tr['final']; sh = [shingle(d.page_content) for d in fin]
    f['dup5'] = sum(len(sh[a] & sh[b]) / max(1, len(sh[a] | sh[b])) >= 0.8 for a in range(len(fin)) for b in range(a + 1, len(fin)))
    f['thin5'] = sum(len(d.page_content.split('. ', 1)[-1].strip()) < 60 for d in fin); f['deleted5'] = sum(bool(d.metadata.get('deleted')) for d in fin)
    f['unknown_src5'] = sum(d.metadata.get('cid', 0) == -1 for d in fin)
    # index-health probe: reconstruct stored vectors of the top BM25 chunks and compare with a fresh embedding of their text
    st = tr['store']; inv = {v: k for k, v in st.index_to_docstore_id.items()}; cs_ = []
    for d in tr['bm'][:8]:
        hit = [k for k, doc in st.docstore._dict.items() if doc.page_content == d.page_content][:1]
        if hit and hit[0] in inv:
            v = st.index.reconstruct(int(inv[hit[0]])); fv = np.asarray(EMB.embed_documents([d.page_content])[0], np.float32)
            cs_.append(float(np.dot(v, fv)) if np.all(np.isfinite(v)) else -1.0)
    f['stale_probe'] = sum(c_ < 0.98 for c_ in cs_); f['stale_min'] = float(min(cs_)) if cs_ else 1.0
    f['bm_absent_dense'] = len(bn - set(doc_ids([d for d, _ in tr['dense']]))) / 10
    f['q_probe'] = float(tr['qv'] @ np.asarray(EMB.embed_query(q), np.float32))       # query-path probe vs pinned config
    f['index_rows'] = st.index.ntotal / len(CHUNKS); f['dense_leg_n'] = tr['dense_leg_n']
    return f

def _nonfinite(st):
    X = st.index.reconstruct_n(0, st.index.ntotal); return int((~np.isfinite(X).all(1)).sum())
_features0 = features
def features(tr):
    f = _features0(tr); f['nonfinite_rows'] = _nonfinite(tr['store']); return f

# %% [markdown]
# ## 4. Base queries, faults through framework knobs, repairs through framework knobs

# %%
from symspellpy import SymSpell
import wordsegment; wordsegment.load()
SYM = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
for w, n in VOCDF.items():
    if w.isalpha() and n >= 2: SYM.create_dictionary_entry(w, n)      # external corrector, dictionary built from the corpus
def qnorm(q): return ' '.join(re.sub(r"[^\w\s'-]", ' ', q.lower()).split())
def hsplit(qid): return 'test' if int(hashlib.md5(f'port2|scifact|{qid}'.encode()).hexdigest()[:8], 16) % 2 else 'train'   # same split as port2
BASE = [dict(bid=qid, q=qnorm(QUERIES[qid]), split=hsplit(qid), gold=set(g)) for qid, g in sorted(qrels.items()) if qid in QUERIES]
CLEAN = RES.get('CLEAN', {})
for n_, b in enumerate(BASE):
    if b['bid'] not in CLEAN:
        tr = run(dict(q=b['q'], cfg=mkcfg())); CLEAN[b['bid']] = dict(h5=succ(tr, b['gold']), feats=features(tr), order=doc_ids(tr['final']))
        if n_ % 50 == 0: maybe_stop('clean_runs')
    b.update(CLEAN[b['bid']])
CLEAN_HIT = {s: float(np.mean([b['h5'] for b in BASE if b['split'] == s])) for s in ('train', 'test')}; log('clean Hit@5', CLEAN_HIT)
def S(b, **kw):
    st = dict(q=b['q'], cfg=mkcfg(), gold=b['gold'], bid=b['bid'], split=b['split']); st.update(kw); return st
def gold_rows(b): return [i for i, c in enumerate(CHUNKS) if c.metadata['doc_id'] in b['gold']]
def edit(w, rng):
    i = rng.randrange(1, len(w) - 1); op = rng.choice('dst')
    return w[:i] + w[i + 1:] if op == 'd' else w[:i] + rng.choice('etaoinshr') + w[i + 1:] if op == 's' else w[:i] + w[i + 1] + w[i] + w[i + 2:]
def inj_Q04(b, rng):
    ts = sorted([t for t in b['q'].split() if t.isalpha() and len(t) >= 5], key=lambda t: df_of(t))[:2]; q = b['q']
    for t in ts:
        w = edit(t, rng)
        if df_of(w) == 0: q = re.sub(rf'\b{t}\b', w, q, count=1)
    return S(b, q=q) if q != b['q'] else None
def inj_Q05(b, rng):
    ws = b['q'].split(); idx = [i for i in range(len(ws) - 1) if ws[i].isalpha() and ws[i + 1].isalpha() and len(ws[i]) >= 3 and len(ws[i + 1]) >= 3]
    if not idx: return None
    i = rng.choice(idx); return S(b, q=' '.join(ws[:i] + [ws[i] + ws[i + 1]] + ws[i + 2:]))
def inj_K04(b, rng): return S(b, cfg=mkcfg(vec={i: VEC[rng.randrange(len(VEC))] for i in gold_rows(b)}))                      # stale vectors (I26, I27)
def inj_K05(b, rng):   # re-ingestion duplicates (llama_index#8832): a competing chunk added again several times
    x = next((d for d in b['order'] if d not in b['gold']), None)
    if x is None: return None
    full = next((d.get('title') or '') + '. ' + d['text'] for d in RAW if d['_id'] == x); w = full.split(); n_ = max(20, len(w) // 4)
    pieces = [' '.join(w[o:o + 3 * n_]) for o in range(0, max(1, len(w) - n_), max(1, n_ // 2))][:6]   # re-chunked with shifted boundaries
    return S(b, cfg=mkcfg(extra=[dict(text=(b['q'] + '. ' if k % 2 == 0 else '') + p_, doc_id=x) for k, p_ in enumerate(pieces)]))
def inj_K08(b, rng): return S(b, cfg=mkcfg(extra=[dict(text=f"{b['q'].capitalize()} {rng.choice(['', 'review', 'study', 'notes'])}. ", thin=True) for _ in range(6)]))
def inj_K11(b, rng):   # deleted documents still served (weaviate#3868, milvus#16961)
    g = gold_rows(b); t = CHUNKS[g[0]].page_content
    return S(b, cfg=mkcfg(extra=[dict(text=f"{b['q']}. {t} (archived version {k + 1})", doc_id='deleted-' + str(k), deleted=True) for k in range(5)]))
def inj_R01(b, rng): return S(b, cfg=mkcfg(drop=tuple(sorted(set(gold_rows(b)) | set(rng.sample(range(len(CHUNKS)), len(CHUNKS) // 3))))))   # rows missing (I7, I8)
def inj_R03(b, rng): return S(b, cfg=mkcfg(emb='noinstr'))                     # BGE query_instruction missing (FlagEmbedding#148)
def inj_R11(b, rng): return S(b, cfg=mkcfg(emb='swap'))                        # query embedded by another 384-d model, index not rebuilt (I31)
def inj_R13(b, rng): return S(b, cfg=mkcfg(bm25='default'))                    # BM25Retriever default preprocess: case-sensitive str.split (I20, I21)
def inj_R19(b, rng): return S(b, cfg=mkcfg(k=4))                               # retriever k left at the framework default of 4 (I18, I19)
def inj_R22(b, rng): return S(b, cfg=mkcfg(w=rng.choice([(1.0, 0.0), (0.0, 1.0)])))   # ensemble weights bound wrongly (haystack#12646)
def inj_R23(b, rng): return S(b, cfg=mkcfg(thresh=rng.choice([0.6, 0.7])))     # similarity_score_threshold mis-scaled (langchain#12707)
def inj_R24(b, rng): return S(b, cfg=mkcfg(ce='trunc'))                        # cross-encoder max_length too small (sentence-transformers#4060)
def inj_R25(b, rng): return S(b, cfg=mkcfg(vec={i: np.full(VEC.shape[1], np.nan, np.float32) for i in gold_rows(b)}))   # NaN vectors (faiss#5684)
FAULTS = ['Q04', 'Q05', 'K04', 'K05', 'K08', 'K11', 'R01', 'R03', 'R11', 'R13', 'R19', 'R22', 'R23', 'R24', 'R25']
INJ = {f: globals()[f'inj_{f}'] for f in FAULTS}
def with_q(st, q): return dict(st, q=q)
def with_cfg(st, **kw): c = dict(st['cfg']); c.update(kw); return dict(st, cfg=c)
def rep_Q04(st, tr): return with_q(st, ' '.join((SYM.lookup(w, 0, max_edit_distance=2) or [None])[0].term if (df_of(w) == 0 and SYM.lookup(w, 0, max_edit_distance=2)) else w for w in st['q'].split()))
def rep_Q05(st, tr): return with_q(st, ' '.join(' '.join(wordsegment.segment(w)) if (df_of(w) == 0 and len(w) >= 7) else w for w in st['q'].split()))
REP = dict(Q04=rep_Q04, Q05=rep_Q05, K04=lambda st, tr: with_cfg(st, vec=None), K05=lambda st, tr: with_cfg(st, dedup=True),
           K08=lambda st, tr: with_cfg(st, thin_filter=True), K11=lambda st, tr: with_cfg(st, registry=True), R01=lambda st, tr: with_cfg(st, drop=None),
           R03=lambda st, tr: with_cfg(st, emb='ok'), R11=lambda st, tr: with_cfg(st, emb='ok'), R13=lambda st, tr: with_cfg(st, bm25='ok'),
           R19=lambda st, tr: with_cfg(st, k=CFG['K']), R22=lambda st, tr: with_cfg(st, w=tuple(CFG['W'])), R23=lambda st, tr: with_cfg(st, thresh=None),
           R24=lambda st, tr: with_cfg(st, ce='ok'), R25=lambda st, tr: with_cfg(st, vec=None))
RULE = {'R25': lambda f: f['nonfinite_rows'], 'R01': lambda f: 1 - f['index_rows'], 'K11': lambda f: f['deleted5'], 'R23': lambda f: CFG['K'] - f['dense_leg_n']}
assert set(REP) == set(FAULTS) == set(INJ)

# %% [markdown]
# ## 5. Hard episodes, detectors, repair gates, verdict (identical gate logic to core-28)

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
        sig = hashlib.md5(repr((b['bid'], st['q'], sorted((k, str(v)[:200]) for k, v in st['cfg'].items()))).encode()).hexdigest()
        if sig in SEEN: g_['not_applicable'] += 1; continue
        SEEN.add(sig); tr = run(st)
        if succ(tr, st['gold']): g_['easy'] += 1; continue
        g_['hard'] += 1; g_['hard_' + b['split']] += 1; gs['per'][b['bid']] += 1
        EPIS.append(dict(fault=f, bid=b['bid'], split=b['split'], st=st, feats=features(tr)))
    tried = g_['attempts'] - g_['not_applicable']; g_['hard_yield'] = round(g_['hard'] / tried, 3) if tried else 0.0
    GEN[f] = g_; gs['done'] = True; GSTATE[f] = gs; log(f, g_)
if not GSTATE.get('_none'):
    for b in BASE: EPIS.append(dict(fault='NONE', bid=b['bid'], split=b['split'], st=dict(q=b['q'], cfg=mkcfg(), gold=b['gold']), feats=b['feats'], clean_h5=b['h5']))
    GSTATE['_none'] = True
save_ckpt('generation_done')
FEATS = sorted(EPIS[0]['feats']); mat = lambda es: np.array([[e['feats'][k] for k in FEATS] for e in es], dtype=np.float32)
TR = [e for e in EPIS if e['split'] == 'train']; TE = [e for e in EPIS if e['split'] == 'test']
Xtr, Xte = mat(TR), mat(TE); ytr, yte = np.array([e['fault'] for e in TR]), np.array([e['fault'] for e in TE])
def boot_auc(y, s, n=500):
    if len(set(y)) < 2: return (float('nan'),) * 3
    r = np.random.default_rng(0); a = roc_auc_score(y, s); bs = [roc_auc_score(y[i], s[i]) for i in (r.integers(0, len(y), len(y)) for _ in range(n)) if len(set(y[i])) == 2]
    return a, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
hgb = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=CFG['SEED'])
DET = []
for f in FAULTS:
    npt, npe = int((ytr == f).sum()), int((yte == f).sum()); row = dict(fault=f, detector='tier0_rule' if f in RULE else 'histgb_head', n_pos_train=npt, n_pos_test=npe)
    s = np.array([RULE[f](e['feats']) for e in TE]) if f in RULE else (hgb().fit(Xtr, (ytr == f).astype(int)).predict_proba(Xte)[:, 1] if npt >= 3 else None)
    if s is None: row['status'] = 'UNTRAINED'
    else:
        a, lo, hi = boot_auc((yte == f).astype(int), s); row.update(auroc=a, ci_lo=lo, ci_hi=hi)
        row['status'] = 'THIN' if npe < GATES['MIN_TEST_POS'] else 'PASS' if a >= GATES['AUROC_BAR'] else 'FAIL'
    DET.append(row); log('detector', row)
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
        HARM[f] = (len(cl), sum(not succ(run(REP[f](dict(q=b['q'], cfg=mkcfg()), None)), b['gold']) for b in cl))
    k = sum(e['rescued'] for e in es); lo, hi = wilson(k, len(es)); cn, lost = HARM[f]
    st_ = 'THIN' if len(es) < GATES['MIN_REPAIR_N'] else 'PASS' if lo >= GATES['RESCUE_BAR_LB'] and lost / max(1, cn) <= GATES['MAX_HARM'] else 'FAIL'
    REPG.append(dict(fault=f, n_hard=len(es), rescued=k, rescue_rate=k / len(es) if es else float('nan'), ci_lo=lo, ci_hi=hi, clean_n=cn, clean_lost=lost, status=st_)); log('repair', REPG[-1])
save_ckpt('repair_done')
ds_, rs_ = {r['fault']: r['status'] for r in DET}, {r['fault']: r['status'] for r in REPG}
SOLVED = [dict(fault=f, detector=ds_[f], repair=rs_[f], solved=ds_[f] == 'PASS' and rs_[f] == 'PASS') for f in FAULTS]; n_sol = sum(r['solved'] for r in SOLVED)
VERDICT = dict(version='langchain arm v2', domain='BEIR SciFact (chunked 1000/200)', stack='LangChain: RecursiveCharacterTextSplitter + HuggingFaceBgeEmbeddings(bge-small) + FAISS + BM25Retriever + EnsembleRetriever + CrossEncoderReranker',
               clean_hit5=CLEAN_HIT, chunks=len(CHUNKS), detectors_pass=sum(v == 'PASS' for v in ds_.values()), repairs_pass=sum(v == 'PASS' for v in rs_.values()),
               solved_both=n_sol, of=len(FAULTS), framework_claim=n_sol >= GATES['TARGET'], not_solved=[r['fault'] for r in SOLVED if not r['solved']],
               protocol=json.load(open(PROTO)))
for name, rows in [('lc_episodes_summary', [dict(fault=f, **g) for f, g in GEN.items()]), ('lc_detector_gates', DET), ('lc_repair_gates', REPG), ('lc_solved', SOLVED)]:
    pd.DataFrame(rows).to_csv(os.path.join(OUT, f'{name}.csv'), index=False)
json.dump(VERDICT, open(os.path.join(OUT, 'LC_VERDICT.json'), 'w'), indent=1, default=str)
open(os.path.join(OUT, 'LC_REPORT.md'), 'w').write('\n'.join(['# DiagRAG framework-stack arm (LangChain) — judged run', '', '```', json.dumps({k: v for k, v in VERDICT.items() if k != 'protocol'}, indent=1, default=str), '```', '',
    '## Episodes', '', pd.DataFrame([dict(fault=f, **g) for f, g in GEN.items()]).to_markdown(index=False), '', '## Detector gates', '', pd.DataFrame(DET).to_markdown(index=False, floatfmt='.4f'), '',
    '## Repair gates', '', pd.DataFrame(REPG).to_markdown(index=False, floatfmt='.3f'), '']))
log('LC VERDICT', {k: v for k, v in VERDICT.items() if k != 'protocol'}); log('done. outputs in', OUT)
