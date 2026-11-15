// build_deck10.js — project presentation for "BEHIND TWO WINDOWS" (SDG 10)
const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");
const SKILL = "/root/.claude/skills/synced/926e2cc1-68cb-4ac4-86ea-4edd9c841c40_31ff3b29-45da-4a5b-9c07-111fd410e2a1/pptx";
const { applyTheme } = require(SKILL + "/scripts/apply_theme.js");

const IMG = path.join(__dirname, "img");
const REFS = path.join(__dirname, "..", "refs");
const img = (n) => path.join(IMG, n);
const has = (p) => fs.existsSync(p);

const THEME = {
  name: "Behind Two Windows",
  headFontFace: "Arial",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "0B1526", lt1: "FFFFFF", dk2: "16273F", lt2: "F6F2E8",
    accent1: "E8BA6A", accent2: "2EC4B6", accent3: "FF6B6B", accent4: "7BE495",
    accent5: "9B7BFF", accent6: "8A98AD", hlink: "2EC4B6", folHlink: "9B7BFF",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.author = "Anvith & Hitesh";
pres.title = "BEHIND TWO WINDOWS - SDG 10 animated short";
const C = pres.SchemeColor;

const FOOT = "BEHIND TWO WINDOWS  ·  SDG 10  ·  Anvith & Hitesh";
pres.defineSlideMaster({
  title: "DARK", background: { color: THEME.colors.dk1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.38, w: 12.1, h: 0.86, fontSize: 33, bold: true, color: THEME.colors.lt2, margin: 0 } } },
    { text: { text: FOOT, options: { x: 0.6, y: 7.02, w: 8, h: 0.3, fontSize: 10, color: THEME.colors.accent6, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: THEME.colors.accent6 },
});
pres.defineSlideMaster({
  title: "LIGHT", background: { color: THEME.colors.lt1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.38, w: 12.1, h: 0.86, fontSize: 33, bold: true, color: THEME.colors.dk1, margin: 0 } } },
    { text: { text: FOOT, options: { x: 0.6, y: 7.02, w: 8, h: 0.3, fontSize: 10, color: THEME.colors.accent6, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: THEME.colors.accent6 },
});
pres.defineSlideMaster({ title: "COVER", background: { color: THEME.colors.dk1 }, objects: [] });

const body = (s, t, o) => s.addText(t, Object.assign({ isTextBox: true, fontSize: 15, color: C.text1, margin: 0, valign: "top" }, o));
const card = (s, x, y, w, h, fill) => s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: fill }, rectRadius: 0.14, line: { color: fill } });
const codeBox = (s, x, y, w, h, caption, code, fs2) => {
  card(s, x, y, w, h, "0A1424");
  s.addText(caption, { isTextBox: true, x: x + 0.2, y: y + 0.1, w: w - 0.4, h: 0.3, fontSize: 11, color: "8A98AD", margin: 0 });
  s.addText(code, { isTextBox: true, x: x + 0.2, y: y + 0.44, w: w - 0.4, h: h - 0.6, fontSize: fs2 || 10, fontFace: "Courier New", color: "DDE6F0", margin: 0, valign: "top" });
};

