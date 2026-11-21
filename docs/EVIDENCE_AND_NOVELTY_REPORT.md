# DiagRAG core-28 — evidence, grounding and novelty report

Date: 14 Nov 2026. Scope: this project's own core-28 suite (`kaggle/diagrag_core28.py`).
The other DiagRAG project (47-fault catalogue, `Muz8786/diagrag-data`) is kept separate.
None of its definitions are used here.

Labels used throughout:
- **[OBS-IND]**: observed in industry evidence (link given).
- **[OBS-DATA]**: observed in a file of ours (path given).
- **[HYP]**: hypothesis.
- **[REC]**: recommendation.
- **[MEAS]**: measured in a run under frozen gates (file given).

**Provenance of the GPU figures in the brief.** The brief quotes a judged GPU run (28/28 + 28/28; Q01 closure 0.10 with
attribution 0.025; Q03 closure 0.225; clean −0.78%). I could not find its output files:
- They are not in `Muz8786/DiagRAG`.
- `Muz8786/diagrag-data` holds the other project's notebook, and it has no saved outputs.

So I report those figures as user-reported and unverified. The pattern they show (Q01 lost to Q04 attribution) matches the
pre-fix dispatch I measured in CPU seed 42 (`kaggle/judged_cpu_run_seed42/closed_loop.csv`: Q01 attribution 0.04).

## 1. Industry failure map

How the evidence was gathered:
- **GitHub issue search:** REST `search/issues`, issues only, sorted by comment count, run on 14 Nov 2026.
  Raw hits: `docs/evidence/github_issue_hits_*.json`. Bodies read: `docs/evidence/issue_bodies.txt`.
- **Web search** for practitioner write-ups and papers.

Each row gives what failed, at which layer, and how it was noticed. Everything in this table is [OBS-IND].

