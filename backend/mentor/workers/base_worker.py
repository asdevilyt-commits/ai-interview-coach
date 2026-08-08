from abc import ABC, abstractmethod
from typing import Dict, Any
from backend.models.student import StudentKnowledgeModel
from backend.core.logger import logger


class BaseWorker(ABC):
    """
    Base class for internal specialist workers.
    Workers are capability providers managed exclusively by the central AI Mentor.
    """
    def __init__(self, worker_name: str):
        self.worker_name = worker_name

    @abstractmethod
    def run_capability(self, goal: str, model: StudentKnowledgeModel, input_text: str) -> Dict[str, Any]:
        pass
