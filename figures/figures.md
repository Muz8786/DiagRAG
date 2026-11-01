# Figures — DiagRAG results, for the publication paper

Open this file in any Markdown editor. Every picture below is
embedded from the `figures/` folder next to this file, so it
renders in Typora, Obsidian, VS Code, and GitHub preview
without any extra step. Edit the captions here, not the PNGs —
the PNGs are generated from verified result files, and if a
number changes, regenerate the PNG, do not edit it by hand.

## 1. Headline closures by domain

![Headline closures](01_closures_by_domain.png)

Source: ESCI GPU 186K results, SecureBank and TeleCall EUD
results, SciFact production results. Oracle-referenced closure,
with 95% intervals where banked. ESCI fixed 96.67% [94.62, 98.61],
tuned 97.33% [95.33, 99.10]; SecureBank tuned 97.7% [96.4, 98.9];
TeleCall tuned 87.7% [83.7, 91.4]; SciFact production tuned
89.19% [86.5, 91.7]. Do not mix the SciFact CPU lineage
(94.1% / 95.3%, no CIs) into this chart without labelling it.

## 2. EUD on ESCI: Hit traded for lower cost

![EUD ESCI](02_eud_esci_hit_cost.png)

Source: ESCI EUD seed 42. Factorised Hit 85.48% at cost 6.69,
utility at lambda=1 0.2975. EUD eud05 Hit 79.88% at cost 4.95,
utility 0.3863. Costs are illustrative (1, 3, 8), not measured.
Say so in the caption in the paper.

## 3. M1: Hit gain bought at three times the cost

![M1](03_m1_vs_standard.png)

Source: M1 judged run, 1 Nov 2026, file-verified. Standard EUD
in THIS run: Hit 35.36%, cost 0.56. M1: Hit 49.29%, cost 1.86,
utility gain +0.0306 CI [0.0193, 0.0411]. Verdict NOT_ADOPTED,
cost bar fails. WARNING: the 35.36% standard Hit in this run
is NOT the banked eud05 Hit 79.88% — the standard comparator
in the M1 run fires K in 0 of 840 episodes. Do not put those
two numbers in one chart.

## 4. TeleCall vs SciFact: K is the gap

![TeleCall vs SciFact](04_telecall_vs_scifact.png)

Source: CPU lineage, same stack and protocol, seed 42.
TeleCall per-factor 89.65%, exact 69.04%, ceiling 49.33%,
K AUROC 0.768. SciFact per-factor 93.14%, exact 80.13%,
ceiling 82.0%, K AUROC 0.937. Q and R are near 1.0 in both,
so the exact-set gap is almost entirely K.

## 5. Withheld combinations: the compositional weakness

![Withheld combinations](05_withheld_combinations.png)

Source: banked withheld-combination exact set. QK 15.8%,
KR 10.0%, QR 45.0%, QKR 36.7%, mean 26.9%. The 37% line is
the CSA proposal bar, not a frozen bar, and not a result.
Label it as proposed if it stays in the paper chart.

## 6. Repair latency, CPU mean versus GPU p50, not the same statistic

![Latency](06_latency_cpu_mean_vs_gpu_p50.png)

Source: Performance_Analysis_Note.md. CPU values are means
(Q 11.6, K 10.4, R 15.4, clean 15.5 ms). New GPU values are
p50 (Q 22.2, K 10.1, R 70.4, clean 17.9 ms, T4, n=40).
The previous chart wrongly labelled the CPU bars as p50;
that is corrected here, and the file is renamed to match.
WARNING: the older GPU flush p50 890.8 ms is NOT in this
chart, because it contradicts the new GPU flush p50 10.1 ms
and that contradiction is unresolved. Never quote a single
flush latency, and never quote a mean without its p50/p95.

## 7. Sequential vs one-shot: a judged negative

![Sequential](07_sequential_vs_oneshot.png)

Source: sequential judged run, 31 Oct – 1 Nov 2026.
One-shot Hit 85.48%, cost about 6.69, utility at lambda=1
about 0.298. Sequential expected-utility Hit 86.31%,
cost 7.97, utility 0.199. Gates: utility FAIL, cost-saving
FAIL, Hit-loss PASS (gain +0.83 points, not significant).
Sequential goes in the paper as a judged negative, not a
headline win.

## How to make a new picture

1. Take the number only from a result file you have read,
   never from a log paste or a browser preview.
2. Add the figure to this folder as a PNG, with a number
   prefix (08_, 09_, …) so the order stays stable.
3. Add a section above, with the picture, its source file,
   its interval or caveat, and what NOT to quote from it.
4. If the number is browser-reported only (B2, CPU batch v1),
   do not chart it as verified — label it browser-reported
   or leave it out until its results file is read.
