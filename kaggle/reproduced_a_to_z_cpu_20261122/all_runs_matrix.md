## All judged runs (every run, pass or fail)

| Run | Stack | Code | Detectors / repairs / both (of 28) | L1 clean loss | L2 closure | U1 (bar 0.50) | N1 natural gain (95% CI) | Verdict |
|---|---|---|---|---|---|---|---|---|
| seed 42 | CPU | v1 (older code, not shipped) | 28 / 27 / 27 | - | - | - | - | **ADOPTED** |
| seed 43 | CPU | v1 | 28 / 28 / 28 | 0.75% (-) | - | 0.207 | - | **ADOPTED** |
| seed 44 | CPU | v2 | 28 / 27 / 27 | 1.28% (FAIL) | 0.871 (PASS) | 0.253 | - | **ADOPTED** |
| seed 45 | CPU | v3 | 27 / 27 / 27 | 0.15% (PASS) | 0.865 (PASS) | 0.365 (FAIL) | +2.25 [+1.40, +3.09] (PASS) | **ADOPTED** |
| seed 46 | GPU T4 | v3 | 27 / 27 / 27 | 0.15% (PASS) | 0.860 (PASS) | 0.395 (FAIL) | +2.06 [+1.21, +2.85] (PASS) | **ADOPTED** |
| seed 47 | CPU | v4 | 28 / 27 / 27 | 0.37% (PASS) | 0.830 (PASS) | 0.485 (FAIL) | +2.31 [+1.52, +3.16] (PASS) | **ADOPTED** |
| seed 48 | GPU T4 | v4 | 26 / 27 / 26 | 0.00% (PASS) | 0.866 (PASS) | 0.456 (FAIL) | +2.18 [+1.27, +3.16] (PASS) | **NOT_ADOPTED** |
| seed 49 | CPU | v5 | 24 / 27 / 24 | 0.15% (PASS) | 0.833 (PASS) | 0.440 (FAIL) | +2.43 [+1.70, +3.22] (PASS) | **NOT_ADOPTED** |
| seed 50 | GPU T4 | v6 (flagship) | 27 / 27 / 27 | 0.28% (PASS) | 0.844 (PASS) | 0.406 (FAIL) | +2.18 [+1.33, +3.03] (PASS) | **ADOPTED** |
| seed 50 (CPU replication) | CPU | v6 | 28 / 27 / 27 | 0.20% (PASS) | 0.854 (PASS) | 0.413 (FAIL) | +2.43 [+1.70, +3.22] (PASS) | **ADOPTED** |
| seed 50 (CPU, retrained attributor) | CPU | v7 (composed arm; single-fault regression check) | 28 / 27 / 27 | 0.16% (PASS) | 0.846 (PASS) | 0.413 (FAIL) | +2.43 [+1.64, +3.22] (PASS) | **ADOPTED** |

Notes: seed 42 used older v1 code whose hash is not shipped. L1 and L2 are defined from v2 onward (v1 runs predate them; "-" means not measured). Natural-traffic samples overlap across v3, v4 and v5 (one query sample), so N1 values are repeated measurements.

## Dispatch policies: clean loss, clean dispatch, mean cost, closure (held-out, same denominators)

### seed 45, CPU, v3

| Policy | Clean loss | Clean dispatch | Classifier-only dispatch | Clean mean cost | Mean closure | On frontier |
|---|---|---|---|---|---|---|
| tau_none_5pct_fpr | 0.15% | 3.9% | - | 0.14 | 0.845 | **yes** |
| global_crc_0.005 | 0.37% | 16.3% | - | 1.03 | 0.869 | **yes** |
| mondrian_crc_0.0025 | 0.15% | 38.0% | - | 2.02 | 0.759 | no |
| mondrian_crc_0.005 | 0.15% | 90.3% | - | 4.24 | 0.865 | **yes** |
| mondrian_crc_0.01 | 0.30% | 92.0% | - | 4.36 | 0.877 | **yes** |
| mondrian_crc_0.02 | 0.30% | 93.2% | - | 4.43 | 0.879 | **yes** |
| diagnosis_free_universal | 1.41% | 100.0% | - | 12.00 | 0.752 | no |

Frontier = no other policy is at least as good on clean loss, clean dispatch and closure and strictly better on one. Targets (v5 protocol): loss <= 0.5%, total clean dispatch <= 25%, mean cost <= 1.5, closure >= 0.80.

### seed 46, GPU T4, v3

| Policy | Clean loss | Clean dispatch | Classifier-only dispatch | Clean mean cost | Mean closure | On frontier |
|---|---|---|---|---|---|---|
| tau_none_5pct_fpr | 0.07% | 4.1% | - | 0.19 | 0.840 | **yes** |
| global_crc_0.005 | 0.22% | 14.1% | - | 0.96 | 0.866 | **yes** |
| mondrian_crc_0.0025 | 0.00% | 7.2% | - | 0.46 | 0.756 | **yes** |
| mondrian_crc_0.005 | 0.15% | 89.8% | - | 5.81 | 0.860 | **yes** |
| mondrian_crc_0.01 | 0.15% | 90.7% | - | 5.86 | 0.870 | **yes** |
| mondrian_crc_0.02 | 0.22% | 93.4% | - | 6.06 | 0.875 | **yes** |
| diagnosis_free_universal | 1.25% | 100.0% | - | 12.00 | 0.744 | no |

