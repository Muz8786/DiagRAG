# v14 flagship programme: pre-registration (written 20 Nov 2026, 18:00 IST, before any v14 run)

Purpose: answer the four reviewer fixes with new evidence, not new caveats. Everything below is fixed before the runs it governs.
Compute: Kaggle only (owner's instruction). Results freeze: Sat 21 Nov 2026, 23:00 IST. Anything not finished by then is reported as not run.

| Reviewer fix | Experiment | Status at registration |
|---|---|---|
| 1. Real failures, not author-injected faults | E3 (ESCI natural traffic) and E4b (NQ, FiQA test queries): real failures labelled by intervention | to run |
| 2a. Frontier model | E5 = arm A4.3 of `llm_baselines_plan.md`, unchanged | waits for the owner's funded key |
| 2b. Seed-robust adoption, untouched seeds | E1: three untouched seeds of the frozen code + a seed-averaged rule | to run |
| 2c. Unseen faults (U1) | E2: ceiling decomposition (descriptive) and E2b: verify-then-escalate policy (dev seed 55, confirm on E1 seeds) | to run |
| 3. Guarantee on a second stack | E4: per-stratum conformal gate on the e5/HNSW stack, FiQA and NQ | to run |
| 4. Classifier oversold | paper wording only (classifier presented as the gate for repairs; natural-traffic gain not in the abstract) | text |

## E1. Untouched seeds and a seed-averaged adoption rule

- Code: frozen v6, SHA-256 `44176b9a5ad633e39ec29581237d9919619b9944471178effb172be1d276e28a`. Notebook = `DiagRAG_v6_kaggle.ipynb` with only the seed and labels changed (as v11.a). Settings unchanged: N_BASE_ESCI 6000, N_PRDC 528, N_HARD 100, MAX_ATT 4000, N_HARM 20. GPU T4.
- Seeds **71, 72, 73**, never used before (seeds used so far: 7 to 9, 42 to 58, 60). One run each. A crash before the verdict is resumed from its checkpoint; nothing else is rerun.
- **Primary rule R-avg (new, judged only on seeds 71 to 73).** A core detector passes if the mean of its three held-out AUROCs is >= 0.70 and every seed has >= 50 held-out positives. A core repair passes if, pooled over the three seeds, it has >= 150 hard episodes, a Wilson 95% lower bound of the pooled rescue rate >= 0.50 and pooled clean loss <= 10% of pooled clean trials. ADOPTED_avg iff >= 27 of 28 detectors and >= 24 of 28 repairs pass (the counts of the per-run rule).
- **Secondary R-maj:** ADOPTED on >= 2 of the 3 seeds under the original per-run rule.
- Every per-seed verdict, L1, L2, U1 and N1 is reported. R-avg is also computed on seeds 50, 52 and 55, labelled descriptive, because it was written after those results were seen.
- Computed by a small script from the three runs' `detector_gates.csv` and `repair_gates.csv` (file reading only).

## E2. Unseen faults: ceiling decomposition (descriptive)

Run inside the frozen v6 harness on a checkpoint (seed 55; also seeds 71 to 73). For each of the 25 leave-one-fault-out (LOFO) faults and each of its 50 held-out episodes, with the LOFO models of the frozen code:
- `P0`: the stored LOFO outcome (reproduction gate: >= 99.5% agreement, else E2 is not reported).
- `own`: success of the fault's own family repair (the repair the system would use if it knew the fault).
- `reach`: success of every repair function the system can still choose without the fault's class: family repairs of every other single fault, the three group repairs and the universal repair (functions shared with another class are reachable).
- Per fault: `C_any` = share of episodes some reachable repair fixes; `C_flag` = share that is flagged (5% clean-FPR threshold of the frozen U1) and fixed by some reachable repair.
- Reported: mean `C_any`, mean `C_flag`, U1, U1 / `C_flag`, and the faults with `C_any` < 0.50. Interpretation fixed now: if mean `C_flag` < 0.50, the 0.50 bar cannot be met by any selector with this flagger and catalogue.

## E2b. Verify-then-escalate (new policy aimed at U1)

- **F_esc:** dispatch as now; re-score the repaired query with the same attributor; if it is still flagged, discard that result and apply the diagnosis-free universal repair to the original query. **F_keep** (variant): if still flagged, apply the universal repair and keep whichever of the two results has the lower fault score.
- In LOFO the flag and escalation threshold is the frozen U1 threshold. In deployment both use a per-stratum CRC threshold recalibrated for the policy on the same calibration queries, with the monotone upper-bound loss 1[s >= lam] * max(l_rep, 1[s1 >= lam] * l_univ), so the guarantee holds by construction.
- **Development on seed 55** (already seen). Selection rule fixed now: the primary is the variant with the higher dev U1 among variants whose dev held-out clean loss is <= 0.005; tie or none: F_esc. The choice is committed as an amendment before any E1-seed analysis is read.
- **Confirmation on seeds 71 to 73. CONFIRMED iff** (i) the mean U1 of the primary over the three seeds >= 0.50; (ii) held-out clean loss <= 0.005 on every seed; (iii) in-distribution mean closure >= that of `mondrian_crc_0.005` minus 0.02 on every seed. Otherwise NOT CONFIRMED, with the failing condition named. Cost (escalation rate, extra repairs) is reported.

## E3. Real failures labelled by intervention (ESCI natural traffic)

- Sample: the 1,648 never-examined natural queries already used for N1. A **real failure** is a query whose clean pipeline misses the gold at Hit@5 and whose gold is not an empty placeholder document (placeholder golds cannot be repaired meaningfully; this exclusion is fixed now).
- Every repair in the catalogue (family repairs, rule repairs, group repairs, universal) is run on every real failure. Label = the set of repairs that restore Hit@5 (interventional label; no author injection, no LLM, no human judgement). A failure is **repairable** if that set is non-empty.
- Reported: coverage (repairable / real failures); label distribution; deployed-loop success on repairable failures against a random catalogue repair (expected success), the universal repair and the oracle (1.0); detection AUROC of the attributor, the invariants and QPP (NQC, WIG) for repairable failures vs real successes and for unrepairable failures vs real successes; harm = share of real successes the loop breaks.
- Claims, fixed now: "detects repairable real failures" iff attributor AUROC >= 0.70; "diagnosis beats chance on real failures" iff loop minus random has a paired-bootstrap 95% lower bound > 0; "no harm on real traffic" iff loop harm on real successes <= 0.5%. Each is reported either way. F_esc is also reported on this sample.

## E4. The do-no-harm gate on a second stack (FiQA, NQ) and real failures there

- Replay of the judged port5 runs (FiQA, NQ; frozen `diagrag_port5.py` `916c3864…294f`, same harness as v13 Idea 2), on Kaggle.
- Attributor: the port's gradient-boosting settings, multi-class over the 20 faults and NONE, fitted on train episodes except a calibration half of the clean train queries (md5('cal|'+id) < 0.5, the ESCI rule). Dispatch: the top fault class's repair; score s = 1 - p(NONE). Strata: rare if `q_lowdf` > 0, else common (the ESCI rule). Loss: clean Hit@5 lost.
- Policies: `mondrian_crc_0.005`, `capped_crc_0.005` (also capped at 20% clean dispatch on calibration), `global_crc_0.005`, the 5%-FPR threshold, and the universal repair (all 20 repairs composed, applied to every query), with none.
- Held-out (test split) reports: clean loss with Wilson interval, clean dispatch, repairs per query and measured median seconds per query, mean closure over faults, and closure on the non-ceiling faults (stored port detector AUROC < 0.995).
- **Pass per corpus, fixed now:** held-out clean loss <= 0.005 for both `mondrian_crc_0.005` and `capped_crc_0.005`, and capped closure >= 0.70.
- **E4b:** real failures = clean test queries missing the gold at Hit@5; all 20 repairs run on each; same metrics and claim rules as E3.
- A trial (TRIAL=1, a few items) runs first; its numbers are not results.

## E5. Frontier arm

Arm A4.3 of `docs/evidence/llm_baselines_plan.md`, unchanged (same prompts, items, temperature 0, spend cap USD 15 set in the provider console, claim rules A4.4). It runs only if the owner supplies a funded key and chooses the model; otherwise it is reported as not run.

## Amendments

- **A1 (20 Nov 2026, 19:10 IST, before any E4 run).** E4 calibration also uses up to 2,000 clean queries that have relevance labels but lie outside the port run's 2,500-query sample (taken in the port's own md5 order), the analogue of ESCI's extra census calibration queries. Reason: at alpha = 0.005 a stratum needs at least 199 calibration queries for a finite threshold, and the clean-train half alone (about 625 queries) may leave the rare stratum without one. The universal repair on the port stack is every repair of the catalogue at once (the four query repairs, then every configuration repair, then the R19 depth repair). The port trace has no corpus-mean sparse score, so port NQC and WIG use the mean of the top-100 sparse scores in its place.

## Rules

- One judged run per item. Trials only check that the code runs. Amendments are dated and committed before the results they touch, with the code hash of every judged script recorded before its judged run.
- Every outcome is reported, pass or fail, in `docs/evidence/v14_results.md`.
- Code is written by an AI assistant (Claude) under the owner's direction; E2b was designed after the seed-50/52/55 U1 results were seen, which is why it is confirmed only on untouched seeds.
