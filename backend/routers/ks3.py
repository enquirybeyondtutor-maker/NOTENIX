"""Notenix KS3 free trial: a parent signs a child up on /ks3/trial with an emailed code.

Only this trial form is public; normal sign-up stays off. One free trial per parent email.
"""
import hashlib
import hmac
import re
import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from database import get_db
from models import User, Test, TestAssignment
from security import hash_password, verify_password, create_token, require_admin
from services import ks3
from services.ks3_content import share_year_notes
from services.email import generate_otp, send_otp_email, EmailSendError
from routers.admin import _free_id
from routers.auth import _user_dict, _within_cooldown, _otp_sent_response, EMAIL_FAIL_MSG

router = APIRouter(prefix="/ks3", tags=["ks3"])


class TrialStartIn(BaseModel):
    child_name: str
    year_group: int
    parent_email: EmailStr
    agree_terms: bool = False
    source: str | None = None  # landing page, e.g. "kent-grammar"


class TrialVerifyIn(BaseModel):
    parent_email: EmailStr
    code: str


class TrialCompleteIn(BaseModel):
    parent_email: EmailStr
    setup_token: str
    password: str


SETUP_MINUTES = 30


async def _pending(email: str, db: AsyncSession) -> User:
    u = (await db.execute(select(User).where(
        User.parent_email == email.lower(), User.ks3_year.isnot(None), User.needs_activation == True,  # noqa: E712
    ).order_by(User.id.desc()))).scalars().first()
    if not u or not u.otp_hash or not u.otp_expires_at:
        raise HTTPException(400, "Please ask for a code first.")
    if datetime.utcnow() > u.otp_expires_at:
        raise HTTPException(400, "That has expired. Please start again and ask for a new code.")
    if (u.otp_attempts or 0) >= settings.otp_max_attempts:
        raise HTTPException(429, "Too many wrong attempts. Please ask for a new code.")
    return u


@router.post("/trial/start")
async def trial_start(data: TrialStartIn, db: AsyncSession = Depends(get_db)):
    name = re.sub(r"\s+", " ", data.child_name).strip()[:120]
    if len(name) < 2:
        raise HTTPException(400, "Please enter your child's name.")
    if data.year_group not in (6, 7, 8, 9):
        raise HTTPException(400, "Notenix KS3 is for Years 7, 8 and 9 (or Year 6 starting Year 7 next September).")
    if not data.agree_terms:
        raise HTTPException(400, "Please agree to the Terms and Privacy policy to continue.")
    email = data.parent_email.lower()
    if email.endswith("@" + settings.student_id_domain.lower()) or email.endswith("@" + settings.ks3_id_domain.lower()):
        raise HTTPException(400, "Please enter your own email address.")
    family = (await db.execute(select(User).where(
        User.parent_email == email, User.ks3_year.isnot(None)).order_by(User.id.desc()))).scalars().all()
    if any(u.ks3_trial_started_at for u in family):
        raise HTTPException(400, "This email has already had a free trial. Sign in at notenix.com, "
                                 "or reply to any of our emails to continue.")
    u = next((x for x in family if x.needs_activation), None)
    if u and _within_cooldown(u):
        raise HTTPException(429, "Please wait a minute before asking for another code.")
    if not u:
        u = User(email=await _free_id(name, db, domain=settings.ks3_id_domain), full_name=name, role="student",
                 is_verified=True, password_hash="!", needs_activation=True,  # no password until the parent picks one
                 parent_email=email, token_version=0)
        db.add(u)
    u.full_name, u.ks3_year = name, max(7, data.year_group)  # Year 6 works on Year 7 content
    ks3.year_set_now(u, starting_next=data.year_group == 6)
    if data.source == "kent-grammar":
        u.ks3_emails = sorted(set(u.ks3_emails or []) | {"src-kent-grammar"})
    code = generate_otp()
    u.otp_hash = hash_password(code)
    u.otp_expires_at = datetime.utcnow() + timedelta(minutes=settings.otp_expiry_minutes)
    u.otp_attempts = 0
    await db.commit()
    try:
        await send_otp_email(email, name, code, kind="ks3")
    except EmailSendError:
        raise HTTPException(502, EMAIL_FAIL_MSG)
    return _otp_sent_response(email, code)


