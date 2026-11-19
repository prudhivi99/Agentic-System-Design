"""
2_eval_rag.py: run the fixed test questions from test_cases.md against the RAG agent
in 1_semantic_rag.py, and show what was retrieved for each one.

Why this exists: 1_semantic_rag.py only prints the final answer. To compare chunk sizes,
k values or embedding models, you need to see WHAT the agent searched for and WHICH
chunks came back. A good-looking answer can hide bad retrieval, and the other way round.

Run from the repo root:
    uv run modules/01-rag/2_eval_rag.py                          # all tests, default config
    uv run modules/01-rag/2_eval_rag.py --chunk-size 512 --k 2   # one experiment
    uv run modules/01-rag/2_eval_rag.py --only T5 T7             # just some tests
    uv run modules/01-rag/2_eval_rag.py --retrieval-only         # no LLM, no API cost
    uv run modules/01-rag/2_eval_rag.py --save                   # also write results/<config>.md

Change ONE setting per run, so you know what caused any difference.
"""

import argparse
import importlib.util
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_REPO = HERE.parents[1] / "sample_data" / "sample_project"

# "1_semantic_rag.py" starts with a digit, so `import 1_semantic_rag` is a syntax error.
# Load it by file path instead. This way the eval uses the exact same pipeline and
# system prompt as the interactive script, so the test is fair.
_spec = importlib.util.spec_from_file_location("semantic_rag", HERE / "1_semantic_rag.py")
rag = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rag)


# ---------------------------------------------------------------------------
# Test cases. Keep in sync with test_cases.md (that file explains the why).
#   facts          = key facts a complete answer should contain (you tick them)
#   must_retrieve  = files the right answer lives in (checked automatically)
#   must_contain   = exact lines from the code that hold the answer. Checked against
#                    the retrieved chunks, so it shows if the RIGHT CHUNK came back.
# ---------------------------------------------------------------------------
TEST_CASES = [
    {
        "id": "T1", "group": "A. Simple lookup",
        "question": "What is the task limit for a free plan user?",
        "facts": ["Free plan limit is 10 tasks",
                  "(bonus) Pro = 200, Enterprise = 10,000"],
        "must_retrieve": ["billing.py"],
        "must_contain": ["PlanTier.FREE.value: 10,"],
    },
    {
        "id": "T2", "group": "A. Simple lookup",
        "question": "What role does a user get if no role is assigned?",
        "facts": ["MEMBER is the default role (PermissionPolicy.get_role)"],
        "must_retrieve": ["permissions.py"],
        "must_contain": ["_user_roles.get(user.id, Role.MEMBER.value)"],
    },
    {
        "id": "T3", "group": "A. Simple lookup",
        "question": "Which actions can a viewer perform?",
        "facts": ["Only task:view"],
        "must_retrieve": ["permissions.py"],
        "must_contain": ["Role.VIEWER.value: {"],
    },
    {
        "id": "T4a", "group": "B. Wording (exact name)",
        "question": "What does check_task_limit do?",
        "facts": ["Gets the user's plan (default free)",
                  "Looks up the limit in TASK_LIMITS",
                  "Counts the user's tasks via db.list_tasks(owner_id=...)",
                  "Raises BillingError when count >= limit"],
        "must_retrieve": ["billing.py"],
        "must_contain": ["if current_count >= limit:"],
    },
    {
        "id": "T4b", "group": "B. Wording (plain English)",
        "question": "How does the app stop users from creating too many tasks?",
        "facts": ["Gets the user's plan (default free)",
                  "Looks up the limit in TASK_LIMITS",
                  "Counts the user's tasks via db.list_tasks(owner_id=...)",
                  "Raises BillingError when count >= limit"],
        "must_retrieve": ["billing.py"],
        "must_contain": ["if current_count >= limit:"],
    },
    {
        "id": "T5", "group": "C. Whole function",
        "question": "Walk me through what happens when a task is created through TaskService.",
        "facts": ["1. auth.get_current_user(token)",
                  "2. policy.require(user, 'task:create')",
                  "3. billing.check_task_limit(user)",
                  "4. db.create_task(...)",
                  "5. audit.record(TASK_CREATED)",
                  "6. notifications.on_task_created (email + Slack)"],
        "must_retrieve": ["task_service.py"],
        "must_contain": ['self.policy.require(user, "task:create")',
                         "self.billing.check_task_limit(user)",
                         "self.notifications.on_task_created(task, user)"],
    },
    {
        "id": "T6", "group": "C. Whole function",
        "question": "Explain how the scheduler's tick() works.",
        "facts": ["Skips schedules that are inactive or not yet due",
                  "Skips owners that are missing or inactive",
                  "Checks billing limit; if hit, logs PERMISSION_DENIED and skips",
                  "Creates the task with db.create_task",
                  "Logs TASK_CREATED in the audit log",
                  "Advances next_run (daily +1d, weekly +1w, monthly +30d)"],
        "must_retrieve": ["scheduler.py"],
        "must_contain": ["if not schedule.is_active or schedule.next_run > now:",
                         "self.billing.check_task_limit(owner)",
                         "schedule.next_run = self._advance("],
    },
    {
        "id": "T7", "group": "D. Cross-file",
        "question": "Do tasks created by the scheduler send email or Slack notifications?",
        "facts": ["No",
                  "TaskScheduler only gets db, billing and audit (no NotificationService)",
                  "It calls db.create_task directly, bypassing TaskService",
                  "(bonus) so there is no permission check either"],
        "must_retrieve": ["scheduler.py", "task_service.py"],
        "must_contain": ["billing: BillingService, audit: AuditLogger):",
                         "title=schedule.title,"],
    },
    {
        "id": "T8", "group": "D. Cross-file",
        "question": "If a user hits their plan limit, what happens to their scheduled task? Does it retry?",
        "facts": ["The task is skipped and PERMISSION_DENIED is logged",
                  "next_run is NOT advanced (_advance only runs after a successful create)",
                  "So it retries on every tick and logs again each time"],
        "must_retrieve": ["scheduler.py"],
        "must_contain": ["Scheduled task skipped",
                         "schedule.next_run = self._advance("],
    },
    {
        "id": "T9", "group": "E. Trap",
        "question": "How are passwords hashed with bcrypt?",
        "facts": ["They are NOT hashed: stored in plaintext in AuthService._passwords",
                  "bcrypt is only mentioned in a comment (use it in production)"],
        "must_retrieve": ["auth.py"],
        "must_contain": ["self._passwords[user.id] = password"],
    },
    {
        "id": "T10", "group": "E. Negative (not in code)",
        "question": "How does the app process payments with Stripe?",
        "facts": ["Says 'I could not find that in the codebase'",
                  "Does NOT invent a payment / Stripe flow"],
        "must_retrieve": [],
        "must_contain": [],
    },
]


