from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.user import User
from services.analytics_service import get_dashboard_stats
from services.srs_service import get_due_cards
from routers.auth import get_current_user

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/dashboard")
async def dashboard(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_dashboard_stats(db, current_user.id)


@router.get("/srs-due")
async def srs_due_cards(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    cards = await get_due_cards(db, current_user.id)
    return {"due_count": len(cards), "cards": cards}
