"""Teacher endpoints: author tests, assign to students, review results."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime
import secrets
import asyncio

from database import get_db
from models import User, Question, Test, TestAssignment, TestAttempt
from security import require_teacher, is_admin
from services import ai
from services.email import send_assignment_email
from services.pdf_extract import extract_text, render_pages_to_png, crop_figures, read_uploads

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
    kind: str = "test"          # test | homework
    duration_minutes: int | None = None
    # Either provide questions manually, or ask AI to generate `num_questions`.
    generate: bool = True
    num_questions: int = 10
    questions: list[QuestionIn] | None = None


class AssignIn(BaseModel):
    student_emails: list[str]
    class_label: str | None = None
    due_at: datetime | None = None


class PhotoQuestionsIn(BaseModel):
    title: str = ""
    subject: str = "general"
    topic: str = ""
    level: str = "GCSE"
    exam_board: str = ""
    marks_per_question: int = 10
    images: list[str] = []          # compressed image data URIs, one per question
    kind: str = "test"              # test | homework
    is_library: bool = False


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
        "kind": getattr(t, "kind", "test"),
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

    # Aggregate counts in two grouped queries instead of 3 per test (avoids N+1).
    ids = [t.id for t in tests]
    assigned_map: dict[int, int] = {}
    completed_map: dict[int, int] = {}
    avg_map: dict[int, float] = {}
    if ids:
        for tid, cnt in (await db.execute(
            select(TestAssignment.test_id, func.count()).where(TestAssignment.test_id.in_(ids)).group_by(TestAssignment.test_id)
        )).all():
            assigned_map[tid] = cnt
        for tid, cnt, avg in (await db.execute(
            select(TestAttempt.test_id, func.count(), func.avg(TestAttempt.score)).where(TestAttempt.test_id.in_(ids)).group_by(TestAttempt.test_id)
        )).all():
            completed_map[tid] = cnt
            avg_map[tid] = avg
    return [_test_summary(t, assigned_map.get(t.id, 0), completed_map.get(t.id, 0), avg_map.get(t.id)) for t in tests]


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

    kind = "homework" if data.kind == "homework" else "test"
    test = Test(
        owner_id=teacher.id,
        title=data.title.strip()[:200] or f"{data.topic} test",
        subject=data.subject, topic=data.topic, level=data.level,
        exam_board=data.exam_board, difficulty=data.difficulty, kind=kind,
        questions=questions, num_questions=len(questions),
        duration_minutes=None if kind == "homework" else data.duration_minutes,
    )
    db.add(test)
    await db.commit()
    await db.refresh(test)
    return _test_summary(test)


@router.post("/tests/from-pdf")
async def create_test_from_pdf(
    files: list[UploadFile] = File(...),
    title: str = Form(""),
    subject: str = Form("general"),
    topic: str = Form(""),
    level: str = Form("GCSE"),
    exam_board: str = Form("AQA"),
    num_questions: int = Form(10),
    duration_minutes: int | None = Form(None),
    faithful: bool = Form(True),  # True = transcribe existing questions verbatim (vision)
    mode: str = Form("mcq"),      # mcq | written
    kind: str = Form("test"),     # test | homework
    is_library: bool = Form(False),  # admin only: publish to shared practice library
    teacher: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db),
):
    """Upload one or more PDFs/images (screenshots/photos) of a past paper and build a
    test from them. Multiple files are merged into one document in order.
    mode=mcq → multiple-choice (faithful transcription or AI generation).
    mode=written → transcribe extended-response questions + draft mark schemes."""
    data = await read_uploads(files)
    first_name = files[0].filename or "PDF"

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

    # Crop any figures/diagrams the vision model located and embed them in the questions.
    generated = crop_figures(data, generated)

    hw = "homework" if kind == "homework" else "test"
    test = Test(
        owner_id=teacher.id,
        title=(title.strip() or first_name.rsplit(".", 1)[0])[:200],
        subject=subject, topic=topic.strip() or "From document", level=level,
        exam_board=exam_board, difficulty="medium",
        mode=mode, kind=hw, is_library=library,
        questions=generated, num_questions=len(generated),
        duration_minutes=None if hw == "homework" else duration_minutes,
    )
    db.add(test)
    await db.commit()
    await db.refresh(test)
    return _test_summary(test)


@router.post("/tests/photo-questions")
async def create_photo_questions(data: PhotoQuestionsIn, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    """Build a written test where each uploaded screenshot IS a question — shown whole,
    no cropping, no AI transcription. Students answer (type/photo) and a teacher marks it."""
    imgs = [i for i in (data.images or []) if isinstance(i, str) and i.startswith("data:image/")]
    if not imgs:
        raise HTTPException(400, "Add at least one screenshot.")
    if len(imgs) > 20:
        raise HTTPException(400, "You can add up to 20 screenshots.")
    total = 0
    for i in imgs:
        if len(i) > 1_600_000:
            raise HTTPException(400, "One of your screenshots is too large. Please use a smaller image.")
        total += len(i)
    if total > 32_000_000:
        raise HTTPException(400, "Your screenshots are too large in total. Please add fewer.")

    marks = max(1, min(int(data.marks_per_question or 10), 100))
    questions = [{"question": "", "marks": marks, "mark_scheme": "", "image": uri} for uri in imgs]
    library = bool(data.is_library) and is_admin(teacher)

    test = Test(
        owner_id=teacher.id,
        title=(data.title.strip() or "Photo questions")[:200],
        subject=data.subject, topic=data.topic.strip() or "From screenshots", level=data.level,
        exam_board=(data.exam_board or "").strip(), difficulty="medium",
        mode="written", kind=("homework" if data.kind == "homework" else "test"), is_library=library,
        questions=questions, num_questions=len(questions),
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
            # integrity signals (null when not yet attempted)
            "integrity": None if not at else {
                "focus_lost": getattr(at, "focus_lost_count", 0) or 0,
                "time_away_seconds": getattr(at, "time_away_seconds", 0) or 0,
                "paste_attempts": getattr(at, "paste_attempts", 0) or 0,
                "auto_submitted": bool(getattr(at, "auto_submitted", False)),
                "ai_flag": getattr(at, "ai_flag", None),
            },
        })

    if is_written:
        preview = [{"question": q.get("question"), "marks": q.get("marks"),
                    "mark_scheme": q.get("mark_scheme"), "image": q.get("image")} for q in test.questions]
    else:
        # question text + options only (no answers) for teacher preview
        preview = [{"question": q.get("question"), "options": q.get("options"), "image": q.get("image")} for q in test.questions]

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
    newly_assigned: list[User] = []
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
        newly_assigned.append(s)
        created += 1
    await db.commit()

    # Notify newly-assigned students (best-effort; never blocks the response on failure).
    if newly_assigned:
        await asyncio.gather(*[
            send_assignment_email(s.email, s.full_name, test.title, test.subject, teacher.full_name, data.due_at)
            for s in newly_assigned
        ], return_exceptions=True)

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


@router.post("/attempts/{attempt_id}/ai-check")
async def ai_check(attempt_id: int, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    """Teacher-initiated: analyse a written attempt for likely AI authorship."""
    row = (await db.execute(
        select(TestAttempt, Test).join(Test, Test.id == TestAttempt.test_id)
        .where(TestAttempt.id == attempt_id)
    )).first()
    if not row:
        raise HTTPException(404, "Attempt not found")
    attempt, test = row
    if not (is_admin(teacher) or test.owner_id == teacher.id):
        raise HTTPException(403, "You don't have access to this attempt.")
    if getattr(test, "mode", "mcq") != "written":
        raise HTTPException(400, "AI check only applies to written answers.")
    items = [
        {"question": r.get("question", ""), "answer": r.get("your_answer", "")}
        for r in (attempt.results or []) if (r.get("your_answer") or "").strip()
    ]
    if not items:
        raise HTTPException(400, "No typed answers to check (the student may have uploaded photos, or the responses were removed).")
    result = await run_in_threadpool(ai.assess_ai_likelihood, items, test.subject)
    attempt.ai_flag = result.get("verdict")
    attempt.ai_notes = result.get("notes")
    await db.commit()
    return result


@router.get("/students")
async def students(teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    """Students this teacher has assigned work to, with attempt stats."""
    rows = (await db.execute(
        select(User)
        .join(TestAssignment, TestAssignment.student_id == User.id)
        .where(TestAssignment.assigned_by == teacher.id)
        .distinct()
    )).scalars().all()

    ids = [s.id for s in rows]
    assigned_map: dict[int, int] = {}
    avg_map: dict[int, float] = {}
    if ids:
        for sid, cnt in (await db.execute(
            select(TestAssignment.student_id, func.count()).where(
                TestAssignment.student_id.in_(ids), TestAssignment.assigned_by == teacher.id
            ).group_by(TestAssignment.student_id)
        )).all():
            assigned_map[sid] = cnt
        for sid, avg in (await db.execute(
            select(TestAttempt.student_id, func.avg(TestAttempt.score)).where(
                TestAttempt.student_id.in_(ids)
            ).group_by(TestAttempt.student_id)
        )).all():
            avg_map[sid] = avg
    return [{
        "id": s.id, "full_name": s.full_name, "email": s.email,
        "assigned": assigned_map.get(s.id, 0),
        "avg_score": round(avg_map[s.id], 1) if avg_map.get(s.id) is not None else None,
    } for s in rows]
