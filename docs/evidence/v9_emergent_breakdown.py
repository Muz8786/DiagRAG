"""v9 analysis V1 (descriptive, post-hoc, no new generation): split the 155 held-out v7 composed episodes by whether each component fails ALONE.
Categories (from `alone_fails`): ALL_FAIL_ALONE, SOME_FAIL_ALONE, NONE_FAIL_ALONE (emergent failure: no single component causes it), UNKNOWN (a component could not be built alone).
For each: n, both causes named (family level, retrained attributor), at least one named, sequential closure, oracle-forward closure, with Wilson 95% intervals.
It first RE-DERIVES the committed totals (62/155 both named, 113/155 sequential, 130/155 oracle-forward) and aborts if they differ, so the reading of the stored fields is checked.
usage: python docs/evidence/v9_emergent_breakdown.py <composed_episodes.jsonl> <out.json>"""
import collections, json, math, sys

FAMILY = dict(Q01='QLEX', Q03='QLEX', Q04='QLEX', Q05='QLEX', K04='STALE', R07='STALE', R03='ENC', R10='ENC', R11='ENC')
fam = lambda f: FAMILY.get(f, f)


def wilson(k, n, z=1.96):
    if n == 0: return [float('nan'), float('nan')]
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return [(c - r) / d, (c + r) / d]


rows = [json.loads(l) for l in open(sys.argv[1], encoding='utf-8')]; te = [r for r in rows if r['split'] == 'test' and r.get('eval')]
assert len(te) == 155, len(te)


def named(e, key):   # family-level: a NON-fallback label equal to the cause or in its family
    labs = [l for l in e[key] if not l.startswith('G')]; fl = {fam(l) for l in labs}
    return [fam(c) in fl for c in e['comps']]


def cat(r):
    a = r['alone_fails']; v = list(a.values())
    if any(x is None for x in v): return 'UNKNOWN'
    return 'ALL_FAIL_ALONE' if all(v) else 'NONE_FAIL_ALONE' if not any(v) else 'SOME_FAIL_ALONE'


def summ(rs):
    n = len(rs); b = sum(all(named(r['eval'], 'lab_new')) for r in rs); b_old = sum(all(named(r['eval'], 'lab_old')) for r in rs); one = sum(any(named(r['eval'], 'lab_new')) for r in rs)
    sq = sum(bool(r['eval']['seq']['ok']) for r in rs); of = sum(bool(r['eval']['oracle_fwd']) for r in rs)
    f = lambda k: dict(k=k, n=n, rate=(k / n if n else None), wilson95=wilson(k, n))
    return dict(n=n, both_named_new=f(b), both_named_old=f(b_old), at_least_one_named_new=f(one), sequential_closure=f(sq), oracle_forward_closure=f(of))


tot = summ(te)
chk = dict(both_named_new=tot['both_named_new']['k'], both_named_old=tot['both_named_old']['k'], sequential=tot['sequential_closure']['k'], oracle_forward=tot['oracle_forward_closure']['k'])
assert (chk['both_named_new'], chk['both_named_old'], chk['sequential'], chk['oracle_forward']) == (62, 47, 113, 130), f'does not reproduce the committed v7 totals: {chk}'
out = dict(source=sys.argv[1], reproduces_committed_totals=chk, all=tot, by_alone_category={c: summ([r for r in te if cat(r) == c]) for c in sorted({cat(r) for r in te})},
           by_stratum_and_category={s: dict(collections.Counter(cat(r) for r in te if r['stratum'] == s)) for s in sorted({r['stratum'] for r in te})},
           caveat='post-hoc, descriptive; 155 episodes from one seed and one CPU stack; small cells have wide intervals; no gate attached')
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print('reproduced', chk)
for c, s in out['by_alone_category'].items():
    print(f"{c:16s} n={s['n']:3d} both named {s['both_named_new']['k']:3d} ({100 * s['both_named_new']['rate']:.1f}%, CI {100 * s['both_named_new']['wilson95'][0]:.0f}-{100 * s['both_named_new']['wilson95'][1]:.0f})  "
          f"seq closure {s['sequential_closure']['k']:3d} ({100 * s['sequential_closure']['rate']:.1f}%)  oracle-fwd {s['oracle_forward_closure']['k']:3d} ({100 * s['oracle_forward_closure']['rate']:.1f}%)")
