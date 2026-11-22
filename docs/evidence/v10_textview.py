"""Replay step of the supervised text baseline (docs/evidence/v10_textbaseline_protocol.md section 1). Read-only on the frozen code and on the run's checkpoint.
Executes ONLY the setup cells of kaggle/diagrag_port3.py (stack, run()) with the run's own settings and caches, then replays run(st) for every stored episode and writes
<out>.jsonl: id, split, fault, query, the five documents (first 360 chars each). It also checks the replay against the stored clean Hit@5. The output contains BEIR text, which is NOT redistributed: do not commit it.
usage: DATASET=nfcorpus SEED=53 python docs/evidence/v10_textview.py <work_dir_with_port3_<ds>_out/checkpoint.pkl> <out.jsonl>     (resumable)"""
import hashlib, json, os, pickle, re, sys, time

work, outp = sys.argv[1], sys.argv[2]; ds = os.environ['DATASET']
os.environ.update(DIAGRAG_WORK=work, N_QUERIES='2500', N_HARD='50', MAX_ATT='2500', N_HARM='20', TIME_BUDGET='36000')
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'kaggle', 'diagrag_port3.py'), encoding='utf-8').read()
assert hashlib.sha256(src.encode('utf-8')).hexdigest() == '677a2f38f24a5b0d64849e95930c93ecfd944e28d708753930fde1b2d3a77ada', 'not the frozen port3 file'
cells = re.split(r'\n# %%(?: \[markdown\])?\n', src); last = max(i for i, c in enumerate(cells) if 'def succ(tr, gold' in c)
g = {'__name__': '__replay__', '__file__': os.path.join(work, 'diagrag_port3.py')}
t0 = time.time()
for i, c in enumerate(cells[:last + 1]):
    if not c.lstrip().startswith('# '): exec(compile(c, f'port3cell{i}', 'exec'), g)
print(f'setup done {time.time() - t0:.0f}s; N docs {g["N"]}', flush=True)
R = pickle.load(open(os.path.join(work, f'port3_{ds}_out', 'checkpoint.pkl'), 'rb')); EP = R['EPIS']; CL = R['CLEAN']
done = set()
if os.path.exists(outp): done = {json.loads(l)['id'] for l in open(outp)}
fh = open(outp, 'a'); dtext = g['dtext']; run = g['run']; succ = g['succ']; bad = tot = 0; n_new = 0
for n, e in enumerate(EP):
    eid = hashlib.sha256(f"{e['split']}|{e['bid']}|{e['fault']}|{n}".encode()).hexdigest()[:16]
    if eid in done: continue
    st = e['st']; tr = run(st); docs = [dtext(i, st.get('ov'))[:360].replace('\n', ' ') for i in tr['final'][:5]]
    if e['fault'] == 'NONE' and e['bid'] in CL:
        tot += 1; bad += int(bool(succ(tr, st['gold'])) != bool(CL[e['bid']]['h5']))
    fh.write(json.dumps(dict(id=eid, n=n, split=e['split'], fault=e['fault'], bid=e['bid'], query=st['q'], docs=docs, replay_hit=bool(succ(tr, st['gold'])))) + '\n'); n_new += 1
    if n_new % 200 == 0: fh.flush(); print(f'{n}/{len(EP)} {time.time() - t0:.0f}s', flush=True)
fh.close(); print('done', len(EP), 'episodes;', 'clean replay check (this chunk): mismatches', bad, 'of', tot)
