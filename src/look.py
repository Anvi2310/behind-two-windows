"""
look.py — render configuration and the cinematic "look" for each sequence.

The 3D is rendered with Blender's Workbench engine over a transparent film; the sky,
colour grade, bloom, vignette and grain are composited afterwards with FFmpeg.  That keeps
the per-frame cost low enough to render a 2.5-minute film on a 2-core CPU, while still
giving per-scene art direction.
"""
import bpy, math

FPS = 24
RES_X, RES_Y = 1920, 1080          # final delivery
RENDER_X, RENDER_Y = 1280, 720     # 3D render size (upscaled in the composite)


def setup_scene(aa='5', transparent=True, res=None):
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    rx, ry = res or (RENDER_X, RENDER_Y)
    sc.render.resolution_x, sc.render.resolution_y = rx, ry
    sc.render.resolution_percentage = 100
    sc.render.fps = FPS
    sc.render.film_transparent = transparent
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.render.image_settings.compression = 15
    sc.display.render_aa = aa
    sc.display.viewport_aa = aa
    sh = sc.display.shading
    sh.light = 'STUDIO'
    sh.color_type = 'OBJECT'
    sh.show_shadows = True
    sh.shadow_intensity = 0.30
    sh.show_cavity = True
    sh.cavity_type = 'BOTH'
    sh.curvature_ridge_factor = 0.55
    sh.curvature_valley_factor = 0.85
    sh.use_world_space_lighting = True
    sh.studiolight_rotate_z = math.radians(-40)
    sh.studio_light = 'rim.sl'
    sh.use_dof = True
    return sc


def set_light(rot_z_deg, shadow=0.32, cavity=True):
    sh = bpy.context.scene.display.shading
    sh.studiolight_rotate_z = math.radians(rot_z_deg)
    sh.shadow_intensity = shadow
    sh.show_cavity = cavity


# ---------------------------------------------------------------- moods
# sky_top, sky_mid, sky_bot (RGB 0-255), sun (x%, y%, radius%, colour), grade
MOODS = {
    # Act 1 — warm sunrise over the city
    "dawn": dict(top=(58, 78, 128), mid=(206, 146, 108), bot=(246, 206, 150),
                 sun=(0.70, 0.74, 0.30, (255, 232, 186)),
                 grade=dict(contrast=1.10, bright=0.045, sat=1.12, gamma=1.10),
                 bloom=0.38, vignette=0.26, light_z=-55, haze=(246, 212, 168, 0.135)),
    # Aarav's bright, resourced home
    "warm_home": dict(top=(126, 168, 206), mid=(186, 206, 220), bot=(232, 226, 206),
                      sun=(0.78, 0.26, 0.22, (255, 244, 214)),
                      grade=dict(contrast=1.09, bright=0.060, sat=1.10, gamma=1.14),
                      bloom=0.30, vignette=0.22, light_z=-35, haze=(236, 230, 212, 0.072)),
    # Maya's home — same warmth of spirit, cooler light, smaller window
    "modest_home": dict(top=(120, 150, 180), mid=(192, 196, 192), bot=(224, 214, 192),
                        sun=(0.22, 0.30, 0.20, (255, 240, 206)),
                        grade=dict(contrast=1.10, bright=0.050, sat=1.02, gamma=1.14),
                        bloom=0.24, vignette=0.30, light_z=-128, haze=(226, 218, 200, 0.081)),
    # the shared-dream sky
    "dream": dict(top=(96, 122, 180), mid=(176, 176, 214), bot=(244, 206, 172),
                  sun=(0.50, 0.66, 0.34, (255, 228, 190)),
                  grade=dict(contrast=1.10, bright=0.050, sat=1.16, gamma=1.12),
                  bloom=0.46, vignette=0.28, light_z=-70, haze=(230, 196, 170, 0.117)),
    # neutral, even light for the contrast sequence
    "neutral": dict(top=(132, 158, 184), mid=(186, 198, 206), bot=(218, 218, 212),
                    sun=(0.50, 0.20, 0.18, (250, 248, 240)),
                    grade=dict(contrast=1.08, bright=0.048, sat=0.99, gamma=1.13),
                    bloom=0.20, vignette=0.26, light_z=-90, haze=(214, 216, 212, 0.063)),
    # the exhibition — bright, busy, hopeful
    "hall": dict(top=(150, 186, 212), mid=(208, 222, 228), bot=(240, 234, 218),
                 sun=(0.30, 0.22, 0.24, (255, 246, 222)),
                 grade=dict(contrast=1.09, bright=0.058, sat=1.12, gamma=1.14),
                 bloom=0.32, vignette=0.22, light_z=-48, haze=(234, 230, 216, 0.063)),
    # collaboration / building — golden and optimistic
    "golden": dict(top=(92, 136, 186), mid=(206, 184, 150), bot=(248, 222, 178),
                   sun=(0.26, 0.30, 0.30, (255, 238, 198)),
                   grade=dict(contrast=1.10, bright=0.062, sat=1.18, gamma=1.13),
                   bloom=0.42, vignette=0.20, light_z=-42, haze=(248, 228, 190, 0.099)),
    # the finished learning centre — bright, vibrant, green
    "bright": dict(top=(110, 168, 212), mid=(176, 212, 224), bot=(230, 236, 214),
                   sun=(0.68, 0.22, 0.26, (255, 250, 228)),
                   grade=dict(contrast=1.09, bright=0.066, sat=1.20, gamma=1.14),
                   bloom=0.38, vignette=0.18, light_z=-36, haze=(230, 238, 220, 0.063)),
    # closing sunset
    "sunset": dict(top=(40, 54, 104), mid=(214, 128, 96), bot=(252, 196, 128),
                   sun=(0.50, 0.70, 0.36, (255, 222, 168)),
                   grade=dict(contrast=1.11, bright=0.050, sat=1.22, gamma=1.11),
                   bloom=0.50, vignette=0.30, light_z=-62, haze=(250, 206, 158, 0.144)),
}


