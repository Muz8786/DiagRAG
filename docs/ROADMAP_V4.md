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

---

# 11. Update, 17 Nov 2026 — the v5 judged run, and the A-venue programme item by item

This section supersedes the "not run" statuses in sections 3, 5, 7 and 9 above (those texts are left as written).

## 11.1 The v5 judged run: **NOT_ADOPTED** (CPU stack, seed 49)

Why CPU: the only Kaggle credential in the environment is rejected with HTTP 401 (same answer as a made-up token), consistent with the owner regenerating keys. Amendment B7 in `docs/evidence/v5_protocol.md`, committed before the run, moved the single judged run to the CPU stack.
Seed 49 and every setting were unchanged. Code `kaggle/diagrag_v5.py`, SHA-256 `deecafad69b49c5ae87ee7031f23d24553ea092cf390b964859dbae81091702a`, equal to the hash recorded in the run's `JUDGED_PROTOCOL.json`. The protocol file also records the library versions (scikit-learn 1.9.1, numpy 2.4.6, torch 2.15.0+cpu, Python 3.11.15).
Output committed whole: `kaggle/judged_cpu_run_v5_seed49/`. The run took six 25-minute chunks.

| Accounting (pre-registered; headline is a) | Detectors | Repairs | Solved both | Not solved |
|---|---|---|---|---|
| **(a) core 28, original rule** | **24** (27 needed) | 27 (24 needed) | 24 | Q03; R03, R15, R22 (THIN) |
| (b) grounded set (22 faults) | 18 | 20 | 18 of 22 | Q03, R15, R22, R26 |
| (c) quarantine set (10 faults) | 9 | 10 | 9 of 10 | R03 |

Loop gates: **L1 PASS** (held-out clean loss 0.15%, bar 0.5%); **L2 PASS** (closure 0.833, bar 0.70); **U1 FAIL** (0.440, bar 0.50; grounded 0.408; without group fallback 0.254); **N1 PASS** (+2.43 points [+1.70, +3.22], 42 fixed, 2 broken, n = 1,648).
Pre-registered GPU-plan analysis on this run: D1 PASS (closure 0.833 against 0.755 for diagnosis-free, clean loss 0.15% against 1.49%); D2 **FAIL** (loop minus universal +0.24 points, CI lower bound -0.61, which is below the -0.50 margin; cost 5.16); D3 **PASS** (+0.61 points [+0.06, +1.15], the first run where detection gating beat always-on K12 with the interval above zero).

**Why the detector count is 24, stated in full.** Q03 fails for the reason section 2b gives (AUROC 0.640 [0.571, 0.714], n = 50). The other three are not detector failures: R03, R15 and R22 have held-out AUROC **1.000, 0.988 and 0.968** and are marked THIN because they produced only **38, 44 and 47** held-out positives, below the 50-positive floor that v5 itself introduced.
The cause is in the generator, not the detectors: the loop stops at `ptr < 4 * len(pool)`, and once the train quota (50) fills, every remaining train-split pool entry is skipped but still consumes `ptr`, so the smaller test half starves. These three faults have the lowest yields (7 to 9%) and about 1,520 of roughly 2,700 attempts were "not applicable".
**Disclosed counterfactual, not a verdict:** under v4's floor of 20 positives these three detectors would pass, giving 27/28 detectors and an ADOPTED verdict by the original numbers. I am not entitled to re-adjudicate with a bar chosen after seeing the result, and the verdict stands as NOT_ADOPTED. A fix (count quota skips separately, or bound the loop by attempts only) belongs in a v6 that needs the owner's approval.

**Prediction scorecard** (section 4 of the protocol, written before the run; the GPU-stack predictions were kept as written):

