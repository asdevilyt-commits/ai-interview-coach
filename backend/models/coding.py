from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class TestCase(BaseModel):
    input_data: str
    expected_output: str
    is_hidden: bool = False


class CodingProblem(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str  # Easy, Medium, Hard
    topic: str  # Arrays, Trees, DP, Graphs, etc.
    source: str = "Standard DSA Engine"  # LeetCode, HackerRank, etc.
    constraints: List[str] = Field(default_factory=list)
    sample_test_cases: List[TestCase] = Field(default_factory=list)
    hints: List[str] = Field(default_factory=list)


class CodeSubmission(BaseModel):
    problem_id: str
    language: str
    code: str


class ComplexityAnalysis(BaseModel):
    time_complexity: str
    space_complexity: str
    is_optimal: bool
    explanation: str


class CodeEvaluationResult(BaseModel):
    submission: CodeSubmission
    is_correct: bool
    score: float = Field(ge=0.0, le=10.0)
    complexity: ComplexityAnalysis
    passed_tests: int
    total_tests: int
    edge_cases_missed: List[str] = Field(default_factory=list)
    feedback: str
    suggested_improvements: List[str] = Field(default_factory=list)
