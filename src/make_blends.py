"""
make_blends.py — write an openable .blend for every shot, plus a character turnaround file.

  python3 -I make_blends.py            # all ten shots + characters
  python3 -I make_blends.py S06        # just one

Each file opens with the set built, both characters animated, the camera keyframed and the
frame range already set, so pressing Space plays the shot back in the viewport.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bpy
import render3d
from look import FPS
import shots

OUT = os.path.join(HERE, "blend")
os.makedirs(OUT, exist_ok=True)


def finish(name, n):
    """Make the file pleasant to open in the GUI, then save it."""
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end, sc.frame_current = 1, n, 1
    sc.render.fps = FPS
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.film_transparent = False          # show a sky colour in the GUI
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = f"//renders/{name}_"
    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")
    sc.world.color = (0.55, 0.64, 0.74)
    # make the viewport show the same Workbench look the film was rendered with
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'SOLID'
                        space.shading.light = 'STUDIO'
                        space.shading.studio_light = 'rim.sl'
                        space.shading.color_type = 'OBJECT'
                        space.shading.show_shadows = True
                        space.shading.show_cavity = True
                        space.shading.use_world_space_lighting = True
    path = os.path.join(OUT, f"{name}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=path, compress=True)
    print(f"  {path}  ({os.path.getsize(path)/1e6:.1f} MB, {n} frames)")
    return path


def shot_file(sid):
    n, mood = render3d.build(sid)
    return finish(sid, n)


def characters_file():
    from rig import make_aarav, make_maya
    import sets as S
    from look import setup_scene, set_light
    render3d.clear()
    S.ground("ground", 40, (0.80, 0.78, 0.73, 1))
    a = make_aarav(loc=(-0.6, 0, 0), rot_z=14)
    m = make_maya(loc=(0.6, 0, 0), rot_z=-14)
    a.idle(1, 96, amp=1.0)
    m.idle(1, 96, amp=1.0, phase=1.3)
    a.blink([24, 70]); m.blink([34, 82])
    a.walk(1, 48, (-0.6, 2.2, 0), (-0.6, -1.4, 0))
    m.walk(1, 48, (0.6, 2.2, 0), (0.6, -1.4, 0))
    setup_scene(transparent=False)
    set_light(-40)
    S.camera("cam", (0.1, -4.2, 1.25), (0, 0, 0.78), lens=45)
    return finish("characters", 96)


if __name__ == "__main__":
    args = sys.argv[1:]
    ids = args if args else list(shots.SHOTS.keys())
    for sid in ids:
        if sid == "characters":
            characters_file()
        else:
            shot_file(sid)
    if not args:
        characters_file()
    print("done ->", OUT)
