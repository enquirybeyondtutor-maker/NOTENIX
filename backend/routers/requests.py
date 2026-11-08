"""Request-a-test service: a student asks for a test, the team assigns one from the
library, the student sits it and the team marks it (written answers go to /marking)."""
import asyncio
import re
from datetime import datetime
from html import escape

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import settings
from database import get_db
from models import User, Test, TestAssignment, TestAttempt, TestRequest, Payment
from security import get_current_user, require_admin, hash_password, create_token, is_free_account
from services.email import send_assignment_email, send_request_cancelled, notify_admins
from routers.payments import reference_for

router = APIRouter(prefix="/requests", tags=["requests"])

EXAMS = {"SAT", "ESAT", "TMUA", "TARA", "GCSE", "IGCSE", "A-Level", "HSC", "VCE", "QCE", "WACE", "NCEA",
         "CBSE", "ICSE", "JEE", "NEET", "Other"}  # CBSE…NEET kept for old requests
OPEN_LIMIT = 5  # unfinished requests a student may have at once
FREE_LIMIT = 1  # requests a free (non-subscriber) account may make in total
SUBSCRIBE_MSG = ("You've used your free test. Subscribe to Notenix (£149 a year) to request more "
                 "tests, or join Beyond Tutors, where Notenix is included.")


def _digits(phone: str | None) -> str:
    return re.sub(r"\D", "", phone or "")[:20]


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
            row["student"] = {"id": s.id, "email": s.email, "full_name": s.full_name,
                              "whatsapp": getattr(s, "phone", None), "free": is_free_account(s)}
        out.append(row)
    return out


# ── Student ──────────────────────────────────────────────────────────────────

class PaperIn(BaseModel):
    """An official past paper the student sits at home ("Get this paper marked" links)."""
    name: str                 # "Paper 1H (Non-calculator)"
    code: str | None = None   # "8300/1H"
    series: str | None = None  # "June 2024"
    course: str | None = None  # "AQA GCSE Maths"
    qp: str | None = None     # official question-paper PDF
    ms: str | None = None     # official mark-scheme PDF


class RequestIn(BaseModel):
    exam: str
    subject: str | None = None
    details: str | None = None
    preferred_date: datetime | None = None
    paper: PaperIn | None = None



def _details(data: "RequestIn") -> str | None:
    text = (data.details or "").strip()
    if data.paper:
        text = f"Mark my past paper: {_paper_label(data.paper)}" + ("\n" + text if text else "")
    return text[:2000] or None

# Only exam-board (and our own) PDFs may be linked from a mark-my-paper test.
_PAPER_HOSTS = ("aqa.org.uk", "pearson.com", "ocr.org.uk", "cambridgeinternational.org", "wjec.co.uk",
                "ccea.org.uk", "sqa.org.uk", "thebeyondtutors.com", "notenix.com", "educationstandards.nsw.edu.au",
                "vcaa.vic.edu.au", "qcaa.qld.edu.au", "scsa.wa.edu.au", "nzqa.govt.nz", "collegeboard.org")
PAPER_PHOTOS = 20  # answer photos a student may upload for a whole paper


def _paper_url(url: str | None) -> str | None:
    from urllib.parse import urlparse
    if not url:
        return None
    u = urlparse(url.strip())
    host = (u.hostname or "").lower()
    board_host = any(host == h or host.endswith("." + h) for h in _PAPER_HOSTS)
    # AQA serves its papers from its own Sanity CMS project, not aqa.org.uk.
    aqa_cdn = host == "cdn.sanity.io" and u.path.startswith("/files/p28bar15/")
    if u.scheme != "https" or not (board_host or aqa_cdn):
        return None
    return url.strip()[:500]


def _paper_label(p: PaperIn) -> str:
    bits = [p.course, p.series, p.name + (f" ({p.code})" if p.code else "")]
    return " · ".join(b.strip() for b in bits if b and b.strip())[:180]


async def _start_marked_paper(db: AsyncSession, req: TestRequest, student: User, p: PaperIn) -> Test:
    """Mark-my-paper request: build a one-question written test (upload every answer page)
    owned by an admin, so it lands in the marking queue, and assign it straight away."""
    qp, ms = _paper_url(p.qp), _paper_url(p.ms)
    label = _paper_label(p)
    question = (f"{label}\n\nSit this paper under timed conditions, closed book. Then photograph every page of "
                f"your answers in order and upload them below (up to {PAPER_PHOTOS} photos). Use the answer box to "
                "tell the tutor anything useful, such as the time you took. A tutor marks it against the official "
                "mark scheme and sends you your mark and feedback.")
    scheme = (f"Official mark scheme: {ms}\n\n" if ms else "") + (
        "Mark against the official mark scheme. Give the raw mark out of the paper total in your feedback, "
        "and award marks here as a percentage (out of 100). List the 2–3 topics to work on next.")
    owner = (await db.execute(select(User).where(User.role == "admin").order_by(User.id))).scalars().first()
    test = Test(
        owner_id=(owner.id if owner else student.id), title=f"Marked past paper: {label}"[:200],
        subject=(req.subject or p.course or req.exam)[:60], topic=(p.name or "Past paper")[:120], level=req.exam,
        exam_board=(p.course or "").split(" ")[0][:40], difficulty="medium", mode="written", kind="homework",  # untimed, not proctored: sat on paper at home
        questions=[{"question": question, "marks": 100, "mark_scheme": scheme, "image": None,
                    "max_photos": PAPER_PHOTOS, "tutor_only": True, "paper_qp": qp}],
        num_questions=1, duration_minutes=None,
    )
    db.add(test)
    await db.flush()
    assignment = TestAssignment(test_id=test.id, student_id=student.id,
                                assigned_by=(owner.id if owner else student.id), class_label="Marked past paper")
    db.add(assignment)
    await db.flush()
    req.assignment_id, req.status = assignment.id, "assigned"
    return test


