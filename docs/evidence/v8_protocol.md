# v8 protocol (pre-registration). Written 19 Nov 2026, before any v8 run and before any v8 result.

## 0. Why v8 exists, said plainly
`docs/ROADMAP_V4.md` section 13.3 and `A_TO_Z_GUIDE.md` sections 8 and 10 list weaknesses that need no LLM key to address. v8 targets three:
(i) **single-run adoption**: v6 was judged once per stack at seed 50, and adoption came only after two NOT_ADOPTED runs and a construction change;
(ii) **fragile verdicts**: several gates were decided by 0.001 to 0.005;
(iii) **inflation risk**: no control shows that the headline AUROC and identification numbers are not produced by leakage or by a feature that reads the label.
v8 is **not** a new method. It runs the **frozen v6 code unchanged** on a fresh seed and adds descriptive checks on saved episodes. v6 stays in the record as ADOPTED (GPU 27/28, CPU 28/28) whatever v8 shows.

## 1. What is fixed
- **Code:** `kaggle/diagrag_v6.py`, SHA-256 `44176b9a5ad633e39ec29581237d9919619b9944471178effb172be1d276e28a` (the frozen v6 hash; asserted by the notebook before it runs). No line of it changes.
- **Every gate, bar, policy and the adoption rule** are those of `docs/evidence/v6_protocol.md` section 1 (>= 27 detectors, >= 24 repairs, L1, L2, U1 0.50, N1, D1, D2, D3 as in `PREREGISTERED_ANALYSIS.json`). Nothing is added, loosened or re-weighted.
- **Settings:** identical to v6 GPU except `SEED`: `N_BASE_ESCI=6000, N_PRDC=528, N_HARD=100, MAX_ATT=4000, N_HARM=20, TIME_BUDGET=30000`, bge-reranker-large on a Kaggle T4.

## 2. What changes
- **Seed 52** (used seeds: 42 to 50 for the judged runs, 51 for the v7 composed arm). Chosen now, before any run; no run has used it. The v6 protocol forbids seed-shopping, so: **one GPU run at seed 52, reported whichever way it falls.** A second run, or any other seed, needs the owner's explicit approval written here as an amendment.
- The notebook is derived from `kaggle/DiagRAG_v6_kaggle.ipynb` by `kaggle/mk_v8_notebook.py`, which asserts it changes only the seed, the title text and the run label. Embedded code, exclusions file and analysis script keep their hashes.

## 3. What the seed does and does not vary (so nobody over-reads a pass)
- **Varies:** injection randomness, hard-episode selection order, model and classifier seeds, bootstrap draws, the ESCI query shuffle.
- **Does not vary:** the train/test split (md5 of the gold component, not the seed), the base-query pool (`N_BASE_ESCI=6000` takes all 5,527 examined ESCI queries), the corpus, the **1,648 natural queries** (fixed by `natural_exclusions_v2.json`) and the author-written fault injectors.
- Therefore v8 tests **stability under re-randomisation of the same construction**. It is **not** an independent sample of queries, a second corpus or a field test, and the natural-traffic result (N1, D2, D3) is **not** a second natural sample: the same 1,648 queries are used again. Problems 2, 8 (new natural sample) and 14 (real field failures) are **not** addressed by v8 and stay open.

## 4. Data-hygiene audit on saved episodes (CPU, descriptive, no new generation)
Script: `docs/evidence/v8_audit.py`, run on `kaggle/judged_gpu_v6_seed50/episodes.jsonl` first and on the v8 episodes after the run. Every check is reported, pass or fail.
- **A1, split leakage:** base-query overlap between train and test (v6: 0), and case-insensitive query-string overlap (v6 audit before this protocol: **7 strings**). Report which faults those 7 belong to and re-compute the held-out identification accuracy with those test episodes removed. A drop larger than 0.5 point is reported as a leak effect.
- **A2, exact duplicates:** identical feature vectors across train and test; identical (query, fault) pairs.
- **A3, label permutation control:** re-fit the attributor with train labels shuffled (20 shuffles); held-out fault-vs-clean AUROC must be within [0.45, 0.55]. If not, the pipeline leaks and **no number in the project is trusted until explained**.
- **A4, single-feature leakage scan:** held-out fault-vs-clean AUROC of every single feature. Any feature with AUROC >= 0.99 alone is listed and the attributor is re-fit without it; the change in headline numbers is reported.
- **A5, re-fit stability:** 20 re-fits of the attributor with different seeds on the same split; report mean and range of detection AUROC and exact-fault accuracy, so reviewers can see how much of a headline number is seed noise.
- **A6, query-text-only supervised baseline:** a TF-IDF (character n-grams) logistic regression on the query string alone, trained on the same train split, scored on the same held-out episodes. It answers "is the telemetry adding anything beyond the (possibly corrupted) query text". It is **not** a document-text baseline: top-5 document text is not stored in `episodes.jsonl`, so that baseline needs a re-run and is **not** part of v8.
- Class balance: test counts per fault and clean share are printed beside every accuracy, so "89.9% on faulted" is never read without n.

