# Reproduce or extend DiagRAG

Two levels. The first takes about 30 minutes and needs no GPU. The second regenerates a judged run and takes 2 to 4 hours on a free Kaggle T4.

## Level 1 — check that the published tables follow from the published episodes (about 30 minutes, CPU)

```bash
git clone -b core28-kaggle-notebook https://github.com/Muz8786/DiagRAG && cd DiagRAG      # or unzip release/DiagRAG_core28_kaggle.zip
pip install numpy scikit-learn                                                              # nothing else is needed for this level
python verify.py                                                                            # zip only: file checksums and code hashes (about 10 seconds)
python kaggle/reproduce_tables.py kaggle/judged_cpu_run_v4_seed47                          # re-fit every detector from the shipped episodes (about 30 seconds)
python kaggle/reproduce_tables.py kaggle/judged_gpu_v4_seed48
python docs/evidence/diagnose_gate_flips.py kaggle /tmp/flips.json                          # the Q03 and C2 diagnosis (about 4 minutes); needs the episode files from the zip
cd bench && python verify_release.py release_v1 && python quickstart_dev_cv.py release_v1 dev.csv && python score.py --labels release_v1/labels_dev.jsonl --track1 dev.csv
```

What to expect (measured on 16 Nov 2026, scikit-learn 1.9.1):
- `judged_cpu_run_v4_seed47`: **31 of 31** detector AUROCs reproduced, largest difference 0.0000.
- `judged_gpu_v4_seed48`: **27 of 31** reproduced within 0.005. K12 (+0.015), Q03 (+0.017, re-fit 0.7085 against a recorded 0.6914), R03 (-0.041) and R06 (+0.017) differ.
  The detector head does not depend on its model seed, so this is a library or numerical-path difference on Kaggle's stack. Its versions were not recorded in that run; v5 records them. The recorded v4 verdict is unchanged.
- The bench quickstart reports a dev cross-validated AUROC of 0.972.

**What Level 1 shows.** The recorded detector table follows from the recorded telemetry with the shipped code. **What it does not show.** That the episodes themselves are right, which needs Level 2, and anything about repairs or the closed loop.

## Level 2 — regenerate a judged run (2 to 4 hours, free Kaggle T4)

Upload `kaggle/DiagRAG_v4_kaggle.ipynb` (or the v5 notebook when it exists), set GPU T4 x1 and Internet On, and press Run All. No key is needed.
The notebook downloads the corpus, ESCI and Webis-QSpell data, checks each file's size and SHA-256, and writes `diagrag_out/VERDICT.json` and `REPORT.md`.
A fresh run will not match to the last digit (GPU numerics, Kaggle library versions). Compare **verdicts and intervals**, not digits. A different outcome on the 27-detector rule is possible and is a valid result.

## Numbers to compare against

| Quantity | Value | Run |
|---|---|---|
| Detectors / repairs passing (core 28) | 26 / 27, NOT_ADOPTED | v4 GPU seed 48 |
| L1 held-out clean loss; L2 closure | 0.0%; 0.866 | v4 GPU seed 48 |
| Natural-traffic gain (paired Hit@5, n = 1,648) | +2.18 points [+1.27, +3.16] | v4 GPU seed 48 |
| Unseen-fault closure (U1, bar 0.50) | 0.456 (FAIL) | v4 GPU seed 48 |
| Fault-vs-clean AUROC, ours vs RAGLog tier-0 features | 0.977 vs 0.761 | v4 GPU seed 48 |
| LLM-judge diagnosis AUROC (n = 320 / 163 / 169) | 0.754 / 0.731 / 0.642 against 0.975 | `docs/LLM_BASELINES_RESULTS.md` |

The full list, including every failure, is `docs/ROADMAP_V3.md` sections 8 and 9 and `docs/ROADMAP_V4.md`.

## Extending

- **A new diagnoser:** `bench/QUICKSTART.md`. Submit test-split predictions to the maintainer.
- **A new fault:** add an injector, a detector rule or head and a repair in `kaggle/diagrag_v5.py` style, keep the gates as they are, and report the result whichever way it falls.
- **A different stack or domain:** `kaggle/diagrag_port2.py` (SciFact, FiQA) and `kaggle/diagrag_langchain2.py` are the templates.
- **Independent replication:** open an issue or a pull request with your `VERDICT.json`, `JUDGED_PROTOCOL.json` (it records the code hash and, from v5, the library versions) and your hardware. Disagreements are welcome and will be added to the record unedited.

Code and documents in this repository were written by Claude (Anthropic), directed by the repository owner.
