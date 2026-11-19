# v11.b protocol (pre-registration). Written 19 Nov 2026. NOT RUN. It starts only after the owner says v11.a is done; no LLM call has been made for it and no key is stored in any file.

## 0. What v11.b is
The free-tier LLM diagnosis comparison (B1 of `docs/evidence/llm_baselines_plan.md`) repeated on **other corpora**: the v9 port corpora (NFCorpus, ArguAna) and, if v11.a produced it, SCIDOCS. The question is the narrow one of B1: can an LLM, shown the query and the five returned documents, tell that retrieval failed, compared with the telemetry attributor on the **same held-out episodes**? It is **additive and descriptive**. It changes no detector, repair, gate or frozen file, and it does not touch the ESCI B1 or B2 results.

## 1. What is fixed
- **Script:** `bench/llm_baselines.py`, SHA-256 `fdb1ea25c6c330cb91f762b5625fcf105f7c68695f6deba5e7cc24b80edb7327`, **unchanged**. Only its `llm` and `analyze` stages are used, with `--out`, `--private`, `--ours-csv` pointing at v11.b folders. The prompts (`DIAG_PROMPT`), the parser, the temperature (0), the call order (md5 of `2026|order|id`), the bootstrap (2,000 resamples) and the verdict rule are the script's. **B2 (CRAG-style repair) is not run**: the port arms have no natural-traffic sample.
- **Arms (same as the ESCI B1):** Gemini `gemini-3.1-flash-lite`, Groq `openai/gpt-oss-120b`, Groq `openai/gpt-oss-20b`. Free tier only. No frontier arm: the Vercel gateway key has a balance of 0.
- **Keys:** read only from the environment (`GEMINI_API_KEYS`, `GROQ_API_KEY`, comma-separated), supplied by the owner at run time, never written to a file, cache, commit or log, and the owner is advised to rotate them afterwards. The v11 verifier scans for secret-looking strings.
- **Samples (frozen by hashing, no choice after seeing results):** per corpus, up to **5 held-out faulted episodes per fault** plus **160 held-out clean episodes**, each ordered by `md5(2026|bid|fault)` (the script's own rule). Each corpus is analysed separately.
- **Inputs:** built from the replay of the frozen retrieval (`docs/evidence/v10_textview.py`, replay check at least 99.5%, already passed for NFCorpus and ArguAna). A document is shown as `title` (the text up to the first ". ", at most 120 characters) and `snip` (the next 240 characters), the same shape as the ESCI inputs. The replayed text is BEIR text and is **not committed**; only counts, ids and results are.
- **Telemetry reference:** the attributor of `docs/evidence/v10_textbaseline.py` (v6 settings), fault-vs-clean score `1 - P(NONE)`, trained on the corpus's own training episodes.
- **Verdict rule (the script's):** paired bootstrap of AUROC(telemetry) minus AUROC(LLM); OURS_BETTER if the lower bound is above 0, OURS_NON_INFERIOR above -0.02, LLM_BETTER if the upper bound is below 0, else INCONCLUSIVE. A combined claim ("telemetry diagnosis is non-inferior to LLM diagnosis on these corpora") needs OURS_BETTER or OURS_NON_INFERIOR in **every analysed arm on every analysed corpus**, partial arms included (the stricter rule of amendment A1). Any claim names the arms and corpora it covers.
- **Quotas:** free daily quotas can stop an arm early. A stopped arm is analysed on the completed items, which are a random subset because the call order is the frozen md5 order, and is labelled PARTIAL with its n (amendments A1 and A3 of the LLM plan). No item is dropped or reordered.

## 2. Predictions (my judgements; written so they can fail)
- Telemetry beats every LLM arm on NFCorpus and on ArguAna (lower bound above 0): about 0.7. The ESCI result was OURS_BETTER in all three arms (+0.22 to +0.35), but these corpora have blunt faults that an LLM may also see (empty or duplicated top-5), so the gap may be smaller.
- LLM AUROC on these corpora within 0.1 of its ESCI value (0.63 to 0.75): about 0.5.
- The LLM judges name the fault group (Q, K or R) correctly less often than telemetry: about 0.9.
- At least one Groq arm ends PARTIAL because of its daily quota: about 0.6.

## 3. What a result would and would not show
- It tests free-tier zero-shot judges on two or three small corpora, one stack, author-injected faults, 25 held-out positives per fault. Intervals will be wide.
- It does not answer the frontier-model objection; the A4.3 arm needs a funded key.
- It is compared with the telemetry attributor, which is **supervised**; the judges are **zero-shot**. The supervised text baseline of `v10_textbaseline_protocol.md` is the like-for-like supervised comparison.

## 4. How the owner runs it (after v11.a)
1. Replay the episodes of each corpus with `v10_textview.py` (or reuse the existing view files).
2. Build `llm_inputs.jsonl`, `llm_diag_labels.jsonl` and the telemetry CSV with a builder script that this protocol allows and that is committed before the first call.
3. Provide the keys as environment variables for the command only; run `llm` in chunks until each arm finishes or its quota ends; run `analyze`.
4. File the result and a scorecard against section 2 as an amendment below, written after the results, with sections 0 to 3 unedited.

## 5. Amendments
(none yet; each is dated and filed before the result it concerns is read)