| Prediction | Outcome |
|---|---|
| Q03 detector FAIL | **correct**: 0.640 FAIL |
| C2 detector PASS (about 0.9) | **correct**: 0.785 PASS, n = 50 |
| 27-detector rule met (about 0.85) | **wrong**: 24. I did not foresee the floor-versus-generator interaction; three of the four misses are THIN, not FAIL |
| U1 >= 0.50 (about 0.15) | **correct** that it would not: 0.440 FAIL |
| L1, L2, N1 PASS | **correct** |
| `two_stage_0.005` misses the dispatch target | **correct**: total clean dispatch 41.1% (classifier-only 15.6%) |
| NA1c small | **correct**: +0.54 [0.00, +1.62] |

## 11.2 The programme's seven attacks, in the brief's order

**#1 "Your flagship run is NOT_ADOPTED." Not closed. Two judged runs in a row (GPU seed 48, CPU seed 49) missed the adoption rule.** The honest reading is split: seed 48 missed on Q03 and C2 (C2 explained below); seed 49 missed on Q03 plus three THIN detectors caused by my floor.
The A plan's fallback applies: the identifiability result becomes the headline and the suite verdict a reported limitation (all-runs matrix: `docs/ALL_RUNS_MATRIX.md`). A GPU replication of v5 was not possible.

**§3 C2: resolved.** `docs/evidence/c2_decomposition.py` and its result file. All 50 C2 positives are ESCI, tenant ALL, k = 5, so source, tenant and k cannot explain anything. **The construction feature is the fault-pair mix:** the generator draws one of 12 pairs at random, about four per type per run; six pair types have almost no second-group mass because the first fault masks the second (Q03+R05, Q04+K05, Q04+R10, K04+R24, Q05+R24, K04+R03; mean score below 0.05).
In seed 48 the test split's composition sat at the 5th percentile of random splits, and the 25 test positives scored far below the 25 train positives under the same head (medians 0.002 and 0.136, Mann-Whitney p = 0.003). With composition held fixed the test AUROC is still low (0.631, below 98.7% of 4,000 within-pair-type re-splits, p = 0.013), but the probability that the worst of seven runs reaches that is 8.6%, so the residual is consistent with chance. In v5 (n = 50, CPU) C2 passes at 0.785.
**Verdict: a construction artefact (unbalanced pair mix per split) plus ordinary small-n variance.** Not fixed in v5, because v5 was frozen; a stratified pair assignment belongs in v6.

**§3 Q03: the identifiability exhibit.** Q03 detector AUROC by construction era (inverse-variance means, 95% CI):

| Era | Runs | AUROCs | Mean [95% CI] | Heterogeneity within era |
|---|---|---|---|---|
| injected synonym swap | seeds 42, 43, 44 | 0.866, 0.934, 0.877 | **0.912 [0.874, 0.950]** | Q = 2.42, df 2, p = 0.30 |
| real query pairs from other users | seeds 45 to 49 | 0.559, 0.654, 0.704, 0.691, 0.640 | **0.643 [0.600, 0.687]** | Q = 4.40, df 4, p = 0.35 |
| all eight | | | | Q = 89.7, df 7, p = 1.5e-16 |

The era difference is 0.268 (z = 9.1). Within the real-pair era one run in five passed. **The upper end of the real-pair interval (0.687) is below the 0.70 bar**, so under that construction the telemetry detector is not expected to meet its bar. The injected and the natural paraphrase task are different problems.

