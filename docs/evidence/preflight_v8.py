"""Synthetic-only structural preflight for the v8 dispatcher; no project data or judged result."""
import ast
import collections
import json
import pathlib
import hashlib
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'kaggle' / 'diagrag_v8.py'
tree = ast.parse(SCRIPT.read_text(encoding='utf-8'))
wanted = {'dispatch_v7', 'dispatch_v3'}
nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in wanted]
assert {n.name for n in nodes} == wanted

class Model:
    def __init__(self, classes, p): self.classes_, self.p = classes, np.asarray(p, dtype=float)
    def predict_proba(self, _): return self.p.reshape(1, -1)

def noop(*args, **kwargs): return ('repair',)

ns = dict(np=np, collections=collections, FEATS=[], CLS=['NONE', 'Q02', 'Q04', 'K04', 'R01'], iN=0,
          GROUP={'Q02':'Q', 'Q04':'Q', 'K04':'K', 'R01':'R'},
          FAMILY={'Q02':'Q02', 'Q04':'Q04', 'K04':'K04', 'R01':'R01'},
          GROUP_REPAIR={g: noop for g in 'QKR'}, fam_repair=lambda label: noop,
          RULE_PRIO=[], RULE_FIRE={}, TAU_C2=0.99, TAU2=0.20,
          CFG={'TAU_FAM':0.6}, ATTG=Model(['NONE','Q','K','R'], [0.05,0.80,0.10,0.05]),
          lab_group=lambda label: label[1] if label.startswith('G') else label[0])
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SCRIPT), 'exec'), ns)
p = np.array([0.05, 0.50, 0.25, 0.10, 0.10])
v7, _ = ns['dispatch_v7'](p, {}, ns['CLS'], 0, ns['ATTG'])
v8, _ = ns['dispatch_v3'](p, {}, ns['CLS'], 0, ns['ATTG'])
assert [label for label, _ in v7] == ['Q02'], [label for label, _ in v7]
assert [label for label, _ in v8] == ['Q02', 'Q04'], [label for label, _ in v8]

# Verify the hard cap and extra-per-group rule on a synthetic three-cause vector.
ns['TAU2'] = 0.10
ns['TAU_C2'] = 0.05
ns['ATTG'] = Model(['NONE','Q','K','R'], [0.03,0.47,0.30,0.20])
p3 = np.array([0.03, 0.25, 0.22, 0.30, 0.20])
three, _ = ns['dispatch_v3'](p3, {}, ns['CLS'], 0, ns['ATTG'])
labels = [label for label, _ in three]
assert len(labels) <= 3 and len(labels) == 3, labels
base3, _ = ns['dispatch_v7'](p3, {}, ns['CLS'], 0, ns['ATTG'])
extra_groups = [ns['lab_group'](label) for label in labels[len(base3):]]
assert len(extra_groups) == len(set(extra_groups)), extra_groups

result = dict(status='PASS', scope='synthetic dispatcher only; no data, training, or judged results',
              checks=['same-letter secondary label is added', 'output cap is three', 'at most one extra label per letter group'],
              v7_labels=[x[0] for x in v7], v8_same_letter_labels=[x[0] for x in v8],
              synthetic_three_labels=labels, v8_sha256=hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
out = ROOT / 'docs' / 'evidence' / 'preflight_v8_result.json'
out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
