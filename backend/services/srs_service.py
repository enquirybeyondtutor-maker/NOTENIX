"""Spaced Repetition System using SM-2 algorithm."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.quiz import SRSCard
from datetime import date, timedelta
import uuid


async def update_srs_cards(db: AsyncSession, user_id: str, attempt_data: dict, analysis: dict):
    """Create or update SRS cards based on quiz performance."""
    for item in analysis.get("question_breakdown", []):
        subtopic = item.get("subtopic", "General")
        is_correct = item.get("is_correct", False)

        result = await db.execute(
            select(SRSCard).where(
                SRSCard.user_id == user_id,
                SRSCard.subject == attempt_data["subject"],
                SRSCard.topic == attempt_data["topic"],
                SRSCard.subtopic == subtopic,
                SRSCard.level == attempt_data["level"],
            )
        )
        card = result.scalar_one_or_none()

        quality = 5 if is_correct else 1

        if card is None:
            card = SRSCard(
                user_id=user_id,
                subject=attempt_data["subject"],
                topic=attempt_data["topic"],
                subtopic=subtopic,
                level=attempt_data["level"],
                due_date=str(date.today()),
            )
            db.add(card)

        card = _sm2_update(card, quality)

    await db.commit()


def _sm2_update(card: SRSCard, quality: int) -> SRSCard:
    """SM-2 algorithm update."""
    if quality >= 3:
        if card.repetitions == 0:
            card.interval_days = 1
        elif card.repetitions == 1:
            card.interval_days = 6
        else:
            card.interval_days = round(card.interval_days * card.ease_factor)
        card.repetitions += 1
    else:
        card.repetitions = 0
        card.interval_days = 1

    card.ease_factor = max(1.3, card.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    card.due_date = str(date.today() + timedelta(days=card.interval_days))
    return card


async def get_due_cards(db: AsyncSession, user_id: str) -> list[dict]:
    """Get all SRS cards due for review today."""
    today = str(date.today())
    result = await db.execute(
        select(SRSCard).where(SRSCard.user_id == user_id, SRSCard.due_date <= today)
        .order_by(SRSCard.due_date)
    )
    cards = result.scalars().all()
    return [
        {
            "id": c.id,
            "subject": c.subject,
            "topic": c.topic,
            "subtopic": c.subtopic,
            "level": c.level,
            "due_date": c.due_date,
            "interval_days": c.interval_days,
            "ease_factor": c.ease_factor,
        }
        for c in cards
    ]
