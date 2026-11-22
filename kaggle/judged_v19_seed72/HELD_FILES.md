# Files held from this push (too large for git)

These two outputs of the Kaggle run `sqmuzammil/diagrag-v19-judged72`
(run completed 2026-11-21) exceed GitHub's 100 MB file limit and are
NOT in this folder. They remain in the kernel's output on Kaggle.

| File | Bytes | SHA-256 |
|---|---|---|
| `diagrag_out/checkpoint.pkl` | 290,677,974 | `a6f21a7eaa85e4d2d27b498c467b59c79e672a23aa0e4663fa89e425c4192a4a` |
| `diagrag_out/qlog_nn_b03a9b172742.npy` | 277,002,368 | `cd63d9107561bd71c6cb0bb1617200e03f0459ad94f2ea63c1e440497ef85064` |

Everything else from the run's output (27 files listed, 25 pushed)
is in this folder with content byte-identical to the Kaggle output
(hashes verified at download time). Two are stored wrapped because
the push path is text-only with a 16 MiB per-file limit:
`code/__pycache__/v19_two_channel_u1.cpython-313.pyc` as `.pyc.b64`
(base64), and `diagrag_out/episodes.jsonl` (17,001,044 bytes,
sha256 `e88f532d22f9a2dd2210f41f2ab8ae0e8fc5664269a6f1edcf8977cb4835ec2e`)
as `episodes.jsonl.gz.b64` (gzip, then base64).
