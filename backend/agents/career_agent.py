from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.orchestrator.state import FrameworkState


class CareerAgent(BaseAgent):
    """
    Autonomous Career & Target Role Agent.
    Provides company tech-stack breakdowns, salary benchmark insights, and career path recommendations.
    """
    def __init__(self):
        super().__init__(agent_name="CareerAgent", domain="career")

    def plan(self, state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "action": "analyze_career_path",
            "request": state.get("user_request", ""),
        }

    def run_tools(self, plan: Dict[str, Any], state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "AI Engineer")
        target_companies = profile.get("target_companies", ["Google", "OpenAI", "Meta"])

        return {
            "target_role": target_role,
            "target_companies": target_companies,
            "salary_range": "$160,000 - $240,000 USD (Senior Level)",
            "key_hiring_focus": [
                "Production RAG & Vector Database Systems",
                "Low-Latency API Design (FastAPI / gRPC)",
                "Distributed Systems & Database Query Optimization",
                "Clean Architecture & Design Patterns",
            ],
            "recommended_actions": [
                "Build 1 production-grade RAG project with FAISS & LangGraph",
                "Practice 25+ LeetCode Medium problems in Arrays, Trees & DP",
                "Conduct 3 timed mock interviews under FAANG Tech Lead persona",
            ]
        }

    def format_output(self, state: FrameworkState, results: Dict[str, Any]) -> str:
        comps = ", ".join(results.get("target_companies", []))
        focus = "\n".join([f"- {f}" for f in results.get("key_hiring_focus", [])])
        actions = "\n".join([f"1. {a}" for a in results.get("recommended_actions", [])])

        return f"""### Career & Target Role Intelligence

**Target Role:** {results.get('target_role')}
**Target Companies:** {comps}
**Estimated Compensation Benchmark:** {results.get('salary_range')}

#### Key Technical Focus Areas for Target Companies:
{focus}

#### Recommended Action Plan:
{actions}
"""


career_agent_instance = CareerAgent()
