"""Manual payments: students pay by bank transfer (Wise or a local account) and an admin
confirms the money arrived. Free to run: no payment gateway, no fees beyond the bank's."""
import json
from datetime import datetime, timedelta
from html import escape

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.payer import clean_dob
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import settings
from database import get_db
from models import User, Payment, TestRequest, Enrolment
from security import get_current_user, require_admin, hash_password, verify_password, create_token
from services.email import send_payment_result, notify_admins
from services import courses as course_svc

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
    course = getattr(p, "course", None)
    row = {
        "id": p.id, "purpose": p.purpose, "request_id": p.request_id, "reference": p.reference,
        "course": course, "course_name": course_svc.course_name(course) if course else None,
        "amount": p.amount, "currency": p.currency, "paid_via": p.paid_via,
        "payer_name": p.payer_name, "payer_note": p.payer_note, "payer_dob": getattr(p, "payer_dob", None), "status": p.status,
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
    payer_dob: str | None = None   # optional; helps match Wise payments


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
        payer_note=(data.payer_note or "")[:1000] or None, payer_dob=clean_dob(data.payer_dob),
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
FX_CURRENCIES = ["AUD", "NZD", "SGD", "CAD", "EUR", "USD", "AED", "INR", "THB"]
_FX_FALLBACK = {"AUD": 1.92, "NZD": 2.39, "SGD": 1.72, "CAD": 1.88, "EUR": 1.20, "USD": 1.35, "AED": 4.95, "INR": 127.5, "THB": 43.5}
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


def _public_price(course: str | None) -> dict:
    """What a new student (not with Beyond Tutors) pays for this course a year, in GBP:
    GCSE £99 a subject, the GCSE bundle £349, SAT £99, anything else the standard £149."""
    import types
    from routers.courses import course_price
    return course_price(types.SimpleNamespace(email="", billing_currency=settings.price_currency), course)


def _known_course(course: str | None) -> bool:
    return bool(course) and (course_svc.is_course(course) or course_svc.is_bundle(course))


@router.get("/user-id")
async def user_id_preview(name: str = "", db: AsyncSession = Depends(get_db)):
    """The @notenix.com user ID a new student would get from this name (aryan@notenix.com, or
    aryan.s@... if that is taken). Shown on the sign-up checkouts as the name is typed; the ID is
    only reserved when the form is sent, so it can still change if someone takes it first."""
    clean = " ".join(name.split())[:120]
    if len(clean) < 2:
        return {"login_id": None}
    from routers.admin import _free_id
    return {"login_id": await _free_id(clean, db, domain=settings.ks3_id_domain)}


@router.get("/revision-checkout")
async def revision_checkout_info(course: str | None = None):
    from services import pricing
    p = _public_price(course if _known_course(course) else None)
    return {"accounts": payment_accounts(), "price": p["amount"], "currency": p["currency"],
            "standard_price": pricing.normal_for_currency(p["currency"])["amount"], "days": settings.subscription_days,
            "course_name": course_svc.course_name(course) if _known_course(course) else None,
            # Wise card links are fixed-amount, one per price; no link for a price -> bank transfer only.
            "pay_link": {settings.revision_price: settings.revision_pay_link, 99: settings.pay_link_99,
                         349: settings.pay_link_349}.get(p["amount"], "")}


class RevisionCheckoutIn(BaseModel):
    full_name: str
    email: str
    password: str
    course: str | None = None   # the course being bought (services/courses.py); None = everything (old checkout)
    paid_via: str | None = None
    payer_name: str | None = None
    payer_note: str | None = None
    payer_dob: str | None = None   # optional; helps match Wise payments


@router.post("/revision-checkout")
async def revision_checkout(data: RevisionCheckoutIn, db: AsyncSession = Depends(get_db)):
    email = data.email.strip().lower()
    if "@" not in email or len(data.password) < 8 or not data.full_name.strip():
        raise HTTPException(400, "Enter your name, a valid email and a password of at least 8 characters.")
    if data.course and not _known_course(data.course):
        raise HTTPException(400, "Please choose your course.")
    price = _public_price(data.course)   # GCSE £99, bundle £349, SAT £99, else £149
    now = datetime.utcnow()
    # Older accounts sign in with their own email; new ones have a name@notenix.com ID and keep the email
    # they typed as notify_email (where receipts and updates go - a login ID has no inbox).
    user = (await db.execute(select(User).where(
        (User.email == email) | (User.notify_email == email)))).scalars().first()
    if user:
        # A free test-request account upgrading: same password, keep their history.
        if getattr(user, "access_kind", None) != "free" or not verify_password(data.password, user.password_hash):
            raise HTTPException(400, f"That email already has a Notenix account (user ID {user.email}). "
                                     "Use its password, or sign in instead.")
    else:
        from routers.admin import _free_id
        login_id = await _free_id(data.full_name, db, domain=settings.ks3_id_domain)   # anushka@notenix.com
        user = User(email=login_id, notify_email=email, full_name=data.full_name.strip()[:120],
                    password_hash=hash_password(data.password), role="student", is_verified=True)
        db.add(user)
    user.access_kind, user.access_until = "pending", now  # locked until the payment is confirmed
    await db.flush()
    # Enrol & pay: with a course chosen, the student starts straight away on a trial of it
    # (settings.trial_days); confirming the payment turns it into a paid year, rejecting it ends it.
    if data.course:
        for c in _checkout_courses(data.course):
            e = (await db.execute(select(Enrolment).where(Enrolment.user_id == user.id,
                                                          Enrolment.course == c))).scalar_one_or_none()
            if not (e and e.kind == "paid" and (e.until is None or e.until > now)):
                await course_svc.grant(user, c, "trial", db)
    p = Payment(
        user_id=user.id, purpose="revision", reference=f"NX-V{user.id}", course=data.course or None,
        amount=price["amount"], currency=price["currency"],
        paid_via=(data.paid_via or "")[:80] or None,
        payer_name=(data.payer_name or "")[:120] or None,
        payer_note=(data.payer_note or "")[:1000] or None, payer_dob=clean_dob(data.payer_dob),
    )
    db.add(p)
    await db.commit()
    await db.refresh(p)
    await notify_admins(
        f"Payment to check: {p.reference}",
        f"{user.full_name} (user ID {user.email}, email {user.notify_email or user.email}) says they paid "
        f"{p.amount:g} {p.currency} for {course_svc.course_name(p.course) if p.course else 'revision access'} "
        f"via {p.paid_via or 'bank transfer'}. Note: {p.payer_note or '-'}",
        "/admin/requests",
    )
    out = {**_payment_row(p), "login_id": user.email}
    if data.course:   # signed straight in: the course is already open on its trial
        from routers.auth import _user_dict
        out.update(access_token=create_token(user.id, user.token_version or 0), user=_user_dict(user))
    return out


def _checkout_courses(course: str) -> list[str]:
    return course_svc.bundle_courses(course) if course_svc.is_bundle(course) else [course]


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
    payer_dob: str | None = None   # optional; helps match Wise payments


@router.post("/ks3-checkout")
async def ks3_checkout(data: Ks3CheckoutIn, db: AsyncSession = Depends(get_db)):
    """Public on purpose: a family whose free week has ended is locked out of the app,
    so they confirm the child's Notenix login here instead of signing in."""
    from services import pricing, ks3
    user = (await db.execute(select(User).where(User.email == data.login_id.strip().lower()))).scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(400, "That Notenix user ID or password isn't right.")
    if not user.ks3_year:
        raise HTTPException(400, "This account isn't on Notenix KS3, Middle School or Ontario. Start a free week at "
                                 "notenix.com/ks3, notenix.com/middle-school or notenix.com/ontario first.")
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
        payer_note=(data.payer_note or "")[:1000] or None, payer_dob=clean_dob(data.payer_dob),
    )
    db.add(p)
    await db.commit()
    await db.refresh(p)
    await notify_admins(
        f"Payment to check: {p.reference}",
        f"{user.full_name} ({user.email}, {ks3.year_label(user)}) says they paid {price['label']} for {ks3.product(user)} "
        f"via {p.paid_via or 'bank transfer'}. Payer: {p.payer_name}. Note: {p.payer_note or '-'}",
        "/admin/requests",
    )
    return _payment_row(p)


