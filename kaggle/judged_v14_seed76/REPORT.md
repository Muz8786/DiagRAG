# DiagRAG v6 judged run report

Device: cuda. Reranker: BAAI/bge-reranker-large. Last session runtime: 10822s.

## Verdict (gates fixed in JUDGED_PROTOCOL.json before results)

```
{
 "detectors_pass": 27,
 "repairs_pass": 27,
 "solved_both": 27,
 "of": 28,
 "new_faults": {
  "R25": {
   "detector": "PASS",
   "repair": "PASS"
  },
  "R26": {
   "detector": "THIN",
   "repair": "THIN"
  },
  "K11": {
   "detector": "PASS",
   "repair": "PASS"
  },
  "K12": {
   "detector": "PASS",
   "repair": "PASS"
  }
 },
 "family_repairs": [
  {
   "fault": "Q01",
   "family": "QLEX",
   "n": 100,
   "rescued": 46,
   "rate": 0.46,
   "ci_lo": 0.36560643853331865
  },
  {
   "fault": "Q03",
   "family": "QLEX",
   "n": 100,
   "rescued": 0,
   "rate": 0.0,
   "ci_lo": 0.0
  },
  {
   "fault": "Q04",
   "family": "QLEX",
   "n": 100,
   "rescued": 64,
   "rate": 0.64,
   "ci_lo": 0.542352199811621
  },
  {
   "fault": "Q05",
   "family": "QLEX",
   "n": 100,
   "rescued": 76,
   "rate": 0.76,
   "ci_lo": 0.6676748127670786
  },
  {
   "fault": "K04",
   "family": "STALE",
   "n": 100,
   "rescued": 94,
   "rate": 0.94,
   "ci_lo": 0.8752303146877749
  },
  {
   "fault": "R03",
   "family": "ENC",
   "n": 100,
   "rescued": 100,
   "rate": 1.0,
   "ci_lo": 0.963005192523998
  },
  {
   "fault": "R07",
   "family": "STALE",
   "n": 100,
   "rescued": 96,
   "rate": 0.96,
   "ci_lo": 0.9016278276739262
  },
  {
   "fault": "R10",
   "family": "ENC",
   "n": 100,
   "rescued": 100,
   "rate": 1.0,
   "ci_lo": 0.963005192523998
  },
  {
   "fault": "R11",
   "family": "ENC",
   "n": 100,
   "rescued": 100,
   "rate": 1.0,
   "ci_lo": 0.963005192523998
  }
 ],
 "loop_gates": {
  "L1": "PASS",
  "L2": "PASS",
  "U1": "FAIL",
  "N1": "PASS"
 },
 "grounded": {
  "faults": [
   "Q02",
   "Q03",
   "Q04",
   "Q05",
   "Q07",
   "K04",
   "K05",
   "K07",
   "K08",
   "K09",
   "R01",
   "R11",
   "R13",
   "R15",
   "R19",
   "R22",
   "R23",
   "R24",
   "R25",
   "R26",
   "K11",
   "K12"
  ],
  "detectors_pass": 20,
  "repairs_pass": 20,
  "solved_both": 20,
  "of": 22,
  "not_solved": [
   "Q03",
   "R26"
  ]
 },
 "quarantine": [
  "Q01",
  "Q09",
  "K03",
  "K06",
  "R03",
  "R05",
  "R06",
  "R07",
  "R10",
  "C2"
 ],
 "accounting": {
  "headline": "a_core28",
  "a_core28": {
   "detectors_pass": 27,
   "repairs_pass": 27,
   "solved_both": 27,
   "of": 28,
   "verdict": "ADOPTED",
   "not_solved": [
    "Q03"
   ],
   "thin": []
  },
  "b_grounded": {
   "faults": [
    "Q02",
    "Q03",
    "Q04",
    "Q05",
    "Q07",
    "K04",
    "K05",
    "K07",
    "K08",
    "K09",
    "R01",
    "R11",
    "R13",
    "R15",
    "R19",
    "R22",
    "R23",
    "R24",
    "R25",
    "R26",
    "K11",
    "K12"
   ],
   "detectors_pass": 20,
   "repairs_pass": 20,
   "solved_both": 20,
   "of": 22,
   "not_solved": [
    "Q03",
    "R26"
   ],
   "v4_baseline": "20/22 (Q03, R26)"
  },
  "c_quarantine": {
   "faults": [
    "Q01",
    "Q09",
    "K03",
    "K06",
    "R03",
    "R05",
    "R06",
    "R07",
    "R10",
    "C2"
   ],
   "detectors_pass": 10,
   "repairs_pass": 10,
   "solved_both": 10,
   "of": 10,
   "not_solved": []
  }
 },
 "cheap_guarantee": {
  "targets": {
   "T1": "held-out clean loss <= 0.005",
   "T2": "total clean dispatch <= 0.25",
   "T3": "clean mean cost <= 1.5",
   "T4": "mean closure >= 0.80"
  },
  "table": [
   {
    "policy": "tau_none_5pct_fpr",
    "clean_loss": 0.0007974481658692185,
    "clean_dispatch_rate": 0.03588516746411483,
    "clean_clf_dispatch_rate": 0.03588516746411483,
    "clean_mean_cost": 0.18859649122807018,
    "mean_closure": 0.836875,
    "T1_loss": true,
    "T2_dispatch": true,
    "T3_cost": true,
    "T4_closure": true,
    "all_targets_met": true
   },
   {
    "policy": "global_crc_0.005",
    "clean_loss": 0.006379585326953748,
    "clean_dispatch_rate": 0.5107655502392344,
    "clean_clf_dispatch_rate": 0.5107655502392344,
    "clean_mean_cost": 3.2188995215311005,
    "mean_closure": 0.87625,
    "T1_loss": false,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.0025",
    "clean_loss": 0.001594896331738437,
    "clean_dispatch_rate": 0.6658692185007975,
    "clean_clf_dispatch_rate": 0.6658692185007975,
    "clean_mean_cost": 3.582934609250399,
    "mean_closure": 0.596875,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": false,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.005",
    "clean_loss": 0.001594896331738437,
    "clean_dispatch_rate": 0.8560606060606061,
    "clean_clf_dispatch_rate": 0.8560606060606061,
    "clean_mean_cost": 4.116028708133971,
    "mean_closure": 0.8325,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.01",
    "clean_loss": 0.0023923444976076554,
    "clean_dispatch_rate": 0.8843700159489634,
    "clean_clf_dispatch_rate": 0.8843700159489634,
    "clean_mean_cost": 4.2842902711323765,
    "mean_closure": 0.86625,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.02",
    "clean_loss": 0.004784688995215311,
    "clean_dispatch_rate": 0.9346092503987241,
    "clean_clf_dispatch_rate": 0.9346092503987241,
    "clean_mean_cost": 4.640749601275917,
    "mean_closure": 0.87625,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "capped_crc_0.005",
    "clean_loss": 0.00039872408293460925,
    "clean_dispatch_rate": 0.13596491228070176,
    "clean_clf_dispatch_rate": 0.13596491228070176,
    "clean_mean_cost": 0.8995215311004785,
    "mean_closure": 0.82375,
    "T1_loss": true,
    "T2_dispatch": true,
    "T3_cost": true,
    "T4_closure": true,
    "all_targets_met": true
   },
   {
    "policy": "two_stage_0.005",
    "clean_loss": 0.0011961722488038277,
    "clean_dispatch_rate": 0.46810207336523124,
    "clean_clf_dispatch_rate": 0.13596491228070176,
    "clean_mean_cost": 2.0657894736842106,
    "mean_closure": 0.809375,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "diagnosis_free_universal",
    "clean_loss": 0.014752791068580542,
    "clean_dispatch_rate": 1.0,
    "clean_clf_dispatch_rate": 1.0,
    "clean_mean_cost": 12.0,
    "mean_closure": 0.745,
    "T1_loss": false,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": false,
    "all_targets_met": false
   }
  ],
  "guaranteed_policies_meeting_all_four": [
   "capped_crc_0.005"
  ],
  "no_guarantee_policies_meeting_all_four": [
   "tau_none_5pct_fpr"
  ],
  "claim": "capped_crc_0.005",
  "claim_rule": "the guarantee claim is as strong as the best CRC-based policy meeting T1-T4 together, and no stronger; None means no CRC-based policy met all four"
 },
 "U1": {
  "mean_closure": 0.3608,
  "mean_closure_without_fallback": 0.23120000000000002,
  "mean_closure_grounded": 0.33375,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5898058252427184,
  "hit_after": 0.6098300970873787,
  "delta": 0.020024271844660196,
  "ci_lo": 0.012135922330097087,
  "ci_hi": 0.028519417475728157,
  "fixed": 40,
  "broken": 7,
  "verdict": "PASS",
  "dispatched": 0.6966019417475728,
  "mean_cost": 5.08252427184466
 },
 "detection_baselines": {
  "ours_1_minus_pNONE": [
   0.976220709115446,
   0.9712131680313493,
   0.9810921446282246
  ],
  "qpp_neg_nqc": [
   0.5833104578170367,
   0.5633337507302582,
   0.601537944104029
  ],
  "qpp_neg_wig": [
   0.5712990226148121,
   0.5508559904182073,
   0.5913380094825454
  ],
  "neg_ce1": [
   0.6151166267942584,
   0.5955945749372971,
   0.6322225244096035
  ],
  "raglog_tier0_best_single_rag_rr_order": [
   0.5596124453032347,
   0.5407870840018042,
   0.5771086968314512
  ],
  "raglog_tier0_features_hgb": [
   0.7192968398560504,
   0.7026460294214348,
   0.7347774627535195
  ],
  "raglog_tier0_detect_rate_at_5pct_fa": 0.37756410256410255,
  "raglog_tier0_features": [
   "rag_rr_best_pos",
   "rag_rr_order",
   "rag_rr_top1_gap",
   "rag_rt_best_rank",
   "rag_rt_coverage",
   "rag_rt_coverage_2nd",
   "rag_rt_order",
   "rag_rt_reconstructed"
  ],
  "ours_detect_rate_at_5pct_fa": 0.9352564102564103
 },
 "repair_baselines": {
  "Q04:symspell": {
   "fault": "Q04",
   "repair": "symspell (external)",
   "n": 100,
   "rescued": 53,
   "ci_lo": 0.4328868313724773
  },
  "Q05:wordsegment": {
   "fault": "Q05",
   "repair": "wordsegment (external)",
   "n": 100,
   "rescued": 90,
   "ci_lo": 0.8256326956323347
  }
 },
 "raglog_error": null,
 "licence_dropped": {
  "rows": 84993,
  "by_partition": {
   "real_world_cc_by_4_0_abo": 84993
  }
 },
 "census": [
  {
   "signature": "misspelling token (q_correctable>=1)",
   "fault": "Q04",
   "n_queries": 7175,
   "with_signature": 785,
   "prevalence": 0.10940766550522649,
   "prev_ci_lo": 0.10239274288605618,
   "prev_ci_hi": 0.11684062200668642,
   "fail_rate_given": 0.46496815286624205,
   "fail_ci_lo": 0.430331658156215,
   "fail_ci_hi": 0.499945852563301,
   "share_of_all_failures": 0.11691223574631647
  },
  {
   "signature": "token absent from corpus vocabulary",
   "fault": "Q04/Q05",
   "n_queries": 7175,
   "with_signature": 728,
   "prevalence": 0.10146341463414635,
   "prev_ci_lo": 0.09468866735401069,
   "prev_ci_hi": 0.1086646981806182,
   "fail_rate_given": 0.5590659340659341,
   "fail_ci_lo": 0.5227824414420583,
   "fail_ci_hi": 0.5947293261316899,
   "share_of_all_failures": 0.13036515054452275
  },
  {
   "signature": "OOV token segmentable into corpus words",
   "fault": "Q05",
   "n_queries": 7175,
   "with_signature": 173,
   "prevalence": 0.02411149825783972,
   "prev_ci_lo": 0.020808563663594456,
   "prev_ci_hi": 0.027923755489400928,
   "fail_rate_given": 0.5317919075144508,
   "fail_ci_lo": 0.4575528637851965,
   "fail_ci_hi": 0.6046496948887805,
   "share_of_all_failures": 0.029468289557975657
  },
  {
   "signature": "unfinished last word (q_prefix)",
   "fault": "Q01",
   "n_queries": 7175,
   "with_signature": 48,
   "prevalence": 0.006689895470383275,
   "prev_ci_lo": 0.005049755294883588,
   "prev_ci_hi": 0.008858003862248392,
   "fail_rate_given": 0.5,
   "fail_ci_lo": 0.36389098932037767,
   "fail_ci_hi": 0.6361090106796222,
   "share_of_all_failures": 0.007687379884689302
  },
  {
   "signature": "identifier/code token",
   "fault": "Q07",
   "n_queries": 7175,
   "with_signature": 311,
   "prevalence": 0.04334494773519164,
   "prev_ci_lo": 0.038872386960387625,
   "prev_ci_hi": 0.048306246428040954,
   "fail_rate_given": 0.2990353697749196,
   "fail_ci_lo": 0.25085499253971905,
   "fail_ci_hi": 0.35211996375576415,
   "share_of_all_failures": 0.029788597053171044
  },
  {
   "signature": "conjunction / multi-intent marker",
   "fault": "Q09",
   "n_queries": 7175,
   "with_signature": 235,
   "prevalence": 0.032752613240418116,
   "prev_ci_lo": 0.02887768827836786,
   "prev_ci_hi": 0.03712761263257577,
   "fail_rate_given": 0.3872340425531915,
   "fail_ci_lo": 0.32724299654688443,
   "fail_ci_hi": 0.4508526115883818,
   "share_of_all_failures": 0.02914798206278027
  },
  {
   "signature": "exact duplicate pair in top-5",
   "fault": "K05",
   "n_queries": 7175,
   "with_signature": 590,
   "prevalence": 0.08222996515679443,
   "prev_ci_lo": 0.07609466300711182,
   "prev_ci_hi": 0.08881238829208386,
   "fail_rate_given": 0.535593220338983,
   "fail_ci_lo": 0.49524908018674163,
   "fail_ci_hi": 0.5754768507685838,
   "share_of_all_failures": 0.10121716848174248
  },
  {
   "signature": ">=2 chunks of one parent in top-5",
   "fault": "K12",
   "n_queries": 7175,
   "with_signature": 2728,
   "prevalence": 0.3802090592334495,
   "prev_ci_lo": 0.36904342007131996,
   "prev_ci_hi": 0.39150290539712335,
   "fail_rate_given": 0.3848973607038123,
   "fail_ci_lo": 0.36681221355167865,
   "fail_ci_hi": 0.40330622962599316,
   "share_of_all_failures": 0.336322869955157
  },
  {
   "signature": "'nan' placeholder doc in top-5",
   "fault": "K08",
   "n_queries": 7175,
   "with_signature": 3100,
   "prevalence": 0.43205574912891986,
   "prev_ci_lo": 0.42063292065284436,
   "prev_ci_hi": 0.4435512953632884,
   "fail_rate_given": 0.3258064516129032,
   "fail_ci_lo": 0.30953224319993683,
   "fail_ci_hi": 0.3425118559577007,
   "share_of_all_failures": 0.32351057014734147
  },
  {
   "signature": "'nan' placeholder ranked above the gold",
   "fault": "K08",
   "n_queries": 7175,
   "with_signature": 1127,
   "prevalence": 0.15707317073170732,
   "prev_ci_lo": 0.1488373411499806,
   "prev_ci_hi": 0.1656760198914443,
   "fail_rate_given": 0.6566104702750666,
   "fail_ci_lo": 0.6283973785925563,
   "fail_ci_hi": 0.6837595141146099,
   "share_of_all_failures": 0.2370275464445868
  },
  {
   "signature": "gold itself is a 'nan' placeholder doc",
   "fault": "K08",
   "n_queries": 7175,
   "with_signature": 4201,
   "prevalence": 0.5855052264808362,
   "prev_ci_lo": 0.5740633426107399,
   "prev_ci_hi": 0.5968555978489577,
   "fail_rate_given": 0.5136872173292073,
   "fail_ci_lo": 0.49856735098419586,
   "fail_ci_hi": 0.5287820740214928,
   "share_of_all_failures": 0.6912235746316464
  },
  {
   "signature": "ALL ESCI queries",
   "fault": "-",
   "n_queries": 7175,
   "with_signature": 7175,
   "prevalence": 1.0,
   "fail_rate_given": 0.4351219512195122,
   "fail_ci_lo": 0.42368798172099437,
   "fail_ci_hi": 0.44662535685441035
  }
 ],
 "verdict": "ADOPTED",
 "clean_net_hit_change": 0.001594896331738437,
 "guarantee": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 0.00019532647876674414,
   "esci_rare": 0.9648740067022706,
   "shop": 2.712730232090621e-05
  },
  "calibration": {
   "esci_common": {
    "n": 1503,
    "losses_if_all_dispatched": 1
   },
   "esci_rare": {
    "n": 269,
    "losses_if_all_dispatched": 9
   },
   "shop": {
    "n": 202,
    "losses_if_all_dispatched": 0
   }
  },
  "heldout_clean_loss": 0.001594896331738437,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0023923444976076554,
   "esci_rare": 0.0,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.8325,
  "L2": "PASS"
 },
 "policies": [
  {
   "policy": "tau_none_5pct_fpr",
   "mean_closure": 0.836875,
   "mean_closure_grounded": 0.8345454545454544,
   "mean_family_attribution": 0.8425,
   "mean_group_attribution": 0.8462500000000001,
   "mean_cost_faulted": 4.92375,
   "clean_dispatch_rate": 0.03588516746411483,
   "clean_clf_dispatch_rate": 0.03588516746411483,
   "clean_mean_cost": 0.18859649122807018,
   "clean_loss": 0.0007974481658692185,
   "clean_net_hit_change": 0.0,
   "clean_loss_esci_common": 0.0005980861244019139,
   "clean_loss_esci_rare": 0.0027100271002710027,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": true,
   "T3_cost": true,
   "T4_closure": true,
   "all_targets_met": true
  },
  {
   "policy": "global_crc_0.005",
   "mean_closure": 0.87625,
   "mean_closure_grounded": 0.8845454545454547,
   "mean_family_attribution": 0.8687499999999999,
   "mean_group_attribution": 0.8775,
   "mean_cost_faulted": 5.481875,
   "clean_dispatch_rate": 0.5107655502392344,
   "clean_clf_dispatch_rate": 0.5107655502392344,
   "clean_mean_cost": 3.2188995215311005,
   "clean_loss": 0.006379585326953748,
   "clean_net_hit_change": 0.0,
   "clean_loss_esci_common": 0.0011961722488038277,
   "clean_loss_esci_rare": 0.037940379403794036,
   "clean_loss_shop": 0.0,
   "T1_loss": false,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "mondrian_crc_0.0025",
   "mean_closure": 0.596875,
   "mean_closure_grounded": 0.5754545454545454,
   "mean_family_attribution": 0.5856250000000001,
   "mean_group_attribution": 0.5931250000000001,
   "mean_cost_faulted": 4.10125,
   "clean_dispatch_rate": 0.6658692185007975,
   "clean_clf_dispatch_rate": 0.6658692185007975,
   "clean_mean_cost": 3.582934609250399,
   "clean_loss": 0.001594896331738437,
   "clean_net_hit_change": 0.001594896331738437,
   "clean_loss_esci_common": 0.0023923444976076554,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": false,
   "all_targets_met": false
  },
  {
   "policy": "mondrian_crc_0.005",
   "mean_closure": 0.8325,
   "mean_closure_grounded": 0.8300000000000001,
   "mean_family_attribution": 0.83625,
   "mean_group_attribution": 0.844375,
   "mean_cost_faulted": 5.1743749999999995,
   "clean_dispatch_rate": 0.8560606060606061,
   "clean_clf_dispatch_rate": 0.8560606060606061,
   "clean_mean_cost": 4.116028708133971,
   "clean_loss": 0.001594896331738437,
   "clean_net_hit_change": 0.001594896331738437,
   "clean_loss_esci_common": 0.0023923444976076554,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "mondrian_crc_0.01",
   "mean_closure": 0.86625,
   "mean_closure_grounded": 0.8681818181818183,
   "mean_family_attribution": 0.865625,
   "mean_group_attribution": 0.875,
   "mean_cost_faulted": 5.3825,
   "clean_dispatch_rate": 0.8843700159489634,
   "clean_clf_dispatch_rate": 0.8843700159489634,
   "clean_mean_cost": 4.2842902711323765,
   "clean_loss": 0.0023923444976076554,
   "clean_net_hit_change": 0.001993620414673046,
   "clean_loss_esci_common": 0.0023923444976076554,
   "clean_loss_esci_rare": 0.005420054200542005,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "mondrian_crc_0.02",
   "mean_closure": 0.87625,
   "mean_closure_grounded": 0.8827272727272729,
   "mean_family_attribution": 0.8725,
   "mean_group_attribution": 0.881875,
   "mean_cost_faulted": 5.498125,
   "clean_dispatch_rate": 0.9346092503987241,
   "clean_clf_dispatch_rate": 0.9346092503987241,
   "clean_mean_cost": 4.640749601275917,
   "clean_loss": 0.004784688995215311,
   "clean_net_hit_change": 0.0023923444976076554,
   "clean_loss_esci_common": 0.0023923444976076554,
   "clean_loss_esci_rare": 0.02168021680216802,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "capped_crc_0.005",
   "mean_closure": 0.82375,
   "mean_closure_grounded": 0.8200000000000002,
   "mean_family_attribution": 0.8218749999999999,
   "mean_group_attribution": 0.8262499999999999,
   "mean_cost_faulted": 4.93,
   "clean_dispatch_rate": 0.13596491228070176,
   "clean_clf_dispatch_rate": 0.13596491228070176,
   "clean_mean_cost": 0.8995215311004785,
   "clean_loss": 0.00039872408293460925,
   "clean_net_hit_change": 0.0007974481658692185,
   "clean_loss_esci_common": 0.0005980861244019139,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": true,
   "T3_cost": true,
   "T4_closure": true,
   "all_targets_met": true
  },
  {
   "policy": "two_stage_0.005",
   "mean_closure": 0.809375,
   "mean_closure_grounded": 0.8309090909090912,
   "mean_family_attribution": 0.8225,
   "mean_group_attribution": 0.82875,
   "mean_cost_faulted": 6.311875000000001,
   "clean_dispatch_rate": 0.46810207336523124,
   "clean_clf_dispatch_rate": 0.13596491228070176,
   "clean_mean_cost": 2.0657894736842106,
   "clean_loss": 0.0011961722488038277,
   "clean_net_hit_change": 0.013556618819776715,
   "clean_loss_esci_common": 0.0017942583732057417,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "diagnosis_free_universal",
   "mean_closure": 0.745,
   "mean_closure_grounded": 0.7809090909090909,
   "mean_family_attribution": 0.0,
   "mean_group_attribution": 0.0,
   "mean_cost_faulted": 12.0,
   "clean_dispatch_rate": 1.0,
   "clean_clf_dispatch_rate": 1.0,
   "clean_mean_cost": 12.0,
   "clean_loss": 0.014752791068580542,
   "clean_net_hit_change": 0.007575757575757576,
   "clean_loss_esci_common": 0.01076555023923445,
   "clean_loss_esci_rare": 0.051490514905149054,
   "clean_loss_shop": 0.0,
   "T1_loss": false,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": false,
   "all_targets_met": false
  }
 ],
 "natural": [
  {
   "arm": "N1",
   "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6098300970873787,
   "delta": 0.020024271844660196,
   "ci_lo": 0.012135922330097087,
   "ci_hi": 0.028519417475728157,
   "fixed": 40,
   "broken": 7,
   "verdict": "PASS",
   "dispatched": 0.6966019417475728,
   "mean_cost": 5.08252427184466
  },
  {
   "arm": "N1a",
   "what": "component: natural rules only",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6116504854368932,
   "delta": 0.021844660194174758,
   "ci_lo": 0.013956310679611651,
   "ci_hi": 0.029733009708737865,
   "fixed": 41,
   "broken": 5,
   "verdict": "PASS"
  },
  {
   "arm": "N1b",
   "what": "component: classifier dispatch only",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.5922330097087378,
   "delta": 0.0024271844660194173,
   "ci_lo": -0.0006067961165048543,
   "ci_hi": 0.005476334951456228,
   "fixed": 6,
   "broken": 2,
   "verdict": "INCONCLUSIVE",
   "dispatched": 0.4866504854368932
  },
  {
   "arm": "B1",
   "what": "baseline: K12 parent collapse always on (no detection)",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6055825242718447,
   "delta": 0.015776699029126214,
   "ci_lo": 0.007888349514563107,
   "ci_hi": 0.024271844660194174,
   "fixed": 37,
   "broken": 11,
   "verdict": "PASS"
  },
  {
   "arm": "B2",
   "what": "baseline: diagnosis-free universal repair on every query (cost 12)",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6086165048543689,
   "delta": 0.018810679611650484,
   "ci_lo": 0.007281553398058253,
   "ci_hi": 0.03033980582524272,
   "fixed": 62,
   "broken": 31,
   "verdict": "PASS"
  },
  {
   "arm": "NA1",
   "what": "natural misspelling: ours (QLEX, log-gated)",
   "n": 185,
   "hit_before": 0.572972972972973,
   "hit_after": 0.518918918918919,
   "delta": -0.05405405405405406,
   "ci_lo": -0.10283783783783784,
   "ci_hi": -0.005405405405405406,
   "fixed": 7,
   "broken": 17,
   "verdict": "HARM"
  },
  {
   "arm": "NA1x",
   "what": "natural misspelling: SymSpell lookup_compound (external)",
   "n": 185,
   "hit_before": 0.572972972972973,
   "hit_after": 0.4486486486486487,
   "delta": -0.12432432432432433,
   "ci_lo": -0.1837837837837838,
   "ci_hi": -0.06486486486486487,
   "fixed": 5,
   "broken": 28,
   "verdict": "HARM"
  },
  {
   "arm": "NA2",
   "what": "natural missing space: ours (QLEX)",
   "n": 47,
   "hit_before": 0.5106382978723404,
   "hit_after": 0.46808510638297873,
   "delta": -0.0425531914893617,
   "ci_lo": -0.14893617021276595,
   "ci_hi": 0.06382978723404255,
   "fixed": 2,
   "broken": 4,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA2x",
   "what": "natural missing space: wordsegment (external)",
   "n": 47,
   "hit_before": 0.5106382978723404,
   "hit_after": 0.48936170212765956,
   "delta": -0.02127659574468085,
   "ci_lo": -0.10638297872340426,
   "ci_hi": 0.06382978723404255,
   "fixed": 2,
   "broken": 3,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA4",
   "what": "natural duplicate in top-5: K05 collapse",
   "n": 141,
   "hit_before": 0.5177304964539007,
   "hit_after": 0.5815602836879432,
   "delta": 0.06382978723404255,
   "ci_lo": 0.02127659574468085,
   "ci_hi": 0.11347517730496454,
   "fixed": 11,
   "broken": 2,
   "verdict": "PASS"
  },
  {
   "arm": "NA5",
   "what": "natural chunk crowding: K12 parent collapse",
   "n": 607,
   "hit_before": 0.6490939044481054,
   "hit_after": 0.6919275123558485,
   "delta": 0.042833607907743,
   "ci_lo": 0.02471169686985173,
   "ci_hi": 0.060955518945634266,
   "fixed": 30,
   "broken": 4,
   "verdict": "PASS"
  },
  {
   "arm": "NA1c",
   "what": "DEPLOYED LOOP, v5 config (natural typo repair OFF), on natural queries with q_correctable >= 1",
   "n": 185,
   "hit_before": 0.572972972972973,
   "hit_after": 0.5837837837837838,
   "delta": 0.010810810810810811,
   "ci_lo": 0.0,
   "ci_hi": 0.02702702702702703,
   "fixed": 2,
   "broken": 0,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA1d",
   "what": "counterfactual: same loop with the v4 config (natural typo repair ON), same queries",
   "n": 185,
   "hit_before": 0.572972972972973,
   "hit_after": 0.5837837837837838,
   "delta": 0.010810810810810811,
   "ci_lo": -0.010810810810810811,
   "ci_hi": 0.032432432432432434,
   "fixed": 3,
   "broken": 1,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "N1v4",
   "what": "counterfactual: DEPLOYED LOOP with the v4 config on all natural queries",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6098300970873787,
   "delta": 0.020024271844660196,
   "ci_lo": 0.011529126213592233,
   "ci_hi": 0.028534587378640695,
   "fixed": 42,
   "broken": 9,
   "verdict": "PASS"
  }
 ],
 "unseen_mean_closure": 0.3608,
 "not_solved": [
  "Q03"
 ],
 "device": "cuda",
 "reranker": "BAAI/bge-reranker-large"
}
```