// ---------------- 1. COVER ----------------
pres.addSection({ title: "Intro" });
{
  const s = pres.addSlide({ masterName: "COVER", sectionTitle: "Intro" });
  if (has(img("cover.jpg"))) s.addImage({ path: img("cover.jpg"), x: 0, y: 0, w: 13.33, h: 7.5 });
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 13.33, h: 7.5, fill: { color: "0B1526", transparency: 32 }, line: { color: "0B1526", transparency: 100 } });
  s.addText("BEHIND TWO WINDOWS", { isTextBox: true, x: 0.8, y: 1.85, w: 11.7, h: 1.25, fontSize: 60, bold: true, color: "F6F2E8", fontFace: "Arial", charSpacing: 7, margin: 0 });
  s.addText("Different beginnings.  Equal dreams.  One shared future.", { isTextBox: true, x: 0.85, y: 3.05, w: 11.6, h: 0.6, fontSize: 23, color: "E8BA6A", margin: 0 });
  s.addText("An original 2 min 47 s 3D animated short on UN SDG 10 — Reduced Inequalities", { isTextBox: true, x: 0.85, y: 3.72, w: 11.6, h: 0.5, fontSize: 15, color: "F6F2E8", margin: 0 });
  s.addText([{ text: "Anvith  &  Hitesh", options: { bold: true, fontSize: 22, color: "F6F2E8" } },
             { text: "\n21CSE255T · Computer Graphics and Animation · LLT-1", options: { fontSize: 14, color: "8A98AD" } }],
            { isTextBox: true, x: 0.85, y: 5.6, w: 11, h: 1.1, margin: 0, valign: "top" });
  s.addNotes("Play the film first (2:47), then walk through these slides.");
}

// ---------------- 2. THE GOAL AND THE STORY ----------------
pres.addSection({ title: "Concept" });
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Concept" });
  s.addText("SDG 10 — and the story we chose to tell it", { placeholder: "title" });
  body(s, "Goal 10 asks us to reduce inequality within and among countries. The hardest form to show on screen is not income — it is unequal access to opportunity. So we told it through two eleven-year-olds in the same city who want the same thing.",
       { x: 0.6, y: 1.4, w: 6.3, h: 1.5, fontSize: 16, color: C.text2 });
  const beats = [
    ["Same dream", "Aarav and Maya both want to be scientists. Neither is cleverer than the other."],
    ["Different access", "One has a laptop, books and a tutor. The other has a shared machine, a queue and a borrowed book."],
    ["The meeting", "At a community science exhibition Aarav finds Maya's handmade solar tracker — built from bottles and cardboard."],
    ["The change", "They build together, and the community turns that into an inclusive learning centre for everyone."],
  ];
  beats.forEach(([t, d], i) => {
    const y = 3.05 + i * 1.0;
    s.addShape(pres.ShapeType.ellipse, { x: 0.6, y: y + 0.06, w: 0.34, h: 0.34, fill: { color: ["E8BA6A", "FF6B6B", "2EC4B6", "7BE495"][i] }, line: { color: "FFFFFF" } });
    s.addText(String(i + 1), { isTextBox: true, x: 0.6, y: y + 0.06, w: 0.34, h: 0.34, fontSize: 14, bold: true, color: "0B1526", align: "center", valign: "middle", margin: 0 });
    s.addText(t, { isTextBox: true, x: 1.08, y: y, w: 1.9, h: 0.4, fontSize: 15, bold: true, color: C.text1, margin: 0 });
    s.addText(d, { isTextBox: true, x: 2.95, y: y - 0.03, w: 3.95, h: 0.95, fontSize: 12.5, color: C.text2, margin: 0, valign: "top" });
  });
  if (has(img("sb_S04.jpg"))) s.addImage({ path: img("sb_S04.jpg"), x: 7.2, y: 1.4, w: 5.5, h: 3.1 });
  s.addText("The title image: one wall, two windows, the same sky.", { isTextBox: true, x: 7.2, y: 4.55, w: 5.5, h: 0.3, fontSize: 11, italic: true, color: C.accent6, margin: 0 });
  card(s, 7.2, 5.0, 5.5, 1.75, "F3F5F9");
  body(s, [
    { text: "The rule we set ourselves:  ", options: { bold: true, color: C.text1 } },
    { text: "never show Maya as helpless and never show poverty as a costume. Inequality appears only as unequal access — a queue for one computer, a shelf with three books, a borrowed table — never as a judgement about the child.", options: { color: C.text2 } },
  ], { x: 7.42, y: 5.2, w: 5.1, h: 1.4, fontSize: 13 });
}

