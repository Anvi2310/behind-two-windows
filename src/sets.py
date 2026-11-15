"""
sets.py — environments and props for "BEHIND TWO WINDOWS".
Everything is built from primitives with per-object colours (Workbench OBJECT colour mode).
"""
import bpy, math, random
from mathutils import Euler
from rig import ball, box, tube, plane, empty, D, TAU

# ---------------------------------------------------------------- palettes
GROUND_WARM = (0.78, 0.73, 0.64, 1)
GROUND_COOL = (0.62, 0.65, 0.62, 1)
ROAD = (0.33, 0.33, 0.35, 1)
ROAD_LINE = (0.88, 0.86, 0.78, 1)
WALL_RICH = (0.88, 0.86, 0.82, 1)
WALL_MODEST = (0.80, 0.74, 0.66, 1)
FLOOR_RICH = (0.72, 0.60, 0.46, 1)
FLOOR_MODEST = (0.66, 0.62, 0.56, 1)
WOOD = (0.62, 0.44, 0.28, 1)
WOOD_DARK = (0.42, 0.29, 0.19, 1)
METAL = (0.55, 0.58, 0.62, 1)
TEAL = (0.30, 0.58, 0.58, 1)
GLASS = (0.72, 0.84, 0.90, 1)
SCREEN_ON = (0.55, 0.78, 0.92, 1)
PAPER = (0.95, 0.93, 0.88, 1)
CARD = (0.72, 0.56, 0.38, 1)
LEAF = (0.36, 0.52, 0.32, 1)
LEAF2 = (0.44, 0.60, 0.36, 1)
TRUNK = (0.40, 0.31, 0.24, 1)
BOOK_COLORS = [(0.80, 0.26, 0.30, 1), (0.25, 0.45, 0.72, 1), (0.92, 0.70, 0.25, 1),
               (0.35, 0.60, 0.42, 1), (0.66, 0.35, 0.68, 1), (0.90, 0.45, 0.28, 1)]
BUILDING_COLORS = [(0.80, 0.76, 0.70, 1), (0.72, 0.70, 0.68, 1), (0.84, 0.78, 0.68, 1),
                   (0.68, 0.66, 0.64, 1), (0.78, 0.72, 0.64, 1), (0.74, 0.72, 0.74, 1),
                   (0.82, 0.74, 0.66, 1), (0.70, 0.73, 0.74, 1)]


def group(name):
    return empty(name, (0, 0, 0))


# ---------------------------------------------------------------- props
def table(name, w=1.4, d=0.7, h=0.72, top=WOOD, leg=TEAL, loc=(0, 0, 0), parent=None, rot_z=0):
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    box(f"{name}.top", (w, d, 0.055), (0, 0, h), top, g, bevel=0.012)
    for sx in (-1, 1):
        for sy in (-1, 1):
            tube(f"{name}.leg{sx}{sy}", 0.028, 0.024, h, (sx * (w / 2 - 0.08), sy * (d / 2 - 0.07), h / 2),
                 leg, g, seg=10)
    return g


def chair(name, loc=(0, 0, 0), rot_z=0, seat=WOOD, frame=TEAL, parent=None, h=0.44):
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    box(f"{name}.seat", (0.40, 0.38, 0.05), (0, 0, h), seat, g, bevel=0.012)
    box(f"{name}.back", (0.40, 0.05, 0.40), (0, 0.165, h + 0.22), seat, g, bevel=0.012)
    for sx in (-1, 1):
        for sy in (-1, 1):
            tube(f"{name}.l{sx}{sy}", 0.018, 0.016, h, (sx * 0.16, sy * 0.15, h / 2), frame, g, seg=8)
    return g


def stool(name, loc=(0, 0, 0), parent=None, h=0.34, color=WOOD):
    g = empty(name, loc, parent)
    tube(f"{name}.top", 0.17, 0.17, 0.05, (0, 0, h), color, g, seg=14)
    for i in range(3):
        a = i * TAU / 3
        tube(f"{name}.l{i}", 0.016, 0.014, h, (math.cos(a) * 0.12, math.sin(a) * 0.12, h / 2),
             WOOD_DARK, g, seg=8)
    return g


