from langgraph.graph import StateGraph, START, END
from backend.orchestrator.state import FrameworkState
from backend.orchestrator.master_orchestrator import master_orchestrator


def orchestrator_node(state: FrameworkState) -> FrameworkState:
    """Master Orchestrator execution node in LangGraph state machine."""
    return master_orchestrator.execute_workflow(state)


def build_career_ai_graph():
    """
    Build and compile the LangGraph StateGraph engine for Enterprise Career AI Platform.
    """
    builder = StateGraph(FrameworkState)
    
    builder.add_node("master_orchestrator", orchestrator_node)
    builder.add_edge(START, "master_orchestrator")
    builder.add_edge("master_orchestrator", END)

    return builder.compile()


career_ai_graph = build_career_ai_graph()
