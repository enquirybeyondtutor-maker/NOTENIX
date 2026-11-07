"""Class notes: teachers upload notes (text and/or one PDF/image) and share them with students."""
import asyncio
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from database import get_db, SessionLocal
from models import User, ClassNote, NoteShare, HomeworkSubmission, NotePage
from services import note_pages
from services.email import in_background, send_new_material
from security import require_teacher, get_current_user, is_admin

router = APIRouter(tags=["notes"])

MAX_FILE_CHARS = 12_000_000  # ~9 MB file once base64-encoded


# ── Page images for students: rendered once per note in the background ──────────
_rendering: dict[int, asyncio.Task] = {}


async def _render_pages(note_id: int) -> None:
    async with SessionLocal() as db:
        if (await db.execute(select(NotePage.id).where(NotePage.note_id == note_id).limit(1))).first():
            return
        data = await db.scalar(select(ClassNote.file_data).where(ClassNote.id == note_id))
        if not data:
            return
        try:
            images = await run_in_threadpool(note_pages.render_all, data)
        except Exception as e:
            print(f"[notes] could not render note {note_id}: {e}")
            return
        del data
        for i, img in enumerate(images, 1):
            db.add(NotePage(note_id=note_id, page=i, data=img))
        await db.commit()


def start_render(note_id: int) -> None:
    t = _rendering.get(note_id)
    if t and not t.done():
        return
    task = asyncio.create_task(_render_pages(note_id))
    _rendering[note_id] = task
    task.add_done_callback(lambda _t: _rendering.pop(note_id, None))


async def _page_count(note_id: int, db: AsyncSession) -> int | None:
    """Number of ready pages, or None while they are still being made."""
    n = await db.scalar(select(func.count()).select_from(NotePage).where(NotePage.note_id == note_id))
    if n:
        return n
    start_render(note_id)
    return None


class NoteIn(BaseModel):
    title: str
    subject: str | None = None
    body: str | None = None
    file_name: str | None = None
    file_data: str | None = None   # data:application/pdf;base64,… or an image data URI
    student_emails: list[str] = []


class ShareIn(BaseModel):
    student_emails: list[str]


def _note_row(n: ClassNote, students: list[dict] | None = None) -> dict:
    row = {
        "id": n.id, "title": n.title, "subject": n.subject, "body": n.body,
        "file_name": n.file_name, "has_file": bool(n.has_file),
        "kind": getattr(n, "kind", None) or "notes",
        "due_at": n.due_at.isoformat() if getattr(n, "due_at", None) else None,
        "class_date": getattr(n, "class_date", None),
        "created_at": n.created_at.isoformat() if n.created_at else None,
    }
    if students is not None:
        row["students"] = students
    return row


async def _share(note: ClassNote, emails: list[str], db: AsyncSession, teacher: User | None = None) -> list[str]:
    """Share with these student IDs; returns the ones that don't exist. Newly added students
    get a "new homework / class notes" email in the background (to their own inbox, if given)."""
    emails = sorted({e.strip().lower() for e in emails if e.strip()})
    if not emails:
        return []
    found = (await db.execute(select(User).where(User.email.in_(emails)))).scalars().all()
    have = {sid for (sid,) in (await db.execute(
        select(NoteShare.student_id).where(NoteShare.note_id == note.id))).all()}
    for u in found:
        if u.id not in have:
            db.add(NoteShare(note_id=note.id, student_id=u.id))
            in_background(send_new_material(u, note.kind or "notes", note.title, note.subject, note.due_at,
                                            note.body, teacher.full_name if teacher else None))
    return [e for e in emails if e not in {u.email for u in found}]


async def _owned(note_id: int, teacher: User, db: AsyncSession) -> ClassNote:
    n = (await db.execute(select(ClassNote).where(ClassNote.id == note_id))).scalar_one_or_none()
    if not n or (n.owner_id != teacher.id and not is_admin(teacher)):
        raise HTTPException(404, "Note not found")
    return n


