"""v16 held-out summary (docs/evidence/v16_diagnosability_protocol.md, A1 rule V-1..V-4). File reading and arithmetic only.
usage: python docs/evidence/v16_summary.py <out.json> <v16_dir_71> <v16_dir_72> <v16_dir_73> --S <v15_S_dir_71> <v15_S_dir_72> <v15_S_dir_73>"""
import json, os, sys
import numpy as np

a = sys.argv[1:]; out = a[0]; i = a.index('--S'); Vd, Sd = a[1:i], a[i + 1:]
rng = np.random.default_rng(7); NB = 4000
rd = lambda d, f: [json.loads(l) for l in open(os.path.join(d, f))]
def boot(fn, rows):
    vals = [fn([rows[k] for k in rng.integers(0, len(rows), len(rows))]) for _ in range(NB)]; return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]
def auc(y, s):
    y = np.asarray(y); s = np.asarray(s, float); pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0: return float('nan')
    return float(np.mean((pos[:, None] > neg[None, :]) + 0.5 * (pos[:, None] == neg[None, :])))
P, SG = [], []
for vd, sd in zip(Vd, Sd):
    S15 = {tuple(r['pair']): r for r in rd(sd, 'S_pairs.jsonl')}; H15 = {(r['fault'], r['inst']): r for r in rd(sd, 'S_single.jsonl')}
    R = json.load(open(os.path.join(vd, 'RESULT.json'))); assert R['battery_matches_v15'] and not R['trial'], vd
    for r in rd(vd, 'D_pairs.jsonl'):
        s = S15[tuple(r['pair'])]
        if s['effective']: P.append(dict(seed=R['seed'], same_group=r['same_group'], D=r['pf']['D'], pas=bool(r['pf']['acc']['all']), pas_st=bool(r['st']['acc']['all']),
                                         acc_pf=r['pf']['acc'], act=bool(s['both_family'])))
    for r in rd(vd, 'D_single.jsonl'):
        if H15[(r['fault'], r['inst'])]['harmful']: SG.append(dict(seed=R['seed'], pf=r['pf']['acc'], st=r['st']['acc']))
y_pas = [int(p['pas']) for p in P]; Dv = [p['D'] for p in P]
V1 = dict(auroc=auc(y_pas, Dv), ci=boot(lambda rw: auc([int(p['pas']) for p in rw], [p['D'] for p in rw]), P))
s1 = lambda rw, ch, m: float(np.mean([r[ch][m] for r in rw]))
V2 = dict(singles_pf_m1=s1(SG, 'pf', '1'), singles_pf_all=float(np.mean([float(r['pf']['all']) for r in SG])),
          pairs_pf_m100_minus_m5=dict(mean=float(np.mean([p['acc_pf']['100'] - p['acc_pf']['5'] for p in P])),
                                      ci=boot(lambda rw: float(np.mean([p['acc_pf']['100'] - p['acc_pf']['5'] for p in rw])), P)))
V3 = {m: dict(mean=s1(SG, 'st', m) - s1(SG, 'pf', m), ci=boot(lambda rw, m=m: s1(rw, 'st', m) - s1(rw, 'pf', m), SG), st=s1(SG, 'st', m), pf=s1(SG, 'pf', m)) for m in ('1', '5')}
PG = [p for p in P if p['same_group']]; cut = float(np.percentile(Dv, 100 / 3)); low = [p for p in P if p['D'] <= cut]
V4 = dict(active=float(np.mean([p['act'] for p in PG])), passive=float(np.mean([p['pas'] for p in PG])),
          diff=dict(mean=float(np.mean([p['act'] - p['pas'] for p in PG])), ci=boot(lambda rw: float(np.mean([p['act'] - p['pas'] for p in rw])), PG)),
          low_D_tertile=dict(cut=cut, n=len(low), active=float(np.mean([p['act'] for p in low])), passive=float(np.mean([p['pas'] for p in low]))))
curves = dict(singles={ch: {m: s1(SG, ch, m) for m in ['1', '2', '3', '5', '10', '20', '40', '60', '100']} for ch in ('pf', 'st')},
              pairs_pf={m: float(np.mean([p['acc_pf'][m] for p in P])) for m in ['1', '2', '3', '5', '10', '20', '40', '60', '100']},
              pairs_passive_full=dict(pf=float(np.mean(y_pas)), st=float(np.mean([p['pas_st'] for p in P]))), pairs_active=float(np.mean([p['act'] for p in P])))
rule = {'V-1 AUROC >= 0.60 and LB > 0.50': bool(V1['auroc'] >= 0.60 and V1['ci'][0] > 0.50),
        'V-2 singles m1 <= 0.30, full >= 0.85; pairs m100 - m5 LB > 0': bool(V2['singles_pf_m1'] <= 0.30 and V2['singles_pf_all'] >= 0.85 and V2['pairs_pf_m100_minus_m5']['ci'][0] > 0),
        'V-3 stage - pass/fail LB > 0 at m=1 and m=5 (singles)': bool(V3['1']['ci'][0] > 0 and V3['5']['ci'][0] > 0),
        'V-4 active - passive LB > 0; low-D tertile active >= 0.70, passive <= 0.30': bool(V4['diff']['ci'][0] > 0 and V4['low_D_tertile']['active'] >= 0.70 and V4['low_D_tertile']['passive'] <= 0.30)}
R = dict(n_effective_pairs=len(P), n_same_group=len(PG), n_harmful_singles=len(SG), V1=V1, V2=V2, V3=V3, V4=V4, curves=curves, rule=rule, V_PASS=bool(all(rule.values())))
json.dump(R, open(out, 'w'), indent=1); print(json.dumps(R, indent=1)[:5000])
