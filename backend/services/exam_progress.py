"""Exam engine progress: skill mastery across practice tests, the diagnostic and drills; the
weekly study plan up to the test date; and the Monday progress email. Same rules as SAT
(services/sat_progress.py), for every exam in services/exams.EXAMS."""
from datetime import date, datetime, timedelta
from math import ceil

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services import exams

STRONG, BUILDING = 0.75, 0.5
DRILL_SIZE = 6


def _week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())   # Monday


async def goal(user_id: int, exam: str, db: AsyncSession, create: bool = False):
    from models import ExamGoal
    g = (await db.execute(select(ExamGoal).where(ExamGoal.user_id == user_id, ExamGoal.exam == exam))).scalar_one_or_none()
    if not g and create:
        g = ExamGoal(user_id=user_id, exam=exam, emails=[])
        db.add(g)
        await db.flush()
    return g


async def answers_by_skill(user_id: int, exam: str, db: AsyncSession, since: datetime | None = None) -> dict[str, list[bool]]:
    """{skill: [correct, ...]} from finished sittings and drills (latest drill answer per question)."""
    from models import ExamAttempt, ExamDrillAnswer
    out: dict[str, list[bool]] = {}
    q = select(ExamAttempt).where(ExamAttempt.user_id == user_id, ExamAttempt.exam == exam, ExamAttempt.status == "done")
    if since:
        q = q.where(ExamAttempt.completed_at >= since)
    for a in (await db.execute(q)).scalars().all():
        f = exams.form(exam, a.form)
        if not f:
            continue
        for key, given in (a.answers or {}).items():
            m = f["modules"].get(key)
            for qq in (m or {}).get("questions", []):
                out.setdefault(qq["skill"], []).append(exams.is_correct(qq, given.get(qq["id"])))
    q = select(ExamDrillAnswer).where(ExamDrillAnswer.user_id == user_id, ExamDrillAnswer.exam == exam).order_by(ExamDrillAnswer.answered_at)
    if since:
        q = q.where(ExamDrillAnswer.answered_at >= since)
    names = {k: m["title"] for k, m in exams.drills(exam).items()}
    latest: dict[str, tuple[str, bool]] = {}
    for r in (await db.execute(q)).scalars().all():
        latest[r.question_id] = (names.get(r.skill, r.skill), r.correct)
    for skill, ok in latest.values():
        out.setdefault(skill, []).append(ok)
    return out


async def skills(user_id: int, exam: str, db: AsyncSession) -> list[dict]:
    """Every skill with accuracy and status: strong / building / weak / untried."""
    got = await answers_by_skill(user_id, exam, db)
    drills = exams.drills(exam)
    rows = []
    for domain, skill in exams.skill_list(exam):
        slug = exams.slugify(skill)
        res = got.get(skill, [])
        acc = sum(res) / len(res) if res else None
        status = "untried" if acc is None else "strong" if acc >= STRONG else "building" if acc >= BUILDING else "weak"
        rows.append({"slug": slug, "skill": skill, "domain": domain, "about": drills.get(slug, {}).get("about", ""),
                     "has_drill": slug in drills, "right": sum(res), "total": len(res),
                     "accuracy": round(acc, 3) if acc is not None else None, "status": status})
    return rows


def focus_skills(rows: list[dict], n: int = 3) -> list[dict]:
    """Weakest tried skills first, then skills not tried yet (only skills with a drill)."""
    rows = [r for r in rows if r["has_drill"]]
    tried = sorted([r for r in rows if r["accuracy"] is not None and r["accuracy"] < STRONG],
                   key=lambda r: (r["accuracy"], -r["total"]))
    untried = [r for r in rows if r["accuracy"] is None]
    return (tried + untried)[:n]


