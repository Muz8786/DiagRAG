"""Verifies the v11.a bundle (docs/evidence/v11_protocol.md). Read-only; standard library only. Run from the repository root:  python docs/evidence/v11_verify.py
Checks: frozen code hashes against the protocol, port4 = port3 + exactly the two declared edits, both notebooks embed the frozen files and carry the pre-registered seeds and settings,
the v6 notebook for R1 differs from the judged v6 notebook only in the seed and labels, and NO secret-looking string is present in any v11 file. Prints ALL OK or lists every failure."""
import base64, difflib, gzip, hashlib, json, os, re, sys

sha = lambda b: hashlib.sha256(b).hexdigest(); rb = lambda p: open(p, 'rb').read(); rt = lambda p: open(p, encoding='utf-8').read(); fails = []


def check(name, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + name + (('  ' + detail) if detail else ''))
    if not cond: fails.append(name)


P = rt('docs/evidence/v11_protocol.md'); last = lambda pat: (re.findall(pat, P) or [None])[-1]
H = dict(port4=last(r'frozen port4 hash is `([0-9a-f]{64})`'), v6='44176b9a5ad633e39ec29581237d9919619b9944471178effb172be1d276e28a', port3='677a2f38f24a5b0d64849e95930c93ecfd944e28d708753930fde1b2d3a77ada',
         port2='ec113b047d2f13caa194713e6e71cbbafc730554460cbcd4820acf25a19134e0')
check('port4 hash in the protocol equals kaggle/diagrag_port4.py', H['port4'] == sha(rb('kaggle/diagrag_port4.py')), (H['port4'] or 'none')[:12])
check('port3 and port2 are the frozen earlier files', sha(rb('kaggle/diagrag_port3.py')) == H['port3'] and sha(rb('kaggle/diagrag_port2.py')) == H['port2'])
check('v6 is the frozen v6 file', sha(rb('kaggle/diagrag_v6.py')) == H['v6'] == re.findall(r'frozen v6 hash is now `([0-9a-f]{64})`', rt('docs/evidence/v6_protocol.md'))[-1])
a = rt('kaggle/diagrag_port3.py').splitlines(); b = rt('kaggle/diagrag_port4.py').splitlines(); d = [l for l in difflib.unified_diff(a, b, lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
rem = [l for l in d if l[0] == '-']; add = [l for l in d if l[0] == '+']
check('port4 differs from port3 by exactly 2 removed and 3 added lines', len(rem) == 2 and len(add) == 3, f'{len(rem)} removed, {len(add)} added')
check('the added lines are only the SCIDOCS entry, the arguana comma and the output folder name', all(('scidocs=' in l or 'port4_' in l or 'arguana=' in l) for l in add))
nb = json.load(open('kaggle/DiagRAG_v11a_port_scidocs.ipynb')); g = {}; exec(''.join(nb['cells'][2]['source']), g); e = g['EMBED']; raw = gzip.decompress(base64.b64decode(''.join(e['b64'])))
check('port notebook embeds exactly diagrag_port4.py', raw == rb('kaggle/diagrag_port4.py') and sha(raw) == e['sha256'] == H['port4'])
check('port notebook carries the pre-registered seed and settings', "CONFIG = dict(DATASET='scidocs', SEED='56', N_QUERIES='2500', N_HARD='50', MAX_ATT='2500', N_HARM='20', TIME_BUDGET='36000')" in ''.join(nb['cells'][1]['source']))
nm = json.load(open('kaggle/DiagRAG_v11a_main.ipynb')); n6 = json.load(open('kaggle/DiagRAG_v6_kaggle.ipynb')); gm = {}; exec(''.join(nm['cells'][2]['source']), gm)
check('main notebook embeds the frozen v6 file', gm['EMBED']['diagrag_v6.py']['sha256'] == H['v6'])
check('main notebook carries seed 55 and the v6 settings', "CONFIG = dict(SEED='55', N_BASE_ESCI='6000', N_PRDC='528', N_HARD='100', MAX_ATT='4000', N_HARM='20', TIME_BUDGET='30000')" in ''.join(nm['cells'][1]['source']))
same = [i for i in range(len(n6['cells'])) if ''.join(n6['cells'][i]['source']) == ''.join(nm['cells'][i]['source'])]
check('main notebook differs from the judged v6 notebook only in cells 0 and 1 (title, config)', len(n6['cells']) == len(nm['cells']) and set(range(len(n6['cells']))) - set(same) <= {0, 1}, f'identical cells: {same}')
pat = re.compile(r'(gsk_[A-Za-z0-9]{20,}|AQ\.[A-Za-z0-9_-]{30,}|KGAT_[0-9a-f]{20,}|vck_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{30,}|sk-[A-Za-z0-9]{30,})')
files = ['docs/evidence/v11_protocol.md', 'docs/evidence/v11_verify.py', 'kaggle/mk_port4.py', 'kaggle/mk_v11a_notebooks.py', 'kaggle/diagrag_port4.py', 'kaggle/DiagRAG_v11a_main.ipynb', 'kaggle/DiagRAG_v11a_port_scidocs.ipynb'] + [f for f in ('docs/evidence/v11b_protocol.md', 'docs/evidence/v11_report.py') if os.path.exists(f)]
hits = [(f, m.group(0)[:8]) for f in files for m in pat.finditer(rt(f))]
check('no secret-looking string in any v11 file', not hits, str(hits[:3]))
print('\nRESULT:', 'ALL OK' if not fails else f'{len(fails)} FAILED: ' + '; '.join(fails)); sys.exit(0 if not fails else 1)
