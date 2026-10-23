#!/usr/bin/env python3
"""
HVAC Website Template — static site generator.

Usage:  python3 _build/build.py
Reads:  _build/site.config.json, _build/content_*.py, _build/pages.py
Writes: the published site into the repository root (HTML pages, sitemap.xml, robots.txt, 404.html).

Per-client settings in site.config.json control the services offered ("services"), the brand colours
("accent", "heat"), the logo ("logo"), the client's own work photos ("photos"; see _build/photos.py), the
opening animation ("intro", "intro_scope"), the animated hero airflow ("hero_fx"), the no-heat band wording
("emergency_24_7") and the instant system estimate's pricing ("estimator").

Shared components (header, footer, CTA, schema, metadata) live in this file, so a change here updates
every page on the next build. Folders starting with "_" are never published.
"""
import json, os, re, html, posixpath, sys, math
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content_services import SERVICES as ALL_SERVICES
from content_cities import CITIES
from content_costs import COSTS, ASK
import pages as P
import photos as PH

CFG = json.load(open(os.path.join(HERE, "site.config.json"), encoding="utf-8"))
ALL_SVC = {s["slug"]: s for s in ALL_SERVICES}
# ---- services the client offers (config "services"; empty = all). Removing a slug drops its pages, menu and footer
# links, related-service links, sitemap entries and form options. Links to it inside other services' text become
# plain text and are listed in _build/removed-service-mentions.txt so those sentences can be reworded.
_wanted = CFG.get("services") or [s["slug"] for s in ALL_SERVICES]
_unknown = [x for x in _wanted if x not in ALL_SVC]
if _unknown:
    sys.exit(f"site.config.json: unknown service slug(s) {_unknown}. Valid: {[s['slug'] for s in ALL_SERVICES]}")
SERVICES = [s for s in ALL_SERVICES if s["slug"] in _wanted]
if not SERVICES:
    sys.exit("site.config.json: services is empty. List at least one service slug.")
SVC = {s["slug"]: s for s in SERVICES}
ALL_OFFERED = len(SERVICES) == len(ALL_SERVICES)
REMOVED_MENTIONS = {}
CITY = {c["slug"]: c for c in CITIES}
CATS = [
    ("heating", "Heating", "Furnaces, heat pumps and boilers, sized to the house and installed by licensed technicians."),
    ("cooling", "Cooling", "Central air, repairs and ductless systems that pull out the heat and the humidity."),
    ("air", "Air Quality & Ductwork", "Filtration, humidity, ventilation and the ducts that decide where the air actually goes."),
    ("care", "Maintenance & More", "Tune-ups, water heaters, thermostats and light commercial equipment."),
]
CATS = [c for c in CATS if any(s["cat"] == c[0] for s in SERVICES)]

EST = dict(CFG.get("estimator") or {})
EST_ON = bool(EST.get("enabled", True))
if EST_ON:
    EST["systems"] = [x for x in EST.get("systems", []) if x.get("service") in SVC or not x.get("service")]
    if not EST["systems"]:
        EST_ON = False
INTRO_ON = bool(CFG.get("intro", True))
INTRO_SCOPE = CFG.get("intro_scope", "all")
FX_ON = bool(CFG.get("hero_fx", True))
H24 = bool(CFG.get("emergency_24_7", False))
LOCALE = CFG.get("locale", "en-CA")                    # html lang, e.g. en-US / en-CA
OG_LOCALE = LOCALE.replace("-", "_")
T = dict({"unit": "C", "cold": -20, "hot": 35, "set": 21, "from": 5}, **(CFG.get("temps") or {}))
def deg(n, sign=True):
    return ("+" if sign and n > 0 else "") + str(n) + "°"

def and_join(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]

def related_of(s):
    return [r for r in s["related"] if r in SVC]

# ---- brand colours (config "accent" + "heat", #rrggbb). Derived shades keep every text/background pair at WCAG AA.
def _rgb(h):
    h = h.lstrip("#"); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
def _lum(h):
    v = [x / 255 for x in _rgb(h)]
    v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
def _mix(h, other, t):
    a, b = _rgb(h), _rgb(other); return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(a, b))
def _darken_until(h, bg, target=4.5):
    t = 0.0
    while contrast(_mix(h, "#000000", t), bg) < target and t < 1:
        t += 0.02
    return _mix(h, "#000000", min(t, 1))

BG = "#080a0e"
INK = "#06121c"   # dark text used on accent buttons and the CTA band
def _colour(key, default):
    v = (CFG.get(key) or default).strip()
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", v):
        sys.exit(f"site.config.json: {key} must be a #rrggbb colour (got {v!r}).")
    if contrast(v, BG) < 4.5 or contrast(INK, v) < 4.5:
        sys.exit(f"site.config.json: {key} {v} is too dark: it is used as text on the dark page and behind dark button text "
                 f"({contrast(v, BG):.1f}:1, needs 4.5:1). Pick a brighter version of the brand colour.")
    return v
ACCENT = _colour("accent", "#3cb4ff")
HEAT = _colour("heat", "#ff6a2b")
ACCENT_2 = _mix(ACCENT, "#ffffff", 0.3)
ACCENT_ON_PAPER = _darken_until(ACCENT, "#e9edf1")
HEAT_ON_PAPER = _darken_until(HEAT, "#e9edf1")

# ---- logo
LOGO_FILE = (CFG.get("logo") or "").strip()
if LOGO_FILE and not os.path.isfile(os.path.join(ROOT, LOGO_FILE.lstrip("/"))):
    sys.exit(f"site.config.json: logo file not found: {LOGO_FILE}")
LOGO_W, LOGO_H = 160, 44

def prep_logo():
    global LOGO_W, LOGO_H
    out = os.path.join(ROOT, "assets", "img", "client-logo.webp")
    if not LOGO_FILE:
        if os.path.exists(out): os.remove(out)
        return
    from PIL import Image
    im = Image.open(os.path.join(ROOT, LOGO_FILE.lstrip("/"))).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox() or (0, 0, im.width, im.height))
    if im.height > 240:
        im = im.resize((round(im.width * 240 / im.height), 240), Image.LANCZOS)
    im.save(out, "WEBP", quality=92, method=6)
    LOGO_W = max(1, round(im.width * LOGO_H / im.height))

PHOTOS = PH.load(CFG, ROOT, set(ALL_SVC), "site.config.json")
PHOTO_CLASSES = {"section": "section section--tight", "head": "sec-head", "kicker": "eyebrow", "h2": "display h-lg", "lead": "lead", "group_title": True}

BIZ = CFG["business_name"]
DOMAIN = CFG["domain"].rstrip("/")
BASE = CFG.get("base_path", "/")
PHONE = CFG["phone_display"]
TEL = CFG["phone_e164"]
CTA = CFG["cta_label"]
CITY_NAMES = [c["name"] for c in CITIES]

def city_list_text():
    return and_join(CITY_NAMES)

# ------------------------------------------------------------------ icons
UI = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
 "chev": '<path d="M6 9l6 6 6-6"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "pin": '<path d="M12 22s7-6.4 7-12a7 7 0 0 0-14 0c0 5.6 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
 "spark": '<path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9"/><path d="M9.5 4.5L12 7l2.5-2.5M9.5 19.5L12 17l2.5 2.5"/>',
 "gauge": '<path d="M4.5 17a8.5 8.5 0 1 1 15 0"/><path d="M12 13l4-4"/><circle cx="12" cy="13" r="1.4"/>',
 "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 "check": '<path d="M4 12l5 5L20 6"/>',
 "flame": '<path d="M12 22c4 0 7-2.8 7-6.8 0-3.6-2.6-5.7-4-8.2-.6 1.8-1.7 3-3 3.4.3-2.9-.6-5.9-3-8.4-.2 3.7-4 6.3-4 11.2C5 19.2 8 22 12 22z"/>',
 "snow": '<path d="M12 2v20M3.3 7l17.4 10M3.3 17L20.7 7"/><path d="M9 3.5l3 2.5 3-2.5M9 20.5l3-2.5 3 2.5"/>',
}
SVC_ICONS = {
 "furnace": ['M6 2h12v20H6z', 'M6 8h12', 'M9 5h2', 'M9.5 16.5c0-1.6 1.3-2.2 1.6-3.5.9.8 1.6 1.7 1.6 2.9a1.6 1.6 0 0 1-3.2.6z', 'M6 19h12'],
 "repair": ['M14.7 6.3a4 4 0 0 0-5.4 5l-6.5 6.5a1.6 1.6 0 0 0 2.3 2.3l6.5-6.5a4 4 0 0 0 5-5.4l-2.4 2.4-2.1-.4-.4-2.1z'],
 "heatpump": ['M3 5h18v14H3z', 'M11 12a3.5 3.5 0 1 0 7 0a3.5 3.5 0 1 0-7 0', 'M14.5 8.5v7M11 12h7', 'M5.5 9h3M5.5 12h3M5.5 15h3'],
 "boiler": ['M7 3h10v18H7z', 'M7 8h10', 'M10 5.5h1', 'M12 18c-1.6 0-2.5-1-2.5-2.3 0-1.6 1.6-2.4 2.5-4.2.9 1.8 2.5 2.6 2.5 4.2 0 1.3-.9 2.3-2.5 2.3z', 'M3 11h4M3 15h4'],
 "ac": ['M3 6h18v13H3z', 'M8 12.5a4 4 0 1 0 8 0a4 4 0 1 0-8 0', 'M12 8.5v8M8 12.5h8', 'M5 21h3M16 21h3'],
 "acrepair": ['M3 6h18v13H3z', 'M7 12.5a3 3 0 1 0 6 0a3 3 0 1 0-6 0', 'M16 9.5v6', 'M18.5 9.5v6'],
 "minisplit": ['M2 5h20v8H2z', 'M5 10h14', 'M6 16c0 1.5 1.2 2 1.2 3.5M12 16c0 1.5 1.2 2 1.2 3.5M18 16c0 1.5 1.2 2 1.2 3.5'],
 "air": ['M3 8h11a3 3 0 1 0-3-3', 'M3 12h16a3 3 0 1 1-3 3', 'M3 16h7'],
 "duct": ['M2 9h10v6H2z', 'M12 9l4-4h6v6h-4l-6 4', 'M5 9v6M9 9v6'],
 "ductclean": ['M2 8h14v8H2z', 'M16 10h3a2 2 0 0 1 2 2v0a2 2 0 0 1-2 2h-3', 'M6 11l-1 2M9 11l-1 2M12 11l-1 2', 'M18 19h4M20 17v4'],
 "maint": ['M9 3h6v3H9z', 'M6 5h12v17H6z', 'M9 11l2 2 4-4', 'M9 17h6'],
 "tank": ['M7 5a5 2 0 0 1 10 0v15a5 2 0 0 1-10 0z', 'M7 5a5 2 0 0 0 10 0', 'M12 1v3', 'M12 14c-1.2 0-2-.8-2-1.8 0-1.2 1.2-1.8 2-3.2.8 1.4 2 2 2 3.2 0 1-.8 1.8-2 1.8z'],
 "thermostat": ['M4 12a8 8 0 1 0 16 0a8 8 0 1 0-16 0', 'M8.5 15.5A5 5 0 0 1 12 7', 'M12 12l3-3', 'M10.5 12a1.5 1.5 0 1 0 3 0a1.5 1.5 0 1 0-3 0'],
 "commercial": ['M4 21V9h16v12', 'M2 21h20', 'M7 4h7v5H7z', 'M8.5 6.5h4', 'M7 13h2M11 13h2M15 13h2M7 17h2M11 17h2M15 17h2'],
 "combo": ['M3 3h8v18H3z', 'M3 8h8', 'M6.5 16c0-1.3 1-1.8 1.2-2.8.8.6 1.3 1.4 1.3 2.3a1.3 1.3 0 0 1-2.5.5z', 'M13 9h8v10h-8z', 'M14.8 14a2.2 2.2 0 1 0 4.4 0a2.2 2.2 0 1 0-4.4 0'],
 "doc": ['M6 2h9l4 4v16H6z', 'M14 2v5h5', 'M9 12h7M9 16h7'],
 "home": ['M3 11l9-8 9 8', 'M5 9.5V21h14V9.5', 'M10 21v-6h4v6'],
 "gauge": ['M3.5 17.5a9 9 0 1 1 17 0', 'M12 13l4.5-4.5', 'M10.5 13a1.5 1.5 0 1 0 3 0a1.5 1.5 0 1 0-3 0', 'M6 13h1.5M12 6v1.5M16.5 13H18'],
}

