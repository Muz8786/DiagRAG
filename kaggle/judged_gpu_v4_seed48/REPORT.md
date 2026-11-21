# DiagRAG v4 judged run report

Device: cuda. Reranker: BAAI/bge-reranker-large. Last session runtime: 7734s.

## Verdict (gates fixed in JUDGED_PROTOCOL.json before results)

```
{
 "detectors_pass": 26,
 "repairs_pass": 27,
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
   "n": 50,
   "rescued": 30,
   "rate": 0.6,
   "ci_lo": 0.46181189102759373
  },
  {
   "fault": "Q03",
   "family": "QLEX",
   "n": 50,
   "rescued": 1,
   "rate": 0.02,
   "ci_lo": 0.0035391680889764613
  },
  {
   "fault": "Q04",
   "family": "QLEX",
   "n": 50,
   "rescued": 30,
   "rate": 0.6,
   "ci_lo": 0.46181189102759373
  },
  {
   "fault": "Q05",
   "family": "QLEX",
   "n": 50,
   "rescued": 43,
   "rate": 0.86,
   "ci_lo": 0.7381354280147191
  },
  {
   "fault": "K04",
   "family": "STALE",
   "n": 50,
   "rescued": 43,
   "rate": 0.86,
   "ci_lo": 0.7381354280147191
  },
  {
   "fault": "R03",
   "family": "ENC",
   "n": 50,
   "rescued": 50,
   "rate": 1.0,
   "ci_lo": 0.9286499658256813
  },
  {
   "fault": "R07",
   "family": "STALE",
   "n": 50,
   "rescued": 50,
   "rate": 1.0,
   "ci_lo": 0.9286499658256813
  },
  {
   "fault": "R10",
   "family": "ENC",
   "n": 50,
   "rescued": 50,
   "rate": 1.0,
   "ci_lo": 0.9286499658256813
  },
  {
   "fault": "R11",
   "family": "ENC",
   "n": 50,
   "rescued": 50,
   "rate": 1.0,
   "ci_lo": 0.9286499658256813
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
 "U1": {
  "mean_closure": 0.456,
  "mean_closure_without_fallback": 0.1984,
  "mean_closure_grounded": 0.475,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5898058252427184,
  "hit_after": 0.6116504854368932,
  "delta": 0.021844660194174758,
  "ci_lo": 0.012742718446601941,
  "ci_hi": 0.03155339805825243,
  "fixed": 47,
  "broken": 11,
  "verdict": "PASS",
  "dispatched": 0.9180825242718447,
  "mean_cost": 5.930825242718447
 },
 "detection_baselines": {
  "ours_1_minus_pNONE": [
   0.9765626493814412,
   0.9697446763468907,
   0.9829546139392894
  ],
  "qpp_neg_nqc": [
   0.592716399931165,
   0.5691742436660868,
   0.6183744716052435
  ],
  "qpp_neg_wig": [
   0.5821832157402627,
   0.5550970339698802,
   0.6070804753226483
  ],
  "neg_ce1": [
   0.6771252796420583,
   0.6521315365197521,
   0.6999571834093039
  ],
  "raglog_tier0_best_single_rag_rt_best_rank": [
   0.6460874012887435,
   0.6233791093513935,
   0.6696105312829722
  ],
  "raglog_tier0_features_hgb": [
   0.7606871068280464,
   0.7376948679783385,
   0.7801080118474064
  ],
  "raglog_tier0_detect_rate_at_5pct_fa": 0.4794871794871795,
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
  "ours_detect_rate_at_5pct_fa": 0.9384615384615385
 },
 "repair_baselines": {
  "Q04:symspell": {
   "fault": "Q04",
   "repair": "symspell (external)",
   "n": 50,
   "rescued": 22,
   "ci_lo": 0.3116198721023535
  },
  "Q05:wordsegment": {
   "fault": "Q05",
   "repair": "wordsegment (external)",
   "n": 50,
   "rescued": 49,
   "ci_lo": 0.8950431352816304
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
 "verdict": "NOT_ADOPTED",
 "clean_net_hit_change": 0.0022371364653243847,
 "guarantee": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 4.137151735350564e-05,
   "esci_rare": 0.7313338506672653,
   "shop": 1.77933851531753e-05
  },
  "calibration": {
   "esci_common": {
    "n": 2296,
    "losses_if_all_dispatched": 3
   },
   "esci_rare": {
    "n": 428,
    "losses_if_all_dispatched": 23
   },
   "shop": {
    "n": 202,
    "losses_if_all_dispatched": 0
   }
  },
  "heldout_clean_loss": 0.0,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0,
   "esci_rare": 0.0,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.86625,
  "L2": "PASS"
 },
 "policies": [
  {
   "policy": "tau_none_5pct_fpr",
   "mean_closure": 0.845,
   "mean_closure_grounded": 0.8472727272727273,
   "mean_family_attribution": 0.83875,
   "mean_group_attribution": 0.84,
   "mean_cost_faulted": 4.8025,
   "clean_dispatch_rate": 0.040268456375838924,
   "clean_mean_cost": 0.2214765100671141,
   "clean_loss": 0.0,
   "clean_net_hit_change": 0.0007457121551081282,
   "clean_loss_esci_common": 0.0,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "global_crc_0.005",
   "mean_closure": 0.8712500000000001,
   "mean_closure_grounded": 0.8763636363636365,
   "mean_family_attribution": 0.855,
   "mean_group_attribution": 0.85625,
   "mean_cost_faulted": 5.0249999999999995,
   "clean_dispatch_rate": 0.12080536912751678,
   "clean_mean_cost": 0.8098434004474273,
   "clean_loss": 0.0,
   "clean_net_hit_change": 0.0044742729306487695,
   "clean_loss_esci_common": 0.0,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.0025",
   "mean_closure": 0.74,
   "mean_closure_grounded": 0.7054545454545454,
   "mean_family_attribution": 0.74,
   "mean_group_attribution": 0.7462500000000001,
   "mean_cost_faulted": 4.6975,
   "clean_dispatch_rate": 0.5264727815063386,
   "clean_mean_cost": 2.9731543624161074,
   "clean_loss": 0.0,
   "clean_net_hit_change": 0.0022371364653243847,
   "clean_loss_esci_common": 0.0,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.005",
   "mean_closure": 0.86625,
   "mean_closure_grounded": 0.8727272727272727,
   "mean_family_attribution": 0.8687499999999999,
   "mean_group_attribution": 0.875,
   "mean_cost_faulted": 5.11125,
   "clean_dispatch_rate": 0.8881431767337807,
   "clean_mean_cost": 4.170022371364653,
   "clean_loss": 0.0,
   "clean_net_hit_change": 0.0022371364653243847,
   "clean_loss_esci_common": 0.0,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.01",
   "mean_closure": 0.8775,
   "mean_closure_grounded": 0.8854545454545455,
   "mean_family_attribution": 0.875,
   "mean_group_attribution": 0.88125,
   "mean_cost_faulted": 5.19375,
   "clean_dispatch_rate": 0.9052945563012678,
   "clean_mean_cost": 4.276659209545116,
   "clean_loss": 0.0,
   "clean_net_hit_change": 0.002982848620432513,
   "clean_loss_esci_common": 0.0,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.02",
   "mean_closure": 0.8825,
   "mean_closure_grounded": 0.889090909090909,
   "mean_family_attribution": 0.87875,
   "mean_group_attribution": 0.885,
   "mean_cost_faulted": 5.24,
   "clean_dispatch_rate": 0.9157345264727815,
   "clean_mean_cost": 4.337061894108874,
   "clean_loss": 0.0,
   "clean_net_hit_change": 0.0044742729306487695,
   "clean_loss_esci_common": 0.0,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "diagnosis_free_universal",
   "mean_closure": 0.76,
   "mean_closure_grounded": 0.8018181818181819,
   "mean_family_attribution": 0.0,
   "mean_group_attribution": 0.0,
   "mean_cost_faulted": 12.0,
   "clean_dispatch_rate": 1.0,
   "clean_mean_cost": 12.0,
   "clean_loss": 0.007457121551081283,
   "clean_net_hit_change": 0.006711409395973154,
   "clean_loss_esci_common": 0.004297994269340974,
   "clean_loss_esci_rare": 0.03977272727272727,
   "clean_loss_shop": 0.0
  }
 ],
 "natural": [
  {
   "arm": "N1",
   "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6116504854368932,
   "delta": 0.021844660194174758,
   "ci_lo": 0.012742718446601941,
   "ci_hi": 0.03155339805825243,
   "fixed": 47,
   "broken": 11,
   "verdict": "PASS",
   "dispatched": 0.9180825242718447,
   "mean_cost": 5.930825242718447
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
   "hit_after": 0.5940533980582524,
   "delta": 0.00424757281553398,
   "ci_lo": -0.0012135922330097086,
   "ci_hi": 0.009708737864077669,
   "fixed": 13,
   "broken": 6,
   "verdict": "INCONCLUSIVE",
   "dispatched": 0.8610436893203883
  },
  {
   "arm": "B1",
   "what": "baseline: K12 parent collapse always on (no detection)",
   "n": 1648,
   "hit_before": 0.5898058252427184,
   "hit_after": 0.6055825242718447,
   "delta": 0.015776699029126214,
   "ci_lo": 0.007281553398058253,
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
   "ci_lo": 0.014184397163120567,
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
  }
 ],
 "unseen_mean_closure": 0.456,
 "not_solved": [
  "Q03",
  "C2"
 ],
 "device": "cuda",
 "reranker": "BAAI/bge-reranker-large"
}
```

