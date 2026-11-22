# DiagRAG portability arm v2 (nq) — judged run

```
{
 "domain": "BEIR nq",
 "stack": "e5-small-v2 + FAISS HNSW + BM25 + min-max fusion + MiniLM-L6 reranker",
 "clean_hit5": {
  "train": 0.6923076923076923,
  "test": 0.6764705882352942
 },
 "detectors_pass": 0,
 "repairs_pass": 0,
 "solved_both": 0,
 "of": 20,
 "suite_ports": false,
 "not_solved": [
  "Q01",
  "Q03",
  "Q04",
  "Q05",
  "K04",
  "K05",
  "K08",
  "R01",
  "R03",
  "R05",
  "R07",
  "R10",
  "R11",
  "R13",
  "R15",
  "R19",
  "R22",
  "R23",
  "R24",
  "R25"
 ],
 "purity": {
  "docs": 2681468,
  "unique_ids": 2681468,
  "empty": 507,
  "exact_dup_rows": 11278,
  "queries_with_qrels": {
   "train": 52,
   "test": 68
  },
  "hnsw_ef128_recall10_vs_exact": 0.985
 },
 "verify": {
  "nq": {
   "bytes": 498307926,
   "sha256": "2553bf7bfbab47b1436ca00a34bce57320e18e611fd00999a2a3a1b4714be752"
  },
  "qspell": {
   "bytes": 2285705,
   "sha256": "f13bd165544ab2ac75d63de4334feb86d74d1b3dfbe48d79423133552b5054e4"
  }
 }
}
```

## Episodes

| fault   |   pool |   attempts |   not_applicable |   easy |   hard |   hard_train |   hard_test |   hard_yield |
|:--------|-------:|-----------:|-----------------:|-------:|-------:|-------------:|------------:|-------------:|
| Q01     |     82 |         57 |               51 |      4 |      2 |            1 |           1 |        0.333 |
| Q03     |     82 |         60 |               57 |      2 |      1 |            0 |           1 |        0.333 |
| Q04     |     82 |          2 |                0 |      0 |      2 |            1 |           1 |        1     |
| Q05     |     82 |          4 |                0 |      2 |      2 |            1 |           1 |        0.5   |
| K04     |     82 |          5 |                0 |      3 |      2 |            1 |           1 |        0.4   |
| K05     |     82 |          5 |                0 |      3 |      2 |            1 |           1 |        0.4   |
| K08     |     82 |          5 |                0 |      3 |      2 |            1 |           1 |        0.4   |
| R01     |     82 |          8 |                0 |      6 |      2 |            1 |           1 |        0.25  |
| R03     |     82 |          6 |                0 |      4 |      2 |            1 |           1 |        0.333 |
| R05     |     82 |          3 |                0 |      1 |      2 |            1 |           1 |        0.667 |
| R07     |     82 |          6 |                0 |      4 |      2 |            1 |           1 |        0.333 |
| R10     |     82 |          9 |                0 |      7 |      2 |            1 |           1 |        0.222 |
| R11     |     82 |          6 |                0 |      4 |      2 |            1 |           1 |        0.333 |
| R13     |     82 |         60 |                0 |     59 |      1 |            0 |           1 |        0.017 |
| R15     |     82 |         10 |                0 |      8 |      2 |            1 |           1 |        0.2   |
| R19     |     82 |          7 |                0 |      5 |      2 |            1 |           1 |        0.286 |
| R22     |     82 |         13 |                0 |     11 |      2 |            1 |           1 |        0.154 |
| R23     |     82 |          4 |                0 |      2 |      2 |            1 |           1 |        0.5   |
| R24     |     82 |          6 |                0 |      4 |      2 |            1 |           1 |        0.333 |
| R25     |     82 |          3 |                0 |      1 |      2 |            1 |           1 |        0.667 |

## Detector gates

| fault   | detector    |   n_pos_train |   n_pos_test | status    |    auroc |    ci_lo |    ci_hi |
|:--------|:------------|--------------:|-------------:|:----------|---------:|---------:|---------:|
| Q01     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| Q03     | histgb_head |             0 |            1 | UNTRAINED | nan      | nan      | nan      |
| Q04     | tier0_rule  |             1 |            1 | THIN      |   1.0000 |   1.0000 |   1.0000 |
| Q05     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| K04     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| K05     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| K08     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| R01     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| R03     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| R05     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| R07     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| R10     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| R11     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| R13     | histgb_head |             0 |            1 | UNTRAINED | nan      | nan      | nan      |
| R15     | tier0_rule  |             1 |            1 | THIN      |   1.0000 |   1.0000 |   1.0000 |
| R19     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| R22     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| R23     | tier0_rule  |             1 |            1 | THIN      |   1.0000 |   1.0000 |   1.0000 |
| R24     | histgb_head |             1 |            1 | UNTRAINED | nan      | nan      | nan      |
| R25     | tier0_rule  |             1 |            1 | THIN      |   1.0000 |   1.0000 |   1.0000 |

## Repair gates

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|:---------|
| Q01     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| Q03     |        1 |         1 |         1.000 |   0.207 |   1.000 |         3 |            0 | THIN     |
| Q04     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| Q05     |        2 |         1 |         0.500 |   0.095 |   0.905 |         3 |            0 | THIN     |
| K04     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| K05     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| K08     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R01     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R03     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R05     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R07     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R10     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R11     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R13     |        1 |         1 |         1.000 |   0.207 |   1.000 |         3 |            0 | THIN     |
| R15     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R19     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            1 | THIN     |
| R22     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R23     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R24     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
| R25     |        2 |         2 |         1.000 |   0.342 |   1.000 |         3 |            0 | THIN     |
