"""Render the 20 November 2026 world-news front page."""

import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
W = H = 1024
PAPER = "#FBF8F1"
WHITE = "#FFFFFF"
INK = "#14213D"
RED = "#C1272D"
MUTED = "#647184"
RULE = "#DAD4C9"
REGION_COLOURS = {
    "MIDDLE EAST": "#C1272D",
    "ASIA-PACIFIC": "#187B74",
    "AMERICAS": "#315FA3",
    "EUROPE": "#7B5AA6",
    "SCIENCE": "#B26B22",
    "AFRICA": "#3B8050",
    "BUSINESS": "#4B6278",
}
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap(draw, text, face, max_width):
    """Wrap words by measured pixel width."""
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and draw.textlength(candidate, font=face) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def fit_line(draw, text, max_width, start_size, min_size=9, bold=True):
    size = start_size
    while size > min_size and draw.textlength(text, font=font(size, bold)) > max_width:
        size -= 1
    return font(size, bold)


def draw_icon(draw, name, x, y, size, colour):
    """Small hand-drawn newspaper pictograms; all geometry stays in its box."""
    s = size / 48
    def p(px, py):
        return (round(x + px * s), round(y + py * s))
    def line(points, width=2):
        draw.line([p(a, b) for a, b in points], fill=colour, width=max(1, round(width * s)), joint="curve")
    def ellipse(box, outline=colour, fill=None, width=2):
        draw.ellipse((round(x + box[0]*s), round(y + box[1]*s), round(x + box[2]*s), round(y + box[3]*s)), outline=outline, fill=fill, width=max(1, round(width*s)))
    def rect(box, outline=colour, fill=None, width=2):
        draw.rectangle((round(x + box[0]*s), round(y + box[1]*s), round(x + box[2]*s), round(y + box[3]*s)), outline=outline, fill=fill, width=max(1, round(width*s)))

    if name == "missile":
        line([(10,34),(29,15),(37,12),(35,21),(16,40),(10,34)])
        line([(12,32),(7,27),(8,37),(17,42)])
        line([(29,15),(34,10),(40,9),(37,15)])
        line([(20,31),(25,36)])
    elif name == "gavel":
        line([(12,37),(37,37)], 3); line([(17,32),(32,17)], 5)
        line([(12,14),(20,6),(32,18),(24,26),(12,14)], 3)
    elif name == "chip":
        rect((11,11,37,37), width=3); rect((17,17,31,31), width=2)
        for k in (16,24,32):
            line([(k,5),(k,11)]); line([(k,37),(k,43)])
            line([(5,k),(11,k)]); line([(37,k),(43,k)])
    elif name == "explosion":
        line([(25,4),(27,17),(35,9),(32,21),(44,18),(36,27),(46,34),(33,33),(32,45),(25,35),(17,43),(19,31),(7,33),(15,25),(6,18),(19,20),(20,8),(25,17),(25,4)], 2)
        ellipse((21,21,29,29), fill=colour)
    elif name == "tanker":
        line([(5,30),(42,30),(36,38),(13,38),(5,30)], 2)
        rect((16,19,34,29), width=2); rect((20,13,29,18), width=2)
        line([(23,7),(23,12)]); line([(37,12),(37,23)]); line([(34,12),(40,12)])
    elif name == "ballot":
        rect((8,20,40,40), width=3); line([(8,24),(40,24)], 2)
        line([(17,20),(18,10),(31,10),(32,20)], 2)
        line([(17,30),(23,35),(34,27)], 3)
    elif name == "cyclone":
        for r in (17,12,7): ellipse((24-r,24-r,24+r,24+r), width=2)
        line([(24,24),(33,22),(37,17)], 2)
    elif name == "chart":
        line([(8,7),(8,40),(42,40)], 2); line([(12,13),(20,18),(26,17),(36,30),(42,34)], 3)
        line([(36,30),(36,23)]); line([(36,30),(43,28)], 2)
    elif name == "drone":
        ellipse((19,18,29,28), width=2); line([(21,20),(12,11)]); line([(27,20),(36,11)]); line([(21,26),(12,36)]); line([(27,26),(36,36)])
        for cx, cy in ((7,8),(33,8),(7,33),(33,33)):
            ellipse((cx-5,cy-2,cx+5,cy+2), width=2)
        line([(23,28),(21,35),(26,40)])
    elif name == "handshake":
        line([(5,20),(15,13),(23,19),(29,14),(43,22)], 3)
        line([(5,20),(16,34),(21,30),(26,35),(30,31),(35,34),(43,24)], 3)
        line([(16,25),(23,31),(29,25),(35,29)], 2)
    elif name == "aid":
        rect((8,15,40,39), width=3); line([(8,22),(40,22)], 2)
        line([(24,24),(24,35)], 4); line([(18,30),(30,30)], 4)
        line([(17,15),(17,9),(31,9),(31,15)], 2)
    elif name == "telescope":
        line([(12,15),(37,10),(40,20),(15,26),(12,15)], 3)
        line([(23,24),(19,39)]); line([(28,23),(34,39)]); line([(14,38),(38,38)])
        line([(7,10),(4,6)]); line([(6,20),(2,20)]); line([(42,7),(45,3)])


