"""Prepare the v7 working checkpoint from the v6 CPU judged run's checkpoint (docs/evidence/v7_composed_protocol.md section 4).
Removes ONLY results that depend on the attributor, so v7 recomputes them with the retrained attributor:
  CAL (conformal calibration scores), NAT3 (natural-traffic rows), LOFO (leave-one-fault-out rows), BASEL['det'] (the attributor's detection baseline), and the per-episode 'loop3' field.
Kept untouched: CLEAN, EPIS (single-fault episodes, their oracle repairs), GEN, GSTATE, SEEN, HARM, FAMR, CENS, the external repair baselines, the text caches.
Usage: python v7_prepare_checkpoint.py <v6 checkpoint.pkl> <out checkpoint.pkl>"""
import hashlib, json, pickle, sys
R = pickle.load(open(sys.argv[1], 'rb')); report = dict(source_stage=R['stage'])
for k in ('CAL', 'NAT3', 'LOFO'): report[f'removed_{k}'] = len(R.pop(k, {}))
report['removed_BASEL_det'] = 'det' in R['BASEL']; R['BASEL'].pop('det', None); R['BASEL'].pop('raglog_error', None)
n = 0
for e in R['EPIS']:
    if 'loop3' in e: del e['loop3']; n += 1
report['removed_episode_loop3'] = n; R['stage'] = 'repair_done'
sig = hashlib.sha256(json.dumps(sorted((e['fault'], e['bid'], e['split'], bool(e.get('oracle_rescued'))) for e in R['EPIS'])).encode()).hexdigest()
report['kept_episode_signature_sha256'] = sig; report['n_episodes'] = len(R['EPIS']); report['kept_keys'] = sorted(k for k in R if k != 'caches')
pickle.dump(R, open(sys.argv[2], 'wb'), protocol=4); print(json.dumps(report, indent=1))
