"""
1_hybrid_rag.py: hybrid search = semantic (embeddings) + lexical (BM25), merged with
Reciprocal Rank Fusion. The agent searches with both at once.

Run from the repo root (needs OPENAI_API_KEY in .env):
    uv run modules/04-hybridrag/1_hybrid_rag.py                     # weights 0.5 / 0.5
    uv run modules/04-hybridrag/1_hybrid_rag.py --weights 0.7 0.3   # favour semantic
    uv run modules/04-hybridrag/1_hybrid_rag.py --weights 0.3 0.7   # favour BM25 (exact names)
    uv run modules/04-hybridrag/1_hybrid_rag.py --repo /path/to/repo

Type a question at "You:". Type exit to quit.
"""

import argparse
import re
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_chroma import Chroma
from langchain_classic.retrievers.ensemble import EnsembleRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.tools.retriever import create_retriever_tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from pydantic import ConfigDict
from rank_bm25 import BM25Okapi

CHUNK_SIZE = 256
TOOL_NAME = "search_codebase"


# ---------------------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------------------


def load_codebase(repo_path: str) -> list:
    docs = []
    for path in Path(repo_path).rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        docs.append(Document(page_content=text, metadata={"source": str(path)}))
    return docs


# ---------------------------------------------------------------------------
# 2. CHUNK: character-based splits shared by both retrievers
# ---------------------------------------------------------------------------


def chunk_code(docs: list) -> list:
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=32,
    )
    return splitter.split_documents(docs)


# ---------------------------------------------------------------------------
# 3a. SEMANTIC: dense vector retriever (same as module 01)
# ---------------------------------------------------------------------------


def build_vector_retriever(chunks: list):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_documents(chunks, embedding=embeddings)
    return vector_store.as_retriever(search_kwargs={"k": 4})


# ---------------------------------------------------------------------------
# 3b. LEXICAL: sparse BM25 retriever (same as module 03, with its tokenizer fix)
# ---------------------------------------------------------------------------

# Filler words that appear everywhere. Matching on them only adds noise.
STOP_WORDS = {"a", "an", "the", "and", "or", "to", "in", "on", "for", "of", "with", "is",
              "are", "was", "be", "at", "by", "it", "this", "that", "how", "what", "does",
              "do", "when", "where", "which", "who", "why", "can", "i", "my", "me"}


def tokenize(text: str) -> list:
    """Split code into searchable words.

    "def check_task_limit(self, user)"
      → ["def", "check_task_limit", "check", "task", "limit", "self", "user"]

    - Punctuation is dropped, so "limit(self," can't glue words together.
    - snake_case names are kept whole (exact-name search) AND split into parts.
    - Stop words ("how", "the", ...) are dropped.
    """
    tokens = []
    for word in re.findall(r"[a-z0-9_]+", text.lower()):
        tokens.append(word)
        if "_" in word:
            tokens.extend(part for part in word.split("_") if part)
    return [t for t in tokens if t not in STOP_WORDS]


class BM25Retriever(BaseRetriever):
    """Thin LangChain-compatible retriever backed by rank_bm25."""

    docs: list
    bm25: object
    k: int = 4

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> list:
        scores = self.bm25.get_scores(tokenize(query))
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[: self.k]
        # Score 0 = no query word in the chunk, so don't return it.
        return [self.docs[i] for i in top_indices if scores[i] > 0]


def build_bm25_retriever(chunks: list) -> BM25Retriever:
    tokenized = [tokenize(doc.page_content) for doc in chunks]
    return BM25Retriever(docs=chunks, bm25=BM25Okapi(tokenized))


# ---------------------------------------------------------------------------
# 3c. HYBRID: fuse both via Reciprocal Rank Fusion (weights sum to 1.0)
# ---------------------------------------------------------------------------


def build_hybrid_retriever(chunks: list, weights: list[float]):
    """
    EnsembleRetriever merges results from both retrievers using RRF.
    weights=[0.5, 0.5] gives equal say to semantic and lexical signals.
    Raise the first weight for queries that need conceptual understanding;
    raise the second for queries with exact identifiers or error strings.
    """
    return EnsembleRetriever(
        retrievers=[build_vector_retriever(chunks), build_bm25_retriever(chunks)],
        weights=weights,
    )


# ---------------------------------------------------------------------------
# 4. AGENT
# ---------------------------------------------------------------------------


def build_agent(retriever):
    retriever_tool = create_retriever_tool(
        retriever,
        name=TOOL_NAME,
        description="Search the codebase for relevant functions, classes, or logic.",
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return create_agent(
        llm,
        tools=[retriever_tool],
        system_prompt=(
            "You are a senior engineer. Always use search_codebase before answering. "
            "Reference specific file and function names. "
            "If not found say 'I could not find that in the codebase'."
        ),
        # Guardrails: stop the agent looping forever on bad search results.
        middleware=[
            ModelCallLimitMiddleware(run_limit=5, exit_behavior="end"),
            # tool_name must match the tool's real name, or this limit never applies.
            ToolCallLimitMiddleware(tool_name=TOOL_NAME, run_limit=2, exit_behavior="end"),
        ],
    )


# ---------------------------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        default=str(Path(__file__).resolve().parents[2] / "sample_data" / "sample_project"),
    )
    parser.add_argument(
        "--weights", nargs=2, type=float, default=[0.5, 0.5],
        metavar=("SEMANTIC", "LEXICAL"),
        help="Retriever blend weights (must sum to 1.0). Default: 0.5 0.5",
    )
    args = parser.parse_args()
    repo_path = str(Path(args.repo).resolve())

    docs = load_codebase(repo_path)
    chunks = chunk_code(docs)
    print(f"Loaded {len(docs)} files → {len(chunks)} chunks (chunk_size={CHUNK_SIZE})")
    print(f"Hybrid weights: semantic {args.weights[0]}, lexical {args.weights[1]}")

    retriever = build_hybrid_retriever(chunks, args.weights)
    agent = build_agent(retriever)

    print("Ready. Ask your question. Type 'exit' to quit")
    while True:
        question = input("\nYou: ").strip()
        if not question or question.lower() in ("exit", "quit"):
            break

        for step in agent.stream(
            {"messages": [{"role": "user", "content": question}]},
            stream_mode="values",
        ):
            last_msg = step["messages"][-1]
            # Show each search the agent makes, then only its final answer.
            if last_msg.type == "ai" and last_msg.tool_calls:
                for call in last_msg.tool_calls:
                    print(f"  🔍 {TOOL_NAME}({call['args'].get('query', '')!r})")
            elif last_msg.type == "ai":
                print(f"Agent: {last_msg.content}")
