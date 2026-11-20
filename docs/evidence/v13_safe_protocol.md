# v13 K04-safe probing (pre-registration). Written 20 Nov 2026, ~12:30 UTC, before any run of this rule.

## 0. Why this exists, said plainly
On ESCI, Ideas 1 + 2 as pre-registered **did not pass** (`v13_esci_ideas_protocol.md` R1: U1 0.368 against the stored dispatcher's 0.396; difference -0.028 [-0.114, +0.044]). Reading the saved per-episode results showed the mechanism: the probe kept a **wrong repair** that made the telemetry look healthier but did not return the gold (K04: the R01 dense-view rebuild kept in 36 of 46 flagged episodes), and it replaced a good group fallback. **The rule below was designed after seeing that failure on the ESCI seed-55 run. It is therefore not confirmed on seed 55.** It is confirmed (or not) only on data that did not shape it: **ESCI seed 52 held-out** and **SCIDOCS (seed 56) held-out**. No numeric threshold is tuned: the rule has no free parameter beyond those already fixed in `v13_idea1_protocol.md` and `v13_idea2_protocol.md`.

## 1. The rule (P-safe). The old method is always candidate 1; probing can only add.
For an episode that the old method flags:
1. **Old repair first.** Apply the old method's repair exactly as it does today (ESCI: `dispatch_v3` repairs with their group fallbacks; port stack: the repair of the attributor's top non-NONE class). Re-run retrieval and re-extract telemetry. If the result is **healthy**, stop and keep it.
2. **Otherwise probe at most 2 more candidates**, each a repair of a fault whose Idea-1 component is **flagged on the original telemetry** (library indexed by component, as in `v13_idea2_protocol.md` D1; the left-out fault's repair at its component's position; ordered by the attributor's probability; repairs identical to the old one removed; no repair from an unflagged component).
3. **Switch only on strong evidence:** keep a candidate only if its result is **healthy**; if several are, the one with the largest P(NONE). If none is healthy, **keep the old repair.**
- **Healthy** = the (leave-one-fault-out) attributor's top class on the repaired telemetry is NONE **and** no Idea-1 invariant is violated (Bonferroni threshold of `v13_idea1_protocol.md`, calibrated on the run's clean training episodes). No gold is used.
- **Cost:** at most 3 retrievals per flagged episode (old + 2).
Whether to repair at all (the flag, thresholds, conformal gate) is unchanged.

## 2. Confirmation runs (Kaggle, once each)
| Run | Data | Code |
|---|---|---|
| C1 | ESCI **seed 52** held-out single-fault episodes, U1 set-up of v6 (leave-one-fault-out, 25 faults), kernel `syedmuzammilquadri/diagrag-v8-gpu-seed52` checkpoint | frozen v6 `44176b9a…` + `v13_esci_safe.py` |
| C2 | **SCIDOCS** (seed 56) held-out episodes, port stack, leave-one-fault-out, kernel `syedmuzammilquadri/diagrag-v11a-port-scidocs` checkpoint | frozen port4 `dd6ddff6…` + `v13_idea2_safe.py` |
| R | ESCI **seed 55** (the run that exposed the failure): reported beside them, **not counted as confirmation** | as C1 |
Each run reports, for the same episodes: P0 (old method; reproduction gate against the stored rows, at least 99.5%), P12 (the earlier rule, to show whether its failure replicates), and **P-safe**.

## 3. Pass rule (fixed now)
**P-safe passes** if **P-safe minus P0** has a 95% lower bound (paired bootstrap over faults, 2,000) **above 0 on both C1 and C2**. Also reported: whether P-safe is non-inferior to P0 (lower bound above -0.01) on R, and mean extra retrievals.

## 4. Trial
Each notebook has a TRIAL flag (2 faults, 5 episodes) used first to check the harness, timing and memory; trial numbers are not results.

## 5. Predictions (judgements; they can fail)
P-safe passes on both: about 0.35 (the stronger the "healthy" requirement, the less often it switches, and earlier development data showed "healthy" is only a weak sign of success). P-safe at least as good as P0 on C1 (point estimate): about 0.7. P-safe better than P12 on C1: about 0.8. K04 recovers to within 0.1 of P0: about 0.7. U1 reaches 0.50 on C1: about 0.1.

## 6. What a result would and would not show
A pass would show that probing with a conservative verifier adds repairs on top of a strong baseline without removing its good ones. A fail would be reported as a negative result, and the paper's claim would stay: Ideas 1 + 2 help on stacks without group fallbacks (four port corpora) and are not shown to help on the main stack. It does not change U1's bar, any frozen file or any earlier verdict.

## 7. Amendments
(none yet)
