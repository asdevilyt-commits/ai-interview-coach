from typing import TypedDict, Any, Dict, List, Optional
from langgraph.graph import StateGraph, START, END
from backend.mentor.ai_mentor import ai_mentor


class MentorState(TypedDict, total=False):
    student_id: str
    student_input: str
    action_type: str
    mentor_response: str
    class_plan: Dict[str, Any]
    student_model: Dict[str, Any]


def mentor_brain_node(state: MentorState) -> MentorState:
    """LangGraph node executing the AI Mentor decision loop."""
    student_id = state.get("student_id", "student_default")
    student_input = state.get("student_input", "")

    if not student_input:
        # Start-of-Class initial loading
        res = ai_mentor.generate_start_of_class_greeting(student_id)
        state["mentor_response"] = res["greeting"]
        state["class_plan"] = res["class_plan"]
        state["student_model"] = res["student_model"]
        state["action_type"] = "START_CLASS"
    else:
        # Conduct tuition class interaction
        res = ai_mentor.conduct_tuition_class(student_id, student_input)
        state["mentor_response"] = res["mentor_response"]
        state["action_type"] = res["action_type"]

    return state


def build_mentor_graph():
    """Build and compile LangGraph state graph for AI Personal Tuition Mentor."""
    builder = StateGraph(MentorState)
    builder.add_node("mentor_brain", mentor_brain_node)
    builder.add_edge(START, "mentor_brain")
    builder.add_edge("mentor_brain", END)
    return builder.compile()


mentor_graph = build_mentor_graph()
