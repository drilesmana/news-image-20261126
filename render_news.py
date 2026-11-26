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
    dict(tag="TRADE", place="WASHINGTON", color=(31, 78, 121),
         head="US proposes tariffs on 14 partners",
         summ="China faces up to 40%, India 25%, Japan 15%. Beijing, "
              "Brussels and Delhi reject the plan.",
         kind="tariffs"),
    dict(tag="CONFLICT", place="RIYADH", color=(140, 29, 24),
         head="Missiles over Riyadh; Houthis hit Saudi refinery",
         summ="Air defences down two ballistic missiles; oil climbs "
              "toward $95 a barrel.",
         kind="missile"),
    dict(tag="SOCIETY", place="NEW YORK", color=(90, 70, 40),
         head="Macy's 100th parade put off to Saturday",
         summ="First weather delay in its history as a nor'easter "
              "bears down on New York.",
         kind="balloon"),
]

GRID = [
    ("DISASTER", "CAIRO", (179, 84, 30), "flame",
     "Tanker fire kills 31 on Cairo ring road",
     "A fuel tanker overturned and burned; 21 hurt."),
    ("CONFLICT", "KYIV", (140, 29, 24), "jet",
     "Ukraine hits five jets at Russian airbase",
     "Kyiv says it struck Savasleyka; Russia hit a mall."),
    ("MARKETS", "SEOUL", (20, 83, 45), "bank",
     "Bank of Korea lifts rate to 3.25%",
     "Third hike of 2026; AI export boom fuels growth."),
    ("CONFLICT", "TEHRAN", (140, 29, 24), "exit",
     "US tells citizens to leave Iran",
     "Washington warns of escalation as Israel readies a strike."),
    ("MARKETS", "NEW YORK", (20, 83, 45), "down",
     "Nasdaq nears bear market in AI sell-off",
     "AI stocks slide again; Nvidia falls, S&P warns."),
    ("TRANSPORT", "OSLO", (91, 70, 54), "jet",
     "Norse Atlantic suspends all flights",
     "Cash-strapped airline seeks funds; bankruptcy looms."),
    ("TECH", "BROOKLYN", (74, 44, 109), "gavel",
     "Huawei guilty on 10 of 12 counts",
     "US jury convicts it of trade-secret theft and fraud."),
    ("SPACE", "WASHINGTON", (15, 42, 74), "sat",
     "FCC clears SpaceX plan for 1m satellites",
     "Approval covers orbital data centres; critics object."),
    ("SPACE", "TIANGONG", (15, 42, 74), "astro",
     "First Pakistani astronaut reaches Tiangong",
     "Muhammad Zeeshan Ali is the first foreign national aboard."),
    ("POLITICS", "PYONGYANG", (91, 70, 54), "flag",
     "N. Korea expels Swiss envoy",
     "Pyongyang orders the Swiss office to close."),
    ("POLITICS", "BRUSSELS", (91, 70, 54), "stars",
     "EU leaders split over \u20ac2tn budget",
     "A \u20ac45bn loan for Ukraine is at stake in Brussels."),
    ("CONFLICT", "PYONGYANG", (140, 29, 24), "nuke",
     "Kim vows wider tactical nuclear push",
     "North Korea's leader tours nuclear sites, rejects talks."),
    ("TRANSPORT", "LONDON", (91, 70, 54), "train",
     "London Tube strike halts lines",
     "RMT drivers walk out at noon in a four-day-week row."),
    ("HEALTH", "KINSHASA", (14, 107, 107), "virus",
     "Ebola cases pass 12,000 in DR Congo",
     "The worst outbreak yet; fighting displaces medics."),
    ("POLITICS", "JERUSALEM", (91, 70, 54), "scales",
     "Judges: drop Netanyahu bribery charge",
     "Court urges a rethink; Netanyahu demands an end."),
    ("CONFLICT", "KHARTOUM", (140, 29, 24), "drone",
     "Sudan drone attacks kill 15 in Blue Nile",
     "At least 15 dead in strikes on the restive state."),
    ("CONFLICT", "GAZA", (140, 29, 24), "burst",
     "Gaza strikes kill Hamas security chief",
     "Israeli strikes kill 16 in a day despite ceasefire."),
    ("TECH", "SANTA CLARA", (74, 44, 109), "chip",
     "Huang returns as Nvidia chief",
     "Jensen Huang is back as US lawmakers probe chips."),
    ("ENERGY", "DUBAI", (179, 84, 30), "ship",
     "Explosion near tanker west of Dubai",
     "UKMTO reports a blast; crew safe, vessel undamaged."),
    ("ENERGY", "LONDON", (179, 84, 30), "bolt",
     "UK energy bills to rise 26% in January",
     "Ofgem lifts the cap; a typical bill hits \u00a32,166."),
    ("SPACE", "PARIS", (15, 42, 74), "rock",
     "Hera images show Dimorphos crater",
     "ESA reveals a stadium-sized crater from the DART hit."),
    ("POLITICS", "SHANGHAI", (91, 70, 54), "probe",
     "China probes Shanghai party chief",
     "Chen Jining investigated in a widening graft drive."),
    ("LABOUR", "DHAKA", (20, 83, 45), "mega",
     "Bangladesh garment protests flare",
     "Police fire tear gas; 360 factories shut in unrest."),
    ("MIGRATION", "LONDON", (20, 83, 45), "people",
     "UK net migration falls to 77,000",
     "Lowest since 1997 outside the pandemic, figures show."),
]

