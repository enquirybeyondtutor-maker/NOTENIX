from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.user import User
from services.rag_service import ingest_pdf, get_collection
from routers.auth import get_current_user
import shutil
import os
import tempfile

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

ALLOWED_SUBJECTS = ["maths", "biology", "chemistry", "physics", "computer_science", "economics", "english_literature", "geography", "history", "psychology", "business"]
ALLOWED_LEVELS = ["gcse", "a_level"]
ALLOWED_BOARDS = ["AQA", "Edexcel", "OCR", "Cambridge"]


@router.post("/ingest-pdf")
async def ingest_pdf_endpoint(
    file: UploadFile = File(...),
    subject: str = Form(...),
    level: str = Form(...),
    exam_board: str = Form(...),
    topic: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if subject not in ALLOWED_SUBJECTS:
        raise HTTPException(status_code=400, detail=f"Invalid subject")
    if level not in ALLOWED_LEVELS:
        raise HTTPException(status_code=400, detail="Invalid level")
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        pages_ingested = await ingest_pdf(tmp_path, subject, level, exam_board, topic)
    finally:
        os.unlink(tmp_path)

    return {"message": f"Ingested {pages_ingested} pages", "subject": subject, "topic": topic}


@router.get("/stats")
async def kb_stats():
    collection = get_collection()
    return {"total_documents": collection.count(), "collection": "notenix_knowledge_base"}
