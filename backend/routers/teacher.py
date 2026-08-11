"""Teacher endpoints: author tests, assign to students, review results."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime
import secrets

from database import get_db
from models import User, Question, Test, TestAssignment, TestAttempt
from security import require_teacher, is_admin
from services import ai
from services.pdf_extract import extract_text, render_pages_to_png

router = APIRouter(prefix="/teacher", tags=["teacher"])


# ── Schemas ──────────────────────────────────────────────────────────────────

class QuestionIn(BaseModel):
    question: str
    options: list[str]
    answer: str
    explanation: str | None = None


class CreateTestIn(BaseModel):
    title: str
    subject: str
    topic: str
    level: str = "GCSE"
    exam_board: str = "AQA"
    difficulty: str = "medium"
    duration_minutes: int | None = None
    # Either provide questions manually, or ask AI to generate `num_questions`.
    generate: bool = True
    num_questions: int = 10
    questions: list[QuestionIn] | None = None


class AssignIn(BaseModel):
    student_emails: list[str]
    class_label: str | None = None
    due_at: datetime | None = None


class UpdateTestIn(BaseModel):
    title: str | None = None
    duration_minutes: int | None = None
    questions: list[QuestionIn] | None = None  # if provided, replaces the question set


# ── Helpers ──────────────────────────────────────────────────────────────────

def _test_summary(t: Test, assigned: int = 0, completed: int = 0, avg: float | None = None) -> dict:
    return {
        "id": t.id, "title": t.title, "subject": t.subject, "topic": t.topic,
        "level": t.level, "exam_board": t.exam_board, "difficulty": t.difficulty,
        "mode": getattr(t, "mode", "mcq"), "is_library": getattr(t, "is_library", False),
        "num_questions": t.num_questions, "duration_minutes": t.duration_minutes,
        "created_at": t.created_at.isoformat() if t.created_at else None,
        "assigned_count": assigned, "completed_count": completed,
        "avg_score": round(avg, 1) if avg is not None else None,
    }


# ── Routes ───────────────────────────────────────────────────────────────────

@router.get("/overview")
async def overview(teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    tests = (await db.execute(select(Test).where(Test.owner_id == teacher.id))).scalars().all()
    test_ids = [t.id for t in tests]

    assigned_count = completed_count = 0
    avg_score = None
    if test_ids:
        assigned_count = (await db.execute(
            select(func.count()).select_from(TestAssignment).where(TestAssignment.test_id.in_(test_ids))
        )).scalar() or 0
        completed_count = (await db.execute(
            select(func.count()).select_from(TestAttempt).where(TestAttempt.test_id.in_(test_ids))
        )).scalar() or 0
        avg_score = (await db.execute(
            select(func.avg(TestAttempt.score)).where(TestAttempt.test_id.in_(test_ids))
        )).scalar()

    # recent attempts across this teacher's tests
    recent = []
    if test_ids:
        rows = (await db.execute(
            select(TestAttempt, User.full_name, Test.title)
            .join(User, User.id == TestAttempt.student_id)
            .join(Test, Test.id == TestAttempt.test_id)
            .where(TestAttempt.test_id.in_(test_ids))
            .order_by(TestAttempt.completed_at.desc()).limit(8)
        )).all()
        recent = [{
            "student": name, "test": title, "score": a.score, "grade": a.grade,
            "completed_at": a.completed_at.isoformat() if a.completed_at else None,
        } for a, name, title in rows]

    return {
        "tests": len(tests),
        "assignments": assigned_count,
        "completed": completed_count,
        "avg_score": round(avg_score, 1) if avg_score is not None else None,
        "recent": recent,
    }


@router.get("/tests")
async def list_tests(teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    tests = (await db.execute(
        select(Test).where(Test.owner_id == teacher.id, Test.is_archived == False)  # noqa: E712
        .order_by(Test.created_at.desc())
    )).scalars().all()

    out = []
    for t in tests:
        assigned = (await db.execute(
            select(func.count()).select_from(TestAssignment).where(TestAssignment.test_id == t.id)
        )).scalar() or 0
        completed = (await db.execute(
            select(func.count()).select_from(TestAttempt).where(TestAttempt.test_id == t.id)
        )).scalar() or 0
        avg = (await db.execute(
            select(func.avg(TestAttempt.score)).where(TestAttempt.test_id == t.id)
        )).scalar()
        out.append(_test_summary(t, assigned, completed, avg))
    return out


@router.post("/tests")
async def create_test(data: CreateTestIn, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    if data.generate:
        n = max(1, min(data.num_questions, 30))
        # Ground generation in any real past-paper questions for this topic.
        rows = (await db.execute(
            select(Question).where(
                Question.subject == data.subject,
                Question.level == data.level,
                Question.topic == data.topic,
            ).limit(15)
        )).scalars().all()
        context = [r.question_text for r in rows]
        generated = ai.generate_mcqs(data.subject, data.topic, data.difficulty, n, context)
        if not generated:
            raise HTTPException(502, "Could not generate questions. Please try again.")
        questions = generated
    else:
        if not data.questions:
            raise HTTPException(400, "Provide questions or enable AI generation.")
        questions = [q.model_dump() for q in data.questions]

    test = Test(
        owner_id=teacher.id,
        title=data.title.strip()[:200] or f"{data.topic} test",
        subject=data.subject, topic=data.topic, level=data.level,
        exam_board=data.exam_board, difficulty=data.difficulty,
        questions=questions, num_questions=len(questions),
        duration_minutes=data.duration_minutes,
    )
    db.add(test)
    await db.commit()
    await db.refresh(test)
    return _test_summary(test)


@router.post("/tests/from-pdf")
async def create_test_from_pdf(
    file: UploadFile = File(...),
    title: str = Form(""),
    subject: str = Form("general"),
    topic: str = Form(""),
    level: str = Form("GCSE"),
    exam_board: str = Form("AQA"),
    num_questions: int = Form(10),
    duration_minutes: int | None = Form(None),
    faithful: bool = Form(True),  # True = transcribe existing questions verbatim (vision)
    mode: str = Form("mcq"),      # mcq | written
    is_library: bool = Form(False),  # admin only: publish to shared practice library
    teacher: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db),
):
    """Upload a PDF (past paper / worksheet) and build a test from it.
    mode=mcq → multiple-choice (faithful transcription or AI generation).
    mode=written → transcribe extended-response questions + draft mark schemes."""
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Please upload a PDF file.")
    data = await file.read()
    if len(data) > 15 * 1024 * 1024:
        raise HTTPException(400, "PDF too large (max 15 MB).")

    mode = "written" if mode == "written" else "mcq"
    library = bool(is_library) and is_admin(teacher)  # only admins publish to the library
    n = max(1, min(num_questions, 30))
    generated = []

    if mode == "written":
        # written practice: vision-transcribe the extended-response questions only
        try:
            images = render_pages_to_png(data, max_pages=8)
        except Exception:
            images = []
        if images:
            generated = ai.extract_written_from_images(images, subject, level, n)
        if not generated:
            raise HTTPException(502, "Could not read written questions from the document. Try a clearer PDF.")
    else:
        if faithful:
            try:
                images = render_pages_to_png(data, max_pages=8)
            except Exception:
                images = []
            if images:
                generated = ai.transcribe_mcqs_from_images(images, subject, n)

        if not generated:
            # fallback (or faithful=False): text extraction + generation
            text = extract_text(data)
            if len(text) < 40 and not faithful:
                raise HTTPException(422, "Couldn't read any text from that PDF. It may be scanned images rather than text.")
            if text and len(text) >= 40:
                generated = ai.generate_mcqs_from_document(text, subject, level, n)

        if not generated:
            raise HTTPException(502, "Could not read questions from the document. Please try again or use a clearer PDF.")

    test = Test(
        owner_id=teacher.id,
        title=(title.strip() or (file.filename or "PDF").rsplit(".", 1)[0])[:200],
        subject=subject, topic=topic.strip() or "From document", level=level,
        exam_board=exam_board, difficulty="medium",
        mode=mode, is_library=library,
        questions=generated, num_questions=len(generated),
        duration_minutes=duration_minutes,
    )
    db.add(test)
    await db.commit()
    await db.refresh(test)
    return _test_summary(test)


@router.post("/tests/{test_id}/share")
async def enable_share(test_id: int, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    """Create (or return existing) a public share token for the test."""
    test = (await db.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == teacher.id)
    )).scalar_one_or_none()
    if not test:
        raise HTTPException(404, "Test not found")
    if not test.share_token:
        test.share_token = secrets.token_urlsafe(9)
        await db.commit()
    return {"share_token": test.share_token}


@router.delete("/tests/{test_id}/share")
async def disable_share(test_id: int, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    test = (await db.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == teacher.id)
    )).scalar_one_or_none()
    if not test:
        raise HTTPException(404, "Test not found")
    test.share_token = None
    await db.commit()
    return {"share_token": None}


@router.get("/tests/{test_id}")
async def test_detail(test_id: int, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    test = (await db.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == teacher.id)
    )).scalar_one_or_none()
    if not test:
        raise HTTPException(404, "Test not found")

    # assignments + their attempt status
    rows = (await db.execute(
        select(TestAssignment, User.full_name, User.email)
        .join(User, User.id == TestAssignment.student_id)
        .where(TestAssignment.test_id == test_id)
        .order_by(TestAssignment.created_at.desc())
    )).all()
    assignment_ids = [a.id for a, _, _ in rows]
    attempts_by_assignment = {}
    if assignment_ids:
        att = (await db.execute(
            select(TestAttempt).where(TestAttempt.assignment_id.in_(assignment_ids))
        )).scalars().all()
        attempts_by_assignment = {a.assignment_id: a for a in att}

    is_written = getattr(test, "mode", "mcq") == "written"
    assignments = []
    for a, name, email in rows:
        at = attempts_by_assignment.get(a.id)
        pending = bool(at and getattr(at, "status", "graded") == "awaiting_marking")
        if not at:
            status = a.status
        elif pending:
            status = "awaiting_marking"
        else:
            status = "completed"
        assignments.append({
            "assignment_id": a.id, "attempt_id": at.id if at else None,
            "student": name, "email": email,
            "class_label": a.class_label,
            "due_at": a.due_at.isoformat() if a.due_at else None,
            "status": status,
            "score": None if (not at or pending) else at.score,
            "grade": None if (not at or pending) else at.grade,
            "completed_at": at.completed_at.isoformat() if at and at.completed_at else None,
        })

    if is_written:
        preview = [{"question": q.get("question"), "marks": q.get("marks"),
                    "mark_scheme": q.get("mark_scheme")} for q in test.questions]
    else:
        # question text + options only (no answers) for teacher preview
        preview = [{"question": q.get("question"), "options": q.get("options")} for q in test.questions]

    return {
        "test": {
            **_test_summary(test),
            "share_token": test.share_token,
            "questions": preview,
        },
        "assignments": assignments,
    }


@router.post("/tests/{test_id}/assign")
async def assign_test(test_id: int, data: AssignIn, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    test = (await db.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == teacher.id)
    )).scalar_one_or_none()
    if not test:
        raise HTTPException(404, "Test not found")

    emails = [e.strip().lower() for e in data.student_emails if e.strip()]
    if not emails:
        raise HTTPException(400, "No student emails provided")

    students = (await db.execute(select(User).where(User.email.in_(emails)))).scalars().all()
    found_by_email = {s.email: s for s in students}

    created, skipped, not_found = 0, 0, []
    for email in emails:
        s = found_by_email.get(email)
        if not s:
            not_found.append(email)
            continue
        exists = (await db.execute(
            select(TestAssignment).where(
                TestAssignment.test_id == test_id, TestAssignment.student_id == s.id
            )
        )).scalar_one_or_none()
        if exists:
            skipped += 1
            continue
        db.add(TestAssignment(
            test_id=test_id, student_id=s.id, assigned_by=teacher.id,
            class_label=data.class_label, due_at=data.due_at,
        ))
        created += 1
    await db.commit()
    return {"assigned": created, "skipped_already_assigned": skipped, "not_found": not_found}


@router.get("/tests/{test_id}/full")
async def test_full(test_id: int, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    """Full test incl. answers — for the teacher's edit screen."""
    test = (await db.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == teacher.id)
    )).scalar_one_or_none()
    if not test:
        raise HTTPException(404, "Test not found")
    attempts = (await db.execute(
        select(func.count()).select_from(TestAttempt).where(TestAttempt.test_id == test_id)
    )).scalar() or 0
    return {
        **_test_summary(test),
        "attempt_count": attempts,
        "questions": test.questions,  # full objects incl. answer/explanation
    }


