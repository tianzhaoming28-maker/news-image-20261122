#!/usr/bin/env python3
"""Front page for Sunday 22 November 2026.

Eight stories from the day, drawn as a newspaper front page with
Pillow primitives only — no photos, no outside assets. The lead panel
carries the COP31 collapse in Antalya; three panels below it cover
Bahrain, the Dymer drone strike and the Indonesian factory fire; the
bottom row covers BepiColombo, the Putin "friend" row, West Bank
arson and Shuri Castle.

Run from this directory: writes entry.png next to itself.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (16, 16, 18)
MUTE = (96, 90, 82)
CARD = (255, 253, 246)
SAND = (236, 230, 214)
RED = (176, 32, 38)
NAVY = (26, 70, 138)
TEAL = (13, 112, 104)
GOLD = (188, 132, 16)
GREEN = (36, 106, 50)
PLUM = (92, 50, 138)
RUST = (206, 92, 18)
CREAM = (240, 220, 150)

FONTS = Path("/usr/share/fonts/truetype/dejavu")


def load(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def serif(size):
    return load("DejaVuSerif-Bold.ttf", size)


def bold(size):
    return load("DejaVuSans-Bold.ttf", size)


def plain(size):
    return load("DejaVuSans.ttf", size)


def wrap(draw, text, font, width):
    """Greedy word wrap, returns the lines that fit in width pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, fill, width, lead=4):
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + lead
    return y


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def panel(self, x0, y0, x1, y1, accent):
        self.d.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=2)
        self.d.rectangle([x0, y0, x1, y0 + 7], fill=accent)

    def kicker(self, x, y, text, color):
        self.d.text((x, y), text, font=bold(14), fill=color)
        return y + 20

    def headline(self, x, y, text, size, width):
        return para(self.d, x, y, text, bold(size), INK, width, lead=2)

    def sub(self, x, y, text, size, width):
        return para(self.d, x, y, text, plain(size), MUTE, width, lead=3)

    def chip(self, x, y, text):
        w = self.d.textlength(text, font=bold(14)) + 22
        self.d.rectangle([x, y, x + w, y + 30], fill=SAND, outline=INK,
                         width=2)
        self.d.text((x + 11, y + 8), text, font=bold(14), fill=INK)
        return x + w + 10


def globe_crack(d, cx, cy):
    """A globe split by a jagged crack, with a rising thermometer."""
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], outline=INK, width=4)
    d.ellipse([cx - 26, cy - 52, cx + 26, cy + 52], outline=INK, width=2)
    d.line([cx - 52, cy, cx + 52, cy], fill=INK, width=2)
    d.line([cx - 44, cy - 28, cx + 44, cy - 28], fill=INK, width=2)
    crack = [(cx - 8, cy - 52), (cx + 6, cy - 26), (cx - 10, cy - 2),
             (cx + 8, cy + 22), (cx - 4, cy + 52)]
    d.line(crack, fill=RED, width=5)
    d.line([cx + 66, cy - 44, cx + 66, cy + 34], fill=INK, width=4)
    d.ellipse([cx + 56, cy + 26, cx + 76, cy + 46], fill=RED, outline=INK,
              width=3)
    d.line([cx + 66, cy + 30, cx + 66, cy - 30], fill=RED, width=4)


def flame_burst(d, cx, cy):
    """Factory block under a flame."""
    d.rectangle([cx - 46, cy - 6, cx + 46, cy + 30], fill=INK)
    d.rectangle([cx - 30, cy - 30, cx - 14, cy - 6], fill=INK)
    d.rectangle([cx + 18, cy - 22, cx + 30, cy - 6], fill=INK)
    pts = [(cx - 18, cy - 30), (cx - 4, cy - 58), (cx + 8, cy - 36),
           (cx + 20, cy - 52), (cx + 16, cy - 26)]
    d.polygon(pts, fill=RUST)
    d.ellipse([cx - 52, cy - 44, cx - 36, cy - 28], fill=MUTE)
    d.line([cx - 52, cy + 36, cx + 52, cy + 36], fill=TEAL, width=3)


