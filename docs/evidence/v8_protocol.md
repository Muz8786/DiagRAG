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
(none yet; each is dated and filed before the result it concerns is read)
