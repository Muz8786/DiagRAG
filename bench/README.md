# DiagRAG-Bench v1.0 — telemetry-only diagnosis and repair of retrieval failures

A benchmark of retrieval-stage failures. Every episode is labelled by cause, and every fault carries an evidence tier
tied to field reports. Built from the v3 judged run (`kaggle/judged_cpu_run_v3_seed45/`, code SHA-256 `a59311c6…515c`).

## Contents (`release_v1/`)

| File | Public | What |
|---|---|---|
| `episodes_dev.jsonl` | yes | 2,718 train-split episodes: query, tenant, k, pipeline state, injected documents (marked synthetic) |
| `labels_dev.jsonl` | yes | dev labels: fault, family, group, k, gold doc ids, clean Hit@5 |
| `telemetry_dev.csv` | yes | the telemetry feature vector of every dev episode |
| `episodes_test.jsonl`, `telemetry_test.csv` | yes | 2,125 held-out episodes, **without labels** |
| `labels_test.jsonl` | **no** | private. Its SHA-256 is in `MANIFEST.json` (`private_test_labels_sha256`) |
| `families.json` | yes | fault → family (repair-equivalence class) → group, plus evidence tier S/M/P/N |
| `MANIFEST.json` | yes | version, SHA-256 of every public file, the private-label commitment |

## Tracks

- **Track 1 — diagnosis from telemetry.** Submit `episode_id, p_fault, family` for the test episodes. The scorer reports:
  - fault-vs-clean AUROC with a 95% CI;
  - detection rate at a 5% clean false-alarm rate;
  - family accuracy, overall and per family;
  - family false alarms on clean episodes.
- **Track 2 — repair.** Run your system on each episode with the harness in `kaggle/diagrag_v3.py`, which reconstructs
  the pipeline state, and submit `episode_id, top5`. The scorer reports:
  - rescue rate per fault;
  - clean Hit@5 loss.

```bash
python bench/score.py --labels bench/release_v1/labels_dev.jsonl --track1 my_dev_predictions.csv
```

Test-split scores are produced by the maintainer from the private labels and can be checked against the published hash.

## Reference results on the private test split

| System | Fault-vs-clean AUROC | Detect @ 5% false alarm | Family accuracy | Family false alarm on clean |
|---|---|---|---|---|
| `baseline_track1.py` (HistGB on public dev telemetry) | 0.976 [0.969, 0.982] | 0.917 | 0.863 | 0.027 |

The same run also scored external detection baselines on the held-out episodes (`detection_baselines.csv`):

| Method | AUROC [95% CI] |
|---|---|
| DiagRAG attributor (1 − P(NONE)) | 0.977 [0.969, 0.982] |
| RAGLog tier-0 feature set (authors' code, commit 7f7d068, no LLM checks), same classifier | 0.756 [0.735, 0.775] |
| RAGLog tier-0, best single feature (`rt_best_rank`, chosen on train) | 0.668 [0.644, 0.689] |
| QPP: −NQC (Shtok et al.) / −WIG (Zhou & Croft) on BM25 | 0.583 / 0.566 |
| −max cross-encoder score | 0.672 [0.644, 0.696] |

How to read the RAGLog comparison:
- It favours us. Our telemetry includes probes designed for the faults in this suite.
- RAGLog's LLM-based checks were not run (no API key in the build environment). Its authors report that those checks
  contribute the most.

## Evidence tiers

A **grounded** fault has tier S or M. The headline results use only the 22 grounded faults. The 10 tier-N/P faults are
in the suite but quarantined from headline claims. Tier definitions and sources: `docs/EVIDENCE_AND_NOVELTY_REPORT.md` §2.

Licences and the datasheet: `DATASHEET.md` and `../NOTICE.md`.
