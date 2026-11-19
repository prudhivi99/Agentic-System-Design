# Images

Pictures used in the docs: diagrams from LinkedIn posts, course slides, screenshots of results.

## Folder layout

```
docs/assets/images/
├── 01-rag/              ← one folder per concept area (same names as docs/concepts/)
│   └── chunk-overlap-diagram.png
└── 02-agentic-ai/
    └── agent-loop.png
```

## How to add a picture

1. Save the image into the matching folder, with a short lowercase name (`what-it-shows.png`).
2. Embed it in the concept page, next to the section it explains. Always add a credit line and
   a short "what this shows" note:

```markdown
![Chunk overlap explained](../../assets/images/01-rag/chunk-overlap-diagram.png)

*Source: [Author Name on LinkedIn](https://www.linkedin.com/posts/...)*

> **What this shows:** two neighbouring chunks share a few sentences, so an idea on the border
> is never cut in half. Compare with our ASCII version above.
```

3. Add a row to [docs/references.md](../../references.md).

Or just give Claude the image and the post link, and ask it to do these steps.

> ⚖️ Images from LinkedIn belong to their authors. Always credit and link the original post.
> If this repo is public, prefer your own redrawn version or ask the author first.
