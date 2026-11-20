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
