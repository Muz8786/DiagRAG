# DiagRAG v6 judged run report

Device: cuda. Reranker: BAAI/bge-reranker-large. Last session runtime: 10545s.

## Verdict (gates fixed in JUDGED_PROTOCOL.json before results)

```
{
 "detectors_pass": 27,
 "repairs_pass": 26,
 "solved_both": 26,
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
   "rescued": 42,
   "rate": 0.42,
   "ci_lo": 0.327982249185113
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
   "rescued": 73,
   "rate": 0.73,
   "ci_lo": 0.6356769977376873
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
   "rescued": 92,
   "rate": 0.92,
   "ci_lo": 0.8500173312059693
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
  "repairs_pass": 19,
  "solved_both": 19,
  "of": 22,
  "not_solved": [
   "Q03",
   "R19",
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
   "repairs_pass": 26,
   "solved_both": 26,
   "of": 28,
   "verdict": "ADOPTED",
   "not_solved": [
    "Q03",
    "R19"
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
   "repairs_pass": 19,
   "solved_both": 19,
   "of": 22,
   "not_solved": [
    "Q03",
    "R19",
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
    "clean_dispatch_rate": 0.034688995215311005,
    "clean_clf_dispatch_rate": 0.034688995215311005,
    "clean_mean_cost": 0.1678628389154705,
    "mean_closure": 0.835625,
    "T1_loss": true,
    "T2_dispatch": true,
    "T3_cost": true,
    "T4_closure": true,
    "all_targets_met": true
   },
   {
    "policy": "global_crc_0.005",
    "clean_loss": 0.006379585326953748,
    "clean_dispatch_rate": 0.9992025518341308,
    "clean_clf_dispatch_rate": 0.9992025518341308,
    "clean_mean_cost": 4.641547049441786,
    "mean_closure": 0.8768750000000001,
    "T1_loss": false,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.0025",
    "clean_loss": 0.0011961722488038277,
    "clean_dispatch_rate": 0.6666666666666666,
    "clean_clf_dispatch_rate": 0.6666666666666666,
    "clean_mean_cost": 3.1503189792663475,
    "mean_closure": 0.58875,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": false,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.005",
    "clean_loss": 0.001594896331738437,
    "clean_dispatch_rate": 0.8628389154704944,
    "clean_clf_dispatch_rate": 0.8628389154704944,
    "clean_mean_cost": 3.9074960127591707,
    "mean_closure": 0.855625,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.01",
    "clean_loss": 0.001594896331738437,
    "clean_dispatch_rate": 0.8640350877192983,
    "clean_clf_dispatch_rate": 0.8640350877192983,
    "clean_mean_cost": 3.9118819776714515,
    "mean_closure": 0.858125,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.02",
    "clean_loss": 0.0027910685805422647,
    "clean_dispatch_rate": 0.9350079744816587,
    "clean_clf_dispatch_rate": 0.9350079744816587,
    "clean_mean_cost": 4.322567783094099,
    "mean_closure": 0.87625,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "capped_crc_0.005",
    "clean_loss": 0.0007974481658692185,
    "clean_dispatch_rate": 0.1547049441786284,
    "clean_clf_dispatch_rate": 0.1547049441786284,
    "clean_mean_cost": 0.9130781499202552,
    "mean_closure": 0.8487499999999999,
    "T1_loss": true,
    "T2_dispatch": true,
    "T3_cost": true,
    "T4_closure": true,
    "all_targets_met": true
   },
   {
    "policy": "two_stage_0.005",
    "clean_loss": 0.001594896331738437,
    "clean_dispatch_rate": 0.47208931419457734,
    "clean_clf_dispatch_rate": 0.1547049441786284,
    "clean_mean_cost": 2.0793460925039873,
    "mean_closure": 0.8268749999999999,
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
    "mean_closure": 0.74625,
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
  "mean_closure": 0.39759999999999995,
  "mean_closure_without_fallback": 0.2176,
  "mean_closure_grounded": 0.35250000000000004,
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
  "fixed": 41,
  "broken": 7,
  "verdict": "PASS",
  "dispatched": 0.6796116504854369,
  "mean_cost": 4.644417475728155
 },
 "detection_baselines": {
  "ours_1_minus_pNONE": [
   0.9761629452418926,
   0.9715951044636001,
   0.9808874896393761
  ],
  "qpp_neg_nqc": [
   0.5837508434547909,
   0.5656091663185563,
   0.5990405337874515
  ],
  "qpp_neg_wig": [
   0.5650363707929497,
   0.5447874661327631,
   0.5830072557766013
  ],
  "neg_ce1": [
   0.6220657996973786,
   0.6019210592513491,
   0.6394588494958331
  ],
  "raglog_tier0_best_single_rag_rr_order": [
   0.5648660184844395,
   0.5475912291302022,
   0.5823382195083773
  ],
  "raglog_tier0_features_hgb": [
   0.732117608268924,
   0.7152737252706524,
   0.7476654303976058
  ],
  "raglog_tier0_detect_rate_at_5pct_fa": 0.3801282051282051,
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
  "ours_detect_rate_at_5pct_fa": 0.9301282051282052
 },
 "repair_baselines": {
  "Q04:symspell": {
   "fault": "Q04",
   "repair": "symspell (external)",
   "n": 100,
   "rescued": 59,
   "ci_lo": 0.4920125056109662
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
 "clean_net_hit_change": -0.00039872408293460925,
 "guarantee": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 4.309841119198854e-05,
   "esci_rare": 0.7877565247206897,
   "shop": 6.890307442020127e-05
  },
  "calibration": {
   "esci_common": {
    "n": 1503,
    "losses_if_all_dispatched": 0
   },
   "esci_rare": {
    "n": 269,
    "losses_if_all_dispatched": 7
   },
   "shop": {
    "n": 202,
    "losses_if_all_dispatched": 0
   }
  },
  "heldout_clean_loss": 0.001594896331738437,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0017942583732057417,
   "esci_rare": 0.0027100271002710027,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.855625,
  "L2": "PASS"
 },
 "policies": [
  {
   "policy": "tau_none_5pct_fpr",
   "mean_closure": 0.835625,
   "mean_closure_grounded": 0.8436363636363636,
   "mean_family_attribution": 0.84625,
   "mean_group_attribution": 0.8543749999999999,
   "mean_cost_faulted": 4.920625,
   "clean_dispatch_rate": 0.034688995215311005,
   "clean_clf_dispatch_rate": 0.034688995215311005,
   "clean_mean_cost": 0.1678628389154705,
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
   "mean_closure": 0.8768750000000001,
   "mean_closure_grounded": 0.889090909090909,
   "mean_family_attribution": 0.879375,
   "mean_group_attribution": 0.8925,
   "mean_cost_faulted": 5.459375,
   "clean_dispatch_rate": 0.9992025518341308,
   "clean_clf_dispatch_rate": 0.9992025518341308,
   "clean_mean_cost": 4.641547049441786,
   "clean_loss": 0.006379585326953748,
   "clean_net_hit_change": -0.0007974481658692185,
   "clean_loss_esci_common": 0.0017942583732057417,
   "clean_loss_esci_rare": 0.03523035230352303,
   "clean_loss_shop": 0.0,
   "T1_loss": false,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "mondrian_crc_0.0025",
   "mean_closure": 0.58875,
   "mean_closure_grounded": 0.5727272727272728,
   "mean_family_attribution": 0.5843750000000001,
   "mean_group_attribution": 0.59375,
   "mean_cost_faulted": 3.9431249999999998,
   "clean_dispatch_rate": 0.6666666666666666,
   "clean_clf_dispatch_rate": 0.6666666666666666,
   "clean_mean_cost": 3.1503189792663475,
   "clean_loss": 0.0011961722488038277,
   "clean_net_hit_change": 0.0,
   "clean_loss_esci_common": 0.0017942583732057417,
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
   "mean_closure": 0.855625,
   "mean_closure_grounded": 0.8609090909090908,
   "mean_family_attribution": 0.86625,
   "mean_group_attribution": 0.8775,
   "mean_cost_faulted": 5.26125,
   "clean_dispatch_rate": 0.8628389154704944,
   "clean_clf_dispatch_rate": 0.8628389154704944,
   "clean_mean_cost": 3.9074960127591707,
   "clean_loss": 0.001594896331738437,
   "clean_net_hit_change": -0.00039872408293460925,
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
   "policy": "mondrian_crc_0.01",
   "mean_closure": 0.858125,
   "mean_closure_grounded": 0.8636363636363636,
   "mean_family_attribution": 0.8674999999999999,
   "mean_group_attribution": 0.879375,
   "mean_cost_faulted": 5.268125,
   "clean_dispatch_rate": 0.8640350877192983,
   "clean_clf_dispatch_rate": 0.8640350877192983,
   "clean_mean_cost": 3.9118819776714515,
   "clean_loss": 0.001594896331738437,
   "clean_net_hit_change": -0.00039872408293460925,
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
   "policy": "mondrian_crc_0.02",
   "mean_closure": 0.87625,
   "mean_closure_grounded": 0.889090909090909,
   "mean_family_attribution": 0.8787499999999999,
   "mean_group_attribution": 0.891875,
   "mean_cost_faulted": 5.453125,
   "clean_dispatch_rate": 0.9350079744816587,
   "clean_clf_dispatch_rate": 0.9350079744816587,
   "clean_mean_cost": 4.322567783094099,
   "clean_loss": 0.0027910685805422647,
   "clean_net_hit_change": 0.001594896331738437,
   "clean_loss_esci_common": 0.0017942583732057417,
   "clean_loss_esci_rare": 0.01084010840108401,
   "clean_loss_shop": 0.0,
   "T1_loss": true,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "capped_crc_0.005",
   "mean_closure": 0.8487499999999999,
   "mean_closure_grounded": 0.8545454545454544,
   "mean_family_attribution": 0.849375,
   "mean_group_attribution": 0.858125,
   "mean_cost_faulted": 5.115625,
   "clean_dispatch_rate": 0.1547049441786284,
   "clean_clf_dispatch_rate": 0.1547049441786284,
   "clean_mean_cost": 0.9130781499202552,
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
   "policy": "two_stage_0.005",
   "mean_closure": 0.8268749999999999,
   "mean_closure_grounded": 0.859090909090909,
   "mean_family_attribution": 0.8512500000000001,
   "mean_group_attribution": 0.86125,
   "mean_cost_faulted": 6.505000000000001,
   "clean_dispatch_rate": 0.47208931419457734,
   "clean_clf_dispatch_rate": 0.1547049441786284,
   "clean_mean_cost": 2.0793460925039873,
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
   "mean_closure": 0.74625,
   "mean_closure_grounded": 0.7945454545454548,
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
   "fixed": 41,
   "broken": 7,
   "verdict": "PASS",
   "dispatched": 0.6796116504854369,
   "mean_cost": 4.644417475728155
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
   "fixed": 4,
   "broken": 2,
   "verdict": "INCONCLUSIVE",
   "dispatched": 0.4411407766990291
  },
  {
   "arm": "B1",
   "what": "baseline: K12 parent collapse always on (no detection)",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6055825242718447,
   "delta": 0.015776699029126214,
   "ci_lo": 0.007888349514563107,
   "ci_hi": 0.02368021844660186,
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
   "ci_hi": 0.030354975728155258,
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
   "ci_lo": -0.10810810810810811,
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
   "ci_lo": -0.1276595744680851,
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
   "ci_hi": 0.06260296540362438,
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
   "ci_lo": -0.016216216216216217,
   "ci_hi": 0.03783783783783784,
   "fixed": 4,
   "broken": 2,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "N1v4",
   "what": "counterfactual: DEPLOYED LOOP with the v4 config on all natural queries",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6110436893203883,
   "delta": 0.021237864077669904,
   "ci_lo": 0.012742718446601941,
   "ci_hi": 0.03033980582524272,
   "fixed": 45,
   "broken": 10,
   "verdict": "PASS"
  }
 ],
 "unseen_mean_closure": 0.39759999999999995,
 "not_solved": [
  "Q03",
  "R19"
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
| R19     | S      | True       | PASS       | FAIL     | False    |
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
| Q01     |   3081 |       1007 |              641 |    266 |    100 |           50 |          50 |            0 |        0.273 |
| Q02     |   3081 |        504 |                0 |    404 |    100 |           50 |          50 |            0 |        0.198 |
| Q03     |   3081 |        263 |               67 |     96 |    100 |           50 |          50 |            0 |        0.51  |
| Q04     |   3081 |        212 |                5 |    107 |    100 |           50 |          50 |           40 |        0.483 |
| Q05     |   3081 |        735 |               70 |    565 |    100 |           50 |          50 |            0 |        0.15  |
| Q07     |   2463 |       2961 |             2266 |    595 |    100 |           50 |          50 |            0 |        0.144 |
| Q09     |   3081 |        345 |                0 |    245 |    100 |           50 |          50 |            0 |        0.29  |
| K03     |   2020 |        923 |              697 |    126 |    100 |           50 |          50 |            0 |        0.442 |
| K04     |   3081 |        170 |                0 |     70 |    100 |           50 |          50 |            0 |        0.588 |
| K05     |   3081 |        250 |                0 |    150 |    100 |           50 |          50 |            0 |        0.4   |
| K06     |   1945 |        121 |                0 |     21 |    100 |           50 |          50 |            0 |        0.826 |
| K07     |    248 |        126 |                0 |     26 |    100 |           50 |          50 |            0 |        0.794 |
| K08     |   3081 |        126 |                0 |     26 |    100 |           50 |          50 |            0 |        0.794 |
| K09     |    284 |        176 |                0 |     76 |    100 |           50 |          50 |            0 |        0.568 |
| R01     |   3081 |        200 |                0 |    100 |    100 |           50 |          50 |            0 |        0.5   |
| R03     |   3081 |       1096 |                0 |    996 |    100 |           50 |          50 |            0 |        0.091 |
| R05     |   3081 |        152 |                0 |     52 |    100 |           50 |          50 |            0 |        0.658 |
| R06     |   3081 |        100 |                0 |      0 |    100 |           50 |          50 |            0 |        1     |
| R07     |   3081 |        390 |                0 |    290 |    100 |           50 |          50 |            0 |        0.256 |
| R10     |   3081 |       1103 |                0 |   1003 |    100 |           50 |          50 |            0 |        0.091 |
| R11     |   3081 |       1247 |                0 |   1147 |    100 |           50 |          50 |            0 |        0.08  |
| R13     |   3081 |       1531 |                0 |   1431 |    100 |           50 |          50 |            0 |        0.065 |
| R15     |   3081 |       1128 |                0 |   1028 |    100 |           50 |          50 |            0 |        0.089 |
| R19     |   3081 |        744 |                0 |    644 |    100 |           50 |          50 |            0 |        0.134 |
| R22     |   3081 |       1080 |                0 |    980 |    100 |           50 |          50 |            0 |        0.093 |
| R23     |   3081 |        291 |                0 |    191 |    100 |           50 |          50 |            0 |        0.344 |
| R24     |   3081 |        324 |                0 |    224 |    100 |           50 |          50 |            0 |        0.309 |
| R25     |   3081 |        309 |                0 |    209 |    100 |           50 |          50 |            0 |        0.324 |
| R26     |   3081 |       4000 |              985 |   2993 |     22 |           12 |          10 |            0 |        0.007 |
| K11     |   1945 |        105 |                0 |      5 |    100 |           50 |          50 |            0 |        0.952 |
| K12     |   3081 |        167 |                0 |     67 |    100 |           50 |          50 |            0 |        0.599 |
| C2      |   3081 |        267 |               96 |     71 |    100 |           50 |          50 |            0 |        0.585 |

## Detector gates (AUROC bar 0.7, min test positives 50)

| fault   | detector                             |   n_pos_train |   n_pos_test |   n_neg_test |   auroc |   ci_lo |   ci_hi |   auroc_vs_clean | status   |
|:--------|:-------------------------------------|--------------:|-------------:|-------------:|--------:|--------:|--------:|-----------------:|:---------|
| Q01     | histgb_head                          |            50 |           50 |         3968 |  0.9980 |  0.9968 |  0.9990 |           0.9978 | PASS     |
| Q02     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| Q03     | histgb_head                          |            50 |           50 |         3968 |  0.6221 |  0.5461 |  0.6916 |           0.6292 | FAIL     |
| Q04     | tier0_rule                           |            50 |           50 |         3968 |  0.9839 |  0.9774 |  0.9903 |           0.9869 | PASS     |
| Q05     | histgb_head                          |            50 |           50 |         3968 |  0.9761 |  0.9444 |  0.9957 |           0.9776 | PASS     |
| Q07     | histgb_head                          |            50 |           50 |         3968 |  0.9994 |  0.9988 |  0.9998 |           0.9994 | PASS     |
| Q09     | histgb_head                          |            50 |           50 |         3968 |  0.9993 |  0.9984 |  0.9998 |           0.9994 | PASS     |
| K03     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  0.9999 |  1.0000 |           1.0000 | PASS     |
| K04     | histgb_head                          |            50 |           50 |         3968 |  0.8984 |  0.8200 |  0.9641 |           0.9007 | PASS     |
| K05     | histgb_head                          |            50 |           50 |         3968 |  0.9992 |  0.9979 |  0.9999 |           0.9999 | PASS     |
| K06     | histgb_head                          |            50 |           50 |         3968 |  0.9869 |  0.9547 |  1.0000 |           0.9874 | PASS     |
| K07     | tier0_rule                           |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K08     | histgb_head                          |            50 |           50 |         3968 |  0.9975 |  0.9944 |  0.9999 |           0.9988 | PASS     |
| K09     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R01     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R03     | histgb_head                          |            50 |           50 |         3968 |  0.9850 |  0.9670 |  0.9983 |           0.9901 | PASS     |
| R05     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R06     | histgb_head                          |            50 |           50 |         3968 |  0.9923 |  0.9845 |  0.9983 |           0.9952 | PASS     |
| R07     | histgb_head                          |            50 |           50 |         3968 |  0.9999 |  0.9998 |  1.0000 |           1.0000 | PASS     |
| R10     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  0.9999 |  1.0000 |           1.0000 | PASS     |
| R11     | histgb_head                          |            50 |           50 |         3968 |  0.9999 |  0.9997 |  1.0000 |           1.0000 | PASS     |
| R13     | histgb_head                          |            50 |           50 |         3968 |  0.9868 |  0.9595 |  1.0000 |           0.9887 | PASS     |
| R15     | tier0_rule                           |            50 |           50 |         3968 |  0.9986 |  0.9975 |  0.9995 |           1.0000 | PASS     |
| R19     | histgb_head                          |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R22     | histgb_head                          |            50 |           50 |         3968 |  0.9467 |  0.8984 |  0.9873 |           0.9481 | PASS     |
| R23     | tier0_rule                           |            50 |           50 |         3968 |  0.9995 |  0.9987 |  1.0000 |           1.0000 | PASS     |
| R24     | histgb_head                          |            50 |           50 |         3968 |  0.9497 |  0.9002 |  0.9840 |           0.9559 | PASS     |
| R25     | tier0_rule                           |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R26     | tier0_rule                           |            12 |           10 |         4008 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | THIN     |
| K11     | tier0_rule                           |            50 |           50 |         3968 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K12     | histgb_head                          |            50 |           50 |         3968 |  0.9940 |  0.9845 |  0.9999 |           0.9972 | PASS     |
| C2      | tier0_rule(second factor-group mass) |            50 |           50 |         4018 |  0.7931 |  0.7074 |  0.8801 |         nan      | PASS     |

## Repair gates (Wilson lower bound >= 0.5)

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost |   harm_rate | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|------------:|:---------|
| Q01     |      100 |        70 |         0.700 |   0.604 |   0.781 |        20 |            0 |       0.000 | PASS     |
| Q02     |      100 |        92 |         0.920 |   0.850 |   0.959 |        20 |            1 |       0.050 | PASS     |
| Q03     |      100 |         3 |         0.030 |   0.010 |   0.085 |        20 |            2 |       0.100 | FAIL     |
| Q04     |      100 |        76 |         0.760 |   0.668 |   0.833 |        20 |            0 |       0.000 | PASS     |
| Q05     |      100 |        84 |         0.840 |   0.756 |   0.899 |        20 |            0 |       0.000 | PASS     |
| Q07     |      100 |        76 |         0.760 |   0.668 |   0.833 |        20 |            0 |       0.000 | PASS     |
| Q09     |      100 |        82 |         0.820 |   0.733 |   0.883 |        20 |            0 |       0.000 | PASS     |
| K03     |      100 |        84 |         0.840 |   0.756 |   0.899 |        20 |            0 |       0.000 | PASS     |
| K04     |      100 |        92 |         0.920 |   0.850 |   0.959 |        20 |            0 |       0.000 | PASS     |
| K05     |      100 |        98 |         0.980 |   0.930 |   0.994 |        20 |            0 |       0.000 | PASS     |
| K06     |      100 |        99 |         0.990 |   0.946 |   0.998 |        20 |            0 |       0.000 | PASS     |
| K07     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K08     |      100 |        91 |         0.910 |   0.838 |   0.952 |        20 |            1 |       0.050 | PASS     |
| K09     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R01     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R03     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R05     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R06     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R07     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R10     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R11     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R13     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R15     |      100 |        96 |         0.960 |   0.902 |   0.984 |        20 |            0 |       0.000 | PASS     |
| R19     |      100 |        91 |         0.910 |   0.838 |   0.952 |        20 |            3 |       0.150 | FAIL     |
| R22     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R23     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R24     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R25     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R26     |       22 |        22 |         1.000 |   0.851 |   1.000 |        20 |            0 |       0.000 | THIN     |
| K11     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K12     |      100 |        90 |         0.900 |   0.826 |   0.945 |        20 |            1 |       0.050 | PASS     |
| C2      |      100 |        79 |         0.790 |   0.700 |   0.858 |         0 |            0 |       0.000 | PASS     |

## Dispatch policies (held-out)

| policy                   |   mean_closure |   mean_closure_grounded |   mean_family_attribution |   mean_group_attribution |   mean_cost_faulted |   clean_dispatch_rate |   clean_clf_dispatch_rate |   clean_mean_cost |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop | T1_loss   | T2_dispatch   | T3_cost   | T4_closure   | all_targets_met   |
|:-------------------------|---------------:|------------------------:|--------------------------:|-------------------------:|--------------------:|----------------------:|--------------------------:|------------------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|:----------|:--------------|:----------|:-------------|:------------------|
| tau_none_5pct_fpr        |         0.8356 |                  0.8436 |                    0.8462 |                   0.8544 |              4.9206 |                0.0347 |                    0.0347 |            0.1679 |       0.0008 |                 0.0000 |                   0.0006 |                 0.0027 |            0.0000 | True      | True          | True      | True         | True              |
| global_crc_0.005         |         0.8769 |                  0.8891 |                    0.8794 |                   0.8925 |              5.4594 |                0.9992 |                    0.9992 |            4.6415 |       0.0064 |                -0.0008 |                   0.0018 |                 0.0352 |            0.0000 | False     | False         | False     | True         | False             |
| mondrian_crc_0.0025      |         0.5887 |                  0.5727 |                    0.5844 |                   0.5938 |              3.9431 |                0.6667 |                    0.6667 |            3.1503 |       0.0012 |                 0.0000 |                   0.0018 |                 0.0000 |            0.0000 | True      | False         | False     | False        | False             |
| mondrian_crc_0.005       |         0.8556 |                  0.8609 |                    0.8662 |                   0.8775 |              5.2613 |                0.8628 |                    0.8628 |            3.9075 |       0.0016 |                -0.0004 |                   0.0018 |                 0.0027 |            0.0000 | True      | False         | False     | True         | False             |
| mondrian_crc_0.01        |         0.8581 |                  0.8636 |                    0.8675 |                   0.8794 |              5.2681 |                0.8640 |                    0.8640 |            3.9119 |       0.0016 |                -0.0004 |                   0.0018 |                 0.0027 |            0.0000 | True      | False         | False     | True         | False             |
| mondrian_crc_0.02        |         0.8762 |                  0.8891 |                    0.8787 |                   0.8919 |              5.4531 |                0.9350 |                    0.9350 |            4.3226 |       0.0028 |                 0.0016 |                   0.0018 |                 0.0108 |            0.0000 | True      | False         | False     | True         | False             |
| capped_crc_0.005         |         0.8487 |                  0.8545 |                    0.8494 |                   0.8581 |              5.1156 |                0.1547 |                    0.1547 |            0.9131 |       0.0008 |                -0.0004 |                   0.0006 |                 0.0027 |            0.0000 | True      | True          | True      | True         | True              |
| two_stage_0.005          |         0.8269 |                  0.8591 |                    0.8513 |                   0.8612 |              6.5050 |                0.4721 |                    0.1547 |            2.0793 |       0.0016 |                 0.0132 |                   0.0018 |                 0.0027 |            0.0000 | True      | False         | False     | True         | False             |
| diagnosis_free_universal |         0.7462 |                  0.7945 |                    0.0000 |                   0.0000 |             12.0000 |                1.0000 |                    1.0000 |           12.0000 |       0.0148 |                 0.0076 |                   0.0108 |                 0.0515 |            0.0000 | False     | False         | False     | False        | False             |

## Loop gates (L1 do-no-harm on held-out clean, L2 mean closure, U1 unseen, N1 natural traffic)

```
{
 "GUARANTEE": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 4.309841119198854e-05,
   "esci_rare": 0.7877565247206897,
   "shop": 6.890307442020127e-05
  },
  "calibration": {
   "esci_common": {
    "n": 1503,
    "losses_if_all_dispatched": 0
   },
   "esci_rare": {
    "n": 269,
    "losses_if_all_dispatched": 7
   },
   "shop": {
    "n": 202,
    "losses_if_all_dispatched": 0
   }
  },
  "heldout_clean_loss": 0.001594896331738437,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0017942583732057417,
   "esci_rare": 0.0027100271002710027,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.855625,
  "L2": "PASS"
 },
 "U1": {
  "mean_closure": 0.39759999999999995,
  "mean_closure_without_fallback": 0.2176,
  "mean_closure_grounded": 0.35250000000000004,
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
  "fixed": 41,
  "broken": 7,
  "verdict": "PASS",
  "dispatched": 0.6796116504854369,
  "mean_cost": 4.644417475728155
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
| ours_1_minus_pNONE                    |  0.9762 |  0.9716 |  0.9809 |
| qpp_neg_nqc                           |  0.5838 |  0.5656 |  0.5990 |
| qpp_neg_wig                           |  0.5650 |  0.5448 |  0.5830 |
| neg_ce1                               |  0.6221 |  0.6019 |  0.6395 |
| raglog_tier0_best_single_rag_rr_order |  0.5649 |  0.5476 |  0.5823 |
| raglog_tier0_features_hgb             |  0.7321 |  0.7153 |  0.7477 |

## External repair baselines (oracle-dispatched, injected held-out + train episodes)

| fault   | repair                 |   n |   rescued |   ci_lo |
|:--------|:-----------------------|----:|----------:|--------:|
| Q04     | symspell (external)    | 100 |        59 |   0.492 |
| Q05     | wordsegment (external) | 100 |        93 |   0.863 |

## Family repairs, oracle-dispatched

| fault   | family   |   n |   rescued |   rate |   ci_lo |
|:--------|:---------|----:|----------:|-------:|--------:|
| Q01     | QLEX     | 100 |        42 |  0.420 |   0.328 |
| Q03     | QLEX     | 100 |         0 |  0.000 |   0.000 |
| Q04     | QLEX     | 100 |        73 |  0.730 |   0.636 |
| Q05     | QLEX     | 100 |        76 |  0.760 |   0.668 |
| K04     | STALE    | 100 |        92 |  0.920 |   0.850 |
| R03     | ENC      | 100 |       100 |  1.000 |   0.963 |
| R07     | STALE    | 100 |       100 |  1.000 |   0.963 |
| R10     | ENC      | 100 |       100 |  1.000 |   0.963 |
| R11     | ENC      | 100 |       100 |  1.000 |   0.963 |

## Natural traffic (no injection, never-examined queries): deployed loop, components, baselines

| arm   | what                                                                                           |    n |   hit_before |   hit_after |   delta |   ci_lo |   ci_hi |   fixed |   broken | verdict      |   dispatched |   mean_cost |
|:------|:-----------------------------------------------------------------------------------------------|-----:|-------------:|------------:|--------:|--------:|--------:|--------:|---------:|:-------------|-------------:|------------:|
| N1    | DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds                | 1648 |       0.5898 |      0.6104 |  0.0206 |  0.0127 |  0.0291 |      41 |        7 | PASS         |       0.6796 |      4.6444 |
| N1a   | component: natural rules only                                                                  | 1648 |       0.5898 |      0.6117 |  0.0218 |  0.0146 |  0.0303 |      41 |        5 | PASS         |     nan      |    nan      |
| N1b   | component: classifier dispatch only                                                            | 1648 |       0.5898 |      0.5910 |  0.0012 | -0.0018 |  0.0042 |       4 |        2 | INCONCLUSIVE |       0.4411 |    nan      |
| B1    | baseline: K12 parent collapse always on (no detection)                                         | 1648 |       0.5898 |      0.6056 |  0.0158 |  0.0079 |  0.0237 |      37 |       11 | PASS         |     nan      |    nan      |
| B2    | baseline: diagnosis-free universal repair on every query (cost 12)                             | 1648 |       0.5898 |      0.6086 |  0.0188 |  0.0073 |  0.0304 |      62 |       31 | PASS         |     nan      |    nan      |
| NA1   | natural misspelling: ours (QLEX, log-gated)                                                    |  185 |       0.5730 |      0.5189 | -0.0541 | -0.1081 | -0.0054 |       7 |       17 | HARM         |     nan      |    nan      |
| NA1x  | natural misspelling: SymSpell lookup_compound (external)                                       |  185 |       0.5730 |      0.4486 | -0.1243 | -0.1838 | -0.0649 |       5 |       28 | HARM         |     nan      |    nan      |
| NA2   | natural missing space: ours (QLEX)                                                             |   47 |       0.5106 |      0.4681 | -0.0426 | -0.1489 |  0.0638 |       2 |        4 | INCONCLUSIVE |     nan      |    nan      |
| NA2x  | natural missing space: wordsegment (external)                                                  |   47 |       0.5106 |      0.4894 | -0.0213 | -0.1277 |  0.0638 |       2 |        3 | INCONCLUSIVE |     nan      |    nan      |
| NA4   | natural duplicate in top-5: K05 collapse                                                       |  141 |       0.5177 |      0.5816 |  0.0638 |  0.0213 |  0.1135 |      11 |        2 | PASS         |     nan      |    nan      |
| NA5   | natural chunk crowding: K12 parent collapse                                                    |  607 |       0.6491 |      0.6919 |  0.0428 |  0.0247 |  0.0626 |      30 |        4 | PASS         |     nan      |    nan      |
| NA1c  | DEPLOYED LOOP, v5 config (natural typo repair OFF), on natural queries with q_correctable >= 1 |  185 |       0.5730 |      0.5838 |  0.0108 |  0.0000 |  0.0270 |       2 |        0 | INCONCLUSIVE |     nan      |    nan      |
| NA1d  | counterfactual: same loop with the v4 config (natural typo repair ON), same queries            |  185 |       0.5730 |      0.5838 |  0.0108 | -0.0162 |  0.0378 |       4 |        2 | INCONCLUSIVE |     nan      |    nan      |
| N1v4  | counterfactual: DEPLOYED LOOP with the v4 config on all natural queries                        | 1648 |       0.5898 |      0.6110 |  0.0212 |  0.0127 |  0.0303 |      45 |       10 | PASS         |     nan      |    nan      |

## Unseen faults (leave-one-fault-out attributor)

| fault   | tier   | family   |   n_test |   flagged |   right_group |   closure |   closure_without_group_fallback |
|:--------|:-------|:---------|---------:|----------:|--------------:|----------:|---------------------------------:|
| Q01     | N      | QLEX     |       50 |     0.540 |         0.400 |     0.120 |                            0.120 |
| Q02     | M      | Q02      |       50 |     0.620 |         0.100 |     0.020 |                            0.020 |
| Q03     | M      | QLEX     |       50 |     0.180 |         0.080 |     0.040 |                            0.000 |
| Q04     | S      | QLEX     |       50 |     0.580 |         0.380 |     0.340 |                            0.340 |
| Q05     | M      | QLEX     |       50 |     0.420 |         0.220 |     0.280 |                            0.280 |
| Q07     | M      | Q07      |       50 |     0.180 |         0.140 |     0.000 |                            0.000 |
| Q09     | P      | Q09      |       50 |     0.320 |         0.160 |     0.000 |                            0.000 |
| K03     | N      | K03      |       50 |     1.000 |         1.000 |     0.400 |                            0.080 |
| K04     | M      | STALE    |       50 |     0.680 |         0.040 |     0.520 |                            0.320 |
| K05     | S      | K05      |       50 |     1.000 |         1.000 |     0.920 |                            0.040 |
| K06     | N      | K06      |       50 |     1.000 |         0.980 |     0.100 |                            0.000 |
| K08     | M      | K08      |       50 |     0.900 |         0.840 |     0.320 |                            0.080 |
| K09     | M      | K09      |       50 |     0.600 |         0.520 |     0.520 |                            0.000 |
| R01     | S      | R01      |       50 |     0.200 |         0.040 |     0.080 |                            0.000 |
| R03     | N      | ENC      |       50 |     1.000 |         0.940 |     0.940 |                            0.920 |
| R05     | N      | R05      |       50 |     0.540 |         0.500 |     0.160 |                            0.000 |
| R06     | P      | R06      |       50 |     0.760 |         0.540 |     0.580 |                            0.000 |
| R07     | P      | STALE    |       50 |     1.000 |         0.000 |     1.000 |                            1.000 |
| R10     | N      | ENC      |       50 |     1.000 |         1.000 |     1.000 |                            1.000 |
| R11     | S      | ENC      |       50 |     1.000 |         1.000 |     1.000 |                            1.000 |
| R13     | M      | R13      |       50 |     0.240 |         0.160 |     0.140 |                            0.040 |
| R19     | S      | R19      |       50 |     0.740 |         0.600 |     0.440 |                            0.060 |
| R22     | S      | R22      |       50 |     0.380 |         0.140 |     0.160 |                            0.040 |
| R24     | M      | R24      |       50 |     0.360 |         0.000 |     0.240 |                            0.000 |
| K12     | S      | K12      |       50 |     0.780 |         0.720 |     0.620 |                            0.100 |

## Closed loop per fault and policy (held-out split)

| policy                   | fault   | tier   |   n_test |   dispatch_rate |   family_attribution |   group_attribution |   mean_cost |   clf_dispatch_rate |   closure |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop |
|:-------------------------|:--------|:-------|---------:|----------------:|---------------------:|--------------------:|------------:|--------------------:|----------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|
| tau_none_5pct_fpr        | Q01     | N      |       50 |           0.980 |                0.960 |               0.960 |       1.140 |               0.980 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q02     | M      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q03     | M      |       50 |           0.040 |                0.000 |               0.000 |       0.260 |               0.040 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q04     | S      |       50 |           0.840 |                0.720 |               0.720 |       1.700 |               0.840 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q05     | M      |       50 |           0.720 |                0.540 |               0.540 |       2.160 |               0.720 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q07     | M      |       50 |           0.960 |                0.900 |               0.900 |       1.440 |               0.960 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q09     | P      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K03     | N      |       50 |           1.000 |                0.980 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K04     | M      |       50 |           0.840 |                0.740 |               0.740 |       3.320 |               0.840 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K05     | S      |       50 |           1.000 |                0.920 |               0.960 |       3.180 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K06     | N      |       50 |           0.980 |                0.980 |               0.980 |       2.940 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K08     | M      |       50 |           0.940 |                0.860 |               0.920 |       2.980 |               0.940 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R01     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R03     | N      |       50 |           0.920 |                0.860 |               0.860 |       7.460 |               0.920 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R05     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R06     | P      |       50 |           0.800 |                0.680 |               0.720 |       6.320 |               0.800 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R07     | P      |       50 |           1.000 |                0.700 |               0.700 |       8.780 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R11     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R13     | M      |       50 |           0.960 |                0.920 |               0.920 |       7.760 |               0.960 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R22     | S      |       50 |           0.780 |                0.780 |               0.780 |       6.240 |               0.780 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R24     | M      |       50 |           0.540 |                0.500 |               0.500 |       4.360 |               0.540 |     0.540 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K12     | S      |       50 |           0.920 |                0.840 |               0.860 |       2.960 |               0.920 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | C2      | N      |       50 |           0.880 |                0.500 |               0.580 |       7.140 |               0.880 |     0.580 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | NONE    | -      |     2508 |           0.035 |                0.965 |               0.965 |       0.168 |               0.035 |   nan     |        0.001 |                  0.000 |                    0.001 |                  0.003 |             0.000 |
| global_crc_0.005         | Q01     | N      |       50 |           1.000 |                0.980 |               0.980 |       1.160 |               1.000 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q02     | M      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q03     | M      |       50 |           1.000 |                0.500 |               0.500 |       4.460 |               1.000 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q04     | S      |       50 |           1.000 |                0.720 |               0.720 |       3.120 |               1.000 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q05     | M      |       50 |           1.000 |                0.680 |               0.680 |       3.440 |               1.000 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q07     | M      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q09     | P      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K03     | N      |       50 |           1.000 |                0.980 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K04     | M      |       50 |           1.000 |                0.740 |               0.740 |       4.060 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K05     | S      |       50 |           1.000 |                0.920 |               0.960 |       3.180 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.120 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K08     | M      |       50 |           1.000 |                0.860 |               0.940 |       3.200 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R01     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R03     | N      |       50 |           1.000 |                0.860 |               0.860 |       8.180 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R05     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R06     | P      |       50 |           1.000 |                0.780 |               0.820 |       8.020 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R07     | P      |       50 |           1.000 |                0.700 |               0.700 |       8.780 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R11     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R13     | M      |       50 |           1.000 |                0.940 |               0.960 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R22     | S      |       50 |           1.000 |                0.880 |               0.920 |       7.760 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R24     | M      |       50 |           1.000 |                0.640 |               0.680 |       8.100 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K12     | S      |       50 |           1.000 |                0.880 |               0.900 |       3.180 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | C2      | N      |       50 |           1.000 |                0.500 |               0.620 |       7.740 |               1.000 |     0.620 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | NONE    | -      |     2508 |           0.999 |                0.001 |               0.001 |       4.642 |               0.999 |   nan     |        0.006 |                 -0.001 |                    0.002 |                  0.035 |             0.000 |
| mondrian_crc_0.0025      | Q01     | N      |       50 |           0.020 |                0.020 |               0.020 |       0.020 |               0.020 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q02     | M      |       50 |           0.780 |                0.760 |               0.760 |       0.940 |               0.780 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q03     | M      |       50 |           0.880 |                0.480 |               0.480 |       3.560 |               0.880 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q04     | S      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q05     | M      |       50 |           0.040 |                0.000 |               0.000 |       0.340 |               0.040 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q07     | M      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q09     | P      |       50 |           0.700 |                0.660 |               0.660 |       1.020 |               0.700 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K03     | N      |       50 |           0.820 |                0.800 |               0.820 |       2.460 |               0.820 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K04     | M      |       50 |           0.860 |                0.660 |               0.660 |       3.360 |               0.860 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K05     | S      |       50 |           0.900 |                0.820 |               0.860 |       2.880 |               0.900 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K06     | N      |       50 |           0.820 |                0.800 |               0.800 |       2.580 |               0.820 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K07     | S      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K08     | M      |       50 |           0.800 |                0.660 |               0.740 |       2.600 |               0.800 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K09     | M      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R01     | S      |       50 |           0.820 |                0.820 |               0.820 |       6.560 |               0.820 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R03     | N      |       50 |           0.800 |                0.700 |               0.700 |       6.540 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R05     | N      |       50 |           0.800 |                0.800 |               0.800 |       6.400 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R06     | P      |       50 |           0.820 |                0.660 |               0.700 |       6.520 |               0.820 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R07     | P      |       50 |           0.840 |                0.620 |               0.620 |       7.380 |               0.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R10     | N      |       50 |           0.720 |                0.720 |               0.720 |       5.760 |               0.720 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R11     | S      |       50 |           0.820 |                0.800 |               0.800 |       6.620 |               0.820 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R13     | M      |       50 |           0.880 |                0.840 |               0.860 |       7.100 |               0.880 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R15     | S      |       50 |           0.780 |                0.780 |               0.780 |       6.240 |               0.780 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R19     | S      |       50 |           0.760 |                0.760 |               0.760 |       6.080 |               0.760 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R22     | S      |       50 |           0.800 |                0.680 |               0.720 |       6.160 |               0.800 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R23     | S      |       50 |           0.860 |                0.860 |               0.860 |       6.880 |               0.860 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R24     | M      |       50 |           0.900 |                0.640 |               0.680 |       7.460 |               0.900 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R25     | S      |       50 |           0.880 |                0.880 |               0.880 |       7.040 |               0.880 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R26     | S      |       10 |           0.700 |                0.700 |               0.700 |       5.600 |               0.700 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K11     | S      |       50 |           0.820 |                0.820 |               0.820 |       2.460 |               0.820 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K12     | S      |       50 |           0.780 |                0.720 |               0.740 |       2.320 |               0.780 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | C2      | N      |       50 |           0.380 |                0.240 |               0.240 |       3.300 |               0.380 |     0.280 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | NONE    | -      |     2508 |           0.667 |                0.333 |               0.333 |       3.150 |               0.667 |   nan     |        0.001 |                  0.000 |                    0.002 |                  0.000 |             0.000 |
| mondrian_crc_0.005       | Q01     | N      |       50 |           0.980 |                0.960 |               0.960 |       1.140 |               0.980 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q02     | M      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q03     | M      |       50 |           0.880 |                0.480 |               0.480 |       3.560 |               0.880 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q04     | S      |       50 |           0.740 |                0.640 |               0.640 |       1.540 |               0.740 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q05     | M      |       50 |           0.640 |                0.460 |               0.460 |       2.060 |               0.640 |     0.460 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q07     | M      |       50 |           0.940 |                0.880 |               0.880 |       1.420 |               0.940 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q09     | P      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K03     | N      |       50 |           1.000 |                0.980 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K04     | M      |       50 |           0.980 |                0.740 |               0.740 |       4.040 |               0.980 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K05     | S      |       50 |           1.000 |                0.920 |               0.960 |       3.180 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.120 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K08     | M      |       50 |           1.000 |                0.860 |               0.940 |       3.200 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R01     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R03     | N      |       50 |           1.000 |                0.860 |               0.860 |       8.180 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R05     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R06     | P      |       50 |           1.000 |                0.780 |               0.820 |       8.020 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R07     | P      |       50 |           1.000 |                0.700 |               0.700 |       8.780 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R11     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R13     | M      |       50 |           1.000 |                0.940 |               0.960 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R22     | S      |       50 |           0.940 |                0.820 |               0.860 |       7.280 |               0.940 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R24     | M      |       50 |           0.900 |                0.640 |               0.680 |       7.460 |               0.900 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K12     | S      |       50 |           0.980 |                0.880 |               0.900 |       3.100 |               0.980 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | C2      | N      |       50 |           0.820 |                0.500 |               0.560 |       6.880 |               0.820 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | NONE    | -      |     2508 |           0.863 |                0.137 |               0.137 |       3.907 |               0.863 |   nan     |        0.002 |                 -0.000 |                    0.002 |                  0.003 |             0.000 |
| mondrian_crc_0.01        | Q01     | N      |       50 |           0.980 |                0.960 |               0.960 |       1.140 |               0.980 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q02     | M      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q03     | M      |       50 |           0.880 |                0.480 |               0.480 |       3.560 |               0.880 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q04     | S      |       50 |           0.780 |                0.660 |               0.660 |       1.640 |               0.780 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q05     | M      |       50 |           0.640 |                0.460 |               0.460 |       2.060 |               0.640 |     0.460 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q07     | M      |       50 |           0.960 |                0.900 |               0.900 |       1.440 |               0.960 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q09     | P      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K03     | N      |       50 |           1.000 |                0.980 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K04     | M      |       50 |           0.980 |                0.740 |               0.740 |       4.040 |               0.980 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K05     | S      |       50 |           1.000 |                0.920 |               0.960 |       3.180 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.120 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K08     | M      |       50 |           1.000 |                0.860 |               0.940 |       3.200 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R01     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R03     | N      |       50 |           1.000 |                0.860 |               0.860 |       8.180 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R05     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R06     | P      |       50 |           1.000 |                0.780 |               0.820 |       8.020 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R07     | P      |       50 |           1.000 |                0.700 |               0.700 |       8.780 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R11     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R13     | M      |       50 |           1.000 |                0.940 |               0.960 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R22     | S      |       50 |           0.940 |                0.820 |               0.860 |       7.280 |               0.940 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R24     | M      |       50 |           0.900 |                0.640 |               0.680 |       7.460 |               0.900 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K12     | S      |       50 |           0.980 |                0.880 |               0.900 |       3.100 |               0.980 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | C2      | N      |       50 |           0.860 |                0.500 |               0.580 |       6.980 |               0.860 |     0.580 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | NONE    | -      |     2508 |           0.864 |                0.136 |               0.136 |       3.912 |               0.864 |   nan     |        0.002 |                 -0.000 |                    0.002 |                  0.003 |             0.000 |
| mondrian_crc_0.02        | Q01     | N      |       50 |           1.000 |                0.980 |               0.980 |       1.160 |               1.000 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q02     | M      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q03     | M      |       50 |           0.960 |                0.480 |               0.480 |       4.280 |               0.960 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q04     | S      |       50 |           1.000 |                0.720 |               0.720 |       3.120 |               1.000 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q05     | M      |       50 |           1.000 |                0.680 |               0.680 |       3.440 |               1.000 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q07     | M      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q09     | P      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K03     | N      |       50 |           1.000 |                0.980 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K04     | M      |       50 |           1.000 |                0.740 |               0.740 |       4.060 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K05     | S      |       50 |           1.000 |                0.920 |               0.960 |       3.180 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.120 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K08     | M      |       50 |           1.000 |                0.860 |               0.940 |       3.200 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R01     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R03     | N      |       50 |           1.000 |                0.860 |               0.860 |       8.180 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R05     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R06     | P      |       50 |           1.000 |                0.780 |               0.820 |       8.020 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R07     | P      |       50 |           1.000 |                0.700 |               0.700 |       8.780 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R11     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R13     | M      |       50 |           1.000 |                0.940 |               0.960 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R22     | S      |       50 |           1.000 |                0.880 |               0.920 |       7.760 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R24     | M      |       50 |           1.000 |                0.640 |               0.680 |       8.100 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K12     | S      |       50 |           1.000 |                0.880 |               0.900 |       3.180 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | C2      | N      |       50 |           0.980 |                0.500 |               0.620 |       7.720 |               0.980 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | NONE    | -      |     2508 |           0.935 |                0.065 |               0.065 |       4.323 |               0.935 |   nan     |        0.003 |                  0.002 |                    0.002 |                  0.011 |             0.000 |
| capped_crc_0.005         | Q01     | N      |       50 |           0.980 |                0.960 |               0.960 |       1.140 |               0.980 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q02     | M      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q03     | M      |       50 |           0.180 |                0.020 |               0.020 |       1.260 |               0.180 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q04     | S      |       50 |           0.740 |                0.640 |               0.640 |       1.540 |               0.740 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q05     | M      |       50 |           0.620 |                0.460 |               0.460 |       1.900 |               0.620 |     0.460 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q07     | M      |       50 |           0.940 |                0.880 |               0.880 |       1.420 |               0.940 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q09     | P      |       50 |           1.000 |                0.900 |               0.900 |       1.800 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K03     | N      |       50 |           1.000 |                0.980 |               1.000 |       3.000 |               1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K04     | M      |       50 |           0.900 |                0.740 |               0.740 |       3.680 |               0.900 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K05     | S      |       50 |           1.000 |                0.920 |               0.960 |       3.180 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       3.120 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K08     | M      |       50 |           0.980 |                0.860 |               0.920 |       3.140 |               0.980 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R01     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R03     | N      |       50 |           0.980 |                0.860 |               0.860 |       8.000 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R05     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R06     | P      |       50 |           0.940 |                0.740 |               0.780 |       7.520 |               0.940 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R07     | P      |       50 |           1.000 |                0.700 |               0.700 |       8.780 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       8.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R11     | S      |       50 |           1.000 |                0.920 |               0.920 |       8.120 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R13     | M      |       50 |           1.000 |                0.940 |               0.960 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R22     | S      |       50 |           0.860 |                0.800 |               0.800 |       6.780 |               0.860 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R24     | M      |       50 |           0.840 |                0.620 |               0.640 |       6.960 |               0.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K12     | S      |       50 |           0.940 |                0.880 |               0.900 |       3.000 |               0.940 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | C2      | N      |       50 |           0.820 |                0.500 |               0.560 |       6.880 |               0.820 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | NONE    | -      |     2508 |           0.155 |                0.845 |               0.845 |       0.913 |               0.155 |   nan     |        0.001 |                 -0.000 |                    0.001 |                  0.003 |             0.000 |
| two_stage_0.005          | Q01     | N      |       50 |           1.000 |                0.960 |               0.960 |       1.860 |               0.980 |     0.380 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q02     | M      |       50 |           1.000 |                0.960 |               0.960 |       2.280 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q03     | M      |       50 |           0.620 |                0.020 |               0.020 |       2.760 |               0.180 |     0.080 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q04     | S      |       50 |           0.820 |                0.640 |               0.640 |       2.200 |               0.740 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q05     | M      |       50 |           0.760 |                0.460 |               0.460 |       3.160 |               0.620 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q07     | M      |       50 |           0.960 |                0.880 |               0.880 |       2.020 |               0.940 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q09     | P      |       50 |           1.000 |                0.900 |               0.900 |       3.600 |               1.000 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K03     | N      |       50 |           1.000 |                0.980 |               1.000 |       4.980 |               1.000 |     0.460 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K04     | M      |       50 |           0.920 |                0.740 |               0.760 |       5.000 |               0.900 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K05     | S      |       50 |           1.000 |                0.920 |               0.960 |       6.180 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K06     | N      |       50 |           1.000 |                0.980 |               0.980 |       5.160 |               1.000 |     0.540 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       5.100 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K08     | M      |       50 |           1.000 |                0.860 |               0.940 |       6.020 |               0.980 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R01     | S      |       50 |           1.000 |                1.000 |               1.000 |       9.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R03     | N      |       50 |           0.980 |                0.860 |               0.860 |       8.900 |               0.980 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R05     | N      |       50 |           1.000 |                1.000 |               1.000 |       8.480 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R06     | P      |       50 |           0.960 |                0.740 |               0.780 |       8.000 |               0.940 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R07     | P      |       50 |           1.000 |                0.700 |               0.700 |      10.160 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R10     | N      |       50 |           1.000 |                0.940 |               0.940 |       9.320 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R11     | S      |       50 |           1.000 |                0.920 |               0.920 |       9.500 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R13     | M      |       50 |           1.000 |                0.940 |               0.960 |       9.940 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R15     | S      |       50 |           1.000 |                1.000 |               1.000 |       9.860 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R19     | S      |       50 |           1.000 |                1.000 |               1.000 |       9.440 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R22     | S      |       50 |           0.920 |                0.800 |               0.800 |       7.800 |               0.860 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R24     | M      |       50 |           0.900 |                0.620 |               0.640 |       8.880 |               0.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       9.320 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R26     | S      |       10 |           1.000 |                1.000 |               1.000 |       8.600 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K11     | S      |       50 |           1.000 |                1.000 |               1.000 |       5.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K12     | S      |       50 |           1.000 |                0.940 |               0.960 |       6.360 |               0.940 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | C2      | N      |       50 |           0.860 |                0.500 |               0.560 |       8.080 |               0.820 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | NONE    | -      |     2508 |           0.472 |                0.528 |               0.528 |       2.079 |               0.155 |   nan     |        0.002 |                  0.013 |                    0.002 |                  0.003 |             0.000 |
| diagnosis_free_universal | Q01     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.360 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q02     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.160 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q03     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.100 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q04     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q05     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q07     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q09     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.120 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K03     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K04     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K05     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K06     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.160 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K07     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K08     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K09     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R01     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R03     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R05     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R06     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R07     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R10     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R11     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R13     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R15     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R19     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R22     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R23     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R24     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R25     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R26     | S      |       10 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K11     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K12     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | C2      | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.660 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | NONE    | -      |     2508 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |   nan     |        0.015 |                  0.008 |                    0.011 |                  0.051 |             0.000 |
