"""Student work as one A4 PDF for marking on paper or on screen.

build():         a worksheet hand-in (HomeworkSubmission photos). Cover page with a mark box,
                 then one photo per page, fitted inside a white border so nothing is cropped.
build_attempt(): a written test attempt (Marking page). Cover with a marks table, then each
                 question with the student's typed answer and answer photos, then the mark scheme.
Every page carries a Notenix header and footer.
"""
import base64
import io
from datetime import datetime
from html import escape

import fitz
from PIL import Image, ImageOps

A4 = fitz.paper_rect("a4")          # 595 x 842 pt
MARGIN = 36                         # white border around each photo (0.5 inch)
HEADER_H, FOOTER_H = 58, 46
INDIGO = (79 / 255, 70 / 255, 229 / 255)
INK = (30 / 255, 27 / 255, 75 / 255)
MUTED = (100 / 255, 116 / 255, 139 / 255)
LINE = (226 / 255, 232 / 255, 240 / 255)

FOOTER_TEXT = ("Notenix: timed tests, homework help and tutor marking, with a progress report for parents "
               "· notenix.com · with Beyond Tutors")

_LOGO_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
<rect width="64" height="64" rx="15" fill="#4F46E5"/>
<path transform="translate(12 12.3) scale(.4 .38)" d="M0 100V8H27L63 64V40L84 4H100L86 34V100H60L23 44V100Z" fill="#fff"/></svg>"""
_logo_png: bytes | None = None


def _logo() -> bytes:
    global _logo_png
    if _logo_png is None:
        svg = fitz.open(stream=_LOGO_SVG, filetype="svg")
        _logo_png = svg[0].get_pixmap(dpi=300).tobytes("png")
        svg.close()
    return _logo_png


def _photo_jpeg(data_uri: str) -> tuple[bytes, int, int] | None:
    """Decode a data: URI photo, turn it upright, shrink to a sensible size and re-encode."""
    try:
        raw = base64.b64decode(data_uri.split(",", 1)[1])
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
    except Exception:
        return None
    im.thumbnail((2000, 2000))
    out = io.BytesIO()
    im.save(out, "JPEG", quality=82, optimize=True)
    return out.getvalue(), im.width, im.height


def _html(page: fitz.Page, rect: fitz.Rect, html: str, css: str = "") -> None:
    page.insert_htmlbox(rect, html, css="* {font-family: sans-serif; color: #1E1B4B;} " + css)


def _frame(page: fitz.Page, student: str, title: str, n: int, total: int) -> None:
    """Notenix header and footer on every page."""
    w, h = page.rect.width, page.rect.height
    page.insert_image(fitz.Rect(MARGIN, 16, MARGIN + 26, 42), stream=_logo())
    _html(page, fitz.Rect(MARGIN + 34, 15, w / 2 + 40, 45),
          '<b style="font-size:15px">Notenix</b><br><span style="font-size:8px;color:#64748B">'
          "Practice · tests · tutor marking · notenix.com</span>")
    _html(page, fitz.Rect(w / 2 - 40, 15, w - MARGIN, 45),
          f'<div style="text-align:right;font-size:9px"><b>{escape(student)}</b><br>'
          f'<span style="color:#64748B">{escape(title)} · page {n} of {total}</span></div>')
    page.draw_line((MARGIN, HEADER_H - 8), (w - MARGIN, HEADER_H - 8), color=LINE, width=0.8)
    page.draw_line((MARGIN, h - FOOTER_H + 6), (w - MARGIN, h - FOOTER_H + 6), color=LINE, width=0.8)
    _html(page, fitz.Rect(MARGIN, h - FOOTER_H + 12, w - MARGIN, h - 8),
          f'<div style="text-align:center;font-size:7.5px;color:#64748B">{escape(FOOTER_TEXT)}</div>')


def _fmt(d: datetime | None) -> str:
    return d.strftime("%d %b %Y, %H:%M UTC") if d else "-"


def build(*, student: str, login: str, title: str, images: list[str], comment: str | None,
          submitted_at: datetime | None, due_at: datetime | None, mark: str | None = None,
          feedback: str | None = None) -> bytes:
    photos = [p for p in (_photo_jpeg(i) for i in images or []) if p]
    total = 1 + len(photos)
    doc = fitz.open()

    # ── Cover page ──────────────────────────────────────────────────────────────
    page = doc.new_page(width=A4.width, height=A4.height)
    _frame(page, student, title, 1, total)
    late = bool(due_at and submitted_at and submitted_at > due_at)
    rows = [("Student", f"{student} ({login})"), ("Homework", title), ("Handed in", _fmt(submitted_at) + (" · LATE" if late else "")),
            ("Due", _fmt(due_at) if due_at else "No due date"), ("Pages", f"{len(photos)} photo{'s' if len(photos) != 1 else ''}")]
    table = "".join(f'<tr><td style="color:#64748B;padding:5px 14px 5px 0;width:90px">{k}</td>'
                    f'<td style="padding:5px 0"><b>{escape(v)}</b></td></tr>' for k, v in rows)
    comment_html = (f'<p style="margin-top:14px;color:#64748B;font-size:10px">Student\'s note</p>'
                    f'<p style="background:#F1F5F9;padding:10px;font-size:11px">&ldquo;{escape(comment)}&rdquo;</p>'
                    if comment else "")
    _html(page, fitz.Rect(MARGIN, HEADER_H + 30, A4.width - MARGIN, 520),
          f'<p style="font-size:10px;color:#4F46E5;letter-spacing:1px"><b>HOMEWORK FOR MARKING</b></p>'
          f'<p style="font-size:22px;margin:4px 0 16px"><b>{escape(title)}</b></p>'
          f'<table style="font-size:11px">{table}</table>{comment_html}')
    # Mark and feedback box, filled in if it has already been marked.
    box = fitz.Rect(MARGIN, 540, A4.width - MARGIN, A4.height - FOOTER_H - 24)
    page.draw_rect(box, color=INDIGO, width=1.2)
    _html(page, fitz.Rect(box.x0 + 14, box.y0 + 10, box.x1 - 14, box.y0 + 40),
          f'<b style="font-size:12px">Mark:</b> <span style="font-size:12px">{escape(mark) if mark else "________ / ________"}</span>')
    _html(page, fitz.Rect(box.x0 + 14, box.y0 + 42, box.x1 - 14, box.y0 + 60), '<b style="font-size:12px">Feedback:</b>')
    if feedback:
        _html(page, fitz.Rect(box.x0 + 14, box.y0 + 62, box.x1 - 14, box.y1 - 10),
              f'<p style="font-size:11px">{escape(feedback)}</p>')
    else:
        for y in range(int(box.y0) + 84, int(box.y1) - 8, 24):
            page.draw_line((box.x0 + 14, y), (box.x1 - 14, y), color=LINE, width=0.7)

    # ── One photo per page, inside a white border ──────────────────────────────
    area = fitz.Rect(MARGIN, HEADER_H + 6, A4.width - MARGIN, A4.height - FOOTER_H - 6)
    for i, (jpg, w, h) in enumerate(photos, start=2):
        landscape = w > h * 1.15   # wide photos get a landscape page so they stay large
        pw, ph = (A4.height, A4.width) if landscape else (A4.width, A4.height)
        page = doc.new_page(width=pw, height=ph)
        _frame(page, student, title, i, total)
        box = fitz.Rect(MARGIN, HEADER_H + 6, pw - MARGIN, ph - FOOTER_H - 6) if landscape else area
        page.insert_image(box, stream=jpg, keep_proportion=True)   # scaled to fit, never cropped
        # thin outline round the photo itself
        s = min(box.width / w, box.height / h)
        iw, ih = w * s, h * s
        x0, y0 = box.x0 + (box.width - iw) / 2, box.y0 + (box.height - ih) / 2
        page.draw_rect(fitz.Rect(x0, y0, x0 + iw, y0 + ih), color=LINE, width=0.6)

    doc.set_metadata({"title": f"{title} - {student}", "author": "Notenix", "creator": "Notenix · notenix.com"})
    data = doc.tobytes(garbage=3, deflate=True)
    doc.close()
    return data


def filename(student: str, title: str) -> str:
    safe = "".join(c for c in f"{student} - {title}" if c.isalnum() or c in " -_.()")[:120].strip()
    return (safe or "homework") + ".pdf"


# ── Written test attempts (Marking page) ───────────────────────────────────────

CONTENT = fitz.Rect(MARGIN, HEADER_H + 10, A4.width - MARGIN, A4.height - FOOTER_H - 10)
_CSS = ("* {font-family: sans-serif; color: #1E1B4B;} body {font-size: 10.5pt;} "
        "h1 {font-size: 18pt; margin: 2pt 0 10pt;} h2 {font-size: 13pt; margin: 0 0 6pt; color: #4F46E5;} "
        ".kicker {font-size: 8.5pt; color: #4F46E5; font-weight: bold; letter-spacing: 1px;} "
        ".muted {color: #64748B;} .q {margin: 0 0 8pt;} "
        ".ans {background-color: #F1F5F9; padding: 8pt; margin: 4pt 0 8pt;} "
        ".ms {background-color: #EEF2FF; padding: 8pt; margin: 4pt 0 10pt;} "
        ".box {border: 1px solid #4F46E5; padding: 8pt; margin-top: 8pt;} "
        "table {border-collapse: collapse; width: 100%;} td, th {border: 1px solid #E2E8F0; padding: 4pt 6pt; text-align: left;} "
        "th {background-color: #F8FAFC;}")


def _text(t) -> str:
    """Plain text to HTML, keeping line breaks."""
    return escape(str(t or "")).replace("\n", "<br>")


def _story_pages(doc: fitz.Document, html: str, archive: fitz.Archive | None = None) -> None:
    """Flow `html` over as many A4 pages as it needs (inside the header/footer area) and add them."""
    buf = io.BytesIO()
    writer = fitz.DocumentWriter(buf)
    story = fitz.Story(html=html, user_css=_CSS, archive=archive)
    more = 1
    while more:
        dev = writer.begin_page(A4)
        more, _ = story.place(CONTENT)
        story.draw(dev)
        writer.end_page()
    writer.close()
    src = fitz.open("pdf", buf.getvalue())
    doc.insert_pdf(src)
    src.close()


def _photo_page(doc: fitz.Document, jpg: bytes, w: int, h: int, caption: str = "") -> None:
    """One photo on its own page, scaled to fit inside the white border (never cropped)."""
    landscape = w > h * 1.15
    pw, ph = (A4.height, A4.width) if landscape else (A4.width, A4.height)
    page = doc.new_page(width=pw, height=ph)
    top = HEADER_H + 6 + (18 if caption else 0)
    if caption:
        _html(page, fitz.Rect(MARGIN, HEADER_H + 2, pw - MARGIN, HEADER_H + 22),
              f'<b style="font-size:10px">{escape(caption)}</b>')
    box = fitz.Rect(MARGIN, top, pw - MARGIN, ph - FOOTER_H - 6)
    page.insert_image(box, stream=jpg, keep_proportion=True)
    s = min(box.width / w, box.height / h)
    iw, ih = w * s, h * s
    x0, y0 = box.x0 + (box.width - iw) / 2, box.y0 + (box.height - ih) / 2
    page.draw_rect(fitz.Rect(x0, y0, x0 + iw, y0 + ih), color=LINE, width=0.6)


def _finish(doc: fitz.Document, student: str, title: str) -> bytes:
    """Notenix header and footer (with page X of N) on every page, then the PDF bytes."""
    total = doc.page_count
    for i, page in enumerate(doc, start=1):
        _frame(page, student, title, i, total)
    doc.set_metadata({"title": f"{title} - {student}", "author": "Notenix", "creator": "Notenix · notenix.com"})
    data = doc.tobytes(garbage=3, deflate=True)
    doc.close()
    return data


def _dur(sec) -> str:
    if sec is None:
        return "-"
    m, s = divmod(int(sec), 60)
    return f"{m} min {s:02d} s" if m else f"{s} s"


def _plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def build_attempt(*, student: str, title: str, subject: str | None, level: str | None,
                  submitted_at: datetime | None, time_taken: int | None, questions: list[dict]) -> bytes:
    """questions: [{question, marks, mark_scheme, image, your_answer, answer_images, time_seconds}]."""
    doc = fitz.open()
    total = sum(int(q.get("marks") or 0) for q in questions)
    photos_total = sum(len(q.get("answer_images") or []) for q in questions)

    # Cover: details and a marks table to fill in.
    rows = "".join(
        f"<tr><td>Question {i}</td><td>{int(q.get('marks') or 0)}</td><td></td><td>{_dur(q.get('time_seconds'))}</td></tr>"
        for i, q in enumerate(questions, start=1))
    info = [("Student", student), ("Test", title), ("Subject", " · ".join(x for x in (subject, level) if x) or "-"),
            ("Submitted", _fmt(submitted_at)), ("Time taken", _dur(time_taken)),
            ("Answer photos", str(photos_total))]
    info_html = "".join(f'<tr><td class="muted" style="border:none;width:110px">{k}</td>'
                        f'<td style="border:none"><b>{escape(v)}</b></td></tr>' for k, v in info)
    _story_pages(doc,
                 f'<p class="kicker">WRITTEN ANSWERS FOR MARKING</p><h1>{escape(title)}</h1>'
                 f'<table>{info_html}</table><br>'
                 f'<table><tr><th>Question</th><th>Out of</th><th>Mark</th><th>Time spent</th></tr>{rows}'
                 f'<tr><td><b>Total</b></td><td><b>{total}</b></td><td></td><td></td></tr></table>'
                 f'<div class="box"><b>Overall feedback:</b><br><br><br><br><br></div>')

    # Each question: text, the student's typed answer, then each answer photo on its own page.
    for i, q in enumerate(questions, start=1):
        marks = int(q.get("marks") or 0)
        arch = fitz.Archive()
        img_html = ""
        qimg = _photo_jpeg(q["image"]) if str(q.get("image") or "").startswith("data:image/") else None
        if qimg:
            arch.add(qimg[0], f"q{i}.jpg")
            img_html = f'<p><img src="q{i}.jpg" width="{min(520, qimg[1])}"/></p>'
        imgs = [p for p in (_photo_jpeg(x) for x in (q.get("answer_images") or [])
                            if str(x).startswith("data:image/")) if p]
        if (q.get("your_answer") or "").strip():
            answer = _text(q.get("your_answer"))
            if imgs:
                answer += f"<br><i>(+ {_plural(len(imgs), 'photo')} on the next page{'s' if len(imgs) > 1 else ''})</i>"
        elif imgs:
            answer = f"(answer in the {_plural(len(imgs), 'photo')} on the next page{'s' if len(imgs) > 1 else ''})"
        else:
            answer = "(not answered)"
        _story_pages(doc, archive=arch, html=(
            f'<h2>Question {i} <span class="muted" style="font-size:10pt">· {_plural(marks, "mark")}'
            f' · time {_dur(q.get("time_seconds"))}</span></h2>'
            f'<p class="q">{_text(q.get("question"))}</p>{img_html}'
            f'<p class="muted" style="font-size:9pt;margin-bottom:0"><b>STUDENT ANSWER</b></p>'
            f'<div class="ans">{answer}</div>'
            f'<div class="box"><b>Mark:</b> ______ / {marks} &nbsp;&nbsp; <b>Feedback:</b><br><br><br></div>'))
        for j, (jpg, w, h) in enumerate(imgs, start=1):
            _photo_page(doc, jpg, w, h, caption=f"Question {i}: answer photo {j} of {len(imgs)}")

    # Mark scheme at the end, so the answer pages stay clean.
    schemes = [(i, q.get("mark_scheme")) for i, q in enumerate(questions, start=1)
               if (q.get("mark_scheme") or "").strip()]
    if schemes:
        _story_pages(doc, '<p class="kicker">FOR THE MARKER</p><h1>Mark scheme</h1>' + "".join(
            f'<h2>Question {i}</h2><div class="ms">{_text(ms)}</div>' for i, ms in schemes))

    return _finish(doc, student, title)
