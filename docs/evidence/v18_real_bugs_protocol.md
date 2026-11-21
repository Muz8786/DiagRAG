# v18: retrieval bugs reproduced from public issue reports. Pre-registration
Written 21 Nov 2026, 14:42 IST, before any v18 code ran. Kaggle only. Results freeze 23:00 IST.

**Why.** All earlier faults were injected or mutated. Production incidents are not available to us. The standard substitute in software testing is to reproduce real bugs exactly as they were reported in public issue trackers. We did that for retrieval bugs.

**Selection.** Web search of public issue trackers and write-ups (GitHub issues of RAG and retrieval libraries, 21 Nov 2026) for retrieval-quality bugs that return wrong results silently (not crashes) and whose mechanism can be reproduced on the main stack without new data. Nine were kept; the list was fixed before any run. Two are the same mechanism as a designed fault (B8 = R15, B9 = R22) and are reported separately. None of the seven others was used to design any detector, repair or the self-test.

| Id | Report | Mechanism reproduced | Stage |
|---|---|---|---|
| B1 | langgenius/dify#6097; e5 model card | query instruction prefix not sent to the encoder | dense |
| B2 | dorianbrown/rank_bm25#50; mem0ai/mem0#4884; mastra-ai/mastra#25928 | query tokenized differently from the index | sparse |
| B3 | langchain-ai/langchain#37046 | fusion accumulates the scores of chunks sharing one source id | fusion |
| B4 | milvus-io/milvus#53672 | reranker scores assigned to the wrong documents when one is not answered | rerank |
| B5 | getzep/graphiti#1720 | reranked list sorted ascending | rerank |
| B6 | castorini/pygaggle#67 | reranker runs but its order is not applied | rerank |
| B7 | run-llama/llama_index QueryFusionRetriever cache report (2026-10-03) | shared state: the previous query's scores reused | dense |
| B8 | facebookresearch/faiss#600 | IVF searched with the default nprobe = 1 (= designed R15) | dense |
| B9 | jenkinsci/resources-ai-chatbot-plugin#542 | BM25 and cosine scores added on raw scales (= designed R22) | fusion |

**Measurement** (script `v18_real_bugs.py`, inside the frozen-v6 harness). Each bug is applied system-wide on the untouched pipelines of seeds 74, 75, 76. Natural traffic = 600 of the 1,648 never-examined ESCI queries (md5 order). A bug is **harmful** if it breaks at least 1% of the natural queries that the clean pipeline answers. Self-test: 100 random probes with known answers (train clean successes); detection = any probe fails; localization = earliest pipeline stage whose output changes (golden trace); repair = roll back the localized component to its last verified version, retest, and roll back everything if probes still fail; accepted only if every probe passes. Baselines: per-query telemetry alarm (sign test on 100 test queries), the frozen deployed loop, the universal repair. A trial on seed 55 runs first; its numbers are not results.

**Pass rule (pooled over bug x seed units, harmful units only):** B-0 at least 5 distinct harmful bugs, else INSUFFICIENT; B-1 self-test detection >= 0.90; B-2 stage localization correct >= 0.80; B-3 repair verified >= 0.90, restores >= 95% of the broken natural queries and breaks <= 0.5% of the working ones. Reported, not in the rule: telemetry detection, queries fixed by the loop and by the universal repair, natural-traffic gain in Hit@5 points.

**What this is not.** These are reproductions of reported bugs on our stack, not incidents from a production system. Rollback assumes that a last verified version of each component exists, as in a normal deployment.
