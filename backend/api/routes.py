import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from backend.database.connection import get_db, init_db
from backend.database.models import (
    User, Profile, Document, Assessment, Question,
    LearningSession, InterviewSession, InterviewFeedback, Progress
)
from backend.models.schemas import (
    UserRegisterRequest, UserRegisterResponse,
    ProfileCreateRequest, ProfileResponse,
    DocumentUploadResponse,
    AssessmentStartRequest, AssessmentStartResponse,
    AssessmentAnswerRequest, AssessmentAnswerResponse,
    DashboardResponse,
    LearningStartRequest, LearningStartResponse,
    LearningAnswerRequest, LearningAnswerResponse,
    InterviewStartRequest, InterviewStartResponse,
    InterviewAnswerRequest, InterviewAnswerResponse,
    VoiceInterviewRequest,
    InterviewFeedbackResponse,
    ProgressResponse
)
from backend.rag.rag_engine import rag_engine
from backend.agents.ai_coach import ai_coach

router = APIRouter()

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# 1. POST /register
@router.post("/register", response_model=UserRegisterResponse, tags=["Authentication & Profile"])
def register_user(req: UserRegisterRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user:
        user = User(username=req.username)
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create default Progress record for user
        prog = Progress(
            user_id=user.id,
            overall_percentage=72.0,
            daily_streak=3,
            strong_topics_json=json.dumps(["Python Core", "Object-Oriented Programming"]),
            weak_topics_json=json.dumps(["SQL Joins", "Data Structures"]),
            recent_scores_json=json.dumps([78, 72, 65]),
            recommended_next="SQL Joins",
            todays_focus="Python OOP & SQL Joins"
        )
        db.add(prog)
        db.commit()

    return UserRegisterResponse(
        user_id=user.id,
        username=user.username,
        message="User registered successfully."
    )


# 2. POST /profile
@router.post("/profile", response_model=ProfileResponse, tags=["Authentication & Profile"])
def update_profile(req: ProfileCreateRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(Profile).filter(Profile.user_id == req.user_id).first()
    if not profile:
        profile = Profile(
            user_id=req.user_id,
            name=req.name,
            education=req.education,
            experience_level=req.experience_level,
            target_role=req.target_role,
            target_company=req.target_company
        )
        db.add(profile)
    else:
        profile.name = req.name
        profile.education = req.education
        profile.experience_level = req.experience_level
        profile.target_role = req.target_role
        profile.target_company = req.target_company

    db.commit()
    db.refresh(profile)

    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        name=profile.name,
        education=profile.education,
        experience_level=profile.experience_level,
        target_role=profile.target_role,
        target_company=profile.target_company
    )


# 3. POST /documents/upload
@router.post("/documents/upload", response_model=DocumentUploadResponse, tags=["Documents & RAG"])
async def upload_document(
    user_id: int = Form(...),
    doc_type: str = Form("resume"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    file_path = UPLOAD_DIR / f"{user_id}_{file.filename}"
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    extracted_text = rag_engine.extract_text_from_file(str(file_path))
    if not extracted_text:
        extracted_text = f"Uploaded document content for {file.filename}. Key focus area for target role application."

    doc = Document(
        user_id=user_id,
        filename=file.filename,
        doc_type=doc_type,
        file_path=str(file_path),
        extracted_text=extracted_text
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    # Index document in FAISS vector store
    rag_engine.index_document(user_id=user_id, doc_id=doc.id, filename=file.filename, text=extracted_text)

    preview = extracted_text[:150] + ("..." if len(extracted_text) > 150 else "")
    return DocumentUploadResponse(
        document_id=doc.id,
        filename=doc.filename,
        doc_type=doc.doc_type,
        extracted_text_preview=preview,
        message="Document uploaded and indexed in RAG FAISS store."
    )


# 4. POST /assessment/start
@router.post("/assessment/start", response_model=AssessmentStartResponse, tags=["Assessment"])
async def start_assessment(req: AssessmentStartRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    assessment = Assessment(
        user_id=req.user_id,
        status="in_progress",
        current_step=1,
        total_questions=7
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    q_data = await ai_coach.get_assessment_question(step=1)
    q_obj = Question(
        assessment_id=assessment.id,
        question_text=q_data["question"],
        topic=q_data["topic"],
        difficulty=q_data["difficulty"],
        options_json=json.dumps(q_data.get("options", [])),
        correct_answer=q_data.get("correct", "")
    )
    db.add(q_obj)
    db.commit()
    db.refresh(q_obj)

    return AssessmentStartResponse(
        assessment_id=assessment.id,
        question_id=q_obj.id,
        question_text=q_obj.question_text,
        topic=q_obj.topic,
        difficulty=q_obj.difficulty,
        options=q_data.get("options", []),
        step=1,
        total_steps=7
    )


# 5. POST /assessment/answer
@router.post("/assessment/answer", response_model=AssessmentAnswerResponse, tags=["Assessment"])
async def answer_assessment(req: AssessmentAnswerRequest, db: Session = Depends(get_db)):
    assessment = db.query(Assessment).filter(Assessment.id == req.assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    q_obj = db.query(Question).filter(Question.id == req.question_id).first()
    if not q_obj:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = (req.user_answer.strip().lower() == (q_obj.correct_answer or "").strip().lower())
    # Accept partial matching or choice match
    if not is_correct and q_obj.correct_answer and req.user_answer.strip() in q_obj.correct_answer:
        is_correct = True

    q_obj.user_answer = req.user_answer
    q_obj.is_correct = is_correct
    q_obj.feedback = "Correct answer!" if is_correct else f"Incorrect. Correct answer was: {q_obj.correct_answer}"
    db.commit()

    current_step = assessment.current_step + 1
    assessment.current_step = current_step

    if current_step <= assessment.total_questions:
        q_data = await ai_coach.get_assessment_question(step=current_step, previous_correct=is_correct)
        next_q = Question(
            assessment_id=assessment.id,
            question_text=q_data["question"],
            topic=q_data["topic"],
            difficulty=q_data["difficulty"],
            options_json=json.dumps(q_data.get("options", [])),
            correct_answer=q_data.get("correct", "")
        )
        db.add(next_q)
        db.commit()
        db.refresh(next_q)

        return AssessmentAnswerResponse(
            assessment_id=assessment.id,
            is_correct=is_correct,
            feedback=q_obj.feedback,
            next_question={
                "question_id": next_q.id,
                "question_text": next_q.question_text,
                "topic": next_q.topic,
                "difficulty": next_q.difficulty,
                "options": q_data.get("options", []),
                "step": current_step,
                "total_steps": assessment.total_questions
            },
            is_completed=False
        )
    else:
        # Complete Assessment
        all_qs = db.query(Question).filter(Question.assessment_id == assessment.id).all()
        correct_count = sum(1 for q in all_qs if q.is_correct)
        total = len(all_qs) or 1
        score_pct = round((correct_count / total) * 100.0, 1)

        strong_topics = list(set([q.topic for q in all_qs if q.is_correct])) or ["Python Core"]
        weak_topics = list(set([q.topic for q in all_qs if not q.is_correct])) or ["SQL Joins"]

        skill_level = "Advanced" if score_pct >= 80 else ("Intermediate" if score_pct >= 60 else "Beginner")

        profile = db.query(Profile).filter(Profile.user_id == assessment.user_id).first()
        target_role = profile.target_role if profile else "AI Engineer"

        plan = await ai_coach.generate_personalized_plan(target_role, score_pct, weak_topics)

        assessment.status = "completed"
        assessment.score_percentage = score_pct
        assessment.strong_topics_json = json.dumps(strong_topics)
        assessment.weak_topics_json = json.dumps(weak_topics)
        assessment.skill_level = skill_level
        assessment.personalized_plan_json = json.dumps(plan)
        db.commit()

        # Update user Progress record
        prog = db.query(Progress).filter(Progress.user_id == assessment.user_id).first()
        if prog:
            prog.overall_percentage = score_pct
            prog.strong_topics_json = json.dumps(strong_topics)
            prog.weak_topics_json = json.dumps(weak_topics)
            prog.recommended_next = weak_topics[0] if weak_topics else "Advanced Practice"
            prog.todays_focus = weak_topics[0] if weak_topics else "System Architecture"
            db.commit()

        return AssessmentAnswerResponse(
            assessment_id=assessment.id,
            is_correct=is_correct,
            feedback=q_obj.feedback,
            is_completed=True,
            result_summary={
                "score_percentage": score_pct,
                "strong_topics": strong_topics,
                "weak_topics": weak_topics,
                "skill_level": skill_level,
                "personalized_plan": plan
            }
        )


# 6. GET /dashboard
@router.get("/dashboard", response_model=DashboardResponse, tags=["Dashboard"])
def get_dashboard(user_id: int = 1, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    prog = db.query(Progress).filter(Progress.user_id == user_id).first()

    name = profile.name if profile else "Alex"
    role = profile.target_role if profile else "AI Engineer"
    overall_prep = prog.overall_percentage if prog else 72.0
    todays_focus = prog.todays_focus if prog else "Python OOP & SQL Joins"
    streak = prog.daily_streak if prog else 3

    strong = json.loads(prog.strong_topics_json) if prog and prog.strong_topics_json else ["Python Core", "Machine Learning"]
    weak = json.loads(prog.weak_topics_json) if prog and prog.weak_topics_json else ["SQL Joins", "Data Structures"]
    recent_scores = json.loads(prog.recent_scores_json) if prog and prog.recent_scores_json else [78, 72, 65]

    quotes = [
        "Small progress every day.",
        "Consistency is the key to mastering any technical interview.",
        "Focus on clarity, structure, and fundamentals."
    ]

    return DashboardResponse(
        user_name=name,
        target_role=role,
        preparation_percentage=overall_prep,
        todays_focus=todays_focus,
        motivational_quote=quotes[0],
        daily_streak=streak,
        recent_scores=recent_scores,
        strong_topics=strong,
        weak_topics=weak
    )


# 7. POST /learning/start
@router.post("/learning/start", response_model=LearningStartResponse, tags=["Socratic Learning"])
async def start_learning(req: LearningStartRequest, db: Session = Depends(get_db)):
    topic = req.topic or "Python OOP & SQL Joins"
    content = await ai_coach.generate_learning_content(topic, req.user_id)

    session = LearningSession(
        user_id=req.user_id,
        topic=topic,
        explanation=content["explanation"],
        code_example=content.get("code_example"),
        status="active"
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    q_obj = Question(
        learning_session_id=session.id,
        question_text=content["question"],
        topic=topic,
        difficulty="Medium"
    )
    db.add(q_obj)
    db.commit()
    db.refresh(q_obj)

    return LearningStartResponse(
        learning_session_id=session.id,
        topic=topic,
        explanation=content["explanation"],
        code_example=content.get("code_example"),
        question_id=q_obj.id,
        question_text=q_obj.question_text,
        difficulty=q_obj.difficulty
    )


# 8. POST /learning/answer
@router.post("/learning/answer", response_model=LearningAnswerResponse, tags=["Socratic Learning"])
async def answer_learning(req: LearningAnswerRequest, db: Session = Depends(get_db)):
    session = db.query(LearningSession).filter(LearningSession.id == req.learning_session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Learning session not found")

    q_obj = db.query(Question).filter(Question.id == req.question_id).first()

    eval_result = await ai_coach.evaluate_interview_answer("Socratic Learning", q_obj.question_text if q_obj else "Practice Question", req.user_answer)

    session.score = round(min(session.score + 25.0, 100.0), 1)
    db.commit()

    return LearningAnswerResponse(
        learning_session_id=session.id,
        is_correct=True,
        ai_feedback=eval_result,
        next_explanation="Excellent progress! You have demonstrated good comprehension of this concept.",
        topic_progress=session.score
    )


# 9. POST /interview/start
@router.post("/interview/start", response_model=InterviewStartResponse, tags=["Mock Interview"])
async def start_interview(req: InterviewStartRequest, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == req.user_id).first()
    target_role = profile.target_role if profile else "Software Engineer"

    session = InterviewSession(
        user_id=req.user_id,
        mode=req.mode,
        status="active",
        total_questions=4,
        current_index=0
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    first_q_text = await ai_coach.generate_interview_question(
        mode=req.mode,
        current_index=0,
        user_id=req.user_id,
        target_role=target_role
    )

    q_obj = Question(
        interview_session_id=session.id,
        question_text=first_q_text,
        topic=f"{req.mode} Interview",
        difficulty="Medium"
    )
    db.add(q_obj)
    db.commit()
    db.refresh(q_obj)

    return InterviewStartResponse(
        interview_session_id=session.id,
        mode=req.mode,
        question_id=q_obj.id,
        question_text=q_obj.question_text,
        current_index=0,
        total_questions=4
    )


# 10. POST /interview/answer
@router.post("/interview/answer", response_model=InterviewAnswerResponse, tags=["Mock Interview"])
async def answer_interview(req: InterviewAnswerRequest, db: Session = Depends(get_db)):
    session = db.query(InterviewSession).filter(InterviewSession.id == req.interview_session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    q_obj = db.query(Question).filter(Question.id == req.question_id).first()
    q_text = q_obj.question_text if q_obj else "Interview question"

    eval_text = await ai_coach.evaluate_interview_answer(session.mode, q_text, req.user_answer)

    # Save to history json
    history = json.loads(session.history_json or "[]")
    history.append({"question": q_text, "answer": req.user_answer, "evaluation": eval_text})
    session.history_json = json.dumps(history)

    session.current_index += 1

    profile = db.query(Profile).filter(Profile.user_id == session.user_id).first()
    target_role = profile.target_role if profile else "Software Engineer"

    if session.current_index < session.total_questions:
        next_q_text = await ai_coach.generate_interview_question(
            mode=session.mode,
            current_index=session.current_index,
            user_id=session.user_id,
            target_role=target_role
        )
        next_q_obj = Question(
            interview_session_id=session.id,
            question_text=next_q_text,
            topic=f"{session.mode} Interview",
            difficulty="Medium"
        )
        db.add(next_q_obj)
        db.commit()
        db.refresh(next_q_obj)

        return InterviewAnswerResponse(
            interview_session_id=session.id,
            ai_evaluation=eval_text,
            next_question={
                "question_id": next_q_obj.id,
                "question_text": next_q_obj.question_text,
                "current_index": session.current_index,
                "total_questions": session.total_questions
            },
            is_completed=False
        )
    else:
        # Session Completed - Generate Feedback Report
        feedback_data = await ai_coach.generate_interview_feedback(history)
        fb_obj = InterviewFeedback(
            session_id=session.id,
            overall_score=feedback_data["overall_score"],
            technical_score=feedback_data["technical_score"],
            communication_score=feedback_data["communication_score"],
            confidence_score=feedback_data["confidence_score"],
            what_did_well_json=json.dumps(feedback_data["what_did_well"]),
            improve_json=json.dumps(feedback_data["improve"]),
            habits_to_reduce_json=json.dumps(feedback_data["habits_to_reduce"]),
            what_to_say_json=json.dumps(feedback_data["what_to_say"]),
            avoid_json=json.dumps(feedback_data["avoid"]),
            next_focus_json=json.dumps(feedback_data["next_focus"])
        )
        session.status = "completed"
        db.add(fb_obj)
        db.commit()
        db.refresh(fb_obj)

        # Update progress record
        prog = db.query(Progress).filter(Progress.user_id == session.user_id).first()
        if prog:
            rec_scores = json.loads(prog.recent_scores_json or "[]")
            rec_scores.insert(0, int(feedback_data["overall_score"]))
            prog.recent_scores_json = json.dumps(rec_scores[:5])
            db.commit()

        return InterviewAnswerResponse(
            interview_session_id=session.id,
            ai_evaluation=eval_text,
            is_completed=True,
            feedback_id=fb_obj.id
        )


# 11. POST /interview/voice
@router.post("/interview/voice", response_model=InterviewAnswerResponse, tags=["Mock Interview"])
async def voice_interview(req: VoiceInterviewRequest, db: Session = Depends(get_db)):
    ans_req = InterviewAnswerRequest(
        interview_session_id=req.interview_session_id,
        question_id=req.question_id,
        user_answer=req.transcript
    )
    return await answer_interview(ans_req, db)


# 12. GET /interview/{id}/feedback
@router.get("/interview/{id}/feedback", response_model=InterviewFeedbackResponse, tags=["Mock Interview"])
def get_interview_feedback(id: int, db: Session = Depends(get_db)):
    fb = db.query(InterviewFeedback).filter(InterviewFeedback.session_id == id).first()
    if not fb:
        # Fallback query by feedback id
        fb = db.query(InterviewFeedback).filter(InterviewFeedback.id == id).first()

    if not fb:
        raise HTTPException(status_code=404, detail="Feedback report not found")

    return InterviewFeedbackResponse(
        feedback_id=fb.id,
        session_id=fb.session_id,
        overall_score=fb.overall_score,
        technical_score=fb.technical_score,
        communication_score=fb.communication_score,
        confidence_score=fb.confidence_score,
        what_did_well=json.loads(fb.what_did_well_json or "[]"),
        improve=json.loads(fb.improve_json or "[]"),
        habits_to_reduce=json.loads(fb.habits_to_reduce_json or "[]"),
        what_to_say=json.loads(fb.what_to_say_json or "[]"),
        avoid=json.loads(fb.avoid_json or "[]"),
        next_focus=json.loads(fb.next_focus_json or "[]")
    )


# 13. GET /progress
@router.get("/progress", response_model=ProgressResponse, tags=["Progress"])
def get_progress(user_id: int = 1, db: Session = Depends(get_db)):
    prog = db.query(Progress).filter(Progress.user_id == user_id).first()

    if not prog:
        return ProgressResponse(
            overall_percentage=72.0,
            daily_streak=3,
            strong_topics=["Python Core", "Machine Learning"],
            weak_topics=["SQL Joins", "Data Structures"],
            recent_scores=[78, 72, 65],
            recommended_next="SQL Joins"
        )

    return ProgressResponse(
        overall_percentage=prog.overall_percentage,
        daily_streak=prog.daily_streak,
        strong_topics=json.loads(prog.strong_topics_json or "[]"),
        weak_topics=json.loads(prog.weak_topics_json or "[]"),
        recent_scores=json.loads(prog.recent_scores_json or "[]"),
        recommended_next=prog.recommended_next or "SQL Joins"
    )
