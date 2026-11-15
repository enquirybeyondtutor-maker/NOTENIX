"""Shows a note's file to students as watermarked page images (no raw PDF to save).

Pages are rendered ONCE per note to plain JPEGs (stored in note_pages); each request
then only lays a cached name overlay on one image, which takes ~50 ms.
"""
import base64
import io
from functools import lru_cache
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont

MAX_PAGES = 80
PAGE_WIDTH_PX = 1300


def _doc(data_uri: str) -> fitz.Document:
    head, b64 = data_uri.split(",", 1)
    raw = base64.b64decode(b64)
    if "application/pdf" in head:
        return fitz.open(stream=raw, filetype="pdf")
    img = fitz.open(stream=raw, filetype=head.split("/")[1].split(";")[0] or "png")
    return fitz.open(stream=img.convert_to_pdf(), filetype="pdf")


def _jpeg(im: Image.Image, quality: int) -> bytes:
    b = io.BytesIO()
    im.save(b, "JPEG", quality=quality, optimize=False)
    return b.getvalue()


def render_all(data_uri: str) -> list[bytes]:
    """Every page as a plain JPEG about PAGE_WIDTH_PX wide."""
    out = []
    with _doc(data_uri) as d:
        for page in d.pages(0, min(len(d), MAX_PAGES)):
            zoom = min(3.0, PAGE_WIDTH_PX / max(page.rect.width, 1))
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
            out.append(_jpeg(Image.frombytes("RGB", (pix.width, pix.height), pix.samples), 82))
    return out


def _font(size: int):
    for name in ("DejaVuSans.ttf", "arial.ttf", "LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size)


@lru_cache(maxsize=64)
def _overlay(mark: str, w: int, h: int) -> Image.Image:
    """Faint diagonal tiles of `mark`, sized for a w×h page (cached per viewer + size)."""
    size = max(16, w // 40)
    font = _font(size)
    step_x = int(font.getlength(mark)) + size * 6
    step_y = size * 7
    big = Image.new("RGBA", (int(w * 1.5), int(h * 1.5)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(big)
    for row, y in enumerate(range(0, big.height, step_y)):
        for x in range(-(step_x // 2) * (row % 2), big.width, step_x):
            draw.text((x, y), mark, font=font, fill=(110, 110, 125, 46))
    big = big.rotate(25, resample=Image.BICUBIC)
    left, top = (big.width - w) // 2, (big.height - h) // 2
    return big.crop((left, top, left + w, top + h))


def watermark(jpeg: bytes, mark: str) -> bytes:
    """Stored page image + the viewer's name tiled faintly across it, as JPEG."""
    im = Image.open(io.BytesIO(jpeg)).convert("RGBA")
    im.alpha_composite(_overlay(mark, *im.size))
    return _jpeg(im.convert("RGB"), 80)


def print_pdf(pages: list[bytes], mark: str, footer: str) -> bytes:
    """A print copy: every stored page with `mark` tiled across it (darker than on screen, so
    it survives printing and photocopying) and a `footer` line, burned into the image and
    assembled as an A4 PDF. Nothing in the PDF is a separate layer that could be removed."""
    out = fitz.open()
    font = _font(22)
    for jpeg in pages:
        im = Image.open(io.BytesIO(jpeg)).convert("RGBA")
        tiles = _overlay(mark, *im.size)
        im.alpha_composite(_darker(tiles))
        draw = ImageDraw.Draw(im)
        h = 34
        draw.rectangle((0, im.height - h, im.width, im.height), fill=(255, 255, 255, 235))
        draw.text((14, im.height - h + 6), footer, font=font, fill=(60, 60, 75, 255))
        b = io.BytesIO()
        im.convert("RGB").save(b, "JPEG", quality=85)
        page = out.new_page(width=595, height=842)  # A4 in points
        r = page.rect
        scale = min(r.width / im.width, r.height / im.height)
        w, hh = im.width * scale, im.height * scale
        x, y = (r.width - w) / 2, (r.height - hh) / 2
        page.insert_image(fitz.Rect(x, y, x + w, y + hh), stream=b.getvalue())
    data = out.tobytes(garbage=3, deflate=True)
    out.close()
    return data


def _darker(tiles: Image.Image) -> Image.Image:
    """The on-screen overlay is very faint; print needs it a little stronger."""
    r, g, b, a = tiles.split()
    return Image.merge("RGBA", (r, g, b, a.point(lambda v: min(255, int(v * 1.6)))))
