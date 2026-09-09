import os
import uuid
import config
from db.vector_db_manager import VectorDbManager
from db.parent_store_manager import ParentStoreManager
from document_chunker import DocumentChunker
from rag_agent.tools import ToolFactory
from rag_agent.graph import create_agent_graph
from core.observability import Observability


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
        # gpt-5 family only accepts the default temperature; leave it unset.
        return ChatOpenAI(
            model=model_override or config.OPENAI_MODEL,
            max_completion_tokens=config.LLM_MAX_TOKENS,
        )

    raise ValueError(f"Unsupported LLM_PROVIDER: {config.LLM_PROVIDER!r} (use anthropic, ollama, or openai)")

class RAGSystem:

    def __init__(self, collection_name=config.CHILD_COLLECTION):
        self.collection_name = collection_name
        self.vector_db = VectorDbManager()
        self.parent_store = ParentStoreManager()
        self.chunker = DocumentChunker()
        self.observability = Observability()
        self.agent_graph = None
        self.thread_id = str(uuid.uuid4())
        self.recursion_limit = config.GRAPH_RECURSION_LIMIT

    def initialize(self):
        self.vector_db.create_collection(self.collection_name)
        collection = self.vector_db.get_collection(self.collection_name)

        llm = build_llm()
        draft_llm = build_llm(config.DRAFTER_MODEL or None)
        tools = ToolFactory(collection).create_tools()
        self.agent_graph = create_agent_graph(llm, tools, draft_llm=draft_llm)

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
