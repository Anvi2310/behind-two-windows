"""
rig.py — toy-style 3D character puppets for "BEHIND TWO WINDOWS" (SDG 10).

Characters are built from primitives parented into a joint hierarchy (stop-motion puppet style):
    root -> pelvis -> spine -> neck -> head -> (hair, eyes, brows, mouth)
                   -> l_sh -> l_elb -> hand     (same for r)
                   -> l_hip -> l_knee -> foot   (same for r)
Animation = keyframing euler rotations on the joint empties.  No armature/skinning needed,
which keeps it fast to render with the Workbench engine on CPU.

All colours are per-object (Workbench OBJECT colour mode).
"""
import bpy, math, random
from mathutils import Vector, Euler

TAU = math.pi * 2
D = math.radians

# ---------------------------------------------------------------- palette
SKIN = {
    "warm":  (0.72, 0.50, 0.35, 1),
    "deep":  (0.56, 0.36, 0.24, 1),
    "light": (0.83, 0.63, 0.47, 1),
    "mid":   (0.65, 0.44, 0.30, 1),
}
HAIR_BLACK = (0.07, 0.06, 0.07, 1)
HAIR_DARK = (0.13, 0.10, 0.09, 1)
WHITE = (0.95, 0.95, 0.95, 1)
EYE_DARK = (0.10, 0.08, 0.08, 1)
MOUTH = (0.45, 0.22, 0.20, 1)

AARAV_SHIRT = (0.32, 0.55, 0.82, 1)      # blue casual shirt
AARAV_PANTS = (0.80, 0.72, 0.56, 1)      # beige trousers
AARAV_SHOES = (0.94, 0.94, 0.92, 1)      # white sneakers
MAYA_KURTA = (0.95, 0.78, 0.25, 1)       # yellow kurta
MAYA_PANTS = (0.18, 0.23, 0.42, 1)       # dark blue trousers
MAYA_SANDAL = (0.52, 0.36, 0.22, 1)      # sandals

# ---------------------------------------------------------------- helpers
def _link(ob, coll=None):
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob

def empty(name, loc=(0, 0, 0), parent=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 0.05
    e.location = loc
    _link(e)
    if parent:
        e.parent = parent
    return e

def _finish(ob, color, parent, shade_smooth=True, bevel=0.0):
    ob.color = color
    _link(ob)
    if parent:
        ob.parent = parent
    if shade_smooth:
        for p in ob.data.polygons:
            p.use_smooth = True
    if bevel:
        m = ob.modifiers.new("bev", "BEVEL")
        m.width = bevel
        m.segments = 2
        m.limit_method = 'ANGLE'
        m.angle_limit = D(40)
    return ob

def _mesh_from(primitive, name, **kw):
    """Create a primitive via bmesh so no ops/context is needed."""
    import bmesh
    bm = bmesh.new()
    if primitive == "sphere":
        bmesh.ops.create_uvsphere(bm, u_segments=kw.get("u", 20), v_segments=kw.get("v", 12),
                                  radius=kw.get("r", 1.0))
    elif primitive == "cube":
        bmesh.ops.create_cube(bm, size=kw.get("size", 1.0))
    elif primitive == "cone":
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=kw.get("seg", 16),
                              radius1=kw.get("r1", 1.0), radius2=kw.get("r2", 1.0), depth=kw.get("d", 1.0))
    elif primitive == "circle":
        bmesh.ops.create_circle(bm, cap_ends=True, segments=kw.get("seg", 24), radius=kw.get("r", 1.0))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return bpy.data.objects.new(name, me)

def ball(name, r, loc, color, parent=None, scale=(1, 1, 1), rot=(0, 0, 0), smooth=True):
    ob = _mesh_from("sphere", name, r=r)
    ob.location = loc
    ob.scale = scale
    ob.rotation_euler = Euler(rot)
    return _finish(ob, color, parent, smooth)

def box(name, size, loc, color, parent=None, rot=(0, 0, 0), bevel=0.0, smooth=False):
    """size = (x, y, z) full dimensions."""
    ob = _mesh_from("cube", name, size=1.0)
    ob.scale = (size[0], size[1], size[2])     # unit cube has edge 1.0
    ob.location = loc
    ob.rotation_euler = Euler(rot)
    return _finish(ob, color, parent, smooth, bevel)

def tube(name, r1, r2, depth, loc, color, parent=None, rot=(0, 0, 0), seg=14):
    ob = _mesh_from("cone", name, r1=r1, r2=r2, d=depth, seg=seg)
    ob.location = loc
    ob.rotation_euler = Euler(rot)
    return _finish(ob, color, parent, True)

def plane(name, size, loc, color, parent=None, rot=(0, 0, 0)):
    sx, sy = size
    ob = _mesh_from("cube", name, size=1.0)
    ob.scale = (sx, sy, 0.004)
    ob.location = loc
    ob.rotation_euler = Euler(rot)
    return _finish(ob, color, parent, False)

# ---------------------------------------------------------------- keyframes
def key(ob, frame, loc=None, rot=None, scale=None):
    if loc is not None:
        ob.location = loc
        ob.keyframe_insert("location", frame=frame)
    if rot is not None:
        ob.rotation_euler = Euler([D(a) if abs(a) > TAU else a for a in rot])
        ob.keyframe_insert("rotation_euler", frame=frame)
    if scale is not None:
        ob.scale = scale
        ob.keyframe_insert("scale", frame=frame)

def key_rot_deg(ob, frame, x=0, y=0, z=0):
    ob.rotation_euler = Euler((D(x), D(y), D(z)))
    ob.keyframe_insert("rotation_euler", frame=frame)

def fcurves_of(ob):
    """F-curves of an object, across Blender's legacy and slotted Action APIs (4.4+/5.x)."""
    ad = getattr(ob, "animation_data", None)
    if not ad or not ad.action:
        return []
    act = ad.action
    fcs = getattr(act, "fcurves", None)
    if fcs is not None:
        return list(fcs)
    out = []
    slot = getattr(ad, "action_slot", None)
    for layer in getattr(act, "layers", []):
        for strip in getattr(layer, "strips", []):
            cb = None
            try:
                cb = strip.channelbag(slot) if slot else None
            except Exception:
                cb = None
            if cb is None:
                for c in getattr(strip, "channelbags", []):
                    out.extend(c.fcurves)
            else:
                out.extend(cb.fcurves)
    return out


def smooth_fcurves(ob, handle='AUTO_CLAMPED'):
    for fc in fcurves_of(ob):
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'
            kp.handle_left_type = kp.handle_right_type = handle

def ease_all(objs):
    for o in objs:
        smooth_fcurves(o)

