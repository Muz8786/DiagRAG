"""Exploration on the TRAIN split of the seed-43 judged run only (held-out never read here).
(a) natural-occurrence census on clean runs, (b) confusability of fault signatures (out-of-fold, train only)."""
import os, re, sys, json, collections
os.environ['DIAGRAG_WORK'] = '/projects/sandbox/_judged43'
os.environ.setdefault('NLTK_DATA', '/projects/sandbox/_data/nltk')
src = open('/projects/sandbox/DiagRAG/kaggle/diagrag_core28.py').read()
cells = re.split(r'\n# %%(?: \[markdown\])?\n', src)
code = '\n'.join(cells[i] for i in (1, 3, 5, 7))
g = {'__name__': 'explore'}
exec(compile(code, 'nb', 'exec'), g)
exec("def enc_docs(texts, bs=32): raise RuntimeError('no model in exploration')", g); g['_QC'] = {}; g['_CEC'] = {}
exec(compile(cells[13], 'nb13', 'exec'), g)
G = g; np = G['np']; RES = G['RES']
EP = RES['EPIS']; CLEAN = RES['CLEAN']
TRN = [e for e in EP if e['fault'] == 'NONE' and e['split'] == 'train']
out = {}

# ---------- (a) natural census on clean TRAIN runs ----------
CH, PKEY, NAND, DOCS, N = G['CH'], G['PKEY'], G['NANDOC'], G['DOCS'], G['N']
def par(i): return DOCS[i]['parent_doc_id'] or DOCS[i]['doc_id']
rows = []
for e in TRN:
    tr = CLEAN[e['bid']]['clean_tr']; fin = [i for i in tr['final'] if i < N]; gold = e['st']['gold']
    q = e['st']['q']; toks = G['tok'](q)
    r = dict(src=e['src'], h5=bool(e['clean_h5']),
             dup_pair=any(CH[a] == CH[b] for x, a in enumerate(fin) for b in fin[x + 1:]),
             twin_pair=any(PKEY[a] == PKEY[b] and par(a) != par(b) for x, a in enumerate(fin) for b in fin[x + 1:]),
             chunk_crowd=max(collections.Counter(par(i) for i in fin).values()) >= 2 if fin else False,
             nan_in_top5=any(NAND[i] for i in fin),
             nan_above_gold=False, gold_is_nan=any(NAND[i] for i in gold if i < N),
             misspell=any(t.isalpha() and len(t) >= 4 and G['df_of'](t) < 3 and G['spell'](t) for t in toks),
             oov_token=any(G['df_of'](t) == 0 for t in toks),
             concat=any(G['segment'](t) for t in toks if t not in G['VOC']),
             code_token=any(re.search(r'[a-z]', t) and re.search(r'\d', t) for t in toks),
             multi_intent=bool(re.search(r'\band\b|,|&', q)), gold_is_chunk=any(DOCS[i]['parent_doc_id'] for i in gold if i < N))
    gr = [k for k, i in enumerate(tr['order']) if i in gold]
    r['nan_above_gold'] = bool(gr) and any(NAND[i] for i in tr['order'][:gr[0]] if i < N)
    rows.append(r)
esci = [r for r in rows if r['src'] == 'esci']
keys = [k for k in rows[0] if k not in ('src', 'h5')]
out['census_train_esci'] = dict(n=len(esci), clean_fail=sum(not r['h5'] for r in esci),
    prevalence={k: sum(r[k] for r in esci) for k in keys},
    among_failures={k: sum(r[k] for r in esci if not r['h5']) for k in keys},
    fail_rate_given={k: (round(sum(not r['h5'] for r in esci if r[k]) / max(1, sum(r[k] for r in esci)), 3)) for k in keys},
    fail_rate_overall=round(sum(not r['h5'] for r in esci) / len(esci), 3))
print(json.dumps(out['census_train_esci'], indent=1))

# ---------- (b) confusability on TRAIN, out-of-fold ----------
from sklearn.model_selection import GroupKFold
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
TR = [e for e in EP if e['split'] == 'train' and e['fault'] != 'C2']
FE = sorted(TR[0]['feats']); X = np.array([[e['feats'][k] for k in FE] for e in TR], dtype=np.float32)
y = np.array([e['fault'] for e in TR]); grp = [e['bid'] for e in TR]
hgb = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5,
                                             l2_regularization=1.0, class_weight='balanced', random_state=42)
cls = sorted(set(y)); oof = np.zeros((len(TR), len(cls)))
for a, b in GroupKFold(5).split(X, y, grp):
    m = hgb().fit(X[a], y[a]); p = m.predict_proba(X[b])
    for j, c in enumerate(m.classes_): oof[b, cls.index(c)] = p[:, j]
pred = np.array(cls)[oof.argmax(1)]
conf = collections.defaultdict(collections.Counter)
for t, p_ in zip(y, pred): conf[t][p_] += 1
faults = [c for c in cls if c != 'NONE']
out['oof_top1_acc'] = {f: round(conf[f][f] / sum(conf[f].values()), 3) for f in faults}
out['oof_main_confusions'] = {f: [(c, n) for c, n in conf[f].most_common(4) if c != f][:3] for f in faults}
# pairwise separability in telemetry: AUROC of a 2-class OOF model on each pair's episodes only
pair = {}
for i, a in enumerate(faults):
    for b in faults[i + 1:]:
        m_ = (y == a) | (y == b)
        if m_.sum() < 20: continue
        Xa, ya, ga = X[m_], (y[m_] == a).astype(int), [grp[k] for k in np.where(m_)[0]]
        s = np.zeros(len(ya))
        for tr_i, te_i in GroupKFold(5).split(Xa, ya, ga):
            s[te_i] = HistGradientBoostingClassifier(max_iter=150, min_samples_leaf=5, random_state=0).fit(Xa[tr_i], ya[tr_i]).predict_proba(Xa[te_i])[:, 1]
        pair[f'{a}|{b}'] = round(float(roc_auc_score(ya, s)), 3)
hard = sorted(pair.items(), key=lambda kv: kv[1])[:15]
out['least_separable_pairs_oof_auroc'] = hard
print('OOF top-1 accuracy (train):', out['oof_top1_acc'])
print('main confusions:', {k: v for k, v in out['oof_main_confusions'].items() if out['oof_top1_acc'][k] < 0.8})
print('least separable pairs:', hard)
json.dump(out, open('/projects/sandbox/_explore/explore_train.json', 'w'), indent=1, default=str)
