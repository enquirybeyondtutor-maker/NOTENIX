from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.quiz import QuizAttempt, QuizAnalysis
from models.progress import SubjectProgress, Badge
from models.user import User
from datetime import date, timedelta
import json


async def update_subject_progress(db: AsyncSession, user_id: str, attempt: QuizAttempt, analysis: dict):
    result = await db.execute(
        select(SubjectProgress).where(
            SubjectProgress.user_id == user_id,
            SubjectProgress.subject == attempt.subject,
            SubjectProgress.level == attempt.level,
            SubjectProgress.exam_board == attempt.exam_board,
        )
    )
    progress = result.scalar_one_or_none()

    if not progress:
        progress = SubjectProgress(
            user_id=user_id,
            subject=attempt.subject,
            level=attempt.level,
            exam_board=attempt.exam_board,
        )
        db.add(progress)

    progress.total_quizzes += 1
    progress.total_questions += analysis["total_questions"]
    progress.correct_answers += analysis["correct_count"]
    progress.time_spent_seconds += attempt.time_taken_seconds or 0

    all_scores = []
    if progress.total_quizzes > 1:
        prev_total = (progress.average_score * (progress.total_quizzes - 1))
        all_scores = [prev_total, analysis["overall_score"]]
        progress.average_score = (prev_total + analysis["overall_score"]) / progress.total_quizzes
    else:
        progress.average_score = analysis["overall_score"]

    if analysis["overall_score"] > progress.best_score:
        progress.best_score = analysis["overall_score"]

    topic_scores = progress.topic_scores or {}
    for subtopic, score in analysis.get("subtopic_scores", {}).items():
        if subtopic in topic_scores:
            topic_scores[subtopic] = (topic_scores[subtopic] + score) / 2
        else:
            topic_scores[subtopic] = score
    progress.topic_scores = topic_scores

    await db.commit()
    return progress


async def update_streak_and_xp(db: AsyncSession, user_id: str, score: float, num_questions: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return

    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    if user.last_activity_date == today:
        pass
    elif user.last_activity_date == yesterday:
        user.streak_days += 1
    else:
        user.streak_days = 1

    user.last_activity_date = today

    xp_earned = int(num_questions * 10 * (score / 100))
    if score >= 90:
        xp_earned = int(xp_earned * 1.5)
    user.xp_points = (user.xp_points or 0) + xp_earned

    await db.commit()
    await check_and_award_badges(db, user)
    return xp_earned


async def check_and_award_badges(db: AsyncSession, user: User):
    existing = await db.execute(select(Badge).where(Badge.user_id == user.id))
    earned_types = {b.badge_type for b in existing.scalars().all()}

    new_badges = []

    badge_map = [
        ("first_quiz", "First Steps", "Completed your first quiz!", lambda u: True),
        ("streak_7", "Week Warrior", "7-day study streak!", lambda u: (u.streak_days or 0) >= 7),
        ("streak_30", "Monthly Master", "30-day study streak!", lambda u: (u.streak_days or 0) >= 30),
        ("xp_1000", "Knowledge Seeker", "Earned 1,000 XP!", lambda u: (u.xp_points or 0) >= 1000),
        ("xp_5000", "Scholar", "Earned 5,000 XP!", lambda u: (u.xp_points or 0) >= 5000),
    ]

    for badge_type, name, desc, condition in badge_map:
        if badge_type not in earned_types and condition(user):
            badge = Badge(user_id=user.id, badge_type=badge_type, badge_name=name, description=desc)
            db.add(badge)
            new_badges.append({"type": badge_type, "name": name})

    if new_badges:
        await db.commit()
    return new_badges


async def get_dashboard_stats(db: AsyncSession, user_id: str) -> dict:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    attempts_result = await db.execute(
        select(QuizAttempt).where(QuizAttempt.user_id == user_id, QuizAttempt.is_completed == True)
        .order_by(QuizAttempt.completed_at.desc()).limit(10)
    )
    recent_attempts = attempts_result.scalars().all()

    progress_result = await db.execute(select(SubjectProgress).where(SubjectProgress.user_id == user_id))
    subject_progress = progress_result.scalars().all()

    badges_result = await db.execute(select(Badge).where(Badge.user_id == user_id))
    badges = badges_result.scalars().all()

    total_quizzes = sum(p.total_quizzes for p in subject_progress)
    total_time = sum(p.time_spent_seconds for p in subject_progress)
    avg_score = sum(p.average_score * p.total_quizzes for p in subject_progress) / max(total_quizzes, 1)

    return {
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "xp_points": user.xp_points or 0,
            "streak_days": user.streak_days or 0,
            "subscription_tier": user.subscription_tier,
            "free_quizzes_used": user.free_quizzes_used,
            "free_quiz_limit": user.free_quiz_limit,
        },
        "stats": {
            "total_quizzes": total_quizzes,
            "total_time_minutes": total_time // 60,
            "average_score": round(avg_score, 1),
        },
        "subject_progress": [
            {
                "subject": p.subject,
                "level": p.level,
                "exam_board": p.exam_board,
                "total_quizzes": p.total_quizzes,
                "average_score": round(p.average_score, 1),
                "best_score": round(p.best_score, 1),
                "topic_scores": p.topic_scores or {},
            }
            for p in subject_progress
        ],
        "recent_attempts": [
            {
                "id": a.id,
                "subject": a.subject,
                "topic": a.topic,
                "score": a.score,
                "num_questions": a.num_questions,
                "completed_at": a.completed_at.isoformat() if a.completed_at else None,
            }
            for a in recent_attempts
        ],
        "badges": [{"type": b.badge_type, "name": b.badge_name, "description": b.description} for b in badges],
    }
