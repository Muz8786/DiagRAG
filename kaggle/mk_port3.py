"""Generate kaggle/diagrag_port3.py from kaggle/diagrag_port2.py (v9 corpus-port arm, docs/evidence/v9_protocol.md).
port3 = port2 with TWO declared edits and nothing else: (1) two more BEIR corpora in the verified-download table (NFCorpus, ArguAna; sizes and SHA-256 measured on 19 Nov 2026),
(2) the output folder is named port3_<dataset>_out. Every gate, fault, injector, repair, stack and statistic is port2's, unchanged.
Each replacement is asserted to occur exactly once. usage: python kaggle/mk_port3.py"""
import hashlib, os

here = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(here, 'diagrag_port2.py'), encoding='utf-8').read()
REPL = [
    ("            fiqa=(17948027, '32c7df99ed21252fdfb2cf3f5673502a8d245ee0c44c4a133570d92ce2b3ad02'))",
     "            fiqa=(17948027, '32c7df99ed21252fdfb2cf3f5673502a8d245ee0c44c4a133570d92ce2b3ad02'),\n"
     "            nfcorpus=(2448432, 'efe5be03f8c5b86a5870102d0599d227c8c6e2484328e68c6522560385671b0b'),\n"
     "            arguana=(3773617, 'cfdf79adce27a401b3cd3ea267903134dbfab2c6afeb95d7fe5724a00bf7557b'))"),
    ("OUT = os.path.join(WORK, f\"port2_{os.environ.get('DATASET', 'scifact')}_out\")", "OUT = os.path.join(WORK, f\"port3_{os.environ.get('DATASET', 'scifact')}_out\")"),
]
out = src
for old, new in REPL:
    assert out.count(old) == 1, f'expected exactly one occurrence of {old[:60]!r}, found {out.count(old)}'
    out = out.replace(old, new)
p = os.path.join(here, 'diagrag_port3.py'); open(p, 'w', encoding='utf-8', newline='').write(out)
print('wrote', p, hashlib.sha256(out.encode('utf-8')).hexdigest(), '| port2 sha', hashlib.sha256(src.encode('utf-8')).hexdigest())
