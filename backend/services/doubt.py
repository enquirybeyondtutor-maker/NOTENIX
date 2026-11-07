"""Doubt Help ("Ask a tutor"): a student photographs any question they're stuck on and a tutor replies.

Sold on its own, first for Singapore secondary families (Sec 1-4):
  trial  - 5 questions over 7 days, free
  annual - S$249 a year (the main offer), 20 questions every 30 days
  doubt  - 20 questions per 30 days
  plus   - 50 questions per 30 days + 2 live 30-minute doubt calls (booked by WhatsApp)
The questions themselves use the existing homework-help system (HelpRequest, /help, /teacher/help).
"""
from datetime import datetime, timedelta
from sqlalchemy import select
from config import settings
from database import SessionLocal
from models import User
from services import mail_template as T
from services.email import _deliver, best_address

PLANS = {
    "trial": {"name": "Free trial", "cap": 5, "days": 7},
    "annual": {"name": "Ask a Tutor · 1 year", "cap": 20, "days": 365, "window": 30},
    "doubt": {"name": "Doubt Help", "cap": 20, "days": 30},
    "plus": {"name": "Doubt Help Plus", "cap": 50, "days": 30, "calls": 2},
}
PRICES = {  # annual: per year; doubt / plus: per 30 days
    "annual": {"SGD": 249, "GBP": 149, "USD": 189, "AED": 699, "AUD": 289, "INR": 15999},
    "doubt": {"SGD": 39, "GBP": 25, "USD": 29, "AED": 109, "AUD": 45, "INR": 2499},
    "plus": {"SGD": 79, "GBP": 49, "USD": 59, "AED": 215, "AUD": 89, "INR": 4999},
}
LEVELS = ("Sec 1", "Sec 2", "Sec 3", "Sec 4", "Sec 5", "JC 1", "JC 2")
LOWER = ("Science", "Maths", "English", "Other")
UPPER = ("Physics", "Chemistry", "Biology", "Combined Science", "E-Math", "A-Math", "English", "Other")
JC = ("H2 Maths", "H2 Physics", "H2 Chemistry", "H2 Biology", "General Paper", "Other")


def subjects_for(level: str | None) -> tuple[str, ...]:
    if not level:
        return LOWER
    if level.startswith("JC"):
        return JC
    return LOWER if level in ("Sec 1", "Sec 2") else UPPER


def price(plan: str, currency: str | None) -> dict:
    from services.pricing import label
    table = PRICES[plan]
    cur = (currency or "SGD").upper()
    if cur not in table:
        cur = "SGD"
    return {"plan": plan, "currency": cur, "amount": table[cur], "label": label(cur, table[cur])}


def live(u) -> bool:
    return bool(getattr(u, "help_plan", None)) and bool(u.help_until) and u.help_until > datetime.utcnow()


def period_start(u) -> datetime:
    """Questions are counted from here: the trial / 30-day plan start, or for the yearly plan
    the last 30 days (so the 20 questions refresh every month)."""
    plan = PLANS.get(u.help_plan or "", PLANS["doubt"])
    start = (u.help_until or datetime.utcnow()) - timedelta(days=plan["days"])
    if plan.get("window"):
        start = max(start, datetime.utcnow() - timedelta(days=plan["window"]))
    return start


def set_plan(u: User, plan: str | None, days: int | None = None) -> None:
    """Start or extend a plan. Paid plans extend from the current end if still running."""
    now = datetime.utcnow()
    if not plan:
        u.help_plan, u.help_until = None, None
        return
    span = timedelta(days=days or PLANS[plan]["days"])
    start = u.help_until if (plan != "trial" and u.help_plan in ("annual", "doubt", "plus") and u.help_until and u.help_until > now) else now
    u.help_plan, u.help_until = plan, start + span
    # Account access may only grow, never shrink: a Beyond Tutors student with a paid year (or no
    # expiry) keeps it. A Doubt-Help-only account whose access ends sooner is moved to the plan's end.
    if u.access_until is not None and u.access_until < u.help_until:
        u.access_until = u.help_until
        if u.access_kind in (None, "trial", "pending") or u.access_kind == "paid":
            u.access_kind = "trial" if plan == "trial" else "paid"


# ── Emails ─────────────────────────────────────────────────────────────────────

def _first(u) -> str:
    return T.first_name(u.full_name, "your child")


