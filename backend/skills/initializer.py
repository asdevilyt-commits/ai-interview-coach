from backend.skills.registry import registry
from backend.tools.resume_tools import parse_resume_text, score_ats_compatibility, optimize_resume_bullets
from backend.tools.learning_tools import generate_personalized_learning_plan
from backend.tools.interview_tools import get_next_question, evaluate_candidate_answer
from backend.tools.coding_tools import fetch_coding_problem, evaluate_submitted_code
from backend.agents import (
    resume_agent_instance,
    learning_agent_instance,
    interview_agent_instance,
    coding_agent_instance,
    career_agent_instance,
)


def initialize_modules():
    """Register all tools, skills, and autonomous sub-agents dynamically into DynamicRegistry."""
    # Register Resume Module
    registry.register_tool("parse_resume_text", parse_resume_text, "Extracts structured skills and data from raw resume text.")
    registry.register_tool("score_ats_compatibility", score_ats_compatibility, "Evaluates ATS compliance score and missing job keywords.")
    registry.register_tool("optimize_resume_bullets", optimize_resume_bullets, "Generates high-impact action bullets.")
    registry.register_agent("ResumeAgent", resume_agent_instance)

    # Register Learning Module
    registry.register_tool("generate_personalized_learning_plan", generate_personalized_learning_plan, "Creates dynamic learning roadmaps.")
    registry.register_agent("LearningAgent", learning_agent_instance)

    # Register Interview Module
    registry.register_tool("get_next_question", get_next_question, "Fetches adaptive technical/behavioral interview questions.")
    registry.register_tool("evaluate_candidate_answer", evaluate_candidate_answer, "Performs 8-metric semantic answer evaluation.")
    registry.register_agent("InterviewAgent", interview_agent_instance)

    # Register Coding Module
    registry.register_tool("fetch_coding_problem", fetch_coding_problem, "Retrieves algorithm and DSA problems matching candidate level.")
    registry.register_tool("evaluate_submitted_code", evaluate_submitted_code, "Evaluates Python code syntax, runtime complexity, and test cases.")
    registry.register_agent("CodingAgent", coding_agent_instance)

    # Register Career Module
    registry.register_agent("CareerAgent", career_agent_instance)


initialize_modules()
