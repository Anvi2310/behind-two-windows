"""
shots.py — the ten sequences of "BEHIND TWO WINDOWS" (SDG 10 — Reduced Inequalities).

Every shot is a function build(n_frames) that constructs the set, places the characters and
keyframes both the performance and the camera.  Frame 1 .. n at 24 fps.
"""
import bpy, math, random
from mathutils import Euler, Vector

from rig import (Character, make_aarav, make_maya, make_kid, make_adult, ball, box, tube,
                 plane, empty, D, TAU, ease_all, fcurves_of, SKIN, HAIR_BLACK, WHITE)
import sets as S
from sets import (ground, camera, key_cam, aim_at, table, chair, stool, shelf, laptop, monitor,
                  papers, pencil, plant, tree, room, wall_with_window, window_frame, ceiling_fan,
                  rug, mat, poster, banner, solar_project, recycled_pile, model_rocket, dna_model,
                  globe, wheelchair, building, road_strip, streetlight, city_block, book_stack,
                  books_row, WOOD, WOOD_DARK, TEAL, PAPER, CARD, METAL, SCREEN_ON, GLASS,
                  WALL_RICH, WALL_MODEST, FLOOR_RICH, FLOOR_MODEST, GROUND_WARM, GROUND_COOL,
                  BOOK_COLORS, LEAF)

FPS = 24


def sec(t):
    return int(round(t * FPS))


def smooth_cam(cam):
    for ob in (cam, cam.data, getattr(cam.data, "dof", None)):
        if ob is None:
            continue
        for fc in fcurves_of(ob):
            for kp in fc.keyframe_points:
                kp.interpolation = 'BEZIER'
                kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'


def drawing_on_paper(name, loc, parent=None, rot_z=0, scale=1.0, kind="lab"):
    """A child's drawing of a laboratory: paper plus simple coloured shapes."""
    g = empty(name, loc, parent)
    g.rotation_euler = Euler((0, 0, D(rot_z)))
    box(f"{name}.sheet", (0.30 * scale, 0.40 * scale, 0.003), (0, 0, 0), PAPER, g)
    z = 0.004
    # bench line
    box(f"{name}.bench", (0.24 * scale, 0.012 * scale, 0.002), (0, -0.09 * scale, z), (0.45, 0.40, 0.38, 1), g)
    # flask
    tube(f"{name}.flask", 0.012 * scale, 0.034 * scale, 0.055 * scale, (-0.07 * scale, -0.055 * scale, z),
         (0.35, 0.65, 0.72, 1), g, rot=(D(90), 0, 0), seg=8)
    # rocket
    box(f"{name}.rk", (0.022 * scale, 0.075 * scale, 0.002), (0.02 * scale, -0.03 * scale, z), (0.85, 0.35, 0.32, 1), g)
    tube(f"{name}.rkn", 0.0, 0.016 * scale, 0.03 * scale, (0.02 * scale, 0.025 * scale, z),
         (0.90, 0.72, 0.30, 1), g, rot=(D(-90), 0, 0), seg=8)
    # atom / orbit rings
    for i, r in enumerate((0.05, 0.034)):
        t = tube(f"{name}.o{i}", r * scale, r * scale, 0.0018, (0.085 * scale, 0.02 * scale, z),
                 (0.40, 0.52, 0.80, 1), g, seg=18)
        t.rotation_euler = Euler((0, 0, D(i * 55)))
        t.scale = (1, 0.42, 1)
    ball(f"{name}.nuc", 0.010 * scale, (0.085 * scale, 0.02 * scale, z + 0.002), (0.90, 0.55, 0.25, 1), g)
    # sun in the corner
    ball(f"{name}.sun", 0.020 * scale, (-0.095 * scale, 0.155 * scale, z), (0.95, 0.78, 0.30, 1), g, scale=(1, 1, 0.3))
    return g


def crowd_kid(i, loc, rot_z, scale=1.0):
    return make_kid(f"kid{i}", i, loc=loc, rot_z=rot_z, scale=scale)


# =====================================================================
# S01 — TWO WORLDS  (aerial sunrise, descend toward two homes)
# =====================================================================
def s01_two_worlds(n):
    ground("gnd", 600, (0.84, 0.78, 0.66, 1))
    rnd = random.Random(4)

    # the two hero homes, side by side on the same street, separated by a wall
    # Aarav's — taller, modern, large glass
    ah = building("home_a", (-5.6, 6.2, 0), 7.2, 6.6, 6.2, (0.90, 0.88, 0.82, 1), seed=11,
                  balcony=True, lod=0)
    box("home_a.glass", (4.8, 0.14, 2.4), (-5.6, 6.2 - 3.35, 3.5), GLASS)
    box("home_a.lit2", (1.6, 0.10, 1.2), (-7.6, 6.2 - 3.36, 1.5), (0.99, 0.90, 0.62, 1))
    box("home_a.door", (1.3, 0.14, 2.3), (-3.6, 6.2 - 3.36, 1.15), WOOD_DARK)
    tree("ta1", (-10.6, 2.0, 0), scale=1.2, seed=21)
    tree("ta2", (-2.2, 2.4, 0), scale=0.95, seed=22)
    # Maya's — single storey, modest, small window
    mh = building("home_m", (5.8, 6.4, 0), 5.8, 5.6, 3.0, (0.82, 0.74, 0.62, 1), seed=31, windows=False)
    box("home_m.roof2", (6.3, 6.1, 0.18), (5.8, 6.4, 3.1), (0.70, 0.56, 0.44, 1))
    window_frame("home_m.win", 1.2, 1.1, (4.8, 6.4 - 2.85, 1.8))
    box("home_m.winglass", (1.2, 0.07, 1.1), (4.8, 6.4 - 2.80, 1.8), (0.99, 0.87, 0.55, 1))
    box("home_m.door", (1.15, 0.14, 2.1), (7.2, 6.4 - 2.86, 1.05), WOOD_DARK)
    box("home_m.step", (2.0, 0.9, 0.16), (7.2, 6.4 - 3.3, 0.08), (0.78, 0.74, 0.66, 1))
    tree("tm1", (10.4, 2.6, 0), scale=0.85, seed=41)
    # lit window on Aarav's side too
    box("home_a.lit", (1.4, 0.09, 1.1), (-7.8, 6.2 - 3.36, 3.5), (0.99, 0.91, 0.62, 1))
    # the wall between the two properties — the film's visual motif
    box("divwall", (0.40, 8.2, 2.3), (0.1, 6.0, 1.15), (0.78, 0.72, 0.63, 1), bevel=0.04)

    road_strip("road", (0, -2.0, 0), length=200, width=9.0, rot_z=0)
    road_strip("road2", (0, 30, 0), length=200, width=8.0, rot_z=90)

    # surrounding city
    city_block("cityL", (-40, 30, 0), nx=3, ny=3, spacing=13.0, seed=7, height=(5, 15), lod=1)
    city_block("cityR", (40, 30, 0), nx=3, ny=3, spacing=13.0, seed=19, height=(5, 15), lod=1)
    city_block("cityB", (0, 76, 0), nx=5, ny=2, spacing=14.0, seed=23, height=(7, 20), lod=2, trees=False)
    city_block("cityF", (-36, -36, 0), nx=2, ny=2, spacing=14.0, seed=29, height=(4, 11), lod=2, trees=False)
    city_block("cityF2", (36, -36, 0), nx=2, ny=2, spacing=14.0, seed=37, height=(4, 11), lod=2, trees=False)
    for i in range(4):
        streetlight(f"sl{i}", (-5.4, -34 + i * 24, 0))
        streetlight(f"sr{i}", (5.4, -34 + i * 24, 0))

    # birds: small dark ellipsoids drifting across the sky
    birds = []
    for i in range(7):
        b = ball(f"bird{i}", 0.5, (0, 0, 0), (0.22, 0.20, 0.24, 1), scale=(1.9, 0.5, 0.34))
        birds.append(b)

    cam = camera("cam", (0, -92, 58), (0, 10, 10), lens=38, dof=60, fstop=3.5)
    a = sec(0)
    key_cam(cam, 1, (3.0, -86, 40), (0, 26, 20), lens=34, focus=86)
    key_cam(cam, sec(7.5), (1.6, -46, 17), (0, 14, 9.5), lens=34, focus=50)
    key_cam(cam, n, (0.4, -14.5, 5.4), (0.0, 6.2, 3.6), lens=35, focus=18)

    for i, b in enumerate(birds):
        x0 = -70 + i * 6
        z = 34 + (i % 3) * 5
        y = 40 + (i % 4) * 9
        for f in (1, n):
            u = (f - 1) / max(1, n - 1)
            b.location = (x0 + u * 46, y, z + math.sin(u * 5 + i) * 1.6)
            b.keyframe_insert("location", frame=f)
            b.rotation_euler = Euler((0, 0, D(10 + 8 * math.sin(u * 7 + i))))
            b.keyframe_insert("rotation_euler", frame=f)
    smooth_cam(cam)


