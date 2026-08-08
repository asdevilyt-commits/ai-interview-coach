from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.orchestrator.state import FrameworkState
from backend.tools.learning_tools import generate_personalized_learning_plan


class LearningAgent(BaseAgent):
    """
    Autonomous Learning Agent.
    Creates personalized learning plans based on candidate level, target job, and weak topics.
    """
    def __init__(self):
        super().__init__(agent_name="LearningAgent", domain="learning")

    def plan(self, state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        profile = context.get("profile", {})
        weaknesses = profile.get("weaknesses", ["Python OOP Architecture", "Decorators & Generators", "Dynamic Programming"])
        return {
            "action": "generate_plan",
            "topic": "Python & System Architecture",
            "weaknesses": weaknesses,
        }

    def run_tools(self, plan: Dict[str, Any], state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        plan_dict = generate_personalized_learning_plan(
            topic=plan["topic"],
            candidate_level="Intermediate to Senior",
            weak_topics=plan["weaknesses"],
        )
        return {"learning_plan": plan_dict}

    def format_output(self, state: FrameworkState, results: Dict[str, Any]) -> str:
        lp = results.get("learning_plan", {})
        weeks = lp.get("weekly_plans", [])
        
        output = f"### 📚 Personalized 4-Week Adaptive Learning Roadmap\n\n"
        output += f"**Target Skill Area:** `{lp.get('target_topic')}` | **Target Level:** `{lp.get('estimated_level')}`\n\n"
        
        for w in weeks:
            output += f"#### Week {w.get('week_number')}: {w.get('focus_area')}\n"
            output += f"*Goals:* {', '.join(w.get('learning_goals', []))}\n\n"
            for m in w.get("modules", []):
                p_badge = "🔴 HIGH" if m.get('priority') == "high" else "🟡 MEDIUM"
                output += f"- `{m.get('title')}` — {m.get('description')} *(Priority: {p_badge})*\n"
            output += "\n"
        return output


learning_agent_instance = LearningAgent()