# ── Notenix SAT after the free week ─────────────────────────────────────────

@router.get("/sat-checkout")
async def sat_checkout_info():
    from services import pricing
    table = {c: pricing.sat_for_currency(c) for c in pricing.SAT_PRICES}
    return {"accounts": payment_accounts(), "prices": table, "usd": pricing.sat_for_currency("USD"),
            "pay_link": settings.revision_pay_link}


class SatCheckoutIn(BaseModel):
    email: str
    password: str
    currency: str = "USD"
    paid_via: str | None = None
    payer_name: str | None = None
    payer_note: str | None = None
    payer_dob: str | None = None   # optional; helps match Wise payments


@router.post("/sat-checkout")
async def sat_checkout(data: SatCheckoutIn, db: AsyncSession = Depends(get_db)):
    """Public on purpose: once the free week ends the student is locked out of the app,
    so they confirm their Notenix SAT login here instead of signing in."""
    from services import pricing
    user = (await db.execute(select(User).where(User.email == data.email.strip().lower()))).scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(400, "That email or password isn't right.")
    if not user.sat_since:
        raise HTTPException(400, "This account isn't on Notenix SAT. Start with the free diagnostic at notenix.com/sat.")
    if not (data.payer_name or "").strip():
        raise HTTPException(400, "Please tell us the name of the person who paid.")
    open_claim = (await db.execute(select(Payment).where(
        Payment.user_id == user.id, Payment.course == "sat", Payment.status == "claimed"))).scalar_one_or_none()
    if open_claim:
        return _payment_row(open_claim)
    price = pricing.sat_for_currency(data.currency)
    user.billing_currency = price["currency"]
    p = Payment(
        user_id=user.id, purpose="course", course="sat", reference=f"NX-C{user.id}",
        amount=price["amount"], currency=price["currency"],
        paid_via=(data.paid_via or "")[:80] or None,
        payer_name=(data.payer_name or "")[:120] or None,
        payer_note=(data.payer_note or "")[:1000] or None, payer_dob=clean_dob(data.payer_dob),
    )
    db.add(p)
    await db.commit()
    await db.refresh(p)
    await notify_admins(
        f"Payment to check: {p.reference}",
        f"{user.full_name} ({user.email}) says they paid {price['label']} for Notenix SAT "
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
    if data.approve and p.purpose == "revision" and not p.course:
        user.access_kind, user.access_until = "paid", datetime.utcnow() + timedelta(days=settings.subscription_days)
    if data.approve and (p.purpose == "course" or (p.purpose == "revision" and p.course)):
        # One course for a year (renewing early adds the year on to the current end date).
        # A bundle payment switches on every course in the bundle.
        from services import tmua_series
        if p.course == tmua_series.KEY:   # fixed-term series: open until the January 2027 test window ends
            await tmua_series.grant(user, db, payment_id=p.id)
        else:
            for c in (course_svc.bundle_courses(p.course) if course_svc.is_bundle(p.course) else [p.course]):
                await course_svc.grant(user, c, "year", db, payment_id=p.id)
    if not data.approve and p.purpose == "revision" and p.course:
        # The trial that started at checkout ends now (kept, not deleted: a student with no
        # enrolments at all would be unrestricted).
        now = datetime.utcnow()
        for c in _checkout_courses(p.course):
            e = (await db.execute(select(Enrolment).where(Enrolment.user_id == user.id,
                                                          Enrolment.course == c))).scalar_one_or_none()
            if e and e.kind == "trial":
                e.until = now
        await db.flush()
        course_svc.sync_access(user, await course_svc.enrolments(user.id, db))
    if data.approve and p.purpose in ("annual", "doubt", "plus"):
        from services import doubt
        doubt.set_plan(user, p.purpose)
    if data.approve and p.purpose == "ks3":
        now = datetime.utcnow()
        start = user.access_until if (user.access_kind == "paid" and user.access_until and user.access_until > now) else now
        user.access_kind, user.access_until = "paid", start + timedelta(days=settings.subscription_days)
    if req and req.status == "payment_claimed":
        req.status = "open" if data.approve else "awaiting_payment"
    await db.commit()
    from services import tmua_series
    is_series = p.course == tmua_series.KEY
    if data.approve and is_series:
        await tmua_series.sync_assignments(user, db)

    course_label = course_svc.course_name(p.course) if p.course else None
    from services import ks3
    what = {"pro": "Notenix Pro", "revision": f"Notenix {course_label}" if course_label else "Notenix revision access",
            "course": f"Notenix {course_label}", "ks3": f"{user.full_name}'s {ks3.product(user)} year",
            "doubt": f"{user.full_name}'s Doubt Help (30 days)", "plus": f"{user.full_name}'s Doubt Help Plus (30 days)",
            "annual": f"{user.full_name}'s Ask a Tutor year"
            }.get(p.purpose, f"test request #{p.request_id}")
    extra = {"pro": f"Pro is on for the next {PRO_DAYS} days.",
             "revision": f"{course_label} is now on for a year." if course_label else "Full revision access is now on for a year.",
             "course": f"{course_label} is now on for a year: practice, revision and tutor-marked papers.",
             "ks3": (f"{ks3.product(user)} is on for a year: {ks3.subjects_text(user)} tests, homework help, notes and a progress report every month."
                     if ks3.is_grades(user) else
                     "Notenix KS3 is on for a year: a test every half-term, homework help, notes and a progress report every month."),
             "doubt": "Ask a Tutor is on for the next 30 days: up to 20 questions, answered step by step.",
             "annual": "Ask a Tutor is on for a whole year: up to 20 questions every month, answered step by step.",
             "plus": "Ask a Tutor is on for the next 30 days: up to 50 questions, plus 2 live 30-minute doubt calls. Reply on WhatsApp to book them.",
             }.get(p.purpose, "Our team will send the test shortly.")
    if is_series:
        extra = ("Your place on the TMUA Mock Series is confirmed. Sign in at notenix.com: the Baseline Mock is waiting "
                 "in Tests, and each mock appears there at 10 a.m. UK time on its date. Stuck on a topic? Request a topic set "
                 "from Request a test (up to 2 a week).")
    try:
        from services.welcome_guide import guide
        await send_payment_result(user, data.approve, what, p.amount, p.currency, p.reference, extra,
                                  guide=guide(user, p) if data.approve else None)
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
