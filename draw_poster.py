#!/usr/bin/env python3
"""Draw the news-image-20261124 poster: 'THE WORLD IN ONE DAY / TUESDAY, 24 NOVEMBER 2026'.

A newspaper front page, 1024x1024 PNG, drawn entirely with PIL (no photos).
Four stories, all verified against reputable sources on 24 Nov 2026:
  1. Nvidia reinstates Jensen Huang as CEO; shares surge 31.5%, ~$952B gain,
     Nasdaq +6.5% — Reuters / Nasdaq / CNBC (announced Mon 23 Nov, after the
     23 Nov poster was submitted; market close Mon 23 Nov)
  2. 24 dead in the PT Fonusa Agung Mulia candy-factory fire, Cikande,
     Banten; ~30 missing; AC short circuit suspected — Reuters / AP
     (death toll confirmed Mon 23 Nov)
  3. NATO sends an AWACS early-warning aircraft to Poland after three
     Russian Kh-101 missiles landed there — Reuters (announced Mon 23 Nov)
  4. South Korea scrambles jets, briefly warns Ulleung Island after
     Russian planes enter its air-defence zone — Reuters (Tue 24 Nov)
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
GRAY = (85, 85, 85)
LIGHT = (233, 227, 214)
SEA = (38, 92, 130)
SAND = (214, 196, 150)
GREEN = (28, 120, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_text_block(draw, x, y, max_w, lines, fnt, fill=INK, leading=6):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def hrule(draw, x0, x1, y, w=3, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def draw_chart(draw, x, y, w, h):
    # rising stock chart: axes, gridlines, steep line, arrow, +31.5%
    ox, oy = x + 14, y + h - 26
    top = y + 34
    right = x + w - 14
    for gy in (oy - 60, oy - 120):
        draw.line([(ox, gy), (right, gy)], fill=(200, 194, 178), width=1)
    draw.line([(ox, top), (ox, oy)], fill=GRAY, width=2)
    draw.line([(ox, oy), (right, oy)], fill=GRAY, width=2)
    pts = [(ox, oy - 8), (ox + 52, oy - 14), (ox + 104, oy - 10),
           (ox + 156, oy - 58), (ox + 208, oy - 108), (ox + 258, oy - 158)]
    draw.line(pts, fill=GREEN, width=6, joint="curve")
    # arrowhead at the last point
    ex, ey = pts[-1]
    draw.polygon([(ex, ey - 14), (ex + 16, ey + 2), (ex - 2, ey + 2)], fill=GREEN)
    draw.text((x + 16, y + 8), "+31.5%", font=font(SANS_B, 34), fill=GREEN)
    draw.text((right - 118, y + 12), "$165.05", font=font(SANS_B, 24), fill=INK)


def draw_factory_fire(draw, x, y, w, h):
    # smokestacks with smoke, flames at the base; base sits at y + h
    base = y + h
    for i, sx in enumerate((x + 8, x + 62, x + 116)):
        draw.rectangle([sx, base - 58, sx + 34, base], fill=(70, 70, 70))
        draw.rectangle([sx - 3, base - 64, sx + 37, base - 58], fill=(50, 50, 50))
        for j, (ox, oy, r) in enumerate(((6, -72, 8), (16, -86, 11), (4, -100, 9))):
            draw.ellipse([sx + ox, base + oy - r, sx + ox + 2 * r, base + oy + r],
                         fill=(150, 150, 150))
    # flames licking the base
    for fx in (x + 20, x + 74, x + 128):
        draw.polygon([(fx, base), (fx + 12, base - 34), (fx + 24, base)],
                     fill=(240, 140, 20))
        draw.polygon([(fx + 6, base), (fx + 12, base - 20), (fx + 18, base)],
                     fill=(240, 200, 40))
    draw.rectangle([x, base - 4, x + w, base], fill=INK)


def draw_awacs(draw, x, y, w, h):
    # radar plane: fuselage, dome disc on top, tail fin, wings
    cx, cy = x + w // 2, y + h // 2 + 6
    # wings (behind fuselage)
    draw.polygon([(cx - 30, cy + 4), (cx + 40, cy + 4), (cx + 10, cy + 34),
                  (cx - 56, cy + 34)], fill=(120, 130, 140))
    # fuselage
    draw.ellipse([x + 8, cy - 16, x + w - 8, cy + 16], fill=(200, 204, 208),
                 outline=INK, width=2)
    # nose + tail
    draw.polygon([(x + w - 8, cy - 10), (x + w + 10, cy), (x + w - 8, cy + 10)],
                 fill=(200, 204, 208), outline=INK)
    draw.polygon([(x + 16, cy - 14), (x + 34, cy - 44), (x + 48, cy - 14)],
                 fill=(90, 98, 106))
    # radar dome on a strut
    draw.line([(cx, cy - 14), (cx, cy - 34)], fill=INK, width=4)
    draw.ellipse([cx - 52, cy - 52, cx + 52, cy - 34], fill=(230, 230, 230),
                 outline=INK, width=2)
    # windows
    for wx in range(x + 40, x + w - 60, 26):
        draw.ellipse([wx, cy - 6, wx + 10, cy + 4], fill=BLUE)


def draw_island_alert(draw, x, y, w, h):
    # sea, island mound, warning triangle with "!"
    base = y + h
    for wx in range(x, x + w, 46):
        draw.arc([wx, base - 34, wx + 44, base - 14], 0, 180, fill=SEA, width=4)
    draw.pieslice([x + 60, base - 78, x + w - 60, base - 6], 180, 360,
                  fill=(96, 140, 82))
    draw.polygon([(x + w - 74, base - 66), (x + w - 40, base - 66),
                  (x + w - 57, base - 108)], fill=(240, 200, 40), outline=INK)
    draw.text((x + w - 63, base - 98), "!", font=font(SANS_B, 26), fill=INK)
    # two jets as small triangles above the island
    for jx, jy in ((x + 30, y + 18), (x + 62, y + 34)):
        draw.polygon([(jx, jy), (jx + 26, jy + 8), (jx, jy + 16)], fill=(80, 88, 94))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    hrule(d, 28, 996, 26, 4)
    f_mast = font(SERIF, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 44), title, font=f_mast, fill=INK)
    f_date = font(SANS_B, 25)
    date = "TUESDAY,  24  NOVEMBER  2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 122), date, font=f_date, fill=RED)
    hrule(d, 28, 996, 162, 3)
    hrule(d, 28, 996, 168, 1)

    # ---- lead story: Nvidia ----
    f_kick = font(SANS_B, 20)
    d.text((40, 188), "TECH  •  SANTA CLARA", font=f_kick, fill=RED)
    f_h1 = font(SERIF, 54)
    y = 218
    y = draw_text_block(d, 40, y, 560, ["HUANG IS BACK"], f_h1, leading=2)
    f_h2 = font(SERIF, 30)
    y = draw_text_block(
        d, 40, y + 8, 560,
        wrap(d, "Nvidia reinstates its CEO after 11 days; shares surge 31.5%", f_h2, 560),
        f_h2, leading=4)
    f_body = font(SANS, 21)
    body = ("Nvidia's board voted unanimously to bring Jensen "
            "Huang back as president and chief executive, "
            "effective immediately, 11 days after he resigned. "
            "Shares jumped 31.5% to $165.05, adding about $952 "
            "billion in market value; the Nasdaq rose 6.5%.")
    y = draw_text_block(d, 40, y + 12, 560, wrap(d, body, f_body, 560), f_body, leading=7)
    # lead illustration: stock chart
    d.rectangle([640, 188, 984, 470], outline=INK, width=2, fill=LIGHT)
    draw_chart(d, 648, 196, 328, 266)
    d.text((652, 448), "The CEO returns; the market roars back.", font=font(SANS, 16), fill=GRAY)

    hrule(d, 40, 984, 496, 2)

    # ---- three stories in a row ----
    cols = [
        dict(x=40, w=296, kick="INDONESIA  •  BANTEN", head="24 dead in\nfactory fire",
             body=("Indonesia confirmed 24 people dead after a "
                   "fire tore through the PT Fonusa Agung Mulia "
                   "candy factory on Saturday. About 30 workers "
                   "are still missing; an air-conditioner short "
                   "circuit is the suspected cause."),
             art=draw_factory_fire),
        dict(x=364, w=296, kick="DEFENCE  •  BRUSSELS", head="NATO sends\nAWACS to Poland",
             body=("NATO will deploy an early-warning AWACS "
                   "aircraft to Poland after three Russian "
                   "Kh-101 missiles landed there on Friday. "
                   "Allies blamed Moscow for the 'dangerous' "
                   "incursion; no one was hurt."),
             art=draw_awacs),
        dict(x=688, w=296, kick="KOREA  •  ULLEUNG ISLAND", head="Seoul scrambles\njets in alert",
             body=("South Korea scrambled jets and told Ulleung "
                   "Island residents to shelter after Russian "
                   "planes entered its air-defence zone on "
                   "Tuesday morning. The alert was lifted within "
                   "minutes; no airspace was violated."),
             art=draw_island_alert),
    ]
    f_kick2 = font(SANS_B, 17)
    f_head = font(SERIF, 32)
    f_body2 = font(SANS, 20)
    for c in cols:
        x, w = c["x"], c["w"]
        d.text((x, 516), c["kick"], font=f_kick2, fill=RED)
        # art panel
        d.rectangle([x, 548, x + w, 668], outline=INK, width=2, fill=LIGHT)
        c["art"](d, x + 8, 552, w - 16, 112)
        y = 684
        y = draw_text_block(d, x, y, w, c["head"].split("\n"), f_head, leading=2)
        y = draw_text_block(d, x, y + 8, w, wrap(d, c["body"], f_body2, w), f_body2, leading=6)

    hrule(d, 40, 984, 972, 2)
    f_foot = font(SANS, 16)
    d.text((40, 984), "Sources: Reuters · AP · Yonhap",
           font=f_foot, fill=GRAY)
    d.text((640, 984), "THE WORLD IN ONE DAY — 24 NOV 2026",
           font=f_foot, fill=GRAY)

    img.save("poster.png", "PNG")
    print("saved poster.png", img.size)


if __name__ == "__main__":
    main()
