from typing import TypedDict, Any


class InterviewState(TypedDict, total=False):
    user_request: str
    candidate_id: str

    messages: list[Any]

    current_action: str
    action_reason: str

    tool_result: str
    response: str

    iteration: int