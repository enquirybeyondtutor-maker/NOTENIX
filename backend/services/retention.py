"""Data-retention purge: student responses are kept only for a limited window.

`response_retention_days` after a student submits, we strip their raw response — the
typed answers and any uploaded answer photos — from the record. Marks, grades, and
examiner feedback are preserved, so teachers keep their records and students keep their
results; only the student's own submitted content is deleted.

Run periodically from the app lifespan (see main.py).
"""
from datetime import datetime, timedelta
from sqlalchemy import select
from database import SessionLocal
from models import TestAttempt, QuizSession
from config import settings


async def purge_old_responses() -> int:
    """Purge student responses older than the retention window. Returns rows affected."""
    days = settings.response_retention_days
    if days <= 0:  # retention disabled
        return 0
    cutoff = datetime.utcnow() - timedelta(days=days)
    now = datetime.utcnow()
    affected = 0

    async with SessionLocal() as db:
        # Assigned / written / photo attempts — drop raw answers + photos, keep marks & feedback.
        attempts = (await db.execute(
            select(TestAttempt).where(
                TestAttempt.completed_at < cutoff,
                TestAttempt.purged_at.is_(None),
            )
        )).scalars().all()
        for a in attempts:
            a.answers = None
            a.answer_images = None
            if a.results:
                cleaned = []
                for row in a.results:
                    row = dict(row)
                    row.pop("your_answer", None)
                    row.pop("answer_images", None)
                    cleaned.append(row)
                a.results = cleaned
            a.purged_at = now
            affected += 1

        # Self-serve quizzes — drop the student's submitted answers, keep the score.
        quizzes = (await db.execute(
            select(QuizSession).where(
                QuizSession.created_at < cutoff,
                QuizSession.answers.isnot(None),
            )
        )).scalars().all()
        for s in quizzes:
            s.answers = None
            affected += 1

        if affected:
            await db.commit()
    return affected
