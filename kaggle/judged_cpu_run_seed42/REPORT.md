# DiagRAG core-28 judged run report

Device: cpu. Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2. Last session runtime: 792s.

## Verdict (gates fixed in JUDGED_PROTOCOL.json before results)

```
{
 "detectors_pass": 28,
 "repairs_pass": 27,
 "solved_both": 27,
 "of": 28,
 "verdict": "ADOPTED",
 "clean_net_hit_change": -0.010606060606060607,
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
 "DETECT_TARGET": 27
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
| C2      | PASS       | PASS     | True     |

## Data verification

|        | file                                      |     bytes | size_ok   | sha256                                                           | sha_ok   |
|:-------|:------------------------------------------|----------:|:----------|:-----------------------------------------------------------------|:---------|
| corpus | kb_tier3_186k.jsonl.gz                    |  53518791 | True      | 5a9f7ea6ae5b8a3e7f1e1ca6e2838dddd6158efb9384d757c6aa755dbe9bda3c | True     |
| cache  | embeddings_cache_186k.npz                 | 533012659 | True      | 3b43603d9689f7c0eee0cbfebdb8b5cfddd05a2fc4e3cf192c8eed1de4a88835 | True     |
| esci   | shopping_queries_dataset_examples.parquet |  51286808 | True      | 4a735b693b4a424a6fc67f5be6e4c811495c488bbf66d02a602d308b2744263a | True     |
| qspell | corpus-webis-qspell-17.zip                |   2285705 | True      | f13bd165544ab2ac75d63de4334feb86d74d1b3dfbe48d79423133552b5054e4 | True     |

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
 "query_log_queries": 94945
}
```

## Episode generation (hard = clean succeeds, faulted fails)

| fault   |   pool |   attempts |   not_applicable |   easy |   hard |   hard_train |   hard_test |   real_typos |   hard_yield |
|:--------|-------:|-----------:|-----------------:|-------:|-------:|-------------:|------------:|-------------:|-------------:|
| Q01     |   1283 |        649 |              488 |    110 |     50 |           25 |          25 |            0 |        0.311 |
| Q02     |   1283 |        272 |                0 |    222 |     50 |           25 |          25 |            0 |        0.184 |
| Q03     |   1283 |        385 |              228 |    107 |     50 |           25 |          25 |            0 |        0.318 |
| Q04     |   1283 |        100 |                1 |     49 |     50 |           25 |          25 |           13 |        0.505 |
| Q05     |   1283 |        193 |               29 |    114 |     50 |           25 |          25 |            0 |        0.305 |
| Q07     |   1351 |        901 |              529 |    322 |     50 |           25 |          25 |            0 |        0.134 |
| Q09     |   1283 |        136 |                0 |     86 |     50 |           25 |          25 |            0 |        0.368 |
| K03     |    910 |        187 |              136 |      1 |     50 |           25 |          25 |            0 |        0.98  |
| K04     |   1283 |         86 |                0 |     36 |     50 |           25 |          25 |            0 |        0.581 |
| K05     |   1283 |        126 |                0 |     76 |     50 |           25 |          25 |            0 |        0.397 |
| K06     |    831 |         54 |                0 |      4 |     50 |           25 |          25 |            0 |        0.926 |
| K07     |    246 |         68 |                0 |     18 |     50 |           25 |          25 |            0 |        0.735 |
| K08     |   1283 |         63 |                0 |     13 |     50 |           25 |          25 |            0 |        0.794 |
| K09     |    282 |         53 |                0 |      3 |     50 |           25 |          25 |            0 |        0.943 |
| R01     |   1283 |        103 |                0 |     53 |     50 |           25 |          25 |            0 |        0.485 |
| R03     |   1283 |        659 |                0 |    609 |     50 |           25 |          25 |            0 |        0.076 |
| R05     |   1283 |         95 |                0 |     45 |     50 |           25 |          25 |            0 |        0.526 |
| R06     |   1283 |         50 |                0 |      0 |     50 |           25 |          25 |            0 |        1     |
| R07     |   1283 |        172 |                0 |    122 |     50 |           25 |          25 |            0 |        0.291 |
| R10     |   1283 |        704 |                0 |    653 |     50 |           25 |          25 |            0 |        0.071 |
| R11     |   1283 |        582 |                0 |    532 |     50 |           25 |          25 |            0 |        0.086 |
| R13     |   1283 |        807 |                0 |    757 |     50 |           25 |          25 |            0 |        0.062 |
| R15     |   1283 |        428 |                0 |    378 |     50 |           25 |          25 |            0 |        0.117 |
| R19     |   1283 |        403 |                0 |    353 |     50 |           25 |          25 |            0 |        0.124 |
| R22     |   1283 |        749 |                0 |    699 |     50 |           25 |          25 |            0 |        0.067 |
| R23     |   1283 |        129 |                0 |     79 |     50 |           25 |          25 |            0 |        0.388 |
| R24     |   1283 |        138 |                0 |     88 |     50 |           25 |          25 |            0 |        0.362 |
| C2      |   1283 |        115 |               27 |     38 |     50 |           25 |          25 |            0 |        0.568 |

