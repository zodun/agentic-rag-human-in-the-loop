# Agentic RAG with Human-in-the-Loop Reply Approval

A multi-agent RAG system where one agent researches an answer from your documents,
a second agent drafts an outbound reply, and **a human approves, edits, or rejects
that draft before anything is sent.**

---

## The idea

Two separate surfaces:

- **Chat tab** — plain Q&A over your documents. Ask a question, get a grounded
  answer with sources. Nothing is drafted or sent.
- **Draft Reply tab** — paste a message you need to answer (from a customer, a
  recruiter, a colleague). The system researches a grounded answer, drafts a
  send-ready reply (subject, greeting, body, sign-off, sources), and **pauses**.
  You edit the draft directly, then choose:

| Action | What happens |
|---|---|
| **Approve & save** | The reply — including any edits you made in the box — is written to `outbox/` as a timestamped Markdown file with front matter recording that a human approved it |
| **Discard** | Nothing is written |
| **Redraft with changes** | The drafter rewrites with your instructions and pauses again |

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

Implemented with LangGraph's `interrupt_before` and the in-memory checkpointer. Two
graphs are compiled from the same nodes: one without the reply stage for the Chat
tab, one with it for the Draft Reply tab. Full node-by-node write-up:
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
2. **Chat** tab → ask questions about the document (grounded answers with sources)
3. **Draft Reply** tab → paste a message → *Research & draft reply* → edit the
   draft → *Approve & save* / *Discard* / *Redraft with changes*
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
| **Human-in-the-loop reply** | New `project/rag_agent/reply_drafter.py` (drafter agent, approval pause, decision router, executor) and `project/core/outbox_manager.py`. Exposed as a dedicated **Draft Reply** tab with edit-in-place + approve/discard/redraft, kept separate from the Q&A chat |
| **Anthropic provider** | `build_llm()` provider factory in `project/core/rag_system.py` (Anthropic / Ollama / OpenAI); dropped `temperature` for models that reject it; normalized responses whose `content` is a list of blocks (thinking + text) across the nodes and the token streamer |
| **Local Qdrant + Gradio** | `force_disable_check_same_thread=True` on the Qdrant client — Gradio runs handlers on worker threads and macOS SQLite otherwise refuses the cross-thread connection, which was silently failing every document upload |
| **Ingestion robustness** | A failed upload now rolls back its orphaned vector-store chunks (not just the parent files) and prints a real traceback |
| **UI** | Hides internal agent chatter by default, calm light theme, clearer separation between the answer, the drafted reply, and the approval prompt |

Deeper documentation of the RAG pipeline is in
[`project/README.md`](project/README.md).

---

## License

MIT. See [`LICENSE`](LICENSE).
