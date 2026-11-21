# DiagRAG v3 judged run report

Device: cpu. Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2. Last session runtime: 1268s.

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
   "n": 50,
   "rescued": 25,
   "rate": 0.5,
   "ci_lo": 0.36644286412332855
  },
  {
   "fault": "Q03",
   "family": "QLEX",
   "n": 50,
   "rescued": 2,
   "rate": 0.04,
   "ci_lo": 0.011038652660826579
  },
  {
   "fault": "Q04",
   "family": "QLEX",
   "n": 50,
   "rescued": 33,
   "rate": 0.66,
   "ci_lo": 0.5215356854148286
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
   "rescued": 45,
   "rate": 0.9,
   "ci_lo": 0.7863950966521162
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
  "mean_closure": 0.36479999999999996,
  "mean_closure_without_fallback": 0.2416,
  "mean_closure_grounded": 0.3325,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5782766990291263,
  "hit_after": 0.6007281553398058,
  "delta": 0.022451456310679612,
  "ci_lo": 0.013956310679611651,
  "ci_hi": 0.030946601941747573,
  "fixed": 45,
  "broken": 8,
  "verdict": "PASS",
  "dispatched": 0.9211165048543689,
  "mean_cost": 6.089199029126213
 },
 "detection_baselines": {
  "ours_1_minus_pNONE": [
   0.9765637212849109,
   0.9686012456897196,
   0.9819999650049126
  ],
  "qpp_neg_nqc": [
   0.582866742922505,
   0.5587251511749471,
   0.606534110621891
  ],
  "qpp_neg_wig": [
   0.5656743875702983,
   0.5351704224734445,
   0.5923792747460198
  ],
  "neg_ce1": [
   0.6715437041273473,
   0.6439023608923541,
   0.6956974293553404
  ],
  "raglog_tier0_best_single_rag_rt_best_rank": [
   0.6676465541893051,
   0.644087231659545,
   0.6894795656193659
  ],
  "raglog_tier0_features_hgb": [
   0.7562186636164331,
   0.7354410019741148,
   0.7752689414986592
  ],
  "raglog_tier0_detect_rate_at_5pct_fa": 0.514102564102564,
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
  "ours_detect_rate_at_5pct_fa": 0.9307692307692308
 },
 "repair_baselines": {
  "Q04:symspell": {
   "fault": "Q04",
   "repair": "symspell (external)",
   "n": 50,
   "rescued": 25,
   "ci_lo": 0.36644286412332855
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
 "clean_net_hit_change": 0.0,
 "guarantee": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 0.0003955049983492831,
   "esci_rare": 0.4823687100220143,
   "shop": 0.0003970579728170831
  },
  "calibration": {
   "esci_common": {
    "n": 2320,
    "losses_if_all_dispatched": 9
   },
   "esci_rare": {
    "n": 424,
    "losses_if_all_dispatched": 14
   },
   "shop": {
    "n": 202,
    "losses_if_all_dispatched": 0
   }
  },
  "heldout_clean_loss": 0.001486988847583643,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0013869625520110957,
   "esci_rare": 0.006369426751592357,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.865,
  "L2": "PASS"
 },
 "policies": [
  {
   "policy": "tau_none_5pct_fpr",
   "mean_closure": 0.845,
   "mean_closure_grounded": 0.8472727272727273,
   "mean_family_attribution": 0.84,
   "mean_group_attribution": 0.84625,
   "mean_cost_faulted": 4.936249999999999,
   "clean_dispatch_rate": 0.03940520446096654,
   "clean_mean_cost": 0.13977695167286244,
   "clean_loss": 0.001486988847583643,
   "clean_net_hit_change": -0.0007434944237918215,
   "clean_loss_esci_common": 0.0,
   "clean_loss_esci_rare": 0.012738853503184714,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "global_crc_0.005",
   "mean_closure": 0.8687499999999999,
   "mean_closure_grounded": 0.8727272727272729,
   "mean_family_attribution": 0.85375,
   "mean_group_attribution": 0.86125,
   "mean_cost_faulted": 5.16375,
   "clean_dispatch_rate": 0.16282527881040892,
   "clean_mean_cost": 1.0275092936802974,
   "clean_loss": 0.0037174721189591076,
   "clean_net_hit_change": -0.0007434944237918215,
   "clean_loss_esci_common": 0.0013869625520110957,
   "clean_loss_esci_rare": 0.025477707006369428,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.0025",
   "mean_closure": 0.75875,
   "mean_closure_grounded": 0.7400000000000001,
   "mean_family_attribution": 0.745,
   "mean_group_attribution": 0.7575,
   "mean_cost_faulted": 4.925,
   "clean_dispatch_rate": 0.37992565055762084,
   "clean_mean_cost": 2.021561338289963,
   "clean_loss": 0.001486988847583643,
   "clean_net_hit_change": 0.0,
   "clean_loss_esci_common": 0.0013869625520110957,
   "clean_loss_esci_rare": 0.006369426751592357,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.005",
   "mean_closure": 0.865,
   "mean_closure_grounded": 0.8672727272727273,
   "mean_family_attribution": 0.855,
   "mean_group_attribution": 0.8687499999999999,
   "mean_cost_faulted": 5.2825,
   "clean_dispatch_rate": 0.9026022304832714,
   "clean_mean_cost": 4.237918215613383,
   "clean_loss": 0.001486988847583643,
   "clean_net_hit_change": 0.0,
   "clean_loss_esci_common": 0.0013869625520110957,
   "clean_loss_esci_rare": 0.006369426751592357,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.01",
   "mean_closure": 0.8775,
   "mean_closure_grounded": 0.881818181818182,
   "mean_family_attribution": 0.8612500000000001,
   "mean_group_attribution": 0.875,
   "mean_cost_faulted": 5.37125,
   "clean_dispatch_rate": 0.9204460966542751,
   "clean_mean_cost": 4.356877323420075,
   "clean_loss": 0.002973977695167286,
   "clean_net_hit_change": -0.001486988847583643,
   "clean_loss_esci_common": 0.0013869625520110957,
   "clean_loss_esci_rare": 0.01910828025477707,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "mondrian_crc_0.02",
   "mean_closure": 0.8787499999999999,
   "mean_closure_grounded": 0.881818181818182,
   "mean_family_attribution": 0.8625,
   "mean_group_attribution": 0.87625,
   "mean_cost_faulted": 5.383749999999999,
   "clean_dispatch_rate": 0.9323420074349442,
   "clean_mean_cost": 4.433457249070632,
   "clean_loss": 0.002973977695167286,
   "clean_net_hit_change": -0.0007434944237918215,
   "clean_loss_esci_common": 0.0013869625520110957,
   "clean_loss_esci_rare": 0.01910828025477707,
   "clean_loss_shop": 0.0
  },
  {
   "policy": "diagnosis_free_universal",
   "mean_closure": 0.7525,
   "mean_closure_grounded": 0.8127272727272729,
   "mean_family_attribution": 0.0,
   "mean_group_attribution": 0.0,
   "mean_cost_faulted": 12.0,
   "clean_dispatch_rate": 1.0,
   "clean_mean_cost": 12.0,
   "clean_loss": 0.01412639405204461,
   "clean_net_hit_change": 0.008921933085501859,
   "clean_loss_esci_common": 0.012482662968099861,
   "clean_loss_esci_rare": 0.06369426751592357,
   "clean_loss_shop": 0.0
  }
 ],
 "natural": [
  {
   "arm": "N1",
   "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
   "n": 1648,
   "hit_before": 0.5782766990291263,
   "hit_after": 0.6007281553398058,
   "delta": 0.022451456310679612,
   "ci_lo": 0.013956310679611651,
   "ci_hi": 0.030946601941747573,
   "fixed": 45,
   "broken": 8,
   "verdict": "PASS",
   "dispatched": 0.9211165048543689,
   "mean_cost": 6.089199029126213
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
   "hit_after": 0.5776699029126213,
   "delta": -0.0006067961165048543,
   "ci_lo": -0.0048543689320388345,
   "ci_hi": 0.0036407766990291263,
   "fixed": 6,
   "broken": 7,
   "verdict": "INCONCLUSIVE",
   "dispatched": 0.8652912621359223
  },
  {
   "arm": "B1",
   "what": "baseline: K12 parent collapse always on (no detection)",
   "n": 1648,
   "hit_before": 0.5782766990291263,
   "hit_after": 0.5964805825242718,
   "delta": 0.01820388349514563,
   "ci_lo": 0.010315533980582525,
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
   "ci_hi": 0.03217536407766982,
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
   "ci_lo": -0.1783783783783784,
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
   "ci_lo": 0.007142857142857143,
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
   "ci_hi": 0.06593406593406594,
   "fixed": 33,
   "broken": 2,
   "verdict": "PASS"
  }
 ],
 "unseen_mean_closure": 0.36479999999999996,
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
| Q01     |   1275 |        403 |              257 |     95 |     50 |           25 |          25 |            0 |        0.342 |
| Q02     |   1275 |        391 |                0 |    341 |     50 |           25 |          25 |            0 |        0.128 |
| Q03     |   1275 |        140 |               31 |     59 |     50 |           25 |          25 |            0 |        0.459 |
| Q04     |   1275 |         91 |                3 |     38 |     50 |           25 |          25 |           15 |        0.568 |
| Q05     |   1275 |        255 |               25 |    180 |     50 |           25 |          25 |            0 |        0.217 |
| Q07     |   1319 |        954 |              554 |    349 |     50 |           25 |          25 |            0 |        0.125 |
| Q09     |   1275 |        140 |                0 |     90 |     50 |           25 |          25 |            0 |        0.357 |
| K03     |    878 |        177 |              123 |      3 |     50 |           25 |          25 |            0 |        0.926 |
| K04     |   1275 |         70 |                0 |     20 |     50 |           25 |          25 |            0 |        0.714 |
| K05     |   1275 |        123 |                0 |     73 |     50 |           25 |          25 |            0 |        0.407 |
| K06     |    799 |         55 |                0 |      5 |     50 |           25 |          25 |            0 |        0.909 |
| K07     |    246 |         74 |                0 |     24 |     50 |           25 |          25 |            0 |        0.676 |
| K08     |   1275 |         59 |                0 |      9 |     50 |           25 |          25 |            0 |        0.847 |
| K09     |    282 |         53 |                0 |      3 |     50 |           25 |          25 |            0 |        0.943 |
| R01     |   1275 |        102 |                0 |     52 |     50 |           25 |          25 |            0 |        0.49  |
| R03     |   1275 |        861 |                0 |    811 |     50 |           25 |          25 |            0 |        0.058 |
| R05     |   1275 |         92 |                0 |     42 |     50 |           25 |          25 |            0 |        0.543 |
| R06     |   1275 |         50 |                0 |      0 |     50 |           25 |          25 |            0 |        1     |
| R07     |   1275 |        197 |                0 |    147 |     50 |           25 |          25 |            0 |        0.254 |
| R10     |   1275 |        656 |                0 |    606 |     50 |           25 |          25 |            0 |        0.076 |
| R11     |   1275 |        683 |                0 |    632 |     50 |           25 |          25 |            0 |        0.073 |
| R13     |   1275 |       1114 |                0 |   1064 |     50 |           25 |          25 |            0 |        0.045 |
| R15     |   1275 |        509 |                0 |    459 |     50 |           25 |          25 |            0 |        0.098 |
| R19     |   1275 |        382 |                0 |    332 |     50 |           25 |          25 |            0 |        0.131 |
| R22     |   1275 |        684 |                0 |    634 |     50 |           25 |          25 |            0 |        0.073 |
| R23     |   1275 |        124 |                0 |     74 |     50 |           25 |          25 |            0 |        0.403 |
| R24     |   1275 |        129 |                0 |     79 |     50 |           25 |          25 |            0 |        0.388 |
| R25     |   1275 |        144 |                0 |     94 |     50 |           25 |          25 |            0 |        0.347 |
| R26     |   1275 |       2500 |             1240 |   1252 |      8 |            3 |           5 |            0 |        0.006 |
| K11     |    799 |         50 |                0 |      0 |     50 |           25 |          25 |            0 |        1     |
| K12     |   1275 |         79 |                0 |     29 |     50 |           25 |          25 |            0 |        0.633 |
| C2      |   1275 |        117 |               23 |     44 |     50 |           25 |          25 |            0 |        0.532 |

