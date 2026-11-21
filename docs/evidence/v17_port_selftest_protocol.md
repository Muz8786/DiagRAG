# v17: the diagnostic self-test on the second retrieval stack. Pre-registration of design and splits
Written 21 Nov 2026, 12:35 IST, before any v17 code ran. Kaggle only. Results freeze 23:00 IST.

Purpose: external validity of the self-test (v15 S), which so far was confirmed only on the main stack. The algorithm (dictionary, battery selection, noisy-OR ranking, repair-and-retest search, rollback, verification) is the v15 A1 algorithm unchanged; only the stack-specific parts differ: the 14 system faults of the second stack (its 20 ported faults minus the query and content faults, and R06, which it does not have), their repairs from the frozen `diagrag_port5.py`, a rollback to the pinned configuration, and the per-query baseline (the second stack's attributor at its 5% false-positive threshold, dispatching its top class's repair; this stack has no frozen gated loop).

- Development: FiQA judged run (seed 60), development draws. Confirmation: **NQ** judged run (seed 58, a different corpus of 2.68M passages), held-out draws. A trial on FiQA runs first; its numbers are not results.
- Sizes (NQ queries are about 40 times slower than FiQA): pool 300 probes, battery 80 random plus up to 20 diagnostic, 2 instances per fault, 30 pairs chosen by md5, traffic 50 test queries (25 for pairs).
- The pass rule is the v15 A1 rule S-1 to S-5 (bars unchanged), restated as an amendment after the FiQA development run and before the NQ run, with any change needed for the second stack written there.
