# -*- coding: utf-8 -*-
"""MiniMax H3 mode wrappers (PROJECT_GOAL.md): the ONE H3 camera core (scripts/adapters.py, model minimax_h3) placed into
the official prompt structures.

  T2VA / I2VA / FL2VA / L2VA  -> Base structure (SRC-008 base-en 2.1-2.2): [alignment line] + integrated_multimodal_description
                                 + overall_soundscape + non_diegetic_music
  Ref2VA                      -> Full-reference structure (SRC-008 ref-en): subject_definitions, summary, retention_analysis,
                                 detailed_description, overall_soundscape, non_diegetic_music

A wrapper never writes or changes camera language. It only decides where the camera text goes, how references are
labelled (<Subject N>, <Picture N>) and how keyframes are aligned. Subjects, scene, action and sound come from the caller.

CLI:  python h3_wrappers.py <mode> "<dsl>" content.json [--layers camera_core,temporal_clarifier,...] [--lint]
content.json (every key optional unless the mode needs it):
  subject_name      what to call the subject in Base modes (default: "the young woman shown in <Picture 1>")
  opening           Base modes: the first sentence(s) of [Shot 1]: style, initial composition, anchors (I2VA: mention <Picture 1>)
  action            what happens after the camera sentences
  soundscape, music overall_soundscape / non_diegetic_music ("N/A" when none)
  duration          FL2VA / L2VA: effective video length in seconds (the last frame's time)
  shots             multi-shot: a list of {"opening", "action", "cut"} (one per DSL shot) instead of opening/action
  generation_profile the generation profile id for the routing evidence (or --profile)
  (no content file: the module's neutral sample content for the mode is used, see sample_content)
  subjects          Ref2VA: lines of subject_definitions, e.g. "<Subject 1> is the young woman whose facial identity comes from <Picture 1> ..."
  task_tags         Ref2VA summary prefix, default ["reference generation"]
  summary           Ref2VA summary text (after the tag)
  retention         Ref2VA retention_analysis lines
  style             Ref2VA: the style line that opens detailed_description
"""
import io
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adapters  # noqa: E402
import camera_dsl as dsl  # noqa: E402

MODES = ("t2va", "i2va", "fl2va", "l2va", "ref2va")
BASE_MODES = ("t2va", "i2va", "fl2va", "l2va")
# alignment lines, verbatim from the official base guide (SRC-008 base-en 2.1)
I2VA_LINE = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced."
FL2VA_LINE = ("How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark "
              "of the target video; Picture 2 (from Shot {n}) aligns with the {s:.2f}-second mark of the target video.")
L2VA_LINE = ("How the reference pictures align with the target video — <Picture 1> (from [Shot {n}]) aligns with the {s:.2f}-second "
             "mark of the target video.")
REF2VA_FIELDS = ("subject_definitions", "summary", "retention_analysis", "detailed_description", "overall_soundscape", "non_diegetic_music")

SAMPLE_CONTENT = {   # neutral fixture content used by tests/h3_wrappers.md
    "subject_name": "the young woman shown in <Picture 1>",
    "opening": "2D hand-painted animation, the young woman shown in <Picture 1> stands in a stone courtyard, preserving her face, hair, and clothes.",
    "action": "She stands still, facing the camera, with both hands empty at her sides.",
    "soundscape": "Quiet outdoor daytime ambience of a stone courtyard, with a light breeze and distant birds.",
    "music": "N/A",
    "duration": 5.17,
    "subjects": ["<Subject 1> is the young woman whose facial identity comes from <Picture 1> and whose hair, figure, and clothes come from <Picture 2>."],
    "task_tags": ["reference generation"],
    "summary": "One continuous shot of <Subject 1> standing still in a stone courtyard.",
    "retention": ["<Subject 1> (appears in [Shot 1]): fully_preserved - her facial identity, hair, and clothes from the reference images are retained."],
    "style": "The target video is a 2D hand-painted animation, in the same painted illustration style as the reference images.",
}
_SAMPLE_BY_MODE = {   # the same fixture, with the opening written the way each mode labels its subject
    "t2va": {"subject_name": "the young woman",
             "opening": "2D hand-painted animation, a young woman in a tan robe with a black apron stands in a stone courtyard."},
    "ref2va": {"opening": "<Subject 1> stands in a stone courtyard."},
}


def sample_content(mode):
    """The neutral fixture content for one mode (tests/h3_wrappers.md and the CLI default)."""
    c = dict(SAMPLE_CONTENT)
    c.update(_SAMPLE_BY_MODE.get(mode.lower(), {}))
    return c