## 5. What is not done, and why
- **No frontier-LLM arm** (needs a funded key).
- **No U1 or Q03 redesign.** Changing either after seeing results is tuning to the test; a redesign would need its own pre-registration and a fresh seed.
- **No multi-label dispatcher, no full-suite second-corpus port, no benchmark release.** Each is a separate piece of work with its own protocol, or needs the owner's decisions.

## 6. Predictions (judgements from the v6 record, written so they can fail)
- Adoption (>= 27 detectors, >= 24 repairs) met at seed 52 on the GPU: about 0.6. The v6 GPU run met it with zero slack and v4 on GPU missed it at 26/28.
- Q03 detector FAIL: about 0.9. U1 below 0.50: about 0.9.
- L1, L2 and N1 PASS: about 0.85 each (N1 reuses the same 1,648 queries).
- Detection AUROC within 0.02 of v6: about 0.9.
- A3 permutation control in [0.45, 0.55]: about 0.97.
- A1 leak effect below 0.5 point: about 0.9.
- A6 query-text-only baseline well below the telemetry attributor: about 0.9.

## 7. What a result would and would not show
- ADOPTED again: the v6 adoption is not a one-seed accident of injection randomness. It still rests on author-injected faults on one corpus.
- NOT_ADOPTED: reported with the same prominence in `docs/ALL_RUNS_MATRIX.md`; the per-fault table says which detector. The v6 ADOPTED verdict is not edited; the headline becomes "adopted at seed 50, not at seed 52".
- A3 or A4 failing is a more serious finding than any gate: it would mean part of the headline is not evidence.

## 8. Amendments
**E1 — A5 corrected (19 Nov 2026, after the v8 GPU kernel was launched; no v8 result and no audit result exists).** A5 said "20 re-fits with different seeds". Checked before any audit ran: the attributor (`HistGradientBoostingClassifier`, no subsampling, no early stopping) gives **identical probabilities for different `random_state` values** (max absolute difference 0.0 on 500 rows, scikit-learn 1.6.1), so seed re-fits would all be identical and would hide the real variability. A5 is replaced by: **20 bootstrap resamples of the training episodes (sampling with replacement, resample seeds 0 to 19), same settings, scored on the same held-out episodes; report mean, min and max of detection AUROC and exact-fault accuracy.** This measures sensitivity to the training sample, which is what a reviewer wants to know. Nothing else in section 4 changes. The audit uses scikit-learn **1.6.1**, the version recorded in the v6 run, because verdicts at the 0.001 level are version-fragile (`A_TO_Z_GUIDE.md` section 10).