async def _after_create(db: AsyncSession, req: TestRequest, student: User, paper: PaperIn | None) -> None:
    """Mark-my-paper requests skip the wait: the upload page is ready as soon as they're free to start."""
    if not paper or req.status != "open":
        return
    test = await _start_marked_paper(db, req, student, paper)
    await db.commit()
    for obj in (req, student, test):
        await db.refresh(obj)
    try:
        await send_assignment_email(student, test.title, test.subject, "The Notenix team", None)
    except Exception as ex:
        print(f"[requests] marked-paper email failed: {ex}")


@router.get("/config")
async def config():
    return {"price": settings.request_price, "currency": settings.price_currency, "exams": sorted(EXAMS)}


@router.post("")
async def create(data: RequestIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if data.exam not in EXAMS:
        raise HTTPException(400, "Please choose an exam from the list.")
    if is_free_account(user):
        used = len((await db.execute(select(TestRequest.id).where(
            TestRequest.student_id == user.id, TestRequest.status != "cancelled"))).all())
        if used >= FREE_LIMIT:
            raise HTTPException(402, SUBSCRIBE_MSG)
    open_count = len((await db.execute(select(TestRequest.id).where(
        TestRequest.student_id == user.id,
        TestRequest.status.in_(["awaiting_payment", "payment_claimed", "open"])))).all())
    if open_count >= OPEN_LIMIT:
        raise HTTPException(400, f"You already have {open_count} requests waiting. We'll get to them soon!")

    price = max(0.0, settings.request_price)
    req = TestRequest(
        student_id=user.id, exam=data.exam,
        subject=(data.subject or "").strip()[:120] or None,
        details=_details(data),
        preferred_date=data.preferred_date,
        status="awaiting_payment" if price > 0 else "open",
        price=price, currency=settings.price_currency,
    )
    db.add(req)
    await db.commit()
    await db.refresh(req)
    await _after_create(db, req, user, data.paper)

    await notify_admins(
        f"New {'marked past paper' if data.paper else 'test request'} #{req.id}: {req.exam}",
        f"{user.full_name} ({user.email}) requested a {req.exam} test"
        f"{' in ' + req.subject if req.subject else ''}. Details: {req.details or '-'}",
        "/admin/requests",
    )
    return (await _rows(db, [req]))[0]


class GuestRequestIn(RequestIn):
    full_name: str
    email: str
    whatsapp: str
    password: str


@router.post("/guest")
async def create_guest(data: GuestRequestIn, db: AsyncSession = Depends(get_db)):
    """Free test request from a visitor without an account. Creates a free student account
    (so they can sit the test we send) and the request. One free test per email and per
    WhatsApp number; after that they need a subscription."""
    if data.exam not in EXAMS:
        raise HTTPException(400, "Please choose an exam from the list.")
    email = data.email.strip().lower()
    phone = _digits(data.whatsapp)
    name = data.full_name.strip()[:120]
    if not name or "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(400, "Enter the student's name and a valid email.")
    if len(phone) < 8:
        raise HTTPException(400, "Enter a WhatsApp number with the country code, e.g. +61 412 345 678.")
    if len(data.password) < 8:
        raise HTTPException(400, "Choose a password of at least 8 characters.")
    if (await db.execute(select(User.id).where(User.email == email))).first():
        raise HTTPException(409, "That email already has a Notenix account. Sign in to request a test.")
    if (await db.execute(select(User.id).where(User.phone == phone))).first():
        raise HTTPException(409, "This WhatsApp number has already had a free test. Sign in, or subscribe to request more.")

    user = User(email=email, full_name=name, password_hash=hash_password(data.password),
                role="student", is_verified=True, phone=phone, last_active=datetime.utcnow())
    user.access_kind, user.access_until = "free", None
    db.add(user)
    await db.flush()
    req = TestRequest(
        student_id=user.id, exam=data.exam,
        subject=(data.subject or "").strip()[:120] or None,
        details=_details(data),
        preferred_date=data.preferred_date, status="open", price=0.0, currency=settings.price_currency,
    )
    db.add(req)
    await db.commit()
    await db.refresh(user)
    await db.refresh(req)
    await _after_create(db, req, user, data.paper)

    await notify_admins(
        f"Free {'marked past paper' if data.paper else 'test request'} #{req.id}: {req.exam}",
        f"{name} ({email}, WhatsApp +{phone}) requested a free {req.exam} test"
        f"{' in ' + req.subject if req.subject else ''}. Details: {req.details or '-'}",
        "/admin/requests",
    )
    from routers.auth import _user_dict
    return {"access_token": create_token(user.id, user.token_version or 0), "token_type": "bearer",
            "user": _user_dict(user), "request": (await _rows(db, [req]))[0]}


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
        await send_assignment_email(student, test.title, test.subject, "The Notenix team", data.due_at)
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
        await asyncio.gather(send_request_cancelled(student, req.exam, req.id, req.admin_note), return_exceptions=True)
    return (await _rows(db, [req], with_student=True))[0]
