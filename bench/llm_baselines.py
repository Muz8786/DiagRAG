"""LLM-based baselines for DiagRAG (free-tier APIs). Subcommands:  prep | llm | rewrite | analyze

B1  LLM diagnosis (a RAGLog-style retrieval-stage check): the LLM sees the query and the top-5 documents the pipeline returned and
    scores P(retrieval failed) and names a cause group. Compared with the DiagRAG attributor on the SAME held-out episodes.
B2  CRAG-style repair, simplified (grade -> rewrite -> re-retrieve; no web search, no knowledge refinement): the LLM grades the
    top-5, and if none is relevant it rewrites the query and the pipeline retrieves again. Compared with the DiagRAG deployed loop on the
    SAME never-examined natural queries.
The prompts, sample sizes, models and gates are frozen in docs/evidence/llm_baselines_plan.md BEFORE any LLM call on this data.
API keys are read from environment variables only and are never written anywhere.
"""
import argparse, collections, hashlib, json, os, re, threading, time, urllib.error, urllib.request
import numpy as np

SAMPLE = dict(SEED=2026, N_DIAG_PER_FAULT=5, N_DIAG_CLEAN=160, N_NAT=300, SNIP=240, TOPK=5)
MODELS = {'groq': dict(model='openai/gpt-oss-120b', min_interval=6.5), 'groq20': dict(model='openai/gpt-oss-20b', min_interval=6.5), 'gemini': dict(model='gemini-3.1-flash-lite', min_interval=4.0)}
FAMILY = dict(Q01='QLEX', Q03='QLEX', Q04='QLEX', Q05='QLEX', K04='STALE', R07='STALE', R03='ENC', R10='ENC', R11='ENC')
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) diagrag-eval/1.0'}

DIAG_PROMPT = """You monitor a product-search retrieval system. Below are a user query and the top-5 documents the system returned.
Decide whether retrieval FAILED: none of the 5 documents is a good answer for the query's intent, or the results are defective
(off-topic, duplicated, placeholder or empty, malformed or misspelled query, results from the wrong source).
Reply with JSON only: {{"p_fail": <number from 0 to 1>, "cause": "query" | "knowledge_base" | "retrieval_stack" | "none"}}
cause = where the problem is: the query itself, the stored documents, or the retrieval machinery.

Query: {query}
Documents:
{docs}"""
GRADE_PROMPT = """Below are a shopping search query and the top-5 documents returned. For each document decide whether it is relevant to
the query, meaning it could satisfy the shopper's intent. Reply with JSON only: {{"relevant": [true or false for document 1, ..., for document 5]}}

Query: {query}
Documents:
{docs}"""
REWRITE_PROMPT = """A product search returned no relevant results for this query. Rewrite it as a corrected, concise product search query
(fix spelling, split joined words, drop filler). Reply with JSON only: {{"query": "<rewritten query>"}}

Query: {query}"""


def fmt_docs(docs):
    return '\n'.join(f"[{i + 1}] {d['title']} — {d['snip']}" for i, d in enumerate(docs))


def md5(s): return hashlib.md5(s.encode()).hexdigest()


