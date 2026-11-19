# Module 02 – Semantic RAG with AST chunking

> 📚 **Read first: [Chunking code with AST](../../docs/concepts/01-rag/07-chunking-code-with-ast.md)**
> (what an AST is, why it chunks code better, and what this simple version still misses,
> measured on `sample_project`). Then run the code and fill in the experiments below.

## 1. What problem does this solve?

In module 01, the splitter cut code by **character count**, so functions were split in half
(T5, T6 in [01-rag/test_cases.md](../01-rag/test_cases.md)). Here, Python's `ast` module reads
the code's structure, and we cut on **whole classes and functions**.

```
 01: by characters                     02: by AST (structure)
 ┌──────────┐┌──────────┐             ┌──────────────────────┐
 │def tick( ││  if not  │  ← cut      │ class TaskScheduler: │  ← one whole
 └──────────┘└──────────┘             │   def tick(...)      │    class
                                      └──────────────────────┘
```

> ✍️ TODO (in my own words): why does cutting on structure help for *code* in particular?

## 2. Key concepts (in my own words)

- **AST (Abstract Syntax Tree)**: the code parsed into a tree of nodes (`Module` → `ClassDef` → `FunctionDef`).
- **One chunk per node**: each top-level class or function becomes one chunk, with metadata
  `type` (class/function) and `name`.

> ✍️ TODO: explain what `ast.get_source_segment` does, and why we add `parent` links.

## 3. Architecture diagram

```
 sample_project/*.py ─► ast.parse ─► top-level class / function ─► embed ─► Chroma
   (13 files)                         = 1 chunk each (28 chunks)     MiniLM
                                                                        │
 You ─► Agent (gpt-4o-mini) ─► search_codebase (k=4) ◄──────────────────┘
```

## 4. How to run

From the repo root:

```bash
uv run modules/02-semanticrag-with-ast/1_semantic_rag_ast.py
```

## 5. What I tried / experiments

Compare with module 01's best settings (chunk 1024, k=5, ~23/35 facts).

| Experiment | What to watch | Result |
|---|---|---|
| Ask T1 (free plan limit) | `TASK_LIMITS` is a module-level constant, not a class/function. Is it in any chunk? | ✍️ TODO |
| Ask T5 (create flow) | `TaskService` is one ~4,500-char chunk. MiniLM reads only ~256 tokens. Found? | ✍️ TODO |
| Ask T7 / T8 | Whole `TaskScheduler` class in one chunk. Does reasoning improve? | ✍️ TODO |
| k 4 → 2 / 8 | Fewer, bigger chunks: does k matter less now? | ✍️ TODO |

## 6. What went wrong & how I fixed it

- Default `--repo` pointed to `modules/sample_project` (doesn't exist), so fixed it to `sample_data/sample_project`.
- ✍️ TODO

## 7. Questions I still have

- Code outside classes/functions (constants, imports) is dropped. How should it be kept?
- Should a big class be one chunk, or one chunk per method?
- ✍️ TODO

## 8. How this could be used in my final project

✍️ TODO