def make_sky(mood_name, path, w=RES_X, h=RES_Y):
    """Paint the sky/backdrop for a mood: vertical gradient + sun glow + soft cloud bands."""
    import numpy as np
    from PIL import Image, ImageFilter
    m = MOODS[mood_name]
    top, mid, bot = np.array(m["top"], float), np.array(m["mid"], float), np.array(m["bot"], float)
    yy = np.linspace(0, 1, h)[:, None]
    # two-segment gradient, smooth
    t1 = np.clip(yy / 0.55, 0, 1) ** 0.9
    t2 = np.clip((yy - 0.55) / 0.45, 0, 1) ** 1.1
    grad = top * (1 - t1) + mid * t1
    grad = grad * (1 - t2) + bot * t2
    img = np.repeat(grad[:, None, :], w, axis=1)
    # sun glow
    sx, sy, sr, scol = m["sun"]
    X, Y = np.meshgrid(np.linspace(0, 1, w), np.linspace(0, 1, h))
    d = np.sqrt(((X - sx) * (w / h)) ** 2 + (Y - sy) ** 2)
    glow = np.clip(1 - d / sr, 0, 1) ** 2.4
    core = np.clip(1 - d / (sr * 0.16), 0, 1) ** 1.6
    img = img + glow[..., None] * (np.array(scol, float) - img) * 0.72
    img = img + core[..., None] * (np.array(scol, float) - img) * 0.9
    # soft horizontal cloud bands
    rng = np.random.default_rng(hash(mood_name) % 9999)
    band = np.zeros((h, w))
    for _ in range(7):
        cy = rng.uniform(0.08, 0.62) * h
        th = rng.uniform(0.012, 0.045) * h
        amp = rng.uniform(0.10, 0.30)
        wob = np.sin(np.linspace(0, rng.uniform(2, 6), w) + rng.uniform(0, 6)) * th * 1.4
        band += amp * np.exp(-((np.arange(h)[:, None] - cy - wob[None, :]) ** 2) / (2 * th ** 2))
    band = np.clip(band, 0, 1)
    cloud = np.array([252, 246, 236], float)
    img = img * (1 - band[..., None] * 0.55) + cloud * band[..., None] * 0.55
    im = Image.fromarray(np.clip(img, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.2))
    im.save(path, quality=95)
    return path
