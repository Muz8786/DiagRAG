# What telemetry can and cannot identify — elementary results for DiagRAG

This note formalises one question: which faults can a telemetry-only diagnoser tell apart, and when does telling them
apart matter for repair? The results are elementary. Their value is that they turn the family-confusion measurements
of the judged runs into statements with a proof behind them. The numbers come from the judged files cited in §4.

## 1. Setup

- An **episode** is a query and a pipeline state. The pipeline is clean, or carries one fault $f \in F$.
- The **diagnoser** sees only the telemetry vector $X = \phi(\text{trace})$: the 50+ features in `features()`, all computed
  from the retrieval trace, with no gold labels and no generated answer.
- For each fault $f$, let $P_f$ be the distribution of $X$ over episodes with fault $f$; $P_0$ is the clean distribution.
- A **repair** is a map $\rho$ from pipeline states to pipeline states. $r_f(\rho)$ is the probability that $\rho$ rescues
  an episode with fault $f$.

## 2. Results

**Lemma 1 (separability is capped by total variation).** For any score function $s$ of the telemetry and any two
faults $f, g$:

$$\mathrm{AUROC}_s(f \text{ vs } g) \;\le\; \tfrac12 + \mathrm{TV}(P_f,P_g) - \tfrac12\,\mathrm{TV}(P_f,P_g)^2 .$$

*Proof.* Write $\delta = \mathrm{TV}(P_f,P_g)$.
- By the Neyman–Pearson lemma, every ROC curve satisfies $\mathrm{TPR}(t) - \mathrm{FPR}(t) \le \delta$.
- Also $\mathrm{TPR} \le 1$. So the ROC curve lies under $\min(1, \mathrm{FPR} + \delta)$.
- $\mathrm{AUROC} - \tfrac12$ is the area between the ROC curve and the diagonal. It is therefore at most
  $\int_0^1 \min(\delta, 1 - x)\,dx = \delta - \delta^2/2$. ∎

**Corollary 1 (measured AUROC lower-bounds the distance).** If an out-of-fold classifier reaches pairwise AUROC $a$,
then $\mathrm{TV}(P_f,P_g) \ge 1 - \sqrt{2 - 2a}$. This inverts Lemma 1. A pair with $a = 0.5$ in our telemetry
proves nothing about separability. A pair with $a = 0.95$ certifies $\mathrm{TV} \ge 0.68$.

**Proposition 2 (indistinguishable by construction — a condition, not our case).** Suppose two faults change the
pipeline only through the same intermediate variable $Z$, and induce the same distribution of $Z$. Then
$P_f = P_g$, and every diagnoser has pairwise AUROC exactly 0.5.

*Measured, and correcting an earlier draft of this note.* The draft claimed this condition holds for the encoder family
{R03, R10, R11} and the stale-vector family {K04, R07}. **It does not hold.** Their $Z$-distributions differ, and
out-of-fold pairwise AUROC on the train split is R03|R10 1.00, R03|R11 0.95, R10|R11 0.94 and K04|R07 0.89. Telemetry
separates them. The confusion seen in the multi-class attributor comes from competition with NONE and with other
classes, not from pairwise indistinguishability. The families are therefore justified by Proposition 3 (one repair
serves all members), not by Proposition 2.

**Proposition 3 (what attribution has to get right).** Call faults $f$ and $g$ *repair-equivalent* if a single repair
$\rho$ satisfies $r_f(\rho) \ge r_f(\rho_f) - \varepsilon$ and $r_g(\rho) \ge r_g(\rho_g) - \varepsilon$. Consider a
dispatcher that identifies only the repair-equivalence class $[f]$ and applies the class repair. Its expected closure
is within $\varepsilon$ of a dispatcher that identifies the exact fault. Its attribution accuracy is bounded by class
separability, not fault separability. So the identifiability requirement is on classes. Confusion inside a class costs
at most $\varepsilon$ closure.

**Proposition 4 (the group fallback is a safe default).** Let a group $G$ have a fallback repair $\rho_G$, with
$r_f(\rho_G) \ge \beta$ for every $f \in G$ and harm $h$ on clean episodes. Then a fault never seen in training
— held out, as in the leave-one-fault-out test — that is placed in its correct group still has closure
$\ge \beta \cdot P(\text{group correct} \wedge \text{dispatched})$. Without the fallback, a held-out fault gets closure
only if its nearest seen family happens to share a repair. The fallback trades its cost and harm $h$ for this
guarantee.

## 3. What this implies for the paper

- **Fault-level attribution accuracy is the wrong headline metric.** Under Proposition 3, attribution should be scored
  by repair-equivalence class (our *families*), and closure should be the headline. The v2 and v3 loops are scored that
  way.
- **The families are a repair choice, not a forced one.** Proposition 2 does not apply to our families (see the
  measurement above). They are justified because their members share a repair (Proposition 3).
- **Generalising to unseen faults is a group-level property.** Proposition 4 explains why: closure on held-out faults
  is 0.36 with group fallbacks versus 0.24 without them in v3 (§4).

## 4. Measurements

All from the v3 judged run (seed 45). Pairwise numbers come from the **train split only**:
`docs/evidence/analysis_v3_seed45.json`, produced by `docs/evidence/analysis_v3.py`.

- **Pairwise separability:** 465 fault pairs, out-of-fold HistGB, grouped by base query.
  - 388 of 465 pairs (83%) have AUROC ≥ 0.95, so their telemetry distributions are certified to differ by
    TV ≥ 0.68 (Corollary 1).
  - Only one pair falls below 0.80: K04|Q03 at 0.79 (TV ≥ 0.36).
  - The next least separable pairs are Q03|R22 0.81, K05|R11 0.87, Q04|R13 0.87 and Q03|R24 0.88.
  - Q03 appears in three of the five least-separable pairs. This matches its detector failing its gate (AUROC 0.56,
    `kaggle/judged_cpu_run_v3_seed45/detector_gates.csv`). Real paraphrases leave almost no telemetry trace — an
    empirical instance of the limit in Lemma 1.
- **Repair-equivalence (Proposition 3):** oracle-dispatched family repairs, `family_repairs.csv`.
  - The ENC repair rescues R03, R10 and R11 at 50/50 each.
  - The STALE repair rescues K04 at 45/50 and R07 at 50/50.
  - The QLEX family repair is weaker than the members' own repairs: Q01 25 vs 33, Q04 33 vs 41, Q05 43 vs 46 (of 50);
    for Q03 both are near zero (2 and 1). So QLEX is **not** repair-equivalent at ε = 0.05. That predicts its loss of
    closure under family dispatch.
- **Group fallback (Proposition 4):** leave-one-fault-out mean closure is 0.365 with group fallbacks and 0.242 without
  (`unseen_faults.csv`).
  - The largest gains come where a group fallback covers the held-out fault: K05 0.00 → 0.88, R06 0.00 → 0.44,
    R13 0.12 → 0.48, R01 0.04 → 0.28, K08 0.08 → 0.32.
  - The pre-registered U1 bar of 0.50 was **not** reached.