def welcome(u) -> tuple[str, str, str]:
    name = _first(u)
    body = (T.para(f"{name}'s free trial of Ask a Tutor has started. For the next 7 days {name} can send up to "
                   f"<b>5 questions</b>: a photo of anything they're stuck on in {', '.join(subjects_for(u.sg_level)[:3])} "
                   "and more. A Beyond Tutors tutor replies with a clear, step-by-step explanation, usually the same evening "
                   "(Singapore time).") +
            T.login_box(u.email, u.full_name) +
            T.subheading("How it works") +
            '<ol style="margin:0 0 6px;padding-left:20px"><li>Sign in and open <b>Ask a tutor</b>.</li>'
            "<li>Pick the subject, add a photo of the question and say what's confusing.</li>"
            "<li>The tutor's explanation appears in Notenix, and we email you when it's ready.</li></ol>")
    html = T.layout(preheader="5 free questions over the next 7 days", heading=f"{name}'s free trial has started",
                    body=body, buttons=[(T.signin_url(u.email), "Ask the first question")], audience="parent",
                    tagline="Ask a Tutor")
    return f"{name}'s Ask a Tutor trial has started", html, f"{name}'s free trial has started. Login: {u.email}" + T.text_footer()


def ending(u) -> tuple[str, str, str]:
    name = _first(u)
    a = price("annual", u.billing_currency or "SGD")
    d, p = price("doubt", u.billing_currency or "SGD"), price("plus", u.billing_currency or "SGD")
    body = (T.para(f"{name}'s free trial ends in <b>2 days</b>. To keep asking, choose a plan:") +
            T.info_table([("1 year (best value)", f"{a['label']} / year · up to 20 questions every month"),
                          ("Doubt Help", f"{d['label']} / month · up to 20 questions"),
                          ("Doubt Help Plus", f"{p['label']} / month · up to 50 questions + 2 live 30-minute calls")]) +
            T.para("Nothing renews by itself: you choose whether to continue."))
    html = T.layout(preheader=f"Keep asking: {a['label']} for a whole year", heading="2 days left of the free trial", body=body,
                    buttons=[(T.site("/ask-a-tutor/continue"), "Choose a plan")], audience="parent", tagline="Ask a Tutor")
    return f"{name}'s free trial ends in 2 days", html, f"{name}'s trial ends in 2 days. Plans: {T.site('/ask-a-tutor/continue')}" + T.text_footer()


def renew(u) -> tuple[str, str, str]:
    name = _first(u)
    pr = price(u.help_plan if u.help_plan in PRICES else "doubt", u.billing_currency or "SGD")
    span = "year" if u.help_plan == "annual" else "30 days"
    until = u.help_until.strftime("%d %b") if u.help_until else ""
    body = (T.para(f"{name}'s {PLANS.get(u.help_plan, PLANS['doubt'])['name']} runs until <b>{until}</b>. "
                   f"To keep it going for another {span}, the payment is {pr['label']}.") +
            T.para(f"Pay in the same way as before; the next {span} is added to the current end date, so nothing is lost by paying early."))
    html = T.layout(preheader=f"Renews {until} · {pr['label']}", heading=f"{name}'s plan ends on {until}", body=body,
                    buttons=[(T.site("/ask-a-tutor/continue"), f"Renew for {span}")], audience="parent", tagline="Ask a Tutor")
    return f"{name}'s Ask a Tutor plan ends on {until}", html, f"Renew: {T.site('/ask-a-tutor/continue')}" + T.text_footer()


async def run_sequence() -> int:
    """Trial day-5 email and a renewal reminder 3 days before a paid plan ends. Each goes once."""
    now, sent = datetime.utcnow(), 0
    async with SessionLocal() as db:
        users = (await db.execute(select(User).where(User.help_plan.isnot(None), User.help_until > now - timedelta(days=1)))).scalars().all()
        for u in users:
            done = set(u.help_emails or [])
            key, builder = None, None
            if u.help_plan == "trial" and u.help_until - now <= timedelta(days=2) and "ending" not in done:
                key, builder = "ending", ending
            elif u.help_plan in ("annual", "doubt", "plus") and u.help_until - now <= timedelta(days=14 if u.help_plan == "annual" else 3):
                key = f"renew-{u.help_until:%Y-%m-%d}"
                builder = renew if key not in done else None
            to = u.parent_email or best_address(u)
            if not builder or not to:
                continue
            try:
                await _deliver(to, *builder(u))
                sent += 1
            except Exception as e:
                print(f"[doubt] {key} email for {u.id} failed: {e}")
            u.help_emails = sorted(done | {key})
        await db.commit()
    return sent
