#!/usr/bin/env python3
"""Generates logo, favicons and the default social-share image from the brand config.
Needs Pillow, fontTools and brotli:  pip install pillow fonttools brotli
Run after changing the business name or colours:  python3 _build/make_images.py"""
import json, os, io, math
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "site.config.json")))
IMG = os.path.join(ROOT, "assets", "img")
os.makedirs(IMG, exist_ok=True)
ACCENT_HEX = (CFG.get("accent") or "#3cb4ff").strip()
HEAT_HEX = (CFG.get("heat") or "#ff6a2b").strip()
BG, TEXT, MUTED = (8, 10, 14), (238, 242, 246), (150, 162, 176)
hexrgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
ACCENT, HEAT = hexrgb(ACCENT_HEX), hexrgb(HEAT_HEX)
LOGO_FILE = (CFG.get("logo") or "").strip()

def font(name, size):
    f = TTFont(os.path.join(ROOT, "assets", "fonts", name))
    f.flavor = None
    buf = io.BytesIO(); f.save(buf); buf.seek(0)
    return ImageFont.truetype(buf, size)

def mark(draw, x, y, s, w):
    """HVAC mark: a comfort dial, cool arc on the left, heat arc on the right, with a needle."""
    cx, cy, r = x + s / 2, y + s / 2, s / 2 - w / 2
    box = [cx - r, cy - r, cx + r, cy + r]
    draw.arc(box, 135, 270, fill=ACCENT, width=w)
    draw.arc(box, 270, 405, fill=HEAT, width=w)
    a = math.radians(-45)
    draw.line([(cx, cy), (cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a))], fill=TEXT, width=w)
    d = w * 0.9
    draw.ellipse([cx - d, cy - d, cx + d, cy + d], fill=TEXT)

name = CFG["business_name"]
first, rest = name.split(" ")[0].upper(), " ".join(name.split(" ")[1:]).upper()

# favicon.svg
open(os.path.join(IMG, "favicon.svg"), "w").write(
 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="7" fill="#080a0e"/>'
 '<g fill="none" stroke-width="3.6" stroke-linecap="round"><path d="M10 30A14 14 0 0 1 20 6" stroke="' + ACCENT_HEX + '"/>'
 '<path d="M20 6a14 14 0 0 1 10 24" stroke="' + HEAT_HEX + '"/><path d="M20 20l6-6" stroke="#eef2f6"/></g>'
 '<circle cx="20" cy="20" r="2.8" fill="#eef2f6"/></svg>')

for size, fname in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")]:
    S = size * 4
    im = Image.new("RGB", (S, S), BG); d = ImageDraw.Draw(im)
    pad = S * 0.14
    mark(d, pad, pad, S - 2 * pad, max(2, int(S * 0.085)))
    im.resize((size, size), Image.LANCZOS).save(os.path.join(IMG, fname))

# logo.png (for schema): the client's logo when supplied, otherwise mark + wordmark on dark
W, H = 1200, 300
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
mark(d, 40, 40, 220, 18)
d.text((300, 52), first, font=font("anton-latin-400-normal.woff2", 140), fill=TEXT)
d.text((306, 218), rest or CFG["short_tagline"].upper(), font=font("barlow-condensed-latin-600-normal.woff2", 44), fill=MUTED)
bbox = d.textbbox((300, 52), first, font=font("anton-latin-400-normal.woff2", 140))
sub = d.textbbox((306, 218), rest or CFG["short_tagline"].upper(), font=font("barlow-condensed-latin-600-normal.woff2", 44))
im = im.crop((0, 0, min(W, max(bbox[2], sub[2], 700) + 50), H))
if LOGO_FILE:
    src = Image.open(os.path.join(ROOT, LOGO_FILE.lstrip("/"))).convert("RGBA")
    src = src.crop(src.getchannel("A").getbbox() or (0, 0, src.width, src.height))
    if src.width > 1200:
        src = src.resize((1200, round(src.height * 1200 / src.width)), Image.LANCZOS)
    im = src
im.save(os.path.join(IMG, "logo.png"))

# og-default.png 1200x630: split cool/heat field with the headline
W, H = 1200, 630
im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
glow = Image.new("RGB", (W, H), BG); g = ImageDraw.Draw(glow)
for i in range(60):
    t = i / 60
    g.ellipse([820 - 420 * (1 - t), 120 - 300 * (1 - t), 1320 + 300 * (1 - t), 760], fill=tuple(int(BG[k] + (HEAT[k] - BG[k]) * 0.18 * t) for k in range(3)))
    g.ellipse([-320, -260 + 200 * t, 520 - 300 * t, 420 + 120 * (1 - t)], fill=tuple(int(BG[k] + (ACCENT[k] - BG[k]) * 0.14 * t) for k in range(3)))
im = Image.blend(im, glow, 1.0); d = ImageDraw.Draw(im)
for y in range(0, H, 6):
    d.line([(0, y), (W, y)], fill=(12, 15, 20))
for k in range(9):   # airflow streamlines
    pts = [(x, 470 + k * 14 + 18 * math.sin(x / 120 + k * 0.7)) for x in range(0, W + 20, 20)]
    for i in range(len(pts) - 1):
        t = i / len(pts)
        col = tuple(int(ACCENT[j] + (HEAT[j] - ACCENT[j]) * t) for j in range(3))
        col = tuple(int(BG[j] + (col[j] - BG[j]) * 0.45) for j in range(3))
        d.line([pts[i], pts[i + 1]], fill=col, width=2)
d.rectangle([0, H - 12, W // 2, H], fill=ACCENT); d.rectangle([W // 2, H - 12, W, H], fill=HEAT)
mark(d, 70, 60, 90, 9)
d.text((182, 70), first, font=font("anton-latin-400-normal.woff2", 64), fill=TEXT)
big = font("anton-latin-400-normal.woff2", 120)
d.text((70, 200), "BUILT FOR", font=big, fill=TEXT)
w1 = d.textlength("BUILT FOR ", font=big)
T = dict({"cold": -20, "hot": 35}, **(CFG.get("temps") or {}))
fmt = lambda n: ("+" if n > 0 else "") + str(n) + "°."
d.text((70 + w1, 200), fmt(T["cold"]), font=big, fill=ACCENT)
d.text((70, 330), "READY FOR", font=big, fill=TEXT)
w2 = d.textlength("READY FOR ", font=big)
d.text((70 + w2, 330), fmt(T["hot"]), font=big, fill=HEAT)
d.text((74, 540), f"HEATING & COOLING  ·  INSTANT SYSTEM ESTIMATE  ·  {CFG['region_label'].upper()}", font=font("barlow-condensed-latin-600-normal.woff2", 32), fill=MUTED)
im.save(os.path.join(IMG, "og-default.png"), optimize=True)
print("Images written to assets/img/")
