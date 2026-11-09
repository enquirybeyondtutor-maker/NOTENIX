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
from models import User, Test, TestAttempt, QuizSession, TestAssignment, Enrolment
from security import require_admin, is_admin, hash_password
from services import pricing
from services import courses as course_svc

router = APIRouter(prefix="/admin", tags=["admin"])


class RoleIn(BaseModel):
    role: str  # student | teacher | admin


class WriteAccessIn(BaseModel):
    enabled: bool


def _user_row(u: User, enrols: list | None = None) -> dict:
    return {
        "courses": [course_svc.enrolment_row(e) for e in (enrols or [])],
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
        "terms_price": getattr(u, "terms_price", None),
        "ks3_year": getattr(u, "ks3_year", None),
        "notify_email": getattr(u, "notify_email", None),
        "help_plan": getattr(u, "help_plan", None),
        "help_until": u.help_until.isoformat() if getattr(u, "help_until", None) else None,
        "sg_level": getattr(u, "sg_level", None),
        "billing_currency": pricing.for_currency(getattr(u, "billing_currency", None))["currency"],
        "subscription_label": pricing.for_currency(getattr(u, "billing_currency", None))["label"],
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
    by_user: dict[int, list] = {}
    for e in (await db.execute(select(Enrolment).order_by(Enrolment.created_at))).scalars().all():
        by_user.setdefault(e.user_id, []).append(e)
    return [_user_row(u, by_user.get(u.id)) for u in rows]


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
    currency: str = "GBP"      # billing currency for the £49-equivalent subscription
    courses: list[str] = []    # e.g. ["igcse-chemistry"]: the student can open these courses only


class AccessIn(BaseModel):
    access: str                # trial | year | none


class CurrencyIn(BaseModel):
    currency: str


@router.get("/prices")
async def list_prices(admin: User = Depends(require_admin)):
    return pricing.options()


@router.post("/users/{user_id}/currency")
async def set_currency(user_id: int, data: CurrencyIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    cur = data.currency.strip().upper()
    if cur not in pricing.prices():
        raise HTTPException(400, "Unknown currency")
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    u.billing_currency = cur
    await db.commit()
    return _user_row(u)


@router.get("/suggest-id")
async def suggest_id(name: str, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    return {"email": await _free_id(name, db)}


async def _free_id(name: str, db: AsyncSession, domain: str | None = None) -> str:
    """musa@beyondtutors.com, then musa.k@…, then musa2@… if taken."""
    domain = domain or settings.student_id_domain
    parts = [re.sub(r"[^a-z0-9]", "", p) for p in name.lower().split()]
    parts = [p for p in parts if p] or ["student"]
    first, last = parts[0], (parts[-1] if len(parts) > 1 else "")
    candidates = [first] + ([f"{first}.{last[0]}", f"{first}.{last}"] if last else [])
    candidates += [f"{first}{n}" for n in range(2, 100)]
    for c in candidates:
        email = f"{c}@{domain}"
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
        raise HTTPException(400, "User ID must look like name@beyondtutors.com")
    if (await db.execute(select(User.id).where(User.email == email))).first():
        raise HTTPException(400, f"{email} is already taken.")
    password = _new_password()
    u = User(email=email, full_name=name, role=data.role, password_hash=hash_password(password),
             is_verified=True, token_version=0, needs_activation=(data.role == "student"))
    if data.role == "student":
        _apply_access(u, data.access)
        cur = (data.currency or "GBP").strip().upper()
        u.billing_currency = cur if cur in pricing.prices() else "GBP"
    bad = [c for c in data.courses if not course_svc.is_course(c)]
    if bad:
        raise HTTPException(400, f"Unknown course: {', '.join(bad)}")
    db.add(u)
    await db.flush()
    if data.role == "student":
        for c in dict.fromkeys(data.courses):  # same access (trial / year / none) for each course
            await course_svc.grant(u, c, data.access, db)
    await db.commit()
    await db.refresh(u)
    return {"user": _user_row(u, await course_svc.enrolments(u.id, db)), "password": password}


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
    u.terms_price = None
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


# ── Courses (services/courses.py): which courses each student can open ───────

@router.get("/courses")
async def courses_catalogue(admin: User = Depends(require_admin)):
    return course_svc.catalogue()


class CourseIn(BaseModel):
    course: str
    access: str = "year"         # trial | year | none | until
    until: datetime | None = None


async def _student(user_id: int, db: AsyncSession) -> User:
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    if (u.role or "student") != "student" or is_admin(u):
        raise HTTPException(400, "Courses are for student accounts.")
    return u


@router.post("/users/{user_id}/courses")
async def add_course(user_id: int, data: CourseIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """Give a student a course (or extend it). Their first course switches them from
    'everything' to 'their courses only'."""
    u = await _student(user_id, db)
    try:
        await course_svc.grant(u, data.course, data.access, db, until=data.until)
    except ValueError as ex:
        raise HTTPException(400, str(ex))
    await db.commit()
    return _user_row(u, await course_svc.enrolments(u.id, db))


@router.delete("/users/{user_id}/courses/{course}")
async def remove_course(user_id: int, course: str, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    u = await _student(user_id, db)
    await course_svc.revoke(u, course, db)
    await db.commit()
    return _user_row(u, await course_svc.enrolments(u.id, db))


@router.get("/courses/suggestions")
async def course_suggestions(admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """Students who still open everything (no courses yet), with the courses their tutors'
    tests suggest, so the admin can move them over in one go."""
    have = {uid for (uid,) in (await db.execute(select(Enrolment.user_id).distinct())).all()}
    students = [u for u in (await db.execute(select(User).where(User.role == "student")
                                             .order_by(User.full_name))).scalars().all()
                if u.id not in have and not is_admin(u) and not getattr(u, "ks3_year", None)]
    seen: dict[int, dict[str, int]] = {}
    if students:
        rows = (await db.execute(
            select(TestAssignment.student_id, Test.level, Test.subject, Test.exam_board)
            .join(Test, Test.id == TestAssignment.test_id)
            .where(TestAssignment.student_id.in_([u.id for u in students]),
                   TestAssignment.class_label.is_distinct_from("Self-practice")))).all()
        for sid, level, subject, board in rows:
            c = course_svc.content_course(level, subject, board)
            if c and not c.endswith("-*"):
                seen.setdefault(sid, {})[c] = seen.setdefault(sid, {}).get(c, 0) + 1
    return [{
        "user_id": u.id, "full_name": u.full_name, "email": u.email,
        "access_kind": u.access_kind, "access_until": u.access_until.isoformat() if u.access_until else None,
        "suggested": [{"course": c, "name": course_svc.course_name(c), "tests": n}
                      for c, n in sorted(seen.get(u.id, {}).items(), key=lambda kv: -kv[1])],
    } for u in students]


class ApplyItem(BaseModel):
    user_id: int
    courses: list[str]


class ApplyIn(BaseModel):
    items: list[ApplyItem]


@router.post("/courses/apply")
async def apply_courses(data: ApplyIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """Move students onto courses, keeping their current end date (and trial/paid status)."""
    done = 0
    for item in data.items:
        u = await _student(item.user_id, db)
        for c in dict.fromkeys(item.courses):
            if not course_svc.is_course(c):
                raise HTTPException(400, f"Unknown course: {c}")
            until, kind = u.access_until, u.access_kind
            e = await course_svc.grant(u, c, "until" if until else "none", db, until=until)
            if kind == "trial":
                e.kind = "trial"
            done += 1
        course_svc.sync_access(u, await course_svc.enrolments(u.id, db))
    await db.commit()
    return {"added": done}

