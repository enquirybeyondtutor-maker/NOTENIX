"""Notenix TMUA Mock Series (January 2027): public info, enrol & pay, and the student's series view.
See services/tmua_series.py for how access and mock release work."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.payer import clean_dob, clean_country
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db
from models import User, Payment
from security import get_current_user, hash_password, verify_password
from services import tmua_series as series
from services.email import notify_admins

router = APIRouter(prefix="/series", tags=["series"])


def _pay_link(amount: int) -> str:
    """Wise card links are fixed-amount: one per price. No link for a price -> bank transfer only."""
    return {99: settings.pay_link_99, 109: getattr(settings, "pay_link_109", "")}.get(amount, "") or ""


@router.get("/tmua")
async def tmua_info():
    from routers.payments import payment_accounts
    info = series.public_info()
    info["accounts"] = payment_accounts()
    info["pay_link"] = _pay_link(info["price"]["amount"])
    return info


class EnrolIn(BaseModel):
    full_name: str
    email: str
    password: str
    paid_via: str | None = None
    payer_name: str | None = None
    payer_note: str | None = None
    payer_dob: str | None = None   # optional; helps match Wise payments
    payer_country: str | None = None   # payer's country of residence


@router.post("/tmua/enrol")
async def tmua_enrol(data: EnrolIn, db: AsyncSession = Depends(get_db)):
    """Enrol & pay in one step. A new account stays locked until the payment is confirmed."""
    email = data.email.strip().lower()
    if "@" not in email or "." not in email.split("@")[-1] or len(data.password) < 8 or not data.full_name.strip():
        raise HTTPException(400, "Enter your name, a valid email and a password of at least 8 characters.")
    if not (data.payer_name or "").strip():
        raise HTTPException(400, "Please tell us the name of the person who paid.")
    now = datetime.utcnow()
    if now >= series.ENDS:
        raise HTTPException(400, "Enrolment for the January 2027 series has closed.")
    user = (await db.execute(select(User).where(
        (User.email == email) | (User.notify_email == email)))).scalars().first()
    if user:
        # An existing Notenix account joins with its own password; its other access is left as it is.
        if not verify_password(data.password, user.password_hash):
            raise HTTPException(400, f"That email already has a Notenix account (user ID {user.email}). "
                                     "Enter that account's password to add the series to it.")
        if await series.is_member(user, db):
            raise HTTPException(400, "You're already enrolled on the TMUA Mock Series. Sign in to see your mocks.")
        if getattr(user, "access_kind", None) == "free":
            user.access_kind, user.access_until = "pending", now
    else:
        from routers.admin import _free_id
        login_id = await _free_id(data.full_name, db, domain=settings.ks3_id_domain)   # priya@notenix.com
        user = User(email=login_id, notify_email=email, full_name=data.full_name.strip()[:120],
                    password_hash=hash_password(data.password), role="student", is_verified=True)
        db.add(user)
        user.access_kind, user.access_until = "pending", now   # locked until the payment is confirmed
    await db.flush()
    open_claim = (await db.execute(select(Payment).where(
        Payment.user_id == user.id, Payment.course == series.KEY, Payment.status == "claimed"))).scalars().first()
    if open_claim:
        raise HTTPException(400, f"We already have your payment (reference {open_claim.reference}) and are checking it.")
    p_info = series.price(now)
    p = Payment(
        user_id=user.id, purpose="course", course=series.KEY, reference=f"NX-T{user.id}",
        amount=p_info["amount"], currency=p_info["currency"],
        paid_via=(data.paid_via or "")[:80] or None,
        payer_name=(data.payer_name or "")[:120] or None,
        payer_note=(data.payer_note or "")[:1000] or None, payer_dob=clean_dob(data.payer_dob), payer_country=clean_country(data.payer_country),
    )
    db.add(p)
    await db.commit()
    await db.refresh(p)
    await notify_admins(
        f"Payment to check: {p.reference} (TMUA Mock Series)",
        f"{user.full_name} (user ID {user.email}, email {user.notify_email or user.email}) enrolled on the "
        f"{series.NAME} and says they paid £{p.amount:g} via {p.paid_via or 'bank transfer'}. "
        f"Payer: {p.payer_name}. Note: {p.payer_note or '-'}",
        "/admin/requests",
    )
    return {"reference": p.reference, "amount": p.amount, "currency": p.currency, "login_id": user.email,
            "email": user.notify_email or user.email}


@router.get("/tmua/mine")
async def tmua_mine(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    member = await series.is_member(user, db)
    if member:
        await series.sync_assignments(user, db)
    used = await series.requests_this_week(user, db) if member else 0
    return {"member": member, **series.public_info(), "requests_left": max(0, series.REQUESTS_PER_WEEK - used)}
