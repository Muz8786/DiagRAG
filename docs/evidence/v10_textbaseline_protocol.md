# Supervised text baseline for fault diagnosis (pre-registration). Written 19 Nov 2026, before any text feature was built from the NFCorpus or ArguAna episodes and before any text model was trained.

## 0. Question and scope
The standing objection to the LLM comparison (B1, `docs/LLM_BASELINES_RESULTS.md`) is that it pits **supervised telemetry** against **zero-shot** LLM judges. This study gives the text side the same supervision: a classifier trained on the **same labelled training episodes**, seeing **what the LLM judge saw** (the query and the five returned documents), scored on the **same held-out episodes** as the telemetry attributor.
It is **descriptive and additive**. No detector, repair, gate or frozen file changes. It runs on the two v9 port corpora only (NFCorpus, ArguAna), because they are the runs whose checkpoints let retrieval be replayed from cache (`kaggle/judged_port3_*/` hold the results; the episode checkpoints are in the Kaggle kernel outputs). The ESCI-based main runs do not store document text and are **not** covered.

## 1. Data and replay (fixed)
- Episodes: every episode in the corpus's `checkpoint.pkl` (`EPIS`: single-fault episodes and clean `NONE` episodes), with its stored `split`, `fault` and telemetry `feats`. The attributor and the text classifier use the **same** train and test split.
- Text view: the frozen `diagrag_port3.py` (hash `677a2f38…3a77ada`) is executed up to its retrieval function with the run's settings and the run's own caches; for each episode `run(st)` is replayed and the **top-5 documents** are read. Each document is shown as its first **360 characters** (about title plus 240 characters, as in B1). Query and documents are joined into one string.
- **Replay check before anything is scored:** for the clean episodes the replayed Hit@5 must equal the Hit@5 stored in the checkpoint for at least **99.5%** of episodes; otherwise the replay is not trusted and the study stops and is reported as not run.
- Clean episodes with the same base query as a faulted episode stay in the same split (the stored split is by query id).

## 2. Models (fixed; no tuning on the held-out set)
- **Telemetry attributor (reference):** `HistGradientBoostingClassifier(max_iter=250, learning_rate=0.08, max_leaf_nodes=15, min_samples_leaf=5, l2_regularization=1.0, class_weight='balanced', random_state=<run seed>)` on the 63-feature-style telemetry vector of the stored `feats`, classes = faults present in training plus `NONE`.
- **Text model, primary (T1):** `TfidfVectorizer(ngram_range=(1,2), min_df=2, max_features=50000, sublinear_tf=True)` on the joined query-and-documents string, then `LogisticRegression(C=3.0, class_weight='balanced', max_iter=500)`, same classes.
- **Text model, sensitivity (T2):** `TfidfVectorizer(analyzer='char_wb', ngram_range=(2,4), min_df=3, max_features=100000, sublinear_tf=True)` then the same logistic regression. **T1 is the primary; T2 is reported beside it and is not chosen after seeing results.** No other text model is tried.
- **Fault-vs-clean score** for all three is 1 - P(NONE). **Exact-fault accuracy** is the top-1 class on faulted held-out episodes.

## 3. Measures and verdict rule (as in the LLM baselines plan)
- Held-out fault-vs-clean AUROC for the attributor, T1 and T2; paired bootstrap (2,000 resamples, resampling episodes) of AUROC(attributor) - AUROC(text).
- Verdict per corpus and per text model: **OURS_BETTER** if the 95% interval's lower bound is > 0; **OURS_NON_INFERIOR** if > -0.02; **TEXT_BETTER** if the upper bound is < 0; else **INCONCLUSIVE**.
- Also reported: exact-fault accuracy on faulted held-out episodes, per-letter-group exact accuracy (Q, K, R), and the number of held-out positives and negatives.
- A claim of the form "telemetry diagnosis is at least as good as a supervised text model" is made **only** if the verdict is OURS_BETTER or OURS_NON_INFERIOR for T1 **on both corpora**; otherwise the result is reported as not shown.

## 4. Predictions (my judgements; they can fail)
- The attributor beats T1 on fault-vs-clean AUROC on both corpora (lower bound > 0): about 0.55. The reason I do not put it higher: the top-5 documents carry real content differences for K and R faults (stale, duplicated, truncated or filtered results), and a supervised model may pick them up.
- T1 beats the zero-shot LLM judges' range on the ESCI task (0.63 to 0.75): about 0.8 (a different corpus; reported only as context, not as a comparison).
- T2 gives a result within 0.05 AUROC of T1: about 0.7.
- Per-group exact accuracy: the text models do worst on R (stack) faults: about 0.7.

