# 01 – RAG: why, when, and when not

## What RAG is

**Retrieval-Augmented Generation**: find relevant text **by meaning**, ahead of time and at
scale, then hand it to the LLM as context.

```
 OFFLINE (once)                        ONLINE (each question)
 ──────────────                        ──────────────────────
 Docs ─► chunk ─► embed ─► Vector DB   Question ─► embed ─► search Vector DB
                                                     │
                                                top-k chunks
                                                     ▼
                                        LLM(question + chunks) ─► Answer
```

## "Coding agents don't use RAG. Why do we need it?"

Coding agents (Claude Code, Copilot agent mode) mostly do **agentic search**: they run
`grep` / `find` / read files in a loop.

```
  "fix the login bug" ─► Agent ─► grep "login" ─► auth.py:42 ─► read, edit, test ─► ✅
```

That works because code is **local**, **small enough**, **exact-match friendly** (function
names, error strings) and **structured** (imports, call chains). Most business data is none
of those, and that's where RAG is needed.

## Mental model

```
 Agentic search  = a detective walking through a house, opening drawers 🕵️
 RAG             = a librarian with a catalog of a million books 📚
```

## When to use RAG ✅

| Situation | Example |
|---|---|
| Large document collections that don't fit in the prompt | Support bot over 20,000 articles |
| Private/company data the model never saw | "What's our travel reimbursement limit?" |
| Users ask in **their own words**, not the docs' terms | "money got stuck" → "pending transaction" doc |
| Need **citations** / proof | Legal: "Clause 7.2 of Contract #4411 says…" |
| Data **changes often** | Weekly FAQ updates: re-index, no retraining |
| Need **permission filtering** per user | Intern must not get answers from salary docs |
| Many users, cost and latency matter | 10K employees using an HR bot daily |
| **Similarity** search | "Find past tickets like this bug" |

## When NOT to use RAG ❌ (and what to use instead)

| Question | Use instead | Why not RAG |
|---|---|---|
| "What is Kubernetes?" | Plain LLM | Already general knowledge |
| "Summarize this one PDF" | Long context | Small enough to send whole |
| "Fix the null-pointer bug" | Agentic search | Code needs exact names and structure |
| "Revenue last quarter by region?" | Text-to-SQL / tool | **RAG finds text, it can't calculate** |
| "AAPL price right now?" | API call | Needs live data |
| "Reply in our brand voice" | Prompt / fine-tune | That's behavior, not knowledge |
| "Get order #123" | DB lookup | Exact IDs; semantic search may return #132 |

## Quick decision checklist

```
  Data HUGE?  UNSTRUCTURED text/PDF?  Users ask in THEIR words?
  SPREAD across systems?  Need CITATIONS?  Need PERMISSIONS?   ──► mostly YES → RAG
  Many users, need FAST + CHEAP?

  Small (send it) · Structured (query it) · Live (call it)
  Local code (grep it) · Behavior (prompt / fine-tune it)       ──► not RAG
```

## Real systems combine them: agentic RAG

```
 "Why did my refund for order #123 take so long, and what's the policy?"
                         ┌──────▼──────┐
                         │    Agent    │
                         └──┬───────┬──┘
                order status│       │refund policy
                            ▼       ▼
                     Order API    RAG over policy docs
                            └───┬───┘
                                ▼
       "Delayed by bank processing (5–7 days per policy §2.1)" 📎
```

## Use cases by industry

| Domain | Use case | Why RAG |
|---|---|---|
| Support | Bot over product docs | Users' words ≠ doc words |
| Enterprise | Knowledge across Confluence/Slack/PDFs | Scattered, huge, behind APIs |
| Legal | Contract & case-law search | Concept search + citations |
| Finance | Analyst over 10-Ks / earnings calls | Long PDFs, exact citations |
| Finance | Bank policy bot | Metadata filters (region, version) |
| Healthcare | Clinical guideline assistant | Must be grounded, no hallucinated dosages |
| Healthcare | Patient history ("allergies?") | Notes say "broke out after amox"; grep misses it |
| HR | Onboarding assistant, resume matching | Multi-system; match by meaning |
| E-commerce | "comfy shoes for standing all day" | Meaning-based product search |
| E-commerce | Answer from 12K reviews | Retrieve the few relevant reviews |
| Education | Chat with your textbook | Answers from *your* syllabus |
| Ops | Incident assistant over postmortems | "Similar past incident" search |
| Manufacturing | Technician + 1000s of scanned manuals | Huge, unstructured, mobile |
| Government | Citizen services, multilingual | Embeddings match across languages |
| Personal | Second brain, chatbot long-term memory | History too long for context |
| Code (large) | Search across 5,000 repos | Too big to grep live → pre-built index |

## Tuning retrieval: chunk size and k

```
 context the LLM sees  ≈  k  ×  chunk_size

 chunk too SMALL                     chunk too BIG
 ┌─────┐┌─────┐┌─────┐               ┌────────────────────┐
 │ def ││ if  ││ ret │ ← 1 function  │ def login(...)     │ ← 2 topics in 1 vector,
 └─────┘└─────┘└─────┘   in pieces   │ def logout(...)    │   so matching gets "blurry"
                                     └────────────────────┘
```

| Knob | Too small | Too big |
|---|---|---|
| `chunk_size` | Functions cut into pieces, so answers are incomplete | Mixed topics give fuzzy matches. The embedder also cuts off long text (MiniLM ~256 tokens) |
| `k` | Misses the right chunk, especially for cross-file questions | More noise and cost. The LLM may grab the wrong code |

Rule of thumb: **small chunks need a bigger k; big chunks can use a smaller k.**

### Chunk size: match it to the answer

Small chunks aren't always bad. It depends on how big the answer is.

```
 answer = 1 line       (default role)      → small chunk ✅  big chunk buries it
 answer = 1 function   (scheduler tick())  → small chunk ❌  cut into pieces
```

### k: how many tickets you buy

```
 k too small: answer is rank 4, k = 2   → never seen ❌
 k too big:   answer is rank 1, k = 10  → seen, plus 9 chunks of noise
```

### How to choose both: measure, don't guess

```
 1. Look at the data      typical answer size?   (code: functions ~400–900 chars)
 2. Try a grid, free      chunk 256/512/1024 × k 2/5/10, --retrieval-only
 3. Pick the SMALLEST     settings that are still near the top chunk-hit score
 4. Then pay for LLM      run the agent on the best 1–2 and check the answers
```

### When tuning stops helping

| Problem | Fix (not a number) |
|---|---|
| Functions cut in half | Split on whole functions |
| LLM mixes up files | Pass the file name with each chunk |
| LLM says "not found" when it's there | Change the prompt |

## Testing retrieval: an eval set

Fixed questions with known answers. Change **one** knob, re-run, compare.

```
 Question ─► [ Retriever ] ─► chunks ─► [ LLM ] ─► Answer
                  │                        │
         ✗ right chunk missing     ✗ ignores chunks / invents
         fix: chunk size, k,       fix: prompt, pass file names,
              embedding model           "say not found" rule
```

So check **two** things per question: *was the right chunk retrieved?* and *is the answer
right, with nothing invented?* A good answer can hide bad retrieval, and the other way round.

Include these question types: simple lookup · same question in two wordings · a whole function ·
cross-file · trap / not-in-the-code. Example set: [modules/01-rag/test_cases.md](../../modules/01-rag/test_cases.md).

## My notes

✍️ TODO: add your own examples and questions here.
