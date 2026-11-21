"""Generate kaggle/diagrag_port4.py from the frozen kaggle/diagrag_port3.py (v11.a, docs/evidence/v11_protocol.md).
port4 = port3 + TWO declared edits and nothing else: (1) SCIDOCS added to the verified-download table (size and SHA-256 measured on 19 Nov 2026), (2) the output folder is named port4_<dataset>_out.
Every gate, fault, injector, repair, stack and statistic is port3's (and so port2's), unchanged. Each replacement is asserted to occur exactly once. usage: python kaggle/mk_port4.py"""
import hashlib, os

here = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(here, 'diagrag_port3.py'), encoding='utf-8').read()
REPL = [
    ("            arguana=(3773617, 'cfdf79adce27a401b3cd3ea267903134dbfab2c6afeb95d7fe5724a00bf7557b'))",
     "            arguana=(3773617, 'cfdf79adce27a401b3cd3ea267903134dbfab2c6afeb95d7fe5724a00bf7557b'),\n"
     "            scidocs=(142471588, '96640201687767c9b1fcc5af7a80b90fb325b37fa25329c2586c25edcfa17ef1'))"),
    ("OUT = os.path.join(WORK, f\"port3_{os.environ.get('DATASET', 'scifact')}_out\")", "OUT = os.path.join(WORK, f\"port4_{os.environ.get('DATASET', 'scifact')}_out\")"),
]
out = src
for old, new in REPL:
    assert out.count(old) == 1, f'expected exactly one occurrence of {old[:60]!r}, found {out.count(old)}'
    out = out.replace(old, new)
p = os.path.join(here, 'diagrag_port4.py'); open(p, 'w', encoding='utf-8', newline='').write(out)
print('wrote', p, hashlib.sha256(out.encode('utf-8')).hexdigest(), '| port3 sha', hashlib.sha256(src.encode('utf-8')).hexdigest())
