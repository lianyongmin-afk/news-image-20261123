#!/usr/bin/env python3
"""Render the 23 November 2026 world-news infographic (entry.png).

A broadsheet-style front page, 1024 x 1024: navy masthead with the date,
then a 2 x 3 grid of story cards. Every card has a number, a section tag,
a headline, one line of detail, its source, and a small pictogram drawn
from PIL primitives -- no image assets, no network, no randomness.

Run:  python3 generate.py        (writes entry.png next to this file)
The output is deterministic: same code, same bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 28, 44)
NAVY = (20, 33, 61)
GOLD = (233, 196, 106)
WHITE = (255, 255, 255)
GREY = (96, 102, 112)
CARD = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines fitting `width` px."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def letter_spaced(draw, text, fnt, x, y, fill, spacing=4):
    """Draw `text` with extra tracking between letters."""
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=fill)
        cx += draw.textlength(ch, font=fnt) + spacing
    return cx


# ---------------------------------------------------------------- stories
# Headline, detail, source, tag, accent colour, pictogram key.
# All six are from the 23 November 2026 news cycle, checked against the
# outlets named on each card.
STORIES = [
    (
        "COP31 climate talks collapse",
        "Nearly 200 countries leave Antalya with no deal on fossil fuels or finance.",
        "SCMP · The Economic Times",
        "CLIMATE",
        (42, 127, 98),
        "globe",
    ),
    (
        "Democrats take the House: 258 seats",
        "Their best House result since 1992, flipping control of Congress.",
        "SCMP · The Economic Times",
        "UNITED STATES",
        (29, 78, 137),
        "ballot",
    ),
    (
        "Russian strikes kill 11 in Kyiv region",
        "Ukraine says homes and a supermarket in Vyshneve were hit.",
        "Arab News PK",
        "WAR IN EUROPE",
        (192, 57, 43),
        "flame",
    ),
    (
        "Drone strikes hit Khartoum and a UN building",
        "Strikes reported in Sudan's capital.",
        "AFP via The Manila Times",
        "AFRICA",
        (93, 109, 126),
        "drone",
    ),
    (
        "Factory fire in Indonesia: 3 dead, 36 missing",
        "Rescue teams search the burned-out plant for the missing.",
        "The Manila Times",
        "ASIA",
        (183, 121, 31),
        "factory",
    ),
    (
        "Paolo Bulgari, jeweller to Hollywood, dies at 89",
        "The chairman who turned a Roman shop into a global luxury house.",
        "The Economic Times",
        "CULTURE",
        (138, 109, 27),
        "gem",
    ),
]


# ------------------------------------------------------------- pictograms
def pictogram(draw, kind, cx, cy, r, colour):
    """A small pictogram inside a coloured disc, drawn from primitives."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    w = (255, 255, 255)
    if kind == "globe":
        draw.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
                     outline=w, width=3)
        draw.arc([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
                 200, 340, fill=w, width=3)
        draw.line([cx - r * 0.55, cy, cx + r * 0.55, cy], fill=w, width=3)
    elif kind == "ballot":
        draw.rectangle([cx - r * 0.5, cy - r * 0.35, cx + r * 0.5, cy + r * 0.5],
                       outline=w, width=3)
        draw.line([cx - r * 0.35, cy + r * 0.05, cx - r * 0.05, cy + r * 0.35,
                   cx + r * 0.45, cy - r * 0.3], fill=w, width=4)
    elif kind == "flame":
        draw.polygon([(cx, cy - r * 0.6), (cx + r * 0.45, cy + r * 0.1),
                      (cx + r * 0.2, cy + r * 0.5), (cx - r * 0.2, cy + r * 0.5),
                      (cx - r * 0.45, cy + r * 0.1)], fill=w)
    elif kind == "drone":
        draw.rectangle([cx - r * 0.3, cy - r * 0.15, cx + r * 0.3, cy + r * 0.15],
                       fill=w)
        for sx in (-1, 1):
            draw.line([cx + sx * r * 0.25, cy - r * 0.15,
                       cx + sx * r * 0.7, cy - r * 0.45], fill=w, width=3)
            draw.line([cx + sx * r * 0.45, cy - r * 0.45,
                       cx + sx * r * 0.95, cy - r * 0.45], fill=w, width=4)
    elif kind == "factory":
        draw.rectangle([cx - r * 0.5, cy - r * 0.1, cx + r * 0.5, cy + r * 0.45],
                       fill=w)
        draw.polygon([(cx - r * 0.5, cy - r * 0.1), (cx - r * 0.25, cy - r * 0.4),
                      (cx, cy - r * 0.1), (cx + r * 0.25, cy - r * 0.4),
                      (cx + r * 0.5, cy - r * 0.1)], fill=w)
        draw.rectangle([cx + r * 0.3, cy - r * 0.55, cx + r * 0.5, cy + r * 0.1],
                       fill=w)
    elif kind == "gem":
        draw.polygon([(cx - r * 0.5, cy - r * 0.1), (cx - r * 0.2, cy - r * 0.45),
                      (cx + r * 0.2, cy - r * 0.45), (cx + r * 0.5, cy - r * 0.1),
                      (cx, cy + r * 0.5)], fill=w)
        draw.line([cx - r * 0.5, cy - r * 0.1, cx + r * 0.5, cy - r * 0.1],
                  fill=colour, width=2)
        draw.line([cx - r * 0.2, cy - r * 0.45, cx, cy + r * 0.5], fill=colour, width=2)
        draw.line([cx + r * 0.2, cy - r * 0.45, cx, cy + r * 0.5], fill=colour, width=2)


# ------------------------------------------------------------------ page
def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    draw.rectangle([0, 0, W, 168], fill=NAVY)
    draw.rectangle([0, 168, W, 174], fill=GOLD)
    f_kicker = font(F_BOLD, 25)
    letter_spaced(draw, "THE WORLD IN ONE DAY", f_kicker, 36, 26, GOLD, spacing=6)
    draw.text((W - 36 - draw.textlength("23 NOV 2026  •  MONDAY", font=f_kicker),
               26), "23 NOV 2026  •  MONDAY", font=f_kicker, fill=GOLD)
    f_date = font(F_BOLD, 54)
    draw.text((34, 62), "MONDAY 23 NOVEMBER 2026", font=f_date, fill=WHITE)
    f_sub = font(F_REG, 24)
    draw.text((36, 128), "Six stories that defined the day — from Antalya to Washington.",
              font=f_sub, fill=(205, 210, 220))

    # --- story grid ----------------------------------------------------
    margin, gap = 24, 16
    top, bottom = 190, 962
    cw = (W - 2 * margin - gap) // 2
    ch = (bottom - top - 2 * gap) // 3
    f_num = font(F_BOLD, 22)
    f_tag = font(F_BOLD, 19)
    f_head = font(F_BOLD, 29)
    f_body = font(F_REG, 21)
    f_src = font(F_REG, 16)

    for i, (headline, detail, source, tag, accent, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (cw + gap)
        y0 = top + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=(200, 192, 176), width=2)
        draw.rectangle([x0, y0, x1, y0 + 8], fill=accent)
        # number disc
        nx, ny = x0 + 34, y0 + 44
        draw.ellipse([nx - 17, ny - 17, nx + 17, ny + 17], fill=accent)
        draw.text((nx - draw.textlength(str(i + 1), font=f_num) / 2, ny - 13),
                  str(i + 1), font=f_num, fill=WHITE)
        draw.text((x0 + 62, y0 + 31), tag, font=f_tag, fill=accent)
        # pictogram, top right
        pictogram(draw, icon, x1 - 52, y0 + 48, 30, accent)
        # headline (up to 3 lines)
        text_w = cw - 48
        lines = wrap(draw, headline, f_head, text_w)[:3]
        y = draw_lines(draw, lines, f_head, x0 + 24, y0 + 80, INK, 34)
        # detail: only as many lines as fit above the source line
        dlines = wrap(draw, detail, f_body, text_w)
        room = (y1 - 32) - (y + 8)
        max_detail = max(1, room // 26)
        dlines = dlines[:max_detail]
        y = draw_lines(draw, dlines, f_body, x0 + 24, y + 8, (52, 58, 70), 26)
        # source
        draw.text((x0 + 24, y1 - 30), "Source: " + source, font=f_src, fill=GREY)

    # --- footer --------------------------------------------------------
    f_foot = font(F_REG, 17)
    foot = ("All six stories are from Monday 23 November 2026  •  "
            "make.fun bounty news-image-20261123")
    draw.text(((W - draw.textlength(foot, font=f_foot)) / 2, 976), foot,
              font=f_foot, fill=GREY)
    draw.rectangle([0, 0, W - 1, H - 1], outline=INK, width=3)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img = render()
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {img.size[0]}x{img.size[1]} "
          f"({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
