# DiagRAG core-28 v2 judged run report

Device: cpu. Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2. Last session runtime: 402s.

## Verdict (gates fixed in JUDGED_PROTOCOL.json before results)

```
{
 "detectors_pass": 28,
 "repairs_pass": 27,
 "solved_both": 27,
 "of": 28,
 "new_faults": {
  "R25": {
   "detector": "PASS",
   "repair": "PASS"
  },
  "R26": {
   "detector": "THIN",
   "repair": "THIN"
  },
  "K11": {
   "detector": "PASS",
   "repair": "PASS"
  }
 },
 "family_repairs": [
  {
   "fault": "Q01",
   "family": "QLEX",
   "n": 50,
   "rescued": 34,
   "rate": 0.68,
   "ci_lo": 0.5418944286372392
  },
  {
   "fault": "Q03",
   "family": "QLEX",
   "n": 50,
   "rescued": 26,
   "rate": 0.52,
   "ci_lo": 0.38511512258808434
  },
  {
   "fault": "Q04",
   "family": "QLEX",
   "n": 50,
   "rescued": 35,
   "rate": 0.7,
   "ci_lo": 0.562493877226366
  },
  {
   "fault": "Q05",
   "family": "QLEX",
   "n": 50,
   "rescued": 42,
   "rate": 0.84,
   "ci_lo": 0.7148551903823401
  },
  {
   "fault": "K04",
   "family": "STALE",
   "n": 50,
   "rescued": 47,
   "rate": 0.94,
   "ci_lo": 0.8378265662912299
  },
  {
   "fault": "R03",
   "family": "ENC",
   "n": 50,
   "rescued": 50,
   "rate": 1.0,
   "ci_lo": 0.9286499658256813
  },
  {
   "fault": "R07",
   "family": "STALE",
   "n": 50,
   "rescued": 50,
   "rate": 1.0,
   "ci_lo": 0.9286499658256813
  },
  {
   "fault": "R10",
   "family": "ENC",
   "n": 50,
   "rescued": 50,
   "rate": 1.0,
   "ci_lo": 0.9286499658256813
  },
  {
   "fault": "R11",
   "family": "ENC",
   "n": 50,
   "rescued": 50,
   "rate": 1.0,
   "ci_lo": 0.9286499658256813
  }
 ],
 "loop_gates": {
  "L1": "FAIL",
  "L2": "PASS"
 },
 "verdict": "ADOPTED",
 "clean_net_hit_change": -0.009022556390977444,
 "guarantee": {
  "alpha": 0.005,
  "lam": 0.00040804650590808844,
  "calibration_n": 811,
  "heldout_clean_loss": 0.012781954887218045,
  "resplit_mean": 0.0030002242647437206,
  "resplit_p95": 0.007300160227879651,
  "L1": "FAIL",
  "L2": "PASS",
  "mean_closure": 0.8706666666666668
 },
 "policies": [
  {
   "policy": "tau_none_5pct_fpr",
   "threshold": 0.46444903013648775,
   "mean_closure": 0.8280000000000001,
   "mean_closure_v1_28": 0.8171428571428573,
   "mean_family_attribution": 0.8013333333333333,
   "clean_dispatch_rate": 0.04586466165413534,
   "clean_loss": 0.006015037593984963,
   "clean_net_hit_change": -0.0037593984962406013
  },
  {
   "policy": "crc_alpha_0.0025",
   "threshold": 0.008642191529207532,
   "mean_closure": 0.8693333333333334,
   "mean_closure_v1_28": 0.8614285714285714,
   "mean_family_attribution": 0.832,
   "clean_dispatch_rate": 0.36917293233082704,
   "clean_loss": 0.009774436090225564,
   "clean_net_hit_change": -0.006015037593984963
  },
  {
   "policy": "crc_alpha_0.005",
   "threshold": 0.00040804650590808844,
   "mean_closure": 0.8706666666666668,
   "mean_closure_v1_28": 0.862857142857143,
   "mean_family_attribution": 0.8346666666666667,
   "clean_dispatch_rate": 0.9954887218045113,
   "clean_loss": 0.012781954887218045,
   "clean_net_hit_change": -0.009022556390977444
  },
  {
   "policy": "crc_alpha_0.01",
   "threshold": 0.00040804650590808844,
   "mean_closure": 0.8706666666666668,
   "mean_closure_v1_28": 0.862857142857143,
   "mean_family_attribution": 0.8346666666666667,
   "clean_dispatch_rate": 0.9954887218045113,
   "clean_loss": 0.012781954887218045,
   "clean_net_hit_change": -0.009022556390977444
  },
  {
   "policy": "crc_alpha_0.02",
   "threshold": 0.00040804650590808844,
   "mean_closure": 0.8706666666666668,
   "mean_closure_v1_28": 0.862857142857143,
   "mean_family_attribution": 0.8346666666666667,
   "clean_dispatch_rate": 0.9954887218045113,
   "clean_loss": 0.012781954887218045,
   "clean_net_hit_change": -0.009022556390977444
  }
 ],
 "natural": [
  {
   "arm": "NA1",
   "what": "natural misspelling (rule q_correctable)",
   "n_selected": 155,
   "hit_before": 0.5612903225806452,
   "hit_after": 0.49032258064516127,
   "delta": -0.07096774193548387,
   "ci_lo": -0.14193548387096774,
   "ci_hi": 0.0,
   "fixed": 11,
   "broken": 22,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA1b",
   "what": "NA1 where the corrected query was typed by another ESCI user",
   "n_selected": 6,
   "hit_before": 0.3333333333333333,
   "hit_after": 0.3333333333333333,
   "delta": 0.0,
   "ci_lo": -0.6666666666666666,
   "ci_hi": 0.6666666666666666,
   "fixed": 2,
   "broken": 2,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA2",
   "what": "natural missing space (rule q_segmentable)",
   "n_selected": 53,
   "hit_before": 0.5094339622641509,
   "hit_after": 0.5283018867924528,
   "delta": 0.018867924528301886,
   "ci_lo": -0.05660377358490566,
   "ci_hi": 0.09433962264150944,
   "fixed": 3,
   "broken": 2,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA3",
   "what": "natural 'nan' placeholder in top-5 (rule thin5)",
   "n_selected": 8,
   "hit_before": 1.0,
   "hit_after": 0.5,
   "delta": -0.5,
   "ci_lo": -0.875,
   "ci_hi": -0.125,
   "fixed": 0,
   "broken": 4,
   "verdict": "HARM"
  },
  {
   "arm": "NA4",
   "what": "natural exact duplicate in top-5 (rule dup5)",
   "n_selected": 125,
   "hit_before": 0.384,
   "hit_after": 0.44,
   "delta": 0.056,
   "ci_lo": 0.016,
   "ci_hi": 0.104,
   "fixed": 8,
   "broken": 1,
   "verdict": "PASS"
  },
  {
   "arm": "NA5",
   "what": "natural chunk crowding (rule chunk_crowd5)",
   "n_selected": 621,
   "hit_before": 0.5523349436392915,
   "hit_after": 0.5974235104669887,
   "delta": 0.04508856682769726,
   "ci_lo": 0.027375201288244767,
   "ci_hi": 0.06280193236714976,
   "fixed": 32,
   "broken": 4,
   "verdict": "PASS"
  },
  {
   "arm": "NA6",
   "what": "closed loop v2 on all natural queries, policy tau_none_5pct_fpr",
   "n_selected": 1500,
   "hit_before": 0.5173333333333333,
   "hit_after": 0.518,
   "delta": 0.0006666666666666666,
   "ci_lo": -0.0033333333333333335,
   "ci_hi": 0.004666666666666667,
   "fixed": 5,
   "broken": 4,
   "dispatched": 0.06,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA6",
   "what": "closed loop v2 on all natural queries, policy crc_alpha_0.0025",
   "n_selected": 1500,
   "hit_before": 0.5173333333333333,
   "hit_after": 0.5133333333333333,
   "delta": -0.004,
   "ci_lo": -0.012,
   "ci_hi": 0.004,
   "fixed": 13,
   "broken": 19,
   "dispatched": 0.52,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA6",
   "what": "closed loop v2 on all natural queries, policy crc_alpha_0.005",
   "n_selected": 1500,
   "hit_before": 0.5173333333333333,
   "hit_after": 0.508,
   "delta": -0.009333333333333334,
   "ci_lo": -0.017349999999999997,
   "ci_hi": -0.0006666666666666666,
   "fixed": 13,
   "broken": 27,
   "dispatched": 0.9933333333333333,
   "verdict": "HARM"
  },
  {
   "arm": "NA6",
   "what": "closed loop v2 on all natural queries, policy crc_alpha_0.01",
   "n_selected": 1500,
   "hit_before": 0.5173333333333333,
   "hit_after": 0.508,
   "delta": -0.009333333333333334,
   "ci_lo": -0.017349999999999997,
   "ci_hi": -0.0006666666666666666,
   "fixed": 13,
   "broken": 27,
   "dispatched": 0.9933333333333333,
   "verdict": "HARM"
  },
  {
   "arm": "NA6",
   "what": "closed loop v2 on all natural queries, policy crc_alpha_0.02",
   "n_selected": 1500,
   "hit_before": 0.5173333333333333,
   "hit_after": 0.508,
   "delta": -0.009333333333333334,
   "ci_lo": -0.017349999999999997,
   "ci_hi": -0.0006666666666666666,
   "fixed": 13,
   "broken": 27,
   "dispatched": 0.9933333333333333,
   "verdict": "HARM"
  }
 ],
 "unseen_mean_closure": 0.25333333333333335,
 "not_solved": [
  "Q03"
 ],
 "device": "cpu",
 "reranker": "cross-encoder/ms-marco-MiniLM-L-6-v2"
}
```