# =====================================================================
# S02 — AARAV'S WORLD
# =====================================================================
def s02_aarav_world(n):
    ground("gnd", 300, GROUND_WARM)
    r = room("rm", w=6.4, d=5.0, h=2.9, wall=WALL_RICH, floor=FLOOR_RICH,
             win_w=2.0, win_h=1.6, win_cx=0.9, win_cz=1.60, ceiling=True)
    rug("rug", (-0.2, -0.6, 0.0), 3.0, 2.2, r)
    # desk setup
    d = table("desk", 1.9, 0.78, 0.74, WOOD, TEAL, (-1.15, 0.45, 0), r, rot_z=0)
    lap = laptop("lap", (-1.25, 0.46, 0.77), 186, r)
    monitor("mon", (-1.95, 0.60, 0.77), 200, r, scale=0.8)
    book_stack("bs1", 4, (-0.42, 0.30, 0.77), r, seed=3)
    papers("pap", (-0.95, 0.24, 0.775), r, n=3, seed=9)
    ch = chair("ch", (-1.15, 1.22, 0), 0, parent=r)
    # a full wall of books
    shelf("sh1", (-2.72, 0.40, 0), 90, w=2.2, h=2.1, parent=r, seed=5)
    shelf("sh2", (2.70, 0.70, 0), -90, w=1.9, h=1.6, parent=r, seed=8)
    # science models on the right shelf
    model_rocket("rk", (2.45, 0.30, 1.62), r, scale=1.0)
    dna_model("dna", (2.45, 1.15, 1.62), r, scale=0.9)
    globe("glb", (2.42, -0.30, 1.62), r, scale=1.0)
    plant("pl", (2.35, -1.75, 0), r, scale=1.2)
    poster("po", (-3.14, -0.9, 1.85), 0.7, 0.95, r, (0.52, 0.66, 0.74, 1), rot_z=90)
    poster("po2", (-3.14, 0.1, 1.9), 0.55, 0.7, r, (0.80, 0.70, 0.45, 1), rot_z=90)
    fan, hub = ceiling_fan("fan", (0.3, -0.5, 2.78), r)

    aarav = make_aarav(loc=(-1.15, 1.20, 0), rot_z=-8)
    aarav.sit(1, seat_z=0.44)
    # parent enters from the right and brings a book
    dad = make_adult("Dad", 1, loc=(3.0, 2.3, 0), rot_z=-116,
                     top=(0.62, 0.40, 0.44, 1), bottom=(0.33, 0.35, 0.45, 1))
    gift = box("giftbook", (0.20, 0.16, 0.05), (0, 0, 0), (0.80, 0.26, 0.30, 1), dad.r_hand, bevel=0.006)
    gift.location = (0, -0.06, -0.09)

    # --- performance ---
    f_type0, f_type1 = sec(0.5), sec(5.2)
    for f in range(f_type0, f_type1, 2):
        u = (f - f_type0) / FPS
        aarav.pose(f, r_sh=(-52 + 5 * math.sin(u * 9), -16, 0), l_sh=(-52 + 5 * math.sin(u * 9 + 2), 16, 0),
                   r_elb=(58, 0, 0), l_elb=(58, 0, 0), spine=(7 + 1.2 * math.sin(u * 2.2), 0, 0))
        aarav.look(f, x=-16 + 1.5 * math.sin(u * 1.7), z=2 * math.sin(u * 1.1))
    aarav.blink([sec(1.6), sec(3.9), sec(8.2), sec(12.0)])

    dad.walk(sec(3.6), sec(7.0), (3.0, 2.3, 0), (1.15, 2.05, 0), face=None, cycle=18, stride=22)
    dad.place(sec(8.2), (1.15, 2.05, 0), -126)
    dad.place(n, (1.15, 2.05, 0), -122)
    dad.idle(sec(7.2), n, amp=0.9, phase=1.0)
    # hands the book over
    dad.pose(sec(7.4), r_sh=(-10, -14, 0), r_elb=(14, 0, 0))
    dad.pose(sec(8.6), r_sh=(-62, -26, 0), r_elb=(42, 0, 0))
    dad.pose(sec(11.5), r_sh=(-58, -22, 0), r_elb=(40, 0, 0))
    dad.look(sec(8.0), x=-20, z=18)

    aarav.look(sec(6.6), x=6, z=38)
    aarav.pose(sec(7.0), spine=(4, 0, 14), r_sh=(-30, -22, 0), r_elb=(40, 0, 0))
    aarav.pose(sec(9.0), spine=(6, 0, 20), r_sh=(-74, -28, 0), r_elb=(48, 0, 0))
    aarav.smile(sec(9.2), 1.0)
    aarav.pose(sec(10.6), spine=(6, 0, 22), r_sh=(-72, -34, 0), r_elb=(44, 0, 0))
    aarav.look(sec(11.0), x=-4, z=28)
    aarav.pose(sec(n / FPS), spine=(5, 0, 14), r_sh=(-56, -22, 0), r_elb=(60, 0, 0))

    # fan turns
    for f in (1, n):
        hub.rotation_euler = Euler((0, 0, (f - 1) / FPS * 2.2))
        hub.keyframe_insert("rotation_euler", frame=f)

    cam = camera("cam", (0.6, -5.2, 1.85), (-0.9, 1.0, 1.25), lens=35, dof=5.2, fstop=2.6)
    key_cam(cam, 1, (2.2, -3.4, 2.05), (-0.35, 1.1, 1.18), lens=28, focus=5.0)
    key_cam(cam, sec(8), (1.75, -2.8, 1.86), (-0.30, 1.1, 1.16), lens=30, focus=4.3)
    key_cam(cam, n, (1.40, -2.4, 1.74), (-0.25, 1.1, 1.14), lens=32, focus=3.8)
    smooth_cam(cam)
    ease_all(aarav.joints + dad.joints + [aarav.root, dad.root])


