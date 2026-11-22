# v11.a protocol (pre-registration). Written 19 Nov 2026, before any v11.a run and before any v11.a result.

v11 has two parts. **v11.a (this file) needs no API key of any kind.** **v11.b (`docs/evidence/v11b_protocol.md`) uses the free-tier LLM keys and is not run until the owner says v11.a is done.** No key, token or secret appears in any v11.a file, notebook or log.

## 0. What v11.a is
A fresh, fully pre-registered run of everything that can run without a key: (R1) the frozen v6 code on a new seed, (R2) the port arm on a **new corpus (SCIDOCS)**, (R3) the analyses that were done post-hoc elsewhere, now fixed in advance and applied to the new runs, and (R4) one generated A-to-Z report that assembles every result in the repository, with anything not run marked "not run". It is **not** a new method and changes no detector, repair, dispatcher or gate.

## 1. Runs

| Id | What | Code (frozen) | Seed | Where | Output folder |
|---|---|---|---|---|---|
| R1 | Main pipeline, ESCI, 32 faults, GPU | `kaggle/diagrag_v6.py`, SHA-256 `44176b9a5ad633e39ec29581237d9919619b9944471178effb172be1d276e28a` | **55** | Kaggle T4 | `kaggle/judged_gpu_v11a_seed55/` |
| R2 | Port arm, BEIR SCIDOCS, 20 faults | `kaggle/diagrag_port4.py` | **56** | Kaggle T4 | `kaggle/judged_port4_scidocs/` |
| R3 | Analyses on the new runs (below) | scripts listed in section 3 | n/a | CPU | `kaggle/judged_v11a/` |
| R4 | A-to-Z report | `docs/evidence/v11_report.py` | n/a | CPU | `kaggle/judged_v11a/REPORT_V11A.md` |

- **Frozen port4 hash:** the frozen port4 hash is `dd6ddff6a7c5541a9ef57612ec3338a1aafb12daa7b19c44cc4b364dded13431`. `kaggle/diagrag_port4.py` is generated from the frozen v9 `diagrag_port3.py` (`677a2f38…3a77ada`) by `kaggle/mk_port4.py`, which asserts **two** edits and nothing else (SCIDOCS added to the verified-download table with its measured size 142,471,588 and SHA-256 `96640201…17ef1`; output folder named `port4_<dataset>_out`). Gates, faults, injectors, repairs and stack are port2's, unchanged.
- **Seeds:** used so far 42 to 50, 51 (v7 composed arm), 52 (v8), 53 and 54 (v9 ports). R1 uses 55 and R2 uses 56. **One run each; no rerun, no other seed.** A rerun needs the owner's written approval as an amendment.
- **R1 settings = v6 GPU settings, only the seed differs:** `N_BASE_ESCI=6000, N_PRDC=528, N_HARD=100, MAX_ATT=4000, N_HARM=20, TIME_BUDGET=30000`, bge-reranker-large.
- **R2 settings = port2 settings, only the corpus and seed differ:** `N_QUERIES=2500` (SCIDOCS has 1,000 queries, so every query with positive qrels is used), `N_HARD=50, MAX_ATT=2500, N_HARM=20, TIME_BUDGET=36000`.

## 2. How R1 is read (the rule that stops this from being seed-shopping)
The v6 code has now been run on three GPU seeds: 50 (ADOPTED), 52 (NOT_ADOPTED) and, here, 55. **The headline for the adoption question is the pair "adopted in k of 3 GPU seeds"**, with all three rows in `docs/ALL_RUNS_MATRIX.md`, and the descriptive interval analysis (`docs/evidence/v10_adoption_intervals.py`) re-run over all judged runs. **No fourth GPU seed is run, whatever R1 shows.** If R1 is ADOPTED the sentence is "adopted in 2 of 3 GPU seeds"; if not, "adopted in 1 of 3". Neither is edited afterwards. The adoption rule, bars and gates are those of `docs/evidence/v6_protocol.md` section 1, unchanged.

