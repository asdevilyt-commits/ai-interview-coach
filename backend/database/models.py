import json
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.database.connection import Base


def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    profile = relationship("Profile", back_populates="user", uselist=False)
    documents = relationship("Document", back_populates="user")
    assessments = relationship("Assessment", back_populates="user")
    learning_sessions = relationship("LearningSession", back_populates="user")
    interview_sessions = relationship("InterviewSession", back_populates="user")
    progress = relationship("Progress", back_populates="user", uselist=False)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    education = Column(String(200), nullable=True)
    experience_level = Column(String(100), nullable=True)
    target_role = Column(String(100), nullable=False)
    target_company = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="profile")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    doc_type = Column(String(50), nullable=False)
    file_path = Column(String(500), nullable=False)
    extracted_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="documents")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="in_progress")
    current_step = Column(Integer, default=1)
    total_questions = Column(Integer, default=7)
    score_percentage = Column(Float, default=0.0)
    strong_topics_json = Column(Text, default="[]")
    weak_topics_json = Column(Text, default="[]")
    skill_level = Column(String(50), default="Beginner")
    personalized_plan_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="assessments")
    questions = relationship("Question", back_populates="assessment")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=True)
    interview_session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=True)
    learning_session_id = Column(Integer, ForeignKey("learning_sessions.id"), nullable=True)
    question_text = Column(Text, nullable=False)
    topic = Column(String(100), nullable=False)
    difficulty = Column(String(50), default="Medium")
    options_json = Column(Text, nullable=True)
    correct_answer = Column(Text, nullable=True)
    user_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    assessment = relationship("Assessment", back_populates="questions")
    interview_session = relationship("InterviewSession", back_populates="questions")
    learning_session = relationship("LearningSession", back_populates="questions")


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(100), nullable=False)
    current_difficulty = Column(String(50), default="Medium")
    explanation = Column(Text, nullable=True)
    code_example = Column(Text, nullable=True)
    status = Column(String(50), default="active")
    history_json = Column(Text, default="[]")
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="learning_sessions")
    questions = relationship("Question", back_populates="learning_session")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mode = Column(String(50), nullable=False)
    status = Column(String(50), default="active")
    total_questions = Column(Integer, default=5)
    current_index = Column(Integer, default=0)
    history_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="interview_sessions")
    questions = relationship("Question", back_populates="interview_session")
    feedback = relationship("InterviewFeedback", back_populates="session", uselist=False)


class InterviewFeedback(Base):
    __tablename__ = "interview_feedback"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    overall_score = Column(Float, default=75.0)
    technical_score = Column(Float, default=80.0)
    communication_score = Column(Float, default=70.0)
    confidence_score = Column(Float, default=75.0)
    what_did_well_json = Column(Text, default="[]")
    improve_json = Column(Text, default="[]")
    habits_to_reduce_json = Column(Text, default="[]")
    what_to_say_json = Column(Text, default="[]")
    avoid_json = Column(Text, default="[]")
    next_focus_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=utc_now)

    session = relationship("InterviewSession", back_populates="feedback")


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    overall_percentage = Column(Float, default=70.0)
    daily_streak = Column(Integer, default=3)
    strong_topics_json = Column(Text, default='["Python", "Machine Learning"]')
    weak_topics_json = Column(Text, default='["SQL Joins", "Data Structures"]')
    recent_scores_json = Column(Text, default='[78, 72, 65]')
    recommended_next = Column(String(100), default="SQL Joins")
    todays_focus = Column(String(100), default="SQL Joins")
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="progress")
