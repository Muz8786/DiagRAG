# Roadmap execution record — Phases A–E (v3)

Date: 15 Nov 2026. Every number below is [MEAS] from a judged run whose gates and code SHA-256 were written before its
results, unless it is marked [EXPLORATORY] (computed afterwards, not pre-registered) or [HYP]. All runs used CPU and
the MiniLM-L6 reranker. **The bge-reranker-large GPU flagship was not run**, because no GPU is available here.

| Run | Code SHA-256 | Folder |
|---|---|---|
| v3 main, seed 45 | `a59311c6…515c` | `kaggle/judged_cpu_run_v3_seed45/` |
| port2 SciFact, seed 8 | `ec113b04…34e0` | `kaggle/judged_port2_scifact/` |
| port2 FiQA, seed 9 | `ec113b04…34e0` | `kaggle/judged_port2_fiqa/` |
| LangChain stack, seed 10 | `87284fe4…115e` | `kaggle/judged_langchain_scifact/` (§3) |

Nothing judged earlier was changed or discarded: v1 seeds 42/43, v2 seed 44 and port v1 are all unchanged. Each fix
listed below was designed after seeing an earlier run's results, so it was judged on a **new seed** and, for natural
traffic, on **never-examined queries**.

## 1. Phase A — make the loop trustworthy

| Gate (pre-registered) | Result |
|---|---|
| **L1 do-no-harm**: held-out clean Hit@5 loss ≤ 0.5% under Mondrian (rarity × source) conformal risk control | **PASS**: 0.149% (2 losses / 1,345). By stratum: common 0.14%, rare 0.64%, shop 0% |
| **L2**: mean held-out closure ≥ 0.70 under the L1 thresholds | **PASS**: 0.865 (grounded faults: 0.867) |
| **U1**: unseen-fault (leave-one-out) mean closure ≥ 0.50 | **FAIL**: 0.365 (0.242 without group fallback; v2: 0.253) |
| **N1**: deployed loop on never-examined natural traffic, 95% CI lower bound of ΔHit@5 > 0 | **PASS**: +2.25 points [+1.40, +3.09], n = 1,648, 45 fixed / 8 broken |

What changed:
- Calibration is per stratum, on 2,946 clean train queries that were never used to fit the attributor.
- Attribution is family-first: group → family, with a group fallback repair (Q: log-gated QLEX; K: corpus hygiene;
  R: config-manifest rollback + verified rebuild).
- QLEX now rewrites only words that real users essentially never type.
- The natural repairs K05 and K12 run as precise rules.

What the numbers mean (`policies.csv`, `natural_traffic.csv`, `docs/evidence/analysis_v3_seed45.json`):
- **The guarantee holds, at a price.** On the common stratum conformal risk control picked λ ≈ 0.0004, so 90% of clean
  queries get a repair, at a mean cost of 4.2 per clean query (illustrative cost vector 1/3/8).
  - The simple τ policy (5% false alarm, out of fold) reaches the same held-out clean loss (0.14%) with 3.9% clean
    dispatch and a cost of 0.14 per query. Its mean closure is 0.845 against 0.865.
  - Only the conformal policy carries a guarantee. τ happened to meet the bound in this run.
- **The natural-traffic gain comes from the two detection-gated natural repairs.**

  | Policy on natural traffic | ΔHit@5 [95% CI] |
  |---|---|
  | Rules only | +2.43 [+1.70, +3.22] |
  | Classifier dispatch only | −0.06 [−0.49, +0.36] |
  | Deployed loop vs rules only [EXPLORATORY] | −0.18 [−0.55, +0.18] |
  | Rules gated vs K12 always on [EXPLORATORY] | **+0.61 [+0.06, +1.15]**, so gating matters |
  | Deployed loop vs diagnosis-free universal repair [EXPLORATORY] | +0.06 [−0.79, +0.85] |

  - The universal repair applies everything to every query, at cost 12. The loop matches it at half the cost
    (6.1). Rules only match it at cost 1.4.
- **The natural repairs replicated** on queries not used in v2:
  - K05 duplicate collapse: +5.0 points [+0.7, +9.3], n = 140 (v2: +5.6).
  - K12 parent collapse: +4.9 points [+3.1, +6.6], n = 637 (v2: +4.5).
- **Natural misspellings remain unsolved.** On 185 queries, QLEX: −4.9 [−10.3, +0.5] (9 fixed / 18 broken).
  - The standard external tool is worse: SymSpell `lookup_compound` scores −11.4 [−17.8, −5.4] (8 / 29), a
    measured HARM.
  - On injected typos the ranking reverses: SymSpell rescues 25/50, ours 41/50.

## 2. Phase B — finish grounding the fault set

- **Licence-clean corpus.** The 84,993 ABO rows with conflicting licence status are removed; 101,297 docs remain. All
  v3 results use this corpus.
- **Evidence tiers in code.** `TIER` in `diagrag_v3.py`.
  - The 22 grounded faults (S/M) are the headline: **20 of 22 solved**. The two not solved are Q03 and R26.
  - The 10 quarantined faults (N/P: Q01, Q09, K03, K06, R03, R05, R06, R07, R10, C2) are run and reported, but no
    headline claim rests on them.
