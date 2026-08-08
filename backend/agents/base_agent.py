from abc import ABC, abstractmethod
from typing import Dict, Any, List
from backend.orchestrator.state import FrameworkState
from backend.memory.hybrid_memory import hybrid_memory
from backend.core.logger import logger


class BaseAgent(ABC):
    """
    Autonomous Sub-Agent Base Class implementing the 9-Step Agent Lifecycle:
    1. Goal Acquisition
    2. Memory Read
    3. Local Planning
    4. Reasoning / ReAct Loop
    5. Skill Selection
    6. Tool Execution
    7. Result Validation
    8. Memory Write
    9. Output Formatting
    """
    def __init__(self, agent_name: str, domain: str):
        self.agent_name = agent_name
        self.domain = domain

    def execute(self, state: FrameworkState) -> FrameworkState:
        logger.info(f"[{self.agent_name}] Step 1: Goal Acquisition -> '{state.get('user_request')}'")
        candidate_id = state.get("candidate_id", "cand_default")

        logger.info(f"[{self.agent_name}] Step 2: Memory Read")
        candidate_context = hybrid_memory.get_candidate_full_context(candidate_id, query=state.get("user_request"))

        logger.info(f"[{self.agent_name}] Step 3: Local Planning")
        plan = self.plan(state, candidate_context)

        logger.info(f"[{self.agent_name}] Step 4-6: Reasoning, Skill Selection & Tool Execution")
        action_results = self.run_tools(plan, state, candidate_context)

        logger.info(f"[{self.agent_name}] Step 7: Result Validation")
        validated_results = self.validate_results(action_results)

        logger.info(f"[{self.agent_name}] Step 8: Memory Write")
        self.write_memory(candidate_id, state, validated_results)

        logger.info(f"[{self.agent_name}] Step 9: Output Formatting")
        final_response = self.format_output(state, validated_results)

        state["current_agent"] = self.agent_name
        state["final_response"] = final_response
        if "agent_outputs" not in state or state["agent_outputs"] is None:
            state["agent_outputs"] = []
        state["agent_outputs"].append({
            "agent": self.agent_name,
            "result": validated_results,
        })
        return state

    @abstractmethod
    def plan(self, state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def run_tools(self, plan: Dict[str, Any], state: FrameworkState, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def validate_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        return results

    def write_memory(self, candidate_id: str, state: FrameworkState, results: Dict[str, Any]):
        hybrid_memory.semantic.add_document(
            candidate_id=candidate_id,
            content=f"Agent '{self.agent_name}' executed action for user request: {state.get('user_request')}",
            metadata={"agent": self.agent_name}
        )

    @abstractmethod
    def format_output(self, state: FrameworkState, results: Dict[str, Any]) -> str:
        pass
