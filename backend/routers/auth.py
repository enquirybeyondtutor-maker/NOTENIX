import re
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from database import get_db
from models import User
from security import (
    hash_password, verify_password, password_needs_rehash, create_token, get_current_user, is_admin,
    can_write_practice, ai_marks_for, access_ended_message,
)
from services.email import (login_domains, generate_otp, send_otp_email, EmailSendError, best_address, student_inbox,
                            is_mailbox, in_background, send_update_email_confirmed)
from config import settings

CLOSED_MSG = "Notenix accounts are issued by Beyond Tutors. Please contact your tutor or hello@thebeyondtutors.com."


def _require_open_signup():
    if not settings.open_signup:
        raise HTTPException(403, CLOSED_MSG)


EMAIL_FAIL_MSG = "We couldn't send the verification email right now. Please try again in a moment."

from services import pricing
from services import doubt

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
        "access_until": u.access_until.isoformat() if getattr(u, "access_until", None) else None,
        "access_kind": getattr(u, "access_kind", None),
        "needs_activation": bool(getattr(u, "needs_activation", False)),
        "parent_email": getattr(u, "parent_email", None),
        "subscription": pricing.for_currency(getattr(u, "billing_currency", None)),
        "ks3_year": getattr(u, "ks3_year", None),
        "notify_email": getattr(u, "notify_email", None),
        "help_plan": getattr(u, "help_plan", None) if doubt.live(u) else None,
        "help_until": u.help_until.isoformat() if getattr(u, "help_until", None) else None,
        "sg_level": getattr(u, "sg_level", None),
        # Show the "get homework by email" prompt: a student with no inbox of their own on file.
        "ask_notify_email": role == "student" and not student_inbox(u),
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
    # Notenix login IDs have no inbox: send the code to the student's real email or the parent's.
    to = best_address(user) or user.email
    try:
        await send_otp_email(to, user.full_name, code, kind=kind)
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
    _require_open_signup()
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

    role = "student"  # self-sign-up is students only; tutor accounts are created by admins
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
        return {"access_token": create_token(user.id, user.token_version or 0), "token_type": "bearer", "user": _user_dict(user)}
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
    return {"access_token": create_token(user.id, user.token_version or 0), "token_type": "bearer", "user": _user_dict(user)}


@router.post("/resend-otp")
async def resend_otp(data: ResendOtpIn, db: AsyncSession = Depends(get_db)):
    _require_open_signup()
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
    _require_open_signup()
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
    _require_open_signup()
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
    return {"access_token": create_token(user.id, user.token_version or 0), "token_type": "bearer", "user": _user_dict(user)}


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = (await db.execute(select(User).where(User.email == form.username.lower()))).scalar_one_or_none()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Incorrect user ID or password")
    if getattr(user, "is_active", True) is False:
        raise HTTPException(403, "Your account has been suspended. Please contact support.")
    if getattr(user, "is_verified", True) is False:
        raise HTTPException(403, "Please verify your email before signing in.")
    ended = access_ended_message(user)
    if ended:
        raise HTTPException(403, ended)
    if (user.role or "student") == "student" and not is_admin(user):
        # One active sign-in per student: this login signs out any other device.
        user.token_version = (user.token_version or 0) + 1
    if password_needs_rehash(user.password_hash):
        user.password_hash = hash_password(form.password)  # faster checks from next sign-in
    user.last_active = datetime.utcnow()
    await db.commit()
    return {"access_token": create_token(user.id, user.token_version or 0), "token_type": "bearer", "user": _user_dict(user)}


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


# ── Parent activation ──────────────────────────────────────────────────────────
# A Beyond Tutors-issued student account starts with needs_activation=True. The parent
# signs in with the issued ID + temporary password, enters their own email and phone,
# then confirms the 6-digit code emailed to them and sets a new password. Until then
# every other API call is refused (see security.get_current_user).

class ActivationStartIn(BaseModel):
    parent_email: EmailStr
    phone: str
    agree_terms: bool = False


class ActivationVerifyIn(BaseModel):
    code: str
    new_password: str


