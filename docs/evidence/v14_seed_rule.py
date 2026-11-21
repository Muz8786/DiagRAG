"""v14 E1 (docs/evidence/v14_flagship_protocol.md): the seed-averaged adoption rule R-avg and the majority rule R-maj, from the judged runs' gate tables (file reading only).
usage: python docs/evidence/v14_seed_rule.py <run_dir_71> <run_dir_72> <run_dir_73> [--descriptive <dir_50> <dir_52> <dir_55>] > out.json"""
import csv, json, math, os, sys

CORE = 'Q01 Q02 Q03 Q04 Q05 Q07 Q09 K03 K04 K05 K06 K07 K08 K09 R01 R03 R05 R06 R07 R10 R11 R13 R15 R19 R22 R23 R24 C2'.split(); assert len(CORE) == 28
def wilson_lo(k, n, z=1.96):
    if n == 0: return float('nan')
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return (c - h) / d
def rule(dirs):
    D = [{r['fault']: r for r in csv.DictReader(open(os.path.join(d, 'detector_gates.csv')))} for d in dirs]
    RP = [{r['fault']: r for r in csv.DictReader(open(os.path.join(d, 'repair_gates.csv')))} for d in dirs]
    V = [json.load(open(os.path.join(d, 'VERDICT.json'))) for d in dirs]
    det, rep = {}, {}
    for f in CORE:
        a = [float(x[f]['auroc']) if f in x and x[f].get('auroc') not in ('', None) else float('nan') for x in D]
        npos = [int(float(x[f]['n_pos_test'])) if f in x else 0 for x in D]
        mean = sum(a) / len(a); det[f] = dict(aurocs=a, mean=mean, n_pos=npos, passed=bool(all(n >= 50 for n in npos) and mean >= 0.70))
        k = sum(int(float(x[f]['rescued'])) for x in RP if f in x); n = sum(int(float(x[f]['n_hard'])) for x in RP if f in x)
        cn = sum(int(float(x[f]['clean_n'])) for x in RP if f in x); cl = sum(int(float(x[f]['clean_lost'])) for x in RP if f in x)
        lo = wilson_lo(k, n); rep[f] = dict(rescued=k, n_hard=n, wilson_lo=lo, clean_n=cn, clean_lost=cl, passed=bool(n >= 150 and lo >= 0.50 and (cl / cn if cn else 0.0) <= 0.10))
    nd, nr = sum(v['passed'] for v in det.values()), sum(v['passed'] for v in rep.values())
    per_run = [dict(dir=os.path.basename(d.rstrip('/')), verdict=v['verdict'], detectors=v['detectors_pass'], repairs=v['repairs_pass'], loop_gates=v.get('loop_gates'),
                    U1=(v.get('U1') or {}).get('mean_closure'), L1=(v.get('guarantee') or {}).get('heldout_clean_loss'), L2=(v.get('guarantee') or {}).get('mean_closure'),
                    N1=(v.get('N1') or {}).get('delta')) for d, v in zip(dirs, V)]
    return dict(R_avg=dict(detectors_pass=nd, repairs_pass=nr, verdict='ADOPTED_avg' if nd >= 27 and nr >= 24 else 'NOT_ADOPTED_avg',
                           failing_detectors=[f for f in CORE if not det[f]['passed']], failing_repairs=[f for f in CORE if not rep[f]['passed']]),
                R_maj=dict(adopted_runs=sum(v['verdict'] == 'ADOPTED' for v in V), of=len(V), verdict='ADOPTED_maj' if sum(v['verdict'] == 'ADOPTED' for v in V) >= 2 else 'NOT_ADOPTED_maj'),
                per_run=per_run, detectors=det, repairs=rep)
a = sys.argv[1:]
if '--descriptive' in a: i = a.index('--descriptive'); judged, desc = a[:i], a[i + 1:]
else: judged, desc = a, []
out = dict(judged_seeds=rule(judged))
if desc: out['descriptive_old_seeds'] = rule(desc)
print(json.dumps(out, indent=1))
