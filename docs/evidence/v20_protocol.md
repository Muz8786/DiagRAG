# v20: feature-family ablations, matched baselines, matched-budget active/passive, leave-one-mechanism-out, failure audit. Pre-registration
Written 21 Nov 2026, 21:58 IST, before any v20 result existed (the script was checked on a 300-episode synthetic stand-in, not on project data). Script SHA-256 `d2924da345eb71312d9a06255374d82e457b93e51591f241d7238ab0f13a5a0b`. Follows the plan "DiagRAG — controlled experimental upgrade for an 8/10 target" (21 Nov 2026), sections A to D. Compute: Kaggle CPU (the GPU queue is jammed); small file-reading analyses locally.

## What can and cannot be run from the project's data

| Plan item | Run tonight? | Data used |
|---|---|---|
| A feature-family ablations F0 to F14 | **yes** | saved `episodes.jsonl` (63 features per episode, labels, splits) |
| A F15 RAGLog tier-0 with the matched estimator | **no**: per-episode RAGLog features were not saved; needs a pipeline re-run | the earlier run-level value 0.734 is reported only with its parity caveats |
| B1 same supervision (LR, RF, MLP, HGB on the same 63 features and labels) | **yes** | same |
| B2 same information (single-feature and score-threshold detectors) | **yes** | same |
| B3 matched intervention budget | **partly**: from stored probe executions (v15, v16); a passive arm with more unique probes than the battery needs new GPU runs | `kaggle/heldout_v15_S_seed7*`, `kaggle/heldout_v16_seed7*` |
| C1 external benchmark selected outside the project | **no** (none available tonight); the plan is kept | — |
| C2 leave-one-mechanism-out detection and coarse localization | **yes** (first run of each notebook) | saved episodes |
| C3 another retriever implementation | already partly done (second stack); no new run | — |
| C4 answer-level outcome | **no** (needs a generator model; the project is cost-free and LLM-free) | — |
| C5 failure-case audit with trace ids | **yes** | stored outputs |
| D machine-readable run manifest | **yes** | repository |

## Feature-family manifest (fixed now; every one of the 63 columns in exactly one family)
The manifest with a description, extra cost and dependencies for each column is `docs/evidence/v20_feature_manifest.json` (written from `features()` in the frozen code before any run).
- **QUERY (16):** q_len, q_oov, q_oov_long, q_lowdf, q_idf_mean, q_idf_max, q_digit, q_code, q_code_oov, q_code_rare, q_conj, q_correctable, q_segmentable, q_prefix, q_synlow, q_filler. Query text and corpus vocabulary only.
- **SCORE (14):** d1, d_gap, d_m5, d_std20, d_n, s1, s_gap, s_n, ce1, ce_gap, ce_std, ce_mean, n_depth, n_final. Scores and list lengths from the retrieval trace.
- **AGREEMENT (8):** s_lex5, d_lex5, ov_ds10, dep_dense, dep_sparse, ce_rrf_rho, ce_dense_rho, sparse_absent_dense. Agreement between the query and the legs, and between legs.
- **INTEGRITY (19):** red_cos5, dup5, ident5, attr_n, attrcov1, attr_gain, attr_title_body_gap, thin5, unver5, tenant_mis5, expired5, versioned5, part_ent, part_top, filter_survival, deleted5, chunk_crowd5, cov, nonfinite. Content and metadata checks on returned documents and index-health counters already in the trace.
- **PROBE (6):** ann_probe, align_probe, q_probe_cos, d_null10, stale_sparse20, stale_min. Need extra computation per query: one exact dense search, one query re-encode, 21 document re-encodes (main stack, PROBE_K = 20), and one empty-query search per process.

## A. Arms (one estimator, fixed in advance)
F0 all 63; F1 to F5 all minus one family (QUERY, SCORE, AGREEMENT, INTEGRITY, PROBE); F6 to F10 one family only; F11 QUERY+SCORE; F12 QUERY+SCORE+AGREEMENT; F13 passive = all minus PROBE (identical to F5, reported once); F14 all features with the six PROBE columns permuted jointly across the test episodes (five permutations; F0 model, no refit). Estimator: the frozen attributor (histogram gradient boosting, 250 iterations, learning rate 0.08, 15 leaves, minimum leaf 5, l2 1.0, balanced class weights, random state = run seed). **No hyperparameter search for any arm or baseline**, so the search budget is equal (zero) for all.

## B. Baselines
- **B1 same supervision, same 63 features, same labels and splits:** multinomial logistic regression (standardized, balanced weights, C = 1, 2,000 iterations), random forest (500 trees, minimum leaf 2, balanced weights), MLP (standardized, 128-64 ReLU, early stopping; sklearn's MLP has no class weights, which is disclosed), and the HGB attributor (= F0).
- **B2 same information, no learning of a classifier over features:** the best single feature for fault-versus-clean, chosen with its sign on the training split, and the negated top reranker score and top dense score as fixed detectors. Detection only.
- **B3 matched intervention budget (from stored files):** for every held-out pair of v15/v16 (seeds 71 to 73), the active self-test's recorded probe executions and outcome, against passive decoding at the same number of probe executions where that is measurable (budgets up to the battery size, about 100), with random probes, pass/fail versus stage-traced, and no intervention. Above the battery size passive decoding has no more unique probes in the stored data, and re-executing a probe on a deterministic pipeline adds no information; that arm is reported as not measured, not as a win.

## Splits, metrics, intervals
Train = the run's train split minus its clean calibration half (as the frozen code); test = the run's held-out split (grouped by gold-product component); C2 composition episodes excluded (as in the identification analysis). Metrics on test: detection AUROC and AUPRC of 1 - p(clean); exact top-1 on faulted episodes; repair-family accuracy on faulted episodes; macro-F1 over the 32 classes (a class never found counts 0); clean false-positive rate (clean episodes whose top class is a fault); recall of Q03, K04, R24. Differences to F0 with a paired bootstrap clustered by base query (500 resamples). **Unit of replication:** each run is one replicate of episode generation; seeds are not independent fault mechanisms, and results are reported per run and as the mean over runs.

**Runs:** primary = the six untouched GPU runs, seeds 71 to 76; the CPU run of seed 50 (source of the headline numbers) checks the F0 reproduction; seeds 52 and 55 are descriptive.

## C2. Leave-one-mechanism-out
For each of the 31 single faults: train the estimator without that fault; on its test episodes and the clean test episodes report binary detection AUROC of 1 - p(clean), the share flagged (top class not clean), and coarse localization (top fault class in the right group Q, K or R). Exact identification of an unseen label is undefined and not reported. Run on the first run of each notebook.

## Interpretation fixed now
A small drop when a family is removed does not show the family is useless (correlated families substitute); the single-family arms and per-fault recall are read together. If removing PROBE features costs more than 0.02 of exact top-1, the paper describes the system as telemetry plus diagnostic probes, not zero-cost passive monitoring.
