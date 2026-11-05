"""Private API for the BT Sessions desktop app (follow-up after each class).

Auth: header `X-Sync-Key` must equal SYNC_KEY. Students are addressed by email.
"""
import hmac
from datetime import datetime
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from database import get_db
from models import User, ClassNote, NoteShare, Test, TestAssignment, TestAttempt, HomeworkSubmission
from routers.notes import MAX_FILE_CHARS

router = APIRouter(prefix="/sync", tags=["sync"])


def require_sync(x_sync_key: str = Header(default="")):
    want = (settings.sync_key or "").strip().strip('"').strip("'")
    if not want:
        raise HTTPException(401, "SYNC_KEY is not set on the server")
    if not hmac.compare_digest(x_sync_key.strip(), want):
        raise HTTPException(401, f"Bad sync key (server key has {len(want)} characters)")


def _iso(d):
    return d.isoformat() if d else None


async def _owner(db: AsyncSession) -> User:
    email = settings.sync_owner_email.strip().lower()
    u = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if not u:
        u = (await db.execute(select(User).where(User.role == "admin").order_by(User.id))).scalars().first()
    if not u:
        raise HTTPException(500, "No admin account to own uploads (set SYNC_OWNER_EMAIL)")
    return u


async def _student(email: str, db: AsyncSession) -> User:
    u = (await db.execute(select(User).where(User.email == email.strip().lower()))).scalar_one_or_none()
    if not u:
        raise HTTPException(404, f"No Notenix account for {email}")
    return u


class SummaryIn(BaseModel):
    emails: list[str]


@router.post("/summary", dependencies=[Depends(require_sync)])
async def summary(data: SummaryIn, db: AsyncSession = Depends(get_db)):
    """Per student: account/access, notes + homework shared, tests assigned with results."""
    emails = sorted({e.strip().lower() for e in data.emails if e.strip()})
    users = (await db.execute(select(User).where(User.email.in_(emails)))).scalars().all() if emails else []
    out = {e: None for e in emails}
    if not users:
        return out
    ids = [u.id for u in users]
    subs = {(x.note_id, x.student_id): x for x in (await db.execute(
        select(HomeworkSubmission).where(HomeworkSubmission.student_id.in_(ids)))).scalars().all()}
    notes: dict[int, list] = {}
    for sid, n in (await db.execute(
        select(NoteShare.student_id, ClassNote).join(ClassNote, ClassNote.id == NoteShare.note_id)
        .where(NoteShare.student_id.in_(ids)).order_by(ClassNote.created_at.desc())
    )).all():
        notes.setdefault(sid, []).append({
            "id": n.id, "title": n.title, "kind": n.kind or "notes", "file_name": n.file_name,
            "class_date": n.class_date, "due_at": _iso(n.due_at), "created_at": _iso(n.created_at),
            "handed_in": _iso(subs[(n.id, sid)].submitted_at) if (n.id, sid) in subs else None,
            "mark": subs[(n.id, sid)].mark if (n.id, sid) in subs else None,
            "marked": bool(subs[(n.id, sid)].marked_at) if (n.id, sid) in subs else False,
        })
    attempts = {}
    for at in (await db.execute(select(TestAttempt).where(TestAttempt.student_id.in_(ids)))).scalars().all():
        attempts[at.assignment_id] = at
    tests: dict[int, list] = {}
    for a, t in (await db.execute(
        select(TestAssignment, Test).join(Test, Test.id == TestAssignment.test_id)
        .where(TestAssignment.student_id.in_(ids)).order_by(TestAssignment.created_at.desc())
    )).all():
        at = attempts.get(a.id)
        tests.setdefault(a.student_id, []).append({
            "assignment_id": a.id, "test_id": t.id, "title": t.title, "kind": t.kind or "test",
            "class_label": a.class_label, "assigned_at": _iso(a.created_at), "due_at": _iso(a.due_at),
            "status": a.status, "score": at.score if at else None,
            "attempt_status": at.status if at else None, "completed_at": _iso(at.completed_at) if at else None,
        })
    for u in users:
        out[u.email] = {
            "id": u.id, "full_name": u.full_name,
            "access_until": _iso(u.access_until), "access_kind": u.access_kind,
            "needs_activation": bool(u.needs_activation), "last_active": _iso(u.last_active),
            "notes": notes.get(u.id, []), "tests": tests.get(u.id, []),
        }
    return out


@router.get("/tests", dependencies=[Depends(require_sync)])
async def list_tests(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Test).where(Test.is_archived == False).order_by(Test.created_at.desc()))).scalars().all()  # noqa: E712
    return [{"id": t.id, "title": t.title, "subject": t.subject, "level": t.level,
             "num_questions": t.num_questions, "created_at": _iso(t.created_at)} for t in rows]


class UploadIn(BaseModel):
    email: str
    kind: str = "notes"          # notes | homework
    title: str
    body: str | None = None
    file_name: str | None = None
    file_data: str | None = None  # data URI
    class_date: str | None = None
    due_at: datetime | None = None


@router.post("/upload", dependencies=[Depends(require_sync)])
async def upload(data: UploadIn, db: AsyncSession = Depends(get_db)):
    if data.kind not in ("notes", "homework"):
        raise HTTPException(400, "kind must be notes or homework")
    if not data.title.strip():
        raise HTTPException(400, "Title needed")
    if not (data.body or "").strip() and not data.file_data:
        raise HTTPException(400, "Add some text or a file")
    if data.file_data and (not data.file_data.startswith("data:") or len(data.file_data) > MAX_FILE_CHARS):
        raise HTTPException(400, "File must be a PDF or image under 9 MB")
    s = await _student(data.email, db)
    owner = await _owner(db)
    n = ClassNote(owner_id=owner.id, title=data.title.strip()[:200], kind=data.kind,
                  body=(data.body or "").strip() or None, file_name=(data.file_name or "")[:255] or None,
                  file_data=data.file_data or None, class_date=(data.class_date or None),
                  due_at=data.due_at.replace(tzinfo=None) if data.due_at else None)
    db.add(n)
    await db.flush()
    db.add(NoteShare(note_id=n.id, student_id=s.id))
    await db.commit()
    return {"id": n.id}


class AssignIn(BaseModel):
    email: str
    test_id: int
    class_label: str | None = None
    due_at: datetime | None = None


@router.post("/assign", dependencies=[Depends(require_sync)])
async def assign(data: AssignIn, db: AsyncSession = Depends(get_db)):
    s = await _student(data.email, db)
    t = (await db.execute(select(Test).where(Test.id == data.test_id))).scalar_one_or_none()
    if not t:
        raise HTTPException(404, "Test not found")
    exists = (await db.execute(select(TestAssignment.id).where(
        TestAssignment.test_id == t.id, TestAssignment.student_id == s.id))).first()
    if exists:
        return {"id": exists[0], "already": True}
    owner = await _owner(db)
    a = TestAssignment(test_id=t.id, student_id=s.id, assigned_by=owner.id, class_label=data.class_label,
                       due_at=data.due_at.replace(tzinfo=None) if data.due_at else None)
    db.add(a)
    await db.commit()
    return {"id": a.id, "already": False}
