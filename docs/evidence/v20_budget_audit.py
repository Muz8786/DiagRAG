"""v20 B3 (bounded execution-budget comparison) and C5 (failure-case audit), from stored outputs only (file reading and arithmetic).
usage: python docs/evidence/v20_budget_audit.py <kaggle_dir> <out.json>"""
import hashlib, json, os, sys
import numpy as np

K, OUT = sys.argv[1:3]; rd = lambda p: [json.loads(l) for l in open(os.path.join(K, p))]
tid = lambda *x: hashlib.md5('|'.join(map(str, x)).encode()).hexdigest()[:12]
R = {}
# ---------------- B3: execution-budget frontier, effective same-group pairs, held-out seeds 71-73
act, pas = [], []
for s in (71, 72, 73):
    bat = json.load(open(os.path.join(K, f'heldout_v15_S_seed{s}', 'RESULT.json')))['battery']['size']
    A = {tuple(r['pair']): r for r in rd(f'heldout_v15_S_seed{s}/S_pairs.jsonl')}
    for r in rd(f'heldout_v16_seed{s}/D_pairs.jsonl'):
        a = A[tuple(r['pair'])]
        if not (a['effective'] and a['same_group']): continue
        act.append(dict(seed=s, pair=r['pair'], runs=a['runs'], ok=bool(a['both_family']), battery=bat))
        pas.append(dict(seed=s, pf=r['pf']['acc'], st=r['st']['acc']))
runs = np.array([a['runs'] for a in act]); ok = np.array([a['ok'] for a in act]); bats = np.array([a['battery'] for a in act])
Bs = [1, 5, 20, 100, 200, 300, 400, 500, 750, 1000, 1500, int(runs.max())]
def pas_at(B, ch):
    keys = [1, 2, 3, 5, 10, 20, 40, 60, 100]
    if B >= int(bats.max()): return float(np.mean([bool(p[ch]['all']) for p in pas])), f'full battery ({int(bats.min())}-{int(bats.max())} executions)'
    k = max(x for x in keys if x <= min(B, 100)); return float(np.mean([p[ch][str(k)] for p in pas])), f'{k} random probes ({k} executions)'
rows = []
for B in Bs:
    pf, how = pas_at(B, 'pf'); st, _ = pas_at(B, 'st')
    rows.append(dict(budget_executions=B, active_named_within_budget=float(np.mean(ok & (runs <= B))), passive_pass_fail=pf, passive_stage=st, passive_basis=how,
                     passive_measured=bool(B <= 100 or B >= int(bats.max()))))
R['B3_budget_frontier'] = dict(
    n_pairs=len(act), unique_probes_per_battery=sorted(set(bats.tolist())),
    active_probe_executions=dict(min=int(runs.min()), median=float(np.median(runs)), mean=float(runs.mean()), p90=float(np.percentile(runs, 90)), max=int(runs.max())),
    active_named_any_budget=float(ok.mean()), rows=rows,
    active_metric='completed_success_within_budget; intermediate predictions unavailable',
    exact_cost_matched=False, adaptive_passive_measured=False,
    causal_intervention_effect_identified=False,
    same_unique_probes=dict(active=float(ok.mean()), passive_pass_fail=float(np.mean([bool(p['pf']['all']) for p in pas])), passive_stage=float(np.mean([bool(p['st']['all']) for p in pas]))),
    reading=('Rows compare active success among cases using at most B executions with passive decoding using the largest saved random-probe prefix no longer than B (up to 100), or the full 102-103 probe battery once B covers it. Active values count successful completed runs divided by all eligible pairs; runs exceeding the ceiling count as zero. Intermediate predictions at interruption were not saved, so these values do not measure a budget-stopped active policy. These are execution-budget ceilings, not exact-cost matched pairs. '
             'The same-unique-probe comparison is reported separately. Passive decoding with as many unique probes as the active executions was not measured.'))
# ---------------- C5: failure audit with trace ids (ids are md5 of run, fault, base-query id; base-query ids are real ESCI queries, nothing is invented)
C = json.load(open(os.path.join(K, '..', 'docs', 'evidence', 'diagnosis_confusion_v6cpu.json')))
per = C['A_attributor']['per_fault']
EP = [json.loads(l) for l in open(os.path.join(K, 'judged_cpu_run_v6_seed50', 'episodes.jsonl'))]
q03 = [e for e in EP if e['fault'] == 'Q03' and e['split'] == 'test']
fails = []
for s_ in (71, 72, 73):
    for r in rd(f'heldout_v15_S_seed{s_}/S_single.jsonl'):
        if r['harmful'] and not r['detected']: fails.append(dict(kind='self-test misses a harmful system fault', run=f'heldout_v15_S_seed{s_}', fault=r['fault'], inst=r['inst'], traffic_broken=r['traffic_broken'], trace_id=tid('v15S', s_, r['fault'], r['inst'])))
for r in rd('judged_v18_seed76/B_bugs.jsonl'):
    if r['id'] == 'B3': fails.append(dict(kind='reproduced bug escapes the probe battery', run='judged_v18_seed76', bug='B3 langchain#37046', natural_broken=r['nat_broken'], probe_fail=r['probe_fail'], trace_id=tid('v18', 76, 'B3')))
pairs = [dict(r, seed=s) for s in (71, 72, 73) for r in rd(f'heldout_v15_S_seed{s}/S_pairs.jsonl') if r['effective'] and r['same_group']]
succ_case = next(r for r in pairs if r['both_family'] and len(r['named']) == 2)
fail_case = next(r for r in pairs if not r['both_family'])
R['C5_failure_audit'] = dict(
    Q03=dict(run='judged_cpu_run_v6_seed50', test_episodes=len(q03), per_class=per.get('Q03'), example_trace_ids=[tid('cpu50', 'Q03', e['bid']) for e in q03[:3]],
             example_base_query_ids=[e['bid'] for e in q03[:3]]),
    K04=per.get('K04'), R24=per.get('R24'), other_failures=fails,
    active_success=dict(seed=succ_case['seed'], pair=succ_case['pair'], named=succ_case['named'], probe_executions=succ_case['runs'], verified=succ_case['verified'], trace_id=tid('v15S', succ_case['seed'], *succ_case['pair'])),
    active_failure=dict(seed=fail_case['seed'], pair=fail_case['pair'], named=fail_case['named'], probe_executions=fail_case['runs'], verified=fail_case['verified'], fallback=fail_case['fallback'], trace_id=tid('v15S', fail_case['seed'], *fail_case['pair'])))
json.dump(R, open(OUT, 'w'), indent=1, default=str); print(json.dumps(R, indent=1, default=str)[:6000])
