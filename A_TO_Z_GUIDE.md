# DiagRAG, A to Z

One Kaggle notebook (`DiagRAG_A_to_Z_kaggle.ipynb`) plus one data zip (`DiagRAG_KAGGLE_A_to_Z.zip`) run the whole project: check every file, re-fit every detector, show every stored result, run the optional simulated-QML comparison and the benchmark, and (if you switch them on) regenerate the pre-registered v6 GPU run and the composed-fault arm. This guide explains what is in the zip, how to run it, what every stage does, and what the results mean, including the failures.

Read section 0 first. It is one page.

---

## 0. One page

**The problem.** A RAG system (retrieval-augmented generation) answers from documents it retrieves. When it answers badly, the cause is often in the retrieval stage: a misspelled query, duplicate documents, a stale vector index, a reranker returning garbage. The system rarely says so, and an LLM check on every query is slow and costs money.

**The idea.** Use only the *telemetry* the retrieval stage already produces (score gaps, rank agreement between the dense and keyword legs, duplicate counts, cheap probes; 63 numbers per query). From it: (1) say whether retrieval failed, (2) say which of 32 known fault types caused it, (3) apply a targeted repair, and (4) promise, with a conformal bound, not to hurt queries that were fine. No generated answer and no LLM call are needed at run time.

**What the evidence says.**
- The pre-registered v6 flagship (GPU, seed 50) is **ADOPTED**: 27 of 28 core detectors and 27 of 28 repairs (the rule needs 27 and 24). A CPU replication at the same seed is also ADOPTED (28 and 27). Only **Q03** is not solved, and it is the one fault whose detector is expected to fail.
- The telemetry diagnoser separates faulty from clean episodes at AUROC **0.975**. The retrieval-stage features of an existing system (RAGLog tier-0) with the same classifier reach 0.735; query-performance predictors reach 0.57 to 0.58. Zero-shot LLM judges of the returned documents reached **0.63 to 0.75** against 0.975 on the same 320 episodes (three free-tier models).
- On **1,648 natural queries no run had examined** (no injection) the deployed loop gained **+2.18 points** of Hit@5 [+1.33, +3.03] (GPU) and +2.43 [+1.70, +3.22] (CPU replication).
- The do-no-harm bound held (held-out clean loss 0.28%, bar 0.5%). A capped variant keeps it with **16.5% clean dispatch** against 86% for the stratified policy that carries the proof, and it meets all four pre-registered targets on both stacks.
- **Composed faults (v7, descriptive):** on 155 held-out fault pairs and triples the retrained attributor named every cause at the family level in **40.0% [32.6, 47.9]**: 0 of 75 for pairs inside one letter group and for triples, 80 to 85% for cross-letter pairs QR and KR. No single-fault gate regressed.
- **QML (simulated, six qubits):** AUROC 0.892 and 0.883 against 0.978 for the project's gradient boosting on all 63 features. **No quantum advantage, and none is claimed.**

**What failed.** v4 on GPU (26 of 28 detectors) and v5 on CPU (24 of 28) were NOT_ADOPTED and stay in the table. Unseen-fault closure (U1) never reached its 0.50 bar (v6: 0.406 and 0.413). Q03 passes in 2 of 7 runs. Repairing natural misspellings does not help. The dispatcher cannot name two faults of one letter group. No frontier-model LLM arm was run, and the benchmark is staged, not released.

**Honest score: about 7.8 out of 10** as a research contribution. 8.3 to 8.5 is not supported by the evidence (section 9).

---

## 1. What is in the zip

`DiagRAG_KAGGLE_A_to_Z.zip` is about 1.2 GB (1.34 GB unpacked, 334 files). **Private use only** (section 11).

