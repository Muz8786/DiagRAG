# DiagRAG core-28 judged run report

Device: cpu. Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2. Last session runtime: 743s.

## Verdict (gates fixed in JUDGED_PROTOCOL.json before results)

```
{
 "detectors_pass": 28,
 "repairs_pass": 28,
 "solved_both": 28,
 "of": 28,
 "verdict": "ADOPTED",
 "clean_net_hit_change": -0.004480955937266617,
 "guarantee": {
  "alpha": 0.005,
  "lam": 0.06820976104398069,
  "heldout_clean_loss": 0.0074682598954443615,
  "resplit_mean": 0.004324410728268735,
  "resplit_p95": 0.009977146417169118,
  "status": "FAIL"
 },
 "policies": [
  {
   "policy": "tau_none_5pct_fpr",
   "threshold": 0.3221747745727125,
   "mean_closure": 0.8200000000000001,
   "mean_attribution": 0.7971428571428572,
   "clean_dispatch_rate": 0.03659447348767737,
   "clean_loss": 0.0022404779686333084,
   "clean_net_hit_change": -0.0007468259895444362
  },
  {
   "policy": "crc_alpha_0.0025",
   "threshold": 0.4914904168674933,
   "mean_closure": 0.8099999999999999,
   "mean_attribution": 0.7928571428571429,
   "clean_dispatch_rate": 0.028379387602688575,
   "clean_loss": 0.0014936519790888724,
   "clean_net_hit_change": -0.0007468259895444362
  },
  {
   "policy": "crc_alpha_0.005",
   "threshold": 0.06820976104398069,
   "mean_closure": 0.852857142857143,
   "mean_attribution": 0.8071428571428572,
   "clean_dispatch_rate": 0.09185959671396565,
   "clean_loss": 0.0074682598954443615,
   "clean_net_hit_change": -0.004480955937266617
  },
  {
   "policy": "crc_alpha_0.01",
   "threshold": 9.612693602423228e-05,
   "mean_closure": 0.8685714285714285,
   "mean_attribution": 0.8285714285714286,
   "clean_dispatch_rate": 1.0,
   "clean_loss": 0.016430171769977596,
   "clean_net_hit_change": -0.01194921583271098
  },
  {
   "policy": "crc_alpha_0.02",
   "threshold": 9.612693602423228e-05,
   "mean_closure": 0.8685714285714285,
   "mean_attribution": 0.8285714285714286,
   "clean_dispatch_rate": 1.0,
   "clean_loss": 0.016430171769977596,
   "clean_net_hit_change": -0.01194921583271098
  }
 ],
 "natural": [
  {
   "set": "natural_typos_esci",
   "policy": "tau_none_5pct_fpr",
   "n": 46,
   "n_fail_before": 33,
   "hit_before": 0.2826086956521739,
   "hit_after": 0.30434782608695654,
   "hit_oracle_repair": 0.32608695652173914,
   "hit_reference": 0.34782608695652173,
   "closure_vs_reference": 0.3333333333333339,
   "dispatched": 0.41304347826086957,
   "to_right_group": 0.41304347826086957
  },
  {
   "set": "natural_typos_esci",
   "policy": "crc_alpha_0.0025",
   "n": 46,
   "n_fail_before": 33,
   "hit_before": 0.2826086956521739,
   "hit_after": 0.2608695652173913,
   "hit_oracle_repair": 0.32608695652173914,
   "hit_reference": 0.34782608695652173,
   "closure_vs_reference": -0.33333333333333304,
   "dispatched": 0.30434782608695654,
   "to_right_group": 0.30434782608695654
  },
  {
   "set": "natural_typos_esci",
   "policy": "crc_alpha_0.005",
   "n": 46,
   "n_fail_before": 33,
   "hit_before": 0.2826086956521739,
   "hit_after": 0.30434782608695654,
   "hit_oracle_repair": 0.32608695652173914,
   "hit_reference": 0.34782608695652173,
   "closure_vs_reference": 0.3333333333333339,
   "dispatched": 0.6304347826086957,
   "to_right_group": 0.6086956521739131
  },
  {
   "set": "natural_typos_esci",
   "policy": "crc_alpha_0.01",
   "n": 46,
   "n_fail_before": 33,
   "hit_before": 0.2826086956521739,
   "hit_after": 0.2826086956521739,
   "hit_oracle_repair": 0.32608695652173914,
   "hit_reference": 0.34782608695652173,
   "closure_vs_reference": 0.0,
   "dispatched": 1.0,
   "to_right_group": 0.9347826086956522
  },
  {
   "set": "natural_typos_esci",
   "policy": "crc_alpha_0.02",
   "n": 46,
   "n_fail_before": 33,
   "hit_before": 0.2826086956521739,
   "hit_after": 0.2826086956521739,
   "hit_oracle_repair": 0.32608695652173914,
   "hit_reference": 0.34782608695652173,
   "closure_vs_reference": 0.0,
   "dispatched": 1.0,
   "to_right_group": 0.9347826086956522
  },
  {
   "set": "natural_superseded_policies",
   "policy": "tau_none_5pct_fpr",
   "n": 36,
   "n_fail_before": 3,
   "hit_before": 0.9166666666666666,
   "hit_after": 0.9166666666666666,
   "hit_oracle_repair": 1.0,
   "hit_reference": 1.0,
   "closure_vs_reference": 0.0,
   "dispatched": 0.5,
   "to_right_group": 0.5
  },
  {
   "set": "natural_superseded_policies",
   "policy": "crc_alpha_0.0025",
   "n": 36,
   "n_fail_before": 3,
   "hit_before": 0.9166666666666666,
   "hit_after": 0.9166666666666666,
   "hit_oracle_repair": 1.0,
   "hit_reference": 1.0,
   "closure_vs_reference": 0.0,
   "dispatched": 0.5,
   "to_right_group": 0.5
  },
  {
   "set": "natural_superseded_policies",
   "policy": "crc_alpha_0.005",
   "n": 36,
   "n_fail_before": 3,
   "hit_before": 0.9166666666666666,
   "hit_after": 0.8888888888888888,
   "hit_oracle_repair": 1.0,
   "hit_reference": 1.0,
   "closure_vs_reference": -0.3333333333333333,
   "dispatched": 0.5555555555555556,
   "to_right_group": 0.5
  },
  {
   "set": "natural_superseded_policies",
   "policy": "crc_alpha_0.01",
   "n": 36,
   "n_fail_before": 3,
   "hit_before": 0.9166666666666666,
   "hit_after": 0.8333333333333334,
   "hit_oracle_repair": 1.0,
   "hit_reference": 1.0,
   "closure_vs_reference": -0.9999999999999987,
   "dispatched": 1.0,
   "to_right_group": 0.6111111111111112
  },
  {
   "set": "natural_superseded_policies",
   "policy": "crc_alpha_0.02",
   "n": 36,
   "n_fail_before": 3,
   "hit_before": 0.9166666666666666,
   "hit_after": 0.8333333333333334,
   "hit_oracle_repair": 1.0,
   "hit_reference": 1.0,
   "closure_vs_reference": -0.9999999999999987,
   "dispatched": 1.0,
   "to_right_group": 0.6111111111111112
  }
 ],
 "unseen_mean_closure": 0.20666666666666667,
 "not_solved": [],
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
 "unseen": "report, not gated: leave-one-fault-out attributor; on the held-out fault test episodes report flagged rate, right-group rate and Hit after dispatch"
}

| fault   | detector   | repair   | solved   |
|:--------|:-----------|:---------|:---------|
| Q01     | PASS       | PASS     | True     |
| Q02     | PASS       | PASS     | True     |
| Q03     | PASS       | PASS     | True     |
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
| Q01     |   1278 |        520 |              378 |     92 |     50 |           25 |          25 |            0 |        0.352 |
| Q02     |   1278 |        279 |                0 |    229 |     50 |           25 |          25 |            0 |        0.179 |
| Q03     |   1278 |        343 |              197 |     96 |     50 |           25 |          25 |            0 |        0.342 |
| Q04     |   1278 |         98 |                3 |     45 |     50 |           25 |          25 |           12 |        0.526 |
| Q05     |   1278 |        259 |               38 |    171 |     50 |           25 |          25 |            0 |        0.226 |
| Q07     |   1333 |        923 |              557 |    316 |     50 |           25 |          25 |            0 |        0.137 |
| Q09     |   1278 |        137 |                0 |     87 |     50 |           25 |          25 |            0 |        0.365 |
| K03     |    892 |        197 |              145 |      2 |     50 |           25 |          25 |            0 |        0.962 |
| K04     |   1278 |         92 |                0 |     42 |     50 |           25 |          25 |            0 |        0.543 |
| K05     |   1278 |        128 |                0 |     78 |     50 |           25 |          25 |            0 |        0.391 |
| K06     |    813 |         58 |                0 |      8 |     50 |           25 |          25 |            0 |        0.862 |
| K07     |    246 |         59 |                0 |      9 |     50 |           25 |          25 |            0 |        0.847 |
| K08     |   1278 |         62 |                0 |     12 |     50 |           25 |          25 |            0 |        0.806 |
| K09     |    282 |         53 |                0 |      3 |     50 |           25 |          25 |            0 |        0.943 |
| R01     |   1278 |        104 |                0 |     54 |     50 |           25 |          25 |            0 |        0.481 |
| R03     |   1278 |        609 |                0 |    559 |     50 |           25 |          25 |            0 |        0.082 |
| R05     |   1278 |         86 |                0 |     36 |     50 |           25 |          25 |            0 |        0.581 |
| R06     |   1278 |         50 |                0 |      0 |     50 |           25 |          25 |            0 |        1     |
| R07     |   1278 |        174 |                0 |    124 |     50 |           25 |          25 |            0 |        0.287 |
| R10     |   1278 |        624 |                0 |    573 |     50 |           25 |          25 |            0 |        0.08  |
| R11     |   1278 |        567 |                0 |    517 |     50 |           25 |          25 |            0 |        0.088 |
| R13     |   1278 |        742 |                0 |    692 |     50 |           25 |          25 |            0 |        0.067 |
| R15     |   1278 |        415 |                0 |    365 |     50 |           25 |          25 |            0 |        0.12  |
| R19     |   1278 |        362 |                0 |    312 |     50 |           25 |          25 |            0 |        0.138 |
| R22     |   1278 |        620 |                0 |    570 |     50 |           25 |          25 |            0 |        0.081 |
| R23     |   1278 |        157 |                0 |    107 |     50 |           25 |          25 |            0 |        0.318 |
| R24     |   1278 |        149 |                0 |     99 |     50 |           25 |          25 |            0 |        0.336 |
| C2      |   1278 |         96 |               14 |     32 |     50 |           25 |          25 |            0 |        0.61  |

## Detector gates (AUROC bar 0.7, min test positives 20)

| fault   | detector                             |   n_pos_train |   n_pos_test |   n_neg_test |   auroc |   ci_lo |   ci_hi |   auroc_vs_clean | status   |
|:--------|:-------------------------------------|--------------:|-------------:|-------------:|--------:|--------:|--------:|-----------------:|:---------|
| Q01     | histgb_head                          |            25 |           25 |         1989 |  0.9947 |  0.9915 |  0.9974 |           0.9984 | PASS     |
| Q02     | histgb_head                          |            25 |           25 |         1989 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| Q03     | histgb_head                          |            25 |           25 |         1989 |  0.9341 |  0.8792 |  0.9740 |           0.9555 | PASS     |
| Q04     | tier0_rule                           |            25 |           25 |         1989 |  0.9658 |  0.9153 |  0.9941 |           0.9711 | PASS     |
| Q05     | histgb_head                          |            25 |           25 |         1989 |  0.9882 |  0.9789 |  0.9956 |           0.9926 | PASS     |
| Q07     | histgb_head                          |            25 |           25 |         1989 |  0.9981 |  0.9940 |  1.0000 |           0.9991 | PASS     |
| Q09     | histgb_head                          |            25 |           25 |         1989 |  0.9996 |  0.9988 |  1.0000 |           0.9995 | PASS     |
| K03     | histgb_head                          |            25 |           25 |         1989 |  0.9997 |  0.9990 |  1.0000 |           0.9999 | PASS     |
| K04     | histgb_head                          |            25 |           25 |         1989 |  0.8045 |  0.6680 |  0.9277 |           0.8140 | PASS     |
| K05     | histgb_head                          |            25 |           25 |         1989 |  0.9997 |  0.9993 |  1.0000 |           0.9999 | PASS     |
| K06     | histgb_head                          |            25 |           25 |         1989 |  0.9999 |  0.9995 |  1.0000 |           1.0000 | PASS     |
| K07     | tier0_rule                           |            25 |           25 |         1989 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K08     | histgb_head                          |            25 |           25 |         1989 |  1.0000 |  0.9999 |  1.0000 |           1.0000 | PASS     |
| K09     | histgb_head                          |            25 |           25 |         1989 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R01     | histgb_head                          |            25 |           25 |         1989 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R03     | histgb_head                          |            25 |           25 |         1989 |  0.9999 |  0.9997 |  1.0000 |           1.0000 | PASS     |
| R05     | histgb_head                          |            25 |           25 |         1989 |  0.9981 |  0.9957 |  0.9997 |           0.9988 | PASS     |
| R06     | histgb_head                          |            25 |           25 |         1989 |  0.9857 |  0.9691 |  0.9979 |           0.9928 | PASS     |
| R07     | histgb_head                          |            25 |           25 |         1989 |  0.9999 |  0.9996 |  1.0000 |           1.0000 | PASS     |
| R10     | histgb_head                          |            25 |           25 |         1989 |  0.9798 |  0.9318 |  1.0000 |           0.9800 | PASS     |
| R11     | histgb_head                          |            25 |           25 |         1989 |  0.9994 |  0.9984 |  1.0000 |           1.0000 | PASS     |
| R13     | histgb_head                          |            25 |           25 |         1989 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R15     | tier0_rule                           |            25 |           25 |         1989 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R19     | histgb_head                          |            25 |           25 |         1989 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R22     | histgb_head                          |            25 |           25 |         1989 |  0.9900 |  0.9772 |  0.9995 |           0.9924 | PASS     |
| R23     | tier0_rule                           |            25 |           25 |         1989 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R24     | histgb_head                          |            25 |           25 |         1989 |  0.9199 |  0.8220 |  0.9966 |           0.9302 | PASS     |
| C2      | tier0_rule(second factor-group mass) |            25 |           25 |         2014 |  0.8232 |  0.7161 |  0.9213 |         nan      | PASS     |

## Repair gates (Wilson lower bound >= 0.5)

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost |   harm_rate | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|------------:|:---------|
| Q01     |       50 |        43 |         0.860 |   0.738 |   0.930 |        20 |            0 |       0.000 | PASS     |
| Q02     |       50 |        41 |         0.820 |   0.692 |   0.902 |        20 |            0 |       0.000 | PASS     |
| Q03     |       50 |        32 |         0.640 |   0.501 |   0.759 |        20 |            0 |       0.000 | PASS     |
| Q04     |       50 |        42 |         0.840 |   0.715 |   0.917 |        20 |            0 |       0.000 | PASS     |
| Q05     |       50 |        43 |         0.860 |   0.738 |   0.930 |        20 |            0 |       0.000 | PASS     |
| Q07     |       50 |        43 |         0.860 |   0.738 |   0.930 |        20 |            0 |       0.000 | PASS     |
| Q09     |       50 |        41 |         0.820 |   0.692 |   0.902 |        20 |            0 |       0.000 | PASS     |
| K03     |       50 |        44 |         0.880 |   0.762 |   0.944 |        20 |            0 |       0.000 | PASS     |
| K04     |       50 |        43 |         0.860 |   0.738 |   0.930 |        20 |            0 |       0.000 | PASS     |
| K05     |       50 |        48 |         0.960 |   0.865 |   0.989 |        20 |            0 |       0.000 | PASS     |
| K06     |       50 |        48 |         0.960 |   0.865 |   0.989 |        20 |            0 |       0.000 | PASS     |
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
| R19     |       50 |        46 |         0.920 |   0.812 |   0.968 |        20 |            1 |       0.050 | PASS     |
| R22     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R23     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R24     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| C2      |       50 |        43 |         0.860 |   0.738 |   0.930 |         0 |            0 |       0.000 | PASS     |

## Dispatch policies (held-out)

| policy            |   threshold |   mean_closure |   mean_attribution |   clean_dispatch_rate |   clean_loss |   clean_net_hit_change |
|:------------------|------------:|---------------:|-------------------:|----------------------:|-------------:|-----------------------:|
| tau_none_5pct_fpr |      0.3222 |         0.8200 |             0.7971 |                0.0366 |       0.0022 |                -0.0007 |
| crc_alpha_0.0025  |      0.4915 |         0.8100 |             0.7929 |                0.0284 |       0.0015 |                -0.0007 |
| crc_alpha_0.005   |      0.0682 |         0.8529 |             0.8071 |                0.0919 |       0.0075 |                -0.0045 |
| crc_alpha_0.01    |      0.0001 |         0.8686 |             0.8286 |                1.0000 |       0.0164 |                -0.0119 |
| crc_alpha_0.02    |      0.0001 |         0.8686 |             0.8286 |                1.0000 |       0.0164 |                -0.0119 |

## Do-no-harm guarantee

```
{
 "alpha": 0.005,
 "lam": 0.06820976104398069,
 "heldout_clean_loss": 0.0074682598954443615,
 "resplit_mean": 0.004324410728268735,
 "resplit_p95": 0.009977146417169118,
 "status": "FAIL"
}
```

## Natural faults (no injection)

| set                         | policy            |   n |   n_fail_before |   hit_before |   hit_after |   hit_oracle_repair |   hit_reference |   closure_vs_reference |   dispatched |   to_right_group |
|:----------------------------|:------------------|----:|----------------:|-------------:|------------:|--------------------:|----------------:|-----------------------:|-------------:|-----------------:|
| natural_typos_esci          | tau_none_5pct_fpr |  46 |              33 |        0.283 |       0.304 |               0.326 |           0.348 |                  0.333 |        0.413 |            0.413 |
| natural_typos_esci          | crc_alpha_0.0025  |  46 |              33 |        0.283 |       0.261 |               0.326 |           0.348 |                 -0.333 |        0.304 |            0.304 |
| natural_typos_esci          | crc_alpha_0.005   |  46 |              33 |        0.283 |       0.304 |               0.326 |           0.348 |                  0.333 |        0.630 |            0.609 |
| natural_typos_esci          | crc_alpha_0.01    |  46 |              33 |        0.283 |       0.283 |               0.326 |           0.348 |                  0.000 |        1.000 |            0.935 |
| natural_typos_esci          | crc_alpha_0.02    |  46 |              33 |        0.283 |       0.283 |               0.326 |           0.348 |                  0.000 |        1.000 |            0.935 |
| natural_superseded_policies | tau_none_5pct_fpr |  36 |               3 |        0.917 |       0.917 |               1.000 |           1.000 |                  0.000 |        0.500 |            0.500 |
| natural_superseded_policies | crc_alpha_0.0025  |  36 |               3 |        0.917 |       0.917 |               1.000 |           1.000 |                  0.000 |        0.500 |            0.500 |
| natural_superseded_policies | crc_alpha_0.005   |  36 |               3 |        0.917 |       0.889 |               1.000 |           1.000 |                 -0.333 |        0.556 |            0.500 |
| natural_superseded_policies | crc_alpha_0.01    |  36 |               3 |        0.917 |       0.833 |               1.000 |           1.000 |                 -1.000 |        1.000 |            0.611 |
| natural_superseded_policies | crc_alpha_0.02    |  36 |               3 |        0.917 |       0.833 |               1.000 |           1.000 |                 -1.000 |        1.000 |            0.611 |

## Unseen faults (leave-one-fault-out attributor)

| fault   |   n_test |   flagged |   right_group |   closure |
|:--------|---------:|----------:|--------------:|----------:|
| Q01     |       25 |     0.360 |         0.280 |     0.000 |
| Q02     |       25 |     0.480 |         0.320 |     0.040 |
| Q03     |       25 |     0.600 |         0.560 |     0.000 |
| Q04     |       25 |     0.640 |         0.480 |     0.000 |
| Q05     |       25 |     0.280 |         0.200 |     0.000 |
| Q07     |       25 |     0.000 |         0.000 |     0.000 |
| Q09     |       25 |     0.120 |         0.040 |     0.000 |
| K03     |       25 |     1.000 |         0.640 |     0.200 |
| K04     |       25 |     0.760 |         0.000 |     0.720 |
| K05     |       25 |     1.000 |         0.960 |     0.040 |
| K06     |       25 |     1.000 |         1.000 |     0.000 |
| K08     |       25 |     0.920 |         0.400 |     0.280 |
| K09     |       25 |     0.560 |         0.000 |     0.000 |
| R01     |       25 |     0.200 |         0.080 |     0.000 |
| R03     |       25 |     1.000 |         0.920 |     0.880 |
| R05     |       25 |     0.160 |         0.040 |     0.000 |
| R06     |       25 |     0.640 |         0.440 |     0.000 |
| R07     |       25 |     1.000 |         0.040 |     0.760 |
| R10     |       25 |     1.000 |         0.960 |     0.920 |
| R11     |       25 |     1.000 |         0.960 |     0.960 |
| R13     |       25 |     0.240 |         0.160 |     0.000 |
| R19     |       25 |     1.000 |         1.000 |     0.000 |
| R22     |       25 |     0.360 |         0.080 |     0.120 |
| R24     |       25 |     0.200 |         0.040 |     0.040 |

## Closed loop per fault and policy (held-out split)

| policy            |   threshold | fault   |   n_test |   dispatch_rate |   attribution_acc |   closure |   clean_loss |   clean_net_hit_change |
|:------------------|------------:|:--------|---------:|----------------:|------------------:|----------:|-------------:|-----------------------:|
| tau_none_5pct_fpr |       0.322 | Q01     |       25 |           1.000 |             0.960 |     0.840 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | Q02     |       25 |           1.000 |             1.000 |     0.760 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | Q03     |       25 |           0.640 |             0.200 |     0.120 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | Q04     |       25 |           0.640 |             0.440 |     0.480 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | Q05     |       25 |           0.720 |             0.560 |     0.640 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | Q07     |       25 |           0.920 |             0.920 |     0.880 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | Q09     |       25 |           0.960 |             0.920 |     0.840 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | K03     |       25 |           1.000 |             0.920 |     0.800 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | K04     |       25 |           0.720 |             0.480 |     0.720 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | K05     |       25 |           1.000 |             0.880 |     0.920 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | K06     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | K07     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | K08     |       25 |           1.000 |             1.000 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | K09     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R01     |       25 |           1.000 |             0.960 |     1.000 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R03     |       25 |           1.000 |             0.840 |     0.920 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R05     |       25 |           0.960 |             0.840 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R06     |       25 |           0.680 |             0.560 |     0.680 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R07     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R10     |       25 |           1.000 |             0.960 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R11     |       25 |           1.000 |             0.840 |     0.920 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R13     |       25 |           0.920 |             0.800 |     0.880 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R15     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R19     |       25 |           1.000 |             1.000 |     0.960 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R22     |       25 |           0.760 |             0.680 |     0.720 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R23     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | R24     |       25 |           0.560 |             0.480 |     0.520 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | C2      |       25 |           0.920 |             0.440 |     0.600 |      nan     |                nan     |
| tau_none_5pct_fpr |       0.322 | NONE    |     1339 |           0.037 |             0.963 |   nan     |        0.002 |                 -0.001 |
| crc_alpha_0.0025  |       0.491 | Q01     |       25 |           1.000 |             0.960 |     0.840 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | Q02     |       25 |           1.000 |             1.000 |     0.760 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | Q03     |       25 |           0.560 |             0.160 |     0.120 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | Q04     |       25 |           0.640 |             0.440 |     0.480 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | Q05     |       25 |           0.680 |             0.560 |     0.600 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | Q07     |       25 |           0.920 |             0.920 |     0.880 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | Q09     |       25 |           0.920 |             0.920 |     0.800 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | K03     |       25 |           1.000 |             0.920 |     0.800 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | K04     |       25 |           0.680 |             0.480 |     0.680 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | K05     |       25 |           1.000 |             0.880 |     0.920 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | K06     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | K07     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | K08     |       25 |           1.000 |             1.000 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | K09     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R01     |       25 |           1.000 |             0.960 |     1.000 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R03     |       25 |           1.000 |             0.840 |     0.920 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R05     |       25 |           0.920 |             0.840 |     0.920 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R06     |       25 |           0.680 |             0.560 |     0.680 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R07     |       25 |           0.960 |             0.840 |     0.920 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R10     |       25 |           1.000 |             0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R11     |       25 |           1.000 |             0.840 |     0.920 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R13     |       25 |           0.880 |             0.760 |     0.840 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R15     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R19     |       25 |           1.000 |             1.000 |     0.960 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R22     |       25 |           0.760 |             0.680 |     0.720 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R23     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | R24     |       25 |           0.520 |             0.480 |     0.480 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | C2      |       25 |           0.880 |             0.440 |     0.600 |      nan     |                nan     |
| crc_alpha_0.0025  |       0.491 | NONE    |     1339 |           0.028 |             0.972 |   nan     |        0.001 |                 -0.001 |
| crc_alpha_0.005   |       0.068 | Q01     |       25 |           1.000 |             0.960 |     0.840 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | Q02     |       25 |           1.000 |             1.000 |     0.760 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | Q03     |       25 |           0.800 |             0.240 |     0.200 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | Q04     |       25 |           0.920 |             0.480 |     0.720 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | Q05     |       25 |           0.840 |             0.560 |     0.760 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | Q07     |       25 |           1.000 |             0.920 |     0.920 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | Q09     |       25 |           0.960 |             0.920 |     0.840 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | K03     |       25 |           1.000 |             0.920 |     0.800 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | K04     |       25 |           0.760 |             0.480 |     0.720 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | K05     |       25 |           1.000 |             0.880 |     0.920 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | K06     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | K07     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | K08     |       25 |           1.000 |             1.000 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | K09     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R01     |       25 |           1.000 |             0.960 |     1.000 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R03     |       25 |           1.000 |             0.840 |     0.920 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R05     |       25 |           0.960 |             0.840 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R06     |       25 |           0.800 |             0.680 |     0.800 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R07     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R10     |       25 |           1.000 |             0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R11     |       25 |           1.000 |             0.840 |     0.920 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R13     |       25 |           1.000 |             0.800 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R15     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R19     |       25 |           1.000 |             1.000 |     0.960 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R22     |       25 |           0.840 |             0.760 |     0.800 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R23     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | R24     |       25 |           0.800 |             0.480 |     0.680 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | C2      |       25 |           0.960 |             0.440 |     0.600 |      nan     |                nan     |
| crc_alpha_0.005   |       0.068 | NONE    |     1339 |           0.092 |             0.908 |   nan     |        0.007 |                 -0.004 |
| crc_alpha_0.01    |       0.000 | Q01     |       25 |           1.000 |             0.960 |     0.840 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q02     |       25 |           1.000 |             1.000 |     0.760 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q03     |       25 |           1.000 |             0.320 |     0.200 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q04     |       25 |           1.000 |             0.520 |     0.720 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q05     |       25 |           1.000 |             0.600 |     0.800 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q07     |       25 |           1.000 |             0.920 |     0.920 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | Q09     |       25 |           1.000 |             0.960 |     0.840 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K03     |       25 |           1.000 |             0.920 |     0.800 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K04     |       25 |           1.000 |             0.560 |     0.720 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K05     |       25 |           1.000 |             0.880 |     0.920 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K06     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K07     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K08     |       25 |           1.000 |             1.000 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | K09     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R01     |       25 |           1.000 |             0.960 |     1.000 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R03     |       25 |           1.000 |             0.840 |     0.920 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R05     |       25 |           1.000 |             0.880 |     1.000 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R06     |       25 |           1.000 |             0.760 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R07     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R10     |       25 |           1.000 |             0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R11     |       25 |           1.000 |             0.840 |     0.920 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R13     |       25 |           1.000 |             0.800 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R15     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R19     |       25 |           1.000 |             1.000 |     0.960 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R22     |       25 |           1.000 |             0.840 |     0.880 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R23     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | R24     |       25 |           1.000 |             0.600 |     0.800 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | C2      |       25 |           1.000 |             0.440 |     0.600 |      nan     |                nan     |
| crc_alpha_0.01    |       0.000 | NONE    |     1339 |           1.000 |             0.000 |   nan     |        0.016 |                 -0.012 |
| crc_alpha_0.02    |       0.000 | Q01     |       25 |           1.000 |             0.960 |     0.840 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q02     |       25 |           1.000 |             1.000 |     0.760 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q03     |       25 |           1.000 |             0.320 |     0.200 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q04     |       25 |           1.000 |             0.520 |     0.720 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q05     |       25 |           1.000 |             0.600 |     0.800 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q07     |       25 |           1.000 |             0.920 |     0.920 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | Q09     |       25 |           1.000 |             0.960 |     0.840 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K03     |       25 |           1.000 |             0.920 |     0.800 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K04     |       25 |           1.000 |             0.560 |     0.720 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K05     |       25 |           1.000 |             0.880 |     0.920 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K06     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K07     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K08     |       25 |           1.000 |             1.000 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | K09     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R01     |       25 |           1.000 |             0.960 |     1.000 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R03     |       25 |           1.000 |             0.840 |     0.920 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R05     |       25 |           1.000 |             0.880 |     1.000 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R06     |       25 |           1.000 |             0.760 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R07     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R10     |       25 |           1.000 |             0.960 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R11     |       25 |           1.000 |             0.840 |     0.920 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R13     |       25 |           1.000 |             0.800 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R15     |       25 |           1.000 |             0.880 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R19     |       25 |           1.000 |             1.000 |     0.960 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R22     |       25 |           1.000 |             0.840 |     0.880 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R23     |       25 |           1.000 |             1.000 |     1.000 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | R24     |       25 |           1.000 |             0.600 |     0.800 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | C2      |       25 |           1.000 |             0.440 |     0.600 |      nan     |                nan     |
| crc_alpha_0.02    |       0.000 | NONE    |     1339 |           1.000 |             0.000 |   nan     |        0.016 |                 -0.012 |
