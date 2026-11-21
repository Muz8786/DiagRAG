"""v15 held-out summary (docs/evidence/v15_selftest_mutants_protocol.md, amendments A1/A2): pooled S rule S-1..S-5 and the M rule, from the held-out runs' jsonl files.
File reading and arithmetic only. usage: python docs/evidence/v15_summary.py <out.json> --S <dir71> <dir72> <dir73> [--M <dir71> <dir72> <dir73>]"""
import json, os, sys
import numpy as np

a = sys.argv[1:]; out = a[0]; Sd = a[a.index('--S') + 1:a.index('--S') + 4] if '--S' in a else []; Md = a[a.index('--M') + 1:a.index('--M') + 4] if '--M' in a else []
rd = lambda d, f: [json.loads(l) for l in open(os.path.join(d, f))]
m = lambda xs, k: float(np.mean([bool(x[k]) for x in xs])) if xs else None
rng = np.random.default_rng(7)
def boot_diff(d, n=4000):
    d = np.asarray(d, float); bs = d[rng.integers(0, len(d), (n, len(d)))].mean(1); return dict(mean=float(d.mean()), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])
def tr(rows, key, sub, who):
    v = [r[key][sub][who] for r in rows if key in r and r[key][sub][who] is not None]; return float(np.mean(v)) if v else None
R = {}
if Sd:
    S = [dict(r, seed=os.path.basename(d.rstrip('/'))) for d in Sd for r in rd(d, 'S_single.jsonl')]
    PR = [dict(r, seed=os.path.basename(d.rstrip('/'))) for d in Sd for r in rd(d, 'S_pairs.jsonl')]
    HS = [r for r in S if r['harmful']]; HT = [r for r in HS if 'traffic' in r]; EP = [r for r in PR if r['effective']]; EG = [r for r in EP if r['same_group']]
    d4 = boot_diff([int(r['both_family']) - int(r['agg_dispatcher_both']) for r in EG]) if EG else None
    c_s, c_p = tr(HT, 'traffic', 'closure', 'selftest'), tr(EP, 'traffic', 'closure', 'selftest')
    l_s, l_p = tr(HT, 'traffic', 'closure', 'loop'), tr(EP, 'traffic', 'closure', 'loop')
    h_s, h_p = tr(HT, 'traffic', 'harm', 'selftest'), tr(EP, 'traffic', 'harm', 'selftest')
    S1, S2 = m(HS, 'detected'), m(HS, 'family'); S3 = (m(HS, 'verified'), m(EP, 'verified')); S4 = m(EG, 'both_family')
    rule = {'S-1 detection >= 0.95': bool(S1 is not None and S1 >= 0.95), 'S-2 family >= 0.90': bool(S2 is not None and S2 >= 0.90),
            'S-3 verified >= 0.95 (singles, pairs)': bool(S3[0] is not None and S3[1] is not None and min(S3) >= 0.95),
            'S-4 same-group pairs both named >= 0.70 and above aggregated dispatcher': bool(S4 is not None and S4 >= 0.70 and d4 and d4['ci'][0] > 0),
            'S-5 closure >= 0.95 and above loop, harm <= 0.5%': bool(None not in (c_s, c_p, l_s, l_p, h_s, h_p) and min(c_s, c_p) >= 0.95 and c_s > l_s and c_p > l_p and max(h_s, h_p) <= 0.005)}
    R['S'] = dict(n_singles=len(S), harmful_singles=len(HS), effective_pairs=len(EP), effective_same_group=len(EG), S1_detection=S1, S2_family=S2, exact=m(HS, 'exact'),
                  S3_verified=dict(singles=S3[0], pairs=S3[1]), S4_both_family_same_group=S4, both_family_all_effective=m(EP, 'both_family'),
                  agg_dispatcher_same_group=m(EG, 'agg_dispatcher_both'), S4_diff_vs_aggregated=d4,
                  S5=dict(closure_singles=dict(selftest=c_s, loop=l_s, universal=tr(HT, 'traffic', 'closure', 'universal')),
                          closure_pairs=dict(selftest=c_p, loop=l_p, universal=tr(EP, 'traffic', 'closure', 'universal')),
                          harm_singles=dict(selftest=h_s, loop=tr(HT, 'traffic', 'harm', 'loop'), universal=tr(HT, 'traffic', 'harm', 'universal')),
                          harm_pairs=dict(selftest=h_p, loop=tr(EP, 'traffic', 'harm', 'loop'), universal=tr(EP, 'traffic', 'harm', 'universal'))),
                  secondary=dict(unseen_family_with_sibling=m([r for r in HS if r['sibling']], 'lofo_family'), unseen_verified=m(HS, 'lofo_verified'),
                                 median_selftest_seconds=float(np.median([r['sec'] for r in S])), mean_probe_runs=float(np.mean([r['runs'] for r in S]))),
                  per_seed={sd: dict(detected=m([r for r in HS if r['seed'] == sd], 'detected'), family=m([r for r in HS if r['seed'] == sd], 'family'),
                                     both_family_same_group=m([r for r in EG if r['seed'] == sd], 'both_family')) for sd in sorted({r['seed'] for r in S})},
                  rule=rule, S_PASS=bool(all(rule.values())))
