"""Brief section 9 and section 5: (1) the all-runs matrix, (2) the dispatch-policy frontier. Both are generated from the judged files; nothing is typed by hand.
Usage: python make_matrix_and_frontier.py <kaggle dir> <out.md> [<out.json>]
Runs that do not exist yet (for example a v5 folder) are listed as "not run"."""
import csv, json, os, sys
import numpy as np

K, OUT = sys.argv[1], sys.argv[2]
RUNS = [('seed 42', 'judged_cpu_run_seed42', 'CPU', 'v1 (older code, not shipped)'), ('seed 43', 'judged_cpu_run_seed43', 'CPU', 'v1'), ('seed 44', 'judged_cpu_run_v2_seed44', 'CPU', 'v2'),
        ('seed 45', 'judged_cpu_run_v3_seed45', 'CPU', 'v3'), ('seed 46', 'judged_gpu_v3_seed46', 'GPU T4', 'v3'), ('seed 47', 'judged_cpu_run_v4_seed47', 'CPU', 'v4'),
        ('seed 48', 'judged_gpu_v4_seed48', 'GPU T4', 'v4'), ('seed 49', 'judged_cpu_run_v5_seed49', 'CPU', 'v5'), ('seed 50', 'judged_gpu_v6_seed50', 'GPU T4', 'v6 (flagship)'), ('seed 50 (CPU replication)', 'judged_cpu_run_v6_seed50', 'CPU', 'v6')]
def f3(x): return '-' if x is None else f'{x:.3f}'
lines = ['## All judged runs (every run, pass or fail)', '',
         '| Run | Stack | Code | Detectors / repairs / both (of 28) | L1 clean loss | L2 closure | U1 (bar 0.50) | N1 natural gain (95% CI) | Verdict |', '|---|---|---|---|---|---|---|---|---|']
for tag, folder, stack, code in RUNS:
    d = os.path.join(K, folder); vp = os.path.join(d, 'VERDICT.json')
    if not os.path.exists(vp): lines.append(f'| {tag} | {stack} | {code} | not run | | | | | |'); continue
    v = json.load(open(vp)); gl = v.get('loop_gates') or {}; g = v.get('guarantee') or {}; u = v.get('U1'); n1 = v.get('N1')
    l1 = g.get('heldout_clean_loss'); l2 = g.get('mean_closure')
    u1s = f"{u['mean_closure']:.3f} ({gl.get('U1', '-')})" if isinstance(u, dict) else (f"{v.get('unseen_mean_closure', float('nan')):.3f}" if v.get('unseen_mean_closure') is not None else '-')
    n1s = f"{100 * n1['delta']:+.2f} [{100 * n1['ci_lo']:+.2f}, {100 * n1['ci_hi']:+.2f}] ({n1['verdict']})" if isinstance(n1, dict) and 'delta' in n1 else '-'
    l1s = f"{100 * l1:.2f}% ({gl.get('L1', '-')})" if l1 is not None else '-'
    l2s = f"{l2:.3f} ({gl.get('L2', '-')})" if l2 is not None else '-'
    lines.append(f"| {tag} | {stack} | {code} | {v['detectors_pass']} / {v['repairs_pass']} / {v['solved_both']} | {l1s} | {l2s} | {u1s} | {n1s} | **{v['verdict']}** |")
lines += ['', 'Notes: seed 42 used older v1 code whose hash is not shipped. L1 and L2 are defined from v2 onward (v1 runs predate them; "-" means not measured). Natural-traffic samples overlap across v3, v4 and v5 (one query sample), so N1 values are repeated measurements.', '']
# ---- frontier
fl = ['## Dispatch policies: clean loss, clean dispatch, mean cost, closure (held-out, same denominators)', '']
for tag, folder, stack, code in RUNS:
    vp = os.path.join(K, folder, 'VERDICT.json')
    if not os.path.exists(vp) or 'policies' not in json.load(open(vp)): continue
    v = json.load(open(vp)); P = v['policies']
    P = [p for p in P if all(k in p for k in ('clean_loss', 'clean_dispatch_rate', 'clean_mean_cost', 'mean_closure'))]
    if not P: continue
    fl += [f'### {tag}, {stack}, {code}', '', '| Policy | Clean loss | Clean dispatch | Classifier-only dispatch | Clean mean cost | Mean closure | On frontier |', '|---|---|---|---|---|---|---|']
    pts = [(p['policy'], p['clean_loss'], p['clean_dispatch_rate'], p['mean_closure'], p) for p in P]
    def dominated(i):   # i is dominated if another point is <= on loss and dispatch and >= on closure, and strictly better on at least one
        _, l, dsp, c, _p = pts[i]
        return any((l2 <= l and d2 <= dsp and c2 >= c) and (l2 < l or d2 < dsp or c2 > c) for j, (_, l2, d2, c2, _q) in enumerate(pts) if j != i)
    for i, (name, l, dsp, c, p) in enumerate(pts):
        fl.append(f"| {name} | {100 * l:.2f}% | {100 * dsp:.1f}% | {('%.1f%%' % (100 * p['clean_clf_dispatch_rate'])) if 'clean_clf_dispatch_rate' in p else '-'} | {p['clean_mean_cost']:.2f} | {c:.3f} | {'no' if dominated(i) else '**yes**'} |")
    fl += ['', 'Frontier = no other policy is at least as good on clean loss, clean dispatch and closure and strictly better on one. Targets (v5 protocol): loss <= 0.5%, total clean dispatch <= 25%, mean cost <= 1.5, closure >= 0.80.', '']
    ch = v.get('cheap_guarantee')
    if ch: fl += [f"Policies meeting all four targets with a CRC guarantee: {ch['guaranteed_policies_meeting_all_four'] or 'none'}; without a guarantee: {ch['no_guarantee_policies_meeting_all_four'] or 'none'}. Claim rule result: {ch['claim']}.", '']
open(OUT, 'w', encoding='utf-8').write('\n'.join(lines + fl)); print('\n'.join(lines + fl)[:6000])