def ui(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{UI[name]}</svg>'

def sicon(key, cls="svc-card__icon"):
    paths = "".join(f'<path pathLength="1" d="{d}"/>' for d in SVC_ICONS[key])
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths}</svg>'

# brand mark: a comfort dial (cool → heat arc with a needle)
LOGO_MARK = ('<svg class="brand__mark" viewBox="0 0 40 40" fill="none" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
             '<path d="M8.7 31.3A16 16 0 0 1 20 4" stroke="var(--accent)"/><path d="M20 4a16 16 0 0 1 11.3 27.3" stroke="var(--heat)"/>'
             '<path d="M20 20l7-7" stroke="currentColor"/><circle cx="20" cy="20" r="2.6" fill="currentColor" stroke="none"/></svg>')

# ------------------------------------------------------------------ "inside the system" drawing (pinned sequence)
def system_svg(label):
    """Cutaway of an upflow furnace with an A-coil, following the air: return + filter → blower → burners/heat
    exchanger → cooling coil → supply ducts. Each data-layer drops in as the visitor scrolls."""
    g = []
    # base: floor, wall, cabinet outline (always visible)
    g.append('<g class="sys-base"><path class="ln ln--dim" d="M10 500H810"/><path class="ln ln--dim ln--dash" d="M770 0V500"/>'
             '<rect class="ln ln--dim ln--dash" x="300" y="176" width="170" height="314" rx="4"/><rect class="ln ln--dim ln--dash" x="300" y="96" width="170" height="80"/>'
             '<text class="sys-note" x="770" y="-2" text-anchor="middle">OUTSIDE</text></g>')
    # 1 return duct + filter
    g.append('<g class="layer" data-layer="1"><path class="sys-duct" d="M40 120H110V392H286V470H40Z"/>'
             '<path class="sys-duct-in" d="M54 134H96V406"/>'
             '<rect class="sys-filter" x="282" y="392" width="18" height="78"/><path class="sys-pleat" d="M282 398l18 6-18 6 18 6-18 6 18 6-18 6 18 6-18 6 18 6-18 6 18 6-18 6"/>'
             '<path class="sys-flow sys-flow--return" d="M75 140V430H292"/><path class="sys-grille" d="M48 110h54M48 102h54"/></g>')
    # 2 blower
    blades = "".join(f'<path d="M{385 + 26 * math.cos(math.radians(a)):.1f} {431 + 26 * math.sin(math.radians(a)):.1f}L{385 + 40 * math.cos(math.radians(a + 14)):.1f} {431 + 40 * math.sin(math.radians(a + 14)):.1f}"/>' for a in range(0, 360, 24))
    g.append(f'<g class="layer" data-layer="2"><path class="sys-housing" d="M385 383a48 48 0 1 0 50 52h0V398"/>'
             f'<g class="sys-wheel"><circle class="sys-hub" cx="385" cy="431" r="22"/><g class="sys-blades">{blades}</g><circle class="sys-wheel-rim" cx="385" cy="431" r="41"/></g>'
             '<rect class="sys-motor" x="370" y="416" width="30" height="30" rx="6"/></g>')
    # 3 burners + heat exchanger + vent to the wall
    tubes = "M322 344H448V318H330V292H448V266H330V240H448"
    g.append(f'<g class="layer" data-layer="3"><path class="sys-hx" d="{tubes}"/><path class="sys-hx-glow" d="{tubes}"/>'
             '<g class="sys-flames"><path d="M318 350c-6-9 0-14 4-22 4 8 10 13 4 22z"/><path d="M318 338c-3-5 0-8 2-12 2 4 5 7 2 12z" class="sys-flame-core"/></g>'
             '<path class="sys-vent" d="M448 240H770"/><path class="sys-vent-in" d="M448 240H770"/>'
             '<path class="sys-flow sys-flow--exhaust" d="M455 240H760"/><text class="sys-note" x="560" y="270">EXHAUST TO OUTDOORS</text></g>')
    # 4 A-coil in the plenum + refrigerant lines out
    fins = "".join(f'<path d="M{x:.0f} {176 - (x - 312) * 1.45:.0f}l10 -4"/>' for x in range(316, 384, 8)) + "".join(f'<path d="M{x:.0f} {176 - (458 - x) * 1.45:.0f}l-10 -4"/>' for x in range(390, 456, 8))
    g.append(f'<g class="layer" data-layer="4"><path class="sys-coil" d="M312 176L385 104L458 176"/><g class="sys-fins">{fins}</g>'
             '<path class="sys-line sys-line--suction" d="M470 130H770"/><path class="sys-line sys-line--liquid" d="M470 142H770"/>'
             '<text class="sys-note" x="560" y="120">REFRIGERANT TO OUTDOOR UNIT</text></g>')
    # 5 supply plenum + trunk + registers
    regs = "".join(f'<g><path class="sys-duct" d="M{x} 70V22H{x + 40}V70Z"/><path class="sys-reg" d="M{x - 4} 18H{x + 44}M{x + 4} 10H{x + 36}"/><path class="sys-flow sys-flow--supply" d="M{x + 20} 70V12"/></g>' for x in (520, 610, 700))
    g.append(f'<g class="layer" data-layer="5"><path class="sys-duct" d="M300 96V40H760V96H470"/><path class="sys-flow sys-flow--supply" d="M385 96V68H750"/>{regs}</g>')
    # callouts: (layer, label, point x, point y, side the label sits on)
    tags = [(1, "Return & filter", 150, 300, 1), (2, "Blower", 434, 470, 1), (3, "Heat exchanger", 448, 318, 1), (4, "Cooling coil", 322, 150, -1), (5, "Supply", 300, 70, -1)]
    callouts = ""
    for n_, t, x, y, d in tags:
        anchor = "" if d > 0 else ' text-anchor="end"'
        callouts += (f'<g class="sys-tag" data-layer="{n_}"><circle cx="{x}" cy="{y}" r="4"/>'
                     f'<path d="M{x} {y}L{x + 26 * d} {y - 30}H{x + 44 * d}"/><text x="{x + 50 * d}" y="{y - 25}"{anchor}>0{n_} {t.upper()}</text></g>')
    return (f'<svg class="system" viewBox="0 -10 820 520" role="img" aria-label="{html.escape(label)}">'
            '<defs><linearGradient id="sys-hot" x1="0" x2="1"><stop offset="0" stop-color="var(--heat)"/><stop offset="1" stop-color="#ffd27a"/></linearGradient></defs>'
            f'{"".join(g)}{callouts}</svg>')

# ------------------------------------------------------------------ opening animation (comfort dial + name)
def intro_markup():
    ticks = ""
    for i in range(61):
        a = math.radians(135 + i * 4.5)   # 270° sweep starting bottom-left
        r1, r2 = (122, 140) if i % 5 == 0 else (130, 140)
        ticks += f'<path d="M{180 + r1 * math.cos(a):.1f} {180 + r1 * math.sin(a):.1f}L{180 + r2 * math.cos(a):.1f} {180 + r2 * math.sin(a):.1f}" style="--k:{i}"/>'
    return f'''<div class="intro" aria-hidden="true">
<div class="intro__panel intro__panel--top"></div><div class="intro__panel intro__panel--bot"></div>
<div class="intro__inner"><div class="intro__stage">
<svg class="intro__dial" viewBox="0 0 360 360" focusable="false"><defs><linearGradient id="intro-grad" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="var(--accent)"/><stop offset="1" stop-color="var(--heat)"/></linearGradient></defs>
<g class="intro__ticks">{ticks}</g>
<path class="intro__track" d="M81 279A140 140 0 1 1 279 279" pathLength="1"/>
<path class="intro__arc" d="M81 279A140 140 0 1 1 279 279" pathLength="1"/>
<g class="intro__needle"><path d="M180 180L180 76"/><circle cx="180" cy="180" r="9"/></g>
<text class="intro__lbl" x="70" y="318">COOL</text><text class="intro__lbl intro__lbl--heat" x="290" y="318" text-anchor="end">HEAT</text>
</svg>
<div class="intro__read"><span class="intro__count" data-from="{T["from"]}" data-to="{T["set"]}">{T["from"]:04.1f}</span><sup>°{T["unit"]}</sup></div>
<p class="intro__name">{html.escape(BIZ)}</p>
<div class="intro__meta"><span>{html.escape(CFG["region_label"])}</span><span>Set point {T["set"]}°</span></div>
<div class="intro__bar"><i></i></div>
</div></div></div>'''

# ------------------------------------------------------------------ url helpers
def url_of(path):
    if path == "index.html":
        return DOMAIN + "/"
    if path.endswith("/index.html"):
        return DOMAIN + "/" + path[:-len("index.html")]
    return DOMAIN + "/" + path

def href(from_path, to_path):
    from_dir = posixpath.dirname(from_path)
    if to_path.endswith("index.html"):
        target_dir = posixpath.dirname(to_path)
        rel = posixpath.relpath(target_dir or ".", from_dir or ".")
        return "./" if rel == "." else rel + "/"
    return posixpath.relpath(to_path, from_dir or ".")

def asset(from_path, a):
    return posixpath.relpath("assets/" + a, posixpath.dirname(from_path) or ".")

_VER = {}
def vasset(from_path, a):
    """Asset URL with a content hash (?v=...), so browsers fetch the new file as soon as it changes after a deploy."""
    if a not in _VER:
        import hashlib
        _VER[a] = hashlib.md5(open(os.path.join(ROOT, "assets", a), "rb").read()).hexdigest()[:8]
    return asset(from_path, a) + "?v=" + _VER[a]

PATH = {
 "home": "index.html",
 "services": "services/index.html",
 "areas": "service-areas/index.html",
 "about": "about/index.html",
 "faq": "faq/index.html",
 "contact": "contact/index.html",
 "estimate": "system-estimate/index.html",
 "thanks": "thank-you/index.html",
 "privacy": "privacy-policy.html",
 "terms": "terms-and-conditions.html",
 "cookies": "cookie-policy.html",
}
def svc_path(slug): return f"services/{slug}/index.html"
def svc_city_path(slug, city): return f"services/{slug}/{city}/index.html"
def city_path(city): return f"service-areas/{city}/index.html"
def quote_path():
    """Where 'get a price' buttons go: the instant estimate when it's on, else the contact form."""
    return PATH["estimate"] if EST_ON else PATH["contact"]

