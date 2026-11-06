"""Loads Notenix KS3 tests and notes from backend/ks3_content/*.json on startup.

tests/<slot>-<subject>.json : {"slot", "subject", "title", "topic", "duration", "questions": [...]}
notes/<key>.json            : {"key", "year", "subject", "title", "body"}

Matching rows are created or updated in place (key = slot+subject for tests, key for notes),
so fixing a typo is a normal deploy. New notes are shared with that year's KS3 students.
"""
import json
from pathlib import Path
from datetime import datetime
from sqlalchemy import select, insert
from database import SessionLocal
from models import User, Test, ClassNote, NoteShare

ROOT = Path(__file__).resolve().parent.parent / "ks3_content"


def _load(folder: str) -> list[dict]:
    out = []
    for p in sorted((ROOT / folder).glob("*.json")):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"[ks3-content] skipped {p.name}: {e}")
    return out


def _check(t: dict) -> list[str]:
    errs = []
    for i, q in enumerate(t.get("questions", []), 1):
        if q.get("options") and q.get("answer") not in q["options"]:
            errs.append(f"Q{i} answer not in options")
        if not q.get("topic"):
            errs.append(f"Q{i} has no topic")
    return errs


async def sync_content() -> dict:
    stats = {"tests_new": 0, "tests_updated": 0, "notes_new": 0, "notes_updated": 0, "shares": 0}
    async with SessionLocal() as db:
        owner = await db.scalar(select(User).where(User.role == "admin").order_by(User.id).limit(1))
        if not owner:
            return stats
        for t in _load("tests"):
            errs = _check(t)
            if errs:
                print(f"[ks3-content] {t.get('slot')} {t.get('subject')}: not loaded: {errs[:3]}")
                continue
            row = await db.scalar(select(Test).where(Test.ks3_slot == t["slot"], Test.subject == t["subject"]))
            fields = dict(title=t["title"], topic=t.get("topic", "Baseline"), level=t.get("level", "KS3"),
                          exam_board=t.get("board", "National Curriculum"), mode="mcq", kind="test",
                          questions=t["questions"], num_questions=len(t["questions"]),
                          duration_minutes=t.get("duration"))
            if not row:
                db.add(Test(owner_id=owner.id, subject=t["subject"], ks3_slot=t["slot"], **fields))
                stats["tests_new"] += 1
            elif row.questions != t["questions"] or row.title != t["title"] or row.duration_minutes != t.get("duration"):
                for k, v in fields.items():
                    setattr(row, k, v)
                stats["tests_updated"] += 1
        await db.flush()
        for n in _load("notes"):
            row = await db.scalar(select(ClassNote).where(ClassNote.ks3_key == n["key"]))
            if not row:
                row = ClassNote(owner_id=owner.id, ks3_key=n["key"], ks3_year=n["year"], kind="notes",
                                title=n["title"], subject=n["subject"], body=n["body"])
                db.add(row)
                stats["notes_new"] += 1
            elif (row.title, row.body, row.subject) != (n["title"], n["body"], n["subject"]):
                row.title, row.body, row.subject = n["title"], n["body"], n["subject"]
                stats["notes_updated"] += 1
        await db.flush()
        stats["shares"] = await share_year_notes(db)
        await db.commit()
    return stats


async def share_year_notes(db, student: User | None = None) -> int:
    """Share every KS3 note for a student's year with them (all KS3 students if none given)."""
    students = [student] if student else (await db.execute(
        select(User).where(User.ks3_year.isnot(None), User.needs_activation == False))).scalars().all()  # noqa: E712
    added = 0
    for s in students:
        notes = (await db.execute(select(ClassNote.id).where(ClassNote.ks3_year == s.ks3_year))).scalars().all()
        if not notes:
            continue
        have = set((await db.execute(select(NoteShare.note_id).where(
            NoteShare.student_id == s.id, NoteShare.note_id.in_(notes)))).scalars().all())
        rows = [{"note_id": nid, "student_id": s.id, "created_at": datetime.utcnow()} for nid in notes if nid not in have]
        if rows:  # one batched insert instead of a round trip per note
            await db.execute(insert(NoteShare), rows)
            added += len(rows)
    return added