# ---------------------------------------------------------------- character
class Character:
    """A jointed toy puppet.  Units: metres, ~1.3 m tall for a child, 1.72 m for an adult."""

    def __init__(self, name, skin=SKIN["warm"], hair=HAIR_BLACK, top=AARAV_SHIRT,
                 bottom=AARAV_PANTS, shoes=AARAV_SHOES, child=True, ponytail=False,
                 kurta=False, loc=(0, 0, 0), rot_z=0.0, bun=False, short_hair=True,
                 glasses=False, scale=1.0):
        self.name = name
        self.child = child
        h = (1.0 if child else 1.27) * scale          # overall height factor
        self.h = h
        self.parts = []

        root = empty(f"{name}.root", loc)
        root.rotation_euler = Euler((0, 0, rot_z))
        self.root = root

        # ---- hierarchy of joints -------------------------------------
        pelvis = empty(f"{name}.pelvis", (0, 0, 0.62 * h), root)
        spine = empty(f"{name}.spine", (0, 0, 0.14 * h), pelvis)
        neck = empty(f"{name}.neck", (0, 0, 0.28 * h), spine)
        head = empty(f"{name}.head", (0, 0, 0.07 * h), neck)
        self.pelvis, self.spine, self.neck, self.head = pelvis, spine, neck, head

        body_w = (0.185 if child else 0.215) * h
        # torso: a tapered pill (narrower at the shoulders, fuller at the waist)
        torso = ball(f"{name}.torso", 1.0, (0, 0, 0.125 * h), top, spine,
                     scale=(body_w, body_w * 0.70, 0.195 * h))
        self.parts.append(torso)
        shoulder_pad = ball(f"{name}.shpad", 1.0, (0, 0, 0.245 * h), top, spine,
                            scale=(body_w * 0.93, body_w * 0.66, 0.072 * h))
        self.parts.append(shoulder_pad)
        if kurta:   # kurta falls past the hips with a soft flare
            hem = tube(f"{name}.hem", 0.205 * h, 0.178 * h, 0.17 * h, (0, 0, 0.012 * h), top, spine)
            self.parts.append(hem)
        # hips
        hips = ball(f"{name}.hips", 1.0, (0, 0, 0.012 * h), bottom,
                    pelvis, scale=(body_w * 0.90, body_w * 0.66, 0.085 * h))
        self.parts.append(hips)

        # ---- head ----------------------------------------------------
        hr = (0.175 if child else 0.155) * h
        self.head_r = hr
        skull = ball(f"{name}.skull", hr, (0, 0, hr * 0.62), skin, head, scale=(1, 0.95, 1.02))
        self.parts.append(skull)
        # ears
        for s in (-1, 1):
            self.parts.append(ball(f"{name}.ear{s}", hr * 0.24, (s * hr * 0.96, hr * 0.04, hr * 0.58),
                                   skin, head, scale=(0.5, 1, 1.25)))
        # eyes: big and clearly proud of the face surface (face front is at y = -0.95 hr)
        ez = hr * 0.70
        ex = hr * 0.375
        self.eyes = []
        for s in (-1, 1):
            w = ball(f"{name}.eyew{s}", hr * 0.255, (s * ex, -hr * 0.80, ez), WHITE, head,
                     scale=(1, 0.60, 1.14))
            i = ball(f"{name}.eyei{s}", hr * 0.150, (s * ex, -hr * 0.90, ez - hr * 0.01), EYE_DARK,
                     head, scale=(1, 0.52, 1))
            g = ball(f"{name}.eyeg{s}", hr * 0.055, (s * ex + hr * 0.07, -hr * 0.945,
                     ez + hr * 0.075), WHITE, head, scale=(1, 0.45, 1))
            self.parts += [w, i, g]
            self.eyes.append((w, i, g))
        # brows just above the eyes, sitting on the face not the hair
        self.brows = []
        for s in (-1, 1):
            b = box(f"{name}.brow{s}", (hr * 0.42, hr * 0.085, hr * 0.065),
                    (s * ex, -hr * 0.845, ez + hr * 0.285), hair, head,
                    rot=(0, D(s * -6), 0), bevel=0.004)
            self.brows.append(b)
            self.parts.append(b)
        # nose + mouth
        self.parts.append(ball(f"{name}.nose", hr * 0.105, (0, -hr * 0.90, ez - hr * 0.30), skin,
                               head, scale=(1, 0.85, 0.80)))
        self.mouth = ball(f"{name}.mouth", hr * 0.165, (0, -hr * 0.875, ez - hr * 0.60), MOUTH, head,
                          scale=(1, 0.32, 0.40))
        self.parts.append(self.mouth)

        # ---- hair ----------------------------------------------------
        cap = ball(f"{name}.hair", hr * 1.05, (0, hr * 0.16, hr * 0.74), hair, head,
                   scale=(1.0, 0.95, 1.0))
        self.parts.append(cap)
        # fringe: a flattened dome across the top of the forehead, above the brows
        fringe = ball(f"{name}.fringe", hr * 1.0, (0, -hr * 0.17, hr * 1.10), hair, head,
                      scale=(1.02, 0.92, 0.42))
        self.parts.append(fringe)
        if ponytail:
            tie = ball(f"{name}.tie", hr * 0.22, (0, hr * 1.02, hr * 0.92), (0.8, 0.25, 0.3, 1), head)
            tail = tube(f"{name}.tail", hr * 0.26, hr * 0.14, hr * 1.25, (0, hr * 1.16, hr * 0.30),
                        hair, head, rot=(D(-22), 0, 0))
            self.parts += [tie, tail]
        if bun:
            self.parts.append(ball(f"{name}.bun", hr * 0.42, (0, hr * 0.85, hr * 1.25), hair, head))
        if glasses:
            for s in (-1, 1):
                self.parts.append(tube(f"{name}.gl{s}", hr * 0.30, hr * 0.30, hr * 0.04,
                                       (s * ex, ey * 1.05, ez), (0.15, 0.15, 0.18, 1), head,
                                       rot=(D(90), 0, 0), seg=16))

        # ---- arms ----------------------------------------------------
        sh_y = 0.0
        sh_z = 0.225 * h
        sh_x = body_w * 0.86
        self.arms = {}
        for s, tag in ((-1, "l"), (1, "r")):
            shoulder = empty(f"{name}.{tag}_sh", (s * sh_x, sh_y, sh_z), spine)
            upper = tube(f"{name}.{tag}_upper", 0.045 * h, 0.040 * h, 0.21 * h,
                         (0, 0, -0.105 * h), top if kurta or True else skin, shoulder)
            elbow = empty(f"{name}.{tag}_elb", (0, 0, -0.21 * h), shoulder)
            fore = tube(f"{name}.{tag}_fore", 0.039 * h, 0.034 * h, 0.19 * h,
                        (0, 0, -0.095 * h), skin, elbow)
            hand = ball(f"{name}.{tag}_hand", 0.056 * h, (0, 0, -0.205 * h), skin, elbow,
                        scale=(1, 0.75, 1.1))
            # short sleeve for kurta/shirt
            sleeve = tube(f"{name}.{tag}_slv", 0.056 * h, 0.050 * h, 0.095 * h, (0, 0, -0.045 * h),
                          top, shoulder)
            self.parts += [upper, fore, hand, sleeve]
            self.arms[tag] = dict(sh=shoulder, elb=elbow, hand=hand)
            setattr(self, f"{tag}_sh", shoulder)
            setattr(self, f"{tag}_elb", elbow)
            setattr(self, f"{tag}_hand", hand)
            # sleeve colour: upper arm shows skin below sleeve
            upper.color = skin

        # ---- legs ----------------------------------------------------
        hip_x = body_w * 0.47
        self.legs = {}
        for s, tag in ((-1, "l"), (1, "r")):
            hip = empty(f"{name}.{tag}_hip", (s * hip_x, 0, -0.02 * h), pelvis)
            thigh = tube(f"{name}.{tag}_thigh", 0.058 * h, 0.050 * h, 0.27 * h, (0, 0, -0.135 * h),
                         bottom, hip)
            knee = empty(f"{name}.{tag}_knee", (0, 0, -0.27 * h), hip)
            shin = tube(f"{name}.{tag}_shin", 0.048 * h, 0.042 * h, 0.26 * h, (0, 0, -0.13 * h),
                        bottom, knee)
            foot = box(f"{name}.{tag}_foot", (0.085 * h, 0.17 * h, 0.065 * h),
                       (0, -0.035 * h, -0.285 * h), shoes, knee, bevel=0.012)
            self.parts += [thigh, shin, foot]
            self.legs[tag] = dict(hip=hip, knee=knee, foot=foot)
            setattr(self, f"{tag}_hip", hip)
            setattr(self, f"{tag}_knee", knee)
            setattr(self, f"{tag}_foot", foot)

        self.joints = [pelvis, spine, neck, head,
                       self.l_sh, self.r_sh, self.l_elb, self.r_elb,
                       self.l_hip, self.r_hip, self.l_knee, self.r_knee]
        self.rest()

    # ------------------------------------------------------------ posing
    def rest(self):
        """Neutral standing pose (arms slightly out, elbows soft)."""
        self.l_sh.rotation_euler = Euler((0, D(9), 0))
        self.r_sh.rotation_euler = Euler((0, D(-9), 0))
        self.l_elb.rotation_euler = Euler((D(6), 0, 0))
        self.r_elb.rotation_euler = Euler((D(6), 0, 0))

    def key_all(self, f):
        for j in self.joints:
            j.keyframe_insert("rotation_euler", frame=f)
        self.root.keyframe_insert("location", frame=f)
        self.root.keyframe_insert("rotation_euler", frame=f)

    def place(self, f, loc=None, rot_z=None):
        if loc is not None:
            self.root.location = loc
            self.root.keyframe_insert("location", frame=f)
        if rot_z is not None:
            self.root.rotation_euler = Euler((0, 0, D(rot_z)))
            self.root.keyframe_insert("rotation_euler", frame=f)

    def pose(self, f, **kw):
        """pose(f, spine=(x,y,z), l_sh=(...), head=(...)) — degrees."""
        for k, v in kw.items():
            j = getattr(self, k)
            j.rotation_euler = Euler((D(v[0]), D(v[1]), D(v[2])))
            j.keyframe_insert("rotation_euler", frame=f)

    # ------------------------------------------------------------ motion
    def idle(self, f0, f1, amp=1.0, phase=0.0, step=6):
        """Gentle breathing + micro sway so nobody is ever frozen."""
        f = f0
        i = 0
        while f <= f1:
            t = (f - f0) / 24.0
            br = math.sin(t * 1.7 + phase) * amp
            sw = math.sin(t * 0.9 + phase * 1.7) * amp
            self.spine.rotation_euler = Euler((D(1.2 * br), D(0.8 * sw), D(1.4 * sw)))
            self.spine.keyframe_insert("rotation_euler", frame=f)
            self.neck.rotation_euler = Euler((D(-0.9 * br), D(0.6 * sw), D(-1.1 * sw)))
            self.neck.keyframe_insert("rotation_euler", frame=f)
            self.pelvis.location = (0, 0, 0.62 * self.h + 0.004 * br)
            self.pelvis.keyframe_insert("location", frame=f)
            i += 1
            f += step
        return self

    def blink(self, frames):
        """frames: list of frame numbers to blink on."""
        for f in frames:
            for (w, i, g) in self.eyes:
                for ob in (w, i, g):
                    sx, sy, sz = ob.scale
                    ob.scale = (sx, sy, sz)
                    ob.keyframe_insert("scale", frame=f - 2)
                    ob.scale = (sx, sy, sz * 0.08)
                    ob.keyframe_insert("scale", frame=f)
                    ob.scale = (sx, sy, sz)
                    ob.keyframe_insert("scale", frame=f + 2)

    def look(self, f, x=0.0, z=0.0):
        """Head turn in degrees: x = up/down (+up), z = left/right."""
        self.head.rotation_euler = Euler((D(-x), 0, D(z)))
        self.head.keyframe_insert("rotation_euler", frame=f)
        self.neck.rotation_euler = Euler((D(-x * 0.35), 0, D(z * 0.4)))
        self.neck.keyframe_insert("rotation_euler", frame=f)

    def smile(self, f, amount=1.0):
        self.mouth.scale = (1 + 0.35 * amount, 0.35, 0.42 * (1 - 0.35 * amount))
        self.mouth.keyframe_insert("scale", frame=f)
        for b in self.brows:
            b.location = (b.location.x, b.location.y, b.location.z)
            b.keyframe_insert("location", frame=f)

    def walk(self, f0, f1, p0, p1, face=None, cycle=16, stride=28, fps=24, bob=True):
        """Walk from p0 to p1 between frames f0..f1 with a proper leg/arm cycle."""
        p0 = Vector(p0)
        p1 = Vector(p1)
        d = p1 - p0
        if face is None:
            # a character's face points along -Y at rot_z = 0
            face = math.degrees(math.atan2(d.x, -d.y))
        n = int(f1 - f0)
        for i in range(n + 1):
            f = f0 + i
            u = i / max(1, n)
            # ease in/out of the whole translation
            e = u * u * (3 - 2 * u)
            pos = p0 + d * e
            ph = (i / cycle) * TAU
            swing = math.sin(ph)
            swing2 = math.sin(ph + math.pi)
            lift = max(0.0, math.sin(ph))
            lift2 = max(0.0, math.sin(ph + math.pi))
            z = 0.0
            if bob:
                z = abs(math.sin(ph)) * 0.022 * self.h
            self.root.location = (pos.x, pos.y, pos.z + z)
            self.root.keyframe_insert("location", frame=f)
            self.root.rotation_euler = Euler((0, 0, D(face)))
            self.root.keyframe_insert("rotation_euler", frame=f)
            # legs
            self.l_hip.rotation_euler = Euler((D(stride * swing), 0, 0))
            self.r_hip.rotation_euler = Euler((D(stride * swing2), 0, 0))
            self.l_knee.rotation_euler = Euler((D(-max(0, -stride * swing) - 34 * lift2 * 0.45 - 4), 0, 0))
            self.r_knee.rotation_euler = Euler((D(-max(0, -stride * swing2) - 34 * lift * 0.45 - 4), 0, 0))
            for j in (self.l_hip, self.r_hip, self.l_knee, self.r_knee):
                j.keyframe_insert("rotation_euler", frame=f)
            # arms counter-swing
            self.l_sh.rotation_euler = Euler((D(-stride * 0.72 * swing), D(9), 0))
            self.r_sh.rotation_euler = Euler((D(-stride * 0.72 * swing2), D(-9), 0))
            self.l_elb.rotation_euler = Euler((D(14 + 10 * max(0, swing)), 0, 0))
            self.r_elb.rotation_euler = Euler((D(14 + 10 * max(0, swing2)), 0, 0))
            for j in (self.l_sh, self.r_sh, self.l_elb, self.r_elb):
                j.keyframe_insert("rotation_euler", frame=f)
            # torso bob/twist
            self.spine.rotation_euler = Euler((D(3), 0, D(4 * swing)))
            self.spine.keyframe_insert("rotation_euler", frame=f)
        return self

    def sit(self, f, seat_z=0.44, lean=6, spread=5):
        """Seated pose.  Places the root so the hips land on a seat at height seat_z."""
        self.pose(f, l_hip=(-84, -spread, 0), r_hip=(-84, spread, 0),
                  l_knee=(78, 0, 0), r_knee=(78, 0, 0), spine=(lean, 0, 0))
        x, y, _ = self.root.location
        self.root.location = (x, y, seat_z + 0.07 - 0.62 * self.h)
        self.root.keyframe_insert("location", frame=f)

    def point_at(self, f, hand="r", fwd=55, out=18, elbow=20):
        s = -1 if hand == "l" else 1
        self.pose(f, **{f"{hand}_sh": (-fwd, s * out, 0), f"{hand}_elb": (elbow, 0, 0)})

    def raise_arm(self, f, hand="r", up=140, fwd=10, elbow=12):
        """Raise the arm out to the side (Y) rather than forward, so it clears the face."""
        s = 1 if hand == "l" else -1
        self.pose(f, **{f"{hand}_sh": (-fwd, s * up, 0), f"{hand}_elb": (elbow, 0, 0)})

    def set_colors(self, top=None, bottom=None, shoes=None, skin=None, hair=None):
        for p in self.parts:
            n = p.name
            if top and (".torso" in n or ".hem" in n or "_slv" in n):
                p.color = top
            if bottom and (".hips" in n or "_thigh" in n or "_shin" in n):
                p.color = bottom
            if shoes and "_foot" in n:
                p.color = shoes

    def ease(self):
        ease_all(self.joints + [self.root])
        return self