**#2 "Your unseen-fault claim fails its own bar." Not closed, and no proved ceiling.** Route A (inside v5): U1 = 0.440, FAIL. Route B (`docs/evidence/route_b.py`, amendment B8, train split only):
- **Pairwise table, rigorous:** over the 465 pairs of the 31 single faults in the v5 training split, 98.1% have out-of-fold AUROC at least 0.95 and none is below 0.80; the median certified total-variation lower bound is 1.00. The least separable pair is **K04|Q03 at 0.875 [0.811, 0.945]**, then K04|R07 (0.926), R05|R13 (0.927), K06|R05 (0.932) and Q07|R13 (0.937). Q03 is in the least-separable pair, consistent with its detector result.
- **The brief's aggregate, as a diagnostic:** 35% of faults have their nearest confusable partner in the same repair group, 65% in another. Read as a bound that would cap U1 near 0.35. **The measured U1 values (0.44 to 0.49) exceed it, so the assumption that an unseen fault is routed like its nearest confusable partner is falsified by the data, and this is not a ceiling.**
- **Oracle-group closure** (closure if the group were always right), from the four runs with group fallbacks: 0.583, 0.666, 0.685 and 0.572, all above 0.50. The mean right-group rate is 0.40, 0.52, 0.52 and 0.58. So the shortfall is mostly group attribution, and a ceiling below 0.50 cannot be derived from repair quality either.
- **Conclusion: neither route closes the attack.** The paper cannot claim "the bound, not the bar". It can claim: unseen-fault closure is limited by group attribution (about 0.5 to 0.6) and by four faults with no effective repair (K06, Q03, Q07, Q09 in the earlier runs); no ceiling is proved; the identifiability table is the rigorous result. The failed neighbour-retrieval probe is the one-paragraph companion.

**#3 "Your guarantee costs 90% dispatch." Closed, with a measured frontier** (`docs/ALL_RUNS_MATRIX.md`, v5 CPU seed 49; held-out clean queries):

| Policy | Clean loss | Total clean dispatch | Mean cost | Mean closure | Meets T1 to T4 |
|---|---|---|---|---|---|
| tau at 5% false alarm (no guarantee) | 0.07% | 2.1% | 0.11 | 0.837 | yes |
| global CRC 0.005 | 0.15% | 14.1% | 0.98 | 0.872 | yes |
| Mondrian CRC 0.005 (the L1 gate) | 0.15% | **89.2%** | 3.66 | 0.833 | no (dispatch, cost) |
| **capped CRC 0.005** | **0.07%** | **15.6%** | **0.96** | **0.821** | **yes** |
| two-stage 0.005 | 0.37% | 41.1% (classifier 15.6%) | 1.91 | 0.782 | no (dispatch, cost, closure) |
| diagnosis-free universal | 1.49% | 100% | 12.00 | 0.755 | no |

Finding: the 89% dispatch is not the price of the guarantee. The stratified threshold is simply the *smallest* one the loss bound allows, so it dispatches almost everything in the common stratum. **Capping dispatch at 20% on the calibration set keeps the loss bound (the loss is monotone in the threshold) and costs 1.2 points of closure (0.833 to 0.821) while cutting dispatch from 89% to 16% and cost from 3.66 to 0.96.** The claim rule picks `capped_crc_0.005`.
Note the single-threshold `global_crc_0.005` already met all four targets (in v4 GPU too: 12.1% dispatch, closure 0.871), so the improvement is in the *per-stratum* guarantee, not in having any guarantee. The two-stage policy misses, as predicted, because the natural rules K12 and K05 fire on about 35% of clean queries (they help on natural traffic: 41 to 45 fixed, 2 to 5 broken). That is a finding about natural traffic.

**#4 "You beat free-tier LLMs; so what." Not closed.** No LLM key is set (`GROQ_API_KEY`, `GEMINI_API_KEYS`, `FRONTIER_API_KEY` all absent), so no call was made. Amendments A4 and A5 are filed, the script is tested against a mock server, and the 700 extra natural inputs are built. Needs keys from the owner.

**#5 "One corpus." Not closed.** The existing ports (FiQA 19/20, SciFact 15/20) remain. A full-suite FiQA port was not built: 9 of the core 28 are absent from the port (Q02, Q07, Q09, K03, K06, K07, K09, R06, C2), and several cannot exist on FiQA by construction (Q07 needs product codes, K07 needs tenants, K09 and K03 need versioned or sibling documents). The honest design is to port what can exist, list what cannot as structurally absent, and not count absent faults as failures.

