# CLAUDE.md

This is my personal learning repo for an **Agentic System Design** course. I'm learning, so
explain the "why", not just the "what".

## Structure (keep to it)

- `modules/NN-topic/`: one folder per course module, numbered in course order
  (`01-rag`, `02-agents`, ...). Each has a `README.md` based on
  `docs/templates/module_readme_template.md`, plus scripts named `1_xxx.py`, `2_xxx.py`.
- `docs/concepts/NN-topic.md`: theory notes (no code needed to understand them).
- `docs/glossary.md`: add new terms here as they come up.
- `sample_data/`: shared data the exercises run against. Don't edit `sample_project`
  unless asked; it's test input for the RAG/agent exercises.
- `project/`: the final capstone. Keep it separate from learning code.
- When adding a module or concept doc, also add it to the index tables in `README.md`.

## Python

- One shared environment at the repo root, managed with `uv` (`pyproject.toml`, `uv.lock`).
- Add dependencies with `uv add <pkg>`; run scripts with `uv run modules/.../script.py`.
- API keys live in `.env` (never commit it). Document new key names in `.env.example`.
- Scripts should run from the repo root, and resolve paths relative to `__file__`.

## Writing docs

- Simple English, short sentences. Explain concepts with small ASCII diagrams.
- Use examples and comparison tables (when to use / when not to use).
- When drafting a module README, leave the "in my own words" parts as clear TODO prompts
  for me to fill in, rather than writing them all for me.
