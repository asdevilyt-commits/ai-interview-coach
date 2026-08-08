import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from fastapi.testclient import TestClient


from backend.skills.initializer import registry
from backend.orchestrator.master_orchestrator import master_orchestrator
from backend.orchestrator.graph import career_ai_graph
from backend.orchestrator.state import FrameworkState
from backend.memory.hybrid_memory import hybrid_memory
from backend.rag.pipeline import rag_pipeline
from backend.models.candidate import CandidateProfile
from backend.api.app import app

client = TestClient(app)


def test_dynamic_registry_population():
    all_registered = registry.list_all()
    assert "ResumeAgent" in all_registered["agents"]
    assert "LearningAgent" in all_registered["agents"]
    assert "InterviewAgent" in all_registered["agents"]
    assert "CodingAgent" in all_registered["agents"]
    assert "CareerAgent" in all_registered["agents"]
    assert "parse_resume_text" in all_registered["tools"]
    assert "evaluate_candidate_answer" in all_registered["tools"]


def test_master_orchestrator_routing():
    assert master_orchestrator.route_intent("Analyze my resume for ATS score") == "RESUME_ANALYSIS"
    assert master_orchestrator.route_intent("Create a learning plan for Python") == "LEARNING_PLAN"
    assert master_orchestrator.route_intent("Ask me a Python interview question") == "MOCK_INTERVIEW"
    assert master_orchestrator.route_intent("def twoSum(nums, target): return []") == "CODING_PRACTICE"
    assert master_orchestrator.route_intent("Give me career advice and target salary benchmarks") == "CAREER_ADVICE"


def test_langgraph_workflow_execution():
    state: FrameworkState = {
        "user_request": "Prepare me for a Python interview.",
        "candidate_id": "cand_test_e2e",
        "intent": "UNKNOWN",
        "current_agent": "MasterOrchestrator",
        "current_action": "route_intent",
        "candidate_profile": {},
        "retrieved_context": [],
        "task_plan": [],
        "tool_results": [],
        "interview_state": {},
        "learning_state": {},
        "coding_state": {},
        "agent_outputs": [],
        "final_response": "",
    }
    output_state = career_ai_graph.invoke(state)
    assert output_state["intent"] == "MOCK_INTERVIEW"
    assert output_state["current_agent"] == "InterviewAgent"
    assert "Adaptive Interview Question" in output_state["final_response"] or "Scorecard" in output_state["final_response"]


def test_hybrid_memory_sync():
    profile = CandidateProfile(
        candidate_id="cand_test_memory",
        name="Test User",
        target_role="AI Engineer",
        target_companies=["Google"],
        weaknesses=["System Design"],
    )
    hybrid_memory.sync_candidate_state(profile)

    fetched = hybrid_memory.structured.get_candidate("cand_test_memory")
    assert fetched.name == "Test User"

    kg = hybrid_memory.graph.get_candidate_subgraph("cand_test_memory")
    assert any(n["id"] == "cand_test_memory" for n in kg["nodes"])


def test_rag_candidate_isolation():
    rag_pipeline.index_document("cand_A", "Candidate A knows Kubernetes and PyTorch.", doc_type="resume")
    rag_pipeline.index_document("cand_B", "Candidate B knows React and Django.", doc_type="resume")

    results_A = rag_pipeline.retrieve("cand_A", "Kubernetes")
    assert len(results_A) > 0
    assert "Kubernetes" in results_A[0]["content"]

    # Ensure Candidate B cannot retrieve Candidate A's documents
    results_B_asking_A = rag_pipeline.retrieve("cand_B", "Kubernetes")
    assert len(results_B_asking_A) == 0


def test_api_orchestrator_endpoint():
    res = client.post("/api/v1/orchestrator/interact", json={
        "candidate_id": "cand_api_test",
        "user_request": "Create a learning roadmap for Python OOP"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["intent"] == "LEARNING_PLAN"
    assert data["current_agent"] == "LearningAgent"
    assert "Adaptive Learning" in data["response"]


def test_api_candidate_and_analytics_endpoints():
    res_cand = client.get("/api/v1/candidates/cand_default")
    assert res_cand.status_code == 200
    
    res_graph = client.get("/api/v1/memory/graph/cand_default")
    assert res_graph.status_code == 200
    
    res_analytics = client.get("/api/v1/analytics/cand_default")
    assert res_analytics.status_code == 200
    assert res_analytics.json()["readiness_score"] > 0
