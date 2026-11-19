# RAG: learning path

> **New here? Read the pages in this order.** Each page builds on the one before.
> You don't need to understand everything the first time. Run the code, then come back.
> It gets clearer every time.

```mermaid
flowchart LR
    A["1. Why RAG?"] --> B["2. Chunking"]
    B --> C["3. Embeddings and vector search"]
    C --> D["4. Chunk size and k"]
    D --> E["5. When to use RAG, and when not"]
    E --> F["6. Testing a RAG system"]
    F --> G["Run modules/01-rag"]
    G --> H["7. Chunking code with AST"]
    H --> I["Run modules/02"]
    I --> J["8. Lexical search and BM25"]
    J --> K["9. Semantic vs. lexical, Hybrid RAG"]
    K --> L["Run modules/03"]
```

| # | Page | You will learn | Time |
|---|---|---|---|
| 1 | [Why RAG?](01-why-rag.md) | The problem RAG solves. With vs. without RAG. | 10 min |
| 2 | [Chunking](02-chunking.md) | Why documents are cut into pieces, and how. | 10 min |
| 3 | [Embeddings and vector search](03-embeddings.md) | How text becomes numbers, and how "search by meaning" works. | 15 min |
| 4 | [Chunk size and k](04-chunk-size-and-k.md) | The two main knobs. What happens in each combination. How to choose. | 15 min |
| 5 | [When to use RAG](05-when-to-use-rag.md) | When RAG is the right tool, when it isn't, and real use cases. | 15 min |
| 6 | [Testing a RAG system](06-evaluating-rag.md) | How to prove a change made things better, not just different. | 10 min |
| 7 | [Chunking code with AST](07-chunking-code-with-ast.md) | What an AST is, why it chunks code better, and what it still gets wrong. Read after running module 01. | 15 min |
| 8 | [Lexical search and BM25](08-lexical-search-and-bm25.md) | Keyword search: tokenizing, the inverted index, and how BM25 scores. Where it beats embeddings. | 15 min |
| 9 | [Semantic vs. lexical, and Hybrid RAG](09-hybrid-rag.md) | When to use which, and how Hybrid RAG merges both (RRF). | 15 min |

## The whole idea on one page

![RAG in 2 steps: prepare (documents, chunk, embed, store) and answer (question, find k closest, add to prompt, LLM answers)](../../assets/images/01-rag/rag-overview.svg)

**R**etrieval (find the right pieces) → **A**ugmented (add them to the prompt) → **G**eneration (the LLM answers).

## Where this appears in the code

| Concept | File | Function |
|---|---|---|
| Load documents | [1_semantic_rag.py](../../../modules/01-rag/1_semantic_rag.py) | `load_codebase()` |
| Chunking | same | `chunk_code()` |
| Embeddings + vector DB | same | `build_vector_store()` |
| Retrieval with top-k | same | `build_agent()` → `as_retriever(search_kwargs={"k": k})` |
| Testing | [2_eval_rag.py](../../../modules/01-rag/2_eval_rag.py) | `run_test()` |
| AST chunking | [1_semantic_rag_ast.py](../../../modules/02-semanticrag-with-ast/1_semantic_rag_ast.py) | `chunk_code()` |
| BM25 search | [2_lexicalrag.py](../../../modules/03-lexicalrag/2_lexicalrag.py) | `tokenize()`, `BM25Retriever` |

## Self-check before moving on

After all nine pages, you should be able to answer these without looking.
Each page has its own questions at the bottom, with answers.

- [ ] Why can't the LLM just answer questions about my private documents?
- [ ] Why do we cut documents into chunks instead of embedding the whole file?
- [ ] What is an embedding, in one sentence?
- [ ] What happens when chunks are small **and** k is small?
- [ ] Give two situations where RAG is the **wrong** tool.
- [ ] Why can a good-looking answer still hide bad retrieval?
- [ ] What is an AST, and why does it chunk code better than a character count?
- [ ] What are BM25's three scoring ideas?
- [ ] When is lexical search better than semantic search, and what does Hybrid RAG do?

Words you don't know → [glossary](../../glossary.md).
