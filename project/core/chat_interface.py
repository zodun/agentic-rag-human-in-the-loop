import json
import re
from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage, ToolMessage
import config
from core.execution_logger import log_chat_end, log_chat_start, log_error

SYSTEM_NODES = {"summarize_history", "rewrite_query"}
FINAL_RESPONSE_NODES = {"aggregate_answers"}
REPLY_DRAFT_NODE = "draft_reply"

SYSTEM_NODE_CONFIG = {
    "rewrite_query":     {"title": "🔍 Query Analysis & Rewriting"},
    "summarize_history": {"title": "📋 Chat History Summary"},
}

# --- Helpers ---

def _chunk_text(chunk) -> str:
    """Text of a streamed chunk. Providers like Anthropic return ``content`` as a
    list of typed blocks (text, thinking); ``.text`` yields only the text parts."""
    text_attr = getattr(chunk, "text", None)
    if isinstance(text_attr, str):
        return text_attr
    if callable(text_attr):
        try:
            return text_attr() or ""
        except Exception:
            pass
    content = getattr(chunk, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            b if isinstance(b, str) else (b.get("text", "") if isinstance(b, dict) and b.get("type") == "text" else "")
            for b in content
        )
    return ""


def make_message(content, *, title=None, node=None):
    msg = {"role": "assistant", "content": content}
    if title or node:
        msg["metadata"] = {k: v for k, v in {"title": title, "node": node}.items() if v}
    return msg


def find_msg_idx(messages, node):
    return next(
        (i for i, m in enumerate(messages) if m.get("metadata", {}).get("node") == node),
        None,
    )


