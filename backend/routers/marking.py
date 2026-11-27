"""Manual marking of written answers by teachers/admins.

Non-Pro students' written submissions land in `awaiting_marking`. A teacher (for
tests they own) or an admin (for any test) reviews the answers against the mark
scheme, enters marks + feedback per question, and the attempt becomes `graded`.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import User, Test, TestAssignment, TestAttempt
from security import require_teacher, is_admin, can_mark_written
from services.grading import finalize_written_marks, estimate_grade
from services.email import send_marked_email, marker_inbox, send_work_pdf

router = APIRouter(prefix="/marking", tags=["marking"])


class MarkEntry(BaseModel):
    marks_awarded: int
    feedback: str | None = None
    model_answer: str | None = None


class SubmitMarksIn(BaseModel):
    marks: list[MarkEntry]


@router.get("/queue")
async def queue(marker: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    """Written attempts awaiting marking that this teacher/admin may mark."""
    q = (
        select(TestAttempt, Test, User.full_name)
        .join(Test, Test.id == TestAttempt.test_id)
        .join(User, User.id == TestAttempt.student_id)
        .where(TestAttempt.status == "awaiting_marking")
        .order_by(TestAttempt.completed_at.asc())
    )
    if not is_admin(marker):
        q = q.where(Test.owner_id == marker.id)
    rows = (await db.execute(q)).all()
    return [{
        "attempt_id": at.id,
        "student": name,
        "test_title": t.title,
        "subject": t.subject,
        "level": t.level,
        "num_questions": t.num_questions,
        "submitted_at": at.completed_at.isoformat() if at.completed_at else None,
    } for at, t, name in rows]


async def _load_for_marking(attempt_id: int, marker: User, db: AsyncSession):
    row = (await db.execute(
        select(TestAttempt, Test).join(Test, Test.id == TestAttempt.test_id)
        .where(TestAttempt.id == attempt_id)
    )).first()
    if not row:
        raise HTTPException(404, "Attempt not found")
    attempt, test = row
    if not can_mark_written(marker, test):
        raise HTTPException(403, "You don't have permission to mark this attempt.")
    return attempt, test


@router.get("/{attempt_id}")
async def get_attempt(attempt_id: int, marker: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    attempt, test = await _load_for_marking(attempt_id, marker, db)
    student = (await db.execute(select(User).where(User.id == attempt.student_id))).scalar_one_or_none()
    answers = attempt.answers or []
    answer_images = attempt.answer_images or []
    qtimes = attempt.question_times or []
    questions = []
    for i, q in enumerate(test.questions):
        questions.append({
            "question": q.get("question"),
            "marks": q.get("marks"),
            "mark_scheme": q.get("mark_scheme"),
            "image": q.get("image"),
            "your_answer": answers[i] if i < len(answers) else "",
            "answer_images": answer_images[i] if i < len(answer_images) else [],
            "time_seconds": qtimes[i] if i < len(qtimes) else None,
        })
    return {
        "attempt_id": attempt.id,
        "status": attempt.status,
        "student": student.full_name if student else "Student",
        "test_title": test.title,
        "subject": test.subject,
        "level": test.level,
        "time_taken_seconds": attempt.time_taken_seconds,
        "questions": questions,
        "email_to": marker_inbox(marker),
        "integrity": {
            "focus_lost": getattr(attempt, "focus_lost_count", 0) or 0,
            "time_away_seconds": getattr(attempt, "time_away_seconds", 0) or 0,
            "paste_attempts": getattr(attempt, "paste_attempts", 0) or 0,
            "copy_attempts": getattr(attempt, "copy_attempts", 0) or 0,
            "fullscreen_exits": getattr(attempt, "fullscreen_exits", 0) or 0,
            "burst_flags": getattr(attempt, "burst_flags", 0) or 0,
            "auto_submitted": bool(getattr(attempt, "auto_submitted", False)),
            "ai_flag": getattr(attempt, "ai_flag", None),
            "ai_notes": getattr(attempt, "ai_notes", None),
        },
    }


@router.post("/{attempt_id}")
async def submit_marks(attempt_id: int, data: SubmitMarksIn, marker: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    attempt, test = await _load_for_marking(attempt_id, marker, db)
    if attempt.status == "graded":
        raise HTTPException(400, "This attempt has already been marked.")

    per_q = [m.model_dump() for m in data.marks]
    score, results = finalize_written_marks(test.questions, per_q, attempt.answers or [])
    # keep the student's uploaded answer photos visible on the graded result
    answer_images = attempt.answer_images or []
    for i, row in enumerate(results):
        row["answer_images"] = answer_images[i] if i < len(answer_images) else []
    grade = estimate_grade(score, test.level)

    attempt.results = results
    attempt.score = score
    attempt.grade = grade
    attempt.status = "graded"
    attempt.marked_by = marker.id

    # award the student XP now that the attempt is graded (streak left untouched —
    # marking can happen days later, so it shouldn't rewrite the student's streak)
    student = (await db.execute(select(User).where(User.id == attempt.student_id))).scalar_one_or_none()
    if student:
        student.xp += int(score / 10) + (5 if score >= 80 else 0)

    await db.commit()

    # Notify the student their work has been marked (best-effort).
    if student:
        try:
            await send_marked_email(student, test.title, score, grade)
        except Exception:
            pass

    return {"attempt_id": attempt.id, "status": "graded", "score": score, "grade": grade}


# ── The attempt as one PDF (download, or emailed to the marker) ───────────────

async def _attempt_pdf(attempt_id: int, marker: User, db: AsyncSession):
    from services import handin_pdf
    data = await get_attempt(attempt_id, marker, db)   # same checks and the same view the marker sees
    attempt, test = await _load_for_marking(attempt_id, marker, db)
    pdf = await run_in_threadpool(lambda: handin_pdf.build_attempt(
        student=data["student"], title=data["test_title"] or "Test", subject=data["subject"], level=data["level"],
        submitted_at=attempt.completed_at, time_taken=data["time_taken_seconds"], questions=data["questions"]))
    return pdf, handin_pdf.filename(data["student"], data["test_title"] or "Test"), data, attempt


@router.get("/{attempt_id}/pdf")
async def attempt_pdf(attempt_id: int, marker: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    pdf, fname, *_ = await _attempt_pdf(attempt_id, marker, db)
    return Response(pdf, media_type="application/pdf", headers={
        "Content-Disposition": f'attachment; filename="{fname}"', "Cache-Control": "no-store, private"})


class EmailPdfIn(BaseModel):
    to: str | None = None   # empty = the marker's own inbox


@router.post("/{attempt_id}/email")
async def email_attempt(attempt_id: int, data: EmailPdfIn, marker: User = Depends(require_teacher),
                        db: AsyncSession = Depends(get_db)):
    """Email the written answers as one PDF (cover with marks table, each question with the student's
    answer and photos, mark scheme at the end) so they can be marked properly on paper or in a PDF app."""
    from html import escape
    pdf, fname, d, attempt = await _attempt_pdf(attempt_id, marker, db)
    total = sum(int(q.get("marks") or 0) for q in d["questions"])
    photos = sum(len(q.get("answer_images") or []) for q in d["questions"])
    submitted = attempt.completed_at.strftime("%d %b %Y, %H:%M UTC") if attempt.completed_at else "-"
    try:
        to = await send_work_pdf(
            marker, data.to, f"[Notenix] To mark: {d['student']} · {d['test_title']}",
            f"{d['student']}: {d['test_title']}",
            [("Student", d["student"]), ("Test", d["test_title"] or "Test"),
             ("Subject", " · ".join(x for x in (d.get("subject"), d.get("level")) if x) or "-"),
             ("Submitted", submitted), ("Questions", f"{len(d['questions'])} ({total} marks)"),
             ("Answer photos", str(photos))],
            f"{escape(d['student'])}'s written answers are attached as a PDF: a cover with a marks table, "
            f"each question with the answer and a mark box, then the mark scheme.",
            "", "/marking", fname, pdf)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return {"sent_to": to, "filename": fname, "size_kb": len(pdf) // 1024}
