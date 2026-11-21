# DiagRAG v4 judged run report

Device: cpu. Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2. Last session runtime: 429s.

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
   "n": 50,
   "rescued": 33,
   "rate": 0.66,
   "ci_lo": 0.5215356854148286
  },
  {
   "fault": "Q03",
   "family": "QLEX",
   "n": 50,
   "rescued": 3,
   "rate": 0.06,
   "ci_lo": 0.02061459636463048
  },
  {
   "fault": "Q04",
   "family": "QLEX",
   "n": 50,
   "rescued": 29,
   "rate": 0.58,
   "ci_lo": 0.4423319668777783
  },
  {
   "fault": "Q05",
   "family": "QLEX",
   "n": 50,
   "rescued": 42,
   "rate": 0.84,
   "ci_lo": 0.7148551903823401
  },
  {
   "fault": "K04",
   "family": "STALE",
   "n": 50,
   "rescued": 46,
   "rate": 0.92,
   "ci_lo": 0.811614974549363
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
 "U1": {
  "mean_closure": 0.48479999999999995,
  "mean_closure_without_fallback": 0.26080000000000003,
  "mean_closure_grounded": 0.45499999999999996,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5782766990291263,
  "hit_after": 0.6013349514563107,
  "delta": 0.023058252427184466,
  "ci_lo": 0.01516990291262136,
  "ci_hi": 0.03155339805825243,
  "fixed": 43,
  "broken": 5,
  "verdict": "PASS",
  "dispatched": 0.9047330097087378,
  "mean_cost": 5.852548543689321
 },
 "detection_baselines": {
  "ours_1_minus_pNONE": [
   0.9795918655397662,
   0.9743461583475062,
   0.9851679794014491
  ],
  "qpp_neg_nqc": [
   0.5824667039289082,
   0.5582932845084236,
   0.6086668110949482
  ],
  "qpp_neg_wig": [
   0.5761532946031853,
   0.5525493209335078,
   0.6023201136259333
  ],
  "neg_ce1": [
   0.6837555446403535,
   0.6596548177616827,
   0.7072694052455581
  ],
  "raglog_tier0_best_single_rag_rt_best_rank": [
   0.6594791002109645,
   0.6382144667573542,
   0.6798848153281091
  ],
  "raglog_tier0_features_hgb": [
   0.7774879603439417,
   0.7574167374277506,
   0.7974559123453397
  ],
  "raglog_tier0_detect_rate_at_5pct_fa": 0.49872122762148335,
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
  "ours_detect_rate_at_5pct_fa": 0.9424552429667519
 },
 "repair_baselines": {
  "Q04:symspell": {
   "fault": "Q04",
   "repair": "symspell (external)",
   "n": 50,
   "rescued": 33,
   "ci_lo": 0.5215356854148286
  },
  "Q05:wordsegment": {
   "fault": "Q05",
   "repair": "wordsegment (external)",
   "n": 50,
   "rescued": 48,
   "ci_lo": 0.8653966212204532
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
 "clean_net_hit_change": -0.0007358351729212656,
 "guarantee": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 4.396426881292381e-05,
   "esci_rare": 0.9649816687696321,
   "shop": 3.719494187037764e-05
  },
  "calibration": {
   "esci_common": {
    "n": 2322,
    "losses_if_all_dispatched": 3
   },
   "esci_rare": {
    "n": 417,
    "losses_if_all_dispatched": 16
   },
   "shop": {
    "n": 202,
    "losses_if_all_dispatched": 0
   }
  },
  "heldout_clean_loss": 0.003679175864606328,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.006925207756232687,
   "esci_rare": 0.0,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.83,
  "L2": "PASS"
 },
 "policies": [
  {
   "policy": "tau_none_5pct_fpr",
   "mean_closure": 0.8499999999999999,
   "mean_closure_grounded": 0.8436363636363637,
   "mean_family_attribution": 0.8325,
   "mean_group_attribution": 0.8362499999999999,
   "mean_cost_faulted": 4.922499999999999,
   "clean_dispatch_rate": 0.036055923473142015,
   "clean_mean_cost": 0.1861662987490802,
   "clean_loss": 0.0007358351729212656,
   "clean_net_hit_change": 0.002207505518763797,
   "clean_loss_esci_common": 0.0013850415512465374,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "global_crc_0.005",
   "mean_closure": 0.87625,
   "mean_closure_grounded": 0.8745454545454545,
   "mean_family_attribution": 0.845,
   "mean_group_attribution": 0.85,
   "mean_cost_faulted": 5.1675,
   "clean_dispatch_rate": 0.12214863870493009,
   "clean_mean_cost": 0.7829286239882266,
   "clean_loss": 0.002207505518763797,
   "clean_net_hit_change": 0.0051508462104488595,
   "clean_loss_esci_common": 0.0013850415512465374,
   "clean_loss_esci_rare": 0.011764705882352941,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.0025",
   "mean_closure": 0.69,
   "mean_closure_grounded": 0.6636363636363636,
   "mean_family_attribution": 0.69,
   "mean_group_attribution": 0.6925,
   "mean_cost_faulted": 4.455,
   "clean_dispatch_rate": 0.5320088300220751,
   "clean_mean_cost": 2.746872700515085,
   "clean_loss": 0.003679175864606328,
   "clean_net_hit_change": -0.0007358351729212656,
   "clean_loss_esci_common": 0.006925207756232687,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.005",
   "mean_closure": 0.83,
   "mean_closure_grounded": 0.8236363636363635,
   "mean_family_attribution": 0.8300000000000001,
   "mean_group_attribution": 0.83125,
   "mean_cost_faulted": 4.97875,
   "clean_dispatch_rate": 0.8763796909492274,
   "clean_mean_cost": 3.6497424576894777,
   "clean_loss": 0.003679175864606328,
   "clean_net_hit_change": -0.0007358351729212656,
   "clean_loss_esci_common": 0.006925207756232687,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.01",
   "mean_closure": 0.8775,
   "mean_closure_grounded": 0.869090909090909,
   "mean_family_attribution": 0.86375,
   "mean_group_attribution": 0.8674999999999999,
   "mean_cost_faulted": 5.24,
   "clean_dispatch_rate": 0.8940397350993378,
   "clean_mean_cost": 3.739514348785872,
   "clean_loss": 0.003679175864606328,
   "clean_net_hit_change": 0.0014716703458425313,
   "clean_loss_esci_common": 0.006925207756232687,
   "clean_loss_esci_rare": 0.0,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.02",
   "mean_closure": 0.8837499999999999,
   "mean_closure_grounded": 0.8763636363636365,
   "mean_family_attribution": 0.86875,
   "mean_group_attribution": 0.87375,
   "mean_cost_faulted": 5.32125,
   "clean_dispatch_rate": 0.9146431199411332,
   "clean_mean_cost": 3.8852097130242824,
   "clean_loss": 0.004415011037527594,
   "clean_net_hit_change": 0.0014716703458425313,
   "clean_loss_esci_common": 0.006925207756232687,
   "clean_loss_esci_rare": 0.0058823529411764705,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "diagnosis_free_universal",
   "mean_closure": 0.7562500000000001,
   "mean_closure_grounded": 0.7872727272727272,
   "mean_family_attribution": 0.0,
   "mean_group_attribution": 0.0,
   "mean_cost_faulted": 12.0,
   "clean_dispatch_rate": 1.0,
   "clean_mean_cost": 12.0,
   "clean_loss": 0.013245033112582781,
   "clean_net_hit_change": 0.017660044150110375,
   "clean_loss_esci_common": 0.015235457063711912,
   "clean_loss_esci_rare": 0.041176470588235294,
   "clean_loss_shop": 0.0
  }
 ],
 "natural": [
  {
   "arm": "N1",
   "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
   "n": 1648,
   "hit_before": 0.5782766990291263,
   "hit_after": 0.6013349514563107,
   "delta": 0.023058252427184466,
   "ci_lo": 0.01516990291262136,
   "ci_hi": 0.03155339805825243,
   "fixed": 43,
   "broken": 5,
   "verdict": "PASS",
   "dispatched": 0.9047330097087378,
   "mean_cost": 5.852548543689321
  },
  {
   "arm": "N1a",
   "what": "component: natural rules only",
   "n": 1648,
   "hit_before": 0.5782766990291263,
   "hit_after": 0.6025485436893204,
   "delta": 0.024271844660194174,
   "ci_lo": 0.01699029126213592,
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
   "hit_after": 0.5807038834951457,
   "delta": 0.0024271844660194173,
   "ci_lo": -0.0012135922330097086,
   "ci_hi": 0.006674757281553398,
   "fixed": 8,
   "broken": 4,
   "verdict": "INCONCLUSIVE",
   "dispatched": 0.837378640776699
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
   "ci_lo": 0.010922330097087379,
   "ci_hi": 0.03337378640776699,
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
   "ci_lo": -0.10810810810810811,
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
   "ci_lo": -0.1837837837837838,
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
   "ci_hi": 0.1276595744680851,
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
  }
 ],
 "unseen_mean_closure": 0.48479999999999995,
 "not_solved": [
  "Q03"
 ],
 "device": "cpu",
 "reranker": "cross-encoder/ms-marco-MiniLM-L-6-v2"
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
| Q01     |   1309 |        394 |              265 |     79 |     50 |           25 |          25 |            0 |        0.388 |
| Q02     |   1309 |        312 |                0 |    262 |     50 |           25 |          25 |            0 |        0.16  |
| Q03     |   1309 |        132 |               37 |     45 |     50 |           25 |          25 |            0 |        0.526 |
| Q04     |   1309 |         86 |                4 |     32 |     50 |           25 |          25 |           20 |        0.61  |
| Q05     |   1309 |        251 |               25 |    176 |     50 |           25 |          25 |            0 |        0.221 |
| Q07     |   1351 |        963 |              582 |    331 |     50 |           25 |          25 |            0 |        0.131 |
| Q09     |   1309 |        162 |                1 |    111 |     50 |           25 |          25 |            0 |        0.311 |
| K03     |    910 |        186 |              134 |      2 |     50 |           25 |          25 |            0 |        0.962 |
| K04     |   1309 |         76 |                0 |     26 |     50 |           25 |          25 |            0 |        0.658 |
| K05     |   1309 |        150 |                0 |    100 |     50 |           25 |          25 |            0 |        0.333 |
| K06     |    831 |         53 |                0 |      3 |     50 |           25 |          25 |            0 |        0.943 |
| K07     |    246 |         74 |                0 |     24 |     50 |           25 |          25 |            0 |        0.676 |
| K08     |   1309 |         65 |                0 |     15 |     50 |           25 |          25 |            0 |        0.769 |
| K09     |    282 |         53 |                0 |      3 |     50 |           25 |          25 |            0 |        0.943 |
| R01     |   1309 |         80 |                0 |     30 |     50 |           25 |          25 |            0 |        0.625 |
| R03     |   1309 |        867 |                0 |    817 |     50 |           25 |          25 |            0 |        0.058 |
| R05     |   1309 |         74 |                0 |     24 |     50 |           25 |          25 |            0 |        0.676 |
| R06     |   1309 |         50 |                0 |      0 |     50 |           25 |          25 |            0 |        1     |
| R07     |   1309 |        186 |                0 |    136 |     50 |           25 |          25 |            0 |        0.269 |
| R10     |   1309 |        590 |                0 |    540 |     50 |           25 |          25 |            0 |        0.085 |
| R11     |   1309 |        637 |                0 |    587 |     50 |           25 |          25 |            0 |        0.078 |
| R13     |   1309 |        997 |                0 |    947 |     50 |           25 |          25 |            0 |        0.05  |
| R15     |   1309 |        433 |                0 |    383 |     50 |           25 |          25 |            0 |        0.115 |
| R19     |   1309 |        402 |                0 |    352 |     50 |           25 |          25 |            0 |        0.124 |
| R22     |   1309 |        757 |                0 |    707 |     50 |           25 |          25 |            0 |        0.066 |
| R23     |   1309 |        145 |                0 |     95 |     50 |           25 |          25 |            0 |        0.345 |
| R24     |   1309 |        123 |                0 |     73 |     50 |           25 |          25 |            0 |        0.407 |
| R25     |   1309 |        148 |                0 |     98 |     50 |           25 |          25 |            0 |        0.338 |
| R26     |   1309 |       2500 |             1207 |   1280 |     12 |            5 |           7 |            0 |        0.009 |
| K11     |    831 |         50 |                0 |      0 |     50 |           25 |          25 |            0 |        1     |
| K12     |   1309 |         80 |                0 |     30 |     50 |           25 |          25 |            0 |        0.625 |
| C2      |   1309 |        101 |               12 |     39 |     50 |           25 |          25 |            0 |        0.562 |

## Detector gates (AUROC bar 0.7, min test positives 20)

| fault   | detector                             |   n_pos_train |   n_pos_test |   n_neg_test |   auroc |   ci_lo |   ci_hi |   auroc_vs_clean | status   |
|:--------|:-------------------------------------|--------------:|-------------:|-------------:|--------:|--------:|--------:|-----------------:|:---------|
| Q01     | histgb_head                          |            25 |           25 |         2091 |  0.9981 |  0.9962 |  0.9996 |           0.9984 | PASS     |
| Q02     | histgb_head                          |            25 |           25 |         2091 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| Q03     | histgb_head                          |            25 |           25 |         2091 |  0.7043 |  0.5839 |  0.8226 |           0.7275 | PASS     |
| Q04     | tier0_rule                           |            25 |           25 |         2091 |  0.9832 |  0.9727 |  0.9919 |           0.9873 | PASS     |
| Q05     | histgb_head                          |            25 |           25 |         2091 |  0.9921 |  0.9869 |  0.9964 |           0.9949 | PASS     |
| Q07     | histgb_head                          |            25 |           25 |         2091 |  1.0000 |  0.9998 |  1.0000 |           1.0000 | PASS     |
| Q09     | histgb_head                          |            25 |           25 |         2091 |  0.9993 |  0.9983 |  1.0000 |           0.9993 | PASS     |
| K03     | histgb_head                          |            25 |           25 |         2091 |  1.0000 |  0.9998 |  1.0000 |           1.0000 | PASS     |
| K04     | histgb_head                          |            25 |           25 |         2091 |  0.7673 |  0.6143 |  0.9197 |           0.7700 | PASS     |
| K05     | histgb_head                          |            25 |           25 |         2091 |  0.9999 |  0.9995 |  1.0000 |           0.9999 | PASS     |
| K06     | histgb_head                          |            25 |           25 |         2091 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K07     | tier0_rule                           |            25 |           25 |         2091 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K08     | histgb_head                          |            25 |           25 |         2091 |  0.9922 |  0.9758 |  1.0000 |           0.9937 | PASS     |
| K09     | histgb_head                          |            25 |           25 |         2091 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R01     | histgb_head                          |            25 |           25 |         2091 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R03     | histgb_head                          |            25 |           25 |         2091 |  0.9998 |  0.9995 |  1.0000 |           1.0000 | PASS     |
| R05     | histgb_head                          |            25 |           25 |         2091 |  0.9989 |  0.9975 |  0.9997 |           0.9995 | PASS     |
| R06     | histgb_head                          |            25 |           25 |         2091 |  0.9862 |  0.9635 |  0.9990 |           0.9928 | PASS     |
| R07     | histgb_head                          |            25 |           25 |         2091 |  1.0000 |  0.9999 |  1.0000 |           1.0000 | PASS     |
| R10     | histgb_head                          |            25 |           25 |         2091 |  0.9798 |  0.9369 |  1.0000 |           0.9800 | PASS     |
| R11     | histgb_head                          |            25 |           25 |         2091 |  0.9998 |  0.9993 |  1.0000 |           1.0000 | PASS     |
| R13     | histgb_head                          |            25 |           25 |         2091 |  0.9977 |  0.9925 |  1.0000 |           0.9996 | PASS     |
| R15     | tier0_rule                           |            25 |           25 |         2091 |  0.9982 |  0.9964 |  0.9995 |           1.0000 | PASS     |
| R19     | histgb_head                          |            25 |           25 |         2091 |  0.9998 |  0.9993 |  1.0000 |           1.0000 | PASS     |
| R22     | histgb_head                          |            25 |           25 |         2091 |  0.9101 |  0.8110 |  0.9877 |           0.9162 | PASS     |
| R23     | tier0_rule                           |            25 |           25 |         2091 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R24     | histgb_head                          |            25 |           25 |         2091 |  0.9968 |  0.9933 |  0.9996 |           0.9980 | PASS     |
| R25     | tier0_rule                           |            25 |           25 |         2091 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R26     | tier0_rule                           |             5 |            7 |         2109 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | THIN     |
| K11     | tier0_rule                           |            25 |           25 |         2091 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K12     | histgb_head                          |            25 |           25 |         2091 |  0.9994 |  0.9985 |  1.0000 |           0.9992 | PASS     |
| C2      | tier0_rule(second factor-group mass) |            25 |           25 |         2116 |  0.9156 |  0.8578 |  0.9618 |         nan      | PASS     |

## Repair gates (Wilson lower bound >= 0.5)

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost |   harm_rate | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|------------:|:---------|
| Q01     |       50 |        40 |         0.800 |   0.670 |   0.888 |        20 |            0 |       0.000 | PASS     |
| Q02     |       50 |        45 |         0.900 |   0.786 |   0.957 |        20 |            0 |       0.000 | PASS     |
| Q03     |       50 |         1 |         0.020 |   0.004 |   0.105 |        20 |            2 |       0.100 | FAIL     |
| Q04     |       50 |        34 |         0.680 |   0.542 |   0.792 |        20 |            0 |       0.000 | PASS     |
| Q05     |       50 |        44 |         0.880 |   0.762 |   0.944 |        20 |            0 |       0.000 | PASS     |
| Q07     |       50 |        42 |         0.840 |   0.715 |   0.917 |        20 |            0 |       0.000 | PASS     |
| Q09     |       50 |        40 |         0.800 |   0.670 |   0.888 |        20 |            0 |       0.000 | PASS     |
| K03     |       50 |        45 |         0.900 |   0.786 |   0.957 |        20 |            0 |       0.000 | PASS     |
| K04     |       50 |        46 |         0.920 |   0.812 |   0.968 |        20 |            0 |       0.000 | PASS     |
| K05     |       50 |        49 |         0.980 |   0.895 |   0.996 |        20 |            0 |       0.000 | PASS     |
| K06     |       50 |        49 |         0.980 |   0.895 |   0.996 |        20 |            0 |       0.000 | PASS     |
| K07     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K08     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
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
| R19     |       50 |        47 |         0.940 |   0.838 |   0.979 |        20 |            1 |       0.050 | PASS     |
| R22     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R23     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R24     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R25     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R26     |       12 |        12 |         1.000 |   0.757 |   1.000 |        20 |            0 |       0.000 | THIN     |
| K11     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K12     |       50 |        48 |         0.960 |   0.865 |   0.989 |        20 |            0 |       0.000 | PASS     |
| C2      |       50 |        41 |         0.820 |   0.692 |   0.902 |         0 |            0 |       0.000 | PASS     |

## Dispatch policies (held-out)

| policy                   |   mean_closure |   mean_closure_grounded |   mean_family_attribution |   mean_group_attribution |   mean_cost_faulted |   clean_dispatch_rate |   clean_mean_cost |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop |
|:-------------------------|---------------:|------------------------:|--------------------------:|-------------------------:|--------------------:|----------------------:|------------------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|
| tau_none_5pct_fpr        |         0.8500 |                  0.8436 |                    0.8325 |                   0.8362 |              4.9225 |                0.0361 |            0.1862 |       0.0007 |                 0.0022 |                   0.0014 |                 0.0000 |            0.0000 |
| global_crc_0.005         |         0.8762 |                  0.8745 |                    0.8450 |                   0.8500 |              5.1675 |                0.1221 |            0.7829 |       0.0022 |                 0.0052 |                   0.0014 |                 0.0118 |            0.0000 |
| mondrian_crc_0.0025      |         0.6900 |                  0.6636 |                    0.6900 |                   0.6925 |              4.4550 |                0.5320 |            2.7469 |       0.0037 |                -0.0007 |                   0.0069 |                 0.0000 |            0.0000 |
| mondrian_crc_0.005       |         0.8300 |                  0.8236 |                    0.8300 |                   0.8313 |              4.9787 |                0.8764 |            3.6497 |       0.0037 |                -0.0007 |                   0.0069 |                 0.0000 |            0.0000 |
| mondrian_crc_0.01        |         0.8775 |                  0.8691 |                    0.8638 |                   0.8675 |              5.2400 |                0.8940 |            3.7395 |       0.0037 |                 0.0015 |                   0.0069 |                 0.0000 |            0.0000 |
| mondrian_crc_0.02        |         0.8837 |                  0.8764 |                    0.8688 |                   0.8738 |              5.3213 |                0.9146 |            3.8852 |       0.0044 |                 0.0015 |                   0.0069 |                 0.0059 |            0.0000 |
| diagnosis_free_universal |         0.7563 |                  0.7873 |                    0.0000 |                   0.0000 |             12.0000 |                1.0000 |           12.0000 |       0.0132 |                 0.0177 |                   0.0152 |                 0.0412 |            0.0000 |

## Loop gates (L1 do-no-harm on held-out clean, L2 mean closure, U1 unseen, N1 natural traffic)

```
{
 "GUARANTEE": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 4.396426881292381e-05,
   "esci_rare": 0.9649816687696321,
   "shop": 3.719494187037764e-05
  },
  "calibration": {
   "esci_common": {
    "n": 2322,
    "losses_if_all_dispatched": 3
   },
   "esci_rare": {
    "n": 417,
    "losses_if_all_dispatched": 16
   },
   "shop": {
    "n": 202,
    "losses_if_all_dispatched": 0
   }
  },
  "heldout_clean_loss": 0.003679175864606328,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.006925207756232687,
   "esci_rare": 0.0,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.83,
  "L2": "PASS"
 },
 "U1": {
  "mean_closure": 0.48479999999999995,
  "mean_closure_without_fallback": 0.26080000000000003,
  "mean_closure_grounded": 0.45499999999999996,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5782766990291263,
  "hit_after": 0.6013349514563107,
  "delta": 0.023058252427184466,
  "ci_lo": 0.01516990291262136,
  "ci_hi": 0.03155339805825243,
  "fixed": 43,
  "broken": 5,
  "verdict": "PASS",
  "dispatched": 0.9047330097087378,
  "mean_cost": 5.852548543689321
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

| method                                    |   auroc |   ci_lo |   ci_hi |
|:------------------------------------------|--------:|--------:|--------:|
| ours_1_minus_pNONE                        |  0.9796 |  0.9743 |  0.9852 |
| qpp_neg_nqc                               |  0.5825 |  0.5583 |  0.6087 |
| qpp_neg_wig                               |  0.5762 |  0.5525 |  0.6023 |
| neg_ce1                                   |  0.6838 |  0.6597 |  0.7073 |
| raglog_tier0_best_single_rag_rt_best_rank |  0.6595 |  0.6382 |  0.6799 |
| raglog_tier0_features_hgb                 |  0.7775 |  0.7574 |  0.7975 |

## External repair baselines (oracle-dispatched, injected held-out + train episodes)

| fault   | repair                 |   n |   rescued |   ci_lo |
|:--------|:-----------------------|----:|----------:|--------:|
| Q04     | symspell (external)    |  50 |        33 |   0.522 |
| Q05     | wordsegment (external) |  50 |        48 |   0.865 |

## Family repairs, oracle-dispatched

| fault   | family   |   n |   rescued |   rate |   ci_lo |
|:--------|:---------|----:|----------:|-------:|--------:|
| Q01     | QLEX     |  50 |        33 |  0.660 |   0.522 |
| Q03     | QLEX     |  50 |         3 |  0.060 |   0.021 |
| Q04     | QLEX     |  50 |        29 |  0.580 |   0.442 |
| Q05     | QLEX     |  50 |        42 |  0.840 |   0.715 |
| K04     | STALE    |  50 |        46 |  0.920 |   0.812 |
| R03     | ENC      |  50 |        50 |  1.000 |   0.929 |
| R07     | STALE    |  50 |        50 |  1.000 |   0.929 |
| R10     | ENC      |  50 |        50 |  1.000 |   0.929 |
| R11     | ENC      |  50 |        50 |  1.000 |   0.929 |

## Natural traffic (no injection, never-examined queries): deployed loop, components, baselines

| arm   | what                                                                            |    n |   hit_before |   hit_after |   delta |   ci_lo |   ci_hi |   fixed |   broken | verdict      |   dispatched |   mean_cost |
|:------|:--------------------------------------------------------------------------------|-----:|-------------:|------------:|--------:|--------:|--------:|--------:|---------:|:-------------|-------------:|------------:|
| N1    | DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds | 1648 |       0.5783 |      0.6013 |  0.0231 |  0.0152 |  0.0316 |      43 |        5 | PASS         |       0.9047 |      5.8525 |
| N1a   | component: natural rules only                                                   | 1648 |       0.5783 |      0.6025 |  0.0243 |  0.0170 |  0.0322 |      42 |        2 | PASS         |     nan      |    nan      |
| N1b   | component: classifier dispatch only                                             | 1648 |       0.5783 |      0.5807 |  0.0024 | -0.0012 |  0.0067 |       8 |        4 | INCONCLUSIVE |       0.8374 |    nan      |
| B1    | baseline: K12 parent collapse always on (no detection)                          | 1648 |       0.5783 |      0.5965 |  0.0182 |  0.0109 |  0.0261 |      37 |        7 | PASS         |     nan      |    nan      |
| B2    | baseline: diagnosis-free universal repair on every query (cost 12)              | 1648 |       0.5783 |      0.6001 |  0.0218 |  0.0109 |  0.0334 |      61 |       25 | PASS         |     nan      |    nan      |
| NA1   | natural misspelling: ours (QLEX, log-gated)                                     |  185 |       0.5622 |      0.5135 | -0.0486 | -0.1081 |  0.0054 |       9 |       18 | INCONCLUSIVE |     nan      |    nan      |
| NA1x  | natural misspelling: SymSpell lookup_compound (external)                        |  185 |       0.5622 |      0.4486 | -0.1135 | -0.1838 | -0.0541 |       8 |       29 | HARM         |     nan      |    nan      |
| NA2   | natural missing space: ours (QLEX)                                              |   47 |       0.4468 |      0.4681 |  0.0213 | -0.0638 |  0.1277 |       3 |        2 | INCONCLUSIVE |     nan      |    nan      |
| NA2x  | natural missing space: wordsegment (external)                                   |   47 |       0.4468 |      0.4894 |  0.0426 |  0.0000 |  0.1064 |       2 |        0 | INCONCLUSIVE |     nan      |    nan      |
| NA4   | natural duplicate in top-5: K05 collapse                                        |  140 |       0.5143 |      0.5643 |  0.0500 |  0.0143 |  0.0929 |       8 |        1 | PASS         |     nan      |    nan      |
| NA5   | natural chunk crowding: K12 parent collapse                                     |  637 |       0.6436 |      0.6923 |  0.0487 |  0.0314 |  0.0675 |      33 |        2 | PASS         |     nan      |    nan      |

## Unseen faults (leave-one-fault-out attributor)

| fault   | tier   | family   |   n_test |   flagged |   right_group |   closure |   closure_without_group_fallback |
|:--------|:-------|:---------|---------:|----------:|--------------:|----------:|---------------------------------:|
| Q01     | N      | QLEX     |       25 |     0.800 |         0.720 |     0.520 |                            0.520 |
| Q02     | M      | Q02      |       25 |     0.920 |         0.040 |     0.000 |                            0.000 |
| Q03     | M      | QLEX     |       25 |     0.240 |         0.080 |     0.040 |                            0.000 |
| Q04     | S      | QLEX     |       25 |     1.000 |         0.440 |     0.480 |                            0.480 |
| Q05     | M      | QLEX     |       25 |     0.760 |         0.400 |     0.600 |                            0.600 |
| Q07     | M      | Q07      |       25 |     0.360 |         0.360 |     0.040 |                            0.040 |
| Q09     | P      | Q09      |       25 |     0.480 |         0.320 |     0.000 |                            0.000 |
| K03     | N      | K03      |       25 |     1.000 |         1.000 |     0.360 |                            0.080 |
| K04     | M      | STALE    |       25 |     0.800 |         0.000 |     0.680 |                            0.640 |
| K05     | S      | K05      |       25 |     1.000 |         1.000 |     0.880 |                            0.000 |
| K06     | N      | K06      |       25 |     1.000 |         1.000 |     0.000 |                            0.000 |
| K08     | M      | K08      |       25 |     0.920 |         0.880 |     0.400 |                            0.160 |
| K09     | M      | K09      |       25 |     0.600 |         0.600 |     0.600 |                            0.000 |
| R01     | S      | R01      |       25 |     0.240 |         0.120 |     0.200 |                            0.000 |
| R03     | N      | ENC      |       25 |     1.000 |         1.000 |     0.920 |                            0.880 |
| R05     | N      | R05      |       25 |     0.840 |         0.240 |     0.640 |                            0.000 |
| R06     | P      | R06      |       25 |     0.680 |         0.480 |     0.440 |                            0.000 |
| R07     | P      | STALE    |       25 |     1.000 |         0.000 |     0.960 |                            0.920 |
| R10     | N      | ENC      |       25 |     1.000 |         1.000 |     1.000 |                            1.000 |
| R11     | S      | ENC      |       25 |     1.000 |         1.000 |     1.000 |                            1.000 |
| R13     | M      | R13      |       25 |     0.600 |         0.360 |     0.520 |                            0.120 |
| R19     | S      | R19      |       25 |     0.640 |         0.440 |     0.480 |                            0.000 |
| R22     | S      | R22      |       25 |     0.440 |         0.240 |     0.280 |                            0.000 |
| R24     | M      | R24      |       25 |     0.800 |         0.440 |     0.480 |                            0.040 |
| K12     | S      | K12      |       25 |     0.760 |         0.760 |     0.600 |                            0.040 |

## Closed loop per fault and policy (held-out split)

| policy                   | fault   | tier   |   n_test |   dispatch_rate |   family_attribution |   group_attribution |   mean_cost |   closure |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop |
|:-------------------------|:--------|:-------|---------:|----------------:|---------------------:|--------------------:|------------:|----------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|
| tau_none_5pct_fpr        | Q01     | N      |       25 |           0.960 |                0.920 |               0.920 |       1.280 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q03     | M      |       25 |           0.080 |                0.040 |               0.040 |       0.400 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q04     | S      |       25 |           0.840 |                0.640 |               0.640 |       2.440 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q05     | M      |       25 |           0.800 |                0.480 |               0.480 |       2.960 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q07     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K03     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K04     | M      |       25 |           0.640 |                0.560 |               0.560 |       2.560 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K05     | S      |       25 |           0.960 |                0.880 |               0.920 |       3.200 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K08     | M      |       25 |           0.960 |                0.840 |               0.880 |       3.440 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R01     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R03     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R05     | N      |       25 |           0.920 |                0.760 |               0.760 |       7.280 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R06     | P      |       25 |           0.640 |                0.440 |               0.440 |       5.320 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R07     | P      |       25 |           1.000 |                0.920 |               0.880 |       7.880 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R10     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R13     | M      |       25 |           0.960 |                0.920 |               0.920 |       7.400 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R15     | S      |       25 |           0.960 |                0.960 |               0.960 |       7.680 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R19     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R22     | S      |       25 |           0.640 |                0.600 |               0.600 |       5.160 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R24     | M      |       25 |           0.840 |                0.480 |               0.480 |       6.920 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R26     | S      |        7 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K11     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K12     | S      |       25 |           0.920 |                0.920 |               0.920 |       2.760 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | C2      | N      |       25 |           0.880 |                0.520 |               0.600 |       7.760 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | NONE    | -      |     1359 |           0.036 |                0.964 |               0.964 |       0.186 |   nan     |        0.001 |                  0.002 |                    0.001 |                  0.000 |             0.000 |
| global_crc_0.005         | Q01     | N      |       25 |           1.000 |                0.920 |               0.920 |       1.640 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q03     | M      |       25 |           0.240 |                0.120 |               0.120 |       1.280 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q04     | S      |       25 |           0.960 |                0.680 |               0.680 |       3.200 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q05     | M      |       25 |           0.920 |                0.560 |               0.560 |       3.400 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q07     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K03     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K04     | M      |       25 |           0.720 |                0.560 |               0.560 |       3.320 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K05     | S      |       25 |           0.960 |                0.880 |               0.920 |       3.200 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K08     | M      |       25 |           1.000 |                0.880 |               0.920 |       3.560 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R01     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R03     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R05     | N      |       25 |           0.960 |                0.800 |               0.800 |       7.600 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R06     | P      |       25 |           0.800 |                0.440 |               0.440 |       6.440 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R07     | P      |       25 |           1.000 |                0.920 |               0.880 |       7.880 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R10     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R13     | M      |       25 |           1.000 |                0.920 |               0.920 |       7.760 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R15     | S      |       25 |           0.960 |                0.960 |               0.960 |       7.680 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R19     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R22     | S      |       25 |           0.720 |                0.640 |               0.640 |       5.840 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R24     | M      |       25 |           0.960 |                0.480 |               0.480 |       8.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R26     | S      |        7 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K11     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | C2      | N      |       25 |           1.000 |                0.520 |               0.640 |       8.480 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | NONE    | -      |     1359 |           0.122 |                0.878 |               0.878 |       0.783 |   nan     |        0.002 |                  0.005 |                    0.001 |                  0.012 |             0.000 |
| mondrian_crc_0.0025      | Q01     | N      |       25 |           0.360 |                0.360 |               0.360 |       0.360 |     0.240 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q03     | M      |       25 |           0.880 |                0.560 |               0.560 |       3.400 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q04     | S      |       25 |           0.280 |                0.280 |               0.280 |       0.280 |     0.120 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q05     | M      |       25 |           0.000 |                0.000 |               0.000 |       0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q07     | M      |       25 |           0.080 |                0.080 |               0.080 |       0.080 |     0.080 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K03     | N      |       25 |           0.680 |                0.680 |               0.680 |       2.040 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K04     | M      |       25 |           0.840 |                0.480 |               0.480 |       3.480 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K05     | S      |       25 |           1.000 |                0.920 |               0.960 |       3.320 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K07     | S      |       25 |           0.000 |                0.000 |               0.000 |       0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K08     | M      |       25 |           1.000 |                0.880 |               0.920 |       3.560 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K09     | M      |       25 |           0.000 |                0.000 |               0.000 |       0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R01     | S      |       25 |           0.880 |                0.880 |               0.880 |       7.040 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R03     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R05     | N      |       25 |           0.760 |                0.680 |               0.680 |       6.240 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R06     | P      |       25 |           0.880 |                0.560 |               0.560 |       6.720 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R07     | P      |       25 |           0.880 |                0.800 |               0.800 |       7.120 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R10     | N      |       25 |           0.920 |                0.920 |               0.920 |       7.360 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R13     | M      |       25 |           0.800 |                0.800 |               0.800 |       6.400 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R15     | S      |       25 |           1.000 |                0.960 |               0.960 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R19     | S      |       25 |           0.840 |                0.840 |               0.840 |       6.720 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R22     | S      |       25 |           0.800 |                0.640 |               0.640 |       5.600 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R24     | M      |       25 |           0.760 |                0.480 |               0.480 |       6.520 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R26     | S      |        7 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K11     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | C2      | N      |       25 |           0.640 |                0.520 |               0.520 |       6.520 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | NONE    | -      |     1359 |           0.532 |                0.468 |               0.468 |       2.747 |   nan     |        0.004 |                 -0.001 |                    0.007 |                  0.000 |             0.000 |
| mondrian_crc_0.005       | Q01     | N      |       25 |           0.640 |                0.640 |               0.640 |       0.640 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q03     | M      |       25 |           0.880 |                0.560 |               0.560 |       3.400 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q04     | S      |       25 |           0.560 |                0.520 |               0.520 |       0.880 |     0.240 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q05     | M      |       25 |           0.160 |                0.040 |               0.040 |       1.120 |     0.160 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q07     | M      |       25 |           0.960 |                0.960 |               0.960 |       0.960 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K03     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K04     | M      |       25 |           0.920 |                0.560 |               0.560 |       3.720 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K05     | S      |       25 |           1.000 |                0.920 |               0.960 |       3.320 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K08     | M      |       25 |           1.000 |                0.880 |               0.920 |       3.560 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R01     | S      |       25 |           0.960 |                0.960 |               0.960 |       7.680 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R03     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R05     | N      |       25 |           0.840 |                0.760 |               0.760 |       6.880 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R06     | P      |       25 |           0.960 |                0.600 |               0.600 |       7.400 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R07     | P      |       25 |           1.000 |                0.920 |               0.880 |       7.880 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R10     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R13     | M      |       25 |           0.880 |                0.880 |               0.880 |       7.040 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R15     | S      |       25 |           1.000 |                0.960 |               0.960 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R19     | S      |       25 |           0.920 |                0.920 |               0.920 |       7.360 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R22     | S      |       25 |           0.920 |                0.720 |               0.720 |       6.600 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R24     | M      |       25 |           0.800 |                0.480 |               0.480 |       6.880 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R26     | S      |        7 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K11     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | C2      | N      |       25 |           0.760 |                0.520 |               0.520 |       7.200 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | NONE    | -      |     1359 |           0.876 |                0.124 |               0.124 |       3.650 |   nan     |        0.004 |                 -0.001 |                    0.007 |                  0.000 |             0.000 |
| mondrian_crc_0.01        | Q01     | N      |       25 |           0.920 |                0.880 |               0.880 |       1.240 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q03     | M      |       25 |           0.920 |                0.560 |               0.560 |       3.760 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q04     | S      |       25 |           0.800 |                0.640 |               0.640 |       2.080 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q05     | M      |       25 |           0.760 |                0.440 |               0.440 |       2.920 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q07     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K03     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K04     | M      |       25 |           0.920 |                0.560 |               0.560 |       3.720 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K05     | S      |       25 |           1.000 |                0.920 |               0.960 |       3.320 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K08     | M      |       25 |           1.000 |                0.880 |               0.920 |       3.560 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R01     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R03     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R05     | N      |       25 |           1.000 |                0.840 |               0.840 |       7.920 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R06     | P      |       25 |           1.000 |                0.600 |               0.600 |       7.760 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R07     | P      |       25 |           1.000 |                0.920 |               0.880 |       7.880 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R10     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R13     | M      |       25 |           0.960 |                0.920 |               0.920 |       7.400 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R15     | S      |       25 |           1.000 |                0.960 |               0.960 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R19     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R22     | S      |       25 |           0.920 |                0.720 |               0.720 |       6.600 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R24     | M      |       25 |           0.960 |                0.520 |               0.520 |       7.960 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R26     | S      |        7 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K11     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | C2      | N      |       25 |           0.880 |                0.520 |               0.600 |       7.760 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | NONE    | -      |     1359 |           0.894 |                0.106 |               0.106 |       3.740 |   nan     |        0.004 |                  0.001 |                    0.007 |                  0.000 |             0.000 |
| mondrian_crc_0.02        | Q01     | N      |       25 |           1.000 |                0.920 |               0.920 |       1.640 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q02     | M      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q03     | M      |       25 |           0.920 |                0.560 |               0.560 |       3.760 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q04     | S      |       25 |           0.920 |                0.680 |               0.680 |       2.840 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q05     | M      |       25 |           0.800 |                0.480 |               0.480 |       2.960 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q07     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q09     | P      |       25 |           1.000 |                0.960 |               0.960 |       1.320 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K03     | N      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K04     | M      |       25 |           0.920 |                0.560 |               0.560 |       3.720 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K05     | S      |       25 |           1.000 |                0.920 |               0.960 |       3.320 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K08     | M      |       25 |           1.000 |                0.880 |               0.920 |       3.560 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R01     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R03     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R05     | N      |       25 |           1.000 |                0.840 |               0.840 |       7.920 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R06     | P      |       25 |           1.000 |                0.600 |               0.600 |       7.760 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R07     | P      |       25 |           1.000 |                0.920 |               0.880 |       7.880 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R10     | N      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R11     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R13     | M      |       25 |           0.960 |                0.920 |               0.920 |       7.400 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R15     | S      |       25 |           1.000 |                0.960 |               0.960 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R19     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R22     | S      |       25 |           0.960 |                0.760 |               0.760 |       6.920 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R24     | M      |       25 |           1.000 |                0.520 |               0.520 |       8.320 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R25     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R26     | S      |        7 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K11     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | C2      | N      |       25 |           1.000 |                0.520 |               0.640 |       8.480 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | NONE    | -      |     1359 |           0.915 |                0.085 |               0.085 |       3.885 |   nan     |        0.004 |                  0.001 |                    0.007 |                  0.006 |             0.000 |
| diagnosis_free_universal | Q01     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q02     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.160 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q03     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.080 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q04     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.520 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q05     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q07     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q09     | P      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.200 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K03     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.320 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K04     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K05     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K06     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.160 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K07     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K08     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K09     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R01     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R03     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R05     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R06     | P      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R07     | P      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R10     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R11     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R13     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R15     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R19     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R22     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R23     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R24     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R25     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R26     | S      |        7 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K11     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K12     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | C2      | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | NONE    | -      |     1359 |           1.000 |                0.000 |               0.000 |      12.000 |   nan     |        0.013 |                  0.018 |                    0.015 |                  0.041 |             0.000 |
