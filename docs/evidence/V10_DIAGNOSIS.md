# Why C2 and Q03 sit under the 0.70 detector bar (descriptive, post-hoc; written 19 Nov 2026)

Script `docs/evidence/v10_diagnosis.py`, output `v10_diagnosis_v6_v8.json`, run on the saved v6 (seed 50) and v8 (seed 52) GPU episodes. No gate, bar, code or verdict was changed. Not pre-registered.

## Findings
1. **C2 (0.751 in v6, 0.681 in v8) is within sampling noise.** The two stored AUROCs and their stored 95% intervals give z = 0.98, two-sided p about 0.33 (normal approximation). Each run has 50 held-out positives, so a 95% interval is about +/-0.10 wide. A detector whose true AUROC is near 0.70 will pass or fail the 0.70 bar at roughly coin-flip odds at this n. The "27 of 28 detectors" adoption rule with 50 positives per detector therefore cannot separate a detector at 0.70 from one just below it. That is a property of the measurement, not a finding about C2.
2. **Q03 is not detectable from this telemetry, in either run.** The multi-class attributor calls 48 of 50 held-out Q03 episodes clean (96%) in both runs; exact identification is 0 of 50; the mean probability it gives the true class is 0.027 (v6) and 0.014 (v8). Q03 swaps a key word for a WordNet synonym, so the query and the retrieval telemetry barely change. `docs/IDENTIFIABILITY.md` had already put Q03 in three of the five least-separable fault pairs. This is a limit of the signal, so no tuning of the detector should be expected to fix it.
3. The attributor puts C2 (a composition) mostly into single-fault classes (R10, R19, K04, ...), and calls only 4 to 8% of C2 episodes clean.

## What this does and does not support
- It supports saying **why** the adoption verdict is fragile: one detector (C2) near the bar with a wide interval, plus one (Q03) that is below it by construction.
- It does **not** change v8's verdict (NOT_ADOPTED), and it does **not** justify lowering the bar, dropping Q03 or C2 from the count, or re-running seed 52. Any such change would be a new, pre-registered version (v10) judged on its own, with v6 and v8 left as they are.
- Possible v10 designs that would be honest (not started): (a) report the adoption rule with an interval, not a hard count, and pre-register that rule before the run; (b) more held-out positives per detector so that a 0.70 detector is classified reliably; (c) leave Q03 as a documented non-identifiable fault and say so in the claim. Each needs your decision and a fresh seed.