def tower_crack(d, cx, cy):
    """A tower block split open, rubble at its base."""
    d.rectangle([cx - 34, cy - 44, cx + 34, cy + 34], fill=SAND,
                outline=INK, width=3)
    for yy in (-28, -8, 12):
        d.line([cx - 34, cy + yy, cx + 34, cy + yy], fill=INK, width=2)
    for xx in (-16, 4):
        for yy in (-40, -20, 0, 20):
            d.rectangle([cx + xx, cy + yy, cx + xx + 10, cy + yy + 8],
                        fill=NAVY)
    d.line([(cx, cy - 44), (cx + 8, cy - 18), (cx - 4, cy + 6),
            (cx + 6, cy + 34)], fill=RED, width=4)
    d.polygon([(cx - 46, cy + 34), (cx - 28, cy + 22), (cx - 10, cy + 34),
               (cx + 8, cy + 24), (cx + 26, cy + 34), (cx + 46, cy + 34)],
              fill=INK)


def factory_fire(d, cx, cy):
    """A candy factory with smoking chimney and flame."""
    d.rectangle([cx - 48, cy - 4, cx + 48, cy + 30], fill=SAND,
                outline=INK, width=3)
    d.rectangle([cx + 28, cy - 40, cx + 44, cy - 4], fill=INK)
    d.ellipse([cx + 20, cy - 58, cx + 40, cy - 38], fill=MUTE)
    d.ellipse([cx + 34, cy - 70, cx + 52, cy - 52], fill=MUTE)
    d.rectangle([cx - 38, cy + 6, cx - 22, cy + 18], fill=RED)
    d.rectangle([cx - 12, cy + 6, cx + 4, cy + 18], fill=RED)
    d.rectangle([cx + 14, cy + 6, cx + 30, cy + 18], fill=RED)
    d.polygon([(cx - 20, cy - 4), (cx - 6, cy - 28), (cx + 4, cy - 10),
               (cx + 16, cy - 24), (cx + 12, cy - 4)], fill=RUST)


def orbit_planet(d, cx, cy):
    """A small cratered planet on a tilted orbit ring."""
    d.ellipse([cx - 62, cy - 18, cx + 62, cy + 18], outline=INK, width=3)
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=RUST,
              outline=INK, width=3)
    d.ellipse([cx - 14, cy - 12, cx - 4, cy - 2], fill=RED)
    d.ellipse([cx + 6, cy + 6, cx + 14, cy + 14], fill=RED)
    d.ellipse([cx + 52, cy - 22, cx + 58, cy - 16], fill=GOLD)
    d.ellipse([cx - 58, cy + 12, cx - 52, cy + 18], fill=GOLD)
    d.text((cx - 40, cy + 34), "MERCURY", font=bold(13), fill=INK)


def bubble_slash(d, cx, cy):
    """A speech bubble saying FRIEND, crossed out in red."""
    d.rectangle([cx - 52, cy - 34, cx + 52, cy + 22], fill=CARD,
                outline=INK, width=3)
    d.polygon([(cx - 24, cy + 22), (cx - 34, cy + 40), (cx - 6, cy + 22)],
              fill=CARD, outline=INK)
    d.text((cx - 42, cy - 20), '"FRIEND"', font=bold(17), fill=INK)
    d.line([cx - 52, cy - 34, cx + 52, cy + 22], fill=RED, width=5)
    d.text((cx - 34, cy + 44), "NOT A FRIEND", font=bold(13), fill=RED)


