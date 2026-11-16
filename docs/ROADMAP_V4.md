# Execution record — programme to 8.5 (v5 and beyond)

Started 16 Nov 2026 on branch `core28-kaggle-notebook`. Every number here is recomputed from files in this repository. Old runs are never edited; corrections go into new dated documents.
Running status of the seven workstreams is in section 9. Honest estimate: section 10 (written last).

## 1. First actions (16 Nov 2026)

1. **Private bench labels: safe.** `labels_test.jsonl` (369,129 bytes) hashes to `2e7cf4c09d1015c5ace01dbd628384c0dd91e9d6a855dfc47aa4c58d3f9de51f`, equal to `private_test_labels_sha256` in `bench/release_v1/MANIFEST.json`.
   It is now in the **private** repo `Muz8786/diagrag-data` under `private_bench_v1/` (commit `45b5212`), with the reference-baseline predictions and the build checkpoint
   (v3 CPU seed 45, uncompressed SHA-256 `59aac053…028b`, gzip-split into three 90 MiB parts, round-trip verified). The repo reports `private: true`. After the push, the labels were
   re-downloaded from GitHub and hashed again: the value matched. All nine uploaded blob IDs equal the local ones.
2. **Keys.** Only `KAGGLE_API_TOKEN` is present in the environment. No Groq, Gemini or frontier key is set, so Workstream 4 cannot run yet (section 6).
   The repo and zip were scanned for key patterns before every push.
3. **Smoke notebook.** The throwaway private notebook `diagrag-v4-notebook-smoke` on the spare Kaggle account can be deleted by the owner. I took no action on it.

## 2. Workstream 1 — why the gates flipped (diagnosis only; no code, bar or threshold changed)

Script: `docs/evidence/diagnose_gate_flips.py` (SHA-256 recorded in the commit). Output: `docs/evidence/gate_flips_result.json`.
It re-fits each run's attributor from that run's own `episodes.jsonl`, using the shipped hyper-parameters, seed and calibration split, then asks the questions below.
The episodes in the v4 GPU checkpoint and in `episodes.jsonl` are bit-identical (0 differing feature cells of 4,845 episodes).

**Replication check.** For all five CPU runs (seeds 42–45 and 47), run in this sandbox, the re-fit reproduces the judged C2 AUROC to within 0.0002 (four of them exactly).
For the two GPU runs, which ran on Kaggle's library stack, it is off by 0.001 (seed 46) and **0.019 (seed 48: reported 0.612, re-fit 0.631)**. Both seed-48 values are below the 0.70 bar, so the verdict is the same either way.
The 0.019 gap is unresolved. I cannot tell from the files whether it comes from library versions or threading on Kaggle, and I did not investigate further.

### 2a. The two detectors across all seven judged runs

| Run | Stack / code era | Q03 held-out AUROC [95% CI] | Q03 verdict | C2 held-out AUROC [95% CI] | C2 verdict | Detectors passing (of 28) |
|---|---|---|---|---|---|---|
| seed 42 | CPU, v1 (synonym-swap Q03) | 0.866 [0.769, 0.950] (n=25) | PASS | 0.808 [0.691, 0.904] (n=25) | PASS | 28 |
| seed 43 | CPU, v1 (synonym-swap Q03) | 0.934 [0.879, 0.974] (n=25) | PASS | 0.823 [0.716, 0.921] (n=25) | PASS | 28 |
| seed 44 | CPU, v2 (synonym-swap Q03) | 0.877 [0.783, 0.966] (n=25) | PASS | 0.825 [0.721, 0.912] (n=25) | PASS | 28 |
| seed 45 | CPU, v3 (real query-pair Q03) | 0.559 [0.462, 0.663] (n=25) | FAIL | 0.777 [0.649, 0.896] (n=25) | PASS | 27 |
| seed 46 | GPU, v3 (real query-pair Q03) | 0.654 [0.547, 0.760] (n=25) | FAIL | 0.909 [0.822, 0.977] (n=25) | PASS | 27 |
| seed 47 | CPU, v4 (real query-pair Q03) | 0.704 [0.584, 0.823] (n=25) | PASS | 0.916 [0.858, 0.962] (n=25) | PASS | 28 |
| seed 48 | GPU, v4 (real query-pair Q03) | 0.691 [0.573, 0.799] (n=25) | FAIL | 0.612 [0.466, 0.733] (n=25) | FAIL | 26 |