## Detector gates (AUROC bar 0.7, min test positives 20)

| fault   | detector                             |   n_pos_train |   n_pos_test |   n_neg_test |   auroc |   ci_lo |   ci_hi |   auroc_vs_clean | status   |
|:--------|:-------------------------------------|--------------:|-------------:|-------------:|--------:|--------:|--------:|-----------------:|:---------|
| Q01     | histgb_head                          |            25 |           25 |         2075 |  0.9968 |  0.9943 |  0.9988 |           0.9978 | PASS     |
| Q02     | histgb_head                          |            25 |           25 |         2075 |  1.0000 |  0.9998 |  1.0000 |           0.9999 | PASS     |
| Q03     | histgb_head                          |            25 |           25 |         2075 |  0.5593 |  0.4617 |  0.6634 |           0.6004 | FAIL     |
| Q04     | tier0_rule                           |            25 |           25 |         2075 |  0.9594 |  0.9099 |  0.9866 |           0.9650 | PASS     |
| Q05     | histgb_head                          |            25 |           25 |         2075 |  0.9940 |  0.9890 |  0.9979 |           0.9958 | PASS     |
| Q07     | histgb_head                          |            25 |           25 |         2075 |  0.9999 |  0.9996 |  1.0000 |           0.9999 | PASS     |
| Q09     | histgb_head                          |            25 |           25 |         2075 |  0.9996 |  0.9990 |  1.0000 |           0.9994 | PASS     |
| K03     | histgb_head                          |            25 |           25 |         2075 |  0.9998 |  0.9992 |  1.0000 |           0.9999 | PASS     |
| K04     | histgb_head                          |            25 |           25 |         2075 |  0.9142 |  0.8198 |  0.9934 |           0.9171 | PASS     |
| K05     | histgb_head                          |            25 |           25 |         2075 |  0.9997 |  0.9992 |  1.0000 |           1.0000 | PASS     |
| K06     | histgb_head                          |            25 |           25 |         2075 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K07     | tier0_rule                           |            25 |           25 |         2075 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K08     | histgb_head                          |            25 |           25 |         2075 |  0.9997 |  0.9992 |  1.0000 |           0.9998 | PASS     |
| K09     | histgb_head                          |            25 |           25 |         2075 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R01     | histgb_head                          |            25 |           25 |         2075 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R03     | histgb_head                          |            25 |           25 |         2075 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R05     | histgb_head                          |            25 |           25 |         2075 |  0.9997 |  0.9990 |  1.0000 |           0.9996 | PASS     |
| R06     | histgb_head                          |            25 |           25 |         2075 |  0.9909 |  0.9842 |  0.9967 |           0.9959 | PASS     |
| R07     | histgb_head                          |            25 |           25 |         2075 |  0.9992 |  0.9980 |  1.0000 |           1.0000 | PASS     |
| R10     | histgb_head                          |            25 |           25 |         2075 |  0.9453 |  0.8769 |  0.9941 |           0.9501 | PASS     |
| R11     | histgb_head                          |            25 |           25 |         2075 |  0.9997 |  0.9990 |  1.0000 |           1.0000 | PASS     |
| R13     | histgb_head                          |            25 |           25 |         2075 |  0.9976 |  0.9933 |  1.0000 |           0.9994 | PASS     |
| R15     | tier0_rule                           |            25 |           25 |         2075 |  0.9791 |  0.9350 |  0.9997 |           0.9800 | PASS     |
| R19     | histgb_head                          |            25 |           25 |         2075 |  0.9998 |  0.9993 |  1.0000 |           1.0000 | PASS     |
| R22     | histgb_head                          |            25 |           25 |         2075 |  0.9805 |  0.9484 |  0.9996 |           0.9868 | PASS     |
| R23     | tier0_rule                           |            25 |           25 |         2075 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R24     | histgb_head                          |            25 |           25 |         2075 |  0.9695 |  0.9326 |  0.9934 |           0.9804 | PASS     |
| R25     | tier0_rule                           |            25 |           25 |         2075 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| R26     | tier0_rule                           |             3 |            5 |         2095 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | THIN     |
| K11     | tier0_rule                           |            25 |           25 |         2075 |  1.0000 |  1.0000 |  1.0000 |           1.0000 | PASS     |
| K12     | histgb_head                          |            25 |           25 |         2075 |  1.0000 |  0.9999 |  1.0000 |           1.0000 | PASS     |
| C2      | tier0_rule(second factor-group mass) |            25 |           25 |         2100 |  0.7774 |  0.6492 |  0.8958 |         nan      | PASS     |

