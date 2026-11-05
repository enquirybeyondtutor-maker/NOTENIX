"""Admin endpoints: issue accounts, reset passwords, set access, suspend, change roles."""
import re
import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from config import settings
from database import get_db
from models import User, Test, TestAttempt, QuizSession
from security import require_admin, is_admin, hash_password

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
        "access_until": u.access_until.isoformat() if getattr(u, "access_until", None) else None,
        "access_kind": getattr(u, "access_kind", None),
        "needs_activation": bool(getattr(u, "needs_activation", False)),
        "parent_email": getattr(u, "parent_email", None),
        "parent_phone": getattr(u, "parent_phone", None),
        "activated_at": u.activated_at.isoformat() if getattr(u, "activated_at", None) else None,
        "terms_accepted_at": u.terms_accepted_at.isoformat() if getattr(u, "terms_accepted_at", None) else None,
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


# ── Beyond Tutors-issued accounts ────────────────────────────────────────────

# No 0/O/1/l/I, so a password read out or copied from WhatsApp isn't misread.
_PW_CHARS = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789"


def _new_password() -> str:
    """e.g. k7Pm-x3Qd-9tRw: 12 random characters, easy to type."""
    return "-".join("".join(secrets.choice(_PW_CHARS) for _ in range(4)) for _ in range(3))


def _apply_access(u: User, kind: str) -> None:
    """trial → free for TRIAL_DAYS; year → +SUBSCRIPTION_DAYS from today or from the
    current end date if still live (renewing early loses nothing); none → no expiry."""
    now = datetime.utcnow()
    if kind == "trial":
        u.access_kind, u.access_until = "trial", now + timedelta(days=settings.trial_days)
    elif kind == "year":
        start = u.access_until if (u.access_until and u.access_until > now and u.access_kind == "paid") else now
        u.access_kind, u.access_until = "paid", start + timedelta(days=settings.subscription_days)
    elif kind == "none":
        u.access_kind, u.access_until = None, None
    else:
        raise HTTPException(400, "Access must be trial, year or none")


class CreateUserIn(BaseModel):
    full_name: str
    email: str | None = None   # blank → firstname@<student_id_domain>
    role: str = "student"      # student | teacher
    access: str = "trial"      # trial | year | none (students only)


class AccessIn(BaseModel):
    access: str                # trial | year | none


@router.get("/suggest-id")
async def suggest_id(name: str, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    return {"email": await _free_id(name, db)}


async def _free_id(name: str, db: AsyncSession) -> str:
    """musa@thebeyondtutors.com, then musa.k@…, then musa2@… if taken."""
    parts = [re.sub(r"[^a-z0-9]", "", p) for p in name.lower().split()]
    parts = [p for p in parts if p] or ["student"]
    first, last = parts[0], (parts[-1] if len(parts) > 1 else "")
    candidates = [first] + ([f"{first}.{last[0]}", f"{first}.{last}"] if last else [])
    candidates += [f"{first}{n}" for n in range(2, 100)]
    for c in candidates:
        email = f"{c}@{settings.student_id_domain}"
        if not (await db.execute(select(User.id).where(User.email == email))).first():
            return email
    raise HTTPException(400, "Couldn't find a free user ID; please type one.")


@router.post("/users")
async def create_user(data: CreateUserIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """Issue a Notenix account. The password is returned once, here, and never stored in plain text."""
    name = data.full_name.strip()[:120]
    if len(name) < 2:
        raise HTTPException(400, "Please enter the student's name.")
    if data.role not in ("student", "teacher"):
        raise HTTPException(400, "Role must be student or teacher")
    email = (data.email or "").strip().lower() or await _free_id(name, db)
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise HTTPException(400, "User ID must look like name@thebeyondtutors.com")
    if (await db.execute(select(User.id).where(User.email == email))).first():
        raise HTTPException(400, f"{email} is already taken.")
    password = _new_password()
    u = User(email=email, full_name=name, role=data.role, password_hash=hash_password(password),
             is_verified=True, token_version=0, needs_activation=(data.role == "student"))
    if data.role == "student":
        _apply_access(u, data.access)
    db.add(u)
    await db.commit()
    await db.refresh(u)
    return {"user": _user_row(u), "password": password}


@router.post("/users/{user_id}/reset-password")
async def reset_password(user_id: int, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """New random password; signs the user out everywhere."""
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    if is_admin(u) and u.id != admin.id:
        raise HTTPException(400, "You can't reset another admin's password.")
    password = _new_password()
    u.password_hash = hash_password(password)
    u.token_version = (u.token_version or 0) + 1
    await db.commit()
    return {"id": u.id, "email": u.email, "password": password}


@router.post("/users/{user_id}/require-activation")
async def require_activation(user_id: int, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """Send a student back to 'Pending activation' with a fresh temporary password, so the
    parent goes through activation (email, phone, terms, OTP) on their next sign-in.
    Clears the previously saved parent details."""
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    if (u.role or "student") != "student" or is_admin(u):
        raise HTTPException(400, "Only student accounts need parent activation.")
    password = _new_password()
    u.password_hash = hash_password(password)
    u.needs_activation = True
    u.parent_email = u.parent_phone = None
    u.activated_at = u.terms_accepted_at = None
    u.otp_hash, u.otp_expires_at, u.otp_attempts = None, None, 0
    u.token_version = (u.token_version or 0) + 1
    await db.commit()
    return {"id": u.id, "email": u.email, "password": password}


@router.post("/users/{user_id}/access")
async def set_access(user_id: int, data: AccessIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    _apply_access(u, data.access)
    await db.commit()
    return _user_row(u)
