# DiagRAG core-28 on Kaggle

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

## CPU judged run, 14 Nov 2026 (`judged_cpu_run/`)

Settings: MiniLM-L6 reranker instead of bge-reranker-large, 2,400 real ESCI queries +
885 ShopNova queries, 50 hard episodes per fault (25 train / 25 held-out). Code SHA-256
b60462fb…163ad, which equals the shipped `diagrag_core28.py`.

| | Result |
|---|---|
| Detectors passing | 28 / 28 (lowest AUROC: C2 0.81, K04 0.84, Q03 0.87) |
| Repairs passing | 27 / 28. Q03 fails: 28/50 rescued, Wilson lower bound 0.42 |
| Solved (both) | 27 / 28 |
| Verdict | ADOPTED (targets 24 repairs, 27 detectors) |
| Clean successes lost to any repair | 0 of 20 per fault |
| Closed loop on clean held-out traffic | 10.3% of queries get a repair, net Hit@5 −1.1 points |

This run used the CPU stack. The Kaggle notebook's default GPU stack (bge-reranker-large)
has to be judged on its own run.
