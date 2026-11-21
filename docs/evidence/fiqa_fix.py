"""EXPLORATORY (dev split only). Tries cheap fixes for the FiQA clean stack: fusion weight, RRF, no reranker, and a stronger reranker (bge-reranker-base) at depth 25 and 50.
Reuses the candidates written by fiqa_analysis.py. usage: python docs/evidence/fiqa_fix.py"""
import collections, csv, json, re, time, zipfile
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer, CrossEncoder

ROOT = '/projects/sandbox'; z = zipfile.ZipFile(f'{ROOT}/_v13data/fiqa.zip'); rd = lambda n: z.read(n).decode('utf-8')
DOCS = [json.loads(l) for l in rd('fiqa/corpus.jsonl').splitlines()]; N = len(DOCS); TEXT = [(d.get('title') or '') + '. ' + d['text'] for d in DOCS]; ID2I = {d['_id']: i for i, d in enumerate(DOCS)}
Q = {j['_id']: j['text'] for j in map(json.loads, rd('fiqa/queries.jsonl').splitlines())}; qn = lambda q: ' '.join(re.sub(r"[^\w\s'-]", ' ', q.lower()).split())
G = collections.defaultdict(set)
for r in list(csv.reader(rd('fiqa/qrels/dev.tsv').splitlines(), delimiter='\t'))[1:]:
    if r[1] in ID2I and int(r[2]) > 0: G[r[0]].add(ID2I[r[1]])
qids = sorted(G); queries = [qn(Q[q]) for q in qids]
CV = CountVectorizer(token_pattern=r'[a-z0-9]+', lowercase=True, dtype=np.float32); TF = CV.fit_transform(TEXT).tocsr(); VOC = CV.vocabulary_
DF = np.bincount(TF.indices, minlength=len(VOC)); IDF = np.log(1 + (N - DF + 0.5) / (DF + 0.5)).astype(np.float32); DL = np.asarray(TF.sum(1)).ravel(); AV = DL.mean()
rows = np.repeat(np.arange(TF.shape[0]), np.diff(TF.indptr)); t = TF.data; TF.data = IDF[TF.indices] * t * 1.9 / (t + 0.9 * (0.6 + 0.4 * DL[rows] / AV)); BM = TF.tocsc(); tok = re.compile(r'[a-z0-9]+')
bm25 = lambda q: (lambda ids: np.asarray(BM[:, ids].sum(1)).ravel() if ids else np.zeros(N, np.float32))([VOC[w] for w in tok.findall(q) if w in VOC])
E = np.load(f'{ROOT}/_t13_fiqa/port5_fiqa_out/corpus_e5.npy'); QV = SentenceTransformer('intfloat/e5-small-v2', device='cpu').encode(['query: ' + q for q in queries], normalize_embeddings=True, batch_size=64)
top = lambda s, k: np.argsort(-s)[:k]; hit = lambda lst, g, k=5: any(j in g for j in lst[:k])
def mm(dt, ds, st, ss, a):
    fs = collections.defaultdict(float)
    for lst, sc, w in ((dt, ds, a), (st, ss, 1 - a)):
        v = sc[lst]; lo, hi = v.min(), v.max()
        for j, x in zip(lst, v): fs[int(j)] += w * ((x - lo) / (hi - lo) if hi > lo else 1.0)
    return sorted(fs, key=lambda j: -fs[j])
def rrf(dt, st, k=60):
    fs = collections.defaultdict(float)
    for lst in (dt, st):
        for r, j in enumerate(lst): fs[int(j)] += 1 / (k + r + 1)
    return sorted(fs, key=lambda j: -fs[j])
res = collections.defaultdict(list); best = []
for i, q in enumerate(queries):
    ds = E @ QV[i]; ss = bm25(q); g = G[qids[i]]; dt, st = top(ds, 100), top(np.where(ss > 0, ss, -np.inf), 100)
    for a in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0): f = mm(dt, ds, st, ss, a); res[f'minmax_a{a}_hit@5'].append(hit(f, g)); res[f'minmax_a{a}_recall@50'].append(hit(f, g, 50))
    res['rrf60_hit@5'].append(hit(rrf(dt, st), g)); best.append(mm(dt, ds, st, ss, 0.7))
t0 = time.time(); ce = CrossEncoder('BAAI/bge-reranker-base', max_length=512, device='cpu')
for i, q in enumerate(queries):
    c = best[i][:50]; s = ce.predict([(q, TEXT[j]) for j in c], batch_size=32, show_progress_bar=False)
    for d in (25, 50): o = [c[j] for j in np.argsort(-s[:d])]; res[f'bge_base_rerank{d}_on_a0.7_hit@5'].append(hit(o, G[qids[i]]))
    if i == 49: print(f'bge-base: 50 queries in {time.time() - t0:.0f}s', flush=True)
out = {k: float(np.mean(v)) for k, v in res.items()}; json.dump(out, open(f'{ROOT}/_fiqa/fix_dev.json', 'w'), indent=1); [print(f'  {k:34s} {v:.3f}') for k, v in out.items()]
