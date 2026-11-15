"""
package.py — collect every deliverable into /mnt/user-data/outputs and a single zip.
"""
import os, shutil, zipfile, glob, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/mnt/user-data/outputs"
PKG = os.path.join(OUT, "BEHIND_TWO_WINDOWS_project")
os.makedirs(OUT, exist_ok=True)


def copy(src, dst_dir, name=None):
    if not os.path.exists(src):
        print("  missing:", src)
        return None
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, name or os.path.basename(src))
    shutil.copy2(src, dst)
    return dst


def main():
    if os.path.exists(PKG):
        shutil.rmtree(PKG)
    os.makedirs(PKG)

    film = os.path.join(HERE, "BEHIND_TWO_WINDOWS.mp4")
    copy(film, OUT)
    copy(film, PKG)

    for s in sorted(glob.glob(os.path.join(HERE, "build", "S*.mp4"))):
        copy(s, os.path.join(PKG, "shots"))
    for r in glob.glob(os.path.join(HERE, "refs", "character_reference_*.png")):
        copy(r, os.path.join(PKG, "character_references"))
        copy(r, OUT)
    for a in glob.glob(os.path.join(HERE, "audio", "vo_*.wav")):
        copy(a, os.path.join(PKG, "audio"))
    for a in ("music.wav", "sfx.wav", "narration.json"):
        copy(os.path.join(HERE, "audio", a), os.path.join(PKG, "audio"))
    for t in glob.glob(os.path.join(HERE, "titles", "*.png")):
        copy(t, os.path.join(PKG, "titles"))
    for b in glob.glob(os.path.join(HERE, "blend", "*.blend")):
        copy(b, os.path.join(PKG, "blend"))
    copy(os.path.join(HERE, "blend", "OPEN_IN_BLENDER.md"), os.path.join(PKG, "blend"))
    for f in ("rig.py", "sets.py", "shots.py", "look.py", "render3d.py",
              "audio10.py", "titles.py", "assemble10.py", "refsheet.py",
              "deckimgs.py", "package.py", "make_blends.py"):
        copy(os.path.join(HERE, f), os.path.join(PKG, "source"))
    copy(os.path.join(HERE, "deck", "build_deck10.js"), os.path.join(PKG, "source"))
    deck = os.path.join(HERE, "deck", "BEHIND_TWO_WINDOWS_presentation.pptx")
    copy(deck, PKG)
    copy(deck, OUT)
    summary = os.path.join(HERE, "PRODUCTION_SUMMARY.md")
    copy(summary, PKG)
    copy(summary, OUT)

    readme = os.path.join(PKG, "README.txt")
    with open(readme, "w") as f:
        f.write(
            "BEHIND TWO WINDOWS - SDG 10 Reduced Inequalities\n"
            "Created and presented by Anvith & Hitesh\n"
            "21CSE255T Computer Graphics and Animation - LLT-1\n\n"
            "BEHIND_TWO_WINDOWS.mp4            the finished film (1920x1080, 24 fps, 2:47)\n"
            "BEHIND_TWO_WINDOWS_presentation.pptx   12-slide production document\n"
            "PRODUCTION_SUMMARY.md             tools used, pipeline, deliverables\n"
            "shots/                            the ten sequence clips, S01-S10\n"
            "character_references/             Aarav and Maya turnaround sheets\n"
            "audio/                            narration stems, score, effects bed\n"
            "titles/                           title and end-credit cards (PNG, alpha)\n"
            "blend/                            openable Blender scenes, one per sequence\n"
            "                                  (see blend/OPEN_IN_BLENDER.md)\n"
            "source/                           every Python script that builds the film\n\n"
            "To rebuild the film from source:\n"
            "  python3 audio10.py all      # narration, score and effects\n"
            "  python3 render3d.py shots S01 S02 ... S10\n"
            "  python3 assemble10.py       # edit, titles and mix\n"
        )

    zpath = os.path.join(OUT, "BEHIND_TWO_WINDOWS_project.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for root, _, files in os.walk(PKG):
            for fn in files:
                p = os.path.join(root, fn)
                z.write(p, os.path.relpath(p, os.path.dirname(PKG)))
    print("package:", zpath, round(os.path.getsize(zpath) / 1e6, 1), "MB")
    for p in sorted(glob.glob(os.path.join(OUT, "*"))):
        print("  ", os.path.basename(p))


if __name__ == "__main__":
    main()
