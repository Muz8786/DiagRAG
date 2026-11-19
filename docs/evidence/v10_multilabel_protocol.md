# Multi-label dispatcher study (pre-registration). Written 19 Nov 2026, before any held-out composed episode was scored by this method.

## 0. Question and scope
v7 found that the dispatcher returns at most one label per letter group, so it names every cause in **0 of 75** episodes of the QQ, KK, RR and TRIPLE strata (`docs/evidence/v7_composed_protocol.md` D4). This study asks whether a **multi-label rule on the same attributor probabilities** can name both causes inside one letter group **without** emitting many wrong labels.
It is **descriptive**. No adoption gate, no change to any detector, repair, gate or frozen file. v6, v7 and v8 results are untouched. It does **not** evaluate repairs or closure (only naming), because the repair loop is not changed here.

## 1. Data (all committed; CPU MiniLM stack of the v7 run)
- Single-fault training rows: `kaggle/judged_cpu_run_v7_seed50/episodes.jsonl`, split `train`, faults other than C2 (the same single-fault episodes the v7 retrained attributor used), minus the clean calibration rows by the v6 rule (md5 of `cal|` + base query below `CAL_FRAC`).
- Composed training rows: `composed_features.jsonl` (rows aligned by order with `composed_episodes.jsonl`, checked: all 310 agree on split and stratum), split `train`, 155 episodes. Each is expanded to **one row per component labelled with that component**, exactly as the v7 retrained attributor did.
- Held-out: the 155 composed `test` episodes, **scored once, at the end**.
- Held-out clean episodes: the single-fault `test` rows with fault `NONE`, for a false-label check.

## 2. Method (fixed now)
- **Attributor:** `HistGradientBoostingClassifier` with the v6 settings (`max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=50`), 32 classes.
- **Multi-label rule:** the predicted set is every non-NONE class with probability >= tau, **capped at 3 labels** (the three most probable), and, if no class reaches tau, **the single most probable non-NONE class is returned only if P(NONE) < 0.5**, otherwise the set is empty.
- **tau is chosen on training data only:** grid {0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40}; 5-fold cross-validation over the 155 composed **training** episodes grouped by base query (single-fault rows always in the fit); the score is mean family-level set-F1 on the held-out fold; the largest mean wins, ties go to the larger tau. **No held-out composed episode is used to choose tau.**
- **Family-level naming and set-F1** use the v7 definitions (`docs/evidence/v9_emergent_breakdown.py`: a non-fallback label equal to the cause or in its repair-equivalence family).
- **Comparison baseline (stored, not re-fitted):** the v7 dispatcher's stored labels `lab_new` on the same 155 held-out episodes: both causes named 62/155 (40.0%), mean set-F1 0.770, recall 0.697, precision 0.923.

## 3. Measures (all reported, with Wilson 95% intervals for proportions)
- Both causes named (family level), overall and by stratum, against the stored v7 figures.
- Mean set-F1, precision, recall, and **mean number of labels per episode** (a method that wins by emitting many labels shows up as low precision and a large set).
- **False-label check on held-out clean episodes:** the share of clean test episodes for which the rule returns a non-empty set, beside the same share for the single-label rule "argmax is not NONE".
- A **top-2 always** reference (the two most probable non-NONE classes, no threshold), reported to show what the threshold buys.

## 4. Predictions (my judgements; they can fail)
- Overall both-cause naming rises above 40.0% (62/155): about 0.7. Overall at or above 50%: about 0.35.
- QQ, KK and RR naming rises above 0 of 20 in at least one stratum: about 0.7; in all three: about 0.35.
- Mean set precision falls below the stored 0.923: about 0.85. Mean set size above 2.0: about 0.4.
- The held-out clean false-label share is higher than the single-label rule's: about 0.8.
- **Whether the study counts as an improvement is decided by the owner, not by this file:** a rise in naming that comes with a large drop in precision, or a clean false-label rise, is reported as a trade-off and not as a gain.

## 5. What a result would and would not show
- It tests naming on **155 synthetic composed episodes, one seed, one CPU stack**, using **155 composed training episodes**; intervals will be wide (about +/-8 points at n = 155 overall, wider by stratum at n = 20).
- Tau is tuned with 155 training episodes; the result depends on that small set.
- A rise in naming does **not** show that repairs improve, and no repair result is claimed.
- Nothing here changes a frozen file or a verdict. A deployed multi-label dispatcher would need its own pre-registered closed-loop study.

## 6. Amendments
(none yet; each is dated and filed before the result it concerns is read)
