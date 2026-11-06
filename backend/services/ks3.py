"""Notenix KS3: free-trial parent emails and the progress report ("Beat the Year 7 dip").

Sequence (days after the trial starts): 0 welcome · 3 check-in · 5 ending soon · 7 report.
Everything here is plain inline-styled HTML so it renders in Gmail/Outlook.
"""
from datetime import datetime, timedelta
from html import escape
from sqlalchemy import select
from config import settings
from database import SessionLocal
from models import User, Test, TestAssignment, TestAttempt
from services import pricing
from services.email import _deliver

BRAND, INK, MUTED, LINE = "#4F46E5", "#0f172a", "#475569", "#e2e8f0"
GOOD, OK, WEAK = "#059669", "#d97706", "#dc2626"
SEQUENCE = (("welcome", 0), ("checkin", 3), ("ending", 5), ("report", 7))


# ── Progress data ──────────────────────────────────────────────────────────────

def gcse_indicator(avg: float | None) -> str | None:
    """A rough early indicator from KS3 scores, never a prediction."""
    if avg is None:
        return None
    for floor, band in ((85, "7–9"), (72, "6–7"), (60, "5–6"), (48, "4–5"), (35, "3–4")):
        if avg >= floor:
            return band
    return "1–3"


async def progress(db, u: User) -> dict:
    rows = (await db.execute(
        select(TestAssignment, Test, TestAttempt)
        .join(Test, Test.id == TestAssignment.test_id)
        .outerjoin(TestAttempt, TestAttempt.assignment_id == TestAssignment.id)
        .where(TestAssignment.student_id == u.id)
        .order_by(TestAssignment.created_at)
    )).all()
    taken, missed, topics = [], [], {}
    for a, t, at in rows:
        if at is None or at.status != "graded":
            if at is None:
                missed.append({"title": t.title, "subject": t.subject})
            continue
        if at.excluded_from_analysis:
            continue
        taken.append({"title": t.title, "subject": t.subject, "score": round(at.score or 0),
                      "date": at.completed_at})
        for r in at.results or []:
            name = (r.get("topic") or t.topic or t.subject or "General").strip()
            key = (t.subject, name)
            right, total = topics.get(key, (0, 0))
            topics[key] = (right + int(bool(r.get("is_correct"))), total + 1)
    subjects = {}
    for x in taken:  # latest + first score per subject
        s = subjects.setdefault(x["subject"], {"first": x["score"], "latest": x["score"], "count": 0})
        s["latest"], s["count"] = x["score"], s["count"] + 1
    topic_list = [{"subject": s, "topic": n, "pct": round(100 * r / tot), "questions": tot}
                  for (s, n), (r, tot) in topics.items() if tot >= 2]
    strengths = sorted([t for t in topic_list if t["pct"] >= 70], key=lambda t: -t["pct"])[:3]
    focus = sorted([t for t in topic_list if t["pct"] < 70], key=lambda t: t["pct"])[:3]
    avg = round(sum(x["score"] for x in taken) / len(taken)) if taken else None
    return {"taken": taken, "missed": missed, "subjects": subjects, "strengths": strengths,
            "focus": focus, "average": avg, "gcse": gcse_indicator(avg)}


# ── HTML pieces ────────────────────────────────────────────────────────────────

def _first(name: str | None) -> str:
    return escape((name or "your child").split(" ")[0])


def _btn(url: str, label: str, primary: bool = True) -> str:
    bg, fg, border = (BRAND, "#fff", BRAND) if primary else ("#fff", BRAND, BRAND)
    return (f'<a href="{url}" style="display:inline-block;background:{bg};color:{fg};border:1.5px solid {border};'
            f'text-decoration:none;font-weight:600;font-size:14px;padding:11px 18px;border-radius:10px;'
            f'margin:0 8px 8px 0">{label}</a>')


