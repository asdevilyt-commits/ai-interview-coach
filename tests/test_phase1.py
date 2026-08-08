import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from fastapi.testclient import TestClient


from backend.config import settings
from backend.core.logger import get_logger
from backend.core.exceptions import CareerAIException, AgentExecutionError
from backend.core.llm import ask_llm
from backend.models import (
    CandidateProfile,
    SkillLevel,
    Question,
    QuestionDifficulty,
    InterviewType,
    AnswerEvaluation,
    LearningPlan,
    CodingProblem,
)
from backend.orchestrator.state import FrameworkState
from backend.api.app import app


def test_settings_loading():
    assert settings.APP_NAME == "Enterprise AI Career Preparation Platform"
    assert settings.PRIMARY_LLM_MODEL == "llama-3.1-8b-instant"
    assert "postgresql" in settings.DATABASE_URL
    assert "redis" in settings.REDIS_URL


def test_logger():
    logger = get_logger("test_logger")
    assert logger.name == "test_logger"


def test_exceptions():
    exc = AgentExecutionError("Agent failed to process request", details={"agent": "ResumeAgent"})
    assert isinstance(exc, CareerAIException)
    assert exc.message == "Agent failed to process request"
    assert exc.details["agent"] == "ResumeAgent"


def test_domain_models():
    candidate = CandidateProfile(
        candidate_id="cand_123",
        name="Alex Smith",
        target_role="Senior AI Engineer",
        skills=[SkillLevel(name="Python", proficiency=0.9, verified=True)],
    )
    assert candidate.candidate_id == "cand_123"
    assert candidate.skills[0].name == "Python"

    question = Question(
        id="q_001",
        topic="Python",
        question_text="Explain Python decorators.",
        difficulty=QuestionDifficulty.MEDIUM,
        interview_type=InterviewType.TECHNICAL,
    )
    assert question.id == "q_001"
    assert question.difficulty == QuestionDifficulty.MEDIUM

    evaluation = AnswerEvaluation(
        score=8.5,
        technical_accuracy=9.0,
        conceptual_understanding=8.0,
        clarity=8.0,
        depth=8.0,
        strengths=["Good explanation of wrapper functions"],
        weaknesses=["Omitted functools.wraps usage"],
        missing_points=["Preserving docstrings and function metadata"],
        ideal_answer="A decorator is a function that takes another function...",
    )
    assert evaluation.score == 8.5


def test_framework_state():
    state: FrameworkState = {
        "user_request": "Prepare me for a Python interview.",
        "candidate_id": "cand_123",
        "intent": "INTERVIEW_PREPARATION",
        "current_agent": "MasterOrchestrator",
        "current_action": "route_intent",
        "candidate_profile": {"name": "Alex Smith"},
        "retrieved_context": [],
        "task_plan": [],
        "tool_results": [],
        "interview_state": {},
        "learning_state": {},
        "coding_state": {},
        "agent_outputs": [],
        "final_response": "",
    }
    assert state["user_request"] == "Prepare me for a Python interview."
    assert state["intent"] == "INTERVIEW_PREPARATION"


def test_llm_invocation():
    response = ask_llm("Return the single word: CONFIRMED")
    assert "CONFIRMED" in response.upper()


def test_fastapi_health_endpoint():
    client = TestClient(app)
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "Enterprise AI" in data["app"]