{
 "detector": "held-out one-vs-rest AUROC >= 0.70 (point estimate) AND >= 20 held-out positives",
 "repair": ">= 20 hard episodes AND Wilson 95% lower bound of rescue rate >= 0.50 AND <= 10% of clean successes lost when the repair is forced on them",
 "solved": "detector PASS and repair PASS",
 "targets": "ADOPTED if repairs PASS >= 24/28 AND detectors PASS >= 27/28, else NOT_ADOPTED",
 "AUROC_BAR": 0.7,
 "MIN_TEST_POS": 20,
 "RESCUE_BAR_LB": 0.5,
 "MIN_REPAIR_N": 20,
 "MAX_HARM": 0.1,
 "REPAIR_TARGET": 24,
 "DETECT_TARGET": 27,
 "guarantee": "do-no-harm dispatch: threshold lambda fitted by conformal risk control on out-of-fold clean TRAIN queries so that E[Hit@5 lost on a clean query] <= ALPHA; PASS if held-out clean loss <= ALPHA; also report 200 calibration re-splits",
 "ALPHA": 0.005,
 "ALPHAS": [
  0.0025,
  0.005,
  0.01,
  0.02
 ],
 "natural": "report, not gated: (a) real misspelled ESCI queries whose corrected spelling was typed by another ESCI user, gold from ESCI labels; (b) in-corpus superseded policy versions with the validity filter off, no injected docs. Metrics: Hit@5 before, after closed loop (guarded and unguarded), after oracle repair, oracle-referenced closure",
 "unseen": "report, not gated: leave-one-fault-out attributor; on the held-out fault test episodes report flagged rate, right-group rate and Hit after dispatch",
 "v2_new_faults": "R25, R26, K11 judged with the same detector and repair gates; reported beside the 28, not counted in the 28-fault verdict",
 "v2_loop": "family-level dispatch; FAMILIES QLEX={Q01,Q03,Q04,Q05}, STALE={K04,R07}, ENC={R03,R10,R11}; attribution correct if the family is right. L1 PASS if held-out clean Hit@5 loss <= ALPHA under the CRC threshold fitted on the separate calibration split. L2 PASS if mean held-out closure over the 31 faults + C2 >= 0.70 under the same threshold",
 "L2_BAR": 0.7,
 "v2_natural": "arms NA1-NA6 on ESCI queries outside natural_exclusions_v1.json; selection by deployed rule only, never by gold; metric paired delta Hit@5 (repair - none) with 95% bootstrap CI (N_BOOT resamples); PASS if CI lower bound > 0, HARM if CI upper bound < 0, else INCONCLUSIVE"
}

