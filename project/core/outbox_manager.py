import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import config
from core.execution_logger import log_error, log_tool_end, log_tool_start


def _slugify(text: str, max_len: int = 60) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return (text[:max_len].rstrip("-")) or "reply"


def split_subject_and_body(draft: str) -> tuple[str, str]:
    """Pull a leading ``Subject:`` line off the draft, if present."""
    lines = (draft or "").splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        match = re.match(r"(?i)^subject:\s*(.+)$", stripped)
        if match:
            body = "\n".join(lines[i + 1:]).strip()
            return match.group(1).strip(), body
        break
    return "(no subject)", (draft or "").strip()


class OutboxManager:
    """File-backed 'outbox' for replies a human has approved.

    Nothing here is written until the human approves the draft in the UI, so the
    contents of this directory are exactly the set of messages a person signed off
    on. Real deployments would swap ``send`` for an email/helpdesk API call.
    """

    def __init__(self, outbox_path: str | None = None):
        self.outbox_path = Path(outbox_path or config.OUTBOX_PATH)

    def _post_to_slack(self, subject: str, body: str) -> bool:
        webhook = getattr(config, "SLACK_WEBHOOK_URL", "")
        if not webhook:
            return False
        payload = json.dumps({"text": f"*{subject}*\n\n{body}"}).encode("utf-8")
        req = urllib.request.Request(
            webhook, data=payload, headers={"Content-Type": "application/json"}, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return 200 <= resp.status < 300
        except Exception as exc:
            log_error("outbox.slack", exc)
            return False

    def send(self, *, draft: str, query: str, revisions: int = 0) -> dict:
        """Deliver a human-approved reply. Always writes a file; also posts to
        Slack when SLACK_WEBHOOK_URL is set. Returns {path, delivered_to}."""
        log_tool_start("outbox.send", {"query": query, "revisions": revisions})
        try:
            self.outbox_path.mkdir(parents=True, exist_ok=True)
            subject, body = split_subject_and_body(draft)
            now = datetime.now(timezone.utc)
            filename = f"{now.strftime('%Y%m%dT%H%M%SZ')}__{_slugify(subject)}.md"
            file_path = self.outbox_path / filename

            slack_ok = self._post_to_slack(subject, body)
            channels = ["outbox/"] + (["Slack"] if slack_ok else [])

            front_matter = (
                "---\n"
                f"sent_at: {now.isoformat()}\n"
                f"subject: {subject}\n"
                f"in_reply_to_query: {query!r}\n"
                f"revisions_before_approval: {revisions}\n"
                f"delivered_to: {', '.join(channels)}\n"
                "approved_by: human (Gradio human-in-the-loop)\n"
                "---\n\n"
            )
            file_path.write_text(front_matter + body + "\n", encoding="utf-8")

            result = {"path": f"outbox/{filename}", "delivered_to": ", ".join(channels)}
            log_tool_end("outbox.send", result["path"])
            return result
        except Exception as exc:
            log_error("outbox.send", exc)
            raise
