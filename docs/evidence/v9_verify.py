"""Verifies the v9 bundle. Read-only. Run from the repository root:  python docs/evidence/v9_verify.py     (needs only the Python standard library)
Checks: (1) every file in kaggle/judged_v9/INPUTS_MANIFEST.json has the recorded size and SHA-256; (2) the frozen code hashes are the ones the protocols state;
(3) each v9 notebook embeds exactly kaggle/diagrag_port3.py and carries the pre-registered seed and settings; (4) diagrag_port3.py differs from the judged diagrag_port2.py by exactly the two declared edits;
(5) the v6 notebook used for v8 still embeds the frozen v6 file. Prints ALL OK or lists every failure."""
import base64, difflib, gzip, hashlib, json, os, re, sys

sha = lambda b: hashlib.sha256(b).hexdigest(); rb = lambda p: open(p, 'rb').read(); fails = []


def check(name, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + name + (('  ' + detail) if detail else ''))
    if not cond: fails.append(name)


M = json.load(open('kaggle/judged_v9/INPUTS_MANIFEST.json'))
def frozen_part(p):
    t = open(p, encoding='utf-8').read(); cut = re.search(r'\n## \d+\. Amendments', t); body = t[:cut.start()] if cut else t
    return len(body.encode('utf-8')), sha(body.encode('utf-8'))


for p, e in M['protocols'].items():
    check(f'protocol (pre-registered part, amendments excluded): {p}', os.path.exists(p) and frozen_part(p) == (e['frozen_part_bytes'], e['frozen_part_sha256']), frozen_part(p)[1][:12] if os.path.exists(p) else 'missing')
for sect in ('frozen_code', 'notebooks', 'analysis_scripts', 'committed_analysis_inputs', 'committed_analysis_outputs'):
    for p, e in M[sect].items():
        if not os.path.exists(p): check(f'{sect}: {p} exists', False); continue
        b = rb(p); check(f'{sect}: {p}', len(b) == e['bytes'] and sha(b) == e['sha256'], sha(b)[:12])
H = M['frozen_hashes']
check('port2 hash is the one the judged SciFact and FiQA runs recorded', sha(rb('kaggle/diagrag_port2.py')) == H['diagrag_port2'] == json.load(open('kaggle/judged_port2_scifact/PORT_PROTOCOL.json'))['code_sha256'] == json.load(open('kaggle/judged_port2_fiqa/PORT_PROTOCOL.json'))['code_sha256'])
check('port3 hash equals the hash in v9_protocol.md', sha(rb('kaggle/diagrag_port3.py')) == H['diagrag_port3'] == re.findall(r'frozen port3 hash is `([0-9a-f]{64})`', open('docs/evidence/v9_protocol.md', encoding='utf-8').read())[-1])
check('v6 hash equals the last hash in v6_protocol.md', sha(rb('kaggle/diagrag_v6.py')) == H['diagrag_v6'] == re.findall(r'frozen v6 hash is now `([0-9a-f]{64})`', open('docs/evidence/v6_protocol.md', encoding='utf-8').read())[-1])
check('v7 hash equals the last hash in v7_composed_protocol.md', sha(rb('kaggle/diagrag_v7.py')) == H['diagrag_v7'] == re.findall(r'frozen v7 hash is now `([0-9a-f]{64})`', open('docs/evidence/v7_composed_protocol.md', encoding='utf-8').read())[-1])

# port3 = port2 + the two declared edits
a = open('kaggle/diagrag_port2.py', encoding='utf-8').read().splitlines(); b = open('kaggle/diagrag_port3.py', encoding='utf-8').read().splitlines()
d = [l for l in difflib.unified_diff(a, b, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
rem = [l for l in d if l[0] == '-']; add = [l for l in d if l[0] == '+']
check('port3 differs from port2 by exactly 2 removed and 4 added lines', len(rem) == 2 and len(add) == 4, f'{len(rem)} removed, {len(add)} added')
check('the added lines are only the two corpora and the output folder name', all(('nfcorpus=' in l or 'arguana=' in l or "'port3_" in l or 'port3_' in l or 'fiqa=' in l) for l in add))

# notebooks embed the frozen port3 file and the pre-registered settings
PRE = dict(nfcorpus='53', arguana='54')
for ds, seed in PRE.items():
    nb = json.load(open(f'kaggle/DiagRAG_v9_port_{ds}.ipynb')); g = {}; exec(''.join(nb['cells'][2]['source']), g); e = g['EMBED']; raw = gzip.decompress(base64.b64decode(''.join(e['b64'])))
    check(f'notebook {ds} embeds exactly diagrag_port3.py', raw == rb('kaggle/diagrag_port3.py') and sha(raw) == e['sha256'] == H['diagrag_port3'])
    cfg = ''.join(nb['cells'][1]['source']); want = f"CONFIG = dict(DATASET='{ds}', SEED='{seed}', N_QUERIES='2500', N_HARD='50', MAX_ATT='2500', N_HARM='20', TIME_BUDGET='36000')"
    check(f'notebook {ds} carries the pre-registered seed and settings', want in cfg)
nb6 = json.load(open('kaggle/DiagRAG_v8_kaggle.ipynb')); g = {}; exec(''.join(nb6['cells'][2]['source']), g)
check('v8 notebook embeds the frozen v6 file', g['EMBED']['diagrag_v6.py']['sha256'] == H['diagrag_v6'])
check('v8 notebook carries seed 52', "SEED='52'" in ''.join(nb6['cells'][1]['source']))
print('\nRESULT:', 'ALL OK' if not fails else f'{len(fails)} FAILED: ' + '; '.join(fails)); sys.exit(0 if not fails else 1)