25 of the 28 core detectors never failed and never fell below AUROC 0.80 in any of the seven runs. The three exceptions are Q03, C2 and K04 (K04: never failed, minimum 0.767).
All the gate instability in the record sits in Q03 and C2.

### 2b. Q03 is not noisy. Its construction changed, and its true AUROC under the v3/v4 construction is below the bar.

| | Runs | AUROCs | Inverse-variance mean [95% CI] | Within-era heterogeneity (Cochran Q) |
|---|---|---|---|---|
| v1/v2, synonym-swap Q03 | seeds 42–44 | 0.866, 0.934, 0.877 | **0.912 [0.874, 0.950]** | Q = 2.42, df 2, p = 0.30 |
| v3/v4, real query pairs from other users | seeds 45–48 | 0.559, 0.654, 0.704, 0.691 | **0.645 [0.591, 0.700]** | Q = 4.39, df 3, p = 0.22 |
| all seven as one population | | | | **Q = 68.3, df 6, p = 9e-13** |

- The era difference is 0.267 AUROC (z = 7.8). The seven runs are not draws from one true AUROC. Within each era they are consistent with one (small samples, so low power).
- Pooled out-of-fold AUROC over all ~50 Q03 positives per run (train + test): 0.557, 0.724, 0.639, 0.712 for seeds 45–48. This agrees with the era mean and not with the bar.
- If 0.645 is the truth, each v3/v4 run passes with probability 0.14–0.18, so 1 pass in 4 runs (0.66 expected) is the typical outcome. **Q03 fails its detector gate by expectation, not by bad luck.**
- Why: v1/v2 replaced words by rare synonyms, which leaves a trace in `q_synlow` and `q_lowdf`. v3 replaced the query by another real user's query for the same product, which leaves almost none. This matches `docs/IDENTIFIABILITY.md`
  (Q03 is in three of the five least-separable pairs, K04|Q03 at 0.79).
- **What this does to the v5 floor of 50 positives.** A larger n narrows the interval and does not move the true AUROC. At true AUROC 0.645 the chance of an observed value ≥ 0.70 falls from 0.18 at n = 25 to 0.10 at n = 50
  (Hanley–McNeil standard errors 0.060 and 0.043; the bootstrap standard errors in the judged runs, 0.051–0.061, agree). So the floor change makes Q03's FAIL more certain.

### 2c. C2 passes in the pooled data every time. The seed-48 FAIL is a test-split outcome whose mechanism I did not identify.

| Run | C2 test split (25) | C2 train split (25, never used to fit the attributor) | C2 pooled (50) | Random 25-of-50 re-splits: mean (SD) | Observed test value sits at percentile |
|---|---|---|---|---|---|
| seed 42 (CPU) | 0.808 [0.70, 0.90] | 0.874 [0.80, 0.93] | 0.841 [0.78, 0.90] | 0.841 (0.032) | 16 |
| seed 43 (CPU) | 0.823 [0.71, 0.92] | 0.812 [0.69, 0.93] | 0.818 [0.73, 0.90] | 0.818 (0.042) | 55 |
| seed 44 (CPU) | 0.825 [0.72, 0.91] | 0.873 [0.77, 0.96] | 0.849 [0.78, 0.91] | 0.849 (0.034) | 25 |
| seed 45 (CPU) | 0.777 [0.65, 0.89] | 0.744 [0.60, 0.88] | 0.761 [0.66, 0.84] | 0.762 (0.046) | 63 |
| seed 46 (GPU) | 0.908 [0.82, 0.98] | 0.754 [0.60, 0.89] | 0.831 [0.74, 0.91] | 0.832 (0.043) | 96 |
| seed 47 (CPU) | 0.916 [0.86, 0.96] | 0.755 [0.65, 0.85] | 0.835 [0.77, 0.89] | 0.836 (0.030) | 100 |
| seed 48 (GPU) | 0.631 [0.48, 0.77] | 0.893 [0.78, 0.97] | 0.762 [0.67, 0.85] | 0.763 (0.044) | 0 |

