import json
from typing import Dict, Any, List
from backend.core.llm import ask_llm
from backend.models.interview import Question, QuestionDifficulty, InterviewType, AnswerEvaluation
from backend.core.logger import logger


QUESTION_BANK = {
    "Python": [
        {
            "id": "py_01",
            "topic": "Python",
            "text": "What is the difference between shallow copy and deep copy in Python? Give a code scenario where choosing deepcopy is mandatory.",
            "difficulty": QuestionDifficulty.EASY,
            "concepts": ["copy module", "mutable objects", "references", "nested lists"],
        },
        {
            "id": "py_02",
            "topic": "Python",
            "text": "Explain Python Decorators and how functools.wraps preserves function signature and docstrings.",
            "difficulty": QuestionDifficulty.MEDIUM,
            "concepts": ["first-class functions", "higher-order functions", "wraps", "metadata"],
        },
        {
            "id": "py_03",
            "topic": "Python",
            "text": "How does the Global Interpreter Lock (GIL) affect multi-threading vs multi-processing in CPython?",
            "difficulty": QuestionDifficulty.HARD,
            "concepts": ["GIL", "CPython", "concurrency", "CPU-bound vs I/O-bound"],
        },
        {
            "id": "py_04",
            "topic": "Python",
            "text": "How do generators work under the hood using yield, and how do they save memory compared to list comprehensions?",
            "difficulty": QuestionDifficulty.MEDIUM,
            "concepts": ["yield", "iterator protocol", "generator objects", "lazy evaluation"],
        },
    ],
    "SQL": [
        {
            "id": "sql_01",
            "topic": "SQL",
            "text": "Explain the difference between WHERE and HAVING clauses in SQL with an aggregation example.",
            "difficulty": QuestionDifficulty.EASY,
            "concepts": ["GROUP BY", "WHERE", "HAVING", "aggregations"],
        },
        {
            "id": "sql_02",
            "topic": "SQL",
            "text": "How do B-Tree indexes accelerate SQL SELECT queries, and what is the trade-off during INSERT/UPDATE operations?",
            "difficulty": QuestionDifficulty.MEDIUM,
            "concepts": ["B-Tree", "Indexes", "Write overhead", "Query execution plan"],
        },
    ],
    "RAG": [
        {
            "id": "rag_01",
            "topic": "RAG",
            "text": "Why choose FAISS vector indexing, and how do you evaluate chunk size vs overlap when building a RAG document retriever?",
            "difficulty": QuestionDifficulty.MEDIUM,
            "concepts": ["Vector DB", "FAISS", "Chunking strategy", "Semantic retrieval"],
        }
    ]
}


def get_next_question(topic: str = "Python", difficulty: str = "medium", index: int = 0) -> Dict[str, Any]:
    """Retrieve adaptive question matching target topic and current difficulty level."""
    pool = QUESTION_BANK.get(topic, QUESTION_BANK["Python"])
    selected = pool[index % len(pool)]
    
    q = Question(
        id=selected["id"],
        topic=selected["topic"],
        question_text=selected["text"],
        difficulty=QuestionDifficulty(difficulty.lower()) if difficulty.lower() in ["easy", "medium", "hard"] else QuestionDifficulty.MEDIUM,
        interview_type=InterviewType.TECHNICAL,
        expected_concepts=selected["concepts"],
    )
    return q.model_dump(mode="json")


def evaluate_candidate_answer(question_text: str, candidate_answer: str, expected_concepts: List[str] = None) -> Dict[str, Any]:
    """
    Multi-dimensional Semantic Evaluation:
    Technical Accuracy, Conceptual Understanding, Depth, Clarity, Communication.
    Generates structured scorecard with strengths, weaknesses, missing points, ideal answer, and follow-up.
    """
    expected_str = ", ".join(expected_concepts or [])
    prompt = f"""
Evaluate the candidate's interview answer.

Question: "{question_text}"
Expected Concepts: {expected_str}
Candidate Answer: "{candidate_answer}"

Return ONLY a raw valid JSON object without markdown fences with these exact keys:
{{
  "score": 8.0,
  "technical_accuracy": 8.5,
  "conceptual_understanding": 8.0,
  "clarity": 7.5,
  "depth": 8.0,
  "strengths": ["Clear explanation"],
  "weaknesses": ["Minor detail omitted"],
  "missing_points": ["Specific edge cases"],
  "ideal_answer": "An ideal answer should state...",
  "follow_up_question": "How would this behave if...?"
}}
"""
    try:
        raw_response = ask_llm(prompt=prompt, temperature=0.0)
        clean_json = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(clean_json)
        eval_model = AnswerEvaluation(**data)
        return eval_model.model_dump(mode="json")
    except Exception as e:
        logger.error(f"Fallback answer evaluation due to LLM error: {e}")
        # Deterministic fallback evaluation
        ans_len = len(candidate_answer.split())
        score = min(9.0, max(4.0, ans_len * 0.2))
        return {
            "score": round(score, 1),
            "technical_accuracy": round(score, 1),
            "conceptual_understanding": round(score, 1),
            "clarity": 8.0,
            "depth": round(score - 0.5, 1),
            "strengths": ["Demonstrates core domain familiarity."],
            "weaknesses": ["Could expand on underlying internals and performance trade-offs."],
            "missing_points": expected_concepts or ["Performance characteristics"],
            "ideal_answer": f"An ideal answer thoroughly explains {question_text} covering core mechanisms and production considerations.",
            "follow_up_question": "Can you provide a practical production code example of this pattern?",
        }
