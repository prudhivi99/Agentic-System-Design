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

## My notes

✍️ TODO: add your own examples and questions here.
