# DiagRAG, explained: what it is, what was built, what the results are, and what failed

Status as of **17 Nov 2026 (after the v6 runs)**. Repository: `Muz8786/DiagRAG`, branch `core28-kaggle-notebook` (PR #1). Every number below comes from a file in this repository and carries its run (seed, stack). Where a number was typed from memory it was checked against its file first; six statements in earlier drafts were wrong and are corrected in the record (`docs/ROADMAP_V4.md`, amendments B3 and B6).

---

## 0. One page

**The problem.** A RAG system (retrieval-augmented generation) answers from documents it retrieves. When it answers badly the cause is often in the retrieval stage: a misspelled query, duplicate documents, a stale vector index, a reranker that returns garbage. The system rarely says so, and an LLM-based check on every query is slow and costs money.

**The idea.** Look only at the *telemetry* the retrieval stage already produces (score gaps, rank agreement between the dense and keyword legs, duplicate counts, cheap probes; 63 numbers per query). From it, (1) say whether retrieval failed, (2) say which of 32 known fault types caused it, (3) apply a targeted repair, and (4) promise, with a conformal bound, not to hurt queries that were fine. No generated answer and no LLM call are needed at run time.

**What was built.**
- A retrieval stack (dense + BM25 + reciprocal-rank fusion + cross-encoder reranker) over a licence-clean corpus of 101,297 documents, with 32 injectable fault types in four groups: query (Q), knowledge base (K), retrieval stack (R) and compositional (C).
- A detector and a repair for each fault, a gradient-boosted attributor, a family-first dispatcher with group fallbacks, and a conformal do-no-harm threshold.
- Judged runs in which every pass/fail gate and the SHA-256 of the exact code were written to a protocol file before any result existed.
- A 4,843-episode public benchmark (DiagRAG-Bench v1.0) with private held-out labels committed by hash, ports to two other corpora and to a LangChain stack, and a comparison against LLM judges.

**What the results say (v6 GPU flagship, T4, seed 50, unless marked).**
- **The pre-registered flagship run is ADOPTED**: 27 of 28 core detectors and 27 of 28 repairs (rule: 27 and 24). A CPU replication at the same seed is also ADOPTED (28 and 27). Only **Q03** is not solved, and it is the one fault whose detector is expected to fail (section 6.1).
- A supervised telemetry diagnoser separates faulty from clean episodes at AUROC **0.975** (v6 GPU); the retrieval-stage features of an existing system (RAGLog tier-0) with the same classifier reach 0.735, and query-performance predictors 0.57 to 0.58. Zero-shot LLM judges of the returned documents reached **0.63 to 0.75** against 0.975 on the same 320 episodes (three free-tier models, all arms complete).
- On **1,648 natural queries that no run had ever examined** (no injection), the deployed repair loop gained **+2.18 points** of Hit@5 [+1.33, +3.03] (GPU) and +2.43 [+1.70, +3.22] (CPU replication). Seven runs now give +2.06 to +2.43 on that one sample.
- The do-no-harm bound held (held-out clean loss 0.28%, bar 0.5%). A capped variant gives the same bound at **16.5% clean dispatch** against 86% for the stratified policy that gates L1, with closure 0.834 against 0.844, and it meets all four pre-registered targets on both stacks.

**What failed, in the same breath.**
- **v5 was NOT_ADOPTED** (CPU, 24 of 28 detectors) and so was **v4 on GPU** (26 of 28). v6 is ADOPTED only after a construction fix motivated by diagnosing v5; v5 and v4 stay in the matrix.
- **Unseen-fault closure (U1) never reached its 0.50 bar** (best 0.485; v6 0.406 and 0.413, the lowest since v3), and no ceiling could be proved.
- **Q03's detector** passes in 2 of 7 runs of the natural-paraphrase construction, by 0.004 and 0.001; its repair rescues 1 to 6 of 100.
- Repairing natural misspellings does not help (negative point estimate in every run that measured it, interval above zero in three).
- A frontier-model LLM arm and a full-suite second-corpus port were **not done**, and the benchmark is **staged, not released** (section 9).

**Honest score: about 7.8 out of 10** as a research contribution (section 10): up from 7.5 because the flagship is now ADOPTED on the GPU stack, the LLM comparison is complete and the guarantee frontier is measured on two stacks. 8.3 to 8.5 was requested and is **not** supported by the evidence; section 10 says what is missing.

---

## 1. The problem in more detail

A retrieval failure is any case where none of the top five returned documents contains the answer. Two kinds matter:

- **Natural failures.** Real traffic. In this corpus the clean pipeline already fails on 43.5% of 7,175 real shopping queries on the GPU stack (v6; 45.2% on the CPU stack in v5). The census shows why: the gold document is itself an empty placeholder (its text is literally "nan") for 58.6% of queries and 69.1% of the failures (v6 GPU; 68.0% in v5 CPU). A repair cannot rescue a query whose gold document has no content, so most natural failures are corpus-data problems, not pipeline faults. That is a finding about the benchmark data and it bounds how much any repair can win on natural traffic.
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
| seed 50 | GPU T4 | v6 (flagship) | 27 / 27 / 27 | 0.28% (PASS) | 0.844 (PASS) | 0.406 (FAIL) | +2.18 [+1.33, +3.03] (PASS) | **ADOPTED** |
| seed 50 (CPU replication) | CPU | v6 | 28 / 27 / 27 | 0.20% (PASS) | 0.854 (PASS) | 0.413 (FAIL) | +2.43 [+1.70, +3.22] (PASS) | **ADOPTED** |

Notes: seed 42 used older v1 code whose hash is not shipped. L1 and L2 are defined from v2 onward (v1 runs predate them; "-" means not measured). Natural-traffic samples overlap across v3, v4 and v5 (one query sample), so N1 values are repeated measurements.

Reading it: runs 42 to 47 are adopted; seed 48 (GPU, v4) and seed 49 (CPU, v5) are not; seed 50 (v6) is adopted on both stacks. The do-no-harm bound failed at seed 43 (0.75%) and seed 44 (1.28%); per-stratum (Mondrian) conformal calibration, introduced in v3, has passed in every run since. U1 (the unseen-fault arm exists from seed 43 on) has been below 0.50 in every run. The natural-traffic gain is +2.06 to +2.43 in all seven runs that measured it, **on one shared query sample**, so these are repeated measurements, not independent evidence.
**How v6 came about.** v5's three THIN detectors (R03, R15, R22) were first blamed on the generator loop and then, after a simulation of the proposed fix failed to reproduce the problem, on supply: those injectors are deterministic, so each base query gives at most one episode, and the test half of 2,400 base queries holds too few hard ones for a floor of 50. v6 uses all 5,527 already-examined ESCI queries and balances C2's pair mix. It was pre-registered before it ran (`docs/evidence/v6_protocol.md`).

### 5.2 The v6 runs (seed 50): the flagship on GPU, and a CPU replication

Code `kaggle/diagrag_v6.py`, SHA-256 `44176b9a…7546`, equal to the hash recorded in both runs' protocol files, which also record the library versions. **Run 1 (the headline): Kaggle T4, bge-reranker-large. Run 2: CPU, MiniLM-L6, same seed and settings.** Both were pre-registered and are reported side by side.

| | GPU T4 (headline) | CPU replication |
|---|---|---|
| (a) core 28, original rule | **27 detectors / 27 repairs: ADOPTED** | **28 / 27: ADOPTED** |
| Not solved | Q03 (detector 0.642 FAIL; repair 6 of 100) | Q03 (repair 1 of 100; its detector passed at 0.701) |
| (b) grounded set (22): detectors / repairs / solved | 20 / 20 / 20 (Q03, R26 not) | 21 / 20 / 20 (Q03, R26 not) |
| (c) quarantine set (10) | 10 / 10 / 10 | 10 / 10 / 10 |
| L1 clean loss (bar 0.5%) | PASS 0.28% | PASS 0.20% |
| L2 closure (bar 0.70) | PASS 0.844 | PASS 0.854 |
| **U1 (bar 0.50)** | **FAIL 0.406** | **FAIL 0.413** |
| N1 natural traffic, n = 1,648 | PASS +2.18 [+1.33, +3.03] | PASS +2.43 [+1.70, +3.22] |
| R03, R15, R22 (v5: THIN at 38, 44, 47) | 50 positives each, AUROC 1.000, 0.999, 0.950, PASS | 50 each, 1.000, 0.979, 0.955, PASS |
| C2 detector | PASS 0.751 (n = 50) | PASS 0.823 (n = 50) |

Per-fault results, GPU flagship (held-out detector AUROC with the number of held-out positives; repair rescue with the Wilson lower bound; tier S/M grounded, N/P quarantined; R25, R26, K11, K12 are outside the core 28):

| Fault | Group | Tier | Detector AUROC (n held-out positives) | Detector | Repair rescued / n (Wilson LB) | Repair | Solved |
|---|---|---|---|---|---|---|---|
| Q01 | Q | N | 0.997 (50) | PASS | 68 / 100 (0.58) | PASS | True |
| Q02 | Q | M | 1.000 (50) | PASS | 86 / 100 (0.78) | PASS | True |
| Q03 | Q | M | 0.642 (50) | FAIL | 6 / 100 (0.03) | FAIL | False |
| Q04 | Q | S | 0.976 (50) | PASS | 65 / 100 (0.55) | PASS | True |
| Q05 | Q | M | 0.994 (50) | PASS | 93 / 100 (0.86) | PASS | True |
| Q07 | Q | M | 0.999 (50) | PASS | 85 / 100 (0.77) | PASS | True |
| Q09 | Q | P | 0.999 (50) | PASS | 80 / 100 (0.71) | PASS | True |
| K03 | K | N | 1.000 (50) | PASS | 84 / 100 (0.76) | PASS | True |
| K04 | K | M | 0.887 (50) | PASS | 85 / 100 (0.77) | PASS | True |
| K05 | K | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| K06 | K | N | 1.000 (50) | PASS | 99 / 100 (0.95) | PASS | True |
| K07 | K | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| K08 | K | M | 1.000 (50) | PASS | 93 / 100 (0.86) | PASS | True |
| K09 | K | M | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| K11 | K | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| K12 | K | S | 1.000 (50) | PASS | 91 / 100 (0.84) | PASS | True |
| R01 | R | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R03 | R | N | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R05 | R | N | 0.990 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R06 | R | P | 0.982 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R07 | R | P | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R10 | R | N | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R11 | R | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R13 | R | M | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R15 | R | S | 0.999 (50) | PASS | 98 / 100 (0.93) | PASS | True |
| R19 | R | S | 1.000 (50) | PASS | 87 / 100 (0.79) | PASS | True |
| R22 | R | S | 0.950 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R23 | R | S | 0.999 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R24 | R | M | 0.888 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R25 | R | S | 1.000 (50) | PASS | 100 / 100 (0.96) | PASS | True |
| R26 | R | S | 1.000 (10) | THIN | 22 / 22 (0.85) | THIN | False |
| C2 | C | N | 0.751 (50) | PASS | 83 / 100 (0.74) | PASS | True |

R26 is THIN by construction (10 held-out positives in 4,000 attempts); it is outside the core 28.
**What the scorecard says.** The protocol's predictions (written before the run) were right that R03, R15 and R22 would reach 50 and pass, that C2 would pass, that the 27-detector rule would be met, that L1, L2 and N1 would pass, that U1 would not, and that the capped policy would meet all four targets. It was wrong on **Q03 on the CPU stack** (predicted fail with probability 0.9; it passed at 0.701, 0.001 above the bar). Details and the disclosures (v6 exists because v5 failed; the GPU job was relocated to another account after a two-hour queue; two construction changes make v6 a different test set from v5) are in amendments C1 to C5 of `docs/evidence/v6_protocol.md`.

### 5.2b The v5 run (CPU stack, seed 49, code `deecafad…702a`), fault by fault

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

**The three THIN detectors (corrected mechanism).** R03 (AUROC 1.000, 38 held-out positives), R15 (0.988, 44) and R22 (0.968, 47) were marked THIN, not failed, because they fell below the 50-positive floor that v5 introduced. I first explained this as a generator loop-budget flaw; a simulation of the proposed fix did not reproduce the failure, and the stored loop state showed the real cause: **supply**.
The injectors for these three faults are deterministic (R03 always uses the same truncated encoder configuration), so each base query can give at most one episode; the duplicate signature turned 56 to 58% of attempts into "not applicable" and no base query had two hard episodes (R10, with random noise, had 11). Only 7 to 9% of base queries are hard, and the test half of 2,400 base queries (872 ESCI queries against 1,528 for train) holds about 39 to 46 of them, matching the observed 38, 44 and 47.
**Counterfactual, not a verdict:** under v4's floor of 20 these three would pass, giving 27/28 and an ADOPTED verdict by the original numbers. The v5 verdict stands as NOT_ADOPTED because a bar chosen after seeing the result is not allowed. The remedy that was pre-registered and run is v6: all 5,527 examined ESCI queries as bases (section 5.2).

### 5.3 Natural traffic (no injection, 1,648 never-examined queries)
| Arm | n | v6 GPU: change in Hit@5 [95% CI] | v5 CPU | Reading |
|---|---|---|---|---|
| **Deployed loop** (v5/v6 config) | 1,648 | **+2.18 points [+1.33, +3.03]**, 42 fixed, 6 broken | +2.43 [+1.70, +3.22] | PASS in all seven runs |
| same loop, v4 config (natural misspelling repair on) | 1,648 | +2.12 [+1.21, +2.97], 45 fixed, 10 broken | +2.43 [+1.58, +3.28] | the config correction removes 3 to 4 broken queries (10 to 6 on GPU) and leaves the point estimate almost unchanged |
| natural rules K12 and K05 alone | 1,648 | +2.18 [+1.40, +3.03] | +2.43 [+1.70, +3.22] | all of the gain |
| classifier dispatch alone | 1,648 | +0.24 [-0.12, +0.61] | +0.30 [+0.06, +0.61] | tiny |
| duplicate collapse (K05) where duplicates occur | 141 | +6.38 [+2.11, +11.35] | +5.00 [+1.43, +9.29] | PASS |
| chunk-crowding collapse (K12) where it occurs | 607 | +4.28 [+2.47, +6.10] | +4.87 [+3.14, +6.59] | PASS |
| **natural misspelling repair (QLEX)** | 185 | **-5.41 [-10.81, -0.54]** | -4.86 [-10.81, +0.54] | **HARM** on GPU; interval touches zero on CPU |
| deployed loop on those 185 queries (misspelling repair off) | 185 | +1.08 [0.00, +2.70] | +0.54 [0.00, +1.62] | the harm is gone |
| SymSpell (external baseline) | 185 | **-12.43 [-17.85, -7.01]** | -11.35 [-17.84, -4.86] | HARM |

So the gain on real traffic comes from two simple rules, not from diagnosis. The misspelling repair has a negative point estimate in all eight runs that measured it (-4.9 to -7.1 points), with an interval that excludes zero in three of them (the GPU runs of seeds 46, 48 and 50) and one that touches zero in the others, and the deployed configuration switches it off for natural traffic. The pre-registered D3 test (detection-gated rules versus always-on K12) passed in v5 and on the v6 CPU replication and failed (lower bound exactly 0.00) on the v6 GPU run; D2 (loop non-inferior to a diagnosis-free universal repair) passed on v6 GPU (lower bound -0.49 against a -0.50 margin) and failed on v5 and v6 CPU (-0.61, -0.55).

### 5.4 Diagnosis against baselines (held-out episodes)
| Method | Fault-vs-clean AUROC | Run |
|---|---|---|
| **DiagRAG attributor** (supervised, 1 minus P(clean)) | **0.975** | v6 GPU (0.979 in v5 CPU) |
| RAGLog tier-0 features, same classifier (authors' code, no LLM checks) | 0.735 [0.720, 0.751] | v6 GPU (0.762 in v5 CPU) |
| query-performance predictors NQC / WIG | 0.583 / 0.566 | v6 GPU |
| zero-shot LLM judge, **Gemini 3.1 Flash-Lite** (n = 320) | 0.754 [0.702, 0.804] against 0.975 for ours: difference **+0.222 [+0.173, +0.270]** | LLM comparison, v3 CPU episodes |
| zero-shot LLM judge, **gpt-oss-120b** (n = 320, complete) | 0.701 [0.645, 0.753]: difference **+0.274 [+0.222, +0.332]** | same |
| zero-shot LLM judge, **gpt-oss-20b** (n = 320, complete) | 0.629 [0.573, 0.682]: difference **+0.347 [+0.292, +0.402]** | same |

All three arms are **complete** (earlier numbers for the two Groq arms were partial); the verdict is OURS_BETTER in every arm under the pre-registered rule. The judges' cause-group accuracy on faulted episodes is 0.42, 0.20 and 0.33 against 0.81 for ours, at 587 to 681 tokens per item against none.
This comparison **favours us**: our model had 2,718 labelled episodes and the LLM judges had none (supervised against zero-shot), our probes were designed for these faults, and RAGLog's own LLM checks were not run. **No frontier model was available** (the Gemini key returned quota errors for its Pro-class models; the only newer model that answered took 28 to 51 seconds per call), so the standing objection "you only beat free-tier models" is **not answered**.

**Repair against a CRAG-style loop (natural queries).** On the extended Gemini sample (**n = 1,000**, all complete) the CRAG-style repair gained +0.99 points [+0.30, +1.80] (13 fixed, 3 broken, 1.13 LLM calls per query) and DiagRAG's deployed loop +2.22 [+1.10, +3.40] (27 fixed, 5 broken, 0 LLM calls). The difference is **+1.23 points [-0.10, +2.60]: OURS_NON_INFERIOR** under the pre-registered margin (lower bound above -0.5), not "better" (the interval touches zero). On the original first-300 sample it is still +0.66 [-1.33, +2.67], INCONCLUSIVE. The two Groq arms, now complete on the first 300 queries, give INCONCLUSIVE as well (+1.32 [-0.67, +3.67] and +0.98 [-1.33, +3.33]).

### 5.5 The do-no-harm guarantee as a frontier (held-out clean queries)
| Policy | Clean loss | Total clean dispatch | Mean cost | Mean closure | Meets all four targets | v6 CPU |
|---|---|---|---|---|---|---|
| tau at 5% false alarm (no guarantee) | 0.12% | 3.7% | 0.19 | 0.831 | yes | yes |
| global CRC 0.005 | 0.56% | 54.1% | 2.75 | 0.866 | **no** (loss above 0.5%) | no (loss 0.60%) |
| **Mondrian CRC 0.005 (the L1 gate)** | 0.28% | **86.2%** | 3.65 | 0.844 | no | no |
| **capped CRC 0.005** | **0.12%** | **16.5%** | **0.93** | **0.834** | **yes** | **yes** |
| two-stage 0.005 | 0.24% | 48.4% (classifier 16.5%) | 2.10 | 0.814 | no | no |
| diagnosis-free universal repair | 1.48% | 100% | 12.00 | 0.749 | no | no |

(v6 GPU; the last column says whether the same holds on the v6 CPU replication.) Targets: loss at most 0.5%, total clean dispatch at most 25%, mean cost at most 1.5, closure at least 0.80. **The 86 to 89% dispatch is not the price of the guarantee**: the stratified threshold is the smallest one the loss bound allows, so it dispatches nearly everything in the common stratum. Capping dispatch at 20% on the calibration set keeps the bound and costs 1.0 to 1.2 points of closure. The single-threshold `global_crc` met all four targets in v5 (loss 0.15%) but **broke the 0.5% bound on both v6 stacks** (0.56%, 0.60%), which the capped per-stratum policy did not; the pre-registered claim rule therefore picks `capped_crc_0.005` on every run where it has been evaluated (v5 CPU, v6 GPU, v6 CPU). The two-stage policy misses because the natural rules K12 and K05 fire on about 35% of clean queries (they help on natural traffic, so this is a finding about the data, not an error).

### 5.6 Unseen faults (U1) and the identifiability analysis
Mean closure on a fault the attributor never saw: 0.395 (GPU v3), 0.485 (CPU v4), 0.456 (GPU v4), 0.440 (CPU v5), **0.406 (GPU v6) and 0.413 (CPU v6)**; bar 0.50. Group fallbacks raised it from 0.24 to 0.365 in v3 (CPU) and v4's group-level attributor to 0.485 (CPU), but it never crossed the bar, and the two v6 runs are the lowest since v3. Why:
- **Group attribution** on unseen faults is right only 40% to 58% of the time (0.50 on v6 GPU, 0.44 on v6 CPU).
- **Several faults have no effective repair**: K06, Q03, Q07 and Q09 stay at or below 0.08 closure in every run with fallbacks, and Q02 joins them in the last four runs.
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
Q03 detector AUROC by construction era (inverse-variance means, 95% CI; all ten judged runs):

| Era | Runs | AUROC per run | Mean [95% CI] | Within-era heterogeneity | Passes |
|---|---|---|---|---|---|
| injected synonym swap | seeds 42, 43, 44 | 0.866, 0.934, 0.877 | **0.912 [0.874, 0.950]** | Q = 2.42, df 2, p = 0.30 | 3 of 3 |
| real query pairs from other users | seeds 45 to 50 (seven runs) | 0.559, 0.654, 0.704, 0.691, 0.640, 0.642 (GPU), 0.701 (CPU) | **0.659 [0.626, 0.691]** | Q = 6.78, df 6, p = 0.34 | **2 of 7** |

The era difference is 0.253 AUROC (z = 9.9). The upper end of the real-pair interval (0.691) is below the 0.70 bar, and the two passes (0.704 and 0.701) are both just above it, which is what a true value near 0.66 would give. The injected and the natural paraphrase task are different problems, and the repair that rescues injected synonym swaps rescues 1 to 6 of 100 real-pair episodes.

### 6.2 C2: the seed-48 failure is explained
C2 is two faults at once; its score is the second-largest group probability mass of an attributor that never trains on C2. The generator drew one of 12 pair types at random, about four per type. **Six pair types have almost no second-group mass** (Q03+R05, Q04+K05, Q04+R10, K04+R24, Q05+R24, K04+R03: the first fault masks the second). In seed 48 the 25 test positives had unlucky composition (5th percentile of random splits) and scored far below the 25 train positives under the same head (medians 0.002 and 0.136, p = 0.003). With composition fixed the test AUROC was still low (p = 0.013), but the worst of seven runs reaches that with probability 8.6%. All 50 C2 positives are ESCI, one tenant, k = 5, so source and tenant cannot explain it. **Verdict: a construction artefact plus ordinary small-sample variance.** v5 (n = 50, CPU) passed at 0.785; v6, with the pair mix balanced inside each split, passed at 0.751 (GPU) and 0.823 (CPU).

### 6.3 The reproducibility gap is identified: it is the scikit-learn version
Re-fitting the detectors from a run's shipped episodes reproduced CPU runs exactly but not Kaggle GPU runs (27 of 31 for v4 seed 48, with the C2 head 0.019 off). The v4 protocol had not recorded library versions, so I called the cause unresolved. The v6 runs record them (Kaggle: scikit-learn 1.6.1, numpy 2.1.3, torch 2.11.0+cu130), which allowed a direct test:
- Re-fitting the **v6 GPU** run's detectors under scikit-learn 1.6.1 reproduces **31 of 31 AUROCs exactly** (largest difference 0.0000); under 1.9.1 the same data gives 28 of 31 (Q03 moves from 0.642 to 0.613).
- Re-fitting the **v4 GPU (seed 48)** and **v3 GPU (seed 46)** runs under 1.6.1 also gives **31 of 31 exactly**, and the C2 head reproduces its recorded **0.6116** (0.6310 under 1.9.1).
So the earlier gap came entirely from re-fitting with a newer library than Kaggle's. The recorded verdicts are unchanged. The practical consequence for anyone reproducing: **install the library versions recorded in the protocol file** (`requirements.txt` lists both sets).
A consequence for the record: a detector near its bar can move by 0.03 between scikit-learn versions (Q03: 0.642 against 0.613), so verdicts that depend on a margin of 0.001 to 0.005 (Q03's CPU pass at 0.701) are fragile in a way unrelated to the data.

### 6.4 Why v5 had three THIN detectors, and what v6 showed
See section 5.2b. The explanation I first gave (a loop-budget flaw) was wrong; the cause is supply of distinct test queries for deterministic low-yield faults. v6 tested that explanation by changing only the supply (all 5,527 examined base queries): R03, R15 and R22 each reached 50 held-out positives on both stacks and passed (AUROC 0.95 to 1.000). A prediction that could have failed did not.

---

## 7. What failed, plainly

1. **Adoption was missed twice before it was met:** v4 on GPU (26/28) and v5 on CPU (24/28, three of them my own floor). v6 is ADOPTED on both stacks, but only after a construction change motivated by v5's failure; a reviewer will see the whole matrix.
2. **U1:** below 0.50 in all nine runs that measured it (seeds 43 to 50), and **lower in v6 (0.406, 0.413) than in v4 (0.485 and 0.456)**. No proved ceiling.
3. **Q03:** the detector passes in 2 of 7 runs of its natural construction, by 0.004 and 0.001; its repair rescues 1 to 6 of 100.
4. **Natural misspellings:** the repair does not help, and the external baseline hurts more.
5. **Frontier LLM comparison:** not run. No frontier model was reachable on the supplied keys. All three free-tier arms are complete and OURS_BETTER on diagnosis; on repair the Gemini arm is OURS_NON_INFERIOR on 1,000 queries and the Groq arms are inconclusive.
6. **Second corpus:** subset ports only (FiQA 19/20, SciFact 15/20); no full-suite port. Q02, Q09 and C2 need new features, a retrieval option and a state merger on the port stack, which was not attempted.
7. **Release:** the benchmark is staged, not published (the name, the ShopNova licence and the timing are the owner's).
8. **The v6 pass is a pass on a changed construction** (6,000 base queries, balanced C2 mix), not a pass on the v5 test set.

---

## 8. Time line of how the project got here (short)

Core-28 notebook (CPU seeds 42, 43) → v2 with natural-validation arms and family-level loop (seed 44) → v3 with licence-clean corpus, tiers, conformal calibration and external baselines (CPU seed 45, GPU seed 46) → v4 with a group attributor (CPU seed 47, GPU seed 48) → ports (SciFact, FiQA), LangChain v1 and v2, LLM baselines (free tiers), benchmark v1.0 → diagnosis of the gate flips, v5 pre-registration and run (CPU seed 49, NOT_ADOPTED) → correction of the THIN diagnosis, v6 pre-registration, GPU flagship and CPU replication (seed 50, ADOPTED on both), completion of the LLM arms, identification of the reproducibility gap → this document.

---

## 9. What is in the repository and how to run it

- `PROJECT_EXPLAINED.md` (this file), `README.md`, `NOTICE.md` (licences).
- `kaggle/` : every notebook and script (v1 to v6, ports, LangChain), the natural-traffic exclusion files, and one `judged_*` folder per judged run (protocol with code hash and library versions from v5 on, verdict, tables, report; episode files are in the zip).
- `docs/` : `ROADMAP_V3.md`, `ROADMAP_V4.md` (execution record), `ALL_RUNS_MATRIX.md` (generated), `IDENTIFIABILITY.md`, `CORE28_FAULTS.md`, `EVIDENCE_AND_NOVELTY_REPORT.md`, `LLM_BASELINES_RESULTS.md`, `REPRODUCE.md`, and `docs/evidence/` (protocols with every amendment: `v5_protocol.md` B1 to B8, `v6_protocol.md` C1 to C5, `llm_baselines_plan.md` A1 to A7; analysis scripts and results).
- `bench/` : DiagRAG-Bench v1.0 public files, scorer, quickstart, verifier. `paper/` : outline and a workshop draft.

**To run.** See `RUN_GUIDE.md`: verify the files (10 seconds), re-fit the detectors from shipped episodes (30 seconds per run; **use the library versions in the protocol file**), run the benchmark quickstart, run any judged script on a laptop CPU in resumable chunks, or run a notebook on a Kaggle GPU. The LLM scripts need keys supplied as environment variables only.

---

## 10. Honest assessment

**Where the project stands: about 7.8 out of 10.** This is my judgement from the evidence, not a measurement and not a venue prediction. It was about 7.5 before the v6 runs. The change is earned by: a pre-registered flagship that is **ADOPTED on the GPU stack** (with a CPU replication), a prediction about a diagnosed construction limit that could have failed and did not, a completed LLM comparison, the guarantee frontier measured on two stacks, and the reproducibility gap identified and fixed (versions recorded).

*Strong.* A well-posed problem with field evidence for each fault; a method with a stated guarantee; protocol discipline that is unusual (hash-bound code, dated amendments, failures in the main table, a wrong diagnosis corrected in the open); a natural-traffic gain measured seven times; a rigorous identifiability table; a benchmark with a private split; and a record of its own corrections.

*Weak.* The ADOPTED verdict followed two failures and a construction change; U1 stayed below its bar and got worse; the gain on natural traffic comes from two simple rules; the diagnosis advantage is over baselines that favour us (supervised against zero-shot); one e-commerce corpus carries the evidence; no frontier-LLM comparison; the repair loop is only non-inferior to a CRAG-style repair, not better; the code was written by an AI assistant under the owner's direction.

**Against the target (CORE A, a CIKM or WSDM-class paper), the seven attacks an A reviewer will make:**

| Attack | State |
|---|---|
| "Your flagship run is NOT_ADOPTED" | **mostly closed**: the pre-registered v6 flagship is ADOPTED on GPU and CPU; v4 (GPU) and v5 (CPU) remain in the matrix as misses, and Q03 is a known failing detector |
| "Your unseen-fault claim fails its own bar" | **open**: 0.406 and 0.413, no ceiling proved |
| "Your guarantee costs 90% dispatch" | **closed**: capped CRC, 16.5% dispatch, closure 0.834, on two stacks |
| "You beat free-tier LLMs; so what" | **open**: all free-tier arms done; no frontier arm |
| "One corpus" | **open**: subset ports only |
| "Artefact?" | **staged**, not released (owner decisions) |
| "Can I trust any of this?" | **addressed**: all-runs matrix, amendments, reproducibility gap identified, this document |

**Why not 8.3 to 8.5.** An A venue still has three open attacks (unseen faults, a frontier-model comparison, a second corpus at suite scale) and an unreleased artefact. I estimate that closing the frontier comparison and the second corpus, and releasing the benchmark, would reach about 8.2; **8.5 would need outside adoption or independent replication, which this repository cannot produce.** 9 is not a target.

---

## 11. Limitations (ours, first)

- **Injected faults, same authors.** The 28 faults are injected by the people who wrote the detectors and repairs; a pass shows the method works on this construction, not on any production RAG system.
- **One domain carries the evidence.** E-commerce search in English. The ports (FiQA, SciFact, LangChain) cover 15 to 20 faults each and use smaller stacks.
- **Quarantine set.** Ten faults (tiers N and P) are reported but excluded from headline claims because their field evidence is weaker. C2 is among them.
- **Natural-traffic evidence rests on one sample.** The seven measurements of the gain use the same 1,648 queries.
- **The guarantee's cost.** The gate that carries the proof (stratified CRC) dispatches on 86 to 89% of clean queries; the cheap variant (capped CRC) keeps the loss bound by construction (loss is monotone in the threshold) but was selected after the stratified one, and its held-out figures come from two runs.
- **Q03** is construction-dependent (section 6.1) and its CPU pass is 0.001 above the bar; **natural misspellings** are not repaired (section 5.3).
- **Supervised against zero-shot** in the LLM comparison; free-tier models; reduced RAGLog and CRAG variants; no frontier model.
- **Library versions matter.** A near-bar detector moves by up to 0.03 between scikit-learn versions; verdicts decided by 0.001 to 0.005 are fragile (section 6.3).
- **Single-run adoption.** Each configuration was judged once per stack and seed; the seed-to-seed spread is visible in the matrix and is not small for the faults that flip.
- **v6 is a different test set from v5** (more base queries, balanced C2 mix); its pass does not mean v5's would have passed.

---

## 12. Authorship, disclosure and open items

**Disclosure.** The code and documents in this project were written by Claude (Anthropic), directed by the repository owner. The owner words the disclosure in any paper.

**Keys.** The owner pasted API keys into the chat three times. They were used only as environment variables during the work and are not stored in the repository, the zips, the logs or any result file (scans were run before each push). **A key pasted in a chat is a leaked key: regenerate every one.**

**Open items for the owner (not decided by the assistant).**
1. A frontier-model arm: provider, model, key (as an environment variable), prices and a spend cap of USD 15 set in the provider console first. Amendment A6 records that none was available on the supplied keys.
2. A full-suite second-corpus port (needs new features for Q02, Q09 and C2 on the port stack and an owner-approved pre-registration).
3. Benchmark name, ShopNova licence, release timing; whether to send the replication email (`docs/REPLICATION_INVITATION.md`, a draft) or submit the workshop draft (`paper/WORKSHOP_DRAFT.md`).
4. Delete the throwaway Kaggle notebooks (`diagrag-v4-notebook-smoke`, `diagrag-v6-gpu-smoke`) and decide whether to keep the v6 GPU kernel.