// ---------------- 3. CHARACTERS ----------------
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Concept" });
  s.addText("Character design and consistency", { placeholder: "title" });
  const a = path.join(REFS, "character_reference_aarav.png");
  const m = path.join(REFS, "character_reference_maya.png");
  if (has(a)) s.addImage({ path: a, x: 0.6, y: 1.35, w: 8.0, h: 1.95 });
  if (has(m)) s.addImage({ path: m, x: 0.6, y: 3.45, w: 8.0, h: 1.95 });
  card(s, 0.6, 5.6, 8.0, 1.15, "16273F");
  body(s, "Both leads are built by one parametric constructor, so every scene instantiates the same geometry, the same colours and the same proportions. Character drift — the usual failure of AI-generated shots — is impossible by construction.",
       { x: 0.8, y: 5.78, w: 7.6, h: 0.95, fontSize: 13, color: "F6F2E8" });
  if (has(img("rig.png"))) s.addImage({ path: img("rig.png"), x: 8.95, y: 1.35, w: 3.8, h: 3.17 });
  body(s, [
    { text: "13-joint puppet rig", options: { bold: true, color: THEME.colors.accent1, breakLine: true } },
    { text: "Head, spine, two arms and two legs hang off empties. Posing is a dictionary of euler angles, so a pose is one readable line of code:", options: { color: "F6F2E8", breakLine: true } },
  ], { x: 8.95, y: 4.65, w: 3.8, h: 1.3, fontSize: 12.5 });
  codeBox(s, 8.95, 5.95, 3.8, 0.9, null,
    "ch.pose(f, r_sh=(-64,-26,0),\n        r_elb=(28,0,0))", 10);
}

// ---------------- 4. STORYBOARD ----------------
pres.addSection({ title: "The film" });
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "The film" });
  s.addText("Ten sequences, 2 min 47 s", { placeholder: "title" });
  const seq = [
    ["S01", "0:00", "Two worlds", "Aerial sunrise; the camera descends to two homes."],
    ["S02", "0:17", "Aarav's world", "Laptop, books, models, a parent bringing another book."],
    ["S03", "0:33", "Maya's world", "A floor mat, a crate shelf, a solar tracker from scrap."],
    ["S04", "0:50", "The same dream", "Both draw the same laboratory; the camera lifts to one sky."],
    ["S05", "1:03", "Different opportunities", "A lateral track: three machines one side, a queue the other."],
    ["S06", "1:19", "The encounter", "The exhibition; Aarav finds Maya's project."],
    ["S07", "1:37", "Working together", "They build as equals and high-five."],
    ["S08", "1:54", "Building equality", "The community carries in the learning centre."],
    ["S09", "2:11", "One shared future", "A full class, including a child using a wheelchair."],
    ["S10", "2:28", "One shared future / end", "Sunset, the centre glowing, the credits."],
  ];
  seq.forEach(([id, tc, name, desc], i) => {
    const col = i % 5, row = Math.floor(i / 5);
    const x = 0.55 + col * 2.5, y = 1.35 + row * 2.85;
    const p = img(`sb_${id}.jpg`);
    if (has(p)) s.addImage({ path: p, x, y, w: 2.35, h: 1.32 });
    s.addText(`${tc}  ${name}`, { isTextBox: true, x, y: y + 1.38, w: 2.35, h: 0.3, fontSize: 11, bold: true, color: C.accent1, margin: 0 });
    s.addText(desc, { isTextBox: true, x, y: y + 1.66, w: 2.35, h: 0.9, fontSize: 10, color: "D6DEEA", margin: 0, valign: "top" });
  });
}

