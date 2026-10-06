"""Staff-only performance reports (downloadable PDF on the frontend) for ESAT/TMUA/etc."""
import asyncio
import secrets
import time
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, SessionLocal
from models import User, Test, TestAttempt
from security import require_teacher, is_admin
from services import report as rpt

router = APIRouter(prefix="/reports", tags=["reports"])


class BuildIn(BaseModel):
    student_id: int
    exam: str
    attempt_ids: list[int] | None = None   # default: every graded MCQ mock in this exam
    target: str = ""                        # e.g. "Cambridge Engineering"
    pronouns: str = ""                      # "he" | "she" | "they" | "" (use the first name only)
    commentary: bool = True


async def _visible_attempts(staff: User, db: AsyncSession, student_id: int | None = None):
    """(attempt, test) pairs this staff member may report on: admins see all, teachers their own tests."""
    q = (select(TestAttempt, Test).join(Test, Test.id == TestAttempt.test_id)
         .where(TestAttempt.status == "graded", Test.mode == "mcq"))
    if student_id is not None:
        q = q.where(TestAttempt.student_id == student_id)
    if not is_admin(staff):
        q = q.where(Test.owner_id == staff.id)
    return (await db.execute(q.order_by(TestAttempt.completed_at))).all()


@router.get("/candidates")
async def candidates(staff: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    """Students with graded MCQ mocks, grouped by exam family."""
    rows = await _visible_attempts(staff, db)
    by_student: dict[int, dict] = defaultdict(lambda: defaultdict(list))
    for a, t in rows:
        by_student[a.student_id][rpt.exam_key(t)].append({
            "attempt_id": a.id, "title": t.title, "score": a.score,
            "date": a.completed_at.isoformat() if a.completed_at else None,
        })
    if not by_student:
        return []
    users = {u.id: u for u in (await db.execute(select(User).where(User.id.in_(list(by_student))))).scalars()}
    out = []
    for sid, exams in by_student.items():
        u = users.get(sid)
        if not u:
            continue
        out.append({"id": sid, "full_name": u.full_name, "email": u.email,
                    "exams": [{"exam": k, "attempts": v} for k, v in sorted(exams.items())]})
    out.sort(key=lambda s: s["full_name"].lower())
    return out


async def _build(data: BuildIn, staff: User, db: AsyncSession) -> dict:
    student = (await db.execute(select(User).where(User.id == data.student_id))).scalar_one_or_none()
    if not student:
        raise HTTPException(404, "Student not found")
    rows = [(a, t) for a, t in await _visible_attempts(staff, db, data.student_id) if rpt.exam_key(t) == data.exam]
    if data.attempt_ids:
        keep = set(data.attempt_ids)
        rows = [(a, t) for a, t in rows if a.id in keep]
    if not rows:
        raise HTTPException(404, "No graded mocks found for this student and exam.")

    # Tag questions once per test (Claude, cached on the test row); papers tagged concurrently.
    tests = {t.id: t for _, t in rows}
    changed = await asyncio.gather(*(run_in_threadpool(rpt.tag_questions, t, data.exam) for t in tests.values()))
    if any(changed):
        await db.commit()

    # Cohort accuracy per question (everyone who sat each test).
    cohort = {}
    for tid, t in tests.items():
        everyone = (await db.execute(select(TestAttempt).where(
            TestAttempt.test_id == tid, TestAttempt.status == "graded"))).scalars().all()
        cohort[tid] = rpt.class_accuracy(t, everyone)

    analyses, all_rows = [], []
    for a, t in rows:
        acc, n = cohort[t.id]
        qrows, known = rpt.question_rows(t, a, data.exam, acc)
        analyses.append(rpt.analyse_attempt(t, a, data.exam, qrows, known, n))
        all_rows.append(qrows)

    rep = rpt.build_report(data.exam, student, analyses, all_rows)
    rep["target"] = data.target.strip()
    rep["commentary"] = (await run_in_threadpool(rpt.write_commentary, rep, rep["target"], data.pronouns)) if data.commentary else None
    return rep


# Building takes 20–60s (topic tagging + commentary) — longer than the frontend proxy allows —
# so it runs as an in-memory background job the page polls. Jobs are per-process and short-lived.
_JOBS: dict[str, dict] = {}
_JOB_TTL = 30 * 60


async def _run_job(job_id: str, data: BuildIn, staff_id: int):
    job = _JOBS[job_id]
    try:
        async with SessionLocal() as db:
            staff = (await db.execute(select(User).where(User.id == staff_id))).scalar_one()
            job["report"] = await _build(data, staff, db)
        job["status"] = "done"
    except HTTPException as e:
        job.update(status="error", error=e.detail)
    except Exception as e:
        print(f"[reports] job {job_id} failed: {e!r}")
        job.update(status="error", error="Something went wrong while building the report.")


@router.post("/jobs")
async def start_job(data: BuildIn, staff: User = Depends(require_teacher)):
    now = time.time()
    for k in [k for k, j in _JOBS.items() if now - j["created"] > _JOB_TTL]:
        _JOBS.pop(k, None)
    job_id = secrets.token_urlsafe(12)
    _JOBS[job_id] = {"status": "running", "owner": staff.id, "created": now}
    asyncio.create_task(_run_job(job_id, data, staff.id))
    return {"job_id": job_id}


@router.get("/jobs/{job_id}")
async def job_status(job_id: str, staff: User = Depends(require_teacher)):
    job = _JOBS.get(job_id)
    if not job or job["owner"] != staff.id:
        raise HTTPException(404, "Report job not found — please build it again.")
    return {k: job.get(k) for k in ("status", "error", "report")}
