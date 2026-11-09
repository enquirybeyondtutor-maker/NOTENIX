from datetime import datetime
from sqlalchemy import UniqueConstraint, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
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
    # Rate-limits display-name changes (once per cooldown window).
    name_changed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    plan: Mapped[str] = mapped_column(String(20), default="free")  # free | pro
    # Set when Pro is bought by bank transfer; the plan drops back to free after this.
    # NULL = no expiry (e.g. Pro granted by hand).
    pro_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Beyond Tutors-issued access. NULL = no expiry (older self-signup accounts, staff).
    # access_kind: trial (free during the trial class) | paid (£49/year subscription).
    access_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    access_kind: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # WhatsApp number (digits only) from the free test-request form; one free test per number.
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    # Bumped on student login and on admin password reset; tokens carrying an older
    # version stop working, so one student account = one active sign-in.
    token_version: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    # Parent activation for Beyond Tutors-issued student accounts. True until the parent
    # signs in with the issued ID, enters their email + phone and confirms the email OTP.
    needs_activation: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    parent_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    parent_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    activated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # When the parent ticked "I agree" (£49/yr billed by Beyond Tutors on their next invoice).
    terms_accepted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Currency Beyond Tutors bills this student in (GBP, AED, USD…), and the exact price
    # shown in the terms the parent agreed to, e.g. "AED 229 per year".
    billing_currency: Mapped[str | None] = mapped_column(String(3), nullable=True)
    terms_price: Mapped[str | None] = mapped_column(String(40), nullable=True)
    # Notenix KS3: school year (7/8/9) when the student is on KS3, when their free trial
    # started, and which parent emails of the trial sequence have gone out.
    ks3_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Notenix SAT: when they joined, their test date (YYYY-MM-DD) and target score.
    sat_since: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    sat_test_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    sat_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sat_emails: Mapped[list | None] = mapped_column(JSON, nullable=True)   # weekly progress emails sent (keys)
    # The student's own inbox for homework / class-notes updates (their login ID is not a mailbox).
    notify_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Doubt Help / Ask a Tutor (services/doubt.py): plan trial|doubt|plus, when it ends, the student's
    # Singapore level (Sec 1 .. JC 2) and which plan emails have gone out.
    help_plan: Mapped[str | None] = mapped_column(String(20), nullable=True)
    help_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    sg_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    help_emails: Mapped[list | None] = mapped_column(JSON, nullable=True)
    notify_email_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ks3_trial_started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ks3_emails: Mapped[list | None] = mapped_column(JSON, nullable=True)
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
    level: Mapped[str] = mapped_column(String(20), default="GCSE")       # GCSE | A-Level | SAT | ESAT | CBSE | …
    exam_board: Mapped[str] = mapped_column(String(40), default="AQA")
    difficulty: Mapped[str] = mapped_column(String(20), default="medium")
    mode: Mapped[str] = mapped_column(String(20), default="mcq", server_default="mcq")  # mcq | written
    kind: Mapped[str] = mapped_column(String(20), default="test", server_default="test")  # test | homework
    is_library: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")  # shared self-practice library
    questions: Mapped[list] = mapped_column(JSON)                        # full snapshot w/ answers
    num_questions: Mapped[int] = mapped_column(Integer, default=0)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)  # timed sitting
    share_token: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True, index=True)  # public join link
    # KS3 programme slot, e.g. "y7-baseline", "y7-ht1"; tests with a slot are handed out automatically.
    ks3_slot: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
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
    # Server-anchored exam clock: set when the student first opens the test so the
    # countdown can't be reset by closing/reopening the tab.
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Autosaved in-progress text answers so a resumed sitting isn't blank.
    draft_answers: Mapped[list | None] = mapped_column(JSON, nullable=True)
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
    # seconds spent on each question, aligned to the question order
    question_times: Mapped[list | None] = mapped_column(JSON, nullable=True)
    results: Mapped[list | None] = mapped_column(JSON, nullable=True)    # per-question breakdown
    score: Mapped[float] = mapped_column(Float, default=0.0)
    grade: Mapped[str | None] = mapped_column(String(8), nullable=True)  # estimated grade
    # graded (MCQ or Pro AI-marked) | awaiting_marking (non-Pro written, pending human marking)
    status: Mapped[str] = mapped_column(String(20), default="graded", server_default="graded", index=True)
    marked_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)  # teacher/admin who marked
    # ── Integrity / anti-cheat signals captured during the sitting ──
    focus_lost_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")   # tab/window switches
    time_away_seconds: Mapped[int] = mapped_column(Integer, default=0, server_default="0")   # total time off-tab
    paste_attempts: Mapped[int] = mapped_column(Integer, default=0, server_default="0")       # blocked paste events
    copy_attempts: Mapped[int] = mapped_column(Integer, default=0, server_default="0")        # blocked copy events
    fullscreen_exits: Mapped[int] = mapped_column(Integer, default=0, server_default="0")     # left fullscreen mid-exam
    burst_flags: Mapped[int] = mapped_column(Integer, default=0, server_default="0")          # returned then dumped a big answer
    auto_submitted: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")  # finalized by the sweep
    # Teacher-flagged as unreliable (e.g. a timing glitch) — left out of averages, timing and reports.
    excluded_from_analysis: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")
    ai_flag: Mapped[str | None] = mapped_column(String(20), nullable=True)   # likely_ai | likely_human | uncertain
    ai_notes: Mapped[str | None] = mapped_column(Text, nullable=True)        # examiner-facing AI-check reasoning
    time_taken_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # set when the student's raw response (answers + photos) is purged by retention policy
    purged_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


