"""Equivalence check for the port5 execution fix (kaggle/mk_port5.py edit 3). Compares two port output folders produced with the SAME dataset, seed, settings and thread count:
corpus embeddings (exact array equality), PORT_VERDICT.json (every field except the code hash and the output-folder name), and every port_*.csv (byte equality).
usage: python docs/evidence/v13_port5_equivalence.py <out_dir_A> <out_dir_B>     exit 0 only if everything is identical"""
import json, os, sys
import numpy as np

a, b = sys.argv[1], sys.argv[2]; ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(('SAME ' if cond else 'DIFF ') + name)
check('corpus_e5.npy (exact array equality)', np.array_equal(np.load(os.path.join(a, 'corpus_e5.npy')), np.load(os.path.join(b, 'corpus_e5.npy'))))
va, vb = json.load(open(os.path.join(a, 'PORT_VERDICT.json'))), json.load(open(os.path.join(b, 'PORT_VERDICT.json')))
strip = lambda v: {k: x for k, x in v.items() if k != 'protocol'}
check('PORT_VERDICT.json (all fields except the embedded protocol)', strip(va) == strip(vb))
for f in sorted(x for x in os.listdir(a) if x.startswith('port_') and x.endswith('.csv')):
    check(f, open(os.path.join(a, f), 'rb').read() == open(os.path.join(b, f), 'rb').read())
print('EQUIVALENCE:', 'IDENTICAL' if ok else 'NOT IDENTICAL'); sys.exit(0 if ok else 1)
