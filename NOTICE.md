# Third-party data and software used by DiagRAG

| Component | Source | Licence (as stated by the publisher) | How it is used |
|---|---|---|---|
| Amazon ESCI (Shopping Queries Dataset) | github.com/amazon-science/esci-data | Apache-2.0 | queries, Exact labels, product text (corpus partition `real_world_apache_esci`) |
| Amazon Berkeley Objects (ABO) | amazon-berkeley-objects.s3.amazonaws.com | CC BY 4.0 per the current project page | product text; **only rows with `license_status = verified`**. The 84,993 `conflicting_unverified` rows are excluded from v3 and from DiagRAG-Bench |
| Apache OFBiz user manual | ofbiz.apache.org | Apache-2.0 | software-documentation partition |
| Webis-QSpell-17 | zenodo.org/records/3570912 | CC BY 4.0 | real misspellings and edit-type distribution for Q04 |
| ShopNova synthetic corpus | this project | **unassigned — the owner must assign a licence before public release** | tenants, policies, product codes |
| BEIR SciFact, BEIR FiQA-2018 | public.ukp.informatik.tu-darmstadt.de/thakur/BEIR | per the original datasets; **not redistributed** | portability arms download them at run time |
| RAGLog | github.com/hiraa221/raglog, commit 7f7d0686 | Apache-2.0 | tier-0 feature extractor used as an external detection baseline (cloned at run time, not vendored) |
| SymSpell (symspellpy) and its English frequency dictionary | github.com/mammothb/symspellpy | MIT | external spelling-correction baseline |
| wordsegment | github.com/grantjenks/python-wordsegment | Apache-2.0 | external segmentation baseline |
| bge-base-en-v1.5, bge-base-en, bge-small-en-v1.5, bge-reranker-* | huggingface.co/BAAI | MIT | encoders and rerankers |
| e5-small-v2, e5-small | huggingface.co/intfloat | MIT | stack 2 encoder; model-drift fault |
| all-mpnet-base-v2, all-MiniLM-L6-v2, ms-marco-MiniLM-L-6-v2 | huggingface.co/sentence-transformers, cross-encoder | Apache-2.0 | drift fault, RAGLog embeddings, CPU reranker |
| LangChain (langchain-core, langchain-community) | github.com/langchain-ai | MIT | framework-stack arm |
| Google Gemini API (`gemini-3.1-flash-lite`, free tier) | ai.google.dev | service terms apply | LLM baselines in `bench/llm_baselines.py`: receives a query and 5 document snippets from the licence-clean corpus. API keys are read from environment variables and are never stored in the repo |
| Groq API (`openai/gpt-oss-120b`, `openai/gpt-oss-20b`, free tier) | console.groq.com | service terms apply; the gpt-oss model weights are published by OpenAI under Apache-2.0 | same use as above |

Before any public data release:
- Verify each licence at its source; this table repeats what the publishers state.
- Assign the ShopNova licence.