def books_row(name, n, x0, y, z, parent=None, scale=1.0, seed=0, vertical=True):
    rnd = random.Random(seed)
    g = empty(name, (0, 0, 0), parent)
    x = x0
    for i in range(n):
        w = rnd.uniform(0.028, 0.045) * scale
        hh = rnd.uniform(0.20, 0.26) * scale
        box(f"{name}.b{i}", (w, 0.17 * scale, hh), (x + w / 2, y, z + hh / 2),
            BOOK_COLORS[rnd.randrange(len(BOOK_COLORS))], g, bevel=0.004)
        x += w + 0.004 * scale
    return g


def book_stack(name, n, loc, parent=None, scale=1.0, seed=1):
    rnd = random.Random(seed)
    g = empty(name, loc, parent)
    z = 0
    for i in range(n):
        t = rnd.uniform(0.028, 0.042) * scale
        box(f"{name}.s{i}", (0.22 * scale, 0.17 * scale, t), (rnd.uniform(-.01, .01), rnd.uniform(-.01, .01), z + t / 2),
            BOOK_COLORS[rnd.randrange(len(BOOK_COLORS))], g, rot=(0, 0, D(rnd.uniform(-9, 9))), bevel=0.004)
        z += t
    return g


def shelf(name, loc=(0, 0, 0), rot_z=0, w=1.0, h=1.5, d=0.26, parent=None, seed=3, full=True):
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    box(f"{name}.back", (w, 0.03, h), (0, d / 2, h / 2), WOOD_DARK, g)
    for sx in (-1, 1):
        box(f"{name}.side{sx}", (0.035, d, h), (sx * (w / 2), 0, h / 2), WOOD, g, bevel=0.008)
    rows = max(2, int(h / 0.38))
    for r in range(rows + 1):
        z = h * r / rows
        box(f"{name}.sh{r}", (w, d, 0.03), (0, 0, z), WOOD, g, bevel=0.006)
        if full and r < rows:
            books_row(f"{name}.row{r}", random.Random(seed + r).randint(5, 9),
                      -w / 2 + 0.06, 0.0, z + 0.015, g, scale=0.95, seed=seed * 7 + r)
    return g


def laptop(name, loc=(0, 0, 0), rot_z=0, parent=None, open_deg=102, screen=SCREEN_ON, scale=1.0):
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    box(f"{name}.base", (0.33 * scale, 0.23 * scale, 0.016 * scale), (0, 0, 0.008 * scale),
        (0.46, 0.48, 0.52, 1), g, bevel=0.004)
    box(f"{name}.keys", (0.28 * scale, 0.16 * scale, 0.004 * scale), (0, -0.02 * scale, 0.018 * scale),
        (0.32, 0.34, 0.38, 1), g)
    lid = empty(f"{name}.lidp", (0, 0.115 * scale, 0.012 * scale), g)
    lid.rotation_euler = Euler((D(-(180 - open_deg)), 0, 0))
    box(f"{name}.lid", (0.33 * scale, 0.012 * scale, 0.22 * scale), (0, 0, 0.11 * scale),
        (0.46, 0.48, 0.52, 1), lid, bevel=0.004)
    box(f"{name}.scr", (0.30 * scale, 0.006 * scale, 0.19 * scale), (0, -0.010 * scale, 0.11 * scale),
        screen, lid)
    return g


def monitor(name, loc=(0, 0, 0), rot_z=0, parent=None, scale=1.0):
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    tube(f"{name}.foot", 0.10 * scale, 0.10 * scale, 0.02 * scale, (0, 0, 0.01 * scale), (0.40, 0.42, 0.46, 1), g, seg=12)
    box(f"{name}.stem", (0.04 * scale, 0.04 * scale, 0.18 * scale), (0, 0, 0.11 * scale), (0.40, 0.42, 0.46, 1), g)
    box(f"{name}.body", (0.46 * scale, 0.025 * scale, 0.29 * scale), (0, 0.01 * scale, 0.35 * scale),
        (0.38, 0.40, 0.44, 1), g, bevel=0.006)
    box(f"{name}.scr", (0.43 * scale, 0.008 * scale, 0.26 * scale), (0, -0.008 * scale, 0.35 * scale), SCREEN_ON, g)
    return g


def papers(name, loc, parent=None, n=3, seed=2, color=PAPER, scale=1.0):
    rnd = random.Random(seed)
    g = empty(name, loc, parent)
    for i in range(n):
        box(f"{name}.p{i}", (0.21 * scale, 0.29 * scale, 0.002), (rnd.uniform(-.03, .03), rnd.uniform(-.03, .03), i * 0.0025),
            color, g, rot=(0, 0, D(rnd.uniform(-14, 14))))
    return g