def _shell(preheader: str, heading: str, body: str) -> str:
    return f"""\
<div style="background:#f8fafc;padding:24px 12px">
<span style="display:none;max-height:0;overflow:hidden">{escape(preheader)}</span>
<div style="font-family:Inter,Segoe UI,system-ui,sans-serif;max-width:560px;margin:0 auto;background:#fff;
  border:1px solid {LINE};border-radius:16px;padding:28px;color:{INK}">
  <table role="presentation" cellpadding="0" cellspacing="0" style="margin-bottom:22px"><tr>
    <td style="width:32px;height:32px;border-radius:10px;background:{BRAND};color:#fff;font-weight:700;text-align:center">N</td>
    <td style="padding-left:10px;font-size:16px;font-weight:700">Notenix <span style="color:{MUTED};font-weight:500">· KS3 by Beyond Tutors</span></td>
  </tr></table>
  <h1 style="font-size:21px;line-height:1.3;margin:0 0 14px">{heading}</h1>
  <div style="color:{MUTED};font-size:15px;line-height:1.65">{body}</div>
  <p style="color:#94a3b8;font-size:12px;margin:26px 0 0;border-top:1px solid {LINE};padding-top:14px">
    You're receiving this because you started a free Notenix KS3 trial. Notenix is a unit of Beyond Groups,
    provided with Beyond Tutors. Questions? Just reply to this email.</p>
</div></div>"""


def _bar(pct: int, color: str) -> str:
    pct = max(0, min(100, pct))
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" width="100%" style="height:8px;'
            f'background:#f1f5f9;border-radius:99px"><tr><td width="{max(pct, 2)}%" style="background:{color};'
            f'border-radius:99px;height:8px;font-size:0">&nbsp;</td><td style="font-size:0">&nbsp;</td></tr></table>')


def _color(pct: int) -> str:
    return GOOD if pct >= 70 else OK if pct >= 50 else WEAK


def _subject_table(p: dict) -> str:
    if not p["subjects"]:
        return ""
    rows = ""
    for name, s in p["subjects"].items():
        change = s["latest"] - s["first"] if s["count"] > 1 else None
        delta = "" if change is None else (
            f' <span style="color:{GOOD if change >= 0 else WEAK};font-size:12px">'
            f'{"▲" if change >= 0 else "▼"} {abs(change)}</span>')
        rows += (f'<tr><td style="padding:8px 0;width:30%;color:{INK};font-weight:600">{escape(name)}</td>'
                 f'<td style="padding:8px 10px">{_bar(s["latest"], _color(s["latest"]))}</td>'
                 f'<td style="padding:8px 0;width:70px;text-align:right;color:{INK};font-weight:700">{s["latest"]}%{delta}</td></tr>')
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 4px">{rows}</table>'


def _topic_list(items: list[dict], title: str, color: str) -> str:
    if not items:
        return ""
    lis = "".join(f'<li style="margin:3px 0"><b style="color:{INK}">{escape(t["topic"])}</b> '
                  f'<span style="color:#94a3b8">({escape(t["subject"])}, {t["pct"]}%)</span></li>' for t in items)
    return (f'<p style="margin:16px 0 4px;color:{color};font-weight:700;font-size:13px;text-transform:uppercase;'
            f'letter-spacing:.4px">{title}</p><ul style="margin:0;padding-left:18px">{lis}</ul>')


def _login_box(u: User) -> str:
    return (f'<div style="background:#eef2ff;border-radius:12px;padding:14px 16px;margin:16px 0;color:{INK}">'
            f'<div style="font-size:12px;color:{MUTED}">{_first(u.full_name)}\'s Notenix login</div>'
            f'<div style="font-size:16px;font-weight:700;margin-top:2px">{escape(u.email)}</div>'
            f'<div style="font-size:12px;color:{MUTED};margin-top:2px">Sign in at notenix.com with the password you chose.</div></div>')


def _price(u: User) -> str:
    return pricing.ks3_for_currency(u.billing_currency)["label"]


def _site(path: str) -> str:
    return settings.public_url.rstrip("/") + path


# ── The four emails ────────────────────────────────────────────────────────────

def welcome(u: User, p: dict) -> tuple[str, str, str]:
    name, yr = _first(u.full_name), u.ks3_year or 7
    body = (f"<p>Thanks for starting {name}'s free trial week. The first year of secondary school is where "
            f"many children quietly slip: new subjects, more homework and a new routine all at once. "
            f"This week shows you exactly where {name} stands, and helps straight away.</p>"
            f"{_login_box(u)}"
            f'<p style="margin:16px 0 6px;color:{INK};font-weight:700">This week</p>'
            f'<ol style="margin:0;padding-left:20px">'
            f"<li><b>Day 1–2: the Year {yr} baseline tests</b> in Maths, Science and English (about 30 minutes each).</li>"
            f"<li><b>Homework help:</b> stuck on school homework? Send a photo in Notenix and a Beyond Tutors tutor replies.</li>"
            f"<li><b>KS3 notes</b> for every Year {yr} topic, to revise from.</li>"
            f"<li><b>Day 7: your progress report</b>: scores, strong topics, and the topics to fix first.</li></ol>")
    subject = f"{_first(u.full_name)}'s free Notenix trial has started"
    html = _shell("Start with the baseline tests", f"Welcome! Let's beat the Year {yr} dip", body
                  + f'<p style="margin-top:20px">{_btn(_site("/tests"), "Start the baseline tests")}</p>')
    text = (f"{name}'s free Notenix KS3 trial week has started.\nLogin: {u.email}\n"
            f"1) Year {yr} baseline tests 2) homework help 3) KS3 notes 4) day-7 progress report.\n{_site('/tests')}")
    return subject, html, text


