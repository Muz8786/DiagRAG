"""Supervised text baseline vs telemetry attributor (docs/evidence/v10_textbaseline_protocol.md). Models, features, split and verdict rule are the pre-registered ones; nothing is tuned on the held-out set.
usage: python docs/evidence/v10_textbaseline.py <ds> <checkpoint.pkl> <view.jsonl> <out.json> <seed>        (scikit-learn 1.6.1)"""
import collections, json, pickle, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ds, ckpt, view, outp, seed = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
EP = pickle.load(open(ckpt, 'rb'))['EPIS']; V = {}
for l in open(view): j = json.loads(l); V[j['n']] = j
assert len(V) == len(EP), (len(V), len(EP))
FE = sorted(EP[0]['feats']); X = np.array([[e['feats'][k] for k in FE] for e in EP], np.float32); y = np.array([e['fault'] for e in EP]); sp = np.array([e['split'] for e in EP])
text = [V[i]['query'] + ' [SEP] ' + ' || '.join(V[i]['docs']) for i in range(len(EP))]
tr, te = sp == 'train', sp == 'test'; fm = y[te] != 'NONE'


def auroc(yy, s):
    yy = np.asarray(yy, int); s = np.asarray(s, float); pos = yy == 1
    if pos.sum() == 0 or (~pos).sum() == 0: return float('nan')
    order = np.argsort(s, kind='mergesort'); ss = s[order]; ranks = np.empty(len(s)); i = 0
    while i < len(ss):
        j = i
        while j + 1 < len(ss) and ss[j + 1] == ss[i]: j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1; i = j + 1
    return float((ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum()))


def fit_score(kind):
    if kind == 'attributor': m = HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=seed).fit(X[tr], y[tr]); P = m.predict_proba(X[te])
    else:
        vec = (TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=50000, sublinear_tf=True) if kind == 'T1_word' else TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), min_df=3, max_features=100000, sublinear_tf=True))
        Xt = vec.fit_transform([text[i] for i in np.where(tr)[0]]); m = LogisticRegression(C=3.0, class_weight='balanced', max_iter=500).fit(Xt, y[tr]); P = m.predict_proba(vec.transform([text[i] for i in np.where(te)[0]]))
    cls = list(m.classes_); pred = np.array([cls[i] for i in P.argmax(1)]); return 1 - P[:, cls.index('NONE')], pred, cls


sc = {}; pred = {}
for k in ('attributor', 'T1_word', 'T2_char'):
    sc[k], pred[k], cls = fit_score(k); print(k, 'AUROC', round(auroc(fm.astype(int), sc[k]), 4), flush=True)
yt = y[te]; rng = np.random.default_rng(7); n = len(yt); B = [rng.integers(0, n, n) for _ in range(2000)]


def boot(a, b):
    d = [auroc(fm[i].astype(int), sc[a][i]) - auroc(fm[i].astype(int), sc[b][i]) for i in B]; d = [x for x in d if x == x]; return float(np.mean(d)), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


verdict = lambda lo, hi: 'OURS_BETTER' if lo > 0 else 'OURS_NON_INFERIOR' if lo > -0.02 else 'TEXT_BETTER' if hi < 0 else 'INCONCLUSIVE'
res = dict(dataset=ds, seed=seed, n_train=int(tr.sum()), n_test=int(te.sum()), n_test_faulted=int(fm.sum()), n_test_clean=int((~fm).sum()), n_features=len(FE), train_classes=sorted(set(y[tr])), arms={})
for k in ('attributor', 'T1_word', 'T2_char'):
    a = dict(auroc=auroc(fm.astype(int), sc[k]), exact_fault_accuracy_on_faulted=float((pred[k][fm] == yt[fm]).mean()),
             by_group={g: dict(n=int(sum(f[0] == g for f in yt[fm])), exact=float(np.mean([p == f for p, f in zip(pred[k][fm], yt[fm]) if f[0] == g])) if any(f[0] == g for f in yt[fm]) else None) for g in 'QKR'})
    if k != 'attributor': m_, lo, hi = boot('attributor', k); a['attributor_minus_text'] = dict(mean=m_, ci_lo=lo, ci_hi=hi, verdict=verdict(lo, hi))
    res['arms'][k] = a
json.dump(res, open(outp, 'w'), indent=1); print(json.dumps({k: {x: v[x] for x in v if x != 'by_group'} for k, v in res['arms'].items()}, indent=1)); print({k: v['by_group'] for k, v in res['arms'].items()})
