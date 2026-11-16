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

## 3. Workstream 2 — v5, the stability run: designed, frozen, tested on CPU, **not run**

- Pre-registration: `docs/evidence/v5_protocol.md`, with amendments B1 to B6, all committed before any v5 result. Frozen code: `kaggle/diagrag_v5.py`, SHA-256 `deecafad69b49c5ae87ee7031f23d24553ea092cf390b964859dbae81091702a` (generated from v4 by `kaggle/mk_v5.py`; the diff against v4 is 26 asserted replacements).
- **What changed against v4:** the 50-positive floor (`MIN_TEST_POS` and `MIN_REPAIR_N` 50, `N_HARD` 100, `MAX_ATT` 4,000); two new policies and four reported targets (section 5); the deployed-config switch (section 7); the three-way accounting (core 28 as headline, grounded set, quarantine set); a library-version record in the protocol file. **Every bar is the v4 bar.**
- **Run:** one GPU run, seed 49 (the next integer, chosen before any result), `kaggle/DiagRAG_v5_kaggle.ipynb`. If it is NOT_ADOPTED, that is the result and the work stops. **It has not been started. The go-ahead and the Kaggle account are the owner's decisions.**
- **Checked:** on tiny CPU settings the script runs to the end (exit 0), the protocol file records the hash, floor, deploy switch and versions, and the unchanged `analysis_gpu_plan.py` reads the output. **Not checked:** behaviour at full scale on a GPU, which is the judged run.
- **Predictions written down before the run (judgements, not guarantees):** Q03 detector FAIL; C2 PASS about 0.9; the 27-detector rule met about 0.85; U1 reaching 0.50 about 0.15; L1, L2, N1 PASS; `two_stage_0.005` misses the dispatch target.
- **What the diagnosis says about the brief's premise.** The brief expects v5 to deliver a stable verdict. Section 2 shows one fault (Q03) fails by expectation and one (C2) is a noisy pass, so a single run is one more draw, not a stability proof. I did not change any bar. The way to a clean ADOPTED is a Q03 detector that works; the probe I tried does not provide one (next section).

## 4. Workstream 3 — U1: one pre-registered probe tried and **rejected**

- Pre-registered admission test (train split only, out-of-fold, run once; `docs/evidence/probe_admission_nbr.py`, result in `probe_admission_result.json`): a neighbour-retrieval probe (one extra retrieval with the query-log nearest neighbour; three features).
  Result: the mean over the five pre-registered pairs fell from 0.941 to 0.939 and Q03-vs-rest from 0.609 to 0.598, against required rises of 0.03. Conditions (a) and (b) failed; (c) and (d) passed. **Not admitted; v5 has no probe.** Disclosed deviations: the script scored 496 pairs, not 465, and the five pairs were the least separable in v3 seed 45, not in the v4 training split used. The rejection holds on any reading.
- Two checks that removed explanations: the Q03 repair is not a no-op from query-log leakage (0 of 25 injected queries are in the log; the repair acts on 18 of 25), so its weak rescue rate is a real limit.
- **What limits U1.** Across v3 GPU, v4 CPU and v4 GPU the group-attribution rate on unseen faults is 0.40, 0.52 and 0.52, and four faults (K06, Q03, Q07, Q09) stay at or below 0.08 closure in all three runs because no repair serves them. A probe cannot add a repair. **A ceiling is not proved:** one probe family failed, and no upper bound was derived (Lemma 1 gives lower bounds only).
- Group-fallback and group-only arms stay in the reported tables as before.

## 5. Workstream 5 — the cheap guarantee: pre-registered, implemented, **not measured**

- Added to the v5 policy table: `capped_crc_0.005` (Mondrian CRC threshold raised so clean classifier dispatch is at most 20% on the calibration set; the guarantee is kept because the loss is monotone in the threshold) and `two_stage_0.005` (precise rules alone; natural rules K12 and K05 additive; the attributor at a capped threshold calibrated on the combined loss).
  Targets reported together for every policy: clean loss <= 0.5%, total clean dispatch <= 25%, clean mean cost <= 1.5, closure >= 0.80. The Mondrian and tau policies stay as controls.
- **Premise corrected before pre-registering:** the brief says the natural rules fire almost never on clean queries. On the v4 GPU training split K12 or K05 fire on **35.0%** of clean episodes (43.5% of ESCI ones) and the precise rules on 0.00%. K12 and K05 are not harmful there (on natural traffic 41 fixed, 5 broken among 718 fired), but they are dispatch. `two_stage_0.005` is therefore predicted to miss the 25% target, and `capped_crc_0.005` is the candidate that can meet all four.
- Training-split evidence for feasibility: at s >= 0.20 the attributor dispatches 10.7% of clean and 93.1% of faulted training episodes (out-of-fold).
- No held-out number exists for either policy yet.

## 6. Workstream 4 — LLM comparison: prepared and tested, **no new call made**

- No LLM key is set in this environment (`KAGGLE_API_TOKEN` only), so nothing could be run. Done instead, before any call: amendments A4 and A5 in `docs/evidence/llm_baselines_plan.md` (widen B2 to 1,000 natural queries as a prefix of the frozen md5 order; finish the Groq arms; one frontier arm with a hard USD 15 cap, key and provider from environment variables); the script extended and its SHA-256 recorded.
- **Tested without spend:** on the existing data the extended script reproduces every previously committed number (0 fields differ; the only new fields are USD columns and a `B2_first300` block equal to the committed B2). The frontier adapter (OpenAI-style and Anthropic-style), the spend cap across resumed chunks, and the no-key skip were exercised against a local mock server.
- The 700 extra natural-query inputs (ranks 300 to 999) are built (`_llm/llm_inputs_ext.jsonl`, sandbox only); none overlaps the first 300 or the exclusion list. Nothing from them has been sent to a model.
- **Needs the owner:** keys as environment variables (`GROQ_API_KEY`, `GEMINI_API_KEYS`), the frontier provider and model, prices, and the USD 15 cap set in the provider console first.

