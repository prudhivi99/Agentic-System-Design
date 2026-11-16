# Environment setup

## 1. Clone the repo

```bash
git clone git@github.com:prudhivi99/Agentic-System-Design.git
cd Agentic-System-Design
```

## 2. Install uv (once per machine)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 3. Install dependencies

`uv sync` creates `.venv/` and installs everything from `pyproject.toml` / `uv.lock`:

```bash
uv sync
```

> First install is large (`sentence-transformers` pulls in PyTorch), so give it a few minutes.

## 4. Add your API keys

```bash
cp .env.example .env
```

Then open `.env` and fill in `OPENAI_API_KEY`.

## 5. Run an exercise

Always run from the repo root:

```bash
uv run modules/01-rag/1_semantic_rag.py
```

## Common tasks

| I want to… | Command |
|---|---|
| Add a new package | `uv add <package>` |
| Run any script | `uv run path/to/script.py` |
| Activate the venv manually | `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`) |
| Leave the venv | `deactivate` |

### Without uv (plain pip)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install python-dotenv langgraph "langchain>=1.0" langchain-core langchain-openai \
  langchain-huggingface langchain-text-splitters langchain-chroma chromadb sentence-transformers
```

(Keep this list in sync with `dependencies` in `pyproject.toml`.)
