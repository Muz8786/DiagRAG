# v17 to v19 results (every outcome, pass or fail)

| Test | Data | Outcome | File |
|---|---|---|---|
| v17 self-test on the second stack (rule A1, S-5 aggregation per A3) | FiQA, held-out fault draws (NQ could not finish: A2) | **PASS** | `kaggle/v17_heldout.json` |
| v18 bugs reproduced from public issue reports (rule B-0 to B-3) | seeds 74, 75, 76; 600 never-examined natural ESCI queries | **PASS** | `kaggle/v18_bugs_pooled.json` |
| v19 two-channel unseen-fault closure (rule U-1, U-2) | seed 71 (72, 73 queued; 74 added per A2) | seed 71: 0.608 (bar 0.50), no false alarm | `kaggle/judged_v19_seed71/RESULT.json` |

v17: harmful singles 27, detection 1.000, family 0.963, verified 1.000; same-group pairs both named 0.870 vs 0.391 aggregated per-query; closure 1.000 (117 and 152 broken traffic queries) vs per-query 0.993 / 0.497 and universal 0.903 / 0.597; harm 0.0% vs 0.5% / 9.4% (per-query) and 4.4% / 7.4% (universal).

v18: 7 of 9 bugs harmful (21 units); detection 20/21, localization 21/21, every accepted repair verified; 1,454 of 1,461 broken natural queries restored, none broken by a repair; per-query telemetry 8/21; per-query loop restores 300, universal repair 339. The miss is B3 on seed 76. B1 and B2 break nothing on this stack.

v19 (seed 71): per-query U1 0.398, two-channel 0.608 (+0.21 [+0.08, +0.35]); system faults 0.52 -> 0.96 (11 of 12 detected; K04 not seen by probes; 8 of 11 closed by verified rollback, 3 by a same-family repair); query and content faults unchanged at 0.28.

Disclosed changes: v17 S-5 for the second stack (singles not below an ungated per-query baseline) and pooled closure aggregation (A1, A3), both before the held-out run; v17 confirmation on FiQA held-out draws instead of NQ (A0 fallback, A2); v18 trial skipped because of the GPU queue (A1); v19 seed 74 added (A2).
