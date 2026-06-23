from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(120))
    plan: Mapped[str] = mapped_column(String(20), default="free")  # free | pro
    xp: Mapped[int] = mapped_column(Integer, default=0)
    streak: Mapped[int] = mapped_column(Integer, default=0)
    quiz_count: Mapped[int] = mapped_column(Integer, default=0)
    last_active: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sessions: Mapped[list["QuizSession"]] = relationship(back_populates="user")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(80), index=True)
    topic: Mapped[str] = mapped_column(String(160), index=True)
    exam_board: Mapped[str] = mapped_column(String(40), index=True)
    level: Mapped[str] = mapped_column(String(20), index=True)  # GCSE | A-Level
    qtype: Mapped[str] = mapped_column(String(20), default="mcq")  # mcq | exam
    difficulty: Mapped[str] = mapped_column(String(20), default="medium")
    question_text: Mapped[str] = mapped_column(Text)
    options: Mapped[list | None] = mapped_column(JSON, nullable=True)   # mcq only
    answer: Mapped[str | None] = mapped_column(Text, nullable=True)     # mcq correct option
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    marks: Mapped[int | None] = mapped_column(Integer, nullable=True)   # exam only
    mark_scheme: Mapped[str | None] = mapped_column(Text, nullable=True)  # exam only (AI generated)
    source_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_type: Mapped[str] = mapped_column(String(20), default="extracted")  # extracted | ai
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    subject: Mapped[str] = mapped_column(String(80))
    topic: Mapped[str] = mapped_column(String(160))
    mode: Mapped[str] = mapped_column(String(20), default="quiz")  # quiz | exam
    questions: Mapped[list] = mapped_column(JSON)   # snapshot of questions asked
    answers: Mapped[list | None] = mapped_column(JSON, nullable=True)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="sessions")
