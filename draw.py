#!/usr/bin/env python3
"""Draw the news-image-20261125 entry: 50 stories from Wednesday 25 November 2026.

Layout (1024x1024): masthead, UTC timeline, world map with 50 numbered dots,
16 featured stories, the other 34 in a dense list, DATE CHECK box.
All stories were verified by web search on 25 Nov 2026 (Reuters, AP, BBC,
Al Jazeera, WHO, PTI and outlet reporting). Stories are events that happened
or were first reported on 25 Nov 2026 in some time zone.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (26, 26, 26)
RED = (179, 39, 30)
GREY = (110, 104, 90)
RULE = (180, 172, 150)
MAP_FILL = (232, 223, 200)
MAP_LINE = (140, 128, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_TITLE = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 44)
F_SUB = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 15)
F_SEC = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 13)
F_FEAT = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 13)
F_SRC = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 10)
F_LIST = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 11)
F_LISTB = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 11)
F_SMALL = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 11)
F_TINY = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 9)
F_MAPNUM = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 8)

# region -> colour
REG = {
    "NA": (31, 95, 168),
    "EU": (46, 125, 50),
    "APAC": (192, 86, 33),
    "ME": (123, 45, 139),
    "AF": (138, 109, 0),
    "LATAM": (14, 124, 123),
    "GLOBAL": (85, 85, 85),
}
REG_NAME = {
    "NA": "NORTH AMERICA", "EU": "EUROPE", "APAC": "ASIA-PACIFIC",
    "ME": "MIDDLE EAST", "AF": "AFRICA", "LATAM": "LATIN AMERICA",
    "GLOBAL": "GLOBAL",
}

# (number, region, headline, source, lon, lat, dx, dy)  dx/dy = map label offset
STORIES = [
    (1, "NA", "CIA and ODNI hit by cyberattack on unclassified systems", "Reuters", -77, 39, -42, -16),
    (2, "NA", "Huawei guilty on 10 of 12 US counts; racketeering acquitted", "AP", -74, 41, 10, -14),
    (3, "NA", "US consumer confidence hits near two-year high", "Reuters", -77, 39, 12, 10),
    (4, "NA", "Trump gives Giuliani the Presidential Medal of Freedom", "Washington Post", -77, 39, -40, 10),
    (5, "NA", "Fort Hood gunman seeks stay of execution set for next week", "Reuters", -98, 31, -8, 12),
    (6, "NA", "Radar fault delays flights at Chicago O'Hare", "FAA", -88, 42, 10, -14),
    (7, "NA", "Trump pardons Thanksgiving turkeys Freedom and Feathers", "Reuters", -77, 39, -38, -14),
    (8, "NA", "Senate probes Vance link to Vitol Venezuela oil deal", "Reuters", -77, 39, 14, 14),
    (9, "NA", "Dell posts record $54.9bn quarter on AI servers", "Reuters", -98, 30, 10, -12),
    (10, "NA", "US PCE inflation print due 08:30 ET, the Fed's key gauge", "BEA", -77, 39, 18, -6),
    (11, "EU", "Zelenskyy confirms Ukraine hit Russian ship in Gulf of Finland", "Reuters", 30, 50, -32, -12),
    (12, "EU", "Sanofi agrees $41bn takeover of US drugmaker Insmed", "Reuters", 2, 49, 8, -14),
    (13, "EU", "Sarkozy corruption case sent to trial; hearing April 2027", "Reuters", 2, 49, -32, 10),
    (14, "EU", "EU announces new sanctions on Russia", "Reuters", 4, 51, 12, 8),
    (15, "EU", "NATO to deploy early-warning aircraft in Poland", "Reuters", 21, 52, 14, 12),
    (16, "EU", "Latvia sees possible 'tipping point' in Ukraine war next year", "Reuters", 24, 57, 16, -14),
    (17, "EU", "Denmark's top court upholds 'ghetto' evictions", "Reuters", 13, 56, -28, -14),
    (18, "EU", "LaLiga hit by cyberattack exposing fan data", "Reuters", -4, 40, -8, 10),
    (19, "EU", "Liverpool thrash Man Utd 4-0; Pochettino fury at Yoro red", "Reuters", -3, 53, 8, -12),
    (20, "APAC", "Australia and Solomon Islands sign security pact", "Reuters", 160, -9, 8, -4),
    (21, "APAC", "England beat Australia by 8 wickets to level T20 series", "Reuters", 151, -34, 8, -4),
    (22, "APAC", "Shenzhou-24 lifts off today with first Pakistani astronaut", "SpacePolicyOnline", 100, 41, 8, -12),
    (23, "APAC", "BJP and Akali Dal reunite for 2027 Punjab polls", "PTI", 77, 31, 12, 10),
    (24, "APAC", "Mumbai extend Syed Mushtaq Ali winning run to five", "PTI", 88, 23, 8, -4),
    (25, "APAC", "Sooryavanshi, 15, smashes 204 off 53 balls", "Reuters", 55, 25, -30, -8),
    (26, "APAC", "Gulf Giants beat MI Emirates by six wickets", "Reuters", 55, 25, 10, -16),
    (27, "APAC", "India women beat China 6-2 in football", "Reuters", 77, 29, -8, 10),
    (28, "APAC", "J&K cricket beat Railways by four wickets", "Reuters", 75, 34, 12, -14),
    (29, "APAC", "RFE/RL returns to shortwave for Afghan girls", "RFE/RL", 69, 35, -38, 12),
    (30, "ME", "Houthis hit Riyadh's tallest tower; 11 wounded", "Al Jazeera", 47, 25, -14, -18),
    (31, "ME", "Fourth tanker explodes on mine in Strait of Hormuz", "Reuters", 56, 26, 16, 12),
    (32, "ME", "Houthis push to 60km from Aden; army says city will hold", "Reuters", 45, 13, -36, 8),
    (33, "ME", "Iran faces winter gas shortages as war damage bites", "RFE/RL", 51, 36, 14, -18),
    (34, "ME", "Iran to ration electricity after US-Israeli strikes", "RFE/RL", 51, 36, -42, -12),
    (35, "ME", "Israeli army suicides at 16-year high", "Haaretz", 35, 32, -30, -14),
    (36, "ME", "UN warns over Gaza humanitarian conditions", "UN", 34, 31, -34, 12),
    (37, "AF", "WHO evacuates Ebola teams in DR Congo after 3 days", "WHO", 30, 1, 10, -4),
    (38, "AF", "Ukraine sank Russian warship at Benghazi, Zelenskyy says", "RFE/RL", 20, 32, -36, -12),
    (39, "AF", "Markram's 150 leads South Africa in Test", "Reuters", 28, -26, 10, -4),
    (40, "AF", "Joburg coalition: ANC and ActionSA carve up posts", "Daily Maverick", 28, -26, -36, 10),
    (41, "AF", "Sudan war: Tasis forces claim Blue Nile base", "Citizen Digital", 33, 16, -36, 14),
    (42, "AF", "Amnesty seeks UN action over 14 civilian deaths in Ethiopia", "Amnesty", 39, 9, 14, -16),
    (43, "AF", "Comoros opens renovated Said Mohamed Cheikh school today", "Comores Infos", 43, -12, 8, -4),
    (44, "LATAM", "Hostages held in Cartagena supermarket after heist fails", "Reuters", -75, 10, 8, -4),
    (45, "LATAM", "Venezuela reports public debt of $237.5bn", "Reuters", -67, 11, 8, -12),
    (46, "LATAM", "Santos lose 2-0 to Gremio in Brasileirao", "Reuters", -47, -24, 8, -4),
    (47, "GLOBAL", "Gukesh and Sindarov draw World Chess opener", "Reuters", 6, 46, 8, -12),
    (48, "GLOBAL", "Russia, Ukraine trade accusations at UN", "Reuters", -74, 41, -30, 10),
    (49, "GLOBAL", "Great Barrier Reef yields 12 'resurrected' coral species", "Reuters", 147, -19, 8, -4),
    (50, "GLOBAL", "Asteroid eclipse: one asteroid's shadow falls on another", "ESA", 9, 50, 8, -12),
]

FEATURED = [1, 2, 11, 30, 31, 20, 37, 3, 4, 12, 13, 21, 22, 38, 10, 32]

TIMELINE = [
    ("00:19", "Shenzhou-24 lifts off with Pakistan's first astronaut"),
    ("~01:00", "Australia signs Solomons security pact"),
    ("~06:00", "CIA + ODNI cyber breach reported"),
    ("13:30", "US PCE inflation print due (08:30 ET)"),
    ("~18:00", "Houthis strike Riyadh's tallest tower"),
    ("~22:00", "Huawei verdict lands in New York"),
]

LEFT_OUT = [
    "COP31 climate talks ended 22 Nov — not today's news.",
    "Trump, Xi and Putin met in China on 19 Nov — not today.",
    "GTA 6 released 19 Nov; Nepal PM's India visit ended 23 Nov.",
    "BepiColombo reached Mercury 22 Nov; SpaceX caught Starship 22 Nov.",
]

# Simplified continent polygons (lon, lat)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66), (-80, 73),
     (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35), (-80, 32), (-85, 30),
     (-90, 29), (-97, 26), (-105, 22), (-110, 23), (-115, 28), (-120, 34),
     (-125, 40), (-125, 48), (-135, 58), (-150, 60), (-165, 60)],  # N America
    [(-58, 64), (-45, 60), (-40, 65), (-50, 70), (-60, 76), (-68, 70)],  # Greenland
    [(-80, 10), (-75, 5), (-70, 10), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-38, -20), (-45, -25), (-50, -30), (-55, -35), (-65, -40), (-70, -50),
     (-73, -40), (-72, -25), (-75, -15), (-80, -5)],  # S America
    [(-10, 35), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (48, 10),
     (51, 12), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30),
     (12, -18), (10, -5), (5, 5), (-5, 5), (-15, 10), (-17, 15), (-15, 25),
     (-10, 30)],  # Africa
    [(-10, 36), (-5, 43), (0, 46), (-2, 50), (5, 53), (8, 57), (10, 59), (18, 56),
     (20, 55), (25, 60), (30, 65), (35, 68), (50, 70), (70, 72), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (160, 55), (150, 50),
     (140, 45), (135, 40), (130, 35), (127, 35), (122, 30), (120, 25), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 20), (85, 20), (80, 15), (75, 10),
     (72, 20), (65, 25), (60, 25), (55, 26), (50, 28), (48, 30), (45, 30), (40, 35),
     (35, 36), (30, 36), (25, 38), (20, 40), (15, 44), (10, 44), (5, 40), (0, 38),
     (-5, 36)],  # Eurasia
    [(-5, 50), (-2, 52), (0, 53), (-3, 58), (-5, 56)],  # UK
    [(113, -22), (120, -15), (130, -12), (135, -12), (142, -11), (145, -15),
     (150, -20), (153, -27), (150, -37), (140, -38), (130, -32), (125, -33),
     (115, -35), (113, -26)],  # Australia
    [(130, 31), (133, 34), (137, 35), (140, 38), (142, 42), (144, 44), (141, 40),
     (138, 36), (134, 33)],  # Japan
    [(167, -45), (170, -42), (174, -38), (178, -37), (175, -40), (172, -43),
     (168, -46)],  # NZ
    [(44, -16), (47, -15), (50, -16), (49, -20), (45, -25), (43, -20)],  # Madagascar
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10), (125, -5),
     (130, 0), (135, -3), (140, -5)],  # SE Asia islands
]

MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 20, 176, 1004, 322


def lonlat_to_xy(lon, lat):
    x = MAP_X0 + (lon + 180) / 360.0 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (75 - lat) / 130.0 * (MAP_Y1 - MAP_Y0)
    return x, y


def trunc(draw, text, font, max_w):
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=font) > max_w:
        text = text[:-1]
    return text + "…"


def draw_image():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 92], fill=(26, 26, 26))
    d.text((20, 10), "THE WORLD IN ONE DAY", font=F_SUB, fill=(248, 244, 232))
    d.text((20, 34), "WEDNESDAY 25 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255))
    d.text((20, 78), "50 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM THIS DAY",
           font=ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 12),
           fill=(230, 200, 90))
    d.rectangle([0, 92, W, 96], fill=RED)

    # ---- Timeline ----
    d.text((20, 104), "THE DAY IN UTC", font=F_SEC, fill=RED)
    for i, (t, label) in enumerate(TIMELINE):
        x = 20 + i * 164
        d.text((x, 124), t, font=F_LISTB, fill=INK)
        # wrap the label over two lines instead of cutting it off
        words = label.split()
        lines, cur = [], ""
        for w in words:
            if d.textlength((cur + " " + w).strip(), font=F_TINY) <= 156:
                cur = (cur + " " + w).strip()
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for j, ln in enumerate(lines[:2]):
            d.text((x, 140 + j * 11), ln, font=F_TINY, fill=GREY)
        if i:
            d.line([(x - 8, 126), (x - 8, 156)], fill=RULE, width=1)
    d.line([(20, 158), (1004, 158)], fill=RULE, width=1)

    # ---- Map ----
    d.text((20, 166), "WHERE IT HAPPENED — 50 STORIES, NUMBERED BELOW",
           font=F_SEC, fill=RED)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=MAP_FILL, outline=MAP_LINE)
    by_num = {s[0]: s for s in STORIES}
    for n, reg, head, src, lon, lat, dx, dy in STORIES:
        x, y = lonlat_to_xy(lon, lat)
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=REG[reg], outline=(255, 255, 255))
        lx, ly = x + dx, y + dy
        d.line([(x, y), (lx + 4, ly + 4)], fill=(150, 140, 120), width=1)
        d.text((lx, ly), str(n), font=F_MAPNUM, fill=INK)

    # ---- Featured stories ----
    d.text((20, 332), "THE DAY'S BIGGEST STORIES", font=F_SEC, fill=RED)
    d.line([(20, 352), (1004, 352)], fill=RULE, width=1)
    col_w = 482
    for i, n in enumerate(FEATURED):
        _, reg, head, src, _, _, _, _ = by_num[n]
        col = i % 2
        row = i // 2
        x = 20 + col * (col_w + 20)
        y = 360 + row * 32
        d.text((x, y), str(n), font=F_LISTB, fill=REG[reg])
        d.text((x + 26, y), trunc(d, head, F_FEAT, col_w - 26), font=F_FEAT, fill=INK)
        d.text((x + 26, y + 16), f"{REG_NAME[reg]}  ·  {src}",
               font=F_SRC, fill=GREY)

    # ---- Also today ----
    d.text((20, 622), "ALSO TODAY", font=F_SEC, fill=RED)
    d.line([(20, 642), (1004, 642)], fill=RULE, width=1)
    rest = [s for s in STORIES if s[0] not in FEATURED]
    for i, (n, reg, head, src, _, _, _, _) in enumerate(rest):
        col = i % 2
        row = i // 2
        x = 20 + col * (col_w + 20)
        y = 650 + row * 17
        line = f"{n}. {head} — {src}"
        d.text((x, y), str(n) + ".", font=F_LISTB, fill=REG[reg])
        d.text((x + 24, y), trunc(d, f"{head} — {src}", F_LIST, col_w - 24),
               font=F_LIST, fill=INK)

    # ---- Date check ----
    d.rectangle([20, 942, 1004, 1018], outline=RED, width=2)
    d.text((32, 948), "DATE CHECK — LEFT OUT ON PURPOSE", font=F_SEC, fill=RED)
    y = 966
    for line in LEFT_OUT:
        d.text((32, y), "•  " + line, font=F_SMALL, fill=INK)
        y += 13
    return img


if __name__ == "__main__":
    im = draw_image()
    im.save("entry.png", optimize=True)
    import os
    print("saved entry.png", os.path.getsize("entry.png"), "bytes", im.size)