def expand(text, here):
    """Replace {biz}/{phone} tokens and [[slug|anchor]] links."""
    text = text.replace("{biz}", html.escape(BIZ)).replace("{phone}", html.escape(PHONE))
    def link(m):
        key, anchor = m.group(1), m.group(2)
        if key == "estimate" and not EST_ON: target = PATH["contact"]
        elif key.startswith("area:"): target = city_path(key[5:])
        elif key in PATH: target = PATH[key]
        elif key in SVC: target = svc_path(key)
        elif key in ALL_SVC:
            start = max(text.rfind(". ", 0, m.start()), text.rfind(">", 0, m.start())) + 1
            ends = [i for i in (text.find(". ", m.end()), text.find("<", m.end())) if i != -1]
            sentence = re.sub(r"\[\[[a-z0-9:\-]+\|([^\]]+)\]\]", r"\1", text[start:(min(ends) + 1 if ends else len(text))]).strip().rstrip("<").strip()
            REMOVED_MENTIONS.setdefault(sentence, set()).add(ALL_SVC[key]["name"])
            return anchor
        else: raise SystemExit(f"Unknown link target [[{key}]]")
        return f'<a href="{href(here, target)}">{anchor}</a>'
    return re.sub(r"\[\[([a-z0-9:\-]+)\|([^\]]+)\]\]", link, text)

# ------------------------------------------------------------------ shared components
def nav_html(here, active):
    def a(key, label):
        cur = ' aria-current="page"' if active == key else ""
        return f'<li class="nav__item"><a class="nav__link" href="{href(here, PATH[key])}"{cur}>{label}</a></li>'
    cols = ""
    for cat, label, _ in CATS:
        items = "".join(f'<li><a href="{href(here, svc_path(s["slug"]))}">{sicon(s["icon"], "")}{s["name"]}</a></li>' for s in SERVICES if s["cat"] == cat)
        cols += f'<div><p class="mega__title">{label}</p><ul>{items}</ul></div>'
    cols += f'<div class="mega__all"><span class="muted">{len(SERVICES)} services across {city_list_text()}</span><a class="link-arrow" href="{href(here, PATH["services"])}">All services {ui("arrow")}</a></div>'
    areas = "".join(f'<li><a href="{href(here, city_path(c["slug"]))}">{ui("pin")}{c["name"]}, {CFG["province"]}</a></li>' for c in CITIES)
    areas += f'<li><a href="{href(here, PATH["areas"])}">{ui("arrow")}All service areas</a></li>'
    svc_cur = ' aria-current="page"' if active == "services" else ""
    area_cur = ' aria-current="page"' if active == "areas" else ""
    est = ""
    if EST_ON:
        cur = ' aria-current="page"' if active == "estimate" else ""
        est = f'<li class="nav__item"><a class="nav__link nav__link--est" href="{href(here, PATH["estimate"])}"{cur}><i aria-hidden="true"></i>Instant Estimate</a></li>'
    return f'''<nav class="nav" aria-label="Main">
<ul class="nav__list">
<li class="nav__item" data-dropdown><button class="nav__link" type="button" aria-expanded="false" aria-controls="mega-services"{svc_cur}>Services {ui("chev")}</button>
<div class="mega mega--{len(CATS)}" id="mega-services">{cols}</div></li>
<li class="nav__item" data-dropdown><button class="nav__link" type="button" aria-expanded="false" aria-controls="mega-areas"{area_cur}>Service Areas {ui("chev")}</button>
<div class="mega mega--small" id="mega-areas"><div><p class="mega__title">Where we work</p><ul>{areas}</ul></div></div></li>
{est}{a("about", "About")}{a("faq", "FAQ")}{a("contact", "Contact")}
</ul>
<div class="nav__cta"><a class="nav__phone" href="tel:{TEL}">{ui("phone")}<span>{PHONE}</span><span class="visually-hidden"> (call us)</span></a>
<a class="btn btn--primary btn--sm" href="{href(here, PATH["contact"])}">{CTA}</a></div>
</nav>'''

def mobile_nav_html(here):
    groups = ""
    for cat, label, _ in CATS:
        items = "".join(f'<li><a href="{href(here, svc_path(s["slug"]))}">{s["name"]}</a></li>' for s in SERVICES if s["cat"] == cat)
        groups += f'<li><p class="mobile-nav__group">{label}</p><ul>{items}</ul></li>'
    groups += f'<li><a href="{href(here, PATH["services"])}">All services →</a></li>'
    areas = "".join(f'<li><a href="{href(here, city_path(c["slug"]))}">{c["name"]}</a></li>' for c in CITIES)
    est = f'<li><a class="mobile-nav__est" href="{href(here, PATH["estimate"])}">Instant Estimate</a></li>' if EST_ON else ""
    return f'''<div class="mobile-nav" id="mobile-nav">
<ul>
<li><a href="{href(here, PATH["home"])}">Home</a></li>
{est}
<li><details><summary>Services {ui("plus")}</summary><ul>{groups}</ul></details></li>
<li><details><summary>Service Areas {ui("plus")}</summary><ul>{areas}<li><a href="{href(here, PATH["areas"])}">All service areas →</a></li></ul></details></li>
<li><a href="{href(here, PATH["about"])}">About</a></li>
<li><a href="{href(here, PATH["faq"])}">FAQ</a></li>
<li><a href="{href(here, PATH["contact"])}">Contact</a></li>
</ul>
<div class="mobile-nav__cta"><a class="btn btn--primary" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a><a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} Call {PHONE}</a></div>
</div>'''

def brand_inner(here):
    if LOGO_FILE:
        return f'<img class="brand__logo" src="{asset(here, "img/client-logo.webp")}" alt="{html.escape(BIZ)}" width="{LOGO_W}" height="{LOGO_H}" decoding="async">'
    return f'{LOGO_MARK}<span class="brand__name">{html.escape(BIZ.split(" ")[0])} <small>{html.escape(" ".join(BIZ.split(" ")[1:]) or CFG["short_tagline"])}</small></span>'

def header_html(here, active):
    return f'''<div class="progress" aria-hidden="true"></div>
<header class="site-header">
<div class="wrap">
<a class="brand" href="{href(here, PATH["home"])}" aria-label="{html.escape(BIZ)} home">{brand_inner(here)}</a>
{nav_html(here, active)}
<button class="burger" type="button" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><span></span><span></span><span></span></button>
</div>
</header>
{mobile_nav_html(here)}'''

def hours_text():
    return [f'{h["label"]}: {fmt_time(h["open"])}–{fmt_time(h["close"])}' for h in CFG.get("hours") or []]

def fmt_time(t):
    hh, mm = map(int, t.split(":"))
    suf = "a.m." if hh < 12 else "p.m."
    h12 = hh % 12 or 12
    return f"{h12}:{mm:02d} {suf}" if mm else f"{h12} {suf}"

def cta_band(here, title="Comfort you don't have to think about.", text=None):
    text = text or ("See a ballpark for a new system in about a minute, or book a home visit for a written, itemized quote." if EST_ON
                    else "Book a home visit and we'll give you a written, itemized quote before any work begins.")
    second = (f'<a class="btn btn--ghost" href="{href(here, PATH["estimate"])}">{ui("gauge")} Instant estimate</a>' if EST_ON
              else f'<a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} {PHONE}</a>')
    return f'''<section class="cta-band" aria-labelledby="cta-title">
<div class="cta-band__flow" aria-hidden="true"></div>
<div class="wrap">
<div><h2 class="display" id="cta-title" data-reveal="rise">{title}</h2><p data-reveal="up">{text}</p></div>
<div class="btn-row" data-reveal="up"><a class="btn btn--primary" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a>{second}<a class="cta-band__tel" href="tel:{TEL}">or call {PHONE}</a></div>
</div>
</section>'''

def footer_html(here):
    cols = ""
    for cat, label, _ in CATS:
        items = "".join(f'<li><a href="{href(here, svc_path(s["slug"]))}">{s["name"]}</a></li>' for s in SERVICES if s["cat"] == cat)
        cols += f'<div class="footer__col"><h2>{label}</h2><ul>{items}</ul></div>'
    areas = "".join(f'<li><a href="{href(here, city_path(c["slug"]))}">{c["name"]}</a></li>' for c in CITIES)
    company = (f'<li><a href="{href(here, PATH["about"])}">About</a></li>'
               + (f'<li><a href="{href(here, PATH["estimate"])}">Instant System Estimate</a></li>' if EST_ON else "")
               + f'<li><a href="{href(here, PATH["services"])}">All Services</a></li>'
               f'<li><a href="{href(here, PATH["areas"])}">Service Areas</a></li><li><a href="{href(here, PATH["faq"])}">FAQ</a></li><li><a href="{href(here, PATH["contact"])}">Contact</a></li>')
    hours = "<br>".join(hours_text())
    links = [("Google Business Profile", CFG.get("google_business_profile_url"))] + [(p.get("name"), p.get("url")) for p in CFG.get("social_profiles", [])]
    links = [(n, u) for n, u in links if u]
    profiles = ("<li><span>Find us</span>" + " · ".join(f'<a href="{html.escape(u)}" rel="noopener">{html.escape(n)}</a>' for n, u in links) + "</li>") if links else ""
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="footer__grid footer__grid--{len(CATS)}">
<div class="footer__brand">
<a class="brand" href="{href(here, PATH["home"])}" aria-label="{html.escape(BIZ)} home">{brand_inner(here)}</a>
<p>Heating and cooling for homes and businesses in {city_list_text()}, {CFG["province"]}.</p>
<ul class="footer__contact">
<li><span>Call</span><a href="tel:{TEL}">{PHONE}</a></li>
<li><span>Email</span><a href="mailto:{CFG["email"]}">{CFG["email"]}</a></li>
<li><span>Hours</span>{hours}</li>
{profiles}
</ul>
</div>
{cols}
<div class="footer__col"><h2>Service Areas</h2><ul>{areas}</ul><h2 class="mt-2">Company</h2><ul>{company}</ul></div>
</div>
<div class="footer__bottom">
<p>© {date.today().year} {html.escape(CFG["legal_name"])}. All rights reserved.</p>
<ul><li><a href="{href(here, PATH["privacy"])}">Privacy Policy</a></li><li><a href="{href(here, PATH["terms"])}">Terms &amp; Conditions</a></li><li><a href="{href(here, PATH["cookies"])}">Cookie Policy</a></li></ul>
</div>
</div>
</footer>
<div class="callbar"><a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} Call</a><a class="btn btn--primary" href="{href(here, quote_path())}">{"Instant Estimate" if EST_ON else CTA}</a></div>'''

def crumbs_html(here, trail):
    items = []
    for label, p in trail:
        items.append(f'<li><span aria-current="page">{label}</span></li>' if p is None else f'<li><a href="{href(here, p)}">{label}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'

def crumbs_schema(trail, here):
    lst = [{"@type": "ListItem", "position": i, "name": html.unescape(re.sub("<[^>]+>", "", label)), "item": url_of(p if p else here)} for i, (label, p) in enumerate(trail, 1)]
    return {"@type": "BreadcrumbList", "itemListElement": lst}

def business_ref():
    return {"@type": "HVACBusiness", "@id": DOMAIN + "/#business", "name": BIZ, "url": DOMAIN + "/", "telephone": TEL}

def business_entity():
    e = {
        "@type": "HVACBusiness",
        "@id": DOMAIN + "/#business",
        "name": BIZ,
        "url": DOMAIN + "/",
        "logo": DOMAIN + "/assets/img/logo.png",
        "image": DOMAIN + "/assets/img/og-default.png",
        "telephone": TEL,
        "email": CFG["email"],
        "areaServed": [{"@type": "City", "name": f'{c["name"]}, {CFG["province"]}'} for c in CITIES],
        "knowsAbout": [s["name"] for s in SERVICES],
    }
    if CFG.get("legal_name") and CFG["legal_name"] != BIZ:
        e["legalName"] = CFG["legal_name"]
    a = CFG.get("address")
    if a:
        e["address"] = {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["city"], "addressRegion": a["region"], "postalCode": a["postal"], "addressCountry": CFG["country"]}
    if CFG.get("hours"):
        e["openingHoursSpecification"] = [{"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"], "opens": h["open"], "closes": h["close"]} for h in CFG["hours"]]
    same = [u for u in [CFG.get("google_business_profile_url")] + [p.get("url") for p in CFG.get("social_profiles", [])] if u]
    if same:
        e["sameAs"] = same
    return e

PAGES = []

def demo_bar():
    if not CFG.get("demo_mode"):
        return ""
    return ('<aside class="demo-bar" aria-label="Website demo notice">Website demo: the business name, phone, email, service areas and estimate pricing on this site are '
            'samples, not a real company.</aside>')

def page(path, *, title, desc, body, active=None, crumbs=None, schema=None, noindex=False, og_type="website", head_extra="", scripts_extra="", body_class=""):
    full_title = title if BIZ in title else f"{title} | {BIZ}"
    if len(full_title) > 65 and BIZ not in title:
        full_title = title
    robots = "noindex, follow" if (noindex or CFG.get("demo_mode")) else "index, follow"
    graph = list(schema or [])
    if crumbs:
        graph.append(crumbs_schema(crumbs, path))
    ld = ""
    if graph:
        ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"
    canonical = url_of(path) if path != "404.html" else DOMAIN + "/404.html"
    verify = f'<meta name="google-site-verification" content="{html.escape(CFG["google_site_verification"])}">' if CFG.get("google_site_verification") else ""
    # Opening animation: plays on whichever indexable page a visitor opens first in a browser session (e.g. a service
    # page from Google), then never again that session. Skipped when the URL has a #hash, for reduced motion, on the
    # 404 and thank-you pages, and everywhere when config "intro" is false ("intro_scope": "home" = home page only).
    intro_here = INTRO_ON and not noindex and (INTRO_SCOPE == "all" or path == "index.html")
    if intro_here:
        boot = ('<script>(function(d){d.className=d.className.replace("no-js","js");try{if(sessionStorage.getItem("hv-intro")||location.hash.length>1||'
                'matchMedia("(prefers-reduced-motion: reduce)").matches)d.className+=" no-intro"}catch(e){d.className+=" no-intro"}})(document.documentElement)</script>')
    else:
        boot = '<script>document.documentElement.className=document.documentElement.className.replace("no-js","js");</script>'
    html_cls = "no-js" + (" has-demo" if CFG.get("demo_mode") else "") + ("" if intro_here else " no-intro")
    out = f'''<!doctype html>