## Repair gates (Wilson lower bound >= 0.5)

| fault   |   n_hard |   rescued |   rescue_rate |   ci_lo |   ci_hi |   clean_n |   clean_lost |   harm_rate | status   |
|:--------|---------:|----------:|--------------:|--------:|--------:|----------:|-------------:|------------:|:---------|
| Q01     |       50 |        33 |         0.660 |   0.522 |   0.776 |        20 |            0 |       0.000 | PASS     |
| Q02     |       50 |        42 |         0.840 |   0.715 |   0.917 |        20 |            0 |       0.000 | PASS     |
| Q03     |       50 |         1 |         0.020 |   0.004 |   0.105 |        20 |            1 |       0.050 | FAIL     |
| Q04     |       50 |        41 |         0.820 |   0.692 |   0.902 |        20 |            0 |       0.000 | PASS     |
| Q05     |       50 |        46 |         0.920 |   0.812 |   0.968 |        20 |            0 |       0.000 | PASS     |
| Q07     |       50 |        39 |         0.780 |   0.648 |   0.872 |        20 |            0 |       0.000 | PASS     |
| Q09     |       50 |        41 |         0.820 |   0.692 |   0.902 |        20 |            0 |       0.000 | PASS     |
| K03     |       50 |        46 |         0.920 |   0.812 |   0.968 |        20 |            0 |       0.000 | PASS     |
| K04     |       50 |        45 |         0.900 |   0.786 |   0.957 |        20 |            0 |       0.000 | PASS     |
| K05     |       50 |        49 |         0.980 |   0.895 |   0.996 |        20 |            1 |       0.050 | PASS     |
| K06     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K07     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K08     |       50 |        46 |         0.920 |   0.812 |   0.968 |        20 |            0 |       0.000 | PASS     |
| K09     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R01     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R03     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R05     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R06     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R07     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R10     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R11     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R13     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R15     |       50 |        49 |         0.980 |   0.895 |   0.996 |        20 |            0 |       0.000 | PASS     |
| R19     |       50 |        47 |         0.940 |   0.838 |   0.979 |        20 |            0 |       0.000 | PASS     |
| R22     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R23     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R24     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R25     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| R26     |        8 |         8 |         1.000 |   0.676 |   1.000 |        20 |            0 |       0.000 | THIN     |
| K11     |       50 |        50 |         1.000 |   0.929 |   1.000 |        20 |            0 |       0.000 | PASS     |
| K12     |       50 |        46 |         0.920 |   0.812 |   0.968 |        20 |            0 |       0.000 | PASS     |
| C2      |       50 |        42 |         0.840 |   0.715 |   0.917 |         0 |            0 |       0.000 | PASS     |