// ---------------- 5. PIPELINE ----------------
pres.addSection({ title: "Production" });
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Production" });
  s.addText("Production pipeline — the whole film is a program", { placeholder: "title" });
  if (has(img("pipeline.png"))) s.addImage({ path: img("pipeline.png"), x: 0.5, y: 1.4, w: 12.33, h: 3.14 });
  const stats = [["~2,900", "lines of Python"], ["4,104", "frames rendered"], ["2.6 s", "per frame, 2-core CPU"], ["0", "assets downloaded"]];
  stats.forEach(([b, l], i) => {
    const x = 0.6 + i * 3.1;
    card(s, x, 4.85, 2.9, 1.3, "F3F5F9");
    s.addText(b, { isTextBox: true, x: x + 0.25, y: 5.0, w: 2.4, h: 0.6, fontSize: 32, bold: true, color: ["E8BA6A", "2EC4B6", "FF6B6B", "7BE495"][i], fontFace: "Arial", margin: 0 });
    s.addText(l, { isTextBox: true, x: x + 0.25, y: 5.6, w: 2.4, h: 0.4, fontSize: 12, color: C.text2, margin: 0 });
  });
  body(s, "Nothing in the film is stock footage, a downloaded model or a generated image. Every character, prop, building, camera move, note of music and sound effect is produced by code in this repository, which is why the look stays identical from the first frame to the last.",
       { x: 0.6, y: 6.3, w: 12.1, h: 0.7, fontSize: 13.5, color: C.text2 });
}

// ---------------- 6. TOOLS ----------------
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Production" });
  s.addText("Tools and applications — and what each cost", { placeholder: "title" });
  const hdr = (t) => ({ text: t, options: { bold: true, color: "F6F2E8", fill: { color: "16273F" } } });
  const rows = [
    [hdr("Tool"), hdr("What we used it for"), hdr("Licence / cost")],
    ["Blender 5.3 (bpy module)", "All 3D: character rigs, sets, props, cameras, animation and rendering — driven headlessly from Python, no GUI", "Free, GPL"],
    ["Blender Workbench engine", "The renderer. Studio lighting + shadows + cavity gives the clay look at ~2.6 s/frame on CPU; Cycles would have needed days", "Free, with Blender"],
    ["Python 3.13 + NumPy / SciPy", "Scene construction, animation maths, the entire music and SFX synthesis", "Free, open source"],
    ["Kokoro-82M (kokoro-onnx)", "The narration voice — a neural TTS run fully offline through ONNX Runtime", "Free, Apache-2.0"],
    ["FFmpeg 6.1", "Sky compositing, grade, bloom, cross-dissolves, title overlays, audio ducking, final H.264/AAC export", "Free, LGPL"],
    ["Pillow", "Sky gradients, title cards, reference sheets, contact sheets", "Free, open source"],
    ["pptxgenjs", "This presentation", "Free, MIT"],
    ["Claude (AI assistant)", "Pair-programmer: concept, code, reviewing rendered frames and fixing staging", "Included"],
  ];
  s.addTable(rows, { x: 0.6, y: 1.35, w: 12.1, colW: [2.75, 7.15, 2.2], fontSize: 12, color: THEME.colors.dk2, border: { type: "solid", color: "E3E7ED", pt: 0.75 }, fill: { color: "FFFFFF" }, rowH: 0.52, valign: "middle", margin: 0.08 });
  body(s, "Every tool in the pipeline is free and open source. No subscriptions, credits or paid upgrades were used, and no asset was purchased or downloaded.",
       { x: 0.6, y: 6.55, w: 12.1, h: 0.4, fontSize: 13, italic: true, color: C.text2 });
}