@router.post("/teacher/notes")
async def create_note(data: NoteIn, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    if not data.title.strip():
        raise HTTPException(400, "Please give the notes a title.")
    if not (data.body or "").strip() and not data.file_data:
        raise HTTPException(400, "Add some text or attach a file.")
    if data.file_data and (not data.file_data.startswith("data:") or len(data.file_data) > MAX_FILE_CHARS):
        raise HTTPException(400, "Attach a PDF or image under 9 MB.")
    n = ClassNote(owner_id=teacher.id, title=data.title.strip()[:200], subject=(data.subject or "").strip()[:80] or None,
                  body=(data.body or "").strip() or None, file_name=(data.file_name or "")[:255] or None,
                  file_data=data.file_data or None)
    db.add(n)
    await db.flush()
    missing = await _share(n, data.student_emails, db, teacher)
    await db.commit()
    await db.refresh(n)
    if n.has_file:
        start_render(n.id)
    return {"note": _note_row(n), "not_found": missing}


@router.get("/teacher/notes")
async def my_notes(teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    q = select(ClassNote).order_by(ClassNote.created_at.desc())
    if not is_admin(teacher):
        q = q.where(ClassNote.owner_id == teacher.id)
    notes = (await db.execute(q)).scalars().all()
    shares: dict[int, list[dict]] = {}
    if notes:
        for nid, uid, email, name in (await db.execute(
            select(NoteShare.note_id, User.id, User.email, User.full_name)
            .join(User, User.id == NoteShare.student_id)
            .where(NoteShare.note_id.in_([n.id for n in notes]))
        )).all():
            shares.setdefault(nid, []).append({"id": uid, "email": email, "full_name": name})
    return [_note_row(n, shares.get(n.id, [])) for n in notes]


@router.post("/teacher/notes/{note_id}/share")
async def share_note(note_id: int, data: ShareIn, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    n = await _owned(note_id, teacher, db)
    missing = await _share(n, data.student_emails, db, teacher)
    await db.commit()
    return {"not_found": missing}


@router.delete("/teacher/notes/{note_id}/share/{student_id}")
async def unshare_note(note_id: int, student_id: int, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    await _owned(note_id, teacher, db)
    await db.execute(delete(NoteShare).where(NoteShare.note_id == note_id, NoteShare.student_id == student_id))
    await db.commit()
    return {"ok": True}


@router.delete("/teacher/notes/{note_id}")
async def delete_note(note_id: int, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    n = await _owned(note_id, teacher, db)
    await db.execute(delete(NoteShare).where(NoteShare.note_id == n.id))
    await db.execute(delete(HomeworkSubmission).where(HomeworkSubmission.note_id == n.id))
    await db.execute(delete(NotePage).where(NotePage.note_id == n.id))
    await db.delete(n)
    await db.commit()
    return {"ok": True}


@router.get("/notes")
async def student_notes(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    notes = (await db.execute(
        select(ClassNote).join(NoteShare, NoteShare.note_id == ClassNote.id)
        .where(NoteShare.student_id == user.id).order_by(ClassNote.created_at.desc())
    )).scalars().all()
    subs = {}
    if notes:
        for sub in (await db.execute(select(HomeworkSubmission).where(
                HomeworkSubmission.student_id == user.id,
                HomeworkSubmission.note_id.in_([n.id for n in notes])))).scalars().all():
            subs[sub.note_id] = _sub_row(sub)
    return [{**_note_row(n), "submission": subs.get(n.id)} for n in notes]


async def _visible(note_id: int, user: User, db: AsyncSession) -> tuple[ClassNote, bool]:
    """(note, is_staff). Students only see notes shared with them."""
    n = (await db.execute(select(ClassNote).where(ClassNote.id == note_id))).scalar_one_or_none()
    staff = bool(n) and (n.owner_id == user.id or is_admin(user))
    shared = n and (await db.execute(select(NoteShare.id).where(
        NoteShare.note_id == note_id, NoteShare.student_id == user.id))).first()
    if not n or not (shared or staff):
        raise HTTPException(404, "Note not found")
    return n, staff


def _sub_row(s: HomeworkSubmission, images: bool = False) -> dict:
    row = {"id": s.id, "note_id": s.note_id, "student_id": s.student_id, "comment": s.comment,
           "submitted_at": s.submitted_at.isoformat() if s.submitted_at else None,
           "mark": s.mark, "feedback": s.feedback, "photos": len(s.images or []),
           "marked_at": s.marked_at.isoformat() if s.marked_at else None}
    if images:
        row["images"] = s.images or []
    return row


@router.get("/notes/{note_id}")
async def get_note(note_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    n, staff = await _visible(note_id, user, db)
    row = _note_row(n)
    if staff:
        # tutors keep the original file
        row["file_data"] = await db.scalar(select(ClassNote.file_data).where(ClassNote.id == n.id))
    elif n.has_file:
        # Students get watermarked page images only (/pages/{n}), never the raw file.
        row["pages"] = await _page_count(n.id, db)
        row["rendering"] = row["pages"] is None
    if not staff and (n.kind or "notes") == "homework":
        sub = (await db.execute(select(HomeworkSubmission).where(
            HomeworkSubmission.note_id == n.id, HomeworkSubmission.student_id == user.id))).scalar_one_or_none()
        row["submission"] = _sub_row(sub, images=True) if sub else None
    return row


@router.get("/notes/{note_id}/pages/{page}")
async def note_page(note_id: int, page: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    n, _ = await _visible(note_id, user, db)
    if not n.has_file:
        raise HTTPException(404, "No file")
    img = await db.scalar(select(NotePage.data).where(NotePage.note_id == n.id, NotePage.page == page))
    if img is None:
        if await _page_count(n.id, db) is None:
            return Response(status_code=202, headers={"Retry-After": "3"})  # still being prepared
        raise HTTPException(404, "No such page")
    jpg = await run_in_threadpool(note_pages.watermark, img, f"{user.full_name} - {user.email}")
    return Response(jpg, media_type="image/jpeg", headers={"Cache-Control": "no-store, private"})


MAX_PHOTOS = 10
MAX_PHOTO_CHARS = 2_000_000


class SubmitIn(BaseModel):
    images: list[str]
    comment: str | None = None


@router.post("/notes/{note_id}/submission")
async def submit_homework(note_id: int, data: SubmitIn, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    n, _ = await _visible(note_id, user, db)
    if (n.kind or "notes") != "homework":
        raise HTTPException(400, "This is not homework.")
    imgs = [i for i in data.images if i]
    if not imgs:
        raise HTTPException(400, "Add at least one photo of your work.")
    if len(imgs) > MAX_PHOTOS:
        raise HTTPException(400, f"Up to {MAX_PHOTOS} photos.")
    if any(not i.startswith("data:image/") or len(i) > MAX_PHOTO_CHARS for i in imgs):
        raise HTTPException(400, "Each photo must be an image under 1.5 MB.")
    sub = (await db.execute(select(HomeworkSubmission).where(
        HomeworkSubmission.note_id == n.id, HomeworkSubmission.student_id == user.id))).scalar_one_or_none()
    if sub and sub.marked_at:
        raise HTTPException(400, "Your tutor has already marked this homework.")
    if not sub:
        sub = HomeworkSubmission(note_id=n.id, student_id=user.id, images=imgs)
        db.add(sub)
    sub.images, sub.comment, sub.submitted_at = imgs, (data.comment or "").strip()[:2000] or None, datetime.utcnow()
    await db.commit()
    return _sub_row(sub)


@router.get("/teacher/homework-submissions")
async def list_submissions(teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    q = (select(HomeworkSubmission, ClassNote, User)
         .join(ClassNote, ClassNote.id == HomeworkSubmission.note_id)
         .join(User, User.id == HomeworkSubmission.student_id)
         .order_by(HomeworkSubmission.submitted_at.desc()))
    if not is_admin(teacher):
        q = q.where(ClassNote.owner_id == teacher.id)
    rows = [{**_sub_row(s), "title": n.title, "due_at": n.due_at.isoformat() if n.due_at else None,
             "student": {"id": u.id, "full_name": u.full_name, "email": u.email}}
            for s, n, u in (await db.execute(q)).all()]
    rows.sort(key=lambda r: r["marked_at"] is not None)  # unmarked first, newest first within each
    return rows


@router.get("/teacher/homework-submissions/{sub_id}")
async def get_submission(sub_id: int, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    s = (await db.execute(select(HomeworkSubmission).where(HomeworkSubmission.id == sub_id))).scalar_one_or_none()
    if not s:
        raise HTTPException(404, "Not found")
    n = await _owned(s.note_id, teacher, db)
    u = (await db.execute(select(User).where(User.id == s.student_id))).scalar_one()
    return {**_sub_row(s, images=True), "title": n.title, "body": n.body, "has_file": bool(n.has_file),
            "due_at": n.due_at.isoformat() if n.due_at else None,
            "student": {"id": u.id, "full_name": u.full_name, "email": u.email}}


class MarkIn(BaseModel):
    mark: str | None = None
    feedback: str | None = None


@router.post("/teacher/homework-submissions/{sub_id}/mark")
async def mark_submission(sub_id: int, data: MarkIn, teacher: User = Depends(require_teacher), db: AsyncSession = Depends(get_db)):
    s = (await db.execute(select(HomeworkSubmission).where(HomeworkSubmission.id == sub_id))).scalar_one_or_none()
    if not s:
        raise HTTPException(404, "Not found")
    await _owned(s.note_id, teacher, db)
    if not (data.mark or "").strip() and not (data.feedback or "").strip():
        raise HTTPException(400, "Add a mark or some feedback.")
    s.mark = (data.mark or "").strip()[:40] or None
    s.feedback = (data.feedback or "").strip() or None
    s.marked_at, s.marked_by = datetime.utcnow(), teacher.id
    await db.commit()
    return _sub_row(s)
