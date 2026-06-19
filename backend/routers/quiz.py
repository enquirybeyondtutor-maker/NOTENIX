from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, field_validator
from datetime import datetime
from database import get_db
from models.user import User
from models.quiz import QuizAttempt, QuizAnalysis
from services.quiz_service import generate_quiz, analyze_quiz_results, sanitise_topic
from services.analytics_service import update_subject_progress, update_streak_and_xp
from services.srs_service import update_srs_cards
from routers.auth import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address
import uuid

router = APIRouter(prefix="/quiz", tags=["quiz"])
limiter = Limiter(key_func=get_remote_address)

VALID_SUBJECTS = {
    "maths", "biology", "chemistry", "physics", "computer_science",
    "economics", "english_literature", "geography", "history", "psychology", "business",
}
VALID_LEVELS = {"gcse", "a_level"}
VALID_BOARDS = {"AQA", "Edexcel", "OCR", "Cambridge"}
VALID_DIFFICULTIES = {"easy", "medium", "hard", "mixed"}


class QuizCreateRequest(BaseModel):
    subject: str
    topic: str
    level: str
    exam_board: str
    num_questions: int = 10
    difficulty: str = "mixed"
    is_mock_exam: bool = False

    @field_validator("topic")
    @classmethod
    def clean_topic(cls, v: str) -> str:
        return sanitise_topic(v)

    @field_validator("num_questions")
    @classmethod
    def clamp_questions(cls, v: int) -> int:
        return max(1, min(40, v))

    @field_validator("subject")
    @classmethod
    def valid_subject(cls, v: str) -> str:
        if v not in VALID_SUBJECTS:
            raise ValueError(f"Invalid subject")
        return v

    @field_validator("level")
    @classmethod
    def valid_level(cls, v: str) -> str:
        if v not in VALID_LEVELS:
            raise ValueError("Invalid level")
        return v

    @field_validator("difficulty")
    @classmethod
    def valid_difficulty(cls, v: str) -> str:
        if v not in VALID_DIFFICULTIES:
            return "mixed"
        return v


class SubmitAnswersRequest(BaseModel):
    attempt_id: str
    answers: dict[str, str]
    time_taken_seconds: int


def check_quiz_access(user: User):
    is_active = user.subscription_status == "active" and user.subscription_tier in ("monthly", "yearly")
    if is_active:
        return
    if (user.free_quizzes_used or 0) >= (user.free_quiz_limit or 3):
        raise HTTPException(
            status_code=402,
            detail="Free quiz limit reached. Please subscribe to continue.",
        )


@router.post("/create")
@limiter.limit("30/minute")
async def create_quiz(
    request: Request,
    req: QuizCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    check_quiz_access(current_user)

    try:
        questions = await generate_quiz(
            subject=req.subject,
            topic=req.topic,
            level=req.level,
            exam_board=req.exam_board,
            num_questions=req.num_questions,
            difficulty=req.difficulty,
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    attempt = QuizAttempt(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        subject=req.subject,
        topic=req.topic,
        level=req.level,
        exam_board=req.exam_board,
        num_questions=len(questions),
        difficulty=req.difficulty,
        questions=questions,
        is_mock_exam=req.is_mock_exam,
    )
    db.add(attempt)
    current_user.free_quizzes_used = (current_user.free_quizzes_used or 0) + 1
    await db.commit()
    await db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "questions": [
            {
                "id": q["id"],
                "question": q["question"],
                "options": q["options"],
                "marks": q.get("marks", 1),
                "difficulty": q.get("difficulty", "medium"),
            }
            for q in questions
        ],
        "subject": req.subject,
        "topic": req.topic,
        "level": req.level,
        "exam_board": req.exam_board,
        "num_questions": len(questions),
    }


@router.post("/submit")
async def submit_quiz(
    req: SubmitAnswersRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(QuizAttempt).where(
            QuizAttempt.id == req.attempt_id,
            QuizAttempt.user_id == current_user.id,
        )
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(status_code=404, detail="Quiz attempt not found")
    if attempt.is_completed:
        raise HTTPException(status_code=400, detail="Quiz already submitted")

    analysis = await analyze_quiz_results(
        attempt.questions, req.answers, attempt.subject, attempt.level
    )

    attempt.answers = req.answers
    attempt.score = analysis["overall_score"]
    attempt.time_taken_seconds = req.time_taken_seconds
    attempt.is_completed = True
    attempt.completed_at = datetime.utcnow()

    quiz_analysis = QuizAnalysis(
        id=str(uuid.uuid4()),
        attempt_id=attempt.id,
        overall_score=analysis["overall_score"],
        strength_areas=analysis["strength_areas"],
        weak_areas=analysis["weak_areas"],
        question_breakdown=analysis["question_breakdown"],
        ai_feedback=analysis["ai_feedback"],
        improvement_tips=analysis["improvement_tips"],
        estimated_grade=analysis["estimated_grade"],
    )
    db.add(quiz_analysis)
    await db.commit()

    attempt_data = {
        "subject": attempt.subject,
        "topic": attempt.topic,
        "level": attempt.level,
    }
    await update_subject_progress(db, current_user.id, attempt, analysis)
    xp_earned = await update_streak_and_xp(db, current_user.id, analysis["overall_score"], attempt.num_questions)
    await update_srs_cards(db, current_user.id, attempt_data, analysis)

    return {**analysis, "xp_earned": xp_earned, "attempt_id": attempt.id}


@router.get("/history")
async def quiz_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(QuizAttempt)
        .where(QuizAttempt.user_id == current_user.id)
        .order_by(QuizAttempt.created_at.desc())
        .limit(20)
    )
    attempts = result.scalars().all()
    return [
        {
            "id": a.id,
            "subject": a.subject,
            "topic": a.topic,
            "level": a.level,
            "exam_board": a.exam_board,
            "score": a.score,
            "num_questions": a.num_questions,
            "is_completed": a.is_completed,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in attempts
    ]


@router.get("/result/{attempt_id}")
async def get_result(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(QuizAttempt).where(
            QuizAttempt.id == attempt_id,
            QuizAttempt.user_id == current_user.id,
        )
    )
    attempt = result.scalar_one_or_none()
    if not attempt:
        raise HTTPException(status_code=404, detail="Not found")

    ar = await db.execute(select(QuizAnalysis).where(QuizAnalysis.attempt_id == attempt_id))
    analysis = ar.scalar_one_or_none()

    return {
        "attempt": {
            "id": attempt.id,
            "subject": attempt.subject,
            "topic": attempt.topic,
            "level": attempt.level,
            "exam_board": attempt.exam_board,
            "score": attempt.score,
            "num_questions": attempt.num_questions,
            "time_taken_seconds": attempt.time_taken_seconds,
        },
        "analysis": {
            "overall_score": analysis.overall_score,
            "estimated_grade": analysis.estimated_grade,
            "strength_areas": analysis.strength_areas,
            "weak_areas": analysis.weak_areas,
            "ai_feedback": analysis.ai_feedback,
            "improvement_tips": analysis.improvement_tips,
            "question_breakdown": analysis.question_breakdown,
            "subtopic_scores": {},
        } if analysis else None,
    }
