"""Tests locked until paid.

A locked assignment (TestAssignment.unlock_price set) shows in the student's list with a
lock, but its questions are never sent until the student pays. One bank-transfer payment
(purpose "unlock") unlocks every locked test of that student together; an admin confirms it
like any other payment, and confirming clears the lock.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Payment, TestAssignment, User

PURPOSE = "unlock"

_SYMBOLS = {"EUR": "€", "GBP": "£", "USD": "$"}


def is_locked(a: TestAssignment) -> bool:
    return bool(getattr(a, "unlock_price", None))


def reference(user_id: int) -> str:
    return f"NX-U{user_id}"


def money(amount: float, currency: str) -> str:
    sym = _SYMBOLS.get(currency.upper())
    num = f"{amount:g}" if float(amount).is_integer() else f"{amount:.2f}"
    return f"{sym}{num}" if sym else f"{num} {currency.upper()}"


async def locked(user: User, db: AsyncSession) -> list[TestAssignment]:
    return list((await db.execute(select(TestAssignment).where(
        TestAssignment.student_id == user.id, TestAssignment.unlock_price.is_not(None),
        TestAssignment.unlock_price > 0))).scalars().all())


async def info(user: User, db: AsyncSession) -> dict | None:
    """What the student owes to unlock their tests, or None if nothing is locked."""
    rows = await locked(user, db)
    if not rows:
        return None
    top = max(rows, key=lambda a: a.unlock_price or 0)
    amount, currency = float(top.unlock_price), (top.unlock_currency or "EUR").upper()
    pending = (await db.execute(select(Payment.id).where(
        Payment.user_id == user.id, Payment.purpose == PURPOSE, Payment.status == "claimed"))).first()
    return {
        "locked": True,
        "count": len(rows),
        "amount": amount,
        "currency": currency,
        "price_label": money(amount, currency),
        "reference": reference(user.id),
        "payment_pending": pending is not None,
    }


async def unlock_all(user: User, db: AsyncSession) -> int:
    rows = await locked(user, db)
    for a in rows:
        a.unlock_price, a.unlock_currency = None, None
    return len(rows)
