"""Parse PhysicsAndMathsTutor-style question paper PDFs into structured questions."""
import re
import pdfplumber

# matches "(6)" or "(Total 15 marks)" mark annotations
MARK_TOTAL = re.compile(r"\(Total\s+(\d+)\s+marks?\)", re.IGNORECASE)
MARK_INLINE = re.compile(r"\((\d+)\)\s*$", re.MULTILINE)
QUESTION_SPLIT = re.compile(r"\n\s*Q\s*\.?\s*\d+\s*\.", re.IGNORECASE)


def clean_text(text: str) -> str:
    # remove the long answer-blank underscore lines
    text = re.sub(r"_{3,}", "", text)
    # remove site watermark
    text = re.sub(r"PhysicsAndMathsTutor\.com", "", text)
    # collapse blank lines / whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def extract_questions(pdf_path: str) -> list[dict]:
    """Return list of {'text': ..., 'marks': int} question blocks from a QP PDF."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            raw = "\n".join((p.extract_text() or "") for p in pdf.pages)
    except Exception as e:
        print(f"  ! failed to read {pdf_path}: {e}")
        return []

    text = clean_text(raw)
    if len(text) < 40:
        return []

    # split into question blocks on "Q1." "Q2." markers
    parts = QUESTION_SPLIT.split(text)
    # first part is usually header/preamble; keep parts that look substantial
    blocks = [p.strip() for p in parts if len(p.strip()) > 60]

    # if splitting failed (single block), treat whole doc as one
    if not blocks:
        blocks = [text]

    questions = []
    for b in blocks:
        total = MARK_TOTAL.search(b)
        if total:
            marks = int(total.group(1))
        else:
            inline = [int(m) for m in MARK_INLINE.findall(b)]
            marks = sum(inline) if inline else 4
        marks = max(1, min(marks, 30))
        # trim each block to a reasonable size
        body = b[:2500].strip()
        if len(body) > 50:
            questions.append({"text": body, "marks": marks})
    return questions
