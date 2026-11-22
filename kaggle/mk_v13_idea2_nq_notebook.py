"""Build kaggle/DiagRAG_v13_idea2_nq.ipynb: runs the frozen docs/evidence/v13_idea2.py (D2) on the held-out split of the v13 judged NQ run, on Kaggle.
Attaches the NQ data dataset (byte-identical zips) and the judged-NQ kernel output (checkpoint + embeddings). usage: python kaggle/mk_v13_idea2_nq_notebook.py"""
import base64, gzip, hashlib, json, os
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
F = {'v13_idea2.py': os.path.join(root, 'docs', 'evidence', 'v13_idea2.py'), 'diagrag_port5.py': os.path.join(here, 'diagrag_port5.py')}
E = {n: (lambda b: dict(sha256=hashlib.sha256(b).hexdigest(), b64=base64.b64encode(gzip.compress(b, 9, mtime=0)).decode()))(open(p, 'rb').read()) for n, p in F.items()}
assert E['v13_idea2.py']['sha256'].startswith('8da2c1627e5a2f79') and E['diagrag_port5.py']['sha256'].startswith('916c3864')
lines = lambda s: s.strip('\n').splitlines(True); code = lambda t: dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=lines(t))
emb = 'EMB = {\n' + ''.join(f"    {n!r}: dict(sha256={e['sha256']!r}, b64=(\n" + ''.join(f"        {e['b64'][i:i + 100]!r}\n" for i in range(0, len(e['b64']), 100)) + "    )),\n" for n, e in E.items()) + '}\n'
cells = [dict(cell_type='markdown', metadata={}, source=lines('# DiagRAG v13 Idea 1 + 2 on NQ (held-out, judged run seed 58)\n\nFrozen `v13_idea2.py` (D2) and frozen `diagrag_port5.py`. See `docs/evidence/v13_idea2_protocol.md` A1. No API key.')),
         code(emb + """
import os, gzip, base64, hashlib, glob, shutil, subprocess, sys
CODE = '/kaggle/working/code'; os.makedirs(CODE, exist_ok=True)
for n, e in EMB.items():
    raw = gzip.decompress(base64.b64decode(''.join(e['b64']))); assert hashlib.sha256(raw).hexdigest() == e['sha256']; open(os.path.join(CODE, n), 'wb').write(raw); print('ok', n, e['sha256'][:16])
os.makedirs('/tmp/diagrag_port_data', exist_ok=True)
for b in glob.glob('/kaggle/input/**/*.zip.bin', recursive=True): shutil.copy(b, os.path.join('/tmp/diagrag_port_data', os.path.basename(b)[:-4])); print('staged', b)
src = [os.path.dirname(p) for p in glob.glob('/kaggle/input/**/port5_nq_out/checkpoint.pkl', recursive=True)]; assert src, 'judged NQ output not attached'
OUTD = '/kaggle/working/port5_nq_out'; os.makedirs(OUTD, exist_ok=True)
for n in ('checkpoint.pkl', 'corpus_e5.npy', 'PORT_PROTOCOL.json'):
    d = os.path.join(OUTD, n)
    if not os.path.exists(d): os.symlink(os.path.join(src[0], n), d)
import json; P = json.load(open(os.path.join(OUTD, 'PORT_PROTOCOL.json'))); assert P['cfg']['SEED'] == 58 and P['code_sha256'].startswith('916c3864'), P['cfg']['SEED']; print('judged NQ run, seed', P['cfg']['SEED'])
"""),
         code("""
env = dict(os.environ, DATASET='nq', NLTK_DATA='/kaggle/working/nltk_data')
r = subprocess.run([sys.executable, os.path.join(CODE, 'v13_idea2.py'), '/kaggle/working', os.path.join(CODE, 'diagrag_port5.py'), 'test', '/kaggle/working/idea2_nq_test.jsonl'], env=env, capture_output=True, text=True)
print(r.stdout[-6000:]); print(r.stderr[-4000:]); assert r.returncode == 0
"""),
         code("import resource; print('peak RSS children (GB):', round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024**2, 2))")]
nb = dict(nbformat=4, nbformat_minor=5, cells=cells, metadata=dict(kernelspec=dict(name='python3', display_name='Python 3', language='python'), language_info=dict(name='python'), kaggle=dict(accelerator='gpu', isInternetEnabled=True)))
json.dump(nb, open(os.path.join(here, 'DiagRAG_v13_idea2_nq.ipynb'), 'w'), indent=1); print('wrote DiagRAG_v13_idea2_nq.ipynb')
