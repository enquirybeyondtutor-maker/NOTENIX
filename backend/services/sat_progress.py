"""Notenix SAT progress: skill mastery across practice tests, the diagnostic and drills; the
weekly study plan up to the test date; and the weekly progress email."""
from datetime import date, datetime, timedelta
from math import ceil

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services import sat

STRONG, BUILDING = 0.75, 0.5


def drills() -> dict:
    """{slug: module} from drills.json (each module is one skill)."""
    f = sat.form("drills")
    return f["modules"] if f else {}


def skill_slug_of(name: str) -> str | None:
    return next((k for k, m in drills().items() if m["title"] == name), None)


def _week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())   # Monday


async def answers_by_skill(user_id: int, db: AsyncSession, since: datetime | None = None) -> dict[str, list[bool]]:
    """{skill name: [correct, ...]} from finished practice tests/diagnostic and drills
    (latest drill answer per question)."""
    from models import SatAttempt, SatDrillAnswer
    out: dict[str, list[bool]] = {}
    q = select(SatAttempt).where(SatAttempt.user_id == user_id, SatAttempt.status == "done")
    if since:
        q = q.where(SatAttempt.completed_at >= since)
    for a in (await db.execute(q)).scalars().all():
        f = sat.form(a.form)
        if not f:
            continue
        for key, given in (a.answers or {}).items():
            m = f["modules"].get(key)
            if not m:
                continue
            for qq in m["questions"]:
                out.setdefault(qq["skill"], []).append(sat.is_correct(qq, given.get(qq["id"])))
    q = select(SatDrillAnswer).where(SatDrillAnswer.user_id == user_id).order_by(SatDrillAnswer.answered_at)
    if since:
        q = q.where(SatDrillAnswer.answered_at >= since)
    latest: dict[str, tuple[str, bool]] = {}
    names = {k: m["title"] for k, m in drills().items()}
    for r in (await db.execute(q)).scalars().all():
        latest[r.question_id] = (names.get(r.skill, r.skill), r.correct)
    for skill, ok in latest.values():
        out.setdefault(skill, []).append(ok)
    return out


async def skills(user_id: int, db: AsyncSession) -> list[dict]:
    """Every SAT skill with accuracy and a status: strong / building / weak / untried."""
    got = await answers_by_skill(user_id, db)
    rows = []
    for slug, m in drills().items():
        res = got.get(m["title"], [])
        acc = sum(res) / len(res) if res else None
        status = "untried" if acc is None else "strong" if acc >= STRONG else "building" if acc >= BUILDING else "weak"
        rows.append({"slug": slug, "skill": m["title"], "domain": m["domain"], "section": m["section"],
                     "about": m.get("about", ""), "right": sum(res), "total": len(res),
                     "accuracy": round(acc, 3) if acc is not None else None, "status": status})
    return rows


def focus_skills(rows: list[dict], n: int = 3) -> list[dict]:
    """Weakest skills first (lowest accuracy among tried), then skills not tried yet."""
    tried = sorted([r for r in rows if r["accuracy"] is not None and r["accuracy"] < STRONG],
                   key=lambda r: (r["accuracy"], -r["total"]))
    untried = [r for r in rows if r["accuracy"] is None]
    return (tried + untried)[:n]


async def plan(user, db: AsyncSession) -> dict:
    """This week's tasks (with progress) and an outline of the weeks up to the test."""
    from models import SatAttempt, SatDrillAnswer
    today = datetime.utcnow().date()
    week0 = _week_start(today)
    since = datetime.combine(week0, datetime.min.time())
    rows = await skills(user.id, db)
    focus = focus_skills(rows, 3)

    # Drill progress this week, per skill.
    week_drills: dict[str, set] = {}
    for r in (await db.execute(select(SatDrillAnswer).where(
            SatDrillAnswer.user_id == user.id, SatDrillAnswer.answered_at >= since))).scalars().all():
        week_drills.setdefault(r.skill, set()).add(r.question_id)
    attempts = (await db.execute(select(SatAttempt).where(
        SatAttempt.user_id == user.id, SatAttempt.form != "diagnostic"))).scalars().all()
    done_forms = {a.form for a in attempts if a.status == "done"}
    last_mock = max((a.completed_at for a in attempts if a.status == "done" and a.completed_at), default=None)
    mock_this_week = bool(last_mock and last_mock >= since)
    next_mock = next((m for m in sat.mocks() if m["slug"] not in done_forms), None)

    # Keep the week stable: skills already drilled this week stay on the list (most-practised
    # first), and the remaining slots go to the weakest skills.
    by_slug = {r["slug"]: r for r in rows}
    started = sorted((s for s in week_drills if s in by_slug), key=lambda s: -len(week_drills[s]))[:3]
    focus = [by_slug[s] for s in started] + [f for f in focus_skills(rows, 6) if f["slug"] not in started]
    focus = focus[:3]
    tasks = []
    for f in focus:
        n = len(week_drills.get(f["slug"], set()))
        tasks.append({"kind": "drill", "title": f"Drill: {f['skill']}", "detail": f"{f['domain']} · 6 questions",
                      "href": f"/sat/drills/{f['slug']}", "done": n >= 6, "progress": f"{min(n, 6)}/6"})
    test_date = date.fromisoformat(user.sat_test_date) if user.sat_test_date else None
    days_left = (test_date - today).days if test_date else None
    due_mock = not last_mock or (today - last_mock.date()).days >= 14 or (days_left is not None and 0 <= days_left <= 10)
    if due_mock or mock_this_week:
        target = next_mock or (sat.mocks()[0] if sat.mocks() else None)
        if target:
            tasks.append({"kind": "mock", "title": f"Take {target['title']}" if not mock_this_week else "Practice test done this week",
                          "detail": "Full test, 2 h 14 min, in one sitting", "href": "/sat/practice#tests", "done": mock_this_week,
                          "progress": "1/1" if mock_this_week else "0/1"})

    weeks = []
    if test_date and days_left is not None and days_left >= 0:
        n_weeks = min(ceil((days_left + 1) / 7), 16)
        rotating = focus_skills(rows, 8) or rows[:8]
        for i in range(n_weeks):
            start = week0 + timedelta(days=7 * i)
            last = i == n_weeks - 1
            if last:
                items = ["Light review of your mistakes", "Check the test centre and what to bring", "Rest the day before"]
            else:
                picks = [rotating[(2 * i + k) % len(rotating)]["skill"] for k in range(2)] if rotating else []
                items = [f"Drills: {', '.join(picks)}"] if picks else []
                if i % 2 == 1 or n_weeks - i <= 3:
                    items.append("Full practice test")
            weeks.append({"week_of": start.isoformat(), "items": items, "current": i == 0})
    return {"test_date": user.sat_test_date, "days_left": days_left, "target": user.sat_target,
            "tasks": tasks, "weeks": weeks, "focus": focus}


