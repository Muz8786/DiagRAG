# LLM-based baselines — results (free-tier APIs)

Pre-registration, with three dated amendments: `docs/evidence/llm_baselines_plan.md` (committed at `6262973`, before any LLM call on this data).
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

| Arm | n (faulted / clean) | LLM AUROC [95% CI] | DiagRAG AUROC | DiagRAG − LLM [95% CI] | Verdict |
|---|---|---|---|---|---|
| Gemini 3.1 flash-lite | 320 (160 / 160) | 0.754 [0.702, 0.804] | 0.975 | **+0.222 [+0.173, +0.270]** | OURS_BETTER |
| Groq gpt-oss-120b, **partial** | 163 (79 / 84) | 0.731 [0.646, 0.805] | 0.975 | **+0.244 [+0.166, +0.331]** | OURS_BETTER |
| Groq gpt-oss-20b, **partial** | 169 (81 / 88) | 0.642 [0.566, 0.721] | 0.976 | **+0.335 [+0.255, +0.416]** | OURS_BETTER |

- **Partial** means the free daily token quota ended. The completed items are a random subset, because calls followed the frozen md5 order (amendment A1/A3).
- Cause-group accuracy on faulted episodes (LLM vs ours): Gemini 41.9% vs 80.9%, Groq-120b 17.7% vs 81.7%, Groq-20b 32.1% vs 80.8%. Chance for three
  groups is 33%. Our figure is a **lower bound**: families STALE and ENC have no single-letter group in the scoring script, so they count as wrong.
- Detection rate at 5% false alarm was also computed, but it is unreliable for verbalised scores. The LLMs output a few distinct values (for example 0.2 or 0.9),
  so ties at the threshold give 0% for Gemini and 0% for Groq-20b, and 11% for Groq-120b. Use AUROC.
- Tokens per item: 587 (Gemini), 673 (Groq-120b), 658 (Groq-20b). DiagRAG uses none.
- **Claim the pre-registered rule allows:** on this task, supervised telemetry diagnosis beat all three zero-shot LLM judges, with the LLM-judge AUROC at 0.64–0.75.

## B2 — repair on 300 never-examined natural queries

| Arm | Status |
|---|---|
| Gemini | analysed, n = 300, no excluded queries |
| Groq-120b, Groq-20b | **NOT_ANALYSABLE**: 31/149 and 34/154 graded queries had an incomplete rewrite step, above the 10% rule (A3) |

Gemini, paired change in Hit@5 versus no repair:

| System | Δ Hit@5 [95% CI] | Fixed / broken | LLM calls per query |
|---|---|---|---|
| CRAG-style | +0.99 pts [0.00, +2.33] | 3 / 0 | 1.15 (about 517 tokens) |
| DiagRAG deployed loop | +1.65 pts [0.00, +3.67] | 6 / 1 | **0** |
| Loop − CRAG-style | +0.66 pts **[−1.33, +2.67]** | | |

- The CRAG-style repair triggered on only 14.7% of queries and fixed 3 queries and broke none. DiagRAG repaired on more queries, fixing 6 and breaking 1.
- **Verdict: INCONCLUSIVE.** The lower bound (−1.33 points) is below the pre-registered non-inferiority margin (−0.5 points), so
  "our loop is non-inferior to a CRAG-style repair" is **not shown**. With 300 queries the interval is too wide to say more.
- What the data does support: both are small, positive and about equal, and DiagRAG reaches it with no LLM calls.

## Bottom line

- Shown: LLM judging of top-5 snippets is a weak diagnoser compared with telemetry (B1), by 0.22–0.34 AUROC, across three free-tier models.
- Not shown: that DiagRAG's loop repairs better than a CRAG-style LLM repair. The honest statement is "comparable on 300 queries, at zero LLM cost".
- Not tested: full RAGLog with its LLM checks and generated answers; the CRAG paper's evaluator; stronger LLMs; few-shot prompts.
