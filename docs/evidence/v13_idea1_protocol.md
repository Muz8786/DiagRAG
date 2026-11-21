# v13 Idea 1: invariant-based fault isolation (pre-registration). Written 20 Nov 2026, ~05:00 UTC, before any invariant score was computed on any episode.

## 0. Question
Can a **training-free** check of the retrieval pipeline's own invariants locate the broken **component** for faults the system was never trained on, better than the trained attributor does when that fault is left out of its training (leave-one-fault-out, LOFO)? Descriptive, on saved episodes; no retrieval is re-run; no frozen file, gate or verdict changes.

## 1. Invariants (feature, the direction that counts as a violation, component). Fixed from the feature definitions in `kaggle/diagrag_v6.py`.
| Component | Invariants (violation direction) |
|---|---|
| QUERY | q_oov ↑, q_oov_long ↑, q_correctable ↑, q_segmentable ↑, q_prefix ↑, q_filler ↑, q_conj ↑, q_code_oov ↑, q_synlow ↑ |
| ENCODER (query path) | q_probe_cos ↓ (served query vector vs pinned re-encode), d_null10 ↑ (dense results that ignore the query) |
| ANN | ann_probe ↓ (ANN top-10 vs exact top-10) |
| VECTORS (dense index) | align_probe ↓, stale_sparse20 ↑, stale_min ↓, nonfinite ↑, cov ↓, sparse_absent_dense ↑ |
| BM25 | s_lex5 ↓ (BM25 hits contain the query words) |
| RERANK | ce_rrf_rho ↓, ce_dense_rho ↓, n_depth ↓ |
| FUSION | dep_dense ↓ (dense share of the reranked depth) |
| SERVING | n_final ↓, deleted5 ↑ |
| FILTERS | tenant_mis5 ↑, expired5 ↑, filter_survival ↓, part_top (two-sided) |
| CONTENT | dup5 ↑, red_cos5 ↑, thin5 ↑, unver5 ↑, ident5 ↑, chunk_crowd5 ↑ |

## 2. True component of each fault (from the fault definitions, `docs/CORE28_FAULTS.md`)
QUERY: Q01 Q02 Q03 Q04 Q05 Q07 Q09 · CONTENT: K03 K05 K06 K08 K12 · VECTORS: K04 R01 R07 R25 · FILTERS: K07 K09 R06 R26 · SERVING: K11 R23 · ENCODER: R03 R10 R11 · RERANK: R05 R19 R24 · BM25: R13 · ANN: R15 · FUSION: R22. C2 (composition) is excluded from the single-fault measures.