# =====================================================================
# S03 — MAYA'S WORLD
# =====================================================================
def s03_maya_world(n):
    ground("gnd", 300, GROUND_COOL)
    r = room("rm", w=5.4, d=4.4, h=2.6, wall=WALL_MODEST, floor=FLOOR_MODEST,
             win_w=1.0, win_h=0.95, win_cx=0.75, win_cz=1.55, ceiling=True)
    mat("mat", (-0.35, 0.05, 0.0), 2.1, 1.6, r, (0.70, 0.58, 0.40, 1))
    # low table on the floor
    lt = table("lowt", 1.15, 0.62, 0.30, (0.66, 0.50, 0.33, 1), WOOD_DARK, (-0.32, -0.62, 0), r)
    # crate shelving instead of a bookcase
    for i, (x, z) in enumerate([(-2.15, 0.0), (-2.15, 0.46), (-1.62, 0.0)]):
        box(f"crate{i}", (0.52, 0.42, 0.44), (x, 1.75, z + 0.22), (0.62, 0.47, 0.32, 1), r, bevel=0.015)
    books_row("mbooks", 4, -2.34, 1.70, 0.90, r, scale=0.9, seed=12)
    book_stack("mbs", 3, (-1.62, 1.72, 0.44), r, seed=4, scale=0.95)
    # the handmade project in progress
    proj, pan = solar_project("proj", (-0.30, -0.66, 0.325), r, rot_z=-172, scale=1.15, handmade=True)
    recycled_pile("scrap", (0.78, -0.35, 0.0), r, seed=6, n=7, scale=1.3)
    papers("mp", (-0.72, -0.55, 0.33), r, n=2, seed=5, scale=0.9)
    pencil("pc", (-0.62, -0.45, 0.345), r, rot=(0, 90, 24))
    # simple lamp + small plant + a single poster
    tube("lampb", 0.07, 0.09, 0.03, (0.26, -0.80, 0.33), METAL, r, seg=10)
    tube("lamps", 0.012, 0.012, 0.26, (0.26, -0.80, 0.46), METAL, r, seg=8)
    tube("lamph", 0.10, 0.05, 0.11, (0.26, -0.80, 0.63), (0.86, 0.80, 0.62, 1), r, seg=12)
    plant("mpl", (1.85, 1.35, 0), r, scale=0.8)
    poster("mpo", (-2.62, -0.2, 1.72), 0.5, 0.66, r, (0.70, 0.72, 0.60, 1), rot_z=90)
    fan, hub = ceiling_fan("fan", (0.1, -0.2, 2.48), r)

    maya = make_maya(loc=(-0.33, 0.22, 0.0), rot_z=-6)
    # kneeling on the floor mat
    maya.root.location = (-0.33, 0.22, 0.0)
    maya.pose(1, l_hip=(-96, 0, 0), r_hip=(-96, 0, 0), l_knee=(96, 0, 0), r_knee=(96, 0, 0),
              spine=(12, 0, 0))
    maya.root.location = (-0.33, 0.22, -0.30)
    maya.root.keyframe_insert("location", frame=1)

    # working on the project: both hands busy
    f0, f1 = sec(0.4), sec(7.0)
    for f in range(f0, f1, 2):
        u = (f - f0) / FPS
        maya.pose(f,
                  r_sh=(-62 + 8 * math.sin(u * 5.5), -22 - 4 * math.sin(u * 3), 0),
                  l_sh=(-58 + 7 * math.sin(u * 5.5 + 1.6), 20 + 4 * math.sin(u * 3 + 1), 0),
                  r_elb=(64 + 6 * math.sin(u * 5.5 + 0.6), 0, 0),
                  l_elb=(62 + 6 * math.sin(u * 5.5 + 2.2), 0, 0),
                  spine=(13 + 1.6 * math.sin(u * 2.0), 0, 2.5 * math.sin(u * 1.3)))
        maya.look(f, x=-24 + 2 * math.sin(u * 1.8), z=3 * math.sin(u * 1.1))
    maya.blink([sec(2.0), sec(4.6), sec(9.4), sec(13.5)])

    # lifts the panel toward the window light and smiles
    # both hands go to the panel and tilt it toward the window
    maya.pose(sec(8.6), r_sh=(-74, -26, 0), l_sh=(-70, 24, 0), r_elb=(52, 0, 0), l_elb=(54, 0, 0),
              spine=(9, 0, -4))
    maya.look(sec(8.8), x=-14, z=-8)
    maya.smile(sec(9.2), 1.0)
    # sits back on her heels and looks at what she has made, then up to the light
    maya.pose(sec(11.0), r_sh=(-16, -18, 0), l_sh=(-16, 18, 0), r_elb=(26, 0, 0), l_elb=(26, 0, 0),
              spine=(-2, 0, -3))
    maya.look(sec(11.2), x=-10, z=-5)
    maya.pose(sec(13.4), r_sh=(-14, -17, 0), l_sh=(-14, 17, 0), r_elb=(24, 0, 0), l_elb=(24, 0, 0),
              spine=(-4, 0, -2))
    maya.look(sec(13.6), x=22, z=-12)
    maya.pose(sec(n / FPS), r_sh=(-13, -16, 0), l_sh=(-13, 16, 0), r_elb=(23, 0, 0), l_elb=(23, 0, 0),
              spine=(-4, 0, -1))

    # the project tilts as she adjusts it
    for f, a in ((1, -30), (sec(5.5), -16), (sec(8.6), -30), (sec(10.2), -56), (n, -52)):
        pan.rotation_euler = Euler((D(a), 0, 0))
        pan.keyframe_insert("rotation_euler", frame=f)
    for f in (1, n):
        hub.rotation_euler = Euler((0, 0, (f - 1) / FPS * 1.6))
        hub.keyframe_insert("rotation_euler", frame=f)

    cam = camera("cam", (0.9, -4.4, 1.55), (-0.4, 0.7, 0.72), lens=36, dof=4.6, fstop=2.6)
    key_cam(cam, 1, (1.45, -3.10, 1.40), (-0.33, -0.25, 0.62), lens=30, focus=3.6)
    key_cam(cam, sec(8), (1.10, -2.65, 1.22), (-0.33, -0.22, 0.60), lens=33, focus=3.1)
    key_cam(cam, n, (0.82, -2.30, 1.12), (-0.32, -0.18, 0.62), lens=36, focus=2.7)
    smooth_cam(cam)
    ease_all(maya.joints + [maya.root])


# =====================================================================
# S04 — THE SAME DREAM  (two rooms, one wall, one sky)
# =====================================================================
def s04_same_dream(n):
    ground("gnd", 400, GROUND_WARM)
    # two rooms side by side sharing a wall — seen from outside, walls cut away
    # left: Aarav's; right: Maya's
    L = empty("L", (-2.75, 0, 0))
    box("L.floor", (5.0, 4.2, 0.1), (0, 0, -0.05), FLOOR_RICH, L)
    S.wall_with_window("L.back", 5.0, 2.8, 1.5, 1.4, 0.6, 1.55, WALL_RICH, (0, 2.1, 0), L)
    box("L.side", (0.12, 4.2, 2.8), (-2.5, 0, 1.4), WALL_RICH, L)
    R = empty("R", (2.75, 0, 0))
    box("R.floor", (5.0, 4.2, 0.1), (0, 0, -0.05), FLOOR_MODEST, R)
    S.wall_with_window("R.back", 5.0, 2.8, 1.0, 0.95, -0.5, 1.5, WALL_MODEST, (0, 2.1, 0), R)
    box("R.side", (0.12, 4.2, 2.8), (2.5, 0, 1.4), WALL_MODEST, R)
    # the shared wall — the two windows motif
    box("shared", (0.30, 4.3, 3.0), (0, 0, 1.5), (0.74, 0.68, 0.60, 1), bevel=0.04)

    # left room: desk and chair
    table("desk", 1.5, 0.7, 0.72, WOOD, TEAL, (-3.1, -0.15, 0))
    chair("ch", (-3.1, 0.62, 0), 0)
    shelf("sh", (-4.95, 0.5, 0), 90, w=1.6, h=1.5, seed=5)
    plant("pl", (-0.95, -1.3, 0), scale=1.0)
    # right room: floor mat and low table
    mat("mat", (2.4, 0.35, 0), 1.9, 1.4, color=(0.70, 0.58, 0.40, 1))
    table("lowt", 1.05, 0.58, 0.30, (0.66, 0.50, 0.33, 1), WOOD_DARK, (2.4, -0.30, 0))
    for i in range(2):
        box(f"crate{i}", (0.5, 0.4, 0.42), (4.6, 1.3 - i * 0.0, 0.21 + i * 0.44), (0.62, 0.47, 0.32, 1), bevel=0.015)
    plant("pl2", (4.5, -1.2, 0), scale=0.75)

    aarav = make_aarav(loc=(-3.1, 0.60, 0), rot_z=-4)
    aarav.sit(1, seat_z=0.44)
    maya = make_maya(loc=(2.42, 0.42, -0.30), rot_z=5)
    maya.pose(1, l_hip=(-96, 0, 0), r_hip=(-96, 0, 0), l_knee=(96, 0, 0), r_knee=(96, 0, 0), spine=(12, 0, 0))

    da = drawing_on_paper("drA", (-3.12, -0.10, 0.748), scale=1.0, rot_z=-6)
    dm = drawing_on_paper("drM", (2.40, -0.28, 0.308), scale=1.0, rot_z=8)
    pencil("pcA", (-2.78, -0.22, 0.76), rot=(0, 72, -30))
    pencil("pcM", (2.72, -0.40, 0.32), rot=(0, 72, 24))

    # both draw with the same rhythm — deliberately mirrored
    for f in range(sec(0.3), sec(9.0), 2):
        u = (f - sec(0.3)) / FPS
        sw = math.sin(u * 6.2)
        aarav.pose(f, r_sh=(-56 + 7 * sw, -18 - 3 * sw, 0), r_elb=(60 + 5 * sw, 0, 0),
                   l_sh=(-30, 14, 0), l_elb=(50, 0, 0), spine=(11 + 1.4 * math.sin(u * 2), 0, -3))
        aarav.look(f, x=-26, z=-4)
        maya.pose(f, r_sh=(-58 + 7 * sw, -20 - 3 * sw, 0), r_elb=(62 + 5 * sw, 0, 0),
                  l_sh=(-32, 16, 0), l_elb=(52, 0, 0), spine=(13 + 1.4 * math.sin(u * 2), 0, 3))
        maya.look(f, x=-28, z=4)
    aarav.blink([sec(2.2), sec(6.1)])
    maya.blink([sec(2.6), sec(6.5)])
    # both look up at the sky at the same moment
    for ch, s in ((aarav, -1), (maya, 1)):
        ch.pose(sec(10.2), spine=(-6, 0, 0), r_sh=(-16, s * -14, 0), r_elb=(18, 0, 0))
        ch.look(sec(10.4), x=38, z=s * 10)
        ch.smile(sec(10.8), 1.0)
        ch.pose(sec(n / FPS), spine=(-7, 0, 0), r_sh=(-14, s * -12, 0), r_elb=(16, 0, 0))
        ch.look(sec(n / FPS - 0.2), x=40, z=s * 8)

    cam = camera("cam", (0, -3.0, 1.0), (0, 0.9, 0.8), lens=34, dof=4.0, fstop=2.8)
    key_cam(cam, 1, (-2.6, -4.6, 1.35), (-2.0, 0.1, 0.92), lens=40, focus=4.8)
    key_cam(cam, sec(5.0), (-1.1, -7.0, 1.70), (-0.4, 0.2, 1.10), lens=30, focus=7.2)
    key_cam(cam, sec(9.8), (0, -9.2, 2.20), (0, 0.4, 1.40), lens=27, focus=9.4)
    key_cam(cam, n, (0, -9.6, 3.55), (0, 0.8, 2.45), lens=27, focus=10.0)
    smooth_cam(cam)
    ease_all(aarav.joints + maya.joints + [aarav.root, maya.root])


