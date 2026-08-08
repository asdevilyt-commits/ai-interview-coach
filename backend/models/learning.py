from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class TopicModule(BaseModel):
    title: str
    description: str
    key_concepts: List[str] = Field(default_factory=list)
    recommended_resources: List[str] = Field(default_factory=list)
    estimated_hours: float = 2.0
    priority: str = "medium"  # high, medium, low
    is_completed: bool = False


class WeeklyPlan(BaseModel):
    week_number: int
    focus_area: str
    modules: List[TopicModule] = Field(default_factory=list)
    learning_goals: List[str] = Field(default_factory=list)


class LearningPlan(BaseModel):
    candidate_id: str
    target_role: str
    target_topic: str
    estimated_level: str
    weekly_plans: List[WeeklyPlan] = Field(default_factory=list)
    strong_topics: List[str] = Field(default_factory=list)
    weak_topics: List[str] = Field(default_factory=list)
    dynamic_adjustments: List[str] = Field(default_factory=list)
