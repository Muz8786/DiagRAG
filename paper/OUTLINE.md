# Publication paper — outline

This folder holds the paper outline and the figure captions
in `../figures/figures.md`. The canonical manuscript is
separate and must stay untouched; edits go on copies.

## Sections

1. Abstract — lead with the queue signal and the subset-valued
   claim, with the delayed-only boundary stated in the same
   paragraph. No state-of-the-art wording until Gap 1 lands.
2. Introduction — compositional attribution over Q/K/R from
   telemetry alone, cause-dispatched repairs, oracle-referenced
   recovery. Novelty is the combination only.
3. Related work — Doctor-RAG (oracle diagnosis bound, not
   recovery), D2R-RAG (bandit cost-dispatch, no compositional
   diagnosis), RAGChecker, RAGExplorer, RAG-QPP, Self-RAG,
   CRAG, Barnett Seven Failure Points, plus RECTIFY and
   Leung et al. for the late-November re-scan. Cite and
   distinguish, never compare raw numbers across tasks.
4. Method — telemetry (29 features, 31 with reranker),
   HistGB per-factor attributor, fixed-threshold and EUD
   dispatch, illustrative cost vector (1, 3, 8) stated openly.
5. Experiments — four domains, injected faults, real-typo
   transfer for Q only (Webis), natural temporal validation
   for K and real-model-shift validation for R outstanding.
6. Results — headline closures (figures 01, 02), judged
   negatives (sequential figure 07, federation, QML, probe
   calibration, fix 3, fix 6, B2 browser-reported, M1 figure 03).
7. Limitations — loop stops at retrieval (no generation),
   absent K unrecoverable, withheld combinations 10-45%,
   tuned thresholds do not transfer, latency contradiction
   unresolved, costs illustrative not measured, repo/DOI
   placeholder until Gap 8 lands.
8. Reproducibility — this repo, the replication package,
   setup.sh, download_data.py, DATA_LINKS.txt, and the
   Zenodo record once published. CPU tests exact, GPU loop
   interval check, not bit-identical across GPUs.

## Headline numbers to use, with their labels

- ESCI fixed closure 96.67% [94.62, 98.61], tuned 97.33%
  [95.33, 99.10], oracle-referenced.
- EUD eud05 qualified frontier pass, headline dispatcher
  unchanged, novelty 7.5 internal (not a paper claim to
  print as a score).
- Sequential, federation, QML, M1: judged negatives, shown,
  not hidden.
