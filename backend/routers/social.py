from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.user import User
from models.progress import SubjectProgress, Badge
from models.quiz import QuizAttempt
from routers.auth import get_current_user
from itsdangerous import URLSafeSerializer
from config import get_settings
import uuid

router = APIRouter(prefix="/social", tags=["social"])
settings = get_settings()
_serializer = URLSafeSerializer(settings.secret_key, salt="share-progress")


@router.post("/share")
async def create_share_link(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate or return existing shareable progress link."""
    if not current_user.share_token:
        current_user.share_token = _serializer.dumps(current_user.id)
        await db.commit()
    share_url = f"{settings.frontend_url}/shared/{current_user.share_token}"
    return {"share_url": share_url, "token": current_user.share_token}


@router.get("/shared/{token}")
async def get_shared_progress(token: str, db: AsyncSession = Depends(get_db)):
    """Public endpoint — no auth needed. Returns read-only progress view."""
    try:
        user_id = _serializer.loads(token)
    except Exception:
        raise HTTPException(status_code=404, detail="Invalid share link")

    ur = await db.execute(select(User).where(User.id == user_id))
    user = ur.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")

    pr = await db.execute(select(SubjectProgress).where(SubjectProgress.user_id == user_id))
    subject_progress = pr.scalars().all()

    br = await db.execute(select(Badge).where(Badge.user_id == user_id))
    badges = br.scalars().all()

    ar = await db.execute(
        select(QuizAttempt)
        .where(QuizAttempt.user_id == user_id, QuizAttempt.is_completed == True)
        .order_by(QuizAttempt.completed_at.desc())
        .limit(5)
    )
    recent = ar.scalars().all()

    return {
        "student_name": user.full_name,
        "xp_points": user.xp_points or 0,
        "streak_days": user.streak_days or 0,
        "subject_progress": [
            {
                "subject": p.subject,
                "level": p.level,
                "exam_board": p.exam_board,
                "total_quizzes": p.total_quizzes,
                "average_score": round(p.average_score, 1),
                "best_score": round(p.best_score, 1),
                "topic_scores": p.topic_scores or {},
            }
            for p in subject_progress
        ],
        "recent_activity": [
            {
                "subject": a.subject,
                "topic": a.topic,
                "score": round(a.score, 1) if a.score else None,
                "completed_at": a.completed_at.isoformat() if a.completed_at else None,
            }
            for a in recent
        ],
        "badges": [{"name": b.badge_name, "description": b.description} for b in badges],
    }
