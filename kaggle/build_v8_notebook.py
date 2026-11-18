"""Embed the frozen v8 runner in a self-contained Kaggle notebook."""
import base64, gzip, hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(HERE, 'diagrag_v8.py')
raw = open(script_path, 'rb').read()
digest = hashlib.sha256(raw).hexdigest()
b64 = base64.b64encode(gzip.compress(raw, 9, mtime=0)).decode()
lines = lambda text: text.strip('\n').splitlines(True)
def md(text): return dict(cell_type='markdown', metadata={}, source=lines(text))
def code(text): return dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=lines(text))
embed = 'EMBED = dict(sha256=' + repr(digest) + ', size=' + str(len(raw)) + ', b64=(\n' + ''.join(
    '    ' + repr(b64[i:i+100]) + '\n' for i in range(0, len(b64), 100)) + '))\n'
cells = [
    md(f'''# DiagRAG v8 multi-label study (seed 52)

Frozen runner SHA-256: `{digest}`. This notebook runs the preregistered v8 runner from a hash-checked embedded copy. The protocol is in `docs/evidence/v8_multilabel_protocol.md`.

Use Kaggle CPU with Internet enabled. The runner pins the CPU reranker used by the v7 CPU baseline, fetches the public inputs and validates their byte lengths and SHA-256 hashes, then writes resumable state and results under `diagrag_v8_out/`. Do not change seeds, quotas, thresholds, or the sample after the run starts. If a session reaches its time budget, rerun this notebook with its prior output attached so it resumes from `checkpoint.pkl`.

The protocol was frozen before any v8 judged result. No Kaggle or language-model credentials are embedded in this notebook.'''),
    code('''# Fixed full-run configuration. Credential values must be entered through Kaggle Secrets if any future stage requires them; this runner makes no LLM API calls.
import os
CONFIG = dict(SEED='50', RERANKER='BAAI/bge-reranker-base', N_BASE_ESCI='6000', N_PRDC='528', N_HARD='100', MAX_ATT='4000', N_HARM='20', TIME_BUDGET='30000')
os.environ.update(CONFIG)
print(CONFIG)
'''),
    code(' # Embedded hash-pinned runner.\n' + embed),
    code(f'''import base64, gzip, hashlib, os, runpy
ON_KAGGLE = os.path.exists('/kaggle/working')
WORK = '/kaggle/working' if ON_KAGGLE else os.getcwd()
CODE_DIR = os.path.join(WORK, 'diagrag_v8_code')
os.makedirs(CODE_DIR, exist_ok=True)
raw = gzip.decompress(base64.b64decode(''.join(EMBED['b64'])))
assert len(raw) == EMBED['size'] and hashlib.sha256(raw).hexdigest() == EMBED['sha256'] == '{digest}'
script = os.path.join(CODE_DIR, 'diagrag_v8.py')
open(script, 'wb').write(raw)
print('verified runner', len(raw), 'bytes', EMBED['sha256'])
runpy.run_path(script, run_name='__main__')
'''),
    code('''import json, os
OUT = os.path.join(WORK, 'diagrag_v8_out')
result = os.path.join(OUT, 'COMPOSED_RESULT.json')
if os.path.exists(result):
    R = json.load(open(result, encoding='utf-8'))
    print(R.get('headline', 'Result headline unavailable'))
    print('tau2:', R.get('tau2'), '| clean sample:', R.get('clean_loss', {}).get('sequential_loop_subsample', {}).get('n'))
else:
    print('Run paused or incomplete. Attach this output and run again to resume. No held-out conclusion is available yet.')
''')]
nb = dict(nbformat=4, nbformat_minor=5, cells=cells,
          metadata=dict(kernelspec=dict(name='python3', display_name='Python 3', language='python'), language_info=dict(name='python'),
                        kaggle=dict(accelerator='none', isInternetEnabled=True)))
out = os.path.join(HERE, 'DiagRAG_v8_kaggle.ipynb')
json.dump(nb, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote', out, os.path.getsize(out), 'bytes', hashlib.sha256(open(out, 'rb').read()).hexdigest())
