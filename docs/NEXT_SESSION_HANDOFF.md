# Handoff to the next session

Written 15 Nov 2026 at the end of the session that built v1 → v3. Read this first, then `docs/ROADMAP_V3.md`.

## 0. Your mission

The owner's goal is **9/10 novelty without changing the core theme**. The core theme is telemetry-only diagnosis
across the Q/K/R/C fault groups, cause-dispatched repair, and recovery measured against an oracle.

- **Honest position today:** about 7/10. That is my estimate, not a measurement.
- **What 9 means:** a reviewer must see results nobody else has, earned under frozen gates. It cannot come from
  better wording.
- **Rules that do not bend:**
  - gates and the code hash are frozen before any reported run;
  - held-out data is never tuned on;
  - failures are reported exactly like successes;
  - no invented numbers;
  - observed, hypothesised and concluded are kept separate.

  Those rules are why the current numbers are believable. Do not trade them for a higher score.

## 1. Where things are

| What | Where |
|---|---|
| Code | `Muz8786/DiagRAG`, branch `core28-kaggle-notebook`, PR #1 (open) |
| Notebooks | `kaggle/diagrag_core28.py` (v1), `diagrag_v2.py`, `diagrag_v3.py`, `diagrag_v4.py` (current flagship), `diagrag_langchain2.py`, `diagrag_port.py` / `diagrag_port2.py` (second stack: SciFact, FiQA), `diagrag_langchain.py` (framework stack). The `.ipynb` files are built with `kaggle/build_notebook.py` |
| Judged results | `kaggle/judged_*` folders. Every one holds a protocol file whose `code_sha256` equals its `.py` |
| Evidence, plan, record | `docs/EVIDENCE_AND_NOVELTY_REPORT.md` (42 field reports, fault verdicts), `docs/ROADMAP_V3.md` (Phases A–E results), `docs/IDENTIFIABILITY.md` (theory), `docs/CROSSWALK_CATALOGUE.md` |
| Benchmark | `bench/` (DiagRAG-Bench v1.0, scorer, datasheet). The private test labels are **not** in the repo; their hash is in `bench/release_v1/MANIFEST.json` |
| Release zips | `release/DiagRAG_FULL_PROJECT_A_to_Z.zip`, `release/DiagRAG_RUN_PACKAGE.zip` (the older `DiagRAG_core28_kaggle.zip` was superseded and removed); the single-file Kaggle notebook is `kaggle/DiagRAG_v4_kaggle.ipynb` (built by `kaggle/build_final_notebook.py`) |
| Data | corpus and cache on Google Drive (IDs in `data/DATA_MANIFEST.md`); ESCI from GitHub LFS; Webis-QSpell-17 from Zenodo; BEIR from UKP. All are SHA-256 checked inside the notebooks |
| The other project | `Muz8786/diagrag-data` (private): the 47-fault catalogue DiagRAG. **Keep it separate unless the owner approves a merge** (the fault IDs collide) |

## 2. API keys — what each one is

None are stored in this repository, by design: the repo is public.

| Key | What it is | Account | Use it for |
|---|---|---|---|
| Kaggle API token …039a (`KGAT_…`) | Kaggle API, new token format | `muzammilveil99` | **Main DiagRAG account.** Owns `qml-banks`. Use it for the GPU runs |
| Kaggle API token …e2e5 | Kaggle API | `syedmuzammilquadri` | spare account, e.g. for a parallel GPU run |
| Kaggle API token …a623 | Kaggle API | `sqmuzammil` | spare account |

How to use a key:
1. Ask the owner to provide it as an **environment variable**, `KAGGLE_API_TOKEN`, rather than in chat.
2. Then run, for example, `KAGGLE_API_TOKEN=$KEY python -m kaggle kernels list --mine`. The Kaggle CLI needs `six`.
3. In this sandbox `~/.config` is read-only, so set `HOME` and `KAGGLE_CONFIG_DIR` to a temporary directory.

All three were checked working on 15 Nov 2026. They were pasted in chat, so **the owner was advised to regenerate
them**. If they fail, ask for fresh ones.

There are **no LLM keys** (no OpenAI, Anthropic or Gemini), **no Hugging Face token**, and no AWS keys. Ask for an LLM
key if you need the LLM-based baselines in §3.

Pushing a notebook or using GPU quota on someone's Kaggle account is an external action. **Confirm with the owner
first.** The last proposal was `muzammilveil99`, private notebook. That proposal was not yet confirmed.

