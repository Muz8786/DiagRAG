"""Pre-flight for the v7 composed-fault arm. Read-only. Usage: python docs/evidence/preflight_v7.py (repository root)."""
import ast, hashlib, json, os, re, sys
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); rd = lambda *p: open(os.path.join(root, *p), encoding='utf-8').read()
sha = lambda *p: hashlib.sha256(open(os.path.join(root, *p), 'rb').read()).hexdigest(); res = {}; ok_all = True
def check(n, ok, d=''):
    global ok_all; ok_all &= bool(ok); res[n] = dict(ok=bool(ok), detail=d); print(('PASS ' if ok else 'FAIL ') + n + ('  ' + d if d else ''))
proto = rd('docs', 'evidence', 'v7_composed_protocol.md'); v7 = rd('kaggle', 'diagrag_v7.py'); v6 = rd('kaggle', 'diagrag_v6.py')
fr = re.findall(r'frozen v7 hash is now `([0-9a-f]{64})`', proto); check('a: protocol-frozen v7 hash equals kaggle/diagrag_v7.py', bool(fr) and fr[-1] == sha('kaggle', 'diagrag_v7.py'), fr[-1][:16] if fr else 'no hash in the protocol')
g = lambda src: re.search(r"AUROC_BAR=[^\n]*\n", src).group(0)
check('b: gate line byte-identical to v6', g(v7) == g(v6))
for key in ('ALPHA=0.005, ALPHAS=[0.0025, 0.005, 0.01, 0.02]', 'L2_BAR=0.70', 'U1_BAR=0.50', 'TAU_FAM=0.6', 'CLEAN_FPR=0.05'): check(f'b2: unchanged bar present: {key}', key in v7 and key in v6)
check('c: composed seed 51 and quotas 20/15 in code and protocol', "COMP_SEED = int(os.environ.get('COMP_SEED', 51))" in v7 and "'WITHIN_FAMILY': 20" in v7 and "'TRIPLE': 15" in v7 and 'Seed 51' in proto)
check('d: composed arm never writes into EPIS', 'EPIS.append' not in rd('kaggle', 'v7_cells', 'composed_gen.py') and 'EPIS.append' not in rd('kaggle', 'v7_cells', 'composed_eval.py'))
check('e: LOFO fits unchanged (single-fault rows only)', "keep_ = ytra != f; mf = hgb().fit(Xtra[keep_], ytra[keep_])" in v7)
import difflib
v6l = v6.splitlines(); v7l = v7.splitlines(); removed = [l for l in difflib.unified_diff(v6l, v7l, lineterm='', n=0) if l.startswith('-') and not l.startswith('---')]
ALLOWED_REMOVED = ("# # DiagRAG v6", "ATT = hgb().fit(Xtra, ytra)", "    mm = hgb().fit(Xtra[a_], ytra[a_]); p_ = mm.predict_proba(Xtra[b_])", "    mm = hgb().fit(Xtra[a_], to_group(ytra[a_])); p_ = mm.predict_proba(Xtra[b_])", "ATTG = hgb().fit(Xtra, to_group(ytra))",
                   "    keep = {k: globals()[k] for k in", "    DETF = {}", "        DETF[id(e)] = row", "md = ['# DiagRAG v6", "               guarantee=GUARANTEE, policies=POLICY,")
bad = [l for l in removed if not any(l[1:].lstrip().startswith(a.lstrip()) or a.lstrip() in l for a in ALLOWED_REMOVED) and l[1:].strip()]
check('f: every line REMOVED from v6 is one of the declared edits (header, attributor fits, checkpoint keys, report title, verdict key)', not bad, ('unexpected: ' + str(bad[:3])[:200]) if bad else f'{len(removed)} removed lines, all declared')
ast.parse(v7); check('g: v7 parses', True); res['ALL_PASS'] = ok_all
json.dump(res, open(os.path.join(root, 'docs', 'evidence', 'preflight_v7_result.json'), 'w'), indent=1); print('PREFLIGHT:', 'ALL PASS' if ok_all else 'FAILED'); sys.exit(0 if ok_all else 1)