# ─────────────────────────────────────────────────────────────────────────────
# Request-a-test service + manual (bank transfer / Wise) payments
# ─────────────────────────────────────────────────────────────────────────────

class TestRequest(Base):
    """A student asks the team for a test; an admin assigns one and the team marks it.
    status: awaiting_payment → payment_claimed → open → assigned (or cancelled).
    Free requests (request_price = 0) start at `open`."""
    __tablename__ = "test_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    exam: Mapped[str] = mapped_column(String(40))                     # SAT | ESAT | CBSE | …
    subject: Mapped[str | None] = mapped_column(String(120), nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)  # topics, tier, target score…
    preferred_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open", index=True)
    price: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(3), default="GBP")
    assignment_id: Mapped[int | None] = mapped_column(ForeignKey("test_assignments.id"), nullable=True)
    admin_note: Mapped[str | None] = mapped_column(Text, nullable=True)  # shown to the student
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Payment(Base):
    """A student's claim that they paid by bank transfer (Wise etc.). Nothing is charged
    automatically: an admin checks the bank account and confirms or rejects."""
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    purpose: Mapped[str] = mapped_column(String(20))                   # pro | test_request
    request_id: Mapped[int | None] = mapped_column(ForeignKey("test_requests.id"), nullable=True)
    reference: Mapped[str] = mapped_column(String(40), index=True)     # what the payer puts on the transfer
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(3))
    paid_via: Mapped[str | None] = mapped_column(String(80), nullable=True)   # which account they used
    payer_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    payer_note: Mapped[str | None] = mapped_column(Text, nullable=True)       # transfer id, amount sent…
    status: Mapped[str] = mapped_column(String(20), default="claimed", index=True)  # claimed | confirmed | rejected
    course: Mapped[str | None] = mapped_column(String(60), nullable=True)   # purpose "course": which course it buys
    reviewed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ─────────────────────────────────────────────────────────────────────────────
# Class notes: a teacher uploads notes (text and/or one file) and shares them
# with specific students.
# ─────────────────────────────────────────────────────────────────────────────

