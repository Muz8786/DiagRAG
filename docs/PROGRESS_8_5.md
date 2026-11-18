# DiagRAG 8.5 programme ledger

Updated 18 Nov 2026. Project-reported results below are baseline evidence from the current repository branch, not new judged runs in this work session.

| Workstream | Status | Current evidence / blocker | Commit |
|---|---|---|---|
| A. Multi-label composed dispatcher | **FROZEN; Kaggle run pending rotated credentials** | v7 family-level both-cause rate 40.0% [32.6, 47.9], with 0/75 same-letter pairs/triples. Official Amazon ESCI source is frozen by hash; the audited 1,648-query fault-injection pool splits into 868 historical-train-component queries and 780 held-out-component queries. This set appeared in prior natural-traffic analysis, which is disclosed. v8 runner, notebook, protocol, and synthetic preflight are frozen on the approved non-main branch; no judged v8 episode/result exists. Kaggle values pasted in chat must be rotated before remote execution. | preregistration branch |
| B. U1 selective diagnosis / probing | **OPEN** | Current v6 U1: 0.406 GPU / 0.413 CPU against 0.50. Existing route-B analysis is diagnostic; no new selective risk curve or admitted active probe result verified in this session. | baseline branch |
| C. Fault identification | **PARTIAL** | Existing post-hoc v7 analysis: 89.9% exact fault identification on held-out faulted episodes, macro-F1 0.896; Q03 never identified; weakest listed faults include R24, K04, Q04, Q05. No new change/run. | baseline branch |
| D. Multi-seed adoption | **OPEN** | Existing v6 GPU and CPU runs use one seed (50); v7 retrains descriptively from the same single-fault seed. No preregistered 3–5 seed final-configuration suite verified. | baseline branch |
| E. Second corpus | **PARTIAL** | Existing FiQA/SciFact ports are incomplete (19/20 and 15/20 in current project documentation). No full 28-fault port verified. | baseline branch |
| F. Blind faults / shadow run | **BLOCKED on external participants** | No independent blind fault author or named consenting production partner documented. | baseline branch |
| G. Fresh natural traffic | **OPEN** | Existing +2.43-point CPU gain is based on the same prior natural sample and is mostly rule-driven. No fresh natural-query sample verified. | baseline branch |
| H. LLM baseline | **PARTIAL** | Three free-tier arms are documented; the frontier-model arm remains unavailable/unrun. Provider, model, pricing, spend cap, and a secure regenerated key are still needed for that arm. | baseline branch |
| I. End-to-end answer quality | **OPEN** | No fixed generator/judge validated on 100 human-labelled answers verified. Requires owner-labelled answers if the judge is to be called validated. | baseline branch |
| J. Benchmark release / replication | **PARTIAL** | Public benchmark package is staged and verified but not released; licence/release decision and outside replication remain outstanding. | baseline branch |
| K. Quantum comparison | **PARTIAL** | Existing simulated comparison reports no quantum advantage, but the paper currently places it in the main body rather than a short appendix. No new experiment planned. | baseline branch |
| L. Paper and artefacts | **PARTIAL** | The current paper includes the v7 composed result and limitations, but needs updates only after any new judged results; no v8 numbers exist. | baseline branch |

## Work performed in this session

- Read the owner-supplied brief and the current `core28-kaggle-notebook` branch.
- Audited checked-in judged episode files for base-query overlap (5 files, 35,290 rows, 6,412 unique base IDs; 5,527 distinct ESCI episode query strings).
- Downloaded the official ESCI query file and the frozen corpus to local scratch; both match their recorded SHA-256 and byte lengths. Cross-checked the fresh-query pool: 7,175 current-corpus Exact queries, 1,648 with no prior injected episode, 868 with gold products in historical training, 780 held out from historical training products.
- Finalized the v8 multi-label preregistration. No new judged episode or result was generated, and no credentials were used.
- Built an isolated v8 CPU runner and self-contained Kaggle notebook. Runner SHA-256: `5ccb86fb4f79d3c52af4985c94afd9d2e3b9942660a4fbee9058b7b38b3a565f`; notebook SHA-256: `95e0bedfe3d8e9c943a3f0beb81bffaf955f3eb100e310de5b512331a3ba0db2`. v8 retains explicit comparisons with the v7 dispatcher and the prior single-fault-only attributor, uses a finite training-only `tau2` or disables the extra-family path if no finite value meets the bounds, checks a component-disjoint 1,000-query clean sample, and keeps its outputs/checkpoints in `diagrag_v8_out/`.
- Synthetic preflight passed for same-letter secondary dispatch, the three-label cap, and one extra family per group. The test used only a small synthetic score vector, no project data or judged result.
- `verify_v8_freeze.py` passed: notebook parses, embedded runner equals the frozen bytes, protocol hashes match, and the staged-file secret scan found no credential-shaped strings.
- Ran the staged LITE archive `verify.py`: **RESULT: ALL OK** (checksums, judged-folder code hashes, v5-v7 frozen hashes, notebook embedding integrity).
- Ran staged benchmark `verify_release.py release_v1`: **RESULT: ALL OK**. The previously run dev quickstart/scorer on 2,718 development rows reported AUROC 0.9716 [0.9647, 0.9780], family accuracy 0.8406. This is a dev cross-validation check, not a held-out result; scikit-learn warned the least-populated class had 3 examples for 5 folds.

## Inputs needed next

1. Regenerated Kaggle credentials, set through the runtime's secure environment mechanism; the credentials pasted into chat must not be used.
2. For dependent workstreams: frontier provider/model/endpoint/prices for H (spend cap waived by owner); owner-labelled judge set or permission to mark the judge unvalidated (I); licensed corpus decision (E); third party and/or consenting production partner (F); benchmark name/licence/release decision (J).