{
 "detector": "held-out one-vs-rest AUROC >= 0.70 (point estimate) AND >= 50 held-out positives (v5 floor; fewer is THIN)",
 "repair": ">= 50 hard episodes (v5 floor; fewer is THIN) AND Wilson 95% lower bound of rescue rate >= 0.50 AND <= 10% of clean successes lost when the repair is forced on them",
 "solved": "detector PASS and repair PASS",
 "targets": "ADOPTED if repairs PASS >= 24/28 AND detectors PASS >= 27/28, else NOT_ADOPTED",
 "AUROC_BAR": 0.7,
 "MIN_TEST_POS": 50,
 "RESCUE_BAR_LB": 0.5,
 "MIN_REPAIR_N": 50,
 "MAX_HARM": 0.1,
 "REPAIR_TARGET": 24,
 "DETECT_TARGET": 27,
 "guarantee": "do-no-harm dispatch: threshold lambda fitted by conformal risk control on out-of-fold clean TRAIN queries so that E[Hit@5 lost on a clean query] <= ALPHA; PASS if held-out clean loss <= ALPHA; also report 200 calibration re-splits",
 "ALPHA": 0.005,
 "ALPHAS": [
  0.0025,
  0.005,
  0.01,
  0.02
 ],
 "natural": "report, not gated: (a) real misspelled ESCI queries whose corrected spelling was typed by another ESCI user, gold from ESCI labels; (b) in-corpus superseded policy versions with the validity filter off, no injected docs. Metrics: Hit@5 before, after closed loop (guarded and unguarded), after oracle repair, oracle-referenced closure",
 "unseen": "report, not gated: leave-one-fault-out attributor; on the held-out fault test episodes report flagged rate, right-group rate and Hit after dispatch",
 "v2_new_faults": "R25, R26, K11 judged with the same detector and repair gates; reported beside the 28, not counted in the 28-fault verdict",
 "v2_loop": "family-level dispatch; FAMILIES QLEX={Q01,Q03,Q04,Q05}, STALE={K04,R07}, ENC={R03,R10,R11}; attribution correct if the family is right. L1 PASS if held-out clean Hit@5 loss <= ALPHA under the CRC threshold fitted on the separate calibration split. L2 PASS if mean held-out closure over the 31 faults + C2 >= 0.70 under the same threshold",
 "L2_BAR": 0.7,
 "v2_natural": "arms NA1-NA6 on ESCI queries outside natural_exclusions_v1.json; selection by deployed rule only, never by gold; metric paired delta Hit@5 (repair - none) with 95% bootstrap CI (N_BOOT resamples); PASS if CI lower bound > 0, HARM if CI upper bound < 0, else INCONCLUSIVE",
 "v3_scope": "headline = GROUNDED set (evidence tier S/M/D, docs/EVIDENCE_AND_NOVELTY_REPORT.md section 2 + v3 additions); QUARANTINE set (tier N/P) is run and reported but excluded from headline claims",
 "L1": "do-no-harm, classifier dispatch: Mondrian CRC, one threshold per stratum (rarity x source), fitted on clean TRAIN queries never used to fit the attributor; PASS iff held-out clean Hit@5 loss <= ALPHA overall",
 "L2": "mean held-out closure over all faults + C2 >= 0.70 under the L1 thresholds",
 "U1": "unseen faults: mean leave-one-fault-out closure >= 0.50 with family-first dispatch + group fallback repairs",
 "N1": "natural traffic: deployed loop (natural rules K05/K12 + classifier at L1 thresholds) on ESCI queries outside natural_exclusions_v2.json; PASS iff the 95% bootstrap CI of paired delta Hit@5 has lower bound > 0",
 "G1": "grounded set: claim solved iff detector PASS and repair PASS; report count of the grounded set",
 "U1_BAR": 0.5,
 "v5_policies": "capped_crc_0.005: Mondrian CRC threshold, raised per stratum to the 80th percentile of the calibration clean score so classifier dispatch on clean is <= 20%; two_stage_0.005: precise rules (alone) or natural rules K12/K05 (additive) then the attributor at a capped threshold, calibrated on the combined loss. Targets reported together: T1 clean loss <= 0.005, T2 total clean dispatch <= 0.25, T3 clean mean cost <= 1.5, T4 mean closure >= 0.80. L1 and L2 stay defined on mondrian_crc_0.005 (L2 bar 0.70).",
 "v6_changes": "D1 base-query supply (N_BASE_ESCI 6000 = all examined ESCI queries); D2 C2 pair mix balanced within each split. Nothing else differs from v5.",
 "v5_accounting": "VERDICT.accounting: (a) core 28 under the original rule [headline], (b) grounded set, (c) quarantine set",
 "v5_deploy": "deployed config: natural-misspelling repair OFF on natural traffic (rep_QLEX not applied); injected-typo repair stays on; counterfactual v4 behaviour reported as h_loop_v4cfg, arms NA1c, NA1d, N1v4"
}

| fault   | tier   | grounded   | detector   | repair   | solved   |
|:--------|:-------|:-----------|:-----------|:---------|:---------|
| Q01     | N      | False      | PASS       | PASS     | True     |
| Q02     | M      | True       | PASS       | PASS     | True     |
| Q03     | M      | True       | FAIL       | FAIL     | False    |
| Q04     | S      | True       | PASS       | PASS     | True     |
| Q05     | M      | True       | PASS       | PASS     | True     |
| Q07     | M      | True       | PASS       | PASS     | True     |
| Q09     | P      | False      | PASS       | PASS     | True     |
| K03     | N      | False      | PASS       | PASS     | True     |
| K04     | M      | True       | PASS       | PASS     | True     |
| K05     | S      | True       | PASS       | PASS     | True     |
| K06     | N      | False      | PASS       | PASS     | True     |
| K07     | S      | True       | PASS       | PASS     | True     |
| K08     | M      | True       | PASS       | PASS     | True     |
| K09     | M      | True       | PASS       | PASS     | True     |
| R01     | S      | True       | PASS       | PASS     | True     |
| R03     | N      | False      | PASS       | PASS     | True     |
| R05     | N      | False      | PASS       | PASS     | True     |
| R06     | P      | False      | PASS       | PASS     | True     |
| R07     | P      | False      | PASS       | PASS     | True     |
| R10     | N      | False      | PASS       | PASS     | True     |
| R11     | S      | True       | PASS       | PASS     | True     |
| R13     | M      | True       | PASS       | PASS     | True     |
| R15     | S      | True       | PASS       | PASS     | True     |
| R19     | S      | True       | PASS       | PASS     | True     |
| R22     | S      | True       | PASS       | PASS     | True     |
| R23     | S      | True       | PASS       | PASS     | True     |
| R24     | M      | True       | PASS       | PASS     | True     |
| R25     | S      | True       | PASS       | PASS     | True     |
| R26     | S      | True       | THIN       | THIN     | False    |
| K11     | S      | True       | PASS       | PASS     | True     |
| K12     | S      | True       | PASS       | PASS     | True     |
| C2      | N      | False      | PASS       | PASS     | True     |

## Data verification

|            | file                                      |     bytes | size_ok   | sha256                                                           | sha_ok   |
|:-----------|:------------------------------------------|----------:|:----------|:-----------------------------------------------------------------|:---------|
| corpus     | kb_tier3_186k.jsonl.gz                    |  53518791 | True      | 5a9f7ea6ae5b8a3e7f1e1ca6e2838dddd6158efb9384d757c6aa755dbe9bda3c | True     |
| cache      | embeddings_cache_186k.npz                 | 533012659 | True      | 3b43603d9689f7c0eee0cbfebdb8b5cfddd05a2fc4e3cf192c8eed1de4a88835 | True     |
| esci       | shopping_queries_dataset_examples.parquet |  51286808 | True      | 4a735b693b4a424a6fc67f5be6e4c811495c488bbf66d02a602d308b2744263a | True     |
| exclusions | natural_exclusions_v2.json                |    165858 | True      | 974341cfb502af67e70ec15c8e9a31c96f8c03002eb9b901321b4db1ed83aeca | True     |
| qspell     | corpus-webis-qspell-17.zip                |   2285705 | True      | f13bd165544ab2ac75d63de4334feb86d74d1b3dfbe48d79423133552b5054e4 | True     |

## Purity

```
{
 "licence_dropped": {
  "rows": 84993,
  "by_partition": {
   "real_world_cc_by_4_0_abo": 84993
  }
 },
 "docs": 101297,
 "schemas": 1,
 "unique_ids": 101297,
 "empty_content": 0,
 "exact_dup_rows_beyond_first": 103,
 "exact_dup_groups": 54,
 "dup_groups_with_2plus_unflagged": 4,
 "flagged_dup_without_exact_twin": 45,
 "chunk_span_mismatch": 3554,
 "replacement_char_rows": 2,
 "nan_placeholder_docs": 3993,
 "license_status": {
  "synthetic_shopnova|unassigned": 1040,
  "real_world_apache_esci|verified": 13229,
  "real_world_cc_by_4_0_abo|verified": 86566,
  "real_world_apache_ofbiz_docs|verified": 462
 },
 "asin_in_both_esci_and_abo": 16,
 "emb": {
  "shape": [
   101297,
   768
  ],
  "nan": 0,
  "zero_rows": 0,
  "norm_min": 0.9999998807907104,
  "norm_max": 1.0000001192092896,
  "ids_in_order": true,
  "identical_rows_beyond_first": 42
 },
 "esci_queries_us_E_in_corpus": 7175,
 "esci_split_counts": {
  "train": 4529,
  "test": 2646
 },
 "esci_gold_components": 1829,
 "esci_test_gold_leak": 0,
 "v2_base_pool_seen": 5527,
 "v2_natural_pool_unseen": 1648,
 "query_log_queries": 90170
}
```

## Episode generation (hard = clean succeeds, faulted fails)

| fault   |   pool |   attempts |   not_applicable |   easy |   hard |   hard_train |   hard_test |   real_typos |   hard_yield |
|:--------|-------:|-----------:|-----------------:|-------:|-------:|-------------:|------------:|-------------:|-------------:|
| Q01     |   3081 |       1031 |              669 |    262 |    100 |           50 |          50 |            0 |        0.276 |
| Q02     |   3081 |        523 |                0 |    423 |    100 |           50 |          50 |            0 |        0.191 |
| Q03     |   3081 |        284 |               69 |    115 |    100 |           50 |          50 |            0 |        0.465 |
| Q04     |   3081 |        208 |                4 |    104 |    100 |           50 |          50 |           31 |        0.49  |
| Q05     |   3081 |        678 |               73 |    505 |    100 |           50 |          50 |            0 |        0.165 |
| Q07     |   2463 |       3797 |             2919 |    778 |    100 |           50 |          50 |            0 |        0.114 |
| Q09     |   3081 |        293 |                0 |    193 |    100 |           50 |          50 |            0 |        0.341 |
| K03     |   2020 |        915 |              703 |    112 |    100 |           50 |          50 |            0 |        0.472 |
| K04     |   3081 |        150 |                0 |     50 |    100 |           50 |          50 |            0 |        0.667 |
| K05     |   3081 |        258 |                0 |    158 |    100 |           50 |          50 |            0 |        0.388 |
| K06     |   1945 |        122 |                0 |     22 |    100 |           50 |          50 |            0 |        0.82  |
| K07     |    248 |        131 |                0 |     31 |    100 |           50 |          50 |            0 |        0.763 |
| K08     |   3081 |        138 |                0 |     38 |    100 |           50 |          50 |            0 |        0.725 |
| K09     |    284 |        168 |                0 |     68 |    100 |           50 |          50 |            0 |        0.595 |
| R01     |   3081 |        175 |                0 |     75 |    100 |           50 |          50 |            0 |        0.571 |
| R03     |   3081 |       1208 |                0 |   1108 |    100 |           50 |          50 |            0 |        0.083 |
| R05     |   3081 |        154 |                0 |     54 |    100 |           50 |          50 |            0 |        0.649 |
| R06     |   3081 |        100 |                0 |      0 |    100 |           50 |          50 |            0 |        1     |
| R07     |   3081 |        350 |                0 |    250 |    100 |           50 |          50 |            0 |        0.286 |
| R10     |   3081 |       1224 |                0 |   1124 |    100 |           50 |          50 |            0 |        0.082 |
| R11     |   3081 |       1171 |                0 |   1071 |    100 |           50 |          50 |            0 |        0.085 |
| R13     |   3081 |       1330 |                0 |   1230 |    100 |           50 |          50 |            0 |        0.075 |
| R15     |   3081 |        922 |                0 |    822 |    100 |           50 |          50 |            0 |        0.108 |
| R19     |   3081 |        665 |                0 |    565 |    100 |           50 |          50 |            0 |        0.15  |
| R22     |   3081 |       1382 |                0 |   1282 |    100 |           50 |          50 |            0 |        0.072 |
| R23     |   3081 |        282 |                0 |    182 |    100 |           50 |          50 |            0 |        0.355 |
| R24     |   3081 |        332 |                0 |    232 |    100 |           50 |          50 |            0 |        0.301 |
| R25     |   3081 |        273 |                0 |    173 |    100 |           50 |          50 |            0 |        0.366 |
| R26     |   3081 |       4000 |              985 |   2993 |     22 |           12 |          10 |            0 |        0.007 |
| K11     |   1945 |        108 |                0 |      8 |    100 |           50 |          50 |            0 |        0.926 |
| K12     |   3081 |        165 |                0 |     65 |    100 |           50 |          50 |            0 |        0.606 |
| C2      |   3081 |        252 |               59 |     93 |    100 |           50 |          50 |            0 |        0.518 |

## Detector gates (AUROC bar 0.7, min test positives 50)

| fault   | detector                             |   n_pos_train |   n_pos_test |   n_neg_test |   auroc |   ci_lo |   ci_hi |   auroc_vs_clean | status   |
|:--------|:-------------------------------------|--------------:|-------------:|-------------:|--------:|--------:|--------:|-----------------:|:---------|
| Q01     | histgb_head                          |            50 |           50 |         3968 |  0.9977 |  0.9964 |  0.9987 |           0.9980 | PASS     |
| Q02     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| Q03     | histgb_head                          |            50 |           50 |         3968 |  0.6939 |  0.6196 |  0.7645 |           0.6686 | FAIL     |
| Q04     | tier0_rule                           |            50 |           50 |         3968 |  0.9572 |  0.9088 |  0.9911 |           0.9599 | PASS     |
| Q05     | histgb_head                          |            50 |           50 |         3968 |  0.9645 |  0.9256 |  0.9878 |           0.9697 | PASS     |
| Q07     | histgb_head                          |            50 |           50 |         3968 |  0.9994 |  0.9988 |  0.9998 |           0.9994 | PASS     |
| Q09     | histgb_head                          |            50 |           50 |         3968 |  0.9991 |  0.9982 |  0.9998 |           0.9991 | PASS     |
| K03     | histgb_head                          |            50 |           50 |         3968 |  0.9996 |  0.9992 |  1.0000 |           0.9999 | PASS     |
| K04     | histgb_head                          |            50 |           50 |         3968 |  0.9580 |  0.9142 |  0.9939 |           0.9621 | PASS     |
| K05     | histgb_head                          |            50 |           50 |         3968 |  0.9999 |  0.9996 |  1.0000 |           1.0000 | PASS     |
| K06     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K07     | tier0_rule                           |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K08     | histgb_head                          |            50 |           50 |         3968 |  0.9999 |  0.9998 |  1.0000 |           1.0000 | PASS     |
| K09     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R01     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R03     | histgb_head                          |            50 |           50 |         3968 |  0.9998 |  0.9996 |  1.0000 |           0.9999 | PASS     |
| R05     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R06     | histgb_head                          |            50 |           50 |         3968 |  0.9891 |  0.9791 |  0.9958 |           0.9924 | PASS     |
| R07     | histgb_head                          |            50 |           50 |         3968 |  0.9992 |  0.9975 |  1.0000 |           0.9997 | PASS     |
| R10     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R11     | histgb_head                          |            50 |           50 |         3968 |  0.9992 |  0.9980 |  1.0000 |           1.0000 | PASS     |
| R13     | histgb_head                          |            50 |           50 |         3968 |  0.9945 |  0.9900 |  0.9982 |           0.9987 | PASS     |
| R15     | tier0_rule                           |            50 |           50 |         3968 |  0.9988 |  0.9979 |  0.9996 |           1.0000 | PASS     |
| R19     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R22     | histgb_head                          |            50 |           50 |         3968 |  0.9784 |  0.9490 |  0.9999 |           0.9806 | PASS     |
| R23     | tier0_rule                           |            50 |           50 |         3968 |  0.9995 |  0.9987 |  1.0000 |           1.0000 | PASS     |
| R24     | histgb_head                          |            50 |           50 |         3968 |  0.9118 |  0.8591 |  0.9561 |           0.9267 | PASS     |
| R25     | tier0_rule                           |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R26     | tier0_rule                           |            12 |           10 |         4008 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | THIN     |
| K11     | tier0_rule                           |            50 |           50 |         3968 |  0.9900 |  0.9639 |  1.0000 |           0.9900 | PASS     |
| K12     | histgb_head                          |            50 |           50 |         3968 |  0.9998 |  0.9995 |  1.0000 |           0.9997 | PASS     |
| C2      | tier0_rule(second factor-group mass) |            50 |           50 |         4018 |  0.7780 |  0.6829 |  0.8645 |         nan      | PASS     |

## Repair gates (Wilson lower bound >= 0.5)

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost |   harm_rate | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|------------:|:---------|
| Q01     |      100 |        64 |         0.640 |   0.542 |   0.727 |        20 |            0 |       0.000 | PASS     |
| Q02     |      100 |        86 |         0.860 |   0.779 |   0.915 |        20 |            0 |       0.000 | PASS     |
| Q03     |      100 |         1 |         0.010 |   0.002 |   0.054 |        20 |            0 |       0.000 | FAIL     |
| Q04     |      100 |        72 |         0.720 |   0.625 |   0.799 |        20 |            1 |       0.050 | PASS     |
| Q05     |      100 |        84 |         0.840 |   0.756 |   0.899 |        20 |            0 |       0.000 | PASS     |
| Q07     |      100 |        74 |         0.740 |   0.646 |   0.816 |        20 |            0 |       0.000 | PASS     |
| Q09     |      100 |        79 |         0.790 |   0.700 |   0.858 |        20 |            0 |       0.000 | PASS     |
| K03     |      100 |        86 |         0.860 |   0.779 |   0.915 |        20 |            0 |       0.000 | PASS     |
| K04     |      100 |        94 |         0.940 |   0.875 |   0.972 |        20 |            0 |       0.000 | PASS     |
| K05     |      100 |        97 |         0.970 |   0.915 |   0.990 |        20 |            0 |       0.000 | PASS     |
| K06     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K07     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K08     |      100 |        94 |         0.940 |   0.875 |   0.972 |        20 |            0 |       0.000 | PASS     |
| K09     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R01     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R03     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R05     |      100 |        99 |         0.990 |   0.946 |   0.998 |        20 |            0 |       0.000 | PASS     |
| R06     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R07     |      100 |        96 |         0.960 |   0.902 |   0.984 |        20 |            0 |       0.000 | PASS     |
| R10     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R11     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R13     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R15     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R19     |      100 |        93 |         0.930 |   0.863 |   0.966 |        20 |            0 |       0.000 | PASS     |
| R22     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R23     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R24     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R25     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R26     |       22 |        22 |         1.000 |   0.851 |   1.000 |        20 |            0 |       0.000 | THIN     |
| K11     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K12     |      100 |        96 |         0.960 |   0.902 |   0.984 |        20 |            0 |       0.000 | PASS     |
| C2      |      100 |        81 |         0.810 |   0.722 |   0.875 |         0 |            0 |       0.000 | PASS     |

## Dispatch policies (held-out)

| policy                   |   mean_closure |   mean_closure_grounded |   mean_family_attribution |   mean_group_attribution |   mean_cost_faulted |   clean_dispatch_rate |   clean_clf_dispatch_rate |   clean_mean_cost |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop | T1_loss   | T2_dispatch   | T3_cost   | T4_closure   | all_targets_met   |
|:-------------------------|---------------:|------------------------:|--------------------------:|-------------------------:|--------------------:|----------------------:|--------------------------:|------------------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|:----------|:--------------|:----------|:-------------|:------------------|
| tau_none_5pct_fpr        |         0.8369 |                  0.8345 |                    0.8425 |                   0.8463 |              4.9238 |                0.0359 |                    0.0359 |            0.1886 |       0.0008 |                 0.0000 |                   0.0006 |                 0.0027 |            0.0000 | True      | True          | True      | True         | True              |
| global_crc_0.005         |         0.8762 |                  0.8845 |                    0.8687 |                   0.8775 |              5.4819 |                0.5108 |                    0.5108 |            3.2189 |       0.0064 |                 0.0000 |                   0.0012 |                 0.0379 |            0.0000 | False     | False         | False     | True         | False             |
| mondrian_crc_0.0025      |         0.5969 |                  0.5755 |                    0.5856 |                   0.5931 |              4.1013 |                0.6659 |                    0.6659 |            3.5829 |       0.0016 |                 0.0016 |                   0.0024 |                 0.0000 |            0.0000 | True      | False         | False     | False        | False             |
| mondrian_crc_0.005       |         0.8325 |                  0.8300 |                    0.8363 |                   0.8444 |              5.1744 |                0.8561 |                    0.8561 |            4.1160 |       0.0016 |                 0.0016 |                   0.0024 |                 0.0000 |            0.0000 | True      | False         | False     | True         | False             |
| mondrian_crc_0.01        |         0.8662 |                  0.8682 |                    0.8656 |                   0.8750 |              5.3825 |                0.8844 |                    0.8844 |            4.2843 |       0.0024 |                 0.0020 |                   0.0024 |                 0.0054 |            0.0000 | True      | False         | False     | True         | False             |
| mondrian_crc_0.02        |         0.8762 |                  0.8827 |                    0.8725 |                   0.8819 |              5.4981 |                0.9346 |                    0.9346 |            4.6407 |       0.0048 |                 0.0024 |                   0.0024 |                 0.0217 |            0.0000 | True      | False         | False     | True         | False             |
| capped_crc_0.005         |         0.8237 |                  0.8200 |                    0.8219 |                   0.8262 |              4.9300 |                0.1360 |                    0.1360 |            0.8995 |       0.0004 |                 0.0008 |                   0.0006 |                 0.0000 |            0.0000 | True      | True          | True      | True         | True              |
| two_stage_0.005          |         0.8094 |                  0.8309 |                    0.8225 |                   0.8287 |              6.3119 |                0.4681 |                    0.1360 |            2.0658 |       0.0012 |                 0.0136 |                   0.0018 |                 0.0000 |            0.0000 | True      | False         | False     | True         | False             |
| diagnosis_free_universal |         0.7450 |                  0.7809 |                    0.0000 |                   0.0000 |             12.0000 |                1.0000 |                    1.0000 |           12.0000 |       0.0148 |                 0.0076 |                   0.0108 |                 0.0515 |            0.0000 | False     | False         | False     | False        | False             |