def jparse(t):
    m = re.search(r'\{.*\}', t or '', re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None


# ----------------------------------------------------------------------------- providers
class Quota(Exception): pass


class Provider:
    def __init__(self, name, keys):
        self.name, self.keys, self.cfg = name, keys, MODELS[name]; self.last = collections.defaultdict(float); self.dead = set()

    def call(self, prompt, ki):
        key = self.keys[ki]; wait = self.last[ki] + self.cfg['min_interval'] - time.time()
        if wait > 0: time.sleep(wait)
        for attempt in range(6):
            self.last[ki] = time.time()
            try:
                if self.name.startswith('groq'):
                    body = {'model': self.cfg['model'], 'messages': [{'role': 'user', 'content': prompt}], 'temperature': 0, 'max_tokens': 800, 'reasoning_effort': 'low'}
                    req = urllib.request.Request('https://api.groq.com/openai/v1/chat/completions', json.dumps(body).encode(),
                                                 {**UA, 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
                    r = json.loads(urllib.request.urlopen(req, timeout=90).read())
                    return r['choices'][0]['message'].get('content') or '', r.get('usage', {}).get('total_tokens', 0)
                body = {'contents': [{'parts': [{'text': prompt}]}], 'generationConfig': {'temperature': 0, 'maxOutputTokens': 400, 'responseMimeType': 'application/json'}}
                req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{self.cfg['model']}:generateContent", json.dumps(body).encode(),
                                             {**UA, 'x-goog-api-key': key, 'Content-Type': 'application/json'})
                r = json.loads(urllib.request.urlopen(req, timeout=90).read())
                return r['candidates'][0]['content']['parts'][0].get('text', ''), r.get('usageMetadata', {}).get('totalTokenCount', 0)
            except urllib.error.HTTPError as e:
                msg = e.read().decode()[:400]
                if e.code == 429:
                    if re.search(r'per ?day|daily|RPD|TPD', msg, re.I): raise Quota(f'{self.name} key {ki}: daily quota ({msg[:120]})')
                    ra = e.headers.get('retry-after'); time.sleep(min(90, float(ra) + 1 if ra and ra.replace('.', '').isdigit() else 20 * (attempt + 1))); continue
                if e.code in (500, 502, 503, 504): time.sleep(5 * (attempt + 1)); continue
                raise RuntimeError(f'{self.name} HTTP {e.code}: {msg[:160]}')
            except (TimeoutError, urllib.error.URLError, ConnectionError):
                time.sleep(5 * (attempt + 1))
        raise RuntimeError(f'{self.name}: retries exhausted')


def keys_of(name):
    v = os.environ.get({'groq': 'GROQ_API_KEY', 'groq20': 'GROQ_API_KEY', 'gemini': 'GEMINI_API_KEYS'}[name], '')
    return [k for k in re.split(r'[,\s]+', v) if k]


# ----------------------------------------------------------------------------- harness (re-runs the judged v3 pipeline on CPU)
def load_harness(work):
    V3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kaggle', 'diagrag_v3.py')
    os.environ.update(DIAGRAG_WORK=work, RERANKER='cross-encoder/ms-marco-MiniLM-L-6-v2', CE_MAXLEN='256', N_BASE_ESCI='2400', N_PRDC='528', N_HARD='50',
                      MAX_ATT='2500', N_HARM='20', SEED='45', NLTK_DATA=os.environ.get('NLTK_DATA', ''))
    src = open(V3).read(); cells = re.split(r'\n# %%(?: \[markdown\])?\n', src)
    last = max(i for i, c in enumerate(cells) if "log('clean runs')" in c); g = {'__name__': '__llm_harness__', '__file__': os.path.abspath(V3)}
    for c in cells[:last + 1]:
        if not c.lstrip().startswith('# '): exec(compile(c, 'v3cell', 'exec'), g)
    return g


def snippet(g, i, ov, n):
    t = g['dtext'](i, ov); title = (g['dtitle'](i, ov) or '').strip().replace('\n', ' '); body = t[len(title):].strip().replace('\n', ' ')
    return dict(title=title[:120], snip=body[:n])


def eids(EP):
    out = {}
    for split in ('train', 'test'):
        for n, e in enumerate([e for e in EP if e['split'] == split]):
            out[id(e)] = hashlib.sha256(f"{e['split']}|{e['bid']}|{e['fault']}|{n}".encode()).hexdigest()[:16]
    return out


# ----------------------------------------------------------------------------- stages
def stage_prep(a):
    import pickle
    g = load_harness(a.work); R = pickle.load(open(os.path.join(a.work, 'diagrag_out', 'checkpoint.pkl'), 'rb')); EP = R['EPIS']; ids = eids(EP)
    S = SAMPLE; items = []
    test = [e for e in EP if e['split'] == 'test']
    for f in sorted({e['fault'] for e in test} - {'NONE'}):
        es = sorted([e for e in test if e['fault'] == f], key=lambda e: md5(f"{S['SEED']}|{e['bid']}|{f}"))[:S['N_DIAG_PER_FAULT']]
        for e in es: items.append(('diag', ids[id(e)], e))
    for e in sorted([e for e in test if e['fault'] == 'NONE'], key=lambda e: md5(f"{S['SEED']}|{e['bid']}|NONE"))[:S['N_DIAG_CLEAN']]: items.append(('diag', ids[id(e)], e))
    nat = sorted(R['NAT3'], key=lambda q: md5(f"{S['SEED']}|{q}"))[:S['N_NAT']]
    out = open(os.path.join(a.out, 'llm_inputs.jsonl'), 'w'); lab = open(os.path.join(a.private, 'llm_diag_labels.jsonl'), 'w'); t0 = time.time()
    for n, (kind, eid, e) in enumerate(items):
        tr = g['run'](e['st']); docs = [snippet(g, i, tr['ov'], S['SNIP']) for i in tr['final'][:S['TOPK']]]
        out.write(json.dumps(dict(kind='diag', id=eid, query=e['st']['q'], docs=docs)) + '\n')
        lab.write(json.dumps(dict(id=eid, fault=e['fault'], family=FAMILY.get(e['fault'], e['fault']) if e['fault'] != 'NONE' else 'NONE', group=e['fault'][0] if e['fault'] != 'NONE' else 'NONE')) + '\n')
        if n % 50 == 0: print(f'prep diag {n}/{len(items)} {time.time() - t0:.0f}s', flush=True)
    for n, q in enumerate(nat):
        r = R['CENS'][q]; gold = g['gold_set']([j for p in r['pids'] for j in g['BY_PKEY'][p]]); st = dict(q=q, tenant='ALL', cfg=g['mkcfg'](), ov=None, gold=gold, k=5, meta={})
        tr = g['run'](st); docs = [snippet(g, i, None, S['SNIP']) for i in tr['final'][:S['TOPK']]]; v = R['NAT3'][q]
        out.write(json.dumps(dict(kind='nat', id='nat:' + md5(q)[:12], query=q, docs=docs, h0=bool(g['succ'](tr, gold, 5)), h_loop=bool(v['h_loop']), h_univ=bool(v['h_univ']),
                                  h_rules=bool(v['h_rules']), cost_loop=v['cost_loop'])) + '\n')
        if n % 50 == 0: print(f'prep nat {n}/{len(nat)} {time.time() - t0:.0f}s', flush=True)
    out.close(); lab.close(); print('prep done', len(items), 'diag items,', len(nat), 'natural queries')


def load_cache(p):
    c = {}
    if os.path.exists(p):
        for l in open(p):
            try: j = json.loads(l); c[j['key']] = j
            except Exception: pass
    return c


def stage_llm(a):
    items = [json.loads(l) for l in open(os.path.join(a.out, 'llm_inputs.jsonl'))]; t_end = time.time() + a.budget
    tasks = []
    for it in items:
        if it['kind'] == 'diag': tasks.append((it['id'], 'diag', DIAG_PROMPT.format(query=it['query'], docs=fmt_docs(it['docs']))))
        else: tasks.append((it['id'], 'grade', GRADE_PROMPT.format(query=it['query'], docs=fmt_docs(it['docs']))))
    tasks.sort(key=lambda t: md5(f"{SAMPLE['SEED']}|order|{t[0]}"))
    for prov in a.providers:
        P = Provider(prov, keys_of(prov)); cp = os.path.join(a.out, f'llm_cache_{prov}.jsonl'); cache = load_cache(cp); lock = threading.Lock()
        if not P.keys: print(prov, 'no key in environment - skipped'); continue
        todo = [t for t in tasks if f'{t[0]}|{t[1]}' not in cache]
        # second pass: rewrite prompts for natural queries whose grades are all false
        for it in items:
            gr = cache.get(f"{it['id']}|grade")
            if gr:
                j = jparse(gr['text']); rel = j.get('relevant') if isinstance(j, dict) else None
                if isinstance(rel, list) and not any(bool(x) for x in rel) and f"{it['id']}|rewrite" not in cache: todo.append((it['id'], 'rewrite', REWRITE_PROMPT.format(query=it['query'])))
        q = list(todo); done = [0]; err = []

        def worker(ki):
            while time.time() < t_end:
                with lock:
                    if not q: return
                    iid, kind, prompt = q.pop(0)
                try: text, tok = P.call(prompt, ki)
                except Quota as e: err.append(str(e)); return
                except Exception as e: err.append(repr(e)[:200]); time.sleep(5); continue
                with lock:
                    cache[f'{iid}|{kind}'] = dict(key=f'{iid}|{kind}', text=text, tokens=tok); done[0] += 1
                    open(cp, 'a').write(json.dumps(cache[f'{iid}|{kind}']) + '\n')
        th = [threading.Thread(target=worker, args=(ki,)) for ki in range(len(P.keys))]
        [t.start() for t in th]; [t.join() for t in th]
        print(f'{prov}: {done[0]} calls this chunk, {len([t for t in tasks if f"{t[0]}|{t[1]}" in cache])}/{len(tasks)} diag+grade done, remaining {len(q)}', ('| ' + '; '.join(sorted(set(err)))[:200]) if err else '')


def stage_rewrite(a):
    import pickle
    items = {j['id']: j for j in map(json.loads, open(os.path.join(a.out, 'llm_inputs.jsonl'))) if j['kind'] == 'nat'}
    g = load_harness(a.work); R = pickle.load(open(os.path.join(a.work, 'diagrag_out', 'checkpoint.pkl'), 'rb'))
    for prov in a.providers:
        cache = load_cache(os.path.join(a.out, f'llm_cache_{prov}.jsonl')); rp = os.path.join(a.out, f'rewrite_hits_{prov}.json'); res = json.load(open(rp)) if os.path.exists(rp) else {}
        for iid, it in items.items():
            c = cache.get(f'{iid}|rewrite')
            if not c or iid in res: continue
            j = jparse(c['text']); q2 = (j or {}).get('query') if isinstance(j, dict) else None
            if not q2 or not isinstance(q2, str): res[iid] = dict(query=None, hit=None); continue
            q = it['query']; r = R['CENS'][q]; gold = g['gold_set']([x for p in r['pids'] for x in g['BY_PKEY'][p]])
            tr = g['run'](dict(q=q2.strip().lower(), tenant='ALL', cfg=g['mkcfg'](), ov=None, gold=gold, k=5, meta={})); res[iid] = dict(query=q2.strip().lower(), hit=bool(g['succ'](tr, gold, 5)))
        json.dump(res, open(rp, 'w')); print(prov, 'rewrite retrievals', len(res))


def auroc(y, s):
    y = np.asarray(y, int); s = np.asarray(s, float); pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0: return float('nan')
    return float(np.mean([(p > n) + 0.5 * (p == n) for p in pos for n in neg]))


def boot(fn, n_items, n=2000, seed=7):
    r = np.random.default_rng(seed); out = []
    for _ in range(n):
        i = r.integers(0, n_items, n_items); v = fn(i)
        if v == v: out.append(v)
    return float(np.mean(out)), float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


def stage_analyze(a):
    items = [json.loads(l) for l in open(os.path.join(a.out, 'llm_inputs.jsonl'))]; diag = [i for i in items if i['kind'] == 'diag']; nat = [i for i in items if i['kind'] == 'nat']
    lab = {j['id']: j for j in map(json.loads, open(os.path.join(a.private, 'llm_diag_labels.jsonl')))}
    ours = {r['episode_id']: r for r in __import__('csv').DictReader(open(a.ours_csv))}
    GROUPMAP = {'query': 'Q', 'knowledge_base': 'K', 'retrieval_stack': 'R', 'none': 'NONE'}; out = {}
    for prov in a.providers:
        cache = load_cache(os.path.join(a.out, f'llm_cache_{prov}.jsonl')); res = {}
        # ---- B1
        d_ok = []
        for it in diag:
            c = cache.get(f"{it['id']}|diag")
            if not c: continue
            j = jparse(c['text']); pf = j.get('p_fail') if isinstance(j, dict) else None
            ok = isinstance(pf, (int, float)) and 0 <= pf <= 1
            d_ok.append(dict(id=it['id'], y=int(lab[it['id']]['fault'] != 'NONE'), llm=float(pf) if ok else 0.5, parsed=ok,
                             cause=GROUPMAP.get(str((j or {}).get('cause', '')).lower(), 'NONE') if isinstance(j, dict) else 'NONE',
                             group=lab[it['id']]['group'], ours=float(ours[it['id']]['p_fault']), our_group=ours[it['id']]['family'], tokens=c['tokens']))
        if d_ok:
            y = np.array([r['y'] for r in d_ok]); sl = np.array([r['llm'] for r in d_ok]); so = np.array([r['ours'] for r in d_ok])
            clean = sl[y == 0]; thr = float(np.quantile(clean, 0.95)) if len(clean) else 1.0
            diff = boot(lambda i: auroc(y[i], so[i]) - auroc(y[i], sl[i]), len(y))
            fa = y == 1
            res['B1'] = dict(n=len(d_ok), n_faulted=int(y.sum()), n_clean=int((1 - y).sum()), unparsed=int(sum(not r['parsed'] for r in d_ok)),
                             auroc_llm=auroc(y, sl), auroc_llm_ci=boot(lambda i: auroc(y[i], sl[i]), len(y))[1:], auroc_ours=auroc(y, so), auroc_ours_ci=boot(lambda i: auroc(y[i], so[i]), len(y))[1:],
                             auroc_ours_minus_llm=dict(mean=diff[0], ci_lo=diff[1], ci_hi=diff[2]),
                             verdict=('OURS_BETTER' if diff[1] > 0 else 'OURS_NON_INFERIOR' if diff[1] > -0.02 else 'LLM_BETTER' if diff[2] < 0 else 'INCONCLUSIVE'),
                             llm_detect_at_5pct_fa=float(np.mean(sl[fa] > thr)) if fa.any() else None,
                             llm_group_accuracy_on_faulted=float(np.mean([r['cause'] == r['group'] for r in d_ok if r['y']])),
                             our_group_accuracy_on_faulted=float(np.mean([r['our_group'][0] == r['group'] for r in d_ok if r['y'] and r['our_group'] != 'NONE'] or [float('nan')])),
                             mean_tokens_per_item=float(np.mean([r['tokens'] for r in d_ok])), llm_calls_per_item=1, our_llm_calls_per_item=0)
        # ---- B2
        rp = os.path.join(a.out, f'rewrite_hits_{prov}.json'); rw = json.load(open(rp)) if os.path.exists(rp) else {}; rows = []; excluded = 0
        for it in nat:
            c = cache.get(f"{it['id']}|grade")
            if not c: continue
            j = jparse(c['text']); rel = j.get('relevant') if isinstance(j, dict) else None
            if not (isinstance(rel, list) and len(rel) >= 1): rel = [True]; unp = 1
            else: unp = 0
            trig = not any(bool(x) for x in rel); hit = it['h0']; calls = 1; toks = c['tokens']
            if trig:
                rc = cache.get(f"{it['id']}|rewrite"); r_ = rw.get(it['id'])
                if not rc or not r_: excluded += 1; continue   # amendment A2: the CRAG-style procedure did not complete for this query
                calls += 1; toks += rc['tokens']
                if r_.get('hit') is not None: hit = bool(r_['hit'])
            rows.append(dict(h0=it['h0'], crag=hit, loop=it['h_loop'], univ=it['h_univ'], trig=trig, calls=calls, tokens=toks, unparsed=unp, h_before_trig=it['h0']))
        graded = len(rows) + excluded
        if excluded > 0.10 * max(1, graded): res['B2'] = dict(verdict='NOT_ANALYSABLE', reason=f'{excluded} of {graded} graded queries had an incomplete CRAG-style procedure (provider quota); amendment A3', graded=graded, excluded_incomplete_procedure=excluded)
        elif rows:
            h0 = np.array([r['h0'] for r in rows], float); hc = np.array([r['crag'] for r in rows], float); hl = np.array([r['loop'] for r in rows], float); hu = np.array([r['univ'] for r in rows], float)
            dc = boot(lambda i: float((hc[i] - h0[i]).mean()), len(rows)); dl = boot(lambda i: float((hl[i] - h0[i]).mean()), len(rows)); dd = boot(lambda i: float((hl[i] - hc[i]).mean()), len(rows))
            res['B2'] = dict(n=len(rows), excluded_incomplete_procedure=excluded, triggered=float(np.mean([r['trig'] for r in rows])), unparsed=int(sum(r['unparsed'] for r in rows)),
                             crag_delta=dict(mean=dc[0], ci_lo=dc[1], ci_hi=dc[2]), loop_delta=dict(mean=dl[0], ci_lo=dl[1], ci_hi=dl[2]), loop_minus_crag=dict(mean=dd[0], ci_lo=dd[1], ci_hi=dd[2]),
                             verdict=('OURS_BETTER' if dd[1] > 0 else 'OURS_NON_INFERIOR' if dd[1] > -0.005 else 'LLM_BETTER' if dd[2] < 0 else 'INCONCLUSIVE'),
                             crag_fixed=int(((hc - h0) > 0).sum()), crag_broken=int(((hc - h0) < 0).sum()), loop_fixed=int(((hl - h0) > 0).sum()), loop_broken=int(((hl - h0) < 0).sum()),
                             mean_llm_calls_per_query=float(np.mean([r['calls'] for r in rows])), mean_tokens_per_query=float(np.mean([r['tokens'] for r in rows])),
                             our_llm_calls_per_query=0, universal_delta=float((hu - h0).mean()))
        out[prov] = dict(model=MODELS[prov]['model'], **res)
    json.dump(out, open(os.path.join(a.out, 'LLM_BASELINES_RESULT.json'), 'w'), indent=1); print(json.dumps(out, indent=1)[:6000])


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('stage', choices=['prep', 'llm', 'rewrite', 'analyze']); ap.add_argument('--work', default='/projects/sandbox/_llmwork')
    ap.add_argument('--out', default='/projects/sandbox/_llm'); ap.add_argument('--private', default='/projects/sandbox/_private'); ap.add_argument('--providers', nargs='+', default=['groq', 'groq20', 'gemini'])
    ap.add_argument('--budget', type=int, default=1300); ap.add_argument('--ours-csv', default='/projects/sandbox/_private/baseline_track1_test.csv'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True); os.makedirs(a.private, exist_ok=True)
    {'prep': stage_prep, 'llm': stage_llm, 'rewrite': stage_rewrite, 'analyze': stage_analyze}[a.stage](a)