BRIEF = [
    ("VOTE", "Spain votes Sunday; right leads polls"),
    ("COURT", "S. Africa court scraps Ramaphosa report"),
    ("FLOOD", "Indonesia mine flood kills 13"),
    ("MEMORIAL", "Hong Kong marks year since fire killed 168"),
    ("RETAIL", "Poundland collapses; 11,000 jobs at risk"),
    ("SPORT", "Liverpool 3\u20130 Club Brugge; Lille stun Bayern"),
    ("CULTURE", "Jennifer Barreto wins Miss Universe 2026"),
    ("MUSIC", "Duran Duran guitarist Andy Taylor dies, 65"),
    ("HEALTH", "Pig-kidney patient a year off dialysis"),
    ("STRIKE", "Iran drone attack on Kuwait kills two"),
    ("BORDER", "Iraq takes over Kurdistan border posts"),
]

# Key figures of the day, all from the stories above.
STATS = [
    ("14", "tariff partners"),
    ("100th", "Macy's parade"),
    ("31", "killed, Cairo fire"),
    ("12,000+", "Ebola cases"),
    ("1m", "satellites cleared"),
    ("77,000", "UK net migration"),
]

# Stories that look like 26 Nov news but are from another day: named here
# so the date scope is explicit.
DATECHECK = ("All 38 stories are from Thursday 26 November 2026. Kept out "
             "as other days: Pitt\u2013Jolie deal, birthright ruling, "
             "Poland no-fly plan, Murmansk sacking \u2014 all 25 Nov.")

# Numbered dots on the world map: (lon, lat, number, label).
DOTS = [
    (-77, 39, "1", "Washington"), (47, 25, "2", "Riyadh"),
    (-74, 41, "3", "New York"), (31, 30, "4", "Cairo"),
    (31, 50, "5", "Kyiv"), (116, 40, "6", "Beijing"),
    (0, 51, "7", "London"), (15, -4, "8", "Kinshasa"),
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
    fnt = font(SERIF_B, 56)
    tw = fnt.getlength(title)
    d.text(((W - tw) / 2, 22), title, font=fnt, fill=INK)
    sub = "THURSDAY, 26 NOVEMBER 2026  \u2022  THE WORLD IN ONE DAY  \u2022  38 STORIES"
    fnt2 = font(SANS_B, 17)
    tw2 = fnt2.getlength(sub)
    d.text(((W - tw2) / 2, 82), sub, font=fnt2, fill=RED)
    d.rectangle([24, 104, 1000, 108], fill=INK)
    d.rectangle([24, 110, 1000, 111], fill=INK)


def draw_bar_chart(d, x, y, w, h):
    """Mini tariff bars: China 40, India 25, Japan 15."""
    data = [("CHINA 40%", 40), ("INDIA 25%", 25), ("JAPAN 15%", 15)]
    bw = 52
    gap = 26
    x0 = x + 14
    base = y + h - 22
    fnt = font(SANS_B, 11)
    for i, (label, val) in enumerate(data):
        bx = x0 + i * (bw + gap)
        bh = int((h - 40) * val / 40)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(31, 78, 121))
        d.text((bx, base - bh - 15), str(val) + "%", font=fnt, fill=INK)
        d.text((bx - 4, base + 4), label, font=fnt, fill=GREY)
    d.line([x + 8, base, x + w - 8, base], fill=INK, width=1)


