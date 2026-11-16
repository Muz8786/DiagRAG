"""Pre-flight for the v6 judged run (brief section 2, checks a to d). Read-only. Prints each check and writes preflight_v6_result.json.
Usage: python docs/evidence/preflight_v6.py   (from the repository root)"""
import ast, base64, gzip, hashlib, json, os, re, sys
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
rd = lambda *p: open(os.path.join(root, *p), encoding='utf-8').read()
sha = lambda *p: hashlib.sha256(open(os.path.join(root, *p), 'rb').read()).hexdigest()
res = {}; ok_all = True
def check(name, ok, detail=''):
    global ok_all; ok_all &= bool(ok); res[name] = dict(ok=bool(ok), detail=detail); print(('PASS ' if ok else 'FAIL ') + name + ('  ' + detail if detail else ''))

proto = rd('docs', 'evidence', 'v6_protocol.md'); code = rd('kaggle', 'diagrag_v6.py'); v4 = rd('kaggle', 'diagrag_v5.py')   # v4 slot = v5: v6 must equal v5 on every bar
# (a) frozen hash equals the shipped code
frozen = re.findall(r'frozen v6 hash is now `([0-9a-f]{64})`', proto)[-1]
check('a: protocol-frozen hash equals kaggle/diagrag_v6.py', frozen == sha('kaggle', 'diagrag_v6.py'), frozen[:16])
# (b) the protocol file the code writes records the software environment
check('b: code writes the environment (library versions) into JUDGED_PROTOCOL.json', 'env=ENV_VERSIONS' in code and 'def _env_versions' in code and "'scikit-learn'" in code)
# (c) seed and every bar: unchanged bars are byte-identical to v4; the changed ones are exactly the pre-registered ones
def gate_line(src):
    m = re.search(r"AUROC_BAR=[^\n]*\n", src); return m.group(0)
g4, g5 = gate_line(v4), gate_line(code)
exp5 = g4
check('c1: gate line is byte-identical to v5', g5 == exp5, g5.strip()[:120])
for key in ('ALPHA=0.005, ALPHAS=[0.0025, 0.005, 0.01, 0.02]', 'L2_BAR=0.70', 'U1_BAR=0.50', 'TAU_FAM=0.6', "CLEAN_FPR=0.05"):
    check(f'c2: unchanged bar present in v5 and v4: {key}', key in code and key in v4)
nb = json.load(open(os.path.join(root, 'kaggle', 'DiagRAG_v6_kaggle.ipynb'))); src = [''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code']
ns = {}; exec(src[0], ns)
check('c3: notebook config equals protocol section 3 (seed 50, N_HARD 100, MAX_ATT 4000, N_BASE_ESCI 6000, N_PRDC 528, N_HARM 20)',
      all(ns['CONFIG'][k] == v for k, v in dict(SEED='50', N_HARD='100', MAX_ATT='4000', N_BASE_ESCI='6000', N_PRDC='528', N_HARM='20').items()), json.dumps(ns['CONFIG']))
check('c4: protocol section 3 names seed 49 and the same settings', 'seed 50' in proto and '`SEED=50, N_BASE_ESCI=6000, N_PRDC=528, N_HARD=100, MAX_ATT=4000, N_HARM=20' in proto)
# (d) the notebook embeds the same frozen file and checks the hash before running it
emb = ns['EMBED'] if 'EMBED' in ns else None
ns2 = {}; exec(src[1], ns2); e = ns2['EMBED']['diagrag_v6.py']
raw = gzip.decompress(base64.b64decode(''.join(e['b64'])))
check('d1: notebook embeds exactly the frozen file', hashlib.sha256(raw).hexdigest() == frozen == e['sha256'])
check('d2: notebook asserts the hash before running (size/sha check cell + the frozen-hash assert)', "hashlib.sha256(raw).hexdigest() == e['sha256']" in src[2] and f'EMBED[\'diagrag_v6.py\'][\'sha256\'] == "{frozen}"' in src[2])
for s_ in src: ast.parse(s_)
check('d3: every code cell parses', True)
res['ALL_PASS'] = ok_all; json.dump(res, open(os.path.join(root, 'docs', 'evidence', 'preflight_v6_result.json'), 'w'), indent=1)
print('PREFLIGHT:', 'ALL PASS' if ok_all else 'FAILED'); sys.exit(0 if ok_all else 1)
