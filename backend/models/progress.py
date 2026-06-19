from sqlalchemy import Column, String, Integer, Float, DateTime, JSON
from sqlalchemy.sql import func
from database import Base
import uuid


class SubjectProgress(Base):
    __tablename__ = "subject_progress"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=False)
    level = Column(String, nullable=False)
    exam_board = Column(String, nullable=False)

    total_quizzes = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    best_score = Column(Float, default=0.0)
    topic_scores = Column(JSON, default=dict)
    time_spent_seconds = Column(Integer, default=0)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Badge(Base):
    __tablename__ = "badges"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    badge_type = Column(String, nullable=False)
    badge_name = Column(String, nullable=False)
    description = Column(String)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
