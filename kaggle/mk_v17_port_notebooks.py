"""Build the v14 E4/E4b notebooks (docs/evidence/v14_flagship_protocol.md): kaggle/DiagRAG_v14_port_{trial_fiqa,judged_fiqa,judged_nq}.ipynb.
Each runs the frozen docs/evidence/v14_port_guarantee.py on the judged port5 run of its corpus (attached kernel output: checkpoint, embeddings, protocol, detector gates)
with the byte-identical data zips (attached dataset). usage: python kaggle/mk_v14_port_notebooks.py"""
import base64, gzip, hashlib, json, os
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
F = {'v17_port_selftest.py': os.path.join(root, 'docs', 'evidence', 'v17_port_selftest.py'), 'diagrag_port5.py': os.path.join(here, 'diagrag_port5.py')}
E = {n: (lambda b: dict(sha256=hashlib.sha256(b).hexdigest(), b64=base64.b64encode(gzip.compress(b, 9, mtime=0)).decode()))(open(p, 'rb').read()) for n, p in F.items()}
assert E['diagrag_port5.py']['sha256'] == '916c3864282b1d9c168cce6943340b52d8728334c3c960d33fcb0d2d4224294f'
lines = lambda s: s.strip('\n').splitlines(True); code = lambda t: dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=lines(t))
emb = 'EMB = {\n' + ''.join(f"    {n!r}: dict(sha256={e['sha256']!r}, b64=(\n" + ''.join(f"        {e['b64'][i:i + 100]!r}\n" for i in range(0, len(e['b64']), 100)) + "    )),\n" for n, e in E.items()) + '}\n'
for name, ds, trial, role in [('trial_fiqa', 'fiqa', 1, 'dev'), ('dev_fiqa', 'fiqa', 0, 'dev'), ('heldout_nq', 'nq', 0, 'heldout')]:
    cells = [dict(cell_type='markdown', metadata={}, source=lines(f"# DiagRAG v17 self-test on the second stack, {ds}, role {role} ({'TRIAL: numbers are not results' if trial else 'JUDGED RUN'})\n\nFrozen `v17_port_selftest.py` and frozen `diagrag_port5.py`, replaying the judged port5 {ds} run. See `docs/evidence/v17_port_selftest_protocol.md`. No API key.")),
             code(emb + f"""
import os, gzip, base64, hashlib, glob, shutil, subprocess, sys, json
CODE = '/kaggle/working/code'; os.makedirs(CODE, exist_ok=True)
for n, e in EMB.items():
    raw = gzip.decompress(base64.b64decode(''.join(e['b64']))); assert hashlib.sha256(raw).hexdigest() == e['sha256']; open(os.path.join(CODE, n), 'wb').write(raw); print('ok', n, e['sha256'][:16])
os.makedirs('/tmp/diagrag_port_data', exist_ok=True)
for b in glob.glob('/kaggle/input/**/*.zip.bin', recursive=True): shutil.copy(b, os.path.join('/tmp/diagrag_port_data', os.path.basename(b)[:-4])); print('staged', b)
src = [os.path.dirname(p) for p in glob.glob('/kaggle/input/**/port5_{ds}_out/checkpoint.pkl', recursive=True)]; assert src, 'judged {ds} output not attached'
OUTD = '/kaggle/working/port5_{ds}_out'; os.makedirs(OUTD, exist_ok=True)
for n in ('checkpoint.pkl', 'corpus_e5.npy', 'PORT_PROTOCOL.json', 'port_detector_gates.csv', 'PORT_VERDICT.json'):
    d = os.path.join(OUTD, n)
    if not os.path.exists(d): os.symlink(os.path.join(src[0], n), d)
P = json.load(open(os.path.join(OUTD, 'PORT_PROTOCOL.json'))); assert P['code_sha256'] == EMB['diagrag_port5.py']['sha256'] and P['cfg']['DATASET'] == '{ds}'; print('judged {ds} run, seed', P['cfg']['SEED'])
"""),
             code(f"""
env = dict(os.environ, DATASET='{ds}', NLTK_DATA='/kaggle/working/nltk_data')
r = subprocess.run([sys.executable, os.path.join(CODE, 'v17_port_selftest.py'), '/kaggle/working', os.path.join(CODE, 'diagrag_port5.py'), '/kaggle/working/v17_portS_{ds}_out', '{role}', '{trial}'], env=env, capture_output=True, text=True)
print(r.stdout[-15000:]); print(r.stderr[-6000:]); assert r.returncode == 0
"""),
             code("import resource; print('peak RSS children (GB):', round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024**2, 2))")]
    nb = dict(nbformat=4, nbformat_minor=5, cells=cells, metadata=dict(kernelspec=dict(name='python3', display_name='Python 3', language='python'), language_info=dict(name='python'), kaggle=dict(accelerator='gpu', isInternetEnabled=True)))
    json.dump(nb, open(os.path.join(here, f'DiagRAG_v17_port_{name}.ipynb'), 'w'), indent=1); print('wrote', name)
print('v17_port_selftest.py sha256', E['v17_port_selftest.py']['sha256'])