| fault   | detector   | repair   | solved   |
|:--------|:-----------|:---------|:---------|
| Q01     | PASS       | PASS     | True     |
| Q02     | PASS       | PASS     | True     |
| Q03     | PASS       | FAIL     | False    |
| Q04     | PASS       | PASS     | True     |
| Q05     | PASS       | PASS     | True     |
| Q07     | PASS       | PASS     | True     |
| Q09     | PASS       | PASS     | True     |
| K03     | PASS       | PASS     | True     |
| K04     | PASS       | PASS     | True     |
| K05     | PASS       | PASS     | True     |
| K06     | PASS       | PASS     | True     |
| K07     | PASS       | PASS     | True     |
| K08     | PASS       | PASS     | True     |
| K09     | PASS       | PASS     | True     |
| R01     | PASS       | PASS     | True     |
| R03     | PASS       | PASS     | True     |
| R05     | PASS       | PASS     | True     |
| R06     | PASS       | PASS     | True     |
| R07     | PASS       | PASS     | True     |
| R10     | PASS       | PASS     | True     |
| R11     | PASS       | PASS     | True     |
| R13     | PASS       | PASS     | True     |
| R15     | PASS       | PASS     | True     |
| R19     | PASS       | PASS     | True     |
| R22     | PASS       | PASS     | True     |
| R23     | PASS       | PASS     | True     |
| R24     | PASS       | PASS     | True     |
| R25     | PASS       | PASS     | True     |
| R26     | THIN       | THIN     | False    |
| K11     | PASS       | PASS     | True     |
| C2      | PASS       | PASS     | True     |

## Data verification

|            | file                                      |     bytes | size_ok   | sha256                                                           | sha_ok   |
|:-----------|:------------------------------------------|----------:|:----------|:-----------------------------------------------------------------|:---------|
| corpus     | kb_tier3_186k.jsonl.gz                    |  53518791 | True      | 5a9f7ea6ae5b8a3e7f1e1ca6e2838dddd6158efb9384d757c6aa755dbe9bda3c | True     |
| cache      | embeddings_cache_186k.npz                 | 533012659 | True      | 3b43603d9689f7c0eee0cbfebdb8b5cfddd05a2fc4e3cf192c8eed1de4a88835 | True     |
| esci       | shopping_queries_dataset_examples.parquet |  51286808 | True      | 4a735b693b4a424a6fc67f5be6e4c811495c488bbf66d02a602d308b2744263a | True     |
| exclusions | natural_exclusions_v1.json                |    128698 | True      | b249216fe1b1f0f8d427d1699c759a402909d08644e70a14bcfc88963fdcce42 | True     |
| qspell     | corpus-webis-qspell-17.zip                |   2285705 | True      | f13bd165544ab2ac75d63de4334feb86d74d1b3dfbe48d79423133552b5054e4 | True     |

## Purity

```
{
 "docs": 186290,
 "schemas": 1,
 "unique_ids": 186290,
 "empty_content": 0,
 "exact_dup_rows_beyond_first": 2558,
 "exact_dup_groups": 1537,
 "dup_groups_with_2plus_unflagged": 68,
 "flagged_dup_without_exact_twin": 45,
 "chunk_span_mismatch": 3554,
 "replacement_char_rows": 2,
 "nan_placeholder_docs": 3993,
 "license_status": {
  "synthetic_shopnova|unassigned": 1040,
  "real_world_apache_esci|verified": 13229,
  "real_world_cc_by_4_0_abo|verified": 86566,
  "real_world_cc_by_4_0_abo|conflicting_unverified": 84993,
  "real_world_apache_ofbiz_docs|verified": 462
 },
 "asin_in_both_esci_and_abo": 36,
 "emb": {
  "shape": [
   186290,
   768
  ],
  "nan": 0,
  "zero_rows": 0,
  "norm_min": 0.9999998807907104,
  "norm_max": 1.0000001192092896,
  "ids_in_order": true,
  "identical_rows_beyond_first": 533
 },
 "esci_queries_us_E_in_corpus": 7175,
 "esci_split_counts": {
  "train": 4529,
  "test": 2646
 },
 "esci_gold_components": 1829,
 "esci_test_gold_leak": 0,
 "v2_base_pool_seen": 4027,
 "v2_natural_pool_unseen": 3148,
 "query_log_queries": 91797
}
```

## Episode generation (hard = clean succeeds, faulted fails)

