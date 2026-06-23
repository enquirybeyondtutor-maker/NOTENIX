"""One-time ingestion: walk knowledge_base/, parse QP PDFs, store exam questions in the DB.

Usage:
    # local sqlite (test):
    python run_ingestion.py
    # against Neon production:
    set DATABASE_URL=postgresql://...   (or export on mac/linux)
    python run_ingestion.py
"""
import os
import re
import sys
import asyncio

# make backend importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from parser import extract_questions  # noqa: E402
from database import SessionLocal, init_db  # noqa: E402
from models import Question  # noqa: E402
from sqlalchemy import delete  # noqa: E402

KB_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge_base")
BOARDS = {"aqa", "edexcel", "ocr", "cambridge", "wjec", "ccea", "edexcel (b)", "edexcel b", "ocr a", "ocr b", "cie"}

LEVEL_MAP = {
    "a levels": "A-Level", "a level": "A-Level", "a-level": "A-Level",
    "gcse": "GCSE", "igcse": "IGCSE",
}


def normalize_level(name: str) -> str:
    return LEVEL_MAP.get(name.strip().lower(), name.strip())


def clean_topic(filename: str) -> str:
    t = os.path.splitext(filename)[0]
    t = re.sub(r"\(\d+\)", "", t)                          # remove "(1)" dup markers
    t = re.sub(r"^\d+(\.\d+)*\s*", "", t)                  # remove leading "1.6 "
    t = re.sub(r"\b(QP|MS|MCQ|Question Paper|Mark Scheme)\b", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s{2,}", " ", t).strip(" -_")
    return t or "General"


def classify(path: str) -> dict | None:
    rel = os.path.relpath(path, KB_DIR)
    parts = rel.split(os.sep)
    if len(parts) < 2:
        return None
    level = normalize_level(parts[0])
    subject = parts[1].strip().title()
    board = "General"
    for p in parts[2:-1]:
        if p.strip().lower() in BOARDS:
            board = p.strip()
            break
    else:
        if len(parts) >= 4:
            board = parts[2].strip()
    topic = clean_topic(parts[-1])
    return {"level": level, "subject": subject, "exam_board": board, "topic": topic}


def is_duplicate_file(name: str) -> bool:
    # skip "(1)" duplicate downloads and mark-scheme files
    if re.search(r"\(\d+\)\.pdf$", name):
        return True
    if re.search(r"\bMS\b", name, re.IGNORECASE) and not re.search(r"\bQP\b", name, re.IGNORECASE):
        return True
    return False


async def main():
    await init_db()
    pdfs = []
    for root, _, files in os.walk(KB_DIR):
        for f in files:
            if f.lower().endswith(".pdf") and not is_duplicate_file(f):
                pdfs.append(os.path.join(root, f))

    print(f"Found {len(pdfs)} PDF files to ingest\n")
    total_q = 0
    async with SessionLocal() as db:
        # fresh import: clear existing extracted questions
        await db.execute(delete(Question).where(Question.source_type == "extracted"))
        await db.commit()

        for i, path in enumerate(pdfs, 1):
            meta = classify(path)
            if not meta:
                continue
            questions = extract_questions(path)
            if not questions:
                print(f"[{i}/{len(pdfs)}] {meta['subject']}/{meta['topic']}: no questions parsed")
                continue
            for q in questions:
                db.add(Question(
                    subject=meta["subject"], topic=meta["topic"],
                    exam_board=meta["exam_board"], level=meta["level"],
                    qtype="exam", question_text=q["text"], marks=q["marks"],
                    source_file=os.path.basename(path), source_type="extracted",
                ))
            total_q += len(questions)
            print(f"[{i}/{len(pdfs)}] {meta['level']} {meta['subject']} / {meta['topic']} "
                  f"({meta['exam_board']}): +{len(questions)} questions")
            if i % 20 == 0:
                await db.commit()
        await db.commit()

    print(f"\nDONE. Ingested {total_q} exam questions from {len(pdfs)} PDFs.")


if __name__ == "__main__":
    asyncio.run(main())
