# DiagRAG v6 judged run report

Device: cuda. Reranker: BAAI/bge-reranker-large. Last session runtime: 11241s.

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
   "rescued": 49,
   "rate": 0.49,
   "ci_lo": 0.3942183009238615
  },
  {
   "fault": "Q03",
   "family": "QLEX",
   "n": 100,
   "rescued": 1,
   "rate": 0.01,
   "ci_lo": 0.0017673865655472639
  },
  {
   "fault": "Q04",
   "family": "QLEX",
   "n": 100,
   "rescued": 72,
   "rate": 0.72,
   "ci_lo": 0.6251178763865428
  },
  {
   "fault": "Q05",
   "family": "QLEX",
   "n": 100,
   "rescued": 78,
   "rate": 0.78,
   "ci_lo": 0.689294652849997
  },
  {
   "fault": "K04",
   "family": "STALE",
   "n": 100,
   "rescued": 84,
   "rate": 0.84,
   "ci_lo": 0.7557955544110558
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
   "rescued": 100,
   "rate": 1.0,
   "ci_lo": 0.963005192523998
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
    "clean_dispatch_rate": 0.03269537480063796,
    "clean_clf_dispatch_rate": 0.03269537480063796,
    "clean_mean_cost": 0.145933014354067,
    "mean_closure": 0.83375,
    "T1_loss": true,
    "T2_dispatch": true,
    "T3_cost": true,
    "T4_closure": true,
    "all_targets_met": true
   },
   {
    "policy": "global_crc_0.005",
    "clean_loss": 0.00518341307814992,
    "clean_dispatch_rate": 0.4302232854864434,
    "clean_clf_dispatch_rate": 0.4302232854864434,
    "clean_mean_cost": 2.590510366826156,
    "mean_closure": 0.875625,
    "T1_loss": false,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.0025",
    "clean_loss": 0.0007974481658692185,
    "clean_dispatch_rate": 0.666267942583732,
    "clean_clf_dispatch_rate": 0.666267942583732,
    "clean_mean_cost": 3.5147527910685805,
    "mean_closure": 0.604375,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": false,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.005",
    "clean_loss": 0.0011961722488038277,
    "clean_dispatch_rate": 0.8608452950558214,
    "clean_clf_dispatch_rate": 0.8608452950558214,
    "clean_mean_cost": 4.187799043062201,
    "mean_closure": 0.85375,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.01",
    "clean_loss": 0.0011961722488038277,
    "clean_dispatch_rate": 0.8923444976076556,
    "clean_clf_dispatch_rate": 0.8923444976076556,
    "clean_mean_cost": 4.378787878787879,
    "mean_closure": 0.8718750000000001,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.02",
    "clean_loss": 0.003189792663476874,
    "clean_dispatch_rate": 0.9314194577352473,
    "clean_clf_dispatch_rate": 0.9314194577352473,
    "clean_mean_cost": 4.64274322169059,
    "mean_closure": 0.878125,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "capped_crc_0.005",
    "clean_loss": 0.0007974481658692185,
    "clean_dispatch_rate": 0.1419457735247209,
    "clean_clf_dispatch_rate": 0.1419457735247209,
    "clean_mean_cost": 0.919457735247209,
    "mean_closure": 0.840625,
    "T1_loss": true,
    "T2_dispatch": true,
    "T3_cost": true,
    "T4_closure": true,
    "all_targets_met": true
   },
   {
    "policy": "two_stage_0.005",
    "clean_loss": 0.001594896331738437,
    "clean_dispatch_rate": 0.46451355661881977,
    "clean_clf_dispatch_rate": 0.1419457735247209,
    "clean_mean_cost": 2.085725677830941,
    "mean_closure": 0.825,
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
    "mean_closure": 0.7625,
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
  "mean_closure": 0.3776,
  "mean_closure_without_fallback": 0.22479999999999997,
  "mean_closure_grounded": 0.3375,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5898058252427184,
  "hit_after": 0.6104368932038835,
  "delta": 0.02063106796116505,
  "ci_lo": 0.012742718446601941,
  "ci_hi": 0.02912621359223301,
  "fixed": 42,
  "broken": 8,
  "verdict": "PASS",
  "dispatched": 0.7117718446601942,
  "mean_cost": 5.005461165048544
 },
 "detection_baselines": {
  "ours_1_minus_pNONE": [
   0.9718288655788656,
   0.9661828001387351,
   0.9770683342493304
  ],
  "qpp_neg_nqc": [
   0.579357977548767,
   0.5606289891505223,
   0.5962262076255445
  ],
  "qpp_neg_wig": [
   0.5483192246350141,
   0.5276185085488178,
   0.5676266099550167
  ],
  "neg_ce1": [
   0.6072043818754346,
   0.589252424430723,
   0.6263703998549691
  ],
  "raglog_tier0_best_single_rag_rr_order": [
   0.562307283359915,
   0.5452018692553982,
   0.5816206733265262
  ],
  "raglog_tier0_features_hgb": [
   0.7191077015090173,
   0.7025086521551208,
   0.7341319734476198
  ],
  "raglog_tier0_detect_rate_at_5pct_fa": 0.3923076923076923,
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
  "ours_detect_rate_at_5pct_fa": 0.9198717948717948
 },
 "repair_baselines": {
  "Q04:symspell": {
   "fault": "Q04",
   "repair": "symspell (external)",
   "n": 100,
   "rescued": 60,
   "ci_lo": 0.5020007846184025
  },
  "Q05:wordsegment": {
   "fault": "Q05",
   "repair": "wordsegment (external)",
   "n": 100,
   "rescued": 93,
   "ci_lo": 0.8625032899347025
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
 "clean_net_hit_change": 0.0,
 "guarantee": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 6.57265257943962e-05,
   "esci_rare": 0.876501853561378,
   "shop": 5.726184461229966e-05
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
  "heldout_clean_loss": 0.0011961722488038277,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0011961722488038277,
   "esci_rare": 0.0027100271002710027,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.85375,
  "L2": "PASS"
 },
 "policies": [
  {
   "policy": "tau_none_5pct_fpr",
   "mean_closure": 0.83375,
   "mean_closure_grounded": 0.8354545454545454,
   "mean_family_attribution": 0.84125,
   "mean_group_attribution": 0.848125,
   "mean_cost_faulted": 4.8475,
   "clean_dispatch_rate": 0.03269537480063796,
   "clean_clf_dispatch_rate": 0.03269537480063796,
   "clean_mean_cost": 0.145933014354067,
   "clean_loss": 0.0007974481658692185,
   "clean_net_hit_change": -0.00039872408293460925,
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
   "mean_closure": 0.875625,
   "mean_closure_grounded": 0.8854545454545455,
   "mean_family_attribution": 0.8631249999999999,
   "mean_group_attribution": 0.879375,
   "mean_cost_faulted": 5.358750000000001,
   "clean_dispatch_rate": 0.4302232854864434,
   "clean_clf_dispatch_rate": 0.4302232854864434,
   "clean_mean_cost": 2.590510366826156,
   "clean_loss": 0.00518341307814992,
   "clean_net_hit_change": 0.0007974481658692185,
   "clean_loss_esci_common": 0.0011961722488038277,
   "clean_loss_esci_rare": 0.02981029810298103,
   "clean_loss_shop": 0.0,
   "T1_loss": false,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "mondrian_crc_0.0025",
   "mean_closure": 0.604375,
   "mean_closure_grounded": 0.5909090909090908,
   "mean_family_attribution": 0.596875,
   "mean_group_attribution": 0.608125,
   "mean_cost_faulted": 4.0575,
   "clean_dispatch_rate": 0.666267942583732,
   "clean_clf_dispatch_rate": 0.666267942583732,
   "clean_mean_cost": 3.5147527910685805,
   "clean_loss": 0.0007974481658692185,
   "clean_net_hit_change": 0.00039872408293460925,
   "clean_loss_esci_common": 0.0011961722488038277,
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
   "mean_closure": 0.85375,
   "mean_closure_grounded": 0.8599999999999999,
   "mean_family_attribution": 0.85125,
   "mean_group_attribution": 0.86625,
   "mean_cost_faulted": 5.203125,
   "clean_dispatch_rate": 0.8608452950558214,
   "clean_clf_dispatch_rate": 0.8608452950558214,
   "clean_mean_cost": 4.187799043062201,
   "clean_loss": 0.0011961722488038277,
   "clean_net_hit_change": 0.0,
   "clean_loss_esci_common": 0.0011961722488038277,
   "clean_loss_esci_rare": 0.0027100271002710027,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "mondrian_crc_0.01",
   "mean_closure": 0.8718750000000001,
   "mean_closure_grounded": 0.8818181818181817,
   "mean_family_attribution": 0.865,
   "mean_group_attribution": 0.880625,
   "mean_cost_faulted": 5.338125,
   "clean_dispatch_rate": 0.8923444976076556,
   "clean_clf_dispatch_rate": 0.8923444976076556,
   "clean_mean_cost": 4.378787878787879,
   "clean_loss": 0.0011961722488038277,
   "clean_net_hit_change": 0.001594896331738437,
   "clean_loss_esci_common": 0.0011961722488038277,
   "clean_loss_esci_rare": 0.0027100271002710027,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "mondrian_crc_0.02",
   "mean_closure": 0.878125,
   "mean_closure_grounded": 0.889090909090909,
   "mean_family_attribution": 0.868125,
   "mean_group_attribution": 0.8843749999999999,
   "mean_cost_faulted": 5.432499999999999,
   "clean_dispatch_rate": 0.9314194577352473,
   "clean_clf_dispatch_rate": 0.9314194577352473,
   "clean_mean_cost": 4.64274322169059,
   "clean_loss": 0.003189792663476874,
   "clean_net_hit_change": 0.0027910685805422647,
   "clean_loss_esci_common": 0.0011961722488038277,
   "clean_loss_esci_rare": 0.016260162601626018,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "capped_crc_0.005",
   "mean_closure": 0.840625,
   "mean_closure_grounded": 0.8427272727272727,
   "mean_family_attribution": 0.84,
   "mean_group_attribution": 0.849375,
   "mean_cost_faulted": 4.956875,
   "clean_dispatch_rate": 0.1419457735247209,
   "clean_clf_dispatch_rate": 0.1419457735247209,
   "clean_mean_cost": 0.919457735247209,
   "clean_loss": 0.0007974481658692185,
   "clean_net_hit_change": 0.00039872408293460925,
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
   "policy": "two_stage_0.005",
   "mean_closure": 0.825,
   "mean_closure_grounded": 0.85,
   "mean_family_attribution": 0.8418749999999999,
   "mean_group_attribution": 0.854375,
   "mean_cost_faulted": 6.351875,
   "clean_dispatch_rate": 0.46451355661881977,
   "clean_clf_dispatch_rate": 0.1419457735247209,
   "clean_mean_cost": 2.085725677830941,
   "clean_loss": 0.001594896331738437,
   "clean_net_hit_change": 0.013157894736842105,
   "clean_loss_esci_common": 0.0017942583732057417,
   "clean_loss_esci_rare": 0.0027100271002710027,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "diagnosis_free_universal",
   "mean_closure": 0.7625,
   "mean_closure_grounded": 0.7963636363636365,
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
   "hit_after": 0.6104368932038835,
   "delta": 0.02063106796116505,
   "ci_lo": 0.012742718446601941,
   "ci_hi": 0.02912621359223301,
   "fixed": 42,
   "broken": 8,
   "verdict": "PASS",
   "dispatched": 0.7117718446601942,
   "mean_cost": 5.005461165048544
  },
  {
   "arm": "N1a",
   "what": "component: natural rules only",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6116504854368932,
   "delta": 0.021844660194174758,
   "ci_lo": 0.014563106796116505,
   "ci_hi": 0.03033980582524272,
   "fixed": 41,
   "broken": 5,
   "verdict": "PASS"
  },
  {
   "arm": "N1b",
   "what": "component: classifier dispatch only",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.5910194174757282,
   "delta": 0.0012135922330097086,
   "ci_lo": -0.0018203883495145632,
   "ci_hi": 0.00424757281553398,
   "fixed": 5,
   "broken": 3,
   "verdict": "INCONCLUSIVE",
   "dispatched": 0.4830097087378641
  },
  {
   "arm": "B1",
   "what": "baseline: K12 parent collapse always on (no detection)",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6055825242718447,
   "delta": 0.015776699029126214,
   "ci_lo": 0.007873179611650486,
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
   "ci_lo": -0.10270270270270271,
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
   "ci_lo": -0.17851351351351352,
   "ci_hi": -0.07027027027027027,
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
   "ci_lo": 0.014184397163120567,
   "ci_hi": 0.12056737588652482,
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
   "ci_lo": 0.026359143327841845,
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
   "hit_after": 0.5783783783783784,
   "delta": 0.005405405405405406,
   "ci_lo": -0.021621621621621623,
   "ci_hi": 0.032432432432432434,
   "fixed": 4,
   "broken": 3,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "N1v4",
   "what": "counterfactual: DEPLOYED LOOP with the v4 config on all natural queries",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6104368932038835,
   "delta": 0.02063106796116505,
   "ci_lo": 0.012135922330097087,
   "ci_hi": 0.029733009708737865,
   "fixed": 46,
   "broken": 12,
   "verdict": "PASS"
  }
 ],
 "unseen_mean_closure": 0.3776,
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
| Q01     |   3081 |       1030 |              648 |    282 |    100 |           50 |          50 |            0 |        0.262 |
| Q02     |   3081 |        581 |                0 |    481 |    100 |           50 |          50 |            0 |        0.172 |
| Q03     |   3081 |        312 |               91 |    121 |    100 |           50 |          50 |            0 |        0.452 |
| Q04     |   3081 |        212 |                6 |    106 |    100 |           50 |          50 |           27 |        0.485 |
| Q05     |   3081 |        736 |               79 |    557 |    100 |           50 |          50 |            0 |        0.152 |
| Q07     |   2463 |       3093 |             2360 |    633 |    100 |           50 |          50 |            0 |        0.136 |
| Q09     |   3081 |        302 |                0 |    202 |    100 |           50 |          50 |            0 |        0.331 |
| K03     |   2020 |        956 |              745 |    111 |    100 |           50 |          50 |            0 |        0.474 |
| K04     |   3081 |        136 |                0 |     36 |    100 |           50 |          50 |            0 |        0.735 |
| K05     |   3081 |        254 |                0 |    154 |    100 |           50 |          50 |            0 |        0.394 |
| K06     |   1945 |        123 |                0 |     23 |    100 |           50 |          50 |            0 |        0.813 |
| K07     |    248 |        130 |                0 |     30 |    100 |           50 |          50 |            0 |        0.769 |
| K08     |   3081 |        132 |                0 |     32 |    100 |           50 |          50 |            0 |        0.758 |
| K09     |    284 |        165 |                0 |     65 |    100 |           50 |          50 |            0 |        0.606 |
| R01     |   3081 |        180 |                0 |     80 |    100 |           50 |          50 |            0 |        0.556 |
| R03     |   3081 |       1130 |                0 |   1030 |    100 |           50 |          50 |            0 |        0.088 |
| R05     |   3081 |        161 |                0 |     61 |    100 |           50 |          50 |            0 |        0.621 |
| R06     |   3081 |        100 |                0 |      0 |    100 |           50 |          50 |            0 |        1     |
| R07     |   3081 |        382 |                0 |    282 |    100 |           50 |          50 |            0 |        0.262 |
| R10     |   3081 |       1270 |                0 |   1170 |    100 |           50 |          50 |            0 |        0.079 |
| R11     |   3081 |       1227 |                0 |   1127 |    100 |           50 |          50 |            0 |        0.081 |
| R13     |   3081 |       1517 |                0 |   1417 |    100 |           50 |          50 |            0 |        0.066 |
| R15     |   3081 |        860 |                0 |    760 |    100 |           50 |          50 |            0 |        0.116 |
| R19     |   3081 |        714 |                0 |    614 |    100 |           50 |          50 |            0 |        0.14  |
| R22     |   3081 |       1299 |                0 |   1199 |    100 |           50 |          50 |            0 |        0.077 |
| R23     |   3081 |        264 |                0 |    164 |    100 |           50 |          50 |            0 |        0.379 |
| R24     |   3081 |        269 |                0 |    169 |    100 |           50 |          50 |            0 |        0.372 |
| R25     |   3081 |        301 |                0 |    201 |    100 |           50 |          50 |            0 |        0.332 |
| R26     |   3081 |       4000 |              985 |   2993 |     22 |           12 |          10 |            0 |        0.007 |
| K11     |   1945 |        107 |                0 |      7 |    100 |           50 |          50 |            0 |        0.935 |
| K12     |   3081 |        174 |                0 |     74 |    100 |           50 |          50 |            0 |        0.575 |
| C2      |   3081 |        216 |               54 |     62 |    100 |           50 |          50 |            0 |        0.617 |

## Detector gates (AUROC bar 0.7, min test positives 50)

| fault   | detector                             |   n_pos_train |   n_pos_test |   n_neg_test |   auroc |   ci_lo |   ci_hi |   auroc_vs_clean | status   |
|:--------|:-------------------------------------|--------------:|-------------:|-------------:|--------:|--------:|--------:|-----------------:|:---------|
| Q01     | histgb_head                          |            50 |           50 |         3968 |  0.9980 |  0.9968 |  0.9990 |           0.9980 | PASS     |
| Q02     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| Q03     | histgb_head                          |            50 |           50 |         3968 |  0.6337 |  0.5636 |  0.7073 |           0.6314 | FAIL     |
| Q04     | tier0_rule                           |            50 |           50 |         3968 |  0.9767 |  0.9501 |  0.9919 |           0.9788 | PASS     |
| Q05     | histgb_head                          |            50 |           50 |         3968 |  0.9779 |  0.9645 |  0.9896 |           0.9792 | PASS     |
| Q07     | histgb_head                          |            50 |           50 |         3968 |  0.9957 |  0.9882 |  0.9994 |           0.9963 | PASS     |
| Q09     | histgb_head                          |            50 |           50 |         3968 |  0.9992 |  0.9984 |  0.9998 |           0.9991 | PASS     |
| K03     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  0.9999 |  1.0000 |           1.0000 | PASS     |
| K04     | histgb_head                          |            50 |           50 |         3968 |  0.8581 |  0.7832 |  0.9187 |           0.8747 | PASS     |
| K05     | histgb_head                          |            50 |           50 |         3968 |  0.9999 |  0.9998 |  1.0000 |           0.9999 | PASS     |
| K06     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K07     | tier0_rule                           |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K08     | histgb_head                          |            50 |           50 |         3968 |  0.9955 |  0.9847 |  1.0000 |           0.9965 | PASS     |
| K09     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R01     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R03     | histgb_head                          |            50 |           50 |         3968 |  0.9999 |  0.9996 |  1.0000 |           0.9999 | PASS     |
| R05     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R06     | histgb_head                          |            50 |           50 |         3968 |  0.9923 |  0.9791 |  0.9993 |           0.9957 | PASS     |
| R07     | histgb_head                          |            50 |           50 |         3968 |  0.9997 |  0.9991 |  1.0000 |           0.9999 | PASS     |
| R10     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R11     | histgb_head                          |            50 |           50 |         3968 |  0.9999 |  0.9997 |  1.0000 |           1.0000 | PASS     |
| R13     | histgb_head                          |            50 |           50 |         3968 |  0.9999 |  0.9997 |  1.0000 |           1.0000 | PASS     |
| R15     | tier0_rule                           |            50 |           50 |         3968 |  0.9987 |  0.9978 |  0.9996 |           1.0000 | PASS     |
| R19     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R22     | histgb_head                          |            50 |           50 |         3968 |  0.9633 |  0.9209 |  0.9984 |           0.9671 | PASS     |
| R23     | tier0_rule                           |            50 |           50 |         3968 |  0.9995 |  0.9987 |  1.0000 |           1.0000 | PASS     |
| R24     | histgb_head                          |            50 |           50 |         3968 |  0.8500 |  0.7772 |  0.9138 |           0.8613 | PASS     |
| R25     | tier0_rule                           |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R26     | tier0_rule                           |            12 |           10 |         4008 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | THIN     |
| K11     | tier0_rule                           |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K12     | histgb_head                          |            50 |           50 |         3968 |  0.9912 |  0.9717 |  0.9997 |           0.9925 | PASS     |
| C2      | tier0_rule(second factor-group mass) |            50 |           50 |         4018 |  0.7313 |  0.6196 |  0.8190 |         nan      | PASS     |

## Repair gates (Wilson lower bound >= 0.5)

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost |   harm_rate | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|------------:|:---------|
| Q01     |      100 |        71 |         0.710 |   0.615 |   0.790 |        20 |            0 |       0.000 | PASS     |
| Q02     |      100 |        88 |         0.880 |   0.802 |   0.930 |        20 |            0 |       0.000 | PASS     |
| Q03     |      100 |         4 |         0.040 |   0.016 |   0.098 |        20 |            1 |       0.050 | FAIL     |
| Q04     |      100 |        80 |         0.800 |   0.711 |   0.867 |        20 |            0 |       0.000 | PASS     |
| Q05     |      100 |        88 |         0.880 |   0.802 |   0.930 |        20 |            0 |       0.000 | PASS     |
| Q07     |      100 |        79 |         0.790 |   0.700 |   0.858 |        20 |            0 |       0.000 | PASS     |
| Q09     |      100 |        71 |         0.710 |   0.615 |   0.790 |        20 |            0 |       0.000 | PASS     |
| K03     |      100 |        84 |         0.840 |   0.756 |   0.899 |        20 |            0 |       0.000 | PASS     |
| K04     |      100 |        84 |         0.840 |   0.756 |   0.899 |        20 |            0 |       0.000 | PASS     |
| K05     |      100 |        97 |         0.970 |   0.915 |   0.990 |        20 |            0 |       0.000 | PASS     |
| K06     |      100 |        97 |         0.970 |   0.915 |   0.990 |        20 |            0 |       0.000 | PASS     |
| K07     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K08     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K09     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R01     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R03     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R05     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R06     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R07     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R10     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R11     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R13     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R15     |      100 |        99 |         0.990 |   0.946 |   0.998 |        20 |            0 |       0.000 | PASS     |
| R19     |      100 |        93 |         0.930 |   0.863 |   0.966 |        20 |            1 |       0.050 | PASS     |
| R22     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R23     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R24     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R25     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R26     |       22 |        22 |         1.000 |   0.851 |   1.000 |        20 |            0 |       0.000 | THIN     |
| K11     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K12     |      100 |        89 |         0.890 |   0.814 |   0.937 |        20 |            0 |       0.000 | PASS     |
| C2      |      100 |        87 |         0.870 |   0.790 |   0.922 |         0 |            0 |       0.000 | PASS     |

## Dispatch policies (held-out)

| policy                   |   mean_closure |   mean_closure_grounded |   mean_family_attribution |   mean_group_attribution |   mean_cost_faulted |   clean_dispatch_rate |   clean_clf_dispatch_rate |   clean_mean_cost |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop | T1_loss   | T2_dispatch   | T3_cost   | T4_closure   | all_targets_met   |
|:-------------------------|---------------:|------------------------:|--------------------------:|-------------------------:|--------------------:|----------------------:|--------------------------:|------------------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|:----------|:--------------|:----------|:-------------|:------------------|
| tau_none_5pct_fpr        |         0.8337 |                  0.8355 |                    0.8413 |                   0.8481 |              4.8475 |                0.0327 |                    0.0327 |            0.1459 |       0.0008 |                -0.0004 |                   0.0006 |                 0.0027 |            0.0000 | True      | True          | True      | True         | True              |
| global_crc_0.005         |         0.8756 |                  0.8855 |                    0.8631 |                   0.8794 |              5.3588 |                0.4302 |                    0.4302 |            2.5905 |       0.0052 |                 0.0008 |                   0.0012 |                 0.0298 |            0.0000 | False     | False         | False     | True         | False             |
| mondrian_crc_0.0025      |         0.6044 |                  0.5909 |                    0.5969 |                   0.6081 |              4.0575 |                0.6663 |                    0.6663 |            3.5148 |       0.0008 |                 0.0004 |                   0.0012 |                 0.0000 |            0.0000 | True      | False         | False     | False        | False             |
| mondrian_crc_0.005       |         0.8538 |                  0.8600 |                    0.8512 |                   0.8662 |              5.2031 |                0.8608 |                    0.8608 |            4.1878 |       0.0012 |                 0.0000 |                   0.0012 |                 0.0027 |            0.0000 | True      | False         | False     | True         | False             |
| mondrian_crc_0.01        |         0.8719 |                  0.8818 |                    0.8650 |                   0.8806 |              5.3381 |                0.8923 |                    0.8923 |            4.3788 |       0.0012 |                 0.0016 |                   0.0012 |                 0.0027 |            0.0000 | True      | False         | False     | True         | False             |
| mondrian_crc_0.02        |         0.8781 |                  0.8891 |                    0.8681 |                   0.8844 |              5.4325 |                0.9314 |                    0.9314 |            4.6427 |       0.0032 |                 0.0028 |                   0.0012 |                 0.0163 |            0.0000 | True      | False         | False     | True         | False             |
| capped_crc_0.005         |         0.8406 |                  0.8427 |                    0.8400 |                   0.8494 |              4.9569 |                0.1419 |                    0.1419 |            0.9195 |       0.0008 |                 0.0004 |                   0.0006 |                 0.0027 |            0.0000 | True      | True          | True      | True         | True              |
| two_stage_0.005          |         0.8250 |                  0.8500 |                    0.8419 |                   0.8544 |              6.3519 |                0.4645 |                    0.1419 |            2.0857 |       0.0016 |                 0.0132 |                   0.0018 |                 0.0027 |            0.0000 | True      | False         | False     | True         | False             |
| diagnosis_free_universal |         0.7625 |                  0.7964 |                    0.0000 |                   0.0000 |             12.0000 |                1.0000 |                    1.0000 |           12.0000 |       0.0148 |                 0.0076 |                   0.0108 |                 0.0515 |            0.0000 | False     | False         | False     | False        | False             |

## Loop gates (L1 do-no-harm on held-out clean, L2 mean closure, U1 unseen, N1 natural traffic)

```
{
 "GUARANTEE": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 6.57265257943962e-05,
   "esci_rare": 0.876501853561378,
   "shop": 5.726184461229966e-05
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
  "heldout_clean_loss": 0.0011961722488038277,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0011961722488038277,
   "esci_rare": 0.0027100271002710027,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.85375,
  "L2": "PASS"
 },
 "U1": {
  "mean_closure": 0.3776,
  "mean_closure_without_fallback": 0.22479999999999997,
  "mean_closure_grounded": 0.3375,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5898058252427184,
  "hit_after": 0.6104368932038835,
  "delta": 0.02063106796116505,
  "ci_lo": 0.012742718446601941,
  "ci_hi": 0.02912621359223301,
  "fixed": 42,
  "broken": 8,
  "verdict": "PASS",
  "dispatched": 0.7117718446601942,
  "mean_cost": 5.005461165048544
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
| ours_1_minus_pNONE                    |  0.9718 |  0.9662 |  0.9771 |
| qpp_neg_nqc                           |  0.5794 |  0.5606 |  0.5962 |
| qpp_neg_wig                           |  0.5483 |  0.5276 |  0.5676 |
| neg_ce1                               |  0.6072 |  0.5893 |  0.6264 |
| raglog_tier0_best_single_rag_rr_order |  0.5623 |  0.5452 |  0.5816 |
| raglog_tier0_features_hgb             |  0.7191 |  0.7025 |  0.7341 |

## External repair baselines (oracle-dispatched, injected held-out + train episodes)

| fault   | repair                 |   n |   rescued |   ci_lo |
|:--------|:-----------------------|----:|----------:|--------:|
| Q04     | symspell (external)    | 100 |        60 |   0.502 |
| Q05     | wordsegment (external) | 100 |        93 |   0.863 |

## Family repairs, oracle-dispatched

| fault   | family   |   n |   rescued |   rate |   ci_lo |
|:--------|:---------|----:|----------:|-------:|--------:|
| Q01     | QLEX     | 100 |        49 |  0.490 |   0.394 |
| Q03     | QLEX     | 100 |         1 |  0.010 |   0.002 |
| Q04     | QLEX     | 100 |        72 |  0.720 |   0.625 |
| Q05     | QLEX     | 100 |        78 |  0.780 |   0.689 |
| K04     | STALE    | 100 |        84 |  0.840 |   0.756 |
| R03     | ENC      | 100 |       100 |  1.000 |   0.963 |
| R07     | STALE    | 100 |       100 |  1.000 |   0.963 |
| R10     | ENC      | 100 |       100 |  1.000 |   0.963 |
| R11     | ENC      | 100 |       100 |  1.000 |   0.963 |

## Natural traffic (no injection, never-examined queries): deployed loop, components, baselines

| arm   | what                                                                                           |    n |   hit_before |   hit_after |   delta |   ci_lo |   ci_hi |   fixed |   broken | verdict      |   dispatched |   mean_cost |
|:------|:-----------------------------------------------------------------------------------------------|-----:|-------------:|------------:|--------:|--------:|--------:|--------:|---------:|:-------------|-------------:|------------:|
| N1    | DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds                | 1648 |       0.5898 |      0.6104 |  0.0206 |  0.0127 |  0.0291 |      42 |        8 | PASS         |       0.7118 |      5.0055 |
| N1a   | component: natural rules only                                                                  | 1648 |       0.5898 |      0.6117 |  0.0218 |  0.0146 |  0.0303 |      41 |        5 | PASS         |     nan      |    nan      |
| N1b   | component: classifier dispatch only                                                            | 1648 |       0.5898 |      0.5910 |  0.0012 | -0.0018 |  0.0042 |       5 |        3 | INCONCLUSIVE |       0.4830 |    nan      |
| B1    | baseline: K12 parent collapse always on (no detection)                                         | 1648 |       0.5898 |      0.6056 |  0.0158 |  0.0079 |  0.0243 |      37 |       11 | PASS         |     nan      |    nan      |
| B2    | baseline: diagnosis-free universal repair on every query (cost 12)                             | 1648 |       0.5898 |      0.6086 |  0.0188 |  0.0073 |  0.0303 |      62 |       31 | PASS         |     nan      |    nan      |
| NA1   | natural misspelling: ours (QLEX, log-gated)                                                    |  185 |       0.5730 |      0.5189 | -0.0541 | -0.1027 | -0.0054 |       7 |       17 | HARM         |     nan      |    nan      |
| NA1x  | natural misspelling: SymSpell lookup_compound (external)                                       |  185 |       0.5730 |      0.4486 | -0.1243 | -0.1785 | -0.0703 |       5 |       28 | HARM         |     nan      |    nan      |
| NA2   | natural missing space: ours (QLEX)                                                             |   47 |       0.5106 |      0.4681 | -0.0426 | -0.1489 |  0.0638 |       2 |        4 | INCONCLUSIVE |     nan      |    nan      |
| NA2x  | natural missing space: wordsegment (external)                                                  |   47 |       0.5106 |      0.4894 | -0.0213 | -0.1064 |  0.0638 |       2 |        3 | INCONCLUSIVE |     nan      |    nan      |
| NA4   | natural duplicate in top-5: K05 collapse                                                       |  141 |       0.5177 |      0.5816 |  0.0638 |  0.0142 |  0.1206 |      11 |        2 | PASS         |     nan      |    nan      |
| NA5   | natural chunk crowding: K12 parent collapse                                                    |  607 |       0.6491 |      0.6919 |  0.0428 |  0.0264 |  0.0610 |      30 |        4 | PASS         |     nan      |    nan      |
| NA1c  | DEPLOYED LOOP, v5 config (natural typo repair OFF), on natural queries with q_correctable >= 1 |  185 |       0.5730 |      0.5838 |  0.0108 |  0.0000 |  0.0270 |       2 |        0 | INCONCLUSIVE |     nan      |    nan      |
| NA1d  | counterfactual: same loop with the v4 config (natural typo repair ON), same queries            |  185 |       0.5730 |      0.5784 |  0.0054 | -0.0216 |  0.0324 |       4 |        3 | INCONCLUSIVE |     nan      |    nan      |
| N1v4  | counterfactual: DEPLOYED LOOP with the v4 config on all natural queries                        | 1648 |       0.5898 |      0.6104 |  0.0206 |  0.0121 |  0.0297 |      46 |       12 | PASS         |     nan      |    nan      |

## Unseen faults (leave-one-fault-out attributor)

| fault   | tier   | family   |   n_test |   flagged |   right_group |   closure |   closure_without_group_fallback |
|:--------|:-------|:---------|---------:|----------:|--------------:|----------:|---------------------------------:|
| Q01     | N      | QLEX     |       50 |     0.580 |         0.460 |     0.220 |                            0.220 |
| Q02     | M      | Q02      |       50 |     0.520 |         0.220 |     0.020 |                            0.020 |
| Q03     | M      | QLEX     |       50 |     0.080 |         0.020 |     0.000 |                            0.000 |
| Q04     | S      | QLEX     |       50 |     0.540 |         0.420 |     0.360 |                            0.360 |
| Q05     | M      | QLEX     |       50 |     0.480 |         0.280 |     0.320 |                            0.320 |
| Q07     | M      | Q07      |       50 |     0.100 |         0.060 |     0.000 |                            0.000 |
| Q09     | P      | Q09      |       50 |     0.340 |         0.200 |     0.000 |                            0.000 |
| K03     | N      | K03      |       50 |     0.960 |         0.960 |     0.380 |                            0.080 |
| K04     | M      | STALE    |       50 |     0.720 |         0.000 |     0.700 |                            0.700 |
| K05     | S      | K05      |       50 |     1.000 |         1.000 |     0.860 |                            0.000 |
| K06     | N      | K06      |       50 |     1.000 |         1.000 |     0.100 |                            0.000 |
| K08     | M      | K08      |       50 |     0.840 |         0.840 |     0.480 |                            0.020 |
| K09     | M      | K09      |       50 |     0.600 |         0.580 |     0.600 |                            0.000 |
| R01     | S      | R01      |       50 |     0.280 |         0.120 |     0.080 |                            0.000 |
| R03     | N      | ENC      |       50 |     1.000 |         0.920 |     0.940 |                            0.760 |
| R05     | N      | R05      |       50 |     0.440 |         0.360 |     0.080 |                            0.040 |
| R06     | P      | R06      |       50 |     0.660 |         0.240 |     0.340 |                            0.000 |
| R07     | P      | STALE    |       50 |     0.980 |         0.000 |     0.980 |                            0.980 |
| R10     | N      | ENC      |       50 |     1.000 |         1.000 |     1.000 |                            0.980 |
| R11     | S      | ENC      |       50 |     1.000 |         1.000 |     1.000 |                            1.000 |
| R13     | M      | R13      |       50 |     0.260 |         0.080 |     0.120 |                            0.020 |
| R19     | S      | R19      |       50 |     0.740 |         0.620 |     0.380 |                            0.040 |
| R22     | S      | R22      |       50 |     0.320 |         0.120 |     0.140 |                            0.060 |
| R24     | M      | R24      |       50 |     0.180 |         0.120 |     0.080 |                            0.000 |
| K12     | S      | K12      |       50 |     0.480 |         0.420 |     0.260 |                            0.020 |

## Closed loop per fault and policy (held-out split)

| policy                   | fault   | tier   |   n_test |   dispatch_rate |   family_attribution |   group_attribution |   mean_cost |   clf_dispatch_rate |   closure |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop |
|:-------------------------|:--------|:-------|---------:|----------------:|---------------------:|--------------------:|------------:|--------------------:|----------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|
| tau_none_5pct_fpr        | Q01     | N      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q03     | M      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q04     | S      |       50 |           0.840 |                0.740 |               0.760 |       1.480 |               0.840 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q05     | M      |       50 |           0.720 |                0.640 |               0.640 |       1.360 |               0.720 |     0.580 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q07     | M      |       50 |           0.840 |                0.780 |               0.780 |       1.320 |               0.840 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q09     | P      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K03     | N      |       50 |           1.000 |                0.960 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K04     | M      |       50 |           0.700 |                0.620 |               0.620 |       2.740 |               0.700 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.180 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K08     | M      |       50 |           0.980 |                0.940 |               0.960 |       3.100 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R01     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R03     | N      |       50 |           0.980 |                0.940 |               0.940 |       7.880 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R05     | N      |       50 |           0.980 |                0.980 |               0.980 |       7.840 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R06     | P      |       50 |           0.780 |                0.740 |               0.740 |       6.360 |               0.780 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R07     | P      |       50 |           0.980 |                0.700 |               0.680 |       8.360 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R10     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R11     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R13     | M      |       50 |           1.000 |                0.900 |               0.900 |       8.020 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R15     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R19     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R22     | S      |       50 |           0.900 |                0.840 |               0.840 |       7.300 |               0.900 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R24     | M      |       50 |           0.380 |                0.280 |               0.280 |       3.220 |               0.380 |     0.360 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R25     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K12     | S      |       50 |           0.820 |                0.820 |               0.820 |       2.460 |               0.820 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | C2      | N      |       50 |           1.000 |                0.440 |               0.580 |       7.380 |               1.000 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | NONE    | -      |     2508 |           0.033 |                0.967 |               0.967 |       0.146 |               0.033 |   nan     |        0.001 |                 -0.000 |                    0.001 |                  0.003 |             0.000 |
| global_crc_0.005         | Q01     | N      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q03     | M      |       50 |           0.620 |                0.220 |               0.260 |       3.260 |               0.620 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q04     | S      |       50 |           1.000 |                0.780 |               0.820 |       2.440 |               1.000 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q05     | M      |       50 |           0.960 |                0.760 |               0.760 |       2.560 |               0.960 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q07     | M      |       50 |           1.000 |                0.800 |               0.800 |       2.600 |               1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q09     | P      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K03     | N      |       50 |           1.000 |                0.960 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K04     | M      |       50 |           0.880 |                0.620 |               0.620 |       3.920 |               0.880 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.180 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K08     | M      |       50 |           1.000 |                0.960 |               0.980 |       3.160 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R01     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R03     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.100 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R05     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R06     | P      |       50 |           1.000 |                0.820 |               0.860 |       8.220 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R07     | P      |       50 |           1.000 |                0.720 |               0.700 |       8.520 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R10     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R11     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R13     | M      |       50 |           1.000 |                0.900 |               0.900 |       8.020 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R15     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R19     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R22     | S      |       50 |           0.980 |                0.860 |               0.880 |       7.980 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R24     | M      |       50 |           0.940 |                0.420 |               0.560 |       7.780 |               0.940 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R25     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K12     | S      |       50 |           0.980 |                0.840 |               0.880 |       3.220 |               0.980 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | C2      | N      |       50 |           1.000 |                0.440 |               0.580 |       7.380 |               1.000 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | NONE    | -      |     2508 |           0.430 |                0.570 |               0.570 |       2.591 |               0.430 |   nan     |        0.005 |                  0.001 |                    0.001 |                  0.030 |             0.000 |
| mondrian_crc_0.0025      | Q01     | N      |       50 |           0.080 |                0.060 |               0.060 |       0.240 |               0.080 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q02     | M      |       50 |           0.820 |                0.820 |               0.820 |       0.820 |               0.820 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q03     | M      |       50 |           0.860 |                0.320 |               0.360 |       4.320 |               0.860 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q04     | S      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q05     | M      |       50 |           0.040 |                0.020 |               0.020 |       0.180 |               0.040 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q07     | M      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q09     | P      |       50 |           0.860 |                0.860 |               0.860 |       0.860 |               0.860 |     0.580 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K03     | N      |       50 |           0.900 |                0.860 |               0.900 |       2.700 |               0.900 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K04     | M      |       50 |           0.840 |                0.540 |               0.540 |       4.000 |               0.840 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K05     | S      |       50 |           0.960 |                0.920 |               0.940 |       3.040 |               0.960 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K06     | N      |       50 |           0.760 |                0.760 |               0.760 |       2.280 |               0.760 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K07     | S      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K08     | M      |       50 |           0.800 |                0.760 |               0.780 |       2.560 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K09     | M      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R01     | S      |       50 |           0.800 |                0.800 |               0.800 |       6.400 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R03     | N      |       50 |           0.840 |                0.820 |               0.820 |       6.780 |               0.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R05     | N      |       50 |           0.800 |                0.800 |               0.800 |       6.400 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R06     | P      |       50 |           0.800 |                0.660 |               0.700 |       6.580 |               0.800 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R07     | P      |       50 |           0.900 |                0.700 |               0.680 |       7.560 |               0.900 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R10     | N      |       50 |           0.720 |                0.720 |               0.720 |       5.760 |               0.720 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R11     | S      |       50 |           0.880 |                0.860 |               0.860 |       7.100 |               0.880 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R13     | M      |       50 |           0.840 |                0.800 |               0.800 |       6.840 |               0.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R15     | S      |       50 |           0.800 |                0.800 |               0.800 |       6.400 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R19     | S      |       50 |           0.800 |                0.800 |               0.800 |       6.400 |               0.800 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R22     | S      |       50 |           0.760 |                0.660 |               0.680 |       6.040 |               0.760 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R23     | S      |       50 |           0.860 |                0.860 |               0.860 |       6.880 |               0.860 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R24     | M      |       50 |           0.960 |                0.440 |               0.580 |       7.780 |               0.960 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R25     | S      |       50 |           0.920 |                0.920 |               0.920 |       7.360 |               0.920 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R26     | S      |       10 |           0.700 |                0.700 |               0.700 |       5.600 |               0.700 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K11     | S      |       50 |           0.840 |                0.840 |               0.840 |       2.520 |               0.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K12     | S      |       50 |           0.900 |                0.760 |               0.800 |       2.980 |               0.900 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | C2      | N      |       50 |           0.380 |                0.240 |               0.260 |       3.460 |               0.380 |     0.280 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | NONE    | -      |     2508 |           0.666 |                0.334 |               0.334 |       3.515 |               0.666 |   nan     |        0.001 |                  0.000 |                    0.001 |                  0.000 |             0.000 |
| mondrian_crc_0.005       | Q01     | N      |       50 |           0.940 |                0.880 |               0.880 |       1.420 |               0.940 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q03     | M      |       50 |           0.860 |                0.320 |               0.360 |       4.320 |               0.860 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q04     | S      |       50 |           0.700 |                0.640 |               0.660 |       1.020 |               0.700 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q05     | M      |       50 |           0.620 |                0.580 |               0.580 |       0.920 |               0.620 |     0.500 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q07     | M      |       50 |           0.800 |                0.740 |               0.740 |       1.280 |               0.800 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q09     | P      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K03     | N      |       50 |           1.000 |                0.960 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K04     | M      |       50 |           0.920 |                0.620 |               0.620 |       4.240 |               0.920 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.180 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K08     | M      |       50 |           0.980 |                0.940 |               0.960 |       3.100 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R01     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R03     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.100 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R05     | N      |       50 |           0.980 |                0.980 |               0.980 |       7.840 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R06     | P      |       50 |           0.940 |                0.800 |               0.840 |       7.700 |               0.940 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R07     | P      |       50 |           1.000 |                0.720 |               0.700 |       8.520 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R10     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R11     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R13     | M      |       50 |           0.960 |                0.880 |               0.880 |       7.680 |               0.960 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R15     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R19     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R22     | S      |       50 |           0.960 |                0.820 |               0.840 |       7.680 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R24     | M      |       50 |           0.960 |                0.440 |               0.580 |       7.780 |               0.960 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R25     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K12     | S      |       50 |           0.980 |                0.840 |               0.880 |       3.220 |               0.980 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | C2      | N      |       50 |           0.960 |                0.440 |               0.560 |       7.180 |               0.960 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | NONE    | -      |     2508 |           0.861 |                0.139 |               0.139 |       4.188 |               0.861 |   nan     |        0.001 |                  0.000 |                    0.001 |                  0.003 |             0.000 |
| mondrian_crc_0.01        | Q01     | N      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q03     | M      |       50 |           0.860 |                0.320 |               0.360 |       4.320 |               0.860 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q04     | S      |       50 |           0.860 |                0.760 |               0.780 |       1.500 |               0.860 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q05     | M      |       50 |           0.880 |                0.720 |               0.720 |       2.140 |               0.880 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q07     | M      |       50 |           0.920 |                0.800 |               0.800 |       1.880 |               0.920 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q09     | P      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K03     | N      |       50 |           1.000 |                0.960 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K04     | M      |       50 |           0.940 |                0.620 |               0.620 |       4.400 |               0.940 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.180 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K08     | M      |       50 |           1.000 |                0.960 |               0.980 |       3.160 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R01     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R03     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.100 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R05     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R06     | P      |       50 |           0.960 |                0.820 |               0.860 |       7.860 |               0.960 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R07     | P      |       50 |           1.000 |                0.720 |               0.700 |       8.520 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R10     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R11     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R13     | M      |       50 |           1.000 |                0.900 |               0.900 |       8.020 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R15     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R19     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R22     | S      |       50 |           1.000 |                0.860 |               0.880 |       8.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R24     | M      |       50 |           0.960 |                0.440 |               0.580 |       7.780 |               0.960 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R25     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K12     | S      |       50 |           1.000 |                0.840 |               0.880 |       3.440 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | C2      | N      |       50 |           1.000 |                0.440 |               0.580 |       7.380 |               1.000 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | NONE    | -      |     2508 |           0.892 |                0.108 |               0.108 |       4.379 |               0.892 |   nan     |        0.001 |                  0.002 |                    0.001 |                  0.003 |             0.000 |
| mondrian_crc_0.02        | Q01     | N      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q03     | M      |       50 |           0.960 |                0.360 |               0.400 |       4.900 |               0.960 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q04     | S      |       50 |           0.960 |                0.760 |               0.800 |       2.240 |               0.960 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q05     | M      |       50 |           1.000 |                0.780 |               0.780 |       2.740 |               1.000 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q07     | M      |       50 |           1.000 |                0.800 |               0.800 |       2.600 |               1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q09     | P      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K03     | N      |       50 |           1.000 |                0.960 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K04     | M      |       50 |           0.960 |                0.620 |               0.620 |       4.420 |               0.960 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.180 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K08     | M      |       50 |           1.000 |                0.960 |               0.980 |       3.160 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R01     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R03     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.100 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R05     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R06     | P      |       50 |           1.000 |                0.820 |               0.860 |       8.220 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R07     | P      |       50 |           1.000 |                0.720 |               0.700 |       8.520 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R10     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R11     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R13     | M      |       50 |           1.000 |                0.900 |               0.900 |       8.020 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R15     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R19     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R22     | S      |       50 |           1.000 |                0.860 |               0.880 |       8.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R24     | M      |       50 |           0.960 |                0.440 |               0.580 |       7.780 |               0.960 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R25     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K12     | S      |       50 |           1.000 |                0.840 |               0.880 |       3.440 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | C2      | N      |       50 |           1.000 |                0.440 |               0.580 |       7.380 |               1.000 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | NONE    | -      |     2508 |           0.931 |                0.069 |               0.069 |       4.643 |               0.931 |   nan     |        0.003 |                  0.003 |                    0.001 |                  0.016 |             0.000 |
| capped_crc_0.005         | Q01     | N      |       50 |           0.940 |                0.880 |               0.880 |       1.420 |               0.940 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q03     | M      |       50 |           0.060 |                0.020 |               0.020 |       0.420 |               0.060 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q04     | S      |       50 |           0.700 |                0.640 |               0.660 |       1.020 |               0.700 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q05     | M      |       50 |           0.580 |                0.560 |               0.560 |       0.740 |               0.580 |     0.500 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q07     | M      |       50 |           0.800 |                0.740 |               0.740 |       1.280 |               0.800 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q09     | P      |       50 |           1.000 |                1.000 |               1.000 |       1.000 |               1.000 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K03     | N      |       50 |           1.000 |                0.960 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K04     | M      |       50 |           0.700 |                0.620 |               0.620 |       2.740 |               0.700 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.180 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K08     | M      |       50 |           0.980 |                0.940 |               0.960 |       3.100 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R01     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R03     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.100 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R05     | N      |       50 |           0.980 |                0.980 |               0.980 |       7.840 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R06     | P      |       50 |           0.880 |                0.780 |               0.780 |       7.220 |               0.880 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R07     | P      |       50 |           1.000 |                0.720 |               0.700 |       8.520 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R10     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R11     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R13     | M      |       50 |           0.960 |                0.880 |               0.880 |       7.680 |               0.960 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R15     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R19     | S      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R22     | S      |       50 |           0.900 |                0.820 |               0.820 |       7.320 |               0.900 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R24     | M      |       50 |           0.760 |                0.420 |               0.480 |       6.560 |               0.760 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R25     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K12     | S      |       50 |           0.940 |                0.840 |               0.880 |       2.980 |               0.940 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | C2      | N      |       50 |           0.960 |                0.440 |               0.560 |       7.180 |               0.960 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | NONE    | -      |     2508 |           0.142 |                0.858 |               0.858 |       0.919 |               0.142 |   nan     |        0.001 |                  0.000 |                    0.001 |                  0.003 |             0.000 |
| two_stage_0.005          | Q01     | N      |       50 |           0.960 |                0.880 |               0.880 |       2.260 |               0.940 |     0.420 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q02     | M      |       50 |           1.000 |                1.000 |               1.000 |       1.840 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q03     | M      |       50 |           0.540 |                0.020 |               0.020 |       1.920 |               0.060 |     0.080 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q04     | S      |       50 |           0.860 |                0.640 |               0.660 |       2.460 |               0.700 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q05     | M      |       50 |           0.660 |                0.560 |               0.560 |       1.400 |               0.580 |     0.500 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q07     | M      |       50 |           0.820 |                0.740 |               0.740 |       1.520 |               0.800 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q09     | P      |       50 |           1.000 |                1.000 |               1.000 |       2.680 |               1.000 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K03     | N      |       50 |           1.000 |                0.960 |               1.000 |       4.860 |               1.000 |     0.360 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K04     | M      |       50 |           0.780 |                0.620 |               0.700 |       4.060 |               0.700 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       6.180 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       5.360 |               1.000 |     0.620 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       5.400 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K08     | M      |       50 |           1.000 |                0.940 |               0.980 |       5.980 |               0.980 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R01     | S      |       50 |           1.000 |                0.920 |               0.920 |       9.280 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R03     | N      |       50 |           1.000 |                0.940 |               0.940 |       9.240 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R05     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.380 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R06     | P      |       50 |           0.900 |                0.780 |               0.780 |       7.760 |               0.880 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R07     | P      |       50 |           1.000 |                0.720 |               0.700 |      10.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R10     | N      |       50 |           1.000 |                1.000 |               1.000 |       9.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R11     | S      |       50 |           1.000 |                0.960 |               0.960 |       9.440 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R13     | M      |       50 |           0.980 |                0.880 |               0.880 |       9.120 |               0.960 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R15     | S      |       50 |           1.000 |                0.980 |               0.980 |       9.520 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R19     | S      |       50 |           1.000 |                0.960 |               0.960 |       9.360 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R22     | S      |       50 |           0.980 |                0.820 |               0.820 |       8.640 |               0.900 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.140 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R24     | M      |       50 |           0.860 |                0.420 |               0.480 |       8.360 |               0.760 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R25     | S      |       50 |           1.000 |                0.980 |               0.980 |       9.460 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.600 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       5.340 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K12     | S      |       50 |           1.000 |                0.900 |               0.940 |       6.040 |               0.940 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | C2      | N      |       50 |           0.960 |                0.440 |               0.560 |       8.620 |               0.960 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | NONE    | -      |     2508 |           0.465 |                0.535 |               0.535 |       2.086 |               0.142 |   nan     |        0.002 |                  0.013 |                    0.002 |                  0.003 |             0.000 |
| diagnosis_free_universal | Q01     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q02     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.140 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q03     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.080 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q04     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q05     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q07     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.060 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q09     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.140 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K03     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.340 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K04     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K05     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K06     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.320 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K07     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K08     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.540 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K09     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R01     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R03     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R05     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R06     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R07     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R10     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R11     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R13     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R15     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R19     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R22     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R23     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R24     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R25     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R26     | S      |       10 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K11     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K12     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | C2      | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | NONE    | -      |     2508 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |   nan     |        0.015 |                  0.008 |                    0.011 |                  0.051 |             0.000 |
