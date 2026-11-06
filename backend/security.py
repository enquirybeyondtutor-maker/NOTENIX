from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config import settings
from database import get_db
from models import User

# 10 bcrypt rounds (passlib default is 12): ~4x faster sign-in on Render's free CPU.
# Still well above OWASP's minimum of 10. Older 12-round hashes keep working and are
# re-saved at 10 rounds the next time that user signs in (see password_needs_rehash).
BCRYPT_ROUNDS = 10
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=BCRYPT_ROUNDS)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

ALGORITHM = "HS256"


def hash_password(p: str) -> str:
    return pwd_context.hash(p)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(plain, hashed)
    except (ValueError, TypeError):  # "!" = no password set yet, or a malformed hash
        return False


def password_needs_rehash(hashed: str) -> bool:
    """True for bcrypt hashes made with a different cost, e.g. $2b$12$…"""
    try:
        return int(hashed.split("$")[2]) != BCRYPT_ROUNDS
    except (IndexError, ValueError, AttributeError):
        return False


def create_token(user_id: int, version: int = 0) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": str(user_id), "v": version, "exp": expire}, settings.secret_key, algorithm=ALGORITHM)


def is_free_account(user: User) -> bool:
    """A visitor who signed up through the free test-request form: they can sit the test
    we send them, but not use the paid revision library or request more tests."""
    return getattr(user, "access_kind", None) == "free" and _role(user) == "student" and not is_admin(user)


def access_ended_message(user: User) -> str | None:
    """Why a student can no longer use Notenix, or None while their access is live.
    Staff and accounts with no access_until are never blocked."""
    until = getattr(user, "access_until", None)
    if until is None or _role(user) != "student" or is_admin(user):
        return None
    if datetime.utcnow() <= until:
        return None
    if getattr(user, "access_kind", None) == "pending":
        return "We're confirming your payment. Your access will switch on as soon as it arrives, and we'll email you."
    if getattr(user, "ks3_year", None):
        what = "free week" if getattr(user, "access_kind", None) == "trial" else "Notenix KS3 year"
        return (f"Your {what} ended on {until.strftime('%d %b %Y')}. Continue Notenix KS3 at "
                f"notenix.com/ks3/continue: your results are saved.")
    what = "free trial" if getattr(user, "access_kind", None) == "trial" else "Notenix subscription"
    return f"Your {what} ended on {until.strftime('%d %b %Y')}. Please contact Beyond Tutors to renew."


# Paths a not-yet-activated student may still call (the activation screen itself).
_ACTIVATION_OK = ("/auth/me", "/auth/activation/send-code", "/auth/activation/verify")


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    creds_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        version = int(payload.get("v", 0))
    except (JWTError, TypeError, ValueError):
        raise creds_exc
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user is None or version != (getattr(user, "token_version", 0) or 0):
        # Older token: someone signed in elsewhere or the password was reset.
        raise creds_exc
    if getattr(user, "is_active", True) is False:
        raise HTTPException(status_code=403, detail="Your account has been suspended. Contact support.")
    ended = access_ended_message(user)
    if ended:
        raise HTTPException(status_code=403, detail=ended)
    if getattr(user, "needs_activation", False) and not request.url.path.rstrip("/").endswith(_ACTIVATION_OK):
        raise HTTPException(status_code=403, detail="activation_required")
    return user


def _admin_emails() -> set[str]:
    return {e.strip().lower() for e in (settings.admin_emails or "").split(",") if e.strip()}


def is_admin(user: User) -> bool:
    return (getattr(user, "role", None) == "admin") or (user.email.lower() in _admin_emails())


def _role(user: User) -> str:
    return getattr(user, "role", None) or "student"


async def require_teacher(user: User = Depends(get_current_user)) -> User:
    """Guard for teacher/admin-only endpoints."""
    if _role(user) not in ("teacher", "admin") and not is_admin(user):
        raise HTTPException(status_code=403, detail="Teacher access required")
    return user


async def require_admin(user: User = Depends(get_current_user)) -> User:
    """Guard for admin-only endpoints (role=admin or email in ADMIN_EMAILS)."""
    if not is_admin(user):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ── Written-answer practice gates ────────────────────────────────────────────

def can_write_practice(user: User) -> bool:
    """May access written-answer practice: Pro, admin-whitelisted, or teacher/admin."""
    return (
        getattr(user, "plan", "free") == "pro"
        or getattr(user, "can_write", False)
        or _role(user) in ("teacher", "admin")
        or is_admin(user)
    )


def ai_marks_for(user: User) -> bool:
    """Whether this user's written answers are AI-marked on submit. Pro only —
    everyone else is marked by hand by a teacher/admin."""
    return getattr(user, "plan", "free") == "pro"


def can_mark_written(user: User, test) -> bool:
    """May manually mark an attempt: admins mark anything; teachers mark tests they own."""
    return is_admin(user) or (_role(user) == "teacher" and getattr(test, "owner_id", None) == user.id)


async def require_write_practice(user: User = Depends(get_current_user)) -> User:
    """Guard for the student written-practice endpoints."""
    if not can_write_practice(user):
        raise HTTPException(status_code=403, detail="Written practice is available on Pro or by invitation.")
    return user