| Path | What it is |
|---|---|
| `DiagRAG_A_to_Z_kaggle.ipynb` | **The one Kaggle notebook.** Contains no project code of its own; it runs the hash-pinned files below. |
| `A_TO_Z_GUIDE.md` | This guide. |
| `PROJECT_EXPLAINED.md` | The full project write-up: every result, every failure, limitations, honest assessment. |
| `PACKAGE_MANIFEST.json`, `CHECKSUMS.sha256` | Build record and the SHA-256 of every file. |
| `verify.py` | Integrity check (stage A). |
| `kaggle/` | Every script (`diagrag_v2.py` to `diagrag_v7.py`, ports, LangChain), `v7_cells/`, `reproduce_tables.py`, and one `judged_*` folder per judged run: protocol with code hash, verdict, tables, report and the `episodes.jsonl` of the run. |
| `docs/evidence/` | Pre-registrations with every dated amendment (`v5_protocol.md`, `v6_protocol.md`, `v7_composed_protocol.md`, `qml_protocol.md`, `llm_baselines_plan.md`), analysis scripts and their results. |
| `docs/` | `ROADMAP_V4.md` (execution record), `ALL_RUNS_MATRIX.md`, `REPRODUCE.md`, `IDENTIFIABILITY.md`, `CORE28_FAULTS.md`, `LLM_BASELINES_RESULTS.md`. |
| `bench/` | DiagRAG-Bench v1.0: public dev episodes, unlabelled held-out episodes, scorer, datasheet, verifier. The test labels are **not** included; only their SHA-256 commitment. |
| `prereq/` | `v6_cpu_checkpoint.pkl` (360 MB) and `qlog_nn_b03a9b172742.npy` (277 MB). Needed only by stage G. |
| `data/` | The four input files the judged scripts otherwise download: corpus (53.5 MB), embedding cache (533 MB), Amazon ESCI queries (51 MB), Webis-QSpell-17 (2.3 MB). Exact sizes and SHA-256 are re-checked by the scripts before use. |
| `DiagRAG_v4/v5/v6_kaggle.ipynb`, `scripts/`, `RUN_GUIDE.md`, `requirements*.txt` | The earlier single-run notebooks and the laptop runners. |

**What is not in the zip.** Model weights (downloaded from Hugging Face at run time), the RAGLog code (cloned from GitHub at a pinned commit), pip packages, and the private benchmark test labels (kept in a private repository). No API key is included or needed.

---

## 2. How to run it on Kaggle

1. **Upload the zip as a Kaggle Dataset** (kaggle.com, Datasets, New Dataset, drop `DiagRAG_KAGGLE_A_to_Z.zip`). Choose **Private**. Kaggle unpacks the zip.
2. **Create a notebook**: Create, New Notebook, File, Import Notebook, and upload `DiagRAG_A_to_Z_kaggle.ipynb` (it is also inside the zip).
3. **Add the dataset** to the notebook: Add Input, your datasets, the one you just made.
4. **Settings**: **Internet On** (needs a phone-verified account). Accelerator: none for the default path; **GPU T4 x1 only if you switch on stage F**.
5. **Run All.**
6. Read the status table printed at the end. Download `DiagRAG_A_to_Z_RESULTS.zip` from the notebook's Output.

**Flags (cell 2 of the notebook).**

| Flag | Default | Stage | What it does | Time |
|---|---|---|---|---|
| `CHECKS` | True | A, B, C | integrity, detector re-fit, stored results | 395 s measured in a sandbox with 8 cores (most of it in B, which installs two pinned library sets); expect somewhat longer on Kaggle's 4 cores |
| `QML` | True | D | simulated quantum-ML comparison | 119 s measured on 8 cores |
| `BENCH` | True | E | benchmark quickstart | 43 s measured |
| `RUN_V6_GPU` | False | F | regenerate the pre-registered v6 judged run (seed 50) | the notebook's own estimate is 4 to 6 hours on a T4; **not re-measured here** |
| `RUN_V7_CPU` | False | G | regenerate the composed-fault arm from the shipped v6 checkpoint | the stored run used 8 chunks of up to 25 minutes on 8 cores (about 3 hours of compute, including two chunks lost to the stall fixed in amendment D3). Plan for 5 to 7 hours on Kaggle's 4 cores; **an estimate, not a measurement**. A Kaggle session is limited to 12 hours |
| `SMOKE` | False | F, G | both stages with tiny settings, to test the wiring | slow for a "tiny" run: in the sandbox it took several chunks of up to 25 minutes each, roughly one to two hours in total (not timed as one run); the numbers mean nothing |

