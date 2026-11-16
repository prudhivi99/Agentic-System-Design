# Module 01 – RAG (Retrieval-Augmented Generation)

## 1. What problem does this solve?

An LLM doesn't know about *my* code or documents. RAG finds the most relevant pieces of my
data **by meaning** and puts them in the prompt, so the LLM answers from real sources
instead of guessing.

In this exercise the "data" is a small codebase (`sample_data/sample_project`, a
task-management app), and an agent answers questions about it.

> ✍️ TODO (in my own words): why can't the LLM just answer from its training data here?

## 2. Key concepts (in my own words)

- **Document**: one file loaded from disk, plus metadata (`source` = file path).
- **Chunking**: splitting documents into small pieces (`CHUNK_SIZE = 256` characters,
  32 overlap). The Python-aware splitter tries to split on `class` / `def` boundaries.
- **Embedding**: turning a chunk into a vector of numbers that captures its meaning
  (model: `all-MiniLM-L6-v2`, runs locally, no API key).
- **Vector store**: a database that finds the chunks whose vectors are closest to the
  question's vector (here: Chroma, in memory).
- **Retriever tool**: wraps the vector store as a tool (`search_codebase`) the agent can call.
- **Agent**: the LLM (`gpt-4o-mini`) decides when to call the tool, reads the results,
  then answers. This is **agentic RAG**.

> ✍️ TODO: rewrite these in your own words once you've run the script.

## 3. Architecture diagram

```
 OFFLINE (at startup)
 ────────────────────
 sample_project/*.py ─► load_codebase() ─► chunk_code() ─► embed ─► Chroma (in memory)
   (13 files)             Documents          ~256-char        MiniLM
                                             chunks

 ONLINE (each question)
 ──────────────────────
 You: "How does billing limit tasks?"
        │
        ▼
   ┌──────────┐  search_codebase("billing task limit")  ┌────────┐
   │  Agent   │ ──────────────────────────────────────► │ Chroma │
   │gpt-4o-mini│ ◄────────────────────────────────────── │ top k=5│
   └──────────┘        5 most similar chunks            └────────┘
        │
        ▼
   Answer citing file + function names
```

## 4. How to run

From the repo root (setup: [docs/setup/environment.md](../../docs/setup/environment.md)):

```bash
uv run modules/01-rag/1_semantic_rag.py
```

Point it at another codebase:

```bash
uv run modules/01-rag/1_semantic_rag.py --repo /path/to/other/repo
```

Questions to try:
- How does a user log in?
- What happens when a task is completed?
- Which plan tiers exist and what are their limits?
- Who is allowed to see the system report?

## 5. What I tried / experiments

| Experiment | Change | Result |
|---|---|---|
| Chunk size | `CHUNK_SIZE` 256 → 512 / 1024 | ✍️ TODO |
| Number of results | `k` 5 → 2 / 10 | ✍️ TODO |
| Embedding model | `all-MiniLM-L6-v2` → another model | ✍️ TODO |
| Question wording | exact function name vs. plain English | ✍️ TODO |

## 6. What went wrong & how I fixed it

✍️ TODO

## 7. Questions I still have

- Code has exact names (function, class). When is plain `grep` better than semantic search?
  (See [concepts/01-rag.md](../../docs/concepts/01-rag.md).)
- What happens when a function is split across two chunks?
- ✍️ TODO

## 8. How this could be used in my final project

✍️ TODO
