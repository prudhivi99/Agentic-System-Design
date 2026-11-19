# Module 01 – RAG test cases

A fixed set of questions about `sample_data/sample_project`, each with its known correct answer.
Ask the **same questions** under every config (chunk size, k, embedding model) and compare.
Without a fixed set you're comparing different questions, not different configs.

The questions also live in [2_eval_rag.py](2_eval_rag.py) (`TEST_CASES`). Keep the two in sync.
Theory behind this: [concepts/01-rag.md § Tuning retrieval](../../docs/concepts/01-rag.md#tuning-retrieval-chunk-size-and-k).

```
 Test group           What it stresses           Knob that should matter most
 A lookup       ──►   one small exact fact   ──►  chunk_size (small helps)
 B wording      ──►   meaning vs exact name  ──►  embedding model
 C whole func   ──►   function kept intact   ──►  chunk_size (big helps)
 D cross-file   ──►   several files at once  ──►  k (bigger helps)
 E traps        ──►   saying "not found"     ──►  prompt, k
```

## How to run

```bash
uv run modules/01-rag/2_eval_rag.py --save                          # baseline: chunk=256, k=5
uv run modules/01-rag/2_eval_rag.py --chunk-size 512 --save         # change ONE thing
uv run modules/01-rag/2_eval_rag.py --k 2 --save
uv run modules/01-rag/2_eval_rag.py --model BAAI/bge-small-en-v1.5 --save
uv run modules/01-rag/2_eval_rag.py --retrieval-only                # free: no LLM call
uv run modules/01-rag/2_eval_rag.py --only T5 T7                    # just a few tests
```

`--save` writes `results/chunk<size>_k<k>_<model>.md`. Open it, tick the facts, and fill in the
summary table at the bottom.

## Why chunk size matters for these tests

`chunk_size` counts **characters**. How the key functions compare:

| Function | Size | 256 | 512 | 1024 |
|---|---|---|---|---|
| `get_role` / `get_plan` | ~100 | ✅ fits | ✅ | ✅ |
| `PermissionPolicy.require` | 387 | ❌ 2 chunks | ✅ | ✅ |
| `check_task_limit` | 531 | ❌ 2–3 | ❌ just over | ✅ |
| `TaskService.create_task` | 882 | ❌ ~4 | ❌ 2 | ✅ |
| `TaskScheduler.tick` | 1518 | ❌ 6+ | ❌ 3+ | ❌ 2 |

## The test cases

### A. Simple lookups (small chunks should do well)

| ID | Input | Expected output | Must retrieve |
|---|---|---|---|
| T1 | What is the task limit for a free plan user? | **10** (Pro 200, Enterprise 10,000) | `billing.py` → `TASK_LIMITS` |
| T2 | What role does a user get if no role is assigned? | **MEMBER** (`get_role` default) | `permissions.py` |
| T3 | Which actions can a viewer perform? | Only **`task:view`** | `permissions.py` → `ROLE_PERMISSIONS` |

### B. Wording: same question, two phrasings

| ID | Input | Expected output | Must retrieve |
|---|---|---|---|
| T4a | What does `check_task_limit` do? | Gets plan (default free) → limit from `TASK_LIMITS` → counts tasks via `db.list_tasks(owner_id)` → raises `BillingError` if count ≥ limit | `billing.py` |
| T4b | How does the app stop users from creating too many tasks? | Same as T4a | `billing.py` |

### C. Whole function (chunk size test)

| ID | Input | Expected output | Must retrieve |
|---|---|---|---|
| T5 | Walk me through what happens when a task is created through TaskService. | **6 steps:** `get_current_user` → `require("task:create")` → `check_task_limit` → `db.create_task` → `audit.record(TASK_CREATED)` → `on_task_created` (email + Slack) | `task_service.py` |
| T6 | Explain how the scheduler's `tick()` works. | Skip inactive / not-due → skip missing or inactive owner → billing check (hit = log `PERMISSION_DENIED`, skip) → `db.create_task` → log `TASK_CREATED` → advance `next_run` (+1d / +1w / +30d) | `scheduler.py` |

### D. Cross-file reasoning (k test)

| ID | Input | Expected output | Must retrieve |
|---|---|---|---|
| T7 | Do tasks created by the scheduler send email or Slack notifications? | **No.** `TaskScheduler` gets only `db`, `billing` and `audit`. It calls `db.create_task` directly, bypassing `TaskService`, so there are no notifications and no permission check | `scheduler.py` + `task_service.py` |
| T8 | If a user hits their plan limit, what happens to their scheduled task? Does it retry? | Skipped and `PERMISSION_DENIED` is logged. `next_run` is **not** advanced, so it **retries every tick** and logs again each time | `scheduler.py` |

### E. Traps and negatives (hallucination test)

| ID | Input | Expected output | The trap |
|---|---|---|---|
| T9 | How are passwords hashed with bcrypt? | **They aren't.** Stored in plaintext in `AuthService._passwords`. bcrypt is only in a comment | "bcrypt" matches the comment, so the LLM may say the passwords are hashed |
| T10 | How does the app process payments with Stripe? | **"I could not find that in the codebase."** | The retriever *always* returns k chunks, and `billing.py` sounds related, so the LLM may invent a flow |

## What to observe

| What | Where in the output | Why it matters |
|---|---|---|
| **Retrieval hit** | `billing.py@1 ✅` | Was the right *file* in the top-k, and at what rank? |
| **Right chunk?** | the `│ first line` of each chunk | A file hit isn't enough: the *specific* lines must be there (see example below) |
| **Fragments** | first lines like `) -> Task:` | The chunk starts mid-function, so it was cut by a small chunk size |
| **Facts** | tick `- [ ]` boxes | Completeness: 4/6 steps, etc. |
| **Wrong facts** | read the answer | Any claim that is false, even if the rest is good |
| **Searches** | `Searches (2)` | The agent rewrites your question. More searches = it wasn't satisfied |

**Real example from the first run (chunk=256, k=5, T1):** `billing.py` was rank 1 ✅, but the
chunk with `TASK_LIMITS` wasn't in the top 5. The agent said "check the `TASK_LIMITS`
dictionary" instead of answering **10**. It also wrote "File: (not specified)", because the
retriever tool passes only chunk text to the LLM, not the `source` metadata.

### Agent vs plain RAG

```
--retrieval-only:  your question ─────────────────────────► retriever
agent mode:        your question ─► LLM rewrites it ─► "task limit free plan" ─► retriever
```

Run a test both ways. If the agent does better, its query rewriting is fixing weak retrieval.

## Rules for a fair test

1. **Change one setting per run.** Keep k=5 while you try chunk sizes, then fix the best chunk size and try k.
2. **Run the agent tests twice.** Even at `temperature=0` the LLM can vary a little. Retrieval is deterministic.
3. **Judge against the expected answer above**, not against "sounds right".

## What to watch per experiment

These are predictions to check, not results:

| Experiment | Watch | Prediction to check |
|---|---|---|
| chunk 256 | T5, T6, T8 | Steps go missing because functions are split |
| chunk 1024 | T2, T3, T6 | Small facts get blurred in big chunks. `all-MiniLM-L6-v2` reads only ~256 tokens, so a chunk's tail is ignored when searching |
| k = 2 | T7, T8 | Cross-file answers break |
| k = 10 | T9, T10 | More context, but more noise. Does it start inventing? |
| wording | T4a vs T4b | Same score = query rewriting is helping |

## My results

Write the summary in your own words in [README.md § 5](README.md#5-what-i-tried--experiments).
The detailed runs live in `results/`.

| Config | Hits (of 10) | Facts total | Hallucinations | Notes |
|---|---|---|---|---|
| chunk=256, k=5 (baseline) | ✍️ TODO | ✍️ TODO | ✍️ TODO | ✍️ TODO |
| chunk=512, k=5 | ✍️ TODO | | | |
| chunk=1024, k=5 | ✍️ TODO | | | |
| chunk=best, k=2 | ✍️ TODO | | | |
| chunk=best, k=10 | ✍️ TODO | | | |
| other embedding model | ✍️ TODO | | | |