## Dispatch policies (held-out)

| policy                   |   mean_closure |   mean_closure_grounded |   mean_family_attribution |   mean_group_attribution |   mean_cost_faulted |   clean_dispatch_rate |   clean_mean_cost |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop |
|:-------------------------|---------------:|------------------------:|--------------------------:|-------------------------:|--------------------:|----------------------:|------------------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|
| tau_none_5pct_fpr        |         0.8450 |                  0.8473 |                    0.8400 |                   0.8462 |              4.9362 |                0.0394 |            0.1398 |       0.0015 |                -0.0007 |                   0.0000 |                 0.0127 |            0.0000 |
| global_crc_0.005         |         0.8687 |                  0.8727 |                    0.8538 |                   0.8612 |              5.1638 |                0.1628 |            1.0275 |       0.0037 |                -0.0007 |                   0.0014 |                 0.0255 |            0.0000 |
| mondrian_crc_0.0025      |         0.7588 |                  0.7400 |                    0.7450 |                   0.7575 |              4.9250 |                0.3799 |            2.0216 |       0.0015 |                 0.0000 |                   0.0014 |                 0.0064 |            0.0000 |
| mondrian_crc_0.005       |         0.8650 |                  0.8673 |                    0.8550 |                   0.8687 |              5.2825 |                0.9026 |            4.2379 |       0.0015 |                 0.0000 |                   0.0014 |                 0.0064 |            0.0000 |
| mondrian_crc_0.01        |         0.8775 |                  0.8818 |                    0.8613 |                   0.8750 |              5.3712 |                0.9204 |            4.3569 |       0.0030 |                -0.0015 |                   0.0014 |                 0.0191 |            0.0000 |
| mondrian_crc_0.02        |         0.8787 |                  0.8818 |                    0.8625 |                   0.8762 |              5.3837 |                0.9323 |            4.4335 |       0.0030 |                -0.0007 |                   0.0014 |                 0.0191 |            0.0000 |
| diagnosis_free_universal |         0.7525 |                  0.8127 |                    0.0000 |                   0.0000 |             12.0000 |                1.0000 |           12.0000 |       0.0141 |                 0.0089 |                   0.0125 |                 0.0637 |            0.0000 |

