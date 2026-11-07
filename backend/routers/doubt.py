"""Doubt Help / Ask a Tutor: free trial sign-up, monthly checkout and the admin switch.
The questions themselves go through routers/help.py. Plans and emails: services/doubt.py."""
import hashlib
import hmac
import re
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from database import get_db
from models import User, Payment
from security import hash_password, verify_password, create_token, require_admin
from services import doubt
from services.email import (generate_otp, send_otp_email, EmailSendError, notify_admins, in_background,
                            _deliver, is_mailbox)
from routers.admin import _free_id
from routers.auth import _user_dict, _within_cooldown, _otp_sent_response, EMAIL_FAIL_MSG

router = APIRouter(prefix="/doubt", tags=["doubt"])


@router.get("/plans")
async def plans(currency: str = "SGD"):
    return {"levels": list(doubt.LEVELS),
            "plans": [{**doubt.price(p, currency), "name": doubt.PLANS[p]["name"], "cap": doubt.PLANS[p]["cap"],
                       "days": doubt.PLANS[p]["days"], "calls": doubt.PLANS[p].get("calls", 0)} for p in ("annual", "doubt", "plus")],
            "trial": {"cap": doubt.PLANS["trial"]["cap"], "days": doubt.PLANS["trial"]["days"]}}


# ── Free trial sign-up (parent email code → @notenix.com ID → parent's password) ─

class StartIn(BaseModel):
    child_name: str
    level: str
    parent_email: EmailStr
    agree_terms: bool = False


class VerifyIn(BaseModel):
    parent_email: EmailStr
    code: str


class CompleteIn(BaseModel):
    parent_email: EmailStr
    setup_token: str
    password: str


async def _pending(email: str, db: AsyncSession) -> User:
    u = (await db.execute(select(User).where(
        User.parent_email == email.lower(), User.help_plan == "pending", User.needs_activation == True,  # noqa: E712
    ).order_by(User.id.desc()))).scalars().first()
    if not u or not u.otp_hash or not u.otp_expires_at:
        raise HTTPException(400, "Please ask for a code first.")
    if datetime.utcnow() > u.otp_expires_at:
        raise HTTPException(400, "That has expired. Please start again and ask for a new code.")
    if (u.otp_attempts or 0) >= settings.otp_max_attempts:
        raise HTTPException(429, "Too many wrong attempts. Please ask for a new code.")
    return u


@router.post("/trial/start")
async def trial_start(data: StartIn, db: AsyncSession = Depends(get_db)):
    name = re.sub(r"\s+", " ", data.child_name).strip()[:120]
    if len(name) < 2:
        raise HTTPException(400, "Please enter your child's name.")
    if data.level not in doubt.LEVELS:
        raise HTTPException(400, "Please choose your child's level.")
    if not data.agree_terms:
        raise HTTPException(400, "Please agree to the Terms and Privacy policy to continue.")
    email = data.parent_email.lower()
    if not is_mailbox(email):
        raise HTTPException(400, "Please enter your own email address.")
    family = (await db.execute(select(User).where(User.parent_email == email, User.sg_level.isnot(None))
                               .order_by(User.id.desc()))).scalars().all()
    if any(u.help_plan and u.help_plan != "pending" or not u.needs_activation for u in family):
        raise HTTPException(400, "This email has already had a free trial. Sign in at notenix.com, or choose a plan at "
                                 "notenix.com/ask-a-tutor/continue.")
    u = next((x for x in family if x.help_plan == "pending"), None)
    if u and _within_cooldown(u):
        raise HTTPException(429, "Please wait a minute before asking for another code.")
    if not u:
        u = User(email=await _free_id(name, db, domain=settings.ks3_id_domain), full_name=name, role="student",
                 is_verified=True, password_hash="!", needs_activation=True, parent_email=email, token_version=0,
                 help_plan="pending", billing_currency="SGD")
        db.add(u)
    u.full_name, u.sg_level = name, data.level
    code = generate_otp()
    u.otp_hash = hash_password(code)
    u.otp_expires_at = datetime.utcnow() + timedelta(minutes=settings.otp_expiry_minutes)
    u.otp_attempts = 0
    await db.commit()
    try:
        await send_otp_email(email, name, code, kind="doubt")
    except EmailSendError:
        raise HTTPException(502, EMAIL_FAIL_MSG)
    return _otp_sent_response(email, code)


@router.post("/trial/verify")
async def trial_verify(data: VerifyIn, db: AsyncSession = Depends(get_db)):
    u = await _pending(data.parent_email, db)
    if not verify_password(data.code.strip(), u.otp_hash):
        u.otp_attempts = (u.otp_attempts or 0) + 1
        await db.commit()
        raise HTTPException(400, "That code isn't right. Please check the email and try again.")
    import secrets
    token = secrets.token_urlsafe(24)
    u.otp_hash = "sha256$" + hashlib.sha256(token.encode()).hexdigest()
    u.otp_expires_at = datetime.utcnow() + timedelta(minutes=30)
    u.otp_attempts = 0
    await db.commit()
    return {"login_id": u.email, "setup_token": token, "child_name": u.full_name}


