"""Build the v13 port notebooks (docs/evidence/v13_datasets.md). Each embeds the FROZEN kaggle/diagrag_port5.py, checks its SHA-256 against this file AND against the dataset freeze,
and runs it with the settings of its row. Trial and judged notebooks differ ONLY in the configuration cell. A last cell reports peak memory and disk use. No API key appears anywhere.
usage: python kaggle/mk_v13_port_notebooks.py"""
import base64, gzip, hashlib, json, os, re

here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
raw = open(os.path.join(here, 'diagrag_port5.py'), 'rb').read(); SHA = hashlib.sha256(raw).hexdigest(); B64 = base64.b64encode(gzip.compress(raw, 9, mtime=0)).decode()
m = re.findall(r'frozen port5 hash is `([0-9a-f]{64})`', open(os.path.join(root, 'docs', 'evidence', 'v13_datasets.md'), encoding='utf-8').read())
assert m and m[-1] == SHA, 'diagrag_port5.py differs from the hash frozen in docs/evidence/v13_datasets.md'
TRIAL = dict(N_QUERIES='120', N_HARD='3', MAX_ATT='60', N_HARM='3', TIME_BUDGET='36000')
RUNS = {'v13_trial_nq': dict(DATASET='nq', SEED='906', **TRIAL), 'v13_trial_fiqa': dict(DATASET='fiqa', SEED='907', **TRIAL)}
JUDGED = dict(N_QUERIES='2500', N_HARD='50', MAX_ATT='2500', N_HARM='20', TIME_BUDGET='36000')   # = judged port2 settings (docs/evidence/v13_judged_ports_protocol.md)
RUNS.update({'v13_judged_nq': dict(DATASET='nq', SEED='58', **JUDGED), 'v13_judged_fiqa': dict(DATASET='fiqa', SEED='60', **JUDGED)})
lines = lambda s: s.strip('\n').splitlines(True)
md = lambda t: dict(cell_type='markdown', metadata={}, source=lines(t)); code = lambda t: dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=lines(t))
EMBED = 'EMBED = dict(sha256=%r, size=%d, b64=(\n' % (SHA, len(raw)) + ''.join(f'    {B64[i:i + 100]!r}\n' for i in range(0, len(B64), 100)) + '))\n'
for name, cfg in RUNS.items():
    trial = 'trial' in name
    cells = [
        md(f"# DiagRAG {name}: {'TRIAL (development seed, tiny query settings; numbers are not results)' if trial else 'JUDGED RUN'} on BEIR {cfg['DATASET']}\n\nFrozen `diagrag_port5.py` (SHA-256 `{SHA}`). GPU T4, Internet On, Run All. No API key is used."),
        code('import os\nCONFIG = ' + repr(cfg) + '\nos.environ.update(CONFIG); print(CONFIG)'),
        code('# Embedded, hash-pinned code.\n' + EMBED),
        code(f"""
import base64, gzip, hashlib
ON_KAGGLE = os.path.exists('/kaggle/working'); CODE_DIR = '/kaggle/working/code' if ON_KAGGLE else os.path.join(os.getcwd(), 'code'); os.makedirs(CODE_DIR, exist_ok=True)
data = gzip.decompress(base64.b64decode(''.join(EMBED['b64'])))
assert len(data) == EMBED['size'] and hashlib.sha256(data).hexdigest() == EMBED['sha256'] == {SHA!r}, 'embedded code is not the frozen port5 file'
open(os.path.join(CODE_DIR, 'diagrag_port5.py'), 'wb').write(data); print('ok diagrag_port5.py', EMBED['sha256'])
"""),
        code("""
# Data staging (outside the frozen code). The BEIR download server was unreachable on 19 Nov 2026, so the byte-identical zips are attached as a private Kaggle
# dataset with a .bin suffix (Kaggle unpacks .zip uploads). They are copied to the path the frozen code expects; the frozen code then checks their exact size
# and SHA-256 itself before use, so a wrong file stops the run. If no attached copy exists, the frozen code downloads from BEIR as before.
import glob, shutil
os.makedirs('/tmp/diagrag_port_data', exist_ok=True)
for b in glob.glob('/kaggle/input/**/*.zip.bin', recursive=True):
    dst = os.path.join('/tmp/diagrag_port_data', os.path.basename(b)[:-4]); shutil.copy(b, dst); print('staged', dst, os.path.getsize(dst))
"""),
    ] + ([code("""
# Embedding reuse (outside the frozen code; declared in docs/evidence/v13_judged_ports_protocol.md section 3). Corpus embeddings do not depend on the seed.
# ONLY corpus_e5.npy from the NQ trial output is copied; its checkpoint is NOT copied, and the assert below makes sure none is present.
import glob, shutil, numpy as np
OUTD = '/kaggle/working/port5_nq_out'; os.makedirs(OUTD, exist_ok=True)
src = glob.glob('/kaggle/input/**/port5_nq_out/corpus_e5.npy', recursive=True)
if src and not os.path.exists(os.path.join(OUTD, 'corpus_e5.npy')):
    E_ = np.load(src[0], mmap_mode='r'); assert E_.shape == (2681468, 384) and E_.dtype == np.float32, E_.shape
    nr = np.linalg.norm(np.asarray(E_[::10007]), axis=1); assert float(abs(nr - 1).max()) < 1e-3; del E_
    shutil.copy(src[0], os.path.join(OUTD, 'corpus_e5.npy')); print('reused corpus embeddings from', src[0])
else: print('no reusable embeddings found: the frozen code will embed the corpus')
assert not os.path.exists(os.path.join(OUTD, 'checkpoint.pkl')), 'a checkpoint must not be present before the judged run'
""")] if name == 'v13_judged_nq' else []) + [
        code("""
import runpy, time
WORK = '/kaggle/working' if ON_KAGGLE else os.getcwd(); os.environ['DIAGRAG_WORK'] = WORK
os.environ.setdefault('NLTK_DATA', os.path.join(WORK, 'nltk_data')); os.makedirs(os.environ['NLTK_DATA'], exist_ok=True)
T_START = time.time()
try: runpy.run_path(os.path.join(CODE_DIR, 'diagrag_port5.py'), run_name='__main__')
except SystemExit as e: print('stopped with SystemExit', e.code)
print('wall time (s):', round(time.time() - T_START))
"""),
        code(f"""
# Resource report (outside the frozen code): peak memory of this process, machine memory, disk used by the outputs.
import resource, json, shutil, subprocess
print('peak RSS (GB):', round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**2, 2))
print([l for l in open('/proc/meminfo') if l.startswith(('MemTotal', 'MemAvailable'))])
OUT = os.path.join(WORK, 'port5_{cfg['DATASET']}_out'); print(subprocess.run(['du', '-sh', OUT], capture_output=True, text=True).stdout)
vp = os.path.join(OUT, 'PORT_VERDICT.json')
if os.path.exists(vp):
    V = json.load(open(vp)); print({{k: V[k] for k in ('domain', 'clean_hit5', 'detectors_pass', 'repairs_pass', 'solved_both', 'of', 'suite_ports') if k in V}})
    print('code hash in protocol:', json.load(open(os.path.join(OUT, 'PORT_PROTOCOL.json'))).get('code_sha256'))
else: print('no PORT_VERDICT.json: the run did not finish')
"""),
    ]
    nb = dict(nbformat=4, nbformat_minor=5, cells=cells, metadata=dict(kernelspec=dict(name='python3', display_name='Python 3', language='python'), language_info=dict(name='python'),
                                                                          kaggle=dict(accelerator='gpu', isInternetEnabled=True)))
    p = os.path.join(here, f'DiagRAG_{name}.ipynb'); json.dump(nb, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); print('wrote', p)
