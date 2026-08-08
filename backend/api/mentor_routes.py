import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from backend.mentor.graph import mentor_graph, MentorState
from backend.mentor.ai_mentor import ai_mentor

router = APIRouter(prefix="/api/v1/mentor", tags=["AI Mentor Tuition"])


class StudentInteractRequest(BaseModel):
    student_id: str = "student_default"
    student_input: str


@router.get("/student/{student_id}")
async def get_student_knowledge_state(student_id: str = "student_default"):
    """Fetch living Student Knowledge Model (profile, skill ratings %, weaknesses, homework, streak)."""
    model = ai_mentor.get_student_model(student_id)
    return model.model_dump(mode="json")


@router.get("/class/today/{student_id}")
async def get_start_of_class_experience(student_id: str = "student_default"):
    """
    Start-of-Class Tuition Experience:
    Generates personalized greeting reminding student of previous class and today's 45-min lesson plan.
    """
    initial_state: MentorState = {
        "student_id": student_id,
        "student_input": "",
    }
    final_state = await asyncio.to_thread(mentor_graph.invoke, initial_state)
    return {
        "greeting": final_state.get("mentor_response"),
        "class_plan": final_state.get("class_plan"),
        "student_model": final_state.get("student_model"),
    }


@router.post("/class/interact")
async def interact_with_ai_mentor(req: StudentInteractRequest):
    """
    Conduct active tuition class interaction with AI Mentor.
    """
    state: MentorState = {
        "student_id": req.student_id,
        "student_input": req.student_input,
    }
    final_state = await asyncio.to_thread(mentor_graph.invoke, state)
    return {
        "mentor_response": final_state.get("mentor_response"),
        "action_type": final_state.get("action_type"),
        "student_id": req.student_id,
    }
