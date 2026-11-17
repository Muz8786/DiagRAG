# v7 composed-fault arm: protocol (pre-registration). Written 17 Nov 2026, before any composed episode of the real run was generated.

The smoke test of the code on tiny settings (700 base queries, 10% quotas) was run during development and is **not** the real run; its numbers are not used anywhere. Everything below is fixed before the real run starts.

## 0. Question and scope
Real retrieval failures often have more than one cause. The single-fault arms of v1 to v6 measure one injected fault at a time (plus one 12-pair "C2" arm). This arm asks, using **only the project's existing detectors, repairs and dispatcher**, what happens when two or three faults from the grounded and solved set act at once.
It is **descriptive**: no adoption gate, no pass or fail bar for any composed quantity. It adds no new detector and no new repair.

## 1. What is composed
- **Eligible faults (20):** grounded (tier S or M) and solved in the v6 judged runs: Q02, Q04, Q05, Q07, K04, K05, K07, K08, K09, R01, R11, R13, R15, R19, R22, R23, R24, R25, K11, K12.
  Excluded, with reasons logged in the result: Q03 (grounded, detector and repair FAIL in v6), R26 (grounded, THIN), every quarantine-tier fault (N or P), and C2 (itself a composition).
- **Strata** (a stratum is a rule for which faults may be paired; the pair itself is chosen inside it):
  `WITHIN_FAMILY` (both faults in the same repair-equivalence family), `QQ`, `KK`, `RR` (different families, same letter), `QK`, `QR`, `KR` (different letters), `TRIPLE` (one Q, one K, one R fault).
  In the eligible set the within-family stratum has one combination (Q04 with Q05); the STALE and ENC families have fewer than two grounded solved members, so no further within-family pairs exist (reported as a fact, not as an exclusion).
- **Source pools:** a combination is allowed only on base queries whose source is accepted by every component (`POOL`); combinations with an empty intersection are excluded and listed with the reason.
- **Composition rule:** query faults chain on the evolving query (Q-letter first); K and R faults act on the original base query; faults that set the same configuration knob to different values are a conflict and the combination is excluded for that episode (reason logged); the success depth is the stricter of the components'.

## 2. Episodes
- **Seed 51; quotas per split and stratum:** 20 kept episodes for each of WITHIN_FAMILY, QQ, KK, RR, QK, QR, KR and 15 for TRIPLE (155 per split, 310 in total).
- **Keep rule:** an episode is kept only if the clean pipeline succeeds on the base query **and** the composed state fails. Every other attempt is logged under its reason (easy, conflict, not applicable, duplicate, no combination for the source).
- **Single-alone record:** for every kept episode each component is also run alone (the same injector with the same random seed on the original base query) and the result is stored: all components fail alone, some do, none do (an emergent failure), or unknown (a component could not be built alone).
- **Splits and overlap:** each base query keeps its v6 split (an md5 of its gold-product component, so no gold product is shared between splits). A base query is used **at most once** in the composed arm and **never** if any single-fault episode of the same run uses it, in either split. The overlap count and the number of base queries with a failing clean pipeline are reported per split.
- **Order:** base queries are visited in md5 order of `seed|order|base-query-id`; the stratum with the lowest fill fraction is served first; inside a stratum the combination with the fewest kept episodes (then fewest attempts) is used, and a combination with 12 attempts and no kept episode is treated as stuck.
- The composed episodes are stored in their own list. They never enter `EPIS`, so the single-fault arms, their gates, the calibration and the natural-traffic arms never see them.

