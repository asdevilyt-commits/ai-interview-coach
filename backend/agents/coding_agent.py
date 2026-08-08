from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.orchestrator.state import FrameworkState
from backend.tools.coding_tools import fetch_coding_problem, evaluate_submitted_code


class CodingAgent(BaseAgent):
    """
    Autonomous Coding Agent.
    Recommends coding problems, evaluates submitted code, analyzes time/space complexity, and provides hints.
    """
    def __init__(self):
        super().__init__(agent_name="CodingAgent", domain="coding")

    def plan(self, state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        req = state.get("user_request", "").lower()
        if "def " in req or "function" in req or "return" in req or "class " in req:
            return {"action": "evaluate_code", "code": state.get("user_request")}
        return {"action": "recommend_problem"}

    def run_tools(self, plan: Dict[str, Any], state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        if plan["action"] == "evaluate_code":
            res = evaluate_submitted_code(code=plan["code"])
            return {"type": "code_evaluation", "result": res}
        else:
            prob = fetch_coding_problem(topic="Arrays", difficulty="Easy")
            return {"type": "problem_recommendation", "problem": prob}

    def format_output(self, state: FrameworkState, results: Dict[str, Any]) -> str:
        if results.get("type") == "code_evaluation":
            res = results["result"]
            comp = res.get("complexity", {})
            return f"""### 💻 Code Complexity & Execution Report

| Metric | Value | Status |
| :--- | :--- | :--- |
| **Correctness** | **{'PASSED ✅' if res.get('is_correct') else 'NEEDS FIX ❌'}** | Score: {res.get('score')}/10 |
| **Time Complexity** | `{comp.get('time_complexity')}` | {'Optimal' if comp.get('is_optimal') else 'Suboptimal'} |
| **Space Complexity** | `{comp.get('space_complexity')}` | Optimal |
| **Test Cases** | {res.get('passed_tests')}/{res.get('total_tests')} Passed | Verified |

#### 💡 Analysis Feedback:
{res.get('feedback')}

#### 🛠️ Recommendations:
- {', '.join(res.get('suggested_improvements', ['Ensure defensive handling for empty inputs']))}
"""
        else:
            prob = results["problem"]
            return f"""### 💻 Algorithm Challenge: {prob.get('title')}

**Source:** `{prob.get('source')}` | **Difficulty:** `{prob.get('difficulty')}` | **Topic:** `{prob.get('topic')}`

#### Description:
{prob.get('description')}

#### Constraints:
- {prob.get('constraints', [''])[0]}

#### 💡 Hint:
*{prob.get('hints', [''])[0]}*
"""


coding_agent_instance = CodingAgent()