def burning_car(d, cx, cy):
    """A car body with two wheels and a flame on its roof."""
    d.rectangle([cx - 48, cy - 6, cx + 48, cy + 16], fill=INK)
    d.polygon([(cx - 30, cy - 6), (cx - 18, cy - 24), (cx + 18, cy - 24),
               (cx + 30, cy - 6)], fill=INK)
    d.ellipse([cx - 38, cy + 12, cx - 16, cy + 34], fill=CARD,
              outline=INK, width=3)
    d.ellipse([cx + 16, cy + 12, cx + 38, cy + 34], fill=CARD,
              outline=INK, width=3)
    d.polygon([(cx - 12, cy - 24), (cx - 2, cy - 48), (cx + 6, cy - 30),
               (cx + 14, cy - 44), (cx + 12, cy - 24)], fill=RUST)


def castle(d, cx, cy):
    """Shuri Castle's red main hall: stacked roofs, pillars, steps."""
    d.rectangle([cx - 44, cy + 18, cx + 44, cy + 34], fill=RED,
                outline=INK, width=3)
    for xx in (-32, -10, 12, 30):
        d.line([cx + xx, cy + 18, cx + xx, cy + 34], fill=INK, width=2)
    d.polygon([(cx - 56, cy + 18), (cx, cy - 2), (cx + 56, cy + 18)],
              fill=RED, outline=INK)
    d.rectangle([cx - 30, cy - 18, cx + 30, cy - 2], fill=RED,
                outline=INK, width=3)
    d.polygon([(cx - 40, cy - 18), (cx, cy - 32), (cx + 40, cy - 18)],
              fill=RED, outline=INK)
    d.line([cx - 52, cy + 40, cx + 52, cy + 40], fill=INK, width=3)
    d.line([cx - 44, cy + 46, cx + 44, cy + 46], fill=INK, width=3)


ICONS = {"globe": globe_crack, "flame": flame_burst, "tower": tower_crack,
         "factory": factory_fire, "orbit": orbit_planet,
         "bubble": bubble_slash, "car": burning_car, "castle": castle}

# (box, accent, kicker, headline, subline, icon, head size, sub size,
#  text width, icon centre)
TOP3 = [
    ((24, 396, 336, 652), RUST, "GULF  ·  BAHRAIN",
     "IRAN STRIKES BAHRAIN PLANT; 2 HURT",
     "Missiles hit a civilian industrial site on Sitra; one man is "
     "critical. Two tankers also hit in Hormuz.", "flame", 21, 15, 276,
     (180, 596)),
    ((348, 396, 660, 652), NAVY, "WAR  ·  DYMER, KYIV REGION",
     "DRONE LEVELS KYIV FLATS; 3 KILLED",
     "A Russian drone tears through a five-storey block; 14 missing "
     "as rescuers dig through the rubble.", "tower", 21, 15, 276,
     (504, 596)),
    ((672, 396, 1000, 652), RED, "DISASTER  ·  BANTEN, INDONESIA",
     "CANDY FACTORY FIRE: 3 DEAD, 37 MISSING",
     "Blaze sweeps a Milkita sweets plant; 300 workers were inside "
     "when it caught fire.", "factory", 21, 15, 292, (836, 596)),
]

BOTTOM4 = [
    ((24, 664, 270, 924), PLUM, "SPACE  ·  MERCURY",
     "BEPICOLOMBO REACHES MERCURY",
     "After eight years, the ESA-JAXA probe slips into orbit — but a "
     "thruster glitch shortens its burn.", "orbit", 20, 14, 210,
     (147, 872)),
    ((282, 664, 528, 924), TEAL, "DIPLOMACY  ·  WASHINGTON",
     "SPY CHIEF: PUTIN 'NOT A FRIEND'",
     "US intelligence chief rebukes Trump days after the president "
     "called Putin 'my friend'.", "bubble", 20, 14, 210, (405, 862)),
    ((540, 664, 786, 924), GOLD, "WEST BANK  ·  RAMALLAH",
     "SETTLERS TORCH 12 CARS IN WEST BANK",
     "Arson hits four villages; Israel opens an inquiry as Eisenkot "
     "calls it 'Jewish terrorism'.", "car", 20, 14, 210, (663, 872)),
    ((798, 664, 1000, 924), GREEN, "CULTURE  ·  OKINAWA",
     "SHURI CASTLE RISES AGAIN",
     "Seven years after fire, Okinawa's royal hall reopens, rebuilt "
     "with sprinklers and old pigments.", "castle", 20, 14, 170,
     (899, 872)),
]