def pencil(name, loc, parent=None, rot=(0, 90, 20), color=(0.92, 0.72, 0.25, 1)):
    g = empty(name, loc, parent)
    t = tube(f"{name}.body", 0.006, 0.006, 0.17, (0, 0, 0), color, g, seg=6)
    t.rotation_euler = Euler((D(rot[0]), D(rot[1]), D(rot[2])))
    return g


def plant(name, loc=(0, 0, 0), parent=None, scale=1.0, pot=(0.74, 0.42, 0.32, 1)):
    g = empty(name, loc, parent)
    tube(f"{name}.pot", 0.11 * scale, 0.14 * scale, 0.19 * scale, (0, 0, 0.095 * scale), pot, g, seg=14)
    rnd = random.Random(hash(name) % 999)
    for i in range(6):
        a = i * TAU / 6 + rnd.uniform(-.3, .3)
        lf = ball(f"{name}.lf{i}", 0.085 * scale, (math.cos(a) * 0.07 * scale, math.sin(a) * 0.07 * scale,
                  0.28 * scale + rnd.uniform(0, 0.10) * scale), LEAF if i % 2 else LEAF2, g,
                  scale=(0.45, 0.45, 1.9))
        lf.rotation_euler = Euler((D(rnd.uniform(-28, 28)), D(rnd.uniform(-28, 28)), 0))
    return g


def tree(name, loc=(0, 0, 0), parent=None, scale=1.0, seed=0):
    rnd = random.Random(seed)
    g = empty(name, loc, parent)
    hh = rnd.uniform(2.0, 3.0) * scale
    tube(f"{name}.trunk", 0.10 * scale, 0.13 * scale, hh, (0, 0, hh / 2), TRUNK, g, seg=8)
    for i in range(3):
        r = rnd.uniform(0.62, 0.86) * scale
        ball(f"{name}.c{i}", r, (rnd.uniform(-.3, .3) * scale, rnd.uniform(-.3, .3) * scale,
             hh + rnd.uniform(-.1, .45) * scale), LEAF if i % 2 else LEAF2, g, scale=(1, 1, 0.82))
    return g


def window_frame(name, w=1.1, h=1.25, loc=(0, 0, 0), parent=None, rot_z=0, frame=(0.92, 0.92, 0.90, 1),
                 bars=True):
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    t = 0.06
    box(f"{name}.l", (t, 0.10, h), (-w / 2, 0, 0), frame, g, bevel=0.01)
    box(f"{name}.r", (t, 0.10, h), (w / 2, 0, 0), frame, g, bevel=0.01)
    box(f"{name}.t", (w + t, 0.10, t), (0, 0, h / 2), frame, g, bevel=0.01)
    box(f"{name}.b", (w + t, 0.12, t * 1.4), (0, 0, -h / 2), frame, g, bevel=0.01)
    if bars:
        box(f"{name}.v", (0.035, 0.07, h), (0, 0, 0), frame, g)
        box(f"{name}.h", (w, 0.07, 0.035), (0, 0, 0), frame, g)
    return g


def wall_with_window(name, w, h, win_w, win_h, win_cx, win_cz, color, loc=(0, 0, 0), parent=None,
                     rot_z=0, thick=0.12):
    """A wall panel with a real hole, built from four boxes."""
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    l_w = (win_cx - win_w / 2) + w / 2
    r_w = w / 2 - (win_cx + win_w / 2)
    if l_w > 0.001:
        box(f"{name}.L", (l_w, thick, h), (-w / 2 + l_w / 2, 0, h / 2), color, g)
    if r_w > 0.001:
        box(f"{name}.R", (r_w, thick, h), (w / 2 - r_w / 2, 0, h / 2), color, g)
    top_h = h - (win_cz + win_h / 2)
    if top_h > 0.001:
        box(f"{name}.T", (win_w, thick, top_h), (win_cx, 0, h - top_h / 2), color, g)
    bot_h = win_cz - win_h / 2
    if bot_h > 0.001:
        box(f"{name}.B", (win_w, thick, bot_h), (win_cx, 0, bot_h / 2), color, g)
    window_frame(f"{name}.win", win_w, win_h, (win_cx, 0, win_cz), g)
    return g


