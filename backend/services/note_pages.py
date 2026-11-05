"""Shows a note's file to students as watermarked page images (no raw PDF to save)."""
import fitz  # PyMuPDF

MAX_PAGES = 60


def _doc(data_uri: str) -> fitz.Document:
    import base64
    head, b64 = data_uri.split(",", 1)
    raw = base64.b64decode(b64)
    if "application/pdf" in head:
        return fitz.open(stream=raw, filetype="pdf")
    img = fitz.open(stream=raw, filetype=head.split("/")[1].split(";")[0] or "png")
    return fitz.open(stream=img.convert_to_pdf(), filetype="pdf")


_counts: dict[tuple[int, int], int] = {}


def page_count(note_id: int, data_uri: str) -> int:
    key = (note_id, len(data_uri))
    if key not in _counts:
        with _doc(data_uri) as d:
            _counts[key] = min(len(d), MAX_PAGES)
    return _counts[key]


def render_page(data_uri: str, n: int, mark: str) -> bytes:
    """Page n (1-based) as PNG with `mark` tiled faintly across it."""
    with _doc(data_uri) as d:
        if n < 1 or n > min(len(d), MAX_PAGES):
            raise IndexError(n)
        page = d[n - 1]
        r = page.rect
        size = max(9, r.width / 38)
        step_y, step_x = size * 7, size * 22
        y = size * 3
        row = 0
        while y < r.height + step_y:
            x = -step_x / 2 if row % 2 else 0
            while x < r.width:
                p = fitz.Point(x, y)
                page.insert_text(p, mark, fontsize=size, color=(0.45, 0.45, 0.5),
                                 fill_opacity=0.16, morph=(p, fitz.Matrix(-25)), overlay=True)
                x += step_x
            y += step_y
            row += 1
        zoom = min(2.0, 1600 / max(r.width, r.height) * 1.0) if max(r.width, r.height) > 0 else 2.0
        zoom = max(zoom, 1.4)
        return page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False).tobytes("png")
