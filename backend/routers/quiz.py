from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
import random

from database import get_db
from models import User, Question, QuizSession
from security import get_current_user
from services import ai
from config import settings

router = APIRouter(prefix="/quiz", tags=["quiz"])


class CreateQuizIn(BaseModel):
    subject: str
    topic: str
    level: str = "A-Level"          # GCSE | A-Level
    difficulty: str = "medium"
    mode: str = "quiz"              # quiz (mcq) | exam
    num_questions: int = 10


class SubmitQuizIn(BaseModel):
    session_id: int
    answers: list  # mcq: list[str chosen option]; exam: list[str written answer]


def _check_quota(user: User):
    if user.plan != "pro" and user.quiz_count >= settings.free_quiz_limit:
        raise HTTPException(402, "Free quiz limit reached. Upgrade to Pro for unlimited quizzes.")


@router.get("/subjects")
async def subjects(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(
        select(Question.subject, Question.level, Question.topic).distinct()
    )).all()
    out: dict = {}
    for subject, level, topic in rows:
        out.setdefault(level, {}).setdefault(subject, set()).add(topic)
    return {lvl: {s: sorted(t) for s, t in subs.items()} for lvl, subs in out.items()}


@router.post("/create")
async def create_quiz(data: CreateQuizIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    _check_quota(user)
    n = max(1, min(data.num_questions, 20))

    if data.mode == "exam":
        if user.plan != "pro":
            raise HTTPException(402, "Exam mode is a Pro feature. Upgrade to unlock real past-paper practice.")
        # pull real extracted exam questions for this topic
        q = await db.execute(
            select(Question).where(
                Question.subject == data.subject,
                Question.level == data.level,
                Question.topic == data.topic,
                Question.qtype == "exam",
            ).limit(50)
        )
        pool = q.scalars().all()
        if not pool:
            raise HTTPException(404, "No exam questions available for this topic yet.")
        chosen = random.sample(pool, min(n, len(pool)))
        questions = [{
            "id": x.id, "question": x.question_text, "marks": x.marks or 4,
            "mark_scheme": x.mark_scheme,
        } for x in chosen]
    else:
        # MCQ mode: pull real past-paper questions for this exact topic as RAG context,
        # then generate fresh auto-gradable MCQs grounded in that authentic content.
        rows = (await db.execute(
            select(Question).where(
                Question.subject == data.subject,
                Question.level == data.level,
                Question.topic == data.topic,
            ).limit(15)
        )).scalars().all()
        context = [r.question_text for r in rows]
        generated = ai.generate_mcqs(data.subject, data.topic, data.difficulty, n, context)
        if not generated:
            raise HTTPException(502, "Could not generate quiz. Please try again.")
        questions = generated

    session = QuizSession(
        user_id=user.id, subject=data.subject, topic=data.topic,
        mode=data.mode, questions=questions,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    # strip answers before sending to client
    safe = []
    for qq in questions:
        item = {k: v for k, v in qq.items() if k not in ("answer", "explanation", "mark_scheme")}
        safe.append(item)
    return {"session_id": session.id, "mode": data.mode, "questions": safe}


@router.post("/submit")
async def submit_quiz(data: SubmitQuizIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    session = (await db.execute(
        select(QuizSession).where(QuizSession.id == data.session_id, QuizSession.user_id == user.id)
    )).scalar_one_or_none()
    if not session:
        raise HTTPException(404, "Quiz session not found")
    if session.completed_at:
        raise HTTPException(400, "Quiz already submitted")

    questions = session.questions
    results = []

    if session.mode == "exam":
        total_marks = sum(q.get("marks", 4) for q in questions)
        earned = 0
        for q, ans in zip(questions, data.answers):
            scheme = q.get("mark_scheme") or ai.generate_mark_scheme(q["question"], q.get("marks", 4), session.subject)
            marked = ai.mark_answer(q["question"], q.get("marks", 4), scheme, str(ans), session.subject)
            earned += marked["marks_awarded"]
            results.append({
                "question": q["question"], "marks": q.get("marks", 4),
                "marks_awarded": marked["marks_awarded"],
                "feedback": marked["feedback"], "model_answer": marked["model_answer"],
                "your_answer": ans,
            })
        score = round(100 * earned / total_marks, 1) if total_marks else 0
    else:
        correct = 0
        for q, ans in zip(questions, data.answers):
            is_correct = str(ans).strip() == str(q.get("answer", "")).strip()
            correct += int(is_correct)
            results.append({
                "question": q["question"], "your_answer": ans,
                "correct_answer": q.get("answer"), "is_correct": is_correct,
                "explanation": q.get("explanation"),
            })
        score = round(100 * correct / len(questions), 1) if questions else 0

    xp = int(score / 10) + (5 if score >= 80 else 0)

    # update streak (based on quiz activity per day)
    today = datetime.utcnow().date()
    last = user.last_active.date() if user.last_active else None
    if last == today:
        user.streak = max(user.streak, 1)        # already active today
    elif last == today - timedelta(days=1):
        user.streak += 1                          # consecutive day
    else:
        user.streak = 1                           # streak reset / first ever
    user.last_active = datetime.utcnow()
    user.xp += xp
    user.quiz_count += 1

    session.answers = data.answers
    session.score = score
    session.xp_earned = xp
    session.completed_at = datetime.utcnow()
    await db.commit()

    return {"score": score, "xp_earned": xp, "results": results, "streak": user.streak, "total_xp": user.xp}


@router.get("/history")
async def history(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(
        select(QuizSession).where(QuizSession.user_id == user.id, QuizSession.completed_at.isnot(None))
        .order_by(QuizSession.completed_at.desc()).limit(20)
    )).scalars().all()
    return [{
        "id": r.id, "subject": r.subject, "topic": r.topic, "mode": r.mode,
        "score": r.score, "xp_earned": r.xp_earned,
        "completed_at": r.completed_at.isoformat() if r.completed_at else None,
    } for r in rows]
