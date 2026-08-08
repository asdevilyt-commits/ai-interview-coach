from typing import TypedDict, Any, List, Dict, Optional
from typing_extensions import NotRequired


class FrameworkState(TypedDict, total=False):
    """
    Central TypedDict state shared across the LangGraph StateGraph engine
    and all autonomous sub-agents.
    """
    user_request: str
    candidate_id: str
    intent: str
    current_agent: str
    current_action: str

    candidate_profile: Dict[str, Any]
    retrieved_context: List[Dict[str, Any]]

    task_plan: List[Dict[str, Any]]
    tool_results: List[Dict[str, Any]]

    interview_state: Dict[str, Any]
    learning_state: Dict[str, Any]
    coding_state: Dict[str, Any]

    agent_outputs: List[Dict[str, Any]]
    final_response: str

    messages: List[Any]
    iteration: int
    error: Optional[str]
