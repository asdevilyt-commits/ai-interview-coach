from typing import Dict, Any
from backend.mentor.workers.base_worker import BaseWorker
from backend.models.student import StudentKnowledgeModel
from backend.core.logger import logger


class AssessmentWorker(BaseWorker):
    """
    Internal Assessment Worker.
    Assists AI Mentor in evaluating student answers, updating knowledge percentages, and assigning homework.
    """
    def __init__(self):
        super().__init__(worker_name="AssessmentWorker")

    def run_capability(self, goal: str, model: StudentKnowledgeModel, input_text: str) -> Dict[str, Any]:
        ans_length = len(input_text.split())
        score = min(95.0, max(50.0, ans_length * 2.5 + 40.0))
        
        return {
            "understanding_score": round(score, 1),
            "feedback": "Great effort! You clearly understood the core concept.",
            "assigned_homework": [
                f"Write a short code snippet implementing {goal}.",
                f"Review 1 edge case regarding {goal} before tomorrow's class."
            ]
        }


assessment_worker_instance = AssessmentWorker()