def _clean_phone(raw: str) -> str:
    digits = re.sub(r"\D", "", raw or "")
    if not 8 <= len(digits) <= 15:
        raise HTTPException(400, "Please enter a valid mobile number with country code, e.g. +44 7700 900123.")
    return "+" + digits


@router.post("/activation/send-code")
async def activation_send_code(data: ActivationStartIn, user: User = Depends(get_current_user),
                               db: AsyncSession = Depends(get_db)):
    if not getattr(user, "needs_activation", False):
        raise HTTPException(400, "This account is already activated.")
    if not data.agree_terms:
        raise HTTPException(400, "Please agree to the Terms and Conditions to continue.")
    email = data.parent_email.lower()
    if email.rsplit("@", 1)[-1] in login_domains():
        raise HTTPException(400, "Please enter your own email address, not the Notenix user ID.")
    phone = _clean_phone(data.phone)
    if _within_cooldown(user):
        raise HTTPException(429, "Please wait a minute before asking for another code.")
    user.parent_email, user.parent_phone = email, phone
    user.terms_accepted_at = datetime.utcnow()
    user.terms_price = pricing.for_currency(user.billing_currency)["label"] + " per year"
    code = generate_otp()
    user.otp_hash = hash_password(code)
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=settings.otp_expiry_minutes)
    user.otp_attempts = 0
    await db.commit()
    try:
        await send_otp_email(email, user.full_name, code, kind="activate")
    except EmailSendError:
        raise HTTPException(502, EMAIL_FAIL_MSG)
    return _otp_sent_response(email, code)


@router.post("/activation/verify")
async def activation_verify(data: ActivationVerifyIn, user: User = Depends(get_current_user),
                            db: AsyncSession = Depends(get_db)):
    if not getattr(user, "needs_activation", False):
        raise HTTPException(400, "This account is already activated.")
    if len(data.new_password) < 8:
        raise HTTPException(400, "Your new password must be at least 8 characters.")
    if not user.otp_hash or not user.otp_expires_at or not user.parent_email:
        raise HTTPException(400, "Please ask for a code first.")
    if datetime.utcnow() > user.otp_expires_at:
        raise HTTPException(400, "That code has expired. Please ask for a new one.")
    if (user.otp_attempts or 0) >= settings.otp_max_attempts:
        raise HTTPException(429, "Too many wrong codes. Please ask for a new one.")
    if not verify_password(data.code.strip(), user.otp_hash):
        user.otp_attempts = (user.otp_attempts or 0) + 1
        await db.commit()
        raise HTTPException(400, "That code isn't right. Please check the email and try again.")
    user.password_hash = hash_password(data.new_password)
    user.needs_activation = False
    user.activated_at = datetime.utcnow()
    user.otp_hash, user.otp_expires_at, user.otp_attempts = None, None, 0
    user.token_version = (user.token_version or 0) + 1  # sessions on the WhatsApp password end here
    user.last_active = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    return {"access_token": create_token(user.id, user.token_version or 0), "token_type": "bearer", "user": _user_dict(user)}



class NotifyEmailIn(BaseModel):
    email: str | None = None   # empty / None turns the emails off


@router.put("/notify-email")
async def set_notify_email(data: NotifyEmailIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """The student's own inbox for homework and class-notes updates."""
    email = (data.email or "").strip().lower()
    if not email:
        user.notify_email, user.notify_email_at = None, None
        await db.commit()
        return _user_dict(user)
    if not re.fullmatch(r"[^@\s]{1,64}@[^@\s]{1,190}\.[a-z]{2,}", email):
        raise HTTPException(400, "That doesn't look like an email address.")
    if not is_mailbox(email):
        raise HTTPException(400, "Please enter your own email (Gmail, Outlook, school email...), not your Notenix user ID.")
    changed = email != (user.notify_email or "")
    user.notify_email, user.notify_email_at = email, datetime.utcnow()
    await db.commit()
    if changed:
        in_background(send_update_email_confirmed(user, email))
    return _user_dict(user)