## 3. Scoring (no fault labels used)
- **Calibration:** clean (`NONE`) **training** episodes of the same run. For each invariant, conformal p-value of a value x in its violation direction: p = (1 + #{clean calibration values at least as extreme}) / (n + 1); two-sided for part_top (2 x the smaller tail, capped at 1).
- **Violation:** p <= alpha / J with alpha = 0.05 and J = number of invariants (Bonferroni).
- **Predicted component:** the component with the smallest p among its invariants, if any invariant is violated; otherwise none. **Flagged set** (for composed faults): every component with a violated invariant.

## 4. Baseline (the trained system, never seeing the fault)
For each fault f: the run's attributor settings (`HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=<run seed>)`) fitted on single-fault training episodes **without f** (clean calibration rows removed as in the run), predicting on held-out episodes of f; the predicted fault is mapped to its component (NONE = none). Also reported: the attributor trained on all faults (seen-fault reference).

## 5. Measures (held-out = split `test`)
- **M1 (primary): unseen-fault component localisation.** Per fault, the share of held-out episodes whose predicted component is the true one; macro mean over faults, for invariants and for the LOFO attributor; paired bootstrap over faults (2,000) of invariants minus LOFO.
- **M2: held-out clean false-alarm rate** of the invariants (any violation).
- **M3: composed faults** (v7 `composed_features.jsonl`, 155 held-out, calibrated on v7 clean training episodes): share whose flagged set contains every true component, by stratum, beside the stored dispatcher's family-level both-named figure.
- Also reported per fault: which component the invariants pick (the isolability map).

## 6. Data
v6 GPU seed 50 (`kaggle/judged_gpu_v6_seed50/episodes.jsonl`), v8 GPU seed 52 (`kaggle/judged_gpu_v8_seed52/`), v11.a GPU seed 55 (`kaggle/judged_gpu_v11a_seed55/episodes.jsonl`, committed with this protocol), v7 CPU (composed).
**Development** (allowed before freezing, recorded below): run sections 3 to 5 on the **training** split of v8 only, to catch coding errors and wrong directions. A direction may be changed only if it is the opposite of the feature's definition (a coding error), and any change is listed here before the held-out run. **Held-out evaluation is run once.**

## 7. Pass rule (fixed now)
Idea 1 **passes** if, in **every** one of the three runs, M1 invariants minus LOFO has a 95% bootstrap lower bound above 0 **and** M2 is at most 10%. Otherwise it is reported as not shown. M3 is descriptive.

## 8. Predictions (judgements; they can fail)
Pass: about 0.5. M2 at most 10%: about 0.6. Q03 localised by invariants: about 0.2 (a synonym swap breaks almost nothing). Invariants beat LOFO on R-group faults: about 0.7; on K-content faults: about 0.5.

## 9. Amendments
**D1 — development run (20 Nov 2026, ~05:20 UTC; v8 training split only; no held-out episode scored).** Script `docs/evidence/v13_idea1.py`, output `_idea1/dev_v8_train.json` (not committed). Training-split numbers: invariants 0.54 macro component accuracy against 0.19 for LOFO (difference +0.35 [+0.21, +0.51]); clean false alarm 1.5%. Directions checked against the data for the faults that scored 0 (R13, R23, R24, R05, Q04, Q05, Q07, R22): **every direction matches the feature definition**, so no coding error was found and **nothing is changed**. Two properties are recorded, not fixed: (a) ties in p-value are broken by the order of the table in section 1 (as coded before the first run); R23 ties RERANK (n_depth) with SERVING (n_final) and is assigned RERANK; (b) query faults rarely reach the Bonferroni threshold because rare words occur in clean queries too. The held-out run follows, once, with the code as committed.

**R1 — held-out result and scorecard (20 Nov 2026, ~05:40 UTC; written after the results were read; sections 0 to 8 and D1 unedited).** Script `v13_idea1.py` (SHA-256 prefix `e35e0b17`, as committed in D1), one held-out run per judged run. Files `v13_idea1_v6gpu.json`, `v13_idea1_v8gpu.json`, `v13_idea1_v11agpu.json`.

| Run | Invariants (no fault labels) | LOFO attributor (fault unseen) | Difference [95% CI] | Seen-fault attributor (reference) | Clean false alarm |
|---|---|---|---|---|---|
| v6 GPU seed 50 | 0.542 | 0.203 | +0.339 [+0.187, +0.501] | 0.904 | 0.72% |
| v8 GPU seed 52 | 0.541 | 0.196 | +0.345 [+0.199, +0.506] | 0.899 | 0.88% |
| v11.a GPU seed 55 | 0.546 | 0.212 | +0.334 [+0.190, +0.498] | 0.912 | 0.92% |

Macro component accuracy over 31 single faults, held-out episodes. **Pass rule (section 7): met in all three runs. Idea 1 passes.**
By group (v8): Q 0.16 vs 0.06, K 0.80 vs 0.23, R 0.56 vs 0.24.
**Not localised by invariants (below 0.1 in v8):** Q01, Q03, Q04, Q05, Q07, Q09, R05, R06, R13, R23, R24, R26. Query faults rarely reach the Bonferroni threshold because rare words also occur in clean queries; R23 is assigned to RERANK by the pre-declared tie order (D1); R26 is picked as ANN; R05, R24, R13, R06 break invariants too weakly against clean variation.
**M3 (composed, v7, descriptive):** every true component flagged in 76 of 155 held-out composed episodes: KK 20/20, QQ 20/20, RR 9/20, KR 9/20, QR 8/20, QK 4/20, TRIPLE 5/15, WITHIN_FAMILY 1/20. Note this is **component level**, not the family-level naming of v7 (40.0%); KK pairs often break two components (e.g. VECTORS and CONTENT), which the v7 dispatcher could never name together (0 of 20).
*Scorecard (section 8):* pass (0.5): **held**. M2 <= 10% (0.6): **held** (0.7 to 0.9%). Q03 localised (0.2): **did not happen** (0.00), as expected. Invariants beat LOFO on R faults (0.7): **held**; on K content faults (0.5): **held**.
*What this does and does not show:* a training-free check locates the broken component of a fault the system never saw about 2.7 times as often as the trained attributor does, at under 1% clean false alarms, stably across three seeds. It does **not** name the exact fault (the seen-fault attributor still does that best, 0.90), it does not repair anything (closure not measured), half the faults are not localisable this way, and the component map and invariant directions are the authors' (fixed before any score). Same injected-fault caveat as the rest of the project.