def parse_rewrite_json(buffer):
    match = re.search(r"\{.*\}", buffer, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except Exception:
        return None


def format_rewrite_content(buffer):
    data = parse_rewrite_json(buffer)
    if not data:
        return "⏳ Analyzing query..."
    if data.get("is_clear"):
        lines = ["✅ **Query is clear**"]
        if data.get("questions"):
            lines += ["\n**Rewritten queries:**"] + [f"- {q}" for q in data["questions"]]
    else:
        lines = ["❓ **Query is unclear**"]
        clarification = data.get("clarification_needed", "")
        if clarification and clarification.strip().lower() != "no":
            lines.append(f"\nClarification needed: *{clarification}*")
    return "\n".join(lines)

# --- End of Helpers ---

class ChatInterface:

    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.show_steps = getattr(config, "SHOW_AGENT_STEPS", False)

    def _handle_system_node(self, chunk, node, response_messages, system_node_buffer):
        """Update (or create) the collapsible system-node message and surface any clarification."""
        system_node_buffer[node] = system_node_buffer.get(node, "") + _chunk_text(chunk)
        buffer = system_node_buffer[node]

        if node == "rewrite_query":
            self._surface_clarification(buffer, response_messages)
            if not parse_rewrite_json(buffer):
                return  # nothing parseable yet - don't leave an "Analyzing query..." box

        if not self.show_steps:
            return

        title  = SYSTEM_NODE_CONFIG[node]["title"]
        content = format_rewrite_content(buffer) if node == "rewrite_query" else buffer

        idx = find_msg_idx(response_messages, node)
        if idx is None:
            response_messages.append(make_message(content, title=title, node=node))
        else:
            response_messages[idx]["content"] = content

    def _surface_clarification(self, buffer, response_messages):
        """If the query is unclear, add/update a plain clarification message."""
        data          = parse_rewrite_json(buffer) or {}
        clarification = data.get("clarification_needed", "")
        if not data.get("is_clear") and clarification.strip().lower() not in ("", "no"):
            cidx = find_msg_idx(response_messages, "clarification")
            if cidx is None:
                response_messages.append(make_message(clarification, node="clarification"))
            else:
                response_messages[cidx]["content"] = clarification

    def _handle_tool_call(self, chunk, response_messages, active_tool_calls):
        """Register new tool calls as collapsible messages."""
        for tc in chunk.tool_calls:
            if tc.get("id") and tc["id"] not in active_tool_calls:
                query = (tc.get("args") or {}).get("query") or (tc.get("args") or {}).get("parent_id") or ""
                label = f"🔎 {tc['name']}" + (f": {query}" if query else "")
                response_messages.append(make_message("Searching…", title=label))
                active_tool_calls[tc["id"]] = len(response_messages) - 1

    def _handle_tool_result(self, chunk, response_messages, active_tool_calls):
        """Fill in the tool result inside the matching collapsible message."""
        idx = active_tool_calls.get(chunk.tool_call_id)
        if idx is not None:
            preview = " ".join(str(chunk.content).split())[:280]
            suffix  = "…" if len(str(chunk.content)) > 280 else ""
            response_messages[idx]["content"] = preview + suffix or "(no results)"

    def _handle_llm_token(self, chunk, node, response_messages):
        """Append streaming LLM tokens to the last plain assistant message."""
        last = response_messages[-1] if response_messages else None
        if not (last and last.get("role") == "assistant" and "metadata" not in last):
            response_messages.append(make_message(""))
        response_messages[-1]["content"] += _chunk_text(chunk)

    def chat(self, message, history):
        """Generator that streams Gradio chat message dicts."""
        if not self.rag_system.agent_graph:
            yield "⚠️ System not initialized!"
            return

        config        = self.rag_system.get_config()
        current_state = self.rag_system.agent_graph.get_state(config)
        log_chat_start(message.strip(), self.rag_system.thread_id, bool(current_state.next))

        try:
            if current_state.next:
                self.rag_system.agent_graph.update_state(config, {"messages": [HumanMessage(content=message.strip())]})
                stream_input = None
            else:
                stream_input = {"messages": [HumanMessage(content=message.strip())]}

            response_messages  = []
            active_tool_calls  = {}
            system_node_buffer = {}
            draft_started      = False

            def clear_status():
                response_messages[:] = [m for m in response_messages
                                        if m.get("metadata", {}).get("node") != "status"]

            for chunk, metadata in self.rag_system.agent_graph.stream(stream_input, config=config, stream_mode="messages"):
                node = metadata.get("langgraph_node", "")

                if node in SYSTEM_NODES and isinstance(chunk, AIMessageChunk) and _chunk_text(chunk):
                    self._handle_system_node(chunk, node, response_messages, system_node_buffer)

                elif hasattr(chunk, "tool_calls") and chunk.tool_calls:
                    if self.show_steps:
                        self._handle_tool_call(chunk, response_messages, active_tool_calls)
                    elif find_msg_idx(response_messages, "status") is None:
                        response_messages.append(make_message("_Researching your question…_", node="status"))
                    else:
                        continue

                elif isinstance(chunk, ToolMessage):
                    if not self.show_steps:
                        continue
                    self._handle_tool_result(chunk, response_messages, active_tool_calls)

                elif isinstance(chunk, AIMessageChunk) and _chunk_text(chunk) and node in FINAL_RESPONSE_NODES:
                    clear_status()
                    self._handle_llm_token(chunk, node, response_messages)

                elif isinstance(chunk, AIMessageChunk) and _chunk_text(chunk) and node == REPLY_DRAFT_NODE:
                    clear_status()
                    if not draft_started:
                        draft_started = True
                        response_messages.append(make_message("---\n#### ✉️ Proposed reply\n\n"))
                    self._handle_llm_token(chunk, node, response_messages)

                else:
                    continue

                yield response_messages

            final_state = self.rag_system.agent_graph.get_state(config)
            log_chat_end(getattr(final_state, "values", final_state))

            for extra in self._reply_status_messages(final_state, response_messages):
                response_messages.append(extra)
                yield response_messages

        except Exception as e:
            log_error("chat", e)
            yield f"❌ Error: {str(e)}"

    def _reply_status_messages(self, final_state, response_messages):
        """After a run, surface the approval prompt or the send/discard receipt."""
        values = getattr(final_state, "values", {}) or {}
        next_nodes = getattr(final_state, "next", ()) or ()

        if "request_clarification" in next_nodes:
            # Fallback for providers that don't stream structured output as text:
            # make sure the clarification question is visible before the pause.
            if find_msg_idx(response_messages, "clarification") is not None:
                return []
            clarification = next(
                (m.content for m in reversed(values.get("messages", []))
                 if isinstance(m, AIMessage) and getattr(m, "name", None) == "clarification"),
                "",
            )
            return [make_message(clarification, node="clarification")] if clarification else []

        if "human_approval" in next_nodes:
            revisions = values.get("replyRevisionCount", 0)
            note = " _(revised once)_" if revisions == 1 else (f" _(revised {revisions}×)_" if revisions else "")
            return [make_message(
                "> **Your call:** reply **approve** to send this, **reject** to discard it, "
                f"or say what to change.{note}"
            )]

        status = values.get("replyStatus")
        if status == "sent":
            return [make_message(f"> ✅ **Approved and sent** — saved to `{values.get('replyPath', 'outbox/')}`")]
        if status == "discarded":
            return [make_message("> 🗑️ **Discarded** — nothing was sent")]
        return []

    def clear_session(self):
        self.rag_system.reset_thread()
        self.rag_system.observability.flush()
