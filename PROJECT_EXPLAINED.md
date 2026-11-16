# DiagRAG, explained: what it is, what was built, what the results are, and what failed

Status as of **17 Nov 2026**. Repository: `Muz8786/DiagRAG`, branch `core28-kaggle-notebook` (PR #1). Every number below comes from a file in this repository and carries its run (seed, stack). Where a number was typed from memory it was checked against its file first; six statements in earlier drafts were wrong and are corrected in the record (`docs/ROADMAP_V4.md`, amendments B3 and B6).

---

## 0. One page

**The problem.** A RAG system (retrieval-augmented generation) answers from documents it retrieves. When it answers badly the cause is often in the retrieval stage: a misspelled query, duplicate documents, a stale vector index, a reranker that returns garbage. The system rarely says so, and an LLM-based check on every query is slow and costs money.

**The idea.** Look only at the *telemetry* the retrieval stage already produces (score gaps, rank agreement between the dense and keyword legs, duplicate counts, cheap probes; 63 numbers per query). From it, (1) say whether retrieval failed, (2) say which of 32 known fault types caused it, (3) apply a targeted repair, and (4) promise, with a conformal bound, not to hurt queries that were fine. No generated answer and no LLM call are needed at run time.

**What was built.**
- A retrieval stack (dense + BM25 + reciprocal-rank fusion + cross-encoder reranker) over a licence-clean corpus of 101,297 documents, with 32 injectable fault types in four groups: query (Q), knowledge base (K), retrieval stack (R) and compositional (C).
- A detector and a repair for each fault, a gradient-boosted attributor, a family-first dispatcher with group fallbacks, and a conformal do-no-harm threshold.
- Judged runs in which every pass/fail gate and the SHA-256 of the exact code were written to a protocol file before any result existed.
- A 4,843-episode public benchmark (DiagRAG-Bench v1.0) with private held-out labels committed by hash, ports to two other corpora and to a LangChain stack, and a comparison against LLM judges.

**What the results say (v5, CPU stack, seed 49 unless marked).**
- A supervised telemetry diagnoser separates faulty from clean episodes at AUROC **0.979**; the retrieval-stage features of an existing system (RAGLog tier-0) with the same classifier reach 0.762, and query-performance predictors 0.59 to 0.60. Zero-shot LLM judges of the returned documents reached 0.64 to 0.75 against 0.975 (earlier, smaller sample).
- On **1,648 natural queries that no run had ever examined** (no injection), the deployed repair loop gained **+2.43 points** of Hit@5 [+1.70, +3.22] (42 queries fixed, 2 broken). Four earlier runs measured +2.06 to +2.31 on the same sample.
- The do-no-harm bound held: held-out clean loss 0.15% against a 0.5% bar. A capped variant gives the bound at **15.6% clean dispatch** (89% for the stratified policy that gates L1) at a cost of 1.2 points of closure.

**What failed, in the same breath.**
- **The adoption rule was missed in the last two judged runs**: GPU seed 48 (26 of 28 detectors, 27 needed) and CPU seed 49 (24 of 28). In v5, three of the four misses are faults whose detectors scored AUROC 1.000, 0.988 and 0.968 but produced fewer than the 50 held-out positives that v5 itself required (a generator flaw of mine); the fourth, **Q03**, is a real failure.
- **Unseen-fault closure (U1) never reached its 0.50 bar** (best 0.485, v5 0.440), and no ceiling could be proved.
- Repairing natural misspellings does not help (negative point estimate in every run that measured it).
- The frontier-LLM comparison, a full-suite second-corpus port and the public release did not happen in this programme (section 9).

**Honest score: about 7.5 out of 10** as a research contribution. The target set was a CORE A venue (CIKM or WSDM class); the evidence supports a solid B-level paper today and names the specific gaps to an A (section 10). 8.0 to 8.2 was requested and is **not** supported by the evidence; the reasons are in section 10.

---

## 1. The problem in more detail

A retrieval failure is any case where none of the top five returned documents contains the answer. Two kinds matter:

- **Natural failures.** Real traffic. In this corpus the clean pipeline already fails on 45.2% of 7,175 real shopping queries (v5 census, CPU stack; 43.5% on the GPU stack in v4). The census shows why: the gold document is itself an empty placeholder (its text is literally "nan") for 58.6% of queries and 68.0% of the failures (v5 census). A repair cannot rescue a query whose gold document has no content, so most natural failures are corpus-data problems, not pipeline faults. That is a finding about the benchmark data and it bounds how much any repair can win on natural traffic.
- **Pipeline faults.** Something broke: a stale vector, a missing index block, a reranker returning random scores. These leave traces in telemetry, and these are what DiagRAG diagnoses.

**Diagnosis versus detection.** A detector says "retrieval failed". A diagnoser says *where*, so a targeted repair can run. The comparison to existing work is deliberately narrow: RAGLog-style (LLM looks at the query and the five returned documents) and CRAG-style (LLM grades the documents, rewrites the query) baselines were implemented in a reduced form. They are **not** the full RAGLog or CRAG systems.

---

## 2. What was built

### 2.1 The retrieval stack
Dense retrieval (bge-base-en-v1.5) and BM25 are fused with reciprocal-rank fusion (k = 60); the top 25 go to a cross-encoder reranker (bge-reranker-large on GPU, MiniLM-L6 on CPU) and the top 5 are returned. A tenant filter and a validity-date filter are on by default. Success means a gold document in the top five (Hit@5); identity-sensitive faults require rank 1.

### 2.2 The 32 faults
Core 28 (the adoption rule counts these) plus four extra faults found in field reports (R25, R26, K11, K12). Each fault has an **evidence tier** (S and M are grounded in public field reports and form the 22-fault "grounded" set; N and P are quarantined). Tiers across all 32: 13 S, 9 M, 7 N, 3 P.

| Group | Faults (core) | What they are |
|---|---|---|
| **Q** query | Q01 unfinished last word, Q02 chatty filler, Q03 paraphrase by another real user, Q04 misspelling, Q05 missing space, Q07 corrupted model number, Q09 two needs in one query | the query is the problem |
| **K** knowledge base | K03 sibling products with the same identity, K04 stale vector, K05 near-duplicates, K06 unverified copies, K07 other-tenant leak, K08 placeholder documents, K09 expired versions | the documents are the problem |
| **R** retrieval stack | R01 index coverage hole, R03 encoder truncation, R05 reranker returns garbage, R06 misrouting, R07 embedding rows shifted, R10 query-vector noise, R11 encoder drift, R13 BM25 dictionary out of sync, R15 ANN recall, R19 rerank depth cut, R22 raw-score fusion, R23 partial results, R24 reranker truncation | the machinery is the problem |
| **C** | C2 two faults at once from different groups | composition |
| extra | R25 non-finite vectors, R26 post-filtered ANN, K11 deleted documents served, K12 chunk crowding | added from field reports; reported beside the core 28 |

**Hard episodes.** An episode is kept only if the clean pipeline succeeds on the query and the faulted pipeline fails, so every episode has something to repair. The hard-episode yield is reported per fault (from 0.9% for R26 to 100% for R06).

### 2.3 Telemetry, detectors, repairs
- **Telemetry:** 63 features computed from the retrieval trace only (no gold, no answer): query features (out-of-vocabulary rate, correctable tokens, segmentable tokens), score statistics (dense gap, sparse gap, cross-encoder gap), agreement between legs, duplicate and chunk-crowding counts, tenant and validity checks, and cheap probes (ANN-versus-exact recall, vector-alignment probe, stale-vector probe).
- **Detectors:** seven faults use a precise rule (Q04, K07, R15, R23, R25, R26, K11); the rest use a gradient-boosted head on the telemetry. Gate: held-out AUROC at least 0.70. C2 is scored from the second-largest group probability mass of the single-fault attributor.
- **Repairs:** one per fault (autocomplete, spelling correction, word segmentation, near-duplicate collapse, re-applying the tenant filter, rebuilding the dense view, restoring RRF fusion, and so on), plus **family repairs** (QLEX for Q01/Q03/Q04/Q05, STALE for K04/R07, ENC for R03/R10/R11) and **group fallbacks** for each of Q, K and R. Gate: Wilson 95% lower bound of the rescue rate at least 0.50, with at most 10% of clean successes lost.

### 2.4 The closed loop
1. A gradient-boosted **attributor** (250 trees) scores each query's telemetry against the clean class and every fault.
2. A **dispatcher** applies a fired precise rule first; otherwise it chooses the group by probability mass, then the family within the group, falling back to the group repair if no family is clearly ahead.
3. A **conformal do-no-harm threshold** (conformal risk control, per stratum: common ESCI queries, rare ESCI queries, ShopNova) decides whether to dispatch at all, so that the expected Hit@5 lost on a clean query stays at most 0.5% (gate L1). L2 asks for mean closure at least 0.70; **U1** asks for mean closure at least 0.50 on faults the attributor never saw (leave-one-fault-out); **N1** asks for a gain on natural traffic whose 95% interval excludes zero.
4. v5 adds a **capped** variant (the threshold is raised so that clean classifier dispatch stays at or below 20% on the calibration set; the loss bound survives because the loss is monotone in the threshold) and a **two-stage** variant (precise rules alone, natural rules K12 and K05 added on top, then the classifier at a capped threshold).

---

## 3. Data and integrity

- **Corpus:** a licence-clean corpus of 101,297 documents (Amazon ESCI under Apache-2.0, Amazon Berkeley Objects rows with a verified CC BY 4.0 licence only, an Apache OFBiz manual, and a synthetic "ShopNova" partition whose licence is not yet assigned by the owner). 84,993 ABO rows with conflicting licences were removed from the original 186,290.
- **Queries:** 2,400 real ESCI queries plus about 885 ShopNova queries as episode bases; a query log of other ESCI queries (never the evaluated ones) feeds the autocomplete and paraphrase repairs; Webis-QSpell-17 supplies real misspellings.
- **Natural traffic:** a census of 7,175 ESCI queries with an Exact product in the corpus; 1,648 of them were never examined during development (a 6,391-query exclusion file is checked in) and form the natural-traffic test.
- **Checks:** every downloaded file is verified by exact byte count and SHA-256 before use; train and held-out are split by gold-product component so no gold product appears in both; a purity report counts duplicates, empty content and licence drops.

---

## 4. How the evidence is kept honest

- **Frozen gates.** Every judged run writes `JUDGED_PROTOCOL.json` (gates, configuration, SHA-256 of the exact code, and from v5 the library versions) before any result exists. Verdicts are ADOPTED only if at least 27 of 28 detectors and 24 of 28 repairs pass.
- **Pre-registration and amendments.** v5 and the LLM comparison have written protocols (`docs/evidence/v5_protocol.md`, `docs/evidence/llm_baselines_plan.md`). Every change after the first commit is a dated amendment committed *before* the result it could affect (A1 to A5, B1 to B8).
- **One run.** v5 allowed exactly one judged run. When the Kaggle token turned out to be revoked, amendment B7 moved that single run to the CPU stack before it started, with seed 49 and every bar unchanged.
- **Failures are reported the same way as passes.** The all-runs matrix below lists every judged run, including the ones that missed.
- **Held-out data is never tuned on.** Design changes happen between versions. The v5 floor and policies were declared in the protocol before any v5 code existed.

---

## 5. Results

### 5.1 Every judged run

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
| seed 49 (GPU replication) | GPU T4 | v5 | not run | | | | | |

Notes: seed 42 used older v1 code whose hash is not shipped. L1 and L2 are defined from v2 onward (v1 runs predate them; "-" means not measured). Natural-traffic samples overlap across v3, v4 and v5 (one query sample), so N1 values are repeated measurements.

Reading it: v1 to v4 CPU runs were adopted; the two GPU runs differ (seed 46 adopted, seed 48 not). The do-no-harm bound failed at seed 43 (0.75%) and seed 44 (1.28%); per-stratum (Mondrian) conformal calibration, introduced in v3, passed in every run since. U1 (the unseen-fault arm exists from seed 43 on) has been below 0.50 in every run. The natural-traffic gain is +2.06 to +2.43 in all five runs that measured it, **on one shared query sample** (so these are repeated measurements, not independent evidence).

### 5.2 The v5 run (CPU stack, seed 49, code `deecafad…702a`), fault by fault

Pre-registered accounting: (a) core 28 under the original rule is the headline; (b) grounded set and (c) quarantine set are reported beside it.

| Accounting | Detectors | Repairs | Solved both | Not solved |
|---|---|---|---|---|
| **(a) core 28** | **24** (27 needed) | 27 (24 needed) | 24 | Q03; R03, R15, R22 (THIN) |
| (b) grounded (22) | 18 | 20 | 18 | Q03, R15, R22, R26 |
| (c) quarantine (10) | 9 | 10 | 9 | R03 |

Verdict **NOT_ADOPTED**. Loop gates: L1 PASS (0.15%), L2 PASS (0.833), **U1 FAIL (0.440)**, N1 PASS (+2.43 points [+1.70, +3.22]).

Per-fault results (held-out detector AUROC with the number of held-out positives; repair rescue with the Wilson lower bound; tier S/M grounded, N/P quarantined; R25, R26, K11, K12 are outside the core 28):

| Fault | Group | Tier | Detector AUROC (n held-out positives) | Detector | Repair rescued / n (Wilson LB) | Repair | Solved |
|---|---|---|---|---|---|---|---|
| Q01 | Q | N | 0.998 (50) | PASS | 73 / 100 (0.64) | PASS | True |
| Q02 | Q | M | 1.000 (50) | PASS | 81 / 100 (0.72) | PASS | True |
| Q03 | Q | M | 0.640 (50) | FAIL | 3 / 100 (0.01) | FAIL | False |
| Q04 | Q | S | 0.974 (50) | PASS | 73 / 100 (0.64) | PASS | True |
| Q05 | Q | M | 0.985 (50) | PASS | 94 / 100 (0.88) | PASS | True |
| Q07 | Q | M | 0.989 (50) | PASS | 80 / 100 (0.71) | PASS | True |
| Q09 | Q | P | 1.000 (50) | PASS | 73 / 100 (0.64) | PASS | True |
| K03 | K | N | 1.000 (50) | PASS | 93 / 100 (0.86) | PASS | True |
| K04 | K | M | 0.947 (50) | PASS | 90 / 100 (0.83) | PASS | True |
| K05 | K | S | 1.000 (50) | PASS | 97 / 100 (0.92) | PASS | True |
| K06 | K | N | 1.000 (50) | PASS | 99 / 100 (0.95) | PASS | True |
| K07 | K | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| K08 | K | M | 1.000 (50) | PASS | 96 / 100 (0.90) | PASS | True |
| K09 | K | M | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| K11 | K | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| K12 | K | S | 1.000 (50) | PASS | 92 / 100 (0.85) | PASS | True |
| R01 | R | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R03 | R | N | 1.000 (38) | THIN | 88 / 88 (0.96) | PASS | False |
| R05 | R | N | 0.983 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R06 | R | P | 0.993 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R07 | R | P | 0.989 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R10 | R | N | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R11 | R | S | 0.961 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R13 | R | M | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R15 | R | S | 0.988 (44) | THIN | 92 / 94 (0.93) | PASS | False |
| R19 | R | S | 1.000 (50) | PASS | 90 / 100 (0.83) | PASS | True |
| R22 | R | S | 0.968 (47) | THIN | 97 / 97 (0.96) | PASS | False |
| R23 | R | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R24 | R | M | 0.980 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R25 | R | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R26 | R | S | 1.000 (7) | THIN | 12 / 12 (0.76) | THIN | False |
| C2 | C | N | 0.785 (50) | PASS | 81 / 100 (0.72) | PASS | True |

**The three THIN detectors.** R03 (AUROC 1.000, 38 held-out positives), R15 (0.988, 44) and R22 (0.968, 47) are marked THIN, not failed, because they fell below the 50-positive floor that v5 introduced. The cause is in the episode generator, and the stored loop state confirms it: all three stopped at the pointer bound (5,228 = 4 x the 1,307-query pool) after only 2,617 to 2,717 attempts, far below the 4,000-attempt cap, while every fault that filled both quotas (for example R10, R11, R13) stopped well before the bound. Entries from a split whose quota is already full are skipped but still consume the pointer, so the smaller test half starves for the lowest-yield faults. **Counterfactual, not a verdict:** under v4's floor of 20 these three would pass, giving 27/28 and an ADOPTED verdict by the original numbers. The verdict stands as NOT_ADOPTED because a bar chosen after seeing the result is not allowed. The fix (count quota skips separately) belongs in a v6 that needs the owner's approval.

### 5.3 Natural traffic (no injection, 1,648 never-examined queries, v5)
| Arm | n | Change in Hit@5 [95% CI] | Reading |
|---|---|---|---|
| **Deployed loop** (v5 config) | 1,648 | **+2.43 points [+1.70, +3.22]**, 42 fixed, 2 broken | PASS |
| same loop, v4 config (natural misspelling repair on) | 1,648 | +2.43 [+1.58, +3.28], 45 fixed, 5 broken | the config correction removes 3 breaks; the point estimate is unchanged |
| natural rules K12 and K05 alone | 1,648 | +2.43 [+1.70, +3.22] | all of the gain |
| classifier dispatch alone | 1,648 | +0.30 [+0.06, +0.61] | tiny |
| duplicate-collapse (K05) where duplicates occur | 140 | +5.00 [+1.43, +9.29] | PASS |
| chunk-crowding collapse (K12) where it occurs | 637 | +4.87 [+3.14, +6.59] | PASS |
| **natural misspelling repair (QLEX)** | 185 | **-4.86 [-10.81, +0.54]** | harms; interval touches zero this time |
| SymSpell (external baseline) | 185 | **-11.35 [-17.84, -4.86]** | HARM |

So the gain on real traffic comes from two simple rules, not from diagnosis. The misspelling repair has a negative point estimate in every run that measured it (-4.9 to -7.1 points; the interval excludes zero in two of them), and the v5 deployed configuration switches it off for natural traffic. The pre-registered D3 test (detection-gated rules versus always-on K12) passed for the first time (+0.61 points [+0.06, +1.15]); D2 (loop non-inferior to a diagnosis-free universal repair) failed narrowly (lower bound -0.61 points against a -0.50 margin) while costing 5.16 against 12.

### 5.4 Diagnosis against baselines (held-out episodes)
| Method | Fault-vs-clean AUROC | Run |
|---|---|---|
| **DiagRAG attributor** (supervised, 1 minus P(clean)) | **0.979** | v5 CPU |
| RAGLog tier-0 features, same classifier (authors' code, no LLM checks) | 0.762 | v5 CPU |
| query-performance predictors NQC / WIG | 0.600 / 0.593 | v5 CPU |
| zero-shot LLM judge, Gemini 3.1 Flash-Lite (n = 320) | 0.754 against 0.975 for ours | earlier CPU sample (v3 seed 45) |
| zero-shot LLM judge, gpt-oss-120b (partial, n = 163) | 0.731 against 0.975 | same |
| zero-shot LLM judge, gpt-oss-20b (partial, n = 169) | 0.642 against 0.976 | same |

This comparison **favours us**: our model had 2,718 labelled episodes and the LLM judges had none (supervised against zero-shot), our probes were designed for these faults, and RAGLog's own LLM checks were not run. On repair, a CRAG-style loop and ours were comparable on 300 natural queries at zero LLM calls for ours (+0.99 against +1.65 points; the difference [-1.33, +2.67] is inconclusive).

### 5.5 The do-no-harm guarantee as a frontier (v5, held-out clean queries)
| Policy | Clean loss | Total clean dispatch | Mean cost | Mean closure | Meets all four targets |
|---|---|---|---|---|---|
| tau at 5% false alarm (no guarantee) | 0.07% | 2.1% | 0.11 | 0.837 | yes |
| global CRC 0.005 | 0.15% | 14.1% | 0.98 | 0.872 | yes |
| **Mondrian CRC 0.005 (the L1 gate)** | 0.15% | **89.2%** | 3.66 | 0.833 | no |
| **capped CRC 0.005** | **0.07%** | **15.6%** | **0.96** | **0.821** | **yes** |
| two-stage 0.005 | 0.37% | 41.1% (classifier 15.6%) | 1.91 | 0.782 | no |
| diagnosis-free universal repair | 1.49% | 100% | 12.00 | 0.755 | no |

Targets: loss at most 0.5%, total clean dispatch at most 25%, mean cost at most 1.5, closure at least 0.80. **The 89% dispatch is not the price of the guarantee**: the stratified threshold is the smallest one the loss bound allows, so it dispatches nearly everything in the common stratum. Capping dispatch keeps the bound and costs 1.2 points of closure. The two-stage policy misses because the natural rules K12 and K05 fire on about 35% of clean queries (they help on natural traffic, so this is a finding about the data, not an error).

### 5.6 Unseen faults (U1) and the identifiability analysis
Mean closure on a fault the attributor never saw: 0.395 (GPU v3), 0.485 (CPU v4), 0.456 (GPU v4), **0.440 (CPU v5)**; bar 0.50. Group fallbacks raised it from 0.24 to 0.365 in v3 (CPU), and v4's group-level attributor to 0.485 (CPU), but never over the bar. Why:
- **Group attribution** on unseen faults is right only 40% to 58% of the time.
- **Four faults have no effective repair** (K06, Q03, Q07, Q09 stay at or below 0.08 closure in all four runs with fallbacks).
- **Pairwise separability is high** (v5 training split, 465 fault pairs): 98.1% have out-of-fold AUROC at least 0.95, none below 0.80, median certified total-variation lower bound 1.00. The least separable pair is **K04|Q03 at 0.875 [0.811, 0.945]**, then K04|R07 (0.926), R05|R13 (0.927), K06|R05 (0.932), Q07|R13 (0.937).
- **No ceiling is proved.** The oracle-group closure (closure if the group were always right) is 0.57 to 0.69, above the bar, and the brief's "nearest confusable partner" aggregate (35% same group) is contradicted by the measured U1 values, so it is a diagnostic, not a bound. A probe that adds a retrieval with the query-log neighbour (pre-registered admission test) was rejected: Q03-versus-rest AUROC 0.609 to 0.598 on the training split.

### 5.7 Other domains and a framework stack
| Arm | Result | Notes |
|---|---|---|
| FiQA (second stack: e5-small-v2, FAISS HNSW, min-max fusion, MiniLM reranker) | **19 of 20** faults solved | clean Hit@5 0.535 (held out) |
| SciFact, same stack | **15 of 20** (bar 15) | exactly at the bar; K04 fails on both domains |
| SciFact, first port attempt | 11 of 20 | before fixes |
| LangChain pipeline v1 | 7 of 15, claim failed | before fixes |
| LangChain pipeline v2 | **11 of 15**, exactly at the bar | fixes designed after seeing v1 |

These ports cover 20 of the core 28 faults; nine are absent from the FiQA port (Q02, Q07, Q09, K03, K06, K07, K09, R06, C2) and some cannot exist there by construction (Q07 needs product codes, K07 needs tenants). A full-suite port was not built.

### 5.8 The benchmark
**DiagRAG-Bench v1.0:** 2,718 dev episodes with public labels and 2,125 test episodes whose labels are private (the SHA-256 `2e7cf4c0…e51f` is public; the labels are in the private repository `Muz8786/diagrag-data`). A scorer, a reference diagnoser (test AUROC **0.976 [0.969, 0.982]**, detection at 5% false alarm 0.917, family accuracy 0.863), a datasheet and a 5-minute quickstart ship with it. The package is **staged and verified, not released**.

---

## 6. Diagnoses of what looked odd

### 6.1 Q03 is an identifiability exhibit, not a flaky detector
Q03 detector AUROC by construction era (inverse-variance means, 95% CI):

| Era | Runs | AUROC per run | Mean [95% CI] | Within-era heterogeneity |
|---|---|---|---|---|
| injected synonym swap | seeds 42, 43, 44 | 0.866, 0.934, 0.877 | **0.912 [0.874, 0.950]** | Q = 2.42, df 2, p = 0.30 |
| real query pairs from other users | seeds 45 to 49 | 0.559, 0.654, 0.704, 0.691, 0.640 | **0.643 [0.600, 0.687]** | Q = 4.40, df 4, p = 0.35 |
| all eight | | | | Q = 89.7, df 7, p = 1.5e-16 |

Under the real-pair construction the upper end of the interval (0.687) is below the 0.70 bar, so Q03's detector is not expected to meet it. The injected and the natural paraphrase task are different problems; the same repair that rescues injected synonym swaps rescues 3 of 100 real-pair episodes in v5.

### 6.2 C2: the seed-48 failure is explained
C2 is two faults at once; its score is the second-largest group probability mass of an attributor that never trains on C2. The generator draws one of 12 pair types at random, about four per type. **Six pair types have almost no second-group mass** (Q03+R05, Q04+K05, Q04+R10, K04+R24, Q05+R24, K04+R03: the first fault masks the second). In seed 48 the 25 test positives had unlucky composition (5th percentile of random splits) and scored far below the 25 train positives under the same head (medians 0.002 and 0.136, p = 0.003). With composition fixed the test AUROC was still low (p = 0.013), but the worst of seven runs reaches that with probability 8.6%. All 50 C2 positives are ESCI, one tenant, k = 5, so source and tenant cannot explain it. **Verdict: a construction artefact plus ordinary small-sample variance.** v5 (n = 50): C2 passes at 0.785.

### 6.3 A reproducibility gap in our own pipeline
Re-fitting the detectors from a run's shipped episodes reproduces CPU runs exactly (31 of 31 AUROCs for v4 seed 47) but not the Kaggle GPU run (27 of 31 within 0.005; Q03 re-fits to 0.7085 against a recorded 0.6914). The model has no seed dependence, so this is a library difference on Kaggle that was not recorded. v5 records library versions. The v4 verdict is unchanged.

### 6.4 Why v5 has three THIN detectors
See section 5.2. It is a generator flaw (quota skips consume the loop budget), found only after the run.

---

## 7. What failed, plainly

1. **Adoption:** two judged runs in a row (GPU seed 48, CPU seed 49) missed the 27-detector rule. The only GPU runs are v3 (adopted) and v4 (not adopted); the v5 design has no GPU run.
2. **U1:** below 0.50 in all seven runs that measured it (seeds 43 to 49). No proved ceiling.
3. **Q03:** the detector fails by expectation under the real-pair construction; its repair rescues 3 of 100.
4. **Natural misspellings:** the repair does not help, and the external baseline hurts more.
5. **Frontier LLM comparison:** not run (no key). The B2 comparison with CRAG-style repair is inconclusive on 300 queries (non-inferiority not shown). Two Groq arms are partial.
6. **Second corpus:** subset ports only; no full-suite port.
7. **Release:** the benchmark is staged, not published.
8. **GPU replication of v5:** impossible here (the Kaggle token is revoked). The notebook is built and its hash is tied to the protocol.

---

## 8. Time line of how the project got here (short)

Core-28 notebook (CPU seeds 42, 43) → v2 with natural-validation arms and family-level loop (seed 44) → v3 with licence-clean corpus, tiers, conformal calibration and external baselines (CPU seed 45, GPU seed 46) → v4 with a group attributor (CPU seed 47, GPU seed 48) → ports (SciFact, FiQA), LangChain v1 and v2, LLM baselines (free tiers), benchmark v1.0 → diagnosis of the gate flips, v5 pre-registration and run (CPU seed 49) → this document.

---

## 9. What is in the repository and how to run it

- `PROJECT_EXPLAINED.md` (this file), `README.md`, `NOTICE.md` (licences).
- `kaggle/` : every notebook and script (v1 to v5, ports, LangChain), the natural-traffic exclusion files, and one `judged_*` folder per judged run (protocol, verdict, tables, report; episode files are in the zip).
- `docs/` : `ROADMAP_V3.md`, `ROADMAP_V4.md` (execution record), `ALL_RUNS_MATRIX.md` (generated), `IDENTIFIABILITY.md`, `CORE28_FAULTS.md`, `EVIDENCE_AND_NOVELTY_REPORT.md`, `LLM_BASELINES_RESULTS.md`, `REPRODUCE.md`, and `docs/evidence/` (protocols, amendments, analysis scripts and their results).
- `bench/` : DiagRAG-Bench v1.0 public files, scorer, quickstart, verifier. `paper/` : outline and a workshop draft.

**To run.** See `RUN_GUIDE.md` (in the run package) for the step-by-step path: verify the files (10 seconds), re-fit the detectors from shipped episodes (30 seconds per run), run the benchmark quickstart (30 seconds), run any judged script on a laptop CPU in resumable chunks, or run a notebook on a Kaggle GPU. The LLM scripts need keys supplied as environment variables only.

---

## 10. Honest assessment

**Where the project stands: about 7.5 out of 10.** This is my judgement from the evidence, not a measurement and not a venue prediction. It rests on the following.

*Strong.* A well-posed problem with field evidence for each fault; a method with a stated guarantee; protocol discipline that is unusual (hash-bound code, dated amendments, failures in the main table); a measured frontier that shows the guarantee need not cost 89% dispatch; a natural-traffic gain measured five times; a rigorous identifiability table; a benchmark with a private split; and a record of its own corrections.

*Weak.* The adoption rule was missed twice in a row, once through my own floor; U1 stayed below its bar with no ceiling; the gain on natural traffic comes from two simple rules; the diagnosis advantage is over baselines that favour us; one e-commerce corpus carries the evidence (ports cover 20 of 28 faults); no frontier-LLM comparison; the code was written by an AI assistant under the owner's direction.

**Against the target (CORE A, a CIKM or WSDM-class paper).** The current record clears a B-level bar. The seven attacks an A reviewer will make, and their state:

| Attack | State |
|---|---|
| "Your flagship run is NOT_ADOPTED" | **open**: two misses; explained, not closed |
| "Your unseen-fault claim fails its own bar" | **open**: no pass, no ceiling |
| "Your guarantee costs 90% dispatch" | **closed**: capped CRC, 15.6% dispatch, closure 0.821 |
| "You beat free-tier LLMs; so what" | **open**: needs a frontier-model arm (keys) |
| "One corpus" | **open**: needs a full-suite second-corpus port |
| "Artefact?" | **staged**, not released (owner decisions) |
| "Can I trust any of this?" | **addressed**: all-runs matrix, amendments, this document |

**Why not 8.0 to 8.2.** Reaching it needs, at minimum: a v6 with the generator fixed and a pass on the adoption rule on the GPU stack; a frontier-LLM arm; and a full-suite port. None could be done here: the Kaggle token is revoked, no LLM key is set, and v6 needs the owner's approval. I estimate that doing all of them *and* having them land well would reach about 8.0; 8.2 and above would need outside adoption, which cannot be scheduled. 9 is not a target.

---

## 11. Limitations (ours, first)

- **Injected faults, same authors.** The 28 faults are injected by the people who wrote the detectors and repairs; a pass shows the method works on this construction, not on any production RAG system.
- **One domain carries the evidence.** E-commerce search in English. The ports (FiQA, SciFact, LangChain) cover 15 to 20 faults each and use smaller stacks.
- **Quarantine set.** Ten faults (tiers N and P) are reported but excluded from headline claims because their field evidence is weaker. C2 is among them.
- **Natural-traffic evidence rests on one sample.** The five measurements of the gain use the same 1,648 queries.
- **The guarantee's cost.** The gate that carries the proof (stratified CRC) dispatches on 89% of clean queries; the cheap variants (global or capped CRC) have weaker or equal guarantees by construction and are reported as such.
- **Q03** is construction-dependent (section 6.1). **Natural misspellings** are not repaired (section 5.3).
- **Supervised against zero-shot** in the LLM comparison; free-tier models; reduced RAGLog and CRAG variants; no frontier model.
- **Library versions** were not recorded before v5, so the GPU runs cannot be re-fitted exactly.
- **Single-run adoption.** Each configuration was judged once (two stacks, one seed each for v4 and v5); the seed-to-seed spread is visible in the matrix and is not small for the two faults that flip.

---

## 12. Authorship, disclosure and open items

**Disclosure.** The code and documents in this project were written by Claude (Anthropic), directed by the repository owner. The owner words the disclosure in any paper.

**Open items for the owner (not decided by the assistant).**
1. A valid Kaggle token (as an environment variable) to run the v5 notebook on a GPU as a stack replication; v6 approval (generator fix and stratified C2 pairs).
2. LLM keys as environment variables (Groq, Gemini) and, for the frontier arm, a provider, model, prices and a spend cap of USD 15 set in the provider console first.
3. Benchmark name, ShopNova licence, release timing; whether to send the replication email (`docs/REPLICATION_INVITATION.md`, a draft) or submit the workshop draft (`paper/WORKSHOP_DRAFT.md`).
4. Delete the throwaway Kaggle notebook `diagrag-v4-notebook-smoke`; regenerate every key that was ever pasted in chat.