def room(name, w=5.0, d=4.0, h=2.7, wall=WALL_RICH, floor=FLOOR_RICH, loc=(0, 0, 0),
         win_w=1.2, win_h=1.3, win_cx=0.0, win_cz=1.45, side_walls=True, ceiling=False,
         back_window=True, rot_z=0):
    """Room opening toward -Y (camera side).  Back wall at +Y carries the window."""
    g = empty(name, loc)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    box(f"{name}.floor", (w, d, 0.08), (0, 0, -0.04), floor, g)
    if back_window:
        bw = wall_with_window(f"{name}.back", w, h, win_w, win_h, win_cx, win_cz, wall,
                              (0, d / 2, 0), g)
    else:
        box(f"{name}.back", (w, 0.12, h), (0, d / 2, h / 2), wall, g)
    if side_walls:
        box(f"{name}.left", (0.12, d, h), (-w / 2, 0, h / 2), wall, g)
        box(f"{name}.right", (0.12, d, h), (w / 2, 0, h / 2), wall, g)
    if ceiling:
        box(f"{name}.ceil", (w, d, 0.10), (0, 0, h), wall, g)
    # skirting
    box(f"{name}.skirt", (w, 0.04, 0.09), (0, d / 2 - 0.07, 0.045), (0.70, 0.66, 0.60, 1), g)
    return g


def ceiling_fan(name, loc, parent=None, color=(0.90, 0.88, 0.84, 1)):
    g = empty(name, loc, parent)
    tube(f"{name}.rod", 0.02, 0.02, 0.22, (0, 0, 0.11), (0.6, 0.6, 0.6, 1), g, seg=8)
    hub = empty(f"{name}.hub", (0, 0, 0), g)
    tube(f"{name}.hubm", 0.07, 0.07, 0.06, (0, 0, 0), color, hub, seg=12)
    for i in range(3):
        b = box(f"{name}.bl{i}", (0.62, 0.11, 0.012), (0, 0, 0), color, hub, bevel=0.004)
        b.rotation_euler = Euler((0, 0, i * TAU / 3))
        b.location = (math.cos(i * TAU / 3) * 0.34, math.sin(i * TAU / 3) * 0.34, -0.01)
    return g, hub


def rug(name, loc, w=2.0, d=1.4, parent=None, color=(0.70, 0.40, 0.34, 1), border=(0.85, 0.72, 0.52, 1)):
    g = empty(name, loc, parent)
    box(f"{name}.a", (w, d, 0.012), (0, 0, 0.006), border, g)
    box(f"{name}.b", (w * 0.86, d * 0.80, 0.014), (0, 0, 0.008), color, g)
    return g


def mat(name, loc, w=1.2, d=0.9, parent=None, color=(0.72, 0.62, 0.42, 1)):
    g = empty(name, loc, parent)
    box(f"{name}.m", (w, d, 0.02), (0, 0, 0.01), color, g, bevel=0.006)
    return g


def poster(name, loc, w=0.6, h=0.8, parent=None, color=(0.85, 0.80, 0.70, 1), rot_z=0, frame=True):
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    if frame:
        box(f"{name}.f", (w + 0.05, 0.02, h + 0.05), (0, 0.012, 0), (0.45, 0.35, 0.28, 1), g)
    box(f"{name}.p", (w, 0.012, h), (0, 0, 0), color, g)
    return g


def banner(name, loc, w=4.0, h=0.5, parent=None, color=TEAL, rot_z=0):
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    box(f"{name}.b", (w, 0.05, h), (0, 0, 0), color, g, bevel=0.01)
    box(f"{name}.e", (w, 0.055, 0.04), (0, 0, h / 2 - 0.05), (0.95, 0.93, 0.86, 1), g)
    return g


