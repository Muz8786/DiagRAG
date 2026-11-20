# v13 dataset freeze (19 Nov 2026, before any v13 run)

The three datasets of the v13 judged runs are frozen here. No dataset is added, dropped or swapped after this point; a run that fails is reported as failed or not run.

| Dataset | Role | Source | Size and integrity | Contents (checked 19 Nov 2026) | Faults | v13 judged seed |
|---|---|---|---|---|---|---|
| **Amazon ESCI** (+ licence-clean corpus, ShopNova partition) | Product search; the only corpus with all 32 faults; natural-traffic test | `data/DATA_MANIFEST.md` (Drive IDs, SHA-256 checked by the frozen v6 code) | as in the manifest | 101,297 documents; 1,648 never-examined natural queries | 32 | **59** |
| **NQ** (BEIR) | Open-domain QA over Wikipedia; the core RAG benchmark; scale | `https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nq.zip` | 498,307,926 bytes; SHA-256 `2553bf7bfbab47b1436ca00a34bce57320e18e611fd00999a2a3a1b4714be752`; md5 `d4d3d2e48787a744b6f6e691ff534307` = the BEIR-published md5 | 2,681,468 passages (0 duplicate ids, 507 with empty text, mean 472 characters); 3,452 test queries, all with a positive qrel; 4,201 qrels rows, 0 pointing to missing passages | 20 | **58** |
| **FiQA-2018** (BEIR) | Financial QA; a standard RAG evaluation set | `https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/fiqa.zip` | 17,948,027 bytes; SHA-256 `32c7df99ed21252fdfb2cf3f5673502a8d245ee0c44c4a133570d92ce2b3ad02` (the frozen value the code asserts at download) | 57K documents (as judged in `kaggle/judged_port2_fiqa/`) | 20 | **60** |

Licences: ESCI Apache-2.0 (ShopNova unassigned, not released); NQ CC BY-SA 3.0; FiQA per its original release. Nothing is redistributed: NQ and FiQA are downloaded at run time and checked.

**Replaced before any run:** CQADupStack was chosen first and dropped on 19 Nov 2026 before any run used it. Its first download stopped at 1,742,340,096 of 5,343,728,040 bytes and failed the md5 check; the owner then chose FiQA. No CQADupStack result exists.

**Fault coverage.** All 32 faults on ESCI. On NQ and FiQA the 20 faults that can occur in any corpus (Q01, Q03, Q04, Q05, K04, K05, K08, R01, R03, R05, R07, R10, R11, R13, R15, R19, R22, R23, R24, R25). The other 12 need tenant, versioning, product or deletion metadata that open corpora do not have, or (Q02, Q09, C2) port-stack features that are not built. Cross-dataset claims are made only on the 20 shared faults.

**Code for NQ and FiQA.** `kaggle/diagrag_port5.py`, generated from the frozen `diagrag_port4.py` by `kaggle/mk_port5.py` (three declared edits: NQ in the verified-download table, output folder name, and an execution-only fix to corpus embedding). The frozen port5 hash is `916c3864282b1d9c168cce6943340b52d8728334c3c960d33fcb0d2d4224294f`.
Equivalence check (`docs/evidence/v13_port5_equivalence.py`, NFCorpus, seed 905, tiny settings, 4 threads, sandbox CPU): port5 and port4 give **identical** embeddings, verdict and every per-fault table, both when run straight through and when port5 is stopped after its first chunk and resumed.

**Trials (development seeds, tiny query settings; their numbers are not results and are not used to tune anything):** NQ seed 906 (full 2.68M-passage corpus, to measure memory and time), FiQA seed 907, ESCI seed 908 (after the two ideas are built).

**Data source note (20 Nov 2026, 00:00 UTC, before any v13 result).** The BEIR download server (`public.ukp.informatik.tu-darmstadt.de`) did not respond from Kaggle or from the sandbox from about 18:30 UTC on 19 Nov, so both first trials stopped at the download step (curl exit 28) before any computation. The data are now attached to the Kaggle runs as private Kaggle datasets holding the byte-identical zips (stored with a `.bin` suffix because Kaggle unpacks `.zip` uploads); a staging cell outside the frozen code copies them into place, and the frozen code checks size and SHA-256 itself.
- NQ: the zip downloaded from BEIR on 19 Nov 2026 (checks above).
- FiQA: fetched unmodified from the Internet Archive snapshot of the BEIR URL (`web.archive.org/web/20250504011332id_/...fiqa.zip`; the archive lists six captures from 2022 to 2025 with one content digest). It matches the frozen size (17,948,027 bytes), the frozen SHA-256 and the BEIR-published md5 `17918ed23cd04fb15047f73e6c3bd9d9`; the zip CRC check passes. It is therefore the same file the judged port2 FiQA run used.
- A repacked FiQA copy on Kaggle (`hamzaidmoudi/fiqa-2018`, different checksum) was **not** used.
