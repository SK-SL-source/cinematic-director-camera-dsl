# -*- coding: utf-8 -*-
"""MiniMax H3 mode wrappers (PROJECT_GOAL.md): the ONE H3 camera core (scripts/adapters.py, model minimax_h3) placed into
the official prompt structures.

  T2VA / I2VA / FL2VA / L2VA  -> Base structure (SRC-008 base-en 2.1-2.2): [alignment line] + integrated_multimodal_description
                                 + overall_soundscape + non_diegetic_music
  Ref2VA                      -> Full-reference structure (SRC-008 ref-en): subject_definitions, summary, retention_analysis,
                                 detailed_description, overall_soundscape, non_diegetic_music

A wrapper never writes or changes camera language. It only decides where the camera text goes, how references are
labelled (<Subject N>, <Picture N>) and how keyframes are aligned. Subjects, scene, action and sound come from the caller.
Every prompt is checked against its content (check_content, CL-059): each subject the camera text names is bound, the cut
times increase and fall inside the video, the required fields are filled. The prompt is still returned so a draft can be
read; the CLI fails unless --draft is given.

CLI:  python h3_wrappers.py <mode> "<dsl>" [content.json] [--layers camera_core,...] [--profile ID] [--lint] [--draft]
      exit 0: no problem found (or --draft) · 1: a problem was found · 2: the prompt could not be built
content.json (every key optional unless the mode needs it):
  subject_name      Base modes: what to call subject A (the subject of a shot whose DSL names none)
  subject_name_b    Base modes: what to call subject B
  subject_map       every DSL subject id and what the prompt calls it: {"A": "the woman", "B": "the man", "C": "the old woman"};
                    Ref2VA: a <Subject N> that subjects defines, {"A": "<Subject 2>", "B": "<Subject 3>"} (default A = <Subject 1>,
                    B = <Subject 2>). A subject the camera text names and nobody is bound to is an error. A shot whose DSL
                    names no subject is about A, or about X in a /REACTION:X shot.
  opening           Base modes: the first sentence(s) of [Shot 1]: style, initial composition, anchors (I2VA: mention <Picture 1>)
  action            what happens after the camera sentences
  soundscape, music overall_soundscape / non_diegetic_music ("N/A" when none)
  duration          seconds of the target video (FL2VA / L2VA: the last frame's time, required); the cut times fall inside it
  frames, fps       the frame count and rate of the generation (fps 24 when not given): the video length when duration is
                    not given; --lint checks the prompt against them
  n_refs            how many reference pictures the workflow attaches (checked by --lint)
  shots             multi-shot: a list of {"opening", "action", "cut"} (one per DSL shot) instead of opening/action; the cut of
                    [Shot 2] onward starts with its time: "At 00:02.500, the camera cuts to ..." (SRC-008 base-en 4.2)
  generation_profile the generation profile id for the routing evidence (or --profile)
  (no content file: the module's neutral sample content for the mode is used, see sample_content: a demo, not production content)
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


def _as_float(x):
    """A JSON number or a numeric string as a float; None for anything else (a bool is not a number here)."""
    if isinstance(x, bool):
        return None
    try:
        return float(x.strip() if isinstance(x, str) else x)
    except (TypeError, ValueError):
        return None


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
    if mode in ("fl2va", "l2va") and _as_float(duration) is None:
        raise ValueError(f"{mode} needs duration, the seconds of the target video (a number, not {duration!r})")
    if mode == "i2va":
        head = I2VA_LINE
    elif mode == "fl2va":
        head = FL2VA_LINE.format(n=n, s=_as_float(duration))
    elif mode == "l2va":
        head = L2VA_LINE.format(n=n, s=_as_float(duration))
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


# ---------------------------------------------------------------- subjects (CL-059)

PLACEHOLDER = re.compile(r"\{([A-Z][A-Z0-9_]*)\}")   # a subject of the camera core: {SUBJECT}, {A}, {B}, {C} ...
LABEL = re.compile(r"<Subject \d+>")


def bindings(mode, content):
    """What the prompt calls each DSL subject id: subject_map first; then Ref2VA A = <Subject 1>, B = <Subject 2>, Base modes
    A = subject_name, B = subject_name_b. An id that is not here is unbound, and check_content reports it."""
    sm = content.get("subject_map")
    b = {str(k).upper(): v for k, v in sm.items() if isinstance(v, str) and v.strip()} if isinstance(sm, dict) else {}
    if mode == "ref2va":
        b.setdefault("A", "<Subject 1>")
        b.setdefault("B", "<Subject 2>")
    else:
        for sid, key in (("A", "subject_name"), ("B", "subject_name_b")):
            if content.get(key):
                b.setdefault(sid, content[key])
    return b


def main_subject(state):
    """Who {SUBJECT} is in one shot: X in a /REACTION:X shot whose DSL names no other subject (the shot frames the one who
    reacts), otherwise A."""
    sh = state["shot"]
    if sh.get("function") == "REACTION" and sh.get("function_target") and sh.get("primary_subject") in (None, "S"):
        return sh["function_target"]
    return "A"


def _fill(text, binding, main="A"):
    """Subject placeholders -> what the prompt calls them ({SUBJECT} is the shot's main subject). An unbound placeholder stays
    as it is for check_content to report. A name that opens a sentence starts with a capital letter
    ("The young woman stays about the same size ...")."""
    def name(sid):
        return binding.get(main if sid == "SUBJECT" else sid)

    def cap(m):
        v = name(m.group(2))
        return m.group(0) if v is None else m.group(1) + v[:1].upper() + v[1:]
    text = re.sub(r"(^|[.!?]\s+)\{([A-Z][A-Z0-9_]*)\}", cap, text)
    return PLACEHOLDER.sub(lambda m: name(m.group(1)) or m.group(0), text)


def wrap_dsl(mode, dsl_text, content, layers=None, profile=None):
    """DSL -> H3 camera core -> official prompt for the mode. Returns {"prompt", "cameras", "warnings", "errors", "render"};
    errors are what check_content found wrong (the prompt is still built, so an unfinished draft can be read).
    profile (or content["generation_profile"]) is the generation profile id the routing evidence is read for; without
    it the routing is UNVERIFIED for this mode."""
    mode = mode.lower()
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}")
    res = dsl.analyze(dsl_text.replace("\\n", "\n"))
    out = adapters.render(res, model="minimax_h3", h3_mode=mode, h3_profile_id=profile or content.get("generation_profile"))
    if out["errors"]:
        raise ValueError("DSL errors: " + "; ".join(out["errors"]))
    binding = bindings(mode, content)
    states = [sh["state"] for sh in res["shots"]]
    raw = [camera_text(sh, layers) for sh in out["shots"]]
    cameras = [_fill(t, binding, main_subject(st)) for t, st in zip(raw, states)]
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
        prompt = ref2va_prompt(content.get("subjects") or [], content.get("task_tags"), content.get("summary", ""),
                               content.get("retention") or [], content.get("style", ""), shots, cameras, sound, music)
    else:
        if mode == "i2va" and "<Picture 1>" not in (shots[0].get("opening") or ""):
            W.append("I2VA: the opening of [Shot 1] should anchor on <Picture 1> (style, subject, composition, scene; SRC-008 base-en 3.1).")
        prompt = base_prompt(mode, shots, cameras, sound, music, content.get("duration"))
    E, cw = check_content(mode, content, shots, raw, states, binding, prompt)
    return {"prompt": prompt, "cameras": cameras, "warnings": W + cw, "errors": E, "render": out}


# ---------------------------------------------------------------- the content contract (CL-059)

CUT_TIME = re.compile(r"At (\d\d):(\d\d\.\d{3})\b")   # the official cut time of [Shot 2] onward, "At 00:02.500" (SRC-008 base-en 4.2)
# content words that ask for the opposite of what a camera sentence fixes about the subject (warned, never rewritten);
# "run" is left out: the floor lines of a set "run toward the far end" (the free-camera baseline content)
_WALKS = re.compile(r"\b(?:walk(?:s|ing)?|strid(?:es|ing)|stroll(?:s|ing)|pac(?:es|ing)|wander(?:s|ing)|approach(?:es|ing)"
                    r"|steps? (?:forward|back|backward|away|aside|toward|towards)|mov(?:es|ing) (?:toward|towards|away|across|forward|back))\b", re.I)
_TURNS = re.compile(r"\b(?:turn(?:s|ing)? (?:around|round|away|back|left|right)|spin(?:s|ning)?|pivot(?:s|ing)?|whirl(?:s|ing)?)\b", re.I)
_STILL = re.compile(r"\b(?:stand(?:s|ing)? still|stay(?:s|ing)? (?:still|in place|put)|remain(?:s|ing)? (?:still|standing|in place)"
                    r"|does not move|doesn't move|sit(?:s|ting)? still|motionless)\b", re.I)
_LOOKS = re.compile(r"\b(?:look(?:s|ing)? (?:away|down|up|around|back|aside)|glanc(?:es|ing)|turn(?:s|ing)? (?:her|his|their) head"
                    r"|clos(?:es|ing) (?:her|his|their) eyes)\b", re.I)


def _positive(x):
    v = _as_float(x)
    return v is not None and v > 0


def video_length(content):
    """Seconds of the target video: duration, else frames / fps (fps 24 when not given); None when neither is given."""
    if _positive(content.get("duration")):
        return _as_float(content["duration"])
    fps = content.get("fps") or 24
    if _positive(content.get("frames")) and _positive(fps):
        return _as_float(content["frames"]) / _as_float(fps)
    return None


def _camera_demands(st):
    """What the camera text of one shot fixes about the subject: (command, what it fixes, content patterns that contradict it)."""
    out = []
    for c in dict.fromkeys(mv["canonical"] for mv in st["movement"]):
        if c == "ORBIT":
            out.append((c, "keeps the subject in place, not turning", (_WALKS, _TURNS)))
        elif c == "DOLLYZOOM":
            out.append((c, "keeps the subject the same size and in the same place", (_WALKS,)))
        elif c in ("TRACK", "FOLLOW", "LEAD", "TRACKSIDE"):
            out.append((c, "moves with a subject who keeps moving", (_STILL,)))
    if st["continuity"].get("screen_direction"):
        out.append(("SCREEN", "has the subject move across the frame", (_STILL,)))
    if any(r.partition(">")[2] not in ("", "CAM", "OFFUP", "OFFDOWN") for r in st["continuity"].get("eyeline", [])):
        out.append(("EYELINE", "keeps the subject's eyes on one spot for the whole video", (_LOOKS,)))
    return out


def check_content(mode, content, shots, raw, states, binding, prompt):
    """The content contract of one wrapped prompt. Errors: a subject the camera text names and nobody is bound to, a Ref2VA
    <Subject N> that subject_definitions does not define, a missing, non-increasing or late cut time, an invalid duration, an
    empty required field. Warnings: the content asks for the opposite of what the camera text fixes. Returns (errors, warnings)."""
    E, W = [], []
    if content.get("subject_map") is not None and not isinstance(content["subject_map"], dict):
        E.append('subject_map must be a JSON object, e.g. {"A": "...", "B": "..."}.')
    unbound = set()
    for n, (t, st) in enumerate(zip(raw, states), 1):
        main = main_subject(st)
        for sid in dict.fromkeys(PLACEHOLDER.findall(t)):
            rid = main if sid == "SUBJECT" else sid
            who = f"the shot's subject ({rid})" if sid == "SUBJECT" else f"subject {rid}"
            v = binding.get(rid)
            if rid == "UNSPECIFIED":
                unbound.add(sid)
                E.append(f"[Shot {n}] the DSL does not say where the eyes go: write /EYELINE:<who>><target>.")
            elif v is None:
                unbound.add(sid)
                E.append(f"[Shot {n}] the camera text names {who}, but the content does not say who {rid} is: "
                         + ("bind it to a defined <Subject N> in subject_map." if mode == "ref2va" else
                            "give it in subject_map" + {"A": " or subject_name", "B": " or subject_name_b"}.get(rid, "") + "."))
            elif mode == "ref2va" and not LABEL.fullmatch(v):
                E.append(f"[Shot {n}] Ref2VA calls {who} by its <Subject N> label, not {v!r} (subject_map).")
    if mode == "ref2va":
        for key in ("subjects", "retention"):
            if content.get(key) is not None and not isinstance(content[key], list):
                E.append(f"Ref2VA: {key} must be a list of lines.")
        defined = {m.group(0) for m in (LABEL.match(str(s or "").strip()) for s in (content.get("subjects") or [])) if m}
        for lab in dict.fromkeys(LABEL.findall(prompt)):
            if lab not in defined:
                E.append(f"the prompt uses {lab}, but no line of subject_definitions defines it.")
    elif LABEL.search(prompt):
        E.append("Base modes call people by name; <Subject N> is the Ref2VA label.")
    left = [x for x in dict.fromkeys(PLACEHOLDER.findall(prompt)) if x not in unbound]
    if left:
        E.append("the content still holds " + ", ".join("{%s}" % x for x in left) + ": write what it stands for.")
    # time line: [Shot 2] onward start with an increasing cut time inside the video (SRC-008 base-en 4.2)
    for key, what in (("duration", "a positive number of seconds"), ("frames", "a positive number"), ("fps", "a positive number")):
        if content.get(key) is not None and not _positive(content[key]):
            E.append(f"{key} must be {what}, not {content[key]!r}.")
    length, prev = video_length(content), 0.0
    for n, sh in enumerate(shots, 1):
        m = CUT_TIME.match((sh.get("cut") or "").strip())
        if n == 1:
            if m:
                E.append("[Shot 1] takes no cut time; the first cut time belongs to [Shot 2] (SRC-008 base-en 4.2).")
            continue
        if not m:
            E.append(f'[Shot {n}] has no cut time: its cut starts with the time, e.g. "At 00:02.500, the camera cuts to ..." (SRC-008 base-en 4.2).')
            continue
        t = int(m.group(1)) * 60 + float(m.group(2))
        if t <= prev:
            E.append(f"[Shot {n}] cuts at {t:.3f} s, not after " + ("the cut before it" if n > 2 else "the start of the video")
                     + f" ({prev:.3f} s): cut times increase.")
        elif length is not None and t >= length:
            E.append(f"[Shot {n}] cuts at {t:.3f} s, but the video is {length:.2f} s long.")
        prev = max(prev, t)
    if len(shots) > 1 and length is None:
        W.append("the cut times were not checked against the video length: give duration (or frames).")
    # required fields (SRC-008 base-en 2.2, ref-en)
    if not str(content.get("soundscape") or "").strip():
        E.append('overall_soundscape is empty: give soundscape ("N/A" only for a video with no sound at all).')
    if mode == "ref2va":
        for key, field in (("subjects", "subject_definitions"), ("summary", "summary"), ("retention", "retention_analysis")):
            v = content.get(key)
            if not any(str(x or "").strip() for x in ([v] if isinstance(v, str) else (v or []))):
                E.append(f"Ref2VA: {field} is empty: give {key} (official field, SRC-008 ref-en).")
    # the camera text and the content must not ask for opposite things (warned; the wrapper rewrites neither)
    for n, (sh, st) in enumerate(zip(shots, states), 1):
        said = " ".join(str(sh.get(k) or "") for k in ("opening", "action"))
        for c, what, patterns in _camera_demands(st):
            m = next((x for x in (p.search(said) for p in patterns) if x), None)
            if m:
                W.append(f'[Shot {n}] /{c} {what}, but the content says "{m.group(0)}": the two ask for opposite things. '
                         "Change the action or the camera move; the wrapper changes neither.")
    return E, W


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


def _lint(mode, prompt, content):
    """The lab lint (LOCAL-002) when CAMERA_DSL_H3_LAB points at it, fed with the content's n_refs and frames (frames from
    duration x fps when only the duration is given). Prints its result; returns the number of lint errors."""
    lab = os.environ.get("CAMERA_DSL_H3_LAB")
    if not lab:
        print("LINT: SKIPPED (CAMERA_DSL_H3_LAB is not set: the lab lint is not on this machine)")
        return 0
    try:
        sys.path.insert(0, lab)
        from h3_prompt_lint import lint
    except ImportError as e:
        print(f"LINT: SKIPPED (the lab lint could not be loaded: {e})")
        return 0
    frames = int(round(_as_float(content["frames"]))) if _positive(content.get("frames")) else None
    if frames is None and _positive(content.get("duration")) and _positive(content.get("fps") or 24):
        frames = int(round(_as_float(content["duration"]) * _as_float(content.get("fps") or 24)))
    n_refs = _as_float(content.get("n_refs"))
    try:
        E, Wl = lint(prompt, None if n_refs is None else int(n_refs), (), frames, mode=mode)
    except Exception as e:   # a lint that cannot run has not passed
        print(f"LINT: FAIL (the lab lint stopped: {type(e).__name__}: {e})")
        return 1
    for e in E:
        print("LINT ERROR:", e)
    for w in Wl:
        print("LINT WARNING:", w)
    print("LINT:", "FAIL" if E else "PASS")
    return len(E)


def _cli(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    import argparse
    ap = argparse.ArgumentParser(description="MiniMax H3 mode wrappers over the shared camera core. Exit 0: no problem found "
                                             "(or --draft); 1: a problem was found; 2: the prompt could not be built.")
    ap.add_argument("mode", choices=MODES)
    ap.add_argument("dsl")
    ap.add_argument("content", nargs="?", help="JSON file with subject / scene / action / sound (see the module docstring)")
    ap.add_argument("--layers", help="comma-separated movement layers to keep (default: all)")
    ap.add_argument("--profile", "--h3-profile", dest="profile",
                    help="generation profile id (models/minimax_h3_profile.yaml) for the routing evidence; without it everything is UNVERIFIED")
    ap.add_argument("--lint", action="store_true", help="also run the lab lint when CAMERA_DSL_H3_LAB is set (otherwise LINT: SKIPPED)")
    ap.add_argument("--draft", action="store_true", help="report the problems without failing (exit 0): for reading an unfinished prompt")
    a = ap.parse_args(argv)
    if a.content:
        try:
            content = json.load(io.open(a.content, encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"ERROR: cannot read the content file {a.content} ({type(e).__name__}: {e})")
            return 2
        if not isinstance(content, dict):
            print("ERROR: the content file must hold one JSON object")
            return 2
    else:
        content = sample_content(a.mode)
    layers = a.layers.split(",") if a.layers else None
    try:
        r = wrap_dsl(a.mode, a.dsl, content, layers, a.profile)
    except ValueError as e:
        print(f"ERROR: {e}")
        return 2
    except (TypeError, AttributeError) as e:   # a content value of the wrong type: a number or a list where text belongs
        print(f"ERROR: a content value has the wrong type ({e})")
        return 2
    print(r["prompt"])
    if not a.content:
        print("NOTE: no content file: the neutral sample content was used (a demo, not production content).")
    for w in r["warnings"]:
        print("WARNING:", w)
    if r["render"].get("routing"):
        print(adapters.routing_text(r["render"]["routing"], "en"))
    problems = structure_check(a.mode, r["prompt"])
    for p in problems:
        print("STRUCTURE:", p)
    for e in r["errors"]:
        print("ERROR:", e)
    n = len(problems) + len(r["errors"]) + (_lint(a.mode, r["prompt"], content) if a.lint else 0)
    if not n:
        print("CHECK: PASS")
        return 0
    print(f"CHECK: {'DRAFT' if a.draft else 'FAIL'} ({n} problem(s){', not blocking: --draft' if a.draft else ''})")
    return 0 if a.draft else 1


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