// ---------------- 7. RIG CODE ----------------
pres.addSection({ title: "Code" });
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Code" });
  s.addText("The character rig and the walk cycle", { placeholder: "title" });
  body(s, [
    { text: "Why a puppet, not an armature", options: { bold: true, color: THEME.colors.accent1, breakLine: true } },
    { text: "Skinned armatures need weight painting and cost deformation time on every frame. Our characters are rigid parts parented into a joint hierarchy — stop-motion style. It renders faster, never produces a broken deformation, and suits the toy-like design.", options: { color: "F6F2E8", breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "The walk cycle", options: { bold: true, color: THEME.colors.accent1, breakLine: true } },
    { text: "One function drives hips, knees, shoulders, elbows, body bob and torso twist from a single phase value, and eases the translation separately — so a character can be sent anywhere with one call.", options: { color: "F6F2E8" } },
  ], { x: 0.6, y: 1.35, w: 5.4, h: 3.4, fontSize: 13.5 });
  codeBox(s, 0.6, 4.95, 5.4, 1.85, "shots.py — one line sends a character across the set",
`aarav.walk(1, sec(6.4),
           (-7.5, 5.6, 0),      # from
           (mx - 0.2, 5.9, 0),  # to
           cycle=17, stride=26)`, 11);
  codeBox(s, 6.3, 1.35, 6.4, 5.45, "rig.py — the walk cycle (abridged)",
`for i in range(n + 1):
    f  = f0 + i
    u  = i / n
    e  = u*u*(3 - 2*u)                 # ease in/out
    ph = (i / cycle) * TAU             # gait phase
    swing, swing2 = sin(ph), sin(ph + pi)
    lift,  lift2  = max(0, swing), max(0, swing2)

    # travel + vertical bob
    pos = p0 + (p1 - p0) * e
    root.location = (pos.x, pos.y,
                     abs(sin(ph)) * 0.022 * self.h)

    # legs: hips swing, knees bend on the lift
    l_hip.rotation_euler  = (D(stride * swing),  0, 0)
    r_hip.rotation_euler  = (D(stride * swing2), 0, 0)
    l_knee.rotation_euler = (D(-34 * lift2 * 0.45 - 4), 0, 0)
    r_knee.rotation_euler = (D(-34 * lift  * 0.45 - 4), 0, 0)

    # arms counter-swing, elbows soften on the forward pass
    l_sh.rotation_euler  = (D(-stride * 0.72 * swing),  D(9), 0)
    r_sh.rotation_euler  = (D(-stride * 0.72 * swing2), D(-9), 0)
    l_elb.rotation_euler = (D(14 + 10 * max(0, swing)), 0, 0)

    spine.rotation_euler = (D(3), 0, D(4 * swing))   # torso twist`, 10.5);
}

// ---------------- 8. SETS ----------------
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Code" });
  s.addText("Sets, props and a city that renders in seconds", { placeholder: "title" });
  if (has(img("city.jpg"))) s.addImage({ path: img("city.jpg"), x: 0.6, y: 1.35, w: 6.0, h: 3.38 });
  body(s, [
    { text: "Parametric set pieces", options: { bold: true, breakLine: true, color: C.text1 } },
    { text: "Tables, chairs, shelves that fill themselves with books, laptops, plants, trees, ceiling fans, a wheelchair, and walls with real window openings cut from four boxes — each is a function with dimensions, colours and a parent.", options: { color: C.text2, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "Level of detail saved the film", options: { bold: true, breakLine: true, color: C.text1 } },
    { text: "The first city gave every building its own windows: ~25,000 objects and 47 s per frame — over five hours for one shot. Three LOD levels (individual windows / per-floor strips / plain blocks) brought it to 2.4 s per frame with no visible difference at that camera distance.", options: { color: C.text2 } },
  ], { x: 6.95, y: 1.35, w: 5.75, h: 3.4, fontSize: 13.5 });
  codeBox(s, 0.6, 4.9, 12.1, 2.0, "sets.py — one switch controls how much a building is worth drawing",
`if windows and lod < 2:
    floors = max(1, min(7, int(h / 1.4)))
    if lod == 1:                      # distant: one strip per floor
        box(f"{name}.ws{fl}", (w*0.80, d + 0.05, 0.42), (0, 0, z), c, g)
    else:                             # hero: individual windows + sills
        box(f"{name}.w{fl}{cx}",  (ww, 0.05, 0.46), (x, -d/2, z), c, g)
        box(f"{name}.wb{fl}{cx}", (ww + 0.07, 0.06, 0.05), (x, -d/2, z - 0.26), sill, g)`, 11);
}

