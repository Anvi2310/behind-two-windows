"""
titles.py — title and end-credit cards for "BEHIND TWO WINDOWS", drawn as transparent PNGs
and composited over the film by FFmpeg.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "titles")
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
FDIR = "/usr/share/fonts/opentype/inter/"

CREAM = (247, 242, 232, 255)
AMBER = (232, 186, 106, 255)
TEAL = (142, 206, 200, 255)
SOFT = (214, 214, 206, 255)


def font(weight, size):
    return ImageFont.truetype(FDIR + f"Inter-{weight}.otf", size)


def draw_text(d, text, cx, y, f, fill, spacing=0, shadow=True):
    if spacing:
        widths = [d.textlength(ch, font=f) for ch in text]
        total = sum(widths) + spacing * (len(text) - 1)
        x = cx - total / 2
        for ch, w in zip(text, widths):
            if shadow:
                d.text((x + 3, y + 3), ch, font=f, fill=(8, 12, 20, 150))
            d.text((x, y), ch, font=f, fill=fill)
            x += w + spacing
    else:
        w = d.textlength(text, font=f)
        if shadow:
            d.text((cx - w / 2 + 3, y + 3), text, font=f, fill=(8, 12, 20, 150))
        d.text((cx - w / 2, y), text, font=f, fill=fill)


def card(name, lines):
    """lines: list of (text, weight, size, colour, y, spacing)"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for text, weight, size, fill, y, sp in lines:
        draw_text(d, text, W / 2, y, font(weight, size), fill, sp)
    p = os.path.join(OUT, f"{name}.png")
    im.save(p)
    return p


def build_all():
    made = {}
    # opening title
    made["t_main"] = card("t_main", [
        ("BEHIND TWO WINDOWS", "ExtraBold", 104, CREAM, 430, 10),
        ("Different beginnings.   Equal dreams.   One shared future.", "Medium", 36, AMBER, 580, 2),
    ])
    # end cards
    made["e_title"] = card("e_title", [
        ("BEHIND TWO WINDOWS", "ExtraBold", 92, CREAM, 360, 8),
        ("SDG 10  ·  REDUCED INEQUALITIES", "Bold", 38, AMBER, 490, 6),
    ])
    made["e_tag"] = card("e_tag", [
        ("Different beginnings.", "SemiBold", 56, CREAM, 350, 2),
        ("Equal dreams.", "SemiBold", 56, CREAM, 430, 2),
        ("One shared future.", "SemiBold", 56, AMBER, 510, 2),
    ])
    made["e_credit"] = card("e_credit", [
        ("CREATED AND PRESENTED BY", "Bold", 32, SOFT, 330, 8),
        ("ANVITH  &  HITESH", "ExtraBold", 86, CREAM, 390, 6),
        ("“Because everyone deserves a fair chance.”", "Medium", 40, AMBER, 540, 1),
        ("Computer Graphics and Animation  ·  LLT-1", "Medium", 24, SOFT, 640, 2),
    ])
    return made


if __name__ == "__main__":
    for k, v in build_all().items():
        print(k, v)
