from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from database import get_db
from models import User
from security import (
    hash_password, verify_password, create_token, get_current_user, is_admin,
    can_write_practice, ai_marks_for,
)
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


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class ResetPasswordIn(BaseModel):
    email: EmailStr
    code: str
    new_password: str


def _name_change_available_at(u: User) -> str | None:
    """ISO timestamp when the user may next change their name, or None if allowed now."""
    changed = getattr(u, "name_changed_at", None)
    if not changed:
        return None
    nxt = changed + timedelta(days=settings.name_change_cooldown_days)
    return nxt.isoformat() if datetime.utcnow() < nxt else None


def _user_dict(u: User) -> dict:
    role = getattr(u, "role", None) or "student"
    return {
        "id": u.id, "email": u.email, "full_name": u.full_name,
        "role": role,
        "name_change_available_at": _name_change_available_at(u),
        "is_admin": is_admin(u),
        "is_active": getattr(u, "is_active", True),
        "is_verified": getattr(u, "is_verified", True),
        "can_write": getattr(u, "can_write", False),
        "can_write_practice": can_write_practice(u),  # may access written practice
        "ai_marking": ai_marks_for(u),                # Pro → instant AI marking
        "can_mark": role in ("teacher", "admin") or is_admin(u),  # may manually mark
        "plan": u.plan, "xp": u.xp, "streak": u.streak, "quiz_count": u.quiz_count,
    }


async def _issue_otp(user: User, db: AsyncSession, kind: str = "verify") -> str:
    """Generate a fresh OTP, persist its hash + expiry, reset attempts, and email it.
    kind = 'verify' (signup) | 'reset' (forgot password).
    Raises HTTP 502 if a configured email provider rejects the message."""
    code = generate_otp()
    user.otp_hash = hash_password(code)
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=settings.otp_expiry_minutes)
    user.otp_attempts = 0
    await db.commit()
    try:
        await send_otp_email(user.email, user.full_name, code, kind=kind)
    except EmailSendError:
        raise HTTPException(502, EMAIL_FAIL_MSG)
    return code


def _within_cooldown(user: User) -> bool:
    """True if a code was issued too recently (used to rate-limit sends)."""
    if not user.otp_expires_at:
        return False
    last_sent = user.otp_expires_at - timedelta(minutes=settings.otp_expiry_minutes)
    return (datetime.utcnow() - last_sent).total_seconds() < settings.otp_resend_cooldown_seconds


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


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordIn, db: AsyncSession = Depends(get_db)):
    """Email a password-reset code. Always returns the same response whether or not the
    account exists, to avoid revealing which emails are registered."""
    email = data.email.lower()
    generic = {"status": "reset_sent", "email": email}
    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if not user:
        return generic
    if _within_cooldown(user):
        return generic  # silently rate-limit; don't reveal the account exists
    try:
        code = await _issue_otp(user, db, kind="reset")
    except HTTPException:
        return generic  # email provider hiccup — stay generic, code is logged server-side
    if settings.dev_expose_otp:  # DEV ONLY
        generic["dev_otp"] = code
    return generic


@router.post("/reset-password")
async def reset_password(data: ResetPasswordIn, db: AsyncSession = Depends(get_db)):
    """Verify the reset code and set a new password; logs the user in on success."""
    if len(data.new_password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    user = (await db.execute(select(User).where(User.email == data.email.lower()))).scalar_one_or_none()
    if not user or not user.otp_hash or not user.otp_expires_at:
        raise HTTPException(400, "No reset request found. Please request a new code.")
    if datetime.utcnow() > user.otp_expires_at:
        raise HTTPException(400, "This code has expired. Please request a new one.")
    if (user.otp_attempts or 0) >= settings.otp_max_attempts:
        raise HTTPException(429, "Too many incorrect attempts. Please request a new code.")
    if not verify_password(data.code.strip(), user.otp_hash):
        user.otp_attempts = (user.otp_attempts or 0) + 1
        await db.commit()
        raise HTTPException(400, "Incorrect code. Please try again.")

    user.password_hash = hash_password(data.new_password)
    user.otp_hash = None
    user.otp_expires_at = None
    user.otp_attempts = 0
    user.is_verified = True  # a successful reset also proves email ownership
    user.last_active = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    return {"access_token": create_token(user.id), "token_type": "bearer", "user": _user_dict(user)}


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


class UpdateProfileIn(BaseModel):
    full_name: str


@router.patch("/profile")
async def update_profile(data: UpdateProfileIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Change the display name — allowed once per `name_change_cooldown_days`."""
    name = (data.full_name or "").strip()[:120]
    if len(name) < 2:
        raise HTTPException(400, "Please enter a name with at least 2 characters.")
    if name == user.full_name:
        return _user_dict(user)  # no change — don't consume the cooldown
    changed = getattr(user, "name_changed_at", None)
    if changed:
        nxt = changed + timedelta(days=settings.name_change_cooldown_days)
        if datetime.utcnow() < nxt:
            raise HTTPException(429, f"You can change your name again on {nxt.strftime('%d %b %Y')}.")
    user.full_name = name
    user.name_changed_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    return _user_dict(user)
