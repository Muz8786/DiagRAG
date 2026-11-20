# v13 Idea 2: probe-and-verify diagnosis (pre-registration). Written 20 Nov 2026, ~06:00 UTC, before any probe was run on any episode.

## 0. Question
When the diagnosis is unsure, can the system **try a few candidate repairs as reversible probes and keep the one whose result looks healthy**, judged only from telemetry (no gold), and so close more faults than applying its single best guess, at a small, measured number of extra retrievals? Tested where the attributor is weakest: **faults it never saw** (leave-one-fault-out, LOFO). Descriptive analysis on saved checkpoints by CPU replay; no frozen file, gate or verdict changes.

## 1. Data and replay
Port corpora with saved checkpoints: **NFCorpus** (v9 judged, seed 53), **ArguAna** (v9, seed 54), **FiQA** (v13 judged, seed 60). The frozen port code's retrieval, repairs (`REP`) and telemetry (`features`) are executed from the run's own caches, as in `v10_textview.py` (replay check: clean Hit@5 reproduced on every clean episode, else the corpus is reported as not run). NQ is **not** included (2.68M-passage index; not replayable on the sandbox CPU in time).
Episodes: held-out (`test`) faulted episodes of the 20 port faults. **Development:** NFCorpus **training** split only, to catch coding errors; held-out evaluation is run once.

## 2. Policies (the gate that decides *whether* to repair is unchanged; these decide *which* repair)
For each fault f, a LOFO attributor (port settings `HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=<run seed>)`) is fitted on training episodes without f.
- **P0 passive:** apply the repair of the attributor's top non-NONE class (today's behaviour).
- **P2 probe (Idea 2):** candidates = the top **3** non-NONE classes by attributor probability. Probe them in order: apply the repair, re-run retrieval, re-extract telemetry. A probe result is **healthy** if the LOFO attributor's top class on it is NONE **and** no Idea-1 invariant is violated (Idea-1 table and threshold, restricted to features the port stack has, calibrated on the corpus's clean training episodes). Stop at the first healthy result; otherwise keep the result with the highest P(NONE).
- **P12 Idea 1 + Idea 2:** as P2, but candidates whose Idea-1 component is in the episode's flagged component set are probed first (ties and the rest by attributor probability), still at most 3.
- **Oracle:** the true fault's repair (the run's stored rescue), as an upper reference.
No policy sees the gold. Gold is used only to score closure afterwards.

## 3. Measures
- **Closure** = gold in the top-k after the chosen repair; per fault, macro mean over faults.
- **Cost** = extra retrievals per episode (P0 = 1; P2 and P12 = number of probes run, 1 to 3).
- **Primary:** P2 minus P0 macro closure, paired bootstrap over faults (2,000); same for P12 minus P0.
- Reported beside them: oracle closure, cost, and per-fault results.

## 4. Pass rule (fixed now)
Idea 2 **passes** if P2 (or P12, reported separately) minus P0 has a 95% lower bound above 0 on **every** analysed corpus, with mean cost at most 3 retrievals per episode.

## 5. Predictions (judgements; they can fail)
P2 passes: about 0.5. P12 passes: about 0.5. P12 at least as good as P2: about 0.6. Mean probes per episode between 1.5 and 2.5: about 0.6. Oracle closure above 0.85 on each corpus: about 0.8.

## 6. Limits stated in advance
Port stack only (20 faults, small corpora, many faults blunt); one seed per corpus; injected faults; probes cost real retrievals (latency measured but CPU, not production); clean-query harm is set by the unchanged gate and is not re-measured here.

## 7. Amendments
**D1 — changes from the development run (20 Nov 2026, ~07:10 UTC; NFCorpus training split only; no held-out episode has been probed).** Development output `_idea2/dev_nfc_train.jsonl` (not committed). Training-split macro closure: P0 0.186, P2 0.184, P12 0.246, oracle 0.924; mean probes 1.9 to 2.0.
Two problems were found, and the method is changed **before** the held-out run (these are design changes motivated by development data, declared here; the held-out run will be run once):
1. **The verifier.** "Top class NONE and no invariant violated" barely predicts that a probe fixed the query (probe-level AUROC of P(NONE) 0.594; P(success | healthy) 0.23 vs 0.11). The **increase** in P(NONE) from the original telemetry to the probed telemetry predicts it better (AUROC 0.713). New rule: probe every candidate up to the budget and **keep the one with the largest increase in P(NONE)** (no early stop; cost = number of candidates, at most 3).
2. **The candidates.** Under LOFO the attributor's classes never include the left-out fault, so a repair specific to that fault can never be a P2 candidate. New candidate set for **P12**: the repairs of every fault whose Idea-1 component is in the flagged set (the repair library is indexed by component and is part of the system; the attributor still never saw the fault), ordered by attributor probability with the left-out fault's repair placed by its component's position; then the attributor's order; at most 3. P2 keeps attributor-only candidates with the new verifier.
3. The development run is repeated with these rules as a code check; its numbers are recorded below and not used for anything else.
P0 and the pass rule (section 4) are unchanged.

