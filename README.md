# Agentic System Design

My learning repo for the **Agentic System Design** course: notes, runnable exercises,
and a final project.

## Repo layout

```
Agentic-System-Design/
├── README.md            ← you are here (index of everything)
├── CLAUDE.md            ← instructions Claude Code reads automatically
├── pyproject.toml       ← one shared Python environment (uv)
├── .env.example         ← API key names (copy to .env)
├── docs/
│   ├── setup/           ← environment setup
│   ├── concepts/        ← theory notes, one per topic
│   ├── templates/       ← template for module READMEs
│   └── glossary.md      ← terms and definitions
├── modules/             ← one numbered folder per course module (code + notes)
├── sample_data/         ← shared data the exercises run against
└── project/             ← final capstone project
```

## Getting started

See [docs/setup/environment.md](docs/setup/environment.md).

## Modules

| # | Module | Notes | Code | Status |
|---|--------|-------|------|--------|
| 01 | RAG | [README](modules/01-rag/README.md) | [1_semantic_rag.py](modules/01-rag/1_semantic_rag.py) | 🟡 In progress |

<!-- Add a row per module: | 02 | Agents | [README](modules/02-agents/README.md) | ... | ⚪ Not started | -->

## Concepts

- [01 – RAG: when to use it and when not to](docs/concepts/01-rag.md)
- [Glossary](docs/glossary.md)

## Final project

See [project/README.md](project/README.md).
