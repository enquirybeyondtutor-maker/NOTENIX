"""TMUA extras on a test result: the 1.0-9.0 score estimate and, for the TMUA Mock Series,
the combined two-paper score and the student's rank.

Any test at level TMUA gets a per-paper estimate on the TMUA scale (services/exams.py `scaled`).
A Mock Series paper (matched by title, see services/tmua_series.py) also gets:
  * the combined score once both papers of that mock are done (all 40 questions together);
  * a rank against the other series students. A numbered mock is ranked on sittings finished
    in its 24-hour window from opening (10:00 UK); later sittings are unranked practice and
    are told where they would have placed. The Baseline Mock has no window: everyone counts.
Only students' first, graded sittings count; teachers, admins and attempts a tutor has
excluded from analysis are left out. Ties share a rank (two people on 5.0 are both 2nd).

Every series paper is also ranked against a SIMULATED cohort of 1,000 strong TMUA candidates
(`simulated_rank`). These are not real people and the page says so: a Rasch (1-parameter IRT)
model where each simulated candidate has an ability, each question a difficulty, and
P(right) = 1 / (1 + e^-(ability - difficulty)). Abilities are drawn from N(SIM_MEAN, SIM_SD),
set so the cohort's median lands near 5.8 on a real-exam-level paper (a strong applicant,
well above the national median of ~3.8). Question difficulty comes from the mock's level
(Hard mocks are harder for everyone) plus the question's own 1-3 difficulty where it has one.
Each simulated candidate sits both papers with the same ability, so a combined rank works too.
The cohort is seeded by the mock's title: everyone on a mock is ranked against the same 1,000.
"""
import math
import random
import re
from datetime import datetime, timedelta
from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services import exams, tmua_series

WINDOW = timedelta(hours=24)

SIM_SIZE = 1000
SIM_MEAN, SIM_SD = 0.7, 1.1                     # ability of the simulated strong candidates
LEVEL_SHIFT = {"Hard": 0.45, "Real exam level": 0.0}   # mock level -> extra question difficulty
QUESTION_SHIFT = {1: -0.8, 2: 0.0, 3: 0.8, "easy": -0.8, "medium": 0.0, "hard": 0.8}

_PAPER = re.compile(r"·\s*Paper\s*([12])\s*$")
_MOCK = re.compile(r"^TMUA January 2027 · Mock (\d+) ·")


def series_paper(title: str) -> tuple[str, int] | None:
    """("baseline" | "3", paper 1/2) for a Mock Series paper title, else None."""
    t = (title or "").strip()
    p = _PAPER.search(t)
    if not p:
        return None
    if t.startswith(tmua_series.BASELINE_PREFIX):
        return "baseline", int(p.group(1))
    m = _MOCK.match(t)
    if m and any(n == int(m.group(1)) for n, _, _ in tmua_series.MOCKS):
        return m.group(1), int(p.group(1))
    return None


def window(mock: str) -> tuple[datetime, datetime] | None:
    """The ranked window (UTC) of a numbered mock; None for the Baseline Mock."""
    for n, at, _ in tmua_series.MOCKS:
        if str(n) == mock:
            return at, at + WINDOW
    return None


def _right(attempt, n_questions: int) -> int:
    rows = attempt.results or []
    if rows and all(isinstance(r, dict) and "is_correct" in r for r in rows):
        return sum(1 for r in rows if r.get("is_correct"))
    return round((attempt.score or 0) * n_questions / 100)


def _scaled(right: int, total: int) -> float:
    return exams.scaled("tmua", right / total if total else 0)


def _rank(mine: float, ranked: list[float]) -> dict:
    """Competition rank of `mine` among `ranked` (which may or may not include it)."""
    return {"rank": 1 + sum(1 for s in ranked if s > mine), "of": len(ranked),
            "average": round(sum(ranked) / len(ranked), 1) if ranked else None}


def _difficulties(test, mock: str) -> tuple[float, ...]:
    level = next((lvl for n, _, lvl in tmua_series.MOCKS if str(n) == mock), None)
    base = LEVEL_SHIFT.get(level, 0.0)
    return tuple(base + QUESTION_SHIFT.get(q.get("difficulty") if isinstance(q, dict) else None, 0.0)
                 for q in (test.questions or []))