## Loop gates (L1 do-no-harm on held-out clean, L2 mean closure, U1 unseen, N1 natural traffic)

```
{
 "GUARANTEE": {
  "alpha": 0.005,
  "lambdas": {
   "esci_common": 0.0003955049983492831,
   "esci_rare": 0.4823687100220143,
   "shop": 0.0003970579728170831
  },
  "calibration": {
   "esci_common": {
    "n": 2320,
    "losses_if_all_dispatched": 9
   },
   "esci_rare": {
    "n": 424,
    "losses_if_all_dispatched": 14
   },
   "shop": {
    "n": 202,
    "losses_if_all_dispatched": 0
   }
  },
  "heldout_clean_loss": 0.001486988847583643,
  "heldout_clean_loss_by_stratum": {
   "esci_common": 0.0013869625520110957,
   "esci_rare": 0.006369426751592357,
   "shop": 0.0
  },
  "L1": "PASS",
  "mean_closure": 0.865,
  "L2": "PASS"
 },
 "U1": {
  "mean_closure": 0.36479999999999996,
  "mean_closure_without_fallback": 0.2416,
  "mean_closure_grounded": 0.3325,
  "status": "FAIL"
 },
 "N1": {
  "arm": "N1",
  "what": "DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds",
  "n": 1648,
  "hit_before": 0.5782766990291263,
  "hit_after": 0.6007281553398058,
  "delta": 0.022451456310679612,
  "ci_lo": 0.013956310679611651,
  "ci_hi": 0.030946601941747573,
  "fixed": 45,
  "broken": 8,
  "verdict": "PASS",
  "dispatched": 0.9211165048543689,
  "mean_cost": 6.089199029126213
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
| ours_1_minus_pNONE                        |  0.9766 |  0.9686 |  0.9820 |
| qpp_neg_nqc                               |  0.5829 |  0.5587 |  0.6065 |
| qpp_neg_wig                               |  0.5657 |  0.5352 |  0.5924 |
| neg_ce1                                   |  0.6715 |  0.6439 |  0.6957 |
| raglog_tier0_best_single_rag_rt_best_rank |  0.6676 |  0.6441 |  0.6895 |
| raglog_tier0_features_hgb                 |  0.7562 |  0.7354 |  0.7753 |

## External repair baselines (oracle-dispatched, injected held-out + train episodes)

| fault   | repair                 |   n |   rescued |   ci_lo |
|:--------|:-----------------------|----:|----------:|--------:|
| Q04     | symspell (external)    |  50 |        25 |   0.366 |
| Q05     | wordsegment (external) |  50 |        48 |   0.865 |

## Family repairs, oracle-dispatched

| fault   | family   |   n |   rescued |   rate |   ci_lo |
|:--------|:---------|----:|----------:|-------:|--------:|
| Q01     | QLEX     |  50 |        25 |  0.500 |   0.366 |
| Q03     | QLEX     |  50 |         2 |  0.040 |   0.011 |
| Q04     | QLEX     |  50 |        33 |  0.660 |   0.522 |
| Q05     | QLEX     |  50 |        43 |  0.860 |   0.738 |
| K04     | STALE    |  50 |        45 |  0.900 |   0.786 |
| R03     | ENC      |  50 |        50 |  1.000 |   0.929 |
| R07     | STALE    |  50 |        50 |  1.000 |   0.929 |
| R10     | ENC      |  50 |        50 |  1.000 |   0.929 |
| R11     | ENC      |  50 |        50 |  1.000 |   0.929 |

## Natural traffic (no injection, never-examined queries): deployed loop, components, baselines

| arm   | what                                                                            |    n |   hit_before |   hit_after |   delta |   ci_lo |   ci_hi |   fixed |   broken | verdict      |   dispatched |   mean_cost |
|:------|:--------------------------------------------------------------------------------|-----:|-------------:|------------:|--------:|--------:|--------:|--------:|---------:|:-------------|-------------:|------------:|
| N1    | DEPLOYED LOOP: natural rules (K12, K05) + classifier at Mondrian-CRC thresholds | 1648 |       0.5783 |      0.6007 |  0.0225 |  0.0140 |  0.0309 |      45 |        8 | PASS         |       0.9211 |      6.0892 |
| N1a   | component: natural rules only                                                   | 1648 |       0.5783 |      0.6025 |  0.0243 |  0.0170 |  0.0322 |      42 |        2 | PASS         |     nan      |    nan      |
| N1b   | component: classifier dispatch only                                             | 1648 |       0.5783 |      0.5777 | -0.0006 | -0.0049 |  0.0036 |       6 |        7 | INCONCLUSIVE |       0.8653 |    nan      |
| B1    | baseline: K12 parent collapse always on (no detection)                          | 1648 |       0.5783 |      0.5965 |  0.0182 |  0.0103 |  0.0261 |      37 |        7 | PASS         |     nan      |    nan      |
| B2    | baseline: diagnosis-free universal repair on every query (cost 12)              | 1648 |       0.5783 |      0.6001 |  0.0218 |  0.0109 |  0.0322 |      61 |       25 | PASS         |     nan      |    nan      |
| NA1   | natural misspelling: ours (QLEX, log-gated)                                     |  185 |       0.5622 |      0.5135 | -0.0486 | -0.1027 |  0.0054 |       9 |       18 | INCONCLUSIVE |     nan      |    nan      |
| NA1x  | natural misspelling: SymSpell lookup_compound (external)                        |  185 |       0.5622 |      0.4486 | -0.1135 | -0.1784 | -0.0541 |       8 |       29 | HARM         |     nan      |    nan      |
| NA2   | natural missing space: ours (QLEX)                                              |   47 |       0.4468 |      0.4681 |  0.0213 | -0.0638 |  0.1277 |       3 |        2 | INCONCLUSIVE |     nan      |    nan      |
| NA2x  | natural missing space: wordsegment (external)                                   |   47 |       0.4468 |      0.4894 |  0.0426 |  0.0000 |  0.1064 |       2 |        0 | INCONCLUSIVE |     nan      |    nan      |
| NA4   | natural duplicate in top-5: K05 collapse                                        |  140 |       0.5143 |      0.5643 |  0.0500 |  0.0071 |  0.0929 |       8 |        1 | PASS         |     nan      |    nan      |
| NA5   | natural chunk crowding: K12 parent collapse                                     |  637 |       0.6436 |      0.6923 |  0.0487 |  0.0314 |  0.0659 |      33 |        2 | PASS         |     nan      |    nan      |

## Unseen faults (leave-one-fault-out attributor)

| fault   | tier   | family   |   n_test |   flagged |   right_group |   closure |   closure_without_group_fallback |
|:--------|:-------|:---------|---------:|----------:|--------------:|----------:|---------------------------------:|
| Q01     | N      | QLEX     |       25 |     0.480 |         0.360 |     0.120 |                            0.120 |
| Q02     | M      | Q02      |       25 |     0.520 |         0.120 |     0.040 |                            0.040 |
| Q03     | M      | QLEX     |       25 |     0.160 |         0.040 |     0.000 |                            0.000 |
| Q04     | S      | QLEX     |       25 |     0.600 |         0.360 |     0.440 |                            0.440 |
| Q05     | M      | QLEX     |       25 |     0.520 |         0.240 |     0.320 |                            0.320 |
| Q07     | M      | Q07      |       25 |     0.120 |         0.120 |     0.000 |                            0.000 |
| Q09     | P      | Q09      |       25 |     0.320 |         0.240 |     0.080 |                            0.080 |
| K03     | N      | K03      |       25 |     1.000 |         0.480 |     0.040 |                            0.040 |
| K04     | M      | STALE    |       25 |     0.880 |         0.000 |     0.800 |                            0.720 |
| K05     | S      | K05      |       25 |     1.000 |         0.440 |     0.880 |                            0.000 |
| K06     | N      | K06      |       25 |     1.000 |         1.000 |     0.000 |                            0.000 |
| K08     | M      | K08      |       25 |     1.000 |         0.120 |     0.320 |                            0.080 |
| K09     | M      | K09      |       25 |     0.280 |         0.000 |     0.080 |                            0.000 |
| R01     | S      | R01      |       25 |     0.440 |         0.040 |     0.280 |                            0.040 |
| R03     | N      | ENC      |       25 |     1.000 |         0.960 |     0.960 |                            0.960 |
| R05     | N      | R05      |       25 |     0.520 |         0.280 |     0.200 |                            0.040 |
| R06     | P      | R06      |       25 |     0.640 |         0.440 |     0.440 |                            0.000 |
| R07     | P      | STALE    |       25 |     1.000 |         0.040 |     0.960 |                            0.960 |
| R10     | N      | ENC      |       25 |     1.000 |         0.920 |     1.000 |                            1.000 |
| R11     | S      | ENC      |       25 |     1.000 |         1.000 |     1.000 |                            1.000 |
| R13     | M      | R13      |       25 |     0.520 |         0.200 |     0.480 |                            0.120 |
| R19     | S      | R19      |       25 |     1.000 |         1.000 |     0.000 |                            0.000 |
| R22     | S      | R22      |       25 |     0.360 |         0.080 |     0.160 |                            0.040 |
| R24     | M      | R24      |       25 |     0.320 |         0.080 |     0.160 |                            0.000 |
| K12     | S      | K12      |       25 |     0.760 |         0.320 |     0.360 |                            0.040 |

## Closed loop per fault and policy (held-out split)

| policy                   | fault   | tier   |   n_test |   dispatch_rate |   family_attribution |   group_attribution |   mean_cost |   closure |   clean_loss |   clean_net_hit_change |   clean_loss_esci_common |   clean_loss_esci_rare |   clean_loss_shop |
|:-------------------------|:--------|:-------|---------:|----------------:|---------------------:|--------------------:|------------:|----------:|-------------:|-----------------------:|-------------------------:|-----------------------:|------------------:|
| tau_none_5pct_fpr        | Q01     | N      |       25 |           0.920 |                0.920 |               0.920 |       0.920 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q02     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q03     | M      |       25 |           0.040 |                0.040 |               0.040 |       0.040 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q04     | S      |       25 |           0.840 |                0.720 |               0.720 |       1.800 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q05     | M      |       25 |           0.840 |                0.760 |               0.760 |       1.480 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q07     | M      |       25 |           0.960 |                0.960 |               0.960 |       0.960 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | Q09     | P      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K03     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K04     | M      |       25 |           0.760 |                0.360 |               0.360 |       5.480 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K05     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K08     | M      |       25 |           0.960 |                0.840 |               0.960 |       2.880 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R01     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R05     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R06     | P      |       25 |           0.760 |                0.680 |               0.680 |       5.840 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R07     | P      |       25 |           0.960 |                0.720 |               0.680 |       8.120 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R10     | N      |       25 |           1.000 |                0.840 |               0.880 |       8.120 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R11     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R13     | M      |       25 |           0.960 |                0.920 |               0.920 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R15     | S      |       25 |           0.960 |                0.960 |               0.960 |       7.680 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R19     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R22     | S      |       25 |           0.800 |                0.720 |               0.720 |       6.480 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R24     | M      |       25 |           0.640 |                0.560 |               0.600 |       5.160 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R25     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.160 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | R26     | S      |        5 |           1.000 |                0.800 |               0.800 |       8.200 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | C2      | N      |       25 |           0.960 |                0.440 |               0.480 |       7.360 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| tau_none_5pct_fpr        | NONE    | -      |     1345 |           0.039 |                0.961 |               0.961 |       0.140 |   nan     |        0.001 |                 -0.001 |                    0.000 |                  0.013 |             0.000 |
| global_crc_0.005         | Q01     | N      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q02     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q03     | M      |       25 |           0.200 |                0.080 |               0.080 |       1.200 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q04     | S      |       25 |           0.920 |                0.720 |               0.720 |       2.320 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q05     | M      |       25 |           0.960 |                0.840 |               0.840 |       1.920 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q07     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | Q09     | P      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K03     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K04     | M      |       25 |           0.880 |                0.360 |               0.360 |       5.920 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K05     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K08     | M      |       25 |           1.000 |                0.840 |               0.960 |       3.240 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R01     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R05     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R06     | P      |       25 |           0.840 |                0.720 |               0.720 |       6.520 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R07     | P      |       25 |           1.000 |                0.720 |               0.680 |       8.480 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R10     | N      |       25 |           1.000 |                0.840 |               0.880 |       8.120 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R11     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R13     | M      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R15     | S      |       25 |           0.960 |                0.960 |               0.960 |       7.680 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R19     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R22     | S      |       25 |           0.920 |                0.800 |               0.800 |       7.160 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R24     | M      |       25 |           0.840 |                0.640 |               0.680 |       6.880 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R25     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.160 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | R26     | S      |        5 |           1.000 |                0.800 |               0.800 |       8.200 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | C2      | N      |       25 |           1.000 |                0.440 |               0.520 |       7.800 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| global_crc_0.005         | NONE    | -      |     1345 |           0.163 |                0.837 |               0.837 |       1.028 |   nan     |        0.004 |                 -0.001 |                    0.001 |                  0.025 |             0.000 |
| mondrian_crc_0.0025      | Q01     | N      |       25 |           0.920 |                0.920 |               0.920 |       0.920 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q02     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q03     | M      |       25 |           0.600 |                0.200 |               0.200 |       3.520 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q04     | S      |       25 |           0.840 |                0.720 |               0.720 |       1.800 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q05     | M      |       25 |           0.800 |                0.760 |               0.760 |       1.120 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q07     | M      |       25 |           0.040 |                0.040 |               0.040 |       0.040 |     0.040 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | Q09     | P      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K03     | N      |       25 |           0.400 |                0.400 |               0.400 |       1.200 |     0.360 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K04     | M      |       25 |           0.840 |                0.360 |               0.360 |       5.880 |     0.760 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K05     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K07     | S      |       25 |           0.000 |                0.000 |               0.000 |       0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K08     | M      |       25 |           1.000 |                0.840 |               0.960 |       3.240 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K09     | M      |       25 |           0.000 |                0.000 |               0.000 |       0.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R01     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R05     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R06     | P      |       25 |           0.920 |                0.760 |               0.760 |       6.880 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R07     | P      |       25 |           0.960 |                0.720 |               0.680 |       8.120 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R10     | N      |       25 |           1.000 |                0.840 |               0.880 |       8.120 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R11     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R13     | M      |       25 |           0.960 |                0.920 |               0.920 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R15     | S      |       25 |           1.000 |                0.960 |               0.960 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R19     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R22     | S      |       25 |           1.000 |                0.800 |               0.880 |       7.800 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R24     | M      |       25 |           0.880 |                0.680 |               0.800 |       7.120 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R25     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.160 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | R26     | S      |        5 |           1.000 |                0.800 |               0.800 |       8.200 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | C2      | N      |       25 |           1.000 |                0.440 |               0.520 |       7.800 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.0025      | NONE    | -      |     1345 |           0.380 |                0.620 |               0.620 |       2.022 |   nan     |        0.001 |                  0.000 |                    0.001 |                  0.006 |             0.000 |
| mondrian_crc_0.005       | Q01     | N      |       25 |           0.920 |                0.920 |               0.920 |       0.920 |     0.400 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q02     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q03     | M      |       25 |           0.880 |                0.240 |               0.240 |       5.280 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q04     | S      |       25 |           0.840 |                0.720 |               0.720 |       1.800 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q05     | M      |       25 |           0.800 |                0.760 |               0.760 |       1.120 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q07     | M      |       25 |           0.960 |                0.960 |               0.960 |       0.960 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | Q09     | P      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K03     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K04     | M      |       25 |           0.880 |                0.360 |               0.360 |       6.200 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K05     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K08     | M      |       25 |           1.000 |                0.840 |               0.960 |       3.240 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R01     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R05     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R06     | P      |       25 |           0.960 |                0.760 |               0.800 |       7.200 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R07     | P      |       25 |           0.960 |                0.720 |               0.680 |       8.120 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R10     | N      |       25 |           1.000 |                0.840 |               0.880 |       8.120 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R11     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R13     | M      |       25 |           0.960 |                0.920 |               0.920 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R15     | S      |       25 |           1.000 |                0.960 |               0.960 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R19     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R22     | S      |       25 |           1.000 |                0.800 |               0.880 |       7.800 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R24     | M      |       25 |           0.880 |                0.680 |               0.800 |       7.120 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R25     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.160 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | R26     | S      |        5 |           1.000 |                0.800 |               0.800 |       8.200 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | C2      | N      |       25 |           1.000 |                0.440 |               0.520 |       7.800 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.005       | NONE    | -      |     1345 |           0.903 |                0.097 |               0.097 |       4.238 |   nan     |        0.001 |                  0.000 |                    0.001 |                  0.006 |             0.000 |
| mondrian_crc_0.01        | Q01     | N      |       25 |           0.960 |                0.960 |               0.960 |       0.960 |     0.440 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q02     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q03     | M      |       25 |           0.880 |                0.240 |               0.240 |       5.280 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q04     | S      |       25 |           0.920 |                0.720 |               0.720 |       2.320 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q05     | M      |       25 |           0.960 |                0.840 |               0.840 |       1.920 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q07     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | Q09     | P      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K03     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K04     | M      |       25 |           0.920 |                0.360 |               0.360 |       6.240 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K05     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K08     | M      |       25 |           1.000 |                0.840 |               0.960 |       3.240 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R01     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R05     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R06     | P      |       25 |           1.000 |                0.800 |               0.840 |       7.520 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R07     | P      |       25 |           1.000 |                0.720 |               0.680 |       8.480 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R10     | N      |       25 |           1.000 |                0.840 |               0.880 |       8.120 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R11     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R13     | M      |       25 |           0.960 |                0.920 |               0.920 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R15     | S      |       25 |           1.000 |                0.960 |               0.960 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R19     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R22     | S      |       25 |           1.000 |                0.800 |               0.880 |       7.800 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R24     | M      |       25 |           0.960 |                0.680 |               0.800 |       7.840 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R25     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.160 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | R26     | S      |        5 |           1.000 |                0.800 |               0.800 |       8.200 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | C2      | N      |       25 |           1.000 |                0.440 |               0.520 |       7.800 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.01        | NONE    | -      |     1345 |           0.920 |                0.080 |               0.080 |       4.357 |   nan     |        0.003 |                 -0.001 |                    0.001 |                  0.019 |             0.000 |
| mondrian_crc_0.02        | Q01     | N      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q02     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q03     | M      |       25 |           0.880 |                0.240 |               0.240 |       5.280 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q04     | S      |       25 |           0.920 |                0.720 |               0.720 |       2.320 |     0.680 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q05     | M      |       25 |           0.960 |                0.840 |               0.840 |       1.920 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q07     | M      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | Q09     | P      |       25 |           1.000 |                1.000 |               1.000 |       1.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K03     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.320 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K04     | M      |       25 |           0.920 |                0.360 |               0.360 |       6.240 |     0.800 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K05     | S      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K06     | N      |       25 |           1.000 |                0.960 |               0.960 |       3.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K07     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K08     | M      |       25 |           1.000 |                0.840 |               0.960 |       3.240 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K09     | M      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R01     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R03     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R05     | N      |       25 |           1.000 |                0.960 |               0.960 |       8.040 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R06     | P      |       25 |           1.000 |                0.800 |               0.840 |       7.520 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R07     | P      |       25 |           1.000 |                0.720 |               0.680 |       8.480 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R10     | N      |       25 |           1.000 |                0.840 |               0.880 |       8.120 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R11     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R13     | M      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R15     | S      |       25 |           1.000 |                0.960 |               0.960 |       7.720 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R19     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.080 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R22     | S      |       25 |           1.000 |                0.800 |               0.880 |       7.800 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R23     | S      |       25 |           1.000 |                1.000 |               1.000 |       8.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R24     | M      |       25 |           0.960 |                0.680 |               0.800 |       7.840 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R25     | S      |       25 |           1.000 |                0.920 |               0.920 |       8.160 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | R26     | S      |        5 |           1.000 |                0.800 |               0.800 |       8.200 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K11     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | K12     | S      |       25 |           1.000 |                1.000 |               1.000 |       3.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | C2      | N      |       25 |           1.000 |                0.440 |               0.520 |       7.800 |     0.640 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| mondrian_crc_0.02        | NONE    | -      |     1345 |           0.932 |                0.068 |               0.068 |       4.433 |   nan     |        0.003 |                 -0.001 |                    0.001 |                  0.019 |             0.000 |
| diagnosis_free_universal | Q01     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.480 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q02     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.200 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q03     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.080 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q04     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q05     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.840 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q07     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | Q09     | P      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.240 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K03     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K04     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K05     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K06     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K07     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K08     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.600 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K09     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R01     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R03     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R05     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R06     | P      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R07     | P      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.880 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R10     | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R11     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R13     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R15     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R19     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R22     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R23     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R24     | M      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.920 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R25     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | R26     | S      |        5 |           1.000 |                0.000 |               0.000 |      12.000 |     1.000 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K11     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | K12     | S      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.960 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | C2      | N      |       25 |           1.000 |                0.000 |               0.000 |      12.000 |     0.720 |      nan     |                nan     |                  nan     |                nan     |           nan     |
| diagnosis_free_universal | NONE    | -      |     1345 |           1.000 |                0.000 |               0.000 |      12.000 |   nan     |        0.014 |                  0.009 |                    0.012 |                  0.064 |             0.000 |
