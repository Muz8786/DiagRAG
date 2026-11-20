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
(none yet)
