"""Student endpoints: view assigned tests, sit them, submit, see results."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from database import get_db
from models import User, Test, TestAssignment, TestAttempt
from security import get_current_user, ai_marks_for
from services.grading import grade_mcq, grade_written, estimate_grade, _pending_written_results

router = APIRouter(prefix="/tests", tags=["student-tests"])


class SubmitIn(BaseModel):
    answers: list
    # written only: per-question list of uploaded answer photos (compressed JPEG data URIs)
    answer_images: list[list[str]] | None = None
    time_taken_seconds: int | None = None


# Cap embedded answer photos so they don't bloat the attempts row.
_MAX_ANSWER_IMAGES_PER_Q = 4
_MAX_ANSWER_IMAGE_CHARS = 1_600_000        # ~1.2 MB per photo (base64)
_MAX_ANSWER_IMAGES_TOTAL_CHARS = 18_000_000  # whole submission


def _sanitize_answer_images(answer_images, n_questions: int) -> list[list[str]]:
    """Validate/trim uploaded answer photos: keep only data-URI images, cap count per
    question and total payload. Returns a per-question list aligned to the questions."""
    out: list[list[str]] = [[] for _ in range(n_questions)]
    if not answer_images:
        return out
    total = 0
    for i in range(min(len(answer_images), n_questions)):
        imgs = answer_images[i] or []
        kept: list[str] = []
        for img in imgs[:_MAX_ANSWER_IMAGES_PER_Q]:
            if not isinstance(img, str) or not img.startswith("data:image/"):
                continue
            if len(img) > _MAX_ANSWER_IMAGE_CHARS:
                raise HTTPException(400, "One of your photos is too large. Please retake or use a smaller image.")
            total += len(img)
            if total > _MAX_ANSWER_IMAGES_TOTAL_CHARS:
                raise HTTPException(400, "Your uploaded photos are too large in total. Please remove some and try again.")
            kept.append(img)
        out[i] = kept
    return out


@router.post("/join/{token}")
async def join_by_link(token: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Self-enrol into a test via a teacher's share link.
    Returns the assignment_id (existing or newly created) so the client can open it."""
    test = (await db.execute(select(Test).where(Test.share_token == token))).scalar_one_or_none()
    if not test:
        raise HTTPException(404, "This test link is invalid or has been disabled.")

    assignment = (await db.execute(
        select(TestAssignment).where(
            TestAssignment.test_id == test.id, TestAssignment.student_id == user.id
        )
    )).scalar_one_or_none()

    if not assignment:
        assignment = TestAssignment(
            test_id=test.id, student_id=user.id, assigned_by=test.owner_id,
            class_label="Via link",
        )
        db.add(assignment)
        await db.commit()
        await db.refresh(assignment)

    attempt = (await db.execute(
        select(TestAttempt).where(TestAttempt.assignment_id == assignment.id)
    )).scalar_one_or_none()

    return {
        "assignment_id": assignment.id,
        "title": test.title,
        "already_completed": attempt is not None,
    }


