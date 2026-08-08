from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from backend.agents.state import InterviewState
from backend.agents.interview_agent import (
    interview_agent,
    tools,
)


tool_node = ToolNode(tools)


def should_continue(state: InterviewState):

    messages = state.get("messages", [])

    if not messages:
        return "end"

    last_message = messages[-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return "end"


def build_interview_graph():

    graph = StateGraph(InterviewState)

    graph.add_node(
        "interview_agent",
        interview_agent,
    )

    graph.add_node(
        "tools",
        tool_node,
    )

    graph.add_edge(
        START,
        "interview_agent",
    )

    graph.add_conditional_edges(
        "interview_agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )

    graph.add_edge(
        "tools",
        "interview_agent",
    )

    return graph.compile()