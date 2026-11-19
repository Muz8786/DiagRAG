# v12 cost-measurement protocol (pre-registration). Written 19 Nov 2026, before any cost-weight sensitivity result and before any timing was taken.

## 0. Why
The "cost" in the policy tables (`docs/ALL_RUNS_MATRIX.md`, targets T3, gate D2) is a sum of **illustrative weights**: Q-group repair 1, K-group repair 3, R-group repair 8; the diagnosis-free universal repair costs 12 (`COST` in `kaggle/diagrag_v6.py`, commented "illustrative ... not measured"). The claim "diagnose first beats repairing everything at about one twelfth of the cost" therefore rests on assumed weights. v12 replaces the assumption with (A) a **weight-sensitivity analysis** on the saved episodes, and (B) **measured** per-repair costs (wall-clock time, on stated hardware). It is **descriptive**: no gate, bar, code or verdict of any earlier run changes, and the frozen v6 code is not edited.

## 1. Part A: weight sensitivity (CPU, saved data, no new retrieval)
- **Data:** the held-out episodes in the v6 GPU, v8 GPU (checkpoint from the Kaggle kernel output) and v7 CPU runs. Each stores its dispatched labels and group per policy decision (`loop3['lab']`, `loop3['nat']`), so the count of Q-, K- and R-group repairs a policy applies to each episode is recoverable. (The recomputation must reproduce each policy's stored `clean_mean_cost` and `mean_cost` exactly under weights 1/3/8, or Part A stops and is reported as failed.)
- **Weight grid (fixed now):** weights `(wQ, wK, wR)` with `wQ = 1` (the query-side repair is the unit) and `wK`, `wR` each in `{0.25, 0.5, 1, 2, 3, 5, 8, 12, 20}` subject to **no ordering assumption** (all 81 combinations, including those where R is cheaper than K or Q).
- **Question 1 (ranking):** for each combination, is the capped policy's mean clean cost **below** the universal repair's cost (which is `wQ + wK + wR`)? It is, by construction, if the capped policy dispatches a fraction below 1 of the same repairs; the analysis reports the **cost ratio** (capped / universal) per combination and its minimum, maximum and the share of combinations where the ratio is below 1 and below 0.25.
- **Question 2 (what drives it):** the weights enter only through the dispatched counts; the report shows the mean number of Q-, K- and R-repairs per clean query for each policy so a reader can substitute their own measured weights.
- **Question 3 (the target):** under which combinations does `capped_crc_0.005` still meet target T3 (mean clean cost <= 1.5 *in units where the universal costs 12*)? Because the target is stated in 1/3/8 units, it is restated as **cost relative to the universal repair** (T3' = clean cost / universal cost <= 0.125) and the share of combinations meeting T3' is reported.

## 2. Part B: measured weights (Kaggle GPU, a timing run)
- **Code:** a new, hash-pinned timing notebook that loads the frozen `kaggle/diagrag_v6.py` setup cells (corpus, indexes, models; not the episode generation) and times repairs on **replayed held-out episodes** from the v8 checkpoint. The checkpoint is attached as a private Kaggle dataset. Nothing in `diagrag_v6.py` is edited.
- **What is timed (per repair):** (i) the repair call itself, (ii) the retrieval re-run with the repaired state (`run(st2)`), and (iii) the base retrieval `run(st)` that every policy already pays. The measured **cost of a repair = (i) + (ii)**, reported in seconds and as a **multiple of (iii)**. One CUDA synchronise per timed call; warm-up calls discarded; caches that would make a repeat free (the query, cross-encoder and document caches) are **cleared before each timed call** so the number is a cold cost, and the effect of warm caches is reported separately.
- **Sample (fixed by hashing):** up to 30 held-out episodes per repair target (fault), ordered by `md5(2026|bid|fault)`; for group repairs, the same episodes; for the universal baseline, 100 held-out clean episodes ordered the same way. Each timed call is repeated 3 times; the **median** is reported with the interquartile range.
- **Hardware recorded:** GPU model, CPU model, library versions. Times are specific to that hardware and are not portable; only the **ratios** between repair groups are expected to transfer, and even those depend on the index size and the reranker.
- **Outputs:** measured cost per repair, per group (Q, K, R) as median seconds and as a multiple of the base retrieval; the measured analogue of `COST`; the universal repair measured end to end; the capped policy's cost recomputed with the measured weights.

## 3. Predictions (my judgements from reading the code; they can fail)
- Part A: the capped policy's cost ratio to the universal repair stays below 1 in **100%** of the 81 weight combinations (about 0.97) and below 0.25 in at least 90% (about 0.8). T3' (<= 0.125) holds in at least 70% of combinations (about 0.6).
- Part B: the measured **R-group** repair is the most expensive of the three groups (about 0.7), because it rolls back configuration and rebuilds the dense view; the **K-group** repair costs more than the **Q-group** repair (about 0.7). The measured ratios differ from 1 : 3 : 8 by more than a factor of 2 for at least one group (about 0.7).
- The measured universal repair costs less than 12 times the base retrieval (about 0.8), because the cross-encoder rerank, which dominates a retrieval, is shared work in some repairs.

## 4. What a result would and would not show
- Part A shows how sensitive the cost claim is to the weights; it does **not** measure anything new.
- Part B measures time on one machine for one stack; it does **not** measure dollars, memory, energy or production latency, and does not include the cost of computing the 63 telemetry features or the attributor's inference (those are timed separately below as an added item, because a "cheap" claim needs them).
- **Added item (Part B2):** the cost of **telemetry feature extraction** and of **attributor inference** per query, in seconds, on the same hardware, because every query pays them even when no repair is dispatched.
- Nothing here changes a verdict, a gate or a frozen file.

## 5. Amendments
(none yet; each is dated and filed before the result it concerns is read)