| fault   |   pool |   attempts |   not_applicable |   easy |   hard |   hard_train |   hard_test |   real_typos |   hard_yield |
|:--------|-------:|-----------:|-----------------:|-------:|-------:|-------------:|------------:|-------------:|-------------:|
| Q01     |   1285 |        520 |              382 |     87 |     50 |           25 |          25 |            0 |        0.362 |
| Q02     |   1285 |        336 |                0 |    286 |     50 |           25 |          25 |            0 |        0.149 |
| Q03     |   1285 |        470 |              296 |    124 |     50 |           25 |          25 |            0 |        0.287 |
| Q04     |   1285 |         70 |                2 |     18 |     50 |           25 |          25 |           14 |        0.735 |
| Q05     |   1285 |        182 |               20 |    112 |     50 |           25 |          25 |            0 |        0.309 |
| Q07     |   1329 |        951 |              575 |    325 |     50 |           25 |          25 |            0 |        0.133 |
| Q09     |   1285 |        132 |                0 |     81 |     50 |           25 |          25 |            0 |        0.379 |
| K03     |    888 |        165 |              112 |      3 |     50 |           25 |          25 |            0 |        0.943 |
| K04     |   1285 |        100 |                0 |     50 |     50 |           25 |          25 |            0 |        0.5   |
| K05     |   1285 |        113 |                0 |     63 |     50 |           25 |          25 |            0 |        0.442 |
| K06     |    809 |         56 |                0 |      6 |     50 |           25 |          25 |            0 |        0.893 |
| K07     |    246 |         70 |                0 |     20 |     50 |           25 |          25 |            0 |        0.714 |
| K08     |   1285 |         62 |                0 |     12 |     50 |           25 |          25 |            0 |        0.806 |
| K09     |    282 |         51 |                0 |      1 |     50 |           25 |          25 |            0 |        0.98  |
| R01     |   1285 |        119 |                0 |     69 |     50 |           25 |          25 |            0 |        0.42  |
| R03     |   1285 |        603 |                0 |    553 |     50 |           25 |          25 |            0 |        0.083 |
| R05     |   1285 |         76 |                0 |     26 |     50 |           25 |          25 |            0 |        0.658 |
| R06     |   1285 |         51 |                0 |      0 |     50 |           25 |          25 |            0 |        0.98  |
| R07     |   1285 |        197 |                0 |    147 |     50 |           25 |          25 |            0 |        0.254 |
| R10     |   1285 |        612 |                0 |    561 |     50 |           25 |          25 |            0 |        0.082 |
| R11     |   1285 |        541 |                0 |    491 |     50 |           25 |          25 |            0 |        0.092 |
| R13     |   1285 |        799 |                0 |    749 |     50 |           25 |          25 |            0 |        0.063 |
| R15     |   1285 |        404 |                0 |    354 |     50 |           25 |          25 |            0 |        0.124 |
| R19     |   1285 |        339 |                0 |    289 |     50 |           25 |          25 |            0 |        0.147 |
| R22     |   1285 |        670 |                0 |    620 |     50 |           25 |          25 |            0 |        0.075 |
| R23     |   1285 |        131 |                0 |     81 |     50 |           25 |          25 |            0 |        0.382 |
| R24     |   1285 |        164 |                0 |    114 |     50 |           25 |          25 |            0 |        0.305 |
| R25     |   1285 |        146 |                0 |     96 |     50 |           25 |          25 |            0 |        0.342 |
| R26     |   1285 |       2500 |             1224 |   1272 |      3 |            3 |           0 |            0 |        0.002 |
| K11     |    809 |         53 |                0 |      3 |     50 |           25 |          25 |            0 |        0.943 |
| C2      |   1285 |         85 |                9 |     26 |     50 |           25 |          25 |            0 |        0.658 |

## Detector gates (AUROC bar 0.7, min test positives 20)

| fault   | detector                             |   n_pos_train |   n_pos_test |   n_neg_test |    auroc |    ci_lo |    ci_hi |   auroc_vs_clean | status   |
|:--------|:-------------------------------------|--------------:|-------------:|-------------:|---------:|---------:|---------:|-----------------:|:---------|
| Q01     | histgb_head                          |            25 |           25 |         2030 |   0.9979 |   0.9961 |   0.9994 |           0.9991 | PASS     |
| Q02     | histgb_head                          |            25 |           25 |         2030 |   0.9999 |   0.9997 |   1.0000 |           0.9999 | PASS     |
| Q03     | histgb_head                          |            25 |           25 |         2030 |   0.8767 |   0.7831 |   0.9657 |           0.8920 | PASS     |
| Q04     | tier0_rule                           |            25 |           25 |         2030 |   0.9831 |   0.9729 |   0.9926 |           0.9870 | PASS     |
| Q05     | histgb_head                          |            25 |           25 |         2030 |   0.9871 |   0.9777 |   0.9941 |           0.9902 | PASS     |
| Q07     | histgb_head                          |            25 |           25 |         2030 |   0.9993 |   0.9978 |   1.0000 |           0.9997 | PASS     |
| Q09     | histgb_head                          |            25 |           25 |         2030 |   0.9998 |   0.9994 |   1.0000 |           0.9998 | PASS     |
| K03     | histgb_head                          |            25 |           25 |         2030 |   0.9999 |   0.9996 |   1.0000 |           1.0000 | PASS     |
| K04     | histgb_head                          |            25 |           25 |         2030 |   0.8758 |   0.7341 |   0.9766 |           0.8776 | PASS     |
| K05     | histgb_head                          |            25 |           25 |         2030 |   0.9996 |   0.9991 |   1.0000 |           1.0000 | PASS     |
| K06     | histgb_head                          |            25 |           25 |         2030 |   0.9934 |   0.9817 |   1.0000 |           0.9955 | PASS     |
| K07     | tier0_rule                           |            25 |           25 |         2030 |   1.0000 |   1.0000 |   1.0000 |           1.0000 | PASS     |
| K08     | histgb_head                          |            25 |           25 |         2030 |   0.9772 |   0.9408 |   1.0000 |           0.9727 | PASS     |
| K09     | histgb_head                          |            25 |           25 |         2030 |   1.0000 |   1.0000 |   1.0000 |           1.0000 | PASS     |
| R01     | histgb_head                          |            25 |           25 |         2030 |   1.0000 |   1.0000 |   1.0000 |           1.0000 | PASS     |
| R03     | histgb_head                          |            25 |           25 |         2030 |   1.0000 |   0.9999 |   1.0000 |           1.0000 | PASS     |
| R05     | histgb_head                          |            25 |           25 |         2030 |   0.9976 |   0.9937 |   0.9997 |           0.9991 | PASS     |
| R06     | histgb_head                          |            25 |           25 |         2030 |   0.9605 |   0.9166 |   0.9949 |           0.9734 | PASS     |
| R07     | histgb_head                          |            25 |           25 |         2030 |   0.9997 |   0.9992 |   1.0000 |           1.0000 | PASS     |
| R10     | histgb_head                          |            25 |           25 |         2030 |   1.0000 |   1.0000 |   1.0000 |           1.0000 | PASS     |
| R11     | histgb_head                          |            25 |           25 |         2030 |   0.9981 |   0.9957 |   0.9999 |           1.0000 | PASS     |
| R13     | histgb_head                          |            25 |           25 |         2030 |   1.0000 |   1.0000 |   1.0000 |           1.0000 | PASS     |
| R15     | tier0_rule                           |            25 |           25 |         2030 |   1.0000 |   1.0000 |   1.0000 |           1.0000 | PASS     |
| R19     | histgb_head                          |            25 |           25 |         2030 |   1.0000 |   1.0000 |   1.0000 |           1.0000 | PASS     |
| R22     | histgb_head                          |            25 |           25 |         2030 |   0.9722 |   0.9272 |   0.9994 |           0.9763 | PASS     |
| R23     | tier0_rule                           |            25 |           25 |         2030 |   1.0000 |   1.0000 |   1.0000 |           1.0000 | PASS     |
| R24     | histgb_head                          |            25 |           25 |         2030 |   0.9693 |   0.9382 |   0.9915 |           0.9830 | PASS     |
| R25     | tier0_rule                           |            25 |           25 |         2030 |   1.0000 |   1.0000 |   1.0000 |           1.0000 | PASS     |
| R26     | tier0_rule                           |             3 |            0 |         2055 | nan      | nan      | nan      |         nan      | THIN     |
| K11     | tier0_rule                           |            25 |           25 |         2030 |   1.0000 |   1.0000 |   1.0000 |           1.0000 | PASS     |
| C2      | tier0_rule(second factor-group mass) |            25 |           25 |         2055 |   0.8247 |   0.7213 |   0.9124 |         nan      | PASS     |

