# DiagRAG v8 multi-label dispatcher: preregistered protocol

Status: **frozen before any v8 judged result**. The protocol, runner, and Kaggle notebook are committed and pushed to the approved non-main branch. The synthetic preflight uses no project data and is not a judged result. No v8 episode or judged result existed at freeze time.

Frozen runner SHA-256: `5ccb86fb4f79d3c52af4985c94afd9d2e3b9942660a4fbee9058b7b38b3a565f` (`kaggle/diagrag_v8.py`). Frozen Kaggle notebook SHA-256: `95e0bedfe3d8e9c943a3f0beb81bffaf955f3eb100e310de5b512331a3ba0db2` (`kaggle/DiagRAG_v8_kaggle.ipynb`). The notebook embeds the runner byte-for-byte and checks its hash before execution.

## Question

Does a dispatcher that can return multiple fault-family labels within the same letter group improve identification and sequential-repair closure on composed faults, while preserving the v7 single-fault gates and clean-query safety?

## Design

- Descriptive evaluation; there is no adoption gate and no tuning against the held-out set.
- Eligible faults, injectors, repairs, strata, and success rule are inherited from `docs/evidence/v7_composed_protocol.md`. No new detectors or repairs are added.
- Keep the frozen v7 dispatcher output as the primary set. Rank remaining repair families by summed class probability across all Q/K/R groups. Add a candidate only when its family probability mass is at least `tau2`; one extra family may be added per letter group, including a group already represented by the v7 output, and the final set is capped at three labels. If more candidates qualify than fit, retain those with the largest family mass. Use only existing family and group-fallback repairs. Ties follow the Python tuple ordering over family and label names in the frozen runner.
- Set `tau2` on training/calibration rows only: choose the smallest finite threshold whose upper 95% Wilson bound on the share of queries receiving any *extra-family dispatch* is at most 0.5% on clean calibration queries and at most 10% on single-fault calibration episodes. Single-fault scores are out-of-fold by base-query ID; clean calibration rows were not used to fit the attributors. If no finite threshold meets both constraints, set `tau2` to infinity, disable the extra-family path, and report that calibration failure. Freeze `tau2` before held-out scoring.
- Refit the v7 attributors on the old training rows plus the new seed-52 composed training rows, one label row per component as in v7. Do not include held-out composed rows or the clean evaluation sample in fitting, calibration, or threshold selection.

## Fresh sample and splits

- Seed: 52 for composed-pair ordering and injector randomness.
- Source: the [official Amazon Shopping Queries Dataset](https://github.com/amazon-science/esci-data), full English-US query-product file. Its published repository reports 97,345 US queries and identifies the project as Apache-2.0 licensed. Query file SHA-256 is `4a735b693b4a424a6fc67f5be6e4c811495c488bbf66d02a602d308b2744263a` (51,286,808 bytes). Frozen retrieval corpus SHA-256 is `5a9f7ea6ae5b8a3e7f1e1ca6e2838dddd6158efb9384d757c6aa755dbe9bda3c` (53,518,791 bytes compressed).
- Candidate filter: US locale, Exact label, gold product present in the frozen corpus, lowercased/trimmed ASCII query with at least one token, and query string absent from every earlier judged episode through v7. The source audit yields 1,648 such fresh query strings. These query strings were included in earlier natural-traffic analysis, so this is a fresh *fault-injection* set, not fresh natural traffic.
- Gold-component split: inherit the frozen v7 component assignment. Of the 1,648 fresh queries, 868 belong to historical train components and form the v8 composed-training pool; 780 belong to held-out components with no gold-product overlap with historical training and form the fresh composed-test pool. No query string in either pool appeared in an earlier injected episode. Report the exact counts after deterministic pool regeneration; abort on a mismatch.
- Per-split stratum quotas: 20 each for WITHIN_FAMILY, QQ, KK, RR, QK, QR, KR and 15 for TRIPLE (155 per split; 310 total), as in v7. The candidate pool is smaller than v7's, so quotas may be short; report every empty/short stratum and never substitute a base query or fault after seeing results.
- Clean-loop safety: run the frozen v8 sequential loop on at least 1,000 clean held-out ESCI queries. Select 1,000 distinct `fault=NONE`, `split=test` query bases from the v8 seed-50 CPU rerun by ascending MD5 of `52|v8-clean|bid`, excluding any gold-product component used in the v8 composed-training pool. The existing split assignment is component-disjoint, and the candidate components are checked against the training pool. This is a reused held-out clean set, not independent new natural-traffic evidence. Abort if fewer than 1,000 eligible queries remain.

## Measures

- Primary: both-cause family-level identification, with Wilson 95% interval, overall and by stratum. Also report at-least-one-cause, group-level both-cause, exact cause set, set precision/recall/F1, and every empty/short stratum.
- Sequential-repair closure: same v7 loop and top-k criterion, with Wilson 95% intervals, overall and by stratum; oracle-forward repair closure is a reference.
- Clean loss: held-out clean Hit@5 loss for one dispatch and for the sequential loop, with denominator and interval; the sequential loop uses at least 1,000 clean queries.
- Regression: rerun all v7 single-fault gates and the v7 section-4 regression definition. Report detector/repair statuses, 28-core counts, L1, L2, U1, N1, C2 AUROC, policy and guarantee tables, and exact changes. Any regression remains a regression.
- Compare three label sets on the same held-out v8 composed episodes: (1) v8 dispatcher + v8 attributor, (2) frozen v7 dispatcher + the same v8 attributor (isolates the dispatcher change), and (3) frozen v7 dispatcher + v6 single-fault-only attributor (the prior comparator). Neither comparator is refit on held-out data.

## Predictions (written before any v8 result)

- The within-letter both-cause family rate will exceed the v7 0/75 baseline, but remain below 50% overall for QQ, KK, RR, and TRIPLE.
- The new dispatcher will improve overall set-F1 by at least 0.05 versus v7 dispatch on the fresh held-out composed set.
- The clean calibration constraints will be met; if not, the multi-label route is disabled and its result is a failed prediction.
- The v7 single-fault adoption verdict and all v7 regression gates will be preserved.
- The sequential loop's clean loss will remain at or below 0.5% on the fresh clean sample.

## Pre-run gates and freeze record

All gates before a judged result are complete: source dataset and retrieval corpus byte lengths and hashes were verified; the new runner is built from v7 without modifying v6/v7; the self-contained Kaggle notebook embeds the runner and verifies its SHA-256; Python compilation passed; the synthetic dispatcher preflight passed; notebook embedding and repository verifier checks are recorded in the progress ledger; and the protocol plus runner were committed and pushed to a non-main branch. This freeze permits starting the judged run, but the run has not started. Every chunk must resume from its versioned v8 checkpoint; no seed shopping or discarded strata. No secret is embedded in the code or notebook.

Frozen Kaggle settings: CPU accelerator, Internet enabled, `SEED=50`, `RERANKER=BAAI/bge-reranker-base`, `N_BASE_ESCI=6000`, `N_PRDC=528`, `N_HARD=100`, `MAX_ATT=4000`, `N_HARM=20`, and `TIME_BUDGET=30000` seconds per invocation. The composed arm seed is fixed in code at 52; quota scaling and clean-sample overrides are not supported.

## External run prerequisite

The Kaggle run has not started because the Kaggle credential values pasted into chat were exposed and must be revoked and regenerated. Do not paste replacements into chat. Configure the new credential securely in the Kaggle CLI or Kaggle account/runtime secret store. The owner approved a public non-main branch push; no release or main-branch push is part of this protocol. No LLM API is called by the v8 runner.