<html lang="{LOCALE}" class="{html_cls}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
{verify}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{html.escape(BIZ)}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(BIZ)} — heating and cooling in {html.escape(CFG["region_label"])}">
<meta property="og:locale" content="{OG_LOCALE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{BG}">
<link rel="icon" href="{asset(path, "img/favicon.svg")}" type="image/svg+xml">
<link rel="icon" href="{asset(path, "img/favicon-32.png")}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{asset(path, "img/apple-touch-icon.png")}">
<link rel="preload" href="{asset(path, "fonts/anton-latin-400-normal.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{asset(path, "fonts/barlow-latin-400-normal.woff2")}" as="font" type="font/woff2" crossorigin>
{head_extra}
<link rel="stylesheet" href="{vasset(path, "css/main.css")}">
<style>:root{{--accent:{ACCENT};--accent-2:{ACCENT_2};--accent-paper:{ACCENT_ON_PAPER};--heat:{HEAT};--heat-paper:{HEAT_ON_PAPER}}}</style>
{boot}
{ld}
</head>
<body{f' class="{body_class}"' if body_class else ""}>
<a class="skip-link" href="#main">Skip to content</a>
{demo_bar()}
{intro_markup() if intro_here else ""}
{header_html(path, active)}
<main id="main">
{body}
</main>
{footer_html(path)}
<script src="{vasset(path, "js/main.js")}" defer></script>
{scripts_extra}
</body>
</html>
'''
    out = re.sub(r"\n{2,}", "\n", out)
    dest = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(dest) or ROOT, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(out)
    PAGES.append({"path": path, "url": canonical if path != "404.html" else None, "title": full_title, "noindex": noindex})

def page_hero(here, *, eyebrow, h1, lead, crumbs, ctas=True, mark_icon=None, est_cta=True, compact=False):
    mark = sicon(mark_icon, "page-hero__mark") if mark_icon else ""
    btns = ""
    if ctas:
        second = (f'<a class="btn btn--ghost" href="{href(here, PATH["estimate"])}">{ui("gauge")} Instant estimate</a>' if (EST_ON and est_cta)
                  else f'<a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} {PHONE}</a>')
        btns = f'<div class="btn-row intro-fade" style="--d:500ms"><a class="btn btn--primary" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a>{second}</div>'
    return f'''<section class="page-hero{" page-hero--compact" if compact else ""}">
<div class="page-hero__flow" aria-hidden="true"></div>
<div class="wrap">
<div class="intro-fade">{crumbs_html(here, crumbs)}</div>
<p class="eyebrow intro-fade" style="--d:100ms">{eyebrow}</p>
<h1 class="display" data-split>{h1}</h1>
<p class="lead intro-fade" style="--d:350ms">{lead}</p>
{btns}
</div>
{mark}
</section>'''

def svc_card(here, s, n, heading="h3", target=None):
    t = target or svc_path(s["slug"])
    return (f'<a class="svc-card svc-card--{s["cat"]}" href="{href(here, t)}" data-reveal="up"><div class="svc-card__top">{sicon(s["icon"])}<span class="svc-card__no">{n:02d}</span></div>'
            f'<{heading}>{s["name"]}</{heading}><p>{s["short"]}</p><span class="svc-card__go">View service {ui("arrow")}</span></a>')

def faq_html(faqs):
    return '<div class="faq">' + "".join(
        f'<details><summary>{html.escape(q)}<i aria-hidden="true"></i></summary><div class="faq__a"><p>{html.escape(a)}</p></div></details>' for q, a in faqs) + "</div>"

def est_card(here):
    if not EST_ON:
        return ""
    return f'''<div class="aside-card aside-card--est" data-reveal="up"><p class="mono accent">Instant estimate</p><h2>Price a new system</h2><p>Pick the system, your home's size and the efficiency level, and see a ballpark installed price in about a minute.</p>
<a class="btn btn--ghost" href="{href(here, PATH["estimate"])}">{ui("gauge")} Start my estimate</a></div>'''

def aside_html(here, s=None, city=None):
    hours = "<br>".join(hours_text())
    quote = f'''<div class="aside-card aside-card--accent" data-reveal="up"><h2>Get a quote</h2><p>Tell us what's going on and we'll book a visit and give you a written, itemized quote.</p>
<a class="btn btn--primary" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a><a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} {PHONE}</a></div>'''
    blocks = [quote, est_card(here)]
    if s:
        rel = "".join(f'<li><a href="{href(here, svc_path(r) if not city else svc_city_path(r, city["slug"]))}">{SVC[r]["name"]}{" in " + city["name"] if city else ""}{ui("arrow")}</a></li>' for r in related_of(s))
        if rel:
            blocks.append(f'<div class="aside-card" data-reveal="up"><h2>Related services</h2><ul class="aside-list">{rel}</ul></div>')
        cl = "".join(f'<li><a href="{href(here, svc_city_path(s["slug"], c["slug"]))}"{" aria-current=\"page\"" if city and c["slug"] == city["slug"] else ""}>{s["name"]} in {c["name"]}{ui("arrow")}</a></li>' for c in CITIES)
        blocks.append(f'<div class="aside-card" data-reveal="up"><h2>Service areas</h2><ul class="aside-list">{cl}</ul></div>')
    blocks.append(f'<div class="aside-card" data-reveal="up"><h2>Hours</h2><p class="muted" style="margin:0">{hours}<br>{CFG.get("hours_note","")}</p></div>')
    return '<aside class="aside" aria-label="Heating and cooling help">' + "".join(b for b in blocks if b) + "</aside>"

# ------------------------------------------------------------------ pages
def lower_name(s):
    """Service name for use mid-sentence: lower case, keeping acronyms (AC, HVAC) in capitals."""
    return re.sub(r"\b(ac|hvac)\b", lambda m: m.group(1).upper(), s["name"].lower())

def build_service(s):
    here = svc_path(s["slug"])
    cat_label = dict((c, l) for c, l, _ in CATS)[s["cat"]]
    crumbs = [("Home", PATH["home"]), ("Services", PATH["services"]), (s["name"], None)]
    cities = "".join(f'<a class="chip" href="{href(here, svc_city_path(s["slug"], c["slug"]))}">{ui("pin")}{s["name"]} in {c["name"]}</a>' for c in CITIES)
    who = "businesses and property managers" if s["slug"] == "commercial-hvac" else "homeowners"
    content = f'''{page_hero(here, eyebrow=cat_label, h1=s["h1"], lead=s["lead"], crumbs=crumbs, mark_icon=s["icon"])}
<section class="section section--tight">
<div class="wrap article">
<div class="prose" data-reveal="up">
{expand(s["body"], here)}
<h2>What affects the cost of {lower_name(s)}</h2>
{COSTS[s["slug"]]}
<h2>{s["name"]} questions</h2>
{faq_html(s["faqs"])}
<h2>Where we offer {lower_name(s)}</h2>
<p>We provide {lower_name(s)} for {who} in {city_list_text()}. See what to expect in your area:</p>
<div class="chips">{cities}</div>
</div>
{aside_html(here, s)}
</div>
</section>
{PH.gallery(PH.for_service(PHOTOS, s["slug"]), lambda x: asset(here, x[len("/assets/"):]), f"{s['name']} we have done", kicker="Our work", limit=3, classes=PHOTO_CLASSES)}
{cta_band(here)}'''
    schema = [{
        "@type": "Service", "@id": url_of(here) + "#service", "name": s["name"], "serviceType": s["name"],
        "description": s["desc"], "url": url_of(here), "provider": business_ref(),
        "areaServed": [{"@type": "City", "name": f'{c["name"]}, {CFG["province"]}'} for c in CITIES],
    }]
    page(here, title=s["title"], desc=s["desc"], body=content, active="services", crumbs=crumbs, schema=schema)

def build_service_city(s, c):
    here = svc_city_path(s["slug"], c["slug"])
    crumbs = [("Home", PATH["home"]), ("Services", PATH["services"]), (s["name"], svc_path(s["slug"])), (c["name"], None)]
    labels = re.findall(r"<li><strong>([^<]+)</strong>", s["body"])
    included = "".join(f"<li>{l}</li>" for l in labels)
    audience = "businesses" if s["slug"] == "commercial-hvac" else "homes"
    others = [x for x in CITIES if x["slug"] != c["slug"]]
    other_links = " and ".join(f'<a href="{href(here, svc_city_path(s["slug"], o["slug"]))}">{lower_name(s)} in {o["name"]}</a>' for o in others)
    rel_links = ", ".join(f'<a href="{href(here, svc_city_path(r, c["slug"]))}">{lower_name(SVC[r])}</a>' for r in related_of(s))
    rel_sentence = (f"People planning {lower_name(s)} in {c['name']} often look at related work too, including {rel_links}. " if rel_links else "")
    est_ok = EST_ON and any(x.get("service") == s["slug"] for x in EST["systems"])
    est_line = (f' Want a ballpark first? Try the <a href="{href(here, PATH["estimate"])}">instant system estimate</a>.' if est_ok else "")
    body = f'''<h2>{s["name"]} for {c["name"]} {audience}</h2>
