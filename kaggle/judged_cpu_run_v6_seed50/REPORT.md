# DiagRAG v6 judged run report

Device: cpu. Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2. Last session runtime: 576s.

## Verdict (gates fixed in JUDGED_PROTOCOL.json before results)

```
{
 "detectors_pass": 28,
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
   "rescued": 51,
   "rate": 0.51,
   "ci_lo": 0.4134784047743415
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
   "rescued": 91,
   "rate": 0.91,
   "ci_lo": 0.8377362530335634
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
  "detectors_pass": 21,
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
   "detectors_pass": 28,
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
   "detectors_pass": 21,
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
    "clean_dispatch_rate": 0.03110047846889952,
    "clean_clf_dispatch_rate": 0.03110047846889952,
    "clean_mean_cost": 0.1638755980861244,
    "mean_closure": 0.84875,
    "T1_loss": true,
    "T2_dispatch": true,
    "T3_cost": true,
    "T4_closure": true,
    "all_targets_met": true
   },
   {
    "policy": "global_crc_0.005",
    "clean_loss": 0.005980861244019139,
    "clean_dispatch_rate": 0.45055821371610844,
    "clean_clf_dispatch_rate": 0.45055821371610844,
    "clean_mean_cost": 2.366427432216906,
    "mean_closure": 0.8943749999999999,
    "T1_loss": false,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.0025",
    "clean_loss": 0.001993620414673046,
    "clean_dispatch_rate": 0.6666666666666666,
    "clean_clf_dispatch_rate": 0.6666666666666666,
    "clean_mean_cost": 2.839712918660287,
    "mean_closure": 0.5861363636363637,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": false,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.005",
    "clean_loss": 0.001993620414673046,
    "clean_dispatch_rate": 0.8564593301435407,
    "clean_clf_dispatch_rate": 0.8564593301435407,
    "clean_mean_cost": 3.632775119617225,
    "mean_closure": 0.85375,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.01",
    "clean_loss": 0.0023923444976076554,
    "clean_dispatch_rate": 0.8592503987240829,
    "clean_clf_dispatch_rate": 0.8592503987240829,
    "clean_mean_cost": 3.645135566188198,
    "mean_closure": 0.8631249999999999,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "mondrian_crc_0.02",
    "clean_loss": 0.005582137161084529,
    "clean_dispatch_rate": 0.9178628389154705,
    "clean_clf_dispatch_rate": 0.9178628389154705,
    "clean_mean_cost": 4.003588516746412,
    "mean_closure": 0.89375,
    "T1_loss": false,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "capped_crc_0.005",
    "clean_loss": 0.0007974481658692185,
    "clean_dispatch_rate": 0.16068580542264752,
    "clean_clf_dispatch_rate": 0.16068580542264752,
    "clean_mean_cost": 1.0546251993620415,
    "mean_closure": 0.8475,
    "T1_loss": true,
    "T2_dispatch": true,
    "T3_cost": true,
    "T4_closure": true,
    "all_targets_met": true
   },
   {
    "policy": "two_stage_0.005",
    "clean_loss": 0.003189792663476874,
    "clean_dispatch_rate": 0.48564593301435405,
    "clean_clf_dispatch_rate": 0.16068580542264752,
    "clean_mean_cost": 2.2137161084529504,
    "mean_closure": 0.825,
    "T1_loss": true,
    "T2_dispatch": false,
    "T3_cost": false,
    "T4_closure": true,
    "all_targets_met": false
   },
   {
    "policy": "diagnosis_free_universal",
    "clean_loss": 0.01634768740031898,
    "clean_dispatch_rate": 1.0,
    "clean_clf_dispatch_rate": 1.0,
    "clean_mean_cost": 12.0,
    "mean_closure": 0.7606249999999999,
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
  "mean_closure": 0.4128,
  "mean_closure_without_fallback": 0.23919999999999997,
  "mean_closure_grounded": 0.38,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5782766990291263,
  "hit_after": 0.6025485436893204,
  "delta": 0.024271844660194174,
  "ci_lo": 0.01699029126213592,
  "ci_hi": 0.03216019417475728,
  "fixed": 42,
  "broken": 2,
  "verdict": "PASS",
  "dispatched": 0.679004854368932,
  "mean_cost": 4.412014563106796
 },
 "detection_baselines": {
  "ours_1_minus_pNONE": [
   0.9766842197217462,
   0.9720210617702423,
   0.9811031535772539
  ],
  "qpp_neg_nqc": [
   0.5670337942287436,
   0.549132214277582,
   0.5869267737774837
  ],
  "qpp_neg_wig": [
   0.5498568577987979,
   0.5298483241209577,
   0.5725558738470913
  ],
  "neg_ce1": [
   0.6324881455575342,
   0.6128015089647666,
   0.6511173401381801
  ],
  "raglog_tier0_best_single_rag_rr_order": [
   0.551238215800406,
   0.5312247559755188,
   0.5688177726566361
  ],
  "raglog_tier0_features_hgb": [
   0.7338938203642004,
   0.718694802170479,
   0.7501671547707432
  ],
  "raglog_tier0_detect_rate_at_5pct_fa": 0.42152466367713004,
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
  "ours_detect_rate_at_5pct_fa": 0.9308135810377963
 },
 "repair_baselines": {
  "Q04:symspell": {
   "fault": "Q04",
   "repair": "symspell (external)",
   "n": 100,
   "rescued": 58,
   "ci_lo": 0.48206307998895265
  },
  "Q05:wordsegment": {
   "fault": "Q05",
   "repair": "wordsegment (external)",
   "n": 100,
   "rescued": 96,
   "ci_lo": 0.9016278276739262
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
   "fail_rate_given": 0.4802547770700637,
   "fail_ci_lo": 0.4454855935855454,
   "fail_ci_hi": 0.5152162760927274,
   "share_of_all_failures": 0.11617873651771957
  },
  {
   "signature": "token absent from corpus vocabulary",
   "fault": "Q04/Q05",
   "n_queries": 7175,
   "with_signature": 728,
   "prevalence": 0.10146341463414635,
   "prev_ci_lo": 0.09468866735401069,
   "prev_ci_hi": 0.1086646981806182,
   "fail_rate_given": 0.5865384615384616,
   "fail_ci_lo": 0.5504022561454514,
   "fail_ci_hi": 0.6217661475091101,
   "share_of_all_failures": 0.13158705701078582
  },
  {
   "signature": "OOV token segmentable into corpus words",
   "fault": "Q05",
   "n_queries": 7175,
   "with_signature": 173,
   "prevalence": 0.02411149825783972,
   "prev_ci_lo": 0.020808563663594456,
   "prev_ci_hi": 0.027923755489400928,
   "fail_rate_given": 0.5722543352601156,
   "fail_ci_lo": 0.4977470713383861,
   "fail_ci_hi": 0.6436223801933801,
   "share_of_all_failures": 0.030508474576271188
  },
  {
   "signature": "unfinished last word (q_prefix)",
   "fault": "Q01",
   "n_queries": 7175,
   "with_signature": 48,
   "prevalence": 0.006689895470383275,
   "prev_ci_lo": 0.005049755294883588,
   "prev_ci_hi": 0.008858003862248392,
   "fail_rate_given": 0.5208333333333334,
   "fail_ci_lo": 0.38328995635984375,
   "fail_ci_hi": 0.6552890998421254,
   "share_of_all_failures": 0.007704160246533128
  },
  {
   "signature": "identifier/code token",
   "fault": "Q07",
   "n_queries": 7175,
   "with_signature": 311,
   "prevalence": 0.04334494773519164,
   "prev_ci_lo": 0.038872386960387625,
   "prev_ci_hi": 0.048306246428040954,
   "fail_rate_given": 0.28938906752411575,
   "fail_ci_lo": 0.24180115838850746,
   "fail_ci_hi": 0.3421165958091589,
   "share_of_all_failures": 0.02773497688751926
  },
  {
   "signature": "conjunction / multi-intent marker",
   "fault": "Q09",
   "n_queries": 7175,
   "with_signature": 235,
   "prevalence": 0.032752613240418116,
   "prev_ci_lo": 0.02887768827836786,
   "prev_ci_hi": 0.03712761263257577,
   "fail_rate_given": 0.40425531914893614,
   "fail_ci_lo": 0.34353776662704033,
   "fail_ci_hi": 0.468052844053846,
   "share_of_all_failures": 0.029275808936825885
  },
  {
   "signature": "exact duplicate pair in top-5",
   "fault": "K05",
   "n_queries": 7175,
   "with_signature": 571,
   "prevalence": 0.07958188153310104,
   "prev_ci_lo": 0.07354203639095715,
   "prev_ci_hi": 0.08607168178886729,
   "fail_rate_given": 0.5884413309982487,
   "fail_ci_lo": 0.5476160014033027,
   "fail_ci_hi": 0.6280845741987414,
   "share_of_all_failures": 0.10354391371340524
  },
  {
   "signature": ">=2 chunks of one parent in top-5",
   "fault": "K12",
   "n_queries": 7175,
   "with_signature": 2810,
   "prevalence": 0.3916376306620209,
   "prev_ci_lo": 0.3804039532484469,
   "prev_ci_hi": 0.40298728357728275,
   "fail_rate_given": 0.3953736654804271,
   "fail_ci_lo": 0.37745028968671496,
   "fail_ci_hi": 0.4135827236854665,
   "share_of_all_failures": 0.3423728813559322
  },
  {
   "signature": "'nan' placeholder doc in top-5",
   "fault": "K08",
   "n_queries": 7175,
   "with_signature": 3253,
   "prevalence": 0.4533797909407665,
   "prev_ci_lo": 0.44188868119135166,
   "prev_ci_hi": 0.46492079625971783,
   "fail_rate_given": 0.34644943129419,
   "fail_ci_lo": 0.3302870936346592,
   "fail_ci_hi": 0.3629740093922734,
   "share_of_all_failures": 0.34730354391371343
  },
  {
   "signature": "'nan' placeholder ranked above the gold",
   "fault": "K08",
   "n_queries": 7175,
   "with_signature": 1297,
   "prevalence": 0.1807665505226481,
   "prev_ci_lo": 0.17203365688395422,
   "prev_ci_hi": 0.1898411057518449,
   "fail_rate_given": 0.6561295296838859,
   "fail_ci_lo": 0.6298514775679679,
   "fail_ci_hi": 0.6814854292468204,
   "share_of_all_failures": 0.26224961479198766
  },
  {
   "signature": "gold itself is a 'nan' placeholder doc",
   "fault": "K08",
   "n_queries": 7175,
   "with_signature": 4201,
   "prevalence": 0.5855052264808362,
   "prev_ci_lo": 0.5740633426107399,
   "prev_ci_hi": 0.5968555978489577,
   "fail_rate_given": 0.5251130683170674,
   "fail_ci_lo": 0.5099961618719644,
   "fail_ci_hi": 0.5401840874862993,
   "share_of_all_failures": 0.6798151001540832
  },
  {
   "signature": "ALL ESCI queries",
   "fault": "-",
   "n_queries": 7175,
   "with_signature": 7175,
   "prevalence": 1.0,
   "fail_rate_given": 0.4522648083623693,
   "fail_ci_lo": 0.4407767385467736,
   "fail_ci_hi": 0.4638039670645606
  }
 ],
 "verdict": "ADOPTED",
 "clean_net_hit_change": 0.0,
 "guarantee": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 4.8937072964050365e-05,
   "esci_rare": 0.9101717871426022,
   "shop": 6.184345755388954e-05
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
  "heldout_clean_loss": 0.001993620414673046,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0029904306220095694,
   "esci_rare": 0.0,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.85375,
  "L2": "PASS"
 },
 "policies": [
  {
   "policy": "tau_none_5pct_fpr",
   "mean_closure": 0.84875,
   "mean_closure_grounded": 0.8427272727272727,
   "mean_family_attribution": 0.845625,
   "mean_group_attribution": 0.84625,
   "mean_cost_faulted": 4.916875,
   "clean_dispatch_rate": 0.03110047846889952,
   "clean_clf_dispatch_rate": 0.03110047846889952,
   "clean_mean_cost": 0.1638755980861244,
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
   "mean_closure": 0.8943749999999999,
   "mean_closure_grounded": 0.8936363636363638,
   "mean_family_attribution": 0.8787499999999999,
   "mean_group_attribution": 0.880625,
   "mean_cost_faulted": 5.390625,
   "clean_dispatch_rate": 0.45055821371610844,
   "clean_clf_dispatch_rate": 0.45055821371610844,
   "clean_mean_cost": 2.366427432216906,
   "clean_loss": 0.005980861244019139,
   "clean_net_hit_change": -0.001594896331738437,
   "clean_loss_esci_common": 0.0017942583732057417,
   "clean_loss_esci_rare": 0.032520325203252036,
   "clean_loss_shop": 0.0,
   "T1_loss": false,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "mondrian_crc_0.0025",
   "mean_closure": 0.5861363636363637,
   "mean_closure_grounded": 0.5734710743801654,
   "mean_family_attribution": 0.5698863636363636,
   "mean_group_attribution": 0.5711363636363636,
   "mean_cost_faulted": 3.8440909090909092,
   "clean_dispatch_rate": 0.6666666666666666,
   "clean_clf_dispatch_rate": 0.6666666666666666,
   "clean_mean_cost": 2.839712918660287,
   "clean_loss": 0.001993620414673046,
   "clean_net_hit_change": 0.0,
   "clean_loss_esci_common": 0.0029904306220095694,
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
   "mean_closure_grounded": 0.8472727272727273,
   "mean_family_attribution": 0.850625,
   "mean_group_attribution": 0.8525,
   "mean_cost_faulted": 5.094374999999999,
   "clean_dispatch_rate": 0.8564593301435407,
   "clean_clf_dispatch_rate": 0.8564593301435407,
   "clean_mean_cost": 3.632775119617225,
   "clean_loss": 0.001993620414673046,
   "clean_net_hit_change": 0.0,
   "clean_loss_esci_common": 0.0029904306220095694,
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
   "mean_closure": 0.8631249999999999,
   "mean_closure_grounded": 0.8590909090909092,
   "mean_family_attribution": 0.86,
   "mean_group_attribution": 0.861875,
   "mean_cost_faulted": 5.151875,
   "clean_dispatch_rate": 0.8592503987240829,
   "clean_clf_dispatch_rate": 0.8592503987240829,
   "clean_mean_cost": 3.645135566188198,
   "clean_loss": 0.0023923444976076554,
   "clean_net_hit_change": -0.00039872408293460925,
   "clean_loss_esci_common": 0.0029904306220095694,
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
   "mean_closure": 0.89375,
   "mean_closure_grounded": 0.8927272727272727,
   "mean_family_attribution": 0.8825000000000001,
   "mean_group_attribution": 0.8843749999999999,
   "mean_cost_faulted": 5.396875,
   "clean_dispatch_rate": 0.9178628389154705,
   "clean_clf_dispatch_rate": 0.9178628389154705,
   "clean_mean_cost": 4.003588516746412,
   "clean_loss": 0.005582137161084529,
   "clean_net_hit_change": -0.001993620414673046,
   "clean_loss_esci_common": 0.0029904306220095694,
   "clean_loss_esci_rare": 0.024390243902439025,
   "clean_loss_shop": 0.0,
   "T1_loss": false,
   "T2_dispatch": false,
   "T3_cost": false,
   "T4_closure": true,
   "all_targets_met": false
  },
  {
   "policy": "capped_crc_0.005",
   "mean_closure": 0.8475,
   "mean_closure_grounded": 0.840909090909091,
   "mean_family_attribution": 0.83875,
   "mean_group_attribution": 0.839375,
   "mean_cost_faulted": 4.96625,
   "clean_dispatch_rate": 0.16068580542264752,
   "clean_clf_dispatch_rate": 0.16068580542264752,
   "clean_mean_cost": 1.0546251993620415,
   "clean_loss": 0.0007974481658692185,
   "clean_net_hit_change": 0.00039872408293460925,
   "clean_loss_esci_common": 0.0011961722488038277,
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
   "mean_closure": 0.825,
   "mean_closure_grounded": 0.8490909090909091,
   "mean_family_attribution": 0.839375,
   "mean_group_attribution": 0.8431249999999999,
   "mean_cost_faulted": 6.373693181818181,
   "clean_dispatch_rate": 0.48564593301435405,
   "clean_clf_dispatch_rate": 0.16068580542264752,
   "clean_mean_cost": 2.2137161084529504,
   "clean_loss": 0.003189792663476874,
   "clean_net_hit_change": 0.014752791068580542,
   "clean_loss_esci_common": 0.004784688995215311,
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
   "mean_closure": 0.7606249999999999,
   "mean_closure_grounded": 0.7963636363636365,
   "mean_family_attribution": 0.0,
   "mean_group_attribution": 0.0,
   "mean_cost_faulted": 12.0,
   "clean_dispatch_rate": 1.0,
   "clean_clf_dispatch_rate": 1.0,
   "clean_mean_cost": 12.0,
   "clean_loss": 0.01634768740031898,
   "clean_net_hit_change": 0.01076555023923445,
   "clean_loss_esci_common": 0.011363636363636364,
   "clean_loss_esci_rare": 0.05962059620596206,
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
   "hit_before": 0.5782766990291263,
   "hit_after": 0.6025485436893204,
   "delta": 0.024271844660194174,
   "ci_lo": 0.01699029126213592,
   "ci_hi": 0.03216019417475728,
   "fixed": 42,
   "broken": 2,
   "verdict": "PASS",
   "dispatched": 0.679004854368932,
   "mean_cost": 4.412014563106796
  },
  {
   "arm": "N1a",
   "what": "component: natural rules only",
   "n": 1648,
   "hit_before": 0.5782766990291263,
   "hit_after": 0.6025485436893204,
   "delta": 0.024271844660194174,
   "ci_lo": 0.0169751213592233,
   "ci_hi": 0.03216019417475728,
   "fixed": 42,
   "broken": 2,
   "verdict": "PASS"
  },
  {
   "arm": "N1b",
   "what": "component: classifier dispatch only",
   "n": 1648,
   "hit_before": 0.5782766990291263,
   "hit_after": 0.5825242718446602,
   "delta": 0.00424757281553398,
   "ci_lo": 0.0012135922330097086,
   "ci_hi": 0.007281553398058253,
   "fixed": 7,
   "broken": 0,
   "verdict": "PASS",
   "dispatched": 0.43143203883495146
  },
  {
   "arm": "B1",
   "what": "baseline: K12 parent collapse always on (no detection)",
   "n": 1648,
   "hit_before": 0.5782766990291263,
   "hit_after": 0.5964805825242718,
   "delta": 0.01820388349514563,
   "ci_lo": 0.010922330097087379,
   "ci_hi": 0.026092233009708737,
   "fixed": 37,
   "broken": 7,
   "verdict": "PASS"
  },
  {
   "arm": "B2",
   "what": "baseline: diagnosis-free universal repair on every query (cost 12)",
   "n": 1648,
   "hit_before": 0.5782766990291263,
   "hit_after": 0.600121359223301,
   "delta": 0.021844660194174758,
   "ci_lo": 0.010315533980582525,
   "ci_hi": 0.032766990291262135,
   "fixed": 61,
   "broken": 25,
   "verdict": "PASS"
  },
  {
   "arm": "NA1",
   "what": "natural misspelling: ours (QLEX, log-gated)",
   "n": 185,
   "hit_before": 0.5621621621621622,
   "hit_after": 0.5135135135135135,
   "delta": -0.04864864864864865,
   "ci_lo": -0.10270270270270271,
   "ci_hi": 0.005405405405405406,
   "fixed": 9,
   "broken": 18,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA1x",
   "what": "natural misspelling: SymSpell lookup_compound (external)",
   "n": 185,
   "hit_before": 0.5621621621621622,
   "hit_after": 0.4486486486486487,
   "delta": -0.11351351351351352,
   "ci_lo": -0.17297297297297298,
   "ci_hi": -0.05405405405405406,
   "fixed": 8,
   "broken": 29,
   "verdict": "HARM"
  },
  {
   "arm": "NA2",
   "what": "natural missing space: ours (QLEX)",
   "n": 47,
   "hit_before": 0.44680851063829785,
   "hit_after": 0.46808510638297873,
   "delta": 0.02127659574468085,
   "ci_lo": -0.06382978723404255,
   "ci_hi": 0.10638297872340426,
   "fixed": 3,
   "broken": 2,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA2x",
   "what": "natural missing space: wordsegment (external)",
   "n": 47,
   "hit_before": 0.44680851063829785,
   "hit_after": 0.48936170212765956,
   "delta": 0.0425531914893617,
   "ci_lo": 0.0,
   "ci_hi": 0.10638297872340426,
   "fixed": 2,
   "broken": 0,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA4",
   "what": "natural duplicate in top-5: K05 collapse",
   "n": 140,
   "hit_before": 0.5142857142857142,
   "hit_after": 0.5642857142857143,
   "delta": 0.05,
   "ci_lo": 0.014285714285714285,
   "ci_hi": 0.09285714285714286,
   "fixed": 8,
   "broken": 1,
   "verdict": "PASS"
  },
  {
   "arm": "NA5",
   "what": "natural chunk crowding: K12 parent collapse",
   "n": 637,
   "hit_before": 0.6436420722135008,
   "hit_after": 0.6923076923076923,
   "delta": 0.04866562009419152,
   "ci_lo": 0.03139717425431711,
   "ci_hi": 0.06750392464678179,
   "fixed": 33,
   "broken": 2,
   "verdict": "PASS"
  },
  {
   "arm": "NA1c",
   "what": "DEPLOYED LOOP, v5 config (natural typo repair OFF), on natural queries with q_correctable >= 1",
   "n": 185,
   "hit_before": 0.5621621621621622,
   "hit_after": 0.5675675675675675,
   "delta": 0.005405405405405406,
   "ci_lo": 0.0,
   "ci_hi": 0.016216216216216217,
   "fixed": 1,
   "broken": 0,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "NA1d",
   "what": "counterfactual: same loop with the v4 config (natural typo repair ON), same queries",
   "n": 185,
   "hit_before": 0.5621621621621622,
   "hit_after": 0.5675675675675675,
   "delta": 0.005405405405405406,
   "ci_lo": -0.016216216216216217,
   "ci_hi": 0.032432432432432434,
   "fixed": 3,
   "broken": 2,
   "verdict": "INCONCLUSIVE"
  },
  {
   "arm": "N1v4",
   "what": "counterfactual: DEPLOYED LOOP with the v4 config on all natural queries",
   "n": 1648,
   "hit_before": 0.5782766990291263,
   "hit_after": 0.6025485436893204,
   "delta": 0.024271844660194174,
   "ci_lo": 0.015776699029126214,
   "ci_hi": 0.03216019417475728,
   "fixed": 45,
   "broken": 5,
   "verdict": "PASS"
  }
 ],
 "unseen_mean_closure": 0.4128,
 "not_solved": [
  "Q03"
 ],
 "device": "cpu",
 "reranker": "cross-encoder/ms-marco-MiniLM-L-6-v2"
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
| Q03     | M      | True       | PASS       | FAIL     | False    |
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
| Q01     |   2977 |        851 |              526 |    225 |    100 |           50 |          50 |            0 |        0.308 |
| Q02     |   2977 |        660 |                0 |    560 |    100 |           50 |          50 |            0 |        0.152 |
| Q03     |   2977 |        279 |               82 |     97 |    100 |           50 |          50 |            0 |        0.508 |
| Q04     |   2977 |        169 |                3 |     66 |    100 |           50 |          50 |           35 |        0.602 |
| Q05     |   2977 |        459 |               42 |    317 |    100 |           50 |          50 |            0 |        0.24  |
| Q07     |   2391 |       2841 |             2130 |    611 |    100 |           50 |          50 |            0 |        0.141 |
| Q09     |   2977 |        266 |                0 |    166 |    100 |           50 |          50 |            0 |        0.376 |
| K03     |   1950 |        457 |              350 |      6 |    100 |           50 |          50 |            0 |        0.935 |
| K04     |   2977 |        160 |                0 |     60 |    100 |           50 |          50 |            0 |        0.625 |
| K05     |   2977 |        292 |                0 |    192 |    100 |           50 |          50 |            0 |        0.342 |
| K06     |   1871 |        111 |                0 |     11 |    100 |           50 |          50 |            0 |        0.901 |
| K07     |    246 |        149 |                0 |     49 |    100 |           50 |          50 |            0 |        0.671 |
| K08     |   2977 |        118 |                0 |     18 |    100 |           50 |          50 |            0 |        0.847 |
| K09     |    282 |        104 |                0 |      4 |    100 |           50 |          50 |            0 |        0.962 |
| R01     |   2977 |        186 |                0 |     86 |    100 |           50 |          50 |            0 |        0.538 |
| R03     |   2977 |       1489 |                0 |   1389 |    100 |           50 |          50 |            0 |        0.067 |
| R05     |   2977 |        157 |                0 |     57 |    100 |           50 |          50 |            0 |        0.637 |
| R06     |   2977 |        100 |                0 |      0 |    100 |           50 |          50 |            0 |        1     |
| R07     |   2977 |        377 |                0 |    277 |    100 |           50 |          50 |            0 |        0.265 |
| R10     |   2977 |       1413 |                0 |   1313 |    100 |           50 |          50 |            0 |        0.071 |
| R11     |   2977 |       1438 |                0 |   1338 |    100 |           50 |          50 |            0 |        0.07  |
| R13     |   2977 |       1651 |                0 |   1550 |    100 |           50 |          50 |            0 |        0.061 |
| R15     |   2977 |        964 |                0 |    864 |    100 |           50 |          50 |            0 |        0.104 |
| R19     |   2977 |        779 |                0 |    679 |    100 |           50 |          50 |            0 |        0.128 |
| R22     |   2977 |       1414 |                0 |   1314 |    100 |           50 |          50 |            0 |        0.071 |
| R23     |   2977 |        281 |                0 |    181 |    100 |           50 |          50 |            0 |        0.356 |
| R24     |   2977 |        254 |                0 |    154 |    100 |           50 |          50 |            0 |        0.394 |
| R25     |   2977 |        304 |                0 |    204 |    100 |           50 |          50 |            0 |        0.329 |
| R26     |   2977 |       4000 |             1071 |   2906 |     23 |           12 |          11 |            0 |        0.008 |
| K11     |   1871 |        102 |                0 |      2 |    100 |           50 |          50 |            0 |        0.98  |
| K12     |   2977 |        145 |                0 |     45 |    100 |           50 |          50 |            0 |        0.69  |
| C2      |   2977 |        242 |               63 |     79 |    100 |           50 |          50 |            0 |        0.559 |

## Detector gates (AUROC bar 0.7, min test positives 50)

| fault   | detector                             |   n_pos_train |   n_pos_test |   n_neg_test |   auroc |   ci_lo |   ci_hi |   auroc_vs_clean | status   |
|:--------|:-------------------------------------|--------------:|-------------:|-------------:|--------:|--------:|--------:|-----------------:|:---------|
| Q01     | histgb_head                          |            50 |           50 |         3969 |  0.9895 |  0.9691 |  0.9991 |           0.9917 | PASS     |
| Q02     | histgb_head                          |            50 |           50 |         3969 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| Q03     | histgb_head                          |            50 |           50 |         3969 |  0.7012 |  0.6314 |  0.7581 |           0.6784 | PASS     |
| Q04     | tier0_rule                           |            50 |           50 |         3969 |  0.9830 |  0.9747 |  0.9895 |           0.9869 | PASS     |
| Q05     | histgb_head                          |            50 |           50 |         3969 |  0.9910 |  0.9821 |  0.9964 |           0.9925 | PASS     |
| Q07     | histgb_head                          |            50 |           50 |         3969 |  0.9996 |  0.9992 |  0.9999 |           0.9996 | PASS     |
| Q09     | histgb_head                          |            50 |           50 |         3969 |  0.9994 |  0.9987 |  1.0000 |           0.9992 | PASS     |
| K03     | histgb_head                          |            50 |           50 |         3969 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K04     | histgb_head                          |            50 |           50 |         3969 |  0.8520 |  0.7655 |  0.9379 |           0.8578 | PASS     |
| K05     | histgb_head                          |            50 |           50 |         3969 |  0.9993 |  0.9979 |  1.0000 |           0.9999 | PASS     |
| K06     | histgb_head                          |            50 |           50 |         3969 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K07     | tier0_rule                           |            50 |           50 |         3969 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K08     | histgb_head                          |            50 |           50 |         3969 |  0.9999 |  0.9998 |  1.0000 |           1.0000 | PASS     |
| K09     | histgb_head                          |            50 |           50 |         3969 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R01     | histgb_head                          |            50 |           50 |         3969 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R03     | histgb_head                          |            50 |           50 |         3969 |  1.0000 |  0.9999 |  1.0000 |           1.0000 | PASS     |
| R05     | histgb_head                          |            50 |           50 |         3969 |  0.9993 |  0.9985 |  0.9998 |           0.9996 | PASS     |
| R06     | histgb_head                          |            50 |           50 |         3969 |  0.9800 |  0.9540 |  0.9978 |           0.9849 | PASS     |
| R07     | histgb_head                          |            50 |           50 |         3969 |  0.9990 |  0.9975 |  1.0000 |           0.9997 | PASS     |
| R10     | histgb_head                          |            50 |           50 |         3969 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R11     | histgb_head                          |            50 |           50 |         3969 |  1.0000 |  0.9999 |  1.0000 |           1.0000 | PASS     |
| R13     | histgb_head                          |            50 |           50 |         3969 |  0.9999 |  0.9996 |  1.0000 |           1.0000 | PASS     |
| R15     | tier0_rule                           |            50 |           50 |         3969 |  0.9789 |  0.9479 |  0.9992 |           0.9800 | PASS     |
| R19     | histgb_head                          |            50 |           50 |         3969 |  0.9999 |  0.9995 |  1.0000 |           1.0000 | PASS     |
| R22     | histgb_head                          |            50 |           50 |         3969 |  0.9548 |  0.8948 |  0.9968 |           0.9561 | PASS     |
| R23     | tier0_rule                           |            50 |           50 |         3969 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R24     | histgb_head                          |            50 |           50 |         3969 |  0.9143 |  0.8490 |  0.9683 |           0.9261 | PASS     |
| R25     | tier0_rule                           |            50 |           50 |         3969 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R26     | tier0_rule                           |            12 |           11 |         4008 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | THIN     |
| K11     | tier0_rule                           |            50 |           50 |         3969 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K12     | histgb_head                          |            50 |           50 |         3969 |  0.9999 |  0.9996 |  1.0000 |           0.9998 | PASS     |
| C2      | tier0_rule(second factor-group mass) |            50 |           50 |         4019 |  0.8232 |  0.7394 |  0.9017 |         nan      | PASS     |

## Repair gates (Wilson lower bound >= 0.5)

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost |   harm_rate | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|------------:|:---------|
| Q01     |      100 |        73 |         0.730 |   0.636 |   0.807 |        20 |            0 |       0.000 | PASS     |
| Q02     |      100 |        84 |         0.840 |   0.756 |   0.899 |        20 |            0 |       0.000 | PASS     |
| Q03     |      100 |         1 |         0.010 |   0.002 |   0.054 |        20 |            0 |       0.000 | FAIL     |
| Q04     |      100 |        78 |         0.780 |   0.689 |   0.850 |        20 |            1 |       0.050 | PASS     |
| Q05     |      100 |        89 |         0.890 |   0.814 |   0.937 |        20 |            0 |       0.000 | PASS     |
| Q07     |      100 |        84 |         0.840 |   0.756 |   0.899 |        20 |            0 |       0.000 | PASS     |
| Q09     |      100 |        78 |         0.780 |   0.689 |   0.850 |        20 |            0 |       0.000 | PASS     |
| K03     |      100 |        86 |         0.860 |   0.779 |   0.915 |        20 |            0 |       0.000 | PASS     |
| K04     |      100 |        91 |         0.910 |   0.838 |   0.952 |        20 |            0 |       0.000 | PASS     |
| K05     |      100 |        97 |         0.970 |   0.915 |   0.990 |        20 |            0 |       0.000 | PASS     |
| K06     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K07     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K08     |      100 |        97 |         0.970 |   0.915 |   0.990 |        20 |            0 |       0.000 | PASS     |
| K09     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R01     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R03     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R05     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R06     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R07     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R10     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R11     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R13     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R15     |      100 |        98 |         0.980 |   0.930 |   0.994 |        20 |            0 |       0.000 | PASS     |
| R19     |      100 |        95 |         0.950 |   0.888 |   0.978 |        20 |            0 |       0.000 | PASS     |
| R22     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R23     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R24     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R25     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R26     |       23 |        23 |         1.000 |   0.857 |   1.000 |        20 |            0 |       0.000 | THIN     |
| K11     |      100 |       100 |         1.000 |   0.963 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K12     |      100 |        96 |         0.960 |   0.902 |   0.984 |        20 |            1 |       0.050 | PASS     |
| C2      |      100 |        82 |         0.820 |   0.733 |   0.883 |         0 |            0 |       0.000 | PASS     |

## Dispatch policies (held-out)

| policy                   |   mean_closure |   mean_closure_grounded |   mean_family_attribution |   mean_group_attribution |   mean_cost_faulted |   clean_dispatch_rate |   clean_clf_dispatch_rate |   clean_mean_cost |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop | T1_loss   | T2_dispatch   | T3_cost   | T4_closure   | all_targets_met   |
|:-------------------------|---------------:|------------------------:|--------------------------:|-------------------------:|--------------------:|----------------------:|--------------------------:|------------------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|:----------|:--------------|:----------|:-------------|:------------------|
| tau_none_5pct_fpr        |         0.8488 |                  0.8427 |                    0.8456 |                   0.8462 |              4.9169 |                0.0311 |                    0.0311 |            0.1639 |       0.0008 |                 0.0000 |                   0.0006 |                 0.0027 |            0.0000 | True      | True          | True      | True         | True              |
| global_crc_0.005         |         0.8944 |                  0.8936 |                    0.8787 |                   0.8806 |              5.3906 |                0.4506 |                    0.4506 |            2.3664 |       0.0060 |                -0.0016 |                   0.0018 |                 0.0325 |            0.0000 | False     | False         | False     | True         | False             |
| mondrian_crc_0.0025      |         0.5861 |                  0.5735 |                    0.5699 |                   0.5711 |              3.8441 |                0.6667 |                    0.6667 |            2.8397 |       0.0020 |                 0.0000 |                   0.0030 |                 0.0000 |            0.0000 | True      | False         | False     | False        | False             |
| mondrian_crc_0.005       |         0.8538 |                  0.8473 |                    0.8506 |                   0.8525 |              5.0944 |                0.8565 |                    0.8565 |            3.6328 |       0.0020 |                 0.0000 |                   0.0030 |                 0.0000 |            0.0000 | True      | False         | False     | True         | False             |
| mondrian_crc_0.01        |         0.8631 |                  0.8591 |                    0.8600 |                   0.8619 |              5.1519 |                0.8593 |                    0.8593 |            3.6451 |       0.0024 |                -0.0004 |                   0.0030 |                 0.0027 |            0.0000 | True      | False         | False     | True         | False             |
| mondrian_crc_0.02        |         0.8938 |                  0.8927 |                    0.8825 |                   0.8844 |              5.3969 |                0.9179 |                    0.9179 |            4.0036 |       0.0056 |                -0.0020 |                   0.0030 |                 0.0244 |            0.0000 | False     | False         | False     | True         | False             |
| capped_crc_0.005         |         0.8475 |                  0.8409 |                    0.8387 |                   0.8394 |              4.9662 |                0.1607 |                    0.1607 |            1.0546 |       0.0008 |                 0.0004 |                   0.0012 |                 0.0000 |            0.0000 | True      | True          | True      | True         | True              |
| two_stage_0.005          |         0.8250 |                  0.8491 |                    0.8394 |                   0.8431 |              6.3737 |                0.4856 |                    0.1607 |            2.2137 |       0.0032 |                 0.0148 |                   0.0048 |                 0.0000 |            0.0000 | True      | False         | False     | True         | False             |
| diagnosis_free_universal |         0.7606 |                  0.7964 |                    0.0000 |                   0.0000 |             12.0000 |                1.0000 |                    1.0000 |           12.0000 |       0.0163 |                 0.0108 |                   0.0114 |                 0.0596 |            0.0000 | False     | False         | False     | False        | False             |

## Loop gates (L1 do-no-harm on held-out clean, L2 mean closure, U1 unseen, N1 natural traffic)

```
{
 "GUARANTEE": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 4.8937072964050365e-05,
   "esci_rare": 0.9101717871426022,
   "shop": 6.184345755388954e-05
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
  "heldout_clean_loss": 0.001993620414673046,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0029904306220095694,
   "esci_rare": 0.0,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.85375,
  "L2": "PASS"
 },
 "U1": {
  "mean_closure": 0.4128,
  "mean_closure_without_fallback": 0.23919999999999997,
  "mean_closure_grounded": 0.38,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5782766990291263,
  "hit_after": 0.6025485436893204,
  "delta": 0.024271844660194174,
  "ci_lo": 0.01699029126213592,
  "ci_hi": 0.03216019417475728,
  "fixed": 42,
  "broken": 2,
  "verdict": "PASS",
  "dispatched": 0.679004854368932,
  "mean_cost": 4.412014563106796
 }
}
```

## Prevalence census (every ESCI query with an Exact product in the corpus)

| signature                               | fault   |   n_queries |   with_signature |   prevalence |   prev_ci_lo |   prev_ci_hi |   fail_rate_given |   fail_ci_lo |   fail_ci_hi |   share_of_all_failures |
|:----------------------------------------|:--------|------------:|-----------------:|-------------:|-------------:|-------------:|------------------:|-------------:|-------------:|------------------------:|
| misspelling token (q_correctable>=1)    | Q04     |        7175 |              785 |       0.1094 |       0.1024 |       0.1168 |            0.4803 |       0.4455 |       0.5152 |                  0.1162 |
| token absent from corpus vocabulary     | Q04/Q05 |        7175 |              728 |       0.1015 |       0.0947 |       0.1087 |            0.5865 |       0.5504 |       0.6218 |                  0.1316 |
| OOV token segmentable into corpus words | Q05     |        7175 |              173 |       0.0241 |       0.0208 |       0.0279 |            0.5723 |       0.4977 |       0.6436 |                  0.0305 |
| unfinished last word (q_prefix)         | Q01     |        7175 |               48 |       0.0067 |       0.0050 |       0.0089 |            0.5208 |       0.3833 |       0.6553 |                  0.0077 |
| identifier/code token                   | Q07     |        7175 |              311 |       0.0433 |       0.0389 |       0.0483 |            0.2894 |       0.2418 |       0.3421 |                  0.0277 |
| conjunction / multi-intent marker       | Q09     |        7175 |              235 |       0.0328 |       0.0289 |       0.0371 |            0.4043 |       0.3435 |       0.4681 |                  0.0293 |
| exact duplicate pair in top-5           | K05     |        7175 |              571 |       0.0796 |       0.0735 |       0.0861 |            0.5884 |       0.5476 |       0.6281 |                  0.1035 |
| >=2 chunks of one parent in top-5       | K12     |        7175 |             2810 |       0.3916 |       0.3804 |       0.4030 |            0.3954 |       0.3775 |       0.4136 |                  0.3424 |
| 'nan' placeholder doc in top-5          | K08     |        7175 |             3253 |       0.4534 |       0.4419 |       0.4649 |            0.3464 |       0.3303 |       0.3630 |                  0.3473 |
| 'nan' placeholder ranked above the gold | K08     |        7175 |             1297 |       0.1808 |       0.1720 |       0.1898 |            0.6561 |       0.6299 |       0.6815 |                  0.2622 |
| gold itself is a 'nan' placeholder doc  | K08     |        7175 |             4201 |       0.5855 |       0.5741 |       0.5969 |            0.5251 |       0.5100 |       0.5402 |                  0.6798 |
| ALL ESCI queries                        | -       |        7175 |             7175 |       1.0000 |     nan      |     nan      |            0.4523 |       0.4408 |       0.4638 |                nan      |

## Detection baselines (held-out, fault vs clean AUROC with 95% bootstrap CI)

| method                                |   auroc |   ci_lo |   ci_hi |
|:--------------------------------------|--------:|--------:|--------:|
| ours_1_minus_pNONE                    |  0.9767 |  0.9720 |  0.9811 |
| qpp_neg_nqc                           |  0.5670 |  0.5491 |  0.5869 |
| qpp_neg_wig                           |  0.5499 |  0.5298 |  0.5726 |
| neg_ce1                               |  0.6325 |  0.6128 |  0.6511 |
| raglog_tier0_best_single_rag_rr_order |  0.5512 |  0.5312 |  0.5688 |
| raglog_tier0_features_hgb             |  0.7339 |  0.7187 |  0.7502 |

## External repair baselines (oracle-dispatched, injected held-out + train episodes)

| fault   | repair                 |   n |   rescued |   ci_lo |
|:--------|:-----------------------|----:|----------:|--------:|
| Q04     | symspell (external)    | 100 |        58 |   0.482 |
| Q05     | wordsegment (external) | 100 |        96 |   0.902 |

## Family repairs, oracle-dispatched

| fault   | family   |   n |   rescued |   rate |   ci_lo |
|:--------|:---------|----:|----------:|-------:|--------:|
| Q01     | QLEX     | 100 |        51 |  0.510 |   0.413 |
| Q03     | QLEX     | 100 |         0 |  0.000 |   0.000 |
| Q04     | QLEX     | 100 |        64 |  0.640 |   0.542 |
| Q05     | QLEX     | 100 |        76 |  0.760 |   0.668 |
| K04     | STALE    | 100 |        91 |  0.910 |   0.838 |
| R03     | ENC      | 100 |       100 |  1.000 |   0.963 |
| R07     | STALE    | 100 |       100 |  1.000 |   0.963 |
| R10     | ENC      | 100 |       100 |  1.000 |   0.963 |
| R11     | ENC      | 100 |       100 |  1.000 |   0.963 |

## Natural traffic (no injection, never-examined queries): deployed loop, components, baselines

| arm   | what                                                                                           |    n |   hit_before |   hit_after |   delta |   ci_lo |   ci_hi |   fixed |   broken | verdict      |   dispatched |   mean_cost |
|:------|:-----------------------------------------------------------------------------------------------|-----:|-------------:|------------:|--------:|--------:|--------:|--------:|---------:|:-------------|-------------:|------------:|
| N1    | DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds                | 1648 |       0.5783 |      0.6025 |  0.0243 |  0.0170 |  0.0322 |      42 |        2 | PASS         |       0.6790 |      4.4120 |
| N1a   | component: natural rules only                                                                  | 1648 |       0.5783 |      0.6025 |  0.0243 |  0.0170 |  0.0322 |      42 |        2 | PASS         |     nan      |    nan      |
| N1b   | component: classifier dispatch only                                                            | 1648 |       0.5783 |      0.5825 |  0.0042 |  0.0012 |  0.0073 |       7 |        0 | PASS         |       0.4314 |    nan      |
| B1    | baseline: K12 parent collapse always on (no detection)                                         | 1648 |       0.5783 |      0.5965 |  0.0182 |  0.0109 |  0.0261 |      37 |        7 | PASS         |     nan      |    nan      |
| B2    | baseline: diagnosis-free universal repair on every query (cost 12)                             | 1648 |       0.5783 |      0.6001 |  0.0218 |  0.0103 |  0.0328 |      61 |       25 | PASS         |     nan      |    nan      |
| NA1   | natural misspelling: ours (QLEX, log-gated)                                                    |  185 |       0.5622 |      0.5135 | -0.0486 | -0.1027 |  0.0054 |       9 |       18 | INCONCLUSIVE |     nan      |    nan      |
| NA1x  | natural misspelling: SymSpell lookup_compound (external)                                       |  185 |       0.5622 |      0.4486 | -0.1135 | -0.1730 | -0.0541 |       8 |       29 | HARM         |     nan      |    nan      |
| NA2   | natural missing space: ours (QLEX)                                                             |   47 |       0.4468 |      0.4681 |  0.0213 | -0.0638 |  0.1064 |       3 |        2 | INCONCLUSIVE |     nan      |    nan      |
| NA2x  | natural missing space: wordsegment (external)                                                  |   47 |       0.4468 |      0.4894 |  0.0426 |  0.0000 |  0.1064 |       2 |        0 | INCONCLUSIVE |     nan      |    nan      |
| NA4   | natural duplicate in top-5: K05 collapse                                                       |  140 |       0.5143 |      0.5643 |  0.0500 |  0.0143 |  0.0929 |       8 |        1 | PASS         |     nan      |    nan      |
| NA5   | natural chunk crowding: K12 parent collapse                                                    |  637 |       0.6436 |      0.6923 |  0.0487 |  0.0314 |  0.0675 |      33 |        2 | PASS         |     nan      |    nan      |
| NA1c  | DEPLOYED LOOP, v5 config (natural typo repair OFF), on natural queries with q_correctable >= 1 |  185 |       0.5622 |      0.5676 |  0.0054 |  0.0000 |  0.0162 |       1 |        0 | INCONCLUSIVE |     nan      |    nan      |
| NA1d  | counterfactual: same loop with the v4 config (natural typo repair ON), same queries            |  185 |       0.5622 |      0.5676 |  0.0054 | -0.0162 |  0.0324 |       3 |        2 | INCONCLUSIVE |     nan      |    nan      |
| N1v4  | counterfactual: DEPLOYED LOOP with the v4 config on all natural queries                        | 1648 |       0.5783 |      0.6025 |  0.0243 |  0.0158 |  0.0322 |      45 |        5 | PASS         |     nan      |    nan      |

## Unseen faults (leave-one-fault-out attributor)

| fault   | tier   | family   |   n_test |   flagged |   right_group |   closure |   closure_without_group_fallback |
|:--------|:-------|:---------|---------:|----------:|--------------:|----------:|---------------------------------:|
| Q01     | N      | QLEX     |       50 |     0.420 |         0.300 |     0.220 |                            0.220 |
| Q02     | M      | Q02      |       50 |     0.540 |         0.080 |     0.060 |                            0.020 |
| Q03     | M      | QLEX     |       50 |     0.260 |         0.100 |     0.020 |                            0.000 |
| Q04     | S      | QLEX     |       50 |     0.660 |         0.440 |     0.360 |                            0.360 |
| Q05     | M      | QLEX     |       50 |     0.420 |         0.320 |     0.280 |                            0.280 |
| Q07     | M      | Q07      |       50 |     0.020 |         0.020 |     0.000 |                            0.000 |
| Q09     | P      | Q09      |       50 |     0.400 |         0.080 |     0.000 |                            0.000 |
| K03     | N      | K03      |       50 |     0.980 |         0.980 |     0.400 |                            0.100 |
| K04     | M      | STALE    |       50 |     0.820 |         0.000 |     0.780 |                            0.760 |
| K05     | S      | K05      |       50 |     1.000 |         0.980 |     0.740 |                            0.020 |
| K06     | N      | K06      |       50 |     1.000 |         1.000 |     0.000 |                            0.000 |
| K08     | M      | K08      |       50 |     0.820 |         0.820 |     0.560 |                            0.040 |
| K09     | M      | K09      |       50 |     0.500 |         0.480 |     0.480 |                            0.000 |
| R01     | S      | R01      |       50 |     0.220 |         0.080 |     0.060 |                            0.000 |
| R03     | N      | ENC      |       50 |     1.000 |         0.980 |     1.000 |                            1.000 |
| R05     | N      | R05      |       50 |     0.300 |         0.200 |     0.240 |                            0.020 |
| R06     | P      | R06      |       50 |     0.700 |         0.320 |     0.420 |                            0.000 |
| R07     | P      | STALE    |       50 |     0.980 |         0.000 |     0.980 |                            0.980 |
| R10     | N      | ENC      |       50 |     1.000 |         1.000 |     0.980 |                            0.980 |
| R11     | S      | ENC      |       50 |     1.000 |         1.000 |     1.000 |                            1.000 |
| R13     | M      | R13      |       50 |     0.420 |         0.160 |     0.260 |                            0.080 |
| R19     | S      | R19      |       50 |     0.600 |         0.460 |     0.360 |                            0.000 |
| R22     | S      | R22      |       50 |     0.420 |         0.180 |     0.280 |                            0.060 |
| R24     | M      | R24      |       50 |     0.500 |         0.280 |     0.380 |                            0.000 |
| K12     | S      | K12      |       50 |     0.740 |         0.660 |     0.460 |                            0.060 |

## Closed loop per fault and policy (held-out split)

| policy                   | fault   | tier   |   n_test |   dispatch_rate |   family_attribution |   group_attribution |   mean_cost |   clf_dispatch_rate |   closure |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop |
|:-------------------------|:--------|:-------|---------:|----------------:|---------------------:|--------------------:|------------:|--------------------:|----------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|
| tau_none_5pct_fpr        | Q01     | N      |       50 |           0.940 |                0.880 |               0.880 |       1.320 |               0.940 |     0.540 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q02     | M      |       50 |           1.000 |                0.940 |               0.940 |       1.380 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q03     | M      |       50 |           0.080 |                0.080 |               0.080 |       0.080 |               0.080 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q04     | S      |       50 |           0.840 |                0.760 |               0.760 |       1.480 |               0.840 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q05     | M      |       50 |           0.680 |                0.540 |               0.540 |       1.700 |               0.680 |     0.500 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q07     | M      |       50 |           0.880 |                0.840 |               0.840 |       1.100 |               0.880 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q09     | P      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K03     | N      |       50 |           0.980 |                0.920 |               0.920 |       3.140 |               0.980 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K04     | M      |       50 |           0.760 |                0.580 |               0.580 |       3.720 |               0.760 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.320 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K06     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K08     | M      |       50 |           0.960 |                0.960 |               0.960 |       2.880 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R01     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R03     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R05     | N      |       50 |           0.880 |                0.820 |               0.820 |       7.100 |               0.880 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R06     | P      |       50 |           0.820 |                0.700 |               0.700 |       6.720 |               0.820 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R07     | P      |       50 |           0.980 |                0.760 |               0.720 |       8.080 |               0.980 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R10     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R11     | S      |       50 |           1.000 |                0.880 |               0.880 |       8.160 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R13     | M      |       50 |           0.960 |                0.840 |               0.840 |       7.880 |               0.960 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R15     | S      |       50 |           0.960 |                0.960 |               0.960 |       7.680 |               0.960 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R19     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R22     | S      |       50 |           0.800 |                0.740 |               0.740 |       6.460 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R24     | M      |       50 |           0.640 |                0.540 |               0.540 |       5.060 |               0.640 |     0.620 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R26     | S      |       11 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K12     | S      |       50 |           0.940 |                0.920 |               0.920 |       2.980 |               0.940 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | C2      | N      |       50 |           0.940 |                0.640 |               0.680 |       7.640 |               0.940 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | NONE    | -      |     2508 |           0.031 |                0.969 |               0.969 |       0.164 |               0.031 |   nan     |        0.001 |                  0.000 |                    0.001 |                  0.003 |             0.000 |
| global_crc_0.005         | Q01     | N      |       50 |           1.000 |                0.920 |               0.920 |       1.540 |               1.000 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q02     | M      |       50 |           1.000 |                0.940 |               0.940 |       1.380 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q03     | M      |       50 |           0.740 |                0.380 |               0.380 |       3.260 |               0.740 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q04     | S      |       50 |           0.980 |                0.780 |               0.780 |       2.480 |               0.980 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q05     | M      |       50 |           1.000 |                0.740 |               0.740 |       2.780 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q07     | M      |       50 |           1.000 |                0.900 |               0.900 |       1.700 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q09     | P      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K03     | N      |       50 |           1.000 |                0.940 |               0.940 |       3.200 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K04     | M      |       50 |           0.920 |                0.620 |               0.620 |       4.800 |               0.920 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.320 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K06     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K08     | M      |       50 |           1.000 |                0.980 |               0.980 |       3.160 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R01     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R03     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R05     | N      |       50 |           1.000 |                0.900 |               0.920 |       8.080 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R06     | P      |       50 |           0.980 |                0.760 |               0.760 |       8.080 |               0.980 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R07     | P      |       50 |           1.000 |                0.760 |               0.720 |       8.260 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R10     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R11     | S      |       50 |           1.000 |                0.880 |               0.880 |       8.160 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R13     | M      |       50 |           1.000 |                0.880 |               0.880 |       8.200 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R15     | S      |       50 |           0.980 |                0.960 |               0.960 |       7.860 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R19     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R22     | S      |       50 |           0.980 |                0.780 |               0.780 |       7.920 |               0.980 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R24     | M      |       50 |           0.960 |                0.620 |               0.640 |       7.620 |               0.960 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R26     | S      |       11 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K12     | S      |       50 |           1.000 |                0.960 |               0.960 |       3.180 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | C2      | N      |       50 |           1.000 |                0.660 |               0.700 |       8.060 |               1.000 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | NONE    | -      |     2508 |           0.451 |                0.549 |               0.549 |       2.366 |               0.451 |   nan     |        0.006 |                 -0.002 |                    0.002 |                  0.033 |             0.000 |
| mondrian_crc_0.0025      | Q01     | N      |       50 |           0.040 |                0.040 |               0.040 |       0.040 |               0.040 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q02     | M      |       50 |           0.860 |                0.800 |               0.800 |       1.240 |               0.860 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q03     | M      |       50 |           0.840 |                0.420 |               0.420 |       3.760 |               0.840 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q04     | S      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q05     | M      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q07     | M      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q09     | P      |       50 |           0.840 |                0.800 |               0.800 |       1.160 |               0.840 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K03     | N      |       50 |           0.660 |                0.600 |               0.600 |       2.180 |               0.660 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K04     | M      |       50 |           0.880 |                0.600 |               0.600 |       4.320 |               0.880 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K05     | S      |       50 |           0.920 |                0.860 |               0.880 |       3.080 |               0.920 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K06     | N      |       50 |           0.720 |                0.720 |               0.720 |       2.160 |               0.720 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K07     | S      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K08     | M      |       50 |           0.820 |                0.820 |               0.820 |       2.460 |               0.820 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K09     | M      |       50 |           0.000 |                0.000 |               0.000 |       0.000 |               0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R01     | S      |       50 |           0.840 |                0.840 |               0.840 |       6.720 |               0.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R03     | N      |       50 |           0.740 |                0.740 |               0.740 |       5.920 |               0.740 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R05     | N      |       50 |           0.700 |                0.640 |               0.640 |       5.660 |               0.700 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R06     | P      |       50 |           0.760 |                0.600 |               0.620 |       6.240 |               0.760 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R07     | P      |       50 |           0.820 |                0.620 |               0.600 |       6.880 |               0.820 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R10     | N      |       50 |           0.760 |                0.760 |               0.760 |       6.080 |               0.760 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R11     | S      |       50 |           0.760 |                0.740 |               0.740 |       6.140 |               0.760 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R13     | M      |       50 |           0.820 |                0.760 |               0.760 |       6.660 |               0.820 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R15     | S      |       50 |           0.760 |                0.720 |               0.720 |       5.960 |               0.760 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R19     | S      |       50 |           0.800 |                0.800 |               0.800 |       6.400 |               0.800 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R22     | S      |       50 |           0.760 |                0.580 |               0.580 |       6.020 |               0.760 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R23     | S      |       50 |           0.780 |                0.780 |               0.780 |       6.240 |               0.780 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R24     | M      |       50 |           0.860 |                0.600 |               0.620 |       6.740 |               0.860 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R25     | S      |       50 |           0.880 |                0.880 |               0.880 |       7.040 |               0.880 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R26     | S      |       11 |           0.636 |                0.636 |               0.636 |       5.091 |               0.636 |     0.636 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K11     | S      |       50 |           0.800 |                0.800 |               0.800 |       2.400 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K12     | S      |       50 |           0.820 |                0.780 |               0.780 |       2.640 |               0.820 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | C2      | N      |       50 |           0.400 |                0.300 |               0.300 |       3.780 |               0.400 |     0.360 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | NONE    | -      |     2508 |           0.667 |                0.333 |               0.333 |       2.840 |               0.667 |   nan     |        0.002 |                  0.000 |                    0.003 |                  0.000 |             0.000 |
| mondrian_crc_0.005       | Q01     | N      |       50 |           0.820 |                0.820 |               0.820 |       0.820 |               0.820 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q02     | M      |       50 |           1.000 |                0.940 |               0.940 |       1.380 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q03     | M      |       50 |           0.900 |                0.480 |               0.480 |       3.820 |               0.900 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q04     | S      |       50 |           0.740 |                0.680 |               0.680 |       1.220 |               0.740 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q05     | M      |       50 |           0.380 |                0.340 |               0.340 |       0.700 |               0.380 |     0.240 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q07     | M      |       50 |           0.800 |                0.800 |               0.800 |       0.800 |               0.800 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q09     | P      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K03     | N      |       50 |           1.000 |                0.940 |               0.940 |       3.200 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K04     | M      |       50 |           0.900 |                0.620 |               0.620 |       4.380 |               0.900 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.320 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K06     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K08     | M      |       50 |           0.980 |                0.980 |               0.980 |       2.940 |               0.980 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R01     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R03     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R05     | N      |       50 |           0.880 |                0.820 |               0.820 |       7.100 |               0.880 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R06     | P      |       50 |           0.920 |                0.720 |               0.740 |       7.560 |               0.920 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R07     | P      |       50 |           1.000 |                0.760 |               0.720 |       8.260 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R10     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R11     | S      |       50 |           1.000 |                0.880 |               0.880 |       8.160 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R13     | M      |       50 |           0.920 |                0.840 |               0.840 |       7.520 |               0.920 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R15     | S      |       50 |           1.000 |                0.960 |               0.960 |       7.880 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R19     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R22     | S      |       50 |           0.920 |                0.700 |               0.700 |       7.340 |               0.920 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R24     | M      |       50 |           0.880 |                0.600 |               0.620 |       6.760 |               0.880 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R26     | S      |       11 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K12     | S      |       50 |           0.980 |                0.940 |               0.940 |       3.120 |               0.980 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | C2      | N      |       50 |           0.880 |                0.640 |               0.680 |       7.280 |               0.880 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | NONE    | -      |     2508 |           0.856 |                0.144 |               0.144 |       3.633 |               0.856 |   nan     |        0.002 |                  0.000 |                    0.003 |                  0.000 |             0.000 |
| mondrian_crc_0.01        | Q01     | N      |       50 |           0.880 |                0.880 |               0.880 |       0.880 |               0.880 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q02     | M      |       50 |           1.000 |                0.940 |               0.940 |       1.380 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q03     | M      |       50 |           0.900 |                0.480 |               0.480 |       3.820 |               0.900 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q04     | S      |       50 |           0.780 |                0.700 |               0.700 |       1.420 |               0.780 |     0.540 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q05     | M      |       50 |           0.480 |                0.420 |               0.420 |       0.960 |               0.480 |     0.340 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q07     | M      |       50 |           0.860 |                0.820 |               0.820 |       1.080 |               0.860 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q09     | P      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K03     | N      |       50 |           1.000 |                0.940 |               0.940 |       3.200 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K04     | M      |       50 |           0.900 |                0.620 |               0.620 |       4.380 |               0.900 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.320 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K06     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K08     | M      |       50 |           0.980 |                0.980 |               0.980 |       2.940 |               0.980 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R01     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R03     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R05     | N      |       50 |           0.920 |                0.860 |               0.860 |       7.420 |               0.920 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R06     | P      |       50 |           0.920 |                0.720 |               0.740 |       7.560 |               0.920 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R07     | P      |       50 |           1.000 |                0.760 |               0.720 |       8.260 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R10     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R11     | S      |       50 |           1.000 |                0.880 |               0.880 |       8.160 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R13     | M      |       50 |           0.960 |                0.860 |               0.860 |       7.860 |               0.960 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R15     | S      |       50 |           1.000 |                0.960 |               0.960 |       7.880 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R19     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R22     | S      |       50 |           0.960 |                0.740 |               0.740 |       7.660 |               0.960 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R24     | M      |       50 |           0.880 |                0.600 |               0.620 |       6.760 |               0.880 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R26     | S      |       11 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K12     | S      |       50 |           1.000 |                0.960 |               0.960 |       3.180 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | C2      | N      |       50 |           0.880 |                0.640 |               0.680 |       7.280 |               0.880 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | NONE    | -      |     2508 |           0.859 |                0.141 |               0.141 |       3.645 |               0.859 |   nan     |        0.002 |                 -0.000 |                    0.003 |                  0.003 |             0.000 |
| mondrian_crc_0.02        | Q01     | N      |       50 |           0.980 |                0.920 |               0.920 |       1.360 |               0.980 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q02     | M      |       50 |           1.000 |                0.940 |               0.940 |       1.380 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q03     | M      |       50 |           0.940 |                0.500 |               0.500 |       4.020 |               0.940 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q04     | S      |       50 |           0.960 |                0.780 |               0.780 |       2.400 |               0.960 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q05     | M      |       50 |           1.000 |                0.740 |               0.740 |       2.780 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q07     | M      |       50 |           1.000 |                0.900 |               0.900 |       1.700 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q09     | P      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K03     | N      |       50 |           1.000 |                0.940 |               0.940 |       3.200 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K04     | M      |       50 |           0.920 |                0.620 |               0.620 |       4.560 |               0.920 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.320 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K06     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K08     | M      |       50 |           1.000 |                0.980 |               0.980 |       3.160 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R01     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R03     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R05     | N      |       50 |           0.980 |                0.900 |               0.900 |       7.920 |               0.980 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R06     | P      |       50 |           1.000 |                0.760 |               0.780 |       8.240 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R07     | P      |       50 |           1.000 |                0.760 |               0.720 |       8.260 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R10     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R11     | S      |       50 |           1.000 |                0.880 |               0.880 |       8.160 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R13     | M      |       50 |           1.000 |                0.880 |               0.880 |       8.200 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R15     | S      |       50 |           1.000 |                0.960 |               0.960 |       7.880 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R19     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R22     | S      |       50 |           1.000 |                0.780 |               0.780 |       7.980 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R24     | M      |       50 |           0.980 |                0.620 |               0.640 |       7.640 |               0.980 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R26     | S      |       11 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K12     | S      |       50 |           1.000 |                0.960 |               0.960 |       3.180 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | C2      | N      |       50 |           0.980 |                0.660 |               0.700 |       7.900 |               0.980 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | NONE    | -      |     2508 |           0.918 |                0.082 |               0.082 |       4.004 |               0.918 |   nan     |        0.006 |                 -0.002 |                    0.003 |                  0.024 |             0.000 |
| capped_crc_0.005         | Q01     | N      |       50 |           0.820 |                0.820 |               0.820 |       0.820 |               0.820 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q02     | M      |       50 |           1.000 |                0.940 |               0.940 |       1.380 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q03     | M      |       50 |           0.280 |                0.140 |               0.140 |       1.340 |               0.280 |     0.020 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q04     | S      |       50 |           0.740 |                0.680 |               0.680 |       1.220 |               0.740 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q05     | M      |       50 |           0.380 |                0.340 |               0.340 |       0.700 |               0.380 |     0.240 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q07     | M      |       50 |           0.800 |                0.800 |               0.800 |       0.800 |               0.800 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | Q09     | P      |       50 |           1.000 |                0.960 |               0.960 |       1.320 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K03     | N      |       50 |           1.000 |                0.940 |               0.940 |       3.200 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K04     | M      |       50 |           0.800 |                0.580 |               0.580 |       4.060 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       3.320 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K06     | N      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K08     | M      |       50 |           0.980 |                0.980 |               0.980 |       2.940 |               0.980 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R01     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R03     | N      |       50 |           1.000 |                0.960 |               0.960 |       8.040 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R05     | N      |       50 |           0.880 |                0.820 |               0.820 |       7.100 |               0.880 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R06     | P      |       50 |           0.880 |                0.720 |               0.720 |       7.180 |               0.880 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R07     | P      |       50 |           0.980 |                0.760 |               0.720 |       8.080 |               0.980 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R10     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R11     | S      |       50 |           1.000 |                0.880 |               0.880 |       8.160 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R13     | M      |       50 |           0.920 |                0.840 |               0.840 |       7.520 |               0.920 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R15     | S      |       50 |           0.960 |                0.960 |               0.960 |       7.680 |               0.960 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R19     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R22     | S      |       50 |           0.880 |                0.700 |               0.700 |       7.260 |               0.880 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R24     | M      |       50 |           0.780 |                0.600 |               0.600 |       6.300 |               0.780 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | R26     | S      |       11 |           1.000 |                1.000 |               1.000 |       8.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       3.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | K12     | S      |       50 |           0.980 |                0.940 |               0.940 |       3.120 |               0.980 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | C2      | N      |       50 |           0.880 |                0.640 |               0.680 |       7.280 |               0.880 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| capped_crc_0.005         | NONE    | -      |     2508 |           0.161 |                0.839 |               0.839 |       1.055 |               0.161 |   nan     |        0.001 |                  0.000 |                    0.001 |                  0.000 |             0.000 |
| two_stage_0.005          | Q01     | N      |       50 |           0.900 |                0.820 |               0.820 |       2.020 |               0.820 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q02     | M      |       50 |           1.000 |                0.940 |               0.940 |       2.760 |               1.000 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q03     | M      |       50 |           0.640 |                0.140 |               0.140 |       2.720 |               0.280 |     0.080 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q04     | S      |       50 |           0.800 |                0.680 |               0.680 |       2.180 |               0.740 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q05     | M      |       50 |           0.640 |                0.340 |               0.340 |       1.900 |               0.380 |     0.300 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q07     | M      |       50 |           0.880 |                0.800 |               0.800 |       1.160 |               0.800 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | Q09     | P      |       50 |           1.000 |                0.960 |               0.960 |       2.880 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K03     | N      |       50 |           1.000 |                0.940 |               0.940 |       5.600 |               1.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K04     | M      |       50 |           0.880 |                0.580 |               0.660 |       5.680 |               0.800 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K05     | S      |       50 |           1.000 |                0.940 |               0.960 |       6.320 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K06     | N      |       50 |           1.000 |                1.000 |               1.000 |       5.160 |               1.000 |     0.460 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K07     | S      |       50 |           1.000 |                1.000 |               1.000 |       5.280 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K08     | M      |       50 |           1.000 |                0.980 |               1.000 |       5.760 |               0.980 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K09     | M      |       50 |           1.000 |                1.000 |               1.000 |       3.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R01     | S      |       50 |           1.000 |                0.980 |               0.980 |       9.100 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R03     | N      |       50 |           1.000 |                0.960 |               0.960 |       9.060 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R05     | N      |       50 |           0.880 |                0.820 |               0.820 |       7.520 |               0.880 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R06     | P      |       50 |           0.900 |                0.720 |               0.720 |       7.720 |               0.880 |     0.860 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R07     | P      |       50 |           0.980 |                0.760 |               0.720 |       8.920 |               0.980 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R10     | N      |       50 |           1.000 |                0.980 |               0.980 |       8.860 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R11     | S      |       50 |           1.000 |                0.880 |               0.880 |       9.240 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R13     | M      |       50 |           0.940 |                0.840 |               0.840 |       8.600 |               0.920 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R15     | S      |       50 |           0.960 |                0.960 |               0.960 |       9.180 |               0.960 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R19     | S      |       50 |           1.000 |                0.980 |               0.980 |       9.460 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R22     | S      |       50 |           0.960 |                0.700 |               0.700 |       8.520 |               0.880 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R23     | S      |       50 |           1.000 |                0.980 |               0.980 |       8.020 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R24     | M      |       50 |           0.880 |                0.600 |               0.600 |       7.980 |               0.780 |     0.820 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R25     | S      |       50 |           1.000 |                1.000 |               1.000 |       9.560 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | R26     | S      |       11 |           1.000 |                1.000 |               1.000 |       8.818 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K11     | S      |       50 |           1.000 |                0.980 |               0.980 |       5.480 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | K12     | S      |       50 |           1.000 |                0.960 |               0.960 |       6.480 |               0.980 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | C2      | N      |       50 |           0.920 |                0.640 |               0.680 |       8.960 |               0.880 |     0.740 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| two_stage_0.005          | NONE    | -      |     2508 |           0.486 |                0.514 |               0.514 |       2.214 |               0.161 |   nan     |        0.003 |                  0.015 |                    0.005 |                  0.000 |             0.000 |
| diagnosis_free_universal | Q01     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.580 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q02     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.200 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q03     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.080 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q04     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.700 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q05     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.780 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q07     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q09     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.060 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K03     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K04     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K05     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K06     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.220 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K07     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K08     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K09     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R01     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R03     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R05     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R06     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R07     | P      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R10     | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R11     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R13     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R15     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R19     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R22     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R23     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R24     | M      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.980 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R25     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.900 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R26     | S      |       11 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K11     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.940 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K12     | S      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | C2      | N      |       50 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | NONE    | -      |     2508 |           1.000 |                0.000 |               0.000 |      12.000 |               1.000 |   nan     |        0.016 |                  0.011 |                    0.011 |                  0.060 |             0.000 |