## 3. Analyses applied to the new runs (fixed now; each is the script already committed)
- **On R1 episodes:** `docs/evidence/v8_audit.py` (split leakage, duplicates, label-permutation control, single-feature scan, bootstrap stability, query-text-only baseline; scikit-learn 1.6.1) and `docs/evidence/v10_adoption_intervals.py` (adoption count with intervals).
- **On R2:** the port summary table (`docs/evidence/v9_port_summary.py`, extended to five corpora by the report generator), and the supervised text baseline of `docs/evidence/v10_textbaseline_protocol.md` applied unchanged to SCIDOCS (replay with `v10_textview.py` on the new frozen hash, then `v10_textbaseline.py`; the same replay check of at least 99.5% must pass or the baseline is reported as not run).
- **Not re-run, already reported:** v6, v7, v8, the v9 ports, the multi-label study and the free-tier LLM baselines. The report generator reads their committed files.

## 4. Predictions (my judgements from the record; written so they can fail)
- **R1 ADOPTED:** about 0.5 (v6 seed 50 adopted; v8 seed 52 not; v4 GPU seed 48 not). Q03 detector FAIL: about 0.9. C2 detector at or above 0.70: about 0.5. U1 below 0.50: about 0.9. L1, L2, N1 each PASS: about 0.85. D2 PASS: about 0.5. Detection AUROC within 0.02 of 0.974: about 0.9.
- **Adoption headline:** "adopted in 2 of 3 GPU seeds" about 0.5; "1 of 3" about 0.5.
- **R1 audit:** label-permutation control inside [0.45, 0.55]: about 0.1 (it missed in both earlier audits). Query-string leak effect below 0.5 point: about 0.9.
- **R2 SCIDOCS:** clean Hit@5 on the test half below 0.50: about 0.9 (a smoke at tiny settings gave about 0.36 to 0.39; not a result). Ports (>= 15 of 20 solved): about 0.3. At least three faults THIN or untrained: about 0.6, because a low clean Hit@5 leaves few eligible base queries.
- **Text baseline on SCIDOCS** (if enough held-out positives): telemetry beats the text model with a positive lower bound: about 0.7.

## 5. What v11.a does not contain
No LLM arm of any kind (v11.b), no frontier arm, no U1 or Q03 redesign, no new natural-traffic sample (the 1,648 are reused in R1), no composed-arm repeat, no full-suite port (Q02, Q09, C2, ShopNova faults), no benchmark release. R1 reuses the same base queries, split and natural sample as v6 and v8, so it tests re-randomisation, not new data; R2 is the new data.

## 6. What a result would and would not show
- R1 tells how stable the v6 adoption is across seeds. It is not new evidence on a new corpus or a field system.
- R2 on SCIDOCS: if it does not port, the reason (few hard episodes under a low clean Hit@5) is part of the result and is reported with the per-fault table. SciFact, FiQA, NFCorpus and ArguAna stay as reported; no corpus is dropped or re-weighted, and no combined "ports on N domains" sentence is allowed unless every corpus is listed with its own count.
- Nothing here moves the score by itself. The score is the owner's judgement.

## 7. How v11.a is run
1. `python docs/evidence/v11_verify.py` prints `ALL OK` (hashes, notebooks, seeds, settings).
2. R1 and R2 are pushed to Kaggle from the unmodified notebooks (GPU T4, Internet On) and left to finish. Kernels: `syedmuzammilquadri/diagrag-v11a-main-seed55` and `syedmuzammilquadri/diagrag-v11a-port-scidocs`. Their outputs are collected only after both report COMPLETE.
3. Identity check before any result is read: code SHA-256, seed, settings, device, no traceback.
4. R3 analyses, then `python docs/evidence/v11_report.py`. Results and a scorecard against section 4 go into section 8 below as a dated amendment, written after the results, with sections 0 to 7 unedited.

## 8. Amendments
(none yet; each is dated and filed before the result it concerns is read)

**A1 — R1 and R2 launched (19 Nov 2026, about 14:00 UTC; no v11.a result exists or has been read; sections 0 to 7 are unedited).** Kernels `syedmuzammilquadri/diagrag-v11a-main-seed55` (R1) and `syedmuzammilquadri/diagrag-v11a-port-scidocs` (R2) were pushed from the unmodified notebooks after `docs/evidence/v11_verify.py` printed ALL OK. At the time of writing R2 was RUNNING and R1 was QUEUED (Kaggle limits concurrent GPU sessions); queueing changes nothing about the run. One run each; no setting changed. No API key was used to build, push or run anything in v11.a; the Kaggle token was supplied only as an environment variable for the push command. The `docs/evidence/v11_report.py` generator was written before any result and prints `not run` for missing files.
