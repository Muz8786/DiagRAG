# Datasheet — DiagRAG-Bench v1.0

This follows Gebru et al., "Datasheets for Datasets" (CACM 2021). Every figure here is either computed by
`make_release.py` and listed in `release_v1/MANIFEST.json`, or carried over from the judged run named in the
manifest.

## Motivation

- **Purpose:** to evaluate systems that diagnose a failure in a retrieval pipeline and repair it, using retrieval
  telemetry alone. There is no generated answer and no LLM judge.
- **Gap it fills:** existing RAG fault datasets label the failing *stage* of whole pipelines (RAGLog Faults), or
  certify injected faults for attribution (AgenticRAG-FP). None of them provides retrieval-stage episodes labelled by
  cause, with gold documents, a repair track, a published injected/natural split, and an evidence tier per fault.
- **Creator:** Muz8786 (DiagRAG). The code was written with the assistance of Kiro, an AI coding assistant using
  Anthropic's Claude model.

## Composition

- **What an instance is:** an episode — a real ESCI shopping query or a ShopNova query, plus a pipeline state that
  is either clean or carries one fault, plus the gold document ids.
- **Composition of the episodes:** clean episodes, and *hard* faulted episodes. A faulted episode is kept only if the
  clean pipeline succeeds and the faulted pipeline fails. Most faults have 50 episodes, half train (dev) and half
  held-out (test); faults with low yield can have fewer, and the episode-generation summary gives the exact counts.
- **What is synthetic:**
  - *Injected documents:* duplicates, siblings, placeholders, other-tenant copies, expired versions, deleted copies,
    and chunks. Every one is marked `synthetic: true`.
  - *Query perturbations:* typos, which come from Webis-QSpell-17 where possible, and truncation and concatenation.
  - *Pipeline-knob faults.*
  - *Q03 is not synthetic:* it pairs two **real** ESCI queries for the same Exact product.
- **Labels:** fault id, family (repair-equivalence class), group (Q/K/R), k, and gold doc ids.
- **Evidence tier:** each fault has one (S/M/P/N, in `families.json`). The headline results use only S/M faults.
- **Splits:** train and held-out are separated by gold-product component (union-find), so no gold product appears in
  both. The held-out labels are private; their SHA-256 is published in `MANIFEST.json` so they can be verified later.
- **Corpus:** this is the **licence-clean** corpus. The 84,993 ABO rows whose licence is `conflicting_unverified` are
  removed.

## Collection

- **ESCI queries and labels:** from Amazon ESCI (Apache-2.0).
- **Products:** Amazon Berkeley Objects (CC BY 4.0, verified rows only).
- **Software documentation:** Apache OFBiz (Apache-2.0).
- **ShopNova:** the project's own synthetic storefront corpus.
- **Real misspellings:** Webis-QSpell-17 (CC BY 4.0).
- No personal data is collected. ESCI queries are anonymised by their publisher.

## Preprocessing

The steps are in `diagrag_v3.py`, sections 1–2:
- deduplication-aware gold sets, which include each document's chunks, ESCI↔ABO twins and exact-content twins;
- the licence filter;
- removal of ESCI queries whose gold products would cross the train/test split.

## Uses

- **Intended:** benchmarking telemetry-only diagnosis (Track 1) and repair (Track 2) of retrieval failures.
- **Not intended:** measuring answer quality, or claiming production prevalence of a fault from its episode count.
  Episodes are selected to be hard, so they over-represent failures by design. Natural prevalence is reported
  separately in `prevalence_census.csv`.

## Distribution and licence

- **Code:** Apache-2.0 is proposed. The repository owner must confirm it.
- **Data:** derived from the sources above under their own licences.
- **ShopNova:** its licence is **unassigned and must be assigned by the owner before public release.** Until then,
  ShopNova episodes are flagged in the manifest.
- **BEIR portability datasets:** SciFact and FiQA are **not redistributed**. The notebooks download them from BEIR.

## Maintenance

- Versioned with semantic versions. Any change to episodes or the scorer bumps the version.
- Results on the private test split are verified against the committed hash.
- Issues go through the GitHub repository.