## Loop gates (L1 do-no-harm on held-out clean, L2 mean closure, U1 unseen, N1 natural traffic)

```
{
 "GUARANTEE": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 0.00019532647876674414,
   "esci_rare": 0.9648740067022706,
   "shop": 2.712730232090621e-05
  },
  "calibration": {
   "esci_common": {
    "n": 1503,
    "losses_if_all_dispatched": 1
   },
   "esci_rare": {
    "n": 269,
    "losses_if_all_dispatched": 9
   },
   "shop": {
    "n": 202,
    "losses_if_all_dispatched": 0
   }
  },
  "heldout_clean_loss": 0.001594896331738437,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0023923444976076554,
   "esci_rare": 0.0,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.8325,
  "L2": "PASS"
 },
 "U1": {
  "mean_closure": 0.3608,
  "mean_closure_without_fallback": 0.23120000000000002,
  "mean_closure_grounded": 0.33375,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5898058252427184,
  "hit_after": 0.6098300970873787,
  "delta": 0.020024271844660196,
  "ci_lo": 0.012135922330097087,
  "ci_hi": 0.028519417475728157,
  "fixed": 40,
  "broken": 7,
  "verdict": "PASS",
  "dispatched": 0.6966019417475728,
  "mean_cost": 5.08252427184466
 }
}
```

## Prevalence census (every ESCI query with an Exact product in the corpus)

| signature                               | fault   |   n_queries |   with_signature |   prevalence |   prev_ci_lo |   prev_ci_hi |   fail_rate_given |   fail_ci_lo |   fail_ci_hi |   share_of_all_failures |
|:----------------------------------------|:--------|------------:|-----------------:|-------------:|-------------:|-------------:|------------------:|-------------:|-------------:|------------------------:|
| misspelling token (q_correctable>=1)    | Q04     |        7175 |              785 |       0.1094 |       0.1024 |       0.1168 |            0.4650 |       0.4303 |       0.4999 |                  0.1169 |
| token absent from corpus vocabulary     | Q04/Q05 |        7175 |              728 |       0.1015 |       0.0947 |       0.1087 |            0.5591 |       0.5228 |       0.5947 |                  0.1304 |
| OOV token segmentable into corpus words | Q05     |        7175 |              173 |       0.0241 |       0.0208 |       0.0279 |            0.5318 |       0.4576 |       0.6046 |                  0.0295 |
| unfinished last word (q_prefix)         | Q01     |        7175 |               48 |       0.0067 |       0.0050 |       0.0089 |            0.5000 |       0.3639 |       0.6361 |                  0.0077 |
| identifier/code token                   | Q07     |        7175 |              311 |       0.0433 |       0.0389 |       0.0483 |            0.2990 |       0.2509 |       0.3521 |                  0.0298 |
| conjunction / multi-intent marker       | Q09     |        7175 |              235 |       0.0328 |       0.0289 |       0.0371 |            0.3872 |       0.3272 |       0.4509 |                  0.0291 |
| exact duplicate pair in top-5           | K05     |        7175 |              590 |       0.0822 |       0.0761 |       0.0888 |            0.5356 |       0.4952 |       0.5755 |                  0.1012 |
| >=2 chunks of one parent in top-5       | K12     |        7175 |             2728 |       0.3802 |       0.3690 |       0.3915 |            0.3849 |       0.3668 |       0.4033 |                  0.3363 |
| 'nan' placeholder doc in top-5          | K08     |        7175 |             3100 |       0.4321 |       0.4206 |       0.4436 |            0.3258 |       0.3095 |       0.3425 |                  0.3235 |
| 'nan' placeholder ranked above the gold | K08     |        7175 |             1127 |       0.1571 |       0.1488 |       0.1657 |            0.6566 |       0.6284 |       0.6838 |                  0.2370 |
| gold itself is a 'nan' placeholder doc  | K08     |        7175 |             4201 |       0.5855 |       0.5741 |       0.5969 |            0.5137 |       0.4986 |       0.5288 |                  0.6912 |
| ALL ESCI queries                        | -       |        7175 |             7175 |       1.0000 |     nan      |     nan      |            0.4351 |       0.4237 |       0.4466 |                nan      |

## Detection baselines (held-out, fault vs clean AUROC with 95% bootstrap CI)

| method                                |   auroc |   ci_lo |   ci_hi |
|:--------------------------------------|--------:|--------:|--------:|
| ours_1_minus_pNONE                    |  0.9762 |  0.9712 |  0.9811 |
| qpp_neg_nqc                           |  0.5833 |  0.5633 |  0.6015 |
| qpp_neg_wig                           |  0.5713 |  0.5509 |  0.5913 |
| neg_ce1                               |  0.6151 |  0.5956 |  0.6322 |
| raglog_tier0_best_single_rag_rr_order |  0.5596 |  0.5408 |  0.5771 |
| raglog_tier0_features_hgb             |  0.7193 |  0.7026 |  0.7348 |

## External repair baselines (oracle-dispatched, injected held-out + train episodes)

| fault   | repair                 |   n |   rescued |   ci_lo |
|:--------|:-----------------------|----:|----------:|--------:|
| Q04     | symspell (external)    | 100 |        53 |   0.433 |
| Q05     | wordsegment (external) | 100 |        90 |   0.826 |

## Family repairs, oracle-dispatched

| fault   | family   |   n |   rescued |   rate |   ci_lo |
|:--------|:---------|----:|----------:|-------:|--------:|
| Q01     | QLEX     | 100 |        46 |  0.460 |   0.366 |
| Q03     | QLEX     | 100 |         0 |  0.000 |   0.000 |
| Q04     | QLEX     | 100 |        64 |  0.640 |   0.542 |
| Q05     | QLEX     | 100 |        76 |  0.760 |   0.668 |
| K04     | STALE    | 100 |        94 |  0.940 |   0.875 |
| R03     | ENC      | 100 |       100 |  1.000 |   0.963 |
| R07     | STALE    | 100 |        96 |  0.960 |   0.902 |
| R10     | ENC      | 100 |       100 |  1.000 |   0.963 |
| R11     | ENC      | 100 |       100 |  1.000 |   0.963 |

## Natural traffic (no injection, never-examined queries): deployed loop, components, baselines

| arm   | what                                                                                           |    n |   hit_before |   hit_after |   delta |   ci_lo |   ci_hi |   fixed |   broken | verdict      |   dispatched |   mean_cost |
|:------|:-----------------------------------------------------------------------------------------------|-----:|-------------:|------------:|--------:|--------:|--------:|--------:|---------:|:-------------|-------------:|------------:|
| N1    | DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds                | 1648 |       0.5898 |      0.6098 |  0.0200 |  0.0121 |  0.0285 |      40 |        7 | PASS         |       0.6966 |      5.0825 |
| N1a   | component: natural rules only                                                                  | 1648 |       0.5898 |      0.6117 |  0.0218 |  0.0140 |  0.0297 |      41 |        5 | PASS         |     nan      |    nan      |
| N1b   | component: classifier dispatch only                                                            | 1648 |       0.5898 |      0.5922 |  0.0024 | -0.0006 |  0.0055 |       6 |        2 | INCONCLUSIVE |       0.4867 |    nan      |
| B1    | baseline: K12 parent collapse always on (no detection)                                         | 1648 |       0.5898 |      0.6056 |  0.0158 |  0.0079 |  0.0243 |      37 |       11 | PASS         |     nan      |    nan      |
| B2    | baseline: diagnosis-free universal repair on every query (cost 12)                             | 1648 |       0.5898 |      0.6086 |  0.0188 |  0.0073 |  0.0303 |      62 |       31 | PASS         |     nan      |    nan      |
| NA1   | natural misspelling: ours (QLEX, log-gated)                                                    |  185 |       0.5730 |      0.5189 | -0.0541 | -0.1028 | -0.0054 |       7 |       17 | HARM         |     nan      |    nan      |
| NA1x  | natural misspelling: SymSpell lookup_compound (external)                                       |  185 |       0.5730 |      0.4486 | -0.1243 | -0.1838 | -0.0649 |       5 |       28 | HARM         |     nan      |    nan      |
| NA2   | natural missing space: ours (QLEX)                                                             |   47 |       0.5106 |      0.4681 | -0.0426 | -0.1489 |  0.0638 |       2 |        4 | INCONCLUSIVE |     nan      |    nan      |
| NA2x  | natural missing space: wordsegment (external)                                                  |   47 |       0.5106 |      0.4894 | -0.0213 | -0.1064 |  0.0638 |       2 |        3 | INCONCLUSIVE |     nan      |    nan      |
| NA4   | natural duplicate in top-5: K05 collapse                                                       |  141 |       0.5177 |      0.5816 |  0.0638 |  0.0213 |  0.1135 |      11 |        2 | PASS         |     nan      |    nan      |
| NA5   | natural chunk crowding: K12 parent collapse                                                    |  607 |       0.6491 |      0.6919 |  0.0428 |  0.0247 |  0.0610 |      30 |        4 | PASS         |     nan      |    nan      |
| NA1c  | DEPLOYED LOOP, v5 config (natural typo repair OFF), on natural queries with q_correctable >= 1 |  185 |       0.5730 |      0.5838 |  0.0108 |  0.0000 |  0.0270 |       2 |        0 | INCONCLUSIVE |     nan      |    nan      |
| NA1d  | counterfactual: same loop with the v4 config (natural typo repair ON), same queries            |  185 |       0.5730 |      0.5838 |  0.0108 | -0.0108 |  0.0324 |       3 |        1 | INCONCLUSIVE |     nan      |    nan      |
| N1v4  | counterfactual: DEPLOYED LOOP with the v4 config on all natural queries                        | 1648 |       0.5898 |      0.6098 |  0.0200 |  0.0115 |  0.0285 |      42 |        9 | PASS         |     nan      |    nan      |

## Unseen faults (leave-one-fault-out attributor)

