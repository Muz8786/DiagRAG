# v16: diagnosability of a retrieval pipeline as noisy group testing. Pre-registration of design and splits
Written 21 Nov 2026, 08:45 IST, before any v16 code ran. Kaggle only. Results freeze: Sat 21 Nov 2026, 23:00 IST.

## Idea (one model behind the earlier results)

A fault is identifiable only if the observations available to the diagnoser separate it from every other explanation. We model the retrieval pipeline as a noisy group-testing system (noisy-OR, as in medical diagnosis networks): each observation is a test, and each fault makes a test fail with a measured probability. Three observation channels are compared:

1. **Per-query telemetry:** one query, one system state (the frozen diagnoser). Pairs inside one fault group were never named (0 of 75), and the self-test could name them (85.3% held out). The model's claim is that identifiability needs **several observations of the same system state** under different inputs.
2. **Pass/fail probes:** m probe queries with known answers (the v15 self-test battery).
3. **Stage-traced probes:** the same probes, also recording which stage's output changed against the clean run (dense, sparse, fused, reranked, served). These are the observation points of design-for-testability (scan chains). The v15 mutant localization used this channel.

For a true fault set T and an alternative H, the per-probe Kullback-Leibler divergence of their test-outcome distributions sets how fast MAP decoding separates them (error falls roughly like exp(-m * c)). So a separability score computed **from the fault dictionary alone, before any instance is seen**, should predict which fault pairs the self-test names, and how many probes it needs.

No frozen method changes. The script rebuilds, with the same random tags and code as the v15 self-test, the same probe pool, dictionary and battery (checked against the stored v15 battery), and the same evaluated fault instances; it records their probe outcomes and stage traces; it decodes from subsets of probes.

## Splits (fixed now)
- Development: seed 55 (v15 development draws). Held-out: seeds 71, 72, 73 (v15 held-out draws; their v15 S outcomes already exist and were read; the v16 quantities have not been computed).
- The pass rule is written as an amendment after the development run and before any held-out v16 run.

## Planned quantities
- D(T): a-priori separability of a pair T = min over alternatives H whose fault families do not cover T of the summed per-probe KL divergence between their predicted outcome distributions (from the dictionary only), for each channel.
- MAP decoding accuracy (both causes named at the family level) as a function of the number m of random probes (m in 1, 2, 3, 5, 10, 20, 40, 60, 100; 40 random subsets each) and on the full battery, for the pass/fail and stage-traced channels; singles and pairs.
- Prediction test: AUROC of D(T) (pass/fail channel) for the observed v15 outcome (both causes named) on effective same-group pairs.
- Certificate (descriptive): with 0 failures on n random clean probes, the one-sided 95% Clopper-Pearson bound on the share of working queries a repair breaks is 1 - 0.05^(1/n) (2.95% for n = 100); compared with the measured traffic harm of every verified v15 repair.

## Amendments

- **A1 (21 Nov 2026, 09:35 IST; after the seed-55 development run, before any held-out v16 run).**
  - Development (seed 55): the rebuilt battery equals the stored v15 battery (101 probes, 100 random, 1 diagnostic, R07 undetected). Singles, pass/fail channel, family named by passive MAP decoding: 0.07 with 1 probe, 0.35 with 5, 0.81 with 40, 0.91 with the full battery; stage-traced channel 0.47, 0.71, 0.87, 0.93. Effective pairs (85; v15 dev outcomes joined): passive decoding names both causes in 0.235 (pass/fail) and 0.294 (stage), against **0.824** for the v15 self-test, which repairs and retests. Passive failures are mostly **masking**: the decoder names one cause of the pair, and the nearest alternative to the true pair shares one of its faults in 87 of 104 pairs.
  - What changed in the hypothesis, written here because the first prediction failed on development: the a-priori separability D (dictionary only) does **not** predict the self-test's outcome (AUROC 0.43) but **does** predict passive decoding (AUROC 0.69; passive success 0.11 / 0.24 / 0.36 across D tertiles), while the self-test's success is flat across the tertiles (0.86 / 0.76 / 0.86). Interpretation: passive observation is limited by separability and masking; intervention (repair, then retest) removes that limit. This is the identifiability distinction between observing and intervening.
  - **Held-out rule (seeds 71, 72, 73 pooled; effective pairs and harmful-fault singles as defined in v15 A1; v15 held-out S outcomes joined by pair; bootstrap by instance, 4000 draws; all must hold for PASS):**
    - **V-1 separability predicts passive identifiability:** AUROC of D (pass/fail channel) for passive both-named on effective pairs >= 0.60 with 95% lower bound > 0.50.
    - **V-2 more observations help:** singles, pass/fail channel: accuracy with 1 probe <= 0.30 and with the full battery >= 0.85; effective pairs: accuracy with 100 random probes minus accuracy with 5, lower bound > 0.
    - **V-3 observation points help:** singles, stage channel minus pass/fail channel at 1 probe and at 5 probes, lower bound > 0 for both.
    - **V-4 intervention breaks masking:** effective same-group pairs, v15 self-test both-named minus passive both-named (pass/fail, full battery), lower bound > 0; and in the lowest D tertile (tertile cut-points from the pooled held-out D) self-test >= 0.70 and passive <= 0.30.
  - Held-out runs use script SHA-256 `8a1231580ecd2fec42524b5ca65e6ea068e8a545fbd0fd7a508fe87e26615a7e` (unchanged from development).