# ---------------------------------------------------------------- factories
def make_aarav(loc=(0, 0, 0), rot_z=0, scale=1.0):
    return Character("Aarav", skin=SKIN["warm"], hair=HAIR_BLACK, top=AARAV_SHIRT,
                     bottom=AARAV_PANTS, shoes=AARAV_SHOES, child=True,
                     loc=loc, rot_z=D(rot_z), scale=scale)

def make_maya(loc=(0, 0, 0), rot_z=0, scale=1.0):
    return Character("Maya", skin=SKIN["mid"], hair=HAIR_BLACK, top=MAYA_KURTA,
                     bottom=MAYA_PANTS, shoes=MAYA_SANDAL, child=True, ponytail=True,
                     kurta=True, loc=loc, rot_z=D(rot_z), scale=scale)

KID_TOPS = [(0.90, 0.42, 0.38, 1), (0.45, 0.72, 0.55, 1), (0.85, 0.55, 0.78, 1),
            (0.40, 0.68, 0.80, 1), (0.95, 0.65, 0.30, 1), (0.62, 0.55, 0.85, 1)]
KID_BOTTOMS = [(0.30, 0.34, 0.45, 1), (0.52, 0.42, 0.33, 1), (0.25, 0.40, 0.38, 1),
               (0.42, 0.30, 0.35, 1)]

