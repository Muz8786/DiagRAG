# Crosswalk: this project's core suite vs the 47-fault DiagRAG catalogue

**Status: analysis only.** Nothing from the catalogue is used in this project's code. The decision to merge the two
projects belongs to the owner, and it is flagged in `docs/ROADMAP_V3.md` §6.

**Sources read:**
- `Muz8786/diagrag-data` → `DiagRAG_Detailed_Report_2026-11-14.md` (the catalogue project's report).
- The same repo's notebook source.

The report names only about 17 of the 47 catalogue faults explicitly. The notebook source has no machine-readable
fault table that I could extract. So this crosswalk is **partial**. A full one needs the catalogue's own fault list.

## Finding 1 — the IDs collide with different meanings

| ID | Catalogue meaning (report §2) | This project's meaning | Same fault? |
|---|---|---|---|
| Q04 | tokenisation fragmentation | real misspelling | related (both lexical); our QLEX family covers both |
| K03 | answer absent from the KB (correct behaviour = abstain) | sibling products share an identity | **no** |
| K04 | gold exists but is unreachable | stale vector for the gold | partly (stale vector is one cause of unreachable gold) |
| K05 | misinformation present | near-duplicate flood | **no** |
| R01 | deceptive grounding | index coverage loss | **no** |
| R05 | duplicate displacement | reranker returns garbage | **no**; the catalogue's R05 ≈ our K05 |
| R07 | citation fabrication (generation side) | embedding rows misaligned | **no** |
| R13 | referent shift across turns | BM25 dictionary desync | **no** |
| R19 | fixed-k truncation | rerank depth too small | **yes**, essentially |
| R22 | double-counting | raw-score fusion bug | related (both fusion) |
| R24 | position fault (decision side, also listed as C3/C4) | reranker input truncation | **no** |
| C2 | silent prompt truncation | two faults at once | **no** |
| C5 | planted instruction in a retrieved document | — (absent here) | — |

**Consequence:** a merged benchmark cannot keep both ID schemes. It needs a namespace (for example `cat:K03` vs
`core:K03`), or new IDs with a published mapping table. Otherwise published numbers become ambiguous.

## Finding 2 — what each project brings to a merged benchmark

| | Catalogue project | This project (core suite) |
|---|---|---|
| Taxonomy breadth | 47 faults incl. generation- and decision-side (C, citation, planted instruction, multi-turn) | 32 retrieval-stage faults |
| Field grounding per fault | not found in the report | evidence tier per fault from 42 field reports + a census |
| Injection machinery and hard-episode quotas | — | yes |
| Natural validation | real-typo transfer for Q (Webis), per its report | 1,648 never-examined queries, paired CIs |
| Portability | — | SciFact + FiQA on stack 2, LangChain stack 3 |
| Repair ladders with byte-identical rollback | yes, per its report | single repairs + group fallback |
| Do-no-harm | gate on baseline-correct queries | Mondrian conformal bound, held-out PASS |

## What a merge would need (not executed)

1. A canonical fault table with namespaced IDs, plus the mapping above, completed from the catalogue's source.
2. Each catalogue fault given an evidence tier with the same method (§1–§2 of the evidence report).
3. Catalogue-only faults (generation and decision side) re-hosted on a pipeline with a generator. The core suite stops
   at retrieval.
4. One frozen gate set for both. The stricter of the two gate definitions should win wherever they differ.
