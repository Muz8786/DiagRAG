"""EXPLORATORY analysis of the clean retrieval stack on FiQA (not a judged run; does not change any frozen file).
Uses the DEV split only (500 queries) for every measurement, so the test split stays untouched. Reproduces the port stack's clean retrieval
(e5-small-v2 HNSW-equivalent exact dense search, BM25 k1 0.9 b 0.4, min-max fusion alpha 0.5, MiniLM-L6 rerank of the top 25) and reports, per stage:
Hit@5, and Recall@k (a relevant document anywhere in the top k), which is the ceiling a reranker can reach.
usage: python docs/evidence/fiqa_analysis.py   (reads _v13data/fiqa.zip and the trial's corpus_e5.npy; writes _fiqa/stage_dev.json)"""
import collections, csv, io, json, re, sys, time, zipfile
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

ROOT = '/projects/sandbox'; z = zipfile.ZipFile(f'{ROOT}/_v13data/fiqa.zip'); rd = lambda n: z.read(n).decode('utf-8')
DOCS = [json.loads(l) for l in rd('fiqa/corpus.jsonl').splitlines()]; N = len(DOCS)
TEXT = [(d.get('title') or '') + '. ' + d['text'] for d in DOCS]; ID2I = {d['_id']: i for i, d in enumerate(DOCS)}
Q = {j['_id']: j['text'] for j in map(json.loads, rd('fiqa/queries.jsonl').splitlines())}
qn = lambda q: ' '.join(re.sub(r"[^\w\s'-]", ' ', q.lower()).split())
G = collections.defaultdict(set)
for r in list(csv.reader(rd('fiqa/qrels/dev.tsv').splitlines(), delimiter='\t'))[1:]:
    if r[1] in ID2I and int(r[2]) > 0: G[r[0]].add(ID2I[r[1]])
qids = sorted(G); queries = [qn(Q[q]) for q in qids]; print('dev queries', len(qids), flush=True)
t0 = time.time()
# BM25 exactly as the port stack
CV = CountVectorizer(token_pattern=r'[a-z0-9]+', lowercase=True, dtype=np.float32); TF = CV.fit_transform(TEXT).tocsr(); VOC = CV.vocabulary_
DF = np.bincount(TF.indices, minlength=len(VOC)); IDF = np.log(1 + (N - DF + 0.5) / (DF + 0.5)).astype(np.float32); DL = np.asarray(TF.sum(1)).ravel(); AV = DL.mean(); K1, B = 0.9, 0.4
rows = np.repeat(np.arange(TF.shape[0]), np.diff(TF.indptr)); t = TF.data; TF.data = IDF[TF.indices] * t * (K1 + 1) / (t + K1 * (1 - B + B * DL[rows] / AV)); BM = TF.tocsc()
tok = re.compile(r'[a-z0-9]+')
def bm25(q):
    ids = [VOC[w] for w in tok.findall(q) if w in VOC]
    return np.asarray(BM[:, ids].sum(1)).ravel() if ids else np.zeros(N, np.float32)
from sentence_transformers import SentenceTransformer, CrossEncoder
E = np.load(f'{ROOT}/_t13_fiqa/port5_fiqa_out/corpus_e5.npy'); enc = SentenceTransformer('intfloat/e5-small-v2', device='cpu')
QV = enc.encode(['query: ' + q for q in queries], normalize_embeddings=True, batch_size=64)
top = lambda s, k: np.argsort(-s)[:k]
res = collections.defaultdict(list); cand = []
for i, q in enumerate(queries):
    ds = E @ QV[i]; ss = bm25(q); g = G[qids[i]]
    dt, st = top(ds, 100), top(np.where(ss > 0, ss, -np.inf), 100)
    fs = collections.defaultdict(float)
    for lst, sc, w in ((dt, ds, 0.5), (st, ss, 0.5)):
        v = sc[lst]; lo, hi = v.min(), v.max()
        for j, x in zip(lst, v): fs[int(j)] += w * ((x - lo) / (hi - lo) if hi > lo else 1.0)
    fused = sorted(fs, key=lambda j: -fs[j])
    for name, lst in (('dense', list(dt)), ('bm25', list(st)), ('fused', fused)):
        for k in (5, 25, 100): res[f'{name}_recall@{k}'].append(any(j in g for j in lst[:k]))
    cand.append(fused[:100])
print(f'retrieval done {time.time() - t0:.0f}s', flush=True)
ce = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=256, device='cpu')
for i, q in enumerate(queries):
    c = cand[i][:25]; s = ce.predict([(q, TEXT[j]) for j in c], batch_size=64, show_progress_bar=False); order = [c[j] for j in np.argsort(-s)]
    res['minilm_rerank25_hit@5'].append(any(j in G[qids[i]] for j in order[:5]))
print(f'rerank done {time.time() - t0:.0f}s', flush=True)
out = {k: float(np.mean(v)) for k, v in res.items()}; out['n'] = len(qids)
json.dump(dict(out=out, cand=cand, qids=qids), open(f'{ROOT}/_fiqa/stage_dev.json', 'w')); [print(f'  {k:28s} {v:.3f}') for k, v in out.items()]
