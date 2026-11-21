# Data manifest — verify before any run

Files below are NOT in this repo (too large for a text push).
Fetch them separately, then check size, and hash where given,
before running anything.

## Corpus and embeddings (spine, never delete the embeddings cache)

- kb_tier3_186k.jsonl.gz — 186,290 docs, exactly 53,518,791 bytes.
  Drive file "kb e shop.gz", Drive ID 1zksoRmKjBn3VKRweFM1pLfDDNAIpnzxm
  (21 Oct 2026 copy, gzip-verified; use this ID for gdown).
  Second Drive copy exists (ID 1gN6jMNOsT1KGBEFMJ8DZCLupy92TEIRQ,
  20 Oct 2026) — do not confuse the two.
- embeddings_cache_186k.npz — (186290, 768) float32, exactly
  533,012,659 bytes, doc_ids match the corpus exactly in order,
  unit row norms, 0 NaNs, 0 zero rows. Drive ID
  1xKaTyYx3qxFFzmRYQQuPmLnKEtygNx2s.
- benchmark_1000_multidomain.xlsx — exactly 419,917 bytes.

Kaggle note: Kaggle dataset ingestion decompresses .gz files, so
the working corpus route on Kaggle is Drive gdown, never a dataset
upload of the .gz. Kaggle editor has no working-directory file
upload in the new editor; the workable transport for small runners
is a temporary private Kaggle dataset, with byte-identical copy
plus size, hash and py_compile verification before running, and
deletion of the temporary dataset after outputs are secured.

## Verification run, 14 Nov 2026 (downloaded signed-out, checked byte by byte)

| File | Bytes | SHA-256 | Source |
|---|---|---|---|
| kb_tier3_186k.jsonl.gz | 53,518,791 (matches) | 5a9f7ea6ae5b8a3e7f1e1ca6e2838dddd6158efb9384d757c6aa755dbe9bda3c | Drive 1zksoRmKjBn3VKRweFM1pLfDDNAIpnzxm |
| embeddings_cache_186k.npz | 533,012,659 (matches) | 3b43603d9689f7c0eee0cbfebdb8b5cfddd05a2fc4e3cf192c8eed1de4a88835 | Drive 1xKaTyYx3qxFFzmRYQQuPmLnKEtygNx2s |
| shopping_queries_dataset_examples.parquet | 51,286,808 | 4a735b693b4a424a6fc67f5be6e4c811495c488bbf66d02a602d308b2744263a | github.com/amazon-science/esci-data (LFS) |
| corpus-webis-qspell-17.zip | 2,285,705 | f13bd165544ab2ac75d63de4334feb86d74d1b3dfbe48d79423133552b5054e4 | zenodo.org/records/3570912 |

Not reachable signed-out: the second corpus copy (Drive 1gN6jMNOsT1KGBEFMJ8DZCLupy92TEIRQ,
gdown permission error), the benchmark xlsx (no Drive ID published), and the private
Kaggle banks. None of these is needed by `kaggle/diagrag_core28.ipynb`.

Passed:
- gzip integrity, 186,290 docs, one schema, 186,290 unique doc_ids, 0 empty contents.
- Cache: (186290, 768) float32, 0 NaN/Inf, 0 zero rows, norms 0.9999999–1.0000001,
  doc_ids identical to the corpus in order.
- Re-encoding 43 docs (40 random + 3 fixed) as `title + "\n" + content` with bge-base-en-v1.5 gives
  cosine 1.0000 to the cache (min 1.0000). Content alone gives 0.946, so the cache text is title + content.

Purity issues found (the notebook handles each one as noted; the corpus file is not modified):
- 2,558 rows are exact-content duplicates beyond the first (1,537 groups). The `duplicate_text`
  flag marks 2,541 rows. 68 duplicate groups have 2 or more unflagged members, and 45 flagged
  rows have no exact twin. Handling: gold-equivalence includes exact-content twins.
- 533 identical embedding rows beyond the first. These are the duplicate texts.
- 36 ASINs exist as both an ESCI doc and an ABO doc. Handling: gold-equivalence includes the twin.
- 3,554 ESCI chunks have `char_end - char_start` ≠ `len(content)`. This is metadata only
  (overlapping chunk spans after whitespace trimming) and does not affect retrieval.
- 3,993 docs carry pandas `nan` placeholders ("Brand: nan", "Description: nan"). The K08
  fault and its repair are built around this real pattern.
- 2 rows contain U+FFFD (ESCI-us-B07YCW6269-c01/-c02).
- Licences: ABO has 84,993 rows `conflicting_unverified` and 86,566 `verified`. The 1,040
  ShopNova synthetic rows are `unassigned`. Resolve both before any public release of
  derived data.
- ESCI queries: 459 query strings repeat under different query_ids, and 161 strings occur
  in both the official train and test splits. Handling: the notebook dedupes by string and
  splits by gold-product component (union-find), and it asserts zero gold leakage between
  its own train and test splits.

## Banks (telemetry only, no document text)

- ESCI bank: loop_features_qml100k_wave1.npz, 24,000 x 31,
  train 16,000 / test 8,000, zero overlap. On Kaggle account
  muzammilveil99, in private dataset "qml-banks" — NOT
  "diagrag-banks" (that dataset does not exist on that account).
- SecureBank bank: loop_features_securebank_s42.npz.
- TeleCall bank: loop_features_telecall_s42.npz.
- SciFact GPU bank: loop_features_scifact_gpu.npz, 8,872 x 31
  (31 features, does not drop into the 29-feature CPU federation).

## Runner and result hashes (checked 1 Nov 2026)

- code/closed_loop_gpu_v7_eud.py — base EUD runner, do not edit.
- code/closed_loop_gpu_v8_seq.py — 86,595 bytes, sequential runner.
- code/m1_gpu_kaggle.py — SHA256
  495b4457aa1756ba91138fc4e5903cd2f78fa2b74ce8dc068892daada0b2e6bd,
  77,255 bytes.
- code/cpu_batch_kaggle_v2.py — SHA256
  ee5fa23d6433ea1c9279c75b340cbb325a1364f4332f518485e3dc82d26bdd9a.
- code/interaction_kaggle.py — SHA256
  d62b696ce45c92cb9f0785485a4ce5aa6c62aed3ce43ad492a4e5d8736aa8de0.
- code/b2_loco_kaggle.py — SHA256
  826e5e48948c212b4aed380e5f790b530b8fbb1d4acb1615a10fc8803f27e838,
  corrected runner only (reorder by feature name, assert set equality).

## Licences (verified at publisher, not from tags)

ESCI repo Apache-2.0 (code); ABO CC BY 4.0; FinQA MIT;
TeleCall CC BY-SA 4.0 (SE CC BY-SA version varies by contribution
date — check per contribution before any derived-bank release);
SciFact annotations CC BY 4.0, abstracts ODC-By 1.0;
Webis-QSpell-17 CC BY 4.0.
