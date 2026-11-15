"""
assemble10.py — final edit of "BEHIND TWO WINDOWS".

Takes the ten rendered shots, cross-dissolves them, lays the title and end-credit cards over
the picture, and mixes narration + score + effects (score and effects ducked under the voice).

  python3 assemble10.py
"""
import os, subprocess, json

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
AUD = os.path.join(HERE, "audio")
OUT = os.path.join(HERE, "BEHIND_TWO_WINDOWS.mp4")

XFADE = 0.4           # cross-dissolve between shots
from audio10 import SHOT_PLAN, NARRATION
import titles

SHOTS = [s for s, _, _ in SHOT_PLAN]
DUR = {s: d for s, d, _ in SHOT_PLAN}
OFF = {s: o for s, _, o in SHOT_PLAN}


def starts():
    """Start time of every shot on the cross-faded timeline."""
    out, t = {}, 0.0
    for i, s in enumerate(SHOTS):
        out[s] = t
        t += DUR[s] - XFADE
    return out, t + XFADE


ST, TOTAL = starts()


def build_video_filter():
    """Chain the ten shots with xfade, then lay the text cards over the result."""
    f = []
    prev = "0:v"
    acc = DUR[SHOTS[0]]
    for i in range(1, len(SHOTS)):
        off = acc - XFADE
        lab = f"x{i}"
        f.append(f"[{prev}][{i}:v]xfade=transition=fade:duration={XFADE}:offset={off:.3f}[{lab}]")
        prev = lab
        acc = off + DUR[SHOTS[i]]
    # ---- text cards -------------------------------------------------
    t10 = ST["S10"]
    cards = [
        ("t_main",   1.2,  7.6),
        ("e_title",  t10 + 2.6,  t10 + 8.2),
        ("e_tag",    t10 + 8.0,  t10 + 13.2),
        ("e_credit", t10 + 12.8, t10 + 19.6),
    ]
    n_in = len(SHOTS)
    for j, (name, t0, t1) in enumerate(cards):
        idx = n_in + j
        fin, fout = 0.7, 0.8
        f.append(f"[{idx}:v]format=rgba,"
                 f"fade=t=in:st={t0:.2f}:d={fin}:alpha=1,"
                 f"fade=t=out:st={t1 - fout:.2f}:d={fout}:alpha=1,"
                 f"setpts=PTS-STARTPTS[c{j}]")
        lab = f"o{j}"
        f.append(f"[{prev}][c{j}]overlay=0:0:enable='between(t,{t0:.2f},{t1:.2f})'[{lab}]")
        prev = lab
    f.append(f"[{prev}]format=yuv420p[v]")
    return f, len(cards)


def build_audio_filter(n_video_inputs, meta):
    """Narration placed on the timeline; music and effects ducked beneath it."""
    f = []
    labs = []
    base = n_video_inputs
    for i, m in enumerate(meta):
        idx = base + i
        ms = int(round((ST[m["shot"]] + OFF[m["shot"]]) * 1000))
        f.append(f"[{idx}:a]aresample=48000,adelay={ms}|{ms},volume=1.45[n{i}]")
        labs.append(f"[n{i}]")
    k = len(meta)
    # pad the voice bus to full length, or sidechaincompress truncates the music to it
    f.append("".join(labs) + f"amix=inputs={k}:normalize=0,alimiter=limit=0.92,"
             f"apad=whole_dur={TOTAL + 1.0:.2f},asplit=3[vo1][vo2][vo3]")
    mi, si = base + k, base + k + 1
    f.append(f"[{mi}:a]aresample=48000,volume=0.90[mus]")
    f.append(f"[{si}:a]aresample=48000,volume=0.74[sfx]")
    # duck the score and the effects under the narration
    f.append("[mus][vo1]sidechaincompress=threshold=0.018:ratio=7:attack=60:release=520:makeup=1[musd]")
    f.append("[sfx][vo2]sidechaincompress=threshold=0.020:ratio=5:attack=60:release=480:makeup=1[sfxd]")
    f.append("[musd][sfxd][vo3]amix=inputs=3:normalize=0,alimiter=limit=0.89,"
             f"afade=t=out:st={TOTAL-2.2:.2f}:d=2.0[a]")
    return f


def main():
    cards = titles.build_all()
    meta = json.load(open(os.path.join(AUD, "narration.json")))
    meta = [m for m in meta if m["shot"] in DUR]

    inputs = []
    for s in SHOTS:
        inputs += ["-i", os.path.join(BUILD, f"{s}.mp4")]
    for name in ("t_main", "e_title", "e_tag", "e_credit"):
        inputs += ["-loop", "1", "-framerate", "24", "-t", f"{TOTAL:.2f}", "-i", cards[name]]
    for m in meta:
        inputs += ["-i", os.path.join(AUD, m["file"])]
    inputs += ["-i", os.path.join(AUD, "music.wav"), "-i", os.path.join(AUD, "sfx.wav")]

    vf, n_cards = build_video_filter()
    af = build_audio_filter(len(SHOTS) + n_cards, meta)
    fc = ";".join(vf + af)

    cmd = ["ffmpeg", "-y", "-loglevel", "error", *inputs,
           "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "224k", "-movflags", "+faststart",
           "-t", f"{TOTAL:.2f}", OUT]
    print(f"timeline: {TOTAL:.1f}s = {int(TOTAL//60)}:{TOTAL%60:04.1f}")
    subprocess.check_call(cmd)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