# =====================================================================
# S05 — DIFFERENT OPPORTUNITIES  (lateral contrast track)
# =====================================================================
def s05_opportunities(n):
    """One symmetrical frame: abundance on the left, a queue for one machine on the right."""
    ground("gnd", 400, GROUND_COOL)
    box("wall", (26.0, 0.3, 4.9), (0, 4.2, 2.45), (0.86, 0.84, 0.80, 1))
    box("ceil", (26.0, 11.4, 0.26), (0, 0, 4.95), (0.90, 0.89, 0.86, 1))
    for _i in range(4):
        box(f"strip{_i}", (7.0, 0.7, 0.07), (-9.0 + _i * 6.0, 1.2, 4.80), (0.99, 0.97, 0.90, 1))
    box("floor", (26.0, 11.0, 0.08), (0, 0, -0.04), (0.72, 0.70, 0.66, 1))
    box("divider", (0.26, 7.6, 4.9), (0, 1.4, 2.45), (0.74, 0.68, 0.60, 1), bevel=0.03)

    # ---------------- left: three machines, full shelves, a teacher
    for i in range(3):
        shelf(f"lsh{i}", (-5.9 + i * 2.1, 3.75, 0), 0, w=2.0, h=2.6, seed=5 + i)
    for i in range(2):
        x = -4.8 + i * 2.4
        table(f"lt{i}", 1.6, 0.8, 0.72, WOOD, TEAL, (x, 1.35, 0))
        laptop(f"ll{i}", (x, 1.30, 0.75), 4, scale=0.95)
        chair(f"lc{i}", (x, 2.25, 0), 0)
        k = crowd_kid(50 + i, (x, 2.23, 0), -5 + i * 10)
        k.sit(1, seat_z=0.44)
        k.pose(1, r_sh=(-50, -16, 0), l_sh=(-50, 16, 0), r_elb=(56, 0, 0), l_elb=(56, 0, 0), spine=(8, 0, 0))
        for f in range(1, n, 3):
            u = f / FPS
            k.pose(f, r_sh=(-50 + 4 * math.sin(u * 8 + i), -16, 0),
                   l_sh=(-50 + 4 * math.sin(u * 8 + i + 2), 16, 0),
                   r_elb=(56, 0, 0), l_elb=(56, 0, 0), spine=(8 + 1.0 * math.sin(u * 2 + i), 0, 0))
        k.blink([sec(2 + i), sec(8 + i)])
    tutor = make_adult("Tutor", 3, loc=(-7.2, 2.1, 0), rot_z=54, female=True)
    tutor.point_at(1, "r", fwd=62, out=26)
    tutor.idle(1, n, amp=0.9)
    book_stack("lbk", 4, (-2.6, 1.25, 0.75), seed=4)
    plant("lp", (-8.4, 0.8, 0), scale=1.1)

    # ---------------- right: one machine, a queue, a nearly empty shelf
    table("rt", 1.6, 0.8, 0.72, WOOD, (0.58, 0.55, 0.50, 1), (3.7, 1.35, 0))
    laptop("rl", (3.7, 1.30, 0.75), 4, scale=0.95, screen=(0.46, 0.58, 0.66, 1))
    chair("rc", (3.7, 2.25, 0), 0)
    sitter = crowd_kid(60, (3.7, 2.23, 0), -4)
    sitter.sit(1, seat_z=0.44)
    sitter.pose(1, r_sh=(-50, -16, 0), l_sh=(-50, 16, 0), r_elb=(56, 0, 0), l_elb=(56, 0, 0), spine=(8, 0, 0))
    sitter.idle(1, n, amp=0.6)
    # the queue waits in front of the desk, facing it
    for i in range(4):
        k = crowd_kid(61 + i, (3.56 + 0.16 * (i % 2), 0.42 - i * 0.74, 0), 178 + (9 if i % 2 else -9))
        k.pose(1, r_sh=(-7, -13, 0), l_sh=(-7, 13, 0), r_elb=(17, 0, 0), l_elb=(17, 0, 0))
        k.idle(1, n, amp=1.2, phase=i * 1.3)
        k.blink([sec(1.5 + i * 0.9), sec(7.0 + i * 0.7)])
        if i == 1:
            k.look(sec(3.0), x=-4, z=-26)
            k.look(sec(6.5), x=0, z=0)
    shelf("rsh", (6.3, 3.75, 0), 0, w=2.0, h=2.6, seed=2, full=False)
    books_row("rbk", 3, 5.5, 3.75, 1.33, scale=0.95, seed=3)
    box("sign", (1.7, 0.07, 0.5), (3.7, 4.0, 2.85), (0.94, 0.92, 0.86, 1), bevel=0.012)
    box("signl1", (1.2, 0.03, 0.055), (3.7, 3.95, 2.95), (0.42, 0.45, 0.50, 1))
    box("signl2", (0.85, 0.03, 0.045), (3.52, 3.95, 2.80), (0.42, 0.45, 0.50, 1))
    for i in range(2):
        box(f"crate{i}", (0.58, 0.48, 0.46), (7.9, 1.5, 0.23 + i * 0.47), (0.62, 0.47, 0.32, 1), bevel=0.015)
    plant("rp", (8.1, 0.5, 0), scale=0.8)

    cam = camera("cam", (0, -8.6, 2.15), (0, 1.4, 1.20), lens=26, dof=9.4, fstop=3.6)
    key_cam(cam, 1, (-0.5, -9.2, 1.95), (-0.2, 1.4, 1.55), lens=25, focus=10.0)
    key_cam(cam, sec(8), (0.1, -8.1, 1.88), (0, 1.4, 1.52), lens=26, focus=9.0)
    key_cam(cam, n, (0.5, -7.3, 1.82), (0.1, 1.4, 1.50), lens=27, focus=8.3)
    smooth_cam(cam)


