# v5 protocol (pre-registration). Written 16 Nov 2026, before any v5 code exists and before any v5 result.

v4's verdict (GPU seed 48: **NOT_ADOPTED**, 26/28 detectors, 27/28 repairs) stands in the record permanently. Nothing below edits a v4 gate, bar or result.
The diagnosis that motivates the changes is `docs/ROADMAP_V4.md` sections 1–2 (`docs/evidence/diagnose_gate_flips.py`, result file in the same folder).
All design changes are declared here. Any further change before the v5 run is a dated amendment (B1, B2, ...) committed before the run starts.

## 1. What is fixed (identical to v4)

- Fault set: the 28 core faults, plus R25, R26, K11, K12 reported as in v4. Core meanings of Q/K/R/C are unchanged.
- Bars: detector AUROC >= 0.70 (point estimate) on held-out data; repair: Wilson 95% lower bound of rescue >= 0.50 and <= 10% of clean successes lost; adoption: >= 27/28 detectors AND >= 24/28 repairs.
- Loop gates exactly as in `diagrag_v4.py`: L1 held-out clean loss <= 0.005 (Mondrian CRC, alpha 0.005), L2 mean closure >= 0.80, U1 unseen-fault mean closure >= 0.50, N1 paired natural-traffic gain with 95% CI lower bound > 0.
- Data, licence-clean corpus, natural-traffic exclusions (`natural_exclusions_v2.json`), census, external baselines, protocol file with the real SHA-256 of the code that ran.
- Split rule: base-query hash, as in v4. Held-out data is never used to choose anything below.

## 2. What changes (each item is declared here, before any result)

**C1. Measurement floor.** `MIN_TEST_POS` 20 -> 50 and `MIN_REPAIR_N` 20 -> 50. Hard episodes per fault `N_HARD` 100 (50 per split), attempt cap `MAX_ATT` 4,000 (v4: 50 and 2,500).
A fault that cannot yield 50 held-out positives is **THIN by construction** and is not counted as a pass. R26 is expected to be THIN (v4 yielded 5 in 2,500 attempts); it is outside the core 28.
Reason (diagnosis section 2c): n = 25 gives a standard error of about 0.06 on the AUROC; n = 50 gives about 0.043.

**C2. Cheap guarantee (Workstream 5).** Two policies are added to the policies table. The v4 policies (tau, global CRC, Mondrian CRC at five alphas, diagnosis-free universal) stay as controls and L1/L2 stay defined on `mondrian_crc_0.005`.
- `capped_crc_0.005`: per stratum, lambda = max(lambda_CRC(alpha = 0.005), lambda_cap), where lambda_cap is the (1 - 0.20) empirical quantile of s = 1 - P(NONE) on the calibration clean queries of that stratum.
  CRC risk control holds for every lambda >= lambda_CRC because the loss is non-increasing in lambda, so the cap does not weaken the guarantee. The 20% calibration cap leaves slack under the 25% target.
- `two_stage_0.005`: Stage 1 = rules, no classifier call: the precise rules (R26, R25, K11, R23, R15, K07) and the natural rules (K12, K05). Stage 2 = only if no Stage-1 rule fired: the attributor with the `capped_crc_0.005` threshold.
  The CRC calibration loss of this policy includes the Stage-1 rules' own losses on the calibration clean queries.
- **Four targets, reported together for every policy, on held-out data:** (T1) clean loss <= 0.5%, (T2) clean dispatch <= 25%, (T3) mean clean cost <= 1.5, (T4) mean closure >= 0.80.
  Clean dispatch is reported twice: total (rules + classifier) and classifier-only. **The claim uses total.**
- Known problem, measured on TRAIN-split clean episodes before writing this: the natural rules K12 or K05 fire on 35.0% of clean episodes (43.5% on ESCI queries), and the precise rules fire on 0.00%.
  The brief assumed near-zero false-fire for the natural rules. That assumption is false here, so `two_stage_0.005` is expected to **miss T2 by construction**, and the table will show the miss.
  On natural traffic those rules help (v4 GPU: 41 fixed, 5 broken among the 718 queries where they fired), so they are not a harm, but they are dispatch.
- Claim wording rule: the guarantee is stated as strongly as the best policy that meets T1–T4 together, with that policy's numbers, and no stronger. If none does, the claim is the best policy's numbers with the missed target named.