- **Q03 rebuilt from real data.** Episodes now pair two real ESCI queries for the same Exact product.
  - The detector **fails** (AUROC 0.56) and the repair **fails** (query-log neighbour rewrite, 1/50).
  - So natural vocabulary variation is not detectable from retrieval telemetry, and the earlier injected-synonym Q03
    results (v1/v2) were an artefact of the injection.
  - Q03 also sits in 3 of the 5 least-separable fault pairs (`docs/IDENTIFIABILITY.md` §4).
- **K12 graduated.** Detector PASS, repair PASS (46/50), natural arm replicated.
- **R25 and K11 solved again** (50/50 each).
- **R26** was run on a dense-only testbed and is still **THIN**: 8 hard episodes in 2,500 attempts (3 train, 5 held
  out). All 5 held-out episodes are repaired by the loop. The filter used (the ESCI partition, about 13% of the corpus) is not selective
  enough to trigger the field-reported failure. [HYP] A tenant-sized filter (about 1%) would.
- **Prevalence census** (`prevalence_census.csv`). Every ESCI query with an Exact product in the corpus, n = 7,175,
  clean pipeline, Wilson 95% CIs. This is the first natural-frequency table for these signatures that I found.

| Signature | Fault | Prevalence [95% CI] | Clean fail rate given signature | Share of all clean failures |
|---|---|---|---|---|
| misspelling token | Q04 | 10.9% [10.2, 11.7] | 48.0% | 11.6% |
| token absent from corpus vocabulary | Q04/Q05 | 10.1% [9.5, 10.9] | 58.6% | 13.1% |
| OOV token segmentable into corpus words | Q05 | 2.4% [2.1, 2.8] | 57.2% | 3.0% |
| unfinished last word | Q01 | 0.7% [0.5, 0.9] | 52.0% | 0.7% |
| identifier / code token | Q07 | 4.3% [3.9, 4.8] | 28.9% | 2.7% |
| conjunction / multi-intent marker | Q09 | 3.3% [2.9, 3.7] | 40.4% | 2.9% |
| exact duplicate pair in top-5 | K05 | 8.0% [7.4, 8.6] | 58.8% | 10.3% |
| ≥ 2 chunks of one parent in top-5 | K12 | 39.2% [38.0, 40.3] | 39.5% | 34.2% |
| "nan" placeholder in top-5 | K08 | 45.3% [44.2, 46.5] | 34.6% | 34.7% |
| "nan" placeholder ranked above the gold | K08 | 18.1% [17.2, 19.0] | 65.6% | 26.2% |
| the gold itself is a "nan" placeholder | K08 | 58.6% [57.4, 59.7] | 52.5% | 67.9% |
| all queries | — | 100% | **45.2%** | — |

- The largest natural failure driver in this corpus is a knowledge-side data-quality defect: the gold document is a
  placeholder in 58.6% of queries. No retrieval repair can fix that. It is the "absent K is unrecoverable" boundary,
  now measured.

## 3. Phase C — generality

- **Flagship GPU run: not run** (no GPU). `diagrag_v3.ipynb` defaults to bge-reranker-large on a Kaggle T4 and resumes
  from checkpoints.
- **Second stack on two domains.** Stack 2 is e5-small-v2 + FAISS HNSW + min-max fusion. The pre-registered "suite
  ports" bar is ≥ 15/20 solved.

  | Domain | Clean Hit@5 (test) | Detectors | Repairs | Solved | Not solved |
  |---|---|---|---|---|---|
  | SciFact (science) | 0.80 | 16/20 | 18/20 | **15/20 — ports** | Q01, Q03, K04, R15, R22 |
  | FiQA (finance, third domain) | 0.54 | 19/20 | 19/20 | **19/20 — ports** | K04 (detector 0.68, repair 26/50) |

  - Port v2 differs from port v1 by four fixes found in the v1 run: a query-punctuation bug in the injectors, R03
    re-expressed as truncation, probe depth 20, and a 50/50 hash split over all labelled queries.
  - Port v1 (11/20 on SciFact) is unchanged and still reported.
  - **K04 (stale vector) is the one fault that fails on both stack-2 domains.** That is the honest generality limit.
- **Framework stack (LangChain).** Real LangChain components with documented defaults, 15 faults injected through
  framework knobs, the same gates. The bar was ≥ 11/15; the result was **7/15 (FAIL)**, see §3a.
  - A first launch was aborted for performance before any gate result existed: it rebuilt an 11k-vector store on
    every attempt.
  - It was relaunched with the same seed, the same semantics, and a new protocol and hash.

### 3a. Framework stack (LangChain) — result: **7/15 solved, the framework claim is NOT made** (bar ≥ 11)

`kaggle/judged_langchain_scifact/`, langchain-core 1.8.0, langchain-community 0.4.2, faiss 1.16.0. The documents are
split into 11,169 chunks. Clean Hit@5 is 0.80 on test.

