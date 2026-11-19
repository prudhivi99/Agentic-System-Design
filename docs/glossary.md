# Glossary

Add terms as they come up in the course. Keep definitions to one or two lines, and link to the
page that explains the term in depth.

| Term | Meaning |
|---|---|
| **LLM** | Large Language Model: predicts text; knows only what it was trained on plus what's in the prompt. |
| **Context window** | How much text (tokens) the model can read in one request. |
| **RAG** | Retrieval-Augmented Generation: retrieve relevant data, put it in the prompt, then generate. See [Why RAG?](concepts/01-rag/01-why-rag.md). |
| **Chunk** | A small piece of a document, the unit that gets embedded and retrieved. |
| **Chunk overlap** | Characters shared between neighbouring chunks, so ideas aren't cut in half. |
| **Embedding** | A vector of numbers representing the meaning of text; similar meaning → nearby vectors. |
| **Vector store / vector DB** | Database that finds the nearest vectors to a query (e.g. Chroma). |
| **Top-k** | How many of the most similar chunks to retrieve (`k=5`). |
| **Retriever** | Component that takes a query and returns relevant chunks. |
| **Semantic search** | Search by meaning, not exact words. |
| **Keyword / lexical search** | Search by exact words (grep, BM25). See [Lexical search and BM25](concepts/01-rag/08-lexical-search-and-bm25.md). |
| **Hybrid RAG** | A retrieval architecture that runs several retrieval strategies (e.g. lexical + semantic) and merges their results. "Hybrid search" usually means lexical + semantic. See [Hybrid RAG](concepts/01-rag/10-hybrid-rag.md). |
| **Agent** | An LLM in a loop that decides which tools to call and when, until the task is done. See [What is an agent?](concepts/02-agentic-ai/01-what-is-an-agent.md). |
| **Tool** | A function the agent can call (search, API, run code). |
| **Agentic search** | The agent explores data itself with tools (grep, read file) instead of a pre-built index. |
| **Agentic RAG** | An agent that uses retrieval as one of its tools. See [Agentic RAG](concepts/02-agentic-ai/03-agentic-rag.md). |
| **Grounding** | Making answers rely on retrieved sources rather than model memory. |
| **Hallucination** | A confident answer that isn't supported by facts or sources. |
| **Eval set / golden set** | Fixed questions with known correct answers, re-run after every change to compare configs fairly. |
| **Retrieval hit** | The chunk with the answer was in the top-k. A file can be a hit while the exact chunk is missed. |
| **Query rewriting** | The agent turns your question into its own search query before calling the retriever. |
| **Distance score** | How far a chunk's vector is from the query's vector. Lower = more similar (Chroma's default). |
| **Max sequence length** | Most tokens an embedding model reads (MiniLM: 256). Anything longer is silently cut off before embedding. |
| **Vector** | A list of numbers. An embedding is a vector. See [Embeddings](concepts/01-rag/03-embeddings.md). |
| **Dimensions** | How many numbers are in a vector (MiniLM: 384). |
| **Cosine similarity** | Similarity measured by the angle between two vectors. Higher = more similar (max 1.0). |
| **Embedding model** | The model that turns text into vectors (e.g. `all-MiniLM-L6-v2`). Not the same model as the LLM. |
| **chunk_size** | Maximum size of one chunk; characters in our splitter, tokens in some tools. See [Chunk size and k](concepts/01-rag/04-chunk-size-and-k.md). |
| **Separators** | The places a splitter prefers to cut (`class`, `def`, blank line, newline…). See [Chunking](concepts/01-rag/02-chunking.md). |
| **Reranker** | A second model that re-sorts the top search results for better precision. |
| **Long context** | Sending the whole document in the prompt instead of retrieving pieces. |
| **Fine-tuning** | Training a model further on your examples. Good for behavior/style, poor for facts. |
| **Token** | The unit LLMs read and charge by; roughly ¾ of an English word. Code often uses more tokens per character. |
| **Workflow / chain** | Fixed steps written in code, always in the same order. See [What is an agent?](concepts/02-agentic-ai/01-what-is-an-agent.md). |
| **ReAct** | The common agent loop: Reason (think) → Act (call a tool) → Observe (read result), repeated. |
| **System prompt** | Instructions that tell the LLM its role, rules and output format. |
| **Short-term memory** | The current conversation (messages, tool results) in the prompt. |
| **Long-term memory** | Facts saved outside the prompt between sessions, retrieved when relevant. |
| **Guardrail** | A limit or check around an agent: max steps, human approval, allowed tools. |
| **Human in the loop** | A person approves or corrects the agent's actions before they take effect. |
| **Multi-agent system** | Several specialised agents working together, usually coordinated by a planner. |
| **Tracing** | Recording every LLM call and tool call so you can debug the agent (e.g. LangSmith). |
| **AST (Abstract Syntax Tree)** | Code turned into a tree of its parts (classes, functions, `if`s…), keeping meaning and dropping formatting. See [Chunking code with AST](concepts/01-rag/07-chunking-code-with-ast.md). |
| **AST node** | One part of the tree, e.g. `ClassDef`, `FunctionDef`, `If`. Knows its type and the lines where it starts and ends. |
| **Parser** | The program that reads code and builds the AST (Python: `ast.parse`). |
| **Decorator** | A `@something` line above a class or function, e.g. `@dataclass`. Not part of the node's source segment in Python's `ast`. |
| **tree-sitter** | A tool that builds syntax trees for many languages (JavaScript, Java, Go…), not just Python. |
| **Linter / static analysis** | Tools that find bugs and style problems by inspecting the code's AST without running it (e.g. Ruff, pylint). |
| **BM25 (Best Matching 25)** | A formula that scores how well a document matches query words, using term frequency, word rarity and document length. Default in Elasticsearch, OpenSearch and Solr. |
| **Inverted index** | A lookup from each word to the list of documents containing it (like a book's index). Makes keyword search fast. |
| **Tokenizer (for search)** | Splits text into the words that get indexed and matched (lowercasing, dropping punctuation, splitting `snake_case`). |
| **Stop words** | Very common words ("the", "how", "is") that are dropped because they match almost everything. |
| **Term frequency (TF)** | How often a word appears in a document. More is better, with diminishing returns. |
| **IDF (Inverse Document Frequency)** | Word rarity: words found in few documents count more. |
| **Lexical gap** | When the query and the document use different words for the same idea ("bill" vs. "invoice"), so keyword search misses it. |
| **Reciprocal Rank Fusion (RRF)** | Merging ranked lists by giving each item `weight / (60 + rank)` points per list and adding them up. Uses ranks, not scores. |
| **Query routing** | Choosing which search or data source to use for each question, often done by the LLM (agentic RAG). |
| **Graph RAG** | Retrieval over a knowledge graph (entities and their relationships) instead of text chunks. |
| **EnsembleRetriever** | LangChain's retriever that runs several retrievers and merges their results with weighted RRF (module 04). |
| **Middleware (agent)** | Code that runs around each LLM or tool call, e.g. to limit how many calls an agent may make (module 04's guardrails). |
