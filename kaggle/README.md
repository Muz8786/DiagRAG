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

Expected runtime on a T4 is roughly 2–4 hours. This estimate is not measured: no GPU
run was possible from the build sandbox. To get a quick first pass, add a cell at the top
with `os.environ['N_BASE_ESCI']='1500'; os.environ['N_HARD']='40'; os.environ['MAX_ATT']='600'`.

## Outputs (`/kaggle/working/diagrag_out/`)

| File | Contents |
|---|---|
| `REPORT.md` | all tables in one readable file |
| `data_verification.json` | bytes + SHA-256 per file, the purity report, fitted thresholds |
| `episodes_summary.csv` | per fault: pool, attempts, not applicable, easy, hard, hard-episode yield |
| `detector_gates.csv` | per fault: rule or head, train/test positives, AUROC + 95% bootstrap CI, AUROC vs clean only, PASS/FAIL/THIN |
| `repair_gates.csv` | per fault: hard episodes, rescued, rate + Wilson CI, harm on clean successes |
| `closed_loop.csv` | per fault on the held-out split: dispatch rate, attribution accuracy, closure; for NONE, the net Hit change |
| `episodes.jsonl` | every episode: query, fault config, injected docs (synthetic, truncated), gold ids, features |

## Overrides (environment variables, set before the first cell runs)

`N_BASE_ESCI` (default 4000), `N_HARD` (80), `MAX_ATT` (1500), `N_HARM` (60), `N_PRDC` (528),
`RERANKER`, `CE_MAXLEN`.

## CPU validation already done

`cpu_validation/` holds the outputs of a full run on CPU on 14 Nov 2026. That run used the
MiniLM-L6 reranker instead of bge-reranker-large, 350 ESCI base queries, and 10 hard
episodes per fault. Its purpose was to prove that every stage runs. Its numbers are not
results: the test split has 1–6 positives per fault, so most rows say THIN.
