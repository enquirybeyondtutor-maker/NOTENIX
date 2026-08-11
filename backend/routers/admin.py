"""Admin endpoints: view all users, suspend/reinstate, change roles."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from models import User, Test, TestAttempt, QuizSession
from security import require_admin, is_admin

router = APIRouter(prefix="/admin", tags=["admin"])


class RoleIn(BaseModel):
    role: str  # student | teacher | admin


class WriteAccessIn(BaseModel):
    enabled: bool


def _user_row(u: User) -> dict:
    return {
        "id": u.id, "email": u.email, "full_name": u.full_name,
        "role": (getattr(u, "role", None) or "student"),
        "is_active": getattr(u, "is_active", True),
        "is_admin": is_admin(u),
        "can_write": getattr(u, "can_write", False),
        "plan": u.plan, "xp": u.xp,
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "last_active": u.last_active.isoformat() if u.last_active else None,
    }


@router.get("/overview")
async def overview(admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    total = (await db.execute(select(func.count()).select_from(User))).scalar() or 0
    teachers = (await db.execute(select(func.count()).select_from(User).where(User.role == "teacher"))).scalar() or 0
    students = (await db.execute(select(func.count()).select_from(User).where(User.role == "student"))).scalar() or 0
    suspended = (await db.execute(select(func.count()).select_from(User).where(User.is_active == False))).scalar() or 0  # noqa: E712
    tests = (await db.execute(select(func.count()).select_from(Test))).scalar() or 0
    attempts = (await db.execute(select(func.count()).select_from(TestAttempt))).scalar() or 0
    quizzes = (await db.execute(select(func.count()).select_from(QuizSession))).scalar() or 0
    return {
        "users": total, "teachers": teachers, "students": students, "suspended": suspended,
        "tests": tests, "test_attempts": attempts, "quiz_sessions": quizzes,
    }


@router.get("/users")
async def list_users(admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(User).order_by(User.created_at.desc()))).scalars().all()
    return [_user_row(u) for u in rows]


@router.post("/users/{user_id}/ban")
async def ban_user(user_id: int, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    if user_id == admin.id:
        raise HTTPException(400, "You can't suspend your own account.")
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    if is_admin(u):
        raise HTTPException(400, "You can't suspend another admin.")
    u.is_active = False
    await db.commit()
    return {"id": u.id, "is_active": False}


@router.post("/users/{user_id}/unban")
async def unban_user(user_id: int, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    u.is_active = True
    await db.commit()
    return {"id": u.id, "is_active": True}


@router.post("/users/{user_id}/role")
async def set_role(user_id: int, data: RoleIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    if data.role not in ("student", "teacher", "admin"):
        raise HTTPException(400, "Invalid role")
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    u.role = data.role
    await db.commit()
    return {"id": u.id, "role": u.role}


@router.post("/users/{user_id}/write-access")
async def set_write_access(user_id: int, data: WriteAccessIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """Grant/revoke written-answer practice access for a non-Pro account."""
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    u.can_write = bool(data.enabled)
    await db.commit()
    return {"id": u.id, "can_write": u.can_write}