**#6 "Artefact?" Staged, not released.** `release/DiagRAG-Bench_v1.0_public_STAGED.zip`: verified from a clean extraction (hashes, quickstart, scorer). The name, the ShopNova licence and the release date are the owner's.

**#7 "Can I trust any of this?" Done in the repository.** The all-runs matrix is generated (`docs/ALL_RUNS_MATRIX.md`, 8 judged runs plus a GPU row marked "not run"); every amendment is dated; six statements in my own earlier text were corrected after checking them against files; the limitations are written in `PROJECT_EXPLAINED.md` section 12.

## 11.3 Honest estimate after the v5 run

**About 7.5 out of 10. The v5 run did not raise it, and the programme's target of 8.0 to 8.2 is not reached.** What moved: a measured guarantee frontier (the strongest new result), a resolved C2 question, a rigorous Q03 identifiability exhibit with five runs in the real-pair era, a fifth natural-traffic measurement (+2.43), D3 passing for the first time, and a reproducibility record.
What did not: the adoption gate was missed again (24/28, three of the misses caused by my own floor), U1 stayed below its bar with no ceiling proved, and the frontier LLM arm, the full FiQA port and the bench release did not happen. A reviewer will see two NOT_ADOPTED runs in the matrix; the explanation is written, but it does not make them pass.
**What would move it to about 8.0:** a v6 with the generator fix (owner approval), a GPU replication with a valid token, the frontier LLM arm with the owner's keys, and a full-suite FiQA port. **8.2 and above is not reachable by this repository alone.**

---

## 11.4 Correction (17 Nov 2026): the mechanism behind v5's three THIN detectors was misdiagnosed

Sections 11.1 and `PROJECT_EXPLAINED.md` 5.2 say the three THIN detectors (R03, R15, R22) came from a generator loop whose pointer budget was consumed by skipped entries, and that "count quota skips separately" is the fix. **That fix would not work, and the explanation is incomplete.** I found this by simulating the proposed fix, which did not reproduce the failure, and then reading the stored generation state:
- The pointer did reach its bound (5,228 = 4 x 1,307) at only 2,617 to 2,717 attempts, as stated. That fact stands.
- But for R03, R15 and R22 the injector is **deterministic** (for example `enc='v15_trunc'`), so a second attempt on the same base query reproduces the same episode, is caught by the duplicate signature and counted "not applicable" (56%, 58% and 57% of attempts). These three faults have **zero** base queries with two hard episodes, while R10 (random noise) has 11.
- So each base query yields at most one episode for these faults, and only 7.4%, 8.6% and 8.5% of queries are hard. One pass over the whole pool would give about 96, 112 and 111 hard episodes in total, and about **39, 46 and 45 in the test half** (the test half has 872 ESCI queries against 1,528 for train). v5 obtained 38, 44 and 47.
- **Conclusion: the 50-positive floor is not reachable for deterministic low-yield faults with this base-query pool.** The limit is supply of distinct test queries, not the loop. A fix has to change supply (more base queries, or a larger test fraction), which is a different design change from the one drafted.
`diagrag_v6.py` as first drafted (loop-budget fix plus C2 pair balancing) was **discarded before any run** and is not in the repository.


---

# 12. Update, 17 Nov 2026 (later): v6 ADOPTED, the LLM arms complete, the reproducibility gap identified

Execution detail and the prediction scorecard are in `docs/evidence/v6_protocol.md` (C1 to C5) and `docs/evidence/llm_baselines_plan.md` (A6, A7). This section supersedes the "not run" and "open" statements in sections 11.1 to 11.3 where it says otherwise.