**E2 — hygiene audit of the v6 GPU episodes (19 Nov 2026). Run on `kaggle/judged_gpu_v6_seed50/episodes.jsonl` while the v8 GPU run was still going; no v8 result existed. scikit-learn 1.6.1. Files: `v8_audit.py`, `v8_audit_v6gpu.json`.** Written after the results; section 4 above is unchanged.
- **Reproduction.** The re-fit reproduces the committed numbers: exact-fault accuracy on faulted 0.8967 (n = 1,510) equals `diagnosis_confusion_v6gpu.json`. Fault-vs-clean AUROC is 0.9739 here against 0.9746 in the run's `detection_baselines.csv` (the run's own score came from a slightly different fit; a 0.0007 gap).
- **A1, split leakage: PASS.** Base-query overlap train/test is 0. 28 held-out episodes (K07 8, K09 5, clean 15) have a query string that also appears in train (case-insensitive; 7 strings in the earlier screen counted bases, this counts episodes). Removing them changes exact-fault accuracy by 0.09 points and AUROC by 0.0003: below the 0.5-point flag.
- **A2, duplicates: no feature-vector duplicates** between train and test (0). 23 held-out episodes repeat a (query, fault) pair seen in train; reported, not removed.
- **A3, label permutation: MISSED its pre-registered band.** 20 shuffles give AUROC mean 0.535, min 0.465, max 0.582; the band was [0.45, 0.55], so **A3 is recorded as FAIL**. The band is not changed. The protocol says a miss means no number is trusted until it is explained, so a follow-up was run (E3 below, post-hoc).
- **A4, single-feature leakage: PASS.** The strongest single feature (`s_gap`) has direction-free AUROC 0.708; none reaches 0.99. No feature alone separates faulted from clean.
- **A5, bootstrap stability (E1 version): AUROC mean 0.9713 [0.9695, 0.9731]; exact-fault accuracy on faulted mean 0.8825 [0.8728, 0.8921]** over 20 resamples of the training set. The committed single-fit 0.8967 sits at the upper edge; the stable figure is about 88 to 90%, not a point value.
- **A6, query-text-only baseline.** Fault-vs-clean AUROC 0.570 and exact-fault accuracy 16.4%, against telemetry 0.974 and 89.7%. By group (exact accuracy, query text vs telemetry): Q 42.6% vs 78.0% (n = 350), K 15.8% vs 94.4% (n = 450), R 3.8% vs 92.4% (n = 710). The telemetry is doing the work, not the query string. This is a query-only baseline; it is **not** the document-text supervised baseline, which needs a re-run.

**E3 — post-hoc explanation of the A3 miss (19 Nov 2026; written after A3 was read, so exploratory, not a gate). Files: `v8_audit_a3_followup.py`, `v8_audit_a3_followup_v6gpu.json`.**
- The shuffled-label drift (mean excess about 0.035 over 0.5; the test-label permutation null is 0.500 with sd 0.009) is a real shift, not noise.
- A score that uses **no labels at all** (mean distance of a held-out episode to its 5 nearest training episodes in standardised feature space) separates faulted from clean with AUROC **0.72** (median distance 3.65 faulted, 2.57 clean). Faulted episodes lie in sparser regions of feature space than clean ones, and a tree model trained on shuffled labels can echo that density structure. **That is the most likely explanation: covariate shift in the features, not label leakage.** It is an explanation, not a proof.
- What this does and does not settle: the real-label AUROC (0.974) is 0.44 above the shuffled-label AUROC (0.535), so the excess of about 0.035 cannot account for the headline. But the headline's **first-order claim stands on a feature space where faulted episodes are already partly separable without labels (0.72)**, and a reader should know that. A stricter control that removes this effect (for example matching clean and faulted episodes on feature density) was not pre-registered and was not run; it is left open.

**E4 — v8 result and scorecard against section 6 (19 Nov 2026, written after the result was read; sections 1 to 7 and E1 to E3 are unedited). Stored in `kaggle/judged_gpu_v8_seed52/`; audit in `docs/evidence/v8_audit_v8gpu.json`.**

*Identity of the run (checked before any result was read).* Kaggle kernel `syedmuzammilquadri/diagrag-v8-gpu-seed52`, status COMPLETE, started 04:39:58 UTC, GPU (`cuda`), reranker `BAAI/bge-reranker-large`. `JUDGED_PROTOCOL.json` records code SHA-256 `44176b9a5ad633e39ec29581237d9919619b9944471178effb172be1d276e28a` (the frozen v6 hash), seed 52, and the pre-registered settings (`N_BASE_ESCI=6000, N_PRDC=528, N_HARD=100, MAX_ATT=4000, N_HARM=20`). The log has no traceback. It is one run, with no rerun and no setting changed.

*Verdict: **NOT_ADOPTED**.* Detectors 26 (bar 27), repairs 27 (bar 24), solved both 26 of 28. The two missing detectors are **Q03** (held-out AUROC 0.618 [0.538, 0.691], bar 0.70; FAIL in v6 as well at 0.642) and **C2** (0.681 [0.579, 0.786]; **PASS in v6 at 0.751 [0.656, 0.847]**). R26 is THIN in both runs and sits outside the core 28. The C2 interval straddles the 0.70 bar and overlaps v6's, so the C2 change from PASS to FAIL is within sampling noise; it is also the whole difference in the verdict.

