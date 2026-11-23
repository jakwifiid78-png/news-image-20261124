#!/usr/bin/env python3
"""THE WORLD TODAY - front page for Tuesday 24 November 2026.

Draws a 1024x1024 newspaper front page with PIL (stdlib + Pillow only)
and writes it to entry.png next to this file, then copies it to
/output/entry.png. Fully deterministic: no randomness, no clock, no
network. Two runs produce identical bytes.
"""
import os
import shutil

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (18, 18, 18)
RED = (178, 34, 28)
GREY = (90, 86, 78)
RULE = (40, 40, 40)
ORANGE = (232, 96, 24)
FLAME = (244, 164, 32)
SMOKE = (120, 118, 112)
SKY = (52, 44, 40)
PANEL = (255, 252, 244)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, path, text, max_width, start_size):
    size = start_size
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(path, 10)


def wrap(draw, text, fnt, width):
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


def draw_lines(draw, lines, fnt, x, y, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer frame
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # ---- Masthead ----
    f_mast = fit_font(d, SERIF_B, "THE WORLD TODAY", W - 72, 84)
    d.text((W // 2, 30), "THE WORLD TODAY", font=f_mast, fill=INK, anchor="ma")
    f_date = font(SANS_B, 20)
    d.text((W // 2, 122), "TUESDAY 24 NOVEMBER 2026  •  WORLD NEWS IN ONE PAGE",
           font=f_date, fill=RED, anchor="ma")
    rule(d, 32, 154, W - 32, 4)
    rule(d, 32, 162, W - 32, 1)

    # ---- Main story ----
    y = 178
    f_kick = font(SANS_B, 19)
    d.text((32, y), "INDONESIA  •  BANTEN", font=f_kick, fill=RED)
    y += 28
    f_head = font(SERIF_B, 50)
    head_lines = wrap(d, "FACTORY FIRE KILLS AT LEAST 24", f_head, W - 64)
    y = draw_lines(d, head_lines, f_head, 32, y, leading=56)
    y += 4
    f_sub = font(SERIF, 22)
    sub_lines = wrap(
        d,
        "Dozens missing as rescuers search the rubble after a blaze "
        "swept a factory in Cikande, west of Jakarta.",
        f_sub, W - 64)
    y = draw_lines(d, sub_lines, f_sub, 32, y, leading=26)
    y += 12

    # ---- Illustration: factory fire at dusk ----
    PH = 150
    px0, py0, px1, py1 = 32, y, W - 32, y + PH
    d.rectangle([px0, py0, px1, py1], fill=SKY)
    d.rectangle([px0, py0 + 92, px1, py1], fill=(96, 52, 36))
    # smoke puffs
    for cx, cy, r in [(180, py0 + 34, 24), (235, py0 + 18, 30),
                      (300, py0 + 32, 20), (760, py0 + 26, 26),
                      (820, py0 + 40, 19)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
        d.ellipse([cx - r + 10, cy - r - 8, cx + r + 10, cy + r - 8],
                  fill=(140, 138, 130))
    # factory silhouette
    d.rectangle([px0 + 60, py0 + 80, px0 + 560, py1], fill=(28, 24, 22))
    d.rectangle([px0 + 600, py0 + 98, px0 + 880, py1], fill=(34, 29, 26))
    # chimney
    d.rectangle([px0 + 500, py0 + 44, px0 + 540, py0 + 82], fill=(28, 24, 22))
    # windows
    for i in range(6):
        wx = px0 + 100 + i * 72
        d.rectangle([wx, py0 + 98, wx + 34, py0 + 118], fill=FLAME)
    for i in range(3):
        wx = px0 + 640 + i * 76
        d.rectangle([wx, py0 + 114, wx + 34, py0 + 132], fill=FLAME)
    # flames on the roofline
    for cx, base, hgt, wdt in [(150, py0 + 80, 40, 40),
                               (260, py0 + 80, 52, 44),
                               (380, py0 + 80, 36, 36),
                               (500, py0 + 80, 46, 40),
                               (700, py0 + 98, 42, 40),
                               (810, py0 + 98, 34, 34)]:
        d.polygon([(cx - wdt // 2, base), (cx, base - hgt),
                   (cx + wdt // 2, base)], fill=ORANGE)
        d.polygon([(cx - wdt // 4, base), (cx, base - hgt // 2),
                   (cx + wdt // 4, base)], fill=FLAME)
    d.rectangle([px0, py0, px1, py1], outline=INK, width=2)
    # caption
    f_cap = font(SANS, 15)
    d.text((px0 + 10, py1 + 5),
           "Smoke rises over the factory in Cikande, Banten, as firefighters battle the blaze.",
           font=f_cap, fill=GREY)
    y = py1 + 22

    rule(d, 32, y, W - 32, 2)
    y += 10

    # ---- Supporting stories: 2 columns x 3 rows ----
    stories = [
        ("UKRAINE", "KYIV REGION HIT BY RUSSIAN STRIKES",
         "A residential building in Dymer was hit; several killed, "
         "others missing."),
        ("BALTIC SEA", "RUSSIAN CARGO SHIP BURNS AFTER DRONE ATTACK",
         "The Sparta II caught fire in the Gulf of Finland."),
        ("CLIMATE", "COP31 ENDS WITH NO FOSSIL-FUEL DEAL",
         "Talks in Antalya closed with no deal to phase out fossil fuels."),
        ("PORTUGAL", "THOUSANDS MARCH IN LISBON OVER LIVING COSTS",
         "Protesters rallied against rising prices."),
        ("SPORT", "VERSTAPPEN WINS LAS VEGAS GRAND PRIX",
         "The Red Bull driver took victory under the lights in Nevada."),
        ("SPORT", "ALCARAZ WINS FIRST ATP FINALS TITLE",
         "The Spaniard beat Zverev to lift the season-ending crown."),
    ]
    col_w = (W - 64 - 28) // 2
    row_h = 112
    f_sk = font(SANS_B, 15)
    f_sh = font(SERIF_B, 21)
    f_sd = font(SERIF, 17)
    for i, (kick, head, deck) in enumerate(stories):
        cx = 32 + (i % 2) * (col_w + 28)
        cy = y + (i // 2) * row_h
        d.text((cx, cy), kick, font=f_sk, fill=RED)
        h_lines = wrap(d, head, f_sh, col_w)
        hy = draw_lines(d, h_lines, f_sh, cx, cy + 20, leading=24)
        d_lines = wrap(d, deck, f_sd, col_w)
        draw_lines(d, d_lines, f_sd, cx, hy + 2, leading=21)
        if i % 2 == 0:
            d.line([(cx + col_w + 14, cy), (cx + col_w + 14, cy + row_h - 14)],
                   fill=(200, 194, 178), width=1)
    y += 3 * row_h + 2
    rule(d, 32, y, W - 32, 2)
    y += 8

    # ---- Markets strip ----
    f_mk = font(SANS_B, 18)
    d.text((32, y), "MARKETS", font=f_mk, fill=RED)
    f_mt = font(SERIF, 19)
    m_lines = wrap(
        d,
        "NVIDIA JUMPS AS TECH RALLIES — shares added about $1tn in value "
        "as Jensen Huang returned to the spotlight.",
        f_mt, W - 64 - 130)
    draw_lines(d, m_lines, f_mt, 168, y, leading=24)
    y += 50
    rule(d, 32, y, W - 32, 1)

    # ---- Footer ----
    f_ft = font(SANS, 14)
    d.text((W // 2, y + 6), "THE WORLD TODAY  •  TUESDAY 24 NOVEMBER 2026",
           font=f_ft, fill=GREY, anchor="ma")

    here = os.path.dirname(os.path.abspath(__file__))
    out_local = os.path.join(here, "entry.png")
    img.save(out_local, format="PNG")
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(out_local, "/output/entry.png")


if __name__ == "__main__":
    main()