def relative_source(doc, repo_path: Path) -> str:
    try:
        return str(Path(doc.metadata["source"]).relative_to(repo_path))
    except ValueError:
        return Path(doc.metadata["source"]).name


def first_line(text: str, width: int = 60) -> str:
    """First non-empty line of a chunk. Shows whether a chunk starts at a `def` or
    mid-function (a sign the chunk is a fragment)."""
    for line in text.splitlines():
        if line.strip():
            line = line.strip()
            return line if len(line) <= width else line[: width - 1] + "…"
    return ""


def run_agent(agent, question: str):
    """Ask the agent and return (search queries it made, final answer)."""
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    messages = result["messages"]
    queries = [
        call["args"].get("query", "")
        for m in messages
        for call in (getattr(m, "tool_calls", None) or [])
        if call["name"] == "search_codebase"
    ]
    return queries, messages[-1].content


def run_test(case, vector_store, agent, k: int, repo_path: Path):
    if agent is None:
        # --retrieval-only: search with YOUR exact question (plain RAG, no rewriting).
        queries, answer = [case["question"]], "_(skipped: --retrieval-only)_"
    else:
        # The agent writes its own search queries. We see them via its tool calls.
        queries, answer = run_agent(agent, case["question"])

    out = [f"## {case['id']} · {case['group']}", "", f"**Q:** {case['question']}", ""]
    out.append(f"**Searches ({len(queries)}):**" if queries else "**Searches: none** ⚠️ answered without searching")

    best_rank: dict[str, int] = {}
    found_snippets: set[str] = set()
    for i, query in enumerate(queries, 1):
        out.append(f"{i}. `{query}`")
        # Similarity search is deterministic, so re-running the agent's query here
        # returns exactly the chunks the agent saw. Score = distance (lower = closer).
        for rank, (doc, score) in enumerate(vector_store.similarity_search_with_score(query, k=k), 1):
            src = relative_source(doc, repo_path)
            out.append(f"   - {rank}. `{src}` ({score:.2f}) │ `{first_line(doc.page_content)}`")
            for f in case["must_retrieve"]:
                if src == f or src.endswith("/" + f):
                    best_rank[f] = min(best_rank.get(f, rank), rank)
            for snippet in case["must_contain"]:
                if snippet in doc.page_content:
                    found_snippets.add(snippet)

    if case["must_retrieve"]:
        file_hit = ", ".join(
            f"{f}@{best_rank[f]} ✅" if f in best_rank else f"{f} ❌" for f in case["must_retrieve"]
        )
    else:
        file_hit = "n/a"

    # File hit = right file came back. Chunk hit = the exact lines with the answer came
    # back. With small chunks a file can be a hit while the answer chunk is missing.
    wanted = case["must_contain"]
    if wanted:
        chunk_hit = f"{len(found_snippets)}/{len(wanted)} " + ("✅" if len(found_snippets) == len(wanted) else "❌")
        chunk_lines = [f"  - {'✅' if s in found_snippets else '❌'} `{s}`" for s in wanted]
    else:
        chunk_hit, chunk_lines = "n/a (answer is not in the code)", []

    out += ["", "**Answer:**", "", answer, "",
            f"**Expected, tick what the answer contains ({len(case['facts'])}):**"]
    out += [f"- [ ] {fact}" for fact in case["facts"]]
    out += ["", f"**File hit:** {file_hit}", f"**Chunk hit:** {chunk_hit}"] + chunk_lines + ["", "---", ""]

    summary = {"id": case["id"], "file_hit": file_hit, "chunk_hit": chunk_hit,
               "searches": "-" if agent is None else str(len(queries)),
               "facts": f"__/{len(case['facts'])}"}
    return out, summary


