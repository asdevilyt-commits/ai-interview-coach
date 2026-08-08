from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class QuestionDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class InterviewType(str, Enum):
    TECHNICAL = "technical"
    RESUME_BASED = "resume_based"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"


class Question(BaseModel):
    id: str
    topic: str
    subtopic: Optional[str] = None
    question_text: str
    difficulty: QuestionDifficulty = QuestionDifficulty.MEDIUM
    interview_type: InterviewType = InterviewType.TECHNICAL
    expected_concepts: List[str] = Field(default_factory=list)
    context: Optional[str] = None


class AnswerEvaluation(BaseModel):
    score: float = Field(ge=0.0, le=10.0)
    technical_accuracy: float = Field(ge=0.0, le=10.0)
    conceptual_understanding: float = Field(ge=0.0, le=10.0)
    clarity: float = Field(ge=0.0, le=10.0)
    depth: float = Field(ge=0.0, le=10.0)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    missing_points: List[str] = Field(default_factory=list)
    ideal_answer: str
    follow_up_question: Optional[str] = None


class AdaptiveInterviewStateModel(BaseModel):
    session_id: str
    candidate_id: str
    interview_type: InterviewType = InterviewType.TECHNICAL
    candidate_level: str = "intermediate"
    current_topic: str = "general"
    question_number: int = 0
    max_questions: int = 5
    current_difficulty: QuestionDifficulty = QuestionDifficulty.MEDIUM
    
    questions_asked: List[Question] = Field(default_factory=list)
    answers: List[str] = Field(default_factory=list)
    evaluations: List[AnswerEvaluation] = Field(default_factory=list)
    
    weak_topics: List[str] = Field(default_factory=list)
    strong_topics: List[str] = Field(default_factory=list)
    follow_up_required: bool = False
    is_completed: bool = False
