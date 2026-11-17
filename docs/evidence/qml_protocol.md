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
`docs/evidence/qml_compare.py`, SHA-256 `9b99c703a7b976d176e8366eff892e738cfb99370afc3270ee969ff13f0922f3`. Amendments: (none yet)