@router.get("")
async def my_assignments(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """All tests assigned to the current student, with status + score."""
    rows = (await db.execute(
        select(TestAssignment, Test, User.full_name)
        .join(Test, Test.id == TestAssignment.test_id)
        .join(User, User.id == TestAssignment.assigned_by)
        .where(TestAssignment.student_id == user.id)
        .order_by(TestAssignment.created_at.desc())
    )).all()

    assignment_ids = [a.id for a, _, _ in rows]
    attempts = {}
    if assignment_ids:
        att = (await db.execute(
            select(TestAttempt).where(TestAttempt.assignment_id.in_(assignment_ids))
        )).scalars().all()
        attempts = {a.assignment_id: a for a in att}

    out = []
    for a, t, teacher_name in rows:
        at = attempts.get(a.id)
        pending = bool(at and getattr(at, "status", "graded") == "awaiting_marking")
        out.append({
            "assignment_id": a.id,
            "test_id": t.id,
            "title": t.title,
            "subject": t.subject,
            "topic": t.topic,
            "level": t.level,
            "exam_board": t.exam_board,
            "mode": getattr(t, "mode", "mcq"),
            "num_questions": t.num_questions,
            "duration_minutes": t.duration_minutes,
            "class_label": a.class_label,
            "assigned_by": teacher_name,
            "due_at": a.due_at.isoformat() if a.due_at else None,
            "status": "completed" if at else "assigned",
            "marking_status": getattr(at, "status", None) if at else None,
            "score": None if (not at or pending) else at.score,
            "grade": None if (not at or pending) else at.grade,
            "completed_at": at.completed_at.isoformat() if at and at.completed_at else None,
        })
    return out


async def _load_assignment(assignment_id: int, user: User, db: AsyncSession):
    row = (await db.execute(
        select(TestAssignment, Test)
        .join(Test, Test.id == TestAssignment.test_id)
        .where(TestAssignment.id == assignment_id, TestAssignment.student_id == user.id)
    )).first()
    if not row:
        raise HTTPException(404, "Assignment not found")
    return row  # (assignment, test)


@router.get("/{assignment_id}")
async def get_test_to_attempt(assignment_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    assignment, test = await _load_assignment(assignment_id, user, db)

    existing = (await db.execute(
        select(TestAttempt).where(TestAttempt.assignment_id == assignment_id)
    )).scalar_one_or_none()
    if existing:
        raise HTTPException(400, "You have already completed this test.")

    mode = getattr(test, "mode", "mcq")
    if mode == "written":
        # written questions: marks visible, mark scheme hidden
        safe = [{"question": q.get("question"), "marks": q.get("marks"), "image": q.get("image")} for q in test.questions]
    else:
        # MCQ questions WITHOUT answers/explanations
        safe = [{"question": q.get("question"), "options": q.get("options"), "image": q.get("image")} for q in test.questions]
    return {
        "assignment_id": assignment.id,
        "test_id": test.id,
        "title": test.title,
        "subject": test.subject,
        "topic": test.topic,
        "level": test.level,
        "exam_board": test.exam_board,
        "mode": mode,
        "duration_minutes": test.duration_minutes,
        "due_at": assignment.due_at.isoformat() if assignment.due_at else None,
        "questions": safe,
    }


@router.post("/{assignment_id}/submit")
async def submit_test(assignment_id: int, data: SubmitIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    assignment, test = await _load_assignment(assignment_id, user, db)

    existing = (await db.execute(
        select(TestAttempt).where(TestAttempt.assignment_id == assignment_id)
    )).scalar_one_or_none()
    if existing:
        raise HTTPException(400, "You have already completed this test.")

    mode = getattr(test, "mode", "mcq")

    # Answer photos (written only). Their presence forces human marking — AI can't
    # reliably grade handwriting — even for Pro students.
    answer_images = _sanitize_answer_images(data.answer_images, len(test.questions)) if mode == "written" else []
    has_photos = any(imgs for imgs in answer_images)

    # ── Written test that isn't AI-marked (non-Pro OR any photo answers): human marking. ──
    if mode == "written" and (not ai_marks_for(user) or has_photos):
        results = _pending_written_results(test.questions, data.answers)
        for i, row in enumerate(results):
            row["answer_images"] = answer_images[i] if i < len(answer_images) else []
        attempt = TestAttempt(
            assignment_id=assignment.id, test_id=test.id, student_id=user.id,
            answers=data.answers, answer_images=answer_images, results=results,
            score=0.0, grade=None,
            status="awaiting_marking", time_taken_seconds=data.time_taken_seconds,
        )
        db.add(attempt)
        assignment.status = "completed"
        await db.commit()
        await db.refresh(attempt)
        return {
            "assignment_id": assignment.id,
            "status": "awaiting_marking",
            "mode": "written",
            "message": "Your answers were submitted and will be marked by your teacher.",
            "results": results,
        }

    # ── Auto-marked: MCQ (string compare) or written (Pro AI marking). ──
    if mode == "written":
        score, results = await grade_written(test.questions, data.answers, test.subject)
    else:
        score, results = grade_mcq(test.questions, data.answers)
    grade = estimate_grade(score, test.level)

    attempt = TestAttempt(
        assignment_id=assignment.id, test_id=test.id, student_id=user.id,
        answers=data.answers, results=results, score=score, grade=grade,
        status="graded", time_taken_seconds=data.time_taken_seconds,
    )
    db.add(attempt)
    assignment.status = "completed"

    # light gamification, consistent with quiz flow
    xp = int(score / 10) + (5 if score >= 80 else 0)
    today = datetime.utcnow().date()
    last = user.last_active.date() if user.last_active else None
    if last == today:
        user.streak = max(user.streak, 1)
    elif last == today - timedelta(days=1):
        user.streak += 1
    else:
        user.streak = 1
    user.last_active = datetime.utcnow()
    user.xp += xp

    await db.commit()
    await db.refresh(attempt)

    return {
        "assignment_id": assignment.id,
        "status": "graded",
        "mode": mode,
        "score": score,
        "grade": grade,
        "xp_earned": xp,
        "results": results,
    }


@router.get("/{assignment_id}/result")
async def get_result(assignment_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    assignment, test = await _load_assignment(assignment_id, user, db)
    attempt = (await db.execute(
        select(TestAttempt).where(TestAttempt.assignment_id == assignment_id)
    )).scalar_one_or_none()
    if not attempt:
        raise HTTPException(404, "No attempt found for this test.")

    pending = getattr(attempt, "status", "graded") == "awaiting_marking"
    return {
        "title": test.title,
        "subject": test.subject,
        "topic": test.topic,
        "level": test.level,
        "mode": getattr(test, "mode", "mcq"),
        "status": getattr(attempt, "status", "graded"),
        "score": None if pending else attempt.score,
        "grade": None if pending else attempt.grade,
        "time_taken_seconds": attempt.time_taken_seconds,
        "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None,
        "results": attempt.results,
    }
