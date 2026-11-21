"""Build kaggle/DiagRAG_v5_kaggle.ipynb: ONE self-contained Kaggle notebook that runs the frozen, hash-pinned
diagrag_v5.py with the v5 judged GPU configuration (seed 49), then runs the pre-registered GPU analysis. The expected hash is read from the LAST
"the frozen v5 hash is now" line of docs/evidence/v5_protocol.md, so the notebook cannot drift from the pre-registration.

The notebook embeds (gzip+base64) diagrag_v5.py, natural_exclusions_v2.json and docs/evidence/analysis_gpu_plan.py.
It checks each against a SHA-256 written into the notebook, writes them to disk and runs the script with runpy, so the
JUDGED_PROTOCOL.json it writes carries the same code hash as the judged run. Nothing about the code comes from the network.

Usage: python kaggle/build_final_notebook.py"""
import base64, gzip, hashlib, json, os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
PARTS = [
    ('diagrag_v5.py', os.path.join(here, 'diagrag_v5.py')),
    ('natural_exclusions_v2.json', os.path.join(here, 'natural_exclusions_v2.json')),
    ('analysis_gpu_plan.py', os.path.join(root, 'docs', 'evidence', 'analysis_gpu_plan.py')),
]
import re
_m = re.findall(r'frozen v5 hash is now `([0-9a-f]{64})`', open(os.path.join(root, 'docs', 'evidence', 'v5_protocol.md'), encoding='utf-8').read())
assert _m, 'no frozen v5 hash in the protocol'
EXPECT_V4 = _m[-1]   # (name kept for the shared code below) the hash frozen in the protocol before any v5 result existed


def blob(path):
    raw = open(path, 'rb').read()
    return hashlib.sha256(raw).hexdigest(), len(raw), base64.b64encode(gzip.compress(raw, 9, mtime=0)).decode()


parts = {name: blob(p) for name, p in PARTS}
assert parts['diagrag_v5.py'][0] == EXPECT_V4, 'diagrag_v5.py differs from the hash frozen in the protocol'
lines = lambda s: s.strip('\n').splitlines(True)


def md(text): return dict(cell_type='markdown', metadata={}, source=lines(text))
def code(text): return dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=lines(text))


EMBED = 'EMBED = {\n' + ''.join(
    f"    {name!r}: dict(sha256={sha!r}, size={size}, b64=(\n" +
    ''.join(f"        {b64[i:i + 100]!r}\n" for i in range(0, len(b64), 100)) + "    )),\n"
    for name, (sha, size, b64) in parts.items()) + '}\n'

