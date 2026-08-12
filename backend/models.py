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
    role: Mapped[str] = mapped_column(String(20), default="student", server_default="student", index=True)  # student | teacher | admin
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")  # False = suspended/banned
    # Email verification (OTP). Defaults True so pre-existing accounts stay verified;
    # register() sets it False for new signups until they enter the emailed code.
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    otp_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)      # bcrypt hash of the 6-digit code
    otp_expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    otp_attempts: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    # Written-practice whitelist: admin-granted access for non-Pro accounts. Their
    # written answers are marked by hand (teacher/admin), not by AI (Pro-only).
    can_write: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
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


# ─────────────────────────────────────────────────────────────────────────────
# Assigned-test system (teacher creates → assigns → student attempts → AI marks)
# All additive: new tables auto-created by create_all on next backend start.
# ─────────────────────────────────────────────────────────────────────────────

class Test(Base):
    """A teacher-authored assessment. `questions` is the canonical content
    snapshot (includes answers/explanations) — MCQ, auto-gradable."""
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)  # teacher
    title: Mapped[str] = mapped_column(String(200))
    subject: Mapped[str] = mapped_column(String(80), index=True)
    topic: Mapped[str] = mapped_column(String(160))
    level: Mapped[str] = mapped_column(String(20), default="GCSE")       # GCSE | A-Level
    exam_board: Mapped[str] = mapped_column(String(40), default="AQA")
    difficulty: Mapped[str] = mapped_column(String(20), default="medium")
    mode: Mapped[str] = mapped_column(String(20), default="mcq", server_default="mcq")  # mcq | written
    is_library: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")  # shared self-practice library
    questions: Mapped[list] = mapped_column(JSON)                        # full snapshot w/ answers
    num_questions: Mapped[int] = mapped_column(Integer, default=0)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)  # timed sitting
    share_token: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True, index=True)  # public join link
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TestAssignment(Base):
    """A test handed to a specific student, optionally with a class label + deadline."""
    __tablename__ = "test_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    assigned_by: Mapped[int] = mapped_column(ForeignKey("users.id"))     # teacher
    class_label: Mapped[str | None] = mapped_column(String(80), nullable=True)  # e.g. "Year 11 Chem"
    due_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="assigned", index=True)  # assigned | completed
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TestAttempt(Base):
    """A student's completed sitting of an assigned test."""
    __tablename__ = "test_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    assignment_id: Mapped[int] = mapped_column(ForeignKey("test_assignments.id"), index=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    answers: Mapped[list | None] = mapped_column(JSON, nullable=True)
    # per-question list of uploaded answer photos (compressed JPEG data URIs); written only
    answer_images: Mapped[list | None] = mapped_column(JSON, nullable=True)
    results: Mapped[list | None] = mapped_column(JSON, nullable=True)    # per-question breakdown
    score: Mapped[float] = mapped_column(Float, default=0.0)
    grade: Mapped[str | None] = mapped_column(String(8), nullable=True)  # estimated grade
    # graded (MCQ or Pro AI-marked) | awaiting_marking (non-Pro written, pending human marking)
    status: Mapped[str] = mapped_column(String(20), default="graded", server_default="graded", index=True)
    marked_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)  # teacher/admin who marked
    time_taken_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