def checkin(u: User, p: dict) -> tuple[str, str, str]:
    name = _first(u.full_name)
    done, left = len(p["taken"]), len(p["missed"])
    if done:
        lead = (f"<p>Three days into the trial, and {name} has finished <b>{done} test{'s' if done != 1 else ''}</b>. "
                f"Here's how it's going:</p>{_subject_table(p)}")
        if left:
            lead += f"<p>{left} test{'s are' if left != 1 else ' is'} still waiting. A full picture needs all three subjects.</p>"
    else:
        lead = (f"<p>Three days in, and {name} hasn't started the baseline tests yet. They take about 30 minutes each, "
                f"and they're what the day-7 report is built on.</p>")
    body = lead + f"<p>Remember {name} can also send a photo of any homework question they're stuck on.</p>"
    subject = f"3 days in: how {_first(u.full_name)} is doing"
    html = _shell("Halfway through the free trial week", "Three days in", body
                  + f'<p style="margin-top:20px">{_btn(_site("/tests"), "Open Notenix")}</p>')
    text = f"Three days into {name}'s trial: {done} tests done, {left} waiting. {_site('/tests')}"
    return subject, html, text


def ending(u: User, p: dict) -> tuple[str, str, str]:
    name, price = _first(u.full_name), _price(u)
    body = (f"<p>{name}'s free trial ends in <b>2 days</b>. On day 7 we'll email your progress report.</p>"
            f"<p>To keep going, Notenix KS3 is <b>{price} a year</b>: a timed test every half-term in Maths, "
            f"Science and English, homework help, KS3 notes, and a progress report in your inbox every month, "
            f"from Year 7 all the way to GCSE.</p>"
            f"<p>Nothing is lost when the trial ends. {name}'s results stay saved and carry on when you continue.</p>")
    subject = f"{_first(u.full_name)}'s free trial ends in 2 days"
    html = _shell(f"Keep tracking for {price} a year", "2 days left", body
                  + f'<p style="margin-top:20px">{_btn(settings.ks3_upgrade_url, f"Continue for {price}/year")}</p>')
    text = f"{name}'s free trial ends in 2 days. Continue for {price}/year: {settings.ks3_upgrade_url}"
    return subject, html, text


def report(u: User, p: dict) -> tuple[str, str, str]:
    name, price, yr = _first(u.full_name), _price(u), u.ks3_year or 7
    if p["taken"]:
        body = (f"<p>Here's what a week of Notenix showed about {name}.</p>"
                f'<p style="margin:16px 0 4px;color:{INK};font-weight:700">Scores by subject</p>{_subject_table(p)}'
                f"{_topic_list(p['strengths'], 'Strong topics', GOOD)}"
                f"{_topic_list(p['focus'], 'Topics to work on first', WEAK)}")
        if p["gcse"]:
            body += (f'<div style="background:#f8fafc;border:1px solid {LINE};border-radius:12px;padding:14px 16px;margin:18px 0">'
                     f'<div style="font-size:12px;color:{MUTED}">Early GCSE indicator</div>'
                     f'<div style="font-size:18px;font-weight:700;color:{INK};margin-top:2px">Working towards grades {p["gcse"]}</div>'
                     f'<div style="font-size:12px;color:{MUTED};margin-top:4px">Based on {len(p["taken"])} test'
                     f'{"s" if len(p["taken"]) != 1 else ""} so far. It is a starting point, not a prediction: '
                     f"Year {yr} is exactly when steady practice moves it.</div></div>")
        if p["missed"]:
            body += f"<p>{len(p['missed'])} test{'s were' if len(p['missed']) != 1 else ' was'} not taken, so this picture is partial.</p>"
    else:
        body = (f"<p>{name} didn't sit the baseline tests during the trial, so we can't show scores yet. "
                f"The tests are still there whenever {name} is ready.</p>")
    body += (f'<p style="margin:20px 0 6px;color:{INK};font-weight:700">Two ways to keep {name} moving</p>'
             f"<p style=\"margin:0 0 6px\"><b>Notenix KS3, {price}/year:</b> a timed test every half-term, homework help, "
             f"notes, and this report every month, from Year 7 to GCSE.</p>"
             f"<p style=\"margin:0\"><b>A free trial class with Beyond Tutors:</b> a 1-to-1 tutor works on the topics above.</p>")
    subject = f"{_first(u.full_name)}'s 1-week progress report"
    html = _shell(f"Scores, strong topics and what to fix first", f"{name}'s progress report", body
                  + f'<p style="margin-top:20px">{_btn(settings.ks3_upgrade_url, f"Continue Notenix KS3 ({price}/yr)")}'
                  f'{_btn(settings.book_class_url, "Book a free trial class", primary=False)}</p>')
    lines = [f"{k}: {v['latest']}%" for k, v in p["subjects"].items()] or ["No tests taken yet."]
    text = (f"{name}'s 1-week progress report\n" + "\n".join(lines)
            + f"\nContinue: {settings.ks3_upgrade_url}\nBook a free class: {settings.book_class_url}")
    return subject, html, text



