from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from database import get_db
from models import User
from security import hash_password, verify_password, create_token, get_current_user, is_admin
from services.email import generate_otp, send_otp_email, EmailSendError
from config import settings

EMAIL_FAIL_MSG = "We couldn't send the verification email right now. Please try again in a moment."

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str | None = None  # student | teacher


class VerifyOtpIn(BaseModel):
    email: EmailStr
    code: str


class ResendOtpIn(BaseModel):
    email: EmailStr


def _user_dict(u: User) -> dict:
    return {
        "id": u.id, "email": u.email, "full_name": u.full_name,
        "role": getattr(u, "role", None) or "student",
        "is_admin": is_admin(u),
        "is_active": getattr(u, "is_active", True),
        "is_verified": getattr(u, "is_verified", True),
        "plan": u.plan, "xp": u.xp, "streak": u.streak, "quiz_count": u.quiz_count,
    }


async def _issue_otp(user: User, db: AsyncSession) -> str:
    """Generate a fresh OTP, persist its hash + expiry, reset attempts, and email it.
    Raises HTTP 502 if a configured email provider rejects the message."""
    code = generate_otp()
    user.otp_hash = hash_password(code)
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=settings.otp_expiry_minutes)
    user.otp_attempts = 0
    await db.commit()
    try:
        await send_otp_email(user.email, user.full_name, code)
    except EmailSendError:
        raise HTTPException(502, EMAIL_FAIL_MSG)
    return code


def _otp_sent_response(email: str, code: str) -> dict:
    resp = {"status": "otp_sent", "email": email}
    if settings.dev_expose_otp:  # DEV ONLY — never enabled in production
        resp["dev_otp"] = code
    return resp


@router.post("/register")
async def register(data: RegisterIn, db: AsyncSession = Depends(get_db)):
    if len(data.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    email = data.email.lower()
    existing = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if existing:
        if getattr(existing, "is_verified", True):
            raise HTTPException(400, "An account with this email already exists")
        # Unverified account — let them resume by resending a fresh code.
        code = await _issue_otp(existing, db)
        return _otp_sent_response(email, code)

    role = data.role if data.role in ("student", "teacher") else "student"
    user = User(
        email=email,
        password_hash=hash_password(data.password),
        full_name=data.full_name.strip()[:120],
        role=role,
        is_verified=False,
        last_active=datetime.utcnow(),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    code = await _issue_otp(user, db)
    return _otp_sent_response(email, code)


@router.post("/verify-otp")
async def verify_otp(data: VerifyOtpIn, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == data.email.lower()))).scalar_one_or_none()
    if not user:
        raise HTTPException(404, "No account found for this email")
    if getattr(user, "is_verified", True):
        # Already verified — just log them in.
        return {"access_token": create_token(user.id), "token_type": "bearer", "user": _user_dict(user)}
    if not user.otp_hash or not user.otp_expires_at:
        raise HTTPException(400, "No verification code pending. Please request a new one.")
    if datetime.utcnow() > user.otp_expires_at:
        raise HTTPException(400, "This code has expired. Please request a new one.")
    if (user.otp_attempts or 0) >= settings.otp_max_attempts:
        raise HTTPException(429, "Too many incorrect attempts. Please request a new code.")

    if not verify_password(data.code.strip(), user.otp_hash):
        user.otp_attempts = (user.otp_attempts or 0) + 1
        await db.commit()
        raise HTTPException(400, "Incorrect code. Please try again.")

    user.is_verified = True
    user.otp_hash = None
    user.otp_expires_at = None
    user.otp_attempts = 0
    user.last_active = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    return {"access_token": create_token(user.id), "token_type": "bearer", "user": _user_dict(user)}


@router.post("/resend-otp")
async def resend_otp(data: ResendOtpIn, db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == data.email.lower()))).scalar_one_or_none()
    if not user:
        raise HTTPException(404, "No account found for this email")
    if getattr(user, "is_verified", True):
        raise HTTPException(400, "This account is already verified. Please sign in.")
    # Cooldown: derive the last-send time from the stored expiry.
    if user.otp_expires_at:
        last_sent = user.otp_expires_at - timedelta(minutes=settings.otp_expiry_minutes)
        elapsed = (datetime.utcnow() - last_sent).total_seconds()
        if elapsed < settings.otp_resend_cooldown_seconds:
            wait = int(settings.otp_resend_cooldown_seconds - elapsed)
            raise HTTPException(429, f"Please wait {wait}s before requesting another code.")
    code = await _issue_otp(user, db)
    return _otp_sent_response(data.email.lower(), code)


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == form.username.lower()))).scalar_one_or_none()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Incorrect email or password")
    if getattr(user, "is_active", True) is False:
        raise HTTPException(403, "Your account has been suspended. Please contact support.")
    if getattr(user, "is_verified", True) is False:
        raise HTTPException(403, "Please verify your email before signing in.")
    user.last_active = datetime.utcnow()
    await db.commit()
    return {"access_token": create_token(user.id), "token_type": "bearer", "user": _user_dict(user)}


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    return _user_dict(user)
