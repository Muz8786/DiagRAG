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

**A2 — B2 incomplete procedures (made before any metric was computed; only call counts had been seen).**
- A natural query whose grade says "no relevant document" but whose rewrite call or rewrite retrieval never ran (provider quota) is **excluded** from that arm's B2
  and counted in `excluded_incomplete_procedure`. Before this amendment such a query would have been scored as "unchanged", which would handicap the baseline.
  The paired comparison with the DiagRAG loop uses the same retained queries.
- Script SHA-256 after A2: `aa8980093a7ae8df539b4f64cedac58aa5f38771c9ffd6ca9855914ad3a23582`.

**A3 — partial arms (made before any metric was computed; the only things seen were call counts and quota messages).**
- Both Groq models hit their free daily token limits: `gpt-oss-120b` at 312/620 and `gpt-oss-20b` at 323/620 hash-ordered calls. Gemini finished 620/620 and all rewrite calls.
- **B1** is analysed for every arm on its completed items (a random subset, because the call order is the frozen md5 order). Each arm's n is printed next to its AUROC.
- **B2**: an arm is analysed only if at most 10% of its graded natural queries are excluded under A2. Otherwise it is reported as NOT_ANALYSABLE with the counts.
  Reason: the excluded queries are exactly those where CRAG-style repair would act, so dropping them would test the baseline on the queries where it does nothing.
  The Groq arms did not reach their rewrite calls, so B2 is expected to be NOT_ANALYSABLE for them and is judged on Gemini only.
- **Claim wording.** Any combined claim names the providers it covers. No claim is made about a provider whose arm is not analysable.
- Script SHA-256 after A3: `3aa855222550fc9bd89224553a8553812e55ab431ba3b5476fb01ab4791e78d2`.

**A4 — widen B2, finish the Groq arms, add a frontier arm (16 Nov 2026, before any new LLM call; the existing results were read, nothing new was).**
Why: the B2 interval on 300 queries ([-1.33, +2.67] points) cannot resolve the -0.5 point non-inferiority margin; two Groq arms are partial; and the standing objection to B1 is that the judges were free-tier models.
- **A4.1 Finish the Groq arms.** Resume `groq` (gpt-oss-120b) and `groq20` (gpt-oss-20b) from their caches in the frozen md5 order when their daily quotas have reset. No prompt, sample or rule changes. The A3 rule governs: more than 10% incomplete => B2 NOT_ANALYSABLE. Groq arms stay on the **first 300** natural queries.
- **A4.2 Widen B2 for Gemini and the frontier arm.** The natural sample grows from 300 to **1,000** never-examined queries (the 1,648 of the v3 run, excluding `natural_exclusions_v2.json`, which the run already respects). It is a **prefix extension** of the same frozen md5 order (seed 2026): ranks 0 to 299 are the original sample, ranks 300 to 999 are new, so nothing already read is replaced.
  New inputs go to `llm_inputs_ext.jsonl`; `llm_inputs.jsonl` is never rewritten. Same prompts, same margin (-0.005 on Hit@5, i.e. -0.5 points), same verdict rules and same 10% rule. The analysis reports the extended B2 and, for continuity, `B2_first300` (which must equal the committed result).
  Natural-query inputs for ranks 300 to 999 come from the same v3 CPU seed-45 run, so both systems see the same documents.
- **A4.3 One frontier arm (B1 judge and B2 grader).** Zero-shot, same prompts, same items, temperature 0, one model chosen by the owner. The provider, model and per-million-token prices come from environment variables (`FRONTIER_PROVIDER`, `FRONTIER_MODEL`, `FRONTIER_PRICE_IN`, `FRONTIER_PRICE_OUT`, `FRONTIER_BASE_URL`); the key only from `FRONTIER_API_KEY`.
  **Hard spend cap USD 15**, set in the provider console before the first call and also enforced by the script before every call from cumulative cost recorded in the cache (checked across resumed chunks; it can overshoot by at most one call). Call order: all B1 diagnosis items first (frozen md5 order), then natural grading in rank order, then rewrites,
  so a capped arm still yields a complete B1. If the cap stops it before B2 finishes, B2 is analysed under the A3 10% rule on the completed prefix only if the stated rule is met; otherwise it is NOT_ANALYSABLE.
  Reported beside every metric: tokens and **USD per item** and **per natural query**, taken from the provider's reported usage times the stated prices.
- **A4.4 Claim rules (unchanged in kind, extended in scope).** A combined claim must name the arms it covers and needs OURS_BETTER or OURS_NON_INFERIOR in every analysed arm, **including the frontier arm**. If the frontier arm is LLM_BETTER or INCONCLUSIVE on B1, that is reported as the headline of the section and the cost comparison (USD per item against zero LLM calls for DiagRAG) is the fallback statement, with the measured numbers. Wording stays RAGLog-style and CRAG-style; "full RAGLog" and "the CRAG paper" appear only in the what-this-is-not paragraph.
- **A4.5 What is still not tested.** Full RAGLog with its own LLM checks and generated answers, the CRAG paper's trained evaluator and web search, few-shot prompts, and any model other than the four named here.
- No LLM call has been made under A4. Environment on 16 Nov 2026: none of `GROQ_API_KEY`, `GEMINI_API_KEYS`, `FRONTIER_API_KEY` is set, so the Groq/Gemini resumption and the frontier arm wait for the owner to provide keys as environment variables.

**A5 — script changes made under A4 (16 Nov 2026, before any new call).** Added: the `extend` stage (no key needed), the `frontier` provider with spend accounting and the hard cap, per-provider natural limits, a `B2_first300` continuity variant, USD fields. Nothing in a prompt, a sample rule, a parser or a verdict rule changed.
Checks: (1) on the existing data the new script reproduces **every previously committed number** (0 fields differ in value or type; the only changes are the new fields `usd_per_item`, `usd_per_query` and the `B2_first300` block, which equals the committed B2 exactly); (2) the frontier adapter, both API styles, the cap across resumed chunks and the no-key skip were exercised against a local mock server (no real key, no spend).
Script SHA-256 after A5: `fdb1ea25c6c330cb91f762b5625fcf105f7c68695f6deba5e7cc24b80edb7327`.
