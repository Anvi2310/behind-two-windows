"""
deckimgs.py — gather every picture the presentation needs:
storyboard thumbnails from the finished shots, a hero cover frame, a look-dev before/after,
and a pipeline diagram drawn with PIL.
"""
import os, subprocess, glob, math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
IMG = os.path.join(HERE, "deck", "img")
PREV = os.path.join(HERE, "preview")
os.makedirs(IMG, exist_ok=True)
FD = "/usr/share/fonts/opentype/inter/"

SHOT_GRABS = {           # shot -> seconds into that shot to grab
    "S01": 14.0, "S02": 11.0, "S03": 10.5, "S04": 12.5, "S05": 3.0,
    "S06": 13.5, "S07": 13.0, "S08": 11.0, "S09": 9.5, "S10": 15.0,
}
HERO = ("S09", 9.0)


def grab(shot, t, out, w=1920):
    src = os.path.join(BUILD, f"{shot}.mp4")
    if not os.path.exists(src):
        fb = sorted(glob.glob(os.path.join(PREV, f"{shot}_*.jpg")))
        if fb:
            Image.open(fb[-1]).save(out, quality=92)
            return out
        return None
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src,
                           "-frames:v", "1", "-vf", f"scale={w}:-2", "-q:v", "2", out])
    return out


def storyboard():
    for s, t in SHOT_GRABS.items():
        grab(s, t, os.path.join(IMG, f"sb_{s}.jpg"), 1280)
    grab(*HERO, out=os.path.join(IMG, "cover.jpg")) if False else grab(HERO[0], HERO[1], os.path.join(IMG, "cover.jpg"))
    grab("S01", 15.5, os.path.join(IMG, "city.jpg"))
    grab("S06", 14.0, os.path.join(IMG, "encounter.jpg"))
    grab("S10", 17.5, os.path.join(IMG, "close.jpg"))


def look_compare():
    """Raw Workbench render (transparent film) next to the finished graded frame."""
    raw = os.path.join(PREV, "_S02_raw.png")
    if os.path.exists(raw):
        im = Image.open(raw).convert("RGBA")
        bg = Image.new("RGBA", im.size, (28, 32, 40, 255))
        bg.alpha_composite(im)
        bg.convert("RGB").resize((1280, 720)).save(os.path.join(IMG, "look_raw.jpg"), quality=92)
    g = grab("S02", 11.0, os.path.join(IMG, "look_graded.jpg"), 1280)
    return g


def pipeline_diagram():
    W, H = 2200, 560
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    f_n = ImageFont.truetype(FD + "Inter-ExtraBold.otf", 34)
    f_t = ImageFont.truetype(FD + "Inter-Bold.otf", 34)
    f_b = ImageFont.truetype(FD + "Inter-Medium.otf", 23)
    steps = [
        ("1", "Script", ["10 narration lines", "written to the", "SDG 10 brief"], (224, 164, 59)),
        ("2", "Voice", ["Kokoro-82M neural", "TTS, offline ONNX", "-> 10 WAV + lengths"], (46, 196, 182)),
        ("3", "Timeline", ["shot lengths set", "from voice lengths", "10 shots = 2:47"], (155, 123, 255)),
        ("4", "3D build", ["Blender bpy: rigs,", "sets, props, cameras", "all from code"], (123, 228, 149)),
        ("5", "Render", ["Workbench engine,", "transparent film,", "1280x720 @ 24fps"], (255, 107, 107)),
        ("6", "Composite", ["sky, haze, bloom,", "grade, grain ->", "upscaled to 1080p"], (94, 184, 255)),
        ("7", "Mix & edit", ["xfades, titles,", "score + SFX ducked", "under narration"], (255, 201, 60)),
    ]
    bw, gap = 272, 36
    x0 = (W - (len(steps) * bw + (len(steps) - 1) * gap)) // 2
    for i, (num, title, lines, col) in enumerate(steps):
        x = x0 + i * (bw + gap)
        d.rounded_rectangle([x, 120, x + bw, 470], 22, fill=(243, 245, 249))
        d.ellipse([x + 22, 146, x + 82, 206], fill=col)
        tw = d.textlength(num, font=f_n)
        d.text((x + 52 - tw / 2, 158), num, font=f_n, fill=(12, 18, 28))
        d.text((x + 22, 226), title, font=f_t, fill=col)
        for j, ln in enumerate(lines):
            d.text((x + 22, 282 + j * 34), ln, font=f_b, fill=(58, 68, 84))
        if i < len(steps) - 1:
            ax = x + bw + 6
            d.polygon([(ax, 285), (ax + 20, 295), (ax, 305)], fill=(138, 152, 173))
            d.line([(ax - 4, 295), (ax + 16, 295)], fill=(138, 152, 173), width=4)
    p = os.path.join(IMG, "pipeline.png")
    im.save(p)
    return p


def rig_diagram():
    W, H = 1200, 1000
    im = Image.new("RGB", (W, H), (11, 21, 38))
    d = ImageDraw.Draw(im)
    f_t = ImageFont.truetype(FD + "Inter-Bold.otf", 26)
    f_b = ImageFont.truetype(FD + "Inter-Medium.otf", 21)
    nodes = {
        "root": (600, 70), "pelvis": (600, 170), "spine": (600, 270), "neck": (600, 370),
        "head": (600, 470), "l_sh": (380, 330), "l_elb": (300, 430), "r_sh": (820, 330),
        "r_elb": (900, 430), "l_hip": (430, 560), "l_knee": (430, 680),
        "r_hip": (770, 560), "r_knee": (770, 680),
    }
    edges = [("root", "pelvis"), ("pelvis", "spine"), ("spine", "neck"), ("neck", "head"),
             ("spine", "l_sh"), ("l_sh", "l_elb"), ("spine", "r_sh"), ("r_sh", "r_elb"),
             ("pelvis", "l_hip"), ("l_hip", "l_knee"), ("pelvis", "r_hip"), ("r_hip", "r_knee")]
    for a, b in edges:
        d.line([nodes[a], nodes[b]], fill=(70, 92, 124), width=4)
    for name, (x, y) in nodes.items():
        col = (224, 164, 59) if name in ("root", "pelvis", "spine") else (46, 196, 182)
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col)
        tw = d.textlength(name, font=f_b)
        d.text((x - tw / 2, y + 20), name, font=f_b, fill=(214, 226, 240))
    d.text((40, 806), "Every joint is an empty; meshes hang off it.", font=f_t, fill=(246, 242, 232))
    d.text((40, 850), "Animation = keyframed euler rotations on these 13 joints,", font=f_b, fill=(160, 176, 198))
    d.text((40, 884), "so the two leads are literally the same object in every shot —", font=f_b, fill=(160, 176, 198))
    d.text((40, 918), "faces, clothing and proportions can never drift between scenes.", font=f_b, fill=(160, 176, 198))
    p = os.path.join(IMG, "rig.png")
    im.save(p)
    return p


if __name__ == "__main__":
    storyboard()
    look_compare()
    print(pipeline_diagram())
    print(rig_diagram())
    print("images in", IMG)