// ---------------- 9. LOOK DEV ----------------
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Code" });
  s.addText("Cinematography and look development", { placeholder: "title" });
  if (has(img("look_raw.jpg"))) s.addImage({ path: img("look_raw.jpg"), x: 0.6, y: 1.5, w: 5.9, h: 3.32 });
  if (has(img("look_graded.jpg"))) s.addImage({ path: img("look_graded.jpg"), x: 6.8, y: 1.5, w: 5.9, h: 3.32 });
  s.addText("Raw Workbench render — transparent sky", { isTextBox: true, x: 0.6, y: 4.9, w: 5.9, h: 0.3, fontSize: 12, color: C.accent6, margin: 0 });
  s.addText("After sky, haze, bloom, grade, vignette and grain", { isTextBox: true, x: 6.8, y: 4.9, w: 5.9, h: 0.3, fontSize: 12, color: C.accent1, margin: 0 });
  const items = [
    ["Camera", "Real lenses (26–52 mm), focus pulls and depth of field; every shot is a dolly or a crane, never a static frame"],
    ["Light", "Workbench studio light in world space, plus cavity shading for form and contact shadows on the ground"],
    ["Sky", "Rendered on a transparent film, then composited over a painted gradient with sun glow and cloud bands — which is also what you see through every window"],
    ["Grade", "Nine moods: warm dawn, bright home, cooler modest home, dream, neutral contrast, hall, golden, bright, sunset — the colour arc carries the story"],
  ];
  items.forEach(([t, d], i) => {
    const x = 0.6 + (i % 2) * 6.2, y = 5.35 + Math.floor(i / 2) * 0.82;
    s.addText(t, { isTextBox: true, x, y, w: 1.1, h: 0.3, fontSize: 13, bold: true, color: C.accent2, margin: 0 });
    s.addText(d, { isTextBox: true, x: x + 1.1, y: y - 0.04, w: 4.9, h: 0.78, fontSize: 11, color: "D6DEEA", margin: 0, valign: "top" });
  });
}

