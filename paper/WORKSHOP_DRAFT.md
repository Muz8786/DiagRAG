# Diagnosing retrieval failures in RAG from telemetry alone: a benchmark, a repair loop, and what failed

**DRAFT for the owner. Not submitted.** Length target about 2,000 words; the page count depends on the venue template and has not been checked. Venue, authorship and disclosure wording are the owner's decisions.
Every number below is taken from a file in the repository and carries its run label (seed, stack). Numbers marked *v4 GPU* come from `kaggle/judged_gpu_v4_seed48/`.

## Abstract

When a RAG system answers badly, the cause is often in the retrieval stage, and the stage rarely says so. We study whether retrieval telemetry alone (scores, ranks, probe results; no generated answer, no labels at run time) can tell a faulty retrieval from a healthy one, name the cause, and trigger a repair that does not harm healthy queries.
We build 32 injected fault types with evidence tiers tied to field reports, a 4,843-episode benchmark, and a repair loop with a conformal bound on harm to healthy queries.
On a GPU run, the telemetry diagnoser separates faulty from clean episodes at AUROC 0.977, against 0.761 for the retrieval-stage features of an existing system (RAGLog) with the same classifier, and 0.64 to 0.75 for zero-shot LLM judges of the returned documents (smaller CPU sample, free-tier models).
A repair loop gained 2.18 points of Hit@5 [1.27, 3.16] on 1,648 never-examined natural queries; four runs gave +2.06 to +2.31 on that one query sample. We also report what failed: the pre-registered adoption gate was missed in the latest GPU run (26 of 28 detectors, 27 needed), closure on unseen faults stayed below its bar (0.456 against 0.50), and repairing natural misspellings does not help.
Most of the room for improvement on natural traffic is bounded by noise in the gold labels, which we measure.

## 1. Problem and framing

Diagnosis is not detection. A detector says that retrieval failed; a diagnoser says where, so that a targeted repair can run, and does so without an LLM call per query. We ask three questions. Can telemetry identify the fault? Can a repair chosen from the diagnosis help on real traffic? Can the loop promise not to hurt queries that were fine?

## 2. Setup

**Faults.** 32 injected fault types in three groups: query (Q), knowledge base (K) and retrieval stack (R), plus one two-fault combination. Each carries an evidence tier (S, M, N, P) linking it to public field reports; headline claims use the 22 faults of tier S or M.
**Episodes.** An episode is kept only if the clean pipeline succeeds on the query and the faulted pipeline fails, so every episode has something to repair. Corpus: licence-clean product text (ESCI, ABO, an OFBiz manual, a synthetic partition).
**Telemetry.** 63 features computed from the retrieval trace, such as score gaps, rank agreement between dense and lexical legs, duplicate and chunk-crowding counts, and cheap probes.
**Gates, fixed before each run.** Detector: held-out AUROC at least 0.70. Repair: the Wilson lower bound of the rescue rate at least 0.50, with at most 10% of clean successes lost. Adoption: at least 27 of 28 detectors and 24 of 28 repairs. Loop: held-out clean loss at most 0.5% (L1), mean closure at least 0.70 (L2), unseen-fault closure at least 0.50 (U1), and a natural-traffic gain whose 95% interval excludes zero (N1).

## 3. Results

**Diagnosis (v4 GPU).** Fault-versus-clean AUROC 0.977. RAGLog's tier-0 features with the same classifier reach 0.761 [0.738, 0.780]; the best single tier-0 feature 0.646; query-performance predictors 0.58 to 0.59. This comparison favours us, because our telemetry includes probes designed for these faults and RAGLog's LLM checks were not run.
**LLM judges (v3 CPU seed 45; a different, smaller sample).** An LLM that sees the query and the five returned documents and rates the chance of failure reached AUROC 0.754 (Gemini 3.1 Flash-Lite, n = 320), 0.731 (gpt-oss-120b, partial n = 163) and 0.642 (gpt-oss-20b, partial n = 169), against 0.975 for the supervised diagnoser on the same episodes (differences +0.22 to +0.34, all intervals above zero).
The diagnoser had 2,718 labelled episodes and the LLMs none, so this is supervised against zero-shot. It is not full RAGLog.
**Do-no-harm (v4 GPU).** With a per-stratum conformal threshold, held-out loss on clean queries was 0.0% (bar 0.5%) and mean closure on injected faults 0.866. The threshold dispatches a repair on 88.8% of clean queries, which is expensive. A capped variant is registered for the next run (Section 5).
**Natural traffic.** On 1,648 queries that no earlier run had examined, with no injection, the deployed loop gained +2.18 points of Hit@5 [+1.27, +3.16] (47 queries fixed, 11 broken) in v4 GPU. The same measurement was +2.06 (v3 GPU), +2.25 (v3 CPU) and +2.31 (v4 CPU). The four runs share one query sample, so they are repeated measurements, not independent samples.
Nearly all of the gain comes from two rules (duplicate and chunk-crowding collapse); the classifier added +0.42 points [-0.12, +0.97] on its own.