## 12.1 v6: the pre-registered flagship is ADOPTED (GPU), and so is the CPU replication
- Why v6: the corrected v5 diagnosis (section 11.4) is supply of distinct test queries. v6 changes only that (all 5,527 examined ESCI bases, `N_BASE_ESCI` 6,000) and balances C2's pair mix inside each split. A first v6 draft (a loop-budget fix) was discarded before any run after a simulation showed it would change nothing; a first version of the C2 balancing rule was caught by a unit test (a never-yielding pair blocked all others) and fixed before any compute.
- **GPU (Kaggle T4, seed 50): 27 detectors / 27 repairs, ADOPTED.** Only Q03 is not solved (detector 0.642). L1 PASS 0.28%, L2 PASS 0.844, **U1 FAIL 0.406**, N1 PASS +2.18 [+1.33, +3.03]. `kaggle/judged_gpu_v6_seed50/`.
- **CPU replication (same seed): 28 / 27, ADOPTED**; Q03's detector passed at 0.701. L1 0.20%, L2 0.854, U1 0.413, N1 +2.43 [+1.70, +3.22]. `kaggle/judged_cpu_run_v6_seed50/`.
- R03, R15 and R22, THIN in v5, reached 50 held-out positives on both stacks and passed (0.95 to 1.000): the supply diagnosis is confirmed by a prediction that could have failed.
- `capped_crc_0.005` met all four targets on both stacks (GPU: loss 0.12%, dispatch 16.5%, cost 0.93, closure 0.834). `global_crc_0.005` broke the 0.5% loss bound on both (0.56%, 0.60%).
- Predictions wrong: Q03 passed on CPU (0.701, predicted fail at 0.9). U1 got worse, not better.
- **Process notes.** The GPU job first sat QUEUED for two hours on one account; I deleted it unexecuted and pushed the same notebook (same SHA-256 prefix) to another account where it ran (amendment C4). A tiny GPU smoke of the same notebook had passed first.

## 12.2 LLM arms: all three free-tier arms are complete (amendments A6, A7)
- B1 (diagnosis, n = 320 each): OURS_BETTER in every arm. Gemini 3.1 Flash-Lite 0.754 (ours minus LLM +0.222 [+0.173, +0.270]); gpt-oss-120b 0.701 (+0.274 [+0.222, +0.332]); gpt-oss-20b 0.629 (+0.347 [+0.292, +0.402]).
- B2 (repair): Gemini on **1,000** natural queries, loop minus CRAG-style **+1.23 points [-0.10, +2.60]: OURS_NON_INFERIOR** (not "better"); first-300 sample unchanged at +0.66 [-1.33, +2.67] INCONCLUSIVE. Groq arms, now complete on 300 queries: INCONCLUSIVE (+1.32 [-0.67, +3.67]; +0.98 [-1.33, +3.33]).
- The first Gemini key hit its 500-requests-per-day quota; a second key resumed the same arm (A7) with the same model and prompts.
- **No frontier arm.** The Gemini key's Pro-class models returned quota or availability errors; `gemini-4-hydrogen` answers at 28 to 51 s per call. The A4.3 arm is not run, and the "only free-tier judges" objection is not answered.
- A process lesson: the first B2 verdicts for Groq read NOT_ANALYSABLE because rewrite calls are queued from grades present at the start of a chunk, so a single chunk left them unfinished (not a quota failure). Finishing the pending rewrites, which is deterministic and does not depend on any outcome, changed them to complete arms.

## 12.3 The reproducibility gap is identified and fixed
Re-fitting under the library versions Kaggle recorded (scikit-learn 1.6.1, numpy 2.1.3) reproduces the v6 GPU run's detectors exactly (31 of 31, largest difference 0.0000), and also the v4 seed-48 and v3 seed-46 GPU runs (31 of 31 each) and the v4 C2 head (0.6116). Under scikit-learn 1.9.1 the same data gives 27 or 28 of 31. The cause is the library version; the v4 verdict is unchanged. `requirements_kaggle_gpu.txt` ships the versions.

