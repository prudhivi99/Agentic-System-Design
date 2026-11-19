# 1. Why RAG?

> ⏱ 10 min · Prerequisites: none · [← Learning path](README.md) · [Next: Chunking →](02-chunking.md)

## In one sentence

**RAG lets an LLM answer from _your_ data by finding the relevant pieces first and putting
them in the prompt.**

## The problem

An LLM only knows two things:

1. What it learned during **training**: public internet text, up to a cutoff date.
2. What you put in the **prompt** right now.

```
            ┌──────────────────────────────────────┐
            │  What the LLM knows                  │
            │                                      │
            │  ✅ Python, history, general facts   │
            │  ❌ YOUR company's HR policy         │
            │  ❌ YOUR codebase                    │
            │  ❌ Anything after its cutoff date   │
            │  ❌ Your customer's order status     │
            └──────────────────────────────────────┘
```

When you ask about something it never saw, it has two choices: say "I don't know", or
**guess**. LLMs are trained to sound helpful, so they often guess confidently.
A confident wrong answer is called a **hallucination**.

## With vs. without RAG

**Question:** "How many tasks can a free user create?" (asked about our `sample_project`)

![Without RAG the LLM guesses; with RAG it looks up billing.py and answers 10 tasks with a citation](../../assets/images/01-rag/with-without-rag.svg)

| | Without RAG | With RAG |
|---|---|---|
| Knows your private data | ❌ No | ✅ Yes, the parts it retrieves |
| Up to date | ❌ Frozen at the training date | ✅ As fresh as your index |
| Can cite a source | ❌ No | ✅ "billing.py, line 19" |
| Hallucination risk | 🔴 High | 🟡 Lower (not zero!) |
| Extra cost and latency | None | Building the index, plus a search on every question (slower and costlier per answer) |

## An analogy: the open-book exam

```
 Closed-book exam (plain LLM)          Open-book exam (RAG)
 ─────────────────────────────         ─────────────────────────────
 Answer from memory only.              First find the right page in the
 If you don't remember, you            textbook, THEN write the answer
 guess and hope.                       using that page.
```

The student (the LLM) is the same. The difference is that they're allowed to **look things
up** before answering. RAG is "looking things up". The quality depends on finding the
**right page**, and that's what chunking, embeddings and `k` are about (pages 2–4).

## "Why not just paste ALL my documents into the prompt?"

Good question. Sometimes you should! If your data is small (one PDF, one file), paste it.
That's called **long context**. But it breaks down as the data grows:

```
 Your data          Paste everything?
 ──────────         ──────────────────────────────────────────────
 1 PDF (10 pages)   ✅ Yes, it fits. Simple. No RAG needed.
 Our sample_project ⚠️ ~30,000 characters. Fits, but you pay for all of it on every question.
 A company wiki     ❌ Millions of pages. Doesn't fit in any model.
```

Even when it fits, sending everything every time:
- **costs more**, because you pay per token, on every question
- is **slower**
- can **confuse** the model. The important line gets lost in the middle of a huge prompt.

RAG sends only the **few relevant pieces**.

## "Why not fine-tune the model on my data instead?"

**Fine-tuning** means training the model further on your examples. It changes *how the model
behaves* (style, format, tone). It's a poor way to teach it *facts*:

| | RAG | Fine-tuning |
|---|---|---|
| Teaches facts | ✅ Good | ⚠️ Unreliable, still hallucinates |
| Teaches style/behavior | ❌ No | ✅ Good |
| Update when data changes | ✅ Re-index in minutes | ❌ Re-train (slow, costly) |
| Can cite sources | ✅ Yes | ❌ No |
| Permission control per user | ✅ Filter at search time | ❌ Model knows everything it saw |

Rule: **RAG for knowledge, fine-tuning for behavior.**

## "Coding agents like Claude Code don't use RAG. Why do we need it?"

Coding agents mostly use **agentic search**: they run `grep`, list folders and open files in a
loop, like a developer would.

```
  "fix the login bug" ─► Agent ─► grep "login" ─► auth.py:42 ─► read, edit, test ─► ✅
```

That works because code is special:

| Code is… | So… |
|---|---|
| **Local**: files on disk | the agent can open them directly |
| **Small enough**: thousands of files | searching live is fast |
| **Exact**: function names, error strings | `grep` finds them perfectly |
| **Structured**: imports, call chains | the agent can follow links like a map |

Most business data is **none of these**: millions of PDFs, Slack threads and tickets spread
across systems, written in everyday language. You can't `grep` "why was my refund late?"
across 2 million support tickets. That's where RAG is needed.

```
 Agentic search  = a detective walking through a house, opening drawers 🕵️
 RAG             = a librarian with a catalog of a million books 📚
```

> 💡 In our module we use RAG **on code**, because code is a small, easy dataset to learn
> with. Real coding tools usually prefer `grep`. You'll see why in the tests: exact names
> like `check_task_limit` don't always match well by "meaning".
> Details: [When to use RAG](05-when-to-use-rag.md).

## Common beginner mistakes

| Mistake | Why it's wrong |
|---|---|
| "RAG removes hallucinations" | It **reduces** them. If the wrong chunks are retrieved, the LLM can still invent things. |
| "RAG makes the model learn my data" | The model doesn't change. RAG only adds text to the prompt for **this one question**. |
| "More retrieved text = better answer" | More text means more noise and cost. See [chunk size and k](04-chunk-size-and-k.md). |

## Check yourself

<details>
<summary>1. An LLM was trained in 2025. You ask about your company's 2026 leave policy. What happens without RAG?</summary>

It never saw that document, so it either says it doesn't know or, more likely, **guesses**
something that sounds like a typical leave policy. That's a hallucination.
</details>

<details>
<summary>2. What do the letters R, A and G stand for, in plain words?</summary>

**Retrieval**: find the relevant pieces of your data.
**Augmented**: add them to the prompt.
**Generation**: the LLM writes the answer using them.
</details>

<details>
<summary>3. You have one 5-page PDF. Do you need RAG?</summary>

Probably not. It fits in the prompt, so just paste it (long context). RAG pays off when data
is too big to send every time.
</details>

<details>
<summary>4. You want the chatbot to always answer in a friendly, short style. RAG or fine-tuning?</summary>

That's **behavior**, not knowledge, so a system prompt (or fine-tuning). RAG adds facts, not style.
</details>

---

[← Learning path](README.md) · [Next: Chunking →](02-chunking.md)
