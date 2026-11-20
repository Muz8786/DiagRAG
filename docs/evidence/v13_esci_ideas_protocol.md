# v13 Ideas 1 + 2 on ESCI, U1 with the new ideas, and real (natural) failures (pre-registration). Written 20 Nov 2026, ~08:40 UTC, before any of this was run.

Runs on Kaggle only. Resumes the **v11.a ESCI checkpoint** (frozen v6 code `44176b9a…e28a`, GPU, seed 55, ADOPTED) and executes the frozen v6 code up to its U1 stage, so every function, threshold and model is the run's own. Nothing in the frozen code changes; no verdict changes.

## Part A — U1 (unseen faults) with Ideas 1 + 2
- **Exactly v6's U1 set-up:** for each single fault not in `RULE_PRIO`, a leave-one-fault-out attributor and group attributor, the flag threshold `thr_f` (5% clean false alarm), and the held-out episodes of that fault. An episode counts as closed only if flagged and its gold is back in the top k.
- **P0 = the stored U1 dispatcher** (`dispatch_v3` with group fallbacks). **Reproduction gate:** P0 recomputed must agree with the stored `LOFO` rows on at least 99.5% of episodes, else Part A stops and is reported as not run.
- **P12 (Idea 1 + Idea 2), the rule of `v13_idea2_protocol.md` D1, applied unchanged:** Idea-1 components flagged on the episode (invariant table of `v13_idea1_protocol.md`, calibrated on the run's clean training episodes); candidates = the family repairs of every fault whose component is flagged (the left-out fault placed at its component's position), ordered by the LOFO attributor's probability, then the attributor's order; duplicates of the same repair removed; at most 3; keep the candidate with the largest increase in the LOFO attributor's P(NONE). No gold is used.
- **Measures:** U1 = mean closure over faults for P0 (must equal the stored 0.396 within reproduction) and P12; paired bootstrap over faults (2,000) of P12 minus P0; U1 bar 0.50 (as pre-registered for v6).

## Part B — real failures, detection (no injected fault)
- The **1,648 never-examined natural ESCI queries** (`NAT3`), clean pipeline, no injection. A real failure = gold not in the top 5.
- AUROC of (i) the run's attributor fault score 1 - P(NONE) and (ii) the Idea-1 invariant score (smallest Bonferroni-scaled p-value), failure vs success; also excluding queries whose gold document is an empty placeholder (`gold_is_nan`), which no repair can fix. Descriptive.

## Part C — real failures, repair (Ideas 1 + 2 inside the deployed loop)
- **Deployed loop (stored N1):** natural rules (K12, K05) + classifier repairs where the Mondrian-CRC gate fires. **Reproduction gate:** recomputed `h_loop` must match the stored value on at least 99.5% of queries, else Part C stops.
- **N1-ideas:** identical gate and natural rules; where the classifier gate fires, the classifier repair is replaced by the P12 choice (candidates from the flagged components and the run's attributor, at most 3, largest increase in P(NONE)).
- **Measures:** paired change in Hit@5 against no repair and against the deployed loop (bootstrap, 2,000); queries fixed and broken; extra retrievals.

## Pass rules (fixed now)
- **A passes** if P12 minus P0 has a 95% lower bound above 0. **U1 passes its original bar** if P12 mean closure is at least 0.50 (reported either way).
- **C passes** if N1-ideas minus the deployed loop has a lower bound above -0.005 (non-inferior) **and** N1-ideas minus no repair has a lower bound above 0.
- B is descriptive.

## Trial and judged run
- **Trial:** the same notebook with `LIMIT` set (2 faults x 5 episodes, 30 natural queries) to check the harness, timing and memory. Its numbers are not results and are not used.
- **Judged run:** `LIMIT` off, run once.

## Predictions (judgements)
A passes: about 0.6. U1 reaches 0.50: about 0.35. C passes: about 0.4. B attributor AUROC on real failures above 0.60: about 0.5.

## Amendments
(none yet)