# ---------------------------------------------------------------- science props
def solar_project(name, loc=(0, 0, 0), parent=None, rot_z=0, scale=1.0, handmade=True):
    """Maya's handmade solar tracker: cardboard base, bottle stand, blue panel."""
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    base_col = CARD if handmade else (0.84, 0.84, 0.86, 1)
    box(f"{name}.base", (0.42 * scale, 0.32 * scale, 0.022 * scale), (0, 0, 0.011 * scale), base_col, g, bevel=0.006)
    tube(f"{name}.post", 0.022 * scale, 0.026 * scale, 0.14 * scale, (0, 0.02 * scale, 0.08 * scale),
         (0.58, 0.60, 0.64, 1) if not handmade else (0.52, 0.68, 0.70, 1), g, seg=10)
    pan = empty(f"{name}.pan", (0, 0.02 * scale, 0.15 * scale), g)
    pan.rotation_euler = Euler((D(-32), 0, 0))
    box(f"{name}.panel", (0.30 * scale, 0.20 * scale, 0.012 * scale), (0, 0, 0), (0.18, 0.28, 0.52, 1), pan, bevel=0.004)
    for i in range(3):
        box(f"{name}.cell{i}", (0.085 * scale, 0.18 * scale, 0.004 * scale),
            (-0.095 * scale + i * 0.095 * scale, 0, 0.008 * scale), (0.26, 0.42, 0.70, 1), pan)
    # little lamp/sun on a wire
    ball(f"{name}.bulb", 0.030 * scale, (0.15 * scale, -0.08 * scale, 0.055 * scale),
         (0.98, 0.84, 0.40, 1), g)
    return g, pan


def recycled_pile(name, loc=(0, 0, 0), parent=None, seed=5, n=6, scale=1.0):
    """Bottles, cardboard, wire — Maya's materials."""
    rnd = random.Random(seed)
    g = empty(name, loc, parent)
    for i in range(n):
        x, y = rnd.uniform(-0.28, 0.28) * scale, rnd.uniform(-0.2, 0.2) * scale
        k = rnd.random()
        if k < 0.45:
            h = rnd.uniform(0.14, 0.2) * scale
            b = tube(f"{name}.bot{i}", 0.035 * scale, 0.042 * scale, h, (x, y, h / 2), (0.62, 0.78, 0.72, 1), g, seg=10)
            tube(f"{name}.cap{i}", 0.016 * scale, 0.016 * scale, 0.03 * scale, (x, y, h + 0.015 * scale),
                 (0.85, 0.45, 0.30, 1), g, seg=8)
        elif k < 0.75:
            box(f"{name}.cb{i}", (rnd.uniform(0.16, 0.26) * scale, rnd.uniform(0.12, 0.2) * scale, 0.09 * scale),
                (x, y, 0.045 * scale), CARD, g, rot=(0, 0, D(rnd.uniform(0, 90))), bevel=0.006)
        else:
            tube(f"{name}.cn{i}", 0.05 * scale, 0.05 * scale, 0.02 * scale, (x, y, 0.01 * scale),
                 (0.70, 0.72, 0.74, 1), g, seg=12)
    return g


def model_rocket(name, loc, parent=None, scale=1.0, color=(0.90, 0.92, 0.94, 1)):
    g = empty(name, loc, parent)
    tube(f"{name}.body", 0.05 * scale, 0.05 * scale, 0.26 * scale, (0, 0, 0.13 * scale), color, g, seg=12)
    tube(f"{name}.nose", 0.0 * scale, 0.05 * scale, 0.10 * scale, (0, 0, 0.31 * scale), (0.86, 0.32, 0.28, 1), g, seg=12)
    for i in range(3):
        a = i * TAU / 3
        f = box(f"{name}.fin{i}", (0.015 * scale, 0.08 * scale, 0.09 * scale),
                (math.cos(a) * 0.055 * scale, math.sin(a) * 0.055 * scale, 0.045 * scale),
                (0.86, 0.32, 0.28, 1), g)
        f.rotation_euler = Euler((0, 0, a))
    return g


def dna_model(name, loc, parent=None, scale=1.0):
    g = empty(name, loc, parent)
    tube(f"{name}.b", 0.06 * scale, 0.07 * scale, 0.02 * scale, (0, 0, 0.01 * scale), (0.5, 0.5, 0.55, 1), g, seg=12)
    for i in range(10):
        t = i / 9
        a = t * TAU * 1.5
        z = 0.03 * scale + t * 0.26 * scale
        for s in (-1, 1):
            ball(f"{name}.n{i}{s}", 0.022 * scale, (math.cos(a) * s * 0.055 * scale,
                 math.sin(a) * s * 0.055 * scale, z), BOOK_COLORS[i % 6], g)
    return g