## Repair gates (Wilson lower bound >= 0.5)

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost |   harm_rate | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|------------:|:---------|
| Q01     |       50 |        39 |         0.780 |   0.648 |   0.872 |        20 |            0 |       0.000 | PASS     |
| Q02     |       50 |        41 |         0.820 |   0.692 |   0.902 |        20 |            0 |       0.000 | PASS     |
| Q03     |       50 |        32 |         0.640 |   0.501 |   0.759 |        20 |            3 |       0.150 | FAIL     |
| Q04     |       50 |        39 |         0.780 |   0.648 |   0.872 |        20 |            1 |       0.050 | PASS     |
| Q05     |       50 |        43 |         0.860 |   0.738 |   0.930 |        20 |            0 |       0.000 | PASS     |
| Q07     |       50 |        44 |         0.880 |   0.762 |   0.944 |        20 |            0 |       0.000 | PASS     |
| Q09     |       50 |        36 |         0.720 |   0.583 |   0.825 |        20 |            1 |       0.050 | PASS     |
| K03     |       50 |        47 |         0.940 |   0.838 |   0.979 |        20 |            0 |       0.000 | PASS     |
| K04     |       50 |        47 |         0.940 |   0.838 |   0.979 |        20 |            0 |       0.000 | PASS     |
| K05     |       50 |        49 |         0.980 |   0.895 |   0.996 |        20 |            0 |       0.000 | PASS     |
| K06     |       50 |        48 |         0.960 |   0.865 |   0.989 |        20 |            0 |       0.000 | PASS     |
| K07     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K08     |       50 |        48 |         0.960 |   0.865 |   0.989 |        20 |            0 |       0.000 | PASS     |
| K09     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R01     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R03     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R05     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R06     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R07     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R10     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R11     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R13     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R15     |       50 |        49 |         0.980 |   0.895 |   0.996 |        20 |            0 |       0.000 | PASS     |
| R19     |       50 |        47 |         0.940 |   0.838 |   0.979 |        20 |            1 |       0.050 | PASS     |
| R22     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R23     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R24     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R25     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R26     |        3 |         3 |         1.000 |   0.438 |   1.000 |        20 |            0 |       0.000 | THIN     |
| K11     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| C2      |       50 |        48 |         0.960 |   0.865 |   0.989 |         0 |            0 |       0.000 | PASS     |

## Dispatch policies (held-out)

| policy            |   threshold |   mean_closure |   mean_closure_v1_28 |   mean_family_attribution |   clean_dispatch_rate |   clean_loss |   clean_net_hit_change |
|:------------------|------------:|---------------:|---------------------:|--------------------------:|----------------------:|-------------:|-----------------------:|
| tau_none_5pct_fpr |      0.4644 |         0.8280 |               0.8171 |                    0.8013 |                0.0459 |       0.0060 |                -0.0038 |
| crc_alpha_0.0025  |      0.0086 |         0.8693 |               0.8614 |                    0.8320 |                0.3692 |       0.0098 |                -0.0060 |
| crc_alpha_0.005   |      0.0004 |         0.8707 |               0.8629 |                    0.8347 |                0.9955 |       0.0128 |                -0.0090 |
| crc_alpha_0.01    |      0.0004 |         0.8707 |               0.8629 |                    0.8347 |                0.9955 |       0.0128 |                -0.0090 |
| crc_alpha_0.02    |      0.0004 |         0.8707 |               0.8629 |                    0.8347 |                0.9955 |       0.0128 |                -0.0090 |

