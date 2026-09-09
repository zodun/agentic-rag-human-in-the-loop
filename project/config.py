import os

# --- Directory Configuration ---
_BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MARKDOWN_DIR = os.path.join(_BASE_DIR, "markdown_docs")
PARENT_STORE_PATH = os.path.join(_BASE_DIR, "parent_store")
QDRANT_DB_PATH = os.path.join(_BASE_DIR, "qdrant_db")
OUTBOX_PATH = os.path.join(_BASE_DIR, "outbox")

# --- LLM Provider Configuration ---
# "anthropic" (default) reads ANTHROPIC_API_KEY; "ollama" uses a local model
# (LLM_MODEL below); "openai" reads OPENAI_API_KEY.
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "anthropic").lower()
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
# Point the OpenAI client at an OpenAI-compatible API. For DeepSeek set
# OPENAI_BASE_URL=https://api.deepseek.com and OPENAI_MODEL=deepseek-chat
# (deepseek-chat supports the forced tool calls this app needs; the v4 "thinking"
# models do not). Blank base URL = real OpenAI.
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "")
LLM_MAX_TOKENS = int(os.environ.get("LLM_MAX_TOKENS", "8192"))
# Model used by the reply-drafting agent. Blank = same as the main model.
DRAFTER_MODEL = os.environ.get("DRAFTER_MODEL", "")

# --- Human-in-the-loop outbound reply ---
# When enabled, a second agent drafts a customer-ready reply after research and
# the graph pauses for human approval before the reply is written to the outbox.
HITL_REPLY_ENABLED = os.environ.get("HITL_REPLY_ENABLED", "true").lower() == "true"

# Show the agent's internal steps in chat (history summary, query analysis, each
# retrieval call). Off by default keeps the transcript readable; on is useful for
# debugging or demos of the pipeline.
SHOW_AGENT_STEPS = os.environ.get("SHOW_AGENT_STEPS", "false").lower() == "true"

# A reviewer agent checks each draft against the researched answer before the
# human sees it (unsupported claims, missing caveats, tone). One auto-revision.
CRITIC_ENABLED = os.environ.get("CRITIC_ENABLED", "true").lower() == "true"

# Let the agent fall back to a public web search when the documents do not cover
# a question (e.g. salary benchmarks). Off by default keeps answers strictly
# grounded; anything from the web is labelled "Estimate (not from your documents)".
WEB_SEARCH_ENABLED = os.environ.get("WEB_SEARCH_ENABLED", "false").lower() == "true"
WEB_SEARCH_MAX_RESULTS = int(os.environ.get("WEB_SEARCH_MAX_RESULTS", "5"))

# If set, an approved reply is also POSTed to this Slack Incoming Webhook (still
# only after human approval). Unset = the reply is only written to outbox/.
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")

# SMTP: if configured, an approved reply is emailed to the recipient entered in
# the Draft Reply tab (or EMAIL_TO as a default). Gmail needs an App Password.
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_FROM = os.environ.get("SMTP_FROM", "")
EMAIL_TO = os.environ.get("EMAIL_TO", "")

# Where the approve / reject / edit-distance log is written.
DECISION_LOG_PATH = os.path.join(OUTBOX_PATH, "_decisions.jsonl")

# --- Qdrant Configuration ---
CHILD_COLLECTION = "document_child_chunks"
SPARSE_VECTOR_NAME = "sparse"

# --- Model Configuration ---
# all-MiniLM-L6-v2 is small and fast on CPU (seconds to index a document).
# Set DENSE_MODEL=Qwen/Qwen3-Embedding-0.6B for higher quality if you have a GPU.
DENSE_MODEL = os.environ.get("DENSE_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
SPARSE_MODEL = "Qdrant/bm25"
LLM_MODEL = "granite4.1:8b"
JUDGE_MODEL = "ministral-3:3b-instruct-2512-q8_0"
LLM_TEMPERATURE = 0
LLM_SEED = 42

# --- Retrieval Configuration ---
RETRIEVAL_SCORE_THRESHOLD = 0.4
DEFAULT_RETRIEVAL_K = 7
CHILD_CHUNK_SEPARATOR = "\n\n<CHILD_CHUNK_BOUNDARY>\n\n"

# --- Agent Configuration ---
MAX_TOOL_CALLS = 8
MAX_ITERATIONS = 10
GRAPH_RECURSION_LIMIT = 50
MAIN_HISTORY_MESSAGES_TO_KEEP = 4
BASE_TOKEN_THRESHOLD = 2000
TOKEN_GROWTH_FACTOR = 0.9

# --- Terminal Execution Logging ---
EXECUTION_LOGGING_ENABLED = False
EXECUTION_LOG_MAX_CHARS = 1200
EXECUTION_LOG_USE_COLOR = True

# --- Text Splitter Configuration ---
CHILD_CHUNK_SIZE = 500
CHILD_CHUNK_OVERLAP = 100
MIN_PARENT_SIZE = 2000
MAX_PARENT_SIZE = 4000
HEADERS_TO_SPLIT_ON = [
    ("#", "H1"),
    ("##", "H2"),
    ("###", "H3")
]

# --- Langfuse Observability ---
LANGFUSE_ENABLED = os.environ.get("LANGFUSE_ENABLED", "false").lower() == "true"
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")
LANGFUSE_BASE_URL = os.environ.get("LANGFUSE_BASE_URL", "http://localhost:3000")
