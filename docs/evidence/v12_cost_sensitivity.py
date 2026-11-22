"""v12 Part A (docs/evidence/v12_cost_protocol.md): how sensitive is the policy cost comparison to the repair-cost weights? Recomputed from the SAVED held-out episodes of a judged run; no retrieval is run.
STEP 1 (gate): rebuild every policy's dispatch decisions from the stored calibration records and REPRODUCE the stored policy table (clean dispatch rate, clean mean cost, faulted mean cost) under the
original weights 1/3/8. If it does not match, the script stops. STEP 2: the grid of weights (wQ = 1; wK, wR in a fixed grid, no ordering assumed).
Not reconstructable and therefore excluded: policy tau_none_5pct_fpr (its threshold comes from out-of-fold group predictions that are not stored).
usage: python docs/evidence/v12_cost_sensitivity.py <judged_folder_with_checkpoint> <out.json>"""
import collections, itertools, json, os, pickle, sys
import numpy as np

d, outp = sys.argv[1], sys.argv[2]
R = pickle.load(open(os.path.join(d, 'checkpoint.pkl'), 'rb')); V = json.load(open(os.path.join(d, 'VERDICT.json')))
EP = [e for e in R['EPIS'] if e['split'] == 'test' and 'loop3' in e]; CAL = R['CAL']; STRATA = ['esci_common', 'esci_rare', 'shop']; ALPHA = 0.005; ALPHAS = [0.0025, 0.005, 0.01, 0.02]; CAP = 0.20
cv = list(CAL.values())
def cal_arr(sn=None): rows = [v for v in cv if sn is None or v[2] == sn]; return np.array([v[0] for v in rows]), np.array([v[1] for v in rows])
def cal_arr5(sn): rows = [v for v in cv if v[2] == sn]; return np.array([v[0] for v in rows]), np.array([v[3] for v in rows]), np.array([v[4] for v in rows])
def crc_lambda(s, l, a):
    n = len(s)
    if n == 0: return float('inf')
    for lam in sorted(set(s.tolist())) + [float('inf')]:
        if n / (n + 1) * np.mean((s >= lam) * l) + 1 / (n + 1) <= a: return lam
    return float('inf')
def crc_ts(s, ln, lc, a):
    n = len(s)
    if n == 0: return float('inf')
    for lam in sorted(set(s.tolist())) + [float('inf')]:
        if n / (n + 1) * np.mean(np.where(s >= lam, np.maximum(ln, lc), ln)) + 1 / (n + 1) <= a: return lam
    return float('inf')
def cap_lambda(s, frac):
    if len(s) == 0: return float('inf')
    for lam in sorted(set(s.tolist())) + [float('inf')]:
        if np.mean(s >= lam) <= frac: return lam
    return float('inf')
LAMS = {a: {sn: crc_lambda(*cal_arr(sn), a) for sn in STRATA} for a in ALPHAS}; LAM_GLOBAL = crc_lambda(*cal_arr(), ALPHA)
LAMS_CAP = {sn: max(LAMS[ALPHA][sn], cap_lambda(cal_arr(sn)[0], CAP)) for sn in STRATA}; LAMS_TS = {sn: max(crc_ts(*cal_arr5(sn), ALPHA), cap_lambda(cal_arr5(sn)[0], CAP)) for sn in STRATA}
# lambdas must equal the ones stored in the verdict
stored_l = V['guarantee']['lambdas']; assert all(abs(LAMS[ALPHA][sn] - stored_l[sn]) < 1e-12 for sn in STRATA), 'reconstructed Mondrian lambdas differ from the stored ones'
GROUP = lambda l: l[1] if l.startswith('G') else l[0]
def counts(labels):
    c = collections.Counter(GROUP(str(l)) for l in labels); return np.array([c['Q'], c['K'], c['R']], float)
def decide(pol, e):
    L = e['loop3']; s = L['s']; st = L['strat']
    if pol == 'global_crc_0.005': return s >= LAM_GLOBAL, counts(L['lab'])
    if pol.startswith('mondrian_crc_'): return s >= LAMS[float(pol.split('_')[-1])][st], counts(L['lab'])
    if pol == 'capped_crc_0.005': return s >= LAMS_CAP[st], counts(L['lab'])
    if pol == 'two_stage_0.005':
        c_ = s >= LAMS_TS[st]; n_ = bool(L['nat'])
        if c_ and n_: return True, counts(list(L['nat']) + list(L['lab']))
        if c_: return True, counts(L['lab'])
        if n_: return True, counts(L['nat'])
        return False, np.zeros(3)
