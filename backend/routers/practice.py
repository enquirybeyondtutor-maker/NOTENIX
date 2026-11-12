"""Student written-answer practice: a shared library of past-paper questions published by the team.
(Uploading your own paper used AI to pull out the questions and is retired.) Gated to Pro + admin-whitelisted accounts + teachers/admins.

Each entry point creates a written `Test` + a self-`TestAssignment`, then hands the
student off to the existing `/tests/{assignment_id}` attempt → submit → result flow.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import User, Test, TestAssignment, TestAttempt
from security import require_write_practice
from services import courses as course_svc

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

    mine = await course_svc.live_courses(user, db)  # only papers for the student's courses
    tests = [t for t in tests if course_svc.allows(mine, t.level, t.subject, t.exam_board)]

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
    if not course_svc.allows(await course_svc.live_courses(user, db), test.level, test.subject, test.exam_board):
        raise HTTPException(403, course_svc.locked_message(test.level, test.subject, test.exam_board))
    assignment = await _self_assignment(test, user, db)
    attempt = (await db.execute(
        select(TestAttempt).where(TestAttempt.assignment_id == assignment.id)
    )).scalar_one_or_none()
    return {"assignment_id": assignment.id, "already_completed": attempt is not None}


@router.post("/upload")
async def upload_paper(user: User = Depends(require_write_practice)):
    """Retired: this used AI to read a student's own paper. Students send a paper to a tutor via /request instead."""
    raise HTTPException(410, "Uploading your own paper has been retired. Use 'Get your past paper marked' to send it to a tutor.")
