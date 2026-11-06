"""Manual payments: students pay by bank transfer (Wise or a local account) and an admin
confirms the money arrived. Free to run: no payment gateway, no fees beyond the bank's."""
import json
from datetime import datetime, timedelta
from html import escape

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import settings
from database import get_db
from models import User, Payment, TestRequest
from security import get_current_user, require_admin, hash_password, verify_password
from services.email import send_payment_result, notify_admins

router = APIRouter(prefix="/payments", tags=["payments"])

PRO_DAYS = 30


def payment_accounts() -> list[dict]:
    try:
        accounts = json.loads(settings.payment_accounts or "[]")
        return [a for a in accounts if isinstance(a, dict) and a.get("details")]
    except json.JSONDecodeError:
        print("[payments] PAYMENT_ACCOUNTS is not valid JSON")
        return []


def reference_for(purpose: str, user_id: int, request_id: int | None = None) -> str:
    """Short code the payer adds to the transfer so it can be matched to them."""
    return f"NX-R{request_id}" if purpose == "test_request" and request_id else f"NX-P{user_id}"


def _payment_row(p: Payment, user: User | None = None) -> dict:
    row = {
        "id": p.id, "purpose": p.purpose, "request_id": p.request_id, "reference": p.reference,
        "amount": p.amount, "currency": p.currency, "paid_via": p.paid_via,
        "payer_name": p.payer_name, "payer_note": p.payer_note, "status": p.status,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "reviewed_at": p.reviewed_at.isoformat() if p.reviewed_at else None,
    }
    if user:
        row["user"] = {"id": user.id, "email": user.email, "full_name": user.full_name}
    return row


@router.get("/plans")
async def plans():
    return {
        "currency": settings.price_currency,
        "accounts_configured": bool(payment_accounts()),
        "free": {"price": 0, "features": [
            "Free sample questions for every exam",
            "Sit tests your tutor assigns",
            "Instant marking and grade estimates",
            "Progress tracking and leaderboard",
        ]},
        "pro": {"price": settings.pro_price, "days": PRO_DAYS, "features": [
            "Unlimited AI quizzes",
            "Written-answer practice with instant AI marking",
            "Full analytics and feedback",
            "Priority support",
        ]},
        "request": {"price": settings.request_price},
    }


@router.get("/accounts")
async def accounts(user: User = Depends(get_current_user)):
    """Bank details are only shown to signed-in users."""
    return {"accounts": payment_accounts(), "currency": settings.price_currency,
            "pro_price": settings.pro_price, "request_price": settings.request_price,
            "pro_reference": reference_for("pro", user.id),
            "plan": user.plan, "pro_until": user.pro_until.isoformat() if user.pro_until else None}


class ClaimIn(BaseModel):
    purpose: str                      # pro | test_request
    request_id: int | None = None
    paid_via: str | None = None
    payer_name: str | None = None
    payer_note: str | None = None