@router.post("/trial/verify")
async def trial_verify(data: TrialVerifyIn, db: AsyncSession = Depends(get_db)):
    """Step 2: the emailed code is right → show the issued @notenix.com user ID and let the
    parent choose the password (step 3) with a short-lived setup token."""
    u = await _pending(data.parent_email, db)
    if not verify_password(data.code.strip(), u.otp_hash):
        u.otp_attempts = (u.otp_attempts or 0) + 1
        await db.commit()
        raise HTTPException(400, "That code isn't right. Please check the email and try again.")
    token = secrets.token_urlsafe(24)
    # A long random token, so a fast SHA-256 is enough (bcrypt is for short, guessable secrets).
    u.otp_hash = "sha256$" + hashlib.sha256(token.encode()).hexdigest()  # the 6-digit code is now spent
    u.otp_expires_at = datetime.utcnow() + timedelta(minutes=SETUP_MINUTES)
    u.otp_attempts = 0
    await db.commit()
    return {"login_id": u.email, "setup_token": token, "child_name": u.full_name}


@router.post("/trial/complete")
async def trial_complete(data: TrialCompleteIn, db: AsyncSession = Depends(get_db)):
    """Step 3: the parent's chosen password → account opens and the trial week starts."""
    if len(data.password) < 8:
        raise HTTPException(400, "Please choose a password of at least 8 characters.")
    u = await _pending(data.parent_email, db)
    want = "sha256$" + hashlib.sha256(data.setup_token.encode()).hexdigest()
    if not hmac.compare_digest(want, u.otp_hash or ""):
        u.otp_attempts = (u.otp_attempts or 0) + 1
        await db.commit()
        raise HTTPException(400, "This sign-up link has expired. Please start again.")
    now = datetime.utcnow()
    u.password_hash = hash_password(data.password)
    u.needs_activation = False
    u.activated_at = u.terms_accepted_at = u.ks3_trial_started_at = u.last_active = now
    u.otp_hash, u.otp_expires_at, u.otp_attempts = None, None, 0
    u.access_kind, u.access_until = "trial", now + timedelta(days=settings.ks3_trial_days)
    u.terms_price = f"Free {settings.ks3_trial_days}-day KS3 trial"
    u.token_version = (u.token_version or 0) + 1
    u.ks3_emails = sorted(set((u.ks3_emails or []) + ["welcome"]))
    await db.flush()  # one UPDATE for all of the above
    await ks3.assign_due_tests(db, u)  # this year's baseline tests
    await db.flush()
    await share_year_notes(db, u)  # this year's KS3 notes
    welcome = ks3.welcome(u, {})  # the welcome email needs no results, so no extra query
    await db.commit()
    ks3.deliver_later(u.parent_email, *welcome)  # don't make the parent wait for the email service
    return {"access_token": create_token(u.id, u.token_version), "token_type": "bearer",
            "user": _user_dict(u), "login_id": u.email}


@router.get("/admin/preview/{user_id}/{kind}", response_class=HTMLResponse)
async def preview_email(user_id: int, kind: str, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """See a trial email exactly as the parent would, with this student's real data."""
    if kind not in ks3.BUILDERS:
        raise HTTPException(404, "Unknown email")
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, "User not found")
    subject, html, _ = await ks3.render(db, u, kind)
    return HTMLResponse(f"<p style='font:13px system-ui;color:#64748b;text-align:center'>Subject: <b>{subject}</b></p>{html}")


class Ks3AdminIn(BaseModel):
    year: int | None = None   # 7, 8, 9, or None to switch KS3 off


@router.post("/admin/users/{user_id}")
async def admin_set_ks3(user_id: int, data: Ks3AdminIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """Add Notenix KS3 to a student (e.g. a Beyond Tutors family) or switch it off."""
    if data.year not in (None, 7, 8, 9):
        raise HTTPException(400, "Year must be 7, 8 or 9.")
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u or (u.role or "student") != "student":
        raise HTTPException(404, "Student not found")
    u.ks3_year = data.year
    ks3.year_set_now(u)
    assigned = 0
    if data.year:
        await share_year_notes(db, u)
        assigned = await ks3.assign_due_tests(db, u)
    await db.commit()
    return {"ks3_year": u.ks3_year, "tests_assigned": assigned}
