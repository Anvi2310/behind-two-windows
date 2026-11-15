"""
audio10.py — complete sound production for "BEHIND TWO WINDOWS" (SDG 10).

  1. NARRATION  — Kokoro-82M neural TTS, run offline through ONNX Runtime.
  2. MUSIC      — an original orchestral score synthesised from scratch with NumPy:
                  felt piano, string ensemble, warm pad, harp, timpani/low pulse.
                  Soft piano intro -> emotional strings -> hopeful orchestration ->
                  inspirational crescendo -> gentle piano ending.
  3. SFX        — morning birds, city ambience, footsteps, school/exhibition murmur,
                  pencil on paper, a small mechanical servo, children's chatter.

  python3 audio10.py narration | music | sfx | all
"""
import os, sys, json, math
import numpy as np
from scipy.signal import fftconvolve, butter, lfilter, sosfilt

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
AUD = os.path.join(HERE, "audio")
os.makedirs(AUD, exist_ok=True)

# shot id, seconds, narration offset inside the shot
SHOT_PLAN = [
    ("S01", 17.0, 2.6), ("S02", 16.0, 1.2), ("S03", 17.0, 1.2), ("S04", 14.0, 1.0),
    ("S05", 16.0, 1.2), ("S06", 19.0, 1.4), ("S07", 18.0, 1.4), ("S08", 17.0, 1.2),
    ("S09", 17.0, 1.4), ("S10", 20.0, 3.0),
]
XFADE = 0.4                                      # cross-dissolve between shots
TOTAL = sum(d for _, d, _ in SHOT_PLAN) - XFADE * (len(SHOT_PLAN) - 1)

NARRATION = {
    "S01": "Every city has millions of stories. But not every child gets the same beginning.",
    "S02": "Meet Aarav. Opportunities surround him. Education, technology and support are "
           "already part of his everyday life.",
    "S03": "Meet Maya. She has the same curiosity and ambition. But access to the opportunities "
           "she needs is not always easy.",
    "S04": "They live in the same city. They look at the same sky. And they dream of the same future.",
    "S05": "But their worlds are different. For one, opportunities are everywhere. For the other, "
           "even the simplest opportunities can feel out of reach.",
    "S06": "Then, one day, their paths crossed. Aarav discovered something remarkable. "
           "Maya's talent had never been limited by her circumstances.",
    "S07": "Sometimes, change begins with a simple opportunity. When we share knowledge, "
           "recognise talent and support one another, barriers can become bridges.",
    "S08": "An equal world is not built by one person alone. It is built when communities "
           "create opportunities for everyone.",
    "S09": "Talent has no economic background. Dreams have no social status. And every child "
           "deserves the opportunity to shine.",
    "S10": "Behind Two Windows. Created and presented by Anvith and Hitesh. "
           "Because everyone deserves a fair chance.",
}

VOICE = "af_heart"
SPEED = 0.90


def shot_start(sid):
    """Start of a shot on the cross-faded timeline."""
    t = 0.0
    for k, d, _ in SHOT_PLAN:
        if k == sid:
            return t
        t += d - XFADE
    return t


# =====================================================================
# 1. NARRATION
# =====================================================================
def make_narration():
    import soundfile as sf
    from kokoro_onnx import Kokoro
    model = os.path.join(HERE, "..", "project", "audio", "kokoro-v1.0.onnx")
    voices = os.path.join(HERE, "..", "project", "audio", "voices-v1.0.bin")
    k = Kokoro(model, voices)
    meta = []
    for sid, dur, off in SHOT_PLAN:
        samples, sr = k.create(NARRATION[sid], voice=VOICE, speed=SPEED, lang="en-us")
        path = os.path.join(AUD, f"vo_{sid}.wav")
        sf.write(path, samples, sr)
        d = len(samples) / sr
        fits = d <= dur - off - 0.3
        meta.append(dict(shot=sid, file=os.path.basename(path), start=shot_start(sid) + off,
                         duration=round(d, 3), shot_seconds=dur, offset=off, fits=fits))
        print(f"{sid}  {d:5.2f}s  (shot {dur}s, starts +{off}s) {'' if fits else '  << TOO LONG'}")
    json.dump(meta, open(os.path.join(AUD, "narration.json"), "w"), indent=2)
    print("narration total", round(sum(m["duration"] for m in meta), 1), "s")
    return meta