## Loop gates (L1 do-no-harm on held-out clean, L2 mean closure)

```
{
 "alpha": 0.005,
 "lam": 0.00040804650590808844,
 "calibration_n": 811,
 "heldout_clean_loss": 0.012781954887218045,
 "resplit_mean": 0.0030002242647437206,
 "resplit_p95": 0.007300160227879651,
 "L1": "FAIL",
 "L2": "PASS",
 "mean_closure": 0.8706666666666668
}
```

## Family repairs, oracle-dispatched

| fault   | family   |   n |   rescued |   rate |   ci_lo |
|:--------|:---------|----:|----------:|-------:|--------:|
| Q01     | QLEX     |  50 |        34 |  0.680 |   0.542 |
| Q03     | QLEX     |  50 |        26 |  0.520 |   0.385 |
| Q04     | QLEX     |  50 |        35 |  0.700 |   0.562 |
| Q05     | QLEX     |  50 |        42 |  0.840 |   0.715 |
| K04     | STALE    |  50 |        47 |  0.940 |   0.838 |
| R03     | ENC      |  50 |        50 |  1.000 |   0.929 |
| R07     | STALE    |  50 |        50 |  1.000 |   0.929 |
| R10     | ENC      |  50 |        50 |  1.000 |   0.929 |
| R11     | ENC      |  50 |        50 |  1.000 |   0.929 |

## Natural-validation arms NA1-NA6 (no injection, never-examined queries)

| arm   | what                                                            |   n_selected |   hit_before |   hit_after |   delta |   ci_lo |   ci_hi |   fixed |   broken | verdict      |   dispatched |
|:------|:----------------------------------------------------------------|-------------:|-------------:|------------:|--------:|--------:|--------:|--------:|---------:|:-------------|-------------:|
| NA1   | natural misspelling (rule q_correctable)                        |          155 |       0.5613 |      0.4903 | -0.0710 | -0.1419 |  0.0000 |      11 |       22 | INCONCLUSIVE |     nan      |
| NA1b  | NA1 where the corrected query was typed by another ESCI user    |            6 |       0.3333 |      0.3333 |  0.0000 | -0.6667 |  0.6667 |       2 |        2 | INCONCLUSIVE |     nan      |
| NA2   | natural missing space (rule q_segmentable)                      |           53 |       0.5094 |      0.5283 |  0.0189 | -0.0566 |  0.0943 |       3 |        2 | INCONCLUSIVE |     nan      |
| NA3   | natural 'nan' placeholder in top-5 (rule thin5)                 |            8 |       1.0000 |      0.5000 | -0.5000 | -0.8750 | -0.1250 |       0 |        4 | HARM         |     nan      |
| NA4   | natural exact duplicate in top-5 (rule dup5)                    |          125 |       0.3840 |      0.4400 |  0.0560 |  0.0160 |  0.1040 |       8 |        1 | PASS         |     nan      |
| NA5   | natural chunk crowding (rule chunk_crowd5)                      |          621 |       0.5523 |      0.5974 |  0.0451 |  0.0274 |  0.0628 |      32 |        4 | PASS         |     nan      |
| NA6   | closed loop v2 on all natural queries, policy tau_none_5pct_fpr |         1500 |       0.5173 |      0.5180 |  0.0007 | -0.0033 |  0.0047 |       5 |        4 | INCONCLUSIVE |       0.0600 |
| NA6   | closed loop v2 on all natural queries, policy crc_alpha_0.0025  |         1500 |       0.5173 |      0.5133 | -0.0040 | -0.0120 |  0.0040 |      13 |       19 | INCONCLUSIVE |       0.5200 |
| NA6   | closed loop v2 on all natural queries, policy crc_alpha_0.005   |         1500 |       0.5173 |      0.5080 | -0.0093 | -0.0173 | -0.0007 |      13 |       27 | HARM         |       0.9933 |
| NA6   | closed loop v2 on all natural queries, policy crc_alpha_0.01    |         1500 |       0.5173 |      0.5080 | -0.0093 | -0.0173 | -0.0007 |      13 |       27 | HARM         |       0.9933 |
| NA6   | closed loop v2 on all natural queries, policy crc_alpha_0.02    |         1500 |       0.5173 |      0.5080 | -0.0093 | -0.0173 | -0.0007 |      13 |       27 | HARM         |       0.9933 |

## Unseen faults (leave-one-fault-out attributor)

| fault   | family   |   n_test |   flagged |   right_family |   closure |
|:--------|:---------|---------:|----------:|---------------:|----------:|
| Q01     | QLEX     |       25 |     0.600 |          0.480 |     0.320 |
| Q02     | Q02      |       25 |     0.600 |          0.000 |     0.040 |
| Q03     | QLEX     |       25 |     0.560 |          0.480 |     0.280 |
| Q04     | QLEX     |       25 |     0.480 |          0.320 |     0.280 |
| Q05     | QLEX     |       25 |     0.560 |          0.520 |     0.400 |
| Q07     | Q07      |       25 |     0.240 |          0.000 |     0.000 |
| Q09     | Q09      |       25 |     0.320 |          0.000 |     0.000 |
| K03     | K03      |       25 |     1.000 |          0.000 |     0.080 |
| K04     | STALE    |       25 |     0.800 |          0.760 |     0.800 |
| K05     | K05      |       25 |     1.000 |          0.000 |     0.000 |
| K06     | K06      |       25 |     1.000 |          0.000 |     0.000 |
| K08     | K08      |       25 |     0.880 |          0.000 |     0.040 |
| K09     | K09      |       25 |     0.120 |          0.000 |     0.000 |
| R01     | R01      |       25 |     0.240 |          0.000 |     0.040 |
| R03     | ENC      |       25 |     1.000 |          0.880 |     0.920 |
| R05     | R05      |       25 |     0.400 |          0.000 |     0.000 |
| R06     | R06      |       25 |     0.760 |          0.000 |     0.000 |
| R07     | STALE    |       25 |     1.000 |          1.000 |     0.960 |
| R10     | ENC      |       25 |     1.000 |          0.960 |     0.960 |
| R11     | ENC      |       25 |     1.000 |          1.000 |     0.920 |
| R13     | R13      |       25 |     0.320 |          0.000 |     0.040 |
| R19     | R19      |       25 |     1.000 |          0.000 |     0.000 |
| R22     | R22      |       25 |     0.320 |          0.000 |     0.000 |
| R24     | R24      |       25 |     0.520 |          0.000 |     0.000 |

