# render.py -- news-image-20261126
# Draws "THE WORLD IN ONE DAY -- Thursday 26 November 2026" as a 1024x1024 PNG.
# Every illustration is drawn in code with PIL primitives (flat drawings, no photos).
# Fully deterministic: no randomness, no timestamps, no network.
# Run: python3 render.py  -> writes entry.png next to this file.

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

CREAM = (247, 242, 231)
PAPER = (252, 249, 240)
INK = (26, 26, 26)
RED = (176, 30, 30)
DARKRED = (140, 20, 20)
BLUE = (30, 74, 122)
GREEN = (34, 120, 60)
GREY = (110, 105, 95)
LIGHTGREY = (200, 194, 182)
GOLD = (198, 148, 32)
TEAL = (18, 110, 105)
ORANGE = (214, 110, 30)
SKY = (214, 232, 244)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


def font_lib(name, size):
    return ImageFont.truetype(os.path.join(FL, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font_lib("LiberationSerif-Italic.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS_O = lambda s: font_lib("LiberationSans-Italic.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines of text; returns y after the last line."""
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, fill=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- stories
# (num, headline, body, why-it-matters, source, region)
LEADS = [
    (1, "STORM STOPS THE 100TH PARADE",
     "Nor'easter gusts to 60 mph; 600,000+ lose power, 420+ flights axed, "
     "NY and NJ under emergency.",
     "Thanksgiving without its centrepiece: the storm, not the parade, owned the day.",
     "Reuters", "NA"),
    (2, "KYIV HIT OVERNIGHT",
     "Ballistic missiles + 113 drones (76 jet); 87 downed. Kyiv shopping "
     "centre hit, 7 hurt; 2 killed in Kharkiv.",
     "Jet drones plus ballistic missiles together: Kyiv's air war is getting faster.",
     "Reuters / Ukr. Air Force", "EU"),
    (3, "GULF WAR WIDENS",
     "Riyadh intercepts 2 Houthi missiles; Jazan refinery hit, a Nepali "
     "worker killed; Iranian drones kill 2 Italians.",
     "One day, three Gulf flashpoints: capitals, refineries and foreign workers hit.",
     "Reuters / SPA", "ME"),
]

# (num, headline, body, source, region)
CARDS = [
    (4, "GUKESH-SINDAROV: THIRD DRAW",
     "Game 3 ends in a 60-move draw after Gukesh's Rio de Janeiro surprise; "
     "Sindarov makes move 40 with 6 seconds to spare. Match 1.5-1.5.",
     "Chess.com", "EU"),
    (5, "WORLD ANSWERS US TARIFF PLAN",
     "China, Japan, Vietnam and Singapore object; the EU rejects it; Brazil "
     "denounces a separate aircraft duty. Hearing 25 Jan.",
     "BBC / Reuters", "GLOBAL"),
    (6, "CAIRO TANKER TOLL HITS 31",
     "A fuel tanker overturns on the Ring Road in Warraq; 31 dead, 21+ hurt, "
     "27 vehicles burned. The driver is detained on Thursday.",
     "Egypt Health Min.", "AF"),
    (7, "INDIA MARKS 18 YEARS SINCE 26/11",
     "Mumbai is on high alert as India honours the 166 killed in 2008; "
     "tributes at the Gateway of India and CSMT.",
     "IANS", "AP"),
    (8, "MACKENZIE GUILTY ON ALL COUNTS",
     "Shakahola cult leader convicted of terrorism charges in Mombasa; "
     "already serving 200 years for the murder of 191 people.",
     "Reuters", "AF"),
    (9, "ANDY TAYLOR DIES AT 65",
     "Duran Duran's guitarist dies of prostate cancer; he helped shape the "
     "band's 1980s sound.",
     "BBC", "EU"),
    (10, "BEARS STUN LIONS 39-35",
     "Caleb Williams finds Rome Odunze on the final play; Gibbs runs for "
     "205 yards and 3 TDs in vain. Bears 9-2, top of the NFC North.",
     "AP", "NA"),
    (11, "SECOND JUDGE BLOCKS BIRTHRIGHT ORDER",
     "Trump's newest order curtailing birthright citizenship is blocked by "
     "a second judge.",
     "Reuters", "NA"),
    (12, "UKRAINE HITS SAVASLEYKA BASE",
     "Kyiv says 5 planes are damaged at the Russian airbase; Zelensky warns "
     "Russia is preparing a new massive strike.",
     "Al Jazeera", "EU"),
    (13, "US CLEARS $621.9M F-16 PACKAGE",
     "Maintenance and equipment for Ukraine's F-16s, funded by European "
     "countries, is approved by Washington.",
     "Reuters", "NA"),
]

# (num, one-line headline, source, region)
INDEX = [
    (14, "Ukraine drones hit Nevinnomyssk power plant; fire reported", "h.ua", "EU"),
    (15, "Ukraine hits Marinovka air base in Volgograd with Neptune missiles", "h.ua", "EU"),
    (16, "Ukraine strikes Subkhankulovo oil station in Bashkortostan", "h.ua", "EU"),
    (17, "Ukraine's Blysk laser downs a Geran drone in combat", "h.ua", "EU"),
    (18, "Kyiv council names Gen Biletskyi an honorary citizen of Kyiv", "h.ua", "EU"),
    (19, "Kyiv water firm urges residents to save water after strikes", "h.ua", "EU"),
    (20, "10 killed, 58 hurt across Ukraine in a day, incl. 3 children", "Kyiv Independent", "EU"),
    (21, "General Staff: 167 clashes on 25 Nov; 228 guided bombs fired", "Naga Report", "EU"),
    (22, "Oil rises after Houthis claim attack on a Saudi refinery", "Reuters", "ME"),
    (23, "Coalition says it destroyed the Houthi launcher at Hodeidah [CLAIM]", "Reuters", "ME"),
    (24, "Saudi civil defence lifts the Riyadh danger alert after intercepts", "Reuters", "ME"),
    (25, "Iran FM calls Kuwait deaths 'suspicious... a precooked recipe for war'", "X / Araghchi", "ME"),
    (26, "Kuwait: a Pakistani national and a Kuwaiti captain also hurt", "Reuters", "ME"),
    (27, "Dozens of countries urge Russia to halt alleged riot-agent use", "Reuters", "GLOBAL"),
    (28, "Lebanon to open a second airport next month", "Reuters", "ME"),
    (29, "Ecuador minister: talks with US focus on reviewing operations", "Reuters", "LATAM"),
    (30, "How China got Nvidia AI chips despite US rules: explainer", "Reuters", "AP"),
    (31, "Sen Booker demands Nvidia answers on Huang's return", "Reuters", "NA"),
    (32, "China condemns the US tariff proposals", "Reuters", "AP"),
    (33, "Japan, Vietnam and Singapore object to the US tariff plan", "BBC", "AP"),
    (34, "European Commission rejects the US tariff proposals", "BBC", "EU"),
    (35, "Brazil denounces a separate US duty on Embraer aircraft", "BBC", "LATAM"),
    (36, "US stocks open over 1% lower on the tariff news", "Reuters", "NA"),
    (37, "Sen Wyden vows to use every tool to end the tariffs", "Reuters", "NA"),
    (38, "China goods surplus passes $1 trillion in the first 10 months", "Reuters", "AP"),
    (39, "India makes its case to the IOC for hosting the 2036 Olympics", "Reuters", "AP"),
    (40, "Poland to sign a Palantir defence agreement on Friday", "Reuters", "EU"),
    (41, "Pakistan, Saudi, Turkey to meet in Islamabad, 27-28 Nov", "Reuters", "AP"),
    (42, "Iraq closes two border crossings in Kurdistan with Syria, Iran", "Reuters", "ME"),
    (43, "UN peacekeepers evacuate Ebola workers trapped by Congo fighting", "Reuters", "AF"),
    (44, "Germany's IG Metall reaches a wage deal with employers", "Reuters", "EU"),
    (45, "Turkey aims to meet MSCI requirements by December", "Reuters", "EU"),
    (46, "Petronas targets first-half 2030 start for Suriname gas", "Reuters", "LATAM"),
    (47, "Mexico urges Asian partners to crack down on tariff dodging", "Reuters", "LATAM"),
    (48, "Japan's Nikkei to rise next year but fall short of record: poll", "Reuters", "AP"),
    (49, "Canada student curbs test Carney's push to attract talent", "Reuters", "NA"),
    (50, "Japan data-centre boom faces a revolt from residents", "Reuters", "AP"),
    (51, "US Army declares success in Iowa explosives detonation", "Reuters", "NA"),
    (52, "Lakers avenge their streak-snapping loss to the Jazz", "Reuters", "NA"),
    (53, "Fresh tear-gas clashes as Dhaka garment workers reject 36% rise", "Reuters", "AP"),
    (54, "Knesset advances a bill for an Oct 7 inquiry; 65 vote in favour", "Knesset", "ME"),
    (55, "France, Iran, Argentina send solidarity to India on 26/11", "IANS", "GLOBAL"),
    (56, "President Murmu pays homage to 26/11 victims; Fadnavis at parade", "IANS", "AP"),
    (57, "Gateway of India lit in tricolour for the #NEVEREVER memorial", "TMV", "AP"),
    (58, "Sadanand Date, who fought the 2008 attackers, now Maharashtra police chief", "ITDC India", "AP"),
    (59, "Wu-Tang Clan play halftime at Ford Field as the Bears rally", "Particle", "NA"),
    (60, "Chiefs at Bills closes Thanksgiving night: Mahomes v Allen, 11th meeting", "NFL", "NA"),
]

NUMBERS = [
    ("100th", "Macy's parade postponed, 1st ever"),
    ("113 / 87", "drones launched / downed"),
    ("31 dead", "Cairo tanker fire; 27 vehicles"),
    ("600,000+", "lose power in the storm"),
    ("20%", "top tariff rate proposed - China"),
    ("1.5-1.5", "Gukesh-Sindarov after Game 3"),
]

# Tariff capped rates, % (USTR proposals, via Reuters). Headline rates run to
# 40% for China if the US-China truce fails; 35% for Vietnam if no deal.
CHART = [("China", 20), ("Vietnam", 20), ("SE Asia*", 18),
         ("India", 17), ("Japan+", 15), ("Singap.", 10)]

TIMELINE = [
    ("00:11", "Andy Taylor's death reported"),
    ("06:00", "Ukraine tally: 113 drones, 87 downed"),
    ("06:11", "Riyadh: 2 missiles destroyed"),
    ("07:16", "Mumbai high alert for 26/11"),
    ("10:25", "Reuters: Kyiv hit, 7 hurt"),
    ("14:00", "Chess Game 3 begins, Geneva"),
    ("18:00", "Bears-Lions kick off (13:00 ET)"),
    ("~19:00", "Game 3 drawn, 60 moves"),
    ("21:30", "Bears stun Lions 39-35"),
]

DATE_CHECK = ("NOT 26 NOV - LEFT OUT: COP31 ends with no deal (22-23 Nov) - "
    "Democrats clinch House, 258 seats (23 Nov) - Netanyahu judges urge dropping "
    "the bribery charge (Wed) - Solomon Islands-Australia treaty (Wed) - "
    "Bangladesh wage board sets +36% (Wed) - Rams beat Packers 26-13 (Wed) - "
    "Gukesh-Sindarov Game 2 draw (Wed) - Shenzhou-24 docks (Wed) - Trump: US can "
    "fund the Iran war to Jan (Wed) - FedEx MD-11 off Miami runway (Wed) - "
    "Houthi projectile hits Jazan port (Wed).")

NOT_YET = ("NOT YET HAPPENED: Ukraine's 26-27 Nov overnight drone tally (due "
    "~06:00 UTC Fri) - Eagles-Cowboys and Chiefs-Bills finals - the Macy's parade "
    "itself (Sat 28 Nov, 8:30 ET) - Mackenzie manslaughter ruling (Fri) - US "
    "tariff hearing (25 Jan).")

WATCH = ("WHAT TO WATCH ON FRIDAY (27 NOV): Mackenzie manslaughter ruling - "
    "Poland signs its Palantir defence deal - Pakistan, Saudi, Turkey meet in "
    "Islamabad - Black Friday travel: 42,000+ departures as the storm eases - "
    "first rest day in chess; Game 4 on Saturday.")


# ---------------------------------------------------------------- illustrations
# Each draws a small flat scene into box (x, y, w, h). All coordinates are
# relative to the box; nothing is loaded from disk. No text inside any scene
# except a single symbol where it is part of the drawing.

def ill_storm(d, x, y, w, h):
    # Sagging parade balloon in a grey storm sky, rain slanting, wind lines.
    d.rectangle([x, y, x + w, y + h], fill=(170, 185, 200))
    # rain
    for i in range(14):
        rx = x + w * (0.05 + 0.07 * i)
        ry = y + h * (0.10 + (i % 4) * 0.20)
        d.line([rx, ry, rx - 6, ry + 12], fill=(120, 140, 160), width=2)
    # balloon, half-deflated
    cx, cy = x + w * 0.46, y + h * 0.44
    d.ellipse([cx - 34, cy - 20, cx + 34, cy + 16], fill=(200, 60, 60), outline=INK, width=1)
    d.ellipse([cx - 20, cy - 26, cx + 8, cy - 8], fill=(220, 90, 90))
    d.polygon([(cx - 34, cy + 8), (cx - 44, cy + 18), (cx - 26, cy + 14)], fill=(200, 60, 60), outline=INK)
    d.line([cx - 10, cy + 16, cx - 14, y + h * 0.92], fill=INK, width=1)
    d.line([cx + 10, cy + 16, cx + 14, y + h * 0.92], fill=INK, width=1)
    # wind gusts
    for gy in (0.18, 0.30, 0.78):
        yy = y + h * gy
        d.line([x + w * 0.68, yy, x + w * 0.94, yy], fill=(255, 255, 255), width=2)
        d.line([x + w * 0.88, yy - 4, x + w * 0.94, yy], fill=(255, 255, 255), width=2)
    # street line
    d.line([x, y + h * 0.92, x + w, y + h * 0.92], fill=INK, width=2)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_kyiv(d, x, y, w, h):
    # Night sky, missile trails, shopping-centre block with smoke, shield.
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
    # stars
    for sx, sy in [(0.12, 0.14), (0.30, 0.08), (0.55, 0.12), (0.78, 0.07), (0.90, 0.18)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1], fill=(255, 255, 255))
    # missile trails
    d.line([x + w * 0.15, y + h * 0.10, x + w * 0.38, y + h * 0.55], fill=(255, 180, 60), width=2)
    d.line([x + w * 0.85, y + h * 0.08, x + w * 0.62, y + h * 0.50], fill=(255, 180, 60), width=2)
    d.ellipse([x + w * 0.36, y + h * 0.53, x + w * 0.40, y + h * 0.57], fill=(255, 220, 120))
    d.ellipse([x + w * 0.60, y + h * 0.48, x + w * 0.64, y + h * 0.52], fill=(255, 220, 120))
    # shopping centre block
    d.rectangle([x + w * 0.18, y + h * 0.62, x + w * 0.82, y + h * 0.92], fill=(90, 95, 110), outline=INK)
    for i in range(5):
        wx = x + w * (0.24 + i * 0.11)
        d.rectangle([wx, y + h * 0.68, wx + w * 0.06, y + h * 0.80], fill=(255, 210, 90))
    # smoke
    for sx, sy, sr in [(0.30, 0.55, 10), (0.38, 0.45, 8), (0.68, 0.52, 9), (0.74, 0.42, 7)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr, y + h * sy + sr], fill=(130, 130, 135))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_gulf(d, x, y, w, h):
    # Desert sky, refinery towers with a flame, missile arcs overhead.
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(240, 200, 130))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(120, 95, 60))
    # sun
    d.ellipse([x + w * 0.80, y + h * 0.08, x + w * 0.80 + 18, y + h * 0.08 + 18], fill=(255, 220, 90))
    # missile arcs (dotted)
    for i in range(7):
        t = i / 6.0
        ax = x + w * (0.08 + 0.30 * t)
        ay = y + h * (0.42 - 0.30 * (1 - (2 * t - 1) ** 2))
        d.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=RED)
    for i in range(7):
        t = i / 6.0
        ax = x + w * (0.55 + 0.35 * t)
        ay = y + h * (0.40 - 0.28 * (1 - (2 * t - 1) ** 2))
        d.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=RED)
    # refinery towers
    for tx, th in [(0.14, 0.30), (0.30, 0.40), (0.52, 0.34)]:
        d.rectangle([x + w * tx, y + h * (0.88 - th), x + w * (tx + 0.10), y + h * 0.88], fill=(70, 70, 80))
    # flame on the middle tower
    fx, fy = x + w * 0.35, y + h * 0.44
    d.polygon([(fx, fy - 12), (fx - 8, fy + 4), (fx - 3, fy), (fx + 3, fy + 6), (fx + 8, fy + 4)], fill=ORANGE)
    d.ellipse([fx - 4, fy - 2, fx + 4, fy + 6], fill=(255, 220, 60))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_chess(d, x, y, w, h):
    # Chessboard corner, king and pawn, clock showing little time left.
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 205))
    sq = w * 0.11
    ox, oy = x + w * 0.06, y + h * 0.12
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([ox + c * sq, oy + r * sq, ox + (c + 1) * sq, oy + (r + 1) * sq], fill=(120, 90, 60))
    # white king
    kx, ky = ox + 1.5 * sq, oy + 1.0 * sq
    d.ellipse([kx - 7, ky - 14, kx + 7, ky - 2], fill=(255, 255, 255), outline=INK)
    d.rectangle([kx - 9, ky - 2, kx + 9, ky + 10], fill=(255, 255, 255), outline=INK)
    d.line([kx, ky - 20, kx, ky - 12], fill=INK, width=2)
    d.line([kx - 4, ky - 16, kx + 4, ky - 16], fill=INK, width=2)
    # black pawn
    px, py = ox + 3.0 * sq, oy + 2.6 * sq
    d.ellipse([px - 6, py - 10, px + 6, py - 2], fill=(30, 30, 30))
    d.rectangle([px - 8, py - 2, px + 8, py + 8], fill=(30, 30, 30))
    # clock
    cx, cy = x + w * 0.78, y + h * 0.62
    d.rectangle([cx - 16, cy - 12, cx + 16, cy + 12], fill=(255, 255, 255), outline=INK)
    d.text((cx, cy), "0:06", font=SANS_B(11), fill=RED, anchor="mm")
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_tariffs(d, x, y, w, h):
    # Container ship with a big red percent sign above it.
    d.rectangle([x, y, x + w, y + h], fill=(210, 228, 242))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(60, 110, 170))
    # percent sign
    d.text((x + w * 0.50, y + h * 0.22), "%", font=SANS_B(30), fill=RED, anchor="mm")
    # containers
    cols = [(0.10, RED), (0.26, BLUE), (0.42, GREEN), (0.58, GOLD), (0.74, (90, 90, 110))]
    for cx, col in cols:
        d.rectangle([x + w * cx, y + h * 0.42, x + w * (cx + 0.14), y + h * 0.60], fill=col, outline=INK)
    # hull
    d.polygon([(x + w * 0.06, y + h * 0.60), (x + w * 0.94, y + h * 0.60),
               (x + w * 0.86, y + h * 0.76), (x + w * 0.14, y + h * 0.76)], fill=(40, 40, 48))
    # waves
    for wx in (0.12, 0.40, 0.68, 0.86):
        d.arc([x + w * wx, y + h * 0.82, x + w * (wx + 0.10), y + h * 0.94], 180, 360, fill=(255, 255, 255), width=2)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_tanker(d, x, y, w, h):
    # Overturned tanker on a highway, flames and black smoke.
    d.rectangle([x, y, x + w, y + h * 0.60], fill=(235, 225, 200))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(90, 90, 95))
    # road line
    d.line([x, y + h * 0.80, x + w, y + h * 0.80], fill=(255, 255, 255), width=2)
    # overturned tanker (on its side)
    tx, ty = x + w * 0.16, y + h * 0.52
    d.ellipse([tx, ty - 12, tx + w * 0.52, ty + 12], fill=(200, 200, 205), outline=INK)
    d.ellipse([tx + w * 0.52, ty - 8, tx + w * 0.62, ty + 8], fill=(60, 60, 66), outline=INK)
    d.ellipse([tx + w * 0.18, ty + 4, tx + w * 0.18 + 8, ty + 12], fill=INK)
    d.ellipse([tx + w * 0.34, ty + 4, tx + w * 0.34 + 8, ty + 12], fill=INK)
    # flames
    for fx, fh in [(0.62, 0.30), (0.72, 0.42), (0.84, 0.30)]:
        px = x + w * fx
        py = y + h * 0.60
        d.polygon([(px, py - h * fh), (px - 9, py), (px - 3, py - 6), (px + 3, py), (px + 9, py)], fill=ORANGE)
    # smoke
    for sx, sy, sr in [(0.68, 0.22, 11), (0.78, 0.14, 9), (0.86, 0.26, 8)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr, y + h * sy + sr], fill=(60, 60, 60))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_mumbai(d, x, y, w, h):
    # Gateway arch at dusk, candles in front.
    d.rectangle([x, y, x + w, y + h * 0.62], fill=(250, 190, 120))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(90, 70, 60))
    # arch
    ax = x + w * 0.50
    d.rectangle([ax - 26, y + h * 0.22, ax + 26, y + h * 0.78], fill=(180, 150, 110), outline=INK)
    d.pieslice([ax - 18, y + h * 0.30, ax + 18, y + h * 0.66], 180, 360, fill=(250, 190, 120))
    d.rectangle([ax - 30, y + h * 0.18, ax + 30, y + h * 0.26], fill=(180, 150, 110), outline=INK)
    d.rectangle([ax - 10, y + h * 0.10, ax + 10, y + h * 0.18], fill=(180, 150, 110), outline=INK)
    # candles
    for cx in (0.22, 0.34, 0.66, 0.78):
        px = x + w * cx
        d.rectangle([px - 3, y + h * 0.84, px + 3, y + h * 0.96], fill=(255, 255, 255), outline=INK)
        d.ellipse([px - 2, y + h * 0.80, px + 2, y + h * 0.85], fill=(255, 200, 40))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_court(d, x, y, w, h):
    # Courtroom: bench, gavel, bars.
    d.rectangle([x, y, x + w, y + h], fill=(225, 215, 190))
    # bars
    for bx in (0.10, 0.24, 0.38):
        d.rectangle([x + w * bx, y, x + w * (bx + 0.04), y + h], fill=(70, 70, 75))
    # bench
    d.rectangle([x + w * 0.50, y + h * 0.55, x + w * 0.94, y + h * 0.92], fill=(110, 80, 50))
    d.rectangle([x + w * 0.50, y + h * 0.50, x + w * 0.94, y + h * 0.55], fill=(140, 105, 65))
    # gavel
    gx, gy = x + w * 0.72, y + h * 0.34
    d.rectangle([gx - 16, gy - 6, gx + 16, gy + 6], fill=(90, 60, 30), outline=INK)
    d.line([gx, gy + 6, gx + 8, gy + 22], fill=(90, 60, 30), width=4)
    d.ellipse([gx - 4, gy + 22, gx + 20, gy + 28], fill=(140, 105, 65), outline=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_guitar(d, x, y, w, h):
    # Electric guitar on a dark stage, single spotlight.
    d.rectangle([x, y, x + w, y + h], fill=(40, 36, 48))
    d.polygon([(x + w * 0.42, y), (x + w * 0.58, y), (x + w * 0.74, y + h * 0.80), (x + w * 0.26, y + h * 0.80)], fill=(80, 76, 100))
    # guitar body
    gx, gy = x + w * 0.50, y + h * 0.58
    d.ellipse([gx - 16, gy - 12, gx + 14, gy + 16], fill=(180, 40, 40), outline=INK)
    d.ellipse([gx - 2, gy - 2, gx + 8, gy + 8], fill=(30, 30, 34), outline=INK)
    # neck + head
    d.line([gx + 10, gy - 8, gx + 34, gy - 34], fill=(120, 85, 50), width=5)
    d.rectangle([gx + 30, gy - 40, gx + 42, gy - 28], fill=(60, 60, 66), outline=INK)
    # strings
    d.line([gx - 4, gy + 6, gx + 36, gy - 34], fill=(220, 220, 220), width=1)
    d.line([gx + 2, gy + 10, gx + 40, gy - 30], fill=(220, 220, 220), width=1)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_football(d, x, y, w, h):
    # American football, goalposts, yard lines.
    d.rectangle([x, y, x + w, y + h], fill=(60, 130, 60))
    # yard lines
    for ly in (0.25, 0.50, 0.75):
        d.line([x, y + h * ly, x + w, y + h * ly], fill=(255, 255, 255), width=2)
    # goalpost
    d.line([x + w * 0.78, y + h * 0.15, x + w * 0.78, y + h * 0.55], fill=(255, 220, 60), width=3)
    d.line([x + w * 0.66, y + h * 0.15, x + w * 0.66, y + h * 0.32], fill=(255, 220, 60), width=3)
    d.line([x + w * 0.90, y + h * 0.15, x + w * 0.90, y + h * 0.32], fill=(255, 220, 60), width=3)
    d.line([x + w * 0.66, y + h * 0.32, x + w * 0.90, y + h * 0.32], fill=(255, 220, 60), width=3)
    # football
    fx, fy = x + w * 0.34, y + h * 0.55
    d.ellipse([fx - 20, fy - 11, fx + 20, fy + 11], fill=(140, 85, 40), outline=INK)
    d.line([fx - 12, fy, fx + 12, fy], fill=(255, 255, 255), width=2)
    for lx in (-8, -4, 0, 4, 8):
        d.line([fx + lx, fy - 4, fx + lx, fy + 4], fill=(255, 255, 255), width=1)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_courthouse(d, x, y, w, h):
    # Courthouse columns and a document with a red stamp line.
    d.rectangle([x, y, x + w, y + h], fill=(228, 232, 238))
    # pediment
    d.polygon([(x + w * 0.10, y + h * 0.30), (x + w * 0.50, y + h * 0.10), (x + w * 0.90, y + h * 0.30)], fill=(200, 200, 205), outline=INK)
    # columns
    for cx in (0.18, 0.38, 0.58, 0.78):
        d.rectangle([x + w * cx - 5, y + h * 0.32, x + w * cx + 5, y + h * 0.78], fill=(255, 255, 255), outline=INK)
    # steps
    d.rectangle([x + w * 0.08, y + h * 0.78, x + w * 0.92, y + h * 0.84], fill=(180, 180, 185))
    d.rectangle([x + w * 0.04, y + h * 0.84, x + w * 0.96, y + h * 0.90], fill=(160, 160, 165))
    # document
    d.rectangle([x + w * 0.60, y + h * 0.42, x + w * 0.90, y + h * 0.72], fill=(255, 255, 255), outline=INK)
    d.line([x + w * 0.64, y + h * 0.50, x + w * 0.86, y + h * 0.50], fill=GREY, width=1)
    d.line([x + w * 0.64, y + h * 0.57, x + w * 0.86, y + h * 0.57], fill=GREY, width=1)
    d.line([x + w * 0.62, y + h * 0.66, x + w * 0.88, y + h * 0.48], fill=RED, width=2)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_airbase(d, x, y, w, h):
    # Airbase at dawn: runway, hangar, two jets, smoke plume.
    d.rectangle([x, y, x + w, y + h * 0.45], fill=(250, 190, 130))
    d.rectangle([x, y + h * 0.45, x + w, y + h], fill=(110, 115, 120))
    # runway
    d.polygon([(x + w * 0.05, y + h), (x + w * 0.45, y + h * 0.55), (x + w * 0.60, y + h * 0.55), (x + w * 0.95, y + h)], fill=(70, 70, 75))
    d.line([x + w * 0.50, y + h * 0.60, x + w * 0.50, y + h * 0.95], fill=(255, 255, 255), width=2)
    # hangar
    d.rectangle([x + w * 0.06, y + h * 0.30, x + w * 0.30, y + h * 0.55], fill=(150, 150, 155), outline=INK)
    d.pieslice([x + w * 0.06, y + h * 0.12, x + w * 0.30, y + h * 0.48], 180, 360, fill=(170, 170, 175), outline=INK)
    # jet silhouettes
    for jx, jy in [(0.62, 0.68), (0.78, 0.80)]:
        jx, jy = x + w * jx, y + h * jy
        d.polygon([(jx, jy - 6), (jx + 18, jy), (jx, jy + 6), (jx - 14, jy + 3), (jx - 14, jy - 3)], fill=(30, 30, 34))
        d.polygon([(jx - 2, jy - 6), (jx + 4, jy - 14), (jx + 8, jy - 6)], fill=(30, 30, 34))
    # smoke plume
    for sx, sy, sr in [(0.20, 0.20, 9), (0.26, 0.12, 7), (0.14, 0.12, 6)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr, y + h * sy + sr], fill=(90, 90, 95))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def ill_jet(d, x, y, w, h):
    # F-16 in the sky over clouds, roundel on the wing.
    d.rectangle([x, y, x + w, y + h], fill=(180, 210, 235))
    # clouds
    for cx, cy, cr in [(0.20, 0.80, 12), (0.32, 0.84, 9), (0.72, 0.86, 11), (0.84, 0.80, 8)]:
        d.ellipse([x + w * cx - cr, y + h * cy - cr // 2, x + w * cx + cr, y + h * cy + cr // 2], fill=(255, 255, 255))
    # jet (side view)
    jx, jy = x + w * 0.50, y + h * 0.45
    d.polygon([(jx - 34, jy), (jx + 30, jy - 6), (jx + 38, jy), (jx + 30, jy + 6), (jx - 34, jy + 4)], fill=(90, 95, 105), outline=INK)
    d.polygon([(jx - 6, jy - 4), (jx + 6, jy - 22), (jx + 12, jy - 4)], fill=(90, 95, 105), outline=INK)
    d.polygon([(jx - 14, jy + 4), (jx - 4, jy + 16), (jx + 2, jy + 4)], fill=(90, 95, 105), outline=INK)
    d.ellipse([jx + 18, jy - 3, jx + 26, jy + 3], fill=BLUE, outline=(255, 255, 255))
    # contrail
    d.line([jx - 34, jy, x + w * 0.02, jy + 6], fill=(255, 255, 255), width=2)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


ILL = {1: ill_storm, 2: ill_kyiv, 3: ill_gulf, 4: ill_chess, 5: ill_tariffs,
       6: ill_tanker, 7: ill_mumbai, 8: ill_court, 9: ill_guitar,
       10: ill_football, 11: ill_courthouse, 12: ill_airbase, 13: ill_jet}


# ---------------------------------------------------------------- world map
# Continents as ellipses in lon/lat; dots are drawn where inside any ellipse.
LAND = [
    (-100, 50, 34, 17), (-90, 34, 20, 11), (-125, 44, 11, 9), (-86, 18, 9, 7),
    (-60, -10, 14, 19), (-70, -32, 8, 10),
    (10, 52, 17, 7), (26, 60, 12, 7),
    (15, 6, 19, 21), (30, -20, 11, 11),
    (70, 50, 44, 17), (100, 30, 24, 14), (45, 30, 14, 9), (78, 20, 9, 11),
    (105, 14, 11, 9), (135, -25, 14, 7),
]


def _inside(lon, lat):
    for clt, clat, rx, ry in LAND:
        if ((lon - clt) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1.0:
            return True
    return False


def lonlat_to_xy(lon, lat, x, y, w, h):
    px = x + (lon + 180.0) / 360.0 * w
    py = y + (84.0 - lat) / 142.0 * h
    return px, py


# (story num, city label, lon, lat, label dx, dy) -- on-map labels only where
# they do not collide; the legend under the map names every pin. Two places
# (5 Kuwait City, 13 Washington) are NOT pinned: their neighbours sit too
# close for a separate pin, so the legend says so instead of faking a spot.
PINS = [
    (1, "New York", -74, 41, -48, -8),
    (2, "Kyiv", 30, 50, 6, -8),
    (3, "Riyadh", 47, 25, 6, -8),
    (4, "Jazan", 43, 17, -36, 8),
    (6, "Cairo", 31, 30, -30, 8),
    (7, "Geneva", 6, 46, -40, -8),
    (8, "Mumbai", 73, 19, -42, 2),
    (9, "Dhaka", 90, 23, 6, -8),
    (10, "Mombasa", 40, -4, 6, -8),
    (11, "Detroit", -83, 42, -40, 10),
    (12, "", 43, 55, 0, 0),
    (29, "Quito", -78.5, -0.2, 6, -8),
    (43, "E. Congo", 29, -1.5, -8, 10),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 246))
    step = 6
    xx = x + 3
    while xx < x + w - 3:
        lon = -180 + (xx - x) / w * 360.0
        yy = y + 3
        while yy < y + h - 3:
            lat = 84 - (yy - y) / h * 142.0
            if _inside(lon, lat):
                d.ellipse([xx - 1, yy - 1, xx + 1, yy + 1], fill=(120, 140, 160))
            yy += step
        xx += step
    fnum = SANS_B(7)
    flab = SANS(8)
    for num, city, lon, lat, dx, dy in PINS:
        px, py = lonlat_to_xy(lon, lat, x, y, w, h)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED, outline=(255, 255, 255), width=1)
        tw = d.textlength(str(num), font=fnum)
        d.text((px - tw / 2, py - 3.5), str(num), font=fnum, fill=(255, 255, 255))
        if city:
            d.text((px + dx, py + dy), city, font=flab, fill=INK)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    fT = SANS_B(10)
    fS = SANS(8)
    fV = SANS_B(9)
    d.text((x + 8, y + 5), "THE TARIFF PLAN, IN RATES (%)", font=fT, fill=INK)
    d.text((x + 8, y + 18), "Capped rates proposed by the USTR, via Reuters", font=fS, fill=GREY)
    bx0, by0 = x + 16, y + h - 34
    bw, gap = 38, 16
    maxv = 20
    for i, (lab, val) in enumerate(CHART):
        bx = bx0 + i * (bw + gap)
        bh = (h - 76) * val / maxv
        d.rectangle([bx, by0 - bh, bx + bw, by0], fill=BLUE)
        d.text((bx + bw / 2, by0 - bh - 11), str(val), font=fV, fill=INK, anchor="ma")
        d.text((bx + bw / 2, by0 + 3), lab, font=fS, fill=INK, anchor="ma")
    d.text((x + 8, y + h - 21),
           "*SE Asia: Cambodia, Indonesia, Malaysia, Thailand + Bangladesh.",
           font=SANS(7), fill=GREY)
    d.text((x + 8, y + h - 11),
           "+Japan, S. Korea, Taiwan, EU, Switzerland. Headline: 40% China if truce fails.",
           font=SANS(7), fill=GREY)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 16  # margin

    # top rule
    d.rectangle([0, 0, W, 7], fill=RED)

    # masthead
    f_mast = SERIF_B(25)
    d.text((W // 2, 30), "THE WORLD IN ONE DAY", font=f_mast, fill=INK, anchor="mm")
    d.text((M, 30), "No. 329", font=SANS(10), fill=GREY, anchor="lm")
    d.text((W - M, 30), "60 STORIES", font=SANS_B(10), fill=RED, anchor="rm")
    hrule(d, M, W - M, 44, fill=INK, width=2)

    # date
    f_date = SERIF_B(30)
    d.text((W // 2, 68), "Thursday 26 November 2026", font=f_date, fill=INK, anchor="mm")
    hrule(d, M, W - M, 88, fill=INK, width=1)

    # red deck
    f_deck = SERIF_I(13)
    deck = ("Storm stops the 100th parade  \u2022  Kyiv hit overnight  "
            "\u2022  Gulf war widens")
    d.text((W // 2, 102), deck, font=f_deck, fill=RED, anchor="mm")

    # numbers band
    y0, bh = 114, 34
    bw = (W - 2 * M - 5 * 4) // 6
    f_nb = SANS_B(13)
    f_ns = SANS(8)
    for i, (big, small) in enumerate(NUMBERS):
        bx = M + i * (bw + 4)
        d.rectangle([bx, y0, bx + bw, y0 + bh], fill=PAPER, outline=INK, width=1)
        d.text((bx + bw / 2, y0 + 4), big, font=f_nb, fill=RED, anchor="ma")
        lines = wrap(d, small, f_ns, bw - 8)
        draw_lines(d, bx + 4, y0 + 20, lines[:1], f_ns, fill=GREY)
    hrule(d, M, W - M, y0 + bh + 6, fill=INK, width=1)

    # region band (counts computed from the story lists)
    regions = {}
    for _, _, _, _, _, reg in LEADS:
        regions[reg] = regions.get(reg, 0) + 1
    for _, _, _, _, reg in CARDS:
        regions[reg] = regions.get(reg, 0) + 1
    for _, _, _, reg in INDEX:
        regions[reg] = regions.get(reg, 0) + 1
    order = ["AP", "EU", "ME", "NA", "AF", "LATAM", "GLOBAL"]
    names = {"AP": "ASIA-PACIFIC", "EU": "EUROPE", "ME": "MIDDLE EAST",
             "NA": "N. AMERICA", "AF": "AFRICA", "LATAM": "LATIN AMERICA",
             "GLOBAL": "GLOBAL"}
    parts = [f"{names[r]} {regions.get(r, 0)}" for r in order]
    f_rb = SANS_B(10)
    d.text((W // 2, 164), "60 STORIES  \u2022  " + "  \u2022  ".join(parts), font=f_rb, fill=BLUE, anchor="mm")

    # timeline strip: two rows, full width, all times UTC
    ty = 176
    d.rectangle([M, ty, W - M, ty + 46], fill=(255, 255, 255), outline=INK, width=1)
    d.text((M + 6, ty + 4), "DAY BY THE CLOCK \u2014 ALL TIMES UTC", font=SANS_B(9), fill=RED)
    f_tt = SANS_B(8)
    f_tl = SANS(8)
    for row, chunk in enumerate((TIMELINE[:5], TIMELINE[5:])):
        tx = M + 6
        yy = ty + 18 + row * 13
        for t, lab in chunk:
            d.text((tx, yy), t, font=f_tt, fill=RED)
            tw = d.textlength(t, font=f_tt)
            d.text((tx + tw + 3, yy), lab, font=f_tl, fill=INK)
            tx += tw + 3 + d.textlength(lab, font=f_tl) + 14

    # leads
    ly = 228
    lh = 148
    lw = (W - 2 * M - 2 * 8) // 3
    for i, (num, head, body, why, src, reg) in enumerate(LEADS):
        bx = M + i * (lw + 8)
        d.rectangle([bx, ly, bx + lw, ly + lh], fill=PAPER, outline=INK, width=1)
        ILL[num](d, bx + 6, ly + 6, lw - 12, 44)
        yy = ly + 54
        d.text((bx + 6, yy), f"{num}.", font=SANS_B(12), fill=RED)
        hl = wrap(d, head, SERIF_B(13), lw - 26)
        draw_lines(d, bx + 24, yy, hl[:2], SERIF_B(13), fill=INK, leading=15)
        yy = ly + 86
        bl = wrap(d, body, SANS(10), lw - 12)
        draw_lines(d, bx + 6, yy, bl[:2], SANS(10), fill=INK, leading=12)
        wl = wrap(d, "WHY IT MATTERS: " + why, SANS_O(8), lw - 12)
        draw_lines(d, bx + 6, ly + 112, wl[:2], SANS_O(8), fill=RED, leading=10)
        d.text((bx + 6, ly + lh - 14), f"Source: {src}", font=SANS_O(8), fill=GREY)

    # cards: 5 cols x 2 rows
    cy = ly + lh + 6
    ch = 78
    cw = (W - 2 * M - 4 * 6) // 5
    for i, (num, head, body, src, reg) in enumerate(CARDS):
        r, c = divmod(i, 5)
        bx = M + c * (cw + 6)
        by = cy + r * (ch + 5)
        d.rectangle([bx, by, bx + cw, by + ch], fill=PAPER, outline=INK, width=1)
        ILL[num](d, bx + 5, by + 5, 52, 52)
        tx0 = bx + 62
        hl = wrap(d, f"{num}. {head}", SANS_B(9), cw - 67)
        yy = draw_lines(d, tx0, by + 5, hl[:2], SANS_B(9), fill=INK, leading=10)
        bl = wrap(d, body, SANS(8), cw - 67)
        max_bl = max(1, (by + ch - 13 - yy - 1) // 9)
        draw_lines(d, tx0, yy + 1, bl[:max_bl], SANS(8), fill=GREY, leading=9)
        d.text((tx0, by + ch - 12), src, font=SANS_O(7), fill=GREY)

    # map + chart
    my = cy + 2 * ch + 5 + 6
    mh = 112
    mw = 636
    d.text((M, my), "WHERE IT HAPPENED", font=SANS_B(11), fill=RED)
    draw_map(d, M, my + 16, mw, mh)
    cx0 = M + mw + 8
    cw2 = W - M - cx0
    d.text((cx0, my), "THE TARIFF PLAN, IN RATES", font=SANS_B(11), fill=RED)
    draw_chart(d, cx0, my + 16, cw2, mh)
    # legend under map (wrapped to the map width, plus the unpinned note)
    leg1 = ("Pins = story numbers: 1 New York \u00b7 2 Kyiv \u00b7 3 Riyadh \u00b7 4 Jazan "
            "\u00b7 6 Cairo \u00b7 7 Geneva \u00b7 8 Mumbai \u00b7 9 Dhaka \u00b7 10 Mombasa "
            "\u00b7 11 Detroit \u00b7 12 Savasleyka \u00b7 29 Quito \u00b7 43 E. Congo")
    leg_lines = wrap(d, leg1, SANS(8), mw)
    ly2 = my + 16 + mh + 3
    ly2 = draw_lines(d, M, ly2, leg_lines, SANS(8), fill=GREY, leading=10)
    ly2 = draw_lines(d, M, ly2, ["Not pinned (neighbours too close): 5 Kuwait City \u00b7 13 Washington."],
                     SANS(8), fill=GREY, leading=10)

    # index: 47 more stories, 3 columns
    iy = ly2 + 6
    d.text((M, iy), "THE REST OF THE DAY \u2014 47 MORE STORIES", font=SANS_B(11), fill=RED)
    hrule(d, M, W - M, iy + 15, fill=INK, width=1)
    colw = (W - 2 * M - 2 * 10) // 3
    f_ix = SANS(9)
    line_h = 12
    per_col = 16
    for ci in range(3):
        cx = M + ci * (colw + 10)
        chunk = INDEX[ci * per_col:(ci + 1) * per_col]
        yy = iy + 20
        for num, head, src, reg in chunk:
            line = f"{num}. {head} \u2014 {src}"
            if d.textlength(line, font=f_ix) > colw:
                line = f"{num}. {head}"
            if d.textlength(line, font=f_ix) > colw:
                words = line.split()
                while words and d.textlength(" ".join(words) + "\u2026", font=f_ix) > colw:
                    words.pop()
                line = " ".join(words) + "\u2026"
            d.text((cx, yy), line, font=f_ix, fill=INK)
            yy += line_h
    iy2 = iy + 20 + per_col * line_h

    # bottom boxes
    by = iy2 + 4
    bh2 = H - 18 - by
    bw2 = (W - 2 * M - 8) // 2
    max_box_lines = max(3, (bh2 - 22) // 10)
    # DATE CHECK
    d.rectangle([M, by, M + bw2, by + bh2], fill=(255, 245, 240), outline=RED, width=2)
    d.text((M + 6, by + 4), "DATE CHECK", font=SANS_B(10), fill=RED)
    dl = wrap(d, DATE_CHECK, SANS(8), bw2 - 12)
    draw_lines(d, M + 6, by + 18, dl[:max_box_lines], SANS(8), fill=INK, leading=10)
    # NOT YET + WATCH
    bx2 = M + bw2 + 8
    d.rectangle([bx2, by, bx2 + bw2, by + bh2], fill=(240, 246, 252), outline=BLUE, width=2)
    d.text((bx2 + 6, by + 4), "NOT YET HAPPENED  +  WHAT TO WATCH FRIDAY", font=SANS_B(9), fill=BLUE)
    nl = wrap(d, NOT_YET + " " + WATCH, SANS(8), bw2 - 12)
    draw_lines(d, bx2 + 6, by + 18, nl[:max_box_lines], SANS(8), fill=INK, leading=10)

    # footer
    d.text((W // 2, H - 11),
           "Sources: Reuters \u00b7 BBC \u00b7 AP \u00b7 IANS \u00b7 Chess.com \u00b7 Ukrinform \u00b7 "
           "Ukrainian Air Force \u00b7 Al Jazeera  |  Every story first reported Thu 26 Nov 2026 "
           "in some timezone, unless dated.  [CLAIM] = unverified claim.",
           font=SANS(8), fill=GREY, anchor="mm")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print(f"wrote {path} ({size} bytes, limit 1048576)")
    im = Image.open(path)
    print(f"size: {im.size}, mode: {im.mode}")
