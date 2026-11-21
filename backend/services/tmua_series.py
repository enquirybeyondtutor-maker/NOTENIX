"""Notenix TMUA Mock Series for the January 2027 sitting: a paid series anyone can join.

How it works
  * notenix.com/tmua-mocks shows the series; "Enrol" goes to /tmua-mocks/enrol.
  * Enrolling creates a Notenix account that is locked (access_kind "pending") until an
    admin confirms the bank-transfer/Wise payment in /admin/requests. Nothing (not even the
    Baseline Mock) is open before that.
  * Confirming the payment gives the student the course KEY until ENDS. From then on, every
    time they open their Tests list, the Baseline Mock and every mock that has opened are
    assigned to them (sync_assignments), so mocks appear on their own at 10:00 UK on the day.
    No background job: nothing wakes the database.
  * Mocks are matched by test title, so the team can upload a mock early without anyone
    seeing it before it opens:  "TMUA January 2027 · Mock 3 · Paper 1", "... · Paper 2".
  * Series students can request TMUA topic sets free (up to REQUESTS_PER_WEEK).
"""
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

KEY = "tmua-mocks-jan27"
NAME = "TMUA Mock Series (January 2027)"
CURRENCY = "GBP"
PRICE = 109
EARLY_PRICE = 99
EARLY_UNTIL = datetime(2026, 11, 25, 0, 0)    # UTC = UK time in November: early bird ends after Tue 24 Nov
ENDS = datetime(2027, 1, 9, 0, 0)             # access ends after the 4-8 Jan test window
EXAM_WINDOW = "4–8 January 2027"
REQUESTS_PER_WEEK = 2
CLASS_LABEL = "TMUA Mock Series"

BASELINE_PREFIX = "TMUA January 2027 Sprint · Baseline Mock"   # tests 82 (Paper 1) and 83 (Paper 2)


def mock_prefix(n: int) -> str:
    return f"TMUA January 2027 · Mock {n} ·"


# (mock number, opens at UTC = UK time, level). The ranked window is 24 hours from opening.
MOCKS = [
    (1, datetime(2026, 11, 25, 10), "Hard"),
    (2, datetime(2026, 11, 28, 10), "Hard"),
    (3, datetime(2026, 12, 5, 10), "Hard"),
    (4, datetime(2026, 12, 12, 10), "Hard"),
    (5, datetime(2026, 12, 13, 10), "Hard"),
    (6, datetime(2026, 12, 19, 10), "Hard"),
    (7, datetime(2026, 12, 20, 10), "Hard"),
    (8, datetime(2026, 12, 26, 10), "Real exam level"),
    (9, datetime(2026, 12, 27, 10), "Real exam level"),
    (10, datetime(2027, 1, 2, 10), "Real exam level"),
]
DEADLINES = [
    (datetime(2026, 12, 14), "UAT-UK deadline: access arrangements & bursary requests"),
    (datetime(2026, 12, 21, 18), "TMUA booking closes, 6pm GMT"),
]


def price(now: datetime | None = None) -> dict:
    now = now or datetime.utcnow()
    early = now < EARLY_UNTIL
    amount = EARLY_PRICE if early else PRICE
    return {"amount": amount, "currency": CURRENCY, "label": f"£{amount}", "early": early,
            "full": PRICE, "early_price": EARLY_PRICE, "early_until": EARLY_UNTIL.isoformat()}


def public_info() -> dict:
    now = datetime.utcnow()
    return {
        "key": KEY, "name": NAME, "price": price(now), "ends": ENDS.isoformat(), "exam_window": EXAM_WINDOW,
        "requests_per_week": REQUESTS_PER_WEEK,
        "mocks": [{"n": n, "opens_at": at.isoformat(), "level": lvl, "open": at <= now} for n, at, lvl in MOCKS],
        "deadlines": [{"at": at.isoformat(), "label": label} for at, label in DEADLINES],
    }


async def is_member(user, db: AsyncSession) -> bool:
    """A paid, live place on the series."""
    from models import Enrolment
    e = (await db.execute(select(Enrolment).where(Enrolment.user_id == user.id, Enrolment.course == KEY))
         ).scalar_one_or_none()
    return bool(e and e.kind == "paid" and (e.until is None or e.until > datetime.utcnow()))


async def grant(user, db: AsyncSession, payment_id: int | None = None):
    from services import courses as course_svc
    return await course_svc.grant(user, KEY, "until", db, until=ENDS, payment_id=payment_id)


def _prefixes(now: datetime) -> list[str]:
    return [BASELINE_PREFIX] + [mock_prefix(n) for n, at, _ in MOCKS if at <= now]


async def sync_assignments(user, db: AsyncSession) -> int:
    """Assign the Baseline Mock and every opened mock to a series student who doesn't have them yet."""
    if not await is_member(user, db):
        return 0
    from models import Test, TestAssignment, User
    from sqlalchemy import or_
    prefixes = _prefixes(datetime.utcnow())
    tests = (await db.execute(
        select(Test).join(User, User.id == Test.owner_id)
        .where(Test.is_archived.is_(False), User.role.in_(["admin", "teacher"]),
               or_(*[Test.title.startswith(p) for p in prefixes]))
    )).scalars().all()
    if not tests:
        return 0
    have = set((await db.execute(select(TestAssignment.test_id).where(
        TestAssignment.student_id == user.id, TestAssignment.test_id.in_([t.id for t in tests])))).scalars().all())
    added = 0
    for t in tests:
        if t.id in have:
            continue
        db.add(TestAssignment(test_id=t.id, student_id=user.id, assigned_by=t.owner_id, class_label=CLASS_LABEL))
        added += 1
    if added:
        await db.commit()
    return added


async def requests_this_week(user, db: AsyncSession) -> int:
    from models import TestRequest
    since = datetime.utcnow() - timedelta(days=7)
    return len((await db.execute(select(TestRequest.id).where(
        TestRequest.student_id == user.id, TestRequest.exam == "TMUA", TestRequest.status != "cancelled",
        TestRequest.created_at >= since))).all())
