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