| | v6 GPU, seed 50 | v8 GPU, seed 52 (same code) |
|---|---|---|
| Verdict | ADOPTED | **NOT_ADOPTED** |
| Detectors / repairs / both | 27 / 27 / 27 | 26 / 27 / 26 |
| L1 clean loss | 0.28% (PASS) | 0.40% (PASS) |
| L2 mean closure | 0.844 (PASS) | 0.886 (PASS) |
| U1 (bar 0.50) | 0.406 (FAIL) | 0.397 (FAIL) |
| N1 natural gain | +2.18 [+1.33, +3.03] (PASS) | +2.06 [+1.21, +2.97] (PASS) |
| Detection AUROC, fault vs clean | 0.9746 [0.970, 0.980] | 0.9734 [0.968, 0.978] |
| D2 (loop non-inferior to universal repair, margin -0.5 pt) | PASS (CI lower bound -0.49 pt) | **FAIL (CI lower bound -0.67 pt)** |
| D3 | FAIL | FAIL |
| `capped_crc_0.005` meets all four targets | yes | yes |

Note on D2: both runs sit within 0.2 points of the margin on either side, on the **same 1,648 natural queries**, so this is a re-measurement of one sample and not evidence from a second one.

*Hygiene audit on the v8 episodes (same script as E2).* Reference exact-fault accuracy on faulted 0.8934 (n = 1,510), AUROC 0.9727. A1 split leakage: base-query overlap 0; 26 held-out episodes share a query string with train; removing them changes accuracy by 0.08 points (below the 0.5 flag). A2: no identical feature vectors across splits; 19 repeated (query, fault) pairs. **A3 missed its band again: mean 0.531, min 0.480, max 0.585 (band 0.45 to 0.55), recorded FAIL; E3's covariate-shift explanation applies unchanged and no new explanation was tested.** A4: strongest single feature `s_gap` AUROC 0.707, none near 0.99. A5: bootstrap AUROC 0.9707 [0.9680, 0.9733], exact-fault accuracy 0.8812 [0.8702, 0.8920]. A6: query-text-only baseline AUROC 0.589 and exact accuracy 15.9%, against telemetry 0.973 and 89.3%.

*Scorecard against section 6 (predictions as written).*
1. Adoption met at seed 52 on the GPU (about 0.6): **did not hold.** NOT_ADOPTED, 26 detectors.
2. Q03 detector FAIL and U1 below 0.50 (about 0.9 each): **held** (Q03 0.618; U1 0.397).
3. L1, L2 and N1 PASS (about 0.85 each): **held**, all three.
4. Detection AUROC within 0.02 of v6 (about 0.9): **held** (0.9734 against 0.9746).
5. A3 permutation control inside [0.45, 0.55] (about 0.97): **did not hold** (mean 0.531, max 0.585), as in v6.
6. A1 leak effect below 0.5 point (about 0.9): **held** (0.08).
7. A6 query-text-only baseline well below telemetry (about 0.9): **held**.
Not predicted, and the reason for item 1: **C2's detector fell below 0.70.**

*What this does and does not show.* The v6 adoption was **not robust to the seed**: the same frozen code, settings and stack gave ADOPTED at seed 50 and NOT_ADOPTED at seed 52, and the margin in both was zero or one detector (v6 had 27 of the 27 required with Q03 failing; v8 has 26). The project record now contains two GPU runs of this configuration with different verdicts; **neither replaces the other**, and the honest statement is "adopted at seed 50, not adopted at seed 52 (C2 at 0.681)". Everything else measured here (detection AUROC about 0.973 to 0.975, exact-fault accuracy 88 to 90%, repairs 27 of 27, L1, L2, N1 pass, U1 about 0.40 failing) is stable between the two seeds. The injectors, corpus, split and natural sample are the same in both, so this tests re-randomisation only, not a new corpus or a new sample. No third seed was run, and none is proposed: seed-shopping to restore ADOPTED is not allowed by the protocol.
