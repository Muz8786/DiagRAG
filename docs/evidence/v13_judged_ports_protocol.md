# v13 judged port runs: NQ and FiQA (pre-registration). Written 20 Nov 2026, ~03:00 UTC, before either judged run and before any judged result.

## 1. What runs
| Run | Dataset | Seed | Code | Kaggle account | Notebook |
|---|---|---|---|---|---|
| J-NQ | BEIR NQ (2,681,468 passages) | **58** | `kaggle/diagrag_port5.py`, SHA-256 `916c3864282b1d9c168cce6943340b52d8728334c3c960d33fcb0d2d4224294f` | muzammilveil99 | `kaggle/DiagRAG_v13_judged_nq.ipynb` |
| J-FiQA | BEIR FiQA-2018 (57,638 documents) | **60** | same | sqmuzammil | `kaggle/DiagRAG_v13_judged_fiqa.ipynb` |

One run each. No rerun and no other seed without the owner's written approval as an amendment here.

## 2. Methods: the port methods, unchanged
- NQ and FiQA use the **port arm** (the method used for every non-ESCI corpus since `kaggle/judged_port2_*`), not the ESCI main pipeline (v6/v7), which needs ESCI-specific data for its 32 faults.
- `diagrag_port5.py` = the judged `diagrag_port2.py` (hash `ec113b04…34e0`) + the declared, checked edits of port3, port4 and port5: datasets added to the verified-download table, output folder names, and the execution-only embedding fix (proven to give identical output, `docs/evidence/v13_datasets.md`).
- Stack, 20 faults, injectors, repairs, attributor, statistics and **gates are port2's**: detector AUROC >= 0.70 with >= 20 held-out positives; repair Wilson lower bound >= 0.50, >= 20 hard episodes, <= 10% clean loss; THIN or untrained counts as not solved; "ports" iff >= 15 of 20 solved.
- **Settings = the judged port2 settings:** `N_QUERIES=2500, N_HARD=50, MAX_ATT=2500, N_HARM=20`; `TIME_BUDGET=36000` (execution only; the run checkpoints and resumes).
- **The clean stack is not changed.** An exploratory analysis of FiQA on its **dev** split (`docs/evidence/fiqa_analysis.py`, 500 queries) was run on 20 Nov before this protocol; it changed nothing. Those dev queries are part of the port's 50/50 hashed sample, as before.

## 3. Execution details declared in advance
- **Data:** attached as private Kaggle datasets with byte-identical zips (`v13_datasets.md`); the frozen code checks size and SHA-256 before use.
- **J-NQ reuses the corpus embeddings of the NQ trial** (`muzammilveil99/diagrag-v13-trial-nq`, seed 906). Corpus embeddings depend only on the corpus and the encoder, not on the seed. A cell outside the frozen code copies **only** `corpus_e5.npy` (after checking shape 2,681,468 x 384, float32, unit-norm rows) and asserts that no checkpoint is present, so no trial episode can enter the judged run. If the file is not found, the frozen code embeds the corpus itself.
- Trial numbers (seeds 906, 907) are not results and were not used to tune anything.

## 4. Ideas 1 and 2
They are **not** inside these runs, because their code is not built. They will be applied **afterwards** to the saved telemetry and checkpoints of J-NQ and J-FiQA as separately pre-registered, descriptive analyses. **They cannot change these verdicts.**

## 5. Predictions (judgements; they can fail)
- J-FiQA ports (>= 15/20): about 0.85 (port2 FiQA, seed 9: 19/20). K04 unsolved: about 0.7.
- J-NQ completes within the session (memory peaked at 23.4 GB of 32 GB in the trial): about 0.7. Given it completes, J-NQ ports: about 0.6.
- J-NQ clean Hit@5 (test half) between 0.55 and 0.80: about 0.8.

## 6. Amendments
(none yet)

**A1 — results and scorecard (20 Nov 2026, ~04:40 UTC; written after the results were read; sections 1 to 5 unedited).** Files: `kaggle/judged_v13_port_nq/`, `kaggle/judged_v13_port_fiqa/` (checkpoints and embeddings not committed).

*Identity, checked before reading verdicts:* both kernels COMPLETE, 0 tracebacks, device cuda, code SHA-256 `916c3864…294f`, seeds 58 and 60, settings exactly as section 2. J-NQ log confirms the reused embeddings came from the NQ trial output and no checkpoint was present.

| Run | Clean Hit@5 (test) | Detectors | Repairs | Solved (of 20) | Ports | Unsolved | Wall time | Peak RAM |
|---|---|---|---|---|---|---|---|---|
| J-NQ (seed 58) | 0.724 | 18 | 19 | **18** | yes | Q01 (detector THIN), K04 (detector and repair FAIL) | 1.6 h | 23.7 GB |
| J-FiQA (seed 60) | 0.535 | 19 | 19 | **19** | yes | K04 (detector and repair FAIL) | 0.25 h | 2.4 GB |

*Scorecard:* FiQA ports (0.85): held. K04 unsolved on FiQA (0.7): held. NQ completes (0.7): held. NQ ports given completion (0.6): held. NQ clean Hit@5 in [0.55, 0.80] (0.8): held (0.724).
*Note:* J-FiQA (seed 60) reproduces the earlier judged port2 FiQA run (seed 9) exactly on every summary figure (clean Hit@5 0.5354, 19/19/19, K04 unsolved). FiQA's hashed 50/50 query split does not depend on the seed, so the agreement is expected and not independent evidence; it confirms the port5 edits changed nothing.
