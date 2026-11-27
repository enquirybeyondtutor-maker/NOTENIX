"""A worksheet hand-in (HomeworkSubmission photos) as one A4 PDF for marking on paper or on screen.

Page 1 is a cover: student, homework, dates, the student's comment and a mark/feedback box.
Then one photo per page, fitted inside a white border so nothing is cropped when printed.
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