## 3.0 Status on 16 Nov 2026 (written after the list below was first drafted)

Done, with judged evidence (all in `docs/ROADMAP_V3.md` sections 8 and 9):
- GPU flagship, twice: v3 seed 46 (ADOPTED, 27/28) and v4 seed 48 (**NOT_ADOPTED**, 26/28 detectors). Loop gates L1, L2, N1 and the diagnosis-vs-diagnosis-free closure test D1 pass on both. **U1 fails on both** (0.395, 0.456).
- LangChain v2: 11/15, exactly at the bar, with fixes designed after v1 (7/15).
- LLM-based baselines on free-tier APIs: diagnosis (B1) beaten by telemetry on three models; repair (B2) comparable to CRAG-style but non-inferiority **not shown**.
- Item 2 below is partly done (LangChain, U1 improved but still under 0.50). Item 3 is done in a narrow form (not full RAGLog, not the CRAG paper).

Still open: U1 >= 0.50 on a fresh seed, Q03 detection (fails the detector gate in 3 of 7 judged runs), natural misspelling repair (harms), diagnosis beating a
diagnosis-free stack on accuracy (D3 fails twice), the full LLM-based baselines with a paid model, and Phase E. Do not rerun the same flagship hoping for a pass:
a gate change after seeing results is not allowed, and a different seed is a new run to report, pass or fail.

## 3. The road from ~7 to 9, in order

Each step names the gate to pre-register. If a step fails, report it as failed.

1. **GPU flagship.**
   - Run `diagrag_v3.ipynb` on a Kaggle T4 with bge-reranker-large, on a new seed. It resumes from checkpoints.
   - Also run `diagrag_port2` with `DATASET=fiqa` and `scifact` on GPU.
   - Every number so far is CPU with MiniLM.
2. **Fix the known misses, then re-judge them on new seeds:**
   - **U1, unseen-fault closure:** 0.365 against a target of 0.50. Idea: more shared group repairs, and a group
     classifier trained without fault labels.
   - **LangChain stack:** 7/15 against a target of 11. Known bugs:
     - K08: filter thin documents *before* reranking. The current code only reorders them.
     - R23: detect it from the dense-leg count, not the final result count.
     - K05: lower the `EmbeddingsRedundantFilter` threshold.
   - **K04 stale vector:** fails on every non-shopping stack. The probe depth or the probe itself is the suspect.
   - **R26:** needs a selective (~1%) tenant filter to become testable.
3. **External baselines that use an LLM:**
   - RAGLog's full system (repo `hiraa221/raglog`, Apache-2.0, pinned commit `7f7d0686…`);
   - a CRAG-style evaluator;
   both on the never-examined natural queries.
4. **Natural failures beyond rules:**
   - natural misspellings are unsolved: our repair is −4.9 points, SymSpell −11.4;
   - natural paraphrase (Q03) is undetectable from telemetry (AUROC 0.56).
   A real win on either is new.
5. **Make diagnosis earn its keep.** Today, on natural traffic, the classifier adds nothing over two detection-gated
   rules, and a diagnosis-free stack matches the loop at twice the cost. Show a regime where diagnosis beats both with
   statistical significance, for example cost-constrained dispatch.
6. **Phase E — adoption.**
   - Public release with a DOI (Zenodo) and a leaderboard on the private split.
   - Other groups using the suite.
   This is what separates 8 from 9, and it cannot be scheduled.

## 4. Open owner decisions

1. Merge with the 47-fault catalogue project? Needs namespaced IDs.
2. Where to keep the private test labels? They existed only in the old sandbox at `/projects/sandbox/_private/`;
   regenerate them with `bench/make_release.py` from the v3 checkpoint if needed.
3. A ShopNova licence, before any data release.
4. Which Kaggle account to use, and confirmation to start GPU runs.

## 5. Operational lessons from this sandbox

- **Command limit:** commands are cut at 30 minutes and background jobs get killed. Run long jobs as resumable chunks
  with `TIME_BUDGET`; see `_work/chunk_v3.sh`, recreated from `kaggle/run_local.sh`.
- **Checkpoint rollbacks:** the sandbox has sometimes reverted checkpoint files between calls. Keep a backup and a
  `LAST_STAGE` file, and restore if they disagree.
- **One chunk per tool call:** parallel tool calls on the same run collide. Use a `flock` lock.
- **`pkill` pattern:** never `pkill -f` a pattern that also appears in your own command line. It kills your shell.