POLS = ['global_crc_0.005'] + [f'mondrian_crc_{a}' for a in ALPHAS] + ['capped_crc_0.005', 'two_stage_0.005']
W0 = np.array([1.0, 3.0, 8.0]); faults = sorted({e['fault'] for e in EP} - {'NONE'})
def cost_counts(pol, e):
    d_, c_ = decide(pol, e); return c_ if d_ else np.zeros(3)   # a policy that does not dispatch pays nothing (as in the stored table)
def per_policy():
    out = {}
    for pol in POLS:
        clean = [e for e in EP if e['fault'] == 'NONE']; cc = np.array([cost_counts(pol, e) for e in clean]); cd = np.mean([decide(pol, e)[0] for e in clean])
        fc = {f: np.mean([cost_counts(pol, e) for e in EP if e['fault'] == f], axis=0) for f in faults}
        out[pol] = dict(clean_counts=cc.mean(0), clean_dispatch=float(cd), faulted_counts=np.mean([fc[f] for f in faults], axis=0))
    return out
PP = per_policy()
# ---- STEP 1: reproduce the stored table
chk = []; stored = {p['policy']: p for p in V['policies']}
for pol in POLS:
    s = stored[pol]; mc = float(PP[pol]['clean_counts'] @ W0); mf = float(PP[pol]['faulted_counts'] @ W0)
    chk.append(dict(policy=pol, clean_dispatch_rec=PP[pol]['clean_dispatch'], clean_dispatch_stored=s['clean_dispatch_rate'], clean_cost_rec=mc, clean_cost_stored=s['clean_mean_cost'], faulted_cost_rec=mf, faulted_cost_stored=s['mean_cost_faulted']))
bad = [c['policy'] for c in chk if abs(c['clean_dispatch_rec'] - c['clean_dispatch_stored']) > 1e-9 or abs(c['clean_cost_rec'] - c['clean_cost_stored']) > 1e-9 or abs(c['faulted_cost_rec'] - c['faulted_cost_stored']) > 1e-9]
print('STEP 1 reproduction of the stored policy table:', 'ALL MATCH' if not bad else f'MISMATCH {bad}'); [print('  ', json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in c.items()})) for c in chk]
if bad: sys.exit(1)
# ---- STEP 2: weight grid
GRID = [0.25, 0.5, 1, 2, 3, 5, 8, 12, 20]; combos = [(1.0, float(a), float(b)) for a in GRID for b in GRID]; res = {}
for pol in POLS:
    cc, fc = PP[pol]['clean_counts'], PP[pol]['faulted_counts']; rc = np.array([cc @ np.array(w) / sum(w) for w in combos]); rf = np.array([fc @ np.array(w) / sum(w) for w in combos])
    res[pol] = dict(clean_cost_ratio_to_universal=dict(min=float(rc.min()), median=float(np.median(rc)), max=float(rc.max()), share_below_1=float((rc < 1).mean()), share_below_0_25=float((rc < 0.25).mean()), share_le_0_125=float((rc <= 0.125).mean())),
                    faulted_cost_ratio_to_universal=dict(min=float(rf.min()), median=float(np.median(rf)), max=float(rf.max()), share_below_1=float((rf < 1).mean())),
                    mean_repairs_per_clean_query_QKR=[float(x) for x in cc], mean_repairs_per_faulted_query_QKR=[float(x) for x in fc], clean_dispatch=PP[pol]['clean_dispatch'])
out = dict(folder=d, n_combinations=len(combos), grid=GRID, weights_note='wQ = 1 fixed; wK and wR free; universal repair = one Q + one K + one R repair per query (cost wQ + wK + wR)', reproduction=chk, policies=res,
           universal_counts_QKR=[1, 1, 1], excluded_policy='tau_none_5pct_fpr (threshold not reconstructable)')
json.dump(out, open(outp, 'w'), indent=1)
print('\nSTEP 2: cost of each policy as a share of the universal repair, over', len(combos), 'weight combinations (clean queries):')
for pol in POLS:
    r = res[pol]['clean_cost_ratio_to_universal']; q = res[pol]['mean_repairs_per_clean_query_QKR']
    print(f"  {pol:20s} Q/K/R repairs per clean query {q[0]:.3f}/{q[1]:.3f}/{q[2]:.3f}  ratio min {r['min']:.3f} median {r['median']:.3f} max {r['max']:.3f} | <1: {100 * r['share_below_1']:.0f}%  <0.25: {100 * r['share_below_0_25']:.0f}%  <=0.125: {100 * r['share_le_0_125']:.0f}%")
