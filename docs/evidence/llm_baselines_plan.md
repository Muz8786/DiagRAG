# Pre-registration: LLM-based baselines (written and committed BEFORE any LLM call on this data)

Script: `bench/llm_baselines.py`, SHA-256 `8fb9c6cf3b82296620a89c588407f7de4b6060aeb7d7afac1f33619ba55714bb`. The prompts, sample sizes, models, parsing rules and verdict rules below are frozen
inside that script. If the script has to change after the first LLM call (for example a parsing bug), the change is listed under
"Amendments" at the bottom with the new hash, and no result is read before it is listed.

## What is compared, and why this is a fair-but-limited comparison
- Our side is the **v3 CPU seed-45 judged run** (`kaggle/judged_cpu_run_v3_seed45/`), MiniLM-L6 reranker, because the LLM baselines need the same
  documents the pipeline returned, and re-running them on the GPU stack would not be a paired comparison. The GPU run is reported separately.
- **B1, diagnosis (a RAGLog-style retrieval-stage check).** An LLM sees the query and the five returned documents (title + 240 characters) and returns
  P(failed) and a cause group. This is **not** the full RAGLog system: it has no generated answer, no reference answer, no multi-stage logs
  and no trained classifier. It tests the narrower question "can an LLM, looking at what a user would see, tell that retrieval failed?"
- **B2, repair (a simplified CRAG).** The LLM grades the five documents; if none is relevant, it rewrites the query and the pipeline retrieves again.
  No web search, no knowledge refinement, no fine-tuned evaluator. It is a diagnosis-by-LLM, repair-by-rewrite baseline.
- Free-tier models: Groq `openai/gpt-oss-120b` and Gemini `gemini-3.1-flash-lite` (two API keys). They are not the models the original
  papers used. Temperature 0. A single prompt per task, no prompt tuning.

## Samples (fixed by hashing; no choice after seeing results)
- B1: up to 5 held-out episodes per fault (every fault incl. new ones) + 160 held-out clean episodes, ordered by md5(seed|id), seed 2026.
- B2: 300 natural queries from the 1,648 never-examined queries of the v3 run, ordered by md5(seed|query), seed 2026.

## Metrics and verdict rules (each per provider)
- **B1**: AUROC (fault vs clean) of the LLM's p_fail and of the DiagRAG attributor (`bench/baseline_track1.py` scores for the same episodes), and
  the paired bootstrap (2,000 resamples) of AUROC_ours - AUROC_LLM.
  OURS_BETTER if the 95% CI lower bound > 0; OURS_NON_INFERIOR if > -0.02; LLM_BETTER if the upper bound < 0; else INCONCLUSIVE.
  Also reported: detection rate at 5% false alarm, cause-group accuracy on faulted episodes, tokens per item. Unparsable answers get p_fail = 0.5 and are counted.
- **B2**: paired change in Hit@5 after repair, for CRAG-style and for the DiagRAG deployed loop on the same queries, and loop minus CRAG-style (bootstrap).
  OURS_BETTER if the lower bound > 0; OURS_NON_INFERIOR if > -0.005; LLM_BETTER if the upper bound < 0; else INCONCLUSIVE.
  Also reported: fixed/broken counts, LLM calls and tokens per query (ours: 0).
- **Combined claim rule.** "Telemetry diagnosis is non-inferior to LLM diagnosis" is made only if B1 is OURS_BETTER or OURS_NON_INFERIOR
  for **both** providers. "Our loop is non-inferior to CRAG-style repair" likewise for B2. Anything else is reported as not shown.
- Small samples (about 315 and 300 items) give wide intervals. INCONCLUSIVE is a possible and acceptable outcome.

## Amendments
**A1 — Groq daily token quota (made after seeing only call counts and that every reply contained a JSON object; no metric was computed).**
- Groq `gpt-oss-120b` exhausted its free daily token budget at 312 of 620 hash-ordered calls. Its arm is analysed on the **completed subset**, which is a
  random sample because the call order is the frozen md5 order, and it is labelled PARTIAL with its n.
- A further Groq arm, `groq20` = `openai/gpt-oss-20b` (same prompts, same key, separate quota), is added and run until its quota ends. It is labelled PARTIAL if it does not finish.
- **Claim rule, stricter than before:** a combined claim needs OURS_BETTER or OURS_NON_INFERIOR in **every** analysed arm (Gemini, Groq-120b, Groq-20b), including partial ones.
- Script SHA-256 after the amendment: `5f9077f6744d8f6e45540777e19ed03eb627a2998f0528792353ad3e3dc7b173`. Gemini finished all 620 calls before the amendment, and its prompts and parsing are unchanged by it.