With the defaults the notebook needs no GPU, no key and no download of project data.

---

## 3. What each stage does, and what a good output looks like

**A. Integrity.** `verify.py` re-hashes every file against `CHECKSUMS.sha256`, checks that every judged run's recorded code hash equals the shipped script, that `diagrag_v5.py`, `diagrag_v6.py` and `diagrag_v7.py` equal the hashes frozen in their protocols, and that the Kaggle notebooks embed exactly the code they name. Expect `RESULT: ALL OK`. The v7 run folder records the code hash of its *first* version; the protocol names the later two (amendments D2 and D3) and `verify.py` checks that the recorded hash is one of the three it names.

**B. Detector re-fit.** For each of seven judged runs the notebook re-fits the 31 detectors from the shipped `episodes.jsonl` and compares them with the recorded AUROCs. Library versions matter: a near-bar detector moves by up to 0.03 between scikit-learn versions. So each run is re-fitted under the versions of its own stack, installed into a separate folder: CPU runs under scikit-learn 1.9.1 and numpy 2.4.6, Kaggle GPU runs under 1.6.1 and 2.1.3. Expected, measured: **31 of 31 for all seven runs, largest difference 0.0000.** If the pinned install fails (for example on an older Python), the notebook says so and uses its own libraries; some GPU runs then show 27 or 28 of 31, which is the version effect, not a defect.

**C. Stored results.** Regenerates the all-runs matrix from the judged files (nothing typed by hand), prints the composed-fault headline sentence that the v7 script generated from its own files, and re-applies the protocol's single-fault regression definition to v6 CPU and v7. Expected: the 11-row matrix of section 5, and `REGRESSIONS: none`.

**D. QML.** Six-qubit noiseless statevector simulation written in the repository (`docs/evidence/qml_compare.py`, hash in `qml_protocol.md`). A quantum-kernel SVM and a variational classifier are compared with classical models on the **same six PCA inputs** and with the project's gradient boosting on all 63 features. Fitted on the train split only, scored once on the held-out split. Expected values in section 7.

**E. Benchmark.** Verifies DiagRAG-Bench v1.0, fits a diagnoser on the dev split and scores it. Expected: Track-1 AUROC about 0.97 (measured 0.9716).

**F. v6 judged run (flag).** Runs `kaggle/diagrag_v6.py` after checking its hash against `docs/evidence/v6_protocol.md`, with the protocol's settings (seed 50, `N_BASE_ESCI=6000`, `N_HARD=100`, `MAX_ATT=4000`), then the pre-registered analysis `analysis_gpu_plan.py`. It stops with an error if there is no GPU (unless `SMOKE`). If the session stops, run the cell again: it resumes from `diagrag_out/checkpoint.pkl`. **The protocol allows one GPU run and one CPU replication at seed 50. A rerun is a reproduction and does not replace the stored result. Do not change the seed to look for a different verdict.**

**G. Composed-fault arm (flag).** Copies the shipped v6 CPU checkpoint, removes **only** the attributor-dependent results (`docs/evidence/v7_prepare_checkpoint.py`), puts the cached query-log embeddings next to it, and runs `kaggle/diagrag_v7.py` in chunks of 1,400 seconds on the CPU configuration (the checkpoint is a CPU-stack state, so the GPU is hidden from the script). It checks the file against the hash frozen in `docs/evidence/v7_composed_protocol.md` (amendment D3). It ends with the composed headline sentence generated from the run's own files and the single-fault regression check against v6 CPU. A reproduction on other hardware may differ in the third decimal.

**H. Collect.** Packs the small result files and the status of every stage into `DiagRAG_A_to_Z_RESULTS.zip`. The notebook ends with an assertion that fails if any stage failed.

**What was tested before this zip was made.** The default path (stages A to E) was run end to end from a fresh extraction of this zip: all stages OK. The `SMOKE` path (F then G then H) ran end to end with tiny settings. Stage G in real mode was started from the shipped checkpoint and ran its first chunk to the time budget (stage `closed_loop`) and resumed correctly. **Not done:** the full real stage F and the full real stage G were not run through this notebook. The stored results were produced by the same scripts under the same hashes (v6: GPU on Kaggle and CPU; v7: CPU in the sandbox), and this notebook has never run on Kaggle itself.

