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
