from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from models import User, QuizSession
from security import get_current_user

router = APIRouter(prefix="/progress", tags=["progress"])

BADGES = [
    {"id": "first_quiz", "name": "First Steps", "threshold": 1, "metric": "quizzes"},
    {"id": "ten_quizzes", "name": "Getting Serious", "threshold": 10, "metric": "quizzes"},
    {"id": "streak_3", "name": "On Fire", "threshold": 3, "metric": "streak"},
    {"id": "streak_7", "name": "Unstoppable", "threshold": 7, "metric": "streak"},
    {"id": "xp_100", "name": "Centurion", "threshold": 100, "metric": "xp"},
    {"id": "xp_500", "name": "Scholar", "threshold": 500, "metric": "xp"},
]


@router.get("/dashboard")
async def dashboard(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    sessions = (await db.execute(
        select(QuizSession).where(QuizSession.user_id == user.id, QuizSession.completed_at.isnot(None))
        .order_by(QuizSession.completed_at.desc())
    )).scalars().all()

    avg_score = round(sum(s.score for s in sessions) / len(sessions), 1) if sessions else 0
    by_subject: dict = {}
    for s in sessions:
        by_subject.setdefault(s.subject, []).append(s.score)
    subject_stats = [{"subject": k, "avg": round(sum(v) / len(v), 1), "count": len(v)} for k, v in by_subject.items()]

    metrics = {"quizzes": user.quiz_count, "streak": user.streak, "xp": user.xp}
    earned_badges = [b for b in BADGES if metrics.get(b["metric"], 0) >= b["threshold"]]

    return {
        "xp": user.xp, "streak": user.streak, "plan": user.plan,
        "quiz_count": user.quiz_count, "avg_score": avg_score,
        "subject_stats": subject_stats,
        "badges": earned_badges,
        "recent": [{
            "subject": s.subject, "topic": s.topic, "mode": s.mode,
            "score": s.score, "completed_at": s.completed_at.isoformat() if s.completed_at else None,
        } for s in sessions[:5]],
    }
