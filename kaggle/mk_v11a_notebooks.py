"""Build the two v11.a Kaggle notebooks (docs/evidence/v11_protocol.md): kaggle/DiagRAG_v11a_main.ipynb (frozen v6 code, seed 55) and kaggle/DiagRAG_v11a_port_scidocs.ipynb (frozen port4 code, seed 56).
No API key appears anywhere. The main notebook is DiagRAG_v6_kaggle.ipynb with ONLY the seed and the labels changed (each replacement asserted); the port notebook is built like the v9 port notebooks.
usage: python kaggle/mk_v11a_notebooks.py"""
import base64, gzip, hashlib, json, os, re

here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here); proto = open(os.path.join(root, 'docs', 'evidence', 'v11_protocol.md'), encoding='utf-8').read()
lines = lambda s: s.strip('\n').splitlines(True)
md = lambda t: dict(cell_type='markdown', metadata={}, source=lines(t)); code = lambda t: dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=lines(t))
META = dict(kernelspec=dict(name='python3', display_name='Python 3', language='python'), language_info=dict(name='python'), kaggle=dict(accelerator='gpu', isInternetEnabled=True))

# ---- R1: main notebook = the v6 notebook with the seed and labels changed
nb = json.load(open(os.path.join(here, 'DiagRAG_v6_kaggle.ipynb'), encoding='utf-8')); orig_embed = ''.join(nb['cells'][2]['source'])
REPL = [("CONFIG = dict(SEED='50',", "CONFIG = dict(SEED='55',", 1),
        ("# DiagRAG v6 on Kaggle: one file, the pre-registered judged run (seed 50)", "# DiagRAG v11.a main run on Kaggle: the frozen v6 code on a fresh seed (seed 55), pre-registered in docs/evidence/v11_protocol.md", 1),
        ("These are the pre-registered v6 settings (seed 50, docs/evidence/v6_protocol.md section 3). The protocol allows ONE GPU run and ONE CPU replication at seed 50; do not change SEED to shop for a verdict.",
         "These are the v6 settings with ONE change, the seed (55), pre-registered in docs/evidence/v11_protocol.md sections 1 and 2. One GPU run at seed 55, read together with seeds 50 and 52; do not change SEED to shop for a verdict.", 1)]
for old, new, want in REPL:
    n = 0
    for c in nb['cells']:
        s = ''.join(c['source'])
        if old in s: n += s.count(old); c['source'] = s.replace(old, new).splitlines(True)
    assert n == want, f'replacement {old[:50]!r}: expected {want}, found {n}'
assert ''.join(nb['cells'][2]['source']) == orig_embed, 'embedded code blobs changed'
assert "SEED='55'" in ''.join(nb['cells'][1]['source']) and "SEED='50'" not in ''.join(nb['cells'][1]['source'])
json.dump(nb, open(os.path.join(here, 'DiagRAG_v11a_main.ipynb'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ---- R2: port notebook on SCIDOCS
raw = open(os.path.join(here, 'diagrag_port4.py'), 'rb').read(); SHA = hashlib.sha256(raw).hexdigest(); B64 = base64.b64encode(gzip.compress(raw, 9, mtime=0)).decode()
m = re.findall(r'frozen port4 hash is `([0-9a-f]{64})`', proto); assert m and m[-1] == SHA, 'diagrag_port4.py differs from the hash in docs/evidence/v11_protocol.md'
EMBED = 'EMBED = dict(sha256=%r, size=%d, b64=(\n' % (SHA, len(raw)) + ''.join(f'    {B64[i:i + 100]!r}\n' for i in range(0, len(B64), 100)) + '))\n'
cells = [
    md(f'''
# DiagRAG v11.a port arm: BEIR SCIDOCS (scientific citation prediction), seed 56

Runs the frozen `diagrag_port4.py` (SHA-256 `{SHA}`) on BEIR **scidocs** with the settings pre-registered in `docs/evidence/v11_protocol.md`. Kaggle **GPU T4 x1**, **Internet On**, Run All. No API key is used.
Gates are port2's, unchanged: a fault is solved only if its held-out detector AUROC >= 0.70 with >= 20 held-out positives AND its repair has >= 20 hard episodes, a Wilson 95% lower bound >= 0.50 and loses <= 10% of clean successes.
THIN or untrained counts as not solved. "The suite ports" is claimed only if >= 15 of the 20 faults are solved. Do not change `SEED` or any setting to shop for a result.
Faults are injected by the project's authors; the code was written by Claude (Anthropic) under the owner's direction. Disclose that in any paper.
'''),
    code('''
# 1. Pre-registered configuration (docs/evidence/v11_protocol.md). One run.
import os
CONFIG = dict(DATASET='scidocs', SEED='56', N_QUERIES='2500', N_HARD='50', MAX_ATT='2500', N_HARM='20', TIME_BUDGET='36000')
os.environ.update(CONFIG); print(CONFIG)
'''),
    code('# 2. Embedded, hash-pinned code.\n' + EMBED),
    code(f'''
# 3. Write the embedded file and verify its SHA-256.
import base64, gzip, hashlib
ON_KAGGLE = os.path.exists('/kaggle/working'); CODE_DIR = '/kaggle/working/code' if ON_KAGGLE else os.path.join(os.getcwd(), 'code'); os.makedirs(CODE_DIR, exist_ok=True)
data = gzip.decompress(base64.b64decode(''.join(EMBED['b64'])))
assert len(data) == EMBED['size'] and hashlib.sha256(data).hexdigest() == EMBED['sha256'] == {SHA!r}, 'embedded code is not the frozen port4 file'
open(os.path.join(CODE_DIR, 'diagrag_port4.py'), 'wb').write(data); print('ok diagrag_port4.py', EMBED['sha256'])
'''),
    code('''
# 4. Run. If the session stops, run again with this output attached: it resumes from its checkpoint.
import runpy, sys
WORK = '/kaggle/working' if ON_KAGGLE else os.getcwd(); os.environ['DIAGRAG_WORK'] = WORK
os.environ.setdefault('NLTK_DATA', os.path.join(WORK, 'nltk_data')); os.makedirs(os.environ['NLTK_DATA'], exist_ok=True)
try: runpy.run_path(os.path.join(CODE_DIR, 'diagrag_port4.py'), run_name='__main__')
except SystemExit as e: print('stopped with SystemExit', e.code, '- if TIME_BUDGET was reached, run again to resume')
'''),
    code('''
# 5. Headline. Every fault is in port_solved.csv, pass or fail.
import json
OUT = os.path.join(WORK, 'port4_scidocs_out'); vp = os.path.join(OUT, 'PORT_VERDICT.json')
if os.path.exists(vp):
    V = json.load(open(vp)); print({k: V[k] for k in ('domain', 'clean_hit5', 'detectors_pass', 'repairs_pass', 'solved_both', 'of', 'suite_ports', 'not_solved') if k in V})
    P = json.load(open(os.path.join(OUT, 'PORT_PROTOCOL.json'))); print('device', P.get('device'), '| code hash in protocol', P.get('code_sha256'))
else: print('no PORT_VERDICT.json yet: run again to resume')
'''),
]
json.dump(dict(nbformat=4, nbformat_minor=5, cells=cells, metadata=META), open(os.path.join(here, 'DiagRAG_v11a_port_scidocs.ipynb'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote DiagRAG_v11a_main.ipynb and DiagRAG_v11a_port_scidocs.ipynb')