## 7. Workstream 6 — deployed config: implemented in v5, **not measured**

- `DEPLOY = {natural_typo_repair: False, injected_typo_repair: True}` with the evidence recorded in the config. The switch acts on the repair function (`rep_QLEX`), not on fault labels, because the labels Q01, Q03, Q04, Q05 and the Q fallback all apply it (amendment B3).
- **Evidence corrected before it was written into the config.** The negative point estimate holds in all five runs that measured natural-misspelling repair (-4.9 to -7.1 points), but the 95% interval excludes zero in only two (GPU seeds 46 and 48); the v3/v4 runs share one query sample. SymSpell is worse in every run.
- The v5 natural arms report the v4 behaviour as a counterfactual (`h_loop_v4cfg`, NA1d, N1v4) beside the corrected loop (NA1c, N1), so the delta from the correction is on record.

## 8. Workstream 7 — adoption groundwork: **done and verified; nothing published**

- **Staged public bench package** `release/DiagRAG-Bench_v1.0_public_STAGED.zip` (1 MB): dev episodes and labels, telemetry, test episodes without labels, `families.json`, scorer, reference baseline, datasheet, `QUICKSTART.md`, `verify_release.py`, checksums. No private labels. Verified from a clean extraction: file hashes pass, the quickstart runs in about 30 seconds, and its dev cross-validated AUROC is 0.972 (the reference baseline scores 0.976 on the private test split).
  **Release timing, the name, and the ShopNova licence are the owner's decisions;** the package says "staged, not released".
- **Reproduction path** `docs/REPRODUCE.md`: a 30-minute path that needs no GPU (verify, re-fit detectors from shipped episodes, rerun the gate diagnosis, bench quickstart) and a 2 to 4 hour path on a free Kaggle T4. The 30-minute path checks that tables follow from the shipped telemetry; it does not regenerate the episodes.
  **Found while building it:** re-fitting detectors from shipped episodes reproduces the CPU run exactly (31 of 31) but not the Kaggle GPU run (27 of 31 within 0.005; Q03 re-fits to 0.7085 against a recorded 0.6914). Library versions were not recorded, so the cause is unidentified; v5 records them (amendment B5). The recorded v4 verdict is unchanged.
- **Replication invitation and email draft** `docs/REPLICATION_INVITATION.md`: **drafted, not sent.** **Workshop draft** `paper/WORKSHOP_DRAFT.md` (about 2,000 words; page count unchecked; its numbers were verified against files and one wrong list was caught and fixed, see amendment B6). **Not submitted.**
- `verify.py` in the zip now checks the v5 code against the hash frozen in the protocol, both notebooks' embedded code, and a v5 judged folder if one is added later.

## 9. Status and what each workstream needs

| Workstream | State | Needs |
|---|---|---|
| Private labels | **done**, hash re-verified from GitHub | nothing |
| 1 Diagnosis | **done** | nothing |
| 2 v5 run | frozen, CPU-smoked, **not run** | owner: go-ahead and Kaggle account |
| 3 Probe / U1 | probe rejected; U1 unchanged | decision whether to design another probe family |
| 4 LLM arms | A4/A5 filed, script tested, inputs built, **no call made** | owner: keys as env vars, frontier provider and model, cap set in the console |
| 5 Cheap guarantee | implemented in v5, **not measured** | the v5 run |
| 6 Deployed config | implemented in v5, **not measured** | the v5 run |
| 7 Adoption groundwork | **done**, not published | owner: name, licence, release timing, whether to send or submit anything |

Other owner items: delete the throwaway Kaggle notebook `diagrag-v4-notebook-smoke`; regenerate every key that was pasted in chat; decide how to report Q03 (a known failing detector under its v3/v4 construction) since I may not change a bar.

## 10. Honest estimate

**About 7.5 out of 10, unchanged by this session.** The empirical evidence is the same as before: this session produced no new judged run. What it added is process quality and honesty about the existing record:
a diagnosis that explains the two gate flips (Q03 is a stable fail since its construction changed; C2 is a noisy pass with an unexplained component), a rejected probe reported as rejected, a reproducibility finding against our own pipeline (the GPU run cannot be re-fitted exactly because library versions were not recorded), and corrections of six statements in my own earlier text, each found by checking a number against a file.

What could move it, with my judgement of the effect (these are estimates, not measurements):
- **v5 lands ADOPTED with a capped CRC policy meeting all four targets:** a cleaner, more stable flagship and a cheap guarantee. About +0.2 to +0.3. If it lands NOT_ADOPTED, no change, and the failure is reported.
- **Frontier arm wins B1 and B2 widens to a decision:** about +0.2 (the standing objection that the judges were free-tier models is answered either way). If the frontier model is better than the diagnoser, the cost comparison becomes the claim and the effect is about zero.
- **Independent replication or use of the benchmark by another group:** the only thing that separates 8 from 8.5. It cannot be scheduled. The adoption groundwork is done so that it is possible.

So 8.0 is reachable if both runs land well; **8.5 is not something this repository can produce by itself, and 9 is not a target.** U1 at or above 0.50 would add little on its own while Q03 and the unrepaired faults remain.
Outside anyone's control here: whether others pick up the benchmark, and whether a venue accepts a paper whose headline result missed its own adoption gate.