// ---------------- 10. AUDIO ----------------
pres.addSection({ title: "Sound" });
{
  const s = pres.addSlide({ masterName: "LIGHT", sectionTitle: "Sound" });
  s.addText("Audio — voice, an original score, and effects", { placeholder: "title" });
  const blocks = [
    ["Narration", "2EC4B6", ["Kokoro-82M neural TTS, offline via ONNX", "Voice af_heart at 0.90 speed for a", "documentary pace", "10 lines, 75.6 s of voice in a 167 s film", "Shot lengths were set from the measured", "line lengths, so picture never outruns word"]],
    ["Score", "E8BA6A", ["Written and synthesised in NumPy — no", "samples, no loops, no library", "Felt piano (inharmonic partials + hammer", "noise), string ensemble (5-way detune +", "vibrato), warm pad, harp, timpani", "Convolution reverb from shaped noise"]],
    ["Effects", "FF6B6B", ["Morning birds (FM chirps), city and room", "tone, footsteps, pencil on paper, paper", "rustle, a servo for the solar tracker,", "crowd murmur from banded noise bursts,", "children laughing, applause built from", "~230 individual claps"]],
  ];
  blocks.forEach(([t, c, lines], i) => {
    const x = 0.6 + i * 4.1;
    card(s, x, 1.35, 3.85, 3.15, "F3F5F9");
    s.addShape(pres.ShapeType.ellipse, { x: x + 0.25, y: 1.55, w: 0.42, h: 0.42, fill: { color: c }, line: { color: c } });
    s.addText(t, { isTextBox: true, x: x + 0.8, y: 1.55, w: 2.8, h: 0.42, fontSize: 18, bold: true, color: c, margin: 0, valign: "middle" });
    s.addText(lines.join("\n"), { isTextBox: true, x: x + 0.25, y: 2.12, w: 3.4, h: 2.2, fontSize: 11.5, color: C.text2, margin: 0, valign: "top" });
  });
  const arc = [["0:00", "Soft piano", "E8BA6A"], ["0:50", "Strings enter", "2EC4B6"],
               ["1:03", "Yearning, sparse", "FF6B6B"], ["1:19", "Hope returns", "7BE495"],
               ["1:37", "Building", "9B7BFF"], ["2:11", "Full crescendo", "E8BA6A"], ["2:28", "Gentle piano", "8A98AD"]];
  s.addText("Emotional arc of the score", { isTextBox: true, x: 0.6, y: 4.68, w: 6, h: 0.3, fontSize: 14, bold: true, color: C.text1, margin: 0 });
  arc.forEach(([tc, n, c], i) => {
    const x = 0.6 + i * 1.74;
    s.addShape(pres.ShapeType.roundRect, { x, y: 5.08, w: 1.6, h: 0.72, fill: { color: "F3F5F9" }, rectRadius: 0.1, line: { color: "E3E7ED" } });
    s.addText(tc, { isTextBox: true, x: x + 0.12, y: 5.14, w: 1.4, h: 0.26, fontSize: 11, bold: true, color: c, margin: 0 });
    s.addText(n, { isTextBox: true, x: x + 0.12, y: 5.38, w: 1.4, h: 0.38, fontSize: 10.5, color: C.text2, margin: 0, valign: "top" });
  });
  codeBox(s, 0.6, 5.98, 12.1, 0.95, "audio10.py — the felt piano, from first principles",
`B = 0.0004                                             # string inharmonicity
for h, amp in ((1,1.0),(2,.42),(3,.22),(4,.12),(5,.07)):
    fh = f * h * sqrt(1 + B*h*h);  out += amp*sin(2*pi*fh*t)*exp(-t*(3.0+h*1.4)/2.6)`, 10.5);
}

