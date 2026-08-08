from typing import Dict, Any
from backend.mentor.workers.base_worker import BaseWorker
from backend.models.student import StudentKnowledgeModel
from backend.core.llm import ask_llm
from backend.core.logger import logger


class TeacherWorker(BaseWorker):
    """
    Internal Teacher Worker.
    Assists AI Mentor in teaching concepts using the Socratic Method (questions, analogies, guided thinking).
    """
    def __init__(self):
        super().__init__(worker_name="TeacherWorker")

    def run_capability(self, goal: str, model: StudentKnowledgeModel, input_text: str) -> Dict[str, Any]:
        weak_topics = ", ".join(model.weak_areas)
        target_role = model.career_goal.target_role
        
        prompt = f"""
You are the internal teaching module of the AI Personal Mentor.
Student Name: {model.profile.name}
Target Role: {target_role}
Student Weak Topics: {weak_topics}

Current Goal: {goal}
Student Message: "{input_text}"

Teach the concept using the Socratic Method.
Do NOT dump a massive wall of text.
1. Briefly state the key intuition with a simple analogy.
2. Ask 1 targeted Socratic thinking question to verify understanding before revealing full code.
"""
        try:
            explanation = ask_llm(prompt=prompt, temperature=0.3)
            return {"status": "success", "teaching_content": explanation}
        except Exception as e:
            logger.error(f"TeacherWorker error: {e}")
            return {
                "status": "fallback",
                "teaching_content": (
                    f"Let's break down {goal} step-by-step! "
                    f"Before we dive into the code, how would you describe the difference between a class blueprint and an actual object instance in your own words?"
                )
            }


teacher_worker_instance = TeacherWorker()