| # | Layer | What failed (one line) | How it was noticed | Source |
|---|---|---|---|---|
| I1 | index (filtered ANN) | HNSW + WHERE filter returns fewer/zero rows because the filter is applied after the ANN candidate list | user saw fewer results than LIMIT | [pgvector#259](https://github.com/pgvector/pgvector/issues/259), [pgvector#263](https://github.com/pgvector/pgvector/issues/263) |
| I2 | index (filtered ANN) | HNSW + range filter recall ≤ ~0.5 while unfiltered ≈ 1.0 | user recall benchmark vs IVF_FLAT | [milvus#44854](https://github.com/milvus-io/milvus/issues/44854) |
| I3 | index (filtered hybrid) | hybrid search filters ineffective for strict pre-filtering | results outside the filter | [weaviate#7681](https://github.com/weaviate/weaviate/issues/7681) |
| I4 | index (ANN recall) | low recall with IVF/IMI/PQ settings; recall low when efSearch < k | recall measured vs brute force | [faiss#600](https://github.com/facebookresearch/faiss/issues/600), [faiss#1244](https://github.com/facebookresearch/faiss/issues/1244), [milvus#27334](https://github.com/milvus-io/milvus/issues/27334) |
| I5 | index (ANN maintenance) | IVFFlat: new inserts hard to find unless probes very high (centroids stale) | user noticed missing new rows | [pgvector#139](https://github.com/pgvector/pgvector/issues/139) |
| I6 | index (rescore) | kNN silently drops candidates from rescore window; "no error, hit count looks normal; recall drops" | maintainer analysis | [elasticsearch#164821](https://github.com/elastic/elasticsearch/issues/164821) |
| I7 | index (coverage) | indexed_vectors_count = 0 although points exist | collection info | [qdrant#2659](https://github.com/qdrant/qdrant/issues/2659) |
| I8 | index (coverage) | persisted index returns empty after restart | empty query results | [chroma#640](https://github.com/chroma-core/chroma/issues/640) |
| I9 | index (coverage/replication) | CDC target stops at about half of source rows; data inconsistent after migration across nodes | row counts / per-node results differ | [milvus#49712](https://github.com/milvus-io/milvus/issues/49712), [qdrant#5101](https://github.com/qdrant/qdrant/issues/5101) |
| I10 | serving (partial results) | some queries retrieve only 1 doc or a small subset | user | [qdrant#3094](https://github.com/qdrant/qdrant/issues/3094) |
| I11 | index (non-finite vectors) | NaN/Inf vectors accepted; NaN scores rank above finite ("silent HNSW corruption") | user repro | [qdrant#9201](https://github.com/qdrant/qdrant/issues/9201) |
| I12 | index (non-finite vectors) | IndexFlatL2 silently drops rows with non-finite components (-1 slots) | user repro | [faiss#5684](https://github.com/facebookresearch/faiss/issues/5684) |
| I13 | index (non-finite scores) | cosine distance returns NaN for small/finite vectors | user repro | [pgvector#1033](https://github.com/pgvector/pgvector/issues/1033), [pgvector#1057](https://github.com/pgvector/pgvector/issues/1057) |
| I14 | fusion (non-finite) | DocumentJoiner propagates NaN scores into final sort | maintainer | [haystack#13678](https://github.com/deepset-ai/haystack/issues/13678) |
| I15 | fusion (normalisation) | distribution-based fusion zeros scores for single-doc / equal-score lists | maintainer | [haystack#12507](https://github.com/deepset-ai/haystack/issues/12507) |
| I16 | fusion (weights) | fusion weights bound to arrival order, not declared order | maintainer | [haystack#12646](https://github.com/deepset-ai/haystack/issues/12646) |
| I17 | fusion (merge) | BM25 results dropped from hybrid results for any alpha; relativeScoreFusion returns only vector results | user | [weaviate#10350](https://github.com/weaviate/weaviate/issues/10350), [weaviate#3243](https://github.com/weaviate/weaviate/issues/3243) |
| I18 | fusion (normalisation/depth) | min-max + arithmetic-mean ranking unexpected; hybrid score depends on number of results requested (docs not surfaced unless size large) | user | [opensearch-neural-search#910](https://github.com/opensearch-project/neural-search/issues/910), [#325](https://github.com/opensearch-project/neural-search/issues/325) |
| I19 | fusion (depth) | small limits need overfetching to score hybrid correctly | maintainer | [weaviate#3317](https://github.com/weaviate/weaviate/issues/3317) |
| I20 | sparse (analyzer) | BM25 returns no results in some situations (tokenizer/stopwords config) | user | [weaviate#3517](https://github.com/weaviate/weaviate/issues/3517) |
| I21 | sparse (analyzer) | default BM25 tokenizer recall failure for CJK; fix trades precision | maintainer | [haystack#12867](https://github.com/deepset-ai/haystack/issues/12867) |
| I22 | sparse (index) | BM25 inverted index corruption after crash | panics | [weaviate#4125](https://github.com/weaviate/weaviate/issues/4125) |
| I23 | corpus (duplicates) | refresh inserts instead of upserting → duplicate docs | user | [llama_index#8832](https://github.com/run-llama/llama_index/issues/8832) |
| I24 | corpus (duplicates) | retriever returns the same document more than once | user | [langchain#22361](https://github.com/langchain-ai/langchain/issues/22361), [chroma#2588](https://github.com/chroma-core/chroma/issues/2588) |
| I25 | corpus (deleted docs) | nearVector returns objects deleted long ago; query non-empty after delete | user / CI | [weaviate#3868](https://github.com/weaviate/weaviate/issues/3868), [milvus#16961](https://github.com/milvus-io/milvus/issues/16961) |
| I26 | corpus (drift) | index drift: deleted docs, stale chunks, duplicate embeddings; detect by comparing source identity/version with what retrieval returns | practitioner guide | [Oracle blog](https://blogs.oracle.com/developers/how-to-detect-rag-index-drift-deleted-docs-stale-chunks-and-duplicate-embeddings) |
| I27 | corpus (stale vectors) | irrelevant results from catalog drift; re-embed one listing and compare with stored vector | practitioner guide | [dev.to](https://dev.to/merrickvance8452/how-to-debug-irrelevant-vector-query-results-game-catalog-drift-2l8f) |
| I28 | index (metadata desync) | payload keyword index desynchronises from stored payloads under concurrent writes | user repro | [qdrant#10302](https://github.com/qdrant/qdrant/issues/10302) |
| I29 | filter (ignored) | doc_ids constraint ignored, whole index searched; OR filter ignored; OData filter not filtering; ID selector ignored | user / repro | [llama_index#11602](https://github.com/run-llama/llama_index/issues/11602), [#11565](https://github.com/run-llama/llama_index/issues/11565), [#19370](https://github.com/run-llama/llama_index/issues/19370), [faiss#5504](https://github.com/facebookresearch/faiss/issues/5504) |
| I30 | filter (wrong rows) | payload filter returns points missing the filtered field | user repro | [qdrant#9255](https://github.com/qdrant/qdrant/issues/9255) |
| I31 | embedding (model migration) | switching the embedding model without re-embedding silently breaks retrieval; with equal dimensions nothing errors | practitioner write-ups | [tianpan 1](https://tianpan.co/blog/2026/05/07/embedding-model-churn-vector-index-invalidation), [tianpan 2](https://tianpan.co/blog/2026/07/05/retiring-an-embedding-model-reindex-without-downtime), [substack](https://thehard70.substack.com/p/why-does-switching-embedding-models), [medium](https://isuruig.medium.com/embedding-model-migration-without-downtime-the-drift-adapter-pattern-for-production-vector-6f3c62abed99) |
| I32 | embedding (dimension) | embedding dimension mismatch between model and collection (loud error) | exception | [chroma#1862](https://github.com/chroma-core/chroma/issues/1862), [llama_index#10166](https://github.com/run-llama/llama_index/issues/10166) |
| I33 | embedding (truncation) | inputs silently truncated at max_seq_length, no signal to caller | maintainer discussion | [sentence-transformers#4060](https://github.com/huggingface/sentence-transformers/issues/4060), [llama_index#10461](https://github.com/run-llama/llama_index/issues/10461) |
| I34 | embedding (prompts) | document prompt never applied; how to add query instruction for BGE in a vector DB | user / maintainer | [sentence-transformers#4090](https://github.com/huggingface/sentence-transformers/issues/4090), [FlagEmbedding#148](https://github.com/FlagOpen/FlagEmbedding/issues/148) |
| I35 | embedding (numerics) | encodings differ with batch size | user repro | [sentence-transformers#3197](https://github.com/huggingface/sentence-transformers/issues/3197) |
| I36 | serving (determinism) | same query, same index, different results (filters / reloads / no writes) | user repro | [qdrant#2374](https://github.com/qdrant/qdrant/issues/2374), [chroma#2675](https://github.com/chroma-core/chroma/issues/2675), [elasticsearch#119180](https://github.com/elastic/elasticsearch/issues/119180) |
| I37 | scoring (thresholds) | similarity_score_threshold behaves unexpectedly; scores not proportional to similarity across stores | user | [langchain#12707](https://github.com/langchain-ai/langchain/issues/12707), [#11386](https://github.com/langchain-ai/langchain/issues/11386), [#13437](https://github.com/langchain-ai/langchain/issues/13437) |
| I38 | corpus (chunking) | answer split across chunk boundary; chunks lose context needed to be findable | experience report / practitioner | [Barnett et al. 2024](https://arxiv.org/abs/2401.05856) (§6.1), [TDS](https://towardsdatascience.com/your-chunks-failed-your-rag-in-production/) |
| I39 | query (misspelling) | misspellings cause the largest robustness drop among syntax-preserving variations; misspellings are a significant share of commercial traffic | papers | [Penha et al. ECIR 2022](https://arxiv.org/abs/2111.13057), [ToRoDer](https://arxiv.org/abs/2304.08138), [Zhuang & Zuccon 2021](https://arxiv.org/abs/2108.12139) |
| I40 | query (variation types) | data-driven taxonomy from UQV100: gen./specialisation, aspect change, misspelling, naturality, ordering, paraphrasing; WordNet synonym swaps valid in under 38% of cases | paper (manual annotation) | [Penha et al. ECIR 2022](https://arxiv.org/abs/2111.13057) |
| I41 | system (taxonomy) | Seven failure points from 3 case studies; FP2 "missed the top ranked documents" is the retrieval-stage one; validation only feasible during operation | experience report | [Barnett et al. 2024](https://arxiv.org/abs/2401.05856) |
| I42 | VDBMS (taxonomy) | 1,671 bug-fix PRs from 15 VDBMSs; 5 symptom categories; 31 recurring fault patterns; 12 fix strategies | empirical study | [Xie et al. 2025, arXiv 2506.02617](https://arxiv.org/abs/2506.02617) |

Evidence quality notes:
- **Practitioner write-ups:** I31 and I26–I27 are practitioner blogs, not incident postmortems with metrics.
- **No public postmortems found:** I found no public postmortem that measures retrieval-quality loss in a named production
  incident. "No evidence found" for quantified incident impact.
- **No prevalence data:** none of the sources gives how often these failures happen in production.
  Prevalence: no evidence found.

## 2. Fault-by-fault verdict table

### Our own data: what occurs naturally

[OBS-DATA] File: `docs/evidence/explore_train_seed43.json`. The census covers the clean runs of the 1,528 ESCI base queries
in the seed-43 TRAIN split, read from the checkpoint. The held-out split was not read.
- 761/1,528 clean queries already fail Hit@5 (fail rate 0.498).
- "Fail rate given X" means the clean fail rate among queries that have property X.

| Natural property in clean TRAIN runs | Queries with it | Of which fail | Fail rate given it |
|---|---|---|---|
| query token with df < 3 and a corpus spelling correction | 145 | 86 | 0.593 |
| query token absent from the corpus vocabulary | 136 | 99 | 0.728 |
| out-of-vocabulary token segmentable into corpus words | 50 | 40 | 0.800 |
| alphanumeric code token | 61 | 17 | 0.279 |
| "and" / "," / "&" in query | 45 | 17 | 0.378 |
| exact-duplicate pair in top-5 | 30 | 18 | 0.600 |
| ≥ 2 chunks of one parent document in top-5 | 625 | 290 | 0.464 |
| "nan" placeholder doc in top-5 | 660 | 236 | 0.358 |
| "nan" placeholder ranked above the gold | 253 | 166 | 0.656 |
| gold itself is a "nan" placeholder doc | 984 | 552 | 0.561 |

### Verdicts

Evidence strength scale:
- **S**: multiple independent reports.
- **M**: single report, or practitioner-only.
- **P**: plausible but unobserved.
- **N**: no evidence found.

| Fault (as built) | Industry evidence (§1) | Our data | Strength | Verdict |
|---|---|---|---|---|
| Q01 unfinished last word | none found | not measured | N | **needs natural validation**. Merge into lexical family QLEX: on telemetry its signature (a low-df token near frequent words) is the same as Q04's |
| Q02 chatty / verbose query | I40 (naturality category, observed in UQV100) | ESCI queries are keyword-style | M | keep. Natural arm not possible on ESCI |
| Q03 rare-synonym swap (WordNet) | I40 says WordNet swaps are valid in < 38% of generated cases | — | M for the category, but the **injection is invalid in most cases** | **needs natural validation; injected results not reportable as is**. Merge into QLEX |
| Q04 misspelling | I39, I40 | 145/1,528 queries, fail 0.593 | S | keep. Natural arm |
| Q05 missing space | none found in retrieval reports | 50/1,528, fail 0.800 | M (data) | keep. Natural arm. Merge into QLEX |
| Q07 identifier corruption | brand/name spelling issue in e-commerce ([arXiv 2410.11655](https://arxiv.org/abs/2410.11655)) | 61 queries, fail 0.279 (below average) | M | keep. Natural evidence weak |
| Q09 multi-intent | I41 FP7 is generation-side; I40 "aspect change" | 45 queries, fail 0.378 (below average) | P | candidate **cut**. Natural data does not show this as a failure driver |
| K03 sibling identity | none found | — | N | keep only as domain-specific hypothesis. Flag "no evidence found" |
| K04 stale vector for a doc | I26, I27, I31 | — | M | **merge with R07** (family STALE): same probe signature, same repair |
| K05 duplicate flood | I23, I24 | 2,558 duplicate rows; 30 queries with a duplicate pair in top-5 | S | keep. **Re-ground**: exact re-ingested duplicates, not keyword-stuffed near-copies. Natural arm |
| K06 conflicting third-party copies | none found at retrieval layer (I41 FP4 is generation-side) | — | N | candidate **cut** |
| K07 tenant filter dropped | I29, I30 (filters silently ignored) | — | S | keep. Re-ground as "metadata filter silently ignored" |
| K08 placeholder docs outrank | weak (practitioner remarks only) | 3,993 nan docs; nan in top-5 for 660/1,528; **gold is nan for 984/1,528** | M (data) | keep. **Natural arm decides**, because the real placeholders are often the gold |
| K09 superseded version served | I25, I26 | 3/36 natural pairs fail (seed-43 run, `kaggle/judged_cpu_run_seed43/natural_faults.csv`) | M | keep. Add K11 (deleted docs served) |
| R01 index coverage loss | I7, I8, I9 | — | S | keep |
| R03 query encoder misconfig (max_seq_length 12) | I34 (missing prompt), I33 (truncation, doc side) | — | M for the category; **N for the specific knob** | re-ground as "query instruction/prompt missing". Merge into family ENC |
| R05 reranker returns garbage | none found | — | N | keep as hypothesis |
| R06 wrong collection served | I9, I29 (adjacent) | — | P | keep as hypothesis |
| R07 embedding rows misaligned | I28 (index desync, adjacent) | — | P/M | merge into STALE |
| R10 Gaussian noise on query vector | none for Gaussian noise. The evidenced numeric faults are non-finite values (I11–I14) and batch-dependent encodings (I35) | — | N | keep in ENC as hypothesis. **Add R25 non-finite vectors** (evidenced) |
| R11 embedding model drift | I31, I32 | real model pair used (bge v1/v1.5) | S | keep |
| R13 BM25 dictionary/analyzer desync | I20, I21, I22 | — | M | keep |
| R15 ANN recall collapse | I4, I5, I6 | — | S | keep |
| R19 rerank depth too small | I18, I19 | — | S | keep |
| R22 fusion normalisation bug | I15–I18 | — | S | keep |
| R23 partial results | I10, I12 | — | S | keep |
| R24 reranker input truncation | I33 (embedder, by analogy) | — | M | keep |
| C2 two faults at once | none found on co-occurrence | — | N | keep as hypothesis |

Summary:
- **Strong (S):** 10 faults — Q04, K05, K07, R01, R11, R15, R19, R22, R23 and the pair R03/R11 via I31–I34.
- **Medium (M):** 9.
- **No evidence found (N):** 7 — Q01, K03, K06, R05, R10, C2, and R03 as built.
- **Merges, by telemetry and repair identity:** QLEX = {Q01, Q03, Q04, Q05}, STALE = {K04, R07}, ENC = {R03, R10, R11}.
- **Cut candidates:** K06, Q09.

These cuts are [REC] for the paper's fault set. The judged 28-fault runs are kept unchanged (see §8).

## 3. Missing faults

The evidence shows these failures, and none of our 28 covers them:

| ID | Candidate fault | Evidence | Built in §8? |
|---|---|---|---|
| R26 | filtered ANN: filter applied after the ANN candidate list, so too few or wrong results | I1, I2, I3 | **yes** |
| R25 | non-finite vectors (NaN/Inf) in the index: rows silently dropped, or NaN ranked first | I11, I12, I13, I14 | **yes** |
| K11 | deleted documents still served (tombstones not applied) | I25, I26 | **yes** |
| K12 | chunk crowding: several chunks of one parent occupy top-k ("same document returned more than once") | I24, I38; [OBS-DATA] 625/1,528 queries | **yes, natural arm + repair** |
| M5 | document text silently truncated at embedding time | I33 | no (candidate) |
| M6 | non-deterministic / replica-inconsistent results | I36, I9 | no (needs replicas) |
| M7 | similarity-score threshold mis-scaled for the store's metric | I37 | no (candidate) |
| M8 | IVF centroids stale after inserts | I5 | no (variant of R15) |
| M9 | metadata index desynchronised from stored payloads | I28 | no (candidate) |

## 4. Natural-validation plan

None of these arms uses injection. Each is selected by our own deployed detector rule, never by gold. Each is measured on ESCI
queries that no earlier run looked at: `kaggle/natural_exclusions_seed43.json` lists the 3,310 query strings already
examined, and they are excluded.
- **Metric:** paired change in Hit@5 (repair minus no repair), with a 95% bootstrap confidence interval.
- **Verdicts:** PASS if the interval lies above 0. HARM if it lies below 0. INCONCLUSIVE otherwise.

| Arm | Fault | Selection (our rule) | Repair | What it measures |
|---|---|---|---|---|
| NA1 | Q04 natural misspelling | `q_correctable ≥ 1` | QLEX family repair | real typo recovery |
| NA2 | Q05 natural missing space | `q_segmentable ≥ 1` | QLEX family repair | real segmentation recovery |
| NA3 | K08 natural placeholders | `thin5 ≥ 1` | K08 repair | whether demoting real placeholders helps or hurts |
| NA4 | K05 natural duplicates | `dup5 ≥ 1` | K05 repair | real duplicate collapse |
| NA5 | K12 natural chunk crowding | ≥ 2 chunks of one parent in top-5 | parent collapse (new) | a natural fault found in our data |
| NA6 | the whole loop | all unseen queries | v2 closed loop | the product claim on natural traffic |

## 5. Portability findings

- **Second domain:** BEIR SciFact (scientific claim retrieval). 5,183 abstracts; 1,109 queries with train and test qrels.
  Downloaded and hashed: `scifact.zip` SHA-256 `536e1444…0165`, 2,816,079 bytes.
- **Second stack:**
  - encoder: intfloat/e5-small-v2, with the mandatory `query:`/`passage:` prefixes
  - index: FAISS HNSW (M=32), real `efSearch` knob
  - fusion: min-max normalised convex combination instead of RRF
  - reranker: ms-marco-MiniLM-L-6-v2
  - real model-version pair for drift: e5-small → e5-small-v2

Translation of the faults:

| Survives translation (stack- and domain-independent) | Re-expressed on stack 2 | Does not translate |
|---|---|---|
| Q01, Q03, Q04, Q05, K04, K05, K08, R01, R05, R07, R10, R13, R19, R23, R24, R25 | R03 → missing e5 `query:` prefix (I34). R11 → e5-small vs e5-small-v2. R15 → HNSW efSearch < k (I4). R22 → un-normalised convex fusion (I15–I18) | Q02 and Q07 (shopping query style). K03, K06, K07, K09, K11 (need product attributes, sources, tenants, validity or tombstones). R06 (one collection). R26 (no metadata to filter). C2 (out of scope) |

So 20 faults are ported. Each is judged on stack 2 with the same gates as core-28.

## 6. Loop diagnosis

From evidence and first principles. Inputs, train split only: out-of-fold confusions in `docs/evidence/explore_train_seed43.json`.

1. **Rule-versus-classifier precedence caused the Q01 collapse.**
   - [OBS-DATA] On train, Q01's out-of-fold top-1 accuracy is 1.00. The classifier separates Q01 well.
   - [MEAS] In seed 42, a hand rule (Q04: "a token has a spelling correction") was given precedence over the classifier.
     Q01's attribution was then 0.04 (`judged_cpu_run_seed42/closed_loop.csv`).
   - In seed 43 the rule no longer overrode the classifier. Q01's held-out attribution was 0.96 and closure 0.84
     (`judged_cpu_run_seed43/closed_loop.csv`).
   - The brief's GPU figure (attribution 0.025) has the seed-42 signature. That is consistent with a pre-fix notebook,
     but unverified.
   - Mechanism: a truncated last word is a low-df token within edit distance 1–2 of a frequent word, which is exactly what a
     spelling rule fires on. A rule that fires on a superset of another fault's signature must not take precedence.
2. **Q03 is hard in principle, and its injection is partly invalid.**
   - Its OOF accuracy is 0.44. Confusions: NONE in 10/25 cases, Q04 in 3/25.
   - The telemetry sees a valid but rare word. Natural clean queries contain rare words all the time, so the fault looks
     like the natural failure base rate. 49.8% of clean ESCI train queries already fail.
   - Penha et al. (I40) found WordNet swaps valid in under 38% of cases, so many Q03 episodes are semantically broken
     queries, not paraphrases.
   - Distinguishing "rare synonym" from "rare but correct word" needs knowledge outside retrieval telemetry, such as a query
     log or a paraphrase model.
3. **K04/R07 and R03/R10/R11 are not separable, and don't need to be.**
   - K04 and R07 confuse with each other (R07 → K04 in 5/25). Both produce "served vector ≠ fresh embedding". They differ
     only in scope, one document versus a block, and a top-k probe cannot see scope. They share the refresh/realign repair.
   - R11 confuses with R03 and R10 (4 and 2 of 25). All three bend the query vector, and they share the encoder reset.
   - Attribution should be scored at the level that determines the repair. These are families, not faults.
4. **Faults with weak signatures are absorbed into NONE.**
   - R24 (9/25 → NONE), Q05 (11/25), K04 (10/25) and R05 (7/25).
   - With a natural base failure rate near 50%, "a failure with no unusual telemetry" is the most common thing the
     classifier sees. Calibrated abstention is the honest response, rather than forcing an attribution.
5. **The calibration flaw in seed 43.** Conformal risk control assumes calibration and test scores are exchangeable. Seed 43
   calibrated on out-of-fold scores and tested on full-model scores. That broke exchangeability, and the guarantee failed
   (`judged_cpu_run_seed43/VERDICT.json`).

[REC] Loop v2:
- precise rules only;
- family-level attribution (QLEX, STALE, ENC; others singletons);
- one family repair per family. QLEX resolves the ambiguous token by query-log likelihood, which is evidence the telemetry lacks;
- abstention threshold from conformal risk control on a separate calibration split scored by the same model.

## 7. Novelty plan

Each move gives (a) what it is, (b) the cap it attacks, (c) the supporting evidence, (d) effort, and (e) what it would let
the paper claim that it cannot claim now.

1. **Evidence-grounded fault map.**
   - (a) Map every fault to field evidence; merge, cut, and add from evidence.
   - (b) Grounding.
   - (c) §1–§3.
   - (d) Done (this report).
   - (e) "Our fault set is derived from 42 cited field reports and a natural census of our data, with strength labels."
     It cannot be claimed as discovered from a mined corpus of incidents.
2. **Natural-validation arms.**
   - (a) NA1–NA6.
   - (b) Natural validity.
   - (c) §2 census: natural occurrences exist at measurable rates.
   - (d) 1 run.
   - (e) Per-fault effect of the repairs on naturally occurring failures, including harm.
3. **Portability run.**
   - (a) 20 faults on SciFact plus stack 2.
   - (b) Generality.
   - (c) §5.
   - (d) New notebook plus 1 run.
   - (e) "N of 20 faults are solved on a second domain and stack under the same frozen gates."
4. **Loop v2 with families and a valid guarantee.**
   - (a) As in §6.
   - (b) Loop.
   - (c) §6.
   - (d) Code change plus 1 new-seed judged run.
   - (e) End-to-end closure and a clean-traffic loss bound that holds on held-out data.
5. **Three evidence-grounded new faults (R25, R26, K11) and one natural fault (K12).**
   - (b) Grounding.
   - (c) §3.
   - (d) Code.
   - (e) Coverage of field-reported failures absent from all prior RAG fault benchmarks I found.

**Prior art that bounds us:**
- RAGLog ([2611.03725](https://arxiv.org/abs/2611.03725)) localises the faulty stage from logs with LLM checks, and has natural-fault runs.
- D2R-RAG ([2606.29377](https://arxiv.org/abs/2606.29377)) does diagnose-then-repair, but needs the generated answer.
- AgenticRAG-FP ([2608.20627](https://arxiv.org/abs/2608.20627)) injects certified faults for causal attribution.
- Barnett et al. (I41) give failure points from case studies.
- Xie et al. (I42) mined a VDBMS bug taxonomy from 1,671 PRs. It covers software defects, not retrieval-quality repair.
- Penha et al. (I40) mined query-variation categories from UQV100.
- DeepCrime ([Humbatova et al. 2021](https://zenodo.org/records/5082873)) and [Humbatova et al. ICSE 2020](https://arxiv.org/abs/1910.11015)
  derive mutation operators from real DL faults.
- [Just et al. FSE 2014](https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf) validated mutants against real faults.

**What would remain original, if the runs hold:** a retrieval-stage, LLM-free diagnose-and-repair loop whose fault operators
are tied to field reports with strength labels. It would be validated on natural failures, on a second stack and domain, and
with a held-out clean-traffic loss bound. No single prior work above combines those.

**Honest ceiling of this plan:** about 7/10 [HYP], and only if the natural arms and the portability run come out positive.
Still missing above it:
- a mined, quantified incident corpus;
- a natural-failure benchmark at scale with independent labels;
- a head-to-head with RAGLog/D2R-RAG on the same natural failures;
- a GPU-stack judged run of everything.

## 8. Execution record

Everything here is [MEAS]. Each result comes from a run whose gates and code SHA-256 were written to a protocol file before
any result existed.

### 8.1 What was built

| Artefact | Content |
|---|---|
| `kaggle/diagrag_v2.py` / `.ipynb` (code SHA-256 `8e329cd2…be854`) | v1 core-28 unchanged in definition, plus R25/R26/K11 (§3); K12 natural repair; family-level loop (§6); a separate calibration split for conformal risk control; natural arms NA1–NA6 (§4) |
| `kaggle/diagrag_port.py` / `.ipynb` (code SHA-256 `59160c29…462e`) | second stack + second domain, 20 faults (§5), the same gates |
| `kaggle/natural_exclusions_v1.json` (SHA-256 `b249216f…ce42`) | the 4,891 query strings any v1 run examined. v2 draws injected-episode bases only from this set, and natural arms only from outside it |
| `docs/evidence/` | raw GitHub search hits and queries, issue bodies, the train-only exploration script and its output |

The v1 notebook `kaggle/diagrag_core28.py` and its judged runs (seeds 42 and 43) are **unchanged**. Nothing judged was discarded.

### 8.2 Runs

All runs were on CPU with the MiniLM-L6 reranker.
- **v2:** seed 44, 2,400 ESCI + 885 ShopNova bases, 50 hard episodes per fault (25 held out), 1,500 never-examined natural
  queries. Outputs: `kaggle/judged_cpu_run_v2_seed44/`.
- **Portability:** SciFact, seed 7, 50 hard episodes per fault. Outputs: `kaggle/judged_port_scifact/`.

Infrastructure incidents (neither changed code, gates or data):
- The sandbox reverted the v2 checkpoint between three consecutive chunks, so those chunks were recomputed.
- One chunk crashed on a vanished `.tmp` file and was re-run.
- The resume is deterministic: random-generator state is checkpointed, and both protocol hashes still match the shipped files.

### 8.3 Results: v2 (`judged_cpu_run_v2_seed44/VERDICT.json`)

| Gate | Result |
|---|---|
| 28 v1 faults: detectors | **28/28 PASS** (lowest AUROC: C2 0.825, K04 0.876, Q03 0.877) |
| 28 v1 faults: repairs | **27/28 PASS**. Q03 FAIL: 32/50 rescued (Wilson lower bound 0.501), but 3/20 clean successes lost (> 10% harm bar) |
| Verdict on the 28 | ADOPTED (third consecutive seed: 42 → 28/27, 43 → 28/28, 44 → 28/27) |
| R25 non-finite vectors (new, evidenced) | detector PASS (rule, AUROC 1.0), repair PASS (50/50) |
| K11 deleted docs served (new, evidenced) | detector PASS (source-of-truth registry rule: trivially separable by construction), repair PASS (50/50) |
| R26 post-filtered ANN (new, evidenced) | **THIN**: 3 hard episodes in 2,500 attempts (yield 0.002) |
| Loop L2: mean closure ≥ 0.70 under the CRC threshold | **PASS** (0.871) |
| Loop L1: held-out clean Hit@5 loss ≤ 0.005 under the CRC threshold | **FAIL** (0.0128) |

**What R26 shows.** The same keyword side, correctly pre-filtered, recovers almost every dense miss caused by post-filtering.
The field-reported failure (pgvector, Milvus, Weaviate) is therefore masked in a hybrid stack. [HYP] It would bite a
dense-only stack.

**Why L1 failed.**
- The calibration split saw 3 losses in 811 queries, so conformal risk control allowed dispatching 99.5% of clean queries
  (λ = 0.0004).
- On the held-out split the loss was 17 of 1,330 queries, all ESCI.
  - 14 of the 17 came from QLEX-family repairs (Q03: 7, Q01: 4, Q05: 2, Q04: 1).
  - The other 3: one composite R22 + Q05 dispatch, one Q09 and one Q07. So 15 of the 17 losses involve a QLEX member.
- Across 200 calibration re-splits the mean loss was 0.0030 and the 95th percentile 0.0073.
  The held-out value lies above that 95th percentile.
- [OBS-DATA] Held-out ESCI clean queries carry a low-df token more often than calibration ones: 17.7% vs 13.3%
  (12.1% vs 9.4% with a correctable token). That is exactly what QLEX acts on.
- [HYP] The hash-based component split is not exchangeable enough on this property. Conformal risk control gave no
  held-out guarantee here.

**Loop results (`policies.csv`, `closed_loop.csv`), held-out:**

| Policy | Mean closure (31 + C2) | Family attribution | Clean queries repaired | Clean Hit@5 loss | Net clean Hit@5 | Q01 closure (attribution) | Q03 closure (attribution) |
|---|---|---|---|---|---|---|---|
| τ at 5% FPR, out of fold | 0.828 | 0.801 | 4.5% | 0.60% | −0.37 points | 0.68 (0.96) | 0.36 (0.52) |
| CRC α = 0.005 | 0.871 | 0.835 | 99.5% | 1.28% | −0.90 points | 0.68 (1.00) | 0.40 (0.72) |

Comparison with earlier runs:
- **Brief's GPU figures (unverified):** Q01 0.10 (attribution 0.025), Q03 0.225, clean −0.78%.
- **Seed-43 CPU, same τ policy:** mean closure 0.82, Q01 0.84, Q03 0.12, clean loss 0.22%.
- **Effect of family attribution:**
  - Q01's attribution collapse stays fixed.
  - Q03 closure improves (0.12 → 0.36).
  - Q01 closure drops (0.84 → 0.68). The shared QLEX family repair is weaker per member than the dedicated repairs.
    `family_repairs.csv`: Q01 34/50 vs dedicated 39/50; Q03 26/50 vs 32/50; Q04 35/50 vs 39/50.
  - Clean-traffic loss went up, not down: 0.22% → 0.60% at τ.

**Natural arms** (`natural_arms.csv`): 1,500 ESCI queries that no earlier run examined, no injection, selection by
deployed rule only. Δ is the paired Hit@5 change with a 2,000-resample bootstrap 95% CI.

| Arm | n | Hit@5 before → after | Δ [95% CI] | Fixed / broken | Verdict |
|---|---|---|---|---|---|
| NA1 natural misspelling (QLEX repair) | 155 | 0.561 → 0.490 | −0.071 [−0.142, 0.000] | 11 / 22 | INCONCLUSIVE (leans harmful) |
| NA1b, the corrected form was typed by another user | 6 | 0.333 → 0.333 | 0.000 [−0.667, 0.667] | 2 / 2 | INCONCLUSIVE |
| NA2 natural missing space | 53 | 0.509 → 0.528 | +0.019 [−0.057, 0.094] | 3 / 2 | INCONCLUSIVE |
| NA3 natural "nan" placeholder demoted | 8 | 1.000 → 0.500 | −0.500 [−0.875, −0.125] | 0 / 4 | **HARM** |
| NA4 natural exact duplicate collapsed (K05 repair) | 125 | 0.384 → 0.440 | **+0.056 [+0.016, +0.104]** | 8 / 1 | **PASS** |
| NA5 natural chunk crowding (K12 parent collapse, new) | 621 | 0.552 → 0.597 | **+0.045 [+0.027, +0.063]** | 32 / 4 | **PASS** |
| NA6 loop v2 on all natural traffic, τ policy | 1,500 | 0.5173 → 0.5180 | +0.0007 [−0.0033, +0.0047] | 5 / 4 | INCONCLUSIVE (6% dispatched) |
| NA6 loop v2, CRC α = 0.005 policy | 1,500 | 0.5173 → 0.5080 | −0.0093 [−0.0173, −0.0007] | 13 / 27 | **HARM** |

**Unseen faults** (`unseen_faults.csv`), leave-one-fault-out: mean closure 0.253 over 24 faults (seed 43: 0.21).
- High where a family shares the repair: R07 0.96, R10 0.96, R03 0.92, R11 0.92, K04 0.80.
- QLEX members: 0.28–0.40.
- Most singletons: ≈ 0.

### 8.4 Results: portability (`judged_port_scifact/PORT_VERDICT.json`)

- **Stack and domain:** SciFact on e5-small-v2 + FAISS HNSW + min-max fusion.
- **Clean Hit@5:** 0.805 train / 0.780 test.
- **HNSW check:** at ef_search = 128, recall@10 against exact search is 0.9995.

| Gate | Result |
|---|---|
| Repairs | **18/20 PASS**. Q01 not testable (0 of 2,500 injections applicable in SciFact's vocabulary); R03 THIN (2 hard: e5 without its `query:` prefix barely degrades on SciFact) |
| Detectors | **11/20 PASS**. Every fault with ≥ 20 held-out positives passed (Q04, K05, K08, R01, R05, R07, R10, R11, R23, R24, R25). Q03, Q05, K04, R13, R15, R19 and R22 were THIN (6–19 positives); K04's AUROC was 0.567 on 17. Q01 and R03 could not be trained |
| Solved (both) | **11/20**. The pre-registered "the suite ports" claim needed ≥ 15, so it is **not made** |

Most detector THINs come from low hard-episode yield on stack 2: R15 0.018, R22 0.034, R13 0.032 (`port_episodes_summary.csv`).
The min-max hybrid on a small, clean corpus absorbs most single-component faults.

### 8.5 Before / after: what the paper can claim

| Topic | Could claim before this task | Can claim now (file) | Still cannot claim |
|---|---|---|---|
| Grounding | nothing. The 28 faults were asserted | each fault mapped to 42 cited field reports with a strength label; 10 strong, 9 medium, 7 with no evidence (§1–§2) | that the fault set was mined from a quantified incident corpus |
| New faults | — | R25 and K11 from field evidence, solved on the main stack; R25 also solved on stack 2 (`VERDICT.json`, `PORT_VERDICT.json`) | that R26 matters for hybrid stacks: it is measured as nearly harmless here |
| Natural validity | 46 natural typos, weak | two repairs **improve naturally occurring failures** on never-examined queries: duplicate collapse +5.6 points; chunk-crowding parent collapse +4.5 points (n = 621). Two repairs **harm** natural traffic: placeholder demotion and, leaning, QLEX on natural typos (`natural_arms.csv`) | that the full loop improves natural traffic. At the τ policy the effect is +0.07 points with a CI spanning 0 |
| Generality | one stack, one domain | 18/20 repairs and every adequately sampled detector (11/11) pass on a second stack and domain (`port_*`) | "the suite ports": 11/20 solved < the frozen 15 |
| Loop | Q01 collapsed (seed 42; GPU brief, unverified) | family attribution keeps Q01 attributed (0.96) and raises Q03 closure (0.12 → 0.36); mean closure 0.83 at 4.5% clean dispatch | a held-out do-no-harm guarantee: L1 failed (0.0128 > 0.005) |
| Stability | two seeds | three seeds at 28/28 detectors and ≥ 27/28 repairs | — |

### 8.6 Revised novelty estimate

About 6.5 [HYP]. The move from about 5.5 is earned by three things:
- the evidence map;
- two natural-failure repairs that pass on never-examined traffic, one of them for a fault found in our own data;
- a second stack and domain with measured portability.

It is capped by three failures, reported as measured:
- the held-out guarantee failed;
- the loop gives no measurable net benefit on natural traffic;
- portability fell short of its pre-registered bar.

To go higher:
1. A calibration scheme that survives split shift. For example, stratify calibration by query-lexicon features, or calibrate
   on natural traffic.
2. Restrict QLEX to dispatch only with query-log support, because NA1 shows it breaks twice as many natural typo queries as
   it fixes.
3. The GPU-stack run of both notebooks.
4. A head-to-head with RAGLog on the NA arms.