// ---------------- 11. EDIT & DELIVERY ----------------
pres.addSection({ title: "Delivery" });
{
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Delivery" });
  s.addText("Editing, mixing and what we are handing in", { placeholder: "title" });
  body(s, [
    { text: "One assembly pass", options: { bold: true, color: THEME.colors.accent1, breakLine: true } },
    { text: "The ten shots are cross-dissolved (0.4 s) in a single FFmpeg graph that also lays the title and end cards over the picture and mixes the audio — so the film is encoded exactly once.", options: { color: "F6F2E8", breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "The mix", options: { bold: true, color: THEME.colors.accent1, breakLine: true } },
    { text: "Narration sits on top. Score and effects are side-chain compressed against the voice, so they duck automatically whenever the narrator speaks and swell back in the gaps. A limiter holds the master at −0.4 dB.", options: { color: "F6F2E8" } },
  ], { x: 0.6, y: 1.35, w: 6.0, h: 3.0, fontSize: 13.5 });
  codeBox(s, 0.6, 4.5, 6.0, 2.3, "assemble10.py — ducking the score under the voice",
`[mus][vo1]sidechaincompress=
    threshold=0.018:ratio=7:
    attack=60:release=520:makeup=1[musd]

[musd][sfxd][vo3]amix=inputs=3:
    normalize=0,alimiter=limit=0.95[a]`, 11);
  const deliv = [
    ["BEHIND_TWO_WINDOWS.mp4", "the film — 1920×1080, 24 fps, H.264 + AAC, 2:47"],
    ["shots/S01–S10.mp4", "the ten individual sequence clips"],
    ["character_reference_*.png", "Aarav and Maya turnaround sheets"],
    ["audio/vo_S01–S10.wav", "the narration stems, one per sequence"],
    ["audio/music.wav · sfx.wav", "the score and the effects bed, separately"],
    ["source/*.py", "every script: rig, sets, shots, look, render, audio, assembly"],
    ["this deck (.pptx)", "the production document"],
  ];
  s.addText("Deliverables", { isTextBox: true, x: 6.95, y: 1.35, w: 5.8, h: 0.35, fontSize: 16, bold: true, color: C.accent1, margin: 0 });
  deliv.forEach(([f, d], i) => {
    const y = 1.78 + i * 0.72;
    card(s, 6.95, y, 5.78, 0.62, "16273F");
    s.addText(f, { isTextBox: true, x: 7.12, y: y + 0.05, w: 5.45, h: 0.26, fontSize: 11.5, bold: true, fontFace: "Courier New", color: "F6F2E8", margin: 0 });
    s.addText(d, { isTextBox: true, x: 7.12, y: y + 0.31, w: 5.45, h: 0.26, fontSize: 10.5, color: "9FB0C6", margin: 0 });
  });
}

// ---------------- 12. CLOSE ----------------
{
  const s = pres.addSlide({ masterName: "COVER", sectionTitle: "Delivery" });
  if (has(img("close.jpg"))) s.addImage({ path: img("close.jpg"), x: 0, y: 0, w: 13.33, h: 7.5 });
  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 13.33, h: 7.5, fill: { color: "0B1526", transparency: 38 }, line: { color: "0B1526", transparency: 100 } });
  const probs = [
    ["No GPU", "EEVEE and Cycles were unusable on a 2-core CPU, so we built the look around the Workbench rasteriser and did the atmosphere in post."],
    ["Camera maths", "Our first aim-at function pointed the camera backwards; every early frame was an empty field. Fixed by deriving the euler from the look vector properly."],
    ["Staging", "Characters faced away from their own desks until we corrected the rig's facing convention, then restaged all ten shots."],
  ];
  s.addText("What was hard", { isTextBox: true, x: 0.8, y: 0.75, w: 11.7, h: 0.5, fontSize: 28, bold: true, color: "F6F2E8", margin: 0 });
  probs.forEach(([t, d], i) => {
    const x = 0.8 + i * 4.05;
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.45, w: 3.8, h: 2.1, fill: { color: "0E1B2E", transparency: 18 }, rectRadius: 0.14, line: { color: "2A3B55" } });
    s.addText(t, { isTextBox: true, x: x + 0.22, y: 1.62, w: 3.4, h: 0.35, fontSize: 15, bold: true, color: "E8BA6A", margin: 0 });
    s.addText(d, { isTextBox: true, x: x + 0.22, y: 2.0, w: 3.4, h: 1.4, fontSize: 11.5, color: "DCE4EF", margin: 0, valign: "top" });
  });
  s.addText("Different beginnings.  Equal dreams.  One shared future.", { isTextBox: true, x: 0.8, y: 4.35, w: 11.7, h: 0.65, fontSize: 30, bold: true, color: "F6F2E8", margin: 0 });
  s.addText("“Because everyone deserves a fair chance.”", { isTextBox: true, x: 0.8, y: 5.05, w: 11.7, h: 0.5, fontSize: 19, color: "E8BA6A", margin: 0 });
  s.addText([{ text: "Anvith  &  Hitesh", options: { bold: true, fontSize: 21, color: "F6F2E8" } },
             { text: "\nBEHIND TWO WINDOWS · SDG 10 Reduced Inequalities · 21CSE255T Computer Graphics and Animation · LLT-1", options: { fontSize: 12.5, color: "9FB0C6" } }],
            { isTextBox: true, x: 0.8, y: 6.0, w: 11.7, h: 1.0, margin: 0, valign: "top" });
}

(async () => {
  const out = path.join(__dirname, "BEHIND_TWO_WINDOWS_presentation.pptx");
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("wrote", out);
})();