# =====================================================================
# S06 — THE ENCOUNTER  (community science exhibition)
# =====================================================================
def _exhibit_hall(n):
    box("floor", (34, 26, 0.08), (0, 4, -0.04), (0.74, 0.72, 0.68, 1))
    box("backwall", (30, 0.35, 5.2), (0, 15.5, 2.6), (0.86, 0.84, 0.80, 1))
    for s in (-1, 1):
        box(f"sidewall{s}", (0.35, 26, 5.2), (s * 15, 4, 2.6), (0.82, 0.80, 0.76, 1))
    box("ceil", (31, 27, 0.3), (0, 4, 5.3), (0.90, 0.89, 0.86, 1))
    # roof skylights
    for i in range(4):
        box(f"sky{i}", (22, 1.1, 0.08), (0, -4 + i * 5.0, 5.14), (0.98, 0.96, 0.88, 1))
    banner("ban", (0, 15.2, 3.9), 11.0, 0.9, color=TEAL)
    box("ban.t1", (6.4, 0.03, 0.16), (0, 15.12, 4.02), (0.96, 0.95, 0.90, 1))
    box("ban.t2", (4.2, 0.03, 0.12), (0, 15.12, 3.76), (0.96, 0.95, 0.90, 1))
    for i in range(6):
        tube(f"col{i}", 0.22, 0.22, 5.2, (-13 + (i % 3) * 13, -2 + (i // 3) * 13, 2.6),
             (0.80, 0.78, 0.76, 1), seg=12)


def s06_encounter(n):
    ground("gnd", 400, GROUND_COOL)
    _exhibit_hall(n)
    rnd = random.Random(12)
    # a row of project tables along +Y, the camera travels past them
    others = []
    for i in range(5):
        x = -8.0 + i * 3.4
        table(f"t{i}", 1.7, 0.8, 0.74, WOOD, TEAL, (x, 7.4, 0))
        if i != 3:
            k = crowd_kid(70 + i, (x, 8.5, 0), 0, scale=1.0)
            k.pose(1, r_sh=(-24, -16, 0), l_sh=(-24, 16, 0), r_elb=(30, 0, 0), l_elb=(30, 0, 0))
            k.idle(1, n, amp=1.0, phase=i * 1.7)
            k.blink([sec(2 + i * 0.8), sec(9 + i * 0.6)])
            others.append(k)
            # their projects
            if i % 2 == 0:
                model_rocket(f"pr{i}", (x, 7.3, 0.77), scale=0.9)
            else:
                dna_model(f"pd{i}", (x, 7.3, 0.77), scale=0.9)
            box(f"pb{i}", (0.5, 0.03, 0.36), (x + 0.5, 7.7, 0.95), (0.92, 0.90, 0.84, 1), bevel=0.008)
    # visitors in the background
    for i in range(6):
        a = make_adult(f"vis{i}", 10 + i, loc=(-10 + i * 3.6, 11.6 + (i % 2) * 1.2, 0),
                       rot_z=rnd.uniform(-35, 35), female=i % 2 == 0)
        a.pose(1, r_sh=(-10, -12, 0), l_sh=(-10, 12, 0), r_elb=(18, 0, 0), l_elb=(18, 0, 0))
        a.idle(1, n, amp=0.8, phase=i * 0.9)
    for i in range(3):
        k = crowd_kid(80 + i, (-6 + i * 5.5, 12.4, 0), rnd.uniform(-30, 30))
        k.idle(1, n, amp=1.2, phase=i * 2.1)

    # ---- Maya's table (the one Aarav stops at) ----
    mx = 2.2
    table("tm", 1.8, 0.85, 0.74, WOOD, TEAL, (mx, 7.4, 0))
    proj, pan = solar_project("proj", (mx + 0.1, 7.3, 0.77), rot_z=-8, scale=1.3, handmade=True)
    box("label", (0.62, 0.03, 0.40), (mx - 0.62, 7.72, 0.97), (0.94, 0.92, 0.86, 1), bevel=0.008)
    box("label.l1", (0.44, 0.02, 0.045), (mx - 0.62, 7.69, 1.07), (0.35, 0.40, 0.45, 1))
    box("label.l2", (0.34, 0.02, 0.040), (mx - 0.67, 7.69, 0.99), (0.35, 0.40, 0.45, 1))
    recycled_pile("scrap", (mx + 0.72, 7.35, 0.775), seed=9, n=4, scale=0.8)

    maya = make_maya(loc=(mx + 0.05, 8.40, 0), rot_z=30)
    maya.pose(1, r_sh=(-18, -14, 0), l_sh=(-18, 14, 0), r_elb=(24, 0, 0), l_elb=(24, 0, 0))
    maya.idle(1, sec(6.0), amp=1.0)
    maya.blink([sec(1.8), sec(4.6), sec(10.5), sec(15.0)])

    aarav = make_aarav(loc=(-7.5, 5.6, 0), rot_z=90)
    # Aarav strolls along the row, slows, and stops at Maya's table
    aarav.walk(1, sec(6.4), (-7.5, 5.6, 0), (mx - 0.2, 5.9, 0), face=90, cycle=17, stride=26)
    aarav.place(sec(7.2), (mx - 0.15, 6.15, 0), 158)
    aarav.place(n, (mx - 0.15, 6.15, 0), 152)
    # he notices the project
    aarav.pose(sec(6.6), l_hip=(0, 0, 0), r_hip=(0, 0, 0), l_knee=(-4, 0, 0), r_knee=(-4, 0, 0),
               l_sh=(-8, 10, 0), r_sh=(-8, -10, 0), l_elb=(12, 0, 0), r_elb=(12, 0, 0), spine=(2, 0, 0))
    aarav.look(sec(7.0), x=-14, z=6)
    aarav.look(sec(8.0), x=-6, z=0)
    aarav.smile(sec(8.4), 1.0)
    aarav.pose(sec(9.4), r_sh=(-64, -26, 0), r_elb=(28, 0, 0), spine=(6, 0, -8))   # points at the panel
    aarav.look(sec(9.6), x=-10, z=-4)
    aarav.pose(sec(12.0), r_sh=(-28, -18, 0), r_elb=(34, 0, 0), spine=(3, 0, -2))
    aarav.look(sec(12.4), x=6, z=2)
    aarav.idle(sec(13.0), n, amp=0.8, phase=0.4)
    aarav.blink([sec(3.0), sec(7.6), sec(11.2), sec(16.0)])

    # Maya explains: gestures at her project, then proudly stands tall
    maya.pose(sec(8.8), l_sh=(-56, 24, 0), l_elb=(40, 0, 0), spine=(6, 0, 7))
    maya.look(sec(9.0), x=-12, z=-8)
    maya.pose(sec(11.0), l_sh=(-56, 44, 0), l_elb=(30, 0, 0), spine=(3, 0, 10))
    maya.smile(sec(11.4), 1.0)
    maya.look(sec(11.6), x=2, z=-14)
    maya.pose(sec(13.6), l_sh=(-24, 16, 0), l_elb=(26, 0, 0), spine=(-2, 0, 2))
    maya.look(sec(14.0), x=4, z=-6)
    maya.idle(sec(14.4), n, amp=0.9, phase=1.6)

    # the panel tracks the light as she demonstrates
    for f, a in ((1, -30), (sec(9.6), -30), (sec(11.6), -58), (sec(13.6), -24), (n, -30)):
        pan.rotation_euler = Euler((D(a), 0, 0))
        pan.keyframe_insert("rotation_euler", frame=f)

    cam = camera("cam", (-9.0, 3.0, 1.6), (-7.5, 6.6, 1.1), lens=35, dof=4.2, fstop=2.6)
    key_cam(cam, 1, (-9.8, 2.6, 1.85), (-7.4, 6.9, 1.20), lens=32, focus=5.2)
    key_cam(cam, sec(6.0), (-0.6, 2.8, 1.78), (mx - 0.4, 6.9, 1.16), lens=32, focus=4.6)
    # arc round to the side of the aisle so both faces read in profile
    key_cam(cam, sec(11.0), (mx + 4.3, 5.9, 1.52), (mx - 0.2, 7.3, 1.10), lens=40, focus=4.6)
    key_cam(cam, n, (mx + 4.9, 6.5, 1.46), (mx - 0.1, 7.4, 1.12), lens=42, focus=4.8)
    smooth_cam(cam)
    ease_all(aarav.joints + maya.joints + [aarav.root, maya.root])


# =====================================================================
# S07 — WORKING TOGETHER
# =====================================================================
def s07_together(n):
    ground("gnd", 300, GROUND_WARM)
    r = room("rm", w=7.0, d=5.4, h=2.9, wall=(0.86, 0.83, 0.77, 1), floor=FLOOR_RICH,
             win_w=2.2, win_h=1.6, win_cx=0.0, win_cz=1.62, ceiling=True)
    t = table("wt", 2.2, 1.0, 0.74, WOOD, TEAL, (0, 0.15, 0), r)
    shelf("sh", (-3.0, 0.8, 0), 90, w=1.8, h=1.7, parent=r, seed=6)
    plant("pl", (2.7, -1.2, 0), r, scale=1.1)
    poster("po", (3.38, 0.6, 1.9), 0.7, 0.9, r, (0.46, 0.62, 0.70, 1), rot_z=-90)
    fan, hub = ceiling_fan("fan", (0, -0.4, 2.78), r)

    proj, pan = solar_project("proj", (0.10, 0.10, 0.77), r, rot_z=-178, scale=1.5, handmade=True)
    recycled_pile("scrap", (-0.88, 0.05, 0.775), r, seed=3, n=5, scale=0.9)
    laptop("lap", (0.92, 0.28, 0.775), 352, r, scale=0.9)
    papers("pp", (-0.38, -0.12, 0.78), r, n=3, seed=7)
    book_stack("bk", 3, (1.02, -0.10, 0.775), r, seed=2, scale=0.9)

    aarav = make_aarav(loc=(-0.66, 1.05, 0), rot_z=34)
    maya = make_maya(loc=(0.72, 1.05, 0), rot_z=-32)

    # both work on the shared project, hands meeting over the middle
    for f in range(1, sec(9.0), 2):
        u = f / FPS
        sw = math.sin(u * 4.4)
        aarav.pose(f, r_sh=(-72 + 8 * sw, -26, 0), r_elb=(52 + 7 * sw, 0, 0),
                   l_sh=(-40, 18, 0), l_elb=(46, 0, 0), spine=(10 + 1.4 * math.sin(u * 2), 0, 6))
        maya.pose(f, l_sh=(-74 + 8 * math.sin(u * 4.4 + 1.8), 26, 0), l_elb=(54 + 7 * math.sin(u * 4.4 + 1.8), 0, 0),
                  r_sh=(-42, -18, 0), r_elb=(48, 0, 0), spine=(10 + 1.4 * math.sin(u * 2 + 1), 0, -6))
        aarav.look(f, x=-22, z=12)
        maya.look(f, x=-22, z=-12)
    aarav.blink([sec(2.1), sec(6.4), sec(13.0)])
    maya.blink([sec(2.7), sec(7.0), sec(13.6)])

    # they look at each other and celebrate
    aarav.look(sec(10.0), x=0, z=28)
    maya.look(sec(10.0), x=0, z=-28)
    aarav.smile(sec(10.4), 1.0)
    maya.smile(sec(10.4), 1.0)
    aarav.pose(sec(10.6), spine=(2, 0, 10), r_sh=(-30, -20, 0), r_elb=(40, 0, 0))
    maya.pose(sec(10.6), spine=(2, 0, -10), l_sh=(-32, 20, 0), l_elb=(42, 0, 0))
    # high five
    aarav.pose(sec(12.2), r_sh=(-22, -142, 0), r_elb=(22, 0, 0), spine=(-2, 0, 16))
    maya.pose(sec(12.2), l_sh=(-22, 142, 0), l_elb=(22, 0, 0), spine=(-2, 0, -16))
    aarav.pose(sec(13.0), r_sh=(-18, -128, 0), r_elb=(28, 0, 0), spine=(0, 0, 12))
    maya.pose(sec(13.0), l_sh=(-18, 128, 0), l_elb=(28, 0, 0), spine=(0, 0, -12))
    aarav.pose(sec(14.6), r_sh=(-34, -22, 0), r_elb=(40, 0, 0), spine=(4, 0, 8))
    maya.pose(sec(14.6), l_sh=(-36, 22, 0), l_elb=(42, 0, 0), spine=(4, 0, -8))
    aarav.look(sec(15.0), x=-10, z=16)
    maya.look(sec(15.0), x=-10, z=-16)
    aarav.idle(sec(15.2), n, amp=0.8)
    maya.idle(sec(15.2), n, amp=0.8, phase=1.1)

    for f, a in ((1, -26), (sec(5), -48), (sec(9), -18), (sec(13), -44), (n, -32)):
        pan.rotation_euler = Euler((D(a), 0, 0))
        pan.keyframe_insert("rotation_euler", frame=f)
    for f in (1, n):
        hub.rotation_euler = Euler((0, 0, (f - 1) / FPS * 2.0))
        hub.keyframe_insert("rotation_euler", frame=f)

    cam = camera("cam", (-2.1, -2.6, 1.70), (0, 0.9, 1.10), lens=40, dof=3.6, fstop=2.4)
    key_cam(cam, 1, (-2.0, -2.2, 1.68), (-0.2, 0.5, 1.10), lens=40, focus=3.2)
    key_cam(cam, sec(9), (0.05, -2.9, 1.60), (0.05, 0.5, 1.12), lens=36, focus=3.5)
    key_cam(cam, n, (2.0, -2.3, 1.70), (0.2, 0.5, 1.16), lens=40, focus=3.3)
    smooth_cam(cam)
    ease_all(aarav.joints + maya.joints + [aarav.root, maya.root])


# =====================================================================
# S08 — BUILDING EQUALITY  (the community builds the learning centre)
# =====================================================================
def s08_building(n):
    ground("gnd", 400, GROUND_WARM)
    # the centre under construction / being filled
    box("bldg", (13.0, 8.0, 4.2), (0, 7.0, 2.1), (0.88, 0.85, 0.78, 1), bevel=0.04)
    box("roof", (13.6, 8.6, 0.25), (0, 7.0, 4.3), (0.70, 0.60, 0.50, 1), bevel=0.03)
    for i in range(3):
        window_frame(f"w{i}", 1.8, 1.5, (-4.2 + i * 4.2, 3.0, 2.1))
        box(f"wg{i}", (1.8, 0.06, 1.5), (-4.2 + i * 4.2, 3.06, 2.1), GLASS)
    box("door", (1.9, 0.12, 2.5), (0, 2.98, 1.25), WOOD_DARK, bevel=0.02)
    # the sign going up over the door
    sign = empty("signg", (0, 2.86, 3.45))
    box("sign.b", (6.6, 0.10, 0.80), (0, 0, 0), TEAL, sign, bevel=0.02)
    box("sign.l1", (4.3, 0.03, 0.14), (0, -0.06, 0.14), (0.96, 0.95, 0.90, 1), sign)
    box("sign.l2", (3.0, 0.03, 0.10), (0, -0.06, -0.10), (0.96, 0.95, 0.90, 1), sign)
    for f, z in ((1, 5.6), (sec(7.5), 3.45), (n, 3.45)):
        sign.location = (0, 2.86, z)
        sign.keyframe_insert("location", frame=f)
    for f, a in ((1, -16), (sec(7.5), 0), (n, 0)):
        sign.rotation_euler = Euler((0, D(a), 0))
        sign.keyframe_insert("rotation_euler", frame=f)

    tree("t1", (-8.6, 1.0, 0), scale=1.2, seed=3)
    tree("t2", (8.8, 1.4, 0), scale=1.05, seed=9)
    tree("t3", (-11.0, 6.0, 0), scale=0.9, seed=13)
    for i in range(5):
        box(f"step{i}", (4.0 - i * 0.0, 0.42, 0.14), (0, 2.6 - i * 0.42, 0.56 - i * 0.14),
            (0.78, 0.74, 0.68, 1), bevel=0.01)
    # a van and crates of donated equipment
    box("van", (2.2, 4.4, 1.9), (-9.5, -1.6, 1.1), (0.80, 0.80, 0.84, 1), bevel=0.06)
    box("van.cab", (2.1, 1.5, 1.3), (-9.5, -4.2, 0.85), (0.56, 0.62, 0.72, 1), bevel=0.05)
    for sx, sy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
        w = tube(f"vw{sx}{sy}", 0.42, 0.42, 0.26, (-9.5 + sx * 1.0, -1.0 + sy * 2.2, 0.42),
                 (0.22, 0.22, 0.24, 1), seg=14)
        w.rotation_euler = Euler((0, D(90), 0))

    # people carrying things in
    carriers = []
    for i in range(4):
        a = make_adult(f"ad{i}", 20 + i, loc=(-7.5 + i * 0.4, -0.4 - i * 1.4, 0), rot_z=0,
                       female=i % 2 == 1)
        crate = box(f"crate{i}", (0.52, 0.40, 0.34), (0, -0.30, -0.12),
                    (0.66, 0.50, 0.34, 1) if i % 2 else (0.52, 0.60, 0.66, 1), a.spine, bevel=0.012)
        crate.location = (0, -0.34, 0.12)
        a.pose(1, r_sh=(-86, -24, 0), l_sh=(-86, 24, 0), r_elb=(56, 0, 0), l_elb=(56, 0, 0))
        p0 = (-7.6 + i * 0.5, -0.6 - i * 1.5, 0)
        p1 = (-1.6 + i * 1.1, 2.2, 0)
        fa = math.degrees(math.atan2(p1[0] - p0[0], -(p1[1] - p0[1])))
        a.walk(sec(0.2 + i * 0.5), sec(8.0 + i * 0.5), p0, p1, face=fa, cycle=19, stride=20)
        # keep the carry pose through the walk
        for f in range(sec(0.2 + i * 0.5), sec(8.0 + i * 0.5), 3):
            a.pose(f, r_sh=(-86, -24, 0), l_sh=(-86, 24, 0), r_elb=(56, 0, 0), l_elb=(56, 0, 0))
        a.place(n, p1, fa)
        carriers.append(a)
    # kids helping with books
    for i in range(3):
        k = crowd_kid(90 + i, (5.0 + i * 1.3, -1.0 - i * 1.0, 0), -20)
        bk = box(f"kb{i}", (0.26, 0.20, 0.18), (0, -0.26, 0.06), BOOK_COLORS[i], k.spine, bevel=0.01)
        k.pose(1, r_sh=(-80, -22, 0), l_sh=(-80, 22, 0), r_elb=(60, 0, 0), l_elb=(60, 0, 0))
        q0 = (5.2 + i * 1.2, -1.2 - i * 1.1, 0)
        q1 = (1.6 + i * 1.0, 2.1, 0)
        fk = math.degrees(math.atan2(q1[0] - q0[0], -(q1[1] - q0[1])))
        k.walk(sec(1.0 + i * 0.6), sec(9.0 + i * 0.6), q0, q1, face=fk, cycle=15, stride=26)
        for f in range(sec(1.0 + i * 0.6), sec(9.0 + i * 0.6), 3):
            k.pose(f, r_sh=(-80, -22, 0), l_sh=(-80, 22, 0), r_elb=(60, 0, 0), l_elb=(60, 0, 0))
        k.place(n, q1, fk)
    # two people on ladders fixing the sign
    for s in (-1, 1):
        lad = empty(f"lad{s}", (s * 3.6, 2.2, 0))
        for j in range(2):
            tube(f"lad{s}.r{j}", 0.045, 0.045, 3.3, (j * 0.42 - 0.21, 0, 1.65), WOOD, lad, seg=8)
        for j in range(7):
            box(f"lad{s}.s{j}", (0.46, 0.06, 0.05), (0, 0, 0.42 + j * 0.42), WOOD_DARK, lad)
        w = make_adult(f"fix{s}", 30 + s, loc=(s * 3.6, 2.55, 1.68), rot_z=0, female=s > 0)
        w.pose(1, l_hip=(-12, 0, 0), r_hip=(10, 0, 0), l_knee=(16, 0, 0), r_knee=(-6, 0, 0),
               r_sh=(-24, -132, 0), l_sh=(-24, 132, 0), r_elb=(26, 0, 0), l_elb=(28, 0, 0))
        for f in range(1, sec(8), 3):
            u = f / FPS
            w.pose(f, r_sh=(-24, -132 + 7 * math.sin(u * 5 + s), 0),
                   l_sh=(-24, 132 - 7 * math.sin(u * 5 + s + 2), 0),
                   r_elb=(26, 0, 0), l_elb=(28, 0, 0))
        w.pose(sec(9.5), r_sh=(-20, -80, 0), l_sh=(-20, 80, 0), r_elb=(40, 0, 0), l_elb=(42, 0, 0))
        w.idle(sec(10), n, amp=0.7, phase=s)

    cam = camera("cam", (0.5, -16.5, 6.2), (0, 3.6, 2.6), lens=36, dof=18, fstop=3.2)
    key_cam(cam, 1, (2.6, -18.5, 7.4), (0.4, 3.8, 2.8), lens=34, focus=20)
    key_cam(cam, sec(9), (0.4, -13.0, 4.6), (0, 3.6, 2.5), lens=38, focus=15)
    key_cam(cam, n, (-0.8, -10.4, 3.6), (0, 3.4, 2.5), lens=42, focus=12.5)
    smooth_cam(cam)


# =====================================================================
# S09 — ONE SHARED FUTURE  (inside the finished learning centre)
# =====================================================================
def s09_shared_future(n):
    ground("gnd", 300, GROUND_WARM)
    r = room("rm", w=12.0, d=8.5, h=3.3, wall=(0.88, 0.86, 0.80, 1), floor=(0.76, 0.70, 0.60, 1),
             win_w=2.6, win_h=1.8, win_cx=-3.2, win_cz=1.95, ceiling=True)
    # second window + banner on the back wall
    window_frame("w2", 2.6, 1.8, (3.2, 4.25, 1.95), r)
    box("w2g", (2.6, 0.06, 1.8), (3.2, 4.3, 1.95), GLASS, r)
    banner("ban", (0, 4.14, 2.95), 6.2, 0.56, r, TEAL)
    box("ban.t", (3.6, 0.03, 0.12), (0, 4.08, 2.95), (0.96, 0.95, 0.90, 1), r)
    shelf("shL", (-5.75, 1.6, 0), 90, w=2.6, h=2.2, parent=r, seed=4)
    shelf("shR", (5.75, 1.6, 0), -90, w=2.6, h=2.2, parent=r, seed=11)
    plant("p1", (-5.1, -2.6, 0), r, scale=1.2)
    plant("p2", (5.1, -2.6, 0), r, scale=1.1)
    fan, hub = ceiling_fan("fan", (0, 0.4, 3.18), r)

    # desks down both sides so the centre stays clear for the presenters
    kids = []
    for side, sx in ((0, -3.15), (1, 3.15)):
        for j in range(2):
            y = 0.9 - j * 2.0
            table(f"d{side}{j}", 1.6, 0.8, 0.70, WOOD, TEAL, (sx, y, 0), r, rot_z=0)
            if (side + j) % 2 == 0:
                laptop(f"dl{side}{j}", (sx, y - 0.05, 0.73), 186, r, scale=0.85)
            else:
                book_stack(f"db{side}{j}", 3, (sx - 0.3, y - 0.05, 0.73), r, seed=side * 5 + j)
                papers(f"dp{side}{j}", (sx + 0.3, y - 0.12, 0.735), r, n=2, seed=side + j)
            chair(f"dc{side}{j}", (sx, y + 0.86, 0), 0, parent=r)
            k = crowd_kid(100 + side * 3 + j, (sx, y + 0.84, 0), -6 if sx < 0 else 6)
            k.sit(1, seat_z=0.44)
            k.pose(1, r_sh=(-46, -16, 0), l_sh=(-46, 16, 0), r_elb=(54, 0, 0), l_elb=(54, 0, 0),
                   spine=(7, 0, 0))
            kids.append(k)
    # a child using a wheelchair at the front row
    wc = wheelchair("wc", (-1.9, -1.9, 0), 14, parent=r)
    wk = crowd_kid(120, (-1.9, -1.84, 0), 14)
    wk.sit(1, seat_z=0.46)
    wk.pose(1, r_sh=(-40, -16, 0), l_sh=(-40, 16, 0), r_elb=(50, 0, 0), l_elb=(50, 0, 0), spine=(5, 0, 0))
    kids.append(wk)

    # Aarav and Maya present their project at the front
    table("ft", 1.9, 0.9, 0.74, WOOD, TEAL, (0, 2.55, 0), r)
    proj, pan = solar_project("proj", (0, 2.50, 0.77), r, rot_z=184, scale=1.6, handmade=True)
    aarav = make_aarav(loc=(-0.90, 1.70, 0), rot_z=-12)
    maya = make_maya(loc=(0.90, 1.70, 0), rot_z=12)
    aarav.idle(1, sec(6), amp=0.9)
    maya.idle(1, sec(6), amp=0.9, phase=1.2)
    # they present, then both raise the project proudly
    aarav.pose(sec(2.0), r_sh=(-60, -26, 0), r_elb=(34, 0, 0), spine=(3, 0, -8))
    maya.pose(sec(2.6), l_sh=(-62, 26, 0), l_elb=(32, 0, 0), spine=(3, 0, 8))
    aarav.look(sec(2.2), x=-8, z=-12)
    maya.look(sec(2.8), x=-8, z=12)
    aarav.pose(sec(7.5), r_sh=(-14, -140, 0), l_sh=(-14, 136, 0), r_elb=(18, 0, 0), l_elb=(20, 0, 0),
               spine=(-5, 0, 0))
    maya.pose(sec(7.5), r_sh=(-14, -136, 0), l_sh=(-14, 140, 0), r_elb=(20, 0, 0), l_elb=(18, 0, 0),
              spine=(-5, 0, 0))
    aarav.smile(sec(7.8), 1.0)
    maya.smile(sec(7.8), 1.0)
    aarav.look(sec(8.0), x=14, z=-6)
    maya.look(sec(8.0), x=14, z=6)
    aarav.pose(sec(n / FPS), r_sh=(-12, -132, 0), l_sh=(-12, 128, 0), r_elb=(22, 0, 0), l_elb=(24, 0, 0),
               spine=(-4, 0, 0))
    maya.pose(sec(n / FPS), r_sh=(-12, -128, 0), l_sh=(-12, 132, 0), r_elb=(24, 0, 0), l_elb=(22, 0, 0),
              spine=(-4, 0, 0))
    aarav.blink([sec(3.1), sec(9.5), sec(14)])
    maya.blink([sec(3.7), sec(10.1), sec(14.6)])

    # the class applauds
    for i, k in enumerate(kids):
        k.look(sec(1.0 + i * 0.1), x=6, z=0)
        for f in range(sec(7.6), n, 2):
            u = (f - sec(7.6)) / FPS
            c = math.sin(u * 11 + i * 0.7)
            k.pose(f, r_sh=(-62, -40 - 10 * c, 0), l_sh=(-62, 40 + 10 * c, 0),
                   r_elb=(74 + 8 * c, 0, 0), l_elb=(74 + 8 * c, 0, 0), spine=(2, 0, 0))
        k.blink([sec(2 + i * 0.6), sec(11 + i * 0.4)])
    for f in (1, n):
        hub.rotation_euler = Euler((0, 0, (f - 1) / FPS * 2.0))
        hub.keyframe_insert("rotation_euler", frame=f)
    for f, a in ((1, -28), (sec(8), -46), (n, -36)):
        pan.rotation_euler = Euler((D(a), 0, 0))
        pan.keyframe_insert("rotation_euler", frame=f)

    cam = camera("cam", (0.2, -6.4, 2.3), (0, 1.6, 1.25), lens=32, dof=7.0, fstop=3.0)
    key_cam(cam, 1, (-1.5, -5.6, 1.78), (-0.3, 1.1, 1.14), lens=26, focus=6.2)
    key_cam(cam, sec(9), (0.1, -4.6, 1.86), (0, 1.3, 1.18), lens=28, focus=5.4)
    key_cam(cam, n, (0.2, -3.9, 2.40), (0, 1.6, 1.26), lens=28, focus=5.0)
    smooth_cam(cam)
    ease_all(aarav.joints + maya.joints + [aarav.root, maya.root])


# =====================================================================
# S10 — ONE SHARED FUTURE / END  (sunset exterior, the centre glowing)
# =====================================================================
def s10_credits(n):
    ground("gnd", 500, (0.72, 0.66, 0.54, 1))
    box("bldg", (13.0, 8.0, 4.2), (0, 9.0, 2.1), (0.84, 0.78, 0.68, 1), bevel=0.04)
    box("roof", (13.6, 8.6, 0.25), (0, 9.0, 4.3), (0.62, 0.50, 0.40, 1), bevel=0.03)
    for i in range(3):
        window_frame(f"w{i}", 1.8, 1.5, (-4.2 + i * 4.2, 5.0, 2.1))
        box(f"wg{i}", (1.8, 0.06, 1.5), (-4.2 + i * 4.2, 5.06, 2.1), (0.99, 0.88, 0.58, 1))
    box("door", (1.9, 0.12, 2.5), (0, 4.98, 1.25), (0.52, 0.36, 0.24, 1), bevel=0.02)
    box("doorglow", (1.5, 0.05, 2.1), (0, 4.92, 1.15), (0.99, 0.90, 0.62, 1))
    sign = empty("signg", (0, 4.86, 5.0))
    box("sign.b", (6.6, 0.10, 0.80), (0, 0, 0), TEAL, sign, bevel=0.02)
    box("sign.l1", (4.3, 0.03, 0.14), (0, -0.06, 0.14), (0.96, 0.95, 0.90, 1), sign)
    box("sign.l2", (3.0, 0.03, 0.10), (0, -0.06, -0.10), (0.96, 0.95, 0.90, 1), sign)
    for i, x in enumerate((-9.2, 9.4, -12.5, 12.8)):
        tree(f"t{i}", (x, 6.0 + (i % 2) * 3.0, 0), scale=1.1 + 0.2 * (i % 2), seed=5 + i)
    # warm pools of light spilling from the windows and the door
    for i, x in enumerate((-4.2, 0.0, 4.2)):
        box(f"pool{i}", (3.0, 2.6, 0.015), (x, 3.3, 0.012), (0.98, 0.90, 0.64, 1))
    for i in range(4):
        streetlight(f"sl{i}", (-7.5 + i * 5.0, 1.2, 0), h=3.8)
    # distant skyline
    city_block("far", (0, 52, 0), nx=7, ny=2, spacing=13.0, seed=17, height=(7, 22), trees=False)

    # the two of them walking out together
    aarav = make_aarav(loc=(-1.2, 3.4, 0), rot_z=0)
    maya = make_maya(loc=(0.5, 3.4, 0), rot_z=0)
    aarav.walk(1, sec(9.0), (-1.2, 3.6, 0), (-1.0, -2.6, 0), face=0, cycle=20, stride=23)
    maya.walk(1, sec(9.0), (0.6, 3.6, 0), (0.8, -2.6, 0), face=0, cycle=20, stride=23)
    for ch, s in ((aarav, 1), (maya, -1)):
        ch.place(sec(10.4), (-1.0 if s > 0 else 0.8, -2.8, 0), 0)
        ch.pose(sec(10.0), l_hip=(0, 0, 0), r_hip=(0, 0, 0), l_knee=(-4, 0, 0), r_knee=(-4, 0, 0),
                r_sh=(-10, -12, 0), l_sh=(-10, 12, 0), r_elb=(16, 0, 0), l_elb=(16, 0, 0))
        ch.place(n, (-1.0 if s > 0 else 0.8, -2.8, 0), s * 16)
        ch.look(sec(11.4), x=10, z=-s * 26)
        ch.smile(sec(11.8), 1.0)
        ch.idle(sec(12.0), n, amp=0.8, phase=s)
        ch.blink([sec(3), sec(7), sec(13)])
    # they wave
    aarav.pose(sec(13.2), r_sh=(-10, -128, 0), r_elb=(26, 0, 0))
    aarav.pose(sec(14.2), r_sh=(-10, -150, 0), r_elb=(14, 0, 0))
    aarav.pose(sec(15.2), r_sh=(-10, -128, 0), r_elb=(26, 0, 0))
    maya.pose(sec(13.4), l_sh=(-10, 128, 0), l_elb=(26, 0, 0))
    maya.pose(sec(14.4), l_sh=(-10, 150, 0), l_elb=(14, 0, 0))
    maya.pose(sec(15.4), l_sh=(-10, 128, 0), l_elb=(26, 0, 0))

    cam = camera("cam", (0, -9.0, 2.2), (0, 2.0, 1.6), lens=40, dof=10, fstop=3.0)
    key_cam(cam, 1, (0.4, -6.6, 1.35), (0, 2.6, 1.70), lens=42, focus=8.4)
    key_cam(cam, sec(10), (0, -9.8, 1.55), (0, 1.8, 1.95), lens=36, focus=8.8)
    key_cam(cam, n, (0, -13.8, 2.20), (0, 2.6, 2.65), lens=32, focus=12.0)
    smooth_cam(cam)
    ease_all(aarav.joints + maya.joints + [aarav.root, maya.root])


# =====================================================================
SHOTS = {
    "S01": (s01_two_worlds,   17.0, "dawn"),
    "S02": (s02_aarav_world,  16.0, "warm_home"),
    "S03": (s03_maya_world,   17.0, "modest_home"),
    "S04": (s04_same_dream,   14.0, "dream"),
    "S05": (s05_opportunities, 16.0, "neutral"),
    "S06": (s06_encounter,    19.0, "hall"),
    "S07": (s07_together,     18.0, "golden"),
    "S08": (s08_building,     17.0, "golden"),
    "S09": (s09_shared_future, 17.0, "bright"),
    "S10": (s10_credits,      20.0, "sunset"),
}
