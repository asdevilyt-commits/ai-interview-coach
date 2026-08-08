import json
import random
from typing import Dict, Any, List, Optional
from backend.services.llm_service import llm_service
from backend.rag.rag_engine import rag_engine


class AICoachAgent:
    """
    Main AI Coach Agent acting as a personal tuition teacher/mentor.
    Understands candidate profile, RAG context, assessment performance,
    socratic teaching flow, and mock interview evaluation.
    """

    ASSESSMENT_BANK = [
        {
            "id": 1,
            "topic": "Python Core",
            "difficulty": "Easy",
            "question": "What is the difference between a list and a tuple in Python?",
            "options": ["Lists are mutable, tuples are immutable", "Lists are immutable, tuples are mutable", "Tuples are faster for searching", "No difference"],
            "correct": "Lists are mutable, tuples are immutable"
        },
        {
            "id": 2,
            "topic": "SQL",
            "difficulty": "Medium",
            "question": "What is the difference between WHERE and HAVING clauses in SQL?",
            "options": ["WHERE filters before grouping, HAVING filters after GROUP BY", "HAVING filters before grouping, WHERE filters after", "They are completely identical", "HAVING is only used with subqueries"],
            "correct": "WHERE filters before grouping, HAVING filters after GROUP BY"
        },
        {
            "id": 3,
            "topic": "Data Structures",
            "difficulty": "Medium",
            "question": "What is the average time complexity for searching an element in a Hash Table?",
            "options": ["O(1)", "O(N)", "O(log N)", "O(N^2)"],
            "correct": "O(1)"
        },
        {
            "id": 4,
            "topic": "System Design",
            "difficulty": "Hard",
            "question": "Which HTTP status code is used when a rate limiter blocks a request?",
            "options": ["429 Too Many Requests", "503 Service Unavailable", "401 Unauthorized", "403 Forbidden"],
            "correct": "429 Too Many Requests"
        },
        {
            "id": 5,
            "topic": "Python Core",
            "difficulty": "Hard",
            "question": "How does Python handle memory management and garbage collection?",
            "options": ["Reference counting and generational garbage collection", "Manual free memory calls", "Pure mark-and-sweep only", "OS virtual memory swap"],
            "correct": "Reference counting and generational garbage collection"
        },
        {
            "id": 6,
            "topic": "SQL",
            "difficulty": "Hard",
            "question": "What is database indexing and what trade-off does it introduce?",
            "options": ["Speeds up SELECT queries but slows down INSERT/UPDATE writes", "Speeds up writes but slows down reads", "Only reduces storage size", "No trade-off"],
            "correct": "Speeds up SELECT queries but slows down INSERT/UPDATE writes"
        },
        {
            "id": 7,
            "topic": "Object Oriented Programming",
            "difficulty": "Easy",
            "question": "What is encapsulation in Object-Oriented Programming?",
            "options": ["Bundling data and methods that operate on data within a single unit", "Creating multiple copies of a class", "Inheriting attributes from a parent class", "Executing multiple threads concurrently"],
            "correct": "Bundling data and methods that operate on data within a single unit"
        }
    ]

    async def get_assessment_question(self, step: int, previous_correct: Optional[bool] = None) -> Dict[str, Any]:
        """
        Adaptive assessment question selector based on previous correctness.
        """
        target_idx = (step - 1) % len(self.ASSESSMENT_BANK)
        q = self.ASSESSMENT_BANK[target_idx]
        
        # Adaptive adjustment if previous answer outcome provided
        if previous_correct is True:
            # Pick a harder question if available
            hard_qs = [item for item in self.ASSESSMENT_BANK if item["difficulty"] in ["Medium", "Hard"]]
            q = random.choice(hard_qs) if hard_qs else q
        elif previous_correct is False:
            # Pick an easier question if available
            easy_qs = [item for item in self.ASSESSMENT_BANK if item["difficulty"] in ["Easy", "Medium"]]
            q = random.choice(easy_qs) if easy_qs else q

        return q

    async def generate_personalized_plan(self, target_role: str, score_pct: float, weak_topics: List[str]) -> Dict[str, Any]:
        prompt = (
            f"Generate a personalized 3-step study plan for a student applying for '{target_role}'. "
            f"Current Score: {score_pct}%. Weak topics: {', '.join(weak_topics)}. "
            f"Provide a structured 3-part plan."
        )
        sys_prompt = "You are an expert AI Interview Coach and tuition teacher."
        response = await llm_service.generate_response(sys_prompt, prompt)
        
        return {
            "target_role": target_role,
            "overall_readiness": f"{score_pct:.0f}%",
            "phase_1": "Core Foundations: Master Python Data Structures & Object Oriented Concepts",
            "phase_2": f"Targeted Skill Repair: Direct focus on {', '.join(weak_topics) if weak_topics else 'SQL & Algorithms'}",
            "phase_3": f"Mock Interview Simulation: Full practice for {target_role} technical & behavioral questions",
            "ai_coach_note": response
        }

    async def generate_learning_content(self, topic: str, user_id: int) -> Dict[str, Any]:
        doc_context = rag_engine.retrieve_context(topic, user_id=user_id)
        context_str = f"\nRelevant Student Notes:\n{doc_context}" if doc_context else ""

        sys_prompt = "You are a personal Socratic AI tuition teacher."
        prompt = (
            f"Teach the topic '{topic}' to a student.{context_str}\n"
            f"Format response with:\n"
            f"1. Clear concise concept explanation\n"
            f"2. Practical code or real-world example\n"
            f"3. One practice question to test understanding."
        )

        response = await llm_service.generate_response(sys_prompt, prompt)

        return {
            "topic": topic,
            "explanation": response,
            "code_example": (
                "```python\n"
                "# Socratic Example: " + topic + "\n"
                "def solve_problem(data):\n"
                "    # Efficient logic demonstration\n"
                "    return [x for x in data if x % 2 == 0]\n"
                "```"
            ),
            "question": f"Based on the concept above, explain how you would handle edge cases in {topic}?"
        }

    async def generate_interview_question(self, mode: str, current_index: int, user_id: int, target_role: str) -> str:
        doc_context = rag_engine.retrieve_context(f"{mode} {target_role}", user_id=user_id)

        if mode == "HR":
            hr_questions = [
                "Tell me about yourself and why you are interested in this position.",
                "Describe a situation where you faced a challenging technical roadblock. How did you resolve it?",
                "Where do you see yourself professionally in the next 2 to 3 years?",
                "What are your key technical strengths, and what area are you actively working to improve?"
            ]
            return hr_questions[current_index % len(hr_questions)]
        elif mode == "Resume/Project":
            if doc_context:
                return f"Based on your uploaded documents: How did you design and implement the architecture described in your project notes? ({doc_context[:120]}...)"
            return "Can you walk me through the most technically complex project listed on your resume and your specific role in it?"
        else: # Technical
            tech_questions = [
                f"How would you design a scalable system for {target_role} handling 10,000 requests per second?",
                "Explain how garbage collection works in Python and how memory leaks can occur.",
                "What is the difference between optimistic and pessimistic locking in database transactions?",
                "How do you approach optimizing an expensive O(N^2) algorithm down to O(N log N)?"
            ]
            return tech_questions[current_index % len(tech_questions)]

    async def evaluate_interview_answer(self, mode: str, question_text: str, user_answer: str) -> str:
        sys_prompt = "You are an encouraging, expert AI Interview Coach evaluating a candidate's mock interview answer."
        prompt = (
            f"Mode: {mode}\n"
            f"Question: {question_text}\n"
            f"Student Answer: {user_answer}\n"
            f"Evaluate the answer. Praise strengths, highlight missing points, and ask a concise follow-up."
        )
        return await llm_service.generate_response(sys_prompt, prompt)

    async def generate_interview_feedback(self, session_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates comprehensive feedback report after interview session.
        """
        # Calculate realistic scores based on answer length and completion
        total = max(len(session_history), 1)
        scores = []
        for item in session_history:
            ans = item.get("answer", "")
            word_count = len(ans.split())
            if word_count > 25:
                scores.append(85)
            elif word_count > 10:
                scores.append(75)
            else:
                scores.append(60)

        avg_score = sum(scores) / len(scores) if scores else 78.0

        return {
            "overall_score": round(avg_score, 1),
            "technical_score": round(min(avg_score + 4.0, 95.0), 1),
            "communication_score": round(max(avg_score - 3.0, 65.0), 1),
            "confidence_score": round(avg_score, 1),
            "what_did_well": [
                "Clear explanation of technical concepts and fundamentals.",
                "Structured approach when describing problem-solving steps.",
                "Good project domain knowledge reflected in responses."
            ],
            "improve": [
                "Structure answers using the STAR method (Situation, Task, Action, Result).",
                "Be more direct and concise in opening sentences.",
                "Include more quantitative metrics (e.g. % performance improvement)."
            ],
            "habits_to_reduce": [
                "Filler words like 'basically', 'like', and 'actually'",
                "Long mid-sentence pauses when thinking",
                "Overly casual introductory phrasing"
            ],
            "what_to_say": [
                {
                    "instead_of": "Basically, I worked on the backend API using Python...",
                    "say": "I architected and deployed RESTful microservices in Python, optimizing endpoint throughput by 30%."
                },
                {
                    "instead_of": "I guess I am pretty good at SQL joins...",
                    "say": "I have extensive experience writing optimized SQL joins and indexing strategies for relational databases."
                }
            ],
            "avoid": [
                "Excessive informal slang during technical explanations",
                "Vague general statements without specific tech stack details",
                "Memorized-sounding generic answers"
            ],
            "next_focus": [
                "SQL Joins & Indexing Optimization",
                "STAR Method Behavioral Response Structuring",
                "System Design Bottleneck Analysis"
            ]
        }


ai_coach = AICoachAgent()
