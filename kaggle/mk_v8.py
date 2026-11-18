"""Build the isolated v8 preregistration runner from frozen v7 sources."""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'diagrag_v7.py'), encoding='utf-8').read()
gen = open(os.path.join(HERE, 'v8_cells', 'composed_gen.py'), encoding='utf-8').read().rstrip() + '\n'
ev = open(os.path.join(HERE, 'v8_cells', 'composed_eval.py'), encoding='utf-8').read().rstrip() + '\n'
gen = gen.replace('Composed-fault arm (v7)', 'Composed-fault arm (v8)').replace('protocol v7', 'protocol v8')
gen = gen.replace('Pre-registered in docs/evidence/v7_composed_protocol.md.', 'Pre-registered in docs/evidence/v8_multilabel_protocol.md.')
ev = ev.replace('Composed-fault arm (v7)', 'Composed-fault arm (v8)').replace('The diagnoser is the project\'s own `dispatch_v3`', 'The v8 diagnoser extends the frozen v7 `dispatch_v3`')
ev = ev.replace('Pre-registered in docs/evidence/v7_composed_protocol.md.', 'Pre-registered in docs/evidence/v8_multilabel_protocol.md.')

# v8-only episode pool: fresh-for-injection ESCI queries, component-split as frozen in v7.
gen = gen.replace("COMP_SEED = int(os.environ.get('COMP_SEED', 51))   # fixed by the protocol; the override exists only for disposable development smoke tests",
                  "COMP_SEED = 52  # fixed by the v8 protocol")
gen = gen.replace("if os.environ.get('COMP_QUOTA_SCALE'): COMP_QUOTA = {k_: max(1, int(v_ * float(os.environ['COMP_QUOTA_SCALE']))) for k_, v_ in COMP_QUOTA.items()}   # development smoke tests only",
                  "# Quotas are fixed by the protocol; no scaling override is permitted.")
gen = gen.replace("    USED_SINGLE = {e['bid'] for e in EPIS if e['fault'] != 'NONE'}\n    for sp_ in ('train', 'test'):\n        allb = [b for b in BASE if b['split'] == sp_]",
'''    USED_SINGLE = {e['bid'] for e in EPIS if e['fault'] != 'NONE'}
    qg_by_query = {r.query: r for r in qg.itertuples()}
    BASE_V8 = []
    for query_, census_ in CENS.items():
        if not census_.get('fresh'): continue
        r_ = qg_by_query.get(query_)
        if r_ is None: continue
        bid_ = f'esci:{query_}'
        assert bid_ not in USED_SINGLE, f'v8 query overlaps an earlier injected episode: {bid_}'
        gold_ = gold_set([j for p_ in r_.product_id for j in BY_PKEY[p_]])
        st0_ = dict(q=query_, tenant='ALL', cfg=mkcfg(), ov=None, gold=gold_, k=5, meta={})
        clean_ = run(st0_)
        BASE_V8.append(dict(bid=bid_, q=query_, tenant='ALL', split=r_.split, src='esci', pids=list(r_.product_id),
                            gold=gold_, comp=r_.comp, clean_tr=clean_, h1=succ(clean_, gold_, 1), h5=succ(clean_, gold_, 5)))
    assert len(BASE_V8) == 1648, f'v8 fresh query pool changed: {len(BASE_V8)}'
    assert sum(b['split'] == 'train' for b in BASE_V8) == 868
    assert sum(b['split'] == 'test' for b in BASE_V8) == 780
    for sp_ in ('train', 'test'):
        allb = [b for b in BASE_V8 if b['split'] == sp_]''')
gen = gen.replace("    USED_SINGLE = {e['bid'] for e in EPIS if e['fault'] != 'NONE'}", "    USED_SINGLE = {e['bid'] for e in EPIS if e['fault'] != 'NONE'}", 1)
# V8 uses the required 1,000 clean held-out episodes and deterministic v8-specific ordering.
ev = ev.replace("int(os.environ.get('COMP_CLEAN_N', 300))", "1000")
ev = ev.replace("f'{COMP_SEED}|clean|{x[\"bid\"]}'", "f'{COMP_SEED}|v8-clean|{x[\"bid\"]}'")
ev = ev.replace("def static_labels(fe, att, cls, inone, mg):\n    p = att.predict_proba(np.array([[fe[k_] for k_ in FEATS]], dtype=np.float32))[0]; reps, s = dispatch_v3(p, fe, cls, inone, mg); return [l_ for l_, _ in reps], float(s)",
'''def static_labels(fe, att, cls, inone, mg, dispatcher=dispatch_v3):
    p = att.predict_proba(np.array([[fe[k_] for k_ in FEATS]], dtype=np.float32))[0]; reps, s = dispatcher(p, fe, cls, inone, mg); return [l_ for l_, _ in reps], float(s)''')
