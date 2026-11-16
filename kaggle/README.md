# DiagRAG core-28 on Kaggle

Every notebook is a single file. Internet must be ON. Use a GPU (T4 x1) for the v3/v4 flagship runs.
**The flagship is `diagrag_v4.ipynb`.** The older notebooks stay because each judged run is pinned to the exact file that produced it.

| Notebook | What it judges | Judged run (folder) |
|---|---|---|
| `diagrag_core28.ipynb` (v1) | the 28 core faults | CPU seeds 42 and 43: `judged_cpu_run_seed42/`, `judged_cpu_run_seed43/` |
| `diagrag_v2.ipynb` | v1's 28 + field-evidenced R25/R26/K11, family-level loop, natural arms NA1-NA6 | CPU seed 44: `judged_cpu_run_v2_seed44/` |
| `diagrag_v3.ipynb` | v2 + licence-clean corpus, evidence tiers, Q03 from real query pairs, K12/R26 testbeds, Mondrian conformal do-no-harm, natural traffic, prevalence census, external baselines (RAGLog tier-0, QPP, SymSpell, wordsegment) | CPU seed 45: `judged_cpu_run_v3_seed45/`; **GPU T4, bge-reranker-large, seed 46: `judged_gpu_v3_seed46/`** |
| `diagrag_v4.ipynb` | v3 + group-level attributor and a larger K fallback (written after the v3 results, then frozen) | CPU seed 47: `judged_cpu_run_v4_seed47/`; GPU seed 48: see "v4 GPU" below |
| `diagrag_port2.ipynb` | stack 2 on SciFact and FiQA (`DATASET=scifact` or `fiqa`) | `judged_port2_scifact/`, `judged_port2_fiqa/` |
| `diagrag_langchain.ipynb` (v1) | 15 faults injected through real LangChain components | `judged_langchain_scifact/` (7/15, claim FAILED) |
| `diagrag_langchain2.ipynb` | same 15 faults after fixes designed from the v1 results | `judged_langchain_v2_scifact/` (11/15, exactly at the bar of 11) |
| `diagrag_port.ipynb` | 20 faults on a second stack and a second domain (SciFact) | CPU seed 7: `judged_port_scifact/` (11/20) |
| (script) `../bench/llm_baselines.py` | RAGLog-style LLM diagnosis and CRAG-style LLM repair against DiagRAG | `judged_llm_baselines/`, `../docs/LLM_BASELINES_RESULTS.md` |

Why v2 and the port arm exist, the evidence behind them, and every number below: `../docs/EVIDENCE_AND_NOVELTY_REPORT.md`.
The v3 roadmap execution, with every v3/port2/LangChain number: `../docs/ROADMAP_V3.md`. The benchmark release: `../bench/`.
v3 and v4 download `natural_exclusions_v2.json` from this repository (SHA-256 checked). v2 downloads `natural_exclusions_v1.json`.
Either file can also be placed next to the notebook.

The v1 notebook, `diagrag_core28.ipynb`, shows the whole job in one file: fetch and verify the data,
run the purity checks, generate hard episodes for the 28 core faults, train and gate the
detectors, gate the repairs, and run the closed loop. `diagrag_core28.py` is the same
code as a plain script (`# %%` cells). Rebuild the notebook after editing the script:
`python kaggle/build_notebook.py`.

Fault definitions, detectors and repairs: `../docs/CORE28_FAULTS.md`.

## Run it

1. Kaggle → New Notebook → File → Import Notebook → upload `diagrag_v4.ipynb` (or any notebook in the table).
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

Runtime on a T4: the v3 GPU run (seed 46) took about 2 hours with the settings in the launcher
(N_BASE_ESCI 2400, N_PRDC 528, N_HARD 50, MAX_ATT 2500, N_HARM 20). The defaults listed under
"Overrides" are larger and will take longer; set the overrides to reproduce the judged runs.
If the Kaggle session dies, run the notebook again: it resumes from `diagrag_out/checkpoint.pkl`.

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
CPU stack. The GPU stack (bge-reranker-large) was judged separately: `judged_gpu_v3_seed46/`.

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
