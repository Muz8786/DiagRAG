"""Build kaggle/DiagRAG_v20_<name>.ipynb (docs/evidence/v20_protocol.md): CPU notebooks that run the frozen v20_ablation.py on every attached judged run.
usage: python kaggle/mk_v20_notebooks.py"""
import base64, gzip, hashlib, json, os
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
F = {'v20_ablation.py': os.path.join(root, 'docs', 'evidence', 'v20_ablation.py'), 'v20_feature_manifest.json': os.path.join(root, 'docs', 'evidence', 'v20_feature_manifest.json')}
E = {n: (lambda b: dict(sha256=hashlib.sha256(b).hexdigest(), b64=base64.b64encode(gzip.compress(b, 9, mtime=0)).decode()))(open(p, 'rb').read()) for n, p in F.items()}
lines = lambda s: s.strip('\n').splitlines(True); code = lambda t: dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=lines(t))
emb = 'EMB = {\n' + ''.join(f"    {n!r}: dict(sha256={e['sha256']!r}, b64=(\n" + ''.join(f"        {e['b64'][i:i + 100]!r}\n" for i in range(0, len(e['b64']), 100)) + "    )),\n" for n, e in E.items()) + '}\n'
for name, lomo in [('acc2', ['71']), ('acc3', ['72']), ('acc4', ['73']), ('desc', [])]:
    cells = [dict(cell_type='markdown', metadata={}, source=lines(f"# DiagRAG v20 ablations and baselines ({name})\n\nFrozen `v20_ablation.py` on every attached judged run (saved episodes only, no retrieval). CPU. See `docs/evidence/v20_protocol.md`.")),
             code(emb + f"""
import os, gzip, base64, hashlib, glob, json, subprocess, sys
CODE = '/kaggle/working/code'; os.makedirs(CODE, exist_ok=True)
for n, e in EMB.items():
    raw = gzip.decompress(base64.b64decode(''.join(e['b64']))); assert hashlib.sha256(raw).hexdigest() == e['sha256']; open(os.path.join(CODE, n), 'wb').write(raw); print('ok', n, e['sha256'][:16])
runs = sorted({{os.path.dirname(p) for p in glob.glob('/kaggle/input/**/episodes.jsonl', recursive=True)}})
LOMO = {lomo!r}
for d in runs:
    P = json.load(open(glob.glob(os.path.join(d, '*PROTOCOL.json'))[0])); s = str(P['cfg']['SEED']); print('run', d, 'seed', s, 'code', str(P.get('code_sha256'))[:12])
    args = [sys.executable, os.path.join(CODE, 'v20_ablation.py'), d, '/kaggle/working/v20_out', os.path.join(CODE, 'v20_feature_manifest.json')] + (['--lomo'] if s in LOMO else [])
    r = subprocess.run(args, capture_output=True, text=True); print(r.stdout[-6000:]); print(r.stderr[-3000:])
"""), code("print(sorted(os.listdir('/kaggle/working/v20_out')))")]
    nb = dict(nbformat=4, nbformat_minor=5, cells=cells, metadata=dict(kernelspec=dict(name='python3', display_name='Python 3', language='python'), language_info=dict(name='python'), kaggle=dict(accelerator='none', isInternetEnabled=False)))
    json.dump(nb, open(os.path.join(here, f'DiagRAG_v20_{name}.ipynb'), 'w'), indent=1); print('wrote', name)
print('v20_ablation.py sha256', E['v20_ablation.py']['sha256'])
