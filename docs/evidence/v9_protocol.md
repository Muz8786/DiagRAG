# v9 protocol (pre-registration). Written 19 Nov 2026, before any v9 run and before any v9 result.

v9 is the **final frozen bundle** that the owner runs by hand on Kaggle. It adds **one new experiment (the corpus-port arm on two new corpora)**, keeps every earlier frozen result as it is, and lists what it does **not** contain. No LLM API key is needed to run it.

## 0. What v9 is, and what it is not
- **It is** a bundle of frozen code, fixed seeds, fixed settings, verified inputs and fixed gates, plus the CPU analyses that were run on already-committed data, so that a reader can re-run everything and compare.
- **It is not** a new method. No detector, repair, dispatcher or gate changed. The v6 pipeline (adopted), v7 (composed arm) and v8 (fresh-seed repeat) stay as they are.
- **It does not claim** that the score moves. The score is the owner's own judgement (`A_TO_Z_GUIDE.md` section 9, about 7.8). Whether v9 moves it is for the owner to say after reading the results, not for this file to say.

## 1. What is in v9

| Part | What | Status when this protocol was written | Where |
|---|---|---|---|
| **P1** | Corpus port: BEIR **NFCorpus**, seed **53**, frozen `diagrag_port3.py` | **not yet run; the owner runs it** | `kaggle/DiagRAG_v9_port_nfcorpus.ipynb` |
| **P2** | Corpus port: BEIR **ArguAna**, seed **54**, frozen `diagrag_port3.py` | **not yet run; the owner runs it** | `kaggle/DiagRAG_v9_port_arguana.ipynb` |
| R1 | v6 judged runs (seed 50, GPU and CPU) | complete, ADOPTED | `kaggle/judged_gpu_v6_seed50/`, `kaggle/judged_cpu_run_v6_seed50/` |
| R2 | v7 composed arm (seed 51, CPU) | complete | `kaggle/judged_cpu_run_v7_seed50/` |
| R3 | v8 fresh-seed repeat of the frozen v6 code (seed 52, GPU) | launched 19 Nov 2026; result **not read** when this was written; protocol `docs/evidence/v8_protocol.md` | Kaggle kernel `syedmuzammilquadri/diagrag-v8-gpu-seed52` |
| A1 | Data-hygiene audit of the v6 GPU episodes | complete | `docs/evidence/v8_audit.py`, `v8_audit_v6gpu.json`, amendments E2 and E3 in `v8_protocol.md` |
| A2 | Emergent-failure breakdown of the v7 composed episodes | complete (post-hoc, descriptive) | `docs/evidence/v9_emergent_breakdown.py`, `v9_emergent_breakdown_v7.json` |
| A3 | v7 code-hash trail check | complete, consistent | `docs/evidence/check_v7_hash_trail.py`, `check_v7_hash_trail_output.txt` |
| A4 | LLM baselines (free-tier, B1 and B2) | complete | `kaggle/judged_llm_baselines/`, `docs/LLM_BASELINES_RESULTS.md` |

Every input of P1 and P2 is listed with its source, size and SHA-256 in `kaggle/judged_v9/INPUTS_MANIFEST.json`. `docs/evidence/v9_verify.py` re-checks every file hash in that manifest.