if Md:
    M = [dict(r, seed=os.path.basename(d.rstrip('/'))) for d in Md for r in rd(d, 'M_mutants.jsonl')]
    H = [r for r in M if r['status'] == 'harmful']; C = [r for r in H if r.get('component_ok') is not None]; SB = [r for r in M if r['status'] == 'subtle']
    ids = sorted({r['pid'] for r in C})
    def cboot(fn, n=4000):   # bootstrap over distinct mutants (clusters), fn maps a list of rows to a number
        by = {i: [r for r in C if r['pid'] == i] for i in ids}; vals = []
        for _ in range(n):
            pick = rng.integers(0, len(ids), len(ids)); rows = [r for k in pick for r in by[ids[k]]]; vals.append(fn(rows))
        return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]
    loc = lambda rows: float(np.mean([r['component_ok'] for r in rows]))
    dec = lambda rows: float(np.mean([bool(r.get('component_ok_decode')) for r in rows]))
    def majority(rows):
        c = {}
        for r in rows: c[r['comp']] = c.get(r['comp'], 0) + 1
        return max(c.values()) / len(rows)
    M2 = dict(localization=loc(C) if C else None, decoder=dec(C) if C else None, majority=majority(C) if C else None,
              loc_minus_decoder=dict(mean=loc(C) - dec(C), ci=cboot(lambda rw: loc(rw) - dec(rw))) if C else None,
              loc_minus_majority=dict(mean=loc(C) - majority(C), ci=cboot(lambda rw: loc(rw) - majority(rw))) if C else None)
    rule = {'M-0 >= 8 distinct scored harmful mutants': len(ids) >= 8, 'M-1 self-test detection >= 0.95': bool(H and m(H, 'selftest_alarm') >= 0.95),
            'M-2 localization >= 0.80 and above decoder and majority (95% LB > 0)': bool(C and M2['localization'] >= 0.80 and M2['loc_minus_decoder']['ci'][0] > 0 and M2['loc_minus_majority']['ci'][0] > 0)}
    R['M'] = dict(evaluated=len(M), harmful=len(H), distinct_harmful=len({r['pid'] for r in H}), distinct_scored=len(ids),
                  status={s: sum(r['status'] == s for r in M) for s in sorted({r['status'] for r in M})},
                  detected_selftest=m(H, 'selftest_alarm'), detected_telemetry=m(H, 'telemetry_alarm'), detected_either=m(H, 'either_alarm'),
                  detected_ce_drop_baseline=m(H, 'ce_drop_alarm'), M2=M2, subtle=dict(n=len(SB), detected_selftest=m(SB, 'selftest_alarm'), detected_telemetry=m(SB, 'telemetry_alarm'),
                  localized=m([r for r in SB if r.get('component_ok') is not None], 'component_ok')),
                  selftest_minus_telemetry=boot_diff([int(r['selftest_alarm']) - int(r['telemetry_alarm']) for r in H]) if H else None,
                  rule=rule, outcome='PASS' if all(rule.values()) else ('INSUFFICIENT' if not rule['M-0 >= 8 distinct scored harmful mutants'] else 'FAIL'))
json.dump(R, open(out, 'w'), indent=1); print(json.dumps(R, indent=1)[:6000])