## 12.4 Honest estimate after v6
**About 7.8 out of 10.** Not 8.3 to 8.5. The flagship is now ADOPTED on the GPU stack with a CPU replication, the LLM comparison is complete, and the guarantee frontier holds on two stacks. Still open: U1 (0.41), a frontier-model arm (no key), a full-suite second-corpus port (not attempted), the benchmark release (owner decisions). I estimate about 8.2 if the last three of those close well; 8.5 needs outside adoption.

# 13. Update, 17 Nov 2026 (latest): the composed-fault arm (v7) and the optional QML comparison

Execution detail, the freeze and the scorecard are in `docs/evidence/v7_composed_protocol.md` (D1 to D4) and `docs/evidence/qml_protocol.md` (Q1). The full write-up is `PROJECT_EXPLAINED.md` sections 5.9 and 5.10. Both pieces are descriptive: no adoption gate, and the QML models are simulated with no advantage claim.

## 13.1 v7: composed faults
- **Design.** Fault pairs (within-family, within-letter QQ/KK/RR, cross-letter QK/QR/KR) and triples are injected; an episode is kept only if the clean query succeeds and the composed one fails, with the alone-failure record of each component. 155 train and 155 held-out episodes, every stratum at quota; seed 51; splits by base-query md5; no base query shared with any single-fault episode. Code hash frozen and committed before generation.
- **Result (held-out, n = 155).** Every cause named at the family level: **40.0% [32.6, 47.9]** (old attributor 30.3%). By stratum: 0/75 for QQ, KK, RR and TRIPLE (the dispatcher returns at most one label per letter group), 45% QK, 85% QR, 80% KR; WITHIN_FAMILY 20/20 by construction (shared family label). Mean set-F1 0.770 (old 0.713). Sequential repair closure **72.9% [65.4, 79.3]** against 83.9% for oracle-forward repairs. Forced reverse order: no difference in closure (25/32 under both orders; oracle-forward and oracle-reverse closure agree in 155 of 155 episodes; in a direct check on 60 episodes the repaired states differed in 2). Held-out clean loss 0.16%; sequential loop on 300 clean queries 0.3% [0.1, 1.9].
- **No regression.** The attributor was retrained with composed rows (train split only) and every single-fault gate re-run: 28/27/27, ADOPTED, L1, L2, N1 PASS, `capped_crc_0.005` meets all four targets, U1 unchanged at 0.413. Differences reported in D4 (C2 AUROC 0.823 to 0.848; capped-CRC closure 0.848 to 0.838).
- **Scorecard.** Held: both-cause rate 0.2 to 0.5 and low within a letter; retraining adds up to 0.1 (+0.097); no regression. Did not hold: closure gap of at least 0.2 (observed 0.11); reverse order lowers some strata; strata short of quota.
- **Execution record.** After the freeze (D1) the run needed two execution fixes, both disclosed: D2 (detection-baseline rows kept under `id(e)` could not resume) and D3 (about 9,000 single-row attributor calls at 0.061 s each pushed the stage past the chunk wall clock; replaced by one batch call with a 1e-9 equality check). D2's diagnosis was incomplete and D3 corrects it. The composed result is byte-identical before and after both.

## 13.2 QML (optional, simulated)
Six-qubit noiseless statevector simulation written in the repository; quantum-kernel SVM and a variational classifier against classical models on the same six PCA inputs and the 63-feature gradient boosting. Single-fault AUROC 0.892 and 0.883 (quantum) against 0.917 and 0.921 (classical, six inputs) and 0.978 (63 features); composed-versus-clean 0.942 and 0.965 against 0.979 and 0.988 and 0.995. Three of four predictions held. **No quantum advantage; none is claimed.**

## 13.3 Honest estimate after v7
**About 7.8 out of 10, unchanged.** The composed arm is a new, pre-registered, partly negative measurement with a no-regression proof; it gives a reviewer something new to read and a clear next step (a dispatcher that returns several labels per letter group). It does not close U1, the frontier-model comparison, the second corpus or the release, and it is 155 synthetic episodes from one seed. 8.3 to 8.5 is not supported by the evidence.