def camera_text(shot_out, layers=None):
    """The camera text of one rendered shot, rebuilt from its H3 structure with only the chosen movement layers.
    layers=None keeps every layer (identical to the adapter's joined text)."""
    h3 = shot_out.get("h3")
    if not h3 or layers is None:
        return shot_out["text"]
    keep = set(layers)
    parts = []
    for grp in ("framing", "lens", "viewpoint", "focus", "composition", "rig"):
        parts += h3.get(grp) or []
    for mv in h3["movements"]:
        for k in adapters.H3_LAYERS:
            if k in keep and mv.get(k):
                parts.append(mv[k]["text"])
    parts += h3.get("continuity") or []
    return " ".join(p for p in parts if p)


def _shot_block(idx, shot, camera):
    cut = (shot.get("cut") or "").strip()
    opening = (shot.get("opening") or "").strip()
    action = (shot.get("action") or "").strip()
    body = " ".join(x for x in (cut, opening, camera, action) if x)
    return f"[Shot {idx}] {body}"


def base_prompt(mode, shots, cameras, soundscape, music, duration=None):
    """Official Base structure. shots: list of {"opening", "action", "cut"}; cameras: camera text per shot."""
    if mode not in BASE_MODES:
        raise ValueError(f"base_prompt: mode must be one of {BASE_MODES}")
    n = len(shots)
    head = ""
    if mode == "i2va":
        head = I2VA_LINE
    elif mode == "fl2va":
        if duration is None:
            raise ValueError("fl2va needs duration (seconds of the target video)")
        head = FL2VA_LINE.format(n=n, s=float(duration))
    elif mode == "l2va":
        if duration is None:
            raise ValueError("l2va needs duration (seconds of the target video)")
        head = L2VA_LINE.format(n=n, s=float(duration))
    desc = " ".join(_shot_block(i + 1, sh, cameras[i]) for i, sh in enumerate(shots))
    body = (f"integrated_multimodal_description: {desc}\n\n"
            f"overall_soundscape: {soundscape.strip()}\n\n"
            f"non_diegetic_music: {(music or 'N/A').strip()}\n")
    return (head + "\n\n" + body) if head else body


def ref2va_prompt(subjects, task_tags, summary, retention, style, shots, cameras, soundscape, music):
    """Official Full-reference structure (six fields in order)."""
    desc = "\n".join(_shot_block(i + 1, sh, cameras[i]) for i, sh in enumerate(shots))
    tags = " + ".join(task_tags or ["reference generation"])
    return ("subject_definitions:\n" + "\n".join(subjects) + "\n\n"
            "summary:\n[" + tags + "] " + summary.strip() + "\n\n"
            "retention_analysis:\n" + "\n".join(retention) + "\n\n"
            "detailed_description:\n" + ((style.strip() + "\n") if style else "") + desc + "\n\n"
            "overall_soundscape:\n" + soundscape.strip() + "\n\n"
            "non_diegetic_music:\n" + (music or "N/A").strip() + "\n")


def _fill(text, mode, content):
    """Subject placeholders: Ref2VA uses the official <Subject N> labels; Base modes use the caller's subject name."""
    if mode == "ref2va":
        rep = {"{SUBJECT}": "<Subject 1>", "{A}": "<Subject 1>", "{B}": "<Subject 2>"}
    else:
        name = content.get("subject_name") or SAMPLE_CONTENT["subject_name"]
        rep = {"{SUBJECT}": name, "{A}": name, "{B}": content.get("subject_name_b", "the second person")}
    # a subject name that opens a sentence starts with a capital letter ("The young woman stays about the same size ...")
    text = re.sub(r"(^|[.!?]\s+)(\{SUBJECT\}|\{A\}|\{B\})", lambda m: m.group(1) + rep[m.group(2)][:1].upper() + rep[m.group(2)][1:], text)
    for k, v in rep.items():
        text = text.replace(k, v)
    return text