<p>{c["short"]} {s["cities"][c["slug"]]}</p>
<h2>What's included</h2>
<p>{s["short"]} Depending on your home and equipment, the work can include:</p>
<ul>{included}</ul>
<p>Full details, how the work runs and common questions are on our main <a href="{href(here, svc_path(s["slug"]))}">{lower_name(s)} page</a>.{est_line}</p>
<h2>Local conditions in {c["name"]}</h2>
<p>{c["cat"][s["cat"]]}</p>
<h2>Questions to ask before you hire</h2>
<p>Whoever you hire for {lower_name(s)} in {c["name"]}, get clear answers to these before signing:</p>
<ul>{"".join(f"<li>{q}</li>" for q in ASK[s["slug"]])}</ul>
<h2>Permits and licensing</h2>
<p>{c["permits"]}</p>
<h2>More from {html.escape(BIZ)} in {c["name"]}</h2>
<p>{rel_sentence}We also provide {other_links}. See every service we offer on our <a href="{href(here, city_path(c["slug"]))}">{c["name"]} service area page</a>.</p>'''
    content = f'''{page_hero(here, eyebrow=f'{c["name"]}, {CFG["province"]}', h1=f'{s["name"]} in {c["name"]}', lead=f'{s["name"]} for {c["name"]} {audience}, assessed in person, priced in writing and tested before we leave.', crumbs=crumbs, mark_icon=s["icon"])}
<section class="section section--tight">
<div class="wrap article">
<div class="prose" data-reveal="up">{expand(body, here)}</div>
{aside_html(here, s, c)}
</div>
</section>
{cta_band(here, title=f"{s['name']} in {c['name']}? Let's talk.")}'''
    desc = f'{s["name"]} in {c["name"]}, {CFG["province"]}: {s["short"][0].lower() + s["short"][1:]}'
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0] + "…"
    schema = [{
        "@type": "Service", "@id": url_of(here) + "#service", "name": f'{s["name"]} in {c["name"]}, {CFG["province"]}',
        "serviceType": s["name"], "url": url_of(here), "provider": business_ref(),
        "areaServed": {"@type": "City", "name": f'{c["name"]}, {CFG["province"]}'},
    }]
    page(here, title=f'{s["name"]} in {c["name"]}, {CFG["province"]}', desc=desc, body=content, active="services", crumbs=crumbs, schema=schema)

def svc_groups(here, heading="h3", city=None, head_tag="h2"):
    groups, n = "", 0
    for i, (cat, label, blurb) in enumerate(CATS, 1):
        cards = ""
        for s in SERVICES:
            if s["cat"] == cat:
                n += 1
                cards += svc_card(here, s, n, heading=heading, target=svc_city_path(s["slug"], city["slug"]) if city else None)
        title = f"{label} in {city['name']}" if city else label
        text = city["cat"][cat] if city else blurb
        groups += (f'<div class="svc-group svc-group--{cat}"><div class="svc-group__head" data-reveal="up"><span class="svc-group__num">0{i}</span><div><{head_tag} class="display h-md">{title}</{head_tag}>'
                   f'<p class="muted" style="margin:6px 0 0">{text}</p></div></div><div class="svc-grid" data-stagger>{cards}</div></div>')
    return groups

def build_services_hub():
    here = PATH["services"]
    crumbs = [("Home", PATH["home"]), ("Services", None)]
    content = f'''{page_hero(here, eyebrow="What we do", h1="Heating & Cooling Services", lead=f"{len(SERVICES)} heating, cooling and air service{'s' if len(SERVICES) != 1 else ''} for homes and businesses in {city_list_text()}, from new furnaces and heat pumps to the ducts and thermostats around them.", crumbs=crumbs, mark_icon="gauge")}
<section class="section section--tight"><div class="wrap">{svc_groups(here)}</div></section>
{cta_band(here)}'''
    items = [{"@type": "ListItem", "position": i, "url": url_of(svc_path(s["slug"])), "name": s["name"]} for i, s in enumerate(SERVICES, 1)]
    names = [lower_name(x) for x in SERVICES]
    desc = f"HVAC services in {city_list_text()}, {CFG['province']}: " + (", ".join(names[:5]) + " and more." if len(names) > 5 else and_join(names) + ".")
    if len(desc) > 158:
        desc = f"HVAC services in {city_list_text()}, {CFG['province']}: " + ", ".join(names[:3]) + " and more."
    page(here, title="Heating & Cooling Services", desc=desc, body=content, active="services", crumbs=crumbs, schema=[{"@type": "ItemList", "itemListElement": items}])

def build_city_hub(c):
    here = city_path(c["slug"])
    crumbs = [("Home", PATH["home"]), ("Service Areas", PATH["areas"]), (c["name"], None)]
    hub = "".join(f"<p>{p}</p>" for p in c["hub"])
    others = " · ".join(f'<a href="{href(here, city_path(o["slug"]))}">{o["name"]}</a>' for o in CITIES if o["slug"] != c["slug"])
    content = f'''{page_hero(here, eyebrow=f'Service area · {c["region"]}', h1=f'Heating & Cooling in {c["name"]}, {CFG["province"]}', lead=c["intro"], crumbs=crumbs, mark_icon="home")}
<section class="section section--tight"><div class="wrap">
<div class="hub-intro prose"><div data-reveal="up">{hub}</div><div data-reveal="up"><h2 class="h-sm" style="margin-top:0">Permits and licensing in {c["name"]}</h2><p>{c["permits"]}</p><p>Also serving: {others}</p></div></div>
{svc_groups(here, city=c)}
</div></section>
{cta_band(here, title=f"Heating & cooling in {c['name']}? We're close by.")}'''
    page(here, title=c["title"], desc=c["desc"], body=content, active="areas", crumbs=crumbs)

def build_areas_hub():
    here = PATH["areas"]
    crumbs = [("Home", PATH["home"]), ("Service Areas", None)]
    cards = "".join(f'''<a class="area-card" href="{href(here, city_path(c["slug"]))}" data-reveal="up"><span class="area-card__no" aria-hidden="true">0{i}</span><div><h2>{c["name"]}</h2><p>{c["intro"]}</p><span class="svc-card__go">{len(SERVICES)} service{"s" if len(SERVICES) != 1 else ""} in {c["name"]} {ui("arrow")}</span></div></a>''' for i, c in enumerate(CITIES, 1))
    content = f'''{page_hero(here, eyebrow=CFG["region_label"], h1="Service Areas", lead=f"We heat and cool homes and businesses in {city_list_text()}. Each area page covers local housing, climate, permits and every service we offer there.", crumbs=crumbs, mark_icon="home")}
<section class="section section--tight"><div class="wrap"><div class="areas" data-stagger>{cards}</div>
<div class="prose mt-3" data-reveal="up"><p>Just outside these communities? <a href="{href(here, PATH["contact"])}">Contact us</a> with your address and what you need, and we'll let you know whether we can help.</p></div></div></section>
{cta_band(here)}'''
    page(here, title=f"Service Areas: {city_list_text()}", desc=f"Heating and cooling in {city_list_text()}, {CFG['province']}: local housing, climate, permits and every HVAC service we offer in your area.", body=content, active="areas", crumbs=crumbs)

def hero_picker(here):
    """System picker in the hero card. A plain GET form to the estimate page, so it works without JavaScript."""
    if not EST_ON:
        return ""
    default = EST.get("default_system")
    opts = "".join(f'''<label class="pick"><input type="radio" name="system" value="{x["id"]}"{" checked" if x["id"] == default else ""}><span class="pick__box">{sicon(x.get("icon", "gauge"), "pick__icon")}<b>{html.escape(x["label"])}</b></span></label>''' for x in EST["systems"])
    return f'''<form class="picker" action="{href(here, PATH["estimate"])}" method="get" aria-label="Instant system estimate">
<fieldset><legend class="picker__label">What are you replacing?</legend><div class="picker__grid">{opts}</div></fieldset>
<button class="btn btn--primary picker__go" type="submit"><span>Price my system</span>{ui("arrow")}</button>
</form>'''

def gauge_svg():
    """Illustration for the home estimate section: a dial with a price-range readout."""
    ticks = "".join(f'<path d="M{200 + 150 * math.cos(math.radians(a)):.1f} {210 + 150 * math.sin(math.radians(a)):.1f}L{200 + (132 if i % 4 == 0 else 140) * math.cos(math.radians(a)):.1f} {210 + (132 if i % 4 == 0 else 140) * math.sin(math.radians(a)):.1f}"/>'
                    for i, a in enumerate(range(150, 391, 6)))
    return f'''<svg class="gauge" viewBox="0 0 400 360" role="img" aria-label="Illustration of an estimate dial showing an example price range">
<defs><linearGradient id="g-arc" x1="0" x2="1"><stop offset="0" stop-color="var(--accent)"/><stop offset="1" stop-color="var(--heat)"/></linearGradient></defs>
<rect x="1" y="1" width="398" height="358" rx="14" class="gauge__bg"/>
<g class="gauge__ticks">{ticks}</g>
<path class="gauge__track" d="M70 285A150 150 0 1 1 330 285" pathLength="1"/>
<path class="gauge__arc" d="M70 285A150 150 0 1 1 330 285" pathLength="1"/>
<g class="gauge__needle"><path d="M200 210L200 88"/><circle cx="200" cy="210" r="10"/></g>
<text class="gauge__k" x="200" y="262" text-anchor="middle">ESTIMATED RANGE</text>
<text class="gauge__v" x="200" y="300" text-anchor="middle">$10,200 – $13,100</text>
<rect x="20" y="20" width="180" height="32" rx="4" class="gauge__chip"/><text class="gauge__chip-t" x="34" y="41">EXAMPLE · NOT A QUOTE</text>
</svg>'''

def build_home():
    here = PATH["home"]
    p = P.home(CFG, CITIES, SERVICES, ALL_OFFERED)
    areas = "".join(f'<a href="{href(here, city_path(c["slug"]))}">{c["name"]}</a>' for c in CITIES)
    marquee_items = "".join(f'<span class="marquee__item">{s["name"]}</span>{ui("snow" if i % 2 else "flame", "marquee__star marquee__star--" + ("cool" if i % 2 else "heat"))}' for i, s in enumerate(SERVICES))
    layer_steps = "".join(f'<li class="sequence__step{" is-active" if i == 0 else ""}"><h3><span>0{i+1}</span>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(p["layers"]))
    feats = "".join(f'<div class="feature" data-reveal="up"><p class="feature__no" aria-hidden="true">0{i+1}</p><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(p["features"]))
    procs = "".join(f'<li class="proc" data-reveal="up"><span class="proc__no" aria-hidden="true">0{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(p["process"] if EST_ON else p["process"][1:]))
    area_cards = "".join(f'''<a class="area-card" href="{href(here, city_path(c["slug"]))}" data-reveal="up"><span class="area-card__no" aria-hidden="true">0{i}</span><div><h3>{c["name"]}</h3><p>{c["short"]}</p><span class="svc-card__go">Heating &amp; cooling in {c["name"]} {ui("arrow")}</span></div></a>''' for i, c in enumerate(CITIES, 1))
    foot = "".join(f'<div data-reveal="up"><h3>{t}</h3><p>{d}</p></div>' for t, d in p["statement_points"])
    tags = "".join(f'<li>{ui("check")}{t}</li>' for t in p["tags"])
    fx = '<canvas class="hero__fx" aria-hidden="true"></canvas>' if FX_ON else ""
    if EST_ON:
        hero_side = f'''<div class="hero__est intro-fade" style="--d:450ms">
