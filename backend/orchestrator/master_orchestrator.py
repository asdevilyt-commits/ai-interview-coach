from typing import Dict, Any, List
from backend.orchestrator.state import FrameworkState
from backend.skills.initializer import registry
from backend.memory.hybrid_memory import hybrid_memory
from backend.core.logger import logger


class MasterOrchestrator:
    """
    Master Orchestrator Agent (Zero Business Logic).
    Only routes intent, decomposes tasks, dispatches to specialized autonomous sub-agents,
    and updates persistent memory.
    """
    def route_intent(self, user_request: str) -> str:
        req_low = user_request.lower()
        if any(w in req_low for w in ["resume", "cv", "ats", "bullet", "experience"]):
            return "RESUME_ANALYSIS"
        elif any(w in req_low for w in ["learn", "plan", "roadmap", "syllabus", "week"]):
            return "LEARNING_PLAN"
        elif any(w in req_low for w in ["code", "coding", "algo", "leetcode", "dsa", "def ", "function"]):
            return "CODING_PRACTICE"
        elif any(w in req_low for w in ["career", "salary", "pay", "offer", "benchmark", "company", "role"]):
            return "CAREER_ADVICE"
        elif any(w in req_low for w in ["interview", "question", "ask me", "mock", "practice", "answer"]):
            return "MOCK_INTERVIEW"
        return "GENERAL_PREPARATION"

    def select_agent_for_intent(self, intent: str) -> str:
        mapping = {
            "RESUME_ANALYSIS": "ResumeAgent",
            "LEARNING_PLAN": "LearningAgent",
            "MOCK_INTERVIEW": "InterviewAgent",
            "CODING_PRACTICE": "CodingAgent",
            "CAREER_ADVICE": "CareerAgent",
            "GENERAL_PREPARATION": "InterviewAgent",
        }
        return mapping.get(intent, "InterviewAgent")

    def execute_workflow(self, state: FrameworkState) -> FrameworkState:
        user_request = state.get("user_request", "")
        candidate_id = state.get("candidate_id", "cand_default")
        logger.info(f"[MasterOrchestrator] Received request: '{user_request}' for candidate '{candidate_id}'")

        # 1. Intent Detection
        intent = self.route_intent(user_request)
        state["intent"] = intent
        logger.info(f"[MasterOrchestrator] Detected Intent: {intent}")

        # 2. Select Sub-Agent from Dynamic Registry
        target_agent_name = self.select_agent_for_intent(intent)
        state["current_agent"] = target_agent_name
        
        agent_instance = registry.get_agent(target_agent_name)
        if not agent_instance:
            logger.error(f"[MasterOrchestrator] Agent '{target_agent_name}' not registered in DynamicRegistry!")
            state["final_response"] = f"Error: Agent '{target_agent_name}' is not registered."
            return state

        # 3. Dispatch Task to Autonomous Sub-Agent
        logger.info(f"[MasterOrchestrator] Dispatching workflow to '{target_agent_name}'...")
        updated_state = agent_instance.execute(state)

        # 4. Sync Memory Layer
        profile = hybrid_memory.structured.get_candidate(candidate_id)
        if profile:
            hybrid_memory.sync_candidate_state(profile)

        return updated_state


master_orchestrator = MasterOrchestrator()
