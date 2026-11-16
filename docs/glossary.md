# Glossary

Add terms as they come up in the course. Keep definitions to one or two lines.

| Term | Meaning |
|---|---|
| **LLM** | Large Language Model: predicts text; knows only what it was trained on plus what's in the prompt. |
| **Context window** | How much text (tokens) the model can read in one request. |
| **RAG** | Retrieval-Augmented Generation: retrieve relevant data, put it in the prompt, then generate. |
| **Chunk** | A small piece of a document, the unit that gets embedded and retrieved. |
| **Chunk overlap** | Characters shared between neighbouring chunks, so ideas aren't cut in half. |
| **Embedding** | A vector of numbers representing the meaning of text; similar meaning → nearby vectors. |
| **Vector store / vector DB** | Database that finds the nearest vectors to a query (e.g. Chroma). |
| **Top-k** | How many of the most similar chunks to retrieve (`k=5`). |
| **Retriever** | Component that takes a query and returns relevant chunks. |
| **Semantic search** | Search by meaning, not exact words. |
| **Keyword / lexical search** | Search by exact words (grep, BM25). |
| **Hybrid search** | Semantic + keyword search combined. |
| **Agent** | An LLM in a loop that decides which tools to call and when, until the task is done. |
| **Tool** | A function the agent can call (search, API, run code). |
| **Agentic search** | The agent explores data itself with tools (grep, read file) instead of a pre-built index. |
| **Agentic RAG** | An agent that uses retrieval as one of its tools. |
| **Grounding** | Making answers rely on retrieved sources rather than model memory. |
| **Hallucination** | A confident answer that isn't supported by facts or sources. |
