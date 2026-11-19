# RAG: learning path

> **New here? Read the pages in this order.** Each page builds on the one before.
> You don't need to understand everything the first time. Run the code, then come back.
> It gets clearer every time.

The path has **three parts**. Part A teaches the basics with module 01. Part B improves
*how* chunks are found, one module per idea. Part C maps the advanced patterns.

```mermaid
flowchart TB
    subgraph A["Part A · RAG basics"]
        direction LR
        A1["1. Why RAG?"] --> A2["2. Chunking"] --> A3["3. Embeddings"] --> A4["4. Chunk size and k"] --> A5["5. When to use RAG"] --> A6["6. Testing"] --> M1["Module 01"]
    end
    subgraph B["Part B · Better retrieval"]
        direction LR
        B7["7. AST chunking"] --> M2["Module 02"] --> B8["8. Lexical and BM25"] --> M3["Module 03"] --> B9["9. Semantic vs. lexical"] --> B10["10. Hybrid RAG"] --> M4["Module 04"]
    end
    subgraph C["Part C · Advanced patterns"]
        direction LR
        C11["11. Advanced RAG patterns"]
    end
    A --> B --> C
```

### Part A · RAG basics

| # | Page | You will learn | Time |
|---|---|---|---|
| 1 | [Why RAG?](01-why-rag.md) | The problem RAG solves. With vs. without RAG. | 10 min |
| 2 | [Chunking](02-chunking.md) | Why documents are cut into pieces, and how. | 10 min |
| 3 | [Embeddings and vector search](03-embeddings.md) | How text becomes numbers, and how "search by meaning" works. | 15 min |
| 4 | [Chunk size and k](04-chunk-size-and-k.md) | The two main knobs. What happens in each combination. How to choose. | 15 min |
| 5 | [When to use RAG](05-when-to-use-rag.md) | When RAG is the right tool, when it isn't, and real use cases. | 15 min |
| 6 | [Testing a RAG system](06-evaluating-rag.md) | How to prove a change made things better, not just different. | 10 min |
| | **Code:** [module 01 – semantic RAG](../../../modules/01-rag/README.md) | Run it, then do the chunk size and k experiments. | |

### Part B · Better retrieval

| # | Page | You will learn | Time |
|---|---|---|---|
| 7 | [Chunking code with AST](07-chunking-code-with-ast.md) | Cut code into whole classes and functions, and what that still misses. | 15 min |
| | **Code:** [module 02 – AST chunking](../../../modules/02-semanticrag-with-ast/README.md) | | |
| 8 | [Lexical search and BM25](08-lexical-search-and-bm25.md) | Keyword search: tokenizing, the inverted index, and how BM25 scores. | 15 min |
| | **Code:** [module 03 – lexical RAG](../../../modules/03-lexicalrag/README.md) | | |
| 9 | [Semantic vs. lexical](09-semantic-vs-lexical.md) | Which search wins which questions, and a quick rule to choose. | 10 min |
| 10 | [Hybrid RAG](10-hybrid-rag.md) | An architecture that combines several retrievers; merging with (weighted) RRF. | 15 min |
| | **Code:** [module 04 – hybrid RAG](../../../modules/04-hybridrag/README.md) | | |

### Part C · Advanced patterns

| # | Page | You will learn | Time |
|---|---|---|---|
| 11 | [Advanced RAG patterns](11-advanced-rag-patterns.md) | "One extra step = a new kind of RAG": RAPTOR, HyDE, reranking, Corrective RAG, Self-RAG, and how to debug wrong answers. | 20 min |

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
| Hybrid merge (RRF) | [1_hybrid_rag.py](../../../modules/04-hybridrag/1_hybrid_rag.py) | `build_hybrid_retriever()` |

## Self-check before moving on

After all eleven pages, you should be able to answer these without looking.
Each page has its own questions at the bottom, with answers.

- [ ] Why can't the LLM just answer questions about my private documents?
- [ ] Why do we cut documents into chunks instead of embedding the whole file?
- [ ] What is an embedding, in one sentence?
- [ ] What happens when chunks are small **and** k is small?
- [ ] Give two situations where RAG is the **wrong** tool.
- [ ] Why can a good-looking answer still hide bad retrieval?
- [ ] What is an AST, and why does it chunk code better than a character count?
- [ ] What are BM25's three scoring ideas?
- [ ] When is lexical search better than semantic search?
- [ ] What is Hybrid RAG, and why merge by rank (RRF) instead of by score?
- [ ] Users say answers are wrong: what do you check first?

Words you don't know → [glossary](../../glossary.md).
