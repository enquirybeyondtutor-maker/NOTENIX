"""Auto-finalize expired in-progress test sittings.

The exam clock is anchored server-side (TestAssignment.started_at). If a student
starts a timed test and never submits, this sweep finalizes it once the time is up
(plus a short grace) so the test doesn't stay open forever and the teacher gets a
result. Any autosaved draft answers are used; written tests go to the marking queue.
"""
from datetime import datetime, timedelta
from sqlalchemy import select
from database import SessionLocal
from models import Test, TestAssignment, TestAttempt
from services.grading import grade_mcq, estimate_grade, _pending_written_results

_GRACE_SECONDS = 60


async def auto_submit_expired() -> int:
    """Finalize timed sittings whose time has elapsed with no submission. Returns count."""
    now = datetime.utcnow()
    finalized = 0
    async with SessionLocal() as db:
        rows = (await db.execute(
            select(TestAssignment, Test)
            .join(Test, Test.id == TestAssignment.test_id)
            .where(
                TestAssignment.started_at.isnot(None),
                TestAssignment.status != "completed",
                Test.duration_minutes.isnot(None),
                Test.duration_minutes > 0,
            )
        )).all()

        for assignment, test in rows:
            deadline = assignment.started_at + timedelta(minutes=test.duration_minutes, seconds=_GRACE_SECONDS)
            if now <= deadline:
                continue
            # guard against a race with a real submission
            existing = (await db.execute(
                select(TestAttempt).where(TestAttempt.assignment_id == assignment.id)
            )).scalar_one_or_none()
            if existing:
                assignment.status = "completed"
                continue

            answers = assignment.draft_answers or []
            mode = getattr(test, "mode", "mcq")
            if mode == "written":
                results = _pending_written_results(test.questions, answers)
                attempt = TestAttempt(
                    assignment_id=assignment.id, test_id=test.id, student_id=assignment.student_id,
                    answers=answers, results=results, score=0.0, grade=None,
                    status="awaiting_marking", auto_submitted=True,
                    time_taken_seconds=test.duration_minutes * 60,
                )
            else:
                score, results = grade_mcq(test.questions, answers)
                attempt = TestAttempt(
                    assignment_id=assignment.id, test_id=test.id, student_id=assignment.student_id,
                    answers=answers, results=results, score=score, grade=estimate_grade(score, test.level),
                    status="graded", auto_submitted=True,
                    time_taken_seconds=test.duration_minutes * 60,
                )
            db.add(attempt)
            assignment.status = "completed"
            assignment.draft_answers = None
            finalized += 1

        if rows:
            await db.commit()
    return finalized
