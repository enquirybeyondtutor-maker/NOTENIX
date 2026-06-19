from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    level = Column(String, nullable=False)       # gcse | a_level
    exam_board = Column(String, nullable=False)  # AQA | Edexcel | OCR | Cambridge
    num_questions = Column(Integer, nullable=False)
    difficulty = Column(String, default="mixed")

    questions = Column(JSON, nullable=False)
    answers = Column(JSON, nullable=True)
    score = Column(Float, nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    is_completed = Column(Boolean, default=False)
    is_mock_exam = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="quiz_attempts")
    analysis = relationship("QuizAnalysis", back_populates="attempt", uselist=False, cascade="all, delete-orphan")


class QuizAnalysis(Base):
    __tablename__ = "quiz_analyses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    attempt_id = Column(String, ForeignKey("quiz_attempts.id"), nullable=False)

    overall_score = Column(Float)
    strength_areas = Column(JSON)
    weak_areas = Column(JSON)
    question_breakdown = Column(JSON)
    ai_feedback = Column(Text)
    improvement_tips = Column(JSON)
    estimated_grade = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    attempt = relationship("QuizAttempt", back_populates="analysis")


class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    week_start = Column(String, nullable=False)
    plan_data = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="study_plans")


class SRSCard(Base):
    __tablename__ = "srs_cards"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    subtopic = Column(String, nullable=True)
    level = Column(String, nullable=False)
    ease_factor = Column(Float, default=2.5)
    interval_days = Column(Integer, default=1)
    repetitions = Column(Integer, default=0)
    due_date = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_reviewed_at = Column(DateTime(timezone=True), nullable=True)
