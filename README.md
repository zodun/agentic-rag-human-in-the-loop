# Agentic RAG with Human-in-the-Loop Reply Approval

A multi-agent RAG system where one agent researches an answer from your documents,
a second agent drafts an outbound reply, and **a human approves, edits, or rejects
that draft before anything is sent.**

Built on [`GiovanniPasq/agentic-rag-for-dummies`](https://github.com/GiovanniPasq/agentic-rag-for-dummies)
(MIT), which supplies the LangGraph agent, parent/child chunking, and hybrid
retrieval. This fork adds the approval gate, an Anthropic provider path, a fix for
running local Qdrant under Gradio's threads, and a cleaner UI. See
[What changed here](#what-changed-here).

---

## The idea

The app treats your question as an **incoming message you need to respond to** (a
customer, a recruiter, a colleague). It does two things:

1. **Answers it** — the existing agentic RAG pipeline retrieves from your uploaded
   documents and produces a grounded answer with sources.
2. **Drafts the reply** — a separate agent turns that answer into a send-ready
   message: subject, greeting, body, sign-off, sources.

Then the graph **pauses**. Nothing is written anywhere until you respond in the chat:

| You type | What happens |
|---|---|
| `approve` (also `yes`, `send`, `lgtm`) | The reply is written to `outbox/` as a timestamped Markdown file with front matter recording that a human approved it |
| `reject` (also `no`, `discard`) | Discarded. Nothing is written. |
| anything else | Treated as revision instructions — the drafter rewrites and asks again |

The gate is structural, not advisory: the "send" node is unreachable except through
an explicit approval, so `outbox/` only ever contains messages a person signed off on.

## Flow

```
                       ┌─ request_clarification ──┐   (pause: ask the user to clarify)
summarize → rewrite ───┤                          │
                       └─ research agents (fan-out, retrieve) ─→ aggregate answer
                                                                      │
                                                                draft_reply            ← second agent
                                                                      │
                                                                human_approval  ⏸      ← interrupt_before
                                                                      │
                                                                apply_decision
                                              ┌──────────────────────┼──────────────────────┐
                                          approve                  revise                 reject
                                              ▼                      │                      ▼
                                         send_reply  ────────────────┘                 discard_reply
                                     (writes outbox/)      (loop back to draft)        (writes nothing)
```

Implemented with LangGraph's `interrupt_before` and the in-memory checkpointer, so
the pause survives across chat turns on the same thread. Full node-by-node write-up:
[`project/HUMAN_IN_THE_LOOP.md`](project/HUMAN_IN_THE_LOOP.md).

---

## Quick start

```bash
pip install -r requirements.txt

cp project/.env.example project/.env
# set ANTHROPIC_API_KEY in project/.env  (or set LLM_PROVIDER=ollama to run fully local)

python project/app.py            # http://localhost:7860
```

Then:

1. **Documents** tab → upload a PDF or Markdown file → *Add Documents*
2. **Chat** tab → ask a question about that document
3. Review the drafted reply → type `approve`, `reject`, or what to change
4. Check `outbox/` for approved replies

### Good questions to ask

Anything a real person would send you that your documents can answer:

- with a resume loaded: *"What was the candidate's first job?"*, *"Do they have incident-response experience?"*, *"Are they available for a full-time role, and where are they based?"*
- with a policy or product doc: *"Can a monthly customer get a refund after 10 days?"*, *"How long does processing take?"*

Questions with no answer in the documents get an honest "we couldn't find that" draft
rather than a guess.

---

## Configuration

Set in `project/.env` or `project/config.py`.

| Setting | Default | Notes |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` | `anthropic` (needs `ANTHROPIC_API_KEY`), `ollama`, or `openai` |
| `ANTHROPIC_MODEL` | `claude-opus-5` | set to `claude-sonnet-5` or `claude-haiku-4-5` to cut cost |
| `DRAFTER_MODEL` | *(blank)* | model for the reply-drafting agent; blank = same as the main model |
| `HITL_REPLY_ENABLED` | `true` | `false` restores the original "answer only" graph |
| `SHOW_AGENT_STEPS` | `false` | `true` shows the retrieval steps in the chat for demos/debugging |

---

## What changed here

| Area | Change |
|---|---|
| **Human-in-the-loop reply** | New `project/rag_agent/reply_drafter.py` (drafter agent, approval pause, decision router, executor) and `project/core/outbox_manager.py`; wired into the graph behind `HITL_REPLY_ENABLED` |
| **Anthropic provider** | `build_llm()` provider factory in `project/core/rag_system.py` (Anthropic / Ollama / OpenAI); dropped `temperature` for models that reject it; normalized responses whose `content` is a list of blocks (thinking + text) across the nodes and the token streamer |
| **Local Qdrant + Gradio** | `force_disable_check_same_thread=True` on the Qdrant client — Gradio runs handlers on worker threads and macOS SQLite otherwise refuses the cross-thread connection, which was silently failing every document upload |
| **Ingestion robustness** | A failed upload now rolls back its orphaned vector-store chunks (not just the parent files) and prints a real traceback |
| **UI** | Hides internal agent chatter by default, calm light theme, clearer separation between the answer, the drafted reply, and the approval prompt |

The upstream project's own documentation is preserved at
[`README.upstream.md`](README.upstream.md) and [`project/README.md`](project/README.md).

---

## Credit & license

Original work: **agentic-rag-for-dummies** by Giovanni Pasqualino —
<https://github.com/GiovanniPasq/agentic-rag-for-dummies>.

MIT licensed. See [`LICENSE`](LICENSE).