Frontier = no other policy is at least as good on clean loss, clean dispatch and closure and strictly better on one. Targets (v5 protocol): loss <= 0.5%, total clean dispatch <= 25%, mean cost <= 1.5, closure >= 0.80.

### seed 47, CPU, v4

| Policy | Clean loss | Clean dispatch | Classifier-only dispatch | Clean mean cost | Mean closure | On frontier |
|---|---|---|---|---|---|---|
| tau_none_5pct_fpr | 0.07% | 3.6% | - | 0.19 | 0.850 | **yes** |
| global_crc_0.005 | 0.22% | 12.2% | - | 0.78 | 0.876 | **yes** |
| mondrian_crc_0.0025 | 0.37% | 53.2% | - | 2.75 | 0.690 | no |
| mondrian_crc_0.005 | 0.37% | 87.6% | - | 3.65 | 0.830 | no |
| mondrian_crc_0.01 | 0.37% | 89.4% | - | 3.74 | 0.877 | **yes** |
| mondrian_crc_0.02 | 0.44% | 91.5% | - | 3.89 | 0.884 | **yes** |
| diagnosis_free_universal | 1.32% | 100.0% | - | 12.00 | 0.756 | no |

Frontier = no other policy is at least as good on clean loss, clean dispatch and closure and strictly better on one. Targets (v5 protocol): loss <= 0.5%, total clean dispatch <= 25%, mean cost <= 1.5, closure >= 0.80.

### seed 48, GPU T4, v4

| Policy | Clean loss | Clean dispatch | Classifier-only dispatch | Clean mean cost | Mean closure | On frontier |
|---|---|---|---|---|---|---|
| tau_none_5pct_fpr | 0.00% | 4.0% | - | 0.22 | 0.845 | **yes** |
| global_crc_0.005 | 0.00% | 12.1% | - | 0.81 | 0.871 | **yes** |
| mondrian_crc_0.0025 | 0.00% | 52.6% | - | 2.97 | 0.740 | no |
| mondrian_crc_0.005 | 0.00% | 88.8% | - | 4.17 | 0.866 | no |
| mondrian_crc_0.01 | 0.00% | 90.5% | - | 4.28 | 0.877 | **yes** |
| mondrian_crc_0.02 | 0.00% | 91.6% | - | 4.34 | 0.882 | **yes** |
| diagnosis_free_universal | 0.75% | 100.0% | - | 12.00 | 0.760 | no |

Frontier = no other policy is at least as good on clean loss, clean dispatch and closure and strictly better on one. Targets (v5 protocol): loss <= 0.5%, total clean dispatch <= 25%, mean cost <= 1.5, closure >= 0.80.

### seed 49, CPU, v5

| Policy | Clean loss | Clean dispatch | Classifier-only dispatch | Clean mean cost | Mean closure | On frontier |
|---|---|---|---|---|---|---|
| tau_none_5pct_fpr | 0.07% | 2.1% | 2.1% | 0.11 | 0.837 | **yes** |
| global_crc_0.005 | 0.15% | 14.1% | 14.1% | 0.98 | 0.872 | **yes** |
| mondrian_crc_0.0025 | 0.07% | 29.2% | 29.2% | 1.86 | 0.720 | no |
| mondrian_crc_0.005 | 0.15% | 89.2% | 89.2% | 3.66 | 0.833 | no |
| mondrian_crc_0.01 | 0.15% | 89.6% | 89.6% | 3.68 | 0.852 | no |
| mondrian_crc_0.02 | 0.15% | 92.8% | 92.8% | 3.86 | 0.882 | **yes** |
| capped_crc_0.005 | 0.07% | 15.6% | 15.6% | 0.96 | 0.821 | no |
| two_stage_0.005 | 0.37% | 41.1% | 15.6% | 1.91 | 0.782 | no |
| diagnosis_free_universal | 1.49% | 100.0% | 100.0% | 12.00 | 0.755 | no |

Frontier = no other policy is at least as good on clean loss, clean dispatch and closure and strictly better on one. Targets (v5 protocol): loss <= 0.5%, total clean dispatch <= 25%, mean cost <= 1.5, closure >= 0.80.

Policies meeting all four targets with a CRC guarantee: ['global_crc_0.005', 'capped_crc_0.005']; without a guarantee: ['tau_none_5pct_fpr']. Claim rule result: capped_crc_0.005.

### seed 50, GPU T4, v6 (flagship)

