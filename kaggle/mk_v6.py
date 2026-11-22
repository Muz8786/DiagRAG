"""Generate kaggle/diagrag_v6.py from kaggle/diagrag_v5.py by exact, asserted replacements. v6 changes ONLY what the v5 diagnosis found
(docs/ROADMAP_V4.md sections 11 and 11.4; docs/evidence/v6_protocol.md):
  D1  base-query supply: N_BASE_ESCI 2400 -> 6000 (all 5,527 already-examined ESCI queries; the 1,648 never-examined natural queries are untouched);
  D2  C2 fault pairs are chosen to balance the accepted pair mix within each split (fewest accepted, then fewest attempts; a pair with 25 attempts and no accepted episode in the split is treated as stuck).
Every gate, bar, sample and analysis rule is the v5 one. Usage: python kaggle/mk_v6.py   (writes diagrag_v6.py, prints its SHA-256)"""
import hashlib, os

here = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(here, 'diagrag_v5.py'), encoding='utf-8').read()


def sub(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:90])
    s = s.replace(old, new)


sub("# # DiagRAG v5 — v4 + a 50-positive measurement floor,",
    "# # DiagRAG v6 — v5 + two construction fixes found by diagnosing the v5 result (docs/evidence/v6_protocol.md). Every gate and bar is unchanged.\n"
    "# D1 (supply): v5 had three THIN detectors (R03, R15, R22; AUROC 1.000, 0.988, 0.968) because those injectors are deterministic, so each base query can give at most\n"
    "#     one episode, only 7-9% of queries are hard, and the test half of 2,400 base queries supplies only about 39-46 of the 50 required. v6 uses every already-examined\n"
    "#     ESCI query as a base (N_BASE_ESCI 6000 = all 5,527). The never-examined natural queries are a separate pool and are not touched.\n"
    "# D2 (C2 composition): the C2 pair was drawn at random per episode, so the pair mix of a split was random. v6 picks the pair with the fewest accepted episodes in the split.\n"
    "# ---- v5 header, unchanged below ----\n"
    "# # DiagRAG v5 — v4 + a 50-positive measurement floor,")

sub("N_BASE_ESCI=int(os.environ.get('N_BASE_ESCI', 4000 if GPU else 320))", "N_BASE_ESCI=int(os.environ.get('N_BASE_ESCI', 6000 if GPU else 320))")

# D2: the pair with the fewest ACCEPTED episodes in this split, ties broken by fewest attempts, so a pair that rarely yields cannot hog attempts
sub("def inj_C2(b, rng):    # compositional: two faults from different factor groups at once\n    fa, fb = rng.choice(C2_PAIRS); A = INJ[fa](b, rng); Bs = INJ[fb](b, rng)\n",
    "_C2_ATT = collections.Counter()\n"
    "def inj_C2(b, rng):    # compositional: two faults from different factor groups at once\n"
    "    acc = collections.Counter(tuple(e['meta']['combo']) for e in EPIS if e['fault'] == 'C2' and e['split'] == b['split'])   # v6 D2: balance the pair mix within each split\n"
    "    live = [p_ for p_ in C2_PAIRS if not (_C2_ATT[(b['split'], p_)] >= 25 and acc[p_] == 0)]   # a pair with 25 attempts and no accepted episode in this split is stuck and is not retried\n"
    "    fa, fb = min(live or C2_PAIRS, key=lambda p_: (acc[p_], _C2_ATT[(b['split'], p_)], C2_PAIRS.index(p_))); _C2_ATT[(b['split'], (fa, fb))] += 1\n"
    "    A = INJ[fa](b, rng); Bs = INJ[fb](b, rng)\n")

sub("md = ['# DiagRAG v5 judged run report',", "md = ['# DiagRAG v6 judged run report',")
sub("    v5_accounting='VERDICT.accounting:", "    v6_changes='D1 base-query supply (N_BASE_ESCI 6000 = all examined ESCI queries); D2 C2 pair mix balanced within each split. Nothing else differs from v5.',\n    v5_accounting='VERDICT.accounting:")

out = os.path.join(here, 'diagrag_v6.py')
open(out, 'w', encoding='utf-8').write(s)
print('wrote', out, hashlib.sha256(s.encode('utf-8')).hexdigest())