## Detector gates (AUROC bar 0.7, min test positives 20)

| fault   | detector                             |   n_pos_train |   n_pos_test |   n_neg_test |   auroc |   ci_lo |   ci_hi |   auroc_vs_clean | status   |
|:--------|:-------------------------------------|--------------:|-------------:|-------------:|--------:|--------:|--------:|-----------------:|:---------|
| Q01     | histgb_head                          |            25 |           25 |         1970 |  0.9981 |  0.9962 |  0.9994 |           0.9988 | PASS     |
| Q02     | histgb_head                          |            25 |           25 |         1970 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| Q03     | histgb_head                          |            25 |           25 |         1970 |  0.8655 |  0.7691 |  0.9504 |           0.8928 | PASS     |
| Q04     | tier0_rule                           |            25 |           25 |         1970 |  0.9946 |  0.9879 |  0.9993 |           0.9963 | PASS     |
| Q05     | histgb_head                          |            25 |           25 |         1970 |  0.9564 |  0.8696 |  0.9960 |           0.9583 | PASS     |
| Q07     | histgb_head                          |            25 |           25 |         1970 |  0.9998 |  0.9993 |  1.0000 |           0.9997 | PASS     |
| Q09     | histgb_head                          |            25 |           25 |         1970 |  0.9989 |  0.9975 |  1.0000 |           0.9991 | PASS     |
| K03     | histgb_head                          |            25 |           25 |         1970 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K04     | histgb_head                          |            25 |           25 |         1970 |  0.8439 |  0.7159 |  0.9493 |           0.8635 | PASS     |
| K05     | histgb_head                          |            25 |           25 |         1970 |  0.9997 |  0.9991 |  1.0000 |           0.9997 | PASS     |
| K06     | histgb_head                          |            25 |           25 |         1970 |  0.9994 |  0.9985 |  0.9999 |           0.9999 | PASS     |
| K07     | tier0_rule                           |            25 |           25 |         1970 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K08     | histgb_head                          |            25 |           25 |         1970 |  0.9938 |  0.9813 |  1.0000 |           0.9929 | PASS     |
| K09     | histgb_head                          |            25 |           25 |         1970 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R01     | histgb_head                          |            25 |           25 |         1970 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R03     | histgb_head                          |            25 |           25 |         1970 |  0.9998 |  0.9995 |  1.0000 |           1.0000 | PASS     |
| R05     | histgb_head                          |            25 |           25 |         1970 |  0.9969 |  0.9923 |  0.9998 |           0.9990 | PASS     |
| R06     | histgb_head                          |            25 |           25 |         1970 |  0.9937 |  0.9877 |  0.9980 |           0.9975 | PASS     |
| R07     | histgb_head                          |            25 |           25 |         1970 |  0.9704 |  0.9088 |  0.9996 |           0.9755 | PASS     |
| R10     | histgb_head                          |            25 |           25 |         1970 |  0.9798 |  0.9266 |  1.0000 |           0.9800 | PASS     |
| R11     | histgb_head                          |            25 |           25 |         1970 |  0.9866 |  0.9719 |  0.9981 |           0.9951 | PASS     |
| R13     | histgb_head                          |            25 |           25 |         1970 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R15     | tier0_rule                           |            25 |           25 |         1970 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R19     | histgb_head                          |            25 |           25 |         1970 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R22     | histgb_head                          |            25 |           25 |         1970 |  0.9437 |  0.8558 |  0.9999 |           0.9454 | PASS     |
| R23     | tier0_rule                           |            25 |           25 |         1970 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R24     | histgb_head                          |            25 |           25 |         1970 |  0.9836 |  0.9550 |  0.9989 |           0.9881 | PASS     |
| C2      | tier0_rule(second factor-group mass) |            25 |           25 |         1995 |  0.8076 |  0.6906 |  0.9036 |         nan      | PASS     |

