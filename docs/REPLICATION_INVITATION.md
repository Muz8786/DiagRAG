# Replication invitation and outreach draft (DRAFT, NOT SENT)

Nothing in this file has been sent. The owner decides whether, when and to whom. Edit the bracketed parts.

## Short note for the repository README (ready to paste)

> **Replicate or extend.** DiagRAG diagnoses retrieval failures in RAG pipelines from retrieval telemetry alone, and repairs them. Every gate was fixed before its run, and failures are in the same tables as passes.
> You can check the tables from the shipped episodes in about 30 minutes without a GPU (`docs/REPRODUCE.md`), run the benchmark quickstart in 5 minutes (`bench/QUICKSTART.md`), or regenerate a judged run on a free Kaggle T4 in a few hours.
> Independent runs, disagreements and new faults are welcome as issues or pull requests.

## Email draft for two or three RAG-evaluation groups (edit before sending)

**Subject:** Benchmark for diagnosing RAG retrieval failures from telemetry: would you try it?

Hello [name],

I am [owner name], working on DiagRAG, a method and benchmark for diagnosing retrieval-stage failures in RAG systems from retrieval telemetry alone (no generated answer), and repairing them. I am writing because your work on [their paper or tool] is the closest I know to this question.

What exists: 32 injected fault types (31 single faults and one two-fault combination) with evidence tiers tied to field reports, a 4,843-episode benchmark (2,718 dev with public labels, 2,125 test with labels held privately) (their SHA-256 is published), and judged runs on a GPU where every gate was fixed before the run.
What the results say, including the failures: in the latest GPU run a supervised telemetry diagnoser separates faulty from clean episodes at AUROC 0.977 against 0.761 for RAGLog's tier-0 features; in a separate, smaller CPU run a zero-shot LLM judge of the top five documents (three free-tier models) reached 0.64 to 0.75 against 0.975 for the diagnoser; on never-examined natural queries a repair loop gained 2.2 points of Hit@5. The 27-of-28 detector bar was missed in the latest GPU run (26 of 28), and unseen-fault closure stayed under its 0.50 bar.

What I am asking: 30 minutes to run `bench/QUICKSTART.md` with your own diagnoser, or to point it at a pipeline you already have, and to tell me where it breaks. I would rather hear that it does not transfer than not hear.
Everything, including the failures, is here: [repository link]. The code and documents were written by Claude (Anthropic) under my direction; that is stated in the repository.

Thank you,
[owner name]

## Notes for the owner

- The ShopNova synthetic partition has no licence assigned yet (`NOTICE.md`). Assign one before inviting others to redistribute the data.
- The benchmark name is yours to decide. It is `DiagRAG-Bench` in every file for now.
- A public release of the package is your decision; it is staged and verified, not published.
