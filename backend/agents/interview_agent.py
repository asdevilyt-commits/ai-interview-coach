from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.orchestrator.state import FrameworkState
from backend.tools.interview_tools import get_next_question, evaluate_candidate_answer


class InterviewAgent(BaseAgent):
    """
    Autonomous Adaptive Interview Agent.
    Conducts technical, resume-based, and behavioral interview loops with multi-dimensional evaluation.
    """
    def __init__(self):
        super().__init__(agent_name="InterviewAgent", domain="interview")

    def plan(self, state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        req = state.get("user_request", "").lower()
        if "answer" in req or "because" in req or len(req.split()) > 4:
            return {"action": "evaluate_answer", "answer": state.get("user_request")}
        return {"action": "ask_question"}

    def run_tools(self, plan: Dict[str, Any], state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        if plan["action"] == "evaluate_answer":
            current_q = state.get("interview_state", {}).get("current_question", "What is the difference between shallow copy and deep copy in Python?")
            evaluation = evaluate_candidate_answer(question_text=current_q, candidate_answer=plan["answer"])
            return {"type": "evaluation", "evaluation": evaluation}
        else:
            q = get_next_question(topic="Python", difficulty="medium", index=0)
            if "interview_state" not in state or state["interview_state"] is None:
                state["interview_state"] = {}
            state["interview_state"]["current_question"] = q.get("question_text")
            return {"type": "question", "question": q}

    def format_output(self, state: FrameworkState, results: Dict[str, Any]) -> str:
        if results.get("type") == "evaluation":
            ev = results["evaluation"]
            return f"""### 🎯 Answer Evaluation Scorecard

| Dimension | Score | Rating |
| :--- | :--- | :--- |
| **Overall Score** | **{ev.get('score')}/10** | **{'Excellent' if ev.get('score', 0)>=8 else 'Good'}** |
| Technical Accuracy | {ev.get('technical_accuracy')}/10 | Accurate |
| Conceptual Understanding | {ev.get('conceptual_understanding')}/10 | Strong |
| Communication Clarity | {ev.get('clarity')}/10 | Clear |
| Technical Depth | {ev.get('depth')}/10 | Detailed |

#### 🌟 Key Strengths:
- {', '.join(ev.get('strengths', ['Clear explanation of core concepts']))}

#### 💡 Areas for Improvement:
- {', '.join(ev.get('weaknesses', ['Could detail edge-case trade-offs']))}

#### 📖 Ideal Answer Summary:
{ev.get('ideal_answer')}

#### ❓ Suggested Follow-up Question:
*{ev.get('follow_up_question')}*
"""
        else:
            q = results["question"]
            return f"""### 🎯 Adaptive Interview Question ({q.get('topic')})

**Difficulty:** `{q.get('difficulty').upper()}`
**Target Domain:** `{q.get('topic')}`

#### Question:
{q.get('question_text')}

---
*Type your detailed answer below and click 'Submit Answer for Evaluation'.*
"""


interview_agent_instance = InterviewAgent()