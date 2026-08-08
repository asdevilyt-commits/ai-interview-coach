from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# User & Auth
class UserRegisterRequest(BaseModel):
    username: str = Field(..., example="alex_student")


class UserRegisterResponse(BaseModel):
    user_id: int
    username: str
    message: str


# Profile
class ProfileCreateRequest(BaseModel):
    user_id: int
    name: str
    education: Optional[str] = "Computer Science"
    experience_level: Optional[str] = "Entry Level"
    target_role: str
    target_company: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    name: str
    education: Optional[str]
    experience_level: Optional[str]
    target_role: str
    target_company: Optional[str]


# Document Upload
class DocumentUploadResponse(BaseModel):
    document_id: int
    filename: str
    doc_type: str
    extracted_text_preview: str
    message: str


# Assessment
class AssessmentStartRequest(BaseModel):
    user_id: int


class AssessmentStartResponse(BaseModel):
    assessment_id: int
    question_id: int
    question_text: str
    topic: str
    difficulty: str
    options: Optional[List[str]] = None
    step: int
    total_steps: int


class AssessmentAnswerRequest(BaseModel):
    assessment_id: int
    question_id: int
    user_answer: str


class AssessmentAnswerResponse(BaseModel):
    assessment_id: int
    is_correct: bool
    feedback: str
    next_question: Optional[Dict[str, Any]] = None
    is_completed: bool = False
    result_summary: Optional[Dict[str, Any]] = None


# Dashboard
class DashboardResponse(BaseModel):
    user_name: str
    target_role: str
    preparation_percentage: float
    todays_focus: str
    motivational_quote: str
    daily_streak: int
    recent_scores: List[float]
    strong_topics: List[str]
    weak_topics: List[str]


# Learning Flow
class LearningStartRequest(BaseModel):
    user_id: int
    topic: Optional[str] = None


class LearningStartResponse(BaseModel):
    learning_session_id: int
    topic: str
    explanation: str
    code_example: Optional[str] = None
    question_id: int
    question_text: str
    difficulty: str


class LearningAnswerRequest(BaseModel):
    learning_session_id: int
    question_id: int
    user_answer: str


class LearningAnswerResponse(BaseModel):
    learning_session_id: int
    is_correct: bool
    ai_feedback: str
    next_explanation: Optional[str] = None
    next_question: Optional[Dict[str, Any]] = None
    topic_progress: float


# Interview Flow
class InterviewStartRequest(BaseModel):
    user_id: int
    mode: str = Field(..., description="HR, Technical, or Resume/Project")


class InterviewStartResponse(BaseModel):
    interview_session_id: int
    mode: str
    question_id: int
    question_text: str
    current_index: int
    total_questions: int


class InterviewAnswerRequest(BaseModel):
    interview_session_id: int
    question_id: int
    user_answer: str


class InterviewAnswerResponse(BaseModel):
    interview_session_id: int
    ai_evaluation: str
    next_question: Optional[Dict[str, Any]] = None
    is_completed: bool = False
    feedback_id: Optional[int] = None


class VoiceInterviewRequest(BaseModel):
    interview_session_id: int
    question_id: int
    transcript: str


# Feedback Report
class InterviewFeedbackResponse(BaseModel):
    feedback_id: int
    session_id: int
    overall_score: float
    technical_score: float
    communication_score: float
    confidence_score: float
    what_did_well: List[str]
    improve: List[str]
    habits_to_reduce: List[str]
    what_to_say: List[Dict[str, str]]
    avoid: List[str]
    next_focus: List[str]


# Progress
class ProgressResponse(BaseModel):
    overall_percentage: float
    daily_streak: int
    strong_topics: List[str]
    weak_topics: List[str]
    recent_scores: List[float]
    recommended_next: str