cells = [
    md('''
# DiagRAG v5 on Kaggle: one file, the pre-registered judged run (seed 49)

Runs the frozen `diagrag_v5.py` (SHA-256 `%s`) on a Kaggle **GPU T4 x1** with **Internet On**, then runs the
pre-registered analysis of the closed loop. Run All. Expect about 3 to 5 hours (more hard episodes than v4); this is an estimate, not a measurement. If the session stops, run it again: it resumes
from `diagrag_out/checkpoint.pkl`.

What it does, in order: (1) writes the embedded code and checks its hashes, (2) downloads and SHA-256-checks the corpus, cache, ESCI
and Webis data, (3) builds the 28 core-fault episodes, trains and gates the detectors and repairs, runs the closed loop and the natural-traffic
arms, (4) writes `VERDICT.json`, `REPORT.md` and the tables, (5) runs `analysis_gpu_plan.py` and writes `GPU_ANALYSIS.json`.

What a pass does and does not show. The 28 faults are **injected** by the same authors who wrote the detectors and repairs, on an e-commerce
search stack. The natural-traffic arms use real, never-examined queries. The result is evidence for this method on these stacks, not a
proof that it works on any production RAG system. Gates are fixed in the code and are reported as pass or fail, whichever way they fall.

Code was written by Claude (Anthropic) with the repository owner directing the work. Disclose that in any paper.
''' % EXPECT_V4),
    code('''
# 1. Configuration. These are the pre-registered v5 settings (seed 49, docs/evidence/v5_protocol.md section 3). The protocol allows ONE judged run; do not change SEED to shop for a verdict.
import os
CONFIG = dict(SEED='49', N_BASE_ESCI='2400', N_PRDC='528', N_HARD='100', MAX_ATT='4000', N_HARM='20', TIME_BUDGET='30000')
os.environ.update(CONFIG)
print(CONFIG)
'''),
    code('# 2. Embedded, hash-pinned files (gzip + base64).\n' + EMBED),
    code('''
# 3. Write the embedded files, verify SHA-256, then fail loudly on any mismatch.
import base64, gzip, hashlib, os
ON_KAGGLE = os.path.exists('/kaggle/working')
CODE_DIR = '/kaggle/working/code' if ON_KAGGLE else os.path.join(os.getcwd(), 'code')
os.makedirs(CODE_DIR, exist_ok=True)
for name, e in EMBED.items():
    raw = gzip.decompress(base64.b64decode(''.join(e['b64'])))
    assert len(raw) == e['size'] and hashlib.sha256(raw).hexdigest() == e['sha256'], f'{name}: embedded file is corrupt'
    open(os.path.join(CODE_DIR, name), 'wb').write(raw)
    print('ok', name, e['size'], 'bytes', e['sha256'][:16])
assert EMBED['diagrag_v5.py']['sha256'] == "%s", 'not the frozen v5 file'
''' % EXPECT_V4),
    code('''
# 4. Run the judged pipeline. runpy sets __file__, so JUDGED_PROTOCOL.json records the hash of the pinned file.
import glob, json, runpy, shutil, sys, time
WORK = '/kaggle/working' if ON_KAGGLE else os.getcwd()
OUT = os.path.join(WORK, 'diagrag_out')
if ON_KAGGLE:   # resume from an attached earlier version of this notebook, if there is one
    for ck in glob.glob('/kaggle/input/**/diagrag_out/checkpoint.pkl', recursive=True):
        if not os.path.exists(os.path.join(OUT, 'checkpoint.pkl')):
            shutil.copytree(os.path.dirname(ck), OUT, dirs_exist_ok=True); print('resumed from', ck)
json.dump(dict(config=CONFIG, code_sha256=EMBED['diagrag_v5.py']['sha256'], started_utc=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())),
          open(os.path.join(WORK, 'RUN_CONFIG.json'), 'w'), indent=1)
try:
    runpy.run_path(os.path.join(CODE_DIR, 'diagrag_v5.py'), run_name='__main__')
except SystemExit as e:
    print('stopped with SystemExit', e.code, '- if TIME_BUDGET was reached, run this notebook again with this output attached to resume')
'''),
    code('''
# 5. Pre-registered analysis (G, D1, D2, D3), exactly as committed before the GPU runs. Skipped if the run has not finished.
import subprocess
ck, vd = os.path.join(OUT, 'checkpoint.pkl'), os.path.join(OUT, 'VERDICT.json')
if os.path.exists(ck) and os.path.exists(vd):
    subprocess.run([sys.executable, os.path.join(CODE_DIR, 'analysis_gpu_plan.py'), ck, vd, os.path.join(OUT, 'GPU_ANALYSIS.json')], check=True)
else:
    print('run not finished: no VERDICT.json yet. Run the notebook again to resume.')
'''),
    code('''
# 6. Headline numbers. Every gate is shown, pass or fail.
if os.path.exists(vd):
    V = json.load(open(vd))
    print('verdict:', V.get('verdict'), '| detectors', V.get('detectors_pass'), '| repairs', V.get('repairs_pass'),
          '| solved both', f"{V.get('solved_both')}/{V.get('of')}")
    print('loop gates:', json.dumps(V.get('loop_gates'), indent=1))
    print('protocol code hash:', json.load(open(os.path.join(OUT, 'JUDGED_PROTOCOL.json'))).get('code_sha256'))
'''),
]
nb = dict(nbformat=4, nbformat_minor=5, cells=cells,
          metadata=dict(kernelspec=dict(name='python3', display_name='Python 3', language='python'), language_info=dict(name='python'),
                        kaggle=dict(accelerator='gpu', isInternetEnabled=True)))
out = os.path.join(here, 'DiagRAG_v5_kaggle.ipynb')
json.dump(nb, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote', out, os.path.getsize(out), 'bytes')
