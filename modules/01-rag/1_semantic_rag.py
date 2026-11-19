

import argparse
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


from langchain_core.documents import Document
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.tools.retriever import create_retriever_tool
from langchain.agents import create_agent


CHUNK_SIZE = 256
CHUNK_OVERLAP = 32
TOP_K = 5
EMBED_MODEL = "all-MiniLM-L6-v2"


def load_codebase(repo_path: str) -> list:
   docs = []
   for path in Path(repo_path).rglob("*.py"):
       text = path.read_text(encoding="utf-8", errors="ignore")
       docs.append(Document(page_content=text, metadata={"source": str(path)}))
   return docs




def chunk_code(docs: list, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> list:
   splitter = RecursiveCharacterTextSplitter.from_language(
       language=Language.PYTHON,
       chunk_size=chunk_size,
       chunk_overlap=chunk_overlap,
   )
   return splitter.split_documents(docs)




def build_vector_store(chunks: list, model_name: str = EMBED_MODEL) -> Chroma:
   embeddings = HuggingFaceEmbeddings(model_name=model_name)
   return Chroma.from_documents(chunks, embedding=embeddings)




def build_agent(vector_store: Chroma, k: int = TOP_K):
   retriever_tool = create_retriever_tool(
       vector_store.as_retriever(search_kwargs={"k": k}),
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




if __name__ == "__main__":


   parser = argparse.ArgumentParser()
   parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[2] / "sample_data" / "sample_project"))
   args = parser.parse_args()
   repo_path = str(Path(args.repo).resolve())


   # load the code base

   docs = load_codebase(repo_path)
   chunks = chunk_code(docs)
   print(f"Loaded {len(docs)} files → {len(chunks)} chunks (chunk_size={CHUNK_SIZE})")




   vector_store = build_vector_store(chunks)
   agent = build_agent(vector_store)




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
           if not getattr(last_msg, "tool_calls", None):
               print(f"Agent: {last_msg.content}")