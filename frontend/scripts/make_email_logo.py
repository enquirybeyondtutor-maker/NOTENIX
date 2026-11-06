"""Builds public/brand/notenix-email-logo.png: the Marked N tile + "Notenix" wordmark, at 3x for sharp
display at 160x40 in emails (most email apps can't show SVG). Same shape as components/ui/Logo.tsx."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

S = 3                      # scale (shown at 1/3 size in the email)
VIOLET, INK = (84, 68, 220), (21, 24, 41)
MARK = [(0, 100), (0, 8), (27, 8), (63, 64), (63, 40), (84, 4), (100, 4), (86, 34), (86, 100), (60, 100), (23, 44), (23, 100)]

W, H = 160 * S, 40 * S
img = Image.new("RGBA", (W, H), (255, 255, 255, 0))
d = ImageDraw.Draw(img)
tile = 40 * S
d.rounded_rectangle((0, 0, tile - 1, tile - 1), radius=10 * S, fill=VIOLET)
# Mark: viewBox x 0..100, y 4..100, drawn about 22 x 21 px inside the 40 px tile
mw, mh = 22 * S, 21 * S
ox, oy = (tile - mw) / 2, (tile - mh) / 2
d.polygon([(ox + x / 100 * mw, oy + (y - 4) / 96 * mh) for x, y in MARK], fill=(255, 255, 255))
font = None
for name in ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
    try:
        font = ImageFont.truetype(name, 22 * S)
        break
    except OSError:
        pass
d.text((tile + 10 * S, tile / 2), "Notenix", font=font, fill=INK, anchor="lm")
bbox = img.getbbox()
img = img.crop((0, 0, bbox[2] + 2 * S, H))
out = Path(__file__).resolve().parent.parent / "public" / "brand" / "notenix-email-logo.png"
img.save(out, optimize=True)
print(out, img.size, "-> show at", (img.size[0] // S, img.size[1] // S))
