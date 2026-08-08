from typing import Dict, Any, Callable, List, Optional
from backend.core.logger import logger


class DynamicRegistry:
    """
    Enterprise Dynamic Tool & Skill Registration System.
    Decouples agent registration from Master Orchestrator.
    """
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._skills: Dict[str, Dict[str, Any]] = {}
        self._agents: Dict[str, Any] = {}

    def register_tool(self, name: str, func: Callable, description: str = ""):
        self._tools[name] = func
        logger.info(f"Registered Tool: '{name}'")

    def register_skill(self, name: str, category: str, handler: Callable, description: str = ""):
        self._skills[name] = {
            "name": name,
            "category": category,
            "handler": handler,
            "description": description,
        }
        logger.info(f"Registered Skill: '{name}' ({category})")

    def register_agent(self, agent_name: str, agent_instance: Any):
        self._agents[agent_name] = agent_instance
        logger.info(f"Registered Autonomous Sub-Agent: '{agent_name}'")

    def get_tool(self, name: str) -> Optional[Callable]:
        return self._tools.get(name)

    def get_skill(self, name: str) -> Optional[Dict[str, Any]]:
        return self._skills.get(name)

    def get_agent(self, agent_name: str) -> Optional[Any]:
        return self._agents.get(agent_name)

    def list_all(self) -> Dict[str, List[str]]:
        return {
            "tools": list(self._tools.keys()),
            "skills": list(self._skills.keys()),
            "agents": list(self._agents.keys()),
        }


registry = DynamicRegistry()
