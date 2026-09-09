import os
import uuid
from langchain_core.messages import AIMessage, HumanMessage
import config
from db.vector_db_manager import VectorDbManager
from db.parent_store_manager import ParentStoreManager
from document_chunker import DocumentChunker
from rag_agent.tools import ToolFactory
from rag_agent.graph import create_agent_graph
from core.observability import Observability
from core import decision_log


def build_llm(model_override: str | None = None):
    """Create a chat model for the configured provider (see config.LLM_PROVIDER)."""
    provider = config.LLM_PROVIDER

    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=model_override or config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE,
            seed=config.LLM_SEED,
        )

    if provider == "anthropic":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Add it to project/.env (or export it), "
                "or set LLM_PROVIDER=ollama to run fully local."
            )
        from langchain_anthropic import ChatAnthropic
        # Current Claude models (Opus 5 / Sonnet 5 / 4.6+) reject `temperature`.
        return ChatAnthropic(
            model=model_override or config.ANTHROPIC_MODEL,
            max_tokens=config.LLM_MAX_TOKENS,
        )

    if provider == "openai":
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set. Add it to project/.env or export it.")
        from langchain_openai import ChatOpenAI
        # Also used for OpenAI-compatible APIs (DeepSeek, etc.) via OPENAI_BASE_URL.
        kwargs = {
            "model": model_override or config.OPENAI_MODEL,
            "max_tokens": config.LLM_MAX_TOKENS,
        }
        base_url = getattr(config, "OPENAI_BASE_URL", "")
        if base_url:
            kwargs["base_url"] = base_url
        return ChatOpenAI(**kwargs)

    raise ValueError(f"Unsupported LLM_PROVIDER: {config.LLM_PROVIDER!r} (use anthropic, ollama, or openai)")

class RAGSystem:

    def __init__(self, collection_name=config.CHILD_COLLECTION):
        self.collection_name = collection_name
        self.vector_db = VectorDbManager()
        self.parent_store = ParentStoreManager()
        self.chunker = DocumentChunker()
        self.observability = Observability()
        self.agent_graph = None    # Chat tab: plain Q&A (no reply drafting)
        self.reply_graph = None    # Draft Reply tab: research -> draft -> human approval
        self.thread_id = str(uuid.uuid4())
        self.recursion_limit = config.GRAPH_RECURSION_LIMIT

    def initialize(self):
        self.vector_db.create_collection(self.collection_name)
        collection = self.vector_db.get_collection(self.collection_name)

        llm = build_llm()
        draft_llm = build_llm(config.DRAFTER_MODEL or None)
        tools = ToolFactory(collection).create_tools()
        self.agent_graph = create_agent_graph(llm, tools, draft_llm=draft_llm, hitl=False)
        if config.HITL_REPLY_ENABLED:
            self.reply_graph = create_agent_graph(llm, tools, draft_llm=draft_llm, hitl=True)

    def get_config(self):
        cfg = {"configurable": {"thread_id": self.thread_id}, "recursion_limit": self.recursion_limit}
        handler = self.observability.get_handler()
        if handler:
            cfg["callbacks"] = [handler]
        return cfg

    def reset_thread(self):
        try:
            self.agent_graph.checkpointer.delete_thread(self.thread_id)
        except Exception as e:
            print(f"Warning: Could not delete thread {self.thread_id}: {e}")
        self.thread_id = str(uuid.uuid4())

    # ------------------------------------------------------------------
    # Draft Reply workflow (Draft Reply tab). Each call chain uses its own
    # LangGraph thread id so drafts don't collide with the chat session.
    # ------------------------------------------------------------------
    def _reply_cfg(self, thread_id):
        cfg = {"configurable": {"thread_id": thread_id}, "recursion_limit": self.recursion_limit}
        handler = self.observability.get_handler()
        if handler:
            cfg["callbacks"] = [handler]
        return cfg

    def start_reply(self, question: str) -> dict:
        """Research the question and produce a first draft. Returns the thread id,
        the grounded answer, the draft, and whether the graph needs clarification."""
        thread_id = str(uuid.uuid4())
        cfg = self._reply_cfg(thread_id)
        self.reply_graph.invoke({"messages": [HumanMessage(content=question.strip())]}, cfg)
        state = self.reply_graph.get_state(cfg)
        values = state.values or {}
        next_nodes = state.next or ()

        if "request_clarification" in next_nodes:
            clarification = next(
                (m.content for m in reversed(values.get("messages", []))
                 if isinstance(m, AIMessage) and getattr(m, "name", None) == "clarification"),
                "The question needs more detail to answer.",
            )
            return {"thread_id": thread_id, "answer": clarification, "draft": "",
                    "passages": [], "critique_notes": [], "needs_clarification": True}

        return {
            "thread_id": thread_id,
            "answer": values.get("researchedAnswer", ""),
            "draft": values.get("draftReply", ""),
            "passages": values.get("retrievedPassages", []),
            "critique_notes": values.get("critiqueNotes", []),
            "needs_clarification": False,
        }

    def revise_reply(self, thread_id: str, instructions: str) -> dict:
        """Redraft with reviewer instructions. Returns the new draft + critic notes."""
        cfg = self._reply_cfg(thread_id)
        self.reply_graph.update_state(cfg, {"messages": [HumanMessage(content=instructions.strip())]})
        self.reply_graph.invoke(None, cfg)
        values = self.reply_graph.get_state(cfg).values or {}
        return {"draft": values.get("draftReply", ""), "critique_notes": values.get("critiqueNotes", [])}

    def approve_reply(self, thread_id: str, final_text: str) -> dict:
        """Approve the (possibly hand-edited) text, deliver it, and log the decision
        plus how far the human moved it from the model's draft."""
        cfg = self._reply_cfg(thread_id)
        before = (self.reply_graph.get_state(cfg).values or {})
        model_draft = before.get("draftReply", "")

        self.reply_graph.update_state(cfg, {"draftReply": final_text})
        self.reply_graph.update_state(cfg, {"messages": [HumanMessage(content="approve")]})
        self.reply_graph.invoke(None, cfg)
        after = self.reply_graph.get_state(cfg).values or {}

        decision_log.record(
            decision="approved",
            query=after.get("originalQuery", ""),
            revisions=after.get("replyRevisionCount", 0),
            critique_rounds=after.get("critiqueRounds", 0),
            edit_ratio=decision_log.edit_ratio(model_draft, final_text),
            delivered_to=after.get("replyDeliveredTo", "outbox/"),
        )
        return {"path": after.get("replyPath", ""), "delivered_to": after.get("replyDeliveredTo", "outbox/")}

    def activity_summary(self) -> dict:
        return decision_log.summary()

    def discard_reply(self, thread_id: str) -> None:
        cfg = self._reply_cfg(thread_id)
        try:
            values = self.reply_graph.get_state(cfg).values or {}
            decision_log.record(
                decision="rejected",
                query=values.get("originalQuery", ""),
                revisions=values.get("replyRevisionCount", 0),
                critique_rounds=values.get("critiqueRounds", 0),
            )
            self.reply_graph.update_state(cfg, {"messages": [HumanMessage(content="reject")]})
            self.reply_graph.invoke(None, cfg)
            self.reply_graph.checkpointer.delete_thread(thread_id)
        except Exception as e:
            print(f"Warning: could not discard reply thread {thread_id}: {e}")