def monthly(u: User, p: dict) -> tuple[str, str, str]:
    """Paying families, once a month: the whole trend so far plus this month's tests."""
    name, yr = _first(u.full_name), u.ks3_year or 7
    month = datetime.utcnow().strftime("%B")
    recent = [x for x in p["taken"] if x["date"] and x["date"] > datetime.utcnow() - timedelta(days=31)]
    if p["taken"]:
        body = (f"<p>Here's {name}'s Notenix progress, Year {yr}. "
                f"{len(recent)} test{'s' if len(recent) != 1 else ''} this month, {len(p['taken'])} so far in total.</p>"
                f'<p style="margin:16px 0 4px;color:{INK};font-weight:700">Latest score in each subject '
                f'<span style="color:#94a3b8;font-weight:500">(change since the first test)</span></p>{_subject_table(p)}'
                f"{_topic_list(p['strengths'], 'Strong topics', GOOD)}"
                f"{_topic_list(p['focus'], 'Topics to work on next', WEAK)}")
        if p["gcse"]:
            body += (f'<div style="background:#f8fafc;border:1px solid {LINE};border-radius:12px;padding:14px 16px;margin:18px 0">'
                     f'<div style="font-size:12px;color:{MUTED}">Early GCSE indicator</div>'
                     f'<div style="font-size:18px;font-weight:700;color:{INK};margin-top:2px">Working towards grades {p["gcse"]}</div>'
                     f'<div style="font-size:12px;color:{MUTED};margin-top:4px">A starting point from {len(p["taken"])} tests, not a prediction.</div></div>')
        if p["missed"]:
            body += f"<p>{len(p['missed'])} test{'s are' if len(p['missed']) != 1 else ' is'} still waiting in Notenix.</p>"
    else:
        body = f"<p>{name} hasn't taken any tests yet. They're waiting in Notenix whenever {name} is ready.</p>"
    body += (f"<p>Need more help with the topics above? A Beyond Tutors tutor can work on them 1-to-1; "
             f'the first class is free.</p>')
    subject = f"{_first(u.full_name)}'s {month} progress report"
    html = _shell("This month's scores and what to work on next", f"{name}'s {month} report", body
                  + f'<p style="margin-top:20px">{_btn(_site("/tests"), "Open Notenix")}'
                  f'{_btn(settings.book_class_url, "Book a free class", primary=False)}</p>')
    lines = [f"{k}: {v['latest']}%" for k, v in p["subjects"].items()] or ["No tests taken yet."]
    return subject, html, f"{name}'s {month} progress report\n" + "\n".join(lines) + f"\n{_site('/tests')}"


def year_set_now(u: User) -> None:
    """The KS3 year was just set by hand or at sign-up: it is right for this school year,
    so the automatic move up waits until next September."""
    now = datetime.utcnow()
    start = now.year if now.month >= 9 else now.year - 1
    u.ks3_emails = sorted(set(u.ks3_emails or []) | {f"yearup-{start}"})


def half_term(d: datetime) -> int:
    """English school half-term number (1 = Sep-Oct ... 6 = Jun-Jul) for a date."""
    return {9: 1, 10: 1, 11: 2, 12: 2, 1: 3, 2: 3, 3: 4, 4: 5, 5: 5, 6: 6, 7: 6, 8: 6}[d.month]


