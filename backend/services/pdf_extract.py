"""Extract plain text from an uploaded PDF for question generation."""
import io
import base64

# Guards so embedded figures don't bloat the questions JSON column.
_MAX_FIGURE_BYTES = 500_000      # skip a crop larger than ~500 KB
_FIGURE_ZOOM = 2.0               # render scale for crops (~144 DPI)
_FIGURE_PAD = 0.02               # expand the AI box by 2% each side


_IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff")


def is_image_upload(filename: str) -> bool:
    return (filename or "").lower().endswith(_IMAGE_EXTS)


def ensure_pdf(data: bytes, filename: str) -> bytes:
    """Return PDF bytes for `data`. If it's an image (screenshot/photo), wrap it in a
    single-page PDF so the rest of the pipeline (render_pages_to_png, crop_figures,
    extract_text) works unchanged. PDFs pass through untouched."""
    if not is_image_upload(filename):
        return data
    import fitz  # PyMuPDF
    with fitz.open(stream=data, filetype="image") as img:
        return img.convert_to_pdf()


_MAX_UPLOAD_FILES = 10
_MAX_UPLOAD_BYTES = 15 * 1024 * 1024
_MAX_UPLOAD_TOTAL = 40 * 1024 * 1024


async def read_uploads(files) -> bytes:
    """Validate a list of UploadFiles (PDFs/images), read them, and merge into one PDF.
    Raises HTTP 400 on bad type/size. Shared by the teacher and practice upload routes."""
    from fastapi import HTTPException
    if not files:
        raise HTTPException(400, "Please upload at least one PDF or image.")
    if len(files) > _MAX_UPLOAD_FILES:
        raise HTTPException(400, f"Please upload at most {_MAX_UPLOAD_FILES} files.")
    items: list[tuple[bytes, str]] = []
    total = 0
    for f in files:
        name = f.filename or ""
        if not (name.lower().endswith(".pdf") or is_image_upload(name)):
            raise HTTPException(400, "Each file must be a PDF or an image (PNG/JPG).")
        b = await f.read()
        total += len(b)
        if len(b) > _MAX_UPLOAD_BYTES:
            raise HTTPException(400, "One of your files is too large (max 15 MB each).")
        if total > _MAX_UPLOAD_TOTAL:
            raise HTTPException(400, "Your files are too large in total. Please upload fewer or smaller files.")
        items.append((b, name))
    return combine_to_pdf(items)


def combine_to_pdf(items: list[tuple[bytes, str]]) -> bytes:
    """Merge several uploaded files (screenshots/photos and/or PDFs) into one PDF, in
    order — each image becomes a page. Lets a question spread across multiple images be
    read as a single document by the extract/crop pipeline."""
    if not items:
        raise ValueError("no files to combine")
    if len(items) == 1:
        return ensure_pdf(items[0][0], items[0][1])
    import fitz  # PyMuPDF
    out = fitz.open()
    try:
        for data, name in items:
            src = fitz.open(stream=ensure_pdf(data, name), filetype="pdf")
            try:
                out.insert_pdf(src)
            finally:
                src.close()
        return out.tobytes()
    finally:
        out.close()


def extract_text(data: bytes) -> str:
    """Best-effort text extraction. Tries pdfplumber, falls back to pypdf."""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages[:30]]
        text = "\n\n".join(pages).strip()
    except Exception:
        text = ""

    if len(text) < 40:  # scanned/empty — try pypdf as a fallback
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            text = "\n\n".join((pg.extract_text() or "") for pg in reader.pages[:30]).strip()
        except Exception:
            pass

    return text


def render_pages_to_png(data: bytes, max_pages: int = 8, zoom: float = 2.0) -> list[bytes]:
    """Render the first `max_pages` PDF pages to PNG image bytes (for vision models).
    zoom=2.0 ~= 144 DPI, enough for legible text/equations."""
    import fitz  # PyMuPDF
    images: list[bytes] = []
    with fitz.open(stream=data, filetype="pdf") as doc:
        for page in doc[:max_pages]:
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            images.append(pix.tobytes("png"))
    return images


def _clamp(v: float) -> float:
    return max(0.0, min(1.0, v))


def crop_figures(data: bytes, questions: list[dict], max_pages: int = 8) -> list[dict]:
    """For each question carrying a `figure` = {page, box:[x0,y0,x1,y1]} (fractions of
    the page, top-left origin) returned by the vision model, crop that region out of the
    PDF page and embed it as a base64 PNG data URI in `question["image"]`. The transient
    `figure` key is removed. Questions without a figure are left untouched.

    Cropping straight from the source PDF (not the downscaled page PNG) keeps figures crisp.
    """
    if not any(q.get("figure") for q in questions):
        return questions
    import fitz  # PyMuPDF
    try:
        with fitz.open(stream=data, filetype="pdf") as doc:
            n_pages = min(len(doc), max_pages)
            for q in questions:
                fig = q.pop("figure", None)
                if not fig:
                    continue
                try:
                    page_idx = int(fig.get("page", 0))
                    box = fig.get("box") or []
                    if page_idx < 0 or page_idx >= n_pages or len(box) != 4:
                        continue
                    x0, y0, x1, y1 = (_clamp(float(v)) for v in box)
                    if x1 <= x0 or y1 <= y0:
                        continue  # non-positive area — nothing to crop
                    # pad slightly so tight AI boxes don't clip labels/axes
                    x0, y0 = _clamp(x0 - _FIGURE_PAD), _clamp(y0 - _FIGURE_PAD)
                    x1, y1 = _clamp(x1 + _FIGURE_PAD), _clamp(y1 + _FIGURE_PAD)
                    if x1 - x0 < 0.02 or y1 - y0 < 0.02:
                        continue  # degenerate box
                    page = doc[page_idx]
                    r = page.rect
                    clip = fitz.Rect(x0 * r.width, y0 * r.height, x1 * r.width, y1 * r.height)
                    pix = page.get_pixmap(matrix=fitz.Matrix(_FIGURE_ZOOM, _FIGURE_ZOOM), clip=clip)
                    png = pix.tobytes("png")
                    if len(png) > _MAX_FIGURE_BYTES:
                        continue  # too heavy to embed inline
                    q["image"] = "data:image/png;base64," + base64.b64encode(png).decode()
                except Exception:
                    continue
    except Exception:
        # if the PDF can't be reopened, just return questions without images
        for q in questions:
            q.pop("figure", None)
    return questions