async def plan(user, exam: str, db: AsyncSession) -> dict:
    """This week's tasks (with progress) and an outline of the weeks up to the test."""
    from models import ExamAttempt, ExamDrillAnswer
    cfg = exams.config(exam)
    today = datetime.utcnow().date()
    week0 = _week_start(today)
    since = datetime.combine(week0, datetime.min.time())
    rows = await skills(user.id, exam, db)
    g = await goal(user.id, exam, db)

    week_drills: dict[str, set] = {}
    for r in (await db.execute(select(ExamDrillAnswer).where(
            ExamDrillAnswer.user_id == user.id, ExamDrillAnswer.exam == exam, ExamDrillAnswer.answered_at >= since))).scalars().all():
        week_drills.setdefault(r.skill, set()).add(r.question_id)
    attempts = (await db.execute(select(ExamAttempt).where(
        ExamAttempt.user_id == user.id, ExamAttempt.exam == exam, ExamAttempt.form != "diagnostic"))).scalars().all()
    done_forms = {a.form for a in attempts if a.status == "done"}
    last_mock = max((a.completed_at for a in attempts if a.status == "done" and a.completed_at), default=None)
    mock_this_week = bool(last_mock and last_mock >= since)
    all_mocks = exams.mocks(exam)
    next_mock = next((m for m in all_mocks if m["slug"] not in done_forms), None)

    # Skills already drilled this week stay on the list; the rest go to the weakest skills.
    by_slug = {r["slug"]: r for r in rows}
    started = sorted((s for s in week_drills if s in by_slug), key=lambda s: -len(week_drills[s]))[:3]
    focus = ([by_slug[s] for s in started] + [f for f in focus_skills(rows, 6) if f["slug"] not in started])[:3]
    tasks = []
    for f in focus:
        n = len(week_drills.get(f["slug"], set()))
        tasks.append({"kind": "drill", "title": f"Drill: {f['skill']}", "detail": f"{f['domain']} · {DRILL_SIZE} questions",
                      "href": f"/{exam}/drills/{f['slug']}", "done": n >= DRILL_SIZE, "progress": f"{min(n, DRILL_SIZE)}/{DRILL_SIZE}"})
    test_date = date.fromisoformat(g.test_date) if g and g.test_date else None
    days_left = (test_date - today).days if test_date else None
    due_mock = not last_mock or (today - last_mock.date()).days >= 14 or (days_left is not None and 0 <= days_left <= 10)
    if (due_mock or mock_this_week) and all_mocks:
        target = next_mock or all_mocks[0]
        tasks.append({"kind": "mock", "title": "Practice test done this week" if mock_this_week else f"Take {target['title']}",
                      "detail": f"{cfg['mock_detail']}, in one sitting", "href": f"/{exam}/practice#tests",
                      "done": mock_this_week, "progress": "1/1" if mock_this_week else "0/1"})

    weeks = []
    if test_date and days_left is not None and days_left >= 0:
        n_weeks = min(ceil((days_left + 1) / 7), 16)
        rotating = focus_skills(rows, 8) or [r for r in rows if r["has_drill"]][:8]
        for i in range(n_weeks):
            start = week0 + timedelta(days=7 * i)
            if i == n_weeks - 1:
                items = ["Light review of your mistakes", "Check your test centre and what to bring", "Rest the day before"]
            else:
                picks = [rotating[(2 * i + k) % len(rotating)]["skill"] for k in range(2)] if rotating else []
                items = [f"Drills: {', '.join(picks)}"] if picks else []
                if i % 2 == 1 or n_weeks - i <= 3:
                    items.append("Full practice test")
            weeks.append({"week_of": start.isoformat(), "items": items, "current": i == 0})
    return {"test_date": g.test_date if g else None, "days_left": days_left, "target": g.target if g else None,
            "tasks": tasks, "weeks": weeks, "focus": focus}


# ── Weekly progress email (Mondays) ───────────────────────────────────────────

async def weekly_summary(user, exam: str, db: AsyncSession) -> dict:
    from models import ExamAttempt
    since = datetime.utcnow() - timedelta(days=7)
    week = await answers_by_skill(user.id, exam, db, since)
    answered = sum(len(v) for v in week.values())
    right = sum(sum(v) for v in week.values())
    last = (await db.execute(select(ExamAttempt).where(
        ExamAttempt.user_id == user.id, ExamAttempt.exam == exam, ExamAttempt.status == "done",
        ExamAttempt.form != "diagnostic").order_by(ExamAttempt.completed_at.desc()))).scalars().first()
    rows = await skills(user.id, exam, db)
    return {"answered": answered, "accuracy": round(100 * right / answered) if answered else None,
            "last_score": last.total_score if last else None, "focus": focus_skills(rows, 2),
            "strong": sum(r["status"] == "strong" for r in rows), "total_skills": len(rows)}


