"""Notenix exam engine routes (/exam/<exam>/...): public diagnostic and signed-in practice
tests, skill map, study plan and drills. Content and scoring: services/exams.py."""
import re
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User, ExamAttempt, ExamDrillAnswer
from security import get_current_user
from services import exams, exam_progress
from services import courses as course_svc

router = APIRouter(prefix="/exam", tags=["exam"])

GRACE_SECONDS = 60


def _cfg(exam: str) -> dict:
    cfg = exams.config(exam)
    if not cfg:
        raise HTTPException(404, "Exam not found.")
    return cfg


async def _allowed(exam: str, user: User, db: AsyncSession) -> dict:
    cfg = _cfg(exam)
    level, subject = cfg.get("access", (cfg["name"], None))   # GCSE courses: ("GCSE", "maths")
    if not course_svc.allows(await course_svc.live_courses(user, db), level, subject):
        raise HTTPException(403, course_svc.locked_message(level, subject))
    return cfg


@router.get("/{exam}/info")
async def info(exam: str):
    cfg = _cfg(exam)
    return {"exam": exam, "name": cfg["name"], "full_name": cfg["full_name"], "sections": cfg["sections"],
            "domains": cfg["domains"], "scale": {k: cfg["scale"][k] for k in ("min", "max", "decimals")},
            "calculator": cfg["calculator"], "no_calculator": list(cfg.get("no_calculator", ())),
            "mock_detail": cfg["mock_detail"], "about_score": cfg["about_score"],
            "has_diagnostic": exams.form(exam, "diagnostic") is not None, "mocks": len(exams.mocks(exam))}


# ── Free diagnostic (public) ──────────────────────────────────────────────────

@router.get("/{exam}/diagnostic")
async def diagnostic(exam: str):
    _cfg(exam)
    f = exams.form(exam, "diagnostic")
    if not f:
        raise HTTPException(404, "This diagnostic isn't available yet.")
    return {"title": f["title"], "modules": [exams.public_module(f, k) for k in f["stages"]]}


class FlatAnswers(BaseModel):
    answers: dict[str, str | None]


@router.post("/{exam}/diagnostic/score")
async def diagnostic_score(exam: str, data: FlatAnswers):
    _cfg(exam)
    f = exams.form(exam, "diagnostic")
    if not f:
        raise HTTPException(404, "This diagnostic isn't available yet.")
    return exams.report(exam, f, exams.split_answers(f, {k: v for k, v in data.answers.items() if isinstance(k, str)}))


