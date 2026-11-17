# Optional quantum-machine-learning comparison: protocol (pre-registration). Written 17 Nov 2026, before the comparison was run on any held-out data.

## 0. What this is and is not
**Machine learning is the project's method. QML here is a side comparison of scores and nothing more.** The models are **simulated classically** with a noiseless statevector simulator written in this repository (`docs/evidence/qml_compare.py`). There is no quantum hardware, no noise model, and **no claim of quantum advantage**. It is not part of the paper's method, adds no gate, and changes no result of any run.

## 1. Task, data, splits
- Task: **fault-versus-clean detection AUROC** on held-out episodes of a judged run's own `episodes.jsonl` (the 63 telemetry features). The single-fault episodes only (C2 excluded, as in the detector gates).
- **Every model is fitted on the TRAIN split only and scored on the TEST split once.** No setting below was chosen on the test split. The only look at data before this protocol was a development check on a split of the **train** rows alone (the QSVM's inner held-out AUROC was 0.889 against 0.910 for a classical RBF-SVM on the same input, and the kernel's off-diagonal mean was 0.056, so it is not degenerate); it changed nothing.
- Run: the **v6 CPU judged run** (`kaggle/judged_cpu_run_v6_seed50/episodes.jsonl`) as the primary dataset. The composed held-out episodes of the v7 run (when that run exists) are scored as a second, descriptive dataset with the same fitted models (composed-versus-clean AUROC, overall and by stratum).

## 2. Models (all settings fixed here)
- **ML main (reference):** the project's HistGradientBoosting classifier on all 63 features (the same settings as the attributor).
- **Classical comparators on the same reduced input the quantum models receive** (standardise, PCA to 6 components, fitted on train): logistic regression; SVM with an RBF kernel (C = 1, gamma scale); HistGradientBoosting. These exist because a quantum model that sees only 6 dimensions must be compared with classical models that also see only 6, or the comparison measures the dimension reduction and not the quantum part.
- **QML 1, quantum-kernel SVM:** 6 qubits, a Havlicek-style ZZ feature map with 2 repetitions with single-qubit phases and pairwise phases around a 6-qubit ring, fidelity kernel `|<psi(x)|psi(x')>|^2`, SVM with C = 1 and balanced class weights, fitted on every TRAIN row. Inputs scaled to [0, pi] with train min and max.
- **QML 2, variational quantum classifier:** 6 qubits, 3 layers of data re-uploading (RY(x_i) on every qubit, trainable RY and RZ, a CNOT ring), readout `<Z_0>`, a trainable scale and bias, binary cross-entropy, Adam with learning rate 0.05, 80 epochs, batch 256, trained on a class-balanced subsample of 2,000 TRAIN rows (seed 0), **5 initial-parameter seeds** reported individually and as mean and spread.
- The simulator was unit-tested before this protocol (normalised states, a unit-diagonal positive-semidefinite kernel, RY flipping exactly the intended qubit, a correct Bell pair, bounded logits with gradients, a valid CNOT permutation); all passed.

## 3. Reported
AUROC with a 95% bootstrap interval (1,000 resamples over test episodes) for every model; for the composed set, composed-versus-clean AUROC overall and by stratum; the kernel's diagonal and off-diagonal means; run time. Descriptive only.

## 4. Predictions (judgements, written so that they can fail)
- The HistGB on 63 features will beat every 6-dimensional model by a clear margin (the reduction discards most of the variance; the PCA keeps about 41%).
- The quantum-kernel SVM will be within about 0.03 AUROC of the classical RBF-SVM on the same input, and will not beat it.
- The variational classifier will be below the quantum-kernel SVM, with seed-to-seed spread of about 0.01 to 0.03.
- On the composed episodes all models will score lower than on single faults or similarly; I do not predict a quantum advantage on them.

## 5. What this does not show
Nothing about quantum hardware, noise, or scaling; nothing about faults other than detection; a 6-qubit simulation on 6 PCA components is a small-scale illustration. A tie or a loss for the quantum models is a valid result and will be reported as such.

## 6. Code and amendments
`docs/evidence/qml_compare.py`, SHA-256 `9b99c703a7b976d176e8366eff892e738cfb99370afc3270ee969ff13f0922f3`. Amendments: Q1 (results, below). The code was not changed after this protocol (hash verified before the run).

## Q1. Results (17 Nov 2026, 08:10 UTC). Written after the run; the protocol above is unchanged.
Run: `qml_compare.py` (hash above, unchanged) on `kaggle/judged_cpu_run_v6_seed50/episodes.jsonl` (5,416 train, 4,019 test: 1,511 faulted, 2,508 clean), with the 155 held-out composed episodes of the v7 run as a second set (`export_composed_features.py` from the v7 checkpoint). CPU, 8 threads, 107 s. PCA to 6 components keeps 40.8% of the variance. Simulated, noiseless, no hardware. Raw output: `qml_result.json`, `qml_run.log`.

| model | single-fault AUROC [95% CI] | composed-vs-clean AUROC |
|---|---|---|
| ML main: HistGB, 63 features | 0.9784 [0.974, 0.983] | 0.9954 |
| ML 6-d: logistic regression | 0.7269 [0.707, 0.744] | 0.8638 |
| ML 6-d: RBF-SVM | 0.9165 [0.907, 0.926] | 0.9794 |
| ML 6-d: HistGB | 0.9211 [0.912, 0.931] | 0.9883 |
| QML: quantum-kernel SVM (6 qubits) | 0.8918 [0.881, 0.903] | 0.9418 |
| QML: variational classifier, mean of 5 seeds | 0.8826 (sd 0.0054; seeds 0.873 to 0.890) | 0.9647 |

Kernel diagnostics: unit diagonal, off-diagonal mean 0.0546 (the kernel is not degenerate). Composed-versus-clean AUROC by stratum is in `qml_result.json`; for the quantum-kernel SVM it ranges from 0.900 (RR) to 0.969 (QR), and for the 63-feature HistGB from 0.97 (WITHIN_FAMILY) to 1.0.

Scorecard. (1) HistGB on 63 features beats every 6-dimensional model by a clear margin: 0.978 against at most 0.921, **held**. (2) The quantum-kernel SVM within about 0.03 of the classical RBF-SVM on the same input and not beating it: 0.892 against 0.917, a gap of 0.025, **held**. (3) The variational classifier below the quantum-kernel SVM, seed spread about 0.01 to 0.03: mean 0.883 against 0.892, seed range 0.016, **held** (the seed standard deviation, 0.005, is smaller than I guessed, and the difference between the two quantum models, 0.009, is smaller than the 95% interval of either). (4) Composed episodes score lower than or similar to single faults: every model scores **higher** on composed-versus-clean (0.86 to 0.995), **did not hold**. A composed episode carries two or more disturbances, so telling it from a clean one is easier than telling a single fault from clean; this is a different task from the single-fault one and the two numbers are not the same measurement.

Reading. Under identical 6-dimensional input the classical RBF-SVM and HistGB score above both quantum models on both sets (single-fault 0.917 and 0.921 against 0.892 and 0.883). On the composed set the variational classifier (0.965) scored above the quantum-kernel SVM (0.942), but both are below the classical 6-d RBF-SVM (0.979) and HistGB (0.988). There is **no quantum advantage in this result**, and none is claimed. The result says only that a 6-qubit simulated model on 6 PCA components gets within about 0.03 of a classical kernel machine on the same input and 0.09 below the full-feature model the project uses. Single run, one seed for the data split, one PCA, one feature map; nothing was tuned on the test split.
