"""v14 amendment A3 (docs/evidence/v14_flagship_protocol.md): small-stratum fallback for the per-stratum CRC gate, computed offline from a judged E4 run's
calibration.jsonl and test.jsonl (file reading and arithmetic only). A stratum with fewer than ceil((1 - alpha) / alpha) calibration queries cannot get a finite CRC threshold,
so it uses the pooled (global) CRC threshold; the capped variant caps with the pooled calibration scores for such a stratum.
usage: python docs/evidence/v14_port_fallback.py <v14_port_<ds>_out dir>  -> prints JSON"""
import json, math, os, sys
import numpy as np

d = sys.argv[1]; ALPHA, CAP = 0.005, 0.20; INF = float('inf'); NMIN = math.ceil((1 - ALPHA) / ALPHA)
cal = [json.loads(l) for l in open(os.path.join(d, 'calibration.jsonl'))]; te = [json.loads(l) for l in open(os.path.join(d, 'test.jsonl'))]
def crc(s, l):
    n = len(s)
    if n == 0: return INF
    for lam in sorted(set(s.tolist())) + [INF]:
        if n / (n + 1) * np.mean((s >= lam) * l) + 1 / (n + 1) <= ALPHA: return lam
    return INF
def cap(s):
    if len(s) == 0: return INF
    for lam in sorted(set(s.tolist())) + [INF]:
        if np.mean(s >= lam) <= CAP: return lam
    return INF
S = sorted({r['strat'] for r in cal} | {r['strat'] for r in te})
sa = lambda sn: np.array([r['s'] for r in cal if sn is None or r['strat'] == sn], float); la = lambda sn: np.array([r['l_rep'] for r in cal if sn is None or r['strat'] == sn], float)
G = crc(sa(None), la(None)); small = {sn: len(sa(sn)) < NMIN for sn in S}
LAM = {sn: (G if small[sn] else crc(sa(sn), la(sn))) for sn in S}
LAMC = {sn: max(LAM[sn], cap(sa(None) if small[sn] else sa(sn))) for sn in S}
def wilson(k, n, z=1.96):
    if n == 0: return [float('nan')] * 2
    p = k / n; dd = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return [(c - h) / dd, (c + h) / dd]
def ev(lam):
    per, clean = {}, []
    for x in te:
        dsp = x['s'] >= lam[x['strat']]; ok = x['ok_rep'] if dsp else (x['h5'] if x['fault'] == 'NONE' else False)
        if x['fault'] == 'NONE': clean.append((x['h5'] and not ok, dsp))
        else: per.setdefault(x['fault'], []).append(ok)
    k = sum(c[0] for c in clean); n = len(clean)
    return dict(clean_loss=k / max(1, n), clean_loss_wilson=wilson(k, n), clean_dispatch=float(np.mean([c[1] for c in clean])), mean_closure=float(np.mean([np.mean(v) for v in per.values()])),
                per_fault={f: float(np.mean(v)) for f, v in per.items()})
out = dict(n_min=NMIN, calibration_n={sn: int(len(sa(sn))) for sn in S}, small_strata=[sn for sn in S if small[sn]], lambdas=dict(fallback=LAM, fallback_capped=LAMC, global_=G),
           mondrian_fallback=ev(LAM), capped_fallback=ev(LAMC))
out['pass'] = dict(mondrian_fallback_loss_ok=out['mondrian_fallback']['clean_loss'] <= ALPHA, capped_fallback_loss_ok=out['capped_fallback']['clean_loss'] <= ALPHA,
                   capped_fallback_closure_ok=out['capped_fallback']['mean_closure'] >= 0.70)
out['pass']['A3_PASS'] = all(out['pass'].values())
print(json.dumps(out, indent=1, default=str))
