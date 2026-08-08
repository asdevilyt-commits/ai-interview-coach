from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class SkillLevel(BaseModel):
    name: str
    category: str = "general"
    proficiency: float = Field(default=0.5, ge=0.0, le=1.0)
    verified: bool = False
    notes: Optional[str] = None


class ProjectDetail(BaseModel):
    title: str
    description: str
    tech_stack: List[str] = Field(default_factory=list)
    key_achievements: List[str] = Field(default_factory=list)
    architecture_highlights: Optional[str] = None


class ExperienceDetail(BaseModel):
    company: str
    role: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: str = ""
    skills_used: List[str] = Field(default_factory=list)


class CandidateProfile(BaseModel):
    candidate_id: str
    name: str
    email: Optional[str] = None
    target_role: str = "Software Engineer"
    target_companies: List[str] = Field(default_factory=list)
    years_experience: float = 0.0

    skills: List[SkillLevel] = Field(default_factory=list)
    projects: List[ProjectDetail] = Field(default_factory=list)
    experiences: List[ExperienceDetail] = Field(default_factory=list)
    education: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)

    weaknesses: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)

    ats_score: float = 0.0
    overall_readiness_score: float = 0.0
    technical_skill_score: float = 0.0
    coding_score: float = 0.0
    communication_score: float = 0.0

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