@router.post("/claim")
async def claim(data: ClaimIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Student says "I've paid". An admin then confirms it against the bank statement."""
    if data.purpose not in ("pro", "test_request"):
        raise HTTPException(400, "Unknown payment purpose")

    req = None
    if data.purpose == "test_request":
        req = (await db.execute(select(TestRequest).where(
            TestRequest.id == data.request_id, TestRequest.student_id == user.id))).scalar_one_or_none()
        if not req:
            raise HTTPException(404, "Request not found")
        if req.status != "awaiting_payment":
            raise HTTPException(400, "This request doesn't need a payment right now.")
        amount, currency = req.price, req.currency
    else:
        if settings.pro_price <= 0:
            raise HTTPException(400, "Pro is not for sale right now.")
        amount, currency = settings.pro_price, settings.price_currency

    pending = (await db.execute(select(Payment).where(
        Payment.user_id == user.id, Payment.purpose == data.purpose, Payment.status == "claimed",
        Payment.request_id == req.id if req else Payment.request_id.is_(None),
    ))).scalars().first()
    if pending:
        raise HTTPException(400, "We already have your payment and are checking it.")

    p = Payment(
        user_id=user.id, purpose=data.purpose, request_id=req.id if req else None,
        reference=reference_for(data.purpose, user.id, req.id if req else None),
        amount=amount, currency=currency,
        paid_via=(data.paid_via or "")[:80] or None,
        payer_name=(data.payer_name or "")[:120] or None,
        payer_note=(data.payer_note or "")[:1000] or None,
    )
    db.add(p)
    if req:
        req.status = "payment_claimed"
    await db.commit()
    await db.refresh(p)

    what = "Pro" if p.purpose == "pro" else f"test request #{p.request_id}"
    await notify_admins(
        f"Payment to check: {p.reference}",
        f"{user.full_name} ({user.email}) says they paid {p.amount:g} {p.currency} for {what} "
        f"via {p.paid_via or 'bank transfer'}. Note: {p.payer_note or '-'}",
        "/admin/requests",
    )
    return _payment_row(p)


@router.get("/mine")
async def mine(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Payment).where(Payment.user_id == user.id)
                             .order_by(Payment.created_at.desc()))).scalars().all()
    return [_payment_row(p) for p in rows]


# ── Revision access for students outside Beyond Tutors (£149/year) ─────────
# No account exists yet (public signup is off), so checkout creates one with access
# switched off. The admin confirms the transfer, which turns on a paid year.

# ── Exchange rates (display only) ───────────────────────────────────────────
# Prices are set in GBP. For visitors elsewhere we show a rounded local equivalent.
# Rates come from open.er-api.com (free, daily) and are cached for 12 hours; if that
# fails we fall back to these rates (5 Nov 2026) so the page never breaks.
FX_CURRENCIES = ["AUD", "NZD", "SGD", "CAD", "EUR", "USD", "AED", "INR"]
_FX_FALLBACK = {"AUD": 1.92, "NZD": 2.39, "SGD": 1.72, "CAD": 1.88, "EUR": 1.20, "USD": 1.35, "AED": 4.95, "INR": 127.5}
_fx_cache: dict = {"at": None, "rates": None}


async def gbp_rates() -> dict[str, float]:
    import httpx
    now = datetime.utcnow()
    if _fx_cache["rates"] and _fx_cache["at"] and now - _fx_cache["at"] < timedelta(hours=12):
        return _fx_cache["rates"]
    rates = dict(_FX_FALLBACK)
    try:
        async with httpx.AsyncClient(timeout=6) as client:
            data = (await client.get("https://open.er-api.com/v6/latest/GBP")).json()
        if data.get("result") == "success":
            rates.update({c: float(data["rates"][c]) for c in FX_CURRENCIES if c in data.get("rates", {})})
            _fx_cache.update(at=now, rates=rates)
    except Exception as ex:
        print(f"[payments] exchange rates unavailable, using fallback: {ex}")
    return rates


@router.get("/fx")
async def fx():
    return {"base": "GBP", "rates": await gbp_rates()}


@router.get("/revision-checkout")
async def revision_checkout_info():
    return {"accounts": payment_accounts(), "price": settings.revision_price,
            "currency": settings.price_currency, "days": settings.subscription_days,
            "pay_link": settings.revision_pay_link}


class RevisionCheckoutIn(BaseModel):
    full_name: str
    email: str
    password: str
    paid_via: str | None = None
    payer_name: str | None = None
    payer_note: str | None = None


@router.post("/revision-checkout")
async def revision_checkout(data: RevisionCheckoutIn, db: AsyncSession = Depends(get_db)):
    email = data.email.strip().lower()
    if "@" not in email or len(data.password) < 8 or not data.full_name.strip():
        raise HTTPException(400, "Enter your name, a valid email and a password of at least 8 characters.")
    now = datetime.utcnow()
    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if user:
        # A free test-request account upgrading: same email and password, keep their history.
        if getattr(user, "access_kind", None) != "free" or not verify_password(data.password, user.password_hash):
            raise HTTPException(400, "That email already has a Notenix account. Use its password, or sign in instead.")
    else:
        user = User(email=email, full_name=data.full_name.strip()[:120], password_hash=hash_password(data.password),
                    role="student", is_verified=True)
        db.add(user)
    user.access_kind, user.access_until = "pending", now  # locked until the payment is confirmed
    await db.flush()
    p = Payment(
        user_id=user.id, purpose="revision", reference=f"NX-V{user.id}",
        amount=settings.revision_price, currency=settings.price_currency,
        paid_via=(data.paid_via or "")[:80] or None,
        payer_name=(data.payer_name or "")[:120] or None,
        payer_note=(data.payer_note or "")[:1000] or None,
    )
    db.add(p)
    await db.commit()
    await db.refresh(p)
    await notify_admins(
        f"Payment to check: {p.reference}",
        f"{user.full_name} ({user.email}) says they paid {p.amount:g} {p.currency} for revision access "
        f"via {p.paid_via or 'bank transfer'}. Note: {p.payer_note or '-'}",
        "/admin/requests",
    )
    return _payment_row(p)


# ── Notenix KS3 (£149/yr): a trial family continues by bank transfer ──────────

@router.get("/ks3-checkout")
async def ks3_checkout_info():
    from services import pricing
    table = {c: pricing.ks3_for_currency(c) for c in pricing.KS3_PRICES}
    return {"accounts": payment_accounts(), "prices": table, "gbp": pricing.ks3_for_currency("GBP"),
            "days": settings.subscription_days, "pay_link": settings.revision_pay_link}


class Ks3CheckoutIn(BaseModel):
    login_id: str
    password: str
    currency: str = "GBP"
    paid_via: str | None = None
    payer_name: str | None = None
    payer_note: str | None = None


@router.post("/ks3-checkout")
async def ks3_checkout(data: Ks3CheckoutIn, db: AsyncSession = Depends(get_db)):
    """Public on purpose: a family whose free week has ended is locked out of the app,
    so they confirm the child's Notenix login here instead of signing in."""
    from services import pricing
    user = (await db.execute(select(User).where(User.email == data.login_id.strip().lower()))).scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(400, "That Notenix user ID or password isn't right.")
    if not user.ks3_year:
        raise HTTPException(400, "This account isn't on Notenix KS3. Start a free week at notenix.com/ks3 first.")
    if not (data.payer_name or "").strip():
        raise HTTPException(400, "Please tell us the name of the person who paid.")
    price = pricing.ks3_for_currency(data.currency)
    open_claim = (await db.execute(select(Payment).where(
        Payment.user_id == user.id, Payment.purpose == "ks3", Payment.status == "claimed"))).scalar_one_or_none()
    if open_claim:
        return _payment_row(open_claim)
    user.billing_currency = price["currency"]
    p = Payment(
        user_id=user.id, purpose="ks3", reference=f"NX-K{user.id}",
        amount=price["amount"], currency=price["currency"],
        paid_via=(data.paid_via or "")[:80] or None,
        payer_name=(data.payer_name or "")[:120] or None,
        payer_note=(data.payer_note or "")[:1000] or None,
    )
    db.add(p)
    await db.commit()
    await db.refresh(p)
    await notify_admins(
        f"Payment to check: {p.reference}",
        f"{user.full_name} ({user.email}, Year {user.ks3_year}) says they paid {price['label']} for Notenix KS3 "
        f"via {p.paid_via or 'bank transfer'}. Payer: {p.payer_name}. Note: {p.payer_note or '-'}",
        "/admin/requests",
    )
    return _payment_row(p)


# ── Admin ────────────────────────────────────────────────────────────────────

@router.get("/admin")
async def admin_list(status: str | None = None, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    q = select(Payment, User).join(User, User.id == Payment.user_id).order_by(Payment.created_at.desc())
    if status:
        q = q.where(Payment.status == status)
    return [_payment_row(p, u) for p, u in (await db.execute(q.limit(300))).all()]


class ReviewIn(BaseModel):
    approve: bool


@router.post("/admin/{payment_id}/review")
async def review(payment_id: int, data: ReviewIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    p = (await db.execute(select(Payment).where(Payment.id == payment_id))).scalar_one_or_none()
    if not p:
        raise HTTPException(404, "Payment not found")
    if p.status != "claimed":
        raise HTTPException(400, f"Payment already {p.status}.")
    user = (await db.execute(select(User).where(User.id == p.user_id))).scalar_one()
    req = None
    if p.request_id:
        req = (await db.execute(select(TestRequest).where(TestRequest.id == p.request_id))).scalar_one_or_none()

    p.status = "confirmed" if data.approve else "rejected"
    p.reviewed_by, p.reviewed_at = admin.id, datetime.utcnow()
    if data.approve and p.purpose == "pro":
        start = max(datetime.utcnow(), user.pro_until or datetime.utcnow())
        user.plan, user.pro_until = "pro", start + timedelta(days=PRO_DAYS)
    if data.approve and p.purpose == "revision":
        user.access_kind, user.access_until = "paid", datetime.utcnow() + timedelta(days=settings.subscription_days)
    if data.approve and p.purpose == "ks3":
        now = datetime.utcnow()
        start = user.access_until if (user.access_kind == "paid" and user.access_until and user.access_until > now) else now
        user.access_kind, user.access_until = "paid", start + timedelta(days=settings.subscription_days)
    if req and req.status == "payment_claimed":
        req.status = "open" if data.approve else "awaiting_payment"
    await db.commit()

    what = {"pro": "Notenix Pro", "revision": "Notenix revision access", "ks3": f"{user.full_name}'s Notenix KS3 year"
            }.get(p.purpose, f"test request #{p.request_id}")
    extra = {"pro": f"Pro is on for the next {PRO_DAYS} days.",
             "revision": "Full revision access is now on for a year.",
             "ks3": "Notenix KS3 is on for a year: a test every half-term, homework help, notes and a progress report every month.",
             }.get(p.purpose, "Our team will send the test shortly.")
    try:
        await send_payment_result(user, data.approve, what, p.amount, p.currency, p.reference, extra)
    except Exception as ex:
        print(f"[payments] notice failed: {ex}")
    return _payment_row(p, user)


async def expire_pro_plans() -> int:
    """Drop bank-transfer Pro back to free once its paid period runs out."""
    from database import SessionLocal
    async with SessionLocal() as db:
        rows = (await db.execute(select(User).where(
            User.plan == "pro", User.pro_until.is_not(None), User.pro_until < datetime.utcnow()))).scalars().all()
        for u in rows:
            u.plan = "free"
        if rows:
            await db.commit()
        return len(rows)