| fault   | tier   | family   |   n_test |   flagged |   right_group |   closure |   closure_without_group_fallback |
|:--------|:-------|:---------|---------:|----------:|--------------:|----------:|---------------------------------:|
| Q01     | N      | QLEX     |       50 |     0.660 |         0.640 |     0.260 |                            0.260 |
| Q02     | M      | Q02      |       50 |     0.300 |         0.040 |     0.000 |                            0.000 |
| Q03     | M      | QLEX     |       50 |     0.120 |         0.060 |     0.000 |                            0.000 |
| Q04     | S      | QLEX     |       50 |     0.700 |         0.520 |     0.400 |                            0.400 |
| Q05     | M      | QLEX     |       50 |     0.420 |         0.340 |     0.280 |                            0.260 |
| Q07     | M      | Q07      |       50 |     0.520 |         0.500 |     0.000 |                            0.000 |
| Q09     | P      | Q09      |       50 |     0.180 |         0.060 |     0.000 |                            0.000 |
| K03     | N      | K03      |       50 |     1.000 |         0.980 |     0.360 |                            0.140 |
| K04     | M      | STALE    |       50 |     0.940 |         0.000 |     0.900 |                            0.880 |
| K05     | S      | K05      |       50 |     1.000 |         1.000 |     0.880 |                            0.000 |
| K06     | N      | K06      |       50 |     1.000 |         1.000 |     0.000 |                            0.000 |
| K08     | M      | K08      |       50 |     0.820 |         0.720 |     0.240 |                            0.040 |
| K09     | M      | K09      |       50 |     0.880 |         0.880 |     0.080 |                            0.000 |
| R01     | S      | R01      |       50 |     0.240 |         0.140 |     0.100 |                            0.000 |
| R03     | N      | ENC      |       50 |     1.000 |         0.960 |     0.900 |                            0.720 |
| R05     | N      | R05      |       50 |     0.420 |         0.300 |     0.100 |                            0.020 |
| R06     | P      | R06      |       50 |     0.720 |         0.460 |     0.140 |                            0.000 |
| R07     | P      | STALE    |       50 |     1.000 |         0.000 |     0.960 |                            0.960 |
| R10     | N      | ENC      |       50 |     1.000 |         1.000 |     0.960 |                            0.940 |
| R11     | S      | ENC      |       50 |     1.000 |         1.000 |     1.000 |                            1.000 |
| R13     | M      | R13      |       50 |     0.400 |         0.180 |     0.240 |                            0.020 |
| R19     | S      | R19      |       50 |     0.780 |         0.620 |     0.480 |                            0.000 |
| R22     | S      | R22      |       50 |     0.340 |         0.140 |     0.200 |                            0.040 |
| R24     | M      | R24      |       50 |     0.160 |         0.040 |     0.100 |                            0.020 |
| K12     | S      | K12      |       50 |     0.740 |         0.700 |     0.440 |                            0.080 |

## Closed loop per fault and policy (held-out split)