def globe(name, loc, parent=None, scale=1.0):
    g = empty(name, loc, parent)
    tube(f"{name}.base", 0.05 * scale, 0.06 * scale, 0.03 * scale, (0, 0, 0.015 * scale), WOOD_DARK, g, seg=12)
    b = ball(f"{name}.ball", 0.11 * scale, (0, 0, 0.15 * scale), (0.38, 0.60, 0.78, 1), g)
    for i, (ox, oy, r) in enumerate([(-0.04, -0.03, 0.045), (0.05, 0.02, 0.038), (-0.01, 0.06, 0.030)]):
        ball(f"{name}.land{i}", r * scale, (ox * scale, oy * scale * 0.6, 0.15 * scale + oy * scale),
             (0.42, 0.62, 0.40, 1), g, scale=(1, 0.5, 1))
    return g


def wheelchair(name, loc=(0, 0, 0), rot_z=0, parent=None, color=(0.42, 0.46, 0.55, 1)):
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    box(f"{name}.seat", (0.42, 0.40, 0.05), (0, 0, 0.44), (0.30, 0.34, 0.42, 1), g, bevel=0.01)
    box(f"{name}.back", (0.42, 0.05, 0.42), (0, 0.18, 0.66), (0.30, 0.34, 0.42, 1), g, bevel=0.01)
    for s in (-1, 1):
        w = tube(f"{name}.w{s}", 0.28, 0.28, 0.035, (s * 0.25, 0.02, 0.28), (0.22, 0.22, 0.24, 1), g, seg=18)
        w.rotation_euler = Euler((0, D(90), 0))
        r = tube(f"{name}.r{s}", 0.22, 0.22, 0.02, (s * 0.285, 0.02, 0.28), METAL, g, seg=16)
        r.rotation_euler = Euler((0, D(90), 0))
        cw = tube(f"{name}.cw{s}", 0.09, 0.09, 0.03, (s * 0.17, -0.26, 0.09), (0.22, 0.22, 0.24, 1), g, seg=12)
        cw.rotation_euler = Euler((0, D(90), 0))
        box(f"{name}.arm{s}", (0.05, 0.34, 0.04), (s * 0.235, 0.0, 0.62), color, g, bevel=0.008)
    return g


# ---------------------------------------------------------------- city
def building(name, loc, w, d, h, color=None, parent=None, seed=0, windows=True, roof=True,
             balcony=False, lod=0):
    """lod 0 = individual windows (hero), 1 = per-floor window strips, 2 = plain block."""
    rnd = random.Random(seed)
    color = color or BUILDING_COLORS[seed % len(BUILDING_COLORS)]
    g = empty(name, loc, parent)
    box(f"{name}.body", (w, d, h), (0, 0, h / 2), color, g, bevel=0.03)
    if roof:
        box(f"{name}.roof", (w * 1.04, d * 1.04, 0.12), (0, 0, h + 0.06),
            (color[0] * 0.82, color[1] * 0.80, color[2] * 0.78, 1), g, bevel=0.02)
    if windows and lod < 2:
        floors = max(1, min(7, int(h / 1.4)))
        if lod == 1:
            for fl in range(floors):
                z = 0.8 + fl * (h - 0.9) / max(1, floors)
                if z > h - 0.4:
                    continue
                c = (0.95, 0.86, 0.60, 1) if rnd.random() < 0.28 else GLASS
                box(f"{name}.ws{fl}", (w * 0.80, d + 0.05, 0.42), (0, 0, z), c, g)
                box(f"{name}.wx{fl}", (w + 0.05, d * 0.80, 0.42), (0, 0, z), c, g)
        else:
            cols = max(1, min(4, int(w / 1.1)))
            for fl in range(floors):
                z = 0.8 + fl * (h - 0.9) / max(1, floors)
                if z > h - 0.4:
                    continue
                for cx in range(cols):
                    x = -w / 2 + (cx + 0.5) * w / cols
                    lit = rnd.random() < 0.3
                    c = (0.95, 0.85, 0.58, 1) if lit else GLASS
                    ww = min(0.52, w / cols * 0.6)
                    box(f"{name}.w{fl}{cx}", (ww, 0.05, 0.46), (x, -d / 2, z), c, g)
                    box(f"{name}.wb{fl}{cx}", (ww + 0.07, 0.06, 0.05),
                        (x, -d / 2 - 0.01, z - 0.26), (0.95, 0.94, 0.92, 1), g)
    if balcony:
        box(f"{name}.balc", (w * 0.7, 0.5, 0.06), (0, -d / 2 - 0.25, h * 0.55), (0.86, 0.84, 0.80, 1), g)
        box(f"{name}.balr", (w * 0.7, 0.05, 0.30), (0, -d / 2 - 0.48, h * 0.55 + 0.17), METAL, g)
    return g


