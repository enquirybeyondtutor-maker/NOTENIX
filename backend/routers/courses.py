"""Student side of per-course access: my courses, the course list, and buying a course
by bank transfer (an admin confirms the payment, which unlocks the course for a year)."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db
from models import User, Payment
from security import get_current_user
from services import courses as course_svc
from services import pricing
from services.email import notify_admins, login_domains

router = APIRouter(prefix="/courses", tags=["courses"])


def _is_bt_student(user: User) -> bool:
    """Beyond Tutors students (IDs issued on a Beyond Tutors domain) pay the BT price."""
    domain = (user.email or "").rsplit("@", 1)[-1].lower()
    return domain in login_domains() and domain.endswith("beyondtutors.com")


GCSE_COURSES = ("gcse-maths", "gcse-biology", "gcse-chemistry", "gcse-physics")   # the Notenix GCSE courses


def course_price(user: User, course: str | None = None) -> dict:
    """Price of one course for a year: £49-equivalent for BT students, £149 for everyone else.
    SAT and the GCSE courses have their own prices (pricing.SAT_PRICES, GCSE_PRICES) for students
    outside Beyond Tutors."""
    if course == "sat" and not _is_bt_student(user):
        return pricing.sat_for_currency(getattr(user, "billing_currency", None))
    if course_svc.is_bundle(course):
        cur = getattr(user, "billing_currency", None)
        if _is_bt_student(user):   # BT students pay the BT price per course, so a bundle saves them nothing
            one = pricing.for_currency(cur)
            n = len(course_svc.bundle_courses(course))
            return {"currency": one["currency"], "amount": one["amount"] * n,
                    "label": pricing.label(one["currency"], one["amount"] * n)}
        return pricing.gcse_bundle_for_currency(cur)
    if course in GCSE_COURSES and not _is_bt_student(user):
        return pricing.gcse_for_currency(getattr(user, "billing_currency", None))
    if _is_bt_student(user):
        return pricing.for_currency(getattr(user, "billing_currency", None))
    return {"currency": settings.price_currency, "amount": settings.revision_price,
            "label": pricing.label(settings.price_currency, settings.revision_price)}


@router.get("/catalogue")
async def catalogue():
    return course_svc.catalogue()


@router.get("/mine")
async def mine(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    rows = await course_svc.enrolments(user.id, db)
    restricted = (await course_svc.live_courses(user, db)) is not None
    pending = (await db.execute(select(Payment.course).where(
        Payment.user_id == user.id, Payment.status == "claimed", Payment.course.is_not(None)))).scalars().all()
    return {
        "restricted": restricted,   # False: an older account that can open every course
        "courses": [course_svc.enrolment_row(e) for e in rows],
        "pending": sorted(set(pending)),  # courses paid for, waiting for the admin to confirm
        "price": course_price(user),
        # courses priced differently from the rest
        "prices": {"sat": course_price(user, "sat"), **{c: course_price(user, c) for c in GCSE_COURSES},
                   **{b: course_price(user, b) for b in course_svc.BUNDLES}},
        "bundles": _bundles(user, rows),
    }


def _bundles(user: User, rows: list) -> list[dict]:
    """Bundles this student could buy, with what they save against buying each course alone.
    Not offered to Beyond Tutors students (no saving) or once any course in it is already live."""
    if _is_bt_student(user):
        return []
    live = {course_svc.enrolment_row(e)["course"] for e in rows if course_svc.enrolment_row(e)["live"]}
    out = []
    for key, (name, courses) in course_svc.BUNDLES.items():
        if live & set(courses):
            continue
        price = course_price(user, key)
        singles = sum(course_price(user, c)["amount"] for c in courses)
        out.append({"key": key, "name": name, "courses": [course_svc.course_name(c) for c in courses],
                    "price": price, "saving": pricing.label(price["currency"], singles - price["amount"])})
    return out


class BuyIn(BaseModel):
    course: str
    paid_via: str | None = None
    payer_name: str | None = None
    payer_note: str | None = None


@router.post("/buy")
async def buy(data: BuyIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """The student says they've paid for a course; it unlocks once an admin confirms."""
    if not course_svc.is_course(data.course) and not course_svc.is_bundle(data.course):
        raise HTTPException(400, "Please choose a course.")
    if (await db.execute(select(Payment.id).where(
            Payment.user_id == user.id, Payment.status == "claimed", Payment.course == data.course))).first():
        raise HTTPException(400, "We already have your payment for this course and are checking it.")
    price = course_price(user, data.course)
    p = Payment(
        user_id=user.id, purpose="course", course=data.course, reference=f"NX-C{user.id}",
        amount=price["amount"], currency=price["currency"],
        paid_via=(data.paid_via or "")[:80] or None,
        payer_name=(data.payer_name or "")[:120] or None,
        payer_note=(data.payer_note or "")[:1000] or None,
    )
    db.add(p)
    await db.commit()
    await db.refresh(p)
    name = course_svc.course_name(data.course)
    await notify_admins(
        f"Payment to check: {p.reference} ({name})",
        f"{user.full_name} ({user.email}) says they paid {p.amount:g} {p.currency} for {name} "
        f"via {p.paid_via or 'bank transfer'}. Note: {p.payer_note or '-'}",
        "/admin/requests",
    )
    return {"id": p.id, "reference": p.reference, "course": p.course, "course_name": name,
            "amount": p.amount, "currency": p.currency, "status": p.status}
