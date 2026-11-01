# Models

No model weights are committed in this repo. Weights are
downloaded automatically on first run from Hugging Face.
That keeps the repo small and the versions explicit.

- bge-base-en-v1.5 — dense encoder for the GPU retrieval stack.
- bge-reranker-large — cross-encoder reranker, after RRF k=60,
  depth 25, in the GPU stack.
- BM25 + TF-IDF — CPU substitute stack, used for the CPU
  lineage domains (SecureBank, TeleCall, SciFact CPU) and
  for the CPU bank tests. Do not mix CPU-substitute numbers
  with GPU-stack numbers without labelling the stack.
- HistGB (Histogram Gradient Boosting) — the loop attributor,
  per factor, not LogReg. LogReg appears only in the bagged
  attributor and in QML controls, never as the loop attributor.
- IsotonicRegression — M1 subtype calibration only, no Platt
  fallback in the frozen M1 spec.
- T5-large (CRAG evaluator) — NOT in this project. It is a
  Gap 1 external-baseline gate candidate only, and its
  checkpoint is [UNVERIFIED] until it is located, hashed,
  and smoke-tested. Do not call a plain t5-large "CRAG".