<div class="hero__est-head"><span class="hero__live"><i></i>Instant estimate</span><span class="mono muted">About 60 seconds</span></div>
<p class="hero__est-title">Price a new system<br><span class="accent">before anyone visits.</span></p>
{hero_picker(here)}
<ul class="hero__est-steps"><li><b>01</b>System</li><li><b>02</b>Home size</li><li><b>03</b>Price</li></ul>
</div>'''
        est_section = f'''<section class="section est-teaser" aria-labelledby="est-title">
<div class="wrap est-teaser__grid">
<div><p class="eyebrow">Instant system estimate</p><h2 class="display h-xl" id="est-title" data-reveal="rise">Know the number<br><span class="outline">before the visit.</span></h2>
<p class="lead mt-1" data-reveal="up">No waiting for a callback to find out whether a new furnace, air conditioner or heat pump fits your budget. Pick what you need and see a ballpark installed price right away.</p>
<ol class="est-teaser__steps" data-stagger><li data-reveal="up"><b>01</b><span><strong>Pick the system.</strong> Furnace, air conditioner, both, a heat pump or ductless.</span></li>
<li data-reveal="up"><b>02</b><span><strong>Tell us the size.</strong> Your home's square footage and the efficiency level you want.</span></li>
<li data-reveal="up"><b>03</b><span><strong>See the range.</strong> Add extras like a smart thermostat or humidifier and the price updates instantly.</span></li></ol>
<div class="btn-row mt-2" data-reveal="up"><a class="btn btn--primary" href="{href(here, PATH["estimate"])}">{ui("gauge")} Get my instant estimate</a></div>
<p class="fine mt-1" data-reveal="up">A ballpark, not a quote. Your written price is confirmed after a home visit.</p></div>
<div class="est-teaser__art" data-reveal="scale">{gauge_svg()}</div>
</div></section>'''
    else:
        hero_side = f'<div class="hero__est hero__est--plain intro-fade" style="--d:450ms"><p class="hero__est-title">No heat right now?</p><p class="hero__est-text">Call and we\'ll get a technician out.</p><a class="btn btn--primary" href="tel:{TEL}">{ui("phone")} {PHONE}</a></div>'
        est_section = ""
    # CLIENT REVIEW: only set emergency_24_7 true if the client really answers no-heat calls around the clock.
    nh_kicker = "24/7 no-heat service" if H24 else "No heat?"
    nh_text = ("Furnace down in the middle of the night? Call any time, day or night, and a licensed technician will get you warm again."
               if H24 else "A furnace that quits in January is an emergency. Call us, and we'll get a licensed technician to you as quickly as the schedule allows and tell you honestly when that will be.")
    repair_link = f'<a class="btn btn--ghost" href="{href(here, svc_path("furnace-repair"))}">Furnace repair {ui("arrow")}</a>' if "furnace-repair" in SVC else ""
    noheat = f'''<section class="noheat" aria-labelledby="noheat-title">
<div class="noheat__frost" aria-hidden="true"></div><div class="noheat__snow" aria-hidden="true"></div>
<div class="wrap noheat__grid">
<div><p class="eyebrow eyebrow--cool">{nh_kicker}</p><h2 class="display h-xl" id="noheat-title" data-reveal="rise">Furnace quit<br><span class="noheat__temp">at {deg(T["cold"])}?</span></h2></div>
<div data-reveal="up"><p class="lead">{nh_text}</p>
<p class="noheat__gas">{ui("flame")}<span>Smell gas? Leave the house first, then call your gas utility's emergency line from outside.</span></p>
<div class="btn-row mt-2"><a class="btn btn--primary" href="tel:{TEL}">{ui("phone")} Call {PHONE}</a>{repair_link}</div></div>
</div></section>''' if ("furnace-repair" in SVC or "boiler-services" in SVC) else ""
    content = f'''<section class="hero" aria-labelledby="hero-title">
<div class="hero__media" aria-hidden="true">{fx}<div class="hero__glow hero__glow--cool"></div><div class="hero__glow hero__glow--heat"></div><div class="hero__shade"></div><div class="hero__grid-lines"></div></div>
<div class="wrap hero__grid">
<div class="hero__copy">
<h1 id="hero-title"><span class="eyebrow intro-fade" style="--d:0ms">{p["eyebrow"]}</span><span class="display hero__title" data-split style="--base-delay:150ms"><span class="line">Built for <span class="cool">{deg(T["cold"])}.</span></span> <span class="line">Ready for <span class="heat">{deg(T["hot"])}.</span></span></span></h1>
<p class="lead intro-fade" style="--d:650ms">{p["lead"]}</p>
<div class="btn-row intro-fade" style="--d:800ms"><a class="btn btn--primary" href="{href(here, PATH["contact"])}">{CTA} {ui("arrow")}</a><a class="btn btn--ghost" href="tel:{TEL}">{ui("phone")} {PHONE}</a></div>
<p class="hero__areas intro-fade" style="--d:950ms"><span>Serving</span>{areas}</p>
</div>
{hero_side}
</div>
<ul class="hero__tags intro-fade" style="--d:1100ms">{tags}</ul>
<div class="scroll-cue" aria-hidden="true"><span>Scroll</span><i></i></div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee__track"><div class="marquee__group">{marquee_items}</div><div class="marquee__group">{marquee_items}</div></div></div>
<section class="section statement" aria-labelledby="statement-title">
<div class="wrap">
<h2 class="eyebrow" id="statement-title">{p["statement_eyebrow"]}</h2>
<p class="fill-text" data-fill>{p["statement"]}</p>
<div class="statement__foot" data-stagger>{foot}</div>
</div>
</section>
<section class="sequence" aria-labelledby="seq-title">
<div class="sequence__sticky"><div class="wrap sequence__grid">
<div><p class="eyebrow">Inside the system</p><h2 class="display h-lg" id="seq-title">Five stages.<br>Zero shortcuts.</h2>
<div class="sequence__steps"><span class="sequence__rail" aria-hidden="true"></span><ol>{layer_steps}</ol></div></div>
<div class="sequence__art"><span class="sequence__pct" aria-hidden="true">00%</span>{system_svg("Cutaway of a furnace and air conditioner coil, following the air: return and filter, blower, burners and heat exchanger, cooling coil, and supply ducts to the rooms")}</div>
</div></div>
</section>
<section class="section" aria-labelledby="services-title">
<div class="wrap">
<div class="sec-head"><div><p class="eyebrow">What we do</p><h2 class="display h-xl" id="services-title" data-reveal="rise">Heat. Cool.<br><span class="outline">Breathe easy.</span></h2></div><p class="lead" data-reveal="up">{p["services_lead"]}</p></div>
{svc_groups(here, heading="h4", head_tag="h3")}
<p class="mt-3 center" data-reveal="up"><a class="btn btn--ghost" href="{href(here, PATH["services"])}">Browse all services {ui("arrow")}</a></p>
</div>
</section>
{est_section}
{noheat}
{PH.gallery(PHOTOS, lambda x: asset(here, x[len("/assets/"):]), f"Recent work from {BIZ}", f"Real installations from around {CFG['region_label']}.", classes=PHOTO_CLASSES)}
<section class="section section--tight" aria-labelledby="proc-title">
<div class="wrap">
<div class="sec-head"><div><p class="eyebrow">How it works</p><h2 class="display h-lg" id="proc-title" data-reveal="rise">From first call<br>to first start-up.</h2></div></div>
<ol class="procs" data-stagger>{procs}</ol>
</div>
</section>
<section class="section" aria-labelledby="why-title">
<div class="wrap">
<div class="sec-head"><div><p class="eyebrow">How we work</p><h2 class="display h-xl" id="why-title" data-reveal="rise">No guesswork.<br><span class="outline">No runaround.</span></h2></div><p class="lead" data-reveal="up">{p["why_lead"]}</p></div>
<div class="features" data-stagger>{feats}</div>
</div>
</section>
<section class="section section--tight" aria-labelledby="areas-title" style="border-top:1px solid var(--line)">
<div class="wrap">
<div class="sec-head"><div><p class="eyebrow">Where we work</p><h2 class="display h-xl" id="areas-title" data-reveal="rise">Local to<br><span class="outline">{html.escape(CFG["region_label"])}.</span></h2></div><p class="lead" data-reveal="up">Every area page covers local housing, climate and permits, along with every service we offer there.</p></div>
<div class="areas" data-stagger>{area_cards}</div>
</div>
</section>
<section class="section" aria-labelledby="faq-title">
<div class="wrap article" style="grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr)">
<div><p class="eyebrow">Questions</p><h2 class="display h-lg" id="faq-title" data-reveal="rise">Straight<br>answers.</h2><p class="lead mt-1" data-reveal="up">What homeowners ask us most, before they commit to anything.</p><p class="mt-2"><a class="link-arrow" href="{href(here, PATH["faq"])}">All FAQs {ui("arrow")}</a></p></div>
<div data-reveal="up">{faq_html(p["faqs"] if EST_ON else p["faqs"][1:])}</div>
</div>
</section>
{cta_band(here)}'''
    website = {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": BIZ, "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": LOCALE}
    page(here, title=f"{BIZ} | Heating & Cooling, {CFG['region_label']}", desc=p["desc"], body=content, active="home", schema=[business_entity(), website], body_class="home")

def build_estimate():
    if not EST_ON:
        return
    here = PATH["estimate"]
    crumbs = [("Home", PATH["home"]), ("Instant System Estimate", None)]
    e = EST
    systems = "".join(f'''<label class="opt opt--sys"><input type="radio" name="system" value="{x["id"]}"{" checked" if x["id"] == e.get("default_system") else ""}>
