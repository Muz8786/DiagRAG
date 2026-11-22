"""Build kaggle/DiagRAG_v8_kaggle.ipynb from kaggle/DiagRAG_v6_kaggle.ipynb for the pre-registered v8 run (docs/evidence/v8_protocol.md).

v8 runs the FROZEN v6 code unchanged. The only things this script changes are the seed (50 -> 52) and the human-readable labels. It asserts every replacement
happens exactly the expected number of times, and that the embedded code blobs are byte-identical to the v6 notebook's.
usage: python kaggle/mk_v8_notebook.py"""
import json, os

here = os.path.dirname(os.path.abspath(__file__))
nb = json.load(open(os.path.join(here, 'DiagRAG_v6_kaggle.ipynb'), encoding='utf-8'))
orig_embed = ''.join(nb['cells'][2]['source'])

REPL = [  # (old, new, expected count over all cell sources)
    ("CONFIG = dict(SEED='50',", "CONFIG = dict(SEED='52',", 1),
    ("# DiagRAG v6 on Kaggle: one file, the pre-registered judged run (seed 50)", "# DiagRAG v8 on Kaggle: the frozen v6 code on a fresh seed (seed 52), pre-registered in docs/evidence/v8_protocol.md", 1),
    ("These are the pre-registered v6 settings (seed 50, docs/evidence/v6_protocol.md section 3). The protocol allows ONE GPU run and ONE CPU replication at seed 50; do not change SEED to shop for a verdict.",
     "These are the v6 settings with ONE change, the seed (52), pre-registered in docs/evidence/v8_protocol.md section 2. One GPU run at seed 52; do not change SEED to shop for a verdict.", 1),
]
counts = {}
for old, new, want in REPL:
    n = 0
    for c in nb['cells']:
        s = ''.join(c['source'])
        if old in s:
            n += s.count(old); c['source'] = (s.replace(old, new)).splitlines(True)
    assert n == want, f'replacement {old[:50]!r}: expected {want}, found {n}'
    counts[old[:40]] = n

assert ''.join(nb['cells'][2]['source']) == orig_embed, 'embedded code blobs changed'
assert "SEED='52'" in ''.join(nb['cells'][1]['source']) and "SEED='50'" not in ''.join(nb['cells'][1]['source'])
out = os.path.join(here, 'DiagRAG_v8_kaggle.ipynb')
json.dump(nb, open(out, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('wrote', out, os.path.getsize(out), 'bytes;', counts)
