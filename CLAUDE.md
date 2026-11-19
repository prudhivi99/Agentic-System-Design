# CLAUDE.md

This is my personal learning repo for an **Agentic System Design** course. I'm learning, so
explain the "why", not just the "what".

## Structure (keep to it)

- `modules/NN-topic/`: one folder per course module, numbered in course order
  (`01-rag`, `02-agents`, ...). Each has a `README.md` based on
  `docs/templates/module_readme_template.md`, plus scripts named `1_xxx.py`, `2_xxx.py`.
- `docs/concepts/NN-topic/`: a learning path per topic: a `README.md` (reading order, a
  one-page overview diagram, a self-check list) plus numbered pages `01-xxx.md`, `02-xxx.md`.
  Theory only; no code needed to understand them.
- `docs/assets/images/NN-topic/`: images used in the docs.
- `docs/references.md`: posts, articles and images collected while learning.
- `docs/glossary.md`: add new terms here as they come up.
- `sample_data/`: shared data the exercises run against. Don't edit `sample_project`
  unless asked; it's test input for the RAG/agent exercises.
- `project/`: the final capstone. Keep it separate from learning code.
- When adding a module or concept page, also add it to the index tables in `README.md` and
  to the topic's learning-path `README.md`.

## Python

- One shared environment at the repo root, managed with `uv` (`pyproject.toml`, `uv.lock`).
- Add dependencies with `uv add <pkg>`; run scripts with `uv run modules/.../script.py`.
- API keys live in `.env` (never commit it). Document new key names in `.env.example`.
- Scripts should run from the repo root, and resolve paths relative to `__file__`.

## Writing docs

The reader is a beginner (me, and anyone else). Docs must be self-explanatory: assume the
reader gets lost easily, so explain more rather than less.

- Simple English, short sentences. Always explain **why** before **how**.
- Diagrams on every page: Mermaid (GitHub renders it) for flows, ASCII for small spatial
  pictures (chunks, vectors). Keep Mermaid simple: quote labels, no special syntax tricks.
- Use our own code and test cases (`sample_project`, T1–T10) as examples where possible.
- Compare with tables: with vs. without, when to use vs. when not, small vs. big.
- Concept page structure:
  1. Header line: read time · prerequisites · ← previous / next → links
  2. "In one sentence"
  3. Why do we need it? (the problem, with an example)
  4. How it works (diagrams), with vs. without, examples
  5. Common beginner mistakes (table)
  6. "Check yourself" questions, answers in `<details>` blocks
  7. Footer with previous / next links
- Every number or claim about our code must be checked against the code (run it if possible).
- New terms go in `docs/glossary.md`, linked to the page that explains them.
- When drafting a module README, leave the "in my own words" parts as clear TODO prompts
  for me to fill in, rather than writing them all for me.

## When I share a LinkedIn post, image or article

1. Save the image to `docs/assets/images/NN-topic/short-name.png`.
2. Embed it in the concept page next to the section it explains, with a caption, a credit
   line (`*Source: [Author on LinkedIn](link)*`) and a 2–4 line "What this shows" note that
   connects it to our own diagrams and code.
3. If the post teaches something new, add it to the page in our own words (don't copy text).
4. Add a row to `docs/references.md`.
5. If the image isn't readable or the link can't be opened (LinkedIn often needs a login),
   ask me to paste the post text or the image file.

## Git

- Commits must be authored by me only:
  `prudhivi99 <63187046+prudhivi99@users.noreply.github.com>` (author and committer).
- No Claude attribution anywhere: no `Co-Authored-By: Claude`, no `Claude-Session` lines in
  commit messages, and no "Generated with Claude Code" footer in pull request descriptions.
