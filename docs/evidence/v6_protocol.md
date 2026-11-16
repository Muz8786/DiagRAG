# v6 protocol (pre-registration). Written 17 Nov 2026, before any v6 run and before any v6 result.

## 0. Where v6 comes from, said plainly

v5 (CPU seed 49) was **NOT_ADOPTED**: 24 of 28 detectors (27 needed). Three of the four missing detectors (R03, R15, R22) have held-out AUROC 1.000, 0.988 and 0.968 and were marked THIN, not failed, because they produced only 38, 44 and 47 held-out positives against the 50 that v5 itself required.
The fourth, Q03, fails by expectation (`docs/ROADMAP_V4.md` section 11.1).
The reason for the three THIN results was first diagnosed wrongly (a loop-budget flaw) and then corrected (`docs/ROADMAP_V4.md` section 11.4): the injectors for those faults are deterministic, so each base query can give at most one episode, only 7 to 9% of base queries are hard, and the **test half of the 2,400 base queries supplies about 39, 46 and 45** hard episodes. The floor of 50 cannot be met from that pool. The first v6 draft (a loop-budget fix) was discarded before any run because a simulation showed it would change nothing.
**v6 exists because of the v5 result.** It is a new version with a design change motivated by a diagnosed construction limit, not by a held-out score. v5 stays in the record and in the all-runs matrix as NOT_ADOPTED. Nothing below edits v5.

## 1. What is fixed (identical to v5)
Every gate and bar: detector AUROC >= 0.70 with >= 50 held-out positives (else THIN); repair Wilson lower bound >= 0.50, <= 10% clean loss, >= 50 hard episodes; adoption >= 27 detectors and >= 24 repairs; L1 0.005, L2 0.70, U1 0.50, N1 interval above zero; the policy table and four targets; the deployed configuration (natural-misspelling repair off); the three-way accounting with the original 28 as headline; the pre-registered analysis `analysis_gpu_plan.py`; the natural-traffic sample (1,648 never-examined queries, `natural_exclusions_v2.json`).

## 2. What changes (two construction fixes; declared here, before any v6 run)
- **D1, base-query supply.** `N_BASE_ESCI` 2,400 -> 6,000, which takes **all 5,527** already-examined ESCI queries as bases. The 1,648 never-examined natural queries are a separate pool and are untouched. Expected effect (from the v5 yields): one pass over the larger test half supplies roughly 90 to 105 hard episodes for R03, R15 and R22, enough to reach 50.
  Side effects declared in advance: more clean episodes in the test split (a larger denominator for the clean-loss figures); a smaller natural-calibration share of the census; longer runtime.
- **D2, C2 pair mix.** C2 chooses the fault pair with the fewest accepted episodes in the episode's own split (ties by fewest attempts; a pair with 25 attempts and no accepted episode in that split is treated as stuck). This balances the pair mix between train and test, which the diagnosis found to be random and unbalanced in v4 (`docs/ROADMAP_V4.md` section 11.2). Unit-tested on stubs: both splits fill in 40/40 simulations, pair-count spread 1.0 against 8.3 for random choice.

## 3. The runs
- Code: `kaggle/diagrag_v6.py`, generated from v5 by `kaggle/mk_v6.py` (SHA-256 recorded in amendment C1 below before the run starts).
- **Run 1, the flagship: GPU (Kaggle T4, bge-reranker-large), seed 50, one run.** Settings `SEED=50, N_BASE_ESCI=6000, N_PRDC=528, N_HARD=100, MAX_ATT=4000, N_HARM=20`. Seed 50 is the next integer after the last used seed (49); it was chosen before any v6 result and no run has used it.
- **Run 2, a stack replication: CPU (MiniLM-L6), the same seed and settings.** Both runs are pre-registered here, run independently, and reported side by side in the all-runs matrix whichever way each falls. **Neither is chosen after seeing the other.** The headline is Run 1 (GPU). If Run 1 cannot complete, Run 2 is the headline and the matrix says so.
- No seed-shopping: one GPU run and one CPU run at seed 50. A second GPU run, a second CPU run, or another seed needs the owner's explicit approval.
- The environment (library versions) is recorded in each run's protocol file. The embedded script and its hash are tied to this protocol by `verify.py`.

## 4. Predictions, written down so they can fail (my judgements from the v5 record, not guarantees)
- **R03, R15, R22 reach 50 held-out positives and pass** (AUROC >= 0.95 in v5): probability about 0.8 that all three do. If one stays THIN, the supply estimate was too optimistic.
- **Q03 detector FAIL** (real-pair era mean 0.643 [0.600, 0.687]): about 0.9.
- **C2 PASS** with the pair mix balanced: about 0.9.
- **27-detector rule met** (needs every detector except at most one to pass): about 0.7. The main risks are a THIN fault, C2, and any new fault that falls just below 0.70 with a larger test split.
- **U1 >= 0.50:** about 0.1 (v5 0.440; nothing in v6 targets it).
- **L1, L2, N1 PASS:** about 0.9 each. N1 should be near +2.4 points because the natural sample is unchanged.
- **`capped_crc_0.005` meets all four targets again:** about 0.8.

## 5. What a result would and would not show
- ADOPTED with Q03 FAIL: the 27-detector rule is met with zero slack; it shows the three THIN faults were a construction limit, not weak detectors.
- NOT_ADOPTED: reported with the same prominence; the per-fault table says which detector.
- A GPU/CPU disagreement on the verdict is itself a result and is reported.
- v6 does not address the unseen-fault bar, the LLM comparison, the second-corpus port or the release.

## 6. Amendments

**C1 — v6 code frozen (17 Nov 2026; no v6 run exists).** `kaggle/diagrag_v6.py` is generated from `kaggle/diagrag_v5.py` by `kaggle/mk_v6.py` (asserted replacements; `diff v5 v6` shows them). The frozen v6 hash is now `44176b9a5ad633e39ec29581237d9919619b9944471178effb172be1d276e28a`.
Checks done before this freeze: the generator runs and its output parses; the D2 selection rule was unit-tested on stubs (and a first version that let a never-yielding pair block the others was caught and fixed before any compute). Not checked yet at this point: the full pipeline on tiny settings (done next, result recorded in C2) and any GPU run.

**C2 — checks done before the runs (17 Nov 2026; no v6 run exists).** (1) `docs/evidence/preflight_v6.py` passes: the frozen hash equals the shipped code; the gate line is byte-identical to v5; the unchanged bars are present; the notebook config equals section 3 (seed 50, `N_BASE_ESCI=6000`); the notebook embeds exactly the frozen file and asserts its hash before running.
(2) A CPU smoke on tiny hard quotas (`N_HARD=6`) with the **full** 6,000-query base pool ran through generation, oracle repair, calibration, the closed loop and natural traffic (1,445 s) and was stopped by its time budget before the final stages; it raised no error. It confirmed D1 (5,527 ESCI bases: train 3,696, test 2,236; per-fault pool 2,977 against 1,307 in v5) and showed the cost: the closed-loop stage is about 1.7x longer because the clean test set grew. Its numbers are meaningless and are not used.
(3) The final stages (detection baselines, leave-one-fault-out, verdict) were not exercised at v6 scale; they ran unchanged in v5.
Execution parameter, not a gate: the Kaggle notebook uses `TIME_BUDGET=30000` seconds so the script stops itself and saves its checkpoint inside Kaggle's session limit; the CPU replication uses 1,400-second chunks.

**C3 — execution note (17 Nov 2026, 13:32 UTC).** Run 1 (GPU) was pushed to Kaggle as `sqmuzammil/diagrag-v6-gpu-flagship` from the unmodified notebook `kaggle/DiagRAG_v6_kaggle.ipynb` with its pre-registered configuration (seed 50). A GPU smoke of the same notebook with tiny settings (`sqmuzammil/diagrag-v6-gpu-smoke`) had completed first: CUDA on a Tesla T4, no traceback, protocol hash equal to the frozen v6 hash, the library versions recorded (scikit-learn 1.6.1, numpy 2.1.3, torch 2.11.0+cu130 on Kaggle), all stages through the verdict in 1,268 s. Its numbers are meaningless and are not used.
Run 2 (CPU, seed 50, the pre-registered stack replication) starts in the sandbox in the same session, as section 3 allows. Neither run's output is read by the other.

**C4 — the single GPU run was relocated to another Kaggle account (17 Nov 2026, 15:37 UTC; no v6 result read).** The run launched at 13:32 on `sqmuzammil` stayed QUEUED for more than two hours although a GPU smoke on the same account had started within minutes. I deleted that kernel (the CLI confirmed "deleted successfully" and a status query on it was then denied, so it could not start), and pushed the **same notebook file** (SHA-256 prefix `ddb071a014816d49`, unchanged; configuration unchanged) to `syedmuzammilquadri/diagrag-v6-gpu-flagship`, which went to RUNNING within 45 seconds.
It is one GPU run: the first job never executed, so no result of it exists. Only the account differs; nothing about the code, seed or settings changed.