{
 "detector": "held-out one-vs-rest AUROC >= 0.70 (point estimate) AND >= 20 held-out positives",
 "repair": ">= 20 hard episodes AND Wilson 95% lower bound of rescue rate >= 0.50 AND <= 10% of clean successes lost when the repair is forced on them",
 "solved": "detector PASS and repair PASS",
 "targets": "ADOPTED if repairs PASS >= 24/28 AND detectors PASS >= 27/28, else NOT_ADOPTED",
 "AUROC_BAR": 0.7,
 "MIN_TEST_POS": 20,
 "RESCUE_BAR_LB": 0.5,
 "MIN_REPAIR_N": 20,
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
 "U1_BAR": 0.5
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
| C2      | N      | False      | FAIL       | PASS     | False    |

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
| Q01     |   1337 |        575 |              369 |    156 |     50 |           25 |          25 |            0 |        0.243 |
| Q02     |   1337 |        271 |                0 |    221 |     50 |           25 |          25 |            0 |        0.185 |
| Q03     |   1337 |        131 |               28 |     53 |     50 |           25 |          25 |            0 |        0.485 |
| Q04     |   1337 |        109 |                3 |     56 |     50 |           25 |          25 |           17 |        0.472 |
| Q05     |   1337 |        336 |               34 |    252 |     50 |           25 |          25 |            0 |        0.166 |
| Q07     |   1365 |       1026 |              605 |    371 |     50 |           25 |          25 |            0 |        0.119 |
| Q09     |   1337 |        183 |                0 |    133 |     50 |           25 |          25 |            0 |        0.273 |
| K03     |    922 |        390 |              271 |     69 |     50 |           25 |          25 |            0 |        0.42  |
| K04     |   1337 |         77 |                0 |     27 |     50 |           25 |          25 |            0 |        0.649 |
| K05     |   1337 |        130 |                0 |     80 |     50 |           25 |          25 |            0 |        0.385 |
| K06     |    847 |         57 |                0 |      7 |     50 |           25 |          25 |            0 |        0.877 |
| K07     |    248 |         63 |                0 |     13 |     50 |           25 |          25 |            0 |        0.794 |
| K08     |   1337 |         63 |                0 |     13 |     50 |           25 |          25 |            0 |        0.794 |
| K09     |    284 |         71 |                0 |     21 |     50 |           25 |          25 |            0 |        0.704 |
| R01     |   1337 |         91 |                0 |     41 |     50 |           25 |          25 |            0 |        0.549 |
| R03     |   1337 |        605 |                0 |    555 |     50 |           25 |          25 |            0 |        0.083 |
| R05     |   1337 |         81 |                0 |     31 |     50 |           25 |          25 |            0 |        0.617 |
| R06     |   1337 |         50 |                0 |      0 |     50 |           25 |          25 |            0 |        1     |
| R07     |   1337 |        178 |                0 |    128 |     50 |           25 |          25 |            0 |        0.281 |
| R10     |   1337 |        523 |                0 |    473 |     50 |           25 |          25 |            0 |        0.096 |
| R11     |   1337 |        608 |                0 |    558 |     50 |           25 |          25 |            0 |        0.082 |
| R13     |   1337 |        745 |                0 |    695 |     50 |           25 |          25 |            0 |        0.067 |
| R15     |   1337 |        427 |                0 |    377 |     50 |           25 |          25 |            0 |        0.117 |
| R19     |   1337 |        416 |                0 |    366 |     50 |           25 |          25 |            0 |        0.12  |
| R22     |   1337 |        507 |                0 |    457 |     50 |           25 |          25 |            0 |        0.099 |
| R23     |   1337 |        128 |                0 |     78 |     50 |           25 |          25 |            0 |        0.391 |
| R24     |   1337 |        130 |                0 |     80 |     50 |           25 |          25 |            0 |        0.385 |
| R25     |   1337 |        128 |                0 |     78 |     50 |           25 |          25 |            0 |        0.391 |
| R26     |   1337 |       2500 |             1190 |   1300 |     10 |            5 |           5 |            0 |        0.008 |
| K11     |    847 |         51 |                0 |      1 |     50 |           25 |          25 |            0 |        0.98  |
| K12     |   1337 |         96 |                0 |     46 |     50 |           25 |          25 |            0 |        0.521 |
| C2      |   1337 |         98 |               13 |     35 |     50 |           25 |          25 |            0 |        0.588 |

## Detector gates (AUROC bar 0.7, min test positives 20)

| fault   | detector                             |   n_pos_train |   n_pos_test |   n_neg_test |   auroc |   ci_lo |   ci_hi |   auroc_vs_clean | status   |
|:--------|:-------------------------------------|--------------:|-------------:|-------------:|--------:|--------:|--------:|-----------------:|:---------|
| Q01     | histgb_head                          |            25 |           25 |         2071 |  0.9975 |  0.9956 |  0.9991 |           0.9982 | PASS     |
| Q02     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  0.9998 |  1.0000 |           0.9999 | PASS     |
| Q03     | histgb_head                          |            25 |           25 |         2071 |  0.6914 |  0.5731 |  0.7994 |           0.7086 | FAIL     |
| Q04     | tier0_rule                           |            25 |           25 |         2071 |  0.9570 |  0.9001 |  0.9871 |           0.9639 | PASS     |
| Q05     | histgb_head                          |            25 |           25 |         2071 |  0.9939 |  0.9870 |  0.9988 |           0.9952 | PASS     |
| Q07     | histgb_head                          |            25 |           25 |         2071 |  0.9981 |  0.9957 |  0.9996 |           0.9991 | PASS     |
| Q09     | histgb_head                          |            25 |           25 |         2071 |  0.9994 |  0.9984 |  1.0000 |           0.9990 | PASS     |
| K03     | histgb_head                          |            25 |           25 |         2071 |  0.9999 |  0.9996 |  1.0000 |           1.0000 | PASS     |
| K04     | histgb_head                          |            25 |           25 |         2071 |  0.9095 |  0.8117 |  0.9808 |           0.9273 | PASS     |
| K05     | histgb_head                          |            25 |           25 |         2071 |  0.9991 |  0.9969 |  1.0000 |           0.9999 | PASS     |
| K06     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K07     | tier0_rule                           |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K08     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K09     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R01     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R03     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R05     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R06     | histgb_head                          |            25 |           25 |         2071 |  0.9501 |  0.9043 |  0.9879 |           0.9739 | PASS     |
| R07     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  0.9999 |  1.0000 |           1.0000 | PASS     |
| R10     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  0.9999 |  1.0000 |           1.0000 | PASS     |
| R11     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R13     | histgb_head                          |            25 |           25 |         2071 |  0.9981 |  0.9938 |  1.0000 |           0.9996 | PASS     |
| R15     | tier0_rule                           |            25 |           25 |         2071 |  0.9989 |  0.9974 |  1.0000 |           1.0000 | PASS     |
| R19     | histgb_head                          |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R22     | histgb_head                          |            25 |           25 |         2071 |  0.9269 |  0.8186 |  0.9998 |           0.9288 | PASS     |
| R23     | tier0_rule                           |            25 |           25 |         2071 |  0.9990 |  0.9976 |  1.0000 |           1.0000 | PASS     |
| R24     | histgb_head                          |            25 |           25 |         2071 |  0.9069 |  0.8032 |  0.9835 |           0.9214 | PASS     |
| R25     | tier0_rule                           |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R26     | tier0_rule                           |             5 |            5 |         2091 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | THIN     |
| K11     | tier0_rule                           |            25 |           25 |         2071 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K12     | histgb_head                          |            25 |           25 |         2071 |  0.9644 |  0.8835 |  1.0000 |           0.9674 | PASS     |
| C2      | tier0_rule(second factor-group mass) |            25 |           25 |         2096 |  0.6116 |  0.4656 |  0.7331 |         nan      | FAIL     |

## Repair gates (Wilson lower bound >= 0.5)

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost |   harm_rate | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|------------:|:---------|
| Q01     |       50 |        39 |         0.780 |   0.648 |   0.872 |        20 |            0 |       0.000 | PASS     |
| Q02     |       50 |        43 |         0.860 |   0.738 |   0.930 |        20 |            0 |       0.000 | PASS     |
| Q03     |       50 |         1 |         0.020 |   0.004 |   0.105 |        20 |            1 |       0.050 | FAIL     |
| Q04     |       50 |        34 |         0.680 |   0.542 |   0.792 |        20 |            0 |       0.000 | PASS     |
| Q05     |       50 |        48 |         0.960 |   0.865 |   0.989 |        20 |            0 |       0.000 | PASS     |
| Q07     |       50 |        44 |         0.880 |   0.762 |   0.944 |        20 |            0 |       0.000 | PASS     |
| Q09     |       50 |        42 |         0.840 |   0.715 |   0.917 |        20 |            0 |       0.000 | PASS     |
| K03     |       50 |        44 |         0.880 |   0.762 |   0.944 |        20 |            0 |       0.000 | PASS     |
| K04     |       50 |        43 |         0.860 |   0.738 |   0.930 |        20 |            0 |       0.000 | PASS     |
| K05     |       50 |        49 |         0.980 |   0.895 |   0.996 |        20 |            0 |       0.000 | PASS     |
| K06     |       50 |        49 |         0.980 |   0.895 |   0.996 |        20 |            0 |       0.000 | PASS     |
| K07     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K08     |       50 |        48 |         0.960 |   0.865 |   0.989 |        20 |            0 |       0.000 | PASS     |
| K09     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R01     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R03     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R05     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R06     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R07     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R10     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R11     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R13     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R15     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R19     |       50 |        49 |         0.980 |   0.895 |   0.996 |        20 |            0 |       0.000 | PASS     |
| R22     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R23     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R24     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R25     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R26     |       10 |        10 |         1.000 |   0.722 |   1.000 |        20 |            0 |       0.000 | THIN     |
| K11     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K12     |       50 |        46 |         0.920 |   0.812 |   0.968 |        20 |            0 |       0.000 | PASS     |
| C2      |       50 |        45 |         0.900 |   0.786 |   0.957 |         0 |            0 |       0.000 | PASS     |

## Dispatch policies (held-out)

| policy                   |   mean_closure |   mean_closure_grounded |   mean_family_attribution |   mean_group_attribution |   mean_cost_faulted |   clean_dispatch_rate |   clean_mean_cost |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop |
|:-------------------------|---------------:|------------------------:|--------------------------:|-------------------------:|--------------------:|----------------------:|------------------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|
| tau_none_5pct_fpr        |         0.8450 |                  0.8473 |                    0.8387 |                   0.8400 |              4.8025 |                0.0403 |            0.2215 |       0.0000 |                 0.0007 |                   0.0000 |                 0.0000 |            0.0000 |
| global_crc_0.005         |         0.8713 |                  0.8764 |                    0.8550 |                   0.8562 |              5.0250 |                0.1208 |            0.8098 |       0.0000 |                 0.0045 |                   0.0000 |                 0.0000 |            0.0000 |
| mondrian_crc_0.0025      |         0.7400 |                  0.7055 |                    0.7400 |                   0.7463 |              4.6975 |                0.5265 |            2.9732 |       0.0000 |                 0.0022 |                   0.0000 |                 0.0000 |            0.0000 |
| mondrian_crc_0.005       |         0.8662 |                  0.8727 |                    0.8687 |                   0.8750 |              5.1113 |                0.8881 |            4.1700 |       0.0000 |                 0.0022 |                   0.0000 |                 0.0000 |            0.0000 |
| mondrian_crc_0.01        |         0.8775 |                  0.8855 |                    0.8750 |                   0.8812 |              5.1937 |                0.9053 |            4.2767 |       0.0000 |                 0.0030 |                   0.0000 |                 0.0000 |            0.0000 |
| mondrian_crc_0.02        |         0.8825 |                  0.8891 |                    0.8788 |                   0.8850 |              5.2400 |                0.9157 |            4.3371 |       0.0000 |                 0.0045 |                   0.0000 |                 0.0000 |            0.0000 |
| diagnosis_free_universal |         0.7600 |                  0.8018 |                    0.0000 |                   0.0000 |             12.0000 |                1.0000 |           12.0000 |       0.0075 |                 0.0067 |                   0.0043 |                 0.0398 |            0.0000 |

## Loop gates (L1 do-no-harm on held-out clean, L2 mean closure, U1 unseen, N1 natural traffic)

```
{
 "GUARANTEE": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 4.137151735350564e-05,
   "esci_rare": 0.7313338506672653,
   "shop": 1.77933851531753e-05
  },
  "calibration": {
   "esci_common": {
    "n": 2296,
    "losses_if_all_dispatched": 3
   },
   "esci_rare": {
    "n": 428,
    "losses_if_all_dispatched": 23
   },
   "shop": {
    "n": 202,
    "losses_if_all_dispatched": 0
   }
  },
  "heldout_clean_loss": 0.0,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0,
   "esci_rare": 0.0,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.86625,
  "L2": "PASS"
 },
 "U1": {
  "mean_closure": 0.456,
  "mean_closure_without_fallback": 0.1984,
  "mean_closure_grounded": 0.475,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5898058252427184,
  "hit_after": 0.6116504854368932,
  "delta": 0.021844660194174758,
  "ci_lo": 0.012742718446601941,
  "ci_hi": 0.03155339805825243,
  "fixed": 47,
  "broken": 11,
  "verdict": "PASS",
  "dispatched": 0.9180825242718447,
  "mean_cost": 5.930825242718447
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

| method                                    |   auroc |   ci_lo |   ci_hi |
|:------------------------------------------|--------:|--------:|--------:|
| ours_1_minus_pNONE                        |  0.9766 |  0.9697 |  0.9830 |
| qpp_neg_nqc                               |  0.5927 |  0.5692 |  0.6184 |
| qpp_neg_wig                               |  0.5822 |  0.5551 |  0.6071 |
| neg_ce1                                   |  0.6771 |  0.6521 |  0.7000 |
| raglog_tier0_best_single_rag_rt_best_rank |  0.6461 |  0.6234 |  0.6696 |
| raglog_tier0_features_hgb                 |  0.7607 |  0.7377 |  0.7801 |

## External repair baselines (oracle-dispatched, injected held-out + train episodes)

| fault   | repair                 |   n |   rescued |   ci_lo |
|:--------|:-----------------------|----:|----------:|--------:|
| Q04     | symspell (external)    |  50 |        22 |   0.312 |
| Q05     | wordsegment (external) |  50 |        49 |   0.895 |

## Family repairs, oracle-dispatched

| fault   | family   |   n |   rescued |   rate |   ci_lo |
|:--------|:---------|----:|----------:|-------:|--------:|
| Q01     | QLEX     |  50 |        30 |  0.600 |   0.462 |
| Q03     | QLEX     |  50 |         1 |  0.020 |   0.004 |
| Q04     | QLEX     |  50 |        30 |  0.600 |   0.462 |
| Q05     | QLEX     |  50 |        43 |  0.860 |   0.738 |
| K04     | STALE    |  50 |        43 |  0.860 |   0.738 |
| R03     | ENC      |  50 |        50 |  1.000 |   0.929 |
| R07     | STALE    |  50 |        50 |  1.000 |   0.929 |
| R10     | ENC      |  50 |        50 |  1.000 |   0.929 |
| R11     | ENC      |  50 |        50 |  1.000 |   0.929 |

## Natural traffic (no injection, never-examined queries): deployed loop, components, baselines

| arm   | what                                                                            |    n |   hit_before |   hit_after |   delta |   ci_lo |   ci_hi |   fixed |   broken | verdict      |   dispatched |   mean_cost |
|:------|:--------------------------------------------------------------------------------|-----:|-------------:|------------:|--------:|--------:|--------:|--------:|---------:|:-------------|-------------:|------------:|
| N1    | DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds | 1648 |       0.5898 |      0.6117 |  0.0218 |  0.0127 |  0.0316 |      47 |       11 | PASS         |       0.9181 |      5.9308 |
| N1a   | component: natural rules only                                                   | 1648 |       0.5898 |      0.6117 |  0.0218 |  0.0140 |  0.0297 |      41 |        5 | PASS         |     nan      |    nan      |
| N1b   | component: classifier dispatch only                                             | 1648 |       0.5898 |      0.5941 |  0.0042 | -0.0012 |  0.0097 |      13 |        6 | INCONCLUSIVE |       0.8610 |    nan      |
| B1    | baseline: K12 parent collapse always on (no detection)                          | 1648 |       0.5898 |      0.6056 |  0.0158 |  0.0073 |  0.0243 |      37 |       11 | PASS         |     nan      |    nan      |
| B2    | baseline: diagnosis-free universal repair on every query (cost 12)              | 1648 |       0.5898 |      0.6086 |  0.0188 |  0.0073 |  0.0303 |      62 |       31 | PASS         |     nan      |    nan      |
| NA1   | natural misspelling: ours (QLEX, log-gated)                                     |  185 |       0.5730 |      0.5189 | -0.0541 | -0.1081 | -0.0054 |       7 |       17 | HARM         |     nan      |    nan      |
| NA1x  | natural misspelling: SymSpell lookup_compound (external)                        |  185 |       0.5730 |      0.4486 | -0.1243 | -0.1838 | -0.0649 |       5 |       28 | HARM         |     nan      |    nan      |
| NA2   | natural missing space: ours (QLEX)                                              |   47 |       0.5106 |      0.4681 | -0.0426 | -0.1489 |  0.0638 |       2 |        4 | INCONCLUSIVE |     nan      |    nan      |
| NA2x  | natural missing space: wordsegment (external)                                   |   47 |       0.5106 |      0.4894 | -0.0213 | -0.1277 |  0.0638 |       2 |        3 | INCONCLUSIVE |     nan      |    nan      |
| NA4   | natural duplicate in top-5: K05 collapse                                        |  141 |       0.5177 |      0.5816 |  0.0638 |  0.0142 |  0.1135 |      11 |        2 | PASS         |     nan      |    nan      |
| NA5   | natural chunk crowding: K12 parent collapse                                     |  607 |       0.6491 |      0.6919 |  0.0428 |  0.0247 |  0.0610 |      30 |        4 | PASS         |     nan      |    nan      |

## Unseen faults (leave-one-fault-out attributor)

| fault   | tier   | family   |   n_test |   flagged |   right_group |   closure |   closure_without_group_fallback |
|:--------|:-------|:---------|---------:|----------:|--------------:|----------:|---------------------------------:|
| Q01     | N      | QLEX     |       25 |     0.800 |         0.480 |     0.360 |                            0.320 |
| Q02     | M      | Q02      |       25 |     0.800 |         0.160 |     0.040 |                            0.000 |
| Q03     | M      | QLEX     |       25 |     0.080 |         0.040 |     0.040 |                            0.040 |
| Q04     | S      | QLEX     |       25 |     0.920 |         0.480 |     0.520 |                            0.520 |
| Q05     | M      | QLEX     |       25 |     0.760 |         0.480 |     0.400 |                            0.400 |
| Q07     | M      | Q07      |       25 |     0.320 |         0.040 |     0.000 |                            0.000 |
| Q09     | P      | Q09      |       25 |     0.280 |         0.080 |     0.040 |                            0.000 |
| K03     | N      | K03      |       25 |     1.000 |         0.960 |     0.160 |                            0.080 |
| K04     | M      | STALE    |       25 |     0.560 |         0.000 |     0.520 |                            0.320 |
| K05     | S      | K05      |       25 |     1.000 |         1.000 |     1.000 |                            0.000 |
| K06     | N      | K06      |       25 |     1.000 |         1.000 |     0.080 |                            0.000 |
| K08     | M      | K08      |       25 |     0.880 |         0.840 |     0.360 |                            0.080 |
| K09     | M      | K09      |       25 |     0.760 |         0.720 |     0.760 |                            0.000 |
| R01     | S      | R01      |       25 |     0.520 |         0.280 |     0.360 |                            0.000 |
| R03     | N      | ENC      |       25 |     1.000 |         0.840 |     0.880 |                            0.080 |
| R05     | N      | R05      |       25 |     0.560 |         0.480 |     0.240 |                            0.000 |
| R06     | P      | R06      |       25 |     0.880 |         0.480 |     0.040 |                            0.000 |
| R07     | P      | STALE    |       25 |     1.000 |         0.040 |     1.000 |                            0.960 |
| R10     | N      | ENC      |       25 |     1.000 |         1.000 |     1.000 |                            1.000 |
| R11     | S      | ENC      |       25 |     1.000 |         1.000 |     1.000 |                            1.000 |
| R13     | M      | R13      |       25 |     0.920 |         0.760 |     0.720 |                            0.000 |
| R19     | S      | R19      |       25 |     0.720 |         0.560 |     0.440 |                            0.040 |
| R22     | S      | R22      |       25 |     0.440 |         0.200 |     0.400 |                            0.080 |
| R24     | M      | R24      |       25 |     0.520 |         0.280 |     0.440 |                            0.000 |
| K12     | S      | K12      |       25 |     0.800 |         0.760 |     0.600 |                            0.040 |

## Closed loop per fault and policy (held-out split)

| policy                   | fault   | tier   |   n_test |   dispatch_rate |   family_attribution |   group_attribution |   mean_cost |   closure |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop |
|:-------------------------|:--------|:-------|---------:|----------------:|---------------------:|--------------------:|------------:|----------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|
| tau_none_5pct_fpr        | Q01     | N      |       25 |           0.920 |                0.840 |               0.840 |       1.560 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q03     | M      |       25 |           0.040 |                0.040 |               0.040 |       0.040 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q04     | S      |       25 |           0.880 |                0.760 |               0.760 |       1.840 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q05     | M      |       25 |           0.840 |                0.680 |               0.680 |       2.120 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q07     | M      |       25 |           0.880 |                0.840 |               0.840 |       1.200 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K03     | N      |       25 |           1.000 |                0.840 |               0.840 |       4.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K04     | M      |       25 |           0.840 |                0.800 |               0.800 |       2.760 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K05     | S      |       25 |           1.000 |                0.920 |               0.920 |       3.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K06     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K08     | M      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R01     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R05     | N      |       25 |           0.960 |                0.960 |               0.960 |       7.680 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R06     | P      |       25 |           0.680 |                0.640 |               0.640 |       5.480 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R07     | P      |       25 |           0.960 |                0.880 |               0.840 |       7.560 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R10     | N      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R13     | M      |       25 |           0.920 |                0.880 |               0.880 |       7.400 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R15     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R19     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R22     | S      |       25 |           0.720 |                0.680 |               0.680 |       5.800 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R23     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R24     | M      |       25 |           0.520 |                0.320 |               0.320 |       3.800 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R26     | S      |        5 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K12     | S      |       25 |           0.920 |                0.920 |               0.920 |       2.760 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | C2      | N      |       25 |           0.960 |                0.280 |               0.360 |       6.600 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | NONE    | -      |     1341 |           0.040 |                0.960 |               0.960 |       0.221 |   nan     |        0.000 |                  0.001 |                    0.000 |                  0.000 |             0.000 |
| global_crc_0.005         | Q01     | N      |       25 |           1.000 |                0.920 |               0.920 |       1.640 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q03     | M      |       25 |           0.080 |                0.040 |               0.040 |       0.360 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q04     | S      |       25 |           0.960 |                0.800 |               0.800 |       2.240 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q05     | M      |       25 |           0.960 |                0.800 |               0.800 |       2.240 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q07     | M      |       25 |           1.000 |                0.840 |               0.840 |       2.280 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K03     | N      |       25 |           1.000 |                0.840 |               0.840 |       4.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K04     | M      |       25 |           0.880 |                0.800 |               0.800 |       2.800 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K05     | S      |       25 |           1.000 |                0.920 |               0.920 |       3.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K06     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K08     | M      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R01     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R05     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R06     | P      |       25 |           0.760 |                0.680 |               0.680 |       6.160 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R07     | P      |       25 |           1.000 |                0.880 |               0.840 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R10     | N      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R13     | M      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R15     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R19     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R22     | S      |       25 |           0.800 |                0.760 |               0.760 |       6.440 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R23     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R24     | M      |       25 |           0.720 |                0.360 |               0.360 |       5.720 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R26     | S      |        5 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K12     | S      |       25 |           0.960 |                0.920 |               0.920 |       3.200 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | C2      | N      |       25 |           0.960 |                0.280 |               0.360 |       6.600 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | NONE    | -      |     1341 |           0.121 |                0.879 |               0.879 |       0.810 |   nan     |        0.000 |                  0.004 |                    0.000 |                  0.000 |             0.000 |
| mondrian_crc_0.0025      | Q01     | N      |       25 |           0.840 |                0.800 |               0.800 |       1.160 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q03     | M      |       25 |           1.000 |                0.680 |               0.680 |       3.240 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q04     | S      |       25 |           0.440 |                0.400 |               0.400 |       0.760 |     0.200 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q05     | M      |       25 |           0.400 |                0.360 |               0.360 |       0.720 |     0.360 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q07     | M      |       25 |           0.040 |                0.040 |               0.040 |       0.040 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q09     | P      |       25 |           0.960 |                0.920 |               0.920 |       1.280 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K03     | N      |       25 |           1.000 |                0.840 |               0.840 |       4.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K04     | M      |       25 |           0.920 |                0.800 |               0.800 |       2.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K05     | S      |       25 |           1.000 |                0.920 |               0.920 |       3.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K06     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K07     | S      |       25 |           0.000 |                0.000 |               0.000 |       0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K08     | M      |       25 |           0.960 |                0.920 |               0.920 |       2.920 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K09     | M      |       25 |           0.000 |                0.000 |               0.000 |       0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R01     | S      |       25 |           0.840 |                0.800 |               0.800 |       6.760 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R05     | N      |       25 |           0.760 |                0.760 |               0.760 |       6.080 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R06     | P      |       25 |           0.920 |                0.640 |               0.680 |       6.960 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R07     | P      |       25 |           1.000 |                0.880 |               0.840 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R10     | N      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R13     | M      |       25 |           0.960 |                0.920 |               0.920 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R15     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R19     | S      |       25 |           0.920 |                0.880 |               0.880 |       7.400 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R22     | S      |       25 |           0.960 |                0.800 |               0.800 |       6.880 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R23     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R24     | M      |       25 |           0.880 |                0.480 |               0.560 |       7.280 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R26     | S      |        5 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K12     | S      |       25 |           0.920 |                0.840 |               0.880 |       3.080 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | C2      | N      |       25 |           0.920 |                0.280 |               0.360 |       6.560 |     0.560 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | NONE    | -      |     1341 |           0.526 |                0.474 |               0.474 |       2.973 |   nan     |        0.000 |                  0.002 |                    0.000 |                  0.000 |             0.000 |
| mondrian_crc_0.005       | Q01     | N      |       25 |           0.920 |                0.840 |               0.840 |       1.560 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q03     | M      |       25 |           1.000 |                0.680 |               0.680 |       3.240 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q04     | S      |       25 |           0.840 |                0.720 |               0.720 |       1.800 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q05     | M      |       25 |           0.760 |                0.680 |               0.680 |       1.400 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q07     | M      |       25 |           0.840 |                0.840 |               0.840 |       0.840 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K03     | N      |       25 |           1.000 |                0.840 |               0.840 |       4.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K04     | M      |       25 |           0.920 |                0.800 |               0.800 |       2.840 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K05     | S      |       25 |           1.000 |                0.920 |               0.920 |       3.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K06     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K08     | M      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R01     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R05     | N      |       25 |           0.920 |                0.920 |               0.920 |       7.360 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R06     | P      |       25 |           0.960 |                0.680 |               0.720 |       7.280 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R07     | P      |       25 |           1.000 |                0.880 |               0.840 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R10     | N      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R13     | M      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R15     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R19     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R22     | S      |       25 |           0.960 |                0.800 |               0.800 |       6.880 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R23     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R24     | M      |       25 |           0.920 |                0.480 |               0.560 |       7.320 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R26     | S      |        5 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K12     | S      |       25 |           1.000 |                0.920 |               0.960 |       3.320 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | C2      | N      |       25 |           0.960 |                0.280 |               0.360 |       6.600 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | NONE    | -      |     1341 |           0.888 |                0.112 |               0.112 |       4.170 |   nan     |        0.000 |                  0.002 |                    0.000 |                  0.000 |             0.000 |
| mondrian_crc_0.01        | Q01     | N      |       25 |           0.960 |                0.880 |               0.880 |       1.600 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q03     | M      |       25 |           1.000 |                0.680 |               0.680 |       3.240 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q04     | S      |       25 |           0.880 |                0.760 |               0.760 |       1.840 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q05     | M      |       25 |           0.880 |                0.720 |               0.720 |       2.160 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q07     | M      |       25 |           0.920 |                0.840 |               0.840 |       1.560 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K03     | N      |       25 |           1.000 |                0.840 |               0.840 |       4.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K04     | M      |       25 |           1.000 |                0.800 |               0.800 |       3.240 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K05     | S      |       25 |           1.000 |                0.920 |               0.920 |       3.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K06     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K08     | M      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R01     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R05     | N      |       25 |           0.960 |                0.960 |               0.960 |       7.680 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R06     | P      |       25 |           0.960 |                0.680 |               0.720 |       7.280 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R07     | P      |       25 |           1.000 |                0.880 |               0.840 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R10     | N      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R13     | M      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R15     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R19     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R22     | S      |       25 |           1.000 |                0.840 |               0.840 |       7.200 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R23     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R24     | M      |       25 |           0.920 |                0.480 |               0.560 |       7.320 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R26     | S      |        5 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K12     | S      |       25 |           1.000 |                0.920 |               0.960 |       3.320 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | C2      | N      |       25 |           1.000 |                0.280 |               0.360 |       6.640 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | NONE    | -      |     1341 |           0.905 |                0.095 |               0.095 |       4.277 |   nan     |        0.000 |                  0.003 |                    0.000 |                  0.000 |             0.000 |
| mondrian_crc_0.02        | Q01     | N      |       25 |           1.000 |                0.920 |               0.920 |       1.640 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q03     | M      |       25 |           1.000 |                0.680 |               0.680 |       3.240 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q04     | S      |       25 |           0.920 |                0.760 |               0.760 |       2.200 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q05     | M      |       25 |           0.920 |                0.760 |               0.760 |       2.200 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q07     | M      |       25 |           1.000 |                0.840 |               0.840 |       2.280 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K03     | N      |       25 |           1.000 |                0.840 |               0.840 |       4.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K04     | M      |       25 |           1.000 |                0.800 |               0.800 |       3.240 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K05     | S      |       25 |           1.000 |                0.920 |               0.920 |       3.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K06     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K08     | M      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R01     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R05     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R06     | P      |       25 |           0.960 |                0.680 |               0.720 |       7.280 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R07     | P      |       25 |           1.000 |                0.880 |               0.840 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R10     | N      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R13     | M      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R15     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R19     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R22     | S      |       25 |           1.000 |                0.840 |               0.840 |       7.200 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R23     | S      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R24     | M      |       25 |           0.920 |                0.480 |               0.560 |       7.320 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R26     | S      |        5 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K12     | S      |       25 |           1.000 |                0.920 |               0.960 |       3.320 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | C2      | N      |       25 |           1.000 |                0.280 |               0.360 |       6.640 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | NONE    | -      |     1341 |           0.916 |                0.084 |               0.084 |       4.337 |   nan     |        0.000 |                  0.004 |                    0.000 |                  0.000 |             0.000 |
| diagnosis_free_universal | Q01     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q02     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.160 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q03     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q04     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q05     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q07     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q09     | P      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.160 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K03     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.280 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K04     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K05     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K06     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.200 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K07     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K08     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K09     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R01     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R03     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R05     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R06     | P      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R07     | P      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R10     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R11     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R13     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R15     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R19     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R22     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R23     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R24     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R25     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R26     | S      |        5 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K11     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K12     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | C2      | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | NONE    | -      |     1341 |           1.000 |                0.000 |               0.000 |      12.000 |   nan     |        0.007 |                  0.007 |                    0.004 |                  0.040 |             0.000 |
