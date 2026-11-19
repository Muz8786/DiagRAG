# LLM-based baselines — results (free-tier APIs)

Pre-registration, with dated amendments A1 to A7: `docs/evidence/llm_baselines_plan.md` (committed at `6262973`, before any LLM call on this data).
**Status (regenerated from `kaggle/judged_llm_baselines/LLM_BASELINES_RESULT.json`): all three arms are complete.** An earlier version of this file showed the two Groq arms as partial (n = 163 and 169) and their repair arm as NOT_ANALYSABLE; that was superseded when the arms were finished (commit `6ef3c0e`). No frontier-model arm has been run (amendment A6).
Script: `bench/llm_baselines.py`. Raw LLM replies and results: `kaggle/judged_llm_baselines/`.

## What was compared

| | DiagRAG | LLM baseline |
|---|---|---|
| **B1 diagnosis** | attributor on retrieval telemetry, **supervised** on 2,718 labelled dev episodes, 0 LLM calls | an LLM sees the query and the 5 returned documents (title + 240 characters) and says how likely retrieval failed and where. **Zero-shot**, 1 call per item |
| **B2 repair** | deployed loop (detection-gated natural repairs + classifier at conformal thresholds), 0 LLM calls | CRAG-style: LLM grades the 5 documents; if none is relevant, it rewrites the query and the pipeline retrieves again |

Models: Gemini `gemini-3.1-flash-lite` (two keys), Groq `openai/gpt-oss-120b` and `openai/gpt-oss-20b`. Everything runs on the **v3 CPU seed-45** run,
so both systems see the same documents. Held-out episodes and never-examined natural queries only.

## What this is not

- **It is not full RAGLog** (no generated answer, no multi-stage logs, no trained classifier over LLM checks) **and not the CRAG paper**
  (no web search, no knowledge refinement, no fine-tuned evaluator). It is the narrower question "can an LLM looking at what the user sees tell that retrieval failed, and
  does an LLM-triggered rewrite fix it?"
- The comparison is **supervised telemetry vs zero-shot LLM**. The LLMs had no labelled fault examples; ours had 2,718. That favours us in B1.
- Free-tier models, one prompt each, no prompt tuning. Stronger models or few-shot prompts could do better.

## B1 — diagnosis (fault vs clean AUROC; paired bootstrap of the difference)

| Arm | n (faulted / clean) | LLM AUROC [95% CI] | DiagRAG AUROC | DiagRAG − LLM [95% CI] | Unparsed | Verdict |
|---|---|---|---|---|---|---|
| Gemini 3.1 flash-lite | 320 (160 / 160) | 0.754 [0.702, 0.804] | 0.975 | **+0.222 [+0.173, +0.270]** | 0 | OURS_BETTER |
| Groq gpt-oss-120b | 320 (160 / 160) | 0.701 [0.645, 0.753] | 0.975 | **+0.274 [+0.222, +0.332]** | 2 | OURS_BETTER |
| Groq gpt-oss-20b | 320 (160 / 160) | 0.629 [0.573, 0.682] | 0.975 | **+0.347 [+0.292, +0.402]** | 0 | OURS_BETTER |

- Cause-group accuracy on faulted episodes (LLM vs ours): Gemini 41.9% vs 80.9%, gpt-oss-120b 20.0% vs 80.9%, gpt-oss-20b 33.1% vs 80.9%. Chance for three groups is 33%. Our figure is a **lower bound**: families STALE and ENC have no single-letter group in the scoring script, so they count as wrong.
- Detection rate at 5% false alarm was also computed, but it is unreliable for verbalised scores (few distinct values, ties at the threshold): Gemini 3.1 flash-lite: 0.0%, Groq gpt-oss-120b: 8.8%, Groq gpt-oss-20b: 0.0%. Use AUROC.
- Tokens per item: Gemini 3.1 flash-lite: 587, Groq gpt-oss-120b: 681, Groq gpt-oss-20b: 661. DiagRAG uses none.
- **Claim the pre-registered rule allows:** on this task, supervised telemetry diagnosis beat all three zero-shot LLM judges (LLM-judge AUROC 0.63 to 0.75). This favours DiagRAG by design: it was trained on labelled episodes and the LLMs were not.

## B2 — repair on never-examined natural queries

Paired change in Hit@5 versus no repair, in points [95% CI]. "Loop − CRAG-style" is the pre-registered contrast; the non-inferiority margin is −0.5 points.

| Arm | n | CRAG-style | DiagRAG loop | Loop − CRAG-style | CRAG fixed / broken | Loop fixed / broken | CRAG triggered | LLM calls per query (CRAG) | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| Gemini 3.1 flash-lite, 1,000 queries | 1000 | +0.99 [+0.30, +1.80] | +2.22 [+1.10, +3.40] | **+1.23 [-0.10, +2.60]** | 13 / 3 | 27 / 5 | 13.3% | 1.13 | OURS NON INFERIOR |
| Gemini, first 300 only | 300 | +0.99 [+0.00, +2.33] | +1.65 [+0.00, +3.67] | **+0.66 [-1.33, +2.67]** | 3 / 0 | 6 / 1 | 14.7% | 1.15 | INCONCLUSIVE |
| Groq gpt-oss-120b | 300 | +0.33 [-0.67, +1.67] | +1.65 [+0.00, +3.67] | **+1.32 [-0.67, +3.67]** | 2 / 1 | 6 / 1 | 22.0% | 1.22 | INCONCLUSIVE |
| Groq gpt-oss-20b | 300 | +0.67 [-0.67, +2.00] | +1.65 [+0.00, +3.67] | **+0.98 [-1.33, +3.33]** | 3 / 1 | 6 / 1 | 24.0% | 1.24 | INCONCLUSIVE |

- **Gemini, 1,000 queries: OURS_NON_INFERIOR.** The lower bound (−0.10 points) is above the −0.5 margin, so the loop is not shown to be worse than a CRAG-style repair. It is **not shown to be better**: the interval includes zero.
- The first 300 queries alone gave INCONCLUSIVE (lower bound −1.33 points); widening to 1,000 queries was amendment A4, made before the new calls.
- **Both Groq arms are INCONCLUSIVE** on 300 queries (intervals too wide for either claim). No query was excluded for an incomplete rewrite step in the final analysis.
- The loop makes **zero** LLM calls; the CRAG-style repair makes about 1.1 to 1.2 calls per query.

## Bottom line

- Shown: LLM judging of the top-5 snippets is a weak diagnoser compared with telemetry (B1), by 0.22 to 0.35 AUROC, across three free-tier models.
- Shown (Gemini, 1,000 queries): the loop is non-inferior to a CRAG-style LLM repair, at zero LLM calls. Not shown: that it repairs better.
- Not tested: full RAGLog with its LLM checks and generated answers; the CRAG paper's evaluator; **a frontier model** (amendment A6: none was reachable on the supplied keys; a flash-class model is not called frontier); few-shot or telemetry-fed LLMs.