@router.post("/trial/complete")
async def trial_complete(data: CompleteIn, db: AsyncSession = Depends(get_db)):
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
    u.activated_at = u.terms_accepted_at = u.last_active = now
    u.otp_hash, u.otp_expires_at, u.otp_attempts = None, None, 0
    u.terms_price = "Free 7-day Ask a Tutor trial"
    u.help_plan = None
    u.access_kind, u.access_until = "trial", now  # a new Doubt-Help-only account: access follows the plan
    doubt.set_plan(u, "trial")
    u.help_emails = ["welcome"]
    u.token_version = (u.token_version or 0) + 1
    await db.commit()
    in_background(_deliver(u.parent_email, *doubt.welcome(u)))
    in_background(notify_admins(f"New Ask a Tutor trial: {u.full_name}", f"{u.full_name} ({u.sg_level}) started a free trial.",
                                "/admin", rows=[("Student", f"{u.full_name} ({u.sg_level})"), ("Login", u.email),
                                                ("Parent", u.parent_email)]))
    return {"access_token": create_token(u.id, u.token_version), "token_type": "bearer",
            "user": _user_dict(u), "login_id": u.email}


# ── Monthly checkout (bank transfer / Wise, confirmed by an admin) ────────────────

class CheckoutIn(BaseModel):
    login_id: str
    password: str
    plan: str = "annual"
    currency: str = "SGD"
    paid_via: str | None = None
    payer_name: str | None = None
    payer_note: str | None = None


@router.get("/checkout")
async def checkout_info():
    from routers.payments import payment_accounts
    return {"accounts": payment_accounts(), "prices": {p: doubt.PRICES[p] for p in ("annual", "doubt", "plus")},
            "plans": {p: {"name": doubt.PLANS[p]["name"], "cap": doubt.PLANS[p]["cap"], "days": doubt.PLANS[p]["days"],
                          "calls": doubt.PLANS[p].get("calls", 0)} for p in ("annual", "doubt", "plus")}}


@router.post("/checkout")
async def checkout(data: CheckoutIn, db: AsyncSession = Depends(get_db)):
    """Public on purpose: an ended trial is locked out of the app, so the child's login is confirmed here."""
    if data.plan not in ("annual", "doubt", "plus"):
        raise HTTPException(400, "Choose a plan.")
    user = (await db.execute(select(User).where(User.email == data.login_id.strip().lower()))).scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(400, "That Notenix user ID or password isn't right.")
    if not (data.payer_name or "").strip():
        raise HTTPException(400, "Please tell us the name of the person who paid.")
    pr = doubt.price(data.plan, data.currency)
    open_claim = (await db.execute(select(Payment).where(
        Payment.user_id == user.id, Payment.purpose.in_(("annual", "doubt", "plus")), Payment.status == "claimed"))).scalar_one_or_none()
    from routers.payments import _payment_row
    if open_claim:
        return _payment_row(open_claim)
    user.billing_currency = pr["currency"]
    p = Payment(user_id=user.id, purpose=data.plan, reference=f"NX-D{user.id}", amount=pr["amount"], currency=pr["currency"],
                paid_via=(data.paid_via or "")[:80] or None, payer_name=(data.payer_name or "")[:120] or None,
                payer_note=(data.payer_note or "")[:1000] or None)
    db.add(p)
    await db.commit()
    await db.refresh(p)
    await notify_admins(f"Payment to check: {p.reference}",
                        f"{user.full_name} says they paid {pr['label']} for {doubt.PLANS[data.plan]['name']}.",
                        "/admin/requests", rows=[("Student", f"{user.full_name} ({user.sg_level or user.email})"),
                                                 ("Plan", doubt.PLANS[data.plan]["name"]), ("Amount", pr["label"]),
                                                 ("Payer", p.payer_name or "-"), ("Note", p.payer_note or "-")])
    return _payment_row(p)


# ── Admin switch ────────────────────────────────────────────────────────────────

class AdminIn(BaseModel):
    plan: str | None = None      # None | trial | annual | doubt | plus
    level: str | None = None
    days: int | None = None


@router.post("/admin/users/{user_id}")
async def admin_set(user_id: int, data: AdminIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """Give a student Doubt Help (e.g. a Beyond Tutors family or a WhatsApp enquiry), extend it, or switch it off."""
    if data.plan not in (None, "trial", "annual", "doubt", "plus"):
        raise HTTPException(400, "Plan must be trial, annual, doubt or plus.")
    if data.level and data.level not in doubt.LEVELS:
        raise HTTPException(400, "Unknown level.")
    u = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if not u or (u.role or "student") != "student":
        raise HTTPException(404, "Student not found")
    if data.level:
        u.sg_level = data.level
    doubt.set_plan(u, data.plan, data.days)
    await db.commit()
    return {"help_plan": u.help_plan, "help_until": u.help_until.isoformat() if u.help_until else None, "sg_level": u.sg_level}
