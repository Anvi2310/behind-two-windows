"""
make_repo.py — assemble a clean, GitHub-ready repository for "BEHIND TWO WINDOWS".

Keeps everything small enough for a normal git repo: source, Blender scenes, reference art,
the deck, and MP3 previews of the audio.  The 71 MB film and the 30 MB WAV stems are left
out of git and belong on a GitHub Release instead.
"""
import os, shutil, subprocess, glob

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "repo")


def sh(*a, **kw):
    return subprocess.run(a, cwd=kw.pop("cwd", REPO), check=kw.pop("check", True),
                          capture_output=True, text=True, **kw)


def copy(src, dstdir, name=None):
    if not os.path.exists(src):
        print("  missing", src)
        return
    os.makedirs(dstdir, exist_ok=True)
    shutil.copy2(src, os.path.join(dstdir, name or os.path.basename(src)))


def main():
    if os.path.exists(REPO):
        shutil.rmtree(REPO)
    os.makedirs(REPO)

    # ---- source
    for f in ("rig.py", "sets.py", "shots.py", "look.py", "render3d.py", "audio10.py",
              "titles.py", "assemble10.py", "refsheet.py", "deckimgs.py", "make_blends.py",
              "package.py", "make_repo.py"):
        copy(os.path.join(HERE, f), os.path.join(REPO, "src"))
    copy(os.path.join(HERE, "deck", "build_deck10.js"), os.path.join(REPO, "src"))

    # ---- Blender scenes
    for b in sorted(glob.glob(os.path.join(HERE, "blend", "*.blend"))):
        copy(b, os.path.join(REPO, "blend"))
    copy(os.path.join(HERE, "blend", "OPEN_IN_BLENDER.md"), os.path.join(REPO, "blend"))

    # ---- character references (re-encoded small)
    os.makedirs(os.path.join(REPO, "characters"), exist_ok=True)
    from PIL import Image
    for who in ("aarav", "maya"):
        p = os.path.join(HERE, "refs", f"character_reference_{who}.png")
        if os.path.exists(p):
            im = Image.open(p).convert("RGB")
            im.resize((im.width // 2, im.height // 2), Image.LANCZOS).save(
                os.path.join(REPO, "characters", f"{who}.jpg"), quality=88, optimize=True)

    # ---- stills, one per sequence
    os.makedirs(os.path.join(REPO, "stills"), exist_ok=True)
    for p in sorted(glob.glob(os.path.join(HERE, "deck", "img", "sb_S*.jpg"))):
        im = Image.open(p)
        im.resize((960, int(960 * im.height / im.width)), Image.LANCZOS).save(
            os.path.join(REPO, "stills", os.path.basename(p).replace("sb_", "")),
            quality=86, optimize=True)

    # ---- audio: MP3 previews only (the WAV stems go on a Release)
    ad = os.path.join(REPO, "audio_preview")
    os.makedirs(ad, exist_ok=True)
    for name, br in (("music.wav", "128k"), ("sfx.wav", "112k")):
        src = os.path.join(HERE, "audio", name)
        if os.path.exists(src):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-c:a", "libmp3lame",
                            "-b:a", br, os.path.join(ad, name.replace(".wav", ".mp3"))], check=True)
    vo = sorted(glob.glob(os.path.join(HERE, "audio", "vo_S*.wav")))
    if vo:
        lst = os.path.join(ad, "_vo.txt")
        with open(lst, "w") as f:
            for v in vo:
                f.write(f"file '{v}'\n")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                        "-c:a", "libmp3lame", "-b:a", "96k",
                        os.path.join(ad, "narration_all.mp3")], check=True)
        os.remove(lst)
    copy(os.path.join(HERE, "audio", "narration.json"), ad)

    # ---- docs & deck
    copy(os.path.join(HERE, "PRODUCTION_SUMMARY.md"), os.path.join(REPO, "docs"))
    copy(os.path.join(HERE, "deck", "BEHIND_TWO_WINDOWS_presentation.pptx"),
         os.path.join(REPO, "docs"))

    print("repo built at", REPO)


if __name__ == "__main__":
    main()