ev = ev.replace("try: return static_labels(fe, ATT0, CLS0, iN0, ATTG0)", "try: return static_labels(fe, ATT0, CLS0, iN0, ATTG0, dispatch_v7)")
ev = ev.replace("def seq_loop(e, rev=False):", "def static_v7(fe): return static_labels(fe, ATT, CLS, iN, ATTG, dispatch_v7)\ndef seq_loop(e, rev=False):")
ev = ev.replace("lab_n, s_n = static_labels(fe, ATT, CLS, iN, ATTG); lab_o, s_o = static_old(fe)\n    r = dict(comps=comps, stratum=e['stratum'], bid=e['bid'], src=e['src'], alone_fails=e['alone_fails'], lab_new=lab_n, s_new=s_n, lab_old=lab_o, s_old=s_o, seq=seq_loop(e))",
'''lab_n, s_n = static_labels(fe, ATT, CLS, iN, ATTG); lab_7, s_7 = static_v7(fe); lab_o, s_o = static_old(fe)
    r = dict(comps=comps, stratum=e['stratum'], bid=e['bid'], src=e['src'], alone_fails=e['alone_fails'], lab_new=lab_n, s_new=s_n,
             lab_v7=lab_7, s_v7=s_7, lab_old=lab_o, s_old=s_o, seq=seq_loop(e))''')
ev = ev.replace("(('new', 'lab_new'), ('old', 'lab_old'))", "(('new', 'lab_new'), ('v7', 'lab_v7'), ('old', 'lab_old'))")
ev = ev.replace("protocol='docs/evidence/v7_composed_protocol.md'", "protocol='docs/evidence/v8_multilabel_protocol.md'")
ev = ev.replace("protocol='docs/evidence/v8_multilabel_protocol.md', n_train_kept=", "protocol='docs/evidence/v8_multilabel_protocol.md', tau2=TAU2,\n    tau2_calibration=dict(single_extra_queries=sum(any(v >= TAU2 for v in vals) for vals, _ in _neg), single_n=len(_neg),\n                          clean_extra_queries=sum(any(v >= TAU2 for v in vals) for vals, _ in _clean), clean_n=len(_clean), disabled=not bool(_tau_candidates)),\n    n_train_kept=")

# Replace the embedded v7 evaluation cell with the edited v8 cell (the generator cell
# and evaluation cells replace the corresponding v7 cells in place).
gen_start = src.index('# %% [markdown]\n# ## 11b. Composed-fault arm')
gen_end = src.index('# %% [markdown]\n# ## 12. Detectors:', gen_start)
src = src[:gen_start] + gen + '\n\n' + src[gen_end:]
ev_start = src.index('# %% [markdown]\n# ## 14c. Composed-fault arm')
ev_end = src.index('# %% [markdown]\n# ## 14b. Natural traffic', ev_start)
src = src[:ev_start] + ev + '\n\n' + src[ev_end:]

def sub(old, new, n=1):
    global src
    count = src.count(old)
    assert count == n, (count, old[:100])
    src = src.replace(old, new)

