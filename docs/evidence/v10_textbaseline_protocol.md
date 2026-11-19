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
