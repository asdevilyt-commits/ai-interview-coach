import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from fastapi.testclient import TestClient

from backend.api.app import app
from backend.models.student import StudentKnowledgeModel, StudentProfile, CareerGoal
from backend.mentor.ai_mentor import ai_mentor
from backend.mentor.graph import mentor_graph

client = TestClient(app)


def test_student_knowledge_model_defaults():
    model = StudentKnowledgeModel(student_id="test_student")
    assert model.student_id == "test_student"
    assert model.profile.name == "Alex Smith"
    assert model.career_goal.target_role == "AI Engineer"
    assert len(model.skills) >= 5
    assert len(model.weak_areas) >= 1
    assert model.current_streak_days == 12


def test_ai_mentor_start_of_class_greeting():
    res = ai_mentor.generate_start_of_class_greeting("test_student")
    assert "greeting" in res
    assert "Good evening" in res["greeting"]
    assert "class_plan" in res
    assert res["class_plan"]["duration_minutes"] == 45


def test_ai_mentor_conduct_tuition_class():
    res = ai_mentor.conduct_tuition_class("test_student", "Yes, I am ready to start!")
    assert "mentor_response" in res
    assert "TUITION" in res["action_type"]


def test_api_mentor_endpoints():
    # 1. Get living student state
    r1 = client.get("/api/v1/mentor/student/test_student")
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["student_id"] == "test_student"

    # 2. Get start-of-class experience
    r2 = client.get("/api/v1/mentor/class/today/test_student")
    assert r2.status_code == 200
    d2 = r2.json()
    assert "greeting" in d2
    assert "class_plan" in d2

    # 3. Post tuition interaction
    r3 = client.post("/api/v1/mentor/class/interact", json={
        "student_id": "test_student",
        "student_input": "Shallow copy copies references, while deep copy recursively copies child objects."
    })
    assert r3.status_code == 200
    d3 = r3.json()
    assert "mentor_response" in d3
    assert "TUITION" in d3["action_type"]