<span class="opt__box">{sicon(x.get("icon", "gauge"), "opt__icon")}<b>{html.escape(x["label"])}</b><small>{html.escape(x.get("hint", ""))}</small></span></label>''' for x in e["systems"])
    sizes = "".join(f'<label class="opt"><input type="radio" name="size" value="{x["id"]}"{" checked" if x["id"] == e.get("default_size") else ""}><span class="opt__box"><b>{html.escape(x["label"])}</b></span></label>' for x in e["home_sizes"])
    tiers = "".join(f'<label class="opt"><input type="radio" name="tier" value="{x["id"]}"{" checked" if x["id"] == e.get("default_tier") else ""}><span class="opt__box"><b>{html.escape(x["label"])}</b><small>{html.escape(x.get("hint", ""))}</small></span></label>' for x in e["tiers"])
    addons = "".join(f'<label class="chk" data-addon="{x["id"]}"><input type="checkbox" name="addon" value="{x["id"]}"><span class="chk__box"><i aria-hidden="true">{ui("check")}</i><b>{html.escape(x["label"])}</b><small class="chk__price" data-price="{x["price"]}"></small></span></label>' for x in e.get("addons", []))
    ms = next((x for x in e["systems"] if x.get("extra_zone")), None)
    zones = ""
    if ms:
        zones = f'''<div class="est-zones" id="est-zones" hidden><label class="field-label" for="est-zone-n">Indoor heads (rooms or zones)</label>
<div class="stepper"><button class="stepper__b" type="button" data-step="-1" aria-label="Fewer zones">−</button><input id="est-zone-n" type="number" min="1" max="{ms.get("max_zones", 5)}" value="1" inputmode="numeric"><button class="stepper__b" type="button" data-step="1" aria-label="More zones">+</button></div></div>'''
    def fld(id_, label, inp, req=True, full=False):
        r = ' <span class="req" aria-hidden="true">*</span>' if req else ' <span class="muted">(optional)</span>'
        return f'<div class="field{" full" if full else ""}"><label for="{id_}">{label}{r}</label>{inp}<span class="field__error" id="{id_}-error" aria-live="polite"></span></div>'
    hidden = "".join(f'<input type="hidden" name="{n}" id="lead-{n.replace(" ", "-").replace("(", "").replace(")", "").lower()}" value="">' for n in ["System", "Home size", "Efficiency", "Zones", "Add-ons", "Estimate shown"])
    sample = '<p class="est-sample" role="note">Demo pricing: the prices on this demo site are samples, set by each heating and cooling company.</p>' if CFG.get("demo_mode") else ""
    cfg_js = {k: e[k] for k in ("systems", "home_sizes", "tiers", "addons", "range_pct", "round_to", "minimum_job", "currency", "repair_rule") if k in e}
    rule = e.get("repair_rule") or {}
    repair = ""
    if rule.get("enabled", True):
        repair = f'''<section class="section section--tight rr" aria-labelledby="rr-title"><div class="wrap rr__grid">
<div><p class="eyebrow eyebrow--heat">Got a repair quote?</p><h2 class="display h-lg" id="rr-title" data-reveal="rise">Repair or<br><span class="outline">replace?</span></h2>
<p class="lead mt-1" data-reveal="up">A common rule of thumb: multiply the equipment's age by the repair price. If the result is over ${rule.get("threshold", 5000):,}, replacement is usually worth a look.</p></div>
<div class="rr__tool" data-reveal="up" data-rr data-threshold="{rule.get("threshold", 5000)}">
<div class="rr__fields"><div class="field"><label for="rr-age">Age of the equipment (years)</label><input id="rr-age" type="number" min="0" max="60" inputmode="numeric" placeholder="e.g. 14"></div>
<div class="field"><label for="rr-cost">Repair price ($)</label><input id="rr-cost" type="number" min="0" step="10" inputmode="numeric" placeholder="e.g. 650"></div></div>
<div class="rr__meter" aria-hidden="true"><i></i><span class="rr__mark"></span></div>
<p class="rr__out" id="rr-out" role="status" aria-live="polite">Enter the age and repair price to see where you land.</p>
<p class="fine">A rule of thumb, not advice for your specific equipment. Safety issues, such as a cracked heat exchanger, change the answer regardless of the numbers.</p>
</div></div></section>'''
    tool = f'''<section class="est" id="estimator" aria-labelledby="est-tool-title">
<div class="wrap">
<h2 class="visually-hidden" id="est-tool-title">System estimate tool</h2>
<noscript><div class="est-noscript"><p><strong>The instant estimate needs JavaScript.</strong> You can still <a href="{href(here, PATH["contact"])}">request a quote</a> or call <a href="tel:{TEL}">{PHONE}</a>.</p></div></noscript>
<div class="est__grid" data-estimator>
<form class="est__panel" id="est-form" novalidate>
<div class="est-card"><p class="est__step"><b>01</b> What do you need?</p>
<fieldset class="opts opts--sys"><legend class="visually-hidden">System type</legend>{systems}</fieldset>{zones}</div>
<div class="est-card"><p class="est__step"><b>02</b> Your home</p>
<fieldset class="opts opts--size" id="est-size"><legend>Home size (finished living space)</legend>{sizes}</fieldset>
<fieldset class="opts opts--tier"><legend>Efficiency level</legend>{tiers}</fieldset></div>
<div class="est-card" id="est-extras-card"><p class="est__step"><b>03</b> Extras <span class="muted">(optional)</span></p>
<fieldset class="chks"><legend class="visually-hidden">Optional extras</legend>{addons}</fieldset></div>
</form>
<div class="est__side">
<div class="est-result" id="est-result">
<div class="est-result__dial" aria-hidden="true"><svg viewBox="0 0 200 120"><path class="est-dial__track" d="M20 110A80 80 0 0 1 180 110" pathLength="1"/><path class="est-dial__arc" id="est-arc" d="M20 110A80 80 0 0 1 180 110" pathLength="1"/></svg></div>
<p class="est-result__label">Estimated installed price</p>
<p class="est-result__price" aria-live="polite"><span id="est-low">$0</span><i>–</i><span id="est-high">$0</span></p>
<p class="est-result__sum" id="est-sum">—</p>
<p class="fine">Includes the equipment, standard installation, removal of the old equipment and normal venting and connection work. Venting reroutes, ductwork changes, electrical upgrades, permits and difficult access are confirmed after a home visit.</p>
{sample}
<button class="btn btn--primary est-result__go" type="button" id="est-lead-open">Book my home visit {ui("arrow")}</button>
</div>
<form class="form est-lead" id="est-lead" action="{html.escape(CFG["form_endpoint"])}" method="POST" data-validate novalidate hidden>
<p class="est__step"><b>04</b> Send it to us</p>
<p class="form__status" role="alert"></p>
<input type="hidden" name="_subject" value="New instant system estimate — {html.escape(BIZ)} website">
<input type="hidden" name="_next" value="{url_of(PATH["thanks"])}">
<input type="hidden" name="_template" value="table">
{hidden}
<div class="hp" aria-hidden="true"><label for="hp-est">Leave this field empty</label><input class="hp-input" id="hp-est" type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
{fld("lead-name", "Full name", '<input id="lead-name" name="name" type="text" autocomplete="name" required data-label="full name" aria-describedby="lead-name-error">')}
{fld("lead-phone", "Phone", '<input id="lead-phone" name="phone" type="tel" autocomplete="tel" required data-label="phone number" aria-describedby="lead-phone-error">')}
{fld("lead-email", "Email", '<input id="lead-email" name="email" type="email" autocomplete="email" required data-label="email address" aria-describedby="lead-email-error">', full=True)}
{fld("lead-age", "Age of your current system", '<select id="lead-age" name="current system age" aria-describedby="lead-age-error"><option value="">Choose one</option><option>Under 10 years</option><option>10 to 15 years</option><option>15 to 20 years</option><option>Over 20 years</option><option>Not sure / no system</option></select>', req=False, full=True)}
{fld("lead-notes", "Anything we should know?", '<textarea id="lead-notes" name="message" rows="3" aria-describedby="lead-notes-error" placeholder="Rooms that are too hot or cold, timing, rebates you are asking about…"></textarea>', req=False, full=True)}
<p class="form__privacy">We use your details only to follow up on this estimate and book a visit. See our <a href="{href(here, PATH["privacy"])}">Privacy Policy</a>.</p>
<div class="full"><button class="btn btn--primary" type="submit">Send my estimate {ui("arrow")}</button></div>
</form>
</div>
</div>
</div>
<div class="est-live" id="est-live" aria-hidden="true"><div><span class="est-live__k">Your estimate</span><span class="est-live__v" id="est-live-v">—</span></div><a class="btn btn--primary" href="#est-result" tabindex="-1">Details</a></div>
<script type="application/json" id="est-config">{json.dumps(cfg_js).replace("</", "<\\/")}</script>
</section>'''
    explain = f'''<section class="section section--tight"><div class="wrap article">
<div class="prose" data-reveal="up">
<h2>How the instant estimate works</h2>
<p>Each system starts from {html.escape(BIZ)}'s typical installed price for a mid-size home at the standard efficiency level. That price includes the equipment, a standard installation, removal of the old equipment and normal venting and connection work. The tool then adjusts it for your home's size and the efficiency level you choose, adds any extras, and shows the result as a range.</p>
<p>Home size is a stand-in for how much heating and cooling your house needs. The real number depends on insulation, windows, air leakage and layout, which is why equipment is sized properly during the home visit rather than from square footage alone.</p>
<h2>Efficiency levels, explained</h2>
<ul>
<li><strong>Standard</strong> — dependable single-stage equipment that runs at full output whenever it's on.</li>
<li><strong>High efficiency</strong> — two-stage equipment that runs on a lower setting most of the time, which is quieter, more even and cheaper to run.</li>
<li><strong>Premium</strong> — variable-speed or modulating equipment that adjusts in small steps for the steadiest temperatures, strongest humidity control and lowest operating cost.</li>
</ul>
<h2>Why the final price can differ</h2>
<p>Some costs can't be known without seeing the house: new venting routes, chimney liners, gas line changes, electrical panel capacity for heat pumps and air conditioners, ductwork that needs to be modified, condensate pumps, permits and tight access. That's why the estimate is a range and your actual price is confirmed in a written quote after a home visit. Rebate programs change often and aren't included in the estimate. For boilers, water heaters or commercial equipment, <a href="{href(here, PATH["contact"])}">contact us</a> for a quote.</p>
<h2>Instant estimate questions</h2>
{faq_html([
("Is the instant estimate a quote?", "No. It's a ballpark based on the options you choose. Your actual price comes in a written quote after a home visit."),
("Do you see my choices when I use the tool?", "No. The estimate is calculated in your browser, and nothing is sent to us unless you submit the form."),
("Are rebates included?", "No. Rebate and financing programs change often, so we check what's currently available when we quote your system."),
])}
</div>
{aside_html(here)}
</div></section>'''
    content = f'''{page_hero(here, eyebrow="Instant system estimate", h1="Instant System Estimate", lead="Pick the system, your home's size and the efficiency level, and see a ballpark installed price in about a minute. Nothing is sent to us until you choose to.", crumbs=crumbs, ctas=False, mark_icon="gauge", compact=True)}
{tool}
{repair}
{explain}
{cta_band(here, title="Ready for the real number?", text="Book a home visit and we'll confirm the price in a written, itemized quote.")}'''
    scripts = f'<script src="{vasset(here, "js/estimate.js")}" defer></script>'
    schema = [{"@type": "WebApplication", "name": f"{BIZ} Instant System Estimate", "url": url_of(here), "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": e.get("currency", "USD")}, "provider": business_ref()}]
    page(here, title="Instant HVAC Estimate: Furnace, AC & Heat Pump Prices", desc="Get a ballpark installed price for a new furnace, air conditioner, heat pump or ductless system in a minute, plus a quick repair-or-replace check.",
         body=content, active="estimate", crumbs=crumbs, schema=schema, scripts_extra=scripts, body_class="page-estimate")

def build_simple(key, *, title, desc, eyebrow, h1, lead, inner, mark="home", active=None, noindex=False, aside=True, schema=None, cta=True, hero_ctas=True):
    here = PATH[key]
    crumbs = [("Home", PATH["home"]), (h1, None)]
    side = aside_html(here) if aside else ""
    grid = "article" if aside else ""
    content = f'''{page_hero(here, eyebrow=eyebrow, h1=h1, lead=lead, crumbs=crumbs, mark_icon=mark, ctas=hero_ctas)}
