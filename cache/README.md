# Cache

Cache files are NOT in Git. They are listed here so a
replicator can fetch and verify them, exactly as in
`data/DATA_LINKS.txt` and `data/DATA_MANIFEST.md` in the
replication package.

- embeddings_cache_186k.npz — (186290, 768) float32,
  exactly 533,012,659 bytes, doc_ids match the corpus
  exactly in order, unit row norms, 0 NaNs, 0 zero rows.
  Drive ID 1xKaTyYx3qxFFzmRYQQuPmLnKEtygNx2s.
  NEVER delete the original cache. Deletion only after
  upload verifies, with an exact list shown, and user
  confirmation — and never for this cache or for live
  boost fold caches.
- Corpus kb_tier3_186k.jsonl.gz — 186,290 docs,
  exactly 53,518,791 bytes. Drive ID
  1zksoRmKjBn3VKRweFM1pLfDDNAIpnzxm.
- Benchmark benchmark_1000_multidomain.xlsx —
  exactly 419,917 bytes.

On Kaggle, fetch the corpus by Drive gdown, never by a
dataset upload of the .gz, because Kaggle dataset
ingestion decompresses .gz files.
