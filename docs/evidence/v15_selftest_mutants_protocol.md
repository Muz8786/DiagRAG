# v15: diagnostic self-test (S) and blind code-mutant faults (M). Pre-registration of design and data splits
Written 20 Nov 2026, 20:45 IST, before any v15 code was run. Compute on Kaggle only. Results freeze: Sat 21 Nov 2026, 23:00 IST.

Nothing in the frozen v6 method changes. S is a new module next to the telemetry diagnoser; M is a new test set. Both run inside the frozen-v6 harness on judged checkpoints.

## Data splits (fixed now)

| Role | Pipeline checkpoint | Fault instances | Mutants | Probe pool |
|---|---|---|---|---|
| Development (design may change freely) | seed 55 | dev draws (rng tag `dev`) | dev half | train split of seed 55 |
| Held-out judged (no design change after reading) | seeds 71, 72, 73 (untouched by S and M) | held-out draws (rng tag `heldout`) | held-out half | train split of each seed |

- Mutants are split by `md5(function|line|col|operator)`: first hex digit 0-7 is dev, 8-f is held-out.
- Probes come only from **train-split** clean successes; all traffic evaluation uses **test-split** queries.
- Pass bars are written as an amendment after the development run and before any held-out run; the development numbers are reported next to them.

## S. Diagnostic self-test (from chip testing and laboratory quality control)

- **System faults (15):** R01, R03, R05, R06, R07, R10, R11, R13, R15, R19, R22, R23, R24, R25 and K04, applied as one system-wide configuration to every query (the per-query injectors' parameters, drawn once per instance; R01 masks 30% of documents at random, R25 floods 40 random rows, K04 makes 5% of document vectors stale, R06 routes to a wrong collection).
- **Battery:** probe queries with known answers (train clean successes). Part A is a random sample (detection by acceptance sampling: a fault that breaks a share h of working queries is missed by m random probes with probability (1 - h)^m). Part B is chosen greedily so that the fault signatures differ (diagnostic test generation).
- **Decoder:** noisy-OR fault model (as in QMR-DT medical diagnosis) estimated on development instances; MAP over no fault, single faults and pairs.
- **Repair and retest:** apply the decoded repairs to the probes, re-run the battery, decode what still fails; at most 3 rounds, then the rollback repair. A repair is accepted only if every probe passes (outcome-verified).
- **Reported:** detection; exact fault and component named (single); both causes named (pairs, all 105); unseen faults (fault removed from the dictionary: component named, verified repair); traffic closure and harm on test-split queries against the frozen per-query loop, a traffic-aggregated dispatcher (most frequent labels) and the universal repair; probes and seconds per self-test.

## M. Blind faults from code mutation (from software testing)

- **Mutated code:** the retrieval path only (`run`, `bm25_scores`, `q_terms`, `topn`, `dense_all`, `ce_scores`, `enc_q`); never the telemetry or the diagnoser. Operators: relational, arithmetic, integer constant +-1, float constant x0.5 / x2, unary minus removal, boolean constant flip, `if` condition negation. One mutation per mutant; caches are bypassed for mutants of cached functions.
- **Kept:** mutants that run without error on 40 test queries and break at least 10% of their clean successes (harmful). Crashing and harmless mutants are counted and reported.
- **Ground truth:** the component of the mutated code region (dense, BM25, fusion, rerank, serving, filters, shared).
- **Reported per harmful mutant:** traffic alarm from per-query telemetry (binomial test of the flagged share on 100 test queries against the clean flagged share), the self-test alarm and decoded component, and both combined.

## Amendments

- **A1 (21 Nov 2026, 00:50 IST; after development runs 1 and 2 on seed 55, before any held-out run).**
  - Development changes, all made on seed 55 only: the decoder never returns "no fault" when a probe fails (clean probes pass by construction); repair-and-retest became a decode-guided greedy search (the repairs of the 6 most likely faults, then their pairs, are tried on the failing probes; the best is kept only if the whole battery improves; at most 4 rounds, then rollback); the random part of the battery grew to 100 probes; random-draw faults get 4 dictionary draws; mutation operators were added (wrong variable, statement deletion, and/or, min/max, slice bound +-1); mutant ids became `fn|line|col|end_col|kind|sub` and the 122 points evaluated in development run 1 are excluded from the held-out half.
  - Definitions fixed now: an instance is **harmful** if it breaks at least one of the 100 traffic queries that succeed on the clean pipeline; a pair is **effective** if each of its two faults alone is harmful; "named" is at the **family** level (faults that share a repair, e.g. R03/R10/R11, K04/R07, are one family).
  - Development run 2 (seed 55) results, reported as development: harmful singles 41, detected 1.000, family named 0.976, verified repair 1.000; effective pairs 85 (78 in one fault group): both causes named 0.824 (same group 0.821) against 0.318 for a traffic-aggregated dispatcher; verified 1.000; traffic closure 1.000 (self-test) against 0.916 / 0.595 (per-query loop, singles / pairs) and 0.926 / 0.967 (universal repair); traffic harm 0.0% / 0.08% against 2.0% / 10.3% (loop) and 5.3% (universal); unseen faults with a same-family sibling named 0.909.
  - **S pass rule for the held-out runs (seeds 71, 72, 73; pooled; all must hold):** S-1 detection of harmful singles >= 0.95; S-2 family named for harmful singles >= 0.90; S-3 verified repair >= 0.95 for harmful singles and for effective pairs; S-4 both causes named in effective same-group pairs >= 0.70 and above the traffic-aggregated dispatcher (paired bootstrap 95% lower bound of the difference > 0); S-5 self-test traffic closure >= 0.95 on harmful singles and on effective pairs, above the per-query loop, with self-test traffic harm <= 0.5%. Secondary, reported but not in the rule: unseen faults with a sibling named (>= 0.75 expected), unseen verified repair.
  - **M:** development run 2 found an evaluation bug: mutants of `run` itself were not exercised, because the script called a local reference to the original `run` (mutants of functions that `run` calls were exercised). Fixed (the mutant path now calls `G['run']`); M is re-run on development (seed 55) before its pass rule is written. S code is unchanged by this fix.
  - Held-out S runs use script SHA-256 `277ca14c0944d53c5897a2b4aaea424970d6d0509caf1d0f98b95da85cf90631` with PARTS = S.

- **A2 (21 Nov 2026, 05:55 IST).** The first held-out S runs (seeds 71, 72, 73) and the M development re-run measured nothing: the script's parameter `PARTS` was overwritten inside `main` by the frozen pipeline's `PARTS` (its list of corpus partitions), so neither the S nor the M block ran. Their RESULT.json files contain only the battery (built from train-split probes); no held-out fault instance, pair or mutant was evaluated, so no held-out result exists or was read. Fix: the parameter is renamed `RUN`; nothing else changes. Re-run with script SHA-256 `03b0240acfda5c03c3b0826d8ef2b62969d01baaf395351a5d80837085af032f`. The S pass rule of A1 is unchanged.

- **A3 (21 Nov 2026, 06:10 IST; before any held-out S or M result exists).** Seeds **74, 75, 76** (never used) are reserved as a second untouched confirmation set. Their frozen-v6 pipeline runs start now (notebook = `DiagRAG_v6_kaggle.ipynb` with only the seed changed, as E1 of v14). Use rule, fixed now: they are used for S or M only if that part fails its held-out rule on seeds 71 to 73 and is then changed on development data (seed 55) with the root cause written here first; the first held-out outcome on 71 to 73 is reported in any case, next to the second. Their per-run adoption verdicts (L1, L2, U1, N1) are reported whatever they are; no further seeds will be added.