def make_kid(name, i, loc=(0, 0, 0), rot_z=0, scale=1.0, female=None):
    rnd = random.Random(1000 + i)
    female = rnd.random() < 0.5 if female is None else female
    return Character(name, skin=rnd.choice(list(SKIN.values())), hair=HAIR_BLACK,
                     top=KID_TOPS[i % len(KID_TOPS)], bottom=KID_BOTTOMS[i % len(KID_BOTTOMS)],
                     shoes=(0.92, 0.92, 0.90, 1) if rnd.random() < 0.5 else (0.45, 0.32, 0.22, 1),
                     child=True, ponytail=female, kurta=female and rnd.random() < 0.5,
                     loc=loc, rot_z=D(rot_z), scale=scale * rnd.uniform(0.95, 1.06))

def make_adult(name, i=0, loc=(0, 0, 0), rot_z=0, female=False, top=None, bottom=None):
    rnd = random.Random(2000 + i)
    return Character(name, skin=rnd.choice(list(SKIN.values())), hair=HAIR_DARK,
                     top=top or ((0.78, 0.38, 0.46, 1) if female else (0.40, 0.56, 0.60, 1)),
                     bottom=bottom or (0.34, 0.36, 0.46, 1),
                     shoes=(0.28, 0.24, 0.22, 1), child=False, ponytail=False,
                     bun=female, kurta=female, loc=loc, rot_z=D(rot_z))