**Noise in the gold labels (census, v4 GPU).** Over 7,175 ESCI queries with an Exact product in the corpus, the clean pipeline fails on 43.5% [42.4, 44.7]. The gold document is itself a placeholder ("nan") text in 58.6% of queries and in 69.1% of failures. A repair cannot rescue a query whose gold document has no content, which bounds the repairable share of failures. We report this as a finding about the benchmark data, not as a caveat.

## 4. What failed

- **The adoption gate (v4 GPU).** 26 of 28 detectors passed. Q03 (a paraphrase by another real user) and C2 (two simultaneous faults) failed their detector gates. Re-fitting the detectors from the shipped episodes shows two different causes. Q03's true AUROC dropped when its construction changed from synonym swaps (0.912 over three runs) to real query pairs (0.645 [0.59, 0.70] over four runs), so it fails by expectation. C2 passes in the pooled data (0.76 to 0.85 in all seven runs) and its test-split value swings more than random re-splitting predicts (variance ratio 5.8); we did not identify why.
- **Unseen faults.** Mean closure on faults the attributor never saw: 0.395, 0.456 and 0.485 in the three runs with group fallbacks (bar 0.50). The faults with closure at or below 0.08 in all three runs (K06, Q03, Q07, Q09) have no effective repair, and a pre-registered neighbour-retrieval probe added no separation (Q03 against the rest 0.609 to 0.598 on the training split).
- **Natural misspellings.** The repair has a negative point estimate in all five runs that measured it (-4.9 to -7.1 points); the interval excludes zero in two. SymSpell is worse (-11 to -12). The v5 protocol switches natural-misspelling repair off.
- **Framework stack.** A LangChain pipeline solved 7 of 15 faults, then 11 of 15 after fixes designed once the first result was known. The second result sits exactly at its bar.
- **Reproducibility.** Re-fitting the detectors from the shipped episodes reproduces a CPU run exactly (31 of 31 AUROCs) but differs for 4 of 31 on a Kaggle GPU run, by up to 0.04, because of a library difference whose versions were not recorded. A re-fit of Q03 on that run gives 0.709 against the recorded 0.691. The recorded verdict stands; later runs record library versions.

## 5. Benchmark and next run

DiagRAG-Bench v1.0 has 2,718 dev episodes with public labels and 2,125 test episodes whose labels are held privately, with a published SHA-256 commitment. A scorer, a reference diagnoser (test AUROC 0.976 [0.969, 0.982]) and a five-minute quickstart ship with it.
The next judged run (v5, one GPU run, seed fixed in advance) raises the measurement floor to 50 held-out positives per fault, adds two dispatch policies with four reported targets (clean loss, clean dispatch, cost, closure), and corrects the deployed configuration. The protocol, including predictions we expect to be wrong, is in `docs/evidence/v5_protocol.md`.

## 6. Limitations

Faults are injected by the same authors who wrote the detectors and repairs. The stack is e-commerce search with one corpus; two other domains and one framework stack were tested on smaller fault sets. Natural-traffic evidence rests on one query sample. LLM baselines use free-tier models and one zero-shot prompt, and are not the full RAGLog or CRAG systems. Single runs per configuration.

## Disclosure

The code and documents in this project were written by Claude (Anthropic) under the direction of the repository owner. [Owner: confirm the authorship and disclosure wording your venue requires.]
