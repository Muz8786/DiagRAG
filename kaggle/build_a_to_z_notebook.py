"""Build kaggle/DiagRAG_A_to_Z_kaggle.ipynb: ONE Kaggle notebook that, together with the data zip DiagRAG_KAGGLE_A_to_Z.zip
(attached to the notebook as a Kaggle dataset), runs the whole project from A to Z:

  A  integrity of every shipped file and every judged run's code hash
  B  re-fit of every detector from the shipped episodes, under the library versions each run recorded
  C  the stored results: verdict table of all judged runs, the composed-fault headline, the single-fault regression check
  D  the optional simulated QML comparison
  E  the benchmark quickstart
  F  (flag) the pre-registered v6 judged run on a GPU
  G  (flag) the composed-fault arm (v7), resumed from the shipped v6 checkpoint on CPU
  H  everything collected into one results zip

The notebook contains no project code of its own: it runs the hash-pinned files from the zip.
Usage: python kaggle/build_a_to_z_notebook.py"""
import json, os

here = os.path.dirname(os.path.abspath(__file__))
lines = lambda s: s.strip('\n').splitlines(True)
def md(t): return dict(cell_type='markdown', metadata={}, source=lines(t))
def code(t): return dict(cell_type='code', metadata={}, execution_count=None, outputs=[], source=lines(t))

