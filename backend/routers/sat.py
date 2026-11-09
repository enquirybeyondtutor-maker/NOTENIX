"""Notenix SAT: free diagnostic (no account), 7-day trial sign-up (student's own email),
and the adaptive mock tests. Content and scoring: services/sat.py."""
import hashlib
import hmac
import re
import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db
from models import User, SatAttempt
from security import hash_password, verify_password, create_token, get_current_user
from services import sat
from services import courses as course_svc
from services import pricing
from services.email import (generate_otp, send_otp_email, EmailSendError, notify_admins, in_background,
                            _deliver, is_mailbox)
from services import mail_template as T
from routers.auth import _user_dict, _within_cooldown, _otp_sent_response, EMAIL_FAIL_MSG

router = APIRouter(prefix="/sat", tags=["sat"])

GRACE_SECONDS = 60  # network slack before an overdue module is submitted for the student
TRIAL_DAYS = 7


# ── Free diagnostic (public) ──────────────────────────────────────────────────

@router.get("/diagnostic")
async def diagnostic():
    f = sat.form("diagnostic")
    if not f:
        raise HTTPException(404, "The SAT diagnostic isn't available yet.")
    return {"title": f["title"], "modules": [sat.public_module(f, k) for k in sat.DIAG_STAGES]}


class DiagnosticIn(BaseModel):
    answers: dict[str, str | None]


@router.post("/diagnostic/score")
async def diagnostic_score(data: DiagnosticIn):
    try:
        return sat.score_diagnostic({k: v for k, v in data.answers.items() if isinstance(k, str)})
    except ValueError as ex:
        raise HTTPException(404, str(ex))


@router.get("/price")
async def price(currency: str = "USD"):
    return pricing.sat_for_currency(currency)


# ── 7-day trial: student's own email (code) → password → signed in ───────────

class StartIn(BaseModel):
    full_name: str
    email: EmailStr
    parent_email: EmailStr | None = None
    test_date: str | None = None     # YYYY-MM-DD
    target: int | None = None        # 400–1600
    currency: str | None = None
    agree_terms: bool = False


class VerifyIn(BaseModel):
    email: EmailStr
    code: str


class CompleteIn(BaseModel):
    email: EmailStr
    setup_token: str
    password: str
    diagnostic_answers: dict[str, str | None] | None = None


async def _pending(email: str, db: AsyncSession) -> User:
    u = (await db.execute(select(User).where(User.email == email.lower(), User.access_kind == "sat_pending"))).scalar_one_or_none()
    if not u or not u.otp_hash or not u.otp_expires_at:
        raise HTTPException(400, "Please ask for a code first.")
    if datetime.utcnow() > u.otp_expires_at:
        raise HTTPException(400, "That has expired. Please start again and ask for a new code.")
    if (u.otp_attempts or 0) >= settings.otp_max_attempts:
        raise HTTPException(429, "Too many wrong attempts. Please ask for a new code.")
    return u


@router.post("/trial/start")
async def trial_start(data: StartIn, db: AsyncSession = Depends(get_db)):
    name = re.sub(r"\s+", " ", data.full_name).strip()[:120]
    if len(name) < 2:
        raise HTTPException(400, "Please enter your name.")
    if not data.agree_terms:
        raise HTTPException(400, "Please agree to the Terms and Privacy policy to continue.")
    email = data.email.lower()
    if not is_mailbox(email):
        raise HTTPException(400, "Please enter your own email address.")
    parent = data.parent_email.lower() if data.parent_email else None
    if parent and (parent == email or not is_mailbox(parent)):
        parent = None
    test_date = data.test_date if data.test_date and re.fullmatch(r"\d{4}-\d{2}-\d{2}", data.test_date) else None
    target = data.target if data.target and 400 <= data.target <= 1600 else None

    u = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if u and u.access_kind != "sat_pending":
        raise HTTPException(400, "This email already has a Notenix account. Sign in, then add SAT from My courses.")
    if u and _within_cooldown(u):
        raise HTTPException(429, "Please wait a minute before asking for another code.")
    if not u:
        cur = (data.currency or "USD").upper()
        u = User(email=email, full_name=name, role="student", is_verified=True, password_hash="!",
                 needs_activation=True, token_version=0, access_kind="sat_pending",
                 billing_currency=cur if cur in pricing.SAT_PRICES else "USD")
        db.add(u)
    u.full_name, u.parent_email, u.sat_test_date, u.sat_target = name, parent, test_date, target
    code = generate_otp()
    u.otp_hash = hash_password(code)
    u.otp_expires_at = datetime.utcnow() + timedelta(minutes=settings.otp_expiry_minutes)
    u.otp_attempts = 0
    await db.commit()
    try:
        await send_otp_email(email, name, code, kind="sat")
    except EmailSendError:
        raise HTTPException(502, EMAIL_FAIL_MSG)
    return _otp_sent_response(email, code)