| Outcome | Faults |
|---|---|
| **Solved (7)** | Q04 (SymSpell on corpus vocabulary), Q05 (wordsegment), R01, R11, R19, R24, R25 (NaN vectors in a real FAISS index) |
| Detector FAIL, repair PASS | K04 stale vector (AUROC 0.65; fails on every non-shopping stack), R22 ensemble weights (0.69), **R23 score threshold (0.50)** |
| Repair FAIL | **K08 0/50**: implementation error. `CrossEncoderReranker` re-sorts the documents after the thin-document filter only *reordered* them; the filter has to remove them. K05 13/21: LangChain's `EmbeddingsRedundantFilter` at 0.98 does not collapse query-stuffed copies |
| THIN (low hard-episode yield) | K05, K11, R03 (bge-small barely degrades without its query instruction: 3 hard in 2,500), R13 |

What the framework stack taught, as measured:
- **R23 is a field-report pattern we reproduced.** A mis-scaled `similarity_score_threshold` silently removes the dense
  leg inside `EnsembleRetriever`, while the result count stays normal (5). Our count rule cannot see it, and the
  detector is at chance. This matches Elasticsearch #164821: "no error and the hit count looks normal".
- **Two causes are my mistakes, not findings:** the K08 repair, and R23 using a count rule instead of a dense-leg count.
- **Fixes for a re-judged run (not run here):**
  - K08 filter-then-rerank;
  - an R23 rule on the dense-leg count;
  - a K05 threshold below 0.98.
  A re-judged run needs a new seed, and only the hash of the fixed file, and its outcome is unknown.

## 4. Phase D — ship it as a benchmark

- **`bench/`:** DiagRAG-Bench v1.0.
  - Public dev episodes with labels; held-out episodes without labels.
  - Telemetry CSVs, families with evidence tiers, a manifest with SHA-256 for every file, and a commitment to the
    **private** held-out labels (`2e7cf4c0…e51f`).
  - A scorer (`score.py`), a reference baseline (`baseline_track1.py`), a datasheet, and `NOTICE.md` for licences.
- **Reference baseline on the private test split.** AUROC 0.976 [0.969, 0.982]; detection at 5% false alarm 0.917;
  family accuracy 0.863; family false alarm on clean 2.7%.
- **External reference points (not written by us).**
  - RAGLog tier-0, the authors' code at a pinned commit without LLM checks: 0.756 [0.735, 0.775] with the same
    classifier; detection 51.4% at 5% false alarm, vs ours 93.1%.
  - QPP NQC 0.583 and WIG 0.566.
  - SymSpell and wordsegment as repair baselines (§1).
  - RAGLog's full system and CRAG need LLM API keys. **Not run.**
- **The private labels are not in the repository.** They are at `/projects/sandbox/_private/diagrag_bench_v1/` in the
  build sandbox, and need a private home chosen by the owner (§6).

## 5. Phase E — not schedulable; what was done towards it

- **`docs/IDENTIFIABILITY.md`** contains:
  - Lemma 1: AUROC ≤ ½ + TV − TV²/2 for any telemetry diagnoser;
  - certified TV lower bounds for all 465 fault pairs, from train-split out-of-fold AUROC;
  - repair-equivalence and group-fallback propositions;
  - a correction: an earlier claim that our families are indistinguishable by construction is false (§4 there).
- **`docs/CROSSWALK_CATALOGUE.md`:** the two projects' fault IDs collide with different meanings. For example,
  catalogue K03 means "answer absent → abstain", while ours means "sibling identity".

## 6. Decisions only the owner can make (flagged, not executed)

1. **Merging with the 47-fault catalogue project.** This changes the project's identity, so it is flagged and not
   done. A merge would need namespaced IDs (`CROSSWALK_CATALOGUE.md`).
2. **Where to keep the private test labels.** Options: the private repo `Muz8786/diagrag-data`, or another private
   location.
3. **ShopNova's licence**, before any public data release.
4. **Running the GPU flagship** and the LLM-based baselines, which need a Kaggle GPU session and API keys.

## 7. What the paper can claim now, and the honest ceiling

New claims, each backed by a file:
- A telemetry-only loop with a held-out do-no-harm bound (L1) and 0.865 closure (L2).
- A significant gain on never-examined natural traffic (N1), with replicated natural repairs.
- A grounded fault set (22 faults with evidence tiers; 20/22 solved) plus a 7,175-query prevalence census.
- Portability on two further domains and a second stack (15/20 and 19/20). The framework stack (7/15) did **not** pass.
- An external-baseline comparison, and a benchmark with a private held-out split.

Still not claimable:
- Generalisation to unseen faults (U1 0.365 < 0.50).
- Portability to a framework stack (LangChain 7/15 < 11).
- That diagnosis beats a diagnosis-free stack on accuracy. It matches it at lower cost.
- Natural misspelling or paraphrase repair.
- Anything on the GPU stack, or against LLM-based baselines.

Estimate [HYP]: about **7/10**, up from about 6.5. Getting to 8 or above still needs the GPU flagship, one
LLM-based baseline on the natural arm, U1 ≥ 0.5, and external adoption (Phase E).
