"""Per-course access.

A student holds one or more courses (an Enrolment each, with its own end date). A course is
either a whole admissions exam ("tmua", "tara", …) or a curriculum + subject ("igcse-chemistry",
"a-level-maths", …). Everything a student opens by themselves (practice library, quizzes,
revision papers, test requests) is limited to their live courses. Work a tutor sends them
directly (assigned tests, homework, class notes) is never limited.

Students with no enrolments at all are "unrestricted": that is how every account worked before
courses existed, so nobody loses access until the admin gives them courses.
"""
import re
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings

# Whole-exam courses: any content labelled with the exam (as its level or its subject).
EXAMS = {
    "tmua": "TMUA", "tara": "TARA", "esat": "ESAT", "sat": "SAT", "ukmt": "UKMT",
    "jee": "JEE", "neet": "NEET",
}
# Curricula: one course per subject.
CURRICULA = {
    "gcse": "GCSE", "igcse": "IGCSE", "a-level": "A-Level", "ib": "IB", "ap": "AP",
    "hsc": "HSC", "vce": "VCE", "qce": "QCE", "wace": "WACE", "ncea": "NCEA",
    "cbse": "CBSE", "icse": "ICSE",
}
SUBJECTS = {
    "maths": "Maths", "further_maths": "Further Maths", "physics": "Physics", "chemistry": "Chemistry",
    "biology": "Biology", "science": "Combined Science", "computer_science": "Computer Science",
    "economics": "Economics", "business": "Business", "accounting": "Accounting",
    "psychology": "Psychology", "geography": "Geography", "history": "History",
    "english_literature": "English Literature", "english_language": "English Language",
}

# Keyword → subject, checked in order (so "further maths" wins over "maths").
_SUBJECT_WORDS = [
    (("further math",), "further_maths"), (("math",), "maths"), (("physic",), "physics"),
    (("chem",), "chemistry"), (("bio",), "biology"), (("computer", "computing"), "computer_science"),
    (("econ",), "economics"), (("business",), "business"), (("account",), "accounting"),
    (("psych",), "psychology"), (("geog",), "geography"), (("histor",), "history"),
    (("literature", "english lit"), "english_literature"), (("english",), "english_language"),
    (("science",), "science"),
]
_LEVEL_WORDS = [  # (regex on the lowercased text, curriculum key); igcse before gcse
    (r"\bigcse\b", "igcse"), (r"\bgcse\b", "gcse"), (r"\b(a[- ]?level|as[- ]?level|ial)\b", "a-level"),
    (r"\bib\b", "ib"), (r"\bap\b", "ap"), (r"\bhsc\b", "hsc"), (r"\bvce\b", "vce"), (r"\bqce\b", "qce"),
    (r"\bwace\b|\batar\b", "wace"), (r"\bncea\b", "ncea"), (r"\bcbse\b", "cbse"), (r"\bicse\b", "icse"),
]


def catalogue() -> list[dict]:
    """Every course, grouped for pickers: admissions tests first, then each curriculum."""
    out = [{"key": k, "name": v, "group": "Admissions tests"} for k, v in EXAMS.items()]
    for ck, cn in CURRICULA.items():
        out += [{"key": f"{ck}-{sk}", "name": f"{cn} {sn}", "group": cn} for sk, sn in SUBJECTS.items()]
    return out


_NAMES = {c["key"]: c["name"] for c in catalogue()}


def course_name(key: str) -> str:
    return _NAMES.get(key, key)


def is_course(key: str) -> bool:
    return key in _NAMES


def norm_subject(text: str | None) -> str | None:
    t = re.sub(r"[^a-z0-9]+", " ", (text or "").lower())
    for words, key in _SUBJECT_WORDS:
        if any(w in t for w in words):
            return key
    return None


def _exam(text: str | None) -> str | None:
    t = re.sub(r"[^a-z0-9]+", " ", (text or "").lower())
    for key in EXAMS:
        if re.search(rf"\b{key}\b", t):
            return key
    return None


def _curriculum(text: str | None) -> str | None:
    t = (text or "").lower()
    for rx, key in _LEVEL_WORDS:
        if re.search(rx, t):
            return key
    return None


def content_course(level: str | None, subject: str | None, board: str | None = None) -> str | None:
    """The course a piece of content belongs to, e.g. ("A-Level", "TMUA") → "tmua",
    ("IGCSE", "chemistry") → "igcse-chemistry", ("GCSE", "AQA GCSE Maths") → "gcse-maths".
    Returns "<curriculum>-*" when only the curriculum is known, None when nothing is."""
    exam = _exam(subject) or _exam(level) or _exam(board)
    if exam:
        return exam
    cur = _curriculum(level) or _curriculum(board) or _curriculum(subject)
    if not cur:
        return None
    subj = norm_subject(subject) or norm_subject(board)
    return f"{cur}-{subj}" if subj else f"{cur}-*"


