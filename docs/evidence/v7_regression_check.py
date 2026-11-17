"""v7 protocol section 4: single-fault regression check, v7 (retrained attributor) against the v6 CPU judged run.
usage: python docs/evidence/v7_regression_check.py <v6_dir> <v7_dir> <out.json>
Nothing here is tuned: it reads the two runs' own files and applies the regression definition fixed in the protocol.
A REGRESSION is: a core-28 detector or repair status going PASS -> FAIL/THIN; the verdict leaving ADOPTED; L1, L2 or N1 PASS -> FAIL;
capped_crc_0.005 ceasing to meet all four targets. Everything else is a reported difference. U1 carries no bar."""
import json, os, sys
import pandas as pd

a_dir, b_dir, out = sys.argv[1:4]
A = json.load(open(os.path.join(a_dir, 'VERDICT.json'))); B = json.load(open(os.path.join(b_dir, 'VERDICT.json')))
res = dict(regressions=[], differences=[]); R = res['regressions']; D = res['differences']

core = A['accounting']['a_core28']
# per-fault statuses (all rows in the gate tables; core-28 = the faults the v6 run counted)
for name, key in (('detector_gates.csv', 'detector'), ('repair_gates.csv', 'repair')):
    ta = pd.read_csv(os.path.join(a_dir, name)); tb = pd.read_csv(os.path.join(b_dir, name))
    ta = ta.drop_duplicates('fault').set_index('fault'); tb = tb.drop_duplicates('fault').set_index('fault')
    res[key + '_status_changes'] = []
    for f in sorted(set(ta.index) | set(tb.index)):
        sa = ta['status'].get(f); sb = tb['status'].get(f)
        if sa != sb:
            res[key + '_status_changes'].append(dict(fault=f, v6=sa, v7=sb))
            if sa == 'PASS' and sb in ('FAIL', 'THIN'): R.append(f'{key} {f}: PASS -> {sb}')
    num = [c for c in ta.columns if c not in ('status', 'detector')] if key == 'detector' else [c for c in ta.columns if c != 'status']
    res[key + '_numeric_identical'] = bool(ta[num].equals(tb[num].reindex(ta.index))) if set(ta.index) == set(tb.index) else False

for k in ('detectors_pass', 'repairs_pass', 'solved_both', 'of'):
    if A[k] != B[k]: D.append(f'{k}: v6 {A[k]} -> v7 {B[k]}')
res['counts'] = {k: (A[k], B[k]) for k in ('detectors_pass', 'repairs_pass', 'solved_both', 'of')}
res['verdict'] = (A['verdict'], B['verdict'])
if B['verdict'] != 'ADOPTED' and A['verdict'] == 'ADOPTED': R.append(f"verdict ADOPTED -> {B['verdict']}")
res['loop_gates'] = (A['loop_gates'], B['loop_gates'])
for g in ('L1', 'L2', 'N1'):
    if A['loop_gates'].get(g) == 'PASS' and B['loop_gates'].get(g) != 'PASS': R.append(f'{g}: PASS -> {B["loop_gates"].get(g)}')
    elif A['loop_gates'].get(g) != B['loop_gates'].get(g): D.append(f'{g}: {A["loop_gates"].get(g)} -> {B["loop_gates"].get(g)}')
res['U1'] = (A['U1'], B['U1'])
res['U1_delta_mean_closure'] = B['U1']['mean_closure'] - A['U1']['mean_closure']
res['N1'] = {k: (A['N1'].get(k), B['N1'].get(k)) for k in ('hit_before', 'hit_after', 'delta', 'ci_lo', 'ci_hi', 'fixed', 'broken', 'verdict')}
ga = A['guarantee']; gb = B['guarantee']
res['guarantee'] = {k: (ga.get(k), gb.get(k)) for k in ('lambdas', 'heldout_clean_loss', 'heldout_clean_loss_by_stratum', 'mean_closure', 'L1', 'L2')}
pa = {p['policy']: p for p in A['policies']}; pb = {p['policy']: p for p in B['policies']}
cap = 'capped_crc_0.005'
res['capped_crc_0.005'] = {k: (pa[cap][k], pb[cap][k]) for k in ('mean_closure', 'clean_loss', 'clean_dispatch_rate', 'clean_mean_cost', 'T1_loss', 'T2_dispatch', 'T3_cost', 'T4_closure', 'all_targets_met')}
if not pb[cap]['all_targets_met']: R.append('capped_crc_0.005 no longer meets all four targets')
res['policy_table'] = {p: {k: (pa[p][k], pb[p][k]) for k in ('mean_closure', 'clean_loss', 'clean_dispatch_rate', 'all_targets_met')} for p in pa if p in pb}
res['detection_baselines'] = {k: (A['detection_baselines'].get(k), B['detection_baselines'].get(k)) for k in A['detection_baselines'] if not isinstance(A['detection_baselines'][k], list) or len(A['detection_baselines'][k]) == 3}
res['unseen_mean_closure'] = (A['unseen_mean_closure'], B['unseen_mean_closure'])
res['cheap_guarantee_changed'] = A['cheap_guarantee'] != B['cheap_guarantee']
ua = pd.read_csv(os.path.join(a_dir, 'unseen_faults.csv')).set_index('fault'); ub = pd.read_csv(os.path.join(b_dir, 'unseen_faults.csv')).set_index('fault')
res['unseen_closure_by_fault_changes'] = {f: (float(ua.loc[f, 'closure']), float(ub.loc[f, 'closure'])) for f in ua.index if f in ub.index and abs(ua.loc[f, 'closure'] - ub.loc[f, 'closure']) > 1e-12}
res['REGRESSION'] = bool(R)
json.dump(res, open(out, 'w'), indent=1, default=str)
print('REGRESSIONS:', R if R else 'none'); print('REGRESSION =', res['REGRESSION'])
print('counts', res['counts'], 'verdict', res['verdict']); print('loop gates', A['loop_gates'], '->', B['loop_gates'])
print('detector status changes', res['detector_status_changes']); print('repair status changes', res['repair_status_changes'])
print('detector numeric tables identical:', res['detector_numeric_identical'], '| repair numeric tables identical:', res['repair_numeric_identical'])
print('U1', A['U1']['mean_closure'], '->', B['U1']['mean_closure'], 'delta', round(res['U1_delta_mean_closure'], 4))
print('N1 delta', res['N1']['delta'], 'hit_after', res['N1']['hit_after'])
print('capped', {k: v for k, v in res['capped_crc_0.005'].items()})
print('guarantee', res['guarantee'])