---

## 4. The project, explained

### 4.1 Stack and faults
A retrieval stack (dense bge-base-en-v1.5 plus BM25, fused by reciprocal-rank fusion with k = 60, top 25 to a cross-encoder reranker, top 5 returned) over a licence-clean corpus of 101,297 documents. Success means a gold document in the top five (Hit@5); identity-sensitive faults need rank 1.

32 injectable faults in four groups. The adoption rule counts the **core 28**; four more (R25, R26, K11, K12) come from field reports. Each fault has an evidence tier; tiers S and M (22 faults) are the "grounded" set and N and P are quarantined.

| Group | Core faults | What they are |
|---|---|---|
| **Q** query | Q01 unfinished last word, Q02 chatty filler, Q03 paraphrase by another real user, Q04 misspelling, Q05 missing space, Q07 corrupted model number, Q09 two needs in one query | the query is the problem |
| **K** knowledge base | K03 sibling products with one identity, K04 stale vector, K05 near-duplicates, K06 unverified copies, K07 other-tenant leak, K08 placeholder documents, K09 expired versions | the documents are the problem |
| **R** retrieval stack | R01 index coverage hole, R03 encoder truncation, R05 reranker returns garbage, R06 misrouting, R07 embedding rows shifted, R10 query-vector noise, R11 encoder drift, R13 BM25 dictionary out of sync, R15 ANN recall, R19 rerank depth cut, R22 raw-score fusion, R23 partial results, R24 reranker truncation | the machinery is the problem |
| **C** | C2 two faults at once from different groups | composition |

An episode is kept only if the clean pipeline succeeds on the query and the faulted pipeline fails, so every episode has something to repair.

### 4.2 Telemetry, detectors, repairs
- **Telemetry:** 63 features from the retrieval trace only (no gold, no answer): query features, score statistics, agreement between legs, duplicate and crowding counts, tenant and validity checks, and cheap probes (ANN-versus-exact recall, vector alignment, stale-vector probe).
- **Detectors:** seven faults use a precise rule (Q04, K07, R15, R23, R25, R26, K11); the rest use a gradient-boosted head. Gate: held-out AUROC at least 0.70 with at least 50 held-out positives.
- **Repairs:** one per fault, plus family repairs (QLEX for Q01/Q03/Q04/Q05, STALE for K04/R07, ENC for R03/R10/R11) and group fallbacks. Gate: Wilson 95% lower bound of the rescue rate at least 0.50, with at most 10% of clean successes lost.

### 4.3 The closed loop and its guarantee
1. A gradient-boosted **attributor** scores each query's telemetry against the clean class and every fault.
2. A **dispatcher** applies a fired precise rule first; otherwise it picks the group by probability mass, then the family, falling back to the group repair.
3. A **conformal do-no-harm threshold** (conformal risk control, calibrated per stratum: common ESCI queries, rare ESCI queries, ShopNova) decides whether to dispatch at all, so that expected Hit@5 lost on a clean query stays at most 0.5% (gate **L1**). **L2**: mean closure at least 0.70. **U1**: mean closure at least 0.50 on faults the attributor never saw (leave-one-fault-out). **N1**: a gain on natural traffic whose 95% interval excludes zero.
4. A **capped** variant raises the threshold until clean classifier dispatch is at most 20% on the calibration set; the loss bound survives because the loss is monotone in the threshold.

### 4.4 How the evidence is kept honest
- Every judged run writes `JUDGED_PROTOCOL.json` (gates, configuration, SHA-256 of the exact code, library versions) before any result exists. ADOPTED needs at least 27 of 28 detectors and 24 of 28 repairs.
- Amendments are dated, committed before the results they touch, and carry a real SHA-256. Failed runs stay in the main table.
- Train and held-out are split by gold-product component. Every downloaded file is checked by exact byte count and SHA-256.
- Test labels of the benchmark are private; only their SHA-256 commitment is public.

---

## 5. Results: every judged run