# =====================================================================
# 2. MUSIC — original orchestral score
# =====================================================================
rng = np.random.default_rng(23)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def env_adsr(n, a, d, s, r):
    e = np.zeros(n)
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    if a_n + d_n + r_n > n:
        f = n / (a_n + d_n + r_n + 1)
        a_n, d_n, r_n = int(a_n * f), int(d_n * f), int(r_n * f)
    s_n = max(0, n - a_n - d_n - r_n)
    i = 0
    e[i:i + a_n] = np.linspace(0, 1, a_n, endpoint=False); i += a_n
    e[i:i + d_n] = np.linspace(1, s, d_n, endpoint=False); i += d_n
    e[i:i + s_n] = s; i += s_n
    e[i:i + r_n] = np.linspace(s, 0, min(r_n, n - i), endpoint=False)
    return e[:n]


def lp(x, f, order=2):
    b, a = butter(order, min(f, SR / 2 - 200) / (SR / 2))
    return lfilter(b, a, x)


def hp(x, f, order=2):
    b, a = butter(order, max(20, min(f, SR / 2 - 200)) / (SR / 2), 'high')
    return lfilter(b, a, x)


def piano(note, dur=3.0, vel=1.0):
    """Felt-piano: inharmonic partials, fast attack, long decay, soft hammer thump."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(note)
    out = np.zeros(n)
    B = 0.0004                                   # inharmonicity
    for h, amp in ((1, 1.0), (2, 0.42), (3, 0.22), (4, 0.12), (5, 0.07), (6, 0.04)):
        fh = f * h * math.sqrt(1 + B * h * h)
        decay = 3.0 + h * 1.4
        out += amp * np.sin(2 * np.pi * fh * t + rng.uniform(0, 6.3)) * np.exp(-t * decay / 2.6)
    out *= (1 - np.exp(-t * 900))
    thump = rng.standard_normal(min(n, int(0.03 * SR)))
    thump = lp(thump, 900) * np.exp(-np.arange(len(thump)) / SR * 90)
    out[:len(thump)] += thump * 0.10
    return lp(out, 6500) * 0.17 * vel


def strings(note, dur=4.0, vel=1.0, bright=0.5):
    """String ensemble: detuned saw-ish stack, slow swell, vibrato."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(note)
    out = np.zeros(n)
    for det in (-7, -3, 0, 3, 7):
        ff = f * 2 ** (det / 1200.0)
        vib = 1 + 0.0032 * np.sin(2 * np.pi * (4.6 + rng.uniform(-.4, .4)) * t + rng.uniform(0, 6))
        ph = 2 * np.pi * np.cumsum(ff * vib) / SR + rng.uniform(0, 6.3)
        for h, amp in ((1, 1.0), (2, 0.5), (3, 0.33), (4, 0.22), (5, 0.15), (6, 0.1)):
            out += (amp / h ** 0.35) * np.sin(ph * h) * (0.5 + bright)
    out *= env_adsr(n, 0.85, 0.5, 0.86, 1.3)
    out = lp(out, 1400 + 2600 * bright)
    return out * 0.020 * vel


def pad(note, dur=4.0, vel=1.0, bright=0.4):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(note)
    out = np.zeros(n)
    for det in (-9, 0, 9):
        ff = f * 2 ** (det / 1200.0)
        for h, amp in ((1, 1.0), (2, 0.34 * bright), (3, 0.16 * bright), (4, 0.08 * bright)):
            out += amp * np.sin(2 * np.pi * ff * h * t + rng.uniform(0, 6.3))
    out *= env_adsr(n, 1.4, 0.6, 0.85, 2.0)
    return lp(out, 800 + 2000 * bright) * 0.034 * vel