**C3. Deployed-config correction (Workstream 6).** `DEPLOY = dict(natural_typo_repair=False, injected_typo_repair=True)`, with its evidence recorded in the config: natural-misspelling repair has a negative point estimate in all five runs that measured it (-4.9 to -7.1 points, n = 185 in the four v3/v4 runs) and a 95% interval that excludes zero in two of them (GPU seeds 46 and 48: -5.4 [-10.8, -0.5]); the other three are INCONCLUSIVE. The v3/v4 runs share one natural-query sample, so they are repeated measurements of the same queries, not independent samples. SymSpell is worse in every run (-11 to -12 points, HARM).
- On natural traffic, the deployed loop drops the Q04 and Q05 repairs from both the rule stage and the classifier stage. Injected-typo repair stays on for injected traffic. Q01 and Q03 are not changed.
- The counterfactual arms NA1 (ours QLEX, SymSpell) and NA2 stay in the report as diagnostics so the harm remains on record.
- New arm **NA1c**: the deployed loop (config-corrected) on the natural queries where `q_correctable >= 1`. Reported with the paired delta and 95% bootstrap CI beside NA1. Expectation: near zero, because the harmful repair is switched off.

**C4. Probe for the least-separable pairs (Workstream 3), conditional.** One candidate probe family, **neighbour-retrieval probe**: one extra retrieval with the query-log nearest neighbour (other users' queries, the same neighbour the Q03 repair uses), giving
`nbr_cos` (neighbour similarity), `nbr_overlap` (Jaccard of the neighbour's top-5 with the original top-5), and `nbr_ce_gain` (neighbour's best cross-encoder score minus the original's).
- **Admission rule (train split only, out-of-fold, grouped by base query, 5 folds):** the probe is admitted iff all hold: (a) mean pairwise AUROC over the five least-separable pairs in `docs/IDENTIFIABILITY.md` section 4 (K04|Q03, Q03|R22, K05|R11, Q04|R13, Q03|R24) rises by >= 0.03 absolute;
  (b) the Q03-vs-rest one-vs-rest AUROC rises by >= 0.03; (c) the mean over all 465 pairs does not fall by more than 0.002; (d) fault-vs-clean AUROC does not fall by more than 0.002.
- The admission test is run once, before the v5 freeze, on the **v4 CPU seed-47 TRAIN split** (the held-out episodes of any run are never read). Its outcome is recorded in a dated amendment (B1) before the freeze. If the probe is rejected, v5 ships without it and the rejection is a reported result.
- A probe that is admitted adds three feature columns to every episode, including the natural-traffic and census rows, and costs one extra retrieval per query (cost units: counted as K-group cost 1).

**C5. Accounting (Workstream 2).** `VERDICT.json` carries all three, and the headline is (a):
(a) the 28 core faults under the original rule; (b) the grounded set (22 faults; v4 baseline 20/22); (c) the quarantine set (Q01, Q09, K03, K06, R03, R05, R06, R07, R10, C2) reported separately.

## 3. The run

- **One judged v5 run, GPU (T4, bge-reranker-large), seed 49.** Seed 49 is the next integer after the last judged seed (48). It was not chosen from any result and no run has used it.
- Settings: `SEED=49, N_BASE_ESCI=2400, N_PRDC=528, N_HARD=100, MAX_ATT=4000, N_HARM=20, TIME_BUDGET=38500`.
- If v5 is NOT_ADOPTED, that is the result. It is reported and the work stops. A v6, a second v5 run, or a re-run on another seed needs the owner's explicit approval. **Seed-shopping is tuning and is forbidden.**
- Which Kaggle account runs it, and the go-ahead, are the owner's decisions.
- Pre-registered analysis after the run: `docs/evidence/analysis_gpu_plan.py` unchanged (G, D1, D2, D3; its bootstrap seed 46 is kept for comparability).

## 4. Predictions, written down so they can fail

These come from the seven-run record and the diagnosis. They are not gates. The probabilities are my judgements from seven runs of one code family, not computed guarantees.
- **Q03 detector: FAIL, unless the probe is admitted.** The v3/v4 construction has a true AUROC near 0.645 [0.59, 0.70]; at n = 50 the chance of an observed value >= 0.70 is about 0.10.
- **C2 detector: PASS with probability about 0.9** (pooled AUROC 0.76–0.85 in every run), with an unexplained extra noise component.
- **Detector rule (>= 27/28): met with probability about 0.85** (frequency model, seven runs; rough).
- **U1 >= 0.50: unlikely without a new mechanism, probability about 0.15.** The three runs with group fallbacks gave 0.395, 0.456, 0.485. The faults with closure <= 0.08 in all three runs are Q02, Q03, Q07, Q09 and K06 (no effective repair; a probe cannot create one).
- **L1, L2, N1: PASS** (passed in every judged v3/v4 run, four of four).
- **T2 for `two_stage_0.005`: MISS** (Stage 1 alone dispatches about 35% of clean queries).
- **NA1c: |delta| small**, because the harmful repair is off.

## 5. What a result would and would not show

- ADOPTED with Q03 FAIL: the 27-detector rule is met with zero slack. It shows the 27 other detectors are stable at n = 50, and nothing about Q03.
- NOT_ADOPTED: the result is reported with the same prominence as v4's. It does not by itself say which fault flipped; the per-fault table does.
- U1 < 0.50: a fourth run under the bar. The write-up then reads U1 as bounded below 0.50 by faults that have no repair, with the closure table as the evidence.
- Nothing in v5 tests generalisation to other stacks or other domains; those are the port2, LangChain and bench arms.

## 6. Amendments

**B1 — probe admission test made resumable (16 Nov 2026, 06:58 UTC; made before any probe number existed).**
The first launch of `docs/evidence/probe_admission_nbr.py` (SHA-256 `8e9b11ac…d647`, committed as `5d751d4`) was killed by the sandbox when its tool call returned, after printing only "probe features 0/2681". No probe feature, AUROC or condition was computed or read.
The script now caches its probe features and pair AUROCs to disk and stops at a time budget so it can be resumed across tool calls. **The probe features, the five pairs, the folds, the models, the thresholds and the four admission conditions are unchanged.**
Script SHA-256 after B1: `9ea82bd189dca9303a4e6009b73da87d4bfbc4fd6f67223891293bbb44d6c077`.

**B2 — outcome of the pre-registered probe admission test (16 Nov 2026, 07:21 UTC). The neighbour-retrieval probe is REJECTED. v5 ships without it.**
Run: `docs/evidence/probe_admission_nbr.py` (SHA-256 `9ea82bd1…c6077`), v4 CPU seed-47 TRAIN split only (2,681 single-fault and clean episodes, out-of-fold, grouped by base query, 5 folds). Result file: `docs/evidence/probe_admission_result.json`.

| Condition | Required | Measured | Verdict |
|---|---|---|---|
| (a) mean pairwise AUROC over the five least-separable pairs | rises by >= 0.03 | 0.9411 -> 0.9386 (-0.003) | **fail** |
| (b) Q03-vs-rest AUROC | rises by >= 0.03 | 0.6086 -> 0.5980 (-0.011) | **fail** |
| (c) mean over all pairs | falls by no more than 0.002 | 0.9805 -> 0.9797 (-0.0008) | pass |
| (d) fault-vs-clean AUROC | falls by no more than 0.002 | 0.9730 -> 0.9721 (-0.0009) | pass |

- **Two deviations from the frozen text, both disclosed here.** (1) The protocol said "all 465 pairs"; the script scored 496, because it included the clean class (32 classes). Conditions (a) and (b) fail by a wide margin on any reading. (2) The five pairs named in C4 were the least separable in the **v3 seed-45** train split. In this **v4 seed-47** train split their baseline AUROCs are 0.89 to 0.98 (K04|Q03 0.968, Q03|R22 0.891, K05|R11 0.966, Q04|R13 0.984, Q03|R24 0.896), so they are no longer the five lowest. I kept the pre-registered five.
- **What this shows.** One probe family, built from the same neighbour the Q03 repair uses, adds no separation for Q03 on the training split. Q03-vs-rest stays near 0.60 (the v3/v4 held-out era mean is 0.645, ROADMAP_V4 section 2b).
  **It is not a proof of a ceiling.** Lemma 1 gives lower bounds on distances; no upper bound was derived. Other probes are untested.
- **Consequence for v5.** No probe features. The v5 prediction for U1 (section 4, about 0.15 chance of reaching 0.50) stands unchanged, and the Q03 detector is expected to FAIL.
- Two earlier checks, on TRAIN data only, are also recorded: the Q03 repair is **not** a no-op from query-log leakage (0 of 25 injected queries are in the log; the neighbour differs from the query in 25 of 25 cases and the repair acts on 18 of 25), so its weak rescue rate is a real limit and not an artefact.

**B3 — three corrections to this protocol, made before any v5 code or result existed (16 Nov 2026, 07:40 UTC).** Found by re-reading section 2 against `diagrag_v4.py`.
1. **L2 bar.** Section 1 says L2 is "mean closure >= 0.80". That is wrong. v4's frozen bar is `L2_BAR = 0.70` and it stays 0.70 for L2. The 0.80 in section 2 C2 (target T4) is a **new target for the policy table only** and does not change L2.
2. **Natural rules are additive, not preemptive.** C2 said Stage 2 runs "only if no Stage-1 rule fired", with the natural rules (K12, K05) in Stage 1. Those rules fire on 35% of clean queries and also on many faulted ones, so letting them skip the classifier would discard true repairs and make T4 unreachable by construction.
   Corrected definition of `two_stage_0.005`: Stage 1a = the precise rules (R26, R25, K11, R23, R15, K07; 0.00% false-fire on train clean); if one fires, it is the only repair, as in v4. Stage 1b = the natural rules K12 and K05, applied **in addition** when they fire, as in the deployed natural loop.
   Stage 2 = the attributor at the capped threshold, applied after Stage 1b. Calibration loss per clean query at threshold lambda is `lost_nat` if the classifier does not dispatch and `max(lost_nat, lost_combined)` if it does. This is non-increasing in lambda, so conformal risk control stays valid, and it includes the natural rules' own losses. It never credits the classifier for repairing a loss caused by a natural rule.
3. **C3 acts on the repair function, not on labels.** In the code the labels Q01, Q03, Q04, Q05 and the Q-group fallback `GQ` all apply the same function, `rep_QLEX` (the family repair). Dropping only the Q04 and Q05 labels would change nothing.
   The deployed natural loop therefore does not apply `rep_QLEX` at all (`DEPLOY['natural_typo_repair'] = False`). This also removes the family repair from the classifier path on natural traffic. Evidence on that path (v4 GPU seed 48, 668 natural queries where the classifier dispatched a Q-group repair): Hit@5 0.501 to 0.503, 5 fixed and 4 broken, so removing it costs nothing measurable and saves its cost.
   Both loops are reported on the natural queries: `h_loop` (v5 deployed config) and `h_loop_v4cfg` (v4 behaviour as a counterfactual), so the delta from the correction is on record. NA1c compares them on queries with `q_correctable >= 1`.

**B4 — v5 code frozen (16 Nov 2026, 08:35 UTC; no v5 judged run exists).**
`kaggle/diagrag_v5.py` is generated from `kaggle/diagrag_v4.py` by `kaggle/mk_v5.py` (25 exact, asserted replacements; `diff v4 v5` shows them). SHA-256 **`bf43658f1c9bab175bdf992647a08d238820dc413b06ebd7d4359c646765591b`**.
Code checks done before this freeze, all on a tiny CPU smoke run (the numbers from it are meaningless and are not reported): the script runs to the end with exit 0; the protocol file records this hash, floor 50 and the deploy switch;
`VERDICT.accounting` carries (a), (b) and (c); the policy table carries the two new policies with T1 to T4; natural arms NA1c, NA1d and N1v4 are present; the unchanged pre-registered `analysis_gpu_plan.py` reads the output.
Not checked: behaviour at full scale on a GPU (that is the judged run itself).
Nothing in the protocol's gates or bars changed in B1 to B4 except as stated there. The judged run is one run, GPU, seed 49, settings in section 3, and waits for the owner's go-ahead and the choice of Kaggle account.

**B5 — the protocol file now records the software environment; v5 hash replaced (16 Nov 2026, 10:05 UTC; still no v5 judged run).**
Reason, found while building the reproduction script (`kaggle/reproduce_tables.py`): re-fitting the detectors from a run's shipped `episodes.jsonl` reproduces the **CPU** run (v4 seed 47) exactly, 31 of 31 AUROCs, largest difference 0.0000.
For the **Kaggle GPU** run (v4 seed 48) it differs for 4 of 31 faults: K12 +0.015, Q03 +0.017 (recorded 0.6914 FAIL; re-fit 0.7085, above the bar), R03 -0.041, R06 +0.017. The head does not depend on its model seed (AUROC identical over five seeds), so this is a library or numerical-path difference on Kaggle's stack, not seed noise.
The seed-48 protocol file recorded the code hash but **no library versions**, so the cause cannot be identified from the files. The v4 verdict is unchanged and stays NOT_ADOPTED as recorded.
Change: `JUDGED_PROTOCOL.json` gains an `env` block (Python, platform, numpy, pandas, scipy, scikit-learn, torch, transformers, sentence-transformers, faiss, nltk, CUDA, GPU name). No gate, bar, sample or computation changes.
Checked: a short CPU run starts, writes the `env` block and its `code_sha256` equals the file hash.
**This supersedes the SHA-256 in B4.** The frozen v5 hash is now `deecafad69b49c5ae87ee7031f23d24553ea092cf390b964859dbae81091702a`.

**B6 — correction of a factual error in section 4 (16 Nov 2026, 11:10 UTC; no v5 run exists).** Section 4 says the faults with closure <= 0.08 "in all three" group-fallback runs are Q02, Q03, Q07, Q09 and K06. Recomputed from `unseen_faults.csv` of v3 GPU seed 46, v4 CPU seed 47 and v4 GPU seed 48, the set is **K06, Q03, Q07 and Q09**.
Q02 has closure 0.16 in v3 GPU and 0.00 and 0.04 in the two v4 runs, so it is not in the set. The v4 runs alone (seeds 47 and 48) give Q02, Q03, Q07, Q09 and K06 (plus R06 in seed 48). The prediction that U1 will be below 0.50 is unchanged. No gate or bar is affected.
