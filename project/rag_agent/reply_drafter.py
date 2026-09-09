"""Human-in-the-loop outbound reply stage.

After the research agents produce a grounded answer (``aggregate_answers``), a
second agent drafts a customer-ready reply. The graph then pauses on
``human_approval`` (``interrupt_before``) so a person can approve, reject, or
request changes. Only an explicit approval reaches ``send_reply``, which writes
the message to the file-backed outbox. Nothing is sent without human sign-off.
"""

from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

import config
from .graph_state import State
from .nodes import _text
from .prompts import get_reply_critic_prompt, get_reply_drafter_prompt
from .schemas import ReplyCritique

CRITIC_MAX_ROUNDS = 1

APPROVE_WORDS = {
    "approve", "approved", "approve it", "yes", "y", "send", "send it", "ok", "okay",
    "lgtm", "looks good", "ship it", "go ahead",
}
REJECT_WORDS = {
    "reject", "rejected", "reject it", "no", "n", "discard", "cancel", "stop",
    "don't send", "do not send", "dont send", "scrap it",
}


def _name_internal_message(message, name):
    """Tag a message so it is excluded from plain chat history."""
    return message.model_copy(update={"name": name})


def _last_human_message(messages):
    return next((m for m in reversed(messages) if isinstance(m, HumanMessage)), None)


def draft_reply(state: State, llm):
    """Second agent: turn the researched answer into an outbound reply draft."""
    researched_answer = state.get("researchedAnswer", "").strip()
    if not researched_answer:
        researched_answer = next(
            (_text(m) for m in reversed(state.get("messages", [])) if isinstance(m, AIMessage) and _text(m)),
            "",
        )

    original_query = state.get("originalQuery", "").strip() or "(question unavailable)"
    feedback = state.get("replyFeedback", "").strip()
    previous_draft = state.get("draftReply", "").strip()

    context_parts = [
        f"Original question:\n{original_query}",
        f"Researched answer (grounded in documentation):\n{researched_answer}",
    ]
    if feedback and previous_draft:
        context_parts.append(f"Previous draft:\n{previous_draft}")
        context_parts.append(f"Reviewer's revision instructions (apply these):\n{feedback}")

    response = llm.invoke([
        SystemMessage(content=get_reply_drafter_prompt()),
        HumanMessage(content="\n\n".join(context_parts)),
    ])
    draft = _text(response).strip().replace("~", "≈")  # "~" renders as strikethrough

    revisions = state.get("replyRevisionCount", 0) + (1 if feedback else 0)
    return {
        "messages": [AIMessage(content=draft, name="reply_draft")],
        "draftReply": draft,
        "replyFeedback": "",
        "replyDecision": "",
        "replyRevisionCount": revisions,
    }


def critique_reply(state: State, llm):
    """Reviewer agent. Checks the draft against the researched answer before a
    human sees it. On a first failure it sends the draft back for one auto-revision;
    after that it passes any remaining notes through for the human to weigh."""
    draft = state.get("draftReply", "").strip()
    answer = state.get("researchedAnswer", "").strip()
    rounds = state.get("critiqueRounds", 0)

    context = (
        f"Researched answer:\n{answer}\n\n"
        f"Drafted reply:\n{draft}"
    )
    prior_feedback = state.get("replyFeedback", "").strip()
    if prior_feedback:
        context += f"\n\nReviewer instructions that were meant to be applied:\n{prior_feedback}"

    try:
        critique = llm.with_structured_output(ReplyCritique).invoke([
            SystemMessage(content=get_reply_critic_prompt()),
            HumanMessage(content=context),
        ])
        issues = [i.strip() for i in (critique.issues or []) if i.strip()]
        ok = bool(critique.ok) and not issues
    except Exception as exc:  # never block the pipeline on the critic
        print(f"critique_reply: skipped ({exc})")
        return {"critiqueNotes": [], "critiqueRounds": rounds}

    if not ok and rounds < CRITIC_MAX_ROUNDS:
        return {
            "replyFeedback": "A reviewer flagged these; fix them: " + "; ".join(issues),
            "critiqueRounds": rounds + 1,
            "critiqueNotes": [],
        }
    return {"critiqueNotes": issues, "critiqueRounds": rounds}


def route_after_critique(state: State) -> Literal["draft_reply", "human_approval"]:
    # If the critic left feedback this round, it wants another draft.
    return "draft_reply" if state.get("replyFeedback", "").strip() else "human_approval"


def human_approval(state: State):
    """Interrupt point. Execution pauses here until a human responds."""
    return {}


def apply_decision(state: State):
    """Interpret the human's reply to the draft as approve / reject / revise."""
    last_human = _last_human_message(state.get("messages", []))
    raw = (last_human.content if last_human else "").strip()
    normalized = raw.lower().rstrip(".!")

    rename = (
        [_name_internal_message(last_human, "reply_instruction")]
        if last_human and not getattr(last_human, "name", None)
        else []
    )

    if normalized in APPROVE_WORDS:
        return {"replyDecision": "approved", "messages": rename}
    if normalized in REJECT_WORDS:
        return {"replyDecision": "rejected", "messages": rename}
    return {"replyDecision": "revise", "replyFeedback": raw, "messages": rename}


def route_after_decision(state: State) -> Literal["draft_reply", "send_reply", "discard_reply"]:
    decision = state.get("replyDecision", "revise")
    if decision == "approved":
        return "send_reply"
    if decision == "rejected":
        return "discard_reply"
    return "draft_reply"


def send_reply(state: State, outbox):
    """Executor. Reached only after an explicit human approval."""
    result = outbox.send(
        draft=state.get("draftReply", ""),
        query=state.get("originalQuery", ""),
        revisions=state.get("replyRevisionCount", 0),
    )
    path, delivered = result["path"], result["delivered_to"]
    return {
        "replyStatus": "sent",
        "replyPath": path,
        "replyDeliveredTo": delivered,
        "messages": [AIMessage(
            content=f"Approved by a human. Delivered to {delivered}. Saved to `{path}`.",
            name="reply_receipt",
        )],
    }


def discard_reply(state: State):
    return {
        "replyStatus": "discarded",
        "messages": [AIMessage(content="Draft discarded. Nothing was sent.", name="reply_receipt")],
    }