## 3. The diagnoser and what is measured (held-out composed episodes only)
- **Diagnoser:** the project's own `dispatch_v3` (precise rules, family-first attribution, group fallbacks) with the attributor from either version. **ATT0** is the v6 attributor (single-fault rows). **ATT** is the v7 attributor: the same model class and settings fitted on the single-fault training rows plus the composed **train-split** rows, one row per component labelled with that component. The group attributor is retrained the same way. The classes are unchanged.
- **Cause named (primary, family level):** a non-fallback label equal to the fault, or in its repair-equivalence family. **Secondary (group level):** any label, fallbacks included, in the cause's letter.
- **Measure 1, both-cause detection:** the share of episodes whose diagnosed set names every cause (family level; the group level is reported beside it). Also reported: the share naming at least one cause.
- **Measure 2, set-F1:** per-episode F1 between the diagnosed label set and the true cause set at the family level (precision counts a label as correct if it names some true cause); mean over episodes, with the group-level mean beside it. For triples the dispatcher can name at most two causes, so recall below 1 is expected.
- **Measure 3, sequential-repair closure:** repair, re-run, re-extract telemetry, re-diagnose, repair again, at most three rounds, gated by the L1 threshold of the query's stratum (`mondrian_crc_0.005`, calibrated on clean TRAIN queries scored by the same attributor). The loop never sees the gold. It stops when the score falls below the threshold, or when the diagnosis repeats a label already applied. Closure is the share of held-out composed episodes whose gold is in the top-k after the loop.
  **Forced reverse-order subsample:** a fixed 25% of the held-out episodes (md5 of `seed|rev|base-query-id` below 0.25) are also run with the first repair forced to be the other cause's (the second label if the diagnosis listed two; otherwise the best label outside the top group; if neither exists the episode is counted as not applicable for the reverse test, and both the all-episode and the applicable-only figures are reported).
  Beside them: **oracle-forward** and **oracle-reverse** closure (the true components' own repairs applied in Q, K, R order and in the reverse order; an upper reference for the repairs, not a diagnoser).
- **Measure 4, held-out clean loss, unchanged do-no-harm accounting:** (a) the v6 L1 figure for the retrained attributor on all held-out clean episodes under `mondrian_crc_0.005`, recomputed exactly as before (bar 0.5%); (b) the same loop used for composed episodes (up to three rounds) on a fixed 300-episode held-out clean subsample, reporting the Hit@5 lost.

## 4. Retraining, and the proof of no regression
- The v7 script resumes the v6 CPU judged run's checkpoint with **every attributor-dependent result discarded and recomputed** (the attributor, thresholds, calibration, the closed loop, natural traffic, leave-one-fault-out, detection baselines); the single-fault episodes, their oracle repairs, the repair gates and the census are the v6 ones.
  Leave-one-fault-out fits use single-fault rows only, so U1 is not influenced by composed rows (a composed row containing the held-out fault would otherwise leak it).
- **Regression check, descriptive:** the v7 single-fault verdict is compared with the v6 CPU verdict item by item: detector and repair statuses, the core-28 counts, L1, L2, U1 and N1 values, C2 AUROC, the policy table and the cheap-guarantee table. A **regression** is defined in advance as: any core-28 detector or repair status that changes from PASS to FAIL or THIN, the adoption verdict leaving ADOPTED, L1, L2 or N1 changing from PASS to FAIL, or `capped_crc_0.005` ceasing to meet all four targets. Anything else is reported as a difference with its size. U1 is reported with its change but carries no bar here.

## 5. Targets (descriptive only, no gate)
None. The arm reports every number, including empty or short strata, with Wilson 95% intervals for proportions. Predictions below are written so that they can fail; they are not targets.

## 6. Predictions (judgements from the v6 record and the smoke, not guarantees)
- Both-cause detection at the family level will be **low for within-letter strata** (the dispatcher's second label depends on the group-mass rule, which is built for cross-group pairs) and higher for cross-letter pairs: about 0.2 to 0.5 overall.
- Adding composed rows will **raise set-F1 and both-cause detection modestly** over ATT0 (by up to about 0.1) and will not change the single-fault gates beyond noise.
- Sequential closure will be **well below** oracle-forward closure (I expect a gap of 0.2 or more), because the loop only repairs what the diagnoser names and stops at a threshold.
- The forced reverse order will lower closure for some strata and make no difference for others.
- Several strata will fall short of quota because of the source-pool intersections (FAQ-based faults K07 and K09 can only pair with FAQ and input-policy sources); the shortfalls are reported.
- No regression in the single-fault gates (probability about 0.8). On v6 CPU `capped_crc_0.005` has margins of 0.0042 on loss, 0.089 on dispatch, 0.45 on cost and **0.047 on closure** (0.848 against 0.80); closure is the thinnest, and the retrained attributor could move it either way.

## 7. Run plan
- Code `kaggle/diagrag_v7.py`, generated from v6 by `kaggle/mk_v7.py` plus two cells in `kaggle/v7_cells/`. The frozen hash is written in amendment D1 below **before** the run.
- **One CPU run** (MiniLM-L6) in the sandbox, seed 50 for the single-fault arms (inherited from v6) and seed 51 for the composed arm, resumed from the v6 CPU checkpoint, in 1,400-second chunks. A GPU run is not planned.
- No second run and no seed change without the owner's approval.

## 8. What the headline sentence may say
It is generated by the script from the run's own files (`COMPOSED_RESULT.json`, `headline`). No figure from any other project (including the 0.775 design figure of the 47-fault catalogue project) is quoted as a result of this one.

## 9. Amendments

**D1 — code frozen (17 Nov 2026; no composed episode of the real run exists).** `kaggle/diagrag_v7.py` is generated from `kaggle/diagrag_v6.py` by `kaggle/mk_v7.py` and the two cells in `kaggle/v7_cells/`. The frozen v7 hash is now `0ebb2fe16e31f4880514e473e051e62ef21408bf4805d3d97fa81beda79fb194`.
Development checks done before this freeze, all on a tiny smoke of the same code (700 base queries, quotas scaled by 0.1; not the real run, numbers unused): the pipeline runs to the verdict (exit 0); the composed episodes use unique base queries, none shared between the splits or with any single-fault episode; every stratum produced episodes including triples; the exclusion reasons and the alone-fails record are written; the headline sentence is built from the run's own result file.
Two defects were found and fixed during development, before this freeze: a resumed run would have skipped one base query at every chunk boundary (the time-budget check sat after the pointer increment), and the composed-row builder failed on an empty set.
One limit of the smoke is recorded: its conformal thresholds were infinite (29 to 188 calibration queries per stratum, fewer than the 199 that a 0.5% bound needs), so its sequential loop never dispatched. The real run has 2,300 and 400 and 200 calibration queries in its three strata, as the v6 runs did.
