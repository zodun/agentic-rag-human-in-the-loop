from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode
from functools import partial

import config
from .graph_state import State, AgentState
from core.execution_logger import logged_node
from core.outbox_manager import OutboxManager
from .nodes import (
    aggregate_answers,
    collect_answer,
    compress_context,
    fallback_response,
    orchestrator,
    request_clarification,
    rewrite_query,
    should_compress_context,
    summarize_history,
)
from .reply_drafter import (
    apply_decision,
    critique_reply,
    discard_reply,
    draft_reply,
    human_approval,
    route_after_critique,
    route_after_decision,
    send_reply,
)
from .edges import route_after_orchestrator_call, route_after_rewrite

def create_agent_graph(llm, tools_list, draft_llm=None, hitl=None):
    draft_llm = draft_llm or llm
    hitl = getattr(config, "HITL_REPLY_ENABLED", False) if hitl is None else hitl
    llm_with_tools = llm.bind_tools(tools_list)
    tool_node = ToolNode(tools_list)

    checkpointer = InMemorySaver()

    print("Compiling agent graph...")
    agent_builder = StateGraph(AgentState)
    agent_builder.add_node("orchestrator", logged_node("agent.orchestrator", partial(orchestrator, llm_with_tools=llm_with_tools)))
    agent_builder.add_node("tools", tool_node)
    agent_builder.add_node("compress_context", logged_node("agent.compress_context", partial(compress_context, llm=llm)))
    agent_builder.add_node("fallback_response", logged_node("agent.fallback_response", partial(fallback_response, llm=llm)))
    agent_builder.add_node("should_compress_context", logged_node("agent.should_compress_context", should_compress_context))
    agent_builder.add_node("collect_answer", logged_node("agent.collect_answer", collect_answer))

    agent_builder.add_edge(START, "orchestrator")
    agent_builder.add_conditional_edges("orchestrator", route_after_orchestrator_call, {"tools": "tools", "fallback_response": "fallback_response", "collect_answer": "collect_answer"})
    agent_builder.add_edge("tools", "should_compress_context")
    agent_builder.add_edge("compress_context", "orchestrator")
    agent_builder.add_edge("fallback_response", "collect_answer")
    agent_builder.add_edge("collect_answer", END)

    agent_subgraph = agent_builder.compile()

    graph_builder = StateGraph(State)
    graph_builder.add_node("summarize_history", logged_node("main.summarize_history", partial(summarize_history, llm=llm)))
    graph_builder.add_node("rewrite_query", logged_node("main.rewrite_query", partial(rewrite_query, llm=llm)))
    graph_builder.add_node("request_clarification", logged_node("main.request_clarification", request_clarification))
    graph_builder.add_node("agent", agent_subgraph)
    graph_builder.add_node("aggregate_answers", logged_node("main.aggregate_answers", partial(aggregate_answers, llm=llm)))

    graph_builder.add_edge(START, "summarize_history")
    graph_builder.add_edge("summarize_history", "rewrite_query")
    graph_builder.add_conditional_edges("rewrite_query", route_after_rewrite)
    graph_builder.add_edge("request_clarification", "rewrite_query")
    graph_builder.add_edge(["agent"], "aggregate_answers")

    interrupt_nodes = ["request_clarification"]

    if hitl:
        # Second agent drafts an outbound reply; the graph then pauses on
        # human_approval until a person approves, rejects, or requests changes.
        outbox = OutboxManager()
        critic_on = getattr(config, "CRITIC_ENABLED", True)
        graph_builder.add_node("draft_reply", logged_node("main.draft_reply", partial(draft_reply, llm=draft_llm)))
        graph_builder.add_node("human_approval", logged_node("main.human_approval", human_approval))
        graph_builder.add_node("apply_decision", logged_node("main.apply_decision", apply_decision))
        graph_builder.add_node("send_reply", logged_node("main.send_reply", partial(send_reply, outbox=outbox)))
        graph_builder.add_node("discard_reply", logged_node("main.discard_reply", discard_reply))

        graph_builder.add_edge("aggregate_answers", "draft_reply")
        if critic_on:
            graph_builder.add_node("critique_reply", logged_node("main.critique_reply", partial(critique_reply, llm=draft_llm)))
            graph_builder.add_edge("draft_reply", "critique_reply")
            graph_builder.add_conditional_edges(
                "critique_reply", route_after_critique,
                {"draft_reply": "draft_reply", "human_approval": "human_approval"},
            )
        else:
            graph_builder.add_edge("draft_reply", "human_approval")
        graph_builder.add_edge("human_approval", "apply_decision")
        graph_builder.add_conditional_edges(
            "apply_decision",
            route_after_decision,
            {"draft_reply": "draft_reply", "send_reply": "send_reply", "discard_reply": "discard_reply"},
        )
        graph_builder.add_edge("send_reply", END)
        graph_builder.add_edge("discard_reply", END)
        interrupt_nodes.append("human_approval")
    else:
        graph_builder.add_edge("aggregate_answers", END)

    agent_graph = graph_builder.compile(checkpointer=checkpointer, interrupt_before=interrupt_nodes)

    print("✓ Agent graph compiled successfully.")
    return agent_graph