<section class="section section--tight"><div class="wrap {grid}"><div class="prose" data-reveal="up">{expand(inner(here), here)}</div>{side}</div></section>
{cta_band(here) if cta else ""}'''
    page(here, title=title, desc=desc, body=content, active=active, crumbs=crumbs, noindex=noindex, schema=schema)

def build_contact():
    here = PATH["contact"]
    crumbs = [("Home", PATH["home"]), ("Contact", None)]
    svc_opts = "".join(f'<option>{s["name"]}</option>' for s in SERVICES) + "<option>Not sure / something else</option>"
    city_opts = "".join(f'<option>{c["name"]}</option>' for c in CITIES) + "<option>Another area</option>"
    def fld(id_, label, inp, req=True, full=False, hint=""):
        r = ' <span class="req" aria-hidden="true">*</span>' if req else ' <span class="muted">(optional)</span>'
        h = f'<span class="field__hint" id="{id_}-hint">{hint}</span>' if hint else ""
        return f'<div class="field{" full" if full else ""}"><label for="{id_}">{label}{r}</label>{inp}{h}<span class="field__error" id="{id_}-error" aria-live="polite"></span></div>'
    form = f'''<form class="form" action="{html.escape(CFG["form_endpoint"])}" method="POST" data-validate novalidate>
<p class="form__status" role="alert"></p>
<input type="hidden" name="_subject" value="New HVAC quote request — {html.escape(BIZ)} website">
<input type="hidden" name="_next" value="{url_of(PATH["thanks"])}">
<input type="hidden" name="_template" value="table">
<div class="hp" aria-hidden="true"><label for="hp-field">Leave this field empty</label><input class="hp-input" id="hp-field" type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
{fld("name", "Full name", '<input id="name" name="name" type="text" autocomplete="name" required data-label="full name" aria-describedby="name-error">')}
{fld("phone", "Phone", '<input id="phone" name="phone" type="tel" autocomplete="tel" required data-label="phone number" aria-describedby="phone-error">')}
{fld("email", "Email", '<input id="email" name="email" type="email" autocomplete="email" required data-label="email address" aria-describedby="email-error">')}
{fld("city", "Property location", f'<select id="city" name="city" required data-label="property location" aria-describedby="city-error"><option value="">Select an area</option>{city_opts}</select>')}
{fld("service", "What do you need?", f'<select id="service" name="service" required data-label="type of work" aria-describedby="service-error"><option value="">Select a service</option>{svc_opts}</select>')}
{fld("urgency", "How soon?", '<select id="urgency" name="urgency" aria-describedby="urgency-error"><option value="">Choose one</option><option>No heat or no cooling right now</option><option>Within the next few weeks</option><option>Planning ahead</option></select>', req=False)}
{fld("message", "Tell us about your system", '<textarea id="message" name="message" required data-label="system details" aria-describedby="message-hint message-error"></textarea>', full=True, hint="What's happening, the type and rough age of your equipment, and when you'd like the work done.")}
<p class="form__privacy">We use the information you submit only to respond to your request and prepare a quote. See our <a href="{href(here, PATH["privacy"])}">Privacy Policy</a>.</p>
<div class="full"><button class="btn btn--primary" type="submit">Send request {ui("arrow")}</button></div>
</form>'''
    hours = "<br>".join(hours_text())
    est_tip = (f'<div class="aside-card aside-card--est mt-2"><p class="mono accent">Want a number first?</p><h2>Instant estimate</h2><p>See a ballpark installed price for a new system before you send anything.</p><a class="btn btn--ghost" href="{href(here, PATH["estimate"])}">{ui("gauge")} Start my estimate</a></div>' if EST_ON else "")
    content = f'''{page_hero(here, eyebrow="Contact", h1="Get a Heating & Cooling Quote", lead="Tell us what's going on with your heating or cooling. We'll follow up to book a visit and give you a written, itemized quote.", crumbs=crumbs, ctas=False, mark_icon="thermostat")}
<section class="section section--tight"><div class="wrap contact-grid">
<div class="contact-panel" data-reveal="up"><h2 class="display h-md" style="margin-bottom:24px">Your system</h2>{form}</div>
<div data-reveal="up"><ul class="info-list">
<li><span>Call</span><a href="tel:{TEL}">{PHONE}</a></li>
<li><span>Email</span><a class="info-list__email" href="mailto:{CFG["email"]}">{CFG["email"]}</a></li>
<li><span>Hours</span><p style="margin:0">{hours}<br><span class="muted">{CFG.get("hours_note","")}</span></p></li>
<li><span>Service area</span><p style="margin:0">{" · ".join(f'<a class="info-list__link" href="{href(here, city_path(c["slug"]))}">{c["name"]}</a>' for c in CITIES)}</p></li>
</ul>
<p class="gas-note">{ui("flame")}<span><strong>Smell gas?</strong> Don't use the form. Leave the building and call your gas utility's emergency line from outside.</span></p>
<div class="prose mt-2"><h2 class="h-sm">What happens next</h2><ol><li><strong>We review your request</strong> and follow up by phone or email.</li><li><strong>Home visit.</strong> We look at your equipment, venting and ductwork, and talk through any comfort problems.</li><li><strong>Written quote.</strong> You receive an itemized quote to review on your own time.</li></ol></div>
{est_tip}
</div>
</div></section>'''
    schema = [{"@type": "ContactPage", "url": url_of(here), "name": f"Contact {BIZ}", "about": {"@id": DOMAIN + "/#business"}}]
    page(here, title="Contact & HVAC Quote", desc=f"Request a heating and cooling quote from {BIZ}. Call {PHONE} or send details about your furnace, air conditioner, heat pump or repair.", body=content, active="contact", crumbs=crumbs, schema=schema)

def build_404():
    here = "404.html"
    global href, asset
    rel_href, rel_asset = href, asset
    def abs_href(_from, to):
        if to == "index.html": return BASE
        if to.endswith("index.html"): return BASE + to[:-len("index.html")]
        return BASE + to
    href = abs_href
    asset = lambda _f, a: BASE + "assets/" + a  # vasset() builds on asset(), so the 404 gets root-based versioned URLs
    links = "".join(f'<li><a href="{abs_href(None, svc_path(s["slug"]))}">{s["name"]}</a></li>' for s in SERVICES[:10])
    content = f'''<section class="notfound"><div class="wrap">
<p class="notfound__code" aria-hidden="true">404</p>
<h1 class="display h-lg mt-1">This page went cold.</h1>
<p class="lead mt-1">The page you're looking for may have moved or no longer exists. Try one of these instead:</p>
<div class="btn-row mt-2"><a class="btn btn--primary" href="{BASE}">Back to home {ui("arrow")}</a><a class="btn btn--ghost" href="{abs_href(None, PATH["services"])}">All services</a><a class="btn btn--ghost" href="{abs_href(None, PATH["contact"])}">Contact us</a></div>
<div class="prose mt-3"><h2 class="h-sm">Popular services</h2><ul style="columns:2;max-width:640px">{links}</ul></div>
</div></section>'''
    page(here, title="Page Not Found", desc="The page you're looking for couldn't be found.", body=content, noindex=True)
    href, asset = rel_href, rel_asset

def write_sitemap_robots():
    urls = [p for p in PAGES if p["url"] and not p["noindex"]]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"  <url><loc>{html.escape(p['url'])}</loc></url>" for p in urls]
    xml.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    return len(urls)

def write_cname():
    host = re.sub(r"^https?://", "", DOMAIN).strip("/")
    cname = os.path.join(ROOT, "CNAME")
    if "example.com" in host or host.endswith(".pages.dev"):
        if os.path.exists(cname): os.remove(cname)
        return None
    open(cname, "w").write(host + "\n")
    return host

def main():
    import shutil
    for d in ("services", "service-areas", "system-estimate"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    prep_logo()
    PH.process(PHOTOS, ROOT)
    PH.ensure_css(os.path.join(ROOT, "assets", "css", "main.css"))
    try:
        import runpy
        runpy.run_path(os.path.join(HERE, "make_images.py"), run_name="__main__")
    except ImportError as e:
        print(f"WARNING: brand images not regenerated ({e}). pip install pillow fonttools brotli")
    build_home()
    build_estimate()
    build_services_hub()
    for s in SERVICES:
        build_service(s)
        for c in CITIES:
            build_service_city(s, c)
    build_areas_hub()
    for c in CITIES:
        build_city_hub(c)
    for key, spec in P.simple_pages(CFG, CITIES, SERVICES, city_list_text(), ALL_OFFERED).items():
        build_simple(key, **spec)
    build_contact()
    build_404()
    n = write_sitemap_robots()
    host = write_cname()
    json.dump([{"path": p["path"], "url": p["url"], "title": p["title"], "indexable": bool(p["url"]) and not p["noindex"]} for p in PAGES],
              open(os.path.join(HERE, "page-inventory.json"), "w"), indent=1)
    print(f"Built {len(PAGES)} pages, {n} URLs in sitemap.xml. CNAME: {host or 'not written (demo or example domain)'}")
    if CFG.get("demo_mode"):
        print("WARNING: demo_mode is ON. Every page has noindex and the demo banner. Set demo_mode to false at launch.")
    review = os.path.join(HERE, "removed-service-mentions.txt")
    if REMOVED_MENTIONS:
        with open(review, "w", encoding="utf-8") as f:
            f.write("Sentences that mention services this client does NOT offer. The links were turned into plain text,\n"
                    "but the wording may still imply the service is offered. Reword or remove each one in _build/content_*.py\n"
                    "or _build/pages.py, then rebuild until this file is gone.\n\n")
            for sent, names in sorted(REMOVED_MENTIONS.items()):
                f.write(f"- [{', '.join(sorted(names))}] {sent}\n")
        print(f"CLIENT REVIEW: {len(REMOVED_MENTIONS)} sentence(s) mention services this client does not offer. See _build/removed-service-mentions.txt")
    elif os.path.exists(review):
        os.remove(review)
    if not LOGO_FILE:
        print("CLIENT INPUT NEEDED: no client logo file (config 'logo'); the built-in mark and business name are used.")
    if not PHOTOS:
        print("CLIENT INPUT NEEDED: no work photos (config 'photos'); photo sections are hidden.")
    for k in ["domain", "phone_display", "email", "form_endpoint"]:
        if "example" in str(CFG[k]) or "555-01" in str(CFG[k]):
            print(f"WARNING: {k} still has a sample value: {CFG[k]}")
    if EST_ON:
        print("Instant estimate: " + ", ".join(f'{x["label"]} ${x["base"]:,}' for x in EST["systems"]) + f" (±{EST['range_pct']}%)."
              + (" CLIENT INPUT NEEDED: set the client's real installed prices." if CFG.get("demo_mode") else ""))
    if H24:
        print("CLIENT REVIEW: emergency_24_7 is ON. Confirm the client really answers no-heat calls around the clock.")

if __name__ == "__main__":
    main()