## Closed loop per fault and policy (held-out split)

| policy            |   threshold | fault   | family   |   n_test |   dispatch_rate |   family_attribution_acc |   closure |   clean_loss |   clean_net_hit_change |
|:------------------|------------:|:--------|:---------|---------:|----------------:|-------------------------:|----------:|-------------:|-----------------------:|
| tau_none_5pct_fpr |       0.464 | Q01     | QLEX     |       25 |           0.960 |                    0.960 |     0.680 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | Q02     | Q02      |       25 |           1.000 |                    0.960 |     0.840 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | Q03     | QLEX     |       25 |           0.600 |                    0.520 |     0.360 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | Q04     | QLEX     |       25 |           0.800 |                    0.680 |     0.640 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | Q05     | QLEX     |       25 |           0.680 |                    0.480 |     0.560 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | Q07     | Q07      |       25 |           0.840 |                    0.840 |     0.680 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | Q09     | Q09      |       25 |           1.000 |                    1.000 |     0.800 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | K03     | K03      |       25 |           0.960 |                    0.920 |     0.840 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | K04     | STALE    |       25 |           0.800 |                    0.480 |     0.800 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | K05     | K05      |       25 |           1.000 |                    0.720 |     0.920 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | K06     | K06      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | K07     | K07      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | K08     | K08      |       25 |           0.960 |                    0.880 |     0.920 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | K09     | K09      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R01     | R01      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R03     | ENC      |       25 |           1.000 |                    0.920 |     0.920 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R05     | R05      |       25 |           0.840 |                    0.760 |     0.800 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R06     | R06      |       25 |           0.800 |                    0.720 |     0.760 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R07     | STALE    |       25 |           0.960 |                    0.560 |     0.920 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R10     | ENC      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R11     | ENC      |       25 |           1.000 |                    0.760 |     0.920 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R13     | R13      |       25 |           1.000 |                    0.960 |     1.000 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R15     | R15      |       25 |           1.000 |                    0.880 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R19     | R19      |       25 |           1.000 |                    0.960 |     0.920 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R22     | R22      |       25 |           0.680 |                    0.440 |     0.600 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R23     | R23      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R24     | R24      |       25 |           0.600 |                    0.320 |     0.400 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | R25     | R25      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | K11     | K11      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | C2      | C2       |       25 |           0.920 |                    0.480 |     0.760 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.464 | NONE    | NONE     |     1330 |           0.046 |                    0.954 |   nan     |        0.006 |                 -0.004 |
| crc_alpha_0.0025  |       0.009 | Q01     | QLEX     |       25 |           1.000 |                    1.000 |     0.680 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | Q02     | Q02      |       25 |           1.000 |                    0.960 |     0.840 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | Q03     | QLEX     |       25 |           0.960 |                    0.680 |     0.400 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | Q04     | QLEX     |       25 |           1.000 |                    0.720 |     0.720 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | Q05     | QLEX     |       25 |           1.000 |                    0.640 |     0.760 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | Q07     | Q07      |       25 |           1.000 |                    0.840 |     0.800 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | Q09     | Q09      |       25 |           1.000 |                    1.000 |     0.800 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | K03     | K03      |       25 |           1.000 |                    0.920 |     0.880 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | K04     | STALE    |       25 |           0.920 |                    0.560 |     0.840 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | K05     | K05      |       25 |           1.000 |                    0.720 |     0.920 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | K06     | K06      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | K07     | K07      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | K08     | K08      |       25 |           1.000 |                    0.880 |     0.920 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | K09     | K09      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R01     | R01      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R03     | ENC      |       25 |           1.000 |                    0.920 |     0.920 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R05     | R05      |       25 |           1.000 |                    0.840 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R06     | R06      |       25 |           0.920 |                    0.760 |     0.800 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R07     | STALE    |       25 |           1.000 |                    0.560 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R10     | ENC      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R11     | ENC      |       25 |           1.000 |                    0.760 |     0.920 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R13     | R13      |       25 |           1.000 |                    0.960 |     1.000 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R15     | R15      |       25 |           1.000 |                    0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R19     | R19      |       25 |           1.000 |                    0.960 |     0.920 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R22     | R22      |       25 |           1.000 |                    0.680 |     0.840 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R23     | R23      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R24     | R24      |       25 |           1.000 |                    0.400 |     0.640 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | R25     | R25      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | K11     | K11      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | C2      | C2       |       25 |           1.000 |                    0.480 |     0.760 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.009 | NONE    | NONE     |     1330 |           0.369 |                    0.631 |   nan     |        0.010 |                 -0.006 |
| crc_alpha_0.005   |       0.000 | Q01     | QLEX     |       25 |           1.000 |                    1.000 |     0.680 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | Q02     | Q02      |       25 |           1.000 |                    0.960 |     0.840 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | Q03     | QLEX     |       25 |           1.000 |                    0.720 |     0.400 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | Q04     | QLEX     |       25 |           1.000 |                    0.720 |     0.720 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | Q05     | QLEX     |       25 |           1.000 |                    0.640 |     0.760 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | Q07     | Q07      |       25 |           1.000 |                    0.840 |     0.800 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | Q09     | Q09      |       25 |           1.000 |                    1.000 |     0.800 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | K03     | K03      |       25 |           1.000 |                    0.920 |     0.880 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | K04     | STALE    |       25 |           1.000 |                    0.600 |     0.880 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | K05     | K05      |       25 |           1.000 |                    0.720 |     0.920 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | K06     | K06      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | K07     | K07      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | K08     | K08      |       25 |           1.000 |                    0.880 |     0.920 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | K09     | K09      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R01     | R01      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R03     | ENC      |       25 |           1.000 |                    0.920 |     0.920 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R05     | R05      |       25 |           1.000 |                    0.840 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R06     | R06      |       25 |           1.000 |                    0.760 |     0.800 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R07     | STALE    |       25 |           1.000 |                    0.560 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R10     | ENC      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R11     | ENC      |       25 |           1.000 |                    0.760 |     0.920 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R13     | R13      |       25 |           1.000 |                    0.960 |     1.000 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R15     | R15      |       25 |           1.000 |                    0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R19     | R19      |       25 |           1.000 |                    0.960 |     0.920 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R22     | R22      |       25 |           1.000 |                    0.680 |     0.840 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R23     | R23      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R24     | R24      |       25 |           1.000 |                    0.400 |     0.640 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | R25     | R25      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | K11     | K11      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | C2      | C2       |       25 |           1.000 |                    0.480 |     0.760 |      nan     |                nan     |
| crc_alpha_0.005   |       0.000 | NONE    | NONE     |     1330 |           0.995 |                    0.005 |   nan     |        0.013 |                 -0.009 |
| crc_alpha_0.01    |       0.000 | Q01     | QLEX     |       25 |           1.000 |                    1.000 |     0.680 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q02     | Q02      |       25 |           1.000 |                    0.960 |     0.840 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q03     | QLEX     |       25 |           1.000 |                    0.720 |     0.400 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q04     | QLEX     |       25 |           1.000 |                    0.720 |     0.720 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q05     | QLEX     |       25 |           1.000 |                    0.640 |     0.760 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q07     | Q07      |       25 |           1.000 |                    0.840 |     0.800 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q09     | Q09      |       25 |           1.000 |                    1.000 |     0.800 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K03     | K03      |       25 |           1.000 |                    0.920 |     0.880 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K04     | STALE    |       25 |           1.000 |                    0.600 |     0.880 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K05     | K05      |       25 |           1.000 |                    0.720 |     0.920 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K06     | K06      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K07     | K07      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K08     | K08      |       25 |           1.000 |                    0.880 |     0.920 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K09     | K09      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R01     | R01      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R03     | ENC      |       25 |           1.000 |                    0.920 |     0.920 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R05     | R05      |       25 |           1.000 |                    0.840 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R06     | R06      |       25 |           1.000 |                    0.760 |     0.800 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R07     | STALE    |       25 |           1.000 |                    0.560 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R10     | ENC      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R11     | ENC      |       25 |           1.000 |                    0.760 |     0.920 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R13     | R13      |       25 |           1.000 |                    0.960 |     1.000 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R15     | R15      |       25 |           1.000 |                    0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R19     | R19      |       25 |           1.000 |                    0.960 |     0.920 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R22     | R22      |       25 |           1.000 |                    0.680 |     0.840 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R23     | R23      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R24     | R24      |       25 |           1.000 |                    0.400 |     0.640 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R25     | R25      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K11     | K11      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | C2      | C2       |       25 |           1.000 |                    0.480 |     0.760 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | NONE    | NONE     |     1330 |           0.995 |                    0.005 |   nan     |        0.013 |                 -0.009 |
| crc_alpha_0.02    |       0.000 | Q01     | QLEX     |       25 |           1.000 |                    1.000 |     0.680 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q02     | Q02      |       25 |           1.000 |                    0.960 |     0.840 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q03     | QLEX     |       25 |           1.000 |                    0.720 |     0.400 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q04     | QLEX     |       25 |           1.000 |                    0.720 |     0.720 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q05     | QLEX     |       25 |           1.000 |                    0.640 |     0.760 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q07     | Q07      |       25 |           1.000 |                    0.840 |     0.800 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q09     | Q09      |       25 |           1.000 |                    1.000 |     0.800 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K03     | K03      |       25 |           1.000 |                    0.920 |     0.880 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K04     | STALE    |       25 |           1.000 |                    0.600 |     0.880 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K05     | K05      |       25 |           1.000 |                    0.720 |     0.920 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K06     | K06      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K07     | K07      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K08     | K08      |       25 |           1.000 |                    0.880 |     0.920 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K09     | K09      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R01     | R01      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R03     | ENC      |       25 |           1.000 |                    0.920 |     0.920 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R05     | R05      |       25 |           1.000 |                    0.840 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R06     | R06      |       25 |           1.000 |                    0.760 |     0.800 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R07     | STALE    |       25 |           1.000 |                    0.560 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R10     | ENC      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R11     | ENC      |       25 |           1.000 |                    0.760 |     0.920 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R13     | R13      |       25 |           1.000 |                    0.960 |     1.000 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R15     | R15      |       25 |           1.000 |                    0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R19     | R19      |       25 |           1.000 |                    0.960 |     0.920 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R22     | R22      |       25 |           1.000 |                    0.680 |     0.840 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R23     | R23      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R24     | R24      |       25 |           1.000 |                    0.400 |     0.640 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R25     | R25      |       25 |           1.000 |                    0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K11     | K11      |       25 |           1.000 |                    1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | C2      | C2       |       25 |           1.000 |                    0.480 |     0.760 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | NONE    | NONE     |     1330 |           0.995 |                    0.005 |   nan     |        0.013 |                 -0.009 |
