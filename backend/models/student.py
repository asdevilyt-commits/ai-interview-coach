from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class StudentProfile(BaseModel):
    student_id: str = "student_default"
    name: str = "Alex Smith"
    education: str = "B.Tech Computer Science"
    current_year: str = "4th Year"
    branch: str = "Computer Science"
    programming_languages: List[str] = Field(default_factory=lambda: ["Python", "SQL", "C++"])
    technical_interests: List[str] = Field(default_factory=lambda: ["AI Engineering", "RAG Systems", "Backend Microservices"])


class CareerGoal(BaseModel):
    target_role: str = "AI Engineer"
    target_companies: List[str] = Field(default_factory=lambda: ["Google", "OpenAI", "Meta"])
    expected_package: str = "$180,000 USD"
    interview_timeline: str = "3 Months"
    available_study_hours_per_day: float = 2.0


class SkillRating(BaseModel):
    topic: str
    proficiency_percentage: float = Field(ge=0.0, le=100.0)  # e.g., 82%
    last_studied: Optional[str] = None
    mistake_count: int = 0
    confidence_level: str = "Medium"  # Low, Medium, High


class HomeworkItem(BaseModel):
    id: str
    title: str
    description: str
    due_date: Optional[str] = None
    is_completed: bool = False


class TuitionClassPlan(BaseModel):
    class_id: str
    topic: str
    duration_minutes: int = 45
    review_summary: str
    today_focus: str
    agenda: List[str] = Field(default_factory=list)
    status: str = "NOT_STARTED"  # NOT_STARTED, IN_PROGRESS, COMPLETED


class StudentKnowledgeModel(BaseModel):
    student_id: str = "student_default"
    profile: StudentProfile = Field(default_factory=StudentProfile)
    career_goal: CareerGoal = Field(default_factory=CareerGoal)
    
    # Skill Matrix %
    skills: List[SkillRating] = Field(default_factory=lambda: [
        SkillRating(topic="Python Core", proficiency_percentage=82.0, confidence_level="High"),
        SkillRating(topic="SQL Aggregations", proficiency_percentage=65.0, confidence_level="Medium"),
        SkillRating(topic="DSA & Algorithms", proficiency_percentage=42.0, confidence_level="Low"),
        SkillRating(topic="Machine Learning", proficiency_percentage=71.0, confidence_level="Medium"),
        SkillRating(topic="Generative AI & RAG", proficiency_percentage=58.0, confidence_level="Medium"),
    ])

    weak_areas: List[str] = Field(default_factory=lambda: ["Recursion & Dynamic Programming", "Python OOP Inheritance", "Database Indexing"])
    strong_areas: List[str] = Field(default_factory=lambda: ["Python Core Syntax", "Pandas DataFrames", "REST API Design"])

    recent_mistakes: List[str] = Field(default_factory=lambda: ["Forgot method overriding syntax in Python", "Confused WHERE vs HAVING in SQL aggregation"])
    homework_list: List[HomeworkItem] = Field(default_factory=lambda: [
        HomeworkItem(id="hw_1", title="Python OOP Practice", description="Implement a shape hierarchy with method overriding"),
        HomeworkItem(id="hw_2", title="SQL Join Drill", description="Solve 2 aggregation queries using GROUP BY and HAVING"),
    ])

    current_streak_days: int = 12
    total_classes_completed: int = 48
    last_class_date: Optional[str] = "Yesterday"
    
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
