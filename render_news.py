#!/usr/bin/env python3
"""Render the news-image-20261126 front page: one day of world news,
Thursday 26 November 2026, as a newspaper front page, 1024x1024.

Drawn with Pillow primitives only (no photos, no network, no AI image):
flat editorial artwork, every headline fitted so nothing is truncated.
Deterministic: same input always writes the same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 240, 230)
INK = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (179, 35, 27)
GREY = (110, 105, 95)
RULE = (60, 58, 52)

FDIR = "/usr/share/fonts/truetype"
SERIF = os.path.join(FDIR, "liberation/LiberationSerif-Regular.ttf")
SERIF_B = os.path.join(FDIR, "liberation/LiberationSerif-Bold.ttf")
SANS = os.path.join(FDIR, "liberation/LiberationSans-Regular.ttf")
SANS_B = os.path.join(FDIR, "liberation/LiberationSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, fnt, width, max_lines):
    """Wrap text; True when it fits within max_lines at this font size."""
    return wrap(text, fnt, width), len(wrap(text, fnt, width)) <= max_lines


WARNINGS = []


def draw_fitted(d, xy, text, path, size, width, max_lines, fill=INK,
                min_size=9, leading=1.18, tag=""):
    """Draw wrapped text, shrinking the font until it fits. Warns if it
    still does not fit at min_size, so copy can be shortened by hand."""
    x, y = xy
    sz = size
    while sz > min_size:
        fnt = font(path, sz)
        lines = wrap(text, fnt, width)
        if len(lines) <= max_lines:
            break
        sz -= 1
    fnt = font(path, sz)
    lines = wrap(text, fnt, width)
    if len(lines) > max_lines:
        WARNINGS.append(f"OVERFLOW {tag}: {text!r} needs {len(lines)} lines, "
                        f"max {max_lines} at {sz}pt")
        lines = lines[:max_lines]
    lh = int(sz * leading)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- stories
# Headlines are written short on purpose: card headlines <= ~44 chars,
# summaries <= ~60 chars, so each fits its box whole. Never truncate.
LEADS = [
    dict(tag="MARKETS", place="SEOUL", color=(20, 83, 45),
         head="Bank of Korea lifts rate to 3.25%",
         summ="Third hike of 2026 as chip exports boom; growth "
              "forecast up to 3.9%.",
         kind="bars", src="Reuters", st="OFFICIAL"),
    dict(tag="CONFLICT", place="KUWAIT", color=(140, 29, 24),
         head="Iran drone attack kills two Italians",
         summ="Two Rheinmetall technicians dead; Rome and Kuwait "
              "confirm.",
         kind="missile", src="Reuters", st="CONFIRMED"),
    dict(tag="CONFLICT", place="BAGHDAD", color=(140, 29, 24),
         head="Baghdad takes Kurd oil; thousands protest",
         summ="Federal troops hold crossings and oil fields.",
         kind="gate", src="AP", st="CONFIRMED"),
]

GRID = [
    ("TRANSPORT", "OSLO", (91, 70, 54), "jet",
     "Norse Atlantic suspends all flights",
     "Cash-strapped airline seeks funds; bankruptcy looms.",
     "Reuters", "OFFICIAL"),
    ("ENERGY", "KHASAB", (179, 84, 30), "ship",
     "Tankers hit mines off Khasab",
     "IRGC says a supertanker with 2m+ barrels was hit.",
     "Reuters", "REPORTED"),
    ("CONFLICT", "KYIV", (140, 29, 24), "jet",
     "Russian missiles hit Kyiv mall",
     "Seven hurt, two serious, in overnight strikes.",
     "Reuters", "CONFIRMED"),
    ("TECH", "SANTA CLARA", (74, 44, 109), "chip",
     "Nvidia halts AI server shipments",
     "Halts AI server sales to four Asian states.",
     "FT", "CONFIRMED"),
    ("MARKETS", "DUBAI", (20, 83, 45), "down",
     "Gulf shares muted as war spreads",
     "Aramco up 0.7%; Abu Dhabi, Qatar dip.",
     "Reuters", "CONFIRMED"),
    ("POLITICS", "BRUSSELS", (91, 70, 54), "stars",
     "EU leaders split over \u20ac2tn budget",
     "A \u20ac45bn loan for Ukraine is at stake in Brussels.",
     "Reuters", "REPORTED"),
    ("CONFLICT", "JAZAN", (140, 29, 24), "flame",
     "Houthis hit Aramco's Jazan refinery",
     "Coalition says it destroyed a launch pad.",
     "Reuters", "REPORTED"),
    ("HEALTH", "HAITI", (14, 107, 107), "cross",
     "4.9m Haitians need health aid",
     "WHO: only a quarter of clinics fully open.",
     "WHO", "OFFICIAL"),
    ("TRANSPORT", "LONDON", (91, 70, 54), "train",
     "London Tube strike halts lines",
     "RMT drivers walk out at noon in a four-day-week row.",
     "Reuters", "OFFICIAL"),
    ("MARKETS", "TOKYO", (20, 83, 45), "bank",
     "Asian shares bounce after Wall St",
     "Nikkei up 1.4%; Kospi gains 1%.",
     "Reuters", "CONFIRMED"),
    ("CONFLICT", "KRASNODAR", (140, 29, 24), "drone",
     "Drones set Russian refinery ablaze",
     "Distillation unit hit in Nov 26 attack.",
     "Reuters", "REPORTED"),
    ("CONFLICT", "PYONGYANG", (140, 29, 24), "nuke",
     "N. Korea halts missile shipments",
     "Kyiv: KN-23 deliveries to Russia paused.",
     "Reuters", "REPORTED"),
    ("HEALTH", "KINSHASA", (14, 107, 107), "virus",
     "Ebola cases pass 12,000 in DR Congo",
     "The worst outbreak yet; fighting displaces medics.",
     "Reuters", "CONFIRMED"),
    ("CONFLICT", "WEST BANK", (140, 29, 24), "exit",
     "Settlers smash Palestinian homes",
     "Two houses wrecked, defying a court order.",
     "Reuters", "CONFIRMED"),
    ("POLITICS", "BUCHAREST", (91, 70, 54), "flag",
     "Romania charges far-right Simion",
     "Accused of inciting violence at polls.",
     "Reuters", "OFFICIAL"),
    ("POLITICS", "WASHINGTON", (91, 70, 54), "probe",
     "Trump demands GDP data probe",
     "Calls pre-midterm figures 'FAKE'.",
     "Reuters", "OFFICIAL"),
    ("CONFLICT", "GAZA", (140, 29, 24), "burst",
     "IDF kills Hamas finance chief",
     "Khaled Abu Nada dead in Deir al-Balah strike.",
     "Reuters", "CONFIRMED"),
    ("ENERGY", "BANGKOK", (179, 84, 30), "flame",
     "Blast at Bangkok refinery hurts nine",
     "Three critical; production halted.",
     "AP", "CONFIRMED"),
    ("POLITICS", "NAIROBI", (91, 70, 54), "scales",
     "Kenya court halts Ebola facility",
     "US-backed site breached constitution.",
     "Reuters", "OFFICIAL"),
    ("SECURITY", "COLOGNE", (140, 29, 24), "gavel",
     "Germany arrests two over synagogue plot",
     "Iraqis held after 17 raids; Iran link probed.",
     "Reuters", "OFFICIAL"),
    ("UN", "NAIROBI", (91, 70, 54), "people",
     "UN opens housing summit in Nairobi",
     "3.4bn lack decent homes, UN-Habitat says.",
     "UN News", "OFFICIAL"),
    ("LABOUR", "DHAKA", (20, 83, 45), "mega",
     "Bangladesh garment protests flare",
     "Police fire tear gas; 360 factories shut in unrest.",
     "Reuters", "CONFIRMED"),
    ("MIGRATION", "LONDON", (20, 83, 45), "people",
     "UK net migration falls to 77,000",
     "Lowest since 1997 outside the pandemic, figures show.",
     "Reuters", "OFFICIAL"),
    ("POLITICS", "PYONGYANG", (91, 70, 54), "flag",
     "N. Korea expels Swiss envoy",
     "Pyongyang orders the Swiss office to close.",
     "Arirang", "REPORTED"),
]

BRIEF = [
    ("VOTE", "Spain votes Sunday; right leads polls"),
    ("TRADE", "Sea trade stalls, costs climb"),
    ("UN", "UN boosts Ituri Ebola protection"),
    ("CLIMATE", "Early action halves El Niño bill"),
    ("OPEC", "OPEC+ meets Sunday on output"),
    ("GOLD", "Gold eases to $3,566 an ounce"),
    ("MARKETS", "Wall Street shut for Thanksgiving"),
    ("ENERGY", "Lukoil founder breaks sale silence"),
    ("UN", "UN condemns peacekeepers' deaths"),
    ("MARKETS", "S&P futures edge up 0.5%"),
    ("MEMORIAL", "Hong Kong marks year since fire killed 168"),
]

# Key figures of the day, all from the stories above.
STATS = [
    ("3.25%", "BoK rate"),
    ("77,000", "UK net migration"),
    ("12,000+", "Ebola cases"),
    ("360", "factories shut"),
    ("2m+", "barrels on one tanker"),
    ("9", "hurt in Bangkok blast"),
]

# Stories that look like 26 Nov news but are from another day: named here
# so the date scope is explicit.
DATECHECK = ("All 38 stories are from Thursday 26 November 2026. Kept out "
             "as other days: tariffs, Macy's, Cairo fire, Eurostar "
             "\u2014 all 25 Nov.")

# The day in UTC: only events with a verifiable UTC time on 26 Nov make
# the strip. BoK announced ~01:00 GMT (Reuters); the Bangkok blast was
# ~07:45 GMT (BBC: 14:45 local); the ONS figures were published at 09:30
# (ONS release); the Tube strike starts at noon GMT (Reuters). Everything
# else on the page has no solid UTC hour, so the strip stays short rather
# than padded with guesses.
TIMELINE = [
    ("01:00", "BoK lifts rate to 3.25%"),
    ("07:45", "Bangkok refinery blast"),
    ("09:30", "UK net migration 77,000"),
    ("12:00", "Tube strike begins at noon"),
]

# Status tags: OFFICIAL only for an official statement or announcement,
# CONFIRMED where the fact is independently confirmed, REPORTED otherwise.
STATUS_COLORS = {
    "OFFICIAL": (140, 29, 24),
    "CONFIRMED": (20, 83, 45),
    "REPORTED": (91, 70, 54),
}

# Numbered dots on the world map: (lon, lat, number, label).
DOTS = [
    (127, 37, "1", "Seoul"), (48, 29, "2", "Kuwait"),
    (44, 33, "3", "Baghdad"), (100, 14, "4", "Bangkok"),
    (31, 50, "5", "Kyiv"), (0, 51, "6", "London"),
    (15, -4, "7", "Kinshasa"), (90, 24, "8", "Dhaka"),
]

# ---------------------------------------------------------------- icons
# Small white pictograms drawn with primitives on a coloured band.
# Each takes (draw, x, y, s) where (x, y) is the band's top-left and
# s the band height; the pictogram sits in a s x s square at the left.

def _poly(d, pts, fill):
    d.polygon(pts, fill=fill)


def icon_flame(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    _poly(d, [(cx - 9, cy + 10), (cx - 11, cy - 2), (cx - 4, cy - 8),
              (cx - 1, cy - 13), (cx + 3, cy - 6), (cx + 10, cy - 3),
              (cx + 9, cy + 10)], WHITE)


def icon_jet(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    _poly(d, [(cx - 12, cy + 2), (cx + 12, cy - 4), (cx + 12, cy + 4),
              (cx - 12, cy + 6)], WHITE)
    _poly(d, [(cx - 2, cy - 10), (cx + 2, cy - 10), (cx + 1, cy + 2),
              (cx - 3, cy + 2)], WHITE)
    _poly(d, [(cx - 6, cy + 4), (cx - 2, cy + 4), (cx - 1, cy + 11),
              (cx - 7, cy + 11)], WHITE)


def icon_exit(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.rectangle([cx - 11, cy - 9, cx - 7, cy + 9], fill=WHITE)
    _poly(d, [(cx - 6, cy - 4), (cx + 6, cy - 4), (cx + 6, cy + 4),
              (cx - 6, cy + 4)], WHITE)
    _poly(d, [(cx + 6, cy - 8), (cx + 12, cy), (cx + 6, cy + 8)], WHITE)


def icon_down(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.line([cx - 11, cy + 10, cx - 11, cy - 10], fill=WHITE, width=2)
    d.line([cx - 11, cy + 10, cx + 12, cy + 10], fill=WHITE, width=2)
    d.line([cx - 11, cy - 8, cx - 3, cy - 1, cx + 3, cy - 5, cx + 11, cy + 7],
           fill=WHITE, width=3)


def icon_gavel(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.line([cx - 10, cy + 10, cx + 10, cy - 10], fill=WHITE, width=3)
    d.rectangle([cx - 12, cy - 8, cx - 2, cy - 1], fill=WHITE)
    d.rectangle([cx + 2, cy + 1, cx + 12, cy + 8], fill=WHITE)


def icon_sat(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.rectangle([cx - 12, cy - 4, cx - 5, cy + 4], outline=WHITE, width=2)
    d.rectangle([cx + 5, cy - 4, cx + 12, cy + 4], outline=WHITE, width=2)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=WHITE)


def icon_astro(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 7, cy - 12, cx + 7, cy + 2], outline=WHITE, width=2)
    d.ellipse([cx - 4, cy - 9, cx + 4, cy - 1], fill=WHITE)
    _poly(d, [(cx - 9, cy + 3), (cx + 9, cy + 3), (cx + 6, cy + 12),
              (cx - 6, cy + 12)], WHITE)


def icon_stars(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    for k in range(8):
        import math
        a = math.pi * 2 * k / 8 - math.pi / 2
        px, py = cx + 10 * math.cos(a), cy + 10 * math.sin(a)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=WHITE)


def icon_nuke(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=WHITE, width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=WHITE)
    for a0 in (200, 320, 80):
        d.pieslice([cx - 11, cy - 11, cx + 11, cy + 11], a0, a0 + 60,
                   fill=WHITE)


def icon_virus(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    import math
    for k in range(8):
        a = math.pi * 2 * k / 8
        d.line([cx + 6 * math.cos(a), cy + 6 * math.sin(a),
                cx + 12 * math.cos(a), cy + 12 * math.sin(a)],
               fill=WHITE, width=2)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=WHITE)


def icon_scales(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.line([cx, cy - 11, cx, cy + 11], fill=WHITE, width=2)
    d.line([cx - 11, cy - 8, cx + 11, cy - 8], fill=WHITE, width=2)
    _poly(d, [(cx - 12, cy - 8), (cx - 8, cy + 1), (cx - 16, cy + 1)], WHITE)
    _poly(d, [(cx + 12, cy - 8), (cx + 8, cy + 1), (cx + 16, cy + 1)], WHITE)


def icon_burst(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    import math
    pts = []
    for k in range(16):
        r = 12 if k % 2 == 0 else 5
        a = math.pi * 2 * k / 16
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=WHITE)


def icon_chip(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.rectangle([cx - 7, cy - 7, cx + 7, cy + 7], outline=WHITE, width=2)
    d.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], fill=WHITE)
    for dx in (-5, 0, 5):
        d.line([cx + dx, cy - 12, cx + dx, cy - 7], fill=WHITE, width=2)
        d.line([cx + dx, cy + 7, cx + dx, cy + 12], fill=WHITE, width=2)
    for dy in (-5, 0, 5):
        d.line([cx - 12, cy + dy, cx - 7, cy + dy], fill=WHITE, width=2)
        d.line([cx + 7, cy + dy, cx + 12, cy + dy], fill=WHITE, width=2)


def icon_bolt(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    _poly(d, [(cx + 3, cy - 12), (cx - 7, cy + 1), (cx - 1, cy + 1),
              (cx - 3, cy + 12), (cx + 7, cy - 1), (cx + 1, cy - 1)],
          WHITE)


def icon_probe(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 8, cy - 11, cx + 4, cy + 1], outline=WHITE, width=2)
    d.line([cx + 2, cy - 1, cx + 11, cy + 11], fill=WHITE, width=3)


def icon_people(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 11, cy - 10, cx - 5, cy - 4], fill=WHITE)
    d.ellipse([cx + 5, cy - 10, cx + 11, cy - 4], fill=WHITE)
    _poly(d, [(cx - 12, cy + 11), (cx - 4, cy + 11), (cx - 5, cy - 2),
              (cx - 11, cy - 2)], WHITE)
    _poly(d, [(cx + 4, cy + 11), (cx + 12, cy + 11), (cx + 11, cy - 2),
              (cx + 5, cy - 2)], WHITE)


def icon_missile(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.line([cx - 11, cy + 11, cx + 11, cy - 11], fill=WHITE, width=2)
    _poly(d, [(cx + 4, cy - 12), (cx + 12, cy - 4), (cx + 7, cy - 2),
              (cx + 2, cy - 7)], WHITE)
    _poly(d, [(cx - 12, cy + 4), (cx - 4, cy + 12), (cx - 2, cy + 7),
              (cx - 7, cy + 2)], WHITE)


def icon_balloon(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 9, cy - 12, cx + 9, cy + 2], fill=WHITE)
    d.line([cx - 6, cy + 2, cx - 4, cy + 10], fill=WHITE, width=2)
    d.line([cx + 6, cy + 2, cx + 4, cy + 10], fill=WHITE, width=2)
    d.rectangle([cx - 5, cy + 10, cx + 5, cy + 13], outline=WHITE, width=2)


def icon_bank(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    _poly(d, [(cx - 12, cy - 4), (cx, cy - 12), (cx + 12, cy - 4)], WHITE)
    for dx in (-9, 0, 9):
        d.rectangle([cx + dx - 2, cy - 2, cx + dx + 2, cy + 9], fill=WHITE)
    d.rectangle([cx - 13, cy + 9, cx + 13, cy + 12], fill=WHITE)


def icon_train(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.rectangle([cx - 10, cy - 11, cx + 10, cy + 8], outline=WHITE, width=2)
    d.rectangle([cx - 7, cy - 8, cx - 1, cy - 2], fill=WHITE)
    d.rectangle([cx + 1, cy - 8, cx + 7, cy - 2], fill=WHITE)
    d.ellipse([cx - 8, cy + 7, cx - 3, cy + 12], fill=WHITE)
    d.ellipse([cx + 3, cy + 7, cx + 8, cy + 12], fill=WHITE)


def icon_ship(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    _poly(d, [(cx - 12, cy + 2), (cx + 12, cy + 2), (cx + 8, cy + 11),
              (cx - 8, cy + 11)], WHITE)
    d.rectangle([cx - 9, cy - 7, cx - 2, cy + 1], fill=WHITE)
    d.rectangle([cx, cy - 7, cx + 7, cy + 1], fill=WHITE)
    d.rectangle([cx + 8, cy - 11, cx + 11, cy + 1], fill=WHITE)


def icon_rock(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=WHITE)
    d.ellipse([cx - 5, cy - 7, cx + 3, cy + 1], outline=INK, width=2)
    d.ellipse([cx + 2, cy + 3, cx + 8, cy + 9], outline=INK, width=2)


def icon_mega(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    _poly(d, [(cx - 11, cy - 4), (cx + 2, cy - 11), (cx + 2, cy + 9),
              (cx - 11, cy + 3)], WHITE)
    d.polygon([(cx + 2, cy - 11), (cx + 12, cy - 6), (cx + 12, cy + 4),
               (cx + 2, cy + 9)], outline=WHITE, width=2)
    d.rectangle([cx - 5, cy + 6, cx - 1, cy + 12], fill=WHITE)


def icon_cross(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.rectangle([cx - 3, cy - 12, cx + 3, cy + 12], fill=WHITE)
    d.rectangle([cx - 12, cy - 3, cx + 12, cy + 3], fill=WHITE)


def icon_flag(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.line([cx - 8, cy - 12, cx - 8, cy + 12], fill=WHITE, width=2)
    _poly(d, [(cx - 8, cy - 12), (cx + 11, cy - 8), (cx - 8, cy - 3)],
          WHITE)


def icon_gate(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.rectangle([cx - 12, cy - 11, cx - 9, cy + 11], fill=WHITE)
    d.rectangle([cx + 9, cy - 11, cx + 12, cy + 11], fill=WHITE)
    d.rectangle([cx - 12, cy - 8, cx + 12, cy - 5], fill=WHITE)
    d.rectangle([cx - 12, cy + 5, cx + 12, cy + 8], fill=WHITE)


def icon_drone(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 5, cy - 3, cx + 5, cy + 3], fill=WHITE)
    for dx, dy in ((-10, -8), (10, -8), (-10, 8), (10, 8)):
        d.ellipse([cx + dx - 4, cy + dy - 2, cx + dx + 4, cy + dy + 2],
                  outline=WHITE, width=2)
        d.line([cx, cy, cx + dx, cy + dy], fill=WHITE, width=2)


ICONS = dict(flame=icon_flame, jet=icon_jet, exit=icon_exit, down=icon_down,
             gavel=icon_gavel, sat=icon_sat, astro=icon_astro,
             stars=icon_stars, nuke=icon_nuke, virus=icon_virus,
             scales=icon_scales, burst=icon_burst, chip=icon_chip,
             bolt=icon_bolt, probe=icon_probe, people=icon_people,
             missile=icon_missile, balloon=icon_balloon, bank=icon_bank,
             train=icon_train, ship=icon_ship, rock=icon_rock,
             mega=icon_mega, cross=icon_cross, flag=icon_flag,
             gate=icon_gate, drone=icon_drone)


# ---------------------------------------------------------------- map
# Rough continent outlines in (lon, lat); equirectangular projection.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-145, 60), (-168, 66)],
    [(-45, 60), (-30, 68), (-20, 70), (-30, 76), (-55, 76), (-58, 70),
     (-45, 60)],
    [(-80, 9), (-75, 11), (-62, 9), (-52, 5), (-35, -8), (-40, -22),
     (-48, -28), (-58, -35), (-65, -41), (-70, -54), (-73, -37),
     (-80, -20), (-81, -5), (-80, 9)],
    [(-17, 15), (-10, 31), (0, 36), (10, 37), (20, 32), (32, 31),
     (35, 28), (43, 12), (51, 11), (48, 2), (40, -10), (35, -18),
     (28, -33), (18, -35), (12, -18), (9, 4), (-8, 5), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (18, 56),
     (21, 55), (24, 59), (30, 60), (30, 70), (45, 68), (60, 70), (70, 73),
     (90, 75), (110, 74), (130, 72), (150, 70), (170, 66), (178, 65),
     (162, 60), (158, 52), (142, 50), (140, 40), (130, 33), (122, 30),
     (110, 20), (105, 9), (100, 8), (95, 16), (90, 22), (80, 8), (77, 8),
     (72, 20), (66, 25), (60, 25), (56, 27), (52, 29), (48, 30), (43, 29),
     (39, 21), (35, 28), (30, 36), (22, 36), (18, 40), (12, 44), (3, 43),
     (-2, 37), (-10, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
     (137, -35), (140, -38), (147, -39), (150, -37), (153, -27),
     (153, -24), (146, -19), (142, -11), (136, -12), (132, -11),
     (126, -14), (122, -17), (113, -22)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-5, 50)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41), (143, 43),
     (140, 39), (136, 37), (132, 33), (130, 31)],
]

# ---------------------------------------------------------------- layout

def draw_masthead(d):
    d.rectangle([24, 14, 1000, 16], fill=INK)
    title = "THE DAILY GLOBE"
    fnt = font(SERIF_B, 50)
    tw = fnt.getlength(title)
    d.text(((W - tw) / 2, 20), title, font=fnt, fill=INK)
    sub = "THURSDAY, 26 NOVEMBER 2026  \u2022  THE WORLD IN ONE DAY  \u2022  38 STORIES"
    fnt2 = font(SANS_B, 17)
    tw2 = fnt2.getlength(sub)
    d.text(((W - tw2) / 2, 76), sub, font=fnt2, fill=RED)
    d.rectangle([24, 96, 1000, 100], fill=INK)
    d.rectangle([24, 102, 1000, 103], fill=INK)


def draw_bar_chart(d, x, y, w, h, data, base=0.0, color=(20, 83, 45)):
    """Mini bar chart; `data` is [(label, value), ...]. Bars rise from
    `base` (a truncated axis — the value labels carry the real numbers),
    centred in the visual."""
    mx = max(v for _, v in data)
    bw = 52
    gap = 26
    total = len(data) * bw + (len(data) - 1) * gap
    x0 = x + (w - total) // 2
    base_y = y + h - 22
    fnt = font(SANS_B, 11)
    for i, (label, val) in enumerate(data):
        bx = x0 + i * (bw + gap)
        bh = int((h - 40) * (val - base) / (mx - base))
        d.rectangle([bx, base_y - bh, bx + bw, base_y], fill=color)
        d.text((bx, base_y - bh - 15), f"{val:.2f}%", font=fnt, fill=INK)
        d.text((bx - 4, base_y + 4), label, font=fnt, fill=GREY)
    d.line([x + 8, base_y, x + w - 8, base_y], fill=INK, width=1)


def draw_lead_visual(d, kind, x, y, w, h):
    if kind == "bars":
        # Bank of Korea rate path: 2.75% (Jul), 3.00% (Aug), 3.25% (Nov),
        # bars from the 2.50% pre-hike level so the steps read clearly.
        draw_bar_chart(d, x, y, w, h,
                       [("JUL", 2.75), ("AUG", 3.00), ("NOV", 3.25)],
                       base=2.50)
        return
    if kind == "gate":
        # Border checkpoint at dusk: posts, striped barrier, flag.
        d.rectangle([x, y, x + w, y + h], fill=(52, 62, 88))
        d.ellipse([x + w - 42, y + 8, x + w - 18, y + 32],
                  fill=(240, 190, 90))
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(30, 32, 40))
        d.rectangle([x + 16, y + 16, x + 22, y + h - 16], fill=(20, 20, 24))
        d.rectangle([x + w - 22, y + 16, x + w - 16, y + h - 16],
                    fill=(20, 20, 24))
        by = y + 24
        seg = (w - 38) // 6
        for i in range(6):
            col = (179, 35, 27) if i % 2 == 0 else WHITE
            d.rectangle([x + 22 + i * seg, by,
                         x + 22 + (i + 1) * seg, by + 8], fill=col)
        d.polygon([(x + 22, y + 16), (x + 42, y + 20), (x + 22, y + 24)],
                  fill=(179, 35, 27))
        return
    if kind == "missile":
        d.rectangle([x, y, x + w, y + h], fill=(16, 28, 48))
        # refinery silhouettes
        for bx, bw, bh in [(0, 26, 34), (30, 18, 48), (52, 30, 28),
                           (86, 16, 56), (106, 24, 36), (134, 20, 44)]:
            d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                        fill=(8, 14, 26))
        d.rectangle([x + 88, y + h - 72, x + 92, y + h - 56], fill=(8, 14, 26))
        # explosion glow + missile trails
        ex, ey = x + w - 52, y + 34
        d.ellipse([ex - 26, ey - 26, ex + 26, ey + 26], fill=(214, 120, 30))
        d.ellipse([ex - 14, ey - 14, ex + 14, ey + 14], fill=(240, 190, 80))
        d.line([x + 12, y + h - 8, ex - 8, ey + 10], fill=WHITE, width=2)
        d.line([x + 60, y + h - 4, ex - 20, ey + 16], fill=WHITE, width=2)
        return



def status_pill_width(st):
    return int(font(SANS_B, 8).getlength(st)) + 10


def draw_status_pill(d, st, x, y):
    """Small white-on-dark status chip; x, y = top-left of the pill."""
    fnt = font(SANS_B, 8)
    pw = status_pill_width(st)
    d.rounded_rectangle([x, y, x + pw, y + 13], radius=6,
                        fill=STATUS_COLORS[st])
    tw = fnt.getlength(st)
    d.text((x + (pw - tw) / 2, y + 2), st, font=fnt, fill=WHITE)
    return pw


def draw_tagline(d, tx, ty, tw, tag, place, color, src, tag_size=10,
                 src_size=9):
    """Tag + place left, source right-aligned, one line."""
    d.text((tx, ty), f"{tag} \u2022 {place}", font=font(SANS_B, tag_size),
           fill=color)
    if src:
        fnt = font(SANS, src_size)
        sw = fnt.getlength(src)
        d.text((tx + tw - sw, ty), src, font=fnt, fill=GREY)


def draw_lead(d, lead, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RULE, width=1)
    vh = 72 if lead["kind"] == "bars" else 60
    draw_lead_visual(d, lead["kind"], x + 1, y + 1, w - 2, vh)
    pw = status_pill_width(lead["st"])
    draw_status_pill(d, lead["st"], x + w - 6 - pw, y + vh - 19)
    ty = y + vh + 8
    draw_tagline(d, x + 10, ty, w - 20, lead["tag"], lead["place"],
                 lead["color"], lead["src"], tag_size=11, src_size=10)
    ty += 16
    ty = draw_fitted(d, (x + 10, ty), lead["head"], SERIF_B, 19, w - 20, 2,
                     tag="lead:" + lead["tag"])
    ty += 4
    draw_fitted(d, (x + 10, ty), lead["summ"], SANS, 11, w - 20, 2,
                tag="lead-summ:" + lead["tag"])


def _shade(color, f):
    return tuple(max(0, min(255, int(c * f))) for c in color)


def _blend(color, f=0.6):
    return tuple(int(c + (255 - c) * f) for c in color)


def draw_mini_scene(d, kind, color, x, y, w, h, st=None):
    """Small drawn scene for a grid card: coloured sky, ground, sun and a
    white pictogram, with a couple of shapes per subject."""
    d.rectangle([x, y, x + w, y + h], fill=color)
    d.ellipse([x + w - 26, y + 8, x + w - 8, y + 26], fill=_blend(color))
    gy = y + h - 20
    d.rectangle([x, gy, x + w, y + h], fill=_shade(color, 0.55))
    d.line([x, gy, x + w, gy], fill=_blend(color, 0.35), width=1)
    if kind == "flame":
        d.ellipse([x + 8, gy - 6, x + w - 8, gy + 10], fill=(230, 140, 40))
    elif kind == "jet":
        d.ellipse([x + 6, y + 12, x + 26, y + 22], fill=_blend(color, 0.7))
        d.ellipse([x + 30, y + 20, x + 52, y + 30], fill=_blend(color, 0.7))
    elif kind == "sat":
        for px, py in [(x + 10, y + 12), (x + 24, y + 8), (x + 44, y + 16)]:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=WHITE)
    elif kind == "astro":
        d.ellipse([x + 6, y + 8, x + w - 6, y + 34], outline=WHITE, width=1)
    elif kind == "ship":
        d.line([x + 6, gy - 8, x + w - 6, gy - 8], fill=WHITE, width=2)
        d.line([x + 10, gy - 4, x + w - 10, gy - 4], fill=WHITE, width=2)
    elif kind in ("burst", "missile"):
        d.ellipse([x + w // 2 - 10, gy - 14, x + w // 2 + 10, gy + 6],
                  fill=(240, 190, 80))
    ICONS[kind](d, x + (w - 40) // 2, y + (h - 40) // 2 - 4, 40)
    if st:
        pw = status_pill_width(st)
        draw_status_pill(d, st, x + (w - pw) // 2, y + h - 16)


def draw_card(d, item, x, y, w, h):
    tag, place, color, kind, head, summ, src, st = item
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RULE, width=1)
    sw = 64
    draw_mini_scene(d, kind, color, x + 1, y + 1, sw, h - 2, st)
    tx = x + sw + 8
    tw = w - sw - 16
    draw_tagline(d, tx, y + 5, tw, tag, place, color, src, tag_size=9,
                 src_size=9)
    ty = draw_fitted(d, (tx, y + 19), head, SERIF_B, 13, tw, 2,
                     tag="card:" + tag)
    draw_fitted(d, (tx, ty + 2), summ, SANS, 10, tw, 2,
                tag="card-summ:" + tag)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RULE, width=1)
    d.text((x + 10, y + 8), "WHERE THE DAY HAPPENED",
           font=font(SANS_B, 12), fill=INK)
    mx, my, mw, mh = x + 8, y + 30, w - 16, h - 62
    # Aspect-preserving equirectangular projection: lon -180..180,
    # lat -55..83, centred in the box so continents keep their shape.
    s = min(mw / 360, mh / 138)
    ox = mx + (mw - 360 * s) / 2
    oy = my + (mh - 138 * s) / 2

    def proj(lon, lat):
        px = ox + (lon + 180) * s
        py = oy + (83 - lat) * s
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly],
                  fill=(207, 200, 180), outline=(138, 130, 114))
    fnt = font(SANS_B, 11)
    for lon, lat, num, _label in DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=WHITE, width=1)
        tw = fnt.getlength(num)
        d.text((px - tw / 2, py - 8), num, font=fnt, fill=WHITE)
    kf = font(SANS, 9)
    for i, kline in enumerate(("1 Seoul  \u2022  2 Kuwait  \u2022  "
                               "3 Baghdad  \u2022  4 Bangkok",
                               "5 Kyiv  \u2022  6 London  \u2022  7 Kinshasa"
                               "  \u2022  8 Dhaka")):
        kw = kf.getlength(kline)
        d.text((x + (w - kw) / 2, y + h - 30 + i * 13), kline, font=kf,
               fill=GREY)


def draw_brief(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RULE, width=1)
    d.text((x + 10, y + 8), "THE DAY IN BRIEF",
           font=font(SANS_B, 12), fill=INK)
    d.line([x + 10, y + 28, x + w - 10, y + 28], fill=RULE, width=1)
    colw = (w - 20) // 2
    for i, (_tag, line) in enumerate(BRIEF):
        col, row = divmod(i, 6)
        bx = x + 10 + col * (colw + 4)
        by = y + 34 + row * 15
        d.text((bx, by), f"{i + 1}.", font=font(SANS_B, 11), fill=RED)
        draw_fitted(d, (bx + 18, by), line, SANS, 11, colw - 22, 1,
                    tag="brief")


def draw_stat_strip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RULE, width=1)
    cw = w // len(STATS)
    for i, (num, label) in enumerate(STATS):
        cx = x + i * cw
        if i:
            d.line([cx, y + 6, cx, y + h - 6], fill=(210, 205, 195), width=1)
        f1 = font(SERIF_B, 19)
        tw = f1.getlength(num)
        d.text((cx + (cw - tw) / 2, y + 3), num, font=f1, fill=RED)
        f2 = font(SANS, 9)
        tw2 = f2.getlength(label)
        d.text((cx + (cw - tw2) / 2, y + 26), label, font=f2, fill=GREY)


def draw_timeline(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RULE, width=1)
    tw_ = 108
    d.text((x + 12, y + 5), "THE DAY", font=font(SANS_B, 11), fill=RED)
    d.text((x + 12, y + 19), "IN UTC", font=font(SANS_B, 11), fill=RED)
    d.line([x + tw_, y + 6, x + tw_, y + h - 6], fill=(210, 205, 195),
           width=1)
    cw = (w - tw_) // len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = x + tw_ + i * cw
        if i:
            d.line([cx, y + 6, cx, y + h - 6], fill=(210, 205, 195),
                   width=1)
        d.text((cx + 12, y + 4), t, font=font(SERIF_B, 13), fill=RED)
        draw_fitted(d, (cx + 12, y + 21), label, SANS, 10, cw - 24, 1,
                    tag="timeline")


def draw_datecheck(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RULE, width=1)
    d.text((x + 10, y + 8), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    d.line([x + 10, y + 28, x + w - 10, y + 28], fill=RULE, width=1)
    draw_fitted(d, (x + 10, y + 34), DATECHECK, SANS, 10, w - 20, 6,
                tag="datecheck")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    # lead band
    draw_lead(d, LEADS[0], 24, 112, 470, 160)
    draw_lead(d, LEADS[1], 502, 112, 238, 160)
    draw_lead(d, LEADS[2], 748, 112, 228, 160)
    # numbers strip
    draw_stat_strip(d, 24, 280, 976, 38)
    # grid: 4 columns x 6 rows, every card illustrated
    cw, ch, gap = 238, 78, 8
    for i, item in enumerate(GRID):
        cx = 24 + (i % 4) * (cw + gap)
        cy = 326 + (i // 4) * (ch + 5)
        draw_card(d, item, cx, cy, cw, ch)
    # the day in UTC
    draw_timeline(d, 24, 825, 976, 37)
    # bottom band: shrunken map, date check, briefs
    draw_map(d, 24, 868, 300, 124)
    draw_datecheck(d, 332, 868, 190, 124)
    draw_brief(d, 530, 868, 470, 124)
    # footer
    foot = ("All events of Thursday 26 November 2026  \u2022  Sources: "
            "Reuters, AP, FT, WHO, UN News, Arirang")
    fnt = font(SANS, 11)
    tw = fnt.getlength(foot)
    d.text(((W - tw) / 2, 1002), foot, font=fnt, fill=GREY)
    return img


def main():
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG")
    size = os.path.getsize(out)
    print(f"wrote {out} {img.size[0]}x{img.size[1]} {size} bytes")
    if WARNINGS:
        print("WARNINGS:")
        for wmsg in WARNINGS:
            print(" -", wmsg)
    else:
        print("no text overflow warnings")
    if size > 1048576:
        print("ERROR: over 1 MiB")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
