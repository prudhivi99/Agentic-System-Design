# Module 03 – Lexical RAG (BM25)

> 📚 **Read first: [Lexical search and BM25](../../docs/concepts/01-rag/08-lexical-search-and-bm25.md)**,
> then [Semantic vs. lexical, and Hybrid RAG](../../docs/concepts/01-rag/09-hybrid-rag.md).

## 1. What problem does this solve?

Semantic search (modules 01, 02) matches meaning, so it can miss **exact names**: with `k=1`,
"what is AuthService for?" returned `AuthError`. Here the search tool uses **BM25 keyword
matching** instead of embeddings, so exact class names, functions and error messages match directly.

> ✍️ TODO (in my own words): when would I pick lexical over semantic search?

## 2. Key concepts (in my own words)

- **Tokenizer**: splits code into words; keeps `snake_case` names whole *and* split into parts;
  drops stop words.
- **Inverted index**: word → the documents that contain it.
- **BM25**: scores matches by term frequency, word rarity (IDF) and document length.
- **Score 0**: no word in common, so `BM25Retriever` returns nothing rather than random chunks.

> ✍️ TODO: explain IDF in your own words, using the table from `1_bm25_visualization.py`.

## 3. Architecture diagram

```
 sample_project/*.py ─► character chunks (256) ─► tokenize ─► BM25 index (rank_bm25)
   (13 files)             173 chunks                              │
                                                                  │  no embeddings,
 You ─► Agent (gpt-4o-mini) ─► search_codebase (BM25, k=4) ◄──────┘  no vector DB
```

## 4. How to run

From the repo root:

```bash
uv run modules/03-lexicalrag/1_bm25_visualization.py   # step-by-step BM25 demo, no API key
```

```bash
uv run modules/03-lexicalrag/2_lexicalrag.py           # the lexical RAG agent (needs OPENAI_API_KEY)
```

## 5. What I tried / experiments

Compare with semantic search (modules 01, 02) on the same questions:

| Question | Semantic result | Lexical result | Notes |
|---|---|---|---|
| "what is AuthService for?" | k=1: `AuthError` ✗ | ✍️ TODO | |
| "Invalid or expired session token" | ✍️ TODO | ✍️ TODO | an exact error message |
| T4a: "What does check_task_limit do?" | ✍️ TODO | ✍️ TODO | exact name |
| T4b: "How does the app stop users from creating too many tasks?" | ✍️ TODO | ✍️ TODO | plain English |
| "auth service" (two words) | ✍️ TODO | ✍️ TODO | the tokenizer keeps `authservice` whole |
| T10: "How does the app process payments with Stripe?" | ✍️ TODO | ✍️ TODO | not in the code |

## 6. What went wrong & how I fixed it

✍️ TODO

## 7. Questions I still have

- Should the tokenizer also split `CamelCase` (`AuthService` → `auth`, `service`)?
- How do I combine BM25 with semantic search? (→ [Hybrid RAG](../../docs/concepts/01-rag/09-hybrid-rag.md))
- ✍️ TODO

## 8. How this could be used in my final project

✍️ TODO: a coding agent often searches for exact names. Where would keyword search help it?
