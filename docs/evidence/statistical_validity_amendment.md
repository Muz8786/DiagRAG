# Statistical validity amendment for submission

**Prepared:** 22 November 2026 (IST)  
**Repository basis:** Muz8786/DiagRAG, branch `core28-kaggle-notebook`, commit `79af64d6f6305646b0a9edacdbc5d86247a55eb3`  
**Scope:** corrective interpretation and reporting for the adaptive self-test harm calculation, sparse-stratum pooled fallback, and v20 active/passive execution-budget comparison.

## Changes made

1. **Adaptive repair harm.** The manuscript no longer claims a 95% harm certificate for self-test repairs. The candidate search and acceptance reuse outcomes from the same probe battery, so the fixed-candidate Clopper–Pearson calculation does not apply. The manuscript reports the observed held-out traffic harm: among 301 measured repairs, 299 had observed harm below the nominal 2.95% fixed-candidate value; two exceeded it, each breaking 1 of 23 measured queries. This is descriptive evidence, not a confidence guarantee. The v15 measurement script and summary now label `verified` as finite-battery verification and explicitly mark harm inference as empirical only.

2. **Sparse calibration strata.** The paper limits the per-stratum conformal statement to strata with at least 199 calibration examples at alpha 0.005. Pooled fallback is retained as a deployment/evaluation policy, but the manuscript says it does not confer a per-stratum risk bound. On the second stack, the rare stratum used fallback in each corpus: FiQA had 71 of 2,632 calibration examples; NQ had 16 of 1,568. Reported loss and closure are explicitly empirical. The v14 fallback evaluator now emits per-stratum calibration counts, held-out harm counts/losses, and a no-per-stratum-guarantee status for pooled-fallback strata.

3. **v20 execution-budget comparability.** The manuscript compares active and passive identification on the same unique probe set only, not as a matched total-execution result. Active runs used a median of 672 executions (range 282–2,369); passive full-battery decoding uses 102–103 unique probes. The v20 audit source now selects the saved random-probe prefix no larger than the requested budget (so a 100-execution row uses 100 random probes rather than the full 102–103 probe battery) and labels its output as a budget frontier. The existing checked-in v20 JSON was not regenerated, so its old 100-execution row is not cited as a corrected matched-budget result.

## Reproducibility and limits

- Source manuscript and experiment scripts were read from the exact branch head above.
- The numerical claims above come from the supplied deep-audit report and stored repository outputs; this revision did not launch a Kaggle run or recompute the archived analysis.
- The task workspace contains no repository checkout, Kaggle checkpoints, or raw v15/v20 inputs. The Kaggle credential is not available to this Work session; it was not used or copied into any file.
- The manuscript compiles from the revised source if compilation succeeds below. Compilation does not validate the historical experimental outputs.
- No independent untouched certification battery was available. A future 95% repair-harm certificate would require a fresh sample reserved after candidate selection, with multiplicity/selection addressed if multiple candidates or rounds are tested.
