from typing import Dict, Any, List
from backend.models.learning import LearningPlan, WeeklyPlan, TopicModule


def generate_personalized_learning_plan(
    topic: str, candidate_level: str = "intermediate", weak_topics: List[str] = None
) -> Dict[str, Any]:
    """Generate a custom 4-week to 5-week structured learning roadmap."""
    weak_topics = weak_topics or ["OOP", "Generators", "DSA"]
    
    plan = LearningPlan(
        candidate_id="cand_default",
        target_role="AI / Software Engineer",
        target_topic=topic,
        estimated_level=candidate_level,
        weak_topics=weak_topics,
        strong_topics=["Fundamentals", "SQL"],
        weekly_plans=[
            WeeklyPlan(
                week_number=1,
                focus_area=f"{topic} Core & Fundamentals",
                learning_goals=[f"Master foundational {topic} mechanics", "Understand memory management"],
                modules=[
                    TopicModule(title="Data Structures & Core Types", description="Primitive types, mutations, memory allocation", priority="medium"),
                    TopicModule(title="Control Flow & Function Mechanics", description="Scope, closures, args/kwargs", priority="medium"),
                ]
            ),
            WeeklyPlan(
                week_number=2,
                focus_area=f"{topic} Advanced & OOP Architecture",
                learning_goals=["Master Object Oriented Design", "Implement dunder/magic methods and decorators"],
                modules=[
                    TopicModule(title="OOP Principles & Design Patterns", description="Inheritance, polymorphism, encapsulation", priority="high"),
                    TopicModule(title="Decorators, Generators & Context Managers", description="Iterators, yields, resource management", priority="high"),
                ]
            ),
            WeeklyPlan(
                week_number=3,
                focus_area="Data Structures & Algorithms Practice",
                learning_goals=["Solve 15+ LeetCode Medium problem patterns"],
                modules=[
                    TopicModule(title="Arrays, HashMaps & Two Pointers", description="Optimizing lookup and traversal algorithms", priority="medium"),
                    TopicModule(title="Trees, Graphs & Dynamic Programming", description="DFS, BFS, memoization strategies", priority="high"),
                ]
            ),
            WeeklyPlan(
                week_number=4,
                focus_area="System Design & Mock Interview Drills",
                learning_goals=["Complete 3 timed technical mock interviews"],
                modules=[
                    TopicModule(title="System Architecture & Scalability", description="Caching, load balancing, DB indexing", priority="medium"),
                    TopicModule(title="Mock Interview Simulations", description="Live technical questioning and feedback loops", priority="high"),
                ]
            ),
        ]
    )
    return plan.model_dump(mode="json")