def wrap_dsl(mode, dsl_text, content, layers=None, profile=None):
    """DSL -> H3 camera core -> official prompt for the mode. Returns {"prompt", "cameras", "warnings", "render"}.
    profile (or content["generation_profile"]) is the generation profile id the routing evidence is read for; without
    it the routing is UNVERIFIED for this mode."""
    mode = mode.lower()
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}")
    res = dsl.analyze(dsl_text.replace("\\n", "\n"))
    out = adapters.render(res, model="minimax_h3", h3_mode=mode, h3_profile_id=profile or content.get("generation_profile"))
    if out["errors"]:
        raise ValueError("DSL errors: " + "; ".join(out["errors"]))
    cameras = [_fill(camera_text(sh, layers), mode, content) for sh in out["shots"]]
    W = list(out["warnings"])
    shots = content.get("shots")
    if not shots:
        shots = [{"opening": content.get("opening", ""), "action": content.get("action", ""), "cut": ""}]
        if len(cameras) > 1:   # single-shot content over a multi-shot DSL: the later shots carry only their camera text
            shots += [{"opening": "", "action": "", "cut": ""} for _ in cameras[1:]]
            W.append(f"content describes one shot; shots 2-{len(cameras)} carry only the camera text (give \"shots\" for each).")
    if len(shots) != len(cameras):
        raise ValueError(f"content gives {len(shots)} shot(s) but the DSL has {len(cameras)}")
    sound, music = content.get("soundscape", ""), content.get("music", "N/A")
    if mode == "ref2va":
        subjects = content.get("subjects") or []
        retention = content.get("retention") or []
        if not subjects or not retention:
            W.append("Ref2VA: subject_definitions and retention_analysis lines are required by the official format (SRC-008 ref-en).")
        prompt = ref2va_prompt(subjects, content.get("task_tags"), content.get("summary", ""), retention, content.get("style", ""), shots, cameras, sound, music)
    else:
        if mode == "i2va" and "<Picture 1>" not in (shots[0].get("opening") or ""):
            W.append("I2VA: the opening of [Shot 1] should anchor on <Picture 1> (style, subject, composition, scene; SRC-008 base-en 3.1).")
        prompt = base_prompt(mode, shots, cameras, sound, music, content.get("duration"))
    return {"prompt": prompt, "cameras": cameras, "warnings": W, "render": out}


def structure_check(mode, prompt):
    """Cheap structural checks of a wrapped prompt (the lab lint is the full gate when it is available)."""
    problems = []
    lines = prompt.split("\n")
    if mode in BASE_MODES:
        if any(f.startswith(("subject_definitions", "retention_analysis", "detailed_description")) for f in lines):
            problems.append("Base mode must not carry Full-reference fields")
        if mode == "t2va" and not lines[0].startswith("integrated_multimodal_description:"):
            problems.append("T2VA must begin with integrated_multimodal_description")
        if mode == "t2va" and "<Picture" in prompt:
            problems.append("T2VA has no reference pictures")
        if mode == "i2va" and lines[0] != I2VA_LINE:
            problems.append("I2VA must begin with the official alignment line")
        if mode in ("fl2va", "l2va") and not lines[0].startswith("How the reference pictures align with the target video"):
            problems.append(f"{mode.upper()} must begin with the official alignment line")
        for f in ("integrated_multimodal_description:", "overall_soundscape:", "non_diegetic_music:"):
            if f not in prompt:
                problems.append(f"missing {f}")
    else:
        pos = [prompt.find(f + ":") for f in REF2VA_FIELDS]
        if any(p < 0 for p in pos) or pos != sorted(pos):
            problems.append("Ref2VA must carry the six fields in the official order")
        if I2VA_LINE in prompt or "How the reference pictures align" in prompt:
            problems.append("Ref2VA must not carry a Base alignment line")
    return problems


def _cli(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    import argparse
    ap = argparse.ArgumentParser(description="MiniMax H3 mode wrappers over the shared camera core")
    ap.add_argument("mode", choices=MODES)
    ap.add_argument("dsl")
    ap.add_argument("content", nargs="?", help="JSON file with subject / scene / action / sound (see the module docstring)")
    ap.add_argument("--layers", help="comma-separated movement layers to keep (default: all)")
    ap.add_argument("--profile", "--h3-profile", dest="profile",
                    help="generation profile id (models/minimax_h3_profile.yaml) for the routing evidence; without it everything is UNVERIFIED")
    ap.add_argument("--lint", action="store_true", help="run the lab lint when CAMERA_DSL_H3_LAB is set")
    a = ap.parse_args(argv)
    content = json.load(io.open(a.content, encoding="utf-8")) if a.content else sample_content(a.mode)
    layers = a.layers.split(",") if a.layers else None
    r = wrap_dsl(a.mode, a.dsl, content, layers, a.profile)
    print(r["prompt"])
    for w in r["warnings"]:
        print("WARNING:", w)
    if r["render"].get("routing"):
        print(adapters.routing_text(r["render"]["routing"], "en"))
    for p in structure_check(a.mode, r["prompt"]):
        print("STRUCTURE:", p)
    lab = os.environ.get("CAMERA_DSL_H3_LAB")
    if a.lint and lab:
        sys.path.insert(0, lab)
        from h3_prompt_lint import lint
        n_refs = {"t2va": 0, "i2va": 1, "fl2va": 2, "l2va": 1, "ref2va": 2}[a.mode]
        E, Wl = lint(r["prompt"], n_refs, (), 124)
        for e in E:
            print("LINT ERROR:", e)
        for w in Wl:
            print("LINT WARNING:", w)
        print("LINT:", "FAIL" if E else "PASS")
    return 0


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
