"""KS3 homework help: students send a stuck homework question, tutors reply.

Free week: up to KS3_HELP_TRIAL_CAP questions. Paying families: KS3_HELP_MONTHLY_CAP a month.
"""
from datetime import datetime, timedelta
from html import escape
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from database import get_db
from models import User, HelpRequest
from security import get_current_user, require_teacher
from services.email import notify_admins, send_notice

router = APIRouter(tags=["help"])

SUBJECTS = ("Maths", "Science", "English", "Other")
MAX_PHOTOS = 4
MAX_PHOTO_CHARS = 2_000_000


def _row(h: HelpRequest, images: bool = True) -> dict:
    row = {"id": h.id, "subject": h.subject, "question": h.question, "status": h.status, "reply": h.reply,
           "created_at": h.created_at.isoformat() if h.created_at else None,
           "replied_at": h.replied_at.isoformat() if h.replied_at else None,
           "photos": len(h.images or [])}
    if images:
        row["images"], row["reply_images"] = h.images or [], h.reply_images or []
    return row


async def _allowance(u: User, db: AsyncSession) -> dict:
    trial = u.access_kind == "trial"
    q = select(func.count()).select_from(HelpRequest).where(HelpRequest.student_id == u.id)
    if not trial:
        q = q.where(HelpRequest.created_at >= datetime.utcnow() - timedelta(days=30))
    used = await db.scalar(q) or 0
    cap = settings.ks3_help_trial_cap if trial else settings.ks3_help_monthly_cap
    return {"used": used, "cap": cap, "left": max(0, cap - used), "period": "trial" if trial else "month"}


def _require_ks3(u: User) -> None:
    if not u.ks3_year:
        raise HTTPException(403, "Homework help is part of Notenix KS3.")


@router.get("/help")
async def my_help(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    _require_ks3(user)
    rows = (await db.execute(select(HelpRequest).where(HelpRequest.student_id == user.id)
                             .order_by(HelpRequest.created_at.desc()))).scalars().all()
    return {"requests": [_row(h) for h in rows], "allowance": await _allowance(user, db)}


class AskIn(BaseModel):
    subject: str
    question: str | None = None
    images: list[str] = []


@router.post("/help")
async def ask(data: AskIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    _require_ks3(user)
    if data.subject not in SUBJECTS:
        raise HTTPException(400, "Pick a subject.")
    text = (data.question or "").strip()[:3000]
    imgs = [i for i in data.images if i][:MAX_PHOTOS]
    if not text and not imgs:
        raise HTTPException(400, "Add a photo of the question or type it out.")
    if any(not i.startswith("data:image/") or len(i) > MAX_PHOTO_CHARS for i in imgs):
        raise HTTPException(400, "Each photo must be an image under 1.5 MB.")
    allow = await _allowance(user, db)
    if allow["left"] <= 0:
        raise HTTPException(429, "You've used all your homework-help questions for the free week. "
                                 "Continue Notenix KS3 to keep asking." if allow["period"] == "trial" else
                                 "You've reached this month's homework-help limit. It resets in a few days.")
    h = HelpRequest(student_id=user.id, subject=data.subject, question=text or None, images=imgs or None)
    db.add(h)
    await db.commit()
    await notify_admins(f"Homework help: {user.full_name} ({data.subject})",
                        f"{user.full_name} (Year {user.ks3_year}) asked: {text[:200] or '[photo]'}", "/teacher/help")
    return _row(h)


@router.get("/teacher/help")
async def help_queue(teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(HelpRequest, User).join(User, User.id == HelpRequest.student_id)
                             .order_by(HelpRequest.created_at.desc()).limit(200))).all()
    out = [{**_row(h, images=False), "student": {"id": u.id, "full_name": u.full_name, "email": u.email,
                                                 "year": u.ks3_year}} for h, u in rows]
    out.sort(key=lambda r: r["status"] != "open")  # open first, newest first within each
    return out


@router.get("/teacher/help/{help_id}")
async def help_detail(help_id: int, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    row = (await db.execute(select(HelpRequest, User).join(User, User.id == HelpRequest.student_id)
                            .where(HelpRequest.id == help_id))).first()
    if not row:
        raise HTTPException(404, "Not found")
    h, u = row
    return {**_row(h), "student": {"id": u.id, "full_name": u.full_name, "email": u.email, "year": u.ks3_year}}


class ReplyIn(BaseModel):
    reply: str
    images: list[str] = []


@router.post("/teacher/help/{help_id}/reply")
async def reply(help_id: int, data: ReplyIn, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    h = (await db.execute(select(HelpRequest).where(HelpRequest.id == help_id))).scalar_one_or_none()
    if not h:
        raise HTTPException(404, "Not found")
    text = data.reply.strip()
    if not text:
        raise HTTPException(400, "Write a reply.")
    imgs = [i for i in data.images if i][:MAX_PHOTOS]
    if any(not i.startswith("data:image/") or len(i) > MAX_PHOTO_CHARS for i in imgs):
        raise HTTPException(400, "Each photo must be an image under 1.5 MB.")
    first_reply = h.status != "answered"
    h.reply, h.reply_images, h.status = text, imgs or None, "answered"
    h.replied_by, h.replied_at = teacher.id, datetime.utcnow()
    await db.commit()
    if first_reply:
        u = (await db.execute(select(User).where(User.id == h.student_id))).scalar_one()
        name = escape(u.full_name.split(" ")[0])
        for to in {e for e in (u.parent_email,) if e}:
            try:
                await send_notice(to, f"A tutor answered {u.full_name.split(' ')[0]}'s homework question",
                                  "Homework question answered",
                                  f"A Beyond Tutors tutor has replied to {name}'s {escape(h.subject)} homework question. "
                                  f"{name} can see the worked hint in Notenix under <b>Homework help</b>.",
                                  f"A tutor replied to {u.full_name}'s {h.subject} homework question.",
                                  "/help", "Open Notenix")
            except Exception as e:
                print(f"[help] reply email failed: {e}")
    return _row(h)
