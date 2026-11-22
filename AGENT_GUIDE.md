# Guide for an AI agent: download DiagRAG locally, understand it, explain it to the owner

Your job: (1) download everything from the links below, (2) read it in the order given, (3) check that it is intact, (4) explain the project to the owner in plain language, with the real numbers and the failures. Do not change any file while doing this.

## 1. Links

| What | Link | Access |
|---|---|---|
| Code, docs, judged runs, paper (public) | https://github.com/Muz8786/DiagRAG, branch `core28-kaggle-notebook` | public |
| Small package (26 MB, everything except data) | https://raw.githubusercontent.com/Muz8786/DiagRAG/core28-kaggle-notebook/release/DiagRAG_KAGGLE_A_to_Z_LITE.zip | public |
| Full data package, 13 parts (1.18 GB) | https://github.com/Muz8786/diagrag-data/tree/a-to-z-full-parts/a_to_z_full | **private**, needs the owner's GitHub access |
| Paper (LaTeX and compiled PDF) | `paper/diagrag_ieee.tex`, `paper/diagrag_ieee.pdf` in the public repo | public |

## 2. Download

```bash
git clone --branch core28-kaggle-notebook --single-branch https://github.com/Muz8786/DiagRAG.git
# optional, only if you have access to the private repo:
git clone --branch a-to-z-full-parts --single-branch https://github.com/Muz8786/diagrag-data.git
cd diagrag-data/a_to_z_full && python merge_parts.py          # must print: OK ... sha256 2f70a33b762675c6ee81fc1ebb3e610dcad334699910b54bdcf3328cb47750a1
unzip DiagRAG_KAGGLE_A_to_Z.zip                               # 1.34 GB unpacked
```
The public repo alone is enough to understand the project and read every result. The full zip is only needed to re-run things.

## 3. Check it is intact

```bash
cd DiagRAG_KAGGLE_A_to_Z && python verify.py      # expect: RESULT: ALL OK   (the LITE zip has the same verify.py)
```
It checks every file's SHA-256 and that every judged run's recorded code hash matches the shipped script.

## 4. Read in this order

1. `PROJECT_EXPLAINED.md`, section 0 (one page), then sections 2, 5, 7, 10, 11.
2. `A_TO_Z_GUIDE.md` (what is in the package, how the Kaggle notebook works).
3. `paper/diagrag_ieee.pdf` (the short, citable version).
4. `docs/evidence/v7_composed_protocol.md` and `docs/evidence/qml_protocol.md` (examples of the pre-registration and amendment style).
5. `docs/ROADMAP_V4.md`, section 13 (latest state), and `docs/ALL_RUNS_MATRIX.md` (every judged run).
6. Evidence files: `docs/evidence/diagnosis_confusion_v6cpu.json` (per-fault precision, recall, F1), `kaggle/judged_cpu_run_v7_seed50/COMPOSED_RESULT.json`, `docs/evidence/natural_split_by_gold_v7cpu.json`.

## 5. What to explain to the owner (use this structure)

1. **The problem** in two sentences: RAG retrieval fails silently; can telemetry alone find and fix the cause?
2. **What was built:** 32 injectable faults, 63 telemetry features, a gradient-boosted attributor, a dispatcher with repairs, and a conformal gate that bounds harm to healthy queries.
3. **How the evidence is kept honest:** gates and code hashes are written before results; failures stay in the tables.
4. **The results, with numbers:** judged runs (11 rows, two NOT_ADOPTED), detection AUROC 0.977, exact fault identification 89.9% on faulted held-out episodes, natural-traffic gain +2.43 points, composed faults 40.0% named, simulated QML (no advantage).
5. **What failed or is weak** (say these before the owner is asked): author-injected faults, one corpus, U1 0.41 against a 0.50 bar, Q03 never identified, dispatcher cannot name two faults of one group, natural gain comes from two rules, no frontier-LLM arm, artefacts not released.
6. **The honest score** (about 7.8/10) and what it would take to reach more (`A_TO_Z_GUIDE.md` section 9).
7. **What you could not verify,** and what you assumed.

Rules for your explanation: quote numbers only from the files; say which run each number comes from; separate pre-registered results from post-hoc ones; do not call 0.977 AUROC an accuracy; do not call the QML result an advantage.

## 6. Do not

- Edit `kaggle/diagrag_v6.py`, `kaggle/diagrag_v7.py` or `kaggle/v7_cells/*` (their hashes are frozen).
- Publish, share or re-upload the full data zip: it contains third-party material and corpus rows with unsettled licences (`data/DATA_NOTICE.md` inside the zip).
- Write any API key or token into a file. The package needs none to read or verify.
