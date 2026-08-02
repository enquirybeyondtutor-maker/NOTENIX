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