| Run | Stack | Code | Detectors / repairs / both (of 28) | L1 clean loss | L2 closure | U1 (bar 0.50) | N1 natural gain (95% CI) | Verdict |
|---|---|---|---|---|---|---|---|---|
| seed 42 | CPU | v1 (older code, not shipped) | 28 / 27 / 27 | - | - | - | - | **ADOPTED** |
| seed 43 | CPU | v1 | 28 / 28 / 28 | 0.75% (-) | - | 0.207 | - | **ADOPTED** |
| seed 44 | CPU | v2 | 28 / 27 / 27 | 1.28% (FAIL) | 0.871 (PASS) | 0.253 | - | **ADOPTED** |
| seed 45 | CPU | v3 | 27 / 27 / 27 | 0.15% (PASS) | 0.865 (PASS) | 0.365 (FAIL) | +2.25 [+1.40, +3.09] (PASS) | **ADOPTED** |
| seed 46 | GPU T4 | v3 | 27 / 27 / 27 | 0.15% (PASS) | 0.860 (PASS) | 0.395 (FAIL) | +2.06 [+1.21, +2.85] (PASS) | **ADOPTED** |
| seed 47 | CPU | v4 | 28 / 27 / 27 | 0.37% (PASS) | 0.830 (PASS) | 0.485 (FAIL) | +2.31 [+1.52, +3.16] (PASS) | **ADOPTED** |
| seed 48 | GPU T4 | v4 | 26 / 27 / 26 | 0.00% (PASS) | 0.866 (PASS) | 0.456 (FAIL) | +2.18 [+1.27, +3.16] (PASS) | **NOT_ADOPTED** |
| seed 49 | CPU | v5 | 24 / 27 / 24 | 0.15% (PASS) | 0.833 (PASS) | 0.440 (FAIL) | +2.43 [+1.70, +3.22] (PASS) | **NOT_ADOPTED** |
| seed 50 | GPU T4 | v6 (flagship) | 27 / 27 / 27 | 0.28% (PASS) | 0.844 (PASS) | 0.406 (FAIL) | +2.18 [+1.33, +3.03] (PASS) | **ADOPTED** |
| seed 50 (CPU replication) | CPU | v6 | 28 / 27 / 27 | 0.20% (PASS) | 0.854 (PASS) | 0.413 (FAIL) | +2.43 [+1.70, +3.22] (PASS) | **ADOPTED** |
| seed 50 (CPU, retrained attributor) | CPU | v7 | 28 / 27 / 27 | 0.16% (PASS) | 0.846 (PASS) | 0.413 (FAIL) | +2.43 [+1.64, +3.22] (PASS) | **ADOPTED** (regression check, not a new test set) |

Reading it. Runs 42 to 47 are adopted; seed 48 (GPU, v4) and seed 49 (CPU, v5) are not; seed 50 (v6) is adopted on both stacks, after a construction change motivated by diagnosing v5. v5's three THIN detectors (R03, R15, R22) were caused by the supply of distinct test queries, not by the loop; v6 fixed that with `N_BASE_ESCI=6000`, and the prediction that they would then pass could have failed and did not. Per-stratum conformal calibration, introduced in v3, has held the do-no-harm bound in every run since. The v7 row re-fits the attributor on the same single-fault episodes as v6 CPU and is not counted as another adoption. U1 is below its bar in every run that measured it.

### Other measured results
- **Diagnosis against baselines (held-out episodes):** ours 0.975; RAGLog tier-0 features with the same classifier 0.735; query-performance predictors 0.57 to 0.58.
- **Zero-shot LLM judges (320 episodes, free-tier models), diagnosis AUROC:** Gemini 0.754, gpt-oss-120b 0.701, gpt-oss-20b 0.629, against 0.975 for ours: ours better in every arm. **Repair:** on 1,000 natural queries the Gemini arm gives loop minus CRAG-style +1.23 points [-0.10, +2.60], which is OURS_NON_INFERIOR (not "better"); the two Groq arms are inconclusive. No frontier-model arm exists (the supplied keys could not reach one).
- **Natural traffic:** the gain comes from two simple rules (near-duplicate collapse K05, chunk-crowding collapse K12), not from diagnosis. Repairing natural misspellings has a negative point estimate in every run that measured it. In the v6 GPU census 58.6% of the queries have an empty placeholder ("nan") as their gold document, which bounds what any repair can win on natural traffic.
- **Do-no-harm frontier:** `capped_crc_0.005` keeps the loss bound at 16.5% clean dispatch with closure 0.834 (GPU) and meets all four targets on every run evaluated. `global_crc_0.005` broke the 0.5% loss bound on both v6 stacks (0.56%, 0.60%).
- **Q03** (paraphrase by another real user) is an identifiability exhibit: the detector passes in 2 of 7 runs of its natural construction, by 0.004 and 0.001, and its repair rescues 1 to 6 of 100.