## 5. What a result would and would not show
- Two small corpora (25 held-out faulted episodes per fault, 500 faulted and 700 to 1,300 clean held-out episodes each), one stack, author-injected faults, a text baseline with no tuning. Intervals will be about +/-0.02 to 0.04 on AUROC.
- Most injected faults are blunt (many detectors reach AUROC 1.000), so a high text AUROC could reflect easy faults and not a strong text model.
- It does **not** cover the ESCI main runs or any frontier LLM. A cross-encoder fine-tuned on the text, or a large LLM given labelled examples, may do better than this simple supervised text model; that is **not** tested.

## 6. Amendments
(none yet; each is dated and filed before the result it concerns is read)

**H1 — result and scorecard (19 Nov 2026; written after the result was read; sections 0 to 5 are unedited). Files: `v10_textview.py` (replay), `v10_textbaseline.py`, `v10_textbaseline_nfcorpus.json`, `v10_textbaseline_arguana.json`.** scikit-learn 1.6.1. The replayed top-5 text (`view_*.jsonl`, BEIR text) is not committed.

*Replay check (pre-registered threshold 99.5%).* The replay of the frozen port3 retrieval from the run's own caches reproduced the stored clean Hit@5 for **2,500 of 2,500** (NFCorpus) and **1,401 of 1,401** (ArguAna) clean episodes (0 mismatches). The study therefore ran.

*Held-out fault-vs-clean AUROC and exact-fault accuracy on faulted episodes.* NFCorpus: 500 faulted and 1,263 clean held-out episodes. ArguAna: 454 faulted and 704 clean.
| Corpus | Model | AUROC | Exact fault (faulted) | Attributor minus text, 95% interval | Verdict |
|---|---|---|---|---|---|
| NFCorpus | Telemetry attributor | 0.9717 | 85.2% | | |
| NFCorpus | T1 word TF-IDF + LR (primary) | 0.5746 | 10.6% | +0.397 [+0.368, +0.427] | **OURS_BETTER** |
| NFCorpus | T2 char TF-IDF + LR | 0.5720 | 16.6% | +0.400 [+0.369, +0.432] | OURS_BETTER |
| ArguAna | Telemetry attributor | 0.9961 | 97.8% | | |
| ArguAna | T1 word TF-IDF + LR (primary) | 0.5956 | 7.3% | +0.401 [+0.369, +0.435] | **OURS_BETTER** |
| ArguAna | T2 char TF-IDF + LR | 0.6134 | 12.6% | +0.383 [+0.351, +0.417] | OURS_BETTER |

By letter group, exact-fault accuracy (T1, NFCorpus): Q 5%, K 27%, R 9% against the attributor's 66%, 84%, 91%; (T1, ArguAna): Q 2%, K 0%, R 10% against 89%, 95%, 100%.

*Claim rule (section 3):* the verdict is OURS_BETTER for T1 on **both** corpora, so the pre-registered statement is allowed: **on these two corpora, a supervised word TF-IDF logistic model on the query and the top-5 documents, trained on the same labelled episodes, is far worse than the telemetry attributor at both detecting and naming the fault.** It does **not** say that no text model can match telemetry.

*Scorecard against section 4.* (1) Attributor beats T1 with a positive lower bound on both corpora, about 0.55: **held** (lower bounds +0.368 and +0.369). (2) T1 inside or above the zero-shot LLM range of 0.63 to 0.75, about 0.8: **did not hold** (0.575 and 0.596; the comparison is context only, a different corpus). (3) T2 within 0.05 AUROC of T1, about 0.7: **held** (0.572 against 0.575; 0.613 against 0.596). (4) Text models do worst on R faults, about 0.7: **did not hold**: the worst group is Q in NFCorpus (T1 5%, T2 7%) and K or Q in ArguAna (T1 K 0%, T2 Q 2%).

*Checks run after the result was read, to rule out a bug (post-hoc).* The view file is aligned with the episodes (every stored query, fault and split equals the viewed one). Fault-vs-clean AUROC of a binary text classifier by view (NFCorpus; Q, K, R faults against clean): query characters 0.57, 0.55, 0.53; documents 0.59, 0.74, 0.57; query plus documents 0.58, 0.75, 0.57. ArguAna: 0.55, 0.51, 0.58; 0.47, 0.66, 0.65; 0.49, 0.70, 0.63. The text signal is weak everywhere and best for K faults (document-level changes). Typo (Q) faults are not separable from the rare words of the corpora by this model.

*Why this is a weak baseline, and what it does not show.* (a) The text models learn from about 25 training positives per fault over 20 classes; a model with prior knowledge (a fine-tuned cross-encoder, or an LLM given labelled examples) could do much better, and that is **not** tested. (b) The attributor sees quantities (score gaps, rank agreement between the dense and lexical legs, duplicate counts, probes) that are not in the top-5 text at all; this is the likely reason for the gap, and it is an explanation, not a tested one. (c) Two small corpora, one stack, author-injected faults, many of which are blunt. (d) The result does not touch the ESCI main runs. **A stronger text baseline would need its own pre-registered amendment, and because this result motivates it, that amendment would be post-hoc and would have to say so.**
