from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config import settings
from database import get_db
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

ALGORITHM = "HS256"


def hash_password(p: str) -> str:
    return pwd_context.hash(p)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": str(user_id), "exp": expire}, settings.secret_key, algorithm=ALGORITHM)


async def get_current_user(
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
    except (JWTError, TypeError, ValueError):
        raise creds_exc
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user is None:
        raise creds_exc
    if getattr(user, "is_active", True) is False:
        raise HTTPException(status_code=403, detail="Your account has been suspended. Contact support.")
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