- C2's score is the second-largest group probability mass of the single-fault attributor. The attributor never trains on C2 episodes, so the 25 train-split C2 episodes are a second held-out sample scored by the same model.
  In seed 48 they score **0.893** while the test split scores 0.631, with the same attributor. The attributor did not get worse; the two halves of the data disagree.
- Pooled over 50 episodes, C2 is 0.761–0.849 in all seven runs. Seed 48 (0.762) and seed 45 (0.761, a PASS on its test split at 0.777) are the same.
- The spread of the test-split value across runs (SD 0.095) is 2.4 times what random re-splitting of each run's own 50 episodes gives (mean SD 0.039; variance ratio 5.8). Seed 48's observed value is below all 4,000 random re-splits.
  So a plain unlucky 25-of-50 draw does not explain it.
- **Hypotheses I tested and rejected or could not support:**
  - *Pair composition.* Q03+R05 is the only pair type that is masked (second-group mass below the 90th percentile of single faults) in at least half of the runs. Seed 48's share of such pairs in its test split is 0.16, mid-range.
    Across the seven runs the correlation between that share and the test AUROC is −0.31 (n = 7, no support).
  - *A shift between stacks.* The two GPU runs sit at opposite ends (0.908 and 0.631), and the CPU runs span 0.777–0.916. Two GPU runs cannot show or exclude a stack effect.
- **Not tested:** whether episodes that share a base query (the split is by base-query hash) create clustering that the episode-level re-split ignores. At most two episodes per base query are allowed, so I expect the effect to be small, but I have not measured it.
- Status: **mechanism not identified.** What the data supports is narrower: C2's detector is marginal-but-passing in pooled data (0.76–0.85, bar 0.70), and its test-split estimate has more noise than binomial sampling predicts.

### 2d. What the record implies for the 27-detector rule (planning aid, not evidence)

- Adoption needs at most one detector failure among 28. Only Q03 and C2 have ever failed (K04 has not). With Q03 failing by expectation, the rule is met only if every other detector passes, C2 included.
- Frequencies from the record (add-one smoothed): Q03 fail rate in the v3/v4 era 0.67, C2 fail rate 0.22. If the two are independent, the 27-detector rule is met with probability about **0.85**, and the observed record is consistent with that (the rule was met in 6 of 7 runs, and missed in the one run where both failed).
- This is built from seven runs of one code family, so treat 0.85 as rough. It is not a stability guarantee. **A single v5 run cannot demonstrate stability; it is one more draw.**

### 2e. Where this contradicts the premise of Workstream 2

The brief expects a v5 whose verdict is "stable rather than seed-lucky". The diagnosis says the instability is two different things. Q03 is a stable FAIL under the v3/v4 construction, and the floor change tightens that FAIL.
C2 is a noisy PASS whose noise is partly unexplained. Raising n to 50 improves C2's odds (at a true AUROC of 0.76 the chance of passing rises from 0.86 to 0.93, at 0.80 from 0.97 to 1.00), but does not remove the unexplained component.
What v5 can honestly deliver on stability is a tighter measurement and the diagnosis above, not a guaranteed ADOPTED. Whether to keep Q03 inside the adoption count is a bar decision, which §10 of the brief forbids me to change.
I flag it for the owner instead of acting on it: report Q03 as a known detector failure in the paper, with the era table above.
