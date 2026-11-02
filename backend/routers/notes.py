"""Class notes: teachers upload notes (text and/or one PDF/image) and share them with students."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database import get_db
from models import User, ClassNote, NoteShare
from security import require_teacher, get_current_user, is_admin

router = APIRouter(tags=["notes"])

MAX_FILE_CHARS = 12_000_000  # ~9 MB file once base64-encoded


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
        "file_name": n.file_name, "has_file": bool(n.file_data),
        "created_at": n.created_at.isoformat() if n.created_at else None,
    }
    if students is not None:
        row["students"] = students
    return row


async def _share(note: ClassNote, emails: list[str], db: AsyncSession) -> list[str]:
    """Share with these student IDs; returns the ones that don't exist."""
    emails = sorted({e.strip().lower() for e in emails if e.strip()})
    if not emails:
        return []
    found = (await db.execute(select(User).where(User.email.in_(emails)))).scalars().all()
    have = {sid for (sid,) in (await db.execute(
        select(NoteShare.student_id).where(NoteShare.note_id == note.id))).all()}
    for u in found:
        if u.id not in have:
            db.add(NoteShare(note_id=note.id, student_id=u.id))
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
    missing = await _share(n, data.student_emails, db)
    await db.commit()
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
    missing = await _share(n, data.student_emails, db)
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
    await db.delete(n)
    await db.commit()
    return {"ok": True}


@router.get("/notes")
async def student_notes(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    notes = (await db.execute(
        select(ClassNote).join(NoteShare, NoteShare.note_id == ClassNote.id)
        .where(NoteShare.student_id == user.id).order_by(ClassNote.created_at.desc())
    )).scalars().all()
    return [_note_row(n) for n in notes]


@router.get("/notes/{note_id}")
async def get_note(note_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    n = (await db.execute(select(ClassNote).where(ClassNote.id == note_id))).scalar_one_or_none()
    shared = n and (await db.execute(select(NoteShare.id).where(
        NoteShare.note_id == note_id, NoteShare.student_id == user.id))).first()
    if not n or not (shared or n.owner_id == user.id or is_admin(user)):
        raise HTTPException(404, "Note not found")
    return {**_note_row(n), "file_data": n.file_data}