def main():
    parser = argparse.ArgumentParser(description="Run the RAG test questions.")
    parser.add_argument("--chunk-size", type=int, default=rag.CHUNK_SIZE)
    parser.add_argument("--k", type=int, default=rag.TOP_K)
    parser.add_argument("--model", default=rag.EMBED_MODEL, help="HuggingFace embedding model")
    parser.add_argument("--only", nargs="+", metavar="ID", help="e.g. --only T5 T7")
    parser.add_argument("--retrieval-only", action="store_true",
                        help="skip the LLM: search with the raw question (free, no API key)")
    parser.add_argument("--save", action="store_true", help="write results/<config>.md")
    parser.add_argument("--repo", default=str(DEFAULT_REPO))
    args = parser.parse_args()

    cases = TEST_CASES
    if args.only:
        wanted = {i.upper() for i in args.only}
        cases = [c for c in TEST_CASES if c["id"].upper() in wanted]
        if not cases:
            parser.error(f"no test with id in {args.only}")

    repo_path = Path(args.repo).resolve()
    chunks = rag.chunk_code(rag.load_codebase(str(repo_path)), chunk_size=args.chunk_size)
    vector_store = rag.build_vector_store(chunks, model_name=args.model)
    agent = None if args.retrieval_only else rag.build_agent(vector_store, k=args.k)

    mode = "retrieval-only" if args.retrieval_only else "agent"
    lines = [
        f"# RAG eval: chunk={args.chunk_size}, k={args.k}, model={args.model}",
        "",
        f"- Date: {date.today()}  ·  Mode: {mode}  ·  Chunks: {len(chunks)} (overlap 32)",
        f"- Context per search ≈ k × chunk_size = {args.k * args.chunk_size} chars",
        "",
        "---",
        "",
    ]
    summaries = []
    for case in cases:
        print(f"Running {case['id']}…", flush=True)
        out, summary = run_test(case, vector_store, agent, args.k, repo_path)
        lines += out
        summaries.append(summary)

    lines += ["## Summary (fill in Facts, Wrong facts and Notes yourself)", "",
              "| ID | File hit | Chunk hit | Searches | Facts | Wrong facts | Notes |",
              "|---|---|---|---|---|---|---|"]
    lines += [f"| {s['id']} | {s['file_hit']} | {s['chunk_hit']} | {s['searches']} | {s['facts']} |  |  |"
              for s in summaries]

    report = "\n".join(lines)
    print("\n" + report)

    if args.save:
        model_slug = args.model.replace("/", "-")
        suffix = "_retrieval" if args.retrieval_only else ""
        path = HERE / "results" / f"chunk{args.chunk_size}_k{args.k}_{model_slug}{suffix}.md"
        path.parent.mkdir(exist_ok=True)
        path.write_text(report + "\n", encoding="utf-8")
        print(f"\nSaved → {path.relative_to(HERE.parents[1])}")


if __name__ == "__main__":
    main()