def render():
    p = Page()
    d = p.d

    # Masthead: black band, paper title, red date.
    d.rectangle([0, 0, 1024, 140], fill=INK)
    d.text((34, 12), "THE WORLD IN ONE IMAGE  ·  GLOBAL FRONT PAGE",
           font=bold(18), fill=CREAM)
    d.text((32, 36), "SUNDAY", font=serif(52), fill=(255, 255, 255))
    d.text((32, 92), "22 NOVEMBER 2026", font=serif(38),
           fill=(255, 96, 96))
    d.text((700, 44), "ONE DAY.", font=serif(30), fill=(255, 255, 255))
    d.text((700, 82), "EIGHT STORIES.", font=serif(30),
           fill=(255, 255, 255))
    d.rectangle([0, 140, 1024, 148], fill=RED)

    # Lead: COP31 collapses in Antalya.
    p.panel(24, 160, 1000, 384, RED)
    y = p.kicker(44, 174, "LEAD  ·  COP31, ANTALYA, TURKEY  ·  CLIMATE",
                 RED)
    y = p.headline(44, y, "COP31 COLLAPSES: NO DEAL ON FOSSIL FUELS",
                   30, 560)
    y = p.sub(44, y + 6,
              "After the longest COP in history, 194 nations reject the "
              "'Antalya Pact' — a deal that never even mentions fossil "
              "fuels.", 17, 560)
    globe_crack(d, 852, 268)
    x = 44
    for chip in ("NO DEAL", "LONGEST COP EVER", "194 NATIONS"):
        x = p.chip(x, 322, chip)
    d.text((44, 362), "EU: 'WE WILL NOT ENDORSE A DEAL THAT DOES NOT "
           "EVEN MENTION FOSSIL FUELS'", font=bold(13), fill=MUTE)

    # Three mid-size stories.
    for box, accent, kick, head, sub, icon, hs, ss, w, (ix, iy) in TOP3:
        p.panel(*box, accent)
        y = p.kicker(box[0] + 18, box[1] + 12, kick, accent)
        y = p.headline(box[0] + 18, y, head, hs, w)
        p.sub(box[0] + 18, y + 2, sub, ss, w)
        ICONS[icon](d, ix, iy)

    # Four bottom stories.
    for box, accent, kick, head, sub, icon, hs, ss, w, (ix, iy) in BOTTOM4:
        p.panel(*box, accent)
        y = p.kicker(box[0] + 16, box[1] + 12, kick, accent)
        y = p.headline(box[0] + 16, y, head, hs, w)
        p.sub(box[0] + 16, y + 2, sub, ss, w)
        ICONS[icon](d, ix, iy)

    # Footer: black band repeating the date and the story list.
    d.rectangle([0, 936, 1024, 1024], fill=INK)
    d.text((34, 948), "SUNDAY 22 NOVEMBER 2026 -- THE DAY IN ONE IMAGE",
           font=bold(19), fill=(255, 255, 255))
    d.text((34, 978),
           "COP31  ·  Bahrain  ·  Dymer  ·  Factory fire  ·  "
           "BepiColombo  ·  Putin row  ·  West Bank  ·  Shuri Castle",
           font=plain(15), fill=(220, 214, 195))
    return p.img


if __name__ == "__main__":
    target = Path(__file__).with_name("entry.png")
    render().save(target, format="PNG", optimize=True)
    print(target, target.stat().st_size)