## Repair gates (Wilson lower bound >= 0.5)

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost |   harm_rate | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|------------:|:---------|
| Q01     |       50 |        40 |         0.800 |   0.670 |   0.888 |        20 |            0 |       0.000 | PASS     |
| Q02     |       50 |        40 |         0.800 |   0.670 |   0.888 |        20 |            0 |       0.000 | PASS     |
| Q03     |       50 |        28 |         0.560 |   0.423 |   0.688 |        20 |            0 |       0.000 | FAIL     |
| Q04     |       50 |        37 |         0.740 |   0.604 |   0.841 |        20 |            0 |       0.000 | PASS     |
| Q05     |       50 |        46 |         0.920 |   0.812 |   0.968 |        20 |            0 |       0.000 | PASS     |
| Q07     |       50 |        43 |         0.860 |   0.738 |   0.930 |        20 |            0 |       0.000 | PASS     |
| Q09     |       50 |        39 |         0.780 |   0.648 |   0.872 |        20 |            0 |       0.000 | PASS     |
| K03     |       50 |        46 |         0.920 |   0.812 |   0.968 |        20 |            0 |       0.000 | PASS     |
| K04     |       50 |        41 |         0.820 |   0.692 |   0.902 |        20 |            0 |       0.000 | PASS     |
| K05     |       50 |        48 |         0.960 |   0.865 |   0.989 |        20 |            0 |       0.000 | PASS     |
| K06     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K07     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K08     |       50 |        48 |         0.960 |   0.865 |   0.989 |        20 |            0 |       0.000 | PASS     |
| K09     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R01     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R03     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R05     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R06     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R07     |       50 |        49 |         0.980 |   0.895 |   0.996 |        20 |            0 |       0.000 | PASS     |
| R10     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R11     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R13     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R15     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R19     |       50 |        46 |         0.920 |   0.812 |   0.968 |        20 |            0 |       0.000 | PASS     |
| R22     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R23     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R24     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| C2      |       50 |        45 |         0.900 |   0.786 |   0.957 |         0 |            0 |       0.000 | PASS     |

## Closed loop (held-out split)

| fault   |   n_test |   dispatch_rate |   attribution_acc |   closure |   clean_net_hit_change |
|:--------|---------:|----------------:|------------------:|----------:|-----------------------:|
| Q01     |       25 |           1.000 |             0.040 |     0.160 |                nan     |
| Q02     |       25 |           1.000 |             0.880 |     0.640 |                nan     |
| Q03     |       25 |           0.760 |             0.080 |     0.160 |                nan     |
| Q04     |       25 |           1.000 |             0.760 |     0.800 |                nan     |
| Q05     |       25 |           0.960 |             0.440 |     0.760 |                nan     |
| Q07     |       25 |           0.960 |             0.920 |     0.880 |                nan     |
| Q09     |       25 |           1.000 |             0.840 |     0.720 |                nan     |
| K03     |       25 |           1.000 |             0.920 |     0.880 |                nan     |
| K04     |       25 |           0.760 |             0.280 |     0.640 |                nan     |
| K05     |       25 |           0.960 |             0.680 |     0.760 |                nan     |
| K06     |       25 |           1.000 |             0.680 |     0.760 |                nan     |
| K07     |       25 |           1.000 |             1.000 |     1.000 |                nan     |
| K08     |       25 |           1.000 |             0.880 |     0.920 |                nan     |
| K09     |       25 |           1.000 |             1.000 |     1.000 |                nan     |
| R01     |       25 |           1.000 |             0.960 |     0.960 |                nan     |
| R03     |       25 |           1.000 |             0.680 |     0.800 |                nan     |
| R05     |       25 |           0.880 |             0.800 |     0.840 |                nan     |
| R06     |       25 |           0.760 |             0.640 |     0.640 |                nan     |
| R07     |       25 |           0.920 |             0.320 |     0.720 |                nan     |
| R10     |       25 |           1.000 |             0.760 |     0.840 |                nan     |
| R11     |       25 |           1.000 |             0.760 |     0.880 |                nan     |
| R13     |       25 |           1.000 |             0.840 |     1.000 |                nan     |
| R15     |       25 |           1.000 |             0.880 |     0.960 |                nan     |
| R19     |       25 |           1.000 |             0.720 |     0.760 |                nan     |
| R22     |       25 |           0.920 |             0.680 |     0.760 |                nan     |
| R23     |       25 |           1.000 |             0.880 |     0.960 |                nan     |
| R24     |       25 |           0.800 |             0.480 |     0.640 |                nan     |
| C2      |       25 |           1.000 |             0.240 |     0.480 |                nan     |
| NONE    |     1320 |           0.103 |             0.897 |   nan     |                 -0.011 |
