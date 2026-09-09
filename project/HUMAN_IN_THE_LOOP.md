# Human-in-the-Loop Outbound Replies

This project layers a **human approval gate** on top of the agentic RAG pipeline.
One agent researches an answer from the document set; a second agent drafts a
customer-ready reply; the graph then **pauses** and a person must approve, edit,
or reject the draft before it is written anywhere. Nothing is "sent" without a
human decision.

It is built with LangGraph's `interrupt_before` mechanism and the existing
`InMemorySaver` checkpointer, so the pause survives across UI turns on the same
thread.

`RAGSystem.initialize()` compiles the graph twice from the same nodes:
`agent_graph` (`hitl=False`, ends at `aggregate_answers`) drives the **Chat** tab
as plain Q&A, and `reply_graph` (`hitl=True`, the diagram below) drives the
**Draft Reply** tab.

## Flow

```
summarize_history → rewrite_query ─┬─▶ request_clarification  (existing HITL pause)
                                   │
                                   └─▶ agent (fan-out research) → aggregate_answers
                                                                        │
                                                                        ▼
                                                                  draft_reply          ← 2nd agent
                                                                        │
                                                                  human_approval  ⏸    ← interrupt_before
                                                                        │
                                                                  apply_decision
                                                       ┌────────────────┼────────────────┐
                                                   approve            revise           reject
                                                       ▼                │                ▼
                                                  send_reply  ──────────┘           discard_reply
                                                (writes outbox/)   (loop to draft)   (writes nothing)
```

| Node | Role |
|------|------|
| `draft_reply` | Second agent. Turns the researched answer + original question into a `Subject:` + body + `Sources:` reply. Re-runs with the reviewer's instructions on a revise loop. |
| `human_approval` | No-op node used purely as an `interrupt_before` pause point. |
| `apply_decision` | Classifies the human's chat reply as **approve** / **reject** / **revise** (anything else is treated as revision instructions) and tags that message so it stays out of chat history. |
| `send_reply` | Executor. Reached **only** on an explicit approval. Writes the approved message to `outbox/<timestamp>__<slug>.md` with front matter (`approved_by`, `revisions_before_approval`, original query). |
| `discard_reply` | Records the rejection; writes nothing. |

State fields added to `State` (`rag_agent/graph_state.py`): `researchedAnswer`,
`draftReply`, `replyFeedback`, `replyDecision`, `replyRevisionCount`,
`replyStatus`, `replyPath`. They are cleared at the top of every fresh turn in
`summarize_history`.

## Using it — the Draft Reply tab

1. Paste the message you need to answer into **Incoming message / question**.
2. Click **Research & draft reply**. The researched answer appears in the
   collapsible context box; the draft appears in the editable **Proposed reply**
   box; the graph is now paused at `human_approval`.
3. Edit the draft directly if you want, then:
   - **Approve & save to outbox** — your edited text (not just the model's
     original) is written to `outbox/`.
   - **Discard** — nothing is written.
   - **Redraft with changes** — type instructions, the drafter rewrites, and the
     graph pauses again.

`RAGSystem.start_reply / revise_reply / approve_reply / discard_reply` drive the
`reply_graph` for these buttons. Each draft runs on its own thread id.
`approve_reply` writes the edited text back to the `draftReply` channel with
`update_state` before resuming, so `send_reply` persists exactly what you approved.

The chat-typed `approve` / `reject` / revision path still works on `reply_graph`
(see `apply_decision`); the dedicated tab is just a friendlier front end for it.

## Configuration

| Setting | Where | Default | Notes |
|---------|-------|---------|-------|
| `HITL_REPLY_ENABLED` | env / `config.py` | `true` | `false` restores the original "answer only, end at `aggregate_answers`" graph. |
| `LLM_PROVIDER` | env / `config.py` | `anthropic` | `anthropic` (needs `ANTHROPIC_API_KEY`), `ollama`, or `openai`. |
| `ANTHROPIC_MODEL` | env / `config.py` | `claude-opus-5` | Set to `claude-sonnet-5` or `claude-haiku-4-5` to reduce cost. |
| `DRAFTER_MODEL` | env / `config.py` | *(blank)* | Model for `draft_reply`; blank = same as the main model. The researcher and drafter are separate model instances with separate system prompts. |

Copy `project/.env.example` to `project/.env` and fill in `ANTHROPIC_API_KEY`.

## Why this design

- **The gate is structural, not advisory.** `send_reply` is unreachable except
  through `apply_decision` returning `approved`. There is no code path that
  writes the outbox without a human turn in between.
- **Auditable output.** Every file in `outbox/` carries the query it answered,
  how many revisions it took, and that a human approved it.
- **Toggle for regression testing.** `HITL_REPLY_ENABLED=false` gives back the
  exact previous behaviour, so the RAG evaluation notebooks are unaffected.