class ClassNote(Base):
    __tablename__ = "class_notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    subject: Mapped[str | None] = mapped_column(String(80), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # data URI (PDF/image). Deferred: it can be ~12 MB, so it is only loaded on purpose.
    file_data: Mapped[str | None] = mapped_column(Text, nullable=True, deferred=True)
    has_file: Mapped[bool] = column_property(file_data.isnot(None))
    # notes | homework. Homework carries a due date; class_date links it to a lesson.
    kind: Mapped[str] = mapped_column(String(20), default="notes", server_default="notes")
    due_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    class_date: Mapped[str | None] = mapped_column(String(10), nullable=True)  # YYYY-MM-DD
    # Notenix KS3 notes library: shared automatically with KS3 students of this year.
    ks3_year: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    ks3_key: Mapped[str | None] = mapped_column(String(60), nullable=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NoteShare(Base):
    __tablename__ = "note_shares"

    id: Mapped[int] = mapped_column(primary_key=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("class_notes.id"), index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # student first opened it


class SatAttempt(Base):
    """A sitting of a Notenix SAT form (services/sat.py): a full adaptive mock or the
    diagnostic (saved when a visitor who took it signs up). stage = index of the current
    module; route = {"rw": "e"|"h", "m": ...} once module 1 of a section is done."""
    __tablename__ = "sat_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    form: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(20), default="in_progress")  # in_progress | done
    stage: Mapped[int] = mapped_column(Integer, default=0)
    route: Mapped[dict] = mapped_column(JSON, default=dict)
    answers: Mapped[dict] = mapped_column(JSON, default=dict)     # {module_key: {question_id: answer}}
    marked: Mapped[dict] = mapped_column(JSON, default=dict)      # {module_key: [question_id, ...]}
    module_started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # None = on a break
    rw_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    math_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class SatDrillAnswer(Base):
    """One answer in a Notenix SAT skill drill (latest answer per question counts for mastery)."""
    __tablename__ = "sat_drill_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    question_id: Mapped[str] = mapped_column(String(80))
    skill: Mapped[str] = mapped_column(String(80))     # drill slug, e.g. "boundaries"
    correct: Mapped[bool] = mapped_column(Boolean, default=False)
    answered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class ExamAttempt(Base):
    """A sitting of a practice test or diagnostic in the exam engine (services/exams.py),
    e.g. TMUA. stage = index into the form's stages; scores = {"p1": 5.6, ..., "total": 5.9}."""
    __tablename__ = "exam_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    exam: Mapped[str] = mapped_column(String(20), index=True)
    form: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(20), default="in_progress")  # in_progress | done
    stage: Mapped[int] = mapped_column(Integer, default=0)
    answers: Mapped[dict] = mapped_column(JSON, default=dict)     # {module_key: {question_id: answer}}
    marked: Mapped[dict] = mapped_column(JSON, default=dict)      # {module_key: [question_id, ...]}
    module_started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # None = between modules
    scores: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    total_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ExamDrillAnswer(Base):
    """One answer in an exam-engine skill drill (latest answer per question counts)."""
    __tablename__ = "exam_drill_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    exam: Mapped[str] = mapped_column(String(20), index=True)
    question_id: Mapped[str] = mapped_column(String(80))
    skill: Mapped[str] = mapped_column(String(80))     # drill slug
    correct: Mapped[bool] = mapped_column(Boolean, default=False)
    answered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class ExamGoal(Base):
    """A student's test date and target for one exam, and the weekly emails already sent."""
    __tablename__ = "exam_goals"
    __table_args__ = (UniqueConstraint("user_id", "exam", name="uq_exam_goal_user_exam"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    exam: Mapped[str] = mapped_column(String(20))
    test_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    target: Mapped[float | None] = mapped_column(Float, nullable=True)
    emails: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Enrolment(Base):
    """A course a student holds (services/courses.py), e.g. "igcse-chemistry" or "tmua",
    each with its own end date. Students with none are unrestricted (pre-course accounts)."""
    __tablename__ = "enrolments"
    __table_args__ = (UniqueConstraint("user_id", "course", name="uq_enrolment_user_course"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    course: Mapped[str] = mapped_column(String(60))
    kind: Mapped[str] = mapped_column(String(20), default="paid")      # trial | paid
    until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # None = no end date
    payment_id: Mapped[int | None] = mapped_column(ForeignKey("payments.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class HomeworkSubmission(Base):
    """A student's hand-in for worksheet homework (a ClassNote with kind="homework"):
    photos of their working, then the tutor's mark and feedback."""
    __tablename__ = "homework_submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("class_notes.id"), index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    images: Mapped[list] = mapped_column(JSON)                         # compressed JPEG data URIs
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    mark: Mapped[str | None] = mapped_column(String(40), nullable=True)  # e.g. "7/10" or "Good"
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    marked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    marked_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)


class NotePage(Base):
    """A note's file pre-rendered to one plain JPEG per page (students see these,
    watermarked per request). Built once, in the background, after upload."""
    __tablename__ = "note_pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("class_notes.id"), index=True)
    page: Mapped[int] = mapped_column(Integer)
    data: Mapped[bytes] = mapped_column(LargeBinary)


class HelpRequest(Base):
    """KS3 homework help: a student sends a school homework question (photos + text)
    and a Beyond Tutors tutor replies with a worked hint."""
    __tablename__ = "help_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    subject: Mapped[str] = mapped_column(String(40))
    question: Mapped[str | None] = mapped_column(Text, nullable=True)
    images: Mapped[list | None] = mapped_column(JSON, nullable=True)        # compressed JPEG data URIs
    status: Mapped[str] = mapped_column(String(20), default="open", index=True)  # open | answered
    reply: Mapped[str | None] = mapped_column(Text, nullable=True)
    reply_images: Mapped[list | None] = mapped_column(JSON, nullable=True)
    replied_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    replied_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
