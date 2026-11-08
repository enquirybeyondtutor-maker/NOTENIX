"""A student's PDF of their answers (e.g. a phone scan) → answer images.

Written tests and worksheet homework both take answers as photos. A PDF is turned into one
JPEG per page, about the size of a phone photo after in-browser compression, so tutors mark
PDF scans and photos the same way."""
import base64

from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool

MAX_PDF_CHARS = 20_000_000  # ~15 MB PDF (base64 data URI)


def _render(raw: bytes, limit: int, max_chars: int) -> tuple[list[str], int]:
    import fitz  # PyMuPDF
    out: list[str] = []
    with fitz.open(stream=raw, filetype="pdf") as doc:
        total = len(doc)
        for page in doc[:limit]:
            zoom = 1200 / max(page.rect.width, page.rect.height)
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
            for q in (75, 55, 40):
                uri = "data:image/jpeg;base64," + base64.b64encode(pix.tobytes("jpeg", jpg_quality=q)).decode()
                if len(uri) <= max_chars:
                    break
            out.append(uri)
    return out, total


async def pdf_to_answer_pages(data_uri: str, limit: int, max_chars: int) -> dict:
    """Render up to `limit` pages. Returns {pages, total_pages, truncated}; raises 400s with
    messages a student can act on."""
    head, _, b64 = (data_uri or "").partition(",")
    if not head.startswith("data:application/pdf") or not b64:
        raise HTTPException(400, "Please choose a PDF file.")
    if len(data_uri) > MAX_PDF_CHARS:
        raise HTTPException(400, "That PDF is too large (max about 15 MB). Try a smaller scan, or add photos instead.")
    limit = max(0, min(int(limit or 0), 24))
    if limit == 0:
        raise HTTPException(400, "You've already added the most pages allowed here.")
    try:
        pages, total = await run_in_threadpool(_render, base64.b64decode(b64), limit, max_chars)
    except Exception:
        raise HTTPException(400, "Couldn't read that PDF. Please check the file, or add photos instead.")
    if not pages:
        raise HTTPException(400, "That PDF has no pages.")
    return {"pages": pages, "total_pages": total, "truncated": total > len(pages)}
