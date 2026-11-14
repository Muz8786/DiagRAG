# DiagRAG core-28 on Kaggle

Three notebooks. Each is a single file with Internet ON, and a GPU is recommended:

| Notebook | What it judges | Latest judged run |
|---|---|---|
| `diagrag_core28.ipynb` (v1) | the 28 core faults | CPU seeds 42 and 43: `judged_cpu_run_seed42/`, `judged_cpu_run_seed43/` |
| `diagrag_v2.ipynb` | v1's 28 + the field-evidenced R25/R26/K11, family-level loop, natural arms NA1–NA6 on never-examined queries | CPU seed 44: `judged_cpu_run_v2_seed44/` |
| `diagrag_port.ipynb` | 20 faults on a second stack (e5-small-v2 + FAISS HNSW + min-max fusion) and a second domain (BEIR SciFact) | CPU seed 7: `judged_port_scifact/` |

Why v2 and the port arm exist, the evidence behind them, and every number below: `../docs/EVIDENCE_AND_NOVELTY_REPORT.md`.

v2 additionally downloads `natural_exclusions_v1.json` from this repository (SHA-256 checked). It needs this branch, or the
file placed next to the notebook.

One notebook, `diagrag_core28.ipynb`, does the whole job: fetch and verify the data,
run the purity checks, generate hard episodes for the 28 core faults, train and gate the
detectors, gate the repairs, and run the closed loop. `diagrag_core28.py` is the same
code as a plain script (`# %%` cells). Rebuild the notebook after editing the script:
`python kaggle/build_notebook.py`.

Fault definitions, detectors and repairs: `../docs/CORE28_FAULTS.md`.

## Run it

1. Kaggle → New Notebook → File → Import Notebook → upload `diagrag_core28.ipynb`.
2. Settings: Accelerator **GPU T4 x1** (or P100), Internet **On**.
3. Run All. No Kaggle dataset is needed. The notebook downloads everything itself:
   - corpus `kb_tier3_186k.jsonl.gz` and cache `embeddings_cache_186k.npz` by gdown from
     the Drive IDs in `data/DATA_MANIFEST.md`. This is the Drive route, not a Kaggle
     dataset upload, because Kaggle decompresses `.gz` files on ingestion.
   - ESCI `shopping_queries_dataset_examples.parquet` from the amazon-science/esci-data GitHub LFS.
   - Webis-QSpell-17 from Zenodo record 3570912.
   - Models from Hugging Face: bge-base-en-v1.5, bge-base-en (v1), all-mpnet-base-v2,
     bge-reranker-large.
4. Every file is checked for exact bytes and SHA-256 before use. A mismatch stops the run.

Expected runtime on a T4: about 3–5 hours. This is an estimate, because no GPU was
available in the build sandbox. The CPU judged run below took about 1 h 50 min of compute
with the small reranker. If the Kaggle session dies, run the notebook again: it resumes
from `diagrag_out/checkpoint.pkl`.

## Judged run

The gates are fixed in code (`GATES`) and written to `JUDGED_PROTOCOL.json` with the
script's SHA-256 before any result exists. At the end, `VERDICT.json` says ADOPTED only if
at least 24/28 repairs and 27/28 detectors pass.

- Detector gate: held-out one-vs-rest AUROC ≥ 0.70 with ≥ 20 held-out positives.
- Repair gate: ≥ 20 hard episodes, Wilson 95% lower bound of rescue ≥ 0.50, and at most
  10% of clean successes lost when the repair is forced on them.

Each fault gets `N_HARD` hard episodes split evenly between train and held-out by quota.
With the default of 80 that is 40 held-out per fault on GPU.

Outside Kaggle, `bash run_local.sh <workdir>` re-runs the script until it finishes. Set
`TIME_BUDGET` (seconds) to cut the run into resumable chunks.

## Outputs (`/kaggle/working/diagrag_out/`)

| File | Contents |
|---|---|
| `VERDICT.json` | counts of detectors/repairs passing, ADOPTED/NOT_ADOPTED, faults not solved |
| `JUDGED_PROTOCOL.json` | gates, config, code SHA-256, written before results |
| `solved.csv` | per fault: detector status, repair status, solved |
| `REPORT.md` | all tables in one readable file |
| `data_verification.json` | bytes + SHA-256 per file, the purity report, fitted thresholds |
| `episodes_summary.csv` | per fault: pool, attempts, not applicable, easy, hard (train/test), hard-episode yield |
| `detector_gates.csv` | per fault: rule or head, positives, AUROC + 95% bootstrap CI, AUROC vs clean only, status |
| `repair_gates.csv` | per fault: hard episodes, rescued, rate + Wilson CI, clean successes lost, status |
| `closed_loop.csv` | held-out: dispatch rate, attribution accuracy, closure; for NONE the net Hit change |
| `episodes.jsonl` | every episode: query, fault config, injected docs (synthetic, truncated), gold ids, features |

## Overrides (environment variables, set before the first cell runs)

`N_BASE_ESCI` (default 4000 on GPU), `N_HARD` (80), `MAX_ATT` (2500), `N_HARM` (60),
`N_PRDC` (528), `RERANKER`, `CE_MAXLEN`, `TIME_BUDGET` (0 = no limit).

## CPU judged runs, 14 Nov 2026

`judged_cpu_run_seed42/` and `judged_cpu_run_seed43/`. Settings: MiniLM-L6 reranker, 2,400 ESCI
queries + 885 ShopNova queries, 50 hard episodes per fault (25 held out). Each folder's
`JUDGED_PROTOCOL.json` holds the SHA-256 of the code that produced it. Seed 43's hash equals the
shipped `diagrag_core28.py`.

| | Seed 42 | Seed 43 |
|---|---|---|
| Detectors / repairs passing | 28 / 27 | 28 / 28 |
| Verdict | ADOPTED | ADOPTED |
| Closed loop, mean closure (τ 5% FPR) | — (old dispatch) | 0.82, clean Hit@5 −0.07 points |
| Do-no-harm guarantee (α 0.005) | — | FAIL: held-out loss 0.0075 |
| Natural misspellings (n = 46) | — | Hit@5 0.283 → 0.304 (corrected query 0.348) |
| Unseen faults, mean closure | — | 0.21 |

Details and the cause of the guarantee failure: `../docs/CORE28_FAULTS.md`. These runs used the
CPU stack. The default GPU stack (bge-reranker-large) needs its own judged run.

## v2 and portability judged runs, 14 Nov 2026 (CPU, MiniLM-L6 reranker)

| | v2 seed 44 | Port SciFact seed 7 |
|---|---|---|
| Detectors passing | 28/28 (v1 faults) | 11/20 (all 11 faults with ≥ 20 held-out positives passed; 7 THIN, 2 not trainable) |
| Repairs passing | 27/28 (Q03 fails the harm bar) | 18/20 |
| New evidenced faults | R25 PASS/PASS, K11 PASS/PASS, R26 THIN (3 hard in 2,500) | R25 PASS/PASS |
| Loop | mean closure 0.83 at 4.5% clean dispatch; do-no-harm L1 **FAIL** (0.0128 > 0.005) | not run |
| Natural arms (1,500 never-examined queries) | duplicate collapse **+5.6 points [+1.6, +10.4]**; chunk-crowding collapse **+4.5 [+2.7, +6.3]**; placeholder demotion **HARM**; full loop +0.07 [−0.33, +0.47] | — |
| Verdict | ADOPTED on the 28 | "suite ports" claim not made (11 < 15) |

Every folder holds its protocol file, with gates and code SHA-256 written before the run. The hashes equal the shipped `.py` files.