def draw_card(draw, card, x, y, w, h):
    colour = REGION_COLOURS.get(card["region"], "#596B7C")
    draw.rounded_rectangle((x, y, x+w, y+h), radius=7, fill=WHITE, outline=RULE, width=1)
    draw.rounded_rectangle((x, y, x+w, y+7), radius=4, fill=colour)
    draw.rectangle((x, y+4, x+w, y+7), fill=colour)
    draw.text((x+11, y+13), f"{card['n']:02d}", font=font(13, True), fill=RED)
    draw.text((x+43, y+15), card["region"], font=font(9, True), fill=colour)
    draw_icon(draw, card["icon"], x+10, y+35, 39, colour)
    hx, hy, hw = x+57, y+32, w-68
    headline_font = font(14, True)
    headline_lines = wrap(draw, card["headline"], headline_font, hw)
    if len(headline_lines) > 3:
        headline_font = font(13, True)
        headline_lines = wrap(draw, card["headline"], headline_font, hw)
    for i, line in enumerate(headline_lines[:3]):
        draw.text((hx, hy+i*16), line, font=headline_font, fill=INK)
    detail_font = font(9)
    detail_lines = wrap(draw, card["detail"], detail_font, w-22)
    dy = y+82
    for i, line in enumerate(detail_lines[:3]):
        draw.text((x+11, dy+i*12), line, font=detail_font, fill=MUTED)


def render():
    data = json.loads((ROOT / "stories.json").read_text(encoding="utf-8"))
    cards, briefs = data["cards"], data["briefs"]
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    # Masthead: newspaper identity, dominant date, and a precise coverage line.
    d.text((24, 16), "THE WORLD IN ONE IMAGE", font=font(17, True), fill=INK)
    date = "FRIDAY 20 NOVEMBER 2026"
    date_font = fit_line(d, date, 976, 47, 39)
    d.text((22, 39), date, font=date_font, fill=INK)
    regions = len({c["region"] for c in cards} | {b["region"] for b in briefs})
    fields = len({c["field"] for c in cards} | {b["field"] for b in briefs})
    total = len(cards) + len(briefs)
    subtitle = f"{total} STORIES  ·  {regions} REGIONS  ·  {fields} FIELDS  ·  EVERYTHING BELOW HAPPENED, OR WAS FIRST REPORTED, TODAY"
    subfont = fit_line(d, subtitle, 976, 13, 10, bold=False)
    d.text((24, 103), subtitle, font=subfont, fill=MUTED)
    d.rectangle((24, 128, 1000, 134), fill=RED)

    # Twelve concise visual lead stories.
    margin, gap, card_h = 24, 9, 116
    card_w = (W-2*margin-3*gap)//4
    for i, item in enumerate(cards):
        row, col = divmod(i, 4)
        draw_card(d, item, margin+col*(card_w+gap), 147+row*(card_h+8), card_w, card_h)

    # Geography tally reflects the entire day's selection.
    tally = Counter(b["region"] for b in briefs)
    tally.update(c["region"] for c in cards)
    region_text = "  ·  ".join(f"{name} {count}" for name, count in sorted(tally.items()))
    d.text((24, 526), "WHERE IT HAPPENED", font=font(11, True), fill=RED)
    d.text((176, 526), region_text, font=fit_line(d, region_text, 800, 10, 8, bold=True), fill=INK)

    # Briefs in three newspaper columns. Each row gets a measured two-line cell.
    d.line((24, 550, 1000, 550), fill=RULE, width=1)
    d.text((24, 556), "MORE OF THE DAY", font=font(14, True), fill=INK)
    d.text((806, 559), f"BRIEFS 13–{12+len(briefs)}", font=font(10, True), fill=MUTED)
    col_gap, cell_w, row_h = 17, (976-34)//3, 27
    start_y = 580
    brief_font = font(9)
    for i, brief in enumerate(briefs):
        col, row = divmod(i, 9)
        x, y = 24+col*(cell_w+col_gap), start_y+row*row_h
        n = 13+i
        d.text((x, y), f"{n:02d}", font=font(9, True), fill=RED)
        lines = wrap(d, brief["text"], brief_font, cell_w-29)
        for j, line in enumerate(lines[:2]):
            d.text((x+25, y+j*11), line, font=brief_font, fill=INK)
        d.line((x, y+row_h-2, x+cell_w, y+row_h-2), fill="#E9E4DA", width=1)

    # Six large-number summaries in a single, calm band.
    band_y, band_h = 831, 76
    d.rounded_rectangle((24, band_y, 1000, band_y+band_h), radius=7, fill="#F1EEE7")
    d.text((37, band_y+8), "THE DAY IN NUMBERS", font=font(11, True), fill=RED)
    slot = 157
    for i, (value, caption) in enumerate(data["numbers"]):
        x = 37+i*slot
        value_font = fit_line(d, value, slot-12, 24, 16, bold=True)
        d.text((x, band_y+24), value, font=value_font, fill=INK)
        cap_font = font(8)
        cap_lines = wrap(d, caption, cap_font, slot-12)
        for j, line in enumerate(cap_lines[:2]):
            d.text((x, band_y+52+j*10), line, font=cap_font, fill=MUTED)
        if i:
            d.line((x-10, band_y+21, x-10, band_y+65), fill=RULE, width=1)

    # Explicitly separates today's reporting from nearby older headlines.
    panel = (24, 918, 1000, 1004)
    d.rounded_rectangle(panel, radius=7, fill="#F8E7E4", outline=RED, width=1)
    d.text((38, 928), "DATE CHECK — CHECKED AND LEFT OUT AS NOT 20 NOVEMBER NEWS:", font=font(12, True), fill=RED)
    check_font = font(10)
    check_lines = wrap(d, data["date_check"], check_font, 940)
    for i, line in enumerate(check_lines[:4]):
        d.text((38, 950+i*13), line, font=check_font, fill=INK)
    d.text((24, 1008), "WORLD DESK  /  FRIDAY EDITION", font=font(8, True), fill=MUTED)
    d.text((887, 1008), "20 NOV 2026  ·  01", font=font(8, True), fill=MUTED)

    im.save(ROOT / "entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    render()