| Policy | Clean loss | Clean dispatch | Classifier-only dispatch | Clean mean cost | Mean closure | On frontier |
|---|---|---|---|---|---|---|
| tau_none_5pct_fpr | 0.12% | 3.7% | 3.7% | 0.19 | 0.831 | **yes** |
| global_crc_0.005 | 0.56% | 54.1% | 54.1% | 2.75 | 0.866 | **yes** |
| mondrian_crc_0.0025 | 0.20% | 66.5% | 66.5% | 2.96 | 0.573 | no |
| mondrian_crc_0.005 | 0.28% | 86.2% | 86.2% | 3.65 | 0.844 | **yes** |
| mondrian_crc_0.01 | 0.28% | 86.4% | 86.4% | 3.67 | 0.849 | **yes** |
| mondrian_crc_0.02 | 0.36% | 90.0% | 90.0% | 3.89 | 0.866 | **yes** |
| capped_crc_0.005 | 0.12% | 16.5% | 16.5% | 0.93 | 0.834 | **yes** |
| two_stage_0.005 | 0.24% | 48.4% | 16.5% | 2.10 | 0.814 | no |
| diagnosis_free_universal | 1.48% | 100.0% | 100.0% | 12.00 | 0.749 | no |

Frontier = no other policy is at least as good on clean loss, clean dispatch and closure and strictly better on one. Targets (v5 protocol): loss <= 0.5%, total clean dispatch <= 25%, mean cost <= 1.5, closure >= 0.80.

Policies meeting all four targets with a CRC guarantee: ['capped_crc_0.005']; without a guarantee: ['tau_none_5pct_fpr']. Claim rule result: capped_crc_0.005.

### seed 50 (CPU replication), CPU, v6

| Policy | Clean loss | Clean dispatch | Classifier-only dispatch | Clean mean cost | Mean closure | On frontier |
|---|---|---|---|---|---|---|
| tau_none_5pct_fpr | 0.08% | 3.1% | 3.1% | 0.16 | 0.849 | **yes** |
| global_crc_0.005 | 0.60% | 45.1% | 45.1% | 2.37 | 0.894 | **yes** |
| mondrian_crc_0.0025 | 0.20% | 66.7% | 66.7% | 2.84 | 0.586 | no |
| mondrian_crc_0.005 | 0.20% | 85.6% | 85.6% | 3.63 | 0.854 | **yes** |
| mondrian_crc_0.01 | 0.24% | 85.9% | 85.9% | 3.65 | 0.863 | **yes** |
| mondrian_crc_0.02 | 0.56% | 91.8% | 91.8% | 4.00 | 0.894 | **yes** |
| capped_crc_0.005 | 0.08% | 16.1% | 16.1% | 1.05 | 0.848 | no |
| two_stage_0.005 | 0.32% | 48.6% | 16.1% | 2.21 | 0.825 | no |
| diagnosis_free_universal | 1.63% | 100.0% | 100.0% | 12.00 | 0.761 | no |

Frontier = no other policy is at least as good on clean loss, clean dispatch and closure and strictly better on one. Targets (v5 protocol): loss <= 0.5%, total clean dispatch <= 25%, mean cost <= 1.5, closure >= 0.80.

Policies meeting all four targets with a CRC guarantee: ['capped_crc_0.005']; without a guarantee: ['tau_none_5pct_fpr']. Claim rule result: capped_crc_0.005.

### seed 50 (CPU, retrained attributor), CPU, v7 (composed arm; single-fault regression check)

| Policy | Clean loss | Clean dispatch | Classifier-only dispatch | Clean mean cost | Mean closure | On frontier |
|---|---|---|---|---|---|---|
| tau_none_5pct_fpr | 0.16% | 3.3% | 3.3% | 0.17 | 0.847 | **yes** |
| global_crc_0.005 | 0.64% | 44.4% | 44.4% | 2.36 | 0.892 | **yes** |
| mondrian_crc_0.0025 | 0.16% | 66.6% | 66.6% | 3.08 | 0.587 | no |
| mondrian_crc_0.005 | 0.16% | 85.4% | 85.4% | 4.03 | 0.846 | no |
| mondrian_crc_0.01 | 0.20% | 86.1% | 86.1% | 4.06 | 0.866 | **yes** |
| mondrian_crc_0.02 | 0.40% | 89.0% | 89.0% | 4.22 | 0.887 | **yes** |
| capped_crc_0.005 | 0.08% | 16.1% | 16.1% | 1.03 | 0.838 | **yes** |
| two_stage_0.005 | 0.32% | 48.8% | 16.1% | 2.19 | 0.815 | no |
| diagnosis_free_universal | 1.63% | 100.0% | 100.0% | 12.00 | 0.761 | no |

Frontier = no other policy is at least as good on clean loss, clean dispatch and closure and strictly better on one. Targets (v5 protocol): loss <= 0.5%, total clean dispatch <= 25%, mean cost <= 1.5, closure >= 0.80.

Policies meeting all four targets with a CRC guarantee: ['capped_crc_0.005']; without a guarantee: ['tau_none_5pct_fpr']. Claim rule result: capped_crc_0.005.
