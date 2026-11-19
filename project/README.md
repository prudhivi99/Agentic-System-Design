# Final project

> Fill this in as the course progresses. Each section of the course adds a feature
> ([course roadmap](../docs/course-roadmap.md)).

## Chosen idea: an AI coding agent (the course capstone)

The course capstone (section 5) is to **design and implement an AI coding agent**: an agent that
can find the right code, understand it, and answer questions or make changes.

```
 Find the right code   ─►  Understand it  ─►  Answer / change it  ─►  Check it
 (sections 1, 3)           (section 2)        (section 3)             (section 4)
 RAG, AST chunks,          context,           tools: read, edit,      tests, evals,
 grep                      memory             run commands            tracing
```

Modules 01 and 02 (RAG over `sample_project`) are the start of the "find the right code" part.

✍️ TODO: in your own words, what should *your* coding agent be able to do?

<details>
<summary>Other ideas considered earlier</summary>

1. **Codebase Q&A + fix agent**: extend `modules/01-rag` with grep / read / edit tools (closest to the capstone).
2. **Company knowledge assistant**: RAG over PDFs and docs, with citations and per-user permission filters.
3. **Incident / on-call assistant**: search runbooks and past postmortems for similar incidents, suggest fixes.
4. **Multi-agent research assistant**: planner, retriever and writer agents produce a report.
</details>

## Problem statement

✍️ TODO: who is the user, what pain does this solve?

## Architecture

```
✍️ TODO: ASCII diagram
```

## Design decisions

| Decision | Options considered | Chosen | Why |
|---|---|---|---|
| | | | |

## Features by module

| Course module | Feature it adds to the project |
|---|---|
| 01 – RAG | Semantic search over the codebase |
| 02 – AST chunking | Chunks = whole classes / functions |

## How to run

✍️ TODO

## Evaluation (how I know it works)

✍️ TODO
