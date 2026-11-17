#!/bin/bash
# Builds the single data zip for the A-to-Z Kaggle notebook:  DiagRAG_KAGGLE_A_to_Z.zip  (PRIVATE USE: contains third-party data, see data/DATA_NOTICE.md)
# It is the run package (code, notebooks, every judged run with its episodes, evidence, benchmark, verifier) plus
#   - DiagRAG_A_to_Z_kaggle.ipynb  : the one Kaggle notebook
#   - A_TO_Z_GUIDE.md              : the detailed guide
#   - prereq/                      : the v6 CPU judged run's checkpoint and the query-log embedding cache, so the composed-fault arm can be regenerated
#   - data/                        : the four input files the judged scripts fetch (exact size and SHA-256 are re-checked by the scripts)
# Run from anywhere:  bash kaggle/build_a_to_z_package.sh     (sandbox paths below)
set -euo pipefail
S=/projects/sandbox; R=$S/DiagRAG; PY=$S/_venv/bin/python; OUTD=$S/deliverables; mkdir -p "$OUTD"
NAME=DiagRAG_KAGGLE_A_to_Z; Z=$S/_final2/$NAME
$PY "$R/kaggle/build_a_to_z_notebook.py"
bash "$S/_work/build_final_zips.sh" > "$S/_work/build_final_zips.log" 2>&1 || { tail -5 "$S/_work/build_final_zips.log"; exit 1; }   # refreshes _final/DiagRAG_RUN_PACKAGE with the current notebook and guide
rm -rf "$S/_final2" && mkdir -p "$Z"
cp -a "$S/_final/DiagRAG_RUN_PACKAGE/." "$Z/"
rm -f "$Z/CHECKSUMS.sha256" "$Z/START_HERE.md"
cp "$R/kaggle/DiagRAG_A_to_Z_kaggle.ipynb" "$Z/"; cp "$R/A_TO_Z_GUIDE.md" "$Z/"
mkdir -p "$Z/prereq" "$Z/data"
cp "$S/_j50/diagrag_out/checkpoint.pkl" "$Z/prereq/v6_cpu_checkpoint.pkl"; cp "$S/_j50/diagrag_out/qlog_nn_b03a9b172742.npy" "$Z/prereq/"
for f in kb_tier3_186k.jsonl.gz embeddings_cache_186k.npz shopping_queries_dataset_examples.parquet corpus-webis-qspell-17.zip; do cp -L "$S/_j47/diagrag_data/$f" "$Z/data/$f"; done
cp "$R/NOTICE.md" "$Z/data/NOTICE.md"
cat > "$Z/data/DATA_NOTICE.md" <<'EOF'
# PRIVATE USE ONLY
These four files are the inputs the judged scripts fetch at run time. They are bundled so a run needs no Google Drive download.
They contain third-party material and project material whose licence is not settled for redistribution:
- `kb_tier3_186k.jsonl.gz` and `embeddings_cache_186k.npz`: the 186,290-document corpus and its embeddings. It includes 84,993 rows whose licence status is `conflicting_unverified` (the judged scripts drop them) and the ShopNova synthetic corpus, whose licence the owner has not assigned.
- `shopping_queries_dataset_examples.parquet`: Amazon ESCI (Apache-2.0). `corpus-webis-qspell-17.zip`: Webis-QSpell-17 (CC BY 4.0). Attribution is in `NOTICE.md`.
**Keep the Kaggle dataset PRIVATE. Do not publish this zip.** Exact sizes and SHA-256 are in `PACKAGE_MANIFEST.json`; the scripts re-check them before use.
EOF
cat > "$Z/prereq/README.md" <<'EOF'
# prereq/: what only the composed-fault arm (v7) needs
- `v6_cpu_checkpoint.pkl`: the checkpoint of the v6 CPU judged run (seed 50, stage `lofo_done`, 9,535 single-fault episodes). `docs/evidence/v7_prepare_checkpoint.py` strips only the attributor-dependent results from it; the episode signature it records must be `a9c93f518338c6be50a1bf5efa0e5f84c0286ca99d617b2857119c35a9e01a2d`.
- `qlog_nn_b03a9b172742.npy`: the cached embeddings of the query log (about 180,000 queries). Without it the script re-encodes them, which takes a long time on CPU.
Stage G of the notebook uses both. Nothing else does.
EOF
cat > "$Z/START_HERE.md" <<'EOF'
# DiagRAG, A to Z (one Kaggle notebook + this data zip)
1. Upload this zip as a PRIVATE Kaggle Dataset. Create a notebook, import `DiagRAG_A_to_Z_kaggle.ipynb`, add the dataset as an input, set Internet On, Run All.
2. Default flags run the check path (about 15 to 25 minutes, CPU, no key). Switch on `RUN_V6_GPU` (GPU T4) or `RUN_V7_CPU` in cell 2 for the long regenerations.
3. `A_TO_Z_GUIDE.md` explains every stage, every result and every limitation. `PROJECT_EXPLAINED.md` is the full project write-up.
No API key is needed or included. The data in `data/` is for private use only (`data/DATA_NOTICE.md`).
EOF
$PY - "$Z" <<'EOF'
import hashlib, json, os, subprocess, sys, time
Z = sys.argv[1]; sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
n = 0; size = 0
for dp, dn, fn in os.walk(Z):
    for f in fn: n += 1; size += os.path.getsize(os.path.join(dp, f))