async def assign_due_tests(db, u: User) -> int:
    """Give a KS3 student the baseline for their year plus every half-term test that is due."""
    from models import Test, TestAssignment
    if not u.ks3_year:
        return 0
    wanted = [f"y{u.ks3_year}-baseline"]
    if u.access_kind != "trial":
        wanted += [f"y{u.ks3_year}-ht{n}" for n in range(1, half_term(datetime.utcnow()) + 1)]
    tests = (await db.execute(select(Test).where(Test.ks3_slot.in_(wanted), Test.is_archived == False))).scalars().all()  # noqa: E712
    if not tests:
        return 0
    have = set((await db.execute(select(TestAssignment.test_id).where(
        TestAssignment.student_id == u.id, TestAssignment.test_id.in_([t.id for t in tests])))).scalars().all())
    owner = await db.scalar(select(User.id).where(User.role == "admin").order_by(User.id).limit(1))
    added = 0
    for t in tests:
        if t.id not in have:
            label = "baseline" if t.ks3_slot.endswith("baseline") else f"half-term {t.ks3_slot.rsplit('ht', 1)[-1]}"
            db.add(TestAssignment(test_id=t.id, student_id=u.id, assigned_by=owner or t.owner_id,
                                  class_label=f"KS3 Year {u.ks3_year} {label}"))
            added += 1
    return added


async def run_yearly() -> dict:
    """Paying KS3 families: due tests, the September year-up, and one report a month."""
    from services.ks3_content import share_year_notes
    now = datetime.utcnow()
    stats = {"assigned": 0, "promoted": 0, "monthly": 0}
    async with SessionLocal() as db:
        users = (await db.execute(select(User).where(
            User.ks3_year.isnot(None), User.needs_activation == False, User.is_active == True,  # noqa: E712
        ))).scalars().all()
        for u in users:
            live = u.access_until is None or u.access_until > now
            if not live or u.access_kind == "trial":
                continue
            done = set(u.ks3_emails or [])
            year_key = f"yearup-{now.year}"
            if now.month >= 9 and year_key not in done:
                if u.ks3_year < 9:
                    u.ks3_year += 1
                    stats["promoted"] += 1
                done.add(year_key)
                await share_year_notes(db, u)
            stats["assigned"] += await assign_due_tests(db, u)
            month_key = f"monthly-{now:%Y-%m}"
            paid_since = (u.access_until - timedelta(days=settings.subscription_days)) if u.access_until else u.created_at
            if month_key not in done and u.parent_email and paid_since and now - paid_since > timedelta(days=14):
                try:
                    subject, html, text = await render(db, u, "monthly")
                    await _deliver(u.parent_email, subject, html, text)
                    stats["monthly"] += 1
                except Exception as e:
                    print(f"[ks3] monthly report for {u.id} failed: {e}")
                done.add(month_key)
            u.ks3_emails = sorted(done)
        await db.commit()
    return stats


BUILDERS = {"welcome": welcome, "checkin": checkin, "ending": ending, "report": report, "monthly": monthly}


async def render(db, u: User, kind: str) -> tuple[str, str, str]:
    return BUILDERS[kind](u, await progress(db, u))


async def send(db, u: User, kind: str) -> bool:
    """Send one sequence email to the parent and record it; returns False if not sent."""
    if not u.parent_email:
        return False
    subject, html, text = await render(db, u, kind)
    ok = await _deliver(u.parent_email, subject, html, text)
    u.ks3_emails = sorted(set((u.ks3_emails or []) + [kind]))
    return ok


async def run_sequence() -> int:
    """Send whatever trial emails are due. Safe to run often: each email goes once."""
    sent = 0
    now = datetime.utcnow()
    async with SessionLocal() as db:
        users = (await db.execute(select(User).where(
            User.ks3_trial_started_at.isnot(None), User.ks3_trial_started_at > now - timedelta(days=30),
            User.is_active == True,  # noqa: E712
        ))).scalars().all()
        for u in users:
            done = set(u.ks3_emails or [])
            days = (now - u.ks3_trial_started_at).total_seconds() / 86400
            if u.access_kind == "paid":
                continue  # already a paying family: no trial nudges
            due = [k for k, d in SEQUENCE if days >= d and k not in done]
            if not due:
                continue
            # Only the latest due email: a late-running server never sends a burst.
            kind = due[-1]
            try:
                await send(db, u, kind)
                u.ks3_emails = sorted(set((u.ks3_emails or []) + due))
                sent += 1
            except Exception as e:
                print(f"[ks3] {kind} email for user {u.id} failed: {e}")
        await db.commit()
    return sent