@router.post("/trial/verify")
async def trial_verify(data: VerifyIn, db: AsyncSession = Depends(get_db)):
    u = await _pending(data.email, db)
    if not verify_password(data.code.strip(), u.otp_hash):
        u.otp_attempts = (u.otp_attempts or 0) + 1
        await db.commit()
        raise HTTPException(400, "That code isn't right. Please check the email and try again.")
    token = secrets.token_urlsafe(24)
    u.otp_hash = "sha256$" + hashlib.sha256(token.encode()).hexdigest()
    u.otp_expires_at = datetime.utcnow() + timedelta(minutes=30)
    u.otp_attempts = 0
    await db.commit()
    return {"setup_token": token, "full_name": u.full_name}


@router.post("/trial/complete")
async def trial_complete(data: CompleteIn, db: AsyncSession = Depends(get_db)):
    if len(data.password) < 8:
        raise HTTPException(400, "Please choose a password of at least 8 characters.")
    u = await _pending(data.email, db)
    want = "sha256$" + hashlib.sha256(data.setup_token.encode()).hexdigest()
    if not hmac.compare_digest(want, u.otp_hash or ""):
        u.otp_attempts = (u.otp_attempts or 0) + 1
        await db.commit()
        raise HTTPException(400, "This sign-up link has expired. Please start again.")
    now = datetime.utcnow()
    u.password_hash = hash_password(data.password)
    u.needs_activation = False
    u.activated_at = u.terms_accepted_at = u.last_active = now
    u.otp_hash, u.otp_expires_at, u.otp_attempts = None, None, 0
    u.terms_price = "Free 7-day Notenix SAT trial"
    u.token_version = (u.token_version or 0) + 1
    await db.flush()
    await course_svc.grant(u, "sat", "trial", db, until=now + timedelta(days=TRIAL_DAYS))
    # Keep the diagnostic they took before signing up.
    f = sat.form("diagnostic")
    if f and data.diagnostic_answers:
        ans = {k: v for k, v in data.diagnostic_answers.items() if isinstance(k, str)}
        res = sat.score_diagnostic(ans)
        db.add(SatAttempt(user_id=u.id, form="diagnostic", status="done", stage=2, route={},
                          answers={"rw": {q["id"]: ans.get(q["id"]) for q in f["modules"]["rw"]["questions"]},
                                   "m": {q["id"]: ans.get(q["id"]) for q in f["modules"]["m"]["questions"]}},
                          marked={}, rw_score=sum(res["rw"]["band"]) // 2, math_score=sum(res["math"]["band"]) // 2,
                          total_score=sum(res["total_band"]) // 2, started_at=now, completed_at=now))
    await db.commit()
    in_background(_deliver(u.email, *welcome(u)))
    in_background(notify_admins(f"New SAT trial: {u.full_name}", f"{u.full_name} ({u.email}) started a free Notenix SAT trial.",
                                "/admin", rows=[("Student", u.full_name), ("Email", u.email),
                                                ("Test date", u.sat_test_date or "-"), ("Target", str(u.sat_target or "-"))]))
    return {"access_token": create_token(u.id, u.token_version), "token_type": "bearer", "user": _user_dict(u)}


def welcome(u: User) -> tuple[str, str, str]:
    name = T.first_name(u.full_name)
    p = pricing.sat_for_currency(u.billing_currency)
    body = (T.para(f"Your free week of Notenix SAT has started, {name}. Here is how to use it well:") +
            '<ol style="margin:0 0 6px;padding-left:20px">'
            "<li>Sit <b>Practice Test 1</b> in one go, like the real thing: 2 hours 14 minutes, with the built-in Desmos calculator.</li>"
            "<li>Read your score report: your estimated score out of 1600 and the skills losing you the most points.</li>"
            "<li>Go back through every question you missed. Each one has a worked explanation.</li></ol>" +
            T.login_box(u.email) +
            T.para(f"After your free week, a full year of Notenix SAT is {p['label']}. Nothing renews by itself."))
    html = T.layout(preheader="Your free week of SAT practice starts now", heading="Your Notenix SAT week has started",
                    body=body, buttons=[(T.site("/sat/practice"), "Start Practice Test 1")], audience="student",
                    tagline="SAT")
    text = f"Your free week of Notenix SAT has started. Sign in with {u.email} at notenix.com/sat/practice." + T.text_footer()
    return "Your free week of Notenix SAT has started", html, text


# ── Signed-in SAT practice ────────────────────────────────────────────────────

async def _sat_user(user: User, db: AsyncSession) -> User:
    if not course_svc.allows(await course_svc.live_courses(user, db), "SAT", None):
        raise HTTPException(403, course_svc.locked_message("SAT", None))
    return user


def _attempt_row(a: SatAttempt) -> dict:
    return {"id": a.id, "form": a.form, "status": a.status, "stage": a.stage,
            "rw_score": a.rw_score, "math_score": a.math_score, "total_score": a.total_score,
            "started_at": a.started_at.isoformat() if a.started_at else None,
            "completed_at": a.completed_at.isoformat() if a.completed_at else None}


@router.get("/home")
async def home(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await _sat_user(user, db)
    attempts = (await db.execute(select(SatAttempt).where(SatAttempt.user_id == user.id)
                                 .order_by(SatAttempt.started_at.desc()))).scalars().all()
    rows = await course_svc.enrolments(user.id, db)
    sat_course = next((e for e in rows if e.course == "sat"), None)
    return {
        "test_date": user.sat_test_date, "target": user.sat_target,
        "course": course_svc.enrolment_row(sat_course) if sat_course else None,
        "price": pricing.sat_for_currency(user.billing_currency),
        "forms": [{"slug": f["slug"], "title": f["title"], "summary": f.get("summary", ""),
                   "attempts": [_attempt_row(a) for a in attempts if a.form == f["slug"]]} for f in sat.mocks()],
        "diagnostic": next((_attempt_row(a) for a in attempts if a.form == "diagnostic"), None),
    }


class GoalIn(BaseModel):
    test_date: str | None = None
    target: int | None = None


@router.post("/goal")
async def set_goal(data: GoalIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user.sat_test_date = data.test_date if data.test_date and re.fullmatch(r"\d{4}-\d{2}-\d{2}", data.test_date) else None
    user.sat_target = data.target if data.target and 400 <= data.target <= 1600 else None
    await db.commit()
    return {"test_date": user.sat_test_date, "target": user.sat_target}


@router.post("/forms/{slug}/start")
async def start(slug: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await _sat_user(user, db)
    f = sat.form(slug)
    if not f or f.get("kind") != "mock":
        raise HTTPException(404, "Practice test not found.")
    open_one = (await db.execute(select(SatAttempt).where(
        SatAttempt.user_id == user.id, SatAttempt.form == slug, SatAttempt.status == "in_progress"))).scalars().first()
    if open_one:
        return {"attempt_id": open_one.id, "resumed": True}
    a = SatAttempt(user_id=user.id, form=slug, status="in_progress", stage=0, route={}, answers={}, marked={})
    db.add(a)
    await db.commit()
    await db.refresh(a)
    return {"attempt_id": a.id, "resumed": False}


async def _own(attempt_id: int, user: User, db: AsyncSession) -> tuple[SatAttempt, dict]:
    a = (await db.execute(select(SatAttempt).where(SatAttempt.id == attempt_id, SatAttempt.user_id == user.id))).scalar_one_or_none()
    if not a:
        raise HTTPException(404, "Attempt not found.")
    f = sat.form(a.form)
    if not f:
        raise HTTPException(404, "This practice test is no longer available.")
    return a, f


def _seconds_left(a: SatAttempt, f: dict, key: str) -> int | None:
    if not a.module_started_at:
        return None
    limit = f["modules"][key]["minutes"] * 60
    return int(limit - (datetime.utcnow() - a.module_started_at).total_seconds())


def _advance(a: SatAttempt, f: dict) -> None:
    """Close the current module: route the section's module 2, move on, or finish."""
    key = sat.stage_key(f, a.stage, a.route or {})
    if key in ("rw1", "m1"):
        c, n = sat.module_score(f, key, (a.answers or {}).get(key, {}))
        a.route = {**(a.route or {}), key[:-1] if key == "rw1" else "m": sat.route_for(c, n)}
    a.stage += 1
    a.module_started_at = None   # the next module's clock starts when they open it (breaks allowed)
    if a.stage >= sat.n_stages(f):
        _finish(a, f)


def _finish(a: SatAttempt, f: dict) -> None:
    route, ans = a.route or {}, a.answers or {}
    rw2, m2 = ("rw2h" if route.get("rw") == "h" else "rw2e"), ("m2h" if route.get("m") == "h" else "m2e")
    c1, n1 = sat.module_score(f, "rw1", ans.get("rw1", {}))
    c2, n2 = sat.module_score(f, rw2, ans.get(rw2, {}))
    d1, k1 = sat.module_score(f, "m1", ans.get("m1", {}))
    d2, k2 = sat.module_score(f, m2, ans.get(m2, {}))
    a.rw_score = sat.section_score(c1, n1, c2, n2, route.get("rw", "e"))
    a.math_score = sat.section_score(d1, k1, d2, k2, route.get("m", "e"))
    a.total_score = a.rw_score + a.math_score
    a.status, a.completed_at = "done", datetime.utcnow()


@router.get("/attempts/{attempt_id}")
async def attempt(attempt_id: int, open_module: bool = False, user: User = Depends(get_current_user),
                  db: AsyncSession = Depends(get_db)):
    """The current module. Its clock starts the first time it is opened with open_module=1
    (so a student can take the break between sections)."""
    await _sat_user(user, db)
    a, f = await _own(attempt_id, user, db)
    if a.status == "done":
        return {"status": "done", "attempt": _attempt_row(a)}
    key = sat.stage_key(f, a.stage, a.route or {})
    left = _seconds_left(a, f, key)
    if left is not None and left < -GRACE_SECONDS:
        _advance(a, f)   # time ran out while they were away: submit what was saved
        await db.commit()
        return await attempt(attempt_id, False, user, db)
    if open_module and a.module_started_at is None:
        a.module_started_at = datetime.utcnow()
        await db.commit()
        left = f["modules"][key]["minutes"] * 60
    stages = sat.n_stages(f)
    return {
        "status": "in_progress", "title": f["title"], "stage": a.stage, "stages": stages,
        "module": sat.public_module(f, key), "seconds_left": left, "started": a.module_started_at is not None,
        "answers": (a.answers or {}).get(key, {}), "marked": (a.marked or {}).get(key, []),
        "break_before": a.stage == stages // 2 and a.module_started_at is None,
    }


class SaveIn(BaseModel):
    module: str
    answers: dict[str, str | None] = {}
    marked: list[str] = []


def _save(a: SatAttempt, f: dict, data: SaveIn) -> None:
    key = sat.stage_key(f, a.stage, a.route or {})
    if data.module != key:
        raise HTTPException(409, "This module has already been submitted.")
    ids = {q["id"] for q in f["modules"][key]["questions"]}
    a.answers = {**(a.answers or {}), key: {k: (v or "")[:40] for k, v in data.answers.items() if k in ids}}
    a.marked = {**(a.marked or {}), key: [m for m in data.marked if m in ids]}


@router.put("/attempts/{attempt_id}/save")
async def save(attempt_id: int, data: SaveIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await _sat_user(user, db)
    a, f = await _own(attempt_id, user, db)
    if a.status == "done":
        raise HTTPException(409, "This test is finished.")
    _save(a, f, data)
    await db.commit()
    return {"ok": True}


@router.post("/attempts/{attempt_id}/submit")
async def submit(attempt_id: int, data: SaveIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Submit the current module (with its final answers) and move to the next one."""
    await _sat_user(user, db)
    a, f = await _own(attempt_id, user, db)
    if a.status == "done":
        return {"status": "done", "attempt": _attempt_row(a)}
    _save(a, f, data)
    _advance(a, f)
    await db.commit()
    return {"status": a.status, "stage": a.stage, "attempt": _attempt_row(a)}


@router.get("/attempts/{attempt_id}/result")
async def result(attempt_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    a, f = await _own(attempt_id, user, db)
    if a.status != "done":
        raise HTTPException(400, "Finish the test to see your score.")
    ans, route = a.answers or {}, a.route or {}
    if f.get("kind") == "mock":
        keys = ["rw1", "rw2h" if route.get("rw") == "h" else "rw2e", "m1", "m2h" if route.get("m") == "h" else "m2e"]
    else:
        keys = ["rw", "m"]
    pairs = [(q, ans.get(k, {}).get(q["id"])) for k in keys for q in f["modules"][k]["questions"]]
    rows = sat.breakdown(pairs)
    return {
        "attempt": _attempt_row(a), "title": f["title"], "kind": f.get("kind"), "route": route,
        "target": user.sat_target, "test_date": user.sat_test_date,
        "modules": [{"key": k, "title": f["modules"][k]["title"], "section": f["modules"][k]["section"],
                     "questions": sat.review(f, k, ans.get(k, {}))} for k in keys],
        "skills": rows, "weakest": sat.weakest(rows),
    }