@router.put("/tests/{test_id}")
async def update_test(test_id: int, data: UpdateTestIn, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    test = (await db.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == teacher.id)
    )).scalar_one_or_none()
    if not test:
        raise HTTPException(404, "Test not found")

    if data.title is not None:
        test.title = data.title.strip()[:200] or test.title
    if data.duration_minutes is not None:
        test.duration_minutes = data.duration_minutes or None
    if data.questions is not None:
        cleaned = [q.model_dump() for q in data.questions if q.question.strip() and all(o.strip() for o in q.options)]
        if not cleaned:
            raise HTTPException(400, "A test needs at least one complete question.")
        test.questions = cleaned
        test.num_questions = len(cleaned)
    await db.commit()
    await db.refresh(test)
    return _test_summary(test)


@router.delete("/tests/{test_id}")
async def delete_test(test_id: int, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    test = (await db.execute(
        select(Test).where(Test.id == test_id, Test.owner_id == teacher.id)
    )).scalar_one_or_none()
    if not test:
        raise HTTPException(404, "Test not found")
    # remove dependent rows first (no DB-level cascade defined)
    from sqlalchemy import delete as sa_delete
    await db.execute(sa_delete(TestAttempt).where(TestAttempt.test_id == test_id))
    await db.execute(sa_delete(TestAssignment).where(TestAssignment.test_id == test_id))
    await db.execute(sa_delete(Test).where(Test.id == test_id))
    await db.commit()
    return {"deleted": test_id}


@router.get("/students")
async def students(teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    """Students this teacher has assigned work to, with attempt stats."""
    rows = (await db.execute(
        select(User)
        .join(TestAssignment, TestAssignment.student_id == User.id)
        .where(TestAssignment.assigned_by == teacher.id)
        .distinct()
    )).scalars().all()

    out = []
    for s in rows:
        assigned = (await db.execute(
            select(func.count()).select_from(TestAssignment)
            .where(TestAssignment.student_id == s.id, TestAssignment.assigned_by == teacher.id)
        )).scalar() or 0
        avg = (await db.execute(
            select(func.avg(TestAttempt.score)).where(TestAttempt.student_id == s.id)
        )).scalar()
        out.append({
            "id": s.id, "full_name": s.full_name, "email": s.email,
            "assigned": assigned, "avg_score": round(avg, 1) if avg is not None else None,
        })
    return out
