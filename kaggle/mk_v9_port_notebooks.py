"""Build the two v9 Kaggle notebooks (docs/evidence/v9_protocol.md): kaggle/DiagRAG_v9_port_nfcorpus.ipynb and kaggle/DiagRAG_v9_port_arguana.ipynb.
Each embeds (gzip+base64) the FROZEN kaggle/diagrag_port3.py, checks its SHA-256 against the value written here AND against the value in the v9 protocol, writes it to disk and runs it with the
pre-registered settings. Nothing about the code comes from the network except the BEIR zip and Webis zip, both SHA-256 checked inside the script.
usage: python kaggle/mk_v9_port_notebooks.py"""
import base64, gzip, hashlib, json, os, re

here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
raw = open(os.path.join(here, 'diagrag_port3.py'), 'rb').read(); SHA = hashlib.sha256(raw).hexdigest(); B64 = base64.b64encode(gzip.compress(raw, 9, mtime=0)).decode()
proto = open(os.path.join(root, 'docs', 'evidence', 'v9_protocol.md'), encoding='utf-8').read(); m = re.findall(r'frozen port3 hash is `([0-9a-f]{64})`', proto)
assert m and m[-1] == SHA, 'diagrag_port3.py differs from the hash written in docs/evidence/v9_protocol.md'
RUNS = {'nfcorpus': dict(seed='53', title='NFCorpus (medical)'), 'arguana': dict(seed='54', title='ArguAna (argument retrieval)')}
lines = lambda s: s.strip('\n').splitlines(True)
md = lambda t: dict(cell_type='markdown', metadata={}, source=lines(t)); code = lambda t: dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=lines(t))
EMBED = 'EMBED = dict(sha256=%r, size=%d, b64=(\n' % (SHA, len(raw)) + ''.join(f'    {B64[i:i + 100]!r}\n' for i in range(0, len(B64), 100)) + '))\n'
for ds, r in RUNS.items():
    cells = [
        md(f'''
# DiagRAG v9 port arm: {r['title']}, seed {r['seed']}

Runs the frozen `diagrag_port3.py` (SHA-256 `{SHA}`) on BEIR **{ds}** with the settings pre-registered in `docs/evidence/v9_protocol.md`. Kaggle **GPU T4 x1** (or CPU), **Internet On**, Run All.
The gates are port2's, unchanged: a fault passes only if its held-out one-vs-rest AUROC >= 0.70 with >= 20 held-out positives AND its repair has >= 20 hard episodes, a Wilson 95% lower bound >= 0.50 and loses <= 10% of clean successes.
"The suite ports" is claimed only if >= 15 of the 20 ported faults pass both gates. Every fault is reported whichever way it falls. Do not change `SEED` or any setting to shop for a result.
The faults are injected by the project's authors; the code was written by Claude (Anthropic) under the owner's direction. Disclose that in any paper.
'''),
        code(f'''
# 1. Pre-registered configuration (docs/evidence/v9_protocol.md). One run per corpus.
import os
CONFIG = dict(DATASET={ds!r}, SEED={r['seed']!r}, N_QUERIES='2500', N_HARD='50', MAX_ATT='2500', N_HARM='20', TIME_BUDGET='36000')
os.environ.update(CONFIG); print(CONFIG)
'''),
        code('# 2. Embedded, hash-pinned code.\n' + EMBED),
        code(f'''
# 3. Write the embedded file and verify its SHA-256.
import base64, gzip, hashlib
ON_KAGGLE = os.path.exists('/kaggle/working'); CODE_DIR = '/kaggle/working/code' if ON_KAGGLE else os.path.join(os.getcwd(), 'code'); os.makedirs(CODE_DIR, exist_ok=True)
data = gzip.decompress(base64.b64decode(''.join(EMBED['b64'])))
assert len(data) == EMBED['size'] and hashlib.sha256(data).hexdigest() == EMBED['sha256'] == {SHA!r}, 'embedded code is not the frozen port3 file'
open(os.path.join(CODE_DIR, 'diagrag_port3.py'), 'wb').write(data); print('ok diagrag_port3.py', EMBED['sha256'])
'''),
        code('''
# 4. Run. runpy sets __file__, so PORT_PROTOCOL.json records the hash of the pinned file. If the session stops, run again with this output attached: it resumes from its checkpoint.
import runpy, sys
WORK = '/kaggle/working' if ON_KAGGLE else os.getcwd(); os.environ['DIAGRAG_WORK'] = WORK
os.environ.setdefault('NLTK_DATA', os.path.join(WORK, 'nltk_data')); os.makedirs(os.environ['NLTK_DATA'], exist_ok=True)
try: runpy.run_path(os.path.join(CODE_DIR, 'diagrag_port3.py'), run_name='__main__')
except SystemExit as e: print('stopped with SystemExit', e.code, '- if TIME_BUDGET was reached, run again to resume')
'''),
        code(f'''
# 5. Headline. Every fault is in port_solved.csv, pass or fail.
import json, glob
OUT = os.path.join(WORK, 'port3_{ds}_out')
vp = os.path.join(OUT, 'PORT_VERDICT.json')
if os.path.exists(vp):
    V = json.load(open(vp)); print({{k: V[k] for k in ('domain', 'clean_hit5', 'detectors_pass', 'repairs_pass', 'solved_both', 'of', 'suite_ports', 'not_solved') if k in V}})
    P = json.load(open(os.path.join(OUT, 'PORT_PROTOCOL.json'))); print('device', P.get('device'), '| code hash in protocol', P.get('code_sha256'))
else: print('no PORT_VERDICT.json yet: run again to resume')
'''),
    ]
    nb = dict(nbformat=4, nbformat_minor=5, cells=cells, metadata=dict(kernelspec=dict(name='python3', display_name='Python 3', language='python'), language_info=dict(name='python'),
                                                                          kaggle=dict(accelerator='gpu', isInternetEnabled=True)))
    out = os.path.join(here, f'DiagRAG_v9_port_{ds}.ipynb'); json.dump(nb, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); print('wrote', out, os.path.getsize(out), 'bytes')
