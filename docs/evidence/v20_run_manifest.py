"""v20 D: machine-readable manifest of every stored run folder (file reading and hashing only).
For each folder under kaggle/ (judged_*, heldout*, dev_*, void_*): kind, seed, dataset, code hash, device and library versions where recorded, and every file with size and SHA-256.
usage: python docs/evidence/v20_run_manifest.py <repo_root> <out.json>"""
import hashlib, json, os, subprocess, sys

root, out = sys.argv[1:3]; K = os.path.join(root, 'kaggle')
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True).stdout.strip()
runs = []
for d in sorted(os.listdir(K)):
    p = os.path.join(K, d)
    if not os.path.isdir(p) or not d.startswith(('judged_', 'heldout', 'dev_', 'void_')): continue
    meta = dict(folder=f'kaggle/{d}', kind=d.split('_')[0])
    for pf in ('JUDGED_PROTOCOL.json', 'PORT_PROTOCOL.json', 'LC2_PROTOCOL.json', 'RESULT.json'):
        f = os.path.join(p, pf)
        if not os.path.exists(f): continue
        try: j = json.load(open(f))
        except Exception: continue
        cfg = j.get('cfg') or {}
        meta.setdefault('seed', cfg.get('SEED', j.get('seed')))
        meta.setdefault('dataset', cfg.get('DATASET', j.get('dataset')))
        meta.setdefault('code_sha256', j.get('code_sha256'))
        meta.setdefault('device', j.get('device'))
        env = j.get('env') or {}
        if isinstance(env, dict) and env: meta.setdefault('env', {k: env[k] for k in list(env)[:12]})
        if 'role' in j: meta.setdefault('role', j['role'])
        if 'trial' in j: meta.setdefault('trial', j['trial'])
    files = []
    for dp, _, fs in os.walk(p):
        for fn in sorted(fs):
            fp = os.path.join(dp, fn); files.append(dict(path=os.path.relpath(fp, root), bytes=os.path.getsize(fp), sha256=sha(fp)))
    meta['files'] = files; runs.append(meta)
json.dump(dict(git_commit_at_generation=commit, n_runs=len(runs), split_rules=dict(main_stack='train/test by gold-product component (union-find over shared gold products), md5 of component < TEST_FRAC; clean calibration half md5(cal|bid) < 0.5',
               second_stack='50/50 by md5(port2|dataset|query id)', mutants='halves by first hex digit of md5(point id)', faults_and_probes='random tags dict / deveval / heldout per v15 protocol'),
               runs=runs), open(out, 'w'), indent=1)
print('runs', len(runs), 'files', sum(len(r['files']) for r in runs))