---

## 6. The composed-fault arm (v7)

**Question.** Real failures often have more than one cause, but every earlier result injects one fault at a time. Does the same diagnoser, with no new detector and no new repair, name both causes and close the loop?

**Design (pre-registered in `docs/evidence/v7_composed_protocol.md`; code hash committed before any episode was generated).** Fault pairs and triples are injected into one base query's state. An episode is kept only if the clean query succeeds and the composed one fails; the record also says whether each component fails alone. Eight strata: WITHIN_FAMILY (Q04+Q05), QQ, KK, RR (two faults of one letter), QK, QR, KR (cross-letter), TRIPLE. Quotas 20 per stratum and split (15 for TRIPLE): 155 train and 155 held-out episodes, every stratum at quota. Faults come from the 20 grounded and solved ones. Splits are by base-query md5 and share no base query with any single-fault episode. Composed seed 51. The attributor was retrained with composed rows in the training split only, and every single-fault gate was re-run.

**Result (155 held-out episodes; Wilson 95% intervals).**

| | new attributor | single-fault-trained |
|---|---|---|
| every cause named, family level | **40.0% [32.6, 47.9]** (62/155) | 30.3% [23.6, 38.0] (47/155) |
| at least one cause named | 96.1% | 96.1% |
| every cause named, group level | 80.0% | 69.0% |
| mean set-F1, family level | 0.770 | 0.713 |
| sequential repair closure | **72.9% [65.4, 79.3]** | oracle-forward repairs: 83.9% [77.3, 88.8] |

| stratum | n | every cause named (new / old) | sequential closure | oracle-forward closure |
|---|---|---|---|---|
| WITHIN_FAMILY | 20 | 20/20 / 20/20 (by construction) | 3/20 | 7/20 |
| QQ | 20 | 0/20 / 0/20 | 11/20 | 18/20 |
| KK | 20 | 0/20 / 0/20 | 20/20 | 20/20 |
| RR | 20 | 0/20 / 0/20 | 19/20 | 19/20 |
| QK | 20 | 9/20 / 2/20 | 12/20 | 15/20 |
| QR | 20 | 17/20 / 12/20 | 14/20 | 16/20 |
| KR | 20 | 16/20 / 13/20 | 20/20 | 20/20 |
| TRIPLE | 15 | 0/15 / 0/15 | 14/15 | 15/15 |

**How to read it.** The dispatcher returns at most one label per letter group, so it cannot name two faults of one letter, or three faults: 0 of 75 in both attributors. The WITHIN_FAMILY 20/20 is by construction (Q04 and Q05 share one family label). The gain from retraining (+9.7 points) is entirely in the cross-letter strata. Closure stays high in KK, RR, KR and TRIPLE even where the pair is not named, because one group repair fixes both causes. In 25.8% of episodes (40) neither component fails alone: the failure is emergent. Forced reverse repair order made no difference to closure (25/32 under both orders); the repairs mostly commute.

**No regression.** Core-28 detectors 28/28 and repairs 27/27 unchanged, verdict ADOPTED, L1, L2, N1 pass, `capped_crc_0.005` meets all four targets, U1 unchanged (0.4128). Differences are reported (capped-CRC closure 0.848 to 0.838, margin to the 0.80 bar 0.038; C2 detector AUROC 0.823 to 0.848).

