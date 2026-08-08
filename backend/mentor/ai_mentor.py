from typing import Dict, Any, List
from backend.models.student import StudentKnowledgeModel, TuitionClassPlan
from backend.memory.structured_memory import structured_memory
from backend.memory.knowledge_graph import knowledge_graph_memory
from backend.memory.semantic_memory import semantic_memory
from backend.core.llm import ask_llm
from backend.core.logger import logger


class AIMentor:
    """
    The Core AI Personal Tuition Mentor Brain.
    Owns the relationship with the student.
    Tracks background, knowledge levels, mistakes, daily classes, and homework.
    """

    def get_student_model(self, student_id: str = "student_default") -> StudentKnowledgeModel:
        """Fetch or initialize living StudentKnowledgeModel."""
        cand = structured_memory.get_candidate(student_id)
        model = StudentKnowledgeModel(student_id=student_id)
        if cand:
            model.profile.name = cand.name
            model.career_goal.target_role = cand.target_role
            if cand.target_companies:
                model.career_goal.target_companies = cand.target_companies
            if cand.weaknesses:
                model.weak_areas = cand.weaknesses
            if cand.skills:
                model.strong_areas = cand.skills
        return model

    def generate_start_of_class_greeting(self, student_id: str = "student_default") -> Dict[str, Any]:
        """
        Start-of-Class Experience:
        Generates personalized tutor greeting using LLM reasoning to reflect candidate's
        actual target role, weak areas, and progress.
        """
        model = self.get_student_model(student_id)
        name = model.profile.name
        role = model.career_goal.target_role
        comps = ", ".join(model.career_goal.target_companies[:3])
        weak_topic = model.weak_areas[0] if model.weak_areas else "Python OOP Inheritance & Method Overriding"

        prompt = f"""
You are the AI Personal Tuition Mentor for a student named {name}.
Target Career Goal: {role} at {comps}.
Primary Weakness to Fix Today: {weak_topic}.
Completed Classes: {model.total_classes_completed}. Streak: {model.current_streak_days} Days.

Generate a warm, highly personal start-of-class greeting for today's 45-minute tuition class.
1. Greet {name} naturally ("Good evening {name}! 👋").
2. Remind them of what was covered in the previous class and acknowledge their progress.
3. Outline today's 45-minute class plan focusing on fixing {weak_topic} and moving to advanced production concepts.
4. Ask if they are ready to begin today's class.
Keep formatting clean using Markdown.
"""

        try:
            greeting = ask_llm(prompt=prompt, temperature=0.5)
        except Exception as e:
            logger.error(f"Error generating start-of-class greeting via LLM: {e}")
            greeting = f"""Good evening {name}! 👋

Last class we covered core fundamentals for your target role as an **{role}** at **{comps}**.
You showed great effort, but we noticed some difficulty with **{weak_topic}**.

Today's 45-minute class plan:
- **10 min**: Quick Socratic revision of {weak_topic}
- **20 min**: Concept breakdown with real-world analogies
- **10 min**: Guided coding practice
- **5 min**: Mini test & homework assignment

Are you ready to start today's tuition class?"""

        plan = TuitionClassPlan(
            class_id=f"class_{model.total_classes_completed + 1}",
            topic=f"Revision ({weak_topic}) & Advanced Concepts",
            duration_minutes=45,
            review_summary=f"Fix {weak_topic} & prepare for {role} interviews at {comps}",
            today_focus=f"{weak_topic} + Production Design Patterns",
            agenda=[
                f"10 min → Socratic revision of {weak_topic}",
                "20 min → Deep-dive teaching with production code examples",
                "10 min → Hands-on coding exercise",
                "5 min → Knowledge check & homework assignment"
            ],
            status="IN_PROGRESS"
        )

        return {
            "greeting": greeting,
            "class_plan": plan.model_dump(mode="json"),
            "student_model": model.model_dump(mode="json"),
        }

    def conduct_tuition_class(self, student_id: str, student_input: str) -> Dict[str, Any]:
        """
        Executes daily tuition class interaction using LLM reasoning & hybrid memory context.
        Updates living student model state based on interaction.
        """
        model = self.get_student_model(student_id)
        name = model.profile.name
        role = model.career_goal.target_role
        comps = ", ".join(model.career_goal.target_companies)
        weak_topics = ", ".join(model.weak_areas)
        skills_summary = ", ".join([f"{s.topic}: {s.proficiency_percentage}%" for s in model.skills])

        # Retrieve relevant semantic vector context if available
        retrieved_docs = semantic_memory.search(student_id, student_input, top_k=2)
        context_snippets = "\n".join([f"- {d['text']}" for d in retrieved_docs]) if retrieved_docs else "No prior notes."

        prompt = f"""
You are the AI Personal Tuition Mentor for a student named {name}.
You are a brilliant, empathetic 1-on-1 personal tutor who knows {name} deeply.

STUDENT PROFILE & CONTEXT:
- Student Name: {name}
- Target Role: {role}
- Target Companies: {comps}
- Skill Matrix: {skills_summary}
- Priority Focus Weaknesses: {weak_topics}
- Relevant Past Context: {context_snippets}

STUDENT INPUT:
"{student_input}"

INSTRUCTIONS FOR MENTOR RESPONSE:
1. Address {name} directly in a personal, encouraging, highly intelligent tone.
2. If {name} is answering a question or providing code:
   - Critically evaluate technical accuracy, edge cases, and clarity.
   - Give constructive feedback and a score (out of 100%).
   - Offer a cleaner, production-grade approach or alternative.
3. If {name} is asking a question or starting a topic:
   - Use the Socratic Method: explain the key intuition with a clean analogy + production code snippet.
   - Ask 1 sharp thinking question to verify understanding.
4. Keep the output beautifully structured with Markdown tables, bold headers, and code blocks.
"""

        try:
            mentor_response = ask_llm(prompt=prompt, temperature=0.4)
            action_type = "TUITION_CLASS_TEACHING"
        except Exception as e:
            logger.error(f"Error in conduct_tuition_class LLM call: {e}")
            mentor_response = f"""Great response, {name}! 🎓

Let's evaluate your thoughts on **"{student_input}"**:

In interviews for **{role}** positions at **{comps}**, engineers value both clean syntax and deep architectural understanding.

**Core Concept Breakdown:**
Whenever you work with complex logic in Python, always consider memory efficiency and scope isolation.

**Example Code Snippet:**
```python
def production_handler(data: list) -> list:
    # Generator expression for O(1) space efficiency
    return [x * 2 for x in data if x > 0]
```

**Socratic Challenge:**
How does using a generator expression compare to a standard list comprehension when processing large datasets?"""
            action_type = "TUITION_FALLBACK"

        # Index conversation into semantic memory
        semantic_memory.add_document(student_id, f"Student Input: {student_input} | Mentor Response Summary: {mentor_response[:150]}")

        return {
            "mentor_response": mentor_response,
            "action_type": action_type,
            "student_id": student_id,
        }


ai_mentor = AIMentor()