@lru_cache(maxsize=64)
def _cohort(seed: str, p1: tuple[float, ...], p2: tuple[float, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Right answers on Paper 1 and Paper 2 for each of the SIM_SIZE simulated candidates."""
    rng = random.Random(seed)
    a, b = [], []
    for _ in range(SIM_SIZE):
        ability = rng.gauss(SIM_MEAN, SIM_SD)
        a.append(sum(rng.random() < 1 / (1 + math.exp(d - ability)) for d in p1))
        b.append(sum(rng.random() < 1 / (1 + math.exp(d - ability)) for d in p2))
    return tuple(a), tuple(b)


def _sim_rank(mine: int, cohort: list[int], total: int) -> dict:
    """Where `mine` (right answers) falls among the simulated candidates; ties share a place."""
    rank = 1 + sum(1 for s in cohort if s > mine)
    median = sorted(cohort)[len(cohort) // 2]
    return {"rank": rank, "of": len(cohort), "top_percent": max(1, math.ceil(100 * rank / len(cohort))),
            "median": _scaled(median, total)}


async def _sittings(test_ids: list[int], db: AsyncSession) -> dict[int, dict[int, object]]:
    """{test_id: {student_id: first graded attempt}} for real students."""
    from models import TestAttempt, User
    rows = (await db.execute(
        select(TestAttempt).join(User, User.id == TestAttempt.student_id)
        .where(TestAttempt.test_id.in_(test_ids), TestAttempt.status == "graded",
               TestAttempt.excluded_from_analysis.is_(False), User.role == "student")
        .order_by(TestAttempt.completed_at)
    )).scalars().all()
    out: dict[int, dict[int, object]] = {t: {} for t in test_ids}
    for a in rows:
        out[a.test_id].setdefault(a.student_id, a)
    return out


async def tmua_extras(test, attempt, user, db: AsyncSession) -> dict | None:
    if (test.level or "").strip().upper() != "TMUA" or getattr(attempt, "status", "graded") != "graded":
        return None
    total = len(test.questions or []) or test.num_questions or 0
    right = _right(attempt, total)
    out: dict = {"paper_score": _scaled(right, total), "right": right, "total": total,
                 "scale_max": exams.EXAMS["tmua"]["scale"]["max"], "about": exams.EXAMS["tmua"]["about_score"],
                 "series": None}
    info = series_paper(test.title)
    if not info:
        return out
    mock, paper = info

    # The other paper of the same mock (a test by the team with the matching title).
    from models import Test, TestAssignment, User
    stem = _PAPER.sub("", test.title.strip()).strip()
    other_title = f"{stem} · Paper {2 if paper == 1 else 1}"
    other = (await db.execute(
        select(Test).join(User, User.id == Test.owner_id)
        .where(Test.title == other_title, Test.is_archived.is_(False), User.role.in_(["admin", "teacher"]))
        .order_by(Test.id)
    )).scalars().first()

    ids = [test.id] + ([other.id] if other else [])
    sit = await _sittings(ids, db)
    win = window(mock)
    now = datetime.utcnow()

    def in_window(a) -> bool:
        return win is None or (a.completed_at is not None and win[0] <= a.completed_at <= win[1])

    def counted(test_id: int) -> dict[int, object]:
        return {sid: a for sid, a in sit.get(test_id, {}).items() if in_window(a)}

    # This paper.
    mine_first = sit[test.id].get(user.id)
    mine_ranked = mine_first is not None and mine_first.id == attempt.id and in_window(attempt)
    pool = [_scaled(_right(a, total), total) for a in counted(test.id).values()]
    paper_rank = {**_rank(out["paper_score"], pool), "ranked": mine_ranked}

    series: dict = {"mock": "Baseline Mock" if mock == "baseline" else f"Mock {mock}", "paper": paper,
                    "paper_rank": paper_rank, "combined": None, "combined_rank": None, "other_paper": None,
                    "window": None}
    if win:
        series["window"] = {"start": win[0].isoformat(), "end": win[1].isoformat(), "open": win[0] <= now <= win[1]}

    if other:
        o_total = len(other.questions or []) or other.num_questions or 0
        o_asg = (await db.execute(select(TestAssignment).where(
            TestAssignment.test_id == other.id, TestAssignment.student_id == user.id))).scalars().first()
        o_mine = sit[other.id].get(user.id)
        series["other_paper"] = {"paper": 2 if paper == 1 else 1, "title": other.title,
                                 "assignment_id": o_asg.id if o_asg else None, "done": o_mine is not None}
        if o_mine is not None:
            c_right, c_total = right + _right(o_mine, o_total), total + o_total
            series["combined"] = {"score": _scaled(c_right, c_total), "right": c_right, "total": c_total}
            # Combined rank: students with both papers counted (in the window, for a numbered mock).
            a_counted, b_counted = counted(test.id), counted(other.id)
            both = [_scaled(_right(a_counted[s], total) + _right(b_counted[s], o_total), c_total)
                    for s in a_counted.keys() & b_counted.keys()]
            series["combined_rank"] = {**_rank(series["combined"]["score"], both),
                                       "ranked": mine_ranked and in_window(o_mine)}

    # Simulated cohort of 1,000 strong candidates (always Paper 1 first, so both papers share one cohort).
    d_this = _difficulties(test, mock)
    d_other = _difficulties(other, mock) if other else ()
    p1, p2 = (d_this, d_other) if paper == 1 else (d_other, d_this)
    sim1, sim2 = _cohort(stem, p1, p2)
    sim_this = sim1 if paper == 1 else sim2
    simulated = {"paper": _sim_rank(right, list(sim_this), total), "combined": None}
    if series["combined"]:
        c = series["combined"]
        simulated["combined"] = _sim_rank(c["right"], [x + y for x, y in zip(sim1, sim2)], c["total"])
    series["simulated"] = simulated

    out["series"] = series
    return out