cells = [
md('''
# DiagRAG, A to Z, in one Kaggle notebook

**What this is.** DiagRAG diagnoses and repairs retrieval faults in a RAG system from telemetry alone. This notebook runs the
whole project from the data zip `DiagRAG_KAGGLE_A_to_Z.zip`: it checks every file, re-fits every detector, shows the stored
results of all 11 judged runs and of the composed-fault arm, runs the optional simulated QML comparison and the benchmark
quickstart, and (if you switch them on) regenerates the pre-registered v6 GPU run and the composed-fault arm.

**How to use it.**
1. Upload `DiagRAG_KAGGLE_A_to_Z.zip` as a Kaggle **Dataset** (private is fine; Kaggle unpacks it). Add it to this notebook as an input.
2. Settings: **Internet On** (models, pip and the RAGLog code are fetched at run time). GPU T4 only for stage F.
3. **Run All.** With the default flags (cell 2) it takes about 15 to 25 minutes on CPU and needs no GPU and no key. (This is an estimate, not a measurement on Kaggle.)
4. Read `A_TO_Z_GUIDE.md` in the zip for what every stage means.

**What a result here does and does not show.** The 28 faults are injected by the people who wrote the detectors and repairs, on an
e-commerce search stack; the natural-traffic arm uses real, never-examined queries. The composed-fault arm and the QML comparison are descriptive: no
adoption gate, and the QML models are simulated, with no claim of quantum advantage. The code was written by Claude (Anthropic) with the repository owner directing the work; disclose that in any paper.
'''),
code('''
# 2. FLAGS. Defaults = the quick check path (CPU, no key, about 15-25 minutes, estimate).
FLAGS = dict(
    CHECKS=True,        # stages A, B, C: integrity, detector re-fit, stored results
    QML=True,           # stage D: simulated quantum-ML comparison (about 2-5 minutes)
    BENCH=True,         # stage E: benchmark quickstart
    RUN_V6_GPU=False,   # stage F: the pre-registered v6 judged run, seed 50 (needs GPU T4 x1; estimated 4-6 hours, not re-measured)
    RUN_V7_CPU=False,   # stage G: composed-fault arm from the shipped v6 checkpoint (CPU; about 3 h on 8 cores in the stored run, more on 4 cores)
    SMOKE=False,        # stages F and G with tiny settings, to test the wiring only (numbers mean nothing)
)
import json as _j, os as _o
if _o.environ.get('DIAGRAG_FLAGS'): FLAGS.update(_j.loads(_o.environ['DIAGRAG_FLAGS']))   # for local tests
print(FLAGS)
'''),
code('''
# 3. Locate and open the data package (the zip you attached as a dataset).
import os, sys, glob, json, shutil, subprocess, time, zipfile, hashlib, platform, re
ON_KAGGLE = os.path.exists('/kaggle/working')
WORKROOT = '/kaggle/working' if ON_KAGGLE else os.environ.get('DIAGRAG_NB_WORK', os.path.join(os.getcwd(), 'nb_work'))
os.makedirs(WORKROOT, exist_ok=True)
MARK = 'PACKAGE_MANIFEST.json'
def find_pkg():
    p = os.environ.get('DIAGRAG_PKG')
    if p and os.path.exists(os.path.join(p, MARK)): return p
    roots = ['/kaggle/input'] if ON_KAGGLE else [os.getcwd(), os.path.dirname(os.getcwd())]
    for r in roots:
        for dp, dn, fn in os.walk(r):
            if dp.count(os.sep) - r.count(os.sep) > 5: dn[:] = []; continue
            if MARK in fn: return dp
    for r in roots:   # a zip attached as a plain file instead of an unpacked dataset
        for z in glob.glob(os.path.join(r, '**', 'DiagRAG_KAGGLE_A_to_Z*.zip'), recursive=True):
            dst = os.path.join(WORKROOT, 'unzipped'); print('unpacking', z); zipfile.ZipFile(z).extractall(dst)
            for dp, dn, fn in os.walk(dst):
                if MARK in fn: return dp
    return None
PKG = find_pkg()
assert PKG, 'The data package was not found. Upload DiagRAG_KAGGLE_A_to_Z.zip as a Kaggle Dataset and add it as an input of this notebook.'
MAN = json.load(open(os.path.join(PKG, MARK)))
print('package:', PKG, '| edition:', MAN.get('edition', 'full')); print('built:', MAN['built_utc'], '| files:', MAN['n_files'], '| size (MB):', MAN['size_mb'])
STATUS = {}   # stage -> dict(ok, seconds, note)
def stage(name):
    class _S:
        def __enter__(s): s.t = time.time(); print('\\n' + '=' * 78 + '\\n== ' + name + '\\n' + '=' * 78); return s
        def __exit__(s, et, ev, tb):
            STATUS[name] = dict(ok=et is None, seconds=round(time.time() - s.t, 1), note=('' if et is None else f'{et.__name__}: {ev}'[:300]))
            print(f'-- {name}: ' + ('OK' if et is None else 'FAILED ' + STATUS[name]['note']), f'({STATUS[name]["seconds"]} s)'); return True   # keep going, report at the end
    return _S()
'''),
code('''
# 4. Environment and helpers.
def sh(cmd, env=None, cwd=None, tail=0, log=None, timeout=None, quiet=False):
    """Run a command, stream its output (optionally filtered to the last lines), return (rc, output)."""
    e = dict(os.environ); e.update(env or {})
    p = subprocess.Popen(cmd, shell=isinstance(cmd, str), cwd=cwd or PKG, env=e, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    out = []; t0 = time.time(); f = open(log, 'a') if log else None
    try:
        for line in p.stdout:
            out.append(line)
            if f: f.write(line); f.flush()
            if not tail and not quiet and not re.search(r'Warning|Loading weights|Batches|it/s\\]', line): print(line, end='')
            if timeout and time.time() - t0 > timeout: p.kill(); out.append('[killed: timeout]\\n'); break
    finally:
        p.wait(); f and f.close()
    if tail and not quiet: print(''.join(out[-tail:]), end='')
    return p.returncode, ''.join(out)
import torch
try: import sklearn, numpy, pandas; V = dict(sklearn=sklearn.__version__, numpy=numpy.__version__, pandas=pandas.__version__)
except Exception as ex: V = dict(error=str(ex))
GPU = torch.cuda.is_available()
du = shutil.disk_usage(WORKROOT)
print('python', platform.python_version(), '| torch', torch.__version__, '| GPU:', torch.cuda.get_device_name(0) if GPU else None, '| cores:', os.cpu_count(), '| libs:', V,
      '| free disk GB:', round(du.free / 2**30, 1))
RES_DIR = os.path.join(WORKROOT, 'a_to_z_results'); os.makedirs(RES_DIR, exist_ok=True)
PY = sys.executable
'''),
code('''
# 5. Stage A: integrity. Every file's SHA-256, every judged run's recorded code hash, the frozen v5/v6/v7 hashes, the Kaggle notebooks' embedded code.
with stage('A integrity') if FLAGS['CHECKS'] else stage('A integrity (skipped)'):
    if FLAGS['CHECKS']:
        rc, out = sh([PY, 'verify.py'], tail=14)
        assert rc == 0 and 'ALL OK' in out, 'verify.py reported a problem'
'''),
code('''
# 6. Stage B: re-fit every detector from the shipped episodes and compare with the recorded AUROCs, each under the library versions of ITS stack.
# (A near-bar detector moves by up to 0.03 between scikit-learn versions; the CPU runs recorded 1.9.1, the Kaggle GPU runs recorded 1.6.1.)
PINS = {'cpu': ('1.9.1', '2.4.6'), 'gpu': ('1.6.1', '2.1.3')}
REFIT_RUNS = [('judged_cpu_run_v4_seed47', 'cpu'), ('judged_cpu_run_v5_seed49', 'cpu'), ('judged_cpu_run_v6_seed50', 'cpu'), ('judged_cpu_run_v7_seed50', 'cpu'),
              ('judged_gpu_v3_seed46', 'gpu'), ('judged_gpu_v4_seed48', 'gpu'), ('judged_gpu_v6_seed50', 'gpu')]
def pinned_pythonpath(stack):
    sk, npv = PINS[stack]; d = os.path.join(WORKROOT, 'pins', f'sk{sk}_np{npv}')
    if not os.path.exists(os.path.join(d, 'sklearn')):
        rc, out = sh([PY, '-m', 'pip', 'install', '-q', '--target', d, f'scikit-learn=={sk}', f'numpy=={npv}'], quiet=True)
        if rc != 0: print('pinned install failed for', stack, '- using the notebook libraries:', out[-300:]); return None
    return d
REFIT = {}
with stage('B detector re-fit') if FLAGS['CHECKS'] else stage('B detector re-fit (skipped)'):
    if FLAGS['CHECKS']:
        for run, stack in REFIT_RUNS:
            if not os.path.isdir(os.path.join(PKG, 'kaggle', run)): print('absent', run); continue
            pp = pinned_pythonpath(stack)
            rc, out = sh([PY, 'kaggle/reproduce_tables.py', f'kaggle/{run}'], env=({'PYTHONPATH': pp} if pp else {}), quiet=True)
            m = re.search(r'(\\d+) of (\\d+) detector AUROCs reproduced within ([0-9.]+); largest difference ([0-9.]+)', out)
            REFIT[run] = dict(stack=stack, pins=PINS[stack] if pp else 'notebook libraries', result=m.group(0) if m else 'no result: ' + out[-200:].replace(chr(10), ' '))
            print(f'{run:34s} [{stack}, {"sklearn %s numpy %s" % PINS[stack] if pp else "notebook libs"}]  {REFIT[run]["result"]}')
        json.dump(REFIT, open(os.path.join(RES_DIR, 'refit.json'), 'w'), indent=1)
'''),
code('''
# 7. Stage C: the stored results. Nothing is recomputed from raw data here; every number is read from the shipped judged-run files.
with stage('C stored results') if FLAGS['CHECKS'] else stage('C stored results (skipped)'):
    if FLAGS['CHECKS']:
        rc, out = sh([PY, 'docs/evidence/make_matrix_and_frontier.py', 'kaggle', os.path.join(RES_DIR, 'all_runs_matrix.md')], quiet=True)
        txt = open(os.path.join(RES_DIR, 'all_runs_matrix.md'), encoding='utf-8').read(); print(txt.split('### ')[0][:5200])
        comp = json.load(open(os.path.join(PKG, 'kaggle', 'judged_cpu_run_v7_seed50', 'COMPOSED_RESULT.json')))
        print('\\nCOMPOSED-FAULT HEADLINE (generated by the v7 script from its own files):\\n' + comp['headline'])
        rc, out = sh([PY, 'docs/evidence/v7_regression_check.py', 'kaggle/judged_cpu_run_v6_seed50', 'kaggle/judged_cpu_run_v7_seed50', os.path.join(RES_DIR, 'v7_regression.json')], quiet=True)
        print('\\nSINGLE-FAULT REGRESSION CHECK, v7 against v6 CPU (protocol section 4):'); print('\\n'.join(l[:230] for l in out.splitlines() if l.startswith(('REGRESSION', 'counts', 'loop gates', 'U1', 'capped'))))
        assert rc == 0 and 'REGRESSION = False' in out, 'the regression check did not pass'
'''),
code('''
# 8. Stage D (optional): simulated quantum machine learning against classical models. Six qubits, noiseless statevector simulator written in the repository.
# No hardware, no noise model, NO claim of quantum advantage. Machine learning is the project's method; this is a side comparison of scores.
with stage('D QML comparison') if FLAGS['QML'] else stage('D QML comparison (skipped)'):
    if FLAGS['QML']:
        rc, out = sh([PY, 'docs/evidence/qml_compare.py', 'kaggle/judged_cpu_run_v6_seed50/episodes.jsonl', os.path.join(RES_DIR, 'qml_result.json'),
                      '--composed', 'kaggle/judged_cpu_run_v7_seed50/composed_features.jsonl', '--threads', str(min(8, os.cpu_count() or 4))], quiet=True)
        print('\\n'.join(l for l in out.splitlines() if re.search(r'AUROC|wrote|VQC seed', l)))
        assert rc == 0, out[-500:]
'''),
code('''
# 9. Stage E: the benchmark quickstart (DiagRAG-Bench v1.0: verify the release, fit a diagnoser on the dev split, score it). The test labels are private; only their SHA-256 commitment is shipped.
with stage('E benchmark quickstart') if FLAGS['BENCH'] else stage('E benchmark quickstart (skipped)'):
    if FLAGS['BENCH']:
        B = os.path.join(PKG, 'bench'); pred = os.path.join(RES_DIR, 'dev_pred.csv')
        rc, out = sh([PY, 'verify_release.py', 'release_v1'], cwd=B, tail=3); assert rc == 0
        rc, out = sh([PY, 'quickstart_dev_cv.py', 'release_v1', pred], cwd=B, quiet=True); assert rc == 0, out[-400:]
        rc, out = sh([PY, 'score.py', '--labels', 'release_v1/labels_dev.jsonl', '--track1', pred], cwd=B, tail=14)
'''),
code('''
# 10. Stage F (flag RUN_V6_GPU or SMOKE): the pre-registered v6 judged run. Runs the hash-pinned diagrag_v6.py from the zip with the protocol's settings (seed 50).
# The protocol allows ONE GPU run and ONE CPU replication at seed 50: this is a reproduction and does not replace the stored result. Do not change SEED to look for a different verdict.
import hashlib, runpy
def file_sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def frozen_hash(proto_name, tag):
    t = open(os.path.join(PKG, 'docs', 'evidence', proto_name), encoding='utf-8').read(); return re.findall(r'frozen %s hash is now `([0-9a-f]{64})`' % tag, t)[-1]
V6_OUT = os.path.join(WORKROOT, 'run_v6_out')
SMOKE6 = dict(N_BASE_ESCI='700', N_PRDC='40', N_HARD='6', MAX_ATT='60', N_HARM='3', N_NATQ='40', N_CAL_EXTRA='60', N_CENSUS='200')
JUDGED6 = dict(N_BASE_ESCI='6000', N_PRDC='528', N_HARD='100', MAX_ATT='4000', N_HARM='20')
CPU_RERANK = dict(RERANKER='cross-encoder/ms-marco-MiniLM-L-6-v2', CE_MAXLEN='256')
def link_data(dst):
    """Put the shipped input files where the script looks for them (exact size and SHA-256 are re-checked by the script itself)."""
    os.makedirs(dst, exist_ok=True)
    if not os.path.isdir(os.path.join(PKG, 'data')):
        print('this package has no data/ folder (LITE edition): the script will download its input files from their original sources (Internet On) and check their SHA-256'); return
    for f in os.listdir(os.path.join(PKG, 'data')):
        if f.endswith('.md') or f.endswith('.sha256'): continue
        d = os.path.join(dst, f)
        if not os.path.exists(d): os.symlink(os.path.join(PKG, 'data', f), d)
def script_env(work, extra):
    e = dict(SEED='50', DIAGRAG_WORK=work, TORCH_THREADS=str(os.cpu_count() or 4)); e.update(extra); return e
run_f = FLAGS['RUN_V6_GPU'] or FLAGS['SMOKE']
with stage('F v6 judged run') if run_f else stage('F v6 judged run (skipped)'):
    if run_f:
        smoke = FLAGS['SMOKE']; script = os.path.join(PKG, 'kaggle', 'diagrag_v6.py')
        assert file_sha(script) == frozen_hash('v6_protocol.md', 'v6'), 'diagrag_v6.py is not the file frozen in the protocol'
        if not smoke: assert GPU, 'The v6 judged configuration is the GPU one: set the accelerator to GPU T4 x1 (or set SMOKE).'
        work = V6_OUT if not ON_KAGGLE else '/kaggle/working'; os.makedirs(work, exist_ok=True)
        link_data('/tmp/diagrag_data' if ON_KAGGLE else os.path.join(work, 'diagrag_data'))
        if ON_KAGGLE:   # resume from an attached earlier version of this notebook's output, if there is one
            for ck in glob.glob('/kaggle/input/**/diagrag_out/checkpoint.pkl', recursive=True):
                if not os.path.exists('/kaggle/working/diagrag_out/checkpoint.pkl'):
                    os.makedirs('/kaggle/working/diagrag_out', exist_ok=True); shutil.copy(ck, '/kaggle/working/diagrag_out/checkpoint.pkl'); print('resuming from', ck)
        if smoke:   # the smoke test would spend its whole time re-encoding the ~180,000-query log on CPU; the shipped cache has the same name only if the query set is identical, otherwise it is ignored
            q = os.path.join(PKG, 'prereq', 'qlog_nn_b03a9b172742.npy'); os.makedirs(os.path.join(work, 'diagrag_out'), exist_ok=True)
            if os.path.exists(q) and not os.path.exists(os.path.join(work, 'diagrag_out', os.path.basename(q))): shutil.copy(q, os.path.join(work, 'diagrag_out'))
        extra = dict(SMOKE6, **CPU_RERANK, TIME_BUDGET='1300') if smoke else dict(JUDGED6, TIME_BUDGET='30000')   # a budget stop saves the checkpoint; the loop below resumes it
        if smoke and GPU: extra.pop('RERANKER'); extra.pop('CE_MAXLEN')
        log = os.path.join(RES_DIR, 'run_v6.log')
        done = False
        for i in range(1, 41):
            rc, out = sh([PY, '-u', script], env=script_env(work, extra), cwd=work, log=log, timeout=(1750 if smoke else None), quiet=True)
            print(f'v6 chunk {i}: exit {rc} |', ([l for l in out.splitlines() if 'checkpoint saved' in l or 'TIME_BUDGET' in l or 'done. outputs' in l][-1:] or ['(no progress line)'])[0][:120])
            if 'done. outputs' in out: done = True; break
            if 'TIME_BUDGET reached' not in out and 'killed: timeout' not in out: print(out[-1500:]); raise RuntimeError('the v6 script stopped with an error; see ' + log)
        assert done, 'not finished; run this cell again to resume from the checkpoint (see ' + log + ')'
        outd = os.path.join(work, 'diagrag_out'); v = json.load(open(os.path.join(outd, 'VERDICT.json')))
        print('\\nV6 RESULT:', v['verdict'], '| detectors', v['detectors_pass'], '| repairs', v['repairs_pass'], '| loop gates', v['loop_gates'])
        if not smoke:
            rc, o = sh([PY, os.path.join(PKG, 'docs', 'evidence', 'analysis_gpu_plan.py'), os.path.join(outd, 'checkpoint.pkl'), os.path.join(outd, 'VERDICT.json'), os.path.join(outd, 'GPU_ANALYSIS.json')], quiet=True)
        if ON_KAGGLE:   # stage G uses the same /kaggle/working/diagrag_out: move this run's outputs aside
            os.makedirs(V6_OUT, exist_ok=True); shutil.move(outd, os.path.join(V6_OUT, 'diagrag_out'))
'''),
code('''
# 11. Stage G (flag RUN_V7_CPU or SMOKE): the composed-fault arm. Resumes from the shipped v6 CPU checkpoint (stage lofo_done, 9,535 single-fault episodes) after removing ONLY the attributor-dependent
# results (docs/evidence/v7_prepare_checkpoint.py), then runs the hash-pinned diagrag_v7.py in chunks on CPU with the settings recorded in docs/evidence/v7_composed_protocol.md.
# It is forced onto the CPU configuration (the checkpoint is a CPU-stack state). A reproduction on other hardware may differ in the third decimal; it does not replace the stored result.
V7_WORK = os.path.join(WORKROOT, 'run_v7')
run_g = FLAGS['RUN_V7_CPU'] or FLAGS['SMOKE']
with stage('G composed-fault arm (v7)') if run_g else stage('G composed-fault arm (v7) (skipped)'):
    if run_g:
        smoke = FLAGS['SMOKE']; script = os.path.join(PKG, 'kaggle', 'diagrag_v7.py')
        assert file_sha(script) == frozen_hash('v7_composed_protocol.md', 'v7'), 'diagrag_v7.py is not the file frozen in the protocol (D3)'
        assert smoke or os.path.exists(os.path.join(PKG, 'prereq', 'v6_cpu_checkpoint.pkl')), 'Stage G needs prereq/v6_cpu_checkpoint.pkl, which is only in the FULL edition of the package (this is the LITE edition). Use SMOKE, or the full zip.'
        work = '/kaggle/working' if ON_KAGGLE else V7_WORK; outd = os.path.join(work, 'diagrag_out'); os.makedirs(outd, exist_ok=True)
        link_data('/tmp/diagrag_data' if ON_KAGGLE else os.path.join(work, 'diagrag_data'))
        src = os.path.join(V6_OUT, 'diagrag_out', 'checkpoint.pkl') if smoke else os.path.join(PKG, 'prereq', 'v6_cpu_checkpoint.pkl')   # smoke: the tiny v6 run of stage F
        if os.path.exists(os.path.join(outd, 'checkpoint.pkl')): print('a checkpoint is already in', outd, '- continuing it (delete it to start from the shipped v6 state)')
        else:
            assert os.path.exists(src), 'checkpoint source not found: ' + src
            rc, o = sh([PY, os.path.join(PKG, 'docs', 'evidence', 'v7_prepare_checkpoint.py'), src, os.path.join(outd, 'checkpoint.pkl')], tail=22)
            assert rc == 0
            if not smoke:
                q = os.path.join(PKG, 'prereq', 'qlog_nn_b03a9b172742.npy'); dst = os.path.join(outd, os.path.basename(q))
                if not os.path.exists(dst): shutil.copy(q, dst)
        extra = dict(CPU_RERANK, CUDA_VISIBLE_DEVICES='', TIME_BUDGET='1400')
        extra.update(dict(SMOKE6, COMP_QUOTA_SCALE='0.15', COMP_CLEAN_N='20') if smoke else dict(JUDGED6, COMP_CLEAN_N='300'))   # the stored run's settings (v7 protocol)
        log = os.path.join(RES_DIR, 'run_v7.log'); done = False
        for i in range(1, 41):
            rc, o = sh([PY, '-u', script], env=script_env(work, extra), cwd=work, log=log, timeout=1750, quiet=True)
            print(f'chunk {i}: exit {rc} |', ([l for l in o.splitlines() if 'checkpoint saved' in l or 'TIME_BUDGET' in l or 'done. outputs' in l][-1:] or ['(no progress line)'])[0][:120])
            if 'done. outputs' in o: done = True; break
            if 'TIME_BUDGET reached' not in o and rc != 0 and 'killed: timeout' not in o: print(o[-1500:]); raise RuntimeError('the v7 script stopped with an error; see ' + log)
        assert done, 'not finished after 40 chunks; run this cell again to resume'
        comp = json.load(open(os.path.join(outd, 'COMPOSED_RESULT.json'))); print('\\nCOMPOSED HEADLINE (this run):\\n' + comp['headline'])
        v = json.load(open(os.path.join(outd, 'VERDICT.json'))); print('V7 single-fault verdict:', v['verdict'], v['detectors_pass'], v['repairs_pass'], v['loop_gates'])
        if ON_KAGGLE: shutil.copytree(outd, os.path.join(V7_WORK, 'diagrag_out'), ignore=shutil.ignore_patterns('checkpoint*', 'qlog_nn*'), dirs_exist_ok=True)   # small result files only
        if not smoke:
            rc, o = sh([PY, os.path.join(PKG, 'docs', 'evidence', 'v7_regression_check.py'), os.path.join(PKG, 'kaggle', 'judged_cpu_run_v6_seed50'), outd, os.path.join(RES_DIR, 'v7_regression_rerun.json')], tail=4)
'''),
code('''
# 12. Stage H: collect results into one zip (small files only) and print the status of every stage.
with stage('H collect'):
    zp = os.path.join(WORKROOT, 'DiagRAG_A_to_Z_RESULTS.zip')
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for root_dir in (RES_DIR, V6_OUT, V7_WORK):
            for dp, dn, fn in os.walk(root_dir):
                if 'diagrag_data' in dp or 'pins' in dp: dn[:] = []; continue
                for f in fn:
                    p = os.path.join(dp, f)
                    if f.startswith('checkpoint') or f.startswith('qlog_nn') or f.endswith('.partial.npy') or os.path.getsize(p) > 60 * 2**20: continue
                    z.write(p, os.path.relpath(p, WORKROOT))
        json.dump(STATUS, open(os.path.join(RES_DIR, 'STATUS.json'), 'w'), indent=1); z.write(os.path.join(RES_DIR, 'STATUS.json'), 'a_to_z_results/STATUS.json')
    print('results zip:', zp, round(os.path.getsize(zp) / 2**20, 1), 'MB')
print('\\nSTAGE STATUS')
for k, v in STATUS.items(): print(f'  {"ok    " if v["ok"] else "FAILED"} {k:42s} {v["seconds"]:8.1f} s  {v["note"]}')
assert all(v['ok'] for v in STATUS.values()), 'at least one stage failed (see above)'
'''),
]

nb = dict(cells=cells, metadata=dict(kernelspec=dict(display_name='Python 3', language='python', name='python3'), language_info=dict(name='python')), nbformat=4, nbformat_minor=5)
import ast
for c in cells:
    if c['cell_type'] == 'code': ast.parse(''.join(c['source']))
out = os.path.join(here, 'DiagRAG_A_to_Z_kaggle.ipynb'); json.dump(nb, open(out, 'w'), indent=1); print('wrote', out, len(cells), 'cells')
