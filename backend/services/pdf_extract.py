"""Extract plain text from an uploaded PDF for question generation."""
import io


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