sub('# # DiagRAG v7 —', '# # DiagRAG v8 — multi-label composed dispatcher; generated from immutable v7 sources.\n# v7 source files are not modified.\n# # DiagRAG v7 —')
sub("OUT = os.path.join(WORK, 'diagrag_out')", "OUT = os.path.join(WORK, 'diagrag_v8_out')")
sub('def dispatch_v3(p, fe, cls=None, inone=None, mg=None):', 'def dispatch_v7(p, fe, cls=None, inone=None, mg=None):')
# The new dispatcher keeps every v7 primary/rule choice and augments it using family mass.
needle = "    return out, s\ndef proba(fe):"
replacement = '''    return out, s

TAU2 = float('inf')  # set exactly once from training-only calibration below
def dispatch_v3(p, fe, cls=None, inone=None, mg=None):
    cls = cls or CLS; inone = iN if inone is None else inone
    out, score = dispatch_v7(p, fe, cls, inone, mg)
    represented = {FAMILY[l] for l, _ in out if not l.startswith('G')}
    masses, best = collections.defaultdict(float), {}
    for j, c in enumerate(cls):
        if c == 'NONE': continue
        fam = FAMILY[c]; masses[fam] += float(p[j])
        if fam not in best or p[j] > p[cls.index(best[fam])]: best[fam] = c
    extras = sorted(((mass, fam, best[fam]) for fam, mass in masses.items() if fam not in represented), reverse=True)
    used_groups = set()  # one additional family is allowed even within a group represented by v7
    for mass, fam, label in extras:
        group = GROUP[label]
        if mass < TAU2 or group in used_groups or len(out) >= 3: continue
        out.append((label, fam_repair(label)))
        used_groups.add(group)
    return out, score

def proba(fe):'''
sub(needle, replacement)
# Calibrate tau2 after the clean calibration rows have been constructed and before use.
needle = "for n_, (bid, x) in enumerate(cal_items):\n"
replacement = '''# Training-only threshold: OOF single-fault scores plus clean calibration rows.
def _wilson_upper(k, n, z=1.96):
    if not n: return 1.0
    den = 1 + z*z/n; ctr = (k/n + z*z/(2*n))/den
    rad = z*((k/n*(1-k/n)/n + z*z/(4*n*n))**0.5)/den
    return ctr + rad
class _FixedGroup:
    classes_ = np.array(GCLS)
    def __init__(self, probs): self.probs = np.asarray(probs)
    def predict_proba(self, _): return self.probs.reshape(1, -1)
def _extra_mass(p, cls, pg, fe):
    base, _ = dispatch_v7(p, fe, cls, cls.index('NONE'), _FixedGroup(pg))
    represented = {FAMILY[l] for l, _ in base if not l.startswith('G')}
    mm = collections.defaultdict(float); best = {}
    for j, c in enumerate(cls):
        if c == 'NONE': continue
        fa = FAMILY[c]; mm[fa] += float(p[j])
        if fa not in best or p[j] > p[cls.index(best[fa])]: best[fa] = c
    candidates = sorted(((v, GROUP[best[fa]]) for fa, v in mm.items() if fa not in represented), reverse=True)
    by_group = {}
    for mass, group in candidates: by_group.setdefault(group, mass)
    return list(by_group.values())
_neg = [(_extra_mass(p, CLS, pg, TRA[i_]['feats']), 'single')
        for i_, (p, pg, y) in enumerate(zip(oof, oofg, ytra)) if y != 'NONE']
_clean = []
for bid_, x_ in cal_items:
    _p = ATT.predict_proba(np.array([[x_['feats'][k] for k in FEATS]], dtype=np.float32))[0]
    _pg = ATTG.predict_proba(np.array([[x_['feats'][k] for k in FEATS]], dtype=np.float32))[0]
    _clean.append((_extra_mass(_p, CLS, _pg, x_['feats']), 'clean'))
_vals = sorted({v for vals, _ in _neg + _clean for v in vals}) + [float('inf')]
_tau_candidates = []
for _t in _vals[:-1]:  # infinity is the explicit disabled state, not a qualifying finite threshold
    _kn = sum(any(v >= _t for v in vals) for vals, _ in _neg); _nn = sum(1 for _, tag in _neg if tag == 'single')
    _kc = sum(any(v >= _t for v in vals) for vals, _ in _clean); _nc = len(_clean)
    if _wilson_upper(_kn, _nn) <= .10 and _wilson_upper(_kc, _nc) <= .005:
        _tau_candidates.append(_t); break
TAU2 = _tau_candidates[0] if _tau_candidates else float('inf')
log('v8 tau2', TAU2, 'single extra dispatch', sum(any(v >= TAU2 for v in vals) for vals, _ in _neg), len(_neg),
    'clean extra dispatch', sum(any(v >= TAU2 for v in vals) for vals, _ in _clean), len(_clean))

for n_, (bid, x) in enumerate(cal_items):
'''
sub(needle, replacement)
out = os.path.join(HERE, 'diagrag_v8.py')
ws = "FEATS = sorted(EPIS[0]['feats']); \n"
assert src.count(ws) == 1
src = src.replace(ws, "FEATS = sorted(EPIS[0]['feats']);\n")
with open(out, 'w', encoding='utf-8', newline='') as fh:
    fh.write(src)
print('wrote', out, hashlib.sha256(open(out, 'rb').read()).hexdigest())
