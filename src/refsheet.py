"""
refsheet.py — character reference sheets for Aarav and Maya.
Renders front / three-quarter / side / back turnarounds and composes a labelled sheet.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from rig import make_aarav, make_maya, D
import sets as S
from look import setup_scene, set_light

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "refs")
os.makedirs(OUT, exist_ok=True)
ANGLES = [("front", 0), ("three_quarter", 35), ("side", 90), ("back", 180)]


def clear():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def shoot(who):
    for name, ang in ANGLES:
        clear()
        S.ground("g", 60, (0.80, 0.78, 0.73, 1))
        ch = make_aarav(loc=(0, 0, 0)) if who == "aarav" else make_maya(loc=(0, 0, 0))
        ch.pose(1, l_sh=(0, 16, 0), r_sh=(0, -16, 0), l_elb=(8, 0, 0), r_elb=(8, 0, 0))
        sc = setup_scene(aa='16', transparent=True, res=(700, 1000))
        set_light(-40)
        r = 3.1
        a = math.radians(ang)
        cam = S.camera("cam", (math.sin(a) * r, -math.cos(a) * r, 0.80), (0, 0, 0.72), lens=52)
        sc.render.filepath = os.path.join(OUT, f"{who}_{name}.png")
        bpy.ops.render.render(write_still=True)
        print("  ", sc.render.filepath)


def compose():
    from PIL import Image, ImageDraw, ImageFont
    FD = "/usr/share/fonts/opentype/inter/"
    f_title = ImageFont.truetype(FD + "Inter-ExtraBold.otf", 46)
    f_lab = ImageFont.truetype(FD + "Inter-SemiBold.otf", 22)
    f_note = ImageFont.truetype(FD + "Inter-Medium.otf", 20)
    notes = {
        "aarav": ["AARAV  ·  age 11", "Short black hair  ·  blue casual shirt",
                  "Beige trousers  ·  white sneakers",
                  "Lives in a comfortable modern home with books, a laptop and support"],
        "maya": ["MAYA  ·  age 11", "Long black hair in a ponytail  ·  yellow kurta",
                 "Dark blue trousers  ·  sandals",
                 "Lives in a modest home; builds her science project from recycled materials"],
    }
    for who in ("aarav", "maya"):
        tiles = [Image.open(os.path.join(OUT, f"{who}_{n}.png")).convert("RGBA") for n, _ in ANGLES]
        tw, th = tiles[0].size
        sheet = Image.new("RGB", (tw * 4 + 60, th + 268), (244, 240, 232))
        d = ImageDraw.Draw(sheet)
        d.rectangle([0, 0, sheet.width, 96], fill=(22, 36, 56))
        d.text((30, 26), notes[who][0], font=f_title, fill=(246, 242, 232))
        for i, (t, (nm, _)) in enumerate(zip(tiles, ANGLES)):
            x = 30 + i * tw
            bg = Image.new("RGBA", t.size, (232, 228, 219, 255))
            bg.alpha_composite(t)
            sheet.paste(bg.convert("RGB"), (x, 110))
            w = d.textlength(nm.replace("_", " ").upper(), font=f_lab)
            d.text((x + tw / 2 - w / 2, 110 + th + 8), nm.replace("_", " ").upper(),
                   font=f_lab, fill=(60, 70, 86))
        for j, line in enumerate(notes[who][1:]):
            d.text((30, 110 + th + 46 + j * 28), line, font=f_note, fill=(52, 62, 78))
        p = os.path.join(OUT, f"character_reference_{who}.png")
        sheet.save(p, quality=95)
        print(p)


if __name__ == "__main__":
    for who in ("aarav", "maya"):
        shoot(who)
    compose()
