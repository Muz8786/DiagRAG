"""Generate kaggle/diagrag_port5.py from the frozen kaggle/diagrag_port4.py (v13, docs/evidence/v13_datasets.md).
port5 = port4 + THREE declared edits and nothing else:
 (1) NQ added to the verified-download table (size and SHA-256 measured on 19 Nov 2026; md5 equals the BEIR-published value),
 (2) output folder named port5_<dataset>_out,
 (3) an EXECUTION-ONLY fix to corpus embedding: port4 re-concatenated the whole embedding array and re-saved it after every 2,048 passages (quadratic in corpus size:
     harmless at 57K passages, hours at 2.68M). port5 writes the SAME 2,048-passage chunks, produced by the SAME encode calls, into a preallocated on-disk array and
     records progress in a counter file so a stopped session resumes. The values are unchanged; this is checked by docs/evidence/v13_port5_equivalence.py.
Every gate, fault, injector, repair, stack and statistic is port2's, unchanged. Each replacement is asserted to occur exactly once. usage: python kaggle/mk_port5.py"""
import hashlib, os

here = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(here, 'diagrag_port4.py'), encoding='utf-8').read()
OLD_EMB = """    E = np.load(_ep) if os.path.exists(_ep) else np.zeros((0, 384), np.float32)
    while len(E) < N:
        a_ = len(E); E = np.concatenate([E, np.asarray(ENC.encode(['passage: ' + t for t in TEXT[a_:a_ + 2048]], normalize_embeddings=True, batch_size=64), np.float32)])
        np.save(_ep, E)
        if over_budget(): log('TIME_BUDGET reached during corpus embedding - run again to resume', len(E)); raise SystemExit(0)
    np.save(_ef, E); os.remove(_ep)"""
NEW_EMB = """    _mm, _pc = _ef + '.partial.f32', _ef + '.partial.n'   # v13 execution fix: same chunks and encode calls, written into a preallocated on-disk array
    done_ = int(open(_pc).read()) if (os.path.exists(_pc) and os.path.exists(_mm)) else 0
    Em = np.memmap(_mm, dtype=np.float32, mode='r+' if done_ else 'w+', shape=(N, 384))
    while done_ < N:
        a_ = done_; Em[a_:a_ + 2048] = np.asarray(ENC.encode(['passage: ' + t for t in TEXT[a_:a_ + 2048]], normalize_embeddings=True, batch_size=64), np.float32)
        done_ = min(N, a_ + 2048)
        if (done_ // 2048) % 50 == 0 or done_ >= N: Em.flush(); open(_pc, 'w').write(str(done_)); log('embedded', done_, 'of', N)
        if over_budget(): Em.flush(); open(_pc, 'w').write(str(done_)); log('TIME_BUDGET reached during corpus embedding - run again to resume', done_); raise SystemExit(0)
    Em.flush(); E = np.array(Em); del Em; np.save(_ef, E); os.remove(_mm); os.remove(_pc)"""
REPL = [
    ("            scidocs=(142471588, '96640201687767c9b1fcc5af7a80b90fb325b37fa25329c2586c25edcfa17ef1'))",
     "            scidocs=(142471588, '96640201687767c9b1fcc5af7a80b90fb325b37fa25329c2586c25edcfa17ef1'),\n"
     "            nq=(498307926, '2553bf7bfbab47b1436ca00a34bce57320e18e611fd00999a2a3a1b4714be752'))"),
    ("OUT = os.path.join(WORK, f\"port4_{os.environ.get('DATASET', 'scifact')}_out\")", "OUT = os.path.join(WORK, f\"port5_{os.environ.get('DATASET', 'scifact')}_out\")"),
    (OLD_EMB, NEW_EMB),
]
out = src
for old, new in REPL:
    assert out.count(old) == 1, f'expected exactly one occurrence of {old[:60]!r}, found {out.count(old)}'
    out = out.replace(old, new)
p = os.path.join(here, 'diagrag_port5.py'); open(p, 'w', encoding='utf-8', newline='').write(out)
print('wrote', p, hashlib.sha256(out.encode('utf-8')).hexdigest(), '| port4 sha', hashlib.sha256(src.encode('utf-8')).hexdigest())