**Predictions written before the run.** Held: both-cause rate about 0.2 to 0.5 and low within a letter; retraining adds up to about 0.1 (+0.097); no regression. Did not hold: closure gap of at least 0.2 (observed 0.11); reverse order lowers some strata; strata short of quota (none).

**Execution record.** After the freeze the run needed two execution fixes, both disclosed in the protocol: D2 (detection-baseline rows kept under `id(e)` could not resume) and D3 (about 9,000 single-row attributor calls at 0.061 s each pushed that stage past the chunk wall clock; replaced by one batch call with a 1e-9 equality check). D2's diagnosis was incomplete and D3 corrects it. The composed result is byte-identical before and after both fixes.

**What it is not.** Synthetic pairs injected by the same authors into one stack, 155 held-out episodes, one seed, CPU. No adoption gate was set and none is claimed.

---

## 7. The QML comparison (optional, simulated)

Machine learning is the project's method. This is a side comparison of scores, committed as a protocol before it was run. Six qubits, a noiseless statevector simulator written in the repository, **no hardware, no noise model**. Task: fault versus clean on the v6 CPU run's held-out episodes (4,019, of which 1,511 faulted); the 155 composed held-out episodes are a second set.

| model | single-fault AUROC [95% CI] | composed-vs-clean AUROC |
|---|---|---|
| ML main: gradient boosting, 63 features | 0.978 [0.974, 0.983] | 0.995 |
| ML on the same 6 PCA inputs: logistic regression | 0.727 | 0.864 |
| ML on the same 6 inputs: RBF-SVM | 0.917 [0.907, 0.926] | 0.979 |
| ML on the same 6 inputs: gradient boosting | 0.921 [0.912, 0.931] | 0.988 |
| QML: quantum-kernel SVM | 0.892 [0.881, 0.903] | 0.942 |
| QML: variational classifier (5 seeds) | 0.883 (sd 0.005) | 0.965 |

Six PCA components keep 40.8% of the variance, which is why same-input classical models are the fair comparison. Both classical six-input models beat both quantum models on both sets. Three of four written predictions held; the fourth (composed episodes score lower or similar) did not: every model scores higher on composed-versus-clean, an easier task. **No quantum advantage, and none is claimed.**

---

## 8. What failed, plainly

1. **Adoption was missed twice** (v4 on GPU, 26/28; v5 on CPU, 24/28) before v6 met it, and v6 is a pass on a changed construction (6,000 base queries, balanced C2 mix), not on the v5 test set.
2. **U1** is below 0.50 in every run that measured it, and lower in v6 (0.406, 0.413) than in v4 (0.485, 0.456). No ceiling could be proved.
3. **Q03's** detector passes in 2 of 7 runs, by 0.004 and 0.001.
4. **Natural misspellings:** the repair does not help; the external baseline hurts more.
5. **No frontier-LLM comparison.** The free-tier arms are complete; no frontier model was reachable.
6. **Second corpus:** subset ports only (FiQA 19/20, SciFact 15/20). No full-suite port.
7. **Release:** the benchmark is staged, not published.
8. **Composed faults:** the dispatcher names every cause in 0 of 75 within-letter pairs and triples; sequential closure is 11 points below the oracle; the pre-registered natural-traffic non-inferiority comparison to the universal repair (D2) fails in v6 and v7 by 0.05 points.

---

## 9. Honest assessment

**About 7.8 out of 10**, my judgement from the evidence, not a measurement and not a venue prediction.

*Strong.* A well-posed problem with field evidence for each fault; a method with a stated guarantee; protocol discipline that is unusual (hash-bound code, dated amendments, failures in the main table, a wrong diagnosis corrected in the open); a natural-traffic gain measured on one sample many times; an identifiability analysis; a benchmark with a private split.

*Weak.* The ADOPTED verdict followed two failures and a construction change; U1 stayed below its bar; the natural-traffic gain comes from two simple rules; the diagnosis advantage is over baselines that favour us (supervised against zero-shot); one e-commerce corpus carries the evidence; no frontier-LLM comparison; the repair loop is only non-inferior to a CRAG-style repair; the code was written by an AI assistant under the owner's direction.