**D2 — development re-run with the D1 rules (code check; NFCorpus training split; numbers not used for anything else).** P0 0.186, P2 0.184, P12 0.468, oracle 0.924; P12 minus P0 +0.282 [+0.136, +0.444]; P2 minus P0 -0.002 [-0.076, +0.076]; 3 probes per episode. **Script frozen for the held-out run: `v13_idea2.py` SHA-256 prefix `8da2c1627e5a2f79`.** Held-out runs, once each: NFCorpus, ArguAna, FiQA (test split).

**R1 — held-out result and scorecard (20 Nov 2026, ~08:10 UTC; written after the results were read; sections 0 to 6, D1 and D2 unedited).** Frozen script (D2), one held-out run per corpus; replay check 0 mismatches of 200 clean episodes on each. Files `v13_idea2_{nfcorpus,arguana,fiqa}.json` (per-episode outputs not committed: they contain only ids and booleans but are large).

Unseen faults (leave-one-fault-out), macro closure over 20 faults:
| Corpus | P0 passive (best guess) | P2 probe, attributor candidates | **P12 Idea 1 + Idea 2** | Oracle (true repair) | P12 minus P0 [95% CI] | Probes per episode |
|---|---|---|---|---|---|---|
| NFCorpus (seed 53) | 0.178 | 0.168 | **0.448** | 0.912 | +0.270 [+0.134, +0.420] | 3 |
| ArguAna (seed 54) | 0.351 | 0.269 | **0.707** | 0.949 | +0.356 [+0.154, +0.544] | 3 |
| FiQA (seed 60) | 0.220 | 0.204 | **0.570** | 0.926 | +0.350 [+0.194, +0.522] | 3 |

**Pass rule (section 4): P12 passes on all three corpora** (lower bounds above 0, cost 3 retrievals per episode, at the cap). **P2 does not pass** (differences -0.010 to -0.082, intervals contain 0): probing alone cannot help when the right repair is not among the attributor's guesses, which under LOFO it never is.
*Scorecard (section 5):* P2 passes (0.5): **did not hold**. P12 passes (0.5): **held**. P12 at least as good as P2 (0.6): **held**. Mean probes 1.5 to 2.5 (0.6): **did not hold** (3.0, because D1 removed early stopping). Oracle above 0.85 everywhere (0.8): **held**.
*What it shows:* combining the two ideas (Idea 1 narrows the broken component, Idea 2 tries that component's repairs and keeps the one whose telemetry improves most, with no gold) more than doubles closure on faults the system never saw, on three corpora, at 3 extra retrievals per faulted query. It is still well below the oracle (0.45 to 0.71 against 0.91 to 0.95).
*Limits:* the verifier and the candidate rule were redesigned on development data (D1) before the held-out run; the cost is the full budget (3) on every faulted episode; clean-query harm of probing was not measured here (the unchanged gate decides whether to repair at all); port stack only, small corpora, one seed each; ESCI and NQ not tested; query faults (Q01, Q03, Q04, Q05) and R05, R23, R24 stay near 0.

**A1 — NQ added (20 Nov 2026, ~07:00 UTC; before any NQ probe).** The owner asked for everything to run on Kaggle, which removes the sandbox-CPU limit that excluded NQ in section 1. The frozen script (D2, SHA-256 prefix `8da2c1627e5a2f79`) is run **unchanged**, once, on the held-out split of the **v13 judged NQ run** (seed 58, code `916c3864…`), on Kaggle (`kaggle/DiagRAG_v13_idea2_nq.ipynb`), with the same pass rule (section 4) for NQ on its own. NFCorpus, ArguAna and FiQA results (R1) are unchanged.
