"""Export the composed episodes' telemetry features from a v7 checkpoint for the QML comparison.
usage: python docs/evidence/export_composed_features.py <checkpoint.pkl> <out.jsonl>"""
import json, pickle, sys
R = pickle.load(open(sys.argv[1], 'rb')); C = R['COMPST']['COMP']
n = 0
with open(sys.argv[2], 'w') as fh:
    for c in C:
        if 'feats' not in c: continue
        fh.write(json.dumps(dict(split=c['split'], stratum=c['stratum'], feats={k: float(v) for k, v in c['feats'].items()})) + '\n'); n += 1
print('wrote', n, 'composed rows;', sum(1 for c in C if c.get('split') == 'test' and 'feats' in c), 'test')
