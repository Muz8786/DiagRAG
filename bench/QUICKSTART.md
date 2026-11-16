# DiagRAG-Bench quickstart (about 5 minutes, CPU only)

You need Python 3.9+ with `numpy` and `scikit-learn`. Everything below runs from the files in this package.

```bash
python verify_release.py release_v1                 # 1. check the files against MANIFEST.json
python quickstart_dev_cv.py release_v1 dev_pred.csv # 2. a reference diagnoser, 5-fold cross-validated on the dev split
python score.py --labels release_v1/labels_dev.jsonl --track1 dev_pred.csv   # 3. score it
```

**Your own diagnoser.** Edit `fit_predict` in `quickstart_dev_cv.py`. The input is a 63-feature telemetry vector per episode (`telemetry_dev.csv`), computed from the retrieval trace only.
The output is `p_fault` (higher = more likely faulty) and a `family` (see `release_v1/families.json`) for each episode.

**Test split.** `release_v1/telemetry_test.csv` and `episodes_test.jsonl` have no labels. Predict them with the same CSV format and send the file to the maintainer, who scores it against the private labels. Their SHA-256 is in `MANIFEST.json`, so the scores can be checked later.
The reference baseline for the test split is `baseline_track1.py`:  `python baseline_track1.py release_v1 test_pred.csv`.

**What the dev score is.** Dev episodes from the same base query can fall in different folds, which could inflate a cross-validated score. For the reference baseline the quickstart's dev figure (AUROC 0.972, detection rate at 5% false alarm 0.892, family accuracy 0.841) was **not** above its score on the private test split (0.976, 0.917, 0.863), so on this one measurement the inflation is not visible. It has not been measured with a grouped split, and one baseline does not show it for every method. The test split uses held-out base queries.
**What the benchmark is not.** The faults are injected into a retrieval stack built on e-commerce search; read `DATASHEET.md` before you generalise from a score.