# ── Weekly progress email (Mondays) ───────────────────────────────────────────

async def weekly_summary(user, db: AsyncSession) -> dict:
    from models import SatAttempt
    since = datetime.utcnow() - timedelta(days=7)
    week = await answers_by_skill(user.id, db, since)
    answered = sum(len(v) for v in week.values())
    right = sum(sum(v) for v in week.values())
    last = (await db.execute(select(SatAttempt).where(
        SatAttempt.user_id == user.id, SatAttempt.status == "done", SatAttempt.form != "diagnostic")
        .order_by(SatAttempt.completed_at.desc()))).scalars().first()
    rows = await skills(user.id, db)
    return {"answered": answered, "accuracy": round(100 * right / answered) if answered else None,
            "last_score": last.total_score if last else None, "focus": focus_skills(rows, 2),
            "strong": sum(r["status"] == "strong" for r in rows), "total_skills": len(rows)}


def weekly_email(user, s: dict, days_left: int | None) -> tuple[str, str, str]:
    from services import mail_template as T
    from html import escape
    name = T.first_name(user.full_name)
    if s["answered"]:
        lead = f"This week you answered <b>{s['answered']}</b> SAT questions" + (f" and got <b>{s['accuracy']}%</b> right." if s["accuracy"] is not None else ".")
    else:
        lead = "You didn't practise on Notenix SAT this week. Twenty minutes of drills a day adds up fast."
    rows = [("Questions this week", str(s["answered"]))]
    if s["last_score"]:
        rows.append(("Latest practice test", f"{s['last_score']} / 1600" + (f" (target {user.sat_target})" if user.sat_target else "")))
    rows.append(("Skills marked strong", f"{s['strong']} of {s['total_skills']}"))
    if days_left is not None and days_left >= 0:
        rows.append(("Days to your SAT", str(days_left)))
    focus = "".join(f"<li><b>{escape(f['skill'])}</b> ({escape(f['domain'])})</li>" for f in s["focus"])
    body = (T.para(lead) + T.info_table(rows) +
            (T.subheading("Practise these next") + f'<ul style="margin:0 0 6px;padding-left:20px">{focus}</ul>' if focus else ""))
    html = T.layout(preheader=f"Your SAT week: {s['answered']} questions", heading=f"{name}'s SAT week", body=body,
                    buttons=[(T.site("/sat/practice"), "Open your study plan")], audience="student", tagline="SAT")
    text = f"{name}'s SAT week: {s['answered']} questions answered. Open your study plan: {T.site('/sat/practice')}" + T.text_footer()
    return f"{name}'s SAT week on Notenix", html, text


async def run_weekly() -> int:
    """Monday progress email to every SAT student with live access (and their parent, if given).
    Sent once per ISO week; safe to call every hour."""
    from database import SessionLocal
    from models import User, Enrolment
    from services.email import _deliver, is_mailbox
    now = datetime.utcnow()
    if now.weekday() != 0 or now.hour < 6:   # Mondays from 06:00 UTC
        return 0
    key = f"week-{now.isocalendar()[0]}-{now.isocalendar()[1]}"
    sent = 0
    async with SessionLocal() as db:
        users = (await db.execute(select(User).join(Enrolment, Enrolment.user_id == User.id).where(
            Enrolment.course == "sat", (Enrolment.until.is_(None)) | (Enrolment.until > now),
            User.is_active == True, User.sat_since.isnot(None)))).scalars().all()  # noqa: E712
        for u in users:
            if key in (u.sat_emails or []):
                continue
            s = await weekly_summary(u, db)
            days_left = (date.fromisoformat(u.sat_test_date) - now.date()).days if u.sat_test_date else None
            subject, html, text = weekly_email(u, s, days_left)
            for to in [u.email, u.parent_email]:
                if to and is_mailbox(to):
                    try:
                        await _deliver(to, subject, html, text)
                    except Exception as ex:
                        print(f"[sat] weekly email to {to} failed: {ex}")
            u.sat_emails = (u.sat_emails or []) + [key]
            sent += 1
        await db.commit()
    return sent