def allows(courses: set[str] | None, level: str | None, subject: str | None, board: str | None = None) -> bool:
    """May a student with these live courses open this content? None = unrestricted."""
    if courses is None:
        return True
    c = content_course(level, subject, board)
    if c is None:
        return False
    if c.endswith("-*"):  # curriculum known, subject not: any course in that curriculum
        return any(k.startswith(c[:-1]) for k in courses)
    if c in courses:
        return True
    # Combined Science overlaps the single sciences: its content is open to a Physics,
    # Chemistry or Biology student, and their content to a Combined Science student.
    # (Chemistry does not open Physics.)
    cur = next((k for k in CURRICULA if c.startswith(k + "-")), None)
    if not cur:
        return False
    subj = c[len(cur) + 1:]
    singles = {"physics", "chemistry", "biology"}
    if subj == "science":
        return any(f"{cur}-{s}" in courses for s in singles)
    return subj in singles and f"{cur}-science" in courses


# ── Enrolments ───────────────────────────────────────────────────────────────

def _live(e, now: datetime) -> bool:
    return e.until is None or e.until > now


async def enrolments(user_id: int, db: AsyncSession) -> list:
    from models import Enrolment
    return list((await db.execute(select(Enrolment).where(Enrolment.user_id == user_id)
                                  .order_by(Enrolment.created_at))).scalars().all())


async def live_courses(user, db: AsyncSession) -> set[str] | None:
    """The student's live course keys, or None when they are unrestricted (staff, KS3
    families, or students who have never been given a course)."""
    from security import is_admin
    if is_admin(user) or (getattr(user, "role", None) or "student") != "student" or getattr(user, "ks3_year", None):
        return None
    rows = await enrolments(user.id, db)
    if not rows:
        return None
    now = datetime.utcnow()
    return {e.course for e in rows if _live(e, now)}


def enrolment_row(e) -> dict:
    now = datetime.utcnow()
    return {"course": e.course, "name": course_name(e.course), "kind": e.kind,
            "until": e.until.isoformat() if e.until else None, "live": _live(e, now)}


def sync_access(user, rows: list) -> None:
    """Keep the account-wide access date (which the rest of Notenix checks) equal to the
    latest course end date, so a student is locked out only when every course has ended."""
    if not rows:
        return
    if any(e.until is None for e in rows):
        until = None
    else:
        until = max(e.until for e in rows)
    now = datetime.utcnow()
    live = [e for e in rows if _live(e, now)]
    user.access_kind = "paid" if any(e.kind == "paid" for e in live) else ("trial" if live else (user.access_kind or "paid"))
    user.access_until = until


async def grant(user, course: str, access: str, db: AsyncSession, until: datetime | None = None,
                payment_id: int | None = None):
    """Give (or extend) a course. access: trial | year | none (no end date) | until (a date).
    A year added to a live paid course starts from its current end, so renewing early loses nothing."""
    from models import Enrolment
    if not is_course(course):
        raise ValueError("Unknown course")
    now = datetime.utcnow()
    e = (await db.execute(select(Enrolment).where(Enrolment.user_id == user.id,
                                                   Enrolment.course == course))).scalar_one_or_none()
    if not e:
        e = Enrolment(user_id=user.id, course=course, kind="trial", created_at=now)
        db.add(e)
    if access == "trial":
        e.kind, e.until = "trial", now + timedelta(days=settings.trial_days)
    elif access == "year":
        start = e.until if (e.kind == "paid" and e.until and e.until > now) else now
        e.kind, e.until = "paid", start + timedelta(days=settings.subscription_days)
    elif access == "none":
        e.kind, e.until = "paid", None
    elif access == "until" and until:
        e.kind, e.until = "paid", until
    else:
        raise ValueError("Access must be trial, year, none or until")
    if payment_id:
        e.payment_id = payment_id
    await db.flush()
    sync_access(user, await enrolments(user.id, db))
    return e


async def revoke(user, course: str, db: AsyncSession) -> None:
    from models import Enrolment
    e = (await db.execute(select(Enrolment).where(Enrolment.user_id == user.id,
                                                   Enrolment.course == course))).scalar_one_or_none()
    if e:
        await db.delete(e)
        await db.flush()
    rows = await enrolments(user.id, db)
    if rows:
        sync_access(user, rows)


def locked_message(level: str | None, subject: str | None, board: str | None = None) -> str:
    c = content_course(level, subject, board)
    name = course_name(c) if c and not c.endswith("-*") else "this course"
    return f"{name} isn't one of your courses. Add it from My courses to unlock it."
