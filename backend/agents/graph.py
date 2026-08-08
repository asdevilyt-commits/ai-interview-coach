from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from backend.agents.ai_coach import ai_coach


class AICoachState(TypedDict):
    user_id: int
    user_request: str
    target_role: str
    mode: str
    doc_context: str
    response: str
    session_data: Dict[str, Any]


async def understand_user_request(state: AICoachState) -> AICoachState:
    # State node 1: Parse intent and target context
    req = state.get("user_request", "")
    mode = state.get("mode", "GENERAL")
    state["response"] = f"Understood request: '{req}' in mode '{mode}'."
    return state


async def execute_coach_task(state: AICoachState) -> AICoachState:
    # State node 2: Execute task through AI Coach Agent
    mode = state.get("mode", "GENERAL")
    user_id = state.get("user_id", 1)
    req = state.get("user_request", "")

    if mode == "LEARNING":
        content = await ai_coach.generate_learning_content(req or "Python Core", user_id=user_id)
        state["response"] = content.get("explanation", "")
        state["session_data"] = content
    else:
        q = await ai_coach.generate_interview_question(mode=mode, current_index=0, user_id=user_id, target_role=state.get("target_role", "Software Engineer"))
        state["response"] = q
        state["session_data"] = {"question": q}

    return state


# Build LangGraph workflow
builder = StateGraph(AICoachState)
builder.add_node("understand", understand_user_request)
builder.add_node("coach_task", execute_coach_task)

builder.set_entry_point("understand")
builder.add_edge("understand", "coach_task")
builder.add_edge("coach_task", END)

ai_coach_graph = builder.compile()
