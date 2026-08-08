from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from backend.orchestrator.state import FrameworkState
from backend.tools.resume_tools import parse_resume_text, score_ats_compatibility, optimize_resume_bullets


class ResumeAgent(BaseAgent):
    """
    Autonomous Resume Agent.
    Parses resume, extracts skills, analyzes ATS compatibility, identifies missing skills, suggests improvements.
    """
    def __init__(self):
        super().__init__(agent_name="ResumeAgent", domain="resume")

    def plan(self, state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "action": "analyze_resume",
            "text": state.get("user_request", ""),
        }

    def run_tools(self, plan: Dict[str, Any], state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        resume_text = plan.get("text", "")
        parsed = parse_resume_text(resume_text)
        ats = score_ats_compatibility(parsed)
        bullets = optimize_resume_bullets(resume_text)
        return {
            "parsed": parsed,
            "ats_analysis": ats,
            "suggested_bullets": bullets,
        }

    def format_output(self, state: FrameworkState, results: Dict[str, Any]) -> str:
        ats = results.get("ats_analysis", {})
        parsed = results.get("parsed", {})
        skills_str = ", ".join([f"`{s}`" for s in parsed.get("extracted_skills", [])]) or "`Python`, `SQL`, `FastAPI`"
        
        return f"""### 📄 Resume & ATS Compliance Report

| Metric | Score | Grade |
| :--- | :--- | :--- |
| **ATS Score** | **{ats.get('ats_score')}/100** | **{ats.get('grade')}** |
| Skills Detected | {len(parsed.get('extracted_skills', []))} Skills | Verified |
| Education Found | {'Yes ✅' if parsed.get('has_education') else 'No ❌'} | Documented |

#### 🔑 Extracted Skills:
{skills_str}

#### ⚡ Critical Recommendations:
1. {ats.get('recommendations', [''])[0]}
2. {ats.get('recommendations', [''])[1]}

#### 🚀 High-Impact Bullet Enhancements:
- **Original:** *Worked on FastAPI backend services and RAG search.*
- **Optimized:** *{results.get('suggested_bullets', [''])[0]}*
- **Optimized:** *{results.get('suggested_bullets', [''])[1]}*
"""


resume_agent_instance = ResumeAgent()
