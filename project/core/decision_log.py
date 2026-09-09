"""Append-only log of every approve / reject decision, plus how much the human
changed the draft. Turns the approval gate into a feedback signal: the edit ratio
trending down over time is evidence the drafter is getting better.
"""

import json
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

import config


def edit_ratio(model_draft: str, final_text: str) -> float:
    """0.0 = approved verbatim, 1.0 = completely rewritten."""
    a, b = (model_draft or "").strip(), (final_text or "").strip()
    if not a and not b:
        return 0.0
    return round(1.0 - SequenceMatcher(None, a, b).ratio(), 3)


def record(**fields) -> None:
    path = Path(config.DECISION_LOG_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": datetime.now(timezone.utc).isoformat(), **fields}
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def _read() -> list[dict]:
    path = Path(config.DECISION_LOG_PATH)
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def summary() -> dict:
    rows = _read()
    approved = [r for r in rows if r.get("decision") == "approved"]
    rejected = [r for r in rows if r.get("decision") == "rejected"]
    edits = [r["edit_ratio"] for r in approved if isinstance(r.get("edit_ratio"), (int, float))]
    verbatim = sum(1 for e in edits if e < 0.02)
    recent = list(reversed(rows[-12:]))
    return {
        "total": len(rows),
        "approved": len(approved),
        "rejected": len(rejected),
        "avg_edit_ratio": round(sum(edits) / len(edits), 3) if edits else None,
        "approved_verbatim": verbatim,
        "avg_critique_rounds": (
            round(sum(r.get("critique_rounds", 0) for r in approved) / len(approved), 2)
            if approved else None
        ),
        "recent": recent,
    }
