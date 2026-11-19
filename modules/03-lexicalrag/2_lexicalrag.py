"""
2_lexicalrag.py: same agent as module 01, but the search tool uses BM25 (keyword
matching) instead of embeddings. No vector store, no embedding model.

Run from the repo root (needs OPENAI_API_KEY in .env):
    uv run modules/03-lexicalrag/2_lexicalrag.py
    uv run modules/03-lexicalrag/2_lexicalrag.py --repo /path/to/repo

Type a question at "You:". Type exit to quit.
"""

import argparse
import re
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


from langchain_core.documents import Document
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from rank_bm25 import BM25Okapi
from langchain_openai import ChatOpenAI
from langchain_core.tools.retriever import create_retriever_tool
from langchain.agents import create_agent




# ---------------------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------------------


CHUNK_SIZE = 256


def load_codebase(repo_path: str) -> list:
   docs = []
   for path in Path(repo_path).rglob("*.py"):
       text = path.read_text(encoding="utf-8", errors="ignore")
       docs.append(Document(page_content=text, metadata={"source": str(path)}))
   return docs




# ---------------------------------------------------------------------------
# 2. CHUNK — same character-based splits as demo 1
# ---------------------------------------------------------------------------


def chunk_code(docs: list) -> list:
   splitter = RecursiveCharacterTextSplitter.from_language(
       language=Language.PYTHON,
       chunk_size=CHUNK_SIZE,
       chunk_overlap=32,
   )
   return splitter.split_documents(docs)
# ---------------------------------------------------------------------------
# 3. BM25 INDEX — no embeddings, pure term frequency
# ---------------------------------------------------------------------------


# Filler words that appear everywhere. Matching on them only adds noise
# ("How does the app..." would match every docstring containing "the").
STOP_WORDS = {"a", "an", "the", "and", "or", "to", "in", "on", "for", "of", "with", "is",
             "are", "was", "be", "at", "by", "it", "this", "that", "how", "what", "does",
             "do", "when", "where", "which", "who", "why", "can", "i", "my", "me"}


def tokenize(text: str) -> list:
   """Split code into searchable words.

   "def check_task_limit(self, user)"
     → ["def", "check_task_limit", "check", "task", "limit", "self", "user"]

   - Punctuation is dropped, so "limit(self," can't glue words together.
   - snake_case names are kept whole (exact-name search) AND split into parts
     (so "task limit" also matches check_task_limit).
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


   class Config:
       arbitrary_types_allowed = True


   def _get_relevant_documents(
       self, query: str, *, run_manager: CallbackManagerForRetrieverRun
   ) -> list:
       tokens = tokenize(query)
       scores = self.bm25.get_scores(tokens)
       top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[: self.k]
       # Score 0 = no query word appears in the chunk. Returning those would hand the
       # agent random chunks, and it keeps re-searching. Return nothing instead.
       return [self.docs[i] for i in top_indices if scores[i] > 0]




def build_bm25_retriever(chunks: list) -> BM25Retriever:
   tokenized = [tokenize(doc.page_content) for doc in chunks]
   bm25 = BM25Okapi(tokenized)
   return BM25Retriever(docs=chunks, bm25=bm25)

# ---------------------------------------------------------------------------
# 4. RETRIEVER + AGENT
# ---------------------------------------------------------------------------


def build_agent(retriever: BaseRetriever):
   retriever_tool = create_retriever_tool(
       retriever,
       name="search_codebase",
       description="Search the codebase for relevant functions, classes, or logic.",
   )
   llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
   return create_agent(
       llm, tools=[retriever_tool],
       system_prompt=(
           "You are a senior engineer. Always use search_codebase before answering. "
           "Reference specific file and function names. "
           "If not found say 'I could not find that in the codebase'."
       ),
   )




# ---------------------------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------------------------


if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[2] / "sample_data" / "sample_project"))
   args = parser.parse_args()
   repo_path = str(Path(args.repo).resolve())






   docs = load_codebase(repo_path)
   chunks = chunk_code(docs)
   print(f"Loaded {len(docs)} files → {len(chunks)} chunks (chunk_size={CHUNK_SIZE})")




   retriever = build_bm25_retriever(chunks)
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
           # (Tool results, i.e. the raw retrieved chunks, are not printed.)
           if last_msg.type == "ai" and last_msg.tool_calls:
               for call in last_msg.tool_calls:
                   print(f"  🔍 search_codebase({call['args'].get('query', '')!r})")
           elif last_msg.type == "ai":
               print(f"Agent: {last_msg.content}")
