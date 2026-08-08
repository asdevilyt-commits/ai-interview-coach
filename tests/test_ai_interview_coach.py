import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
import pytest
from fastapi.testclient import TestClient
from backend.api.app import app
from backend.database.connection import init_db


init_db()
client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_and_profile():
    # 1. Register
    reg_resp = client.post("/register", json={"username": "test_user_capstone"})
    assert reg_resp.status_code == 200
    user_id = reg_resp.json()["user_id"]
    assert user_id > 0

    # 2. Profile
    prof_resp = client.post("/profile", json={
        "user_id": user_id,
        "name": "Test Candidate",
        "education": "B.S. Software Engineering",
        "experience_level": "Entry Level",
        "target_role": "AI Engineer",
        "target_company": "Tech Corp"
    })
    assert prof_resp.status_code == 200
    assert prof_resp.json()["name"] == "Test Candidate"


def test_document_upload_and_rag():
    # Create temp text file
    sample_path = "sample_resume.txt"
    with open(sample_path, "w") as f:
        f.write("Experienced Python developer proficient in SQL joins, FastAPI, and machine learning models.")

    with open(sample_path, "rb") as f:
        resp = client.post(
            "/documents/upload",
            data={"user_id": 1, "doc_type": "resume"},
            files={"file": ("sample_resume.txt", f, "text/plain")}
        )

    if os.path.exists(sample_path):
        os.remove(sample_path)

    assert resp.status_code == 200
    assert "Document uploaded" in resp.json()["message"]


def test_assessment_flow():
    # Start assessment
    start_resp = client.post("/assessment/start", json={"user_id": 1})
    assert start_resp.status_code == 200
    data = start_resp.json()
    assert "question_text" in data
    assessment_id = data["assessment_id"]
    question_id = data["question_id"]

    # Answer question 1
    ans_resp = client.post("/assessment/answer", json={
        "assessment_id": assessment_id,
        "question_id": question_id,
        "user_answer": "Lists are mutable, tuples are immutable"
    })
    assert ans_resp.status_code == 200
    assert "is_correct" in ans_resp.json()


def test_dashboard_endpoint():
    resp = client.get("/dashboard?user_id=1")
    assert resp.status_code == 200
    data = resp.json()
    assert "user_name" in data
    assert "preparation_percentage" in data


def test_socratic_learning_flow():
    # Start learning
    start_resp = client.post("/learning/start", json={"user_id": 1, "topic": "SQL Joins"})
    assert start_resp.status_code == 200
    data = start_resp.json()
    session_id = data["learning_session_id"]
    question_id = data["question_id"]

    # Answer learning practice question
    ans_resp = client.post("/learning/answer", json={
        "learning_session_id": session_id,
        "question_id": question_id,
        "user_answer": "Non-matching rows will return NULL for columns from the right table."
    })
    assert ans_resp.status_code == 200
    assert ans_resp.json()["is_correct"] is True


def test_mock_interview_and_feedback():
    # Start interview
    start_resp = client.post("/interview/start", json={"user_id": 1, "mode": "Technical"})
    assert start_resp.status_code == 200
    data = start_resp.json()
    session_id = data["interview_session_id"]
    question_id = data["question_id"]

    # Answer interview question
    ans_resp = client.post("/interview/answer", json={
        "interview_session_id": session_id,
        "question_id": question_id,
        "user_answer": "I optimized database queries by adding composite B-tree indexes and using inner joins."
    })
    assert ans_resp.status_code == 200

    # Voice endpoint test
    voice_resp = client.post("/interview/voice", json={
        "interview_session_id": session_id,
        "question_id": question_id,
        "transcript": "I designed microservice architectures using FastAPI and Docker containers."
    })
    assert voice_resp.status_code == 200


def test_progress_endpoint():
    resp = client.get("/progress?user_id=1")
    assert resp.status_code == 200
    data = resp.json()
    assert "overall_percentage" in data
    assert "strong_topics" in data
    assert "weak_topics" in data