| policy                   | fault   | tier   |   n_test |   dispatch_rate |   family_attribution |   group_attribution |   mean_cost |   clf_dispatch_rate |   closure |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop |
|:-------------------------|:--------|:-------|---------:|----------------:|---------------------:|--------------------:|------------:|--------------------:|----------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|
| tau_none_5pct_fpr        | Q01     | N      |       50 |           0.960 |                0.940 |               0.940 |       1.120 |               0.960 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q03     | M      |       50 |           0.020 |                0.020 |               0.020 |       0.020 |               0.020 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q04     | S      |       50 |           0.880 |                0.760 |               0.760 |       1.840 |               0.880 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q05     | M      |       50 |           0.660 |                0.460 |               0.460 |       2.260 |               0.660 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q07     | M      |       50 |           0.940 |                0.900 |               0.900 |       1.260 |               0.940 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q09     | P      |       50 |           1.000 |                0.980 |               0.980 |       1.160 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K03     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K04     | M      |       50 |           0.900 |                0.780 |               0.760 |       3.560 |               0.900 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K05     | S      |       50 |           1.000 |                0.840 |               0.900 |       3.520 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K08     | M      |       50 |           0.960 |                0.900 |               0.900 |       3.220 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R01     | S      |       50 |           1.000 |                0.960 |               0.960 |       7.880 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R03     | N      |       50 |           0.980 |                0.920 |               0.920 |       7.900 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R05     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R06     | P      |       50 |           0.800 |                0.680 |               0.680 |       6.560 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R07     | P      |       50 |           1.000 |                0.820 |               0.800 |       8.120 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R11     | S      |       50 |           1.000 |                0.900 |               0.900 |       8.140 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R13     | M      |       50 |           0.960 |                0.800 |               0.800 |       7.880 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R22     | S      |       50 |           0.780 |                0.700 |               0.700 |       6.200 |               0.780 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R23     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R24     | M      |       50 |           0.440 |                0.360 |               0.360 |       3.640 |               0.440 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K11     | S      |       50 |           0.980 |                0.980 |               0.980 |       2.940 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K12     | S      |       50 |           0.960 |                0.860 |               0.860 |       3.400 |               0.960 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | C2      | N      |       50 |           1.000 |                0.520 |               0.620 |       7.820 |               1.000 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | NONE    | -      |     2508 |           0.036 |                0.964 |               0.964 |       0.189 |               0.036 |   nan     |        0.001 |                  0.000 |                    0.001 |                  0.003 |             0.000 |
| global_crc_0.005         | Q01     | N      |       50 |           1.000 |                0.980 |               0.980 |       1.160 |               1.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q03     | M      |       50 |           0.800 |                0.260 |               0.260 |       5.040 |               0.800 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q04     | S      |       50 |           1.000 |                0.780 |               0.780 |       2.760 |               1.000 |     0.580 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q05     | M      |       50 |           1.000 |                0.620 |               0.620 |       4.020 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q07     | M      |       50 |           1.000 |                0.920 |               0.920 |       1.640 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q09     | P      |       50 |           1.000 |                0.980 |               0.980 |       1.160 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K03     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K04     | M      |       50 |           1.000 |                0.780 |               0.760 |       4.420 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K05     | S      |       50 |           1.000 |                0.840 |               0.900 |       3.520 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K08     | M      |       50 |           1.000 |                0.940 |               0.940 |       3.340 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R01     | S      |       50 |           1.000 |                0.960 |               0.960 |       7.880 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R03     | N      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R05     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R06     | P      |       50 |           0.960 |                0.720 |               0.760 |       7.920 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R07     | P      |       50 |           1.000 |                0.820 |               0.800 |       8.120 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R11     | S      |       50 |           1.000 |                0.900 |               0.900 |       8.140 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R13     | M      |       50 |           1.000 |                0.840 |               0.840 |       8.200 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R22     | S      |       50 |           1.000 |                0.860 |               0.900 |       8.020 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R23     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R24     | M      |       50 |           0.980 |                0.440 |               0.520 |       8.240 |               0.980 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       3.120 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K12     | S      |       50 |           1.000 |                0.860 |               0.860 |       3.700 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | C2      | N      |       50 |           1.000 |                0.520 |               0.620 |       7.820 |               1.000 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | NONE    | -      |     2508 |           0.511 |                0.489 |               0.489 |       3.219 |               0.511 |   nan     |        0.006 |                  0.000 |                    0.001 |                  0.038 |             0.000 |
| mondrian_crc_0.0025      | Q01     | N      |       50 |           0.100 |                0.100 |               0.100 |       0.100 |               0.100 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q02     | M      |       50 |           0.800 |                0.800 |               0.800 |       0.800 |               0.800 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q03     | M      |       50 |           0.960 |                0.380 |               0.380 |       5.440 |               0.960 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q04     | S      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q05     | M      |       50 |           0.020 |                0.000 |               0.000 |       0.160 |               0.020 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q07     | M      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q09     | P      |       50 |           0.700 |                0.700 |               0.700 |       0.700 |               0.700 |     0.580 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K03     | N      |       50 |           0.820 |                0.820 |               0.820 |       2.460 |               0.820 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K04     | M      |       50 |           0.760 |                0.600 |               0.580 |       3.500 |               0.760 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K05     | S      |       50 |           0.940 |                0.820 |               0.880 |       3.300 |               0.940 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K06     | N      |       50 |           0.740 |                0.740 |               0.740 |       2.220 |               0.740 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K07     | S      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K08     | M      |       50 |           0.760 |                0.740 |               0.740 |       2.440 |               0.760 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K09     | M      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R01     | S      |       50 |           0.880 |                0.860 |               0.860 |       7.060 |               0.880 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R03     | N      |       50 |           0.800 |                0.760 |               0.760 |       6.440 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R05     | N      |       50 |           0.720 |                0.720 |               0.720 |       5.760 |               0.720 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R06     | P      |       50 |           0.920 |                0.720 |               0.780 |       7.540 |               0.920 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R07     | P      |       50 |           0.860 |                0.740 |               0.720 |       7.100 |               0.860 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R10     | N      |       50 |           0.740 |                0.740 |               0.740 |       5.920 |               0.740 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R11     | S      |       50 |           0.840 |                0.760 |               0.760 |       6.840 |               0.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R13     | M      |       50 |           0.820 |                0.720 |               0.720 |       6.700 |               0.820 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R15     | S      |       50 |           0.800 |                0.800 |               0.800 |       6.400 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R19     | S      |       50 |           0.880 |                0.880 |               0.880 |       7.040 |               0.880 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R22     | S      |       50 |           0.800 |                0.720 |               0.760 |       6.520 |               0.800 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R23     | S      |       50 |           0.880 |                0.880 |               0.880 |       7.040 |               0.880 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R24     | M      |       50 |           0.880 |                0.440 |               0.520 |       7.340 |               0.880 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R25     | S      |       50 |           0.840 |                0.840 |               0.840 |       6.720 |               0.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R26     | S      |       10 |           0.700 |                0.700 |               0.700 |       5.600 |               0.700 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K11     | S      |       50 |           0.760 |                0.740 |               0.740 |       2.400 |               0.760 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K12     | S      |       50 |           0.800 |                0.680 |               0.680 |       3.080 |               0.800 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | C2      | N      |       50 |           0.480 |                0.340 |               0.380 |       4.620 |               0.480 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | NONE    | -      |     2508 |           0.666 |                0.334 |               0.334 |       3.583 |               0.666 |   nan     |        0.002 |                  0.002 |                    0.002 |                  0.000 |             0.000 |
| mondrian_crc_0.005       | Q01     | N      |       50 |           0.800 |                0.800 |               0.800 |       0.800 |               0.800 |     0.380 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q03     | M      |       50 |           0.960 |                0.380 |               0.380 |       5.440 |               0.960 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q04     | S      |       50 |           0.740 |                0.680 |               0.680 |       1.220 |               0.740 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q05     | M      |       50 |           0.220 |                0.140 |               0.140 |       0.840 |               0.220 |     0.160 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q07     | M      |       50 |           0.820 |                0.820 |               0.820 |       0.820 |               0.820 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q09     | P      |       50 |           0.920 |                0.900 |               0.900 |       1.080 |               0.920 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K03     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K04     | M      |       50 |           0.960 |                0.780 |               0.760 |       4.060 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K05     | S      |       50 |           1.000 |                0.840 |               0.900 |       3.520 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K08     | M      |       50 |           1.000 |                0.940 |               0.940 |       3.340 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R01     | S      |       50 |           1.000 |                0.960 |               0.960 |       7.880 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R03     | N      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R05     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R06     | P      |       50 |           0.960 |                0.740 |               0.800 |       7.880 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R07     | P      |       50 |           0.980 |                0.800 |               0.780 |       7.960 |               0.980 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R11     | S      |       50 |           1.000 |                0.900 |               0.900 |       8.140 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R13     | M      |       50 |           0.900 |                0.760 |               0.760 |       7.380 |               0.900 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R22     | S      |       50 |           0.880 |                0.760 |               0.800 |       7.200 |               0.880 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R23     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R24     | M      |       50 |           0.880 |                0.440 |               0.520 |       7.340 |               0.880 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       3.120 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K12     | S      |       50 |           1.000 |                0.860 |               0.860 |       3.700 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | C2      | N      |       50 |           0.780 |                0.480 |               0.540 |       6.660 |               0.780 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | NONE    | -      |     2508 |           0.856 |                0.144 |               0.144 |       4.116 |               0.856 |   nan     |        0.002 |                  0.002 |                    0.002 |                  0.000 |             0.000 |
| mondrian_crc_0.01        | Q01     | N      |       50 |           0.980 |                0.960 |               0.960 |       1.140 |               0.980 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q03     | M      |       50 |           0.960 |                0.380 |               0.380 |       5.440 |               0.960 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q04     | S      |       50 |           0.900 |                0.760 |               0.760 |       2.020 |               0.900 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q05     | M      |       50 |           0.740 |                0.500 |               0.500 |       2.640 |               0.740 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q07     | M      |       50 |           0.960 |                0.900 |               0.900 |       1.440 |               0.960 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q09     | P      |       50 |           1.000 |                0.980 |               0.980 |       1.160 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K03     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K04     | M      |       50 |           0.960 |                0.780 |               0.760 |       4.060 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K05     | S      |       50 |           1.000 |                0.840 |               0.900 |       3.520 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K08     | M      |       50 |           1.000 |                0.940 |               0.940 |       3.340 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R01     | S      |       50 |           1.000 |                0.960 |               0.960 |       7.880 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R03     | N      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R05     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R06     | P      |       50 |           1.000 |                0.740 |               0.800 |       8.240 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R07     | P      |       50 |           1.000 |                0.820 |               0.800 |       8.120 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R11     | S      |       50 |           1.000 |                0.900 |               0.900 |       8.140 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R13     | M      |       50 |           0.980 |                0.820 |               0.820 |       8.040 |               0.980 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R22     | S      |       50 |           0.960 |                0.820 |               0.860 |       7.700 |               0.960 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R23     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R24     | M      |       50 |           0.900 |                0.440 |               0.520 |       7.520 |               0.900 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       3.120 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K12     | S      |       50 |           1.000 |                0.860 |               0.860 |       3.700 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | C2      | N      |       50 |           1.000 |                0.520 |               0.620 |       7.820 |               1.000 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | NONE    | -      |     2508 |           0.884 |                0.116 |               0.116 |       4.284 |               0.884 |   nan     |        0.002 |                  0.002 |                    0.002 |                  0.005 |             0.000 |
| mondrian_crc_0.02        | Q01     | N      |       50 |           1.000 |                0.980 |               0.980 |       1.160 |               1.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q03     | M      |       50 |           1.000 |                0.380 |               0.380 |       5.800 |               1.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q04     | S      |       50 |           0.960 |                0.780 |               0.780 |       2.400 |               0.960 |     0.540 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q05     | M      |       50 |           0.980 |                0.600 |               0.600 |       4.000 |               0.980 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q07     | M      |       50 |           1.000 |                0.920 |               0.920 |       1.640 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q09     | P      |       50 |           1.000 |                0.980 |               0.980 |       1.160 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K03     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K04     | M      |       50 |           1.000 |                0.780 |               0.760 |       4.420 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K05     | S      |       50 |           1.000 |                0.840 |               0.900 |       3.520 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K08     | M      |       50 |           1.000 |                0.940 |               0.940 |       3.340 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R01     | S      |       50 |           1.000 |                0.960 |               0.960 |       7.880 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R03     | N      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R05     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R06     | P      |       50 |           1.000 |                0.740 |               0.800 |       8.240 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R07     | P      |       50 |           1.000 |                0.820 |               0.800 |       8.120 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R11     | S      |       50 |           1.000 |                0.900 |               0.900 |       8.140 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R13     | M      |       50 |           1.000 |                0.840 |               0.840 |       8.200 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R22     | S      |       50 |           1.000 |                0.860 |               0.900 |       8.020 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R23     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R24     | M      |       50 |           0.960 |                0.440 |               0.520 |       8.060 |               0.960 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       3.120 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K12     | S      |       50 |           1.000 |                0.860 |               0.860 |       3.700 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | C2      | N      |       50 |           1.000 |                0.520 |               0.620 |       7.820 |               1.000 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | NONE    | -      |     2508 |           0.935 |                0.065 |               0.065 |       4.641 |               0.935 |   nan     |        0.005 |                  0.002 |                    0.002 |                  0.022 |             0.000 |
| capped_crc_0.005         | Q01     | N      |       50 |           0.800 |                0.800 |               0.800 |       0.800 |               0.800 |     0.380 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q03     | M      |       50 |           0.120 |                0.040 |               0.040 |       0.740 |               0.120 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q04     | S      |       50 |           0.740 |                0.680 |               0.680 |       1.220 |               0.740 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q05     | M      |       50 |           0.220 |                0.140 |               0.140 |       0.840 |               0.220 |     0.160 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q07     | M      |       50 |           0.820 |                0.820 |               0.820 |       0.820 |               0.820 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q09     | P      |       50 |           0.920 |                0.900 |               0.900 |       1.080 |               0.920 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K03     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K04     | M      |       50 |           0.920 |                0.780 |               0.760 |       3.740 |               0.920 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K05     | S      |       50 |           1.000 |                0.840 |               0.900 |       3.520 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K08     | M      |       50 |           0.960 |                0.900 |               0.900 |       3.220 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R01     | S      |       50 |           1.000 |                0.960 |               0.960 |       7.880 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R03     | N      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R05     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R06     | P      |       50 |           0.900 |                0.720 |               0.740 |       7.400 |               0.900 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R07     | P      |       50 |           0.980 |                0.800 |               0.780 |       7.960 |               0.980 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R11     | S      |       50 |           1.000 |                0.900 |               0.900 |       8.140 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R13     | M      |       50 |           0.900 |                0.760 |               0.760 |       7.380 |               0.900 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R22     | S      |       50 |           0.820 |                0.740 |               0.740 |       6.720 |               0.820 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R23     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R24     | M      |       50 |           0.700 |                0.400 |               0.440 |       6.020 |               0.700 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K11     | S      |       50 |           0.980 |                0.980 |               0.980 |       2.940 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K12     | S      |       50 |           0.980 |                0.860 |               0.860 |       3.480 |               0.980 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | C2      | N      |       50 |           0.780 |                0.480 |               0.540 |       6.660 |               0.780 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | NONE    | -      |     2508 |           0.136 |                0.864 |               0.864 |       0.900 |               0.136 |   nan     |        0.000 |                  0.001 |                    0.001 |                  0.000 |             0.000 |
| two_stage_0.005          | Q01     | N      |       50 |           0.880 |                0.800 |               0.800 |       1.460 |               0.800 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       2.260 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q03     | M      |       50 |           0.620 |                0.040 |               0.040 |       2.360 |               0.120 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q04     | S      |       50 |           0.820 |                0.680 |               0.680 |       2.180 |               0.740 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q05     | M      |       50 |           0.540 |                0.140 |               0.140 |       2.040 |               0.220 |     0.300 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q07     | M      |       50 |           0.960 |                0.820 |               0.820 |       1.360 |               0.820 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q09     | P      |       50 |           0.960 |                0.900 |               0.900 |       2.880 |               0.920 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K03     | N      |       50 |           1.000 |                1.000 |               1.000 |       5.340 |               1.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K04     | M      |       50 |           0.960 |                0.780 |               0.800 |       5.060 |               0.920 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K05     | S      |       50 |           1.000 |                0.840 |               0.900 |       6.520 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       4.820 |               1.000 |     0.620 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       5.280 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K08     | M      |       50 |           0.980 |                0.900 |               0.920 |       5.920 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R01     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.960 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R03     | N      |       50 |           1.000 |                0.920 |               0.920 |       9.220 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R05     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.400 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R06     | P      |       50 |           0.940 |                0.720 |               0.740 |       8.600 |               0.900 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R07     | P      |       50 |           1.000 |                0.800 |               0.780 |       8.800 |               0.980 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       9.260 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R11     | S      |       50 |           1.000 |                0.900 |               0.900 |       8.980 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R13     | M      |       50 |           0.920 |                0.760 |               0.760 |       9.060 |               0.900 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       9.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       9.320 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R22     | S      |       50 |           0.860 |                0.740 |               0.740 |       7.680 |               0.820 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R23     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.300 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R24     | M      |       50 |           0.920 |                0.400 |               0.440 |       8.000 |               0.700 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       9.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.600 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K11     | S      |       50 |           0.980 |                0.980 |               0.980 |       5.100 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K12     | S      |       50 |           1.000 |                0.880 |               0.880 |       6.720 |               0.980 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | C2      | N      |       50 |           1.000 |                0.480 |               0.540 |       8.340 |               0.780 |     0.620 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | NONE    | -      |     2508 |           0.468 |                0.532 |               0.532 |       2.066 |               0.136 |   nan     |        0.001 |                  0.014 |                    0.002 |                  0.000 |             0.000 |
| diagnosis_free_universal | Q01     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.380 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q02     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.240 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q03     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q04     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.580 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q05     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q07     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q09     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.160 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K03     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.420 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K04     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K05     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K06     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.260 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K07     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K08     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.340 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K09     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R01     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R03     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R05     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R06     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R07     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R10     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R11     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R13     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R15     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R19     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R22     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R23     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R24     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R25     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R26     | S      |       10 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K11     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K12     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | C2      | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | NONE    | -      |     2508 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |   nan     |        0.015 |                  0.008 |                    0.011 |                  0.051 |             0.000 |
