"""Verify the v8 frozen runner/notebook pair and their protocol hash commitments."""
import ast, base64, gzip, hashlib, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
runner = ROOT / 'kaggle' / 'diagrag_v8.py'
notebook = ROOT / 'kaggle' / 'DiagRAG_v8_kaggle.ipynb'
protocol = ROOT / 'docs' / 'evidence' / 'v8_multilabel_protocol.md'
source = runner.read_bytes(); code_sha = hashlib.sha256(source).hexdigest()
nb_bytes = notebook.read_bytes(); nb_sha = hashlib.sha256(nb_bytes).hexdigest()
text = protocol.read_text(encoding='utf-8')
assert f'`{code_sha}` (`kaggle/diagrag_v8.py`)' in text
assert f'`{nb_sha}` (`kaggle/DiagRAG_v8_kaggle.ipynb`)' in text
ast.parse(source.decode('utf-8'))
nb = json.loads(nb_bytes)
assert nb['nbformat'] == 4 and nb['metadata']['kaggle']['isInternetEnabled']
assert nb['metadata']['kaggle']['accelerator'] == 'none'
embed_cell = next(c for c in nb['cells'] if c['cell_type'] == 'code' and 'EMBED = dict(' in ''.join(c['source']))
ns = {}
exec(''.join(embed_cell['source']), ns)
embedded = gzip.decompress(base64.b64decode(''.join(ns['EMBED']['b64'])))
assert embedded == source
assert ns['EMBED']['sha256'] == code_sha and ns['EMBED']['size'] == len(source)
assert "OUT = os.path.join(WORK, 'diagrag_v8_out')" in source.decode('utf-8')
assert "COMP_SEED = 52" in source.decode('utf-8')
assert 'COMP_QUOTA_SCALE' not in source.decode('utf-8')
secret_pattern = re.compile(rb'(KGAT_[A-Za-z0-9_-]{20,}|coa_[A-Za-z0-9_-]{20,}|KAGGLE_KEY\s*=\s*[\"\'][^\"\']+)')
check_paths = [runner, notebook, protocol, ROOT/'kaggle'/'mk_v8.py', ROOT/'kaggle'/'build_v8_notebook.py',
               ROOT/'kaggle'/'v8_cells'/'composed_gen.py', ROOT/'kaggle'/'v8_cells'/'composed_eval.py',
               ROOT/'docs'/'evidence'/'preflight_v8.py']
assert not any(secret_pattern.search(path.read_bytes()) for path in check_paths)
print(json.dumps(dict(status='PASS', runner_sha256=code_sha, notebook_sha256=nb_sha,
                      embedded_runner_bytes=len(embedded), protocol_hashes_match=True, secret_scan='PASS'), indent=2))
