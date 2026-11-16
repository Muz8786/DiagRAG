# DiagRAG — Publication Repo (structure, private for now)

A clean, reviewer-facing copy of DiagRAG, laid out so anyone can
find the result, the code that produced it, and the picture that
shows it, without digging through the working workspace.

## Structure

- `README.md` — this file. Start here.
- `data/` — what the data are, where to fetch them, and how to
  verify them. Large data files are NOT in Git (see below).
  Item 2 in the requested structure is taken here as `data/`.
  If you meant a different folder for item 2, rename it in one
  line — the rest of the structure does not change.
- `models/` — the models used, what each one does, and where its
  weights come from. Model weights are downloaded automatically
  on first run from Hugging Face, they are not committed here.
- `cache/` — the embeddings and other caches: what they are,
  their exact sizes, and how to fetch and verify them. The
  cache files themselves are NOT in Git.
- `figures/` — bar graphs and charts for the paper, all made
  from verified result files only, plus `figures.md`, a
  Markdown document you can open and edit in any Markdown
  editor (Typora, Obsidian, VS Code preview, or GitHub preview)
  with every figure embedded and captioned.
- `kaggle/DiagRAG_v4_kaggle.ipynb` — **the one-file Kaggle notebook**. It embeds the frozen `diagrag_v4.py`, checks its SHA-256
  and runs the judged GPU configuration (about 2 h 10 min on a T4). Judged result of that configuration: NOT_ADOPTED, 26/28
  detectors (27 needed), 27/28 repairs. See `docs/ROADMAP_V3.md` section 8.
- `kaggle/` — the other notebooks (v1 to v4, port, port2, LangChain v1 and v2), their `.py` sources, `build_notebook.py`,
  `build_final_notebook.py`, and one `judged_*` folder per judged run. See `kaggle/README.md`.
- `release/DiagRAG_core28_kaggle.zip` — the single package: the Kaggle notebook, all code, every judged run with its
  episode file, the benchmark (without private labels), the docs, `verify.py` and `CHECKSUMS.sha256`. Start with
  `README_RUN_ON_KAGGLE.md` inside it.
- `docs/ROADMAP_V3.md` — execution record of roadmap Phases A–E (v3,
  port2, LangChain): every gate, result, failure and remaining decision.
- `bench/` — DiagRAG-Bench v1.0: public dev episodes, unlabelled
  held-out episodes, scorer, datasheet, reference baseline.
- `docs/IDENTIFIABILITY.md`, `docs/CROSSWALK_CATALOGUE.md`, `NOTICE.md`.
- `docs/EVIDENCE_AND_NOVELTY_REPORT.md` — field evidence for every
  fault, verdicts, missing faults, the natural-validation, portability
  and loop findings, and the execution record of the v2 and portability
  judged runs. Raw evidence is in `docs/evidence/`.
- `docs/CORE28_FAULTS.md` — for each core fault: the problem, the
  episodes, the detector and the repair.
- `paper/` — the publication paper outline, with sections,
  headline numbers, and honest boundaries. The canonical
  manuscript is separate; do not edit it from here.

## How a reviewer uses this repo

1. Read this README, then `data/DATA_LINKS.txt`.
2. Run the setup in the replication package (setup.sh), fetch
   the data, verify sizes with download_data.py --check-only.
3. Run the CPU tests in minutes for an exact check, or the
   GPU loop in 2-3 hours on a T4-class GPU for an interval check.
   See REPRODUCIBILITY.md in the replication package.
4. Open `figures/figures.md` in a Markdown editor to see every
   result picture with its source and its caveat.

## What is NOT in Git, and why

- Corpus: 53,518,791 bytes — fits a normal Git push, but is
  kept outside Git with the other data so the repo stays small.
- Embeddings cache: 533,012,659 bytes — GitHub blocks normal
  Git pushes over 100 MB per file. It fits as a GitHub Release
  asset (under 2 GiB each), and fits Zenodo (up to 50 GB per
  record, with a DOI). See `cache/README.md` and
  `data/DATA_LINKS.txt` for the Drive mirror links and the
  Zenodo route for the permanent archive.