## 2. The port arm (P1, P2)
- **Code:** `kaggle/diagrag_port3.py`, generated from the judged `kaggle/diagrag_port2.py` (SHA-256 `ec113b047d2f13caa194713e6e71cbbafc730554460cbcd4820acf25a19134e0`, the hash of the SciFact and FiQA judged runs) by `kaggle/mk_port3.py`. The generator asserts **two** edits and nothing else: NFCorpus and ArguAna added to the verified-download table, and the output folder named `port3_<dataset>_out`. `diff diagrag_port2.py diagrag_port3.py` shows two hunks (`16c16` and `60c60,62`): 2 lines removed and 4 added. The frozen port3 hash is `677a2f38f24a5b0d64849e95930c93ecfd944e28d708753930fde1b2d3a77ada`.
- **Stack (unchanged from port2):** e5-small-v2 dense encoder in a FAISS HNSW index (M=32), BM25, min-max convex fusion (alpha 0.5), ms-marco-MiniLM-L-6-v2 reranker, Hit@5. English, free, no API.
- **Faults:** the 20 that port2 ported (Q01, Q03, Q04, Q05, K04, K05, K08, R01, R03, R05, R07, R10, R11, R13, R15, R19, R22, R23, R24, R25). **Q02, Q09, C2 and the ShopNova tenant, policy and product-code faults are not ported** (they need new injector code on the port stack; see section 5).
- **Settings (same as the judged port2 runs, except seed and corpus):** `N_QUERIES=2500, N_HARD=50, MAX_ATT=2500, N_HARM=20`, `TIME_BUDGET=36000`. Port2 ran on CPU; the Kaggle notebooks use a T4 if available. The device changes where the models run, not the arithmetic they perform in the script (no half precision), and the device is recorded in `PORT_PROTOCOL.json`. A device difference is therefore noted, not hidden.
- **Seeds:** NFCorpus 53, ArguAna 54. Used so far: 42 to 50 (judged runs), 51 (v7 composed arm), 52 (v8). **One run per corpus. A rerun or another seed needs the owner's written approval as an amendment here.**
- **Gates (port2's, unchanged):** a detector passes with held-out one-vs-rest AUROC >= 0.70 and >= 20 held-out positives; a repair passes with >= 20 hard episodes, Wilson 95% lower bound >= 0.50, and <= 10% of clean successes lost. A fault is solved only if both pass. **THIN, FAIL or missing counts as not solved.** "The suite ports" is claimed only if **>= 15 of the 20** pass both gates. The count and the list of unsolved faults are the headline, never a rate computed after dropping faults.
- **Splits:** 50/50 by an md5 of the query id (port2's rule), so the train and test halves share no query.

## 3. What each corpus is, and the limits that come with it (stated before any run)
- **NFCorpus (medical, 3,633 documents, 3,237 queries):** many relevant documents per query (graded qrels), which makes Hit@5 easier and the gold sets larger.
- **ArguAna (argument retrieval, 8,674 documents, 1,406 queries):** each query is a full argument and the single relevant document is its counter-argument. The script does **not** apply BEIR's rule that ignores the query's own document, so the clean Hit@5 is lower than published ArguAna figures (a **development smoke on 120 queries gave about 0.53 on the test half; that number is not used anywhere**). Fewer clean successes mean fewer eligible base queries for injected faults.
- **Query length differs a lot** (short medical questions against full paragraphs), so the query-letter faults (Q01, Q03, Q04, Q05) behave differently from the ESCI and BEIR SciFact and FiQA queries. That is a result, not a defect, but it is the likeliest place for failures.
- **Both are subsets of the project's fault catalogue on a different stack and domain.** Injected faults by the same authors remain the weakness; this arm tests generality across corpora, not field validity.

## 4. Predictions (my judgements from the port2 record, written so they can fail; not targets)
- NFCorpus ports (>= 15 of 20): about 0.6. ArguAna ports: about 0.45.
- The not-solved faults will include some of Q01, Q03, K04, R15, R22 (the ones that failed on SciFact): about 0.7 for at least two of them in at least one corpus.
- ArguAna clean Hit@5 (test half) below 0.60: about 0.8.
- A corpus yields **fewer than 20 held-out positives for at least one fault** (reported as THIN, counted not solved): about 0.5.
- Per-fault AUROC for the faults that pass is within 0.1 of the SciFact and FiQA values: about 0.6.

## 5. What v9 does not contain, and why (so nothing is read into its absence)
- **No frontier-LLM arm.** It needs a funded key and a spend cap set by the owner. The free-tier arms (R-A4) remain the only LLM comparison.
- **No document-text supervised baseline** (the "supervised telemetry against zero-shot LLM" objection stays open). The saved episodes do not store top-5 document text, so it needs a re-run and new code that was not written and tested in this session.
- **No multi-label dispatcher, no composed-arm repeat on the GPU stack, no local open-weight LLM arm, no full-suite port (Q02, Q09, C2, ShopNova faults), no density-matched permutation control.** Each needs new code and its own pre-registration; none was implemented, so none is claimed.
- **No change to U1 or Q03.** Redesigning either after seeing its result would be tuning to the test.
- **No new natural-traffic sample.** The 1,648 natural queries are the only ones left unexamined; they are used in R1 to R3 and are not independent across those runs.
- **No benchmark release.** The licence of the ShopNova corpus is unassigned and the owner publishes.

## 6. What a result would and would not show
- **A corpus ports (>= 15/20):** the detectors and repairs, built on ESCI, are not specific to one corpus **on this stack, for these 20 faults, injected by the same authors**. It would not show field validity, and it would not cover the 12 faults not ported.
- **A corpus does not port:** reported with the same prominence; `port_solved.csv` names the faults. SciFact (15/20) and FiQA (19/20) stay as reported; they are not edited or re-weighted.
- **Do not combine** the four corpora into one "ports on four domains" claim unless every corpus is listed with its own count. Two stacks (ESCI stack 1, BEIR stack 2) and four domains are not four independent stacks.
- **The owner's own number.** If the owner moves the score after reading these results, the reasoning belongs in the owner's section of the guide, not here.

## 7. How the owner runs it (in this order)
1. `python docs/evidence/v9_verify.py` from the repository root. It must print `ALL OK`. It checks the code hashes, the notebook embeds, the manifest file hashes and the protocol hashes.
2. Upload `kaggle/DiagRAG_v9_port_nfcorpus.ipynb` to Kaggle, Internet On, GPU T4 (or CPU), Run All. Same for `DiagRAG_v9_port_arguana.ipynb`. **One run each, no setting changed.** If the session stops, run again with the output attached; the script resumes from its checkpoint.
3. Save each notebook's `port3_<dataset>_out/` folder (`PORT_VERDICT.json`, `PORT_PROTOCOL.json`, `PORT_REPORT.md`, `port_*.csv`) into `kaggle/judged_port3_<dataset>/` (these four names: `judged_port3_nfcorpus`, `judged_port3_arguana`).
4. Check `PORT_PROTOCOL.json`: its `code_sha256` must equal `677a2f38…3a77ada`, and `device`, `cfg` must match section 2. If either differs, the run is not the pre-registered run and must be said so.
5. Compare the verdict with section 4, then add a dated amendment F1 below with the scorecard, **written after the results, leaving sections 1 to 7 unedited.**
6. R3 (v8): read its output and add its verdict to `docs/ALL_RUNS_MATRIX.md` under `docs/evidence/v8_protocol.md`, with the audit from `v8_audit.py` run on its `episodes.jsonl`.

## 8. Amendments
(none yet; each is dated and filed before the result it concerns is read)

**F0 — v8 result now in the bundle (19 Nov 2026; sections 1 to 7 are unedited).** Row R3 of section 1 said the v8 result had not been read. It has been: **NOT_ADOPTED at seed 52 (26 of 28 detectors; Q03 and C2 fail)**, scorecard in `docs/evidence/v8_protocol.md` E4, files in `kaggle/judged_gpu_v8_seed52/`, audit in `docs/evidence/v8_audit_v8gpu.json`, row added to `docs/ALL_RUNS_MATRIX.md`. v9's design does not depend on the v8 verdict (the port arm uses port2's own gates and stack), and nothing in sections 2 to 6 changes. **The seed-robustness of the v6 adoption is now an open finding that v9 does not address:** the same frozen code is ADOPTED at seed 50 and NOT_ADOPTED at seed 52.

**F1 — P1 and P2 launched (19 Nov 2026, 11:41 UTC; no v9 result exists or has been read; sections 1 to 7 are unedited).** The owner gave written permission in the session to run the new corpora, so the runs were started by the assistant through the Kaggle API instead of by the owner by hand (section 7 step 2 otherwise unchanged). Kernels: `syedmuzammilquadri/diagrag-v9-port-nfcorpus` (seed 53) and `syedmuzammilquadri/diagrag-v9-port-arguana` (seed 54), GPU T4, Internet On, pushed from the unmodified notebooks after `v9_verify.py` printed ALL OK. One run each; no setting was changed. Nothing about the pre-registered gates, seeds or predictions changed.
