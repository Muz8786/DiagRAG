"""Check the public files of a DiagRAG-Bench release against MANIFEST.json (SHA-256). Usage: python verify_release.py release_v1
Also prints the commitment to the private test labels; the labels themselves are not in the package."""
import hashlib, json, os, sys
rel = sys.argv[1]; m = json.load(open(os.path.join(rel, 'MANIFEST.json'))); bad = 0
for name, h in m['files'].items():
    p = os.path.join(rel, name); ok = os.path.exists(p) and hashlib.sha256(open(p, 'rb').read()).hexdigest() == h
    print(('ok       ' if ok else 'MISMATCH ') + name); bad += (not ok)
print('private test labels are NOT included. Their SHA-256 commitment:', m['private_test_labels_sha256'])
assert not os.path.exists(os.path.join(rel, 'labels_test.jsonl')), 'labels_test.jsonl must not be in a public release'
print('RESULT:', 'ALL OK' if not bad else f'{bad} PROBLEM(S)'); sys.exit(1 if bad else 0)
