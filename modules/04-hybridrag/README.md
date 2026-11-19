# Module 04 – Hybrid RAG (lexical + semantic)

> 📚 **Read first: [Hybrid RAG](../../docs/concepts/01-rag/10-hybrid-rag.md)**
> (and [Semantic vs. lexical](../../docs/concepts/01-rag/09-semantic-vs-lexical.md) if you skipped it).

## 1. What problem does this solve?

Semantic search (module 01) misses exact names; lexical search (module 03) misses synonyms.
This module runs **both** on every search and merges the results with **weighted Reciprocal
Rank Fusion**, so each one covers the other's blind spot.

> ✍️ TODO (in my own words): which questions failed in module 01 or 03 that should work here?

## 2. Key concepts (in my own words)

- **Two retrievers, same chunks**: semantic (MiniLM + Chroma, top 4) and lexical (BM25, top 4).
- **`EnsembleRetriever`**: merges both lists with weighted RRF, `weight / (60 + rank)` per list.
  It returns **every unique chunk** from both lists (up to 8), not just 4.
- **`--weights SEMANTIC LEXICAL`**: tilts the merge toward one retriever.
- **Guardrails** (middleware): at most 5 LLM calls and 2 `search_codebase` calls per question,
  so the agent can't loop forever on bad results.

> ✍️ TODO: explain in your own words why RRF uses ranks instead of scores.

## 3. Architecture diagram

```
 sample_project/*.py ─► character chunks (256) ─┬─► embed (MiniLM) ─► Chroma   ─► top 4 ─┐
   (13 files)             173 chunks            └─► tokenize ──────► BM25     ─► top 4 ─┤
                                                                                         ▼
 You ─► Agent (gpt-4o-mini) ─► search_codebase ─► EnsembleRetriever (weighted RRF) ─► up to 8 chunks
         (max 5 LLM calls, max 2 searches)
```

## 4. How to run

From the repo root (needs `OPENAI_API_KEY` in `.env`):

```bash
uv run modules/04-hybridrag/1_hybrid_rag.py                     # weights 0.5 / 0.5
```

```bash
uv run modules/04-hybridrag/1_hybrid_rag.py --weights 0.3 0.7   # favour BM25 (exact names)
```

```bash
uv run modules/04-hybridrag/1_hybrid_rag.py --weights 0.7 0.3   # favour semantic
```

## 5. What I tried / experiments

Same questions as modules 02 and 03, now with hybrid search:

| Question | Semantic (01/02) | Lexical (03) | Hybrid 0.5/0.5 | Notes |
|---|---|---|---|---|
| "what is AuthService for?" | k=1: `AuthError` ✗ | ✍️ TODO | ✍️ TODO | exact name |
| "Invalid or expired session token" | ✍️ TODO | ✍️ TODO | ✍️ TODO | error message |
| T4b: "How does the app stop users from creating too many tasks?" | ✍️ TODO | ✍️ TODO | ✍️ TODO | plain English |
| "auth service" (two words) | ✍️ TODO | ✍️ TODO | ✍️ TODO | the BM25 tokenizer misses it |
| T10: "How does the app process payments with Stripe?" | ✍️ TODO | ✍️ TODO | ✍️ TODO | not in the code |
| Same questions with `--weights 0.3 0.7` | | | ✍️ TODO | did the order change? |

## 6. What went wrong & how I fixed it

✍️ TODO

## 7. Questions I still have

- Would AST chunks (module 02) work better than character chunks here?
- Should the agent get two separate tools (semantic, keyword) instead of one hybrid tool?
- ✍️ TODO

## 8. How this could be used in my final project

✍️ TODO: a coding agent gets both kinds of questions. Which weights would you start with?