def road_strip(name, loc, length=60, width=7.0, parent=None, rot_z=0, lines=True):
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    box(f"{name}.r", (width, length, 0.04), (0, 0, 0.02), ROAD, g)
    for s in (-1, 1):
        box(f"{name}.k{s}", (0.30, length, 0.14), (s * (width / 2 + 0.15), 0, 0.07), (0.78, 0.76, 0.72, 1), g)
    if lines:
        n = int(length / 4)
        for i in range(n):
            box(f"{name}.l{i}", (0.16, 1.6, 0.01), (0, -length / 2 + 2 + i * 4, 0.045), ROAD_LINE, g)
    return g


def streetlight(name, loc, parent=None, h=4.2):
    g = empty(name, loc, parent)
    tube(f"{name}.p", 0.07, 0.09, h, (0, 0, h / 2), (0.52, 0.54, 0.56, 1), g, seg=8)
    box(f"{name}.a", (0.9, 0.08, 0.08), (0.42, 0, h), (0.52, 0.54, 0.56, 1), g)
    ball(f"{name}.l", 0.13, (0.82, 0, h - 0.04), (0.98, 0.92, 0.70, 1), g, scale=(1, 1, 0.55))
    return g


def city_block(name, origin=(0, 0, 0), nx=4, ny=4, spacing=9.0, seed=7, parent=None,
               skip=(), height=(3.0, 11.0), trees=True, lod=1):
    rnd = random.Random(seed)
    g = empty(name, origin, parent)
    for ix in range(nx):
        for iy in range(ny):
            if (ix, iy) in skip:
                continue
            x = (ix - (nx - 1) / 2) * spacing + rnd.uniform(-0.6, 0.6)
            y = (iy - (ny - 1) / 2) * spacing + rnd.uniform(-0.6, 0.6)
            w = rnd.uniform(3.6, 6.0)
            d = rnd.uniform(3.6, 6.0)
            h = rnd.uniform(*height)
            building(f"{name}.b{ix}_{iy}", (x, y, 0), w, d, h, parent=g, seed=rnd.randrange(999),
                     balcony=lod == 0 and rnd.random() < 0.3, lod=lod)
            if trees and rnd.random() < 0.55:
                tree(f"{name}.t{ix}_{iy}", (x + rnd.uniform(-4, 4), y + rnd.uniform(-4, 4), 0),
                     g, scale=rnd.uniform(0.7, 1.1), seed=rnd.randrange(999))
    return g


# ---------------------------------------------------------------- world helpers
def ground(name="ground", size=400, color=GROUND_WARM, z=0.0):
    return plane(name, (size, size), (0, 0, z), color)


def camera(name="cam", loc=(0, -6, 2), look=(0, 0, 1.2), lens=42, dof=None, fstop=2.8):
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = lens
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.location = loc
    aim_at(cam, look)
    if dof is not None:
        cam_data.dof.use_dof = True
        cam_data.dof.focus_distance = dof
        cam_data.dof.aperture_fstop = fstop
    return cam


def aim_at(ob, target):
    """Point the object's -Z axis at `target` with +Y up (Blender camera convention)."""
    from mathutils import Vector
    d = Vector(target) - ob.location
    if d.length < 1e-6:
        return
    rz = math.atan2(-d.x, d.y)
    rx = math.atan2(math.hypot(d.x, d.y), -d.z)
    ob.rotation_euler = Euler((rx, 0, rz))


def key_cam(cam, frame, loc=None, look=None, lens=None, focus=None):
    if loc is not None:
        cam.location = loc
        cam.keyframe_insert("location", frame=frame)
    if look is not None:
        aim_at(cam, look)
        cam.keyframe_insert("rotation_euler", frame=frame)
    if lens is not None:
        cam.data.lens = lens
        cam.data.keyframe_insert("lens", frame=frame)
    if focus is not None:
        cam.data.dof.focus_distance = focus
        cam.data.dof.keyframe_insert("focus_distance", frame=frame)