def draw_lead_visual(d, kind, x, y, w, h):
    if kind == "tariffs":
        draw_bar_chart(d, x, y, w, h)
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
    if kind == "balloon":
        d.rectangle([x, y, x + w, y + h], fill=(120, 140, 165))
        # storm cloud + rain
        d.ellipse([x + 8, y + 6, x + 70, y + 30], fill=(70, 80, 100))
        d.ellipse([x + 40, y + 2, x + 110, y + 28], fill=(85, 95, 115))
        for rx in range(x + 14, x + w - 8, 18):
            d.line([rx, y + 34, rx - 5, y + 52], fill=(230, 235, 240),
                   width=2)
        # big balloon, half-deflated on the street
        d.ellipse([x + w // 2 - 46, y + 34, x + w // 2 + 46, y + h - 6],
                  fill=(179, 35, 27))
        d.ellipse([x + w // 2 - 46, y + 34, x + w // 2 + 46, y + h - 6],
                  outline=(120, 20, 15), width=2)
        d.line([x + w // 2 - 46, y + (34 + h - 6) // 2,
                x + w // 2 + 46, y + (34 + h - 6) // 2],
               fill=(120, 20, 15), width=2)
        return


def draw_lead(d, lead, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RULE, width=1)
    vh = 66 if lead["kind"] != "tariffs" else 78
    draw_lead_visual(d, lead["kind"], x + 1, y + 1, w - 2, vh)
    ty = y + vh + 8
    tag = f"{lead['tag']} \u2022 {lead['place']}"
    d.text((x + 10, ty), tag, font=font(SANS_B, 11), fill=lead["color"])
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


def draw_mini_scene(d, kind, color, x, y, w, h):
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


def draw_card(d, item, x, y, w, h):
    tag, place, color, kind, head, summ = item
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=RULE, width=1)
    sw = 64
    draw_mini_scene(d, kind, color, x + 1, y + 1, sw, h - 2)
    tx = x + sw + 8
    tw = w - sw - 16
    d.text((tx, y + 5), f"{tag} \u2022 {place}", font=font(SANS_B, 10),
           fill=color)
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
    for i, kline in enumerate(("1 Washington  \u2022  2 Riyadh  \u2022  "
                               "3 New York  \u2022  4 Cairo",
                               "5 Kyiv  \u2022  6 Beijing  \u2022  7 London"
                               "  \u2022  8 Kinshasa")):
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
        by = y + 36 + row * 16
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
        f1 = font(SERIF_B, 20)
        tw = f1.getlength(num)
        d.text((cx + (cw - tw) / 2, y + 4), num, font=f1, fill=RED)
        f2 = font(SANS, 10)
        tw2 = f2.getlength(label)
        d.text((cx + (cw - tw2) / 2, y + 28), label, font=f2, fill=GREY)


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
    draw_lead(d, LEADS[0], 24, 116, 470, 172)
    draw_lead(d, LEADS[1], 502, 116, 238, 172)
    draw_lead(d, LEADS[2], 748, 116, 228, 172)
    # numbers strip
    draw_stat_strip(d, 24, 296, 976, 40)
    # grid: 4 columns x 6 rows, every card illustrated
    cw, ch, gap = 238, 80, 8
    for i, item in enumerate(GRID):
        cx = 24 + (i % 4) * (cw + gap)
        cy = 344 + (i // 4) * (ch + 6)
        draw_card(d, item, cx, cy, cw, ch)
    # bottom band: shrunken map, date check, briefs
    draw_map(d, 24, 860, 300, 132)
    draw_datecheck(d, 332, 860, 190, 132)
    draw_brief(d, 530, 860, 470, 132)
    # footer
    foot = ("All events of Thursday 26 November 2026  \u2022  Sources: "
            "Reuters, BBC, AP, AFP, CNBC, Al Jazeera")
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
