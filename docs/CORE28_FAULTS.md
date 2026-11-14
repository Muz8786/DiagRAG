# Core-28 faults: episodes, detector and repair for each one

All of this is implemented in `kaggle/diagrag_core28.ipynb` (source: `kaggle/diagrag_core28.py`).
Only these 28 faults are built. The other 19 of the old 47 are out of scope.

## Read this first: where the definitions come from

The V4/V5 code, the fault catalogue and the trial harness are not in this repo.
`Muz8786/DiagRAG-Replication-repo-` is empty. So each fault below is defined from
its ID, its group (Q = query, K = knowledge/corpus, R = retrieval stack, C = compositional)
and the notes in the problem list (for example "K03: sibling products carry the same
identity", "R19: widen-k uses an unfitted CE2 floor of 0.5", "R15: ANN recall").
If a V4 fault ID meant something different, change three functions for that ID:
`inj_<ID>`, `rep_<ID>`, and the head or rule in section 12. Nothing else depends on the meaning.

## Shared stack and rules

- Retrieval: bge-base-en-v1.5 dense over the verified 186,290-doc cache, plus BM25
  (k1 0.9, b 0.4). Fusion is RRF with k=60. Depth 25 goes to the bge-reranker-large
  cross-encoder, and the top 5 are delivered. Tenant filter and validity-date filter
  are on by default.
- Hard-episode rule (fixes "too easy" and "baseline already right"): an episode is kept
  only if the clean pipeline succeeds and the faulted pipeline fails. Each fault keeps
  injecting until it has `N_HARD` = 80 hard episodes (a quota of half per split, so 40 are
  held out) or reaches `MAX_ATT` = 2,500 attempts.
  It records how many injections were easy and how many were not applicable, so the hard-episode yield is reported.
- Success metric: gold in the top 5. Identity-sensitive faults (Q07, K03, K06, K07, K09)
  need gold at rank 1.
- Gold-equivalence (purity fix): gold = the labelled doc, its chunks, the same-ASIN
  ESCI/ABO twin, and exact-content twins. Without this, a correct twin counts as a miss.
- Split: ESCI queries are grouped by shared gold products (union-find) and the groups
  are hashed to train/test, so no gold product appears in both splits. The code asserts
  zero leakage.
- Detector gate: held-out one-vs-rest AUROC ≥ 0.70 with ≥ 20 test positives.
  Fewer than 20 test positives is reported as THIN, not PASS.
- Repair gate: ≥ 20 hard episodes, oracle-dispatched rescue rate with a Wilson 95% lower
  bound ≥ 0.50, and at most 10% of clean successes lost when the repair is forced on them.
- Gates are fixed before results (`JUDGED_PROTOCOL.json`). The verdict is ADOPTED only if at
  least 24/28 repairs and 27/28 detectors pass.
- Fixes that apply to every head: each head must have ≥ 5 training positives or the run
  stops (this guards against the R06-style "never trained, AUROC 0.50" bug). Every fault's
  repair is asserted to come from this file's `REP` table (this is the R05 plugin check).

## Q group (query faults, real ESCI queries)

| ID | Problem we had | Episodes now | Detector | Repair |
|---|---|---|---|---|
| Q01 | too easy, V4 thin | unfinished last word ("nike fleece sho") | HistGB head on query features (`q_prefix`, `q_oov`, `q_lowdf`) + retrieval stats | autocomplete from the ESCI query log; the log excludes every base query, so nothing leaks |
| Q02 | baseline right 4/5 | chatty filler + context clause ("hi im looking for … for my sister who loves hiking") | head (`q_filler`, `q_len`, idf stats) | strip filler words and "who loves X" clauses |
| Q03 | too easy, V4 thin | key word swapped for its most-common-sense WordNet synonym that the catalogue rarely uses | head (`q_synlow`, `q_lowdf`) | map rare words to catalogue-common synonyms, chosen by corpus co-occurrence with the rest of the query |
| Q04 | trial episodes too easy | real misspellings from Webis-QSpell-17 (4,534 pairs), else one edit drawn from Webis' edit-type mix | tier-0 rule: a token has a corpus spelling correction (`q_correctable ≥ 1`) | SymSpell-style correction from corpus words: closest edit distance first, then co-occurrence, then df |
| Q05 | never measured | missing space ("screenprotector") | head (`q_oov_long`, `q_segmentable`) | dynamic-programming word segmentation over corpus words |
| Q07 | too easy, V4 thin | model-number corruption (digit swap/substitution) on ESCI codes and on 528 "brand + model code" ShopNova queries; Hit@1 | head (`q_code`, `q_code_oov`, `q_code_rare`) | candidate ladder: in-corpus variants of the code, keep the one the reranker scores highest |
| Q09 | never measured | two shopping needs in one query ("A and also B") | head (`q_conj`, `q_len`, partition spread) | split on conjunctions, retrieve each part, interleave results |

## K group (knowledge/corpus faults)

| ID | Problem we had | Episodes now | Detector | Repair |
|---|---|---|---|---|
| K03 | AUROC 0.5106, 0/4 detected, no abstention because siblings share the identity | 6 synthetic sibling variants of the gold doc; the body differs on the asked attribute and the title is keyword-stuffed with the query; Hit@1 | v2 features: `ident5` (shared identity in top 5), `attrcov1` (attribute match in the body of top-1), `attr_gain`, `attr_title_body_gap` (title claims an attribute the body lacks), `red_cos5` | inside the top-1 identity cluster (body shingle Jaccard ≥ 0.5), rerank by attribute match in the body, then CE |
| K04 | 0/5 detected; ladder can't reach gold outside the top-5 neighbourhood | gold's dense vector is stale (replaced by another doc's vector) | new index-health probe: re-embed the BM25 top-20 and compare with the served vectors (`stale_sparse20`, `stale_min`, `sparse_absent_dense`) | re-embed the full-corpus BM25 top-50 that are missing from the dense list, correct stale vectors, re-fuse. This reaches beyond the delivered top 5 |
| K05 | detector 0.6937, 0.006 under the bar | 7 near-copies of the strongest competing doc, half keyword-stuffed | redundancy features `dup5`, `red_cos5`, `ident5` | collapse near-duplicates (shingle Jaccard ≥ 0.8 or cosine ≥ 0.985) before rerank, refill from depth |
| K06 | never measured | 6 third-party copies of the gold with altered numbers (licence unverified); Hit@1 | head (`unver5`, `ident5`, `red_cos5`) | in same-title clusters, rank verified sources first |
| K07 | repair never gate-measured | tenant filter off; synthetic other-tenant versions of tenant-scoped FAQ/policy docs; Hit@1 | tier-0 rule: a delivered doc outside the query tenant's scope (`tenant_mis5 ≥ 1`) | re-apply the tenant filter |
| K08 | too easy, unmeasured | 6 placeholder docs ("Title: <query> / Brand: nan / Description: nan"), copying the 3,993 real nan docs in the corpus | head (`thin5`) | move placeholder docs whose title just echoes the query behind informative docs, before rerank |
| K09 | never measured | validity filter off; the corpus's own V1/V2 policy pairs (36) + 2 synthetic expired versions per FAQ/policy; Hit@1 | head (`expired5`, `versioned5`) | re-apply the "In force from … until …" validity filter at the query date |

TimeQA/FreshQA are not used for K09. Their questions do not map onto this corpus's
documents. The in-corpus versioned policies do, so they are used instead, together with synthetic older versions.

## R group (retrieval-stack faults)

| ID | Problem we had | Episodes now | Detector | Repair |
|---|---|---|---|---|
| R01 | only 5 episodes; ladder needed ≥ 0.999 coverage at three points | 30% of the dense index missing, gold included | head (`cov`, `sparse_absent_dense`) | one coverage check (< 0.999), then rebuild the dense view from the verified cache |
| R03 | V4 thin | encoder `max_seq_length` set to 12, so the 8-token bge prompt leaves about 2 query tokens | head (dense score stats, dense/sparse agreement) | re-encode with the pinned encoder config |
| R05 | 1/6 on real queries; still served by the old harness plugin | reranker plugin returns garbage scores | head (`ce_rrf_rho`, CE stats) | swap to a fresh reranker; fall back to the fused order if it still disagrees. The `REP` assertion proves R05 is served by this file |
| R06 | AUROC exactly 0.50 (routing bug); repair never measured | router sends the query to the wrong collection | head (`part_top`, `part_ent`) | route to the full collection |
| R07 | healthy | embedding rows shifted by 1–3 in a 20k block around the gold | `align_probe`, `stale_sparse20` | alignment probe on dense top-5; if misaligned, remap and refresh |
| R10 | too easy, V4 thin | noise on the query vector (cosine to clean ≈ 0.3–0.45) | head (dense stats vs sparse/CE agreement) | re-encode through the pinned path |
| R11 | too easy, V4 thin | real model drift: query encoded by bge-base-en v1 or all-mpnet-base-v2 against the v1.5 index | head | re-encode with the index's model |
| R13 | detector unmeasured | BM25 term dictionary out of sync (term-id shift) | head (`s_lex5`: sparse hits don't contain the query words) | reload the matching dictionary |
| R15 | ANN-recall episodes hard to build | real IVF index (1,024 lists, k-means on the cache) served at nprobe=1 | tier-0 rule: ANN top-10 vs exact top-10 recall < 0.9 | ladder nprobe 32 → 128 → exact; stop when ANN top-10 = exact top-10 |
| R19 | widen-k used an unfitted CE floor of 0.5 | rerank depth cut from 25 to 5 | head | widen to 50 → 100, verified against a CE floor fitted on clean train (10th percentile of clean top-1 CE) |
| R22 | detector thin | raw-score fusion (BM25 scale swamps cosine) instead of RRF | head | restore RRF |
| R23 | healthy | partial results after a timeout (1–2 docs) | tier-0 rule: fewer than 5 results | retry with full results |
| R24 | healthy | reranker sees only 24 characters per doc | head (CE stats) | rerank with full text |

R03, R10 and R11 share one repair (re-encode through the pinned encoder), so the closed
loop counts confusion among those three as correct attribution.

## C group

| ID | Episodes | Detector | Repair |
|---|---|---|---|
| C2 | two faults at once from different groups (12 pairs: Q+R, K+R, Q+K) | tier-0 rule: two rules from different groups fire, or the second group's probability mass from the attributor ≥ `TAU_C2` (the 90th percentile on single-fault out-of-fold data, so ≤ 10% of single faults get a second repair) | apply the top fault's repair for each group, in Q → K → R order |

## Closed loop

A HistGB attributor is trained on all single-fault and clean training episodes.
`TAU_NONE` is set on out-of-fold clean episodes so that at most 5% of clean queries
get a repair. Dispatch order: a fired tier-0 rule first, then the attributor's top fault,
then the C2 check. The loop reports closure per fault, attribution accuracy, and the net
Hit change on clean held-out traffic.

## Judged CPU runs, 14 Nov 2026

Both runs used the CPU stack (MiniLM-L6 reranker) with 50 hard episodes per fault, 25 of
them held out. Full outputs: `kaggle/judged_cpu_run_seed42/` and `kaggle/judged_cpu_run_seed43/`.

| | Seed 42 (code b60462fb) | Seed 43 (code 591a323d) |
|---|---|---|
| Detectors passing | 28/28 | 28/28 (lowest: K04 0.80, R24 0.92, Q03 0.93) |
| Repairs passing | 27/28 (Q03 fails, lower bound 0.42) | 28/28 (Q03 passes only just, 32/50, lower bound 0.501) |
| Verdict | ADOPTED | ADOPTED |

Between the runs: the Q03 repair now chooses the synonym from the search query log, and the
Q04 rule no longer overrides dispatch. Seed 43 is the run that judges both changes.

**Closed loop on held-out episodes (seed 43)**

| Policy | Mean closure | Attribution | Clean queries repaired | Clean Hit@5 lost |
|---|---|---|---|---|
| τ at 5% FPR (out of fold) | 0.82 | 0.80 | 3.7% | 0.22 points |
| Conformal, α = 0.005 | 0.85 | 0.81 | 9.2% | 0.75 points |

Seed 42 under the old dispatch: Q01 closure 0.16 and clean Hit@5 −1.1 points.

**Do-no-harm guarantee: FAIL.** The pre-registered check was held-out clean loss ≤ α = 0.005.
- The measured loss was 0.0075.
- Across 200 re-splits of the calibration set the mean was 0.0043, but the 95th percentile was 0.0100.
- The cause is a design flaw. Calibration scores come from 5-fold out-of-fold models, while
  held-out scores come from the attributor trained on all of train. The two sets of scores
  aren't exchangeable, and conformal risk control needs them to be.
- The fix is a separate calibration split scored by the same model, judged in a new run.

**Natural faults (no injection), seed 43**
- **Real misspellings:** 46 ESCI queries had a misspelled token whose corrected spelling
  another user typed. 33 of them failed before repair.
  - Hit@5 went from 0.283 to 0.304 after the closed loop and to 0.326 with the oracle Q04 repair.
  - The corrected query itself scores 0.348.
  - The loop recovers one third of the reachable gain on 46 queries, which is weak and thin evidence.
- **Superseded policies:** only 3 of the 36 in-corpus V1/V2 pairs fail with the validity filter
  off, too few to judge. At lower thresholds the dispatcher made them worse.

**Unseen faults (each fault left out of attributor training), seed 43:** mean closure 0.21 over 24 faults.
- Recovery happens only where a sibling fault shares the repair: R03, R10 and R11 (one encoder
  reset, 0.88–0.96) and K04/R07 (vector refresh, 0.72–0.76).
- The other faults recover almost nothing. Repairs are specific to each fault; they don't generalize.

## What the numbers mean

- Faults are injected, so detector AUROCs measure whether telemetry can see the injected
  signature. They are not a measure of natural-fault detection. Natural validation is
  still outstanding for K (temporal) and R (model shift), as `paper/OUTLINE.md` already says.
- The judged run above used the CPU stack (MiniLM-L6 reranker). The notebook's default GPU
  stack (bge-reranker-large, 80 episodes per fault) is a different stack and needs its own
  judged run before its numbers can be quoted.