def harp(note, dur=2.2, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(note)
    out = (np.sin(2 * np.pi * f * t) + 0.32 * np.sin(2 * np.pi * 2 * f * t)
           + 0.14 * np.sin(2 * np.pi * 3 * f * t))
    out *= np.exp(-t * 3.4) * (1 - np.exp(-t * 700))
    return out * 0.14 * vel


def low_pulse(note, dur=2.5, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(note)
    out = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 0.5 * t)
    out *= env_adsr(n, 0.05, 0.5, 0.5, 1.0)
    return lp(out, 200) * 0.26 * vel


def timpani(note=36, dur=2.0, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(note) * (1 + 0.35 * np.exp(-t * 22))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    noise = lp(rng.standard_normal(n), 300) * np.exp(-t * 26)
    return (tone * np.exp(-t * 3.2) + noise * 0.5) * 0.30 * vel


# --- chords (midi note numbers) -------------------------------------
C  = [48, 55, 60, 64];      Am = [45, 52, 57, 60];     F  = [41, 48, 57, 60]
G  = [43, 50, 59, 62];      Dm = [50, 57, 62, 65];     Em = [40, 47, 55, 59]
Fm = [41, 48, 56, 60];      Bb = [46, 53, 58, 62];     Csus= [48, 55, 60, 65]
Fmaj7 = [41, 48, 57, 60, 64];  Cadd9 = [48, 55, 62, 64];  Gsus = [43, 50, 60, 62]
Am7 = [45, 52, 57, 64];     Dm7 = [50, 57, 60, 65]

L = np.zeros(int((TOTAL + 6) * SR))
R = np.zeros_like(L)


def place(sig, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i < 0:
        sig = sig[-i:]; i = 0
    n = min(len(sig), len(L) - i)
    if n <= 0:
        return
    gl = gain * math.sqrt(0.5 * (1 - pan))
    gr = gain * math.sqrt(0.5 * (1 + pan))
    L[i:i + n] += sig[:n] * gl
    R[i:i + n] += sig[:n] * gr


def section(t0, t1, prog, style, bar=3.2, gain=1.0):
    """style: intro_piano | gentle | yearning | hopeful | build | triumphant | outro"""
    t = t0
    k = 0
    while t < t1 - 0.05:
        ch = prog[k % len(prog)]
        d = min(bar, t1 - t)
        root = ch[0] - 12
        if style == "intro_piano":
            for j, nt in enumerate(ch):
                place(piano(nt, d + 2.2, 0.85 if j == 0 else 0.6), t + j * 0.09, rng.uniform(-.3, .3), gain)
            place(pad(ch[0], d + 1.6, 0.5, 0.25), t, 0, gain)
        elif style == "gentle":
            for j, nt in enumerate(ch):
                place(piano(nt, d + 2.0, 0.8 if j == 0 else 0.55), t + j * 0.07, rng.uniform(-.3, .3), gain)
            place(pad(ch[0], d + 1.5, 0.7, 0.3), t, 0, gain)
            for s in range(2):
                place(harp(ch[(s + 1) % len(ch)] + 12, 1.8, 0.4), t + bar * (0.5 + 0.25 * s), 0.35, gain)
        elif style == "yearning":
            for nt in ch:
                place(strings(nt, d + 1.4, 0.95, 0.35), t, rng.uniform(-.45, .45), gain)
            place(low_pulse(root, d, 0.6), t, 0, gain)
            place(piano(ch[-1] + 12, d + 1.5, 0.5), t + bar * 0.5, 0.25, gain)
        elif style == "hopeful":
            for nt in ch:
                place(strings(nt, d + 1.2, 1.0, 0.55), t, rng.uniform(-.45, .45), gain)
            place(pad(ch[0], d + 1.2, 0.8, 0.5), t, 0, gain)
            for j, nt in enumerate(ch):
                place(piano(nt, d + 1.6, 0.7), t + j * 0.075, rng.uniform(-.25, .25), gain)
            for s in range(3):
                place(harp(ch[s % len(ch)] + 12, 1.6, 0.45), t + bar * s / 3, -0.3, gain)
            place(low_pulse(root, d, 0.7), t, 0, gain)
        elif style == "build":
            w = 0.55 + 0.45 * (t - t0) / max(0.1, t1 - t0)
            for nt in ch:
                place(strings(nt, d + 1.1, 1.05 * w, 0.62), t, rng.uniform(-.5, .5), gain)
            for j, nt in enumerate(ch):
                place(piano(nt, d + 1.4, 0.8 * w), t + j * 0.06, rng.uniform(-.3, .3), gain)
            place(low_pulse(root, d, 0.85 * w), t, 0, gain)
            place(timpani(root - 12, 1.8, 0.5 * w), t, 0, gain)
            if k % 2 == 1:
                place(timpani(root - 12, 1.4, 0.35 * w), t + bar * 0.5, 0, gain)
            for s in range(4):
                place(harp(ch[s % len(ch)] + 12, 1.3, 0.5 * w), t + bar * s / 4, 0.3, gain)
        elif style == "triumphant":
            for nt in ch + [ch[0] + 12, ch[1] + 12]:
                place(strings(nt, d + 1.2, 1.1, 0.72), t, rng.uniform(-.5, .5), gain)
            for j, nt in enumerate(ch):
                place(piano(nt, d + 1.6, 0.95), t + j * 0.05, rng.uniform(-.3, .3), gain)
                place(piano(nt + 12, d + 1.2, 0.6), t + j * 0.05 + 0.02, rng.uniform(-.3, .3), gain)
            place(low_pulse(root, d, 1.0), t, 0, gain)
            place(timpani(root - 12, 2.0, 0.7), t, 0, gain)
            for s in range(4):
                place(harp(ch[s % len(ch)] + 24, 1.2, 0.5), t + bar * s / 4, rng.uniform(-.4, .4), gain)
        elif style == "outro":
            for j, nt in enumerate(ch):
                place(piano(nt, d + 2.6, 0.72 if j == 0 else 0.48), t + j * 0.10, rng.uniform(-.3, .3), gain)
            place(pad(ch[0], d + 2.0, 0.55, 0.28), t, 0, gain)
            place(strings(ch[2], d + 1.6, 0.45, 0.3), t, 0.2, gain)
        t += bar
        k += 1


def make_music():
    s = lambda sid: shot_start(sid)
    # S01 two worlds — soft piano, dawn
    section(0.0, s("S02"), [Cadd9, Fmaj7, Am7, Gsus], "intro_piano")
    # S02 Aarav — gentle, warm
    section(s("S02"), s("S03"), [C, G, Am, F], "gentle")
    # S03 Maya — same theme, lower and softer (equal dignity, different light)
    section(s("S03"), s("S04"), [Am, F, C, G], "gentle")
    # S04 same dream — strings enter
    section(s("S04"), s("S05"), [F, C, Dm7, Gsus], "hopeful")
    # S05 different opportunities — yearning strings, sparse
    section(s("S05"), s("S06"), [Am, Em, F, Dm, Am, Bb, Fm, G], "yearning")
    # S06 the encounter — hope returns
    section(s("S06"), s("S07"), [F, C, G, Am], "hopeful")
    # S07 working together — building
    section(s("S07"), s("S08"), [C, G, Am, F], "build")
    # S08 building equality — crescendo
    section(s("S08"), s("S09"), [F, G, C, Am], "build")
    # S09 one shared future — full triumphant
    section(s("S09"), s("S10"), [C, G, Am, F], "triumphant")
    # S10 credits — gentle piano ending
    section(s("S10"), TOTAL, [Cadd9, Fmaj7, Am7, Gsus], "outro")

    def reverb(x, decay=2.4, wet=0.30):
        n = int(decay * SR)
        t = np.arange(n) / SR
        ir = rng.standard_normal(n) * np.exp(-t * (6.9 / decay))
        ir = lp(ir, 5200)
        ir /= np.sqrt((ir ** 2).sum())
        return x * (1 - wet) + fftconvolve(x, ir)[:len(x)] * wet

    l, r = reverb(L), reverb(R)
    mix = np.stack([l, r], axis=1)[:int(TOTAL * SR)]
    t = np.arange(len(mix)) / SR
    env = np.clip(t / 2.5, 0, 1) * np.clip((TOTAL - t) / 4.5, 0, 1)
    mix *= env[:, None]
    mix = mix / (np.abs(mix).max() + 1e-9) * 0.46
    import soundfile as sf
    out = os.path.join(AUD, "music.wav")
    sf.write(out, mix.astype(np.float32), SR)
    print("music ->", out, f"{len(mix)/SR:.1f}s")
    return out


# =====================================================================
# 3. SFX
# =====================================================================
def _noise(n):
    return rng.standard_normal(n)


def bird_chirp(dur=0.26, f0=2400, f1=3600, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    k = np.sin(2 * np.pi * 7 * t) * 0.5 + 0.5
    f = f0 + (f1 - f0) * k
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    x *= np.exp(-t * 11) * (1 - np.exp(-t * 300))
    return x * 0.10 * vel


def city_bed(dur, vel=1.0):
    n = int(dur * SR)
    x = lp(_noise(n), 420) * 0.9 + lp(_noise(n), 140) * 0.6
    mod = 1 + 0.25 * np.sin(2 * np.pi * 0.07 * np.arange(n) / SR)
    return x * mod * 0.030 * vel


def room_tone(dur, vel=1.0):
    n = int(dur * SR)
    return lp(_noise(n), 260) * 0.016 * vel


def footstep(vel=1.0, bright=1.0):
    n = int(0.16 * SR)
    t = np.arange(n) / SR
    x = lp(_noise(n), 900 * bright) * np.exp(-t * 42)
    x += np.sin(2 * np.pi * 95 * t) * np.exp(-t * 36) * 0.4
    return x * 0.26 * vel


def pencil_stroke(dur=0.38, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = hp(lp(_noise(n), 5200), 1600)
    x *= (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 3.1 * t))) * np.exp(-((t - dur / 2) ** 2) / (2 * (dur / 3) ** 2))
    return x * 0.055 * vel


def paper_rustle(dur=0.5, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = hp(_noise(n), 2200) * np.exp(-t * 7) * (0.5 + 0.5 * np.sin(2 * np.pi * 11 * t))
    return x * 0.07 * vel


def servo(dur=0.8, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 190 + 55 * np.sin(2 * np.pi * 2.0 * t)
    x = 0.5 * np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
    x = lp(x, 2200) * env_adsr(n, 0.05, 0.1, 0.8, 0.2)
    x += lp(_noise(n), 1400) * 0.25 * env_adsr(n, 0.05, 0.1, 0.8, 0.2)
    return x * 0.055 * vel


def chatter(dur, vel=1.0, density=5.0):
    """A crowd murmur: many short band-passed noise bursts at speech frequencies."""
    n = int(dur * SR)
    out = np.zeros(n)
    count = int(dur * density)
    for _ in range(count):
        ln = int(rng.uniform(0.18, 0.55) * SR)
        i = rng.integers(0, max(1, n - ln))
        t = np.arange(ln) / SR
        f = rng.uniform(140, 300)
        syl = np.abs(np.sin(2 * np.pi * rng.uniform(3.5, 6.5) * t))
        x = np.sin(2 * np.pi * f * t) * 0.5 + np.sin(2 * np.pi * 2 * f * t) * 0.25
        x = lp(x * syl, rng.uniform(900, 2000))
        x *= np.hanning(ln)
        out[i:i + ln] += x * rng.uniform(0.3, 1.0)
    return out * 0.030 * vel


def kid_laugh(vel=1.0):
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = 330 + 60 * np.sin(2 * np.pi * 5.5 * t)
    syl = np.abs(np.sin(2 * np.pi * 5.5 * t)) ** 2
    x = (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(2 * np.pi * 2 * np.cumsum(f) / SR))
    return lp(x * syl, 2600) * np.exp(-t * 1.1) * 0.08 * vel


def hammer_tap(vel=1.0):
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    x = lp(_noise(n), 2600) * np.exp(-t * 48) + np.sin(2 * np.pi * 420 * t) * np.exp(-t * 40) * 0.5
    return x * 0.16 * vel


def make_sfx():
    n = int(TOTAL * SR)
    SL = np.zeros(n)
    SR_ = np.zeros(n)

    def put(sig, t, pan=0.0, gain=1.0):
        i = int(t * SR)
        if i < 0 or i >= n:
            return
        m = min(len(sig), n - i)
        gl = gain * math.sqrt(0.5 * (1 - pan))
        gr = gain * math.sqrt(0.5 * (1 + pan))
        SL[i:i + m] += sig[:m] * gl
        SR_[i:i + m] += sig[:m] * gr

    s = shot_start
    # --- S01 dawn city: birds + distant traffic
    put(city_bed(17.0, 1.0), s("S01"))
    for i in range(16):
        put(bird_chirp(rng.uniform(0.18, 0.32), rng.uniform(2100, 2800), rng.uniform(3200, 4200),
                       rng.uniform(0.5, 1.0)), s("S01") + rng.uniform(0.4, 15.5), rng.uniform(-.7, .7))
    # --- S02 Aarav's room: soft room tone, typing, a page turn, footsteps of the parent
    put(room_tone(16.0, 1.0), s("S02"))
    for i in range(34):
        put(footstep(0.20, 1.4), s("S02") + 0.6 + i * 0.13, 0.1)      # key taps (light, fast)
    for i in range(7):
        put(footstep(0.85, 0.7), s("S02") + 3.7 + i * 0.46, -0.2)     # parent walking in
    put(paper_rustle(0.6, 1.0), s("S02") + 9.0, 0.15)
    put(kid_laugh(0.5), s("S02") + 10.4, -0.1)
    # --- S03 Maya's room: quieter tone, pencil, bottle/cardboard handling, a servo
    put(room_tone(17.0, 0.8), s("S03"))
    for i in range(9):
        put(pencil_stroke(rng.uniform(0.28, 0.46), rng.uniform(0.6, 1.0)),
            s("S03") + 0.8 + i * 0.62, rng.uniform(-.2, .2))
    put(paper_rustle(0.5, 0.8), s("S03") + 5.6, 0.1)
    put(servo(0.9, 0.9), s("S03") + 8.5, 0.0)
    for i in range(4):
        put(bird_chirp(0.22, 2000, 3000, 0.4), s("S03") + 11.0 + i * 1.3, 0.5)
    # --- S04 both drawing
    put(room_tone(14.0, 0.7), s("S04"))
    for i in range(16):
        put(pencil_stroke(rng.uniform(0.26, 0.44), rng.uniform(0.5, 0.9)),
            s("S04") + 0.5 + i * 0.52, -0.45 if i % 2 else 0.45)
    # --- S05 contrast: school murmur on one side, near silence on the other
    put(chatter(8.5, 0.9, density=6.0), s("S05"), -0.35)
    put(room_tone(16.0, 0.7), s("S05"))
    for i in range(10):
        put(footstep(0.5, 0.8), s("S05") + 1.0 + i * 0.5, -0.4)
    put(chatter(5.0, 0.35, density=2.0), s("S05") + 10.5, 0.35)
    # --- S06 exhibition: busy hall, footsteps approaching, servo demo, murmur
    put(chatter(19.0, 1.0, density=9.0), s("S06"), 0.0)
    put(room_tone(19.0, 0.9), s("S06"))
    for i in range(14):
        put(footstep(0.9, 1.0), s("S06") + 0.5 + i * 0.44, -0.35 + i * 0.05)
    put(servo(1.0, 1.0), s("S06") + 9.6, 0.1)
    put(servo(0.8, 0.9), s("S06") + 11.6, 0.1)
    put(kid_laugh(0.6), s("S06") + 13.2, 0.2)
    # --- S07 working together: table work, servo, a clap on the high five
    put(room_tone(18.0, 0.8), s("S07"))
    for i in range(12):
        put(hammer_tap(rng.uniform(0.3, 0.7)), s("S07") + 0.8 + i * 0.68, rng.uniform(-.3, .3))
    put(servo(1.1, 1.0), s("S07") + 5.0, 0.0)
    put(servo(0.9, 0.9), s("S07") + 9.2, 0.0)
    put(hammer_tap(1.6), s("S07") + 12.35, 0.0)        # the high five
    put(kid_laugh(0.9), s("S07") + 12.7, -0.15)
    put(kid_laugh(0.8), s("S07") + 13.0, 0.2)
    # --- S08 building the centre: outdoor air, many footsteps, hammering, a van
    put(city_bed(17.0, 0.8), s("S08"))
    for i in range(40):
        put(footstep(rng.uniform(0.4, 0.9)), s("S08") + 0.4 + i * 0.22, rng.uniform(-.6, .6))
    for i in range(14):
        put(hammer_tap(rng.uniform(0.5, 1.0)), s("S08") + 1.0 + i * 0.95, rng.uniform(-.5, .5))
    put(chatter(17.0, 0.7, density=4.0), s("S08"), 0.0)
    for i in range(5):
        put(bird_chirp(0.2, 2300, 3300, 0.4), s("S08") + 2 + i * 2.6, 0.55)
    # --- S09 the class: murmur, then applause
    put(room_tone(17.0, 0.9), s("S09"))
    put(chatter(7.5, 0.8, density=5.0), s("S09"), 0.0)
    # applause = dense short noise bursts
    for i in range(int(9.0 * 26)):
        t0 = s("S09") + 7.6 + rng.uniform(0, 9.0)
        nl = int(rng.uniform(0.016, 0.034) * SR)
        tt = np.arange(nl) / SR
        clap = hp(lp(_noise(nl), 6500), 900) * np.exp(-tt * 190)
        put(clap * rng.uniform(0.5, 1.0) * 0.26, t0, rng.uniform(-.8, .8))
    put(kid_laugh(0.7), s("S09") + 9.5, -0.3)
    put(kid_laugh(0.6), s("S09") + 11.0, 0.35)
    # --- S10 sunset: calm air, birds, two sets of footsteps walking away
    put(city_bed(20.0, 0.45), s("S10"))
    for i in range(10):
        put(bird_chirp(rng.uniform(0.2, 0.3), rng.uniform(1900, 2600), rng.uniform(2900, 3800), 0.5),
            s("S10") + rng.uniform(0.5, 16.0), rng.uniform(-.6, .6))
    for i in range(18):
        put(footstep(0.55, 0.8), s("S10") + 0.5 + i * 0.46, -0.18)
        put(footstep(0.50, 0.8), s("S10") + 0.72 + i * 0.46, 0.18)

    mix = np.stack([SL, SR_], axis=1)
    mix = mix / (np.abs(mix).max() + 1e-9) * 0.30
    t = np.arange(len(mix)) / SR
    mix *= (np.clip(t / 1.2, 0, 1) * np.clip((TOTAL - t) / 2.5, 0, 1))[:, None]
    import soundfile as sf
    out = os.path.join(AUD, "sfx.wav")
    sf.write(out, mix.astype(np.float32), SR)
    print("sfx ->", out, f"{len(mix)/SR:.1f}s")
    return out


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("narration", "all"):
        make_narration()
    if mode in ("music", "all"):
        make_music()
    if mode in ("sfx", "all"):
        make_sfx()
