"""Student written-answer practice: a shared library of past-paper questions and
self-uploaded PDFs. Gated to Pro + admin-whitelisted accounts + teachers/admins.

Each entry point creates a written `Test` + a self-`TestAssignment`, then hands the
student off to the existing `/tests/{assignment_id}` attempt → submit → result flow.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database import get_db
from models import User, Test, TestAssignment, TestAttempt
from security import require_write_practice, ai_marks_for
from services import ai
from services.pdf_extract import render_pages_to_png, crop_figures

router = APIRouter(prefix="/practice", tags=["practice"])


async def _self_assignment(test: Test, user: User, db: AsyncSession) -> TestAssignment:
    """Create (or return existing) a self-assignment so `test` flows through /tests/*."""
    assignment = (await db.execute(
        select(TestAssignment).where(
            TestAssignment.test_id == test.id, TestAssignment.student_id == user.id
        )
    )).scalar_one_or_none()
    if not assignment:
        assignment = TestAssignment(
            test_id=test.id, student_id=user.id, assigned_by=user.id,
            class_label="Self-practice",
        )
        db.add(assignment)
        await db.commit()
        await db.refresh(assignment)
    return assignment


@router.get("/library")
async def library(user: User = Depends(require_write_practice), db: AsyncSession = Depends(get_db)):
    """Shared library of written practice papers (admin-published)."""
    tests = (await db.execute(
        select(Test).where(
            Test.mode == "written", Test.is_library == True, Test.is_archived == False  # noqa: E712
        ).order_by(Test.created_at.desc())
    )).scalars().all()

    # which of these the student has already started/finished
    test_ids = [t.id for t in tests]
    done: dict[int, TestAttempt] = {}
    if test_ids:
        rows = (await db.execute(
            select(TestAssignment, TestAttempt)
            .join(TestAttempt, TestAttempt.assignment_id == TestAssignment.id)
            .where(TestAssignment.student_id == user.id, TestAssignment.test_id.in_(test_ids))
        )).all()
        done = {a.test_id: at for a, at in rows}

    out = []
    for t in tests:
        at = done.get(t.id)
        total_marks = sum(int(q.get("marks") or 0) for q in (t.questions or []))
        out.append({
            "test_id": t.id, "title": t.title, "subject": t.subject, "topic": t.topic,
            "level": t.level, "exam_board": t.exam_board,
            "num_questions": t.num_questions, "total_marks": total_marks,
            "attempted": at is not None,
            "marking_status": getattr(at, "status", None) if at else None,
        })
    return out


@router.post("/library/{test_id}/start")
async def start_library(test_id: int, user: User = Depends(require_write_practice), db: AsyncSession = Depends(get_db)):
    """Self-enrol into a library paper and return the assignment to open."""
    test = (await db.execute(
        select(Test).where(
            Test.id == test_id, Test.mode == "written", Test.is_library == True  # noqa: E712
        )
    )).scalar_one_or_none()
    if not test:
        raise HTTPException(404, "Practice paper not found.")
    assignment = await _self_assignment(test, user, db)
    attempt = (await db.execute(
        select(TestAttempt).where(TestAttempt.assignment_id == assignment.id)
    )).scalar_one_or_none()
    return {"assignment_id": assignment.id, "already_completed": attempt is not None}


@router.post("/upload")
async def upload_paper(
    file: UploadFile = File(...),
    subject: str = Form("general"),
    level: str = Form("GCSE"),
    title: str = Form(""),
    num_questions: int = Form(6),
    user: User = Depends(require_write_practice),
    db: AsyncSession = Depends(get_db),
):
    """Upload a past-paper PDF → extract its written questions → start a private
    practice test the student can answer immediately."""
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Please upload a PDF file.")
    data = await file.read()
    if len(data) > 15 * 1024 * 1024:
        raise HTTPException(400, "PDF too large (max 15 MB).")

    n = max(1, min(num_questions, 20))
    try:
        images = render_pages_to_png(data, max_pages=8)
    except Exception:
        images = []
    if not images:
        raise HTTPException(422, "Couldn't read that PDF. It may be corrupted or password-protected.")

    questions = ai.extract_written_from_images(images, subject, level, n)
    if not questions:
        raise HTTPException(502, "Couldn't find written questions in that paper. Try a clearer PDF.")
    questions = crop_figures(data, questions)

    test = Test(
        owner_id=user.id,
        title=(title.strip() or (file.filename or "Practice").rsplit(".", 1)[0])[:200],
        subject=subject, topic="Self-practice", level=level,
        exam_board="", difficulty="medium",
        mode="written", is_library=False,
        questions=questions, num_questions=len(questions),
    )
    db.add(test)
    await db.commit()
    await db.refresh(test)

    assignment = await _self_assignment(test, user, db)
    return {
        "assignment_id": assignment.id,
        "num_questions": len(questions),
        "ai_marked": ai_marks_for(user),
    }
