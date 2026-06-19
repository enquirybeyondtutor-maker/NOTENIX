from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from database import get_db
from models.user import User
from routers.auth import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/global")
async def global_leaderboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(User.id, User.full_name, User.xp_points, User.streak_days)
        .where(User.xp_points > 0)
        .order_by(desc(User.xp_points))
        .limit(20)
    )
    rows = result.all()
    leaderboard = []
    current_rank = None
    for i, row in enumerate(rows):
        is_you = row.id == current_user.id
        entry = {
            "rank": i + 1,
            "name": row.full_name if is_you else _mask_name(row.full_name),
            "xp": row.xp_points or 0,
            "streak": row.streak_days or 0,
            "is_you": is_you,
            "badge": _rank_badge(i + 1),
        }
        if is_you:
            current_rank = i + 1
        leaderboard.append(entry)
    return {"leaderboard": leaderboard, "your_rank": current_rank}


@router.get("/weekly")
async def weekly_leaderboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from models.quiz import QuizAttempt
    week_ago = datetime.utcnow() - timedelta(days=7)
    result = await db.execute(
        select(
            QuizAttempt.user_id,
            func.count(QuizAttempt.id).label("quizzes"),
            func.avg(QuizAttempt.score).label("avg_score"),
        )
        .where(QuizAttempt.completed_at >= week_ago, QuizAttempt.is_completed == True)
        .group_by(QuizAttempt.user_id)
        .order_by(desc("quizzes"))
        .limit(10)
    )
    rows = result.all()
    leaderboard = []
    current_rank = None
    for i, row in enumerate(rows):
        ur = await db.execute(select(User).where(User.id == row.user_id))
        user = ur.scalar_one_or_none()
        if not user:
            continue
        is_you = user.id == current_user.id
        entry = {
            "rank": i + 1,
            "name": user.full_name if is_you else _mask_name(user.full_name),
            "quizzes_this_week": row.quizzes,
            "avg_score": round(row.avg_score or 0, 1),
            "xp": user.xp_points or 0,
            "is_you": is_you,
            "badge": _rank_badge(i + 1),
        }
        if is_you:
            current_rank = i + 1
        leaderboard.append(entry)
    return {"leaderboard": leaderboard, "your_rank": current_rank}


def _mask_name(full_name: str) -> str:
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0][0] + "***"
    return parts[0] + " " + parts[-1][0] + "."


def _rank_badge(rank: int) -> str:
    return {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "")
