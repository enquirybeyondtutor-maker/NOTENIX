from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from database import get_db
from models import User, QuizSession
from security import get_current_user

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/global")
async def global_board(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(
        select(User.id, User.full_name, User.xp).order_by(User.xp.desc()).limit(20)
    )).all()
    return [{"rank": i + 1, "name": n, "xp": x} for i, (uid, n, x) in enumerate(rows)]


@router.get("/weekly")
async def weekly_board(db: AsyncSession = Depends(get_db)):
    week_ago = datetime.utcnow() - timedelta(days=7)
    rows = (await db.execute(
        select(User.full_name, func.coalesce(func.sum(QuizSession.xp_earned), 0).label("wxp"))
        .join(QuizSession, QuizSession.user_id == User.id)
        .where(QuizSession.completed_at >= week_ago)
        .group_by(User.id, User.full_name)
        .order_by(func.sum(QuizSession.xp_earned).desc())
        .limit(20)
    )).all()
    return [{"rank": i + 1, "name": n, "xp": int(x)} for i, (n, x) in enumerate(rows)]
