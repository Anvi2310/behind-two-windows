"""
render3d.py — build, render and composite the shots of "BEHIND TWO WINDOWS".

  python3 -I render3d.py still  S02 40        -> preview/S02_0040.jpg   (single graded frame)
  python3 -I render3d.py probe  S02           -> 3 frames + timing estimate
  python3 -I render3d.py shot   S02           -> build/S02.mp4
  python3 -I render3d.py list
"""
import os, sys, subprocess, time, math, glob

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BUILD = os.path.join(HERE, "build")
PREV = os.path.join(HERE, "preview")
FRAMES = os.path.join(HERE, "frames")
SKY = os.path.join(HERE, "sky")
for d in (BUILD, PREV, FRAMES, SKY):
    os.makedirs(d, exist_ok=True)

import bpy
from look import setup_scene, set_light, MOODS, make_sky, FPS, RES_X, RES_Y, RENDER_X, RENDER_Y


def clear():
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for d in (bpy.data.meshes, bpy.data.cameras, bpy.data.actions, bpy.data.lights):
        for b in list(d):
            if b.users == 0:
                d.remove(b)


def build(shot_id):
    """Build a shot; returns (n_frames, mood)."""
    import shots
    clear()
    fn, secs, mood = shots.SHOTS[shot_id]
    sc = setup_scene()
    set_light(MOODS[mood]["light_z"])
    n = int(round(secs * FPS))
    sc.frame_start, sc.frame_end = 1, n
    fn(n)
    return n, mood


# ---------------------------------------------------------------- compositing
def sky_for(mood):
    p = os.path.join(SKY, f"{mood}.png")
    if not os.path.exists(p):
        make_sky(mood, p)
    return p


def composite_cmd(mood, frames_glob, out, n, still=False, fps=FPS):
    m = MOODS[mood]
    g = m["grade"]
    hz = m["haze"]
    haze_col = "0x%02X%02X%02X" % hz[:3]
    bloom = m["bloom"]
    vig = m["vignette"]
    fc = (
        f"[0:v]scale={RES_X}:{RES_Y}[sky];"
        f"[1:v]scale={RES_X}:{RES_Y}:flags=lanczos[fg];"
        f"[sky][fg]overlay=format=auto:shortest=1[o];"
        # atmospheric haze toward the horizon
        f"color=c={haze_col}@1.0:s={RES_X}x{RES_Y},format=rgba,"
        f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*{hz[3]}*pow(clip(1-abs(Y-{int(RES_Y*0.52)})/{int(RES_Y*0.52)},0,1),1.6)'[hz];"
        f"[o][hz]overlay=format=auto[oh];"
        # bloom
        f"[oh]split[a][b];"
        f"[b]format=gbrp,lutrgb=r='if(gt(val,186),val,0)':g='if(gt(val,186),val,0)':b='if(gt(val,186),val,0)',"
        f"gblur=sigma=22[bl];"
        f"[a][bl]blend=all_mode=screen:all_opacity={bloom}[bo];"
        f"[bo]eq=contrast={g['contrast']}:brightness={g['bright']}:saturation={g['sat']}:gamma={g['gamma']},"
        f"vignette=PI/5:eval=init,"
        f"noise=alls=3:allf=t+u,"
        f"format=yuv420p[v]"
    )
    if still:
        return ["ffmpeg", "-y", "-loglevel", "error", "-i", sky_for(mood), "-i", frames_glob,
                "-filter_complex", fc, "-map", "[v]", "-frames:v", "1", out]
    return ["ffmpeg", "-y", "-loglevel", "error",
            "-loop", "1", "-framerate", str(fps), "-i", sky_for(mood),
            "-framerate", str(fps), "-start_number", "1", "-i", frames_glob,
            "-filter_complex", fc, "-map", "[v]",
            "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
            "-pix_fmt", "yuv420p", "-r", str(fps), out]


# ---------------------------------------------------------------- render
def render_still(shot_id, frame):
    n, mood = build(shot_id)
    sc = bpy.context.scene
    sc.frame_set(min(frame, n))
    tmp = os.path.join(PREV, f"_{shot_id}_raw.png")
    sc.render.filepath = tmp
    t = time.time()
    bpy.ops.render.render(write_still=True)
    dt = time.time() - t
    out = os.path.join(PREV, f"{shot_id}_{frame:04d}.jpg")
    subprocess.check_call(composite_cmd(mood, tmp, out, 1, still=True))
    print(f"{out}   ({dt:.2f}s render)")
    return out


def probe(shot_id, frames=(1, None, None)):
    n, mood = build(shot_id)
    sc = bpy.context.scene
    fl = [1, max(1, n // 2), n]
    tot = 0
    outs = []
    for f in fl:
        sc.frame_set(f)
        tmp = os.path.join(PREV, f"_{shot_id}_raw.png")
        sc.render.filepath = tmp
        t = time.time()
        bpy.ops.render.render(write_still=True)
        tot += time.time() - t
        out = os.path.join(PREV, f"{shot_id}_{f:04d}.jpg")
        subprocess.check_call(composite_cmd(mood, tmp, out, 1, still=True))
        outs.append(out)
    per = tot / len(fl)
    print(f"{shot_id}: {n} frames, {per:.2f}s/frame -> {n*per/60:.1f} min")
    for o in outs:
        print(o)
    return per, n


def render_shot(shot_id, skip_existing=True):
    out = os.path.join(BUILD, f"{shot_id}.mp4")
    if skip_existing and os.path.exists(out):
        print(f"{shot_id}: already rendered")
        return out
    n, mood = build(shot_id)
    sc = bpy.context.scene
    fdir = os.path.join(FRAMES, shot_id)
    os.makedirs(fdir, exist_ok=True)
    for old in glob.glob(os.path.join(fdir, "*.png")):
        os.remove(old)
    t0 = time.time()
    for f in range(1, n + 1):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(fdir, f"f{f:05d}.png")
        bpy.ops.render.render(write_still=True)
    rt = time.time() - t0
    tmp = out + ".tmp.mp4"
    subprocess.check_call(composite_cmd(mood, os.path.join(fdir, "f%05d.png"), tmp, n))
    os.replace(tmp, out)
    for old in glob.glob(os.path.join(fdir, "*.png")):
        os.remove(old)
    print(f"{shot_id}: {n} frames in {rt/60:.1f} min ({rt/n:.2f}s/f) -> {out}")
    return out


if __name__ == "__main__":
    import shots
    mode = sys.argv[1] if len(sys.argv) > 1 else "list"
    if mode == "list":
        tot = 0
        for k, (fn, secs, mood) in shots.SHOTS.items():
            print(f"{k}  {secs:5.1f}s  {mood}")
            tot += secs
        print(f"TOTAL {tot:.1f}s = {int(tot//60)}:{tot%60:04.1f}")
    elif mode == "still":
        render_still(sys.argv[2], int(sys.argv[3]))
    elif mode == "probe":
        probe(sys.argv[2])
    elif mode == "shot":
        render_shot(sys.argv[2], skip_existing=False)
    elif mode == "shots":
        for s in sys.argv[2:]:
            render_shot(s)
