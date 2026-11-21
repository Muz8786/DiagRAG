"""Build the v15 S/M notebooks (docs/evidence/v15_selftest_mutants_protocol.md):
kaggle/DiagRAG_v15_{trial55,dev55,heldout71,heldout72,heldout73}.ipynb.
Cells: title; config (v6 settings, the run's seed, TIME_BUDGET 0, TRIAL flag); the v11.a notebook's hash-pinned embed and write cells UNCHANGED; the analysis script embedded with its hash;
checkpoint staging from the attached judged run output (code hash and seed asserted); harness (frozen v6 executed up to its U1 stage on the resumed checkpoint); analysis; resource report.
usage: python kaggle/mk_v14_esci_notebooks.py"""
import base64, gzip, hashlib, json, os

here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
v11 = json.load(open(os.path.join(here, 'DiagRAG_v11a_main.ipynb'), encoding='utf-8'))
raw = open(os.path.join(root, 'docs', 'evidence', 'v15_selftest_mutants.py'), 'rb').read(); XSHA = hashlib.sha256(raw).hexdigest(); XB = base64.b64encode(gzip.compress(raw, 9, mtime=0)).decode()
lines = lambda s: s.strip('\n').splitlines(True)
md = lambda t: dict(cell_type='markdown', metadata={}, source=lines(t)); code = lambda t: dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=lines(t))
for name, SEED, TRIAL, ROLE, PARTS in [('dev55m', '55', 0, 'dev', ('M',)), ('heldout71s', '71', 0, 'heldout', ('S',)), ('heldout72s', '72', 0, 'heldout', ('S',)), ('heldout73s', '73', 0, 'heldout', ('S',)),
                                       ('heldout71m', '71', 0, 'heldout', ('M',)), ('heldout72m', '72', 0, 'heldout', ('M',)), ('heldout73m', '73', 0, 'heldout', ('M',)),
                                       ('dev71m', '71', 0, 'dev', ('M',)), ('heldout74m', '74', 0, 'heldout', ('M',)), ('heldout75m', '75', 0, 'heldout', ('M',)), ('heldout76m', '76', 0, 'heldout', ('M',))]:
    cells = [
        md(f"# DiagRAG v15 self-test (S) and code mutants (M) on ESCI, seed {SEED}, role {ROLE}, parts {'+'.join(PARTS)} ({'TRIAL: limited work, numbers are not results' if TRIAL else 'JUDGED RUN'})\n\nResumes the judged ESCI checkpoint of seed {SEED} and runs the frozen v6 code (`44176b9a…e28a`) up to its U1 stage, then the measurements of `docs/evidence/v15_selftest_mutants_protocol.md`. GPU T4, Internet On. No API key."),
        code(f"import os\nCONFIG = dict(SEED='{SEED}', N_BASE_ESCI='6000', N_PRDC='528', N_HARD='100', MAX_ATT='4000', N_HARM='20', TIME_BUDGET='0')   # v6 settings; TIME_BUDGET 0 = no self-stop\nos.environ.update(CONFIG); TRIAL = {TRIAL}; ROLE = {ROLE!r}; RUN_PARTS = {PARTS!r}; print(CONFIG, 'TRIAL', TRIAL, 'ROLE', ROLE, 'RUN_PARTS', RUN_PARTS)"),
        v11['cells'][2],
        v11['cells'][3],
        code(f"XEMBED = dict(sha256={XSHA!r}, size={len(raw)}, b64=(\n" + ''.join(f'    {XB[i:i + 100]!r}\n' for i in range(0, len(XB), 100)) + "))\n"
             f"xr = gzip.decompress(base64.b64decode(''.join(XEMBED['b64']))); assert hashlib.sha256(xr).hexdigest() == XEMBED['sha256'] == {XSHA!r}\nopen(os.path.join(CODE_DIR, 'v15_selftest_mutants.py'), 'wb').write(xr); print('ok v15_selftest_mutants.py', XEMBED['sha256'][:16])"),
        code(f"""
# Stage the judged checkpoint folder (attached kernel output) and check its identity before anything else runs.
import glob, shutil, json
WORK = '/kaggle/working'; OUTD = os.path.join(WORK, 'diagrag_out')
src = [os.path.dirname(p) for p in glob.glob('/kaggle/input/**/diagrag_out/checkpoint.pkl', recursive=True)]
assert src, 'judged checkpoint not attached'
if not os.path.exists(os.path.join(OUTD, 'checkpoint.pkl')): shutil.copytree(src[0], OUTD, dirs_exist_ok=True)
P = json.load(open(os.path.join(OUTD, 'JUDGED_PROTOCOL.json')))
assert P['code_sha256'] == '44176b9a5ad633e39ec29581237d9919619b9944471178effb172be1d276e28a' and str(P['cfg']['SEED']) == '{SEED}', 'not the judged seed-{SEED} run'
assert os.path.exists(os.path.join(OUTD, 'VERDICT.json')), 'the judged run did not finish'
print('staged checkpoint from', src[0], '| code', P['code_sha256'][:12], '| seed', P['cfg']['SEED'])
"""),
        code("""
# Harness: execute the frozen v6 code cell by cell up to and including its U1 stage, on the resumed checkpoint (stages already done are skipped by the code itself).
import re, time, sys
T0 = time.time(); SRC = open(os.path.join(CODE_DIR, 'diagrag_v6.py'), encoding='utf-8').read()
CELLS = re.split(r'\\n# %%(?: \\[markdown\\])?\\n', SRC); LAST = max(i for i, c in enumerate(CELLS) if "log('U1', U1)" in c)
G = {'__name__': '__harness__', '__file__': os.path.join(CODE_DIR, 'diagrag_v6.py')}
for i, c in enumerate(CELLS[:LAST + 1]):
    if not c.lstrip().startswith('# '): exec(compile(c, f'v6cell{i}', 'exec'), G)
print('harness done in', round(time.time() - T0), 's; stored U1:', G['U1'])
"""),
        code("""
sys.path.insert(0, CODE_DIR); import v15_selftest_mutants
T1 = time.time(); v15_selftest_mutants.main(G, os.path.join(WORK, 'v15_out'), TRIAL, ROLE, RUN_PARTS); print('analysis wall time (s):', round(time.time() - T1))
"""),
        code("import resource\nprint('peak RSS (GB):', round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**2, 2)); print([l for l in open('/proc/meminfo') if l.startswith(('MemTotal', 'MemAvailable'))])"),
    ]
    nb = dict(nbformat=4, nbformat_minor=5, cells=cells, metadata=v11['metadata'])
    p = os.path.join(here, f'DiagRAG_v15_{name}.ipynb'); json.dump(nb, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); print('wrote', p)
print('analysis script sha256', XSHA)