ref = {'data/kb_tier3_186k.jsonl.gz': 53518791, 'data/embeddings_cache_186k.npz': 533012659, 'data/shopping_queries_dataset_examples.parquet': 51286808, 'data/corpus-webis-qspell-17.zip': 2285705}
for k, v in ref.items(): assert os.path.getsize(os.path.join(Z, k)) == v, ('size mismatch', k)
commit = subprocess.run(['git', '-C', '/projects/sandbox/DiagRAG', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
man = dict(name='DiagRAG_KAGGLE_A_to_Z', built_utc=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()), repo_commit_at_build=commit, n_files=n + 2, size_mb=round(size / 2**20, 1), private_use_only=True,
           data={k: dict(bytes=v, sha256=sha(os.path.join(Z, k))) for k, v in ref.items()},
           prereq={f: dict(bytes=os.path.getsize(os.path.join(Z, 'prereq', f)), sha256=sha(os.path.join(Z, 'prereq', f))) for f in ('v6_cpu_checkpoint.pkl', 'qlog_nn_b03a9b172742.npy')})
json.dump(man, open(os.path.join(Z, 'PACKAGE_MANIFEST.json'), 'w'), indent=1); print(json.dumps(man, indent=1)[:900])
EOF
# secrets and private labels, then checksums, then the zip
find "$Z" -name 'labels_test*' | grep . && { echo "PRIVATE LABELS FOUND"; exit 1; } || echo "no private labels"
if grep -rEIl "KGAT_[A-Za-z0-9]{20}|gsk_[A-Za-z0-9]{20}|AQ\.Ab8R[A-Za-z0-9_-]{10}|sk-[A-Za-z0-9]{32}|AIza[0-9A-Za-z_-]{30}" "$Z" >/dev/null 2>&1; then echo "SECRET FOUND"; exit 1; fi; echo "no secrets"
( cd "$Z" && find . -type f ! -name CHECKSUMS.sha256 | sort | sed 's#^\./##' | while read -r p; do printf '%s  %s\n' "$(sha256sum "$p" | cut -d' ' -f1)" "$p"; done > CHECKSUMS.sha256 )
rm -f "$OUTD/$NAME.zip"; ( cd "$S/_final2" && zip -q -r -1 "$OUTD/$NAME.zip" "$NAME" ); ls -la "$OUTD/$NAME.zip"
cp "$R/kaggle/DiagRAG_A_to_Z_kaggle.ipynb" "$R/A_TO_Z_GUIDE.md" "$OUTD/"
