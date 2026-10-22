"""Request-a-test service: a student asks for a test, the team assigns one from the
library, the student sits it and the team marks it (written answers go to /marking)."""
import asyncio
from datetime import datetime
from html import escape

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import settings
from database import get_db
from models import User, Test, TestAssignment, TestAttempt, TestRequest, Payment
from security import get_current_user, require_admin
from services.email import send_assignment_email, send_notice, notify_admins
from routers.payments import reference_for

router = APIRouter(prefix="/requests", tags=["requests"])

EXAMS = {"SAT", "ESAT", "TMUA", "TARA", "GCSE", "IGCSE", "A-Level", "CBSE", "ICSE", "JEE", "NEET", "Other"}
OPEN_LIMIT = 5  # unfinished requests a student may have at once


def _progress(assignment: TestAssignment | None, attempt: TestAttempt | None) -> str | None:
    """Where an assigned request has got to: assigned → submitted → marked."""
    if not assignment:
        return None
    if not attempt:
        return "assigned"
    return "marked" if attempt.status == "graded" else "submitted"


async def _rows(db: AsyncSession, reqs: list[TestRequest], with_student: bool = False) -> list[dict]:
    a_ids = [r.assignment_id for r in reqs if r.assignment_id]
    assignments, attempts, tests = {}, {}, {}
    if a_ids:
        assignments = {a.id: a for a in (await db.execute(
            select(TestAssignment).where(TestAssignment.id.in_(a_ids)))).scalars().all()}
        attempts = {t.assignment_id: t for t in (await db.execute(
            select(TestAttempt).where(TestAttempt.assignment_id.in_(a_ids)))).scalars().all()}
        t_ids = {a.test_id for a in assignments.values()}
        tests = {t.id: t for t in (await db.execute(select(Test).where(Test.id.in_(t_ids)))).scalars().all()}
    students = {}
    if with_student:
        s_ids = {r.student_id for r in reqs}
        students = {u.id: u for u in (await db.execute(select(User).where(User.id.in_(s_ids)))).scalars().all()}
    payments: dict[int, Payment] = {}
    if reqs:
        for p in (await db.execute(select(Payment).where(
                Payment.request_id.in_([r.id for r in reqs])).order_by(Payment.created_at))).scalars().all():
            payments[p.request_id] = p  # latest wins

    out = []
    for r in reqs:
        a = assignments.get(r.assignment_id)
        att = attempts.get(r.assignment_id) if a else None
        t = tests.get(a.test_id) if a else None
        p = payments.get(r.id)
        row = {
            "id": r.id, "exam": r.exam, "subject": r.subject, "details": r.details,
            "preferred_date": r.preferred_date.isoformat() if r.preferred_date else None,
            "status": r.status, "progress": _progress(a, att),
            "price": r.price, "currency": r.currency, "reference": reference_for("test_request", r.student_id, r.id),
            "assignment_id": r.assignment_id,
            "test": {"id": t.id, "title": t.title, "num_questions": t.num_questions,
                     "duration_minutes": t.duration_minutes} if t else None,
            "score": att.score if att and att.status == "graded" else None,
            "grade": att.grade if att and att.status == "graded" else None,
            "payment": {"id": p.id, "status": p.status, "paid_via": p.paid_via, "payer_name": p.payer_name,
                        "payer_note": p.payer_note, "amount": p.amount, "currency": p.currency} if p else None,
            "admin_note": r.admin_note,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        if with_student and r.student_id in students:
            s = students[r.student_id]
            row["student"] = {"id": s.id, "email": s.email, "full_name": s.full_name}
        out.append(row)
    return out


# ── Student ──────────────────────────────────────────────────────────────────

class RequestIn(BaseModel):
    exam: str
    subject: str | None = None
    details: str | None = None
    preferred_date: datetime | None = None


@router.get("/config")
async def config():
    return {"price": settings.request_price, "currency": settings.price_currency, "exams": sorted(EXAMS)}


@router.post("")
async def create(data: RequestIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if data.exam not in EXAMS:
        raise HTTPException(400, "Please choose an exam from the list.")
    open_count = len((await db.execute(select(TestRequest.id).where(
        TestRequest.student_id == user.id,
        TestRequest.status.in_(["awaiting_payment", "payment_claimed", "open"])))).all())
    if open_count >= OPEN_LIMIT:
        raise HTTPException(400, f"You already have {open_count} requests waiting. We'll get to them soon!")

    price = max(0.0, settings.request_price)
    req = TestRequest(
        student_id=user.id, exam=data.exam,
        subject=(data.subject or "").strip()[:120] or None,
        details=(data.details or "").strip()[:2000] or None,
        preferred_date=data.preferred_date,
        status="awaiting_payment" if price > 0 else "open",
        price=price, currency=settings.price_currency,
    )
    db.add(req)
    await db.commit()
    await db.refresh(req)

    await notify_admins(
        f"New test request #{req.id}: {req.exam}",
        f"{user.full_name} ({user.email}) requested a {req.exam} test"
        f"{' in ' + req.subject if req.subject else ''}. Details: {req.details or '-'}",
        "/admin/requests",
    )
    return (await _rows(db, [req]))[0]


@router.get("/mine")
async def mine(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    reqs = (await db.execute(select(TestRequest).where(TestRequest.student_id == user.id)
                             .order_by(TestRequest.created_at.desc()))).scalars().all()
    return await _rows(db, list(reqs))


@router.post("/{request_id}/cancel")
async def cancel(request_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    req = (await db.execute(select(TestRequest).where(
        TestRequest.id == request_id, TestRequest.student_id == user.id))).scalar_one_or_none()
    if not req:
        raise HTTPException(404, "Request not found")
    if req.status not in ("awaiting_payment", "open"):
        raise HTTPException(400, "This request can't be cancelled now. Contact us if you need help.")
    req.status = "cancelled"
    await db.commit()
    return {"id": req.id, "status": req.status}


# ── Admin / team ─────────────────────────────────────────────────────────────

@router.get("/admin")
async def admin_list(admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    reqs = (await db.execute(select(TestRequest).order_by(TestRequest.created_at.desc()).limit(300))).scalars().all()
    return await _rows(db, list(reqs), with_student=True)


@router.get("/admin/tests")
async def admin_tests(admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    """Every live test any teacher has made, for picking one to send."""
    rows = (await db.execute(select(Test).where(Test.is_archived == False)  # noqa: E712
                             .order_by(Test.created_at.desc()))).scalars().all()
    return [{"id": t.id, "title": t.title, "level": t.level, "subject": t.subject, "mode": t.mode,
             "kind": t.kind, "num_questions": t.num_questions, "duration_minutes": t.duration_minutes}
            for t in rows]


class AssignIn(BaseModel):
    test_id: int
    due_at: datetime | None = None
    note: str | None = None


@router.post("/admin/{request_id}/assign")
async def assign(request_id: int, data: AssignIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    req = (await db.execute(select(TestRequest).where(TestRequest.id == request_id))).scalar_one_or_none()
    if not req:
        raise HTTPException(404, "Request not found")
    if req.status != "open":
        raise HTTPException(400, "Only paid (or free) requests that haven't been sent yet can be assigned.")
    test = (await db.execute(select(Test).where(Test.id == data.test_id))).scalar_one_or_none()
    if not test:
        raise HTTPException(404, "Test not found")
    student = (await db.execute(select(User).where(User.id == req.student_id))).scalar_one()

    assignment = (await db.execute(select(TestAssignment).where(
        TestAssignment.test_id == test.id, TestAssignment.student_id == student.id))).scalar_one_or_none()
    if assignment:
        raise HTTPException(400, "This student already has that test. Pick a different one.")
    assignment = TestAssignment(
        test_id=test.id, student_id=student.id, assigned_by=admin.id,
        class_label=f"Requested {req.exam}", due_at=data.due_at,
    )
    db.add(assignment)
    await db.flush()
    req.assignment_id, req.status = assignment.id, "assigned"
    if data.note is not None:
        req.admin_note = data.note.strip()[:1000] or None
    await db.commit()

    try:
        await send_assignment_email(student.email, student.full_name, test.title, test.subject,
                                    "The Notenix team", data.due_at)
    except Exception as ex:
        print(f"[requests] assignment email failed: {ex}")
    return (await _rows(db, [req], with_student=True))[0]


class UpdateIn(BaseModel):
    status: str | None = None   # open (waive payment) | cancelled
    note: str | None = None


@router.post("/admin/{request_id}")
async def update(request_id: int, data: UpdateIn, admin: User = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    req = (await db.execute(select(TestRequest).where(TestRequest.id == request_id))).scalar_one_or_none()
    if not req:
        raise HTTPException(404, "Request not found")
    if data.status:
        if data.status not in ("open", "cancelled"):
            raise HTTPException(400, "Status can only be set to open or cancelled.")
        if req.status == "assigned":
            raise HTTPException(400, "This request already has a test.")
        req.status = data.status
    if data.note is not None:
        req.admin_note = data.note.strip()[:1000] or None
    await db.commit()

    if data.status == "cancelled":
        student = (await db.execute(select(User).where(User.id == req.student_id))).scalar_one()
        name = escape((student.full_name or "there").split(" ")[0])
        body = (f"Hi {name}, your {escape(req.exam)} test request #{req.id} has been cancelled."
                + (f" Note from the team: {escape(req.admin_note)}" if req.admin_note else ""))
        await asyncio.gather(send_notice(student.email, "Test request cancelled", "Test request cancelled",
                                         body, body, "/requests", "My requests"), return_exceptions=True)
    return (await _rows(db, [req], with_student=True))[0]
