"""Build the three E1 notebooks of docs/evidence/v14_flagship_protocol.md: kaggle/DiagRAG_v14_seed{71,72,73}.ipynb.
Each is DiagRAG_v6_kaggle.ipynb (frozen v6 code 44176b9a...e28a) with ONLY the seed and the labels changed (every replacement asserted, embedded code blobs asserted unchanged).
usage: python kaggle/mk_v14_seed_notebooks.py"""
import json, os

here = os.path.dirname(os.path.abspath(__file__))
for seed in ('71', '72', '73'):
    nb = json.load(open(os.path.join(here, 'DiagRAG_v6_kaggle.ipynb'), encoding='utf-8')); orig_embed = ''.join(nb['cells'][2]['source'])
    REPL = [("CONFIG = dict(SEED='50',", f"CONFIG = dict(SEED='{seed}',", 1),
            ("# DiagRAG v6 on Kaggle: one file, the pre-registered judged run (seed 50)",
             f"# DiagRAG v14 E1: the frozen v6 code on an untouched seed ({seed}), pre-registered in docs/evidence/v14_flagship_protocol.md", 1),
            ("These are the pre-registered v6 settings (seed 50, docs/evidence/v6_protocol.md section 3). The protocol allows ONE GPU run and ONE CPU replication at seed 50; do not change SEED to shop for a verdict.",
             f"These are the v6 settings with ONE change, the seed ({seed}), pre-registered in docs/evidence/v14_flagship_protocol.md (E1). One GPU run per seed; seeds 71, 72 and 73 are read together under the seed-averaged rule R-avg; do not change SEED to shop for a verdict.", 1)]
    for old, new, want in REPL:
        n = 0
        for c in nb['cells']:
            s = ''.join(c['source'])
            if old in s: n += s.count(old); c['source'] = s.replace(old, new).splitlines(True)
        assert n == want, f'replacement {old[:50]!r}: expected {want}, found {n}'
    assert ''.join(nb['cells'][2]['source']) == orig_embed, 'embedded code blobs changed'
    assert f"SEED='{seed}'" in ''.join(nb['cells'][1]['source']) and "SEED='50'" not in ''.join(nb['cells'][1]['source'])
    p = os.path.join(here, f'DiagRAG_v14_seed{seed}.ipynb'); json.dump(nb, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False); print('wrote', p)