def weekly_email(user, exam: str, s: dict, target: float | None, days_left: int | None) -> tuple[str, str, str]:
    from html import escape
    from services import mail_template as T
    cfg = exams.config(exam)
    name, ex = T.first_name(user.full_name), cfg["name"]
    if s["answered"]:
        lead = f"This week you answered <b>{s['answered']}</b> {ex} questions" + (f" and got <b>{s['accuracy']}%</b> right." if s["accuracy"] is not None else ".")
    else:
        lead = f"You didn't practise {ex} on Notenix this week. Twenty minutes of drills a day adds up fast."
    sc = cfg["scale"]
    rows = [("Questions this week", str(s["answered"]))]
    if s["last_score"] is not None:
        rows.append(("Latest practice test", f"{s['last_score']:.1f} out of {sc['max']:.1f}" + (f" (target {target:.1f})" if target else "")))
    rows.append(("Skills marked strong", f"{s['strong']} of {s['total_skills']}"))
    if days_left is not None and days_left >= 0:
        rows.append((f"Days to your {ex}", str(days_left)))
    focus = "".join(f"<li><b>{escape(f['skill'])}</b> ({escape(f['domain'])})</li>" for f in s["focus"])
    body = (T.para(lead) + T.info_table(rows) +
            (T.subheading("Practise these next") + f'<ul style="margin:0 0 6px;padding-left:20px">{focus}</ul>' if focus else ""))
    html = T.layout(preheader=f"Your {ex} week: {s['answered']} questions", heading=f"{name}'s {ex} week", body=body,
                    buttons=[(T.site(f"/{exam}/practice"), "Open your study plan")], audience="student", tagline=ex)
    text = f"{name}'s {ex} week: {s['answered']} questions answered. Open your study plan: {T.site(f'/{exam}/practice')}" + T.text_footer()
    return f"{name}'s {ex} week on Notenix", html, text


async def run_weekly() -> int:
    """Monday progress email for every exam: to each student with live access who has opened
    that exam's practice (an ExamGoal row), and their parent if given. Once per ISO week."""
    from database import SessionLocal
    from models import User, Enrolment, ExamGoal
    from services.email import _deliver, is_mailbox
    now = datetime.utcnow()
    if now.weekday() != 0 or now.hour < 6:   # Mondays from 06:00 UTC
        return 0
    key = f"week-{now.isocalendar()[0]}-{now.isocalendar()[1]}"
    sent = 0
    async with SessionLocal() as db:
        for exam, cfg in exams.EXAMS.items():
            rows = (await db.execute(select(User, ExamGoal).join(ExamGoal, ExamGoal.user_id == User.id)
                                     .join(Enrolment, Enrolment.user_id == User.id).where(
                ExamGoal.exam == exam, Enrolment.course == cfg["course"],
                (Enrolment.until.is_(None)) | (Enrolment.until > now), User.is_active == True))).all()  # noqa: E712
            for u, g in rows:
                if key in (g.emails or []):
                    continue
                s = await weekly_summary(u, exam, db)
                if not s["answered"] and s["last_score"] is None:
                    g.emails = (g.emails or []) + [key]   # never practised: don't nag
                    continue
                days_left = (date.fromisoformat(g.test_date) - now.date()).days if g.test_date else None
                subject, html, text = weekly_email(u, exam, s, g.target, days_left)
                for to in [u.email, u.parent_email]:
                    if to and is_mailbox(to):
                        try:
                            await _deliver(to, subject, html, text)
                        except Exception as ex:
                            print(f"[exam] weekly {exam} email to {to} failed: {ex}")
                g.emails = (g.emails or []) + [key]
                sent += 1
        await db.commit()
    return sent