@router.post("/{exam}/diagnostic/save")
async def diagnostic_save(exam: str, data: FlatAnswers, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Keep a diagnostic taken before signing in (once per student)."""
    await _allowed(exam, user, db)
    f = exams.form(exam, "diagnostic")
    if not f:
        raise HTTPException(404, "This diagnostic isn't available yet.")
    have = (await db.execute(select(ExamAttempt).where(ExamAttempt.user_id == user.id, ExamAttempt.exam == exam,
                                                       ExamAttempt.form == "diagnostic"))).scalars().first()
    if have:
        return {"attempt_id": have.id, "saved": False}
    ans = exams.split_answers(f, {k: v for k, v in data.answers.items() if isinstance(k, str)})
    s = exams.score(exam, f, ans)
    now = datetime.utcnow()
    a = ExamAttempt(user_id=user.id, exam=exam, form="diagnostic", status="done", stage=len(f["stages"]), answers=ans,
                    marked={}, scores={**{k: v["score"] for k, v in s["sections"].items()}, "total": s["score"]},
                    total_score=s["score"], started_at=now, completed_at=now)
    db.add(a)
    await db.commit()
    await db.refresh(a)
    return {"attempt_id": a.id, "saved": True}


# ── Signed-in practice ────────────────────────────────────────────────────────

def _row(a: ExamAttempt) -> dict:
    return {"id": a.id, "form": a.form, "status": a.status, "stage": a.stage, "scores": a.scores,
            "total_score": a.total_score,
            "started_at": a.started_at.isoformat() if a.started_at else None,
            "completed_at": a.completed_at.isoformat() if a.completed_at else None}


@router.get("/{exam}/home")
async def home(exam: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    cfg = await _allowed(exam, user, db)
    g = await exam_progress.goal(user.id, exam, db, create=True)
    await db.commit()
    attempts = (await db.execute(select(ExamAttempt).where(ExamAttempt.user_id == user.id, ExamAttempt.exam == exam)
                                 .order_by(ExamAttempt.started_at.desc()))).scalars().all()
    return {
        "exam": exam, "name": cfg["name"], "test_date": g.test_date, "target": g.target,
        "forms": [{"slug": f["slug"], "title": f["title"], "summary": f.get("summary", ""),
                   "attempts": [_row(a) for a in attempts if a.form == f["slug"]]} for f in exams.mocks(exam)],
        "diagnostic": next((_row(a) for a in attempts if a.form == "diagnostic"), None),
        "has_diagnostic": exams.form(exam, "diagnostic") is not None,
    }


class GoalIn(BaseModel):
    test_date: str | None = None
    target: float | None = None


@router.post("/{exam}/goal")
async def set_goal(exam: str, data: GoalIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    cfg = await _allowed(exam, user, db)
    g = await exam_progress.goal(user.id, exam, db, create=True)
    lo, hi = cfg["target_range"]
    g.test_date = data.test_date if data.test_date and re.fullmatch(r"\d{4}-\d{2}-\d{2}", data.test_date) else None
    g.target = round(data.target, 1) if data.target is not None and lo <= data.target <= hi else None
    await db.commit()
    return {"test_date": g.test_date, "target": g.target}


@router.post("/{exam}/forms/{slug}/start")
async def start(exam: str, slug: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await _allowed(exam, user, db)
    f = exams.form(exam, slug)
    if not f or f.get("kind") not in ("mock", "diagnostic"):
        raise HTTPException(404, "Practice test not found.")
    open_one = (await db.execute(select(ExamAttempt).where(
        ExamAttempt.user_id == user.id, ExamAttempt.exam == exam, ExamAttempt.form == slug,
        ExamAttempt.status == "in_progress"))).scalars().first()
    if open_one:
        return {"attempt_id": open_one.id, "resumed": True}
    a = ExamAttempt(user_id=user.id, exam=exam, form=slug, status="in_progress", stage=0, answers={}, marked={})
    db.add(a)
    await db.commit()
    await db.refresh(a)
    return {"attempt_id": a.id, "resumed": False}


async def _own(attempt_id: int, user: User, db: AsyncSession) -> tuple[ExamAttempt, dict]:
    a = (await db.execute(select(ExamAttempt).where(ExamAttempt.id == attempt_id, ExamAttempt.user_id == user.id))).scalar_one_or_none()
    if not a:
        raise HTTPException(404, "Attempt not found.")
    f = exams.form(a.exam, a.form)
    if not f:
        raise HTTPException(404, "This practice test is no longer available.")
    return a, f


def _seconds_left(a: ExamAttempt, f: dict, key: str) -> int | None:
    if not a.module_started_at:
        return None
    return int(f["modules"][key]["minutes"] * 60 - (datetime.utcnow() - a.module_started_at).total_seconds())


def _advance(a: ExamAttempt, f: dict) -> None:
    a.stage += 1
    a.module_started_at = None
    if a.stage >= len(f["stages"]):
        s = exams.score(a.exam, f, a.answers or {})
        a.scores = {**{k: v["score"] for k, v in s["sections"].items()}, "total": s["score"]}
        a.total_score = s["score"]
        a.status, a.completed_at = "done", datetime.utcnow()


@router.get("/attempts/{attempt_id}")
async def attempt(attempt_id: int, open_module: bool = False, user: User = Depends(get_current_user),
                  db: AsyncSession = Depends(get_db)):
    a, f = await _own(attempt_id, user, db)
    cfg = await _allowed(a.exam, user, db)
    if a.status == "done":
        return {"status": "done", "exam": a.exam, "attempt": _row(a)}
    key = f["stages"][a.stage]
    left = _seconds_left(a, f, key)
    if left is not None and left < -GRACE_SECONDS:
        _advance(a, f)   # time ran out while they were away: submit what was saved
        await db.commit()
        return await attempt(attempt_id, False, user, db)
    if open_module and a.module_started_at is None:
        a.module_started_at = datetime.utcnow()
        await db.commit()
        left = f["modules"][key]["minutes"] * 60
    return {
        "status": "in_progress", "exam": a.exam, "name": cfg["name"], "title": f["title"], "kind": f.get("kind"),
        "stage": a.stage, "stages": len(f["stages"]), "module": exams.public_module(f, key), "seconds_left": left,
        "started": a.module_started_at is not None,
        "calculator": exams.calculator_for(a.exam, f["modules"][key]["section"]),
        "answers": (a.answers or {}).get(key, {}), "marked": (a.marked or {}).get(key, []),
        "break_before": a.stage > 0 and a.module_started_at is None,
    }


class SaveIn(BaseModel):
    module: str
    answers: dict[str, str | None] = {}
    marked: list[str] = []


def _save(a: ExamAttempt, f: dict, data: SaveIn) -> None:
    key = f["stages"][a.stage]
    if data.module != key:
        raise HTTPException(409, "This section has already been submitted.")
    ids = {q["id"] for q in f["modules"][key]["questions"]}
    a.answers = {**(a.answers or {}), key: {k: (v or "")[:40] for k, v in data.answers.items() if k in ids}}
    a.marked = {**(a.marked or {}), key: [m for m in data.marked if m in ids]}


@router.put("/attempts/{attempt_id}/save")
async def save(attempt_id: int, data: SaveIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    a, f = await _own(attempt_id, user, db)
    await _allowed(a.exam, user, db)
    if a.status == "done":
        raise HTTPException(409, "This test is finished.")
    _save(a, f, data)
    await db.commit()
    return {"ok": True}


@router.post("/attempts/{attempt_id}/submit")
async def submit(attempt_id: int, data: SaveIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    a, f = await _own(attempt_id, user, db)
    await _allowed(a.exam, user, db)
    if a.status == "done":
        return {"status": "done", "attempt": _row(a)}
    _save(a, f, data)
    _advance(a, f)
    await db.commit()
    return {"status": a.status, "stage": a.stage, "attempt": _row(a)}


@router.get("/attempts/{attempt_id}/result")
async def result(attempt_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    a, f = await _own(attempt_id, user, db)
    if a.status != "done":
        raise HTTPException(400, "Finish the test to see your score.")
    g = await exam_progress.goal(user.id, a.exam, db)
    return {"attempt": _row(a), "exam": a.exam, "title": f["title"], "kind": f.get("kind"),
            "target": g.target if g else None, **exams.report(a.exam, f, a.answers or {})}


# ── Skills, study plan and drills ─────────────────────────────────────────────

@router.get("/{exam}/skills")
async def skills(exam: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await _allowed(exam, user, db)
    return await exam_progress.skills(user.id, exam, db)


@router.get("/{exam}/plan")
async def study_plan(exam: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await _allowed(exam, user, db)
    return await exam_progress.plan(user, exam, db)


@router.get("/{exam}/drills/{slug}")
async def drill(exam: str, slug: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await _allowed(exam, user, db)
    m = exams.drills(exam).get(slug)
    if not m:
        raise HTTPException(404, "Skill not found.")
    ids = [q["id"] for q in m["questions"]]
    prev = {}
    for r in (await db.execute(select(ExamDrillAnswer).where(
            ExamDrillAnswer.user_id == user.id, ExamDrillAnswer.question_id.in_(ids)).order_by(ExamDrillAnswer.answered_at))).scalars().all():
        prev[r.question_id] = r.correct
    return {"slug": slug, "skill": m["title"], "domain": m["domain"], "about": m.get("about", ""),
            "questions": [exams.public_question(q) for q in m["questions"]], "previous": prev}


class DrillAnswerIn(BaseModel):
    question_id: str
    answer: str


@router.post("/{exam}/drills/{slug}/answer")
async def drill_answer(exam: str, slug: str, data: DrillAnswerIn, user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    await _allowed(exam, user, db)
    m = exams.drills(exam).get(slug)
    q = next((x for x in (m or {}).get("questions", []) if x["id"] == data.question_id), None)
    if not q:
        raise HTTPException(404, "Question not found.")
    ok = exams.is_correct(q, data.answer)
    db.add(ExamDrillAnswer(user_id=user.id, exam=exam, question_id=q["id"], skill=slug, correct=ok))
    await db.commit()
    return {"correct": ok, "answer": q["answer"], "explanation": q["explanation"]}