*The composed arm and QML do not move the score.* The composed arm is a new, pre-registered, partly negative measurement with a no-regression proof. It closes none of the open attacks. QML is a side table in which the quantum models lose to classical ones on the same input.

**Why not 8.3 to 8.5.** An A venue still has open attacks: unseen faults (U1), a frontier-model comparison, a second corpus at suite scale, and an unreleased artefact. Closing the frontier comparison and the second corpus and releasing the benchmark might reach about 8.2; 8.5 would need outside adoption or independent replication, which this repository cannot produce.

---

## 10. Limitations

- **Injected faults, same authors.** A pass shows the method works on this construction, not on any production RAG system.
- **One domain carries the evidence.** English e-commerce search. The ports cover 15 to 20 faults each on smaller stacks.
- **Quarantine set.** Ten faults (tiers N and P, including C2) are reported but excluded from headline claims.
- **Natural-traffic evidence rests on one sample** (the same 1,648 queries).
- **The guarantee's cost.** The gate that carries the proof dispatches on 86 to 89% of clean queries; the capped variant keeps the bound by construction but was selected after the stratified one.
- **Library versions matter.** Verdicts decided by 0.001 to 0.005 are fragile across scikit-learn versions (stage B shows it).
- **Single-run adoption.** Each configuration was judged once per stack and seed.
- **Composed faults are synthetic and few** (155 held-out episodes from 20 faults, one seed); the filter keeps only pairs that break retrieval. **QML is simulated** on six PCA components, one data split.
- **This notebook has not been run on Kaggle.** Its default path and its smoke path were tested in the sandbox with the same package.

---

## 11. Privacy, licences, keys

- **Keep the Kaggle dataset private and do not publish the zip.** `data/` contains the 186,290-document corpus, which includes 84,993 rows with `conflicting_unverified` licences (the judged scripts drop them) and the ShopNova synthetic corpus, whose licence the owner has not assigned. It also holds Amazon ESCI (Apache-2.0) and Webis-QSpell-17 (CC BY 4.0); attribution is in `NOTICE.md`.
- No API key is in the zip. The LLM scripts (`bench/llm_baselines.py`) need keys only as environment variables; stages A to H never use one.
- If you pasted keys into any chat during this project, **regenerate them**.
- **Disclosure.** The code and documents were written by Claude (Anthropic), directed by the repository owner. The owner words the disclosure in any paper.

---

## 12. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `The data package was not found` | The dataset is not added as an input of the notebook. Add it (Add Input). |
| Stage A reports `MISMATCH` | A file was altered or the upload was damaged. Upload the zip again. |
| Stage B shows 27 or 28 of 31 for a GPU run | The pinned install failed and the notebook libraries were used (the message says so). It is the library-version effect. |
| Stage F stops with "set the accelerator to GPU" | Set GPU T4 x1, or set `SMOKE`. |
| Stage F or G: "not finished; run this cell again" | The session or budget ended. Run the same cell again; it resumes from the checkpoint. If the session itself restarted, `/kaggle/working` is lost unless you saved a version: attach the earlier version's output as an input (stage F looks for `diagrag_out/checkpoint.pkl` there). |
| A hash assertion in F or G | The script differs from the one frozen in its protocol. Re-extract the zip; do not edit the scripts. |
| Download errors for models or RAGLog | Internet is off, or the host is busy. Turn Internet On and run the cell again; the data checks are idempotent. |
| Out of memory | The sandbox runs used a 30 GB, 8-core machine; the minimum was not measured. |

---

## 13. Open items for the owner

1. A frontier-model arm: provider, model, key (as an environment variable), prices and a spend cap set in the provider console first.
2. A full-suite second-corpus port (needs new features for Q02, Q09 and C2 on the port stack and an owner-approved pre-registration).
3. Benchmark name, ShopNova licence, release timing.
4. Whether to build a dispatcher that returns several labels per letter group (the composed arm's main finding); it would need its own pre-registration.
5. Delete the throwaway Kaggle notebooks (`diagrag-v4-notebook-smoke`, `diagrag-v6-gpu-smoke`) and decide whether to keep the v6 GPU kernel.
6. Regenerate every API key that was pasted into a chat.
