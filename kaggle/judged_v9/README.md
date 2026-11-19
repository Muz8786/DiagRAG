# v9: frozen bundle, inputs, and where the owner's results go

**Read first:** `docs/evidence/v9_protocol.md` (the pre-registration; written before any v9 run). Every input and frozen file, with size and SHA-256, is in `INPUTS_MANIFEST.json`.

## Run order (by the owner)
1. `python docs/evidence/v9_verify.py` from the repository root. Must print `RESULT: ALL OK`.
2. Kaggle, Internet On, GPU T4 (or CPU), **Run All, one run each, no setting changed:**
   - `kaggle/DiagRAG_v9_port_nfcorpus.ipynb` (BEIR NFCorpus, seed 53)
   - `kaggle/DiagRAG_v9_port_arguana.ipynb` (BEIR ArguAna, seed 54)
3. Copy each run's `port3_<dataset>_out/` into `kaggle/judged_port3_nfcorpus/` and `kaggle/judged_port3_arguana/`.
4. Check each `PORT_PROTOCOL.json`: `code_sha256` = `677a2f38f24a5b0d64849e95930c93ecfd944e28d708753930fde1b2d3a77ada`, `cfg` as in the manifest. If not, say the run is not the pre-registered one.
5. Add a dated amendment to `v9_protocol.md` section 8 with the scorecard against section 4, written after the results. Do not edit sections 1 to 7.
6. v8 (seed 52, Kaggle kernel `syedmuzammilquadri/diagrag-v8-gpu-seed52`): save its output to `kaggle/judged_gpu_v8_seed52/`, run `python docs/evidence/v8_audit.py kaggle/judged_gpu_v8_seed52 docs/evidence/v8_audit_v8gpu.json` (scikit-learn 1.6.1), and add its verdict to `docs/ALL_RUNS_MATRIX.md`.

## Results already in the repository (inputs to nothing new; re-runnable)
- v6 GPU and CPU (seed 50), v7 composed arm (seed 51), LLM baselines, v6 hygiene audit, emergent-failure breakdown, v7 hash trail. See the protocol's table in section 1.

## Not in v9
Frontier-LLM arm, document-text supervised baseline, multi-label dispatcher, composed-arm repeat, local LLM arm, full-suite port, density-matched control, benchmark release. See protocol section 5.

## Caveats the manifest records
- The frozen script does **not** pin model revisions or library versions; the revisions observed on 19 Nov 2026 are listed in the manifest.
- Smoke tests of the port notebooks were run in a CPU sandbox with tiny settings; **their numbers are not used anywhere.**
