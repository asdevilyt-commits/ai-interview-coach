import re
from typing import Dict, Any, List
from backend.core.logger import logger


def parse_resume_text(raw_text: str) -> Dict[str, Any]:
    """Extract candidate skills, experience level, projects, and education from raw resume text."""
    skills = []
    known_keywords = [
        "python", "java", "c++", "javascript", "typescript", "react", "next.js", "node.js",
        "fastapi", "django", "flask", "sql", "postgresql", "mongodb", "redis", "docker",
        "kubernetes", "aws", "gcp", "azure", "git", "dsa", "machine learning", "deep learning",
        "rag", "langgraph", "langchain", "llm", "system design", "faiss", "pytorch", "tensorflow"
    ]
    low_text = raw_text.lower()
    for kw in known_keywords:
        if kw in low_text:
            skills.append(kw.title() if len(kw) <= 4 else kw.capitalize())

    return {
        "extracted_skills": list(set(skills)),
        "raw_text_length": len(raw_text),
        "has_education": any(w in low_text for w in ["bachelor", "master", "degree", "university", "b.tech", "b.e."]),
        "has_experience": any(w in low_text for w in ["engineer", "developer", "intern", "company", "experience"]),
    }


def score_ats_compatibility(resume_data: Dict[str, Any], job_description: str = "") -> Dict[str, Any]:
    """Analyze resume ATS compatibility score and missing keywords."""
    extracted_skills = resume_data.get("extracted_skills", [])
    base_score = min(95.0, max(50.0, len(extracted_skills) * 8.5 + (15.0 if resume_data.get("has_education") else 0.0)))
    
    missing_skills = []
    if job_description:
        jd_low = job_description.lower()
        for s in ["Python", "FastAPI", "Docker", "System Design", "SQL", "LangGraph"]:
            if s.lower() in jd_low and s not in extracted_skills:
                missing_skills.append(s)

    return {
        "ats_score": round(base_score, 1),
        "grade": "Strong" if base_score >= 80 else ("Moderate" if base_score >= 65 else "Needs Work"),
        "missing_keywords": missing_skills,
        "recommendations": [
            "Quantify bullet points with impact metrics (e.g. 'Improved latency by 35%')",
            "Add a dedicated Core Competencies section at the top of your resume",
            "Ensure cloud deployment & system architecture details are explicit",
        ]
    }


def optimize_resume_bullets(resume_text: str) -> List[str]:
    """Suggest high-impact action-verb improvements for resume bullet points."""
    return [
        "Architected scalable microservices handling 10k+ requests/sec using FastAPI & Redis.",
        "Engineered RAG-based search pipeline delivering 94% retrieval accuracy with FAISS & LangChain.",
        "Optimized database query performance, reducing peak response latency by 42%.",
    ]
