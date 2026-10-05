# -*- coding: utf-8 -*-
"""Model adapters: camera state -> model-specific camera text. Same intent, different wording.

Each adapter writes CAMERA TEXT ONLY. Subjects stay as placeholders ({SUBJECT}, {A}, {B}); no people,
clothes, props, dialogue or actions are invented (spec section 28). Unspecified parameters are left
out of the text and listed in 'unspecified' (STRICT mode, research 07 D16).
Evidence for every model rule: models/<model>.md.
"""
import os
import re

import camera_dsl as dsl
import yaml_lite

MODELS = {
    "generic_video": {"kind": "video", "lang": "en", "langs": ["en"]},
    "minimax_h3": {"kind": "video", "lang": "en", "langs": ["en"]},
    "kling": {"kind": "video", "lang": "zh", "langs": ["zh", "en"]},
    "veo": {"kind": "video", "lang": "en", "langs": ["en"]},
    "generic_image": {"kind": "image", "lang": "en", "langs": ["en"]},
    "flux": {"kind": "image", "lang": "en", "langs": ["en"]},
    "qwen_image": {"kind": "image", "lang": "en", "langs": ["en", "zh"]},
    "qwen_image_edit": {"kind": "image_edit", "lang": "en", "langs": ["en", "zh"]},
}

S = "{SUBJECT}"
TEMPORAL_VERBS = re.compile(
    r"\b(pans|pushes|pulls|moves|travels|tracks|orbits|circles|rises|descends|zooms|tilts|trucks|slides|"
    r"rolls|sweeps|follows|flies|whips|arcs|pedestals|booms|cranes|racks|shifts)\b", re.I)

# ---------------------------------------------------------------- english phrase tables

SIZE_EN = {
    "EWS": "an extreme wide shot; {S} is small in a vast space",
    "WS": "a wide shot; {S} is seen full-body with plenty of surroundings",
    "FS": "a full shot framing {S} from head to toe",
    "MFS": "a medium full shot framing {S} from the knees up",
    "COWBOY": "a cowboy shot framing {S} from mid-thigh up",
    "MS": "a medium shot framing {S} from the waist up",
    "MCU": "a medium close-up framing {S} from the chest up",
    "CU": "a close-up of {S}'s face, head and shoulders",
    "ECU": "an extreme close-up on one detail of {S}",
}
SIZE_SHORT_EN = {"EWS": "extreme wide shot", "WS": "wide shot", "FS": "full shot", "MFS": "medium full shot",
                 "COWBOY": "cowboy shot", "MS": "medium shot", "MCU": "medium close-up", "CU": "close-up",
                 "ECU": "extreme close-up"}
SIZE_BODY_EN = {"EWS": "small in a vast space", "WS": "full-body with plenty of surroundings",
                "FS": "from head to toe", "MFS": "from the knees up", "COWBOY": "from mid-thigh up",
                "MS": "from the waist up", "MCU": "from the chest up", "CU": "head and shoulders",
                "ECU": "on one detail"}
KEEP_IN_FRAME_EN = {"EWS": "whole body", "WS": "whole body", "FS": "whole body, feet included,", "MFS": "body from the knees up",
                    "COWBOY": "body from mid-thigh up", "MS": "whole upper body", "MCU": "head and chest",
                    "CU": "face", "ECU": "detail"}
HEIGHT_EN = {
    "GROUND": "The camera is at ground level, just above the floor.",
    "ANKLE": "The camera is at ankle height.",
    "KNEE": "The camera is at knee height.",
    "HIP": "The camera is at waist height.",
    "CHEST": "The camera is at chest height.",
    "SHOULDER": "The camera is at shoulder height.",
    "EYE": None,  # expressed by EYELEVEL
    "ELEVATED": "The camera is elevated, above head height.",
    "AERIAL": "The camera is high above the scene, seen from the air.",
}
SPEED_EN = {"IMPERCEPTIBLE": "almost imperceptibly", "VSLOW": "very slowly", "SLOW": "slowly",
            "STEADY": "at a steady pace", "BRISK": "briskly", "FAST": "fast"}
DIR_EN = {"L": "left", "R": "right", "UP": "up", "DOWN": "down", "CW": "clockwise", "CCW": "counterclockwise",
          "IN": "in", "OUT": "out", "BACK": "back"}


def _subj(name):
    return "{" + name + "}" if name and name != "S" else S


def _amount_en(mv, kind="generic"):
    a = mv.get("amount")
    if not a:
        return ""
    v, u = a["value"], a["unit"]
    if u == "deg":
        return f"about {int(v)} degrees"
    if u == "%":
        return f"about {int(v)}% of the way" if kind == "dolly" else f"about {int(v)}%"
    if u == "m":
        return f"about {v:g} m" if v >= 1 else f"about {int(round(v * 100))} cm"
    return {"SMALL": "a short distance", "LARGE": "a long way", "PARTIAL": "in a partial arc",
            "FULL": "a full circle", "MEDIUM": ""}.get(v, "")


def _speed_en(mv):
    return SPEED_EN.get(mv.get("speed") or "", "")


def _join(*parts):
    return " ".join(p.strip() for p in parts if p and p.strip())


def _cap(s):
    return s[:1].upper() + s[1:] if s else s


def _a(size):
    """'a medium shot' / 'an extreme wide shot'."""
    w = SIZE_SHORT_EN[size]
    return ("an " if w[0] in "aeiou" else "a ") + w


# Physical channels each movement uses. A guard sentence ("stays in one spot", "does not turn", "stays at the
# same height", "focal length stays the same") is written only when no simultaneous move breaks it.
MOVE_CHANNELS = {
    "PAN": {"yaw"}, "WHIPPAN": {"yaw"}, "TILT": {"pitch"}, "ROLL": {"roll"},
    "DOLLYIN": {"travel"}, "DOLLYOUT": {"travel"}, "TRUCK": {"travel"}, "PEDESTAL": {"travel", "height"},
    "TRACK": {"travel"}, "FOLLOW": {"travel"}, "LEAD": {"travel"}, "TRACKSIDE": {"travel"},
    "ORBIT": {"travel", "yaw"}, "CRANE": {"travel", "height", "pitch"}, "FLYTHROUGH": {"travel"},
    "DOLLYZOOM": {"travel", "zoom"}, "FLYOVER": {"travel"}, "DRONEREVEAL": {"travel", "height"},
    "ZOOMIN": {"zoom"}, "ZOOMOUT": {"zoom"}, "CRASHZOOM": {"zoom"}, "STATIC": set(),
}


def _step_prefixes(st, lang="en"):
    """Prefix per movement: its time window or its place in a THEN sequence; later moves of the same step
    are simultaneous with the first one (spec section 20)."""
    steps = sorted({m["step"] for m in st["movement"] if m.get("sequential")})
    seen, out = set(), []
    for m in st["movement"]:
        key = (m.get("step"), tuple(m["time"]) if m.get("time") else None)
        if not m.get("sequential"):
            p = ""
        elif key in seen:
            p = "At the same time, " if lang == "en" else "同时，"
        elif m.get("time"):
            t0, t1 = m["time"]
            p = f"From {t0:g}s to {t1:g}s: " if lang == "en" else f"第{t0:g}至{t1:g}秒，"
        else:
            first = m["step"] == steps[0]
            p = ("First, " if first else "Then, ") if lang == "en" else ("首先，" if first else "然后，")
        seen.add(key)
        out.append(p)
    return out


def _others(mv, st):
    """Channels used by the other moves that run at the same time as mv."""
    ch = set()
    for o in st["movement"]:
        if o is not mv and o.get("time") == mv.get("time"):
            ch |= MOVE_CHANNELS.get(o["canonical"], set())
    return ch


def _later_step(mv, st):
    """True when mv starts after the shot's first step (its start is where the previous step ended)."""
    steps = sorted({m["step"] for m in st["movement"] if m.get("sequential")})
    return bool(mv.get("sequential") and steps and mv["step"] != steps[0])


def _last_step(mv, st):
    steps = sorted({m["step"] for m in st["movement"] if m.get("sequential")})
    return bool(mv.get("sequential") and steps and mv["step"] == steps[-1])


def _guards(mv, st):
    o = _others(mv, st)
    return {"still": "travel" not in o, "level": "height" not in o, "noturn": not ({"yaw", "pitch"} & o),
            "nozoom": "zoom" not in o, "nomove": not ({"travel", "yaw", "pitch", "roll"} & o)}


# ---------------------------------------------------------------- shared state phrases (EN)


def framing_en(st, style, skip_size=False):
    out = []
    sh = st["shot"]
    subj = _subj(sh.get("primary_subject"))
    size = sh["size"]
    if size and not skip_size:
        if style == "h3":
            out.append(f"{_cap(_a(size))} frames {subj} {SIZE_BODY_EN[size]}.")
        else:
            out.append(_cap(SIZE_EN[size].replace("{S}", subj)) + ".")
    fr = sh["framing"]
    fg = sh.get("foreground_subject")
    if sh["viewpoint"] == "OTS":
        a, b = _subj(fg or "A"), _subj(sh.get("primary_subject") or "B")
        if sh.get("ots_variant") == "CLEAN":
            out.append(f"The camera is at {a}'s shoulder looking at {b}, but {a} stays out of the frame.")
        else:
            out.append(f"Over-the-shoulder: the camera is behind {a}'s shoulder looking at {b}; {a}'s shoulder is in the near foreground.")
    if sh["viewpoint"] == "POV":
        o = _subj(sh.get("pov_owner") or "VIEWER")
        out.append(f"Point of view: we see through {o}'s eyes; {o} is never visible.")
    cnt = sh.get("subject_count")
    if cnt == "1":
        out.append(f"Only one person, {subj}, is in the frame.")
    elif cnt == "2" and sh["viewpoint"] != "OTS":
        out.append("Two-shot: {A} and {B} are both in the frame.")
    elif cnt == "3":
        out.append("Three-shot: all three subjects are in the frame.")
    elif cnt == "GROUP":
        out.append("Group shot: the whole group is in the frame.")
    ori = sh.get("orientation")
    if ori and st["meta"]["origins"].get("shot.orientation") not in (None, "DEFINITIONAL"):
        out.append({"FRONTAL": f"{subj} faces the camera square-on.",
                    "THREEQUARTER": f"{subj} is turned three-quarters to the camera.",
                    "PROFILE": f"{subj} is seen in profile, from the side.",
                    "REAR": f"{subj} is seen from behind, back to the camera."}[ori])
    fn = sh.get("function")
    if fn == "INSERT":
        t = (sh.get("function_target") or "object").lower()
        out.append(f"Insert: a detail of the {t} fills the frame.")
    elif fn == "CUTAWAY":
        t = (sh.get("function_target") or "surroundings").lower()
        out.append(f"Cutaway: the {t}, away from the main action.")
    elif fn == "REACTION":
        out.append(f"Reaction: {_subj(sh.get('function_target'))}'s reacting face stays readable in the frame.")
    return out


def angle_en(st, style):
    out = []
    cam = st["camera"]
    subj = _subj(st["shot"].get("primary_subject"))
    h, p = cam.get("height"), cam.get("angle")
    pos = cam.get("position")
    inten = cam.get("angle_intensity")
    adj = {"SLIGHT": "slightly ", "MILD": "slightly ", "STEEP": "steep ", "EXTREME": "steep "}.get(inten or "", "")
    if pos == "FAR_ABOVE":
        if style == "h3":  # plain-English rule (H3LAB-PLAIN-01): no similes
            out.append(f"Bird's-eye view: the camera is far above and looks straight down. The ground fills the frame, and {subj} is small in it.")
        else:
            out.append(f"Bird's-eye view: from far above, the camera looks straight down; the ground looks like a map and {subj} looks small.")
        return out
    if pos == "DRONE":
        # H3 draws named gear into the frame (SRC-009 gear.md), so H3 gets the position without the word "drone"
        view = "Aerial view: the camera is high in the air" if style == "h3" else "Drone view: the camera is at drone height in the air"
        if p == "HIGH" and st["meta"]["origins"].get("camera.angle") == "DEFINITIONAL":
            out.append(f"{view}, looking down at {subj} at an angle.")
        else:
            out.append(f"{view}.")
            p_phr = _pitch_en(p, subj, adj)
            if p_phr:
                out.append(p_phr)
        return out
    if h == "EYE" and p == "LEVEL":
        out.append(f"The camera is at {subj}'s eye level, looking straight across.")
    else:
        if h and HEIGHT_EN.get(h):
            out.append(HEIGHT_EN[h])
        pp = _pitch_en(p, subj, adj)
        if pp:
            out.append(pp if out else pp.replace("It looks", "The camera looks").replace("Worm's-eye view: it looks", "Worm's-eye view: the camera looks"))
    return out


def _pitch_en(p, subj, adj=""):
    return {"LOW": f"It looks up at {subj} from a {adj}low angle.",
            "HIGH": f"It looks down on {subj} from a {adj}high angle, an oblique view.",
            "VERTICAL_DOWN": f"It looks straight down at {subj} (top-down).",
            "VERTICAL_UP": f"Worm's-eye view: it looks straight up at {subj}.",
            "LEVEL": "The lens axis is level."}.get(p)


def dutch_en(st, style):
    cam = st["camera"]
    if cam.get("orientation") != "DUTCH":
        return []
    d = cam.get("dutch") or {}
    side = {"L": " to the left", "R": " to the right"}.get(d.get("direction") or "", "")
    deg = f", about {int(d['degrees'])} degrees" if d.get("degrees") else ""
    if style == "h3":
        return [f"The horizon is tilted{side} in a Dutch angle{deg} for the whole video."]
    return [f"Dutch angle: the horizon is tilted{side}{deg}."]


def lens_en(st, style):
    L = st["lens"]
    out = []
    subj = _subj(st["shot"].get("primary_subject"))
    mm = L.get("focal_length")
    cls = L.get("lens_type")
    if mm:
        m = int(mm)
        eff = ("near things look huge and depth is stretched" if m <= 18 else
               "depth feels expanded" if m <= 30 else "natural perspective" if m <= 60 else
               "the background is softly compressed" if m <= 110 else f"the background looks close behind {subj}")
        out.append(f"{m}mm lens: {eff}.")
    elif cls:
        out.append({"ULTRAWIDE": "Ultra-wide lens: near things look huge and depth is stretched.",
                    "WIDE": "Wide-angle lens: depth feels expanded.",
                    "NORMAL": "Normal lens: natural, human-like perspective.",
                    "PORTRAIT": "Portrait lens, about 85mm: the face looks natural and the background is softly compressed.",
                    "TELE": f"Telephoto, a long lens: strong compression; the background looks close behind {subj}."}[cls])
    for t in L.get("types", []):
        if t == "FISHEYE" and cls == "ULTRAWIDE" and not mm:
            out = [x for x in out if not x.startswith("Ultra-wide")]
        out.append({"MACRO": "Macro lens: a tiny detail is magnified and the focus plane is razor thin.",
                    "FISHEYE": "Fisheye lens: straight lines bow outward.",
                    "ANAMORPHIC": "Anamorphic lens: oval out-of-focus highlights and horizontal flares."}[t])
    return out


def focus_en(st, style, image=False):
    F = st["focus"]
    subj = _subj(st["shot"].get("primary_subject"))
    out = []
    if F.get("depth_of_field") == "SHALLOW":
        out.append(f"Shallow focus: {subj} is sharp and the background is soft.")
    elif F.get("depth_of_field") == "DEEP":
        out.append("Deep focus: everything from foreground to background is sharp.")
    tgt = F.get("target")
    if tgt:
        out.append({"FG": "The foreground is sharp; farther planes are soft.",
                    "MG": "The midground is sharp; near and far planes are soft.",
                    "BG": "The background is sharp; the foreground is soft."}[tgt])
    if F.get("special") == "SPLIT_DIOPTER":
        out.append("Split-diopter: a near subject and a far subject are both sharp, with a soft seam between them.")
    tr = F.get("transition")
    if tr:
        fr, to = _plane(tr.get("from")), _plane(tr.get("to"))
        still = not any(not m.get("time") for m in st["movement"])  # a simultaneous move does change the framing
        if image:
            out.append(f"Focus is on {fr}, the start of a rack focus; {to} is soft.")
        else:
            sp = SPEED_EN.get(tr.get("speed") or "", "")
            if style == "h3":
                out.append(f"The focus then racks from {fr} to {to}{', ' + sp if sp else ''}, and {fr} falls soft as {to} turns sharp.")
                if still:
                    out.append("The framing does not change.")
            else:
                out.append(f"The focus shifts from {fr} to {to}" + (f", {sp}" if sp else "") + ("; the framing does not change." if still else "."))
    return out


def _plane(x):
    return {"FG": "the foreground", "MG": "the midground", "BG": "the background", None: "the first subject",
            "": "the first subject"}.get(x, _subj(x))


def composition_en(st, style):
    C = st["composition"]
    subj = _subj(st["shot"].get("primary_subject"))
    out = []
    pl = C.get("placement")
    if pl == "CENTER":
        out.append(f"{subj} is centered in the frame.")
    elif pl and pl.startswith("THIRD"):
        side = {"THIRD_L": "left ", "THIRD_R": "right "}.get(pl, "")
        out.append(f"{subj} sits on the {side}third of the frame.".replace("the third", "a third line"))
    if C.get("symmetry"):
        out.append("The frame is symmetrical.")
    ns = C.get("negative_space")
    if ns:
        side = {"L": "left side", "R": "right side", "UP": "top", "DOWN": "bottom"}.get(ns if isinstance(ns, str) else "", "frame")
        out.append(f"A large empty area fills the {side} of the frame." if side != "frame" else "A large empty area surrounds the subject.")
    hr = C.get("headroom")
    if hr:
        out.append({"TIGHT": f"Very little room above {subj}'s head.", "NORMAL": f"A normal amount of room above {subj}'s head.",
                    "LOOSE": f"Plenty of room above {subj}'s head."}[hr])
    lr = C.get("lookroom")
    if lr:
        side = {"L": "left", "R": "right"}.get(lr if isinstance(lr, str) else "", "")
        out.append(f"Open space on the {side} side, in front of {subj}'s face." if side else f"Open space in front of {subj}'s face.")
    if C.get("leading_lines"):
        out.append(f"Lines in the scene lead the eye to {subj}.")
    if C.get("frame_in_frame"):
        out.append(f"{subj} is framed inside an opening in the scene.")
    fg = C.get("foreground")
    if fg:
        thing = "An element of the scene" if fg == "FOREGROUND_ELEMENT" else f"The {fg.lower()}"
        out.append(f"{thing} sits in the near foreground, between the camera and {subj}.")
    if C.get("depth_layers"):
        out.append("The subjects are at different depths: one near, one farther back.")
    return out


def rig_en(st, style, has_move):
    R = st["rig"]
    out = []
    t, stab, inten = R.get("type"), R.get("stability"), R.get("intensity")
    gimbal_too = "GIMBAL" in (R.get("types") or []) and t in ("DRONE", "FPV")
    if t in ("DRONE", "FPV") and gimbal_too:
        if style == "h3":
            out.append("The camera moves very smoothly and level through the air." if has_move else "The camera hovers very smoothly and level in the air.")
        else:
            out.append("Carried by a drone on a gimbal: very smooth, level airborne movement." if has_move
                       else "Carried by a hovering drone on a gimbal; the frame stays very smooth and level.")
        if R.get("locked") and not has_move:
            out.append("The camera stays locked in one position.")
        return out
    if stab == "LOCKED" and not t:
        if not has_move:
            out.append("The camera holds a Static Shot throughout." if style == "h3"
                       else "The camera stays locked in one position for the whole shot.")
        return out
    if style == "h3" and t and R.get("locked") and not has_move and t == "DRONE":
        return ["The camera hovers steadily in the air.", "The camera holds a Static Shot throughout."]
    if style == "h3" and t:
        # H3: never name a rig the camera could see; describe the effect (SRC-009 gear.md)
        if R.get("locked") and not has_move and t != "DRONE":
            out.append("The camera holds a Static Shot throughout.")
        out.append({"TRIPOD": "The camera stays at one fixed spot.",
                    "HANDHELD": "The camera shakes strongly, handheld." if inten == "STRONG" else "The camera shakes slightly, handheld.",
                    "SHOULDER": "The camera sways slightly, carried on a shoulder.",   # no 'as if' (lab lint FLOURISH)
                    "STEADICAM": "The camera floats smoothly, with no shake.",
                    "GIMBAL": "The camera moves very smoothly and level, with no shake.",
                    "SLIDER": "The camera moves in a short, smooth, straight line.",
                    "DRONE": "The camera moves smoothly through the air." if has_move else "The camera hovers steadily in the air.",
                    "FPV": "The camera flies fast and agile, diving and weaving."}.get(t, ""))
        return out
    if t == "TRIPOD":
        out.append("The camera is on a tripod at one fixed spot." + ("" if has_move else " It does not move."))
    elif t == "HANDHELD":
        if style == "h3":
            out.append("The camera shakes strongly, handheld." if inten == "STRONG" else "The camera shakes slightly, handheld.")
        else:
            out.append("Handheld with strong shake." if inten == "STRONG" else "Handheld: small natural shake and drift the whole time.")
    elif t == "SHOULDER":
        out.append("Shoulder-mounted: a slight rolling sway, as if on an operator's shoulder.")
    elif t == "STEADICAM":
        out.append("Steadicam: smooth, floating movement with no shake.")
    elif t == "GIMBAL":
        out.append("On a gimbal: very smooth, level movement with no shake.")
    elif t == "SLIDER":
        out.append("On a short slider rail: a small, smooth, straight move.")
    elif t == "DRONE":
        out.append("Carried by a drone: smooth airborne movement." if has_move else "Carried by a hovering drone; the frame stays steady.")
    elif t == "FPV":
        out.append("FPV drone: fast, agile flight that can dive, weave and bank.")
    if (R.get("locked") or stab == "LOCKED") and t and t != "TRIPOD" and not has_move:
        out.append("The camera stays locked in one position.")
    return out


def continuity_en(st, style):
    C = st["continuity"]
    out = []
    crossing = C.get("cross_axis") in ("MOVE", "BLOCKING")  # the sides swap during this shot
    if crossing:
        out.append("The camera visibly crosses the line of action during the move." if C["cross_axis"] == "MOVE"
                   else "This shot crosses the line of action by the actors' own movement.")
    if C.get("axis"):
        a, b = C["axis"].split("-")
        out.append(f"By the end of the shot, {{{a}}} is on the left side of the frame and {{{b}}} on the right." if crossing
                   else f"{{{a}}} stays on the left side of the frame and {{{b}}} on the right.")
    for rel in C.get("eyeline", []):
        src, _, tgt = rel.partition(">")
        who = _subj(src)
        if tgt == "CAM":
            out.append(f"{who} looks directly into the lens.")
        elif tgt in ("OFFL", "OFFR"):
            out.append(f"{who}'s eyes are on something off-screen to the {'left' if tgt == 'OFFL' else 'right'}"
                       + (", and they stay there for the whole video." if style == "h3" else "."))
        elif tgt in ("OFFUP", "OFFDOWN"):
            out.append(f"{who} looks {'up' if tgt == 'OFFUP' else 'down'}, off-screen.")
        elif tgt:
            out.append(f"{who}'s eyes are on {_subj(tgt)}" + (", and they stay there for the whole video." if style == "h3" else "."))
    sd = C.get("screen_direction")
    subj = _subj(st["shot"].get("primary_subject"))
    if sd:
        out.append({"L2R": f"{subj} moves from frame-left toward frame-right.",
                    "R2L": f"{subj} moves from frame-right toward frame-left.",
                    "TOWARD": f"{subj} moves toward the camera.",
                    "AWAY": f"{subj} moves away from the camera."}[sd])
    for r in C.get("relation_to_previous_shot", []):
        if r["type"] == "SRS":
            v = r.get("value") or ">"
            a, _, b = v.partition(">")
            out.append(f"Reverse angle of the previous shot: now looking at {_subj(b)} from {_subj(a)}'s side, with the same lens and distance, mirrored.")
        elif r["type"] == "MATCHACTION":
            out.append("The shot opens by continuing the same action the previous shot ended on.")
        elif r["type"] == "MATCHCUT":
            out.append(f"Match cut: the main {(r.get('value') or 'shape').lower()} sits in the same frame position as in the previous shot.")
    if C.get("cross_axis") and not crossing:
        how = {"NEUTRAL": "via a neutral shot on the line", "CUTAWAY": "via a cutaway",
               "REESTABLISH": "by re-establishing with a wide"}.get(C["cross_axis"], "in the edit")
        out.append(f"This shot crosses the line of action {how}.")
    return out


def continuity_image_en(st):
    """Continuity for a still: positions and poses, no motion verbs (spec section 21)."""
    subj = _subj(st["shot"].get("primary_subject"))
    out = []
    for x in continuity_en(st, "generic"):
        if x.startswith("The shot opens"):
            out.append("Posed partway through the same action the previous shot ended on.")
        elif " moves from frame-left toward frame-right" in x:
            out.append(f"{subj} is caught heading from frame-left toward frame-right.")
        elif " moves from frame-right toward frame-left" in x:
            out.append(f"{subj} is caught heading from frame-right toward frame-left.")
        elif " moves toward the camera" in x:
            out.append(f"{subj} is caught heading toward the camera.")
        elif " moves away from the camera" in x:
            out.append(f"{subj} is caught heading away from the camera.")
        elif "visibly crosses the line" in x:
            out.append("The camera stands on the far side of the line of action (a crossing).")
        else:
            out.append(x)
    return out


# ---------------------------------------------------------------- movement phrases (EN)


def _p(base, *mods):
    mods = [m for m in mods if m]
    return base + ((", " + ", ".join(mods)) if mods else "") + "."


def move_video_en(mv, st, style):
    """Return (sentences, warnings) for one movement in video mode.
    Generic style states START (opening framing), PATH/DIRECTION, SPEED, SUBJECT RELATION, PARALLAX, END
    (spec section 22); unspecified values are left out (research 07 D16)."""
    c, d = mv["canonical"], mv.get("direction")
    tgt = mv.get("target") if c in ("FOLLOW", "LEAD", "TRACK", "TRACKSIDE") else None
    subj = _subj(tgt or st["shot"].get("primary_subject"))
    sp, amt = _speed_en(mv), _amount_en(mv, "dolly" if c in ("DOLLYIN", "DOLLYOUT") else "generic")
    start, end = mv.get("start_position"), mv.get("end_position")
    W = []
    if style == "h3":
        return _move_h3(mv, st, subj, W)
    g = _guards(mv, st)
    opening = "From this opening framing, the camera" if start and not _later_step(mv, st) else "The camera"
    endp = f"It ends on {_a(end)}." if end else ""
    dd = DIR_EN.get(d or "", "")
    s = []
    if c == "DOLLYIN":
        s = [_p(f"{opening} moves forward along the lens axis toward {subj}", amt, sp),
             f"{subj} grows larger in the frame; near objects grow faster than the background, which spreads past the frame edges.",
             endp, "The focal length stays the same." if g["nozoom"] else ""]
    elif c == "DOLLYOUT":
        s = [_p(f"{opening} moves backward along the lens axis, away from {subj}", amt, sp),
             f"{subj} gets smaller and more of the surroundings appear at the frame edges; near objects shrink faster than distant ones.",
             endp, "The focal length stays the same." if g["nozoom"] else ""]
    elif c in ("ZOOMIN", "ZOOMOUT"):
        io = "in" if c == "ZOOMIN" else "out"
        s = [_p(f"{opening} stays in place while the lens zooms {io}" if g["still"] else f"The lens zooms {io}", amt, sp),
             ("Everything in the frame magnifies by the same amount, with no parallax." if io == "in"
              else "The view widens evenly, with no parallax.") if g["still"] else "",
             endp, "The camera itself does not move." if g["nomove"] else ""]
    elif c == "CRASHZOOM":
        io = "in" if d != "OUT" else "out"
        s = [f"A sudden crash zoom {io}: the lens snaps {'tighter' if io == 'in' else 'wider'} in one violent move.",
             endp, "The world itself does not move; only the focal length changes." if g["nomove"] else ""]
    elif c == "WHIPPAN":
        dest = mv.get("target")
        s = [f"The camera whips {dd or 'sideways'} in a very fast pan" + (f" and lands on the {dest.lower()}" if dest else "") + ".",
             "Everything between the start and the landing smears.", "The camera stays in one spot while it turns." if g["still"] else ""]
        if not dest:
            W.append("WHIPPAN has no destination; a whip pan reads best with a named landing point (/WHIPPAN:R:DOOR).")
    elif c == "PAN":
        s = [_p((f"The camera stays in one spot and pans {dd}" if g["still"] else f"The camera pans {dd}").rstrip(), amt, sp),
             "The view sweeps across the scene with no parallax." if g["still"] else ""]
    elif c == "TILT":
        s = [_p((f"The camera stays in one spot and tilts {dd}" if g["still"] else f"The camera tilts {dd}").rstrip(), amt, sp),
             "The camera stays at the same height." if g["level"] else ""]
    elif c == "ROLL":
        s = [_p(f"The camera rolls {dd} around the lens axis".replace("rolls  ", "rolls "), amt, sp), "The horizon rotates in the frame."]
    elif c == "TRUCK":
        s = [_p(f"The camera slides {dd or 'sideways'}" + (" sideways" if dd else ""), amt, sp),
             "The foreground passes faster than the background.", "The camera does not turn." if g["noturn"] else ""]
    elif c == "PEDESTAL":
        verb = {"UP": "rises straight up", "DOWN": "lowers straight down"}.get(d or "", "moves straight up or down")
        s = [_p(f"The whole camera {verb}", amt, sp),
             "It keeps its angle; near objects shift faster than far ones." if g["noturn"] else "Near objects shift faster than far ones."]
    elif c == "TRACK":
        s = [_p(f"The camera travels with {subj} in a tracking shot", sp),
             f"{subj} stays in the frame the entire way while the background streams past behind."]
    elif c == "FOLLOW":
        s = [_p(f"The camera follows behind {subj} as they move", sp),
             f"{subj} stays in the frame, seen from behind, with the path ahead visible."]
    elif c == "LEAD":
        s = [_p(f"The camera moves backward ahead of {subj} as they walk toward it", sp),
             f"{subj}'s face stays in the frame the entire way."]
    elif c == "TRACKSIDE":
        side = {"L": "toward frame-left", "R": "toward frame-right"}.get(d or "", "")
        s = [_p(f"The camera travels beside {subj}" + (f", moving {side}" if side else "") + ", at the same pace", sp),
             f"{subj} stays about the same size and side-on while the background slides past behind them."]
    elif c == "ORBIT":
        side = {"L": "toward camera-left (clockwise seen from above)", "R": "toward camera-right (counterclockwise seen from above)"}.get(d or "", "")
        a = mv.get("amount") or {}
        full = a.get("value") == "FULL" or (a.get("unit") == "deg" and a["value"] >= 330)
        s = [_p(f"The camera circles {subj}" + (f" {side}" if side else ""), "a full circle" if full else amt, sp),
             f"{subj} stays in place and centered and does not turn; the background sweeps behind {subj}."]
    elif c == "CRANE":
        verb = {"UP": "rises", "DOWN": "descends"}.get(d or "", "moves up or down")
        s = [_p(f"The camera {verb} in a long arc on a crane arm, tilting to keep {subj} framed", sp),
             {"UP": "The view opens out below as it rises.", "DOWN": "The view closes in as it descends."}.get(d or "", "")]
    elif c == "FLYTHROUGH":
        lab = (mv.get("target") or "opening").lower()
        s = [_p(f"The camera moves forward and passes through the {lab} into the space beyond", sp)]
    elif c == "DOLLYZOOM":
        s = [f"{subj} keeps exactly the same size and position in the frame for the whole shot.",
             "The camera moves backward as the lens zooms in to match, and the background flattens and looms closer."
             if d == "OUT" else
             "The camera moves forward as the lens zooms out to match, and the background recedes and stretches away."]
    elif c == "FLYOVER":
        s = [_p("The camera flies forward high over the landscape", sp), "The ground passes underneath."]
    elif c == "DRONEREVEAL":
        how = "rises and pulls back" if d == "BACK" else "rises"
        s = [_p(f"From the air the camera {how} until {subj} is small far below and the whole place opens out around them", sp)]
    elif c == "STATIC":
        s = ["The camera holds still."]
    return [x for x in s if x], W


def _h3_truck_left_verified(mv, st):
    """Truck left alone in a shot: the truck wording measured 3/3 on H3 (LOCAL-002 H3LAB-TRUCK-01)."""
    return (mv["canonical"] == "TRUCK" and mv.get("direction") == "L" and len(st["movement"]) == 1
            and not mv.get("sequential"))


OFFICIAL = "MINIMAX_OFFICIAL"          # verb from the official camera-motion table (SRC-008 base-en 4.3)
PROJECT = "PROJECT_DEFINED"            # wording this project added; its evidence id is kept next to it
H3_LAYERS = ("camera_core", "temporal_clarifier", "derived_visual_constraint", "negative_clarifier")


def _layer(text, source, evidence=None):
    text = " ".join(t for t in text if t) if isinstance(text, (list, tuple)) else text
    if not text:
        return None
    d = {"text": text, "source": source}
    if evidence:
        d["evidence"] = evidence
    return d


def _move_h3_layers(mv, st, subj, W):
    """The H3 camera core for one movement, in four layers (PROJECT_GOAL.md):
    camera_core           the official motion vocabulary, plus the amplitude / speed tokens ONLY when the DSL gives them
    temporal_clarifier    how the move spreads over the clip (project wording)
    derived_visual_constraint  what the move does to the picture: where the subject ends up, what stays in frame, amounts in
                               degrees / percent / metres that the official vocabulary cannot carry (never dropped)
    negative_clarifier    what the camera does NOT do (project wording, written only when no other move contradicts it)
    Returns (layers dict, opening sentence or None). The opening sentence is the start framing of a push/pull, which
    belongs to the framing position of the shot, not to the move."""
    c, d = mv["canonical"], mv.get("direction")
    start, end = mv.get("start_position"), mv.get("end_position")
    spd = mv.get("speed")
    amount = mv.get("amount") or {}
    mag = amount.get("value")
    numeric = amount.get("unit") in ("deg", "%", "m")
    g = _guards(mv, st)
    L = {"canonical": c, "direction": d}
    opening = None
    # official tokens, only when asked for (SRC-008 base-en:114-115: medium amplitude / normal speed are omitted)
    fast = " at fast speed" if spd == "FAST" else " at slow speed" if spd in ("SLOW", "VSLOW", "IMPERCEPTIBLE") else ""
    if spd == "BRISK":
        W.append("H3 has only 'at slow speed' and 'at fast speed' (SRC-008 base-en:114-115); BRISK is written as normal speed.")
    amp = " with large amplitude" if mag == "LARGE" else " with small amplitude" if mag == "SMALL" else ""
    if mag == "SMALL":
        W.append("H3: 'with small amplitude' is nearly inert (SRC-009 camera-grammar); a closer end size controls a push better.")
    num = _amount_en(mv, "dolly" if c in ("DOLLYIN", "DOLLYOUT") else "generic") if numeric else ""

    def core(text, source=OFFICIAL, evidence=None):
        L["camera_core"] = _layer(text, source, evidence)

    def temporal(text, evidence=None):
        L["temporal_clarifier"] = _layer(text, PROJECT, evidence)

    def derived(text, evidence=None):
        L["derived_visual_constraint"] = _layer(text, PROJECT, evidence)

    def negative(text, evidence=None):
        L["negative_clarifier"] = _layer(text, PROJECT, evidence)

    if c in ("DOLLYIN", "DOLLYOUT"):
        verb = "pushes in" if c == "DOLLYIN" else "pulls out"
        noun = "push" if c == "DOLLYIN" else "pull-out"
        if mv.get("sequential"):
            start = None if _later_step(mv, st) else start
        if start:
            opening = f"The camera starts on {_a(start)} that frames {subj} {SIZE_BODY_EN[start]}."
        core(f"The camera {verb}{amp}{fast}" + ("" if start else f" toward {subj}") + ".")
        steady = not (spd in ("FAST", "BRISK") or mag == "LARGE")
        if steady:   # a slow or unstated push is carried by the lab's steady wording (LOCAL-002 H3LAB-PUSH-01)
            if mv.get("sequential"):
                temporal(f"The {noun} continues steadily for the rest of the video." if _last_step(mv, st) else f"The {noun} continues steadily.",
                         "LOCAL-002 H3LAB-PUSH-01; research/07 D41")
            else:
                temporal(f"The {noun} continues steadily over the whole video.", "LOCAL-002 H3LAB-PUSH-01")
        derived([f"The {noun} covers {num}." if num else "",
                 f"The final frame is {_a(end)} of {subj} {SIZE_BODY_EN[end]}." if end else ""], "LOCAL-002 H3LAB-PUSH-01")
        if g["nozoom"]:
            negative("The focal length stays the same.", "research/07 D39")
        if not end:
            W.append("H3: the push/pull has no end size. Measured control comes from stating the start and end framing (LOCAL-002 H3LAB-PUSH-01; SRC-009 framing.md). Add a range, e.g. /%s:%s>%s." % (c, start or "MS", "MCU" if c == "DOLLYIN" else "WS"))
        if not st["composition"].get("foreground"):
            W.append("H3: with nothing near the lens a push reads as a zoom (SRC-009 camera-grammar:41-43). The DSL cannot add scene objects; add a near object in the scene description if the travel must read.")
        if spd == "FAST" or mag == "LARGE":
            W.append("H3: 'large amplitude' / 'fast speed' over-drive a push (3.18x / 2.90x vs 1.53x, SRC-009) and do not stack.")
    elif c in ("ZOOMIN", "ZOOMOUT"):
        io_ = "in" if c == "ZOOMIN" else "out"
        core(f"The camera zooms {io_}{amp}{fast} on {subj}.")
        derived([f"The zoom covers {num}." if num else "", f"The final frame is {_a(end)}." if end else ""], "LOCAL-002 H3LAB-PUSH-01")
        if g["nomove"]:
            negative("The camera itself does not move.", "research/07 D39")
    elif c == "CRASHZOOM":
        io_ = "in" if d != "OUT" else "out"
        # a crash zoom IS a sudden, large, fast zoom: the tokens are definitional, not added (SRC-009 shots/crash-zoom-in.md)
        core(f"The camera zooms {io_} with large amplitude at fast speed on {subj}, a sudden crash zoom.", OFFICIAL, "SRC-009 shots/crash-zoom-in.md")
        if g["nomove"]:
            negative("The camera itself does not move.", "research/07 D39")
    elif c == "WHIPPAN":
        dd = DIR_EN.get(d or "", "sideways")
        dest = mv.get("target")
        if dest:
            core([f"The camera first frames {subj}.", f"Then it whip pans {dd} and lands on the {dest.lower()}."], "SRC-009", "SRC-009 shots/whip-pan.md")
            temporal(f"It holds on the {dest.lower()} until the end of the video.", "SRC-009 shots/whip-pan.md")
        else:
            core(f"The camera whip pans {dd}.", "SRC-009", "SRC-009 shots/whip-pan.md")
            W.append("H3: a whip pan needs a destination; naming it raised the speed about nine times (SRC-009 camera-grammar:78-82). Use /WHIPPAN:R:DOOR.")
    elif c == "PAN":
        core(f"The camera pans {DIR_EN.get(d or '', '')}{amp}{fast}.".replace("pans .", "pans."))
        if num:
            derived(f"The pan turns {num}.")
        if g["still"]:
            negative("The camera stays in place.", "research/07 D39")
    elif c == "TILT":
        core(f"The camera tilts {DIR_EN.get(d or '', '')}{amp}{fast}.".replace("tilts .", "tilts."))
        if num:
            derived(f"The tilt turns {num}.")
        if g["still"]:
            negative("The camera stays in place.", "research/07 D39")
    elif c == "ROLL":
        core(f"The camera rolls {dict(CW='clockwise', CCW='counterclockwise').get(d or '', '')}{fast}.".replace("rolls .", "rolls."))
        if num:
            derived(f"The roll turns {num}.")
    elif c == "TRUCK":
        core(f"The camera trucks {DIR_EN.get(d or '', 'sideways')}{amp}{fast}.")
        # naming where the subject ends up stopped H3 locking her in the centre (LOCAL-002 H3LAB-TRUCK-01, 3/3 alone);
        # the mirrored clause for a truck right was 1/3 (H3LAB-TRUCK-02), so it is written only for the verified case
        derived([f"The truck covers {num}." if num else "",
                 f"In the final frame {subj} is on the right side of the frame." if _h3_truck_left_verified(mv, st) else ""],
                "LOCAL-002 H3LAB-TRUCK-01")
        negative("The camera slides sideways and does not turn." if g["noturn"] else "The camera slides sideways.", "research/07 D39")
    elif c == "PEDESTAL":
        core(f"The camera pedestals {DIR_EN.get(d or '', '')}{amp}{fast}.".replace("pedestals .", "pedestals."))
        if num:
            derived(f"The pedestal covers {num}.")
        if g["noturn"]:
            negative("The camera stays level.", "research/07 D39")
    elif c in ("TRACK", "FOLLOW", "LEAD", "TRACKSIDE"):
        keep = KEEP_IN_FRAME_EN.get(st["shot"].get("size") or "MS", "whole upper body")
        if c == "TRACK":
            core(f"The camera follows {subj} in a tracking shot{fast}.")
            derived(f"{subj}'s {keep} stays inside the frame the entire way.", "LOCAL-002 H3LAB-TRACK-01")
        elif c == "FOLLOW":
            core(f"The camera follows behind {subj} in a tracking shot{fast}.")
            derived(f"{subj}'s {keep} stays inside the frame the entire way.", "LOCAL-002 H3LAB-TRACK-01")
        elif c == "LEAD":
            core(f"The camera moves backward ahead of {subj} in a tracking shot{fast}.")
            derived(f"{subj}'s face stays inside the frame the entire way.", "LOCAL-002 H3LAB-TRACK-01")
        else:
            side = {"L": "toward frame-left", "R": "toward frame-right"}.get(d or "", "")
            core(f"The camera travels beside {subj} in a tracking shot{fast}{', moving ' + side if side else ''} at {subj}'s pace.")
            derived([f"The camera stays at {subj}'s side the whole time, and {subj}'s {keep} stays inside the frame.",
                     f"{subj} stays about the same size while the background slides past behind."], "spec section 23; LOCAL-002 H3LAB-TRACK-01")
    elif c == "ORBIT":
        full = mag == "FULL" or (amount.get("unit") == "deg" and amount["value"] >= 330)
        side = {"L": " toward camera-left", "R": " toward camera-right"}.get(d or "", "")
        if full:
            core(f"The camera circles {subj} all the way around in an arc shot{amp}{fast}, ending back at the front.")
            if fast != " at fast speed":
                W.append("H3 completed a full circle only 'with large amplitude at fast speed' (SRC-009 orbit-360); without :FAST it may stop partway. The tokens are not added unless the DSL asks for them.")
        else:
            core(f"The camera moves in an arc shot around {subj}{side}{amp}{fast}.")
        derived([f"The arc covers {num}." if (num and not full) else "",
                 f"The camera keeps {subj} in the center." if not full else "",
                 f"{subj} stays in place and does not turn."], "registry ORBIT definition")
    elif c == "CRANE":
        if d == "DOWN":
            core(f"The camera pedestals down in one long descent{amp}{fast}.")
            derived(f"It tilts up to keep {subj} in frame.", "registry CRANE definition")
            W.append("H3: a crane descent (Pedestal Down + Tilt Up) is untested; only the rise was measured (SRC-009 direction.md).")
        else:
            core(f"The camera pedestals up high in one long rise{amp}{fast}.")
            derived(f"It tilts down to keep {subj} in frame.", "registry CRANE definition")
    elif c == "FLYTHROUGH":
        lab = (mv.get("target") or "opening").lower()
        core(f"The camera pushes in{fast}.")
        derived(f"It passes through the {lab} into the space beyond.", "registry FLYTHROUGH definition")
    elif c == "DOLLYZOOM":
        if d == "OUT":
            core("The camera pulls out while zooming in at the matching rate.", OFFICIAL, "SRC-009 shots/dolly-zoom.md")
            derived([f"{subj} keeps the same size and position in the frame for the whole video.",
                     "Only the background changes: it flattens and looms closer."], "SRC-009 shots/dolly-zoom.md")
            W.append("H3: the telephoto dolly zoom (Pull Out + Zoom In) has weaker evidence than the forward one (SRC-009 direction.md).")
        else:
            core("The camera pushes in while zooming out at the matching rate.", OFFICIAL, "SRC-009 shots/dolly-zoom.md")
            derived([f"{subj} keeps the same size and position in the frame for the whole video.",
                     "Only the background changes: it recedes and spreads apart."], "SRC-009 shots/dolly-zoom.md")
        W.append("H3: the dolly zoom is the least reliable measured shot; open at the size it keeps (SRC-009 shots/dolly-zoom.md).")
    elif c == "FLYOVER":
        core(f"The camera flies forward high over the landscape{fast}.", PROJECT, "registry FLYOVER definition")
        derived("The ground passes underneath.", "registry FLYOVER definition")
    elif c == "DRONEREVEAL":
        if d == "BACK":
            core(f"The camera pulls out{amp}{fast} while pedestalling up.")
        else:
            core(f"The camera pedestals up{amp}{fast}.")
        derived(f"It rises until {subj} is small far below and the whole place opens out around them.", "registry DRONEREVEAL definition")
    elif c == "STATIC":
        core("The camera holds a Static Shot.", OFFICIAL, "LOCAL-002 H3LAB-STATIC-01")
    else:
        core(f"The camera {c.lower()}s.", PROJECT)
    untested = {("PAN", "L"), ("TILT", "UP"), ("PEDESTAL", "DOWN"), ("ROLL", "CW"), ("TRUCK", "L"), ("TRUCK", "R")}
    if (c, d) in untested and not _h3_truck_left_verified(mv, st):
        W.append(f"H3: {c.lower()} {DIR_EN.get(d, d)} is a documented primitive but untested in SRC-009 (direction.md); judge the first render.")
    for k in H3_LAYERS:
        L.setdefault(k, None)
    return L, opening


def _move_h3(mv, st, subj, W):
    """Flat sentence list of the layered H3 core, in layer order (the joined text the wrappers place into the prompt)."""
    L, opening = _move_h3_layers(mv, st, subj, W)
    s = [opening] if opening else []
    for k in H3_LAYERS:
        if L.get(k):
            s += re.split(r"(?<=[.!?])\s+", L[k]["text"])
    return s, W


# ---------------------------------------------------------------- image-mode movement phrases (EN)


def move_image_en(mv, st, edit=False):
    c, d = mv["canonical"], mv.get("direction")
    subj = _subj(st["shot"].get("primary_subject"))
    end = mv.get("end_position")
    a = mv.get("amount") or {}
    deg = int(a["value"]) if a.get("unit") == "deg" else None
    side = {"L": "camera-left", "R": "camera-right"}.get(d or "", "")
    if c == "DOLLYIN":
        return f"The camera is positioned close to {subj}" + (f", at the {SIZE_SHORT_EN[end]} a push-in would reach" if end else ", as if partway through a push-in") + "; near objects look large at the frame edges."
    if c == "DOLLYOUT":
        return f"The camera is positioned farther back from {subj}" + (f", at the {SIZE_SHORT_EN[end]} a pull-back would reach" if end else ", as if partway through a pull-back") + "; more of the surroundings show at the edges."
    if c == "ZOOMIN":
        return f"Framed as if through a longer focal length: a flat, compressed view of {subj}" + (f" at {_a(end)}" if end else "") + "."
    if c == "ZOOMOUT":
        return "Framed wider from the same camera position" + (f", at {_a(end)}" if end else "") + "."
    if c == "CRASHZOOM":
        return f"Framed at the landing point of a crash zoom: a tight view of {subj}."
    if c == "PAN":
        opp = {"L": "right", "R": "left"}.get(d or "", "")
        return (f"Composed as a moment within a pan to the {DIR_EN[d]}: {subj} sits toward the {opp} edge with open space to the {DIR_EN[d]}."
                if d else "Composed as a moment within a pan.")
    if c == "WHIPPAN":
        dest = (mv.get("target") or "next view").lower()
        return f"A whip-pan moment: strong horizontal motion blur streaks across the frame, with the {dest} starting to resolve."
    if c == "TILT":
        return f"Composed as a moment within a tilt {DIR_EN.get(d or '', '')}: the frame favors the {'upper' if d == 'UP' else 'lower'} part of the scene." if d else "Composed as a moment within a tilt."
    if c == "ROLL":
        return "The horizon is strongly tilted, as a moment within a roll."
    if c == "TRUCK":
        return f"The camera is positioned side-on, as a moment within a sideways move toward {side or 'the side'}."
    if c == "PEDESTAL":
        return f"The camera is at the height the {'rise' if d == 'UP' else 'descent'} reaches, still level."
    if c == "TRACK":
        return f"Seen from a tracking position that keeps pace with {subj}."
    if c == "FOLLOW":
        return f"Seen from a following position behind {subj}."
    if c == "LEAD":
        return f"Seen from a leading position in front of {subj}, facing them."
    if c == "TRACKSIDE":
        return f"Seen side-on from a tracking position beside {subj}."
    if c == "ORBIT":
        if a.get("value") == "FULL":
            return f"The camera is positioned on an implied orbit path around {subj}; {subj} stays centered."
        where = f"about {deg} degrees around {subj}" if deg else f"partway around {subj}"
        return f"The camera is positioned {where}{' toward ' + side if side else ''}, as a moment on an implied orbit path; {subj} stays centered."
    if c == "CRANE":
        return f"The camera is high on a crane at the top of the {'rise' if d != 'DOWN' else 'descent'}, looking toward {subj}." if d != "DOWN" else f"The camera is low, at the bottom of a crane descent, looking toward {subj}."
    if c == "FLYTHROUGH":
        lab = (mv.get("target") or "opening").lower()
        return f"Framed through the {lab}, its edges in the near foreground, with the space beyond in view."
    if c == "DOLLYZOOM":
        return (f"{subj} at the same size as the opening frame, while the background looks unusually "
                + ("compressed and looming close." if d == "OUT" else "stretched far away."))
    if c == "FLYOVER":
        return "Seen from the air over the landscape, as a moment in forward flight."
    if c == "DRONEREVEAL":
        return f"{subj} is small far below, inside the wide place the rise has revealed."
    return ""


# ---------------------------------------------------------------- chinese (Kling zh, Qwen zh)

SIZE_ZH = {"EWS": "大远景，{S}在广阔空间里很小", "WS": "远景，{S}全身入画并带到大量环境", "FS": "全景，{S}从头到脚完整入画",
           "MFS": "中全景，{S}膝盖以上入画", "COWBOY": "{S}大腿中部以上入画", "MS": "中景，{S}腰部以上入画",
           "MCU": "近景，{S}胸口以上入画", "CU": "特写，{S}的脸部（头肩）", "ECU": "大特写，只拍{S}的一个局部"}
HEIGHT_ZH = {"GROUND": "贴地机位，镜头紧贴地面", "ANKLE": "脚踝高度机位", "KNEE": "膝盖高度机位", "HIP": "机位齐腰高度",
             "CHEST": "胸口高度机位", "SHOULDER": "肩膀高度机位", "ELEVATED": "高于视线的机位", "AERIAL": "空中机位，航拍"}
PITCH_ZH = {"LOW": "仰拍，镜头从下往上看{S}", "HIGH": "俯拍，镜头从上往下斜看{S}（不是垂直俯视）",
            "VERTICAL_DOWN": "顶拍，镜头垂直向下看{S}", "VERTICAL_UP": "极低机位垂直仰拍（虫视）"}
SPEED_ZH = {"IMPERCEPTIBLE": "几乎察觉不到地", "VSLOW": "非常缓慢地", "SLOW": "缓慢地", "STEADY": "匀速", "BRISK": "较快地", "FAST": "快速地"}


def state_zh(st, image=False):
    out = []
    sh, cam = st["shot"], st["camera"]
    subj = _subj(sh.get("primary_subject"))
    if sh["size"]:
        out.append(SIZE_ZH[sh["size"]].replace("{S}", subj))
    if sh["viewpoint"] == "OTS":
        a, b = _subj(sh.get("foreground_subject") or "A"), _subj(sh.get("primary_subject") or "B")
        out.append(f"过肩镜头，机位在{a}肩后看向{b}，" + ("前景人物不入画" if sh.get("ots_variant") == "CLEAN" else f"前景可见{a}的肩膀"))
    if sh["viewpoint"] == "POV":
        out.append(f"主观镜头，透过{_subj(sh.get('pov_owner') or 'VIEWER')}的眼睛看，本人不入画")
    cnt = sh.get("subject_count")
    if cnt == "1":
        out.append("单人镜头")
    elif cnt == "2" and sh["viewpoint"] != "OTS":
        out.append("双人镜头，{A}和{B}同时入画")
    elif cnt == "3":
        out.append("三人镜头")
    elif cnt == "GROUP":
        out.append("群像镜头")
    ori = sh.get("orientation")
    if ori and st["meta"]["origins"].get("shot.orientation") not in (None, "DEFINITIONAL"):
        out.append({"FRONTAL": f"{subj}正面朝向镜头", "THREEQUARTER": f"{subj}四分之三侧面", "PROFILE": f"{subj}侧面",
                    "REAR": f"{subj}背面朝向镜头"}[ori])
    if cam.get("position") == "FAR_ABOVE":
        out.append(f"鸟瞰，从极高处垂直向下看，地面像地图，{subj}很小")
    elif cam.get("position") == "DRONE":
        out.append("无人机视角，从无人机高度" + ("向下斜看" if cam.get("angle") == "HIGH" else ""))
        if cam.get("angle") and cam.get("angle") != "HIGH":
            out.append(PITCH_ZH.get(cam["angle"], "").replace("{S}", subj))
    elif cam.get("height") == "EYE" and cam.get("angle") == "LEVEL":
        out.append(f"平视，机位在{subj}的视线高度")
    else:
        if cam.get("height") in HEIGHT_ZH:
            out.append(HEIGHT_ZH[cam["height"]])
        if cam.get("angle") in PITCH_ZH:
            out.append(PITCH_ZH[cam["angle"]].replace("{S}", subj))
    if cam.get("orientation") == "DUTCH":
        out.append("斜角构图（荷兰角），地平线倾斜")
    L = st["lens"]
    if L.get("focal_length"):
        out.append(f"{int(L['focal_length'])}mm 镜头")
    elif L.get("lens_type"):
        out.append({"ULTRAWIDE": "超广角镜头", "WIDE": "广角镜头", "NORMAL": "标准镜头", "PORTRAIT": "人像镜头（约85mm）",
                    "TELE": "长焦镜头，背景被压缩"}[L["lens_type"]])
    for t in L.get("types", []):
        if t == "FISHEYE" and L.get("lens_type") == "ULTRAWIDE" and not L.get("focal_length"):
            out = [x for x in out if x != "超广角镜头"]
        out.append({"MACRO": "微距镜头", "FISHEYE": "鱼眼镜头", "ANAMORPHIC": "变形宽银幕镜头，椭圆焦外光斑"}[t])
    F = st["focus"]
    if F.get("depth_of_field") == "SHALLOW":
        out.append(f"浅景深，{subj}清晰，背景虚化")
    elif F.get("depth_of_field") == "DEEP":
        out.append("深焦，前景到背景都清晰")
    if F.get("target"):
        out.append({"FG": "焦点在前景", "MG": "焦点在中景", "BG": "焦点在背景"}[F["target"]])
    if F.get("special"):
        out.append("分屈光镜，近处和远处同时清晰")
    tr = F.get("transition")
    if tr:
        fr, to = _plane_zh(tr.get("from")), _plane_zh(tr.get("to"))
        still = not any(not m.get("time") for m in st["movement"])
        out.append(f"焦点在{fr}（移焦的起点），{to}虚" if image else f"移焦：焦点从{fr}转移到{to}" + ("，构图不变" if still else ""))
    C = st["composition"]
    if C.get("placement") == "CENTER":
        out.append("居中构图")
    elif (C.get("placement") or "").startswith("THIRD"):
        out.append("三分法构图" + {"THIRD_L": "，主体在左三分线", "THIRD_R": "，主体在右三分线"}.get(C["placement"], ""))
    if C.get("symmetry"):
        out.append("对称构图")
    if C.get("negative_space"):
        out.append("大面积留白")
    if C.get("headroom"):
        out.append({"TIGHT": "头部空间很少", "NORMAL": "头部空间适中", "LOOSE": "头部空间充足"}[C["headroom"]])
    if C.get("lookroom"):
        out.append("视线空间：主体面朝的一侧留出空间")
    if C.get("leading_lines"):
        out.append("引导线指向主体")
    if C.get("frame_in_frame"):
        out.append("框中框构图")
    if C.get("foreground"):
        out.append("前景遮挡，近处有场景元素挡在镜头与主体之间")
    if C.get("depth_layers"):
        out.append("纵深调度，人物分布在不同景深")
    R = st["rig"]
    if R.get("stability") == "LOCKED" and not R.get("type") and not st["movement"]:
        out.append("固定镜头，机位从头到尾保持不动")
    elif R.get("type"):
        out.append({"TRIPOD": "三脚架固定机位", "HANDHELD": "手持，" + ("强烈晃动" if R.get("intensity") == "STRONG" else "轻微自然晃动"),
                    "SHOULDER": "肩扛拍摄，轻微摇晃", "STEADICAM": "斯坦尼康，平稳漂浮", "GIMBAL": "稳定器，非常平稳",
                    "SLIDER": "滑轨，短距离平滑移动", "DRONE": "无人机拍摄", "FPV": "穿越机，快速灵活飞行"}[R["type"]])
        if "GIMBAL" in (R.get("types") or []) and R["type"] != "GIMBAL":
            out.append("稳定器，非常平稳")
        if R.get("locked") and not st["movement"]:
            out.append("固定镜头，机位从头到尾保持不动")
    return out


def _plane_zh(x):
    return {"FG": "前景", "MG": "中景", "BG": "背景", None: "第一个主体", "": "第一个主体"}.get(x, _subj(x))


def move_zh(mv, st):
    c, d = mv["canonical"], mv.get("direction")
    g = _guards(mv, st)
    still = "机位不动，" if g["still"] else ""
    subj = _subj(st["shot"].get("primary_subject"))
    sp = SPEED_ZH.get(mv.get("speed") or "", "")
    end = mv.get("end_position")
    endz = ("，最后停在" + SIZE_ZH[end].split("，")[0]) if end else ""
    dz = {"L": "向左", "R": "向右", "UP": "向上", "DOWN": "向下"}.get(d or "", "")
    return {
        "DOLLYIN": f"推镜：镜头{sp}向前推进靠近{subj}{endz}，{subj}在画面中变大" + ("，焦距不变" if g["nozoom"] else ""),
        "DOLLYOUT": f"拉镜：镜头{sp}向后拉远{endz}，{subj}变小，画面边缘露出更多环境" + ("，焦距不变" if g["nozoom"] else ""),
        "ZOOMIN": f"变焦推近：{still if g['nomove'] else ''}镜头{sp}变焦推近{endz}",
        "ZOOMOUT": f"变焦拉远：{still if g['nomove'] else ''}镜头{sp}变焦拉远{endz}",
        "CRASHZOOM": "急速变焦：镜头突然猛烈" + ("推近" if d != "OUT" else "拉远") + ("，机位不动" if g["nomove"] else ""),
        "PAN": f"横摇：{still}镜头{sp}{dz}横摇",
        "WHIPPAN": f"甩镜：镜头极快地{dz}甩过去" + (f"，停在{(mv.get('target') or '').lower()}上" if mv.get("target") else ""),
        "TILT": f"纵摇：{still}镜头{sp}{dz}纵摇",
        "ROLL": "旋转镜头：镜头绕光轴" + {"CW": "顺时针", "CCW": "逆时针"}.get(d or "", "") + "滚转",
        "TRUCK": f"横移：镜头{sp}{dz}平移，" + ("机位不转动，" if g["noturn"] else "") + "前景比背景移动得快",
        "PEDESTAL": f"升降：整个机位{sp}{dz}垂直移动" + ("，角度不变" if g["noturn"] else ""),
        "TRACK": f"跟拍：镜头{sp}跟随{subj}移动，{subj}始终在画面内",
        "FOLLOW": f"背后跟拍：镜头{sp}在{subj}身后跟随",
        "LEAD": f"前方倒退跟拍：镜头在{subj}前方{sp}后退，{subj}的脸始终在画面内",
        "TRACKSIDE": f"侧面跟拍：镜头在{subj}身旁{sp}" + {"L": "向左", "R": "向右"}.get(d or "", "") + f"平行移动，{subj}大小不变，背景从身后滑过",
        "ORBIT": f"环绕：镜头{sp}绕着{subj}" + {"L": "向左", "R": "向右"}.get(d or "", "") + "移动"
                 + (f"约{int(mv['amount']['value'])}度" if (mv.get("amount") or {}).get("unit") == "deg" else
                    "一整圈（360度）" if (mv.get("amount") or {}).get("value") == "FULL" else
                    "一段弧线" if (mv.get("amount") or {}).get("value") == "PARTIAL" else "")
                 + f"，{subj}保持在原地不转身，背景在身后扫过",
        "CRANE": f"摇臂：镜头{sp}" + ("大幅升起" if d == "UP" else "大幅下降" if d == "DOWN" else "升降") + f"，同时调整角度保持{subj}在画面内",
        "FLYTHROUGH": f"穿越：镜头向前穿过{(mv.get('target') or '开口').lower()}进入另一个空间",
        "DOLLYZOOM": f"滑动变焦：{subj}在画面中的大小和位置始终不变，" + ("镜头后拉同时变焦推近，背景被压缩逼近" if d == "OUT" else "镜头前推同时变焦拉远，背景向后退远"),
        "FLYOVER": "飞越：镜头从高空向前飞过地面",
        "DRONEREVEAL": f"航拍揭示：镜头升高" + ("并后退" if d == "BACK" else "") + f"，直到{subj}在下方变得很小，整个场景展开",
        "STATIC": "镜头保持不动",
    }.get(c, "")


def continuity_zh(st):
    C = st["continuity"]
    out = []
    crossing = C.get("cross_axis") in ("MOVE", "BLOCKING")
    if crossing:
        out.append("越轴：镜头在运动中明确跨过轴线" if C["cross_axis"] == "MOVE" else "越轴：由演员走位跨过轴线")
    if C.get("axis"):
        a, b = C["axis"].split("-")
        out.append(f"镜头结束时{{{a}}}在画面左侧，{{{b}}}在右侧" if crossing else f"{{{a}}}始终在画面左侧，{{{b}}}在右侧")
    for rel in C.get("eyeline", []):
        src, _, tgt = rel.partition(">")
        if tgt == "CAM":
            out.append(f"{_subj(src)}直视镜头")
        elif tgt in ("OFFL", "OFFR"):
            out.append(f"{_subj(src)}看向画面外{'左' if tgt == 'OFFL' else '右'}侧")
        elif tgt:
            out.append(f"{_subj(src)}的视线落在{_subj(tgt)}身上")
    sd = C.get("screen_direction")
    if sd:
        out.append(_subj(st["shot"].get("primary_subject"))
                   + {"L2R": "从左向右移动", "R2L": "从右向左移动", "TOWARD": "朝镜头移动", "AWAY": "远离镜头移动"}[sd])
    for r in C.get("relation_to_previous_shot", []):
        out.append({"SRS": "正反打：与上一镜对称的反打机位，镜头与距离相同",
                    "MATCHACTION": "动作剪辑：开场延续上一镜结束时的动作",
                    "MATCHCUT": "匹配剪辑：主要形状放在与上一镜相同的画面位置"}.get(r["type"], ""))
    if C.get("cross_axis") and not crossing:
        out.append("越轴：按剪辑方式处理越轴")
    fn = st["shot"].get("function")
    if fn:
        t = (st["shot"].get("function_target") or "").lower()
        out.append({"REACTION": f"反应镜头：{_subj(st['shot'].get('function_target'))}的反应表情清楚可见",
                    "INSERT": f"插入镜头：{t or '物体'}的细节占满画面",
                    "CUTAWAY": f"空镜（切出镜头）：{t or '周围环境'}，离开主要动作"}[fn])
    return out


# ---------------------------------------------------------------- render entry


# ---------------------------------------------------------------- H3 capability profile and production routing

_PROFILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "minimax_h3_profile.yaml")


MODES_H3 = ("T2VA", "I2VA", "FL2VA", "L2VA", "REF2VA")


def h3_profile():
    """models/minimax_h3_profile.yaml as a dict: generation_profiles, reality_evidence (bound to mode + generation
    profile) and production_routes (PROJECT_GOAL.md); {} when the file is missing."""
    try:
        return yaml_lite.load_file(_PROFILE_PATH) or {}
    except Exception:
        return {}


EVIDENCE_TABLES = ("viewpoint", "focus", "lens", "continuity", "camera_motion")
# MEASURED: the reality matrix and lab cells; PROVISIONAL: tested before the mode-wrapper audit (kept, not generalised);
# POST_REFACTOR_VALIDATION: re-tested with the formal camera core and mode wrapper
EVIDENCE_STATUSES = ("MEASURED", "PROVISIONAL", "POST_REFACTOR_VALIDATION")
# CURRENT_CORE_EXACT_MATCH: the evidence was generated with the camera text the formal core writes today (current-core evidence);
# PRE_REFACTOR_WORDING: generated with the wording before CL-030 (historical evidence; current-core applicability UNVERIFIED).
# The same semantics with another sentence split changed H3's behaviour (H3LAB-PAN-NEGATIVE-CLARIFIER-01).
PROMPT_COMPATIBILITY = ("CURRENT_CORE_EXACT_MATCH", "PRE_REFACTOR_WORDING")
# The evidence scope of a production route: mode + generation profile + direction + start framing + end framing.
# end_framing: FREE = measured for a move without a stated end size, SPECIFIED = measured for a move with one
# (/DOLLYIN:MS>MCU); a plain push and a push with an end size behaved differently (PROD_06, PROD_02_R2).
# start_framing / end_size: the shot sizes the route was measured with; measured_dsl: the DSL it was measured with.
# A route is applied only to a move that matches every field it carries. Any other start / end pair is UNVERIFIED:
# the measured_dsl of the related routes is named, their grade is never applied (a 3/3 for MS>MCU says nothing about
# MS>CU or FS>MS). The rows of the reality matrix carry start_framing (and end_size when their dsl has one) and follow
# the same rule: a row measured for /MS /PAN:R is not a measured grade for /FS /PAN:R; it is named there as related
# evidence with its grade, and the shot is UNVERIFIED (CL-044). A row or route without these fields is shown for every framing.
# angle (CL-048): a route measured with a stated angle (the arc of an ORBIT, in degrees) carries angle and is applied only
# to a move that states exactly that angle. Another angle, a keyword such as FULL, or no stated angle is UNVERIFIED:
# the measured_dsl is named as related evidence, its grade is never applied.
END_FRAMINGS = ("FREE", "SPECIFIED")
# which evidence table a matrix row belongs to: the registry category of its commands decides, never the name
EVIDENCE_TABLE_OF_CATEGORY = {
    "CAMERA_ANGLE": "viewpoint", "CAMERA_HEIGHT": "viewpoint", "FOCUS": "focus", "LENS": "lens", "CONTINUITY": "continuity",
    "CAMERA_ROTATION": "camera_motion", "CAMERA_TRANSLATION": "camera_motion", "CAMERA_TRACKING": "camera_motion",
    "COMPLEX_MOVEMENT": "camera_motion", "ZOOM": "camera_motion", "AERIAL": "camera_motion", "CAMERA_RIG": "camera_motion"}
_SCOPE_NOTES = {   # why a scope has no evidence: (English, Chinese); ids, modes and enums stay as they are
    "NO_SCOPE": ("mode and generation profile not given", "未指定 H3 mode 與 generation profile"),
    "NO_PROFILE": ("no generation profile given for mode {mode}", "mode {mode} 未指定 generation profile"),
    "NO_EVIDENCE": ("no reality evidence was measured under {pid}", "{pid} 之下沒有量測過的實測證據"),
    "UNKNOWN_PROFILE": ("unknown generation profile {pid} (known: {known})", "不認得的 generation profile {pid}（已知：{known}）"),
    "MODE_MISMATCH": ("{pid} is a {pmode} profile but mode {mode} was given", "{pid} 是 {pmode} 的 profile，但指定的 mode 是 {mode}"),
    "EVIDENCE_MODE": ("the evidence of {pid} is for mode {emode}, not {mode}", "{pid} 的證據屬於 mode {emode}，不是 {mode}"),
    "UNKNOWN_CONTEXT": ("unknown subject context {ctx} (known: CHARACTER_ANCHORED, ENVIRONMENT_ONLY)",
                        "不認得的 subject context {ctx}（已知：CHARACTER_ANCHORED、ENVIRONMENT_ONLY）"),
    "NO_CONTEXT_EVIDENCE": ("no {ctx} evidence was measured under {pid}", "{pid} 之下沒有量測過 {ctx} 的實測證據"),
}
# subject context of the evidence (CL-051): CHARACTER_ANCHORED = the camera holds, follows or frames a character (every record
# before the free-camera baseline; a record without the field is CHARACTER_ANCHORED); ENVIRONMENT_ONLY = no character in the
# frame, the camera moves through a fixed environment. A grade of one context is never applied to the other.
SUBJECT_CONTEXTS = ("CHARACTER_ANCHORED", "ENVIRONMENT_ONLY")
# the public evidence names (v1.0, CL-052) are aliases of the stored contexts; the records and the routing text keep the stored names
SUBJECT_CONTEXT_ALIASES = {"CONSTRAINED_PRODUCTION": "CHARACTER_ANCHORED", "CAMERA_ONLY": "ENVIRONMENT_ONLY"}


def _ctx_of(rec):
    return str((rec or {}).get("subject_context") or "CHARACTER_ANCHORED").upper()


def h3_scope(h3_mode=None, h3_profile_id=None, subject_context=None):
    """The evidence scope of one render. Reality evidence is read only when the generation profile is given, exists,
    matches the mode and holds evidence for it; otherwise the scope is UNVERIFIED and no grade is borrowed from another
    mode or profile. There is no default profile: nothing is guessed. The subject context (CL-051) selects the evidence of
    that context: ENVIRONMENT_ONLY reads the profile's environment_only_baseline block only; without a context the scope is
    CHARACTER_ANCHORED, the context of every record before CL-051. Returns {mode, generation_profile, subject_context,
    subject_context_given, evidence, evidence_status, note, note_zh, note_code, other_scopes, other_scopes_zh}."""
    P = h3_profile()
    gp = P.get("generation_profiles", {}) or {}
    ev_all = P.get("reality_evidence", {}) or {}
    mode = (h3_mode or "").upper() or None
    pid = h3_profile_id or None
    ctx_raw = (subject_context or "").strip().upper().replace("-", "_") or None
    ctx_raw = SUBJECT_CONTEXT_ALIASES.get(ctx_raw, ctx_raw)
    ctx = ctx_raw or "CHARACTER_ANCHORED"
    code, kw, ev = None, {}, None
    if ctx_raw and ctx_raw not in SUBJECT_CONTEXTS:
        code, kw = "UNKNOWN_CONTEXT", {"ctx": ctx_raw}
    elif pid and pid not in gp:
        code, kw = "UNKNOWN_PROFILE", {"pid": pid, "known": ", ".join(gp) or "none"}
    elif pid:
        pmode = str(gp[pid].get("mode", "")).upper()
        if mode is None and pmode in MODES_H3:
            mode = pmode
        if mode and pmode != mode:
            code, kw = "MODE_MISMATCH", {"pid": pid, "pmode": pmode, "mode": mode}
        else:
            ev = ev_all.get(pid)
            if ev is not None and str(ev.get("mode", "")).upper() != (mode or ""):
                code, kw, ev = "EVIDENCE_MODE", {"pid": pid, "emode": ev.get("mode"), "mode": mode}, None
            elif ev is None:
                code, kw = "NO_EVIDENCE", {"pid": pid}
            elif ctx == "ENVIRONMENT_ONLY":
                env = ev.get("environment_only_baseline")
                if isinstance(env, dict) and _ctx_of(env) == ctx:
                    ev = env
                else:
                    code, kw, ev = "NO_CONTEXT_EVIDENCE", {"ctx": ctx, "pid": pid}, None
    elif mode:
        code, kw = "NO_PROFILE", {"mode": mode}
    else:
        code = "NO_SCOPE"
    note = _SCOPE_NOTES[code][0].format(**kw) if code else None
    note_zh = _SCOPE_NOTES[code][1].format(**kw) if code else None
    others, others_zh, env_others, env_others_zh = [], [], [], []   # the ENVIRONMENT_ONLY scopes are listed after the others
    for k, e in ev_all.items():
        if not isinstance(e, dict):
            continue
        if not (ev is not None and k == pid and ctx == "CHARACTER_ANCHORED"):
            prov = "" if (e.get("evidence_status") or "MEASURED") == "MEASURED" else " " + str(e.get("evidence_status"))
            others.append(f"{e.get('mode')}/{k}" + (f" ({e['scope_short']})" if e.get("scope_short") else "") + prov)
            zs = e.get("scope_short_zh") or e.get("scope_short")
            others_zh.append(f"{e.get('mode')}/{k}" + (f"（{zs}）" if zs else "") + prov)
        env = e.get("environment_only_baseline")
        if isinstance(env, dict) and not (ev is not None and k == pid and ctx == "ENVIRONMENT_ONLY"):
            prov = "" if (env.get("evidence_status") or "MEASURED") == "MEASURED" else " " + str(env.get("evidence_status"))
            env_others.append(f"{e.get('mode')}/{k} ENVIRONMENT_ONLY" + (f" ({env['scope_short']})" if env.get("scope_short") else "") + prov)
            zs = env.get("scope_short_zh") or env.get("scope_short")
            env_others_zh.append(f"{e.get('mode')}/{k} ENVIRONMENT_ONLY" + (f"（{zs}）" if zs else "") + prov)
    return {"mode": mode, "generation_profile": pid, "subject_context": ctx, "subject_context_given": bool(ctx_raw),
            "evidence": ev, "note": note, "note_zh": note_zh, "note_code": code,
            "evidence_status": "UNVERIFIED" if ev is None else (ev.get("evidence_status") or "MEASURED"),
            "other_scopes": others + env_others, "other_scopes_zh": others_zh + env_others_zh}


_H3_SIZES = set(SIZE_EN)
_H3_MOVES = {"PAN", "TILT", "DOLLYIN", "DOLLYOUT", "ZOOMIN", "ZOOMOUT", "TRUCK", "PEDESTAL", "ROLL", "FOLLOW", "LEAD",
             "TRACKSIDE", "ORBIT", "CRANE", "STATIC", "WHIPPAN"}


def _h3_lookup_groups(sh, st):
    """What one shot looks up in the evidence tables: one group per movement (keys canonical:direction:degrees, then
    canonical:direction), STATIC for a locked rig, and the other commands of the shot sorted and joined by '+'
    (the viewpoint cells and the combination cells)."""
    groups = []
    for mv in st["movement"]:
        k = mv["canonical"]
        if mv.get("direction"):
            k += ":" + mv["direction"]
        keys = []
        a = mv.get("amount")
        if isinstance(a, dict) and a.get("unit") == "deg":
            keys.append(f"{k}:{int(a['value'])}")
        keys.append(k)
        groups.append({"label": k, "keys": keys, "canonical": mv["canonical"], "start": mv.get("start_position"), "end_size": mv.get("end_position")})
    if st["rig"].get("locked") and not st["movement"]:
        groups.append({"label": "STATIC", "keys": ["STATIC"], "canonical": "STATIC", "static": True})
    others = sorted({c["canonical"] for seg in sh["segments"] for c in seg["commands"]
                     if c["canonical"] not in _H3_SIZES and c["canonical"] not in _H3_MOVES})
    if others:
        groups.append({"label": "+".join(others), "keys": ["+".join(others)], "canonical": None, "static": True})
    return groups


def _routes_summary(routes):
    """One line for the production routes of a command under the current scope: input: result reliability (details)
    [PROVISIONAL caveat], plus the recipe."""
    parts, recipe = [], ""
    for f in routes:
        tags = [str(f[k]) for k in ("result", "reliability") if f.get(k)]
        extra = [f"{k.replace('_', ' ')} {f[k]}" for k in ("input_limitation", "failure_behavior", "mechanism", "limitation", "visual_usability",
                                                            "physical_fidelity", "confidence") if f.get(k)]
        prov = (f" [PROVISIONAL: {str(f.get('caveat', '')).replace('_', ' ')}]" if f.get("evidence_status") == "PROVISIONAL" else
                " [POST_REFACTOR_VALIDATION]" if f.get("evidence_status") == "POST_REFACTOR_VALIDATION" else "")
        pre = " [pre-refactor prompt wording; current-core applicability UNVERIFIED]" if f.get("prompt_compatibility") == "PRE_REFACTOR_WORDING" else ""
        parts.append(f"{f.get('input')}: " + " ".join(tags) + (f" ({', '.join(extra)})" if extra else "") + prov + pre)
        recipe = f.get("recipe") or recipe
    return "; ".join(parts) + (". " + recipe if recipe else "")


def _asked_angle(mv):
    """The angle a move states: degrees as a number, a keyword (FULL) as text, None when it states none."""
    a = mv.get("amount")
    if not isinstance(a, dict):
        return None
    v = a.get("value")
    if a.get("unit") == "deg" and isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    return v if isinstance(v, str) else None


def _asked_framing(d, zh=False):
    """The start / end framing a move asked for, as words (routing: a route measured for another start / end pair); for a
    command whose routes were measured with a stated angle, the angle that was asked is named too."""
    ang = ""
    if d.get("angle_scope"):
        a = d.get("angle")
        if a is None:
            ang = "、沒有指定角度" if zh else ", no stated angle"
        elif isinstance(a, str):
            ang = f"、角度 {a}" if zh else f", angle {a}"
        else:
            ang = f"、角度 {a:g} 度" if zh else f", angle {a:g} degrees"
    if d.get("end_size"):
        return f"{d.get('start') or '?'}>{d['end_size']}" + ang
    if d.get("static"):     # a viewpoint, focus, lens or continuity row, or a locked shot: its scope is the shot size
        if not d.get("start"):
            return "沒有景別的鏡頭" if zh else "a shot without a shot size"
        return f"景別 {d['start']}" if zh else f"shot size {d['start']}"
    if not d.get("start"):
        return ("沒有景別的運鏡" if zh else "a move without a shot size") + ang
    if zh:
        return f"起幅 {d['start']}" + ("、沒有指定落幅" if d.get("free_end") else "") + ang
    return f"start framing {d['start']}" + (", free end framing" if d.get("free_end") else "") + ang


_MEASURED_TEXT = {}


def _measured_text(md):
    """The H3 camera text the current core writes for a measured DSL (one shot); None when the DSL is not one shot."""
    if md not in _MEASURED_TEXT:
        res = dsl.analyze(md)
        _MEASURED_TEXT[md] = _render_video(res["shots"][0]["state"], "minimax_h3", "en")[0] if len(res["shots"]) == 1 else None
    return _MEASURED_TEXT[md]


def _measured_dsls(items):
    out = []
    for x in items:
        md = x.get("measured_dsl", x.get("dsl"))
        for one in (md if isinstance(md, list) else [md]):
            if one and one not in out:
                out.append(one)
    return out


def _evidence_relation(item, text, one_shot):
    """EXACT when the evidence was measured with exactly this shot: one shot per generation (every measurement was), the
    current core wording, and the same H3 camera text as its measured DSL. RELATED otherwise: another speed, amount,
    sequence, extra command or shot, or the historical wording; its grade is named, never applied (CL-059)."""
    if not one_shot or text is None or item.get("prompt_compatibility") == "PRE_REFACTOR_WORDING":
        return "RELATED"
    return "EXACT" if any(_measured_text(m) == text for m in _measured_dsls([item])) else "RELATED"


def _h3_routing(sh, st, scope, text=None, one_shot=True):
    """Production routing for one shot under one evidence scope (mode + generation profile): shot-size reliability,
    viewpoint and camera-move grades, production routes, and what is UNVERIFIED there. Only the evidence of that scope
    is read. text is the shot's H3 camera text and one_shot says the DSL has no other shot: a grade is applied only to the
    shot it was measured with (evidence_relation EXACT, applicability VERIFIED); a measurement of another shot is named as
    related evidence (RELATED, UNVERIFIED) and nothing at all is NONE (CL-059). Returns (routing dict, warning lines)."""
    ev = scope["evidence"]
    tag = f"{scope['mode'] or 'mode ?'}/{scope['generation_profile'] or 'no profile'}"
    size = st["shot"]["size"]
    if not size:
        for mv in st["movement"]:
            if mv.get("start_position"):
                size = mv["start_position"]
                break
    subj = _subj(st["shot"].get("primary_subject"))
    ctx = scope.get("subject_context") or "CHARACTER_ANCHORED"
    routing = {"scope": {k: scope.get(k) for k in ("mode", "generation_profile", "subject_context", "subject_context_given", "evidence_status",
                                                   "note", "note_zh", "note_code", "other_scopes", "other_scopes_zh")},
               "shot": sh["label"], "shot_size": size, "shot_size_reliability": None, "shot_size_source": None, "shot_size_status": None,
               "recommended_mode": None, "viewpoint": [], "focus": [], "lens": [], "continuity": [], "camera_motion": [],
               "production_routes": {}, "unverified": [], "evidence_relation": "NONE", "applicability": "UNVERIFIED",
               "seed_sensitivity": (ev or {}).get("seed_sensitivity", {}) or {}, "advice": []}
    W = []
    groups = _h3_lookup_groups(sh, st)
    size_name = SIZE_SHORT_EN[size].upper() if size else None
    if ev is None:
        routing["unverified"] = ([f"shot size {size_name}"] if size else []) + [g["label"] for g in groups]
        if routing["unverified"]:
            W.append(f"H3 ROUTING [{tag}]: no reality evidence for this mode and generation profile ({scope['note']}); "
                     + ", ".join(routing["unverified"]) + " — UNVERIFIED, no grade is borrowed from another mode or profile."
                     + (" Evidence exists under " + "; ".join(scope["other_scopes"]) + " and is not applied here." if scope["other_scopes"] else ""))
        return routing, W
    fr = ev.get("framing", {}) or {}
    tos, ff = fr.get("text_only_shot_size"), fr.get("first_frame_framing")
    if size and tos and size in set(tos.get("strict_sizes", []) or []):
        rel = tos.get("reliability", "LOW")
        rec = (fr.get("strict_medium_shot", {}) or {}).get("recommended_mode", "I2VA_FIRST_FRAME")
        routing.update({"shot_size_reliability": rel, "shot_size_source": "text_only", "recommended_mode": rec})
        if scope["mode"] == "REF2VA":
            routing["advice"] = [
                "If the framing must be exact, use a real first frame (I2VA); the frame then decides framing, height and angle and the text controls the move only.",
                f"If Ref2VA is kept, describe what environment {subj} is in, not which environment elements must be visible; a {SIZE_SHORT_EN[size]} frame is not guaranteed.",
            ]
            W.append(f"H3 ROUTING [{tag}]: shot size {size_name} asked; text-only shot size reliability {rel} "
                     f"(models/minimax_h3_profile.yaml). {routing['advice'][0]} {routing['advice'][1]} Environment lists widened the frame "
                     f"(H3LAB-FRAMING-SCENE-01); seed sensitivity HIGH: judge the first render, try another seed before rewording.")
        else:   # the environment advice and its evidence were measured under Ref2VA: not applied to another mode (CL-050)
            routing["advice"] = [
                "If the framing must be exact, use a real first frame (I2VA); the frame then decides framing, height and angle and the text controls the move only.",
                f"If {scope['mode']} is kept, a {SIZE_SHORT_EN[size]} frame is not guaranteed.",
            ]
            W.append(f"H3 ROUTING [{tag}]: shot size {size_name} asked; text-only shot size reliability {rel} "
                     f"(models/minimax_h3_profile.yaml, mode {scope['mode']}). {routing['advice'][0]} {routing['advice'][1]}")
    elif size and ff:
        routing.update({"shot_size_reliability": ff.get("reliability"), "shot_size_source": "first_frame",
                        "shot_size_status": ff.get("evidence_status") or scope["evidence_status"]})
    elif size and not tos and not ff:
        routing["unverified"].append(f"shot size {size_name}")
    tables = []   # (table, key -> rows); one key can have several rows when several cells tested the same commands
    for t in EVIDENCE_TABLES:
        idx = {}
        for e in ((ev.get(t, {}) or {}).get("by_command", []) or []):
            if isinstance(e, dict):
                idx.setdefault(e["key"], []).append(e)
        tables.append((t, idx))
    routes = h3_profile().get("production_routes", {}) or {}
    routed, related_done = set(), set()
    moves = list(st["movement"])
    if st["rig"].get("locked") and not moves:     # a locked shot looks up the STATIC routes (CL-051)
        moves = [{"canonical": "STATIC", "direction": None, "start_position": None, "end_position": None, "amount": None}]
    for mv in moves:
        r = routes.get(mv["canonical"])
        if not r or mv["canonical"] in routing["production_routes"] or mv["canonical"] in related_done:
            continue
        allr = [x for x in (r.get("routes", []) or []) if isinstance(x, dict)]
        here = [x for x in allr if str(x.get("mode", "")).upper() == scope["mode"] and x.get("generation_profile") == scope["generation_profile"]]
        # a route of one subject context is never applied to the other (CL-051)
        same = [x for x in here if _ctx_of(x) == ctx]
        ctx_other = sorted({_ctx_of(x) for x in here if _ctx_of(x) != ctx})
        # a route measured in one direction is not applied to the other direction (the truck left / right asymmetry was real);
        # a route measured with a free end framing is not applied to a move with a stated end size, and the reverse;
        # a route measured for one start / end pair is not applied to another pair;
        # a route measured with a stated angle is not applied to another angle, nor to a move that states none (CL-048)
        start, end_size = mv.get("start_position") or size, mv.get("end_position")
        end = "SPECIFIED" if end_size else "FREE"
        angle = _asked_angle(mv)
        in_dir = [x for x in same if not x.get("direction") or x.get("direction") == mv.get("direction")]
        # start_framing NONE: the route was measured with no shot size (the free-camera routes, CL-051); it is applied only to
        # a move without a shot size, and a route with a shot size never to such a move
        mine = [x for x in in_dir if (not x.get("end_framing") or x.get("end_framing") == end)
                and (not x.get("start_framing") or x.get("start_framing") == (start or "NONE"))
                and (not x.get("end_size") or x.get("end_size") == end_size)
                and ("angle" not in x or (isinstance(angle, float) and float(x["angle"]) == angle))]
        other = sorted({f"{x.get('mode')}/{x.get('generation_profile')}" + ("" if _ctx_of(x) == "CHARACTER_ANCHORED" else " " + _ctx_of(x))
                        + (" PROVISIONAL" if x.get("evidence_status") == "PROVISIONAL" else "") for x in allr if x not in same})
        if mine:
            # a route measured with exactly this shot is applied; a route measured with another shot of the same move
            # (another speed, amount, sequence or extra command) is named as related evidence, its grade never applied (CL-059)
            exact = [x for x in mine if _evidence_relation(x, text, one_shot) == "EXACT"]
            near = [x for x in mine if not any(x is y for y in exact)]
            note = f" Other scopes hold evidence for {mv['canonical']} ({'; '.join(other)}) — not applied." if other else ""
            if exact:
                routing["production_routes"][mv["canonical"]] = exact
                routed.add(mv["canonical"])
                W.append(f"H3 ROUTING [{tag}]: {mv['canonical']} production route — " + _routes_summary(exact) + note)
                note = ""
            if near:
                related_done.add(mv["canonical"])
                md = _measured_dsls(near)
                routing.setdefault("related_routes", []).append({"canonical": mv["canonical"], "routes": near, "measured": md, "one_shot": one_shot})
                W.append(f"H3 ROUTING [{tag}]: {mv['canonical']} related evidence only (measured with {', '.join(md)}"
                         + ("" if one_shot else "; this DSL puts several shots in one generation") + ") — not applied, UNVERIFIED: "
                         + _routes_summary(near) + note)
        elif same and not in_dir:
            measured = "/".join(sorted({str(x.get("direction")) for x in same if x.get("direction")}))
            routing.setdefault("direction_only", []).append({"canonical": mv["canonical"], "measured": measured, "asked": mv.get("direction")})
            W.append(f"H3 ROUTING [{tag}]: {mv['canonical']} was measured under this scope for direction {measured} only; "
                     f"the result is not applied to direction {mv.get('direction')}.")
        elif in_dir:   # measured under this scope, but for another start / end framing or another angle: related routes are named, no grade is applied
            related = []
            for x in ([y for y in in_dir if y.get("end_framing") == end] or in_dir):
                md = x.get("measured_dsl")
                for one in (md if isinstance(md, list) else [md] if md else []):
                    if one not in related:
                        related.append(one)
            d = {"canonical": mv["canonical"], "start": start, "end_size": end_size, "related": related,
                 "free_end": bool(not end_size and any(x.get("end_framing") for x in in_dir))}
            if any("angle" in x for x in in_dir):     # the routes of this command carry an angle: say which angle was asked
                d.update({"angle_scope": True, "angle": angle})
            routing.setdefault("framing_only", []).append(d)
            W.append(f"H3 ROUTING [{tag}]: {mv['canonical']} has no production route measured under this scope for {_asked_framing(d)}; "
                     + (f"related evidence ({', '.join(related)}) is not applied — " if related else "") + "UNVERIFIED.")
        elif ctx_other:   # this profile measured the command only in the other subject context: named, never applied (CL-051)
            routing.setdefault("context_only", []).append({"canonical": mv["canonical"], "measured": "/".join(ctx_other), "asked": ctx})
            W.append(f"H3 ROUTING [{tag}]: {mv['canonical']} was measured under this profile for subject context {'/'.join(ctx_other)} only; "
                     f"it is not applied to subject context {ctx} — UNVERIFIED.")
    seen = set()
    for g in groups:
        hits, where, mk = [], None, None
        for k in g["keys"]:
            for t, idx in tables:
                if k in idx:
                    hits, where, mk = idx[k], t, k
                    break
            if hits:
                break
        if not hits:
            if g["canonical"] not in routed:
                routing["unverified"].append(g["label"])
            continue
        # a matrix row is applied only to the start framing (and end size) it was measured with; another framing is
        # UNVERIFIED and the row is named as related evidence with its grade, never applied
        q_start, q_end = g.get("start") or size, g.get("end_size")
        fit = [x for x in hits if "start_framing" not in x or (x["start_framing"] == q_start and (x.get("end_size") or None) == (q_end or None))]
        if not fit:
            d = {"label": mk, "table": where, "start": q_start, "end_size": q_end, "static": bool(g.get("static")),
                 "free_end": bool(not q_end and any(x.get("end_size") for x in hits)),
                 "related": [{"dsl": x.get("dsl"), "grade": x["grade"], "cell": x["cell"],
                              "historical": x.get("prompt_compatibility") == "PRE_REFACTOR_WORDING"} for x in hits]}
            routing.setdefault("framing_only_rows", []).append(d)
            label = ("" if where == "camera_motion" else where + " ") + mk
            W.append(f"H3 ROUTING [{tag}]: {label} has no row measured under this scope for {_asked_framing(d)}; related evidence ("
                     + ", ".join(f"{x['dsl']} = {x['grade']}" for x in d["related"]) + ") is not applied — UNVERIFIED.")
            if g["canonical"] not in routed:
                routing["unverified"].append(g["label"])
            continue
        hits = fit
        applied = related = False
        for hit in hits:
            if hit["cell"] in seen:
                continue
            seen.add(hit["cell"])
            label = ("" if where == "camera_motion" else where + " ") + mk
            if hit.get("prompt_compatibility") == "PRE_REFACTOR_WORDING":   # historical evidence, never a current measurement
                routing[where].append(dict(hit, matched=mk, relation="RELATED"))
                applied = True
                W.append(f"H3 ROUTING [{tag}]: {label} has a historical grade only: {hit['grade']} ({hit['cell']}, measured with the pre-refactor "
                         f"prompt wording); current-core applicability UNVERIFIED — the formal core writes these sentences differently.")
            elif _evidence_relation(hit, text, one_shot) == "RELATED":   # measured with another shot: named, never applied (CL-059)
                routing.setdefault("related_rows", []).append(dict(hit, matched=mk, table=where))
                related = True
                W.append(f"H3 ROUTING [{tag}]: {label} related evidence only (measured with {hit['dsl']}"
                         + ("" if one_shot else "; this DSL puts several shots in one generation")
                         + f"): H3_RELIABILITY {hit['grade']} ({hit['cell']}) — not applied, UNVERIFIED.")
            else:
                routing[where].append(dict(hit, matched=mk, relation="EXACT"))
                applied = True
                if str(hit["grade"]) in ("C", "D", "F"):
                    W.append(f"H3 ROUTING [{tag}]: {label} measured H3_RELIABILITY {hit['grade']} "
                             f"({hit['cell']}: mechanism {hit['mechanism']}, framing {hit['framing']}, timing {hit['timing']}, continuity {hit['continuity']}); "
                             f"seed sensitivity HIGH: judge the first render, try another seed before rewording.")
        if related and not applied and g["canonical"] not in routed:
            routing["unverified"].append(g["label"])
    if routing["unverified"]:
        W.append(f"H3 ROUTING [{tag}]: no evidence under this scope for " + ", ".join(routing["unverified"])
                 + " — UNVERIFIED (no grade borrowed from another mode or profile).")
    exact = bool(routing["production_routes"]) or any(e.get("relation") == "EXACT" for t in EVIDENCE_TABLES for e in routing[t])
    some = any(routing.get(k) for k in ("related_routes", "related_rows", "framing_only", "framing_only_rows", "direction_only", "context_only")
               ) or any(routing[t] for t in EVIDENCE_TABLES)
    routing["evidence_relation"] = "EXACT" if exact else "RELATED" if some else "NONE"
    routing["applicability"] = "VERIFIED" if exact else "UNVERIFIED"
    return routing, W


_TABLE_LABELS = {"viewpoint": ("viewpoint", "機位"), "focus": ("focus", "對焦"), "lens": ("lens", "鏡頭光學"),
                 "continuity": ("continuity", "連戲"), "camera_motion": ("measured", "實測")}


def routing_text(routings, lang="en"):
    """The routing block the CLI prints under the camera text (English, or Chinese with lang='zh'): the evidence scope
    first, then what that scope says about the shot, then what it cannot say (UNVERIFIED). With lang='zh' the sentences
    are Chinese; ids, modes and enums (UNVERIFIED, PROVISIONAL, profile ids, grades, cell ids) stay as they are."""
    zh = lang == "zh"
    if not routings:
        return ""
    sc = routings[0].get("scope", {})
    mode = sc.get("mode") or ("未指定" if zh else "not given")
    pid = sc.get("generation_profile") or ("未指定" if zh else "not given")
    status = sc.get("evidence_status", "UNVERIFIED")
    note = (sc.get("note_zh") or sc.get("note")) if zh else sc.get("note")
    ctx = sc.get("subject_context") or "CHARACTER_ANCHORED"
    show_ctx = ctx != "CHARACTER_ANCHORED" or sc.get("subject_context_given")   # the default context keeps the pre-CL-051 line
    if zh:
        L = [f"H3 路由（models/minimax_h3_profile.yaml）— 證據範圍：mode {mode}、generation profile {pid}" + (f"、subject context {ctx}" if show_ctx else "")
             + f"：{status}" + (f"（{note}）" if note else "")]
    else:
        L = [f"H3 routing (models/minimax_h3_profile.yaml) — evidence scope: mode {mode}, generation profile {pid}" + (f", subject context {ctx}" if show_ctx else "")
             + f": {status}" + (f" ({note})" if note else "")]
    for r in routings:
        tag = f"[{r['shot']}] " if len(routings) > 1 else ""
        rel = r.get("evidence_relation")
        if rel and status != "UNVERIFIED":   # a scope without evidence already says UNVERIFIED in its first line (CL-059)
            app = r.get("applicability")
            if zh:
                L.append(f"  {tag}證據關係：{rel}——適用性：{app}" + {"EXACT": "（這個範圍量過的就是這個鏡頭）",
                                                                   "RELATED": "（下面的實測是別的鏡頭或舊用字，等級不套用到這個鏡頭）",
                                                                   "NONE": "（這個範圍沒有量過這個鏡頭）"}[rel])
            else:
                L.append(f"  {tag}evidence relation: {rel} — applicability: {app}" + {
                    "EXACT": " (this exact shot was measured under this scope)",
                    "RELATED": " (the measurements below are of other shots or the old wording; their grades are not applied to this shot)",
                    "NONE": " (nothing was measured for this shot under this scope)"}[rel])
        if r.get("shot_size_reliability") and r.get("shot_size_source") == "text_only":
            name = SIZE_SHORT_EN[r["shot_size"]].upper()
            if zh:
                L += [f"  {tag}景別要求：{name}", f"  {tag}可靠度：{r['shot_size_reliability']}（只靠文字）",
                      f"  {tag}建議：若景別必須精確，使用實際首幀／I2VA（首幀決定景別、機位高度與角度，文字只控制運鏡）。",
                      f"  {tag}若仍用 Ref2VA：寫人物所在的是什麼環境，不要列出畫面必須看到的環境元素；不保證維持{name}構圖。" if mode == "REF2VA" else
                      f"  {tag}若仍用 {mode}：不保證維持{name}構圖。"]
            else:
                L += [f"  {tag}shot size asked: {name} — text-only reliability: {r['shot_size_reliability']}",
                      f"  {tag}recommended: {r['recommended_mode']} — {r['advice'][0]}", f"  {tag}{r['advice'][1]}"]
        elif r.get("shot_size_reliability"):
            name = SIZE_SHORT_EN[r["shot_size"]].upper()
            item_status = r.get("shot_size_status") or status
            L.append(f"  {tag}景別 {name}：由首幀決定——可靠度 {r['shot_size_reliability']}（{item_status}）" if zh else
                     f"  {tag}shot size {name}: from the first frame — reliability {r['shot_size_reliability']} ({item_status})")
        for grp in EVIDENCE_TABLES:
            en_name, zh_name = _TABLE_LABELS[grp]
            for e in r.get(grp, []):
                if e.get("prompt_compatibility") == "PRE_REFACTOR_WORDING":   # shown as history, never as a current measurement
                    if zh:
                        L.append(f"  {tag}歷史等級 {'' if grp == 'camera_motion' else '（' + zh_name + '）'}{e['matched']}：{e['grade']}（{e['cell']}：機制 {e['mechanism']}、景別 {e['framing']}、時間 {e['timing']}、連續性 {e['continuity']}）"
                                 f"— 提示詞用字：PRE_REFACTOR；對目前 Core 的適用性：UNVERIFIED［profile {e.get('profile')}］")
                    else:
                        L.append(f"  {tag}historical grade {'' if grp == 'camera_motion' else '(' + en_name + ') '}{e['matched']}: {e['grade']} ({e['cell']}: mechanism {e['mechanism']}, framing {e['framing']}, timing {e['timing']}, continuity {e['continuity']}) "
                                 f"— prompt wording: PRE_REFACTOR; current-core applicability: UNVERIFIED [profile {e.get('profile')}]")
                elif zh:
                    L.append(f"  {tag}{zh_name} {e['matched']}：H3_RELIABILITY {e['grade']}（{e['cell']}：機制 {e['mechanism']}、景別 {e['framing']}、時間 {e['timing']}、連續性 {e['continuity']}）［profile {e.get('profile')}］")
                else:
                    L.append(f"  {tag}{en_name} {e['matched']}: H3_RELIABILITY {e['grade']} ({e['cell']}: mechanism {e['mechanism']}, framing {e['framing']}, timing {e['timing']}, continuity {e['continuity']}) [profile {e.get('profile')}]")
        for e in r.get("related_rows", []):      # measured with another shot under this scope: named, never applied (CL-059)
            en_name, zh_name = _TABLE_LABELS[e["table"]]
            if zh:
                L.append(f"  {tag}{'' if e['table'] == 'camera_motion' else zh_name + ' '}{e['matched']} 相關證據（不套用；實測的是 {e['dsl']}）："
                         f"H3_RELIABILITY {e['grade']}（{e['cell']}：機制 {e['mechanism']}、景別 {e['framing']}、時間 {e['timing']}、連續性 {e['continuity']}）"
                         f"［profile {e.get('profile')}］——UNVERIFIED")
            else:
                L.append(f"  {tag}{'' if e['table'] == 'camera_motion' else en_name + ' '}{e['matched']} related evidence (not applied; measured with {e['dsl']}): "
                         f"H3_RELIABILITY {e['grade']} ({e['cell']}: mechanism {e['mechanism']}, framing {e['framing']}, timing {e['timing']}, continuity {e['continuity']}) "
                         f"[profile {e.get('profile')}] — UNVERIFIED")
        for d in r.get("framing_only_rows", []):      # measured, but for another shot size / end size: named, never applied
            en_name, zh_name = _TABLE_LABELS[d["table"]]
            if zh:
                rel = "、".join(f"{x['dsl']} = {x['grade']}（{'歷史' if x['historical'] else '目前 Core'}，{x['cell']}）" for x in d["related"])
                L.append(f"  {tag}{'' if d['table'] == 'camera_motion' else zh_name + ' '}{d['label']}：這個範圍沒有量過 {_asked_framing(d, True)}——UNVERIFIED；相近證據（不套用）：{rel}")
            else:
                rel = ", ".join(f"{x['dsl']} = {x['grade']} ({'historical' if x['historical'] else 'current'}, {x['cell']})" for x in d["related"])
                L.append(f"  {tag}{'' if d['table'] == 'camera_motion' else en_name + ' '}{d['label']}: no row measured under this scope for {_asked_framing(d)} — UNVERIFIED; "
                         f"related evidence (not applied): {rel}")
        for cmd, pr in (r.get("production_routes") or {}).items():
            L.append((f"  {tag}{cmd} 路徑（DSL 語義不變）：" if zh else f"  {tag}{cmd} production route (DSL semantics unchanged): ") + _routes_summary(pr))
        for d in r.get("related_routes", []):    # routes measured with another shot of the move: named, never applied (CL-059)
            more = "" if d.get("one_shot", True) else ("；這個 DSL 一次生成多個鏡頭" if zh else "; this DSL puts several shots in one generation")
            L.append((f"  {tag}{d['canonical']} 相關證據（不套用；實測的是 {'、'.join(d['measured'])}{more}）——UNVERIFIED：" if zh else
                      f"  {tag}{d['canonical']} related evidence (not applied; measured with {', '.join(d['measured'])}{more}) — UNVERIFIED: ")
                     + _routes_summary(d["routes"]))
        for d in r.get("direction_only", []):
            L.append(f"  {tag}{d['canonical']}：這個範圍只量過方向 {d['measured']}，不套用到方向 {d['asked']}" if zh else
                     f"  {tag}{d['canonical']}: measured under this scope for direction {d['measured']} only — not applied to direction {d['asked']}")
        for d in r.get("context_only", []):
            L.append(f"  {tag}{d['canonical']}：這個 profile 只量過 subject context {d['measured']}，不套用到 subject context {d['asked']}——UNVERIFIED" if zh else
                     f"  {tag}{d['canonical']}: measured under this profile for subject context {d['measured']} only — not applied to subject context {d['asked']} (UNVERIFIED)")
        for d in r.get("framing_only", []):
            rel = d.get("related") or []
            if zh:
                L.append(f"  {tag}{d['canonical']}：這個範圍沒有量過 {_asked_framing(d, True)}——UNVERIFIED" + (f"；相近證據（不套用）：{'、'.join(rel)}" if rel else ""))
            else:
                L.append(f"  {tag}{d['canonical']}: no production route measured under this scope for {_asked_framing(d)} — UNVERIFIED"
                         + (f"; related evidence (not applied): {', '.join(rel)}" if rel else ""))
        if r.get("unverified"):
            items = [("景別 " + u[len("shot size "):]) if zh and u.startswith("shot size ") else u for u in r["unverified"]]
            L.append((f"  {tag}此範圍無證據（UNVERIFIED）：" if zh else f"  {tag}UNVERIFIED under this scope: ") + ("、" if zh else ", ").join(items))
        ss = r.get("seed_sensitivity", {})
        if ss:
            L.append((f"  {tag}seed 敏感度：景別 {ss.get('framing')}、運鏡機制 {ss.get('camera_mechanism')}——先看第一次生成，換 seed 再改字" if zh else
                      f"  {tag}seed sensitivity: framing {ss.get('framing')}, camera mechanism {ss.get('camera_mechanism')} — judge the first render; try another seed before rewording"))
    others = (sc.get("other_scopes_zh") or sc.get("other_scopes")) if zh else sc.get("other_scopes")
    if others:
        L.append(("  其他範圍有證據（不套用）：" if zh else "  evidence under other scopes (not applied): ") + ("；" if zh else "; ").join(others))
    if not sc.get("generation_profile"):   # no default profile is ever assumed
        L.append("  指定 --h3-profile 才會查詢實測證據。" if zh else "  Specify --h3-profile to query measured evidence.")
    return "\n".join(L)


def h3_layers_text(out):
    """The H3 camera core of a render, shot by shot, with every layer and its source (CLI --layers)."""
    L = ["h3_camera_output:"]
    for sh in out["shots"]:
        h3 = sh.get("h3")
        if not h3:
            continue
        tag = f"  [{sh['label']}] " if len(out["shots"]) > 1 else "  "
        for grp in ("framing", "viewpoint", "lens", "focus", "composition", "rig"):
            if h3.get(grp):
                L.append(f"{tag}{grp}: {' '.join(h3[grp])}")
        for mv in h3["movements"]:
            L.append(f"{tag}movement {mv['canonical']}" + (f":{mv['direction']}" if mv.get("direction") else "") + ":")
            for k in H3_LAYERS:
                if mv.get(k):
                    L.append(f"{tag}  {k}:")
                    L.append(f"{tag}    text: {mv[k]['text']}")
                    L.append(f"{tag}    source: {mv[k]['source']}" + (f" ({mv[k]['evidence']})" if mv[k].get("evidence") else ""))
        if h3.get("continuity"):
            L.append(f"{tag}continuity: {' '.join(h3['continuity'])}")
    return "\n".join(L)


def render(result, model="generic_video", mode=None, lang=None, h3_mode=None, h3_profile_id=None, h3_subject_context=None):
    if model not in MODELS:
        raise ValueError(f"unknown model {model!r}; choose from {', '.join(MODELS)}")
    spec = MODELS[model]
    kind = spec["kind"]
    if mode is None and "IMAGE" in result.get("modes", []):
        mode = "image"
    if mode == "image" and kind == "video":
        kind = "image"
    lang = lang or spec["lang"]
    if lang not in spec["langs"]:
        lang = spec["lang"]
    shots_out, warnings, unspecified, implied, routings = [], [], [], [], []
    scope = h3_scope(h3_mode, h3_profile_id, h3_subject_context) if model == "minimax_h3" and kind == "video" else None
    for sh in result["shots"]:
        st = sh["state"]
        h3 = None
        if kind == "video":
            text, w, h3 = _render_video(st, model, lang)
        else:
            text, w = _render_image(st, model, lang, edit=(kind == "image_edit"))
        if scope:
            routing, rw = _h3_routing(sh, st, scope, text, len(result["shots"]) == 1)
            w += rw
            routings.append(routing)
        warnings += [f"{sh['label']}: {x}" for x in w]
        unspecified += [f"{sh['label']}.{u}" for u in st["meta"]["unspecified"]]
        implied += [f"{sh['label']}.{d['from']}.{d['dimension']}={d['value']}" for d in st["meta"]["definitional"]
                    if d.get("source") == "COMMAND_DEFINITION"]
        shots_out.append({"label": sh["label"], "text": text, "h3": h3})
        if any(len(s["commands"]) and not s["global"] for s in sh["segments"]) and model == "minimax_h3":
            warnings.append(f"{sh['label']}: H3 cannot place events at exact times (SRC-009); cuts inside one generation are unreliable (LOCAL-002 H3LAB-CUT-01). Consider one shot per generation.")
    if len(result["shots"]) > 1 and model == "minimax_h3":
        warnings.append("H3: one shot per generation; join the clips in the edit (LOCAL-002 H3LAB-CUT-01).")
    notes = MODEL_NOTES.get(model, [])
    joined = "\n\n".join((f"[{s['label']}] " if len(shots_out) > 1 else "") + s["text"] for s in shots_out)
    all_diags = result["diagnostics"] + [d for s in result["shots"] for d in s["diagnostics"]]
    diag_msgs = [d for d in all_diags if dsl.SEVERITY.get(d["type"]) == "WARN"]
    errors = [f"{d.get('shot', '')}: [{d['rule']}] {d['message']}" + (f" Fix: {d['fix']}" if d.get("fix") else "")
              for d in all_diags if dsl.SEVERITY.get(d["type"]) == "ERROR"]
    origins = {}
    for sh in result["shots"]:
        for seg in sh["segments"]:
            for c in seg["commands"]:
                origins.setdefault(c["origin"], []).append(c["raw"])
    return {"model": model, "mode": kind, "lang": lang, "text": joined, "shots": shots_out,
            "warnings": warnings + [f"{d.get('shot', '')}: [{d['rule']}] {d['message']}" for d in diag_msgs],
            "errors": errors,
            "unspecified": unspecified, "definition_implied": implied, "notes": notes, "status": result["status"],
            "user_specified": origins.get("USER_SPECIFIED", []) + origins.get("STORYBOARD", []),
            "director_suggested": origins.get("DIRECTOR_SUGGESTED", []),
            "routing": routings or None}


MODEL_NOTES = {
    "minimax_h3": ["Place these sentences in [Shot N] of integrated_multimodal_description (base modes) or detailed_description (Ref2VA), after the opening style/composition sentence (SRC-008 base-en:78).",
                   "Run the H3 prompt through the lab lint before sending (LOCAL-002).",
                   "Settings can erase camera motion: 4-step turbo suppresses it; a background reference plate halves it (SRC-009 settings.md)."],
    "kling": ["Use either a Kling camera preset or these camera words, never both (SRC-004 vidadapt:242).",
              "Put exclusions in the negative field, not in this text (SRC-004 vidadapt:242)."],
    "veo": ["Keep audio in its own sentence after the camera text (SRC-005D SKILL:68-75)."],
    "flux": ["Keep size, angle and lens early in the prompt (SRC-004 imgadapt:66-83)."],
    "qwen_image": ["Evidence for Qwen-Image camera wording is limited to a capability matrix (SRC-004 imgadapt:19-42): UNVERIFIED."],
    "qwen_image_edit": ["Hold-plus-change: name what must stay the same (SRC-004 imgadapt:38). Camera-viewpoint edits on Qwen are UNVERIFIED."],
}


def _has_move(st):
    return bool(st["movement"])


def _render_video(st, model, lang):
    W = []
    if model == "kling" and lang == "zh":
        parts = state_zh(st)
        for mv, prefix in zip(st["movement"], _step_prefixes(st, "zh")):
            parts.append(prefix + move_zh(mv, st))
        parts += continuity_zh(st)
        if st["style"].get("visual_style"):
            parts.insert(0, "电影感")
        return "。".join(p for p in parts if p) + "。", W, None
    if model == "kling" and lang == "en":
        return _kling_en(st), W, None
    style = "h3" if model == "minimax_h3" else "generic"
    lines = []
    if st["style"].get("visual_style"):
        lines.append("Cinematic." if style != "h3" else "Cinematic style.")
    skip = style == "h3" and any(m["canonical"] in ("DOLLYIN", "DOLLYOUT") and m.get("start_position")
                                 and m["start_position"] == st["shot"]["size"] and not m.get("sequential") for m in st["movement"])
    lines += framing_en(st, style, skip_size=skip)
    lens = lens_en(st, style)
    if style == "h3":
        lines += lens
        if lens:
            W.append("H3: focal-length and gear words are nearly cosmetic (8mm rendered like 50mm, SRC-009 gear.md); the shot size carries the framing.")
    lines += angle_en(st, style)
    lines += dutch_en(st, style)
    if style != "h3":
        lines += lens
    if model != "veo":
        lines += focus_en(st, style)
        lines += composition_en(st, style)
    lines += rig_en(st, style, _has_move(st))
    move_lines = []
    for mv, prefix in zip(st["movement"], _step_prefixes(st)):
        if style == "h3" and prefix.startswith("From "):
            t0, t1 = mv["time"]
            prefix = f"For the first {t1:g} seconds, " if t0 == 0 else f"At about the {t0:g}-second mark, "
        s, w = move_video_en(mv, st, style)
        W += w
        if s and prefix:
            s[0] = prefix + (s[0][0].lower() + s[0][1:] if prefix.endswith(", ") else s[0])
        move_lines += s
    lines += move_lines
    if style == "h3":
        h3 = {"framing": framing_en(st, style, skip_size=skip), "viewpoint": angle_en(st, style) + dutch_en(st, style), "lens": lens,
              "focus": focus_en(st, style), "composition": composition_en(st, style), "rig": rig_en(st, style, _has_move(st)),
              "movements": [], "continuity": continuity_en(st, style)}
        for mv, prefix in zip(st["movement"], _step_prefixes(st)):
            Lw = []
            tgt = mv.get("target") if mv["canonical"] in ("FOLLOW", "LEAD", "TRACK", "TRACKSIDE") else None
            L, opening = _move_h3_layers(mv, st, _subj(tgt or st["shot"].get("primary_subject")), Lw)
            if style == "h3" and prefix.startswith("From "):
                t0, t1 = mv["time"]
                prefix = f"For the first {t1:g} seconds, " if t0 == 0 else f"At about the {t0:g}-second mark, "
            if prefix:   # the time prefix goes on the first sentence of the move, as in the joined text
                if opening:
                    opening = prefix + (opening[0].lower() + opening[1:] if prefix.endswith(", ") else opening)
                elif L.get("camera_core"):
                    t = L["camera_core"]["text"]
                    L["camera_core"]["text"] = prefix + (t[0].lower() + t[1:] if prefix.endswith(", ") else t)
            if opening:
                h3["framing"].append(opening)
            h3["movements"].append(L)
    if model == "veo":
        # Veo order: size/angle/lens, camera movement, then focus behaviour (SRC-005D SKILL:68-75)
        lines += focus_en(st, style)
        lines += composition_en(st, style)
    lines += continuity_en(st, style)
    if model == "veo" and not st["movement"] and st["rig"].get("stability") != "LOCKED":
        pass
    text = " ".join(x for x in lines if x)
    if style == "h3":
        for sent in re.split(r"(?<=[.!?])\s+", text):
            n = len(re.findall(r"[A-Za-z0-9'{}_-]+", sent))
            if n > 35:
                W.append(f"H3: a sentence has {n} words (>35); the plain-English rule is one idea per sentence, 35 words max (LOCAL-002 H3LAB-PLAIN-01).")
        return text, W, h3
    return text, W, None


def _kling_en(st):
    """fal Kling English: short declarative camera phrases, comma separated (SRC-003 kling.md:48-84)."""
    sh, cam = st["shot"], st["camera"]
    subj = _subj(sh.get("primary_subject"))
    p = []
    if sh["size"]:
        p.append(SIZE_SHORT_EN[sh["size"]] + f" of {subj} {SIZE_BODY_EN[sh['size']]}")
    p += [x.rstrip(".") for x in framing_en(st, "generic", skip_size=True)]
    if cam.get("position") == "FAR_ABOVE":
        p.append("bird's-eye view straight down from far above")
    elif cam.get("position") == "DRONE":
        p.append("drone view from drone height" + (" looking down at an angle" if cam.get("angle") == "HIGH" else ""))
        if cam.get("angle") and cam.get("angle") != "HIGH":
            p.append({"LOW": "low angle looking up", "VERTICAL_DOWN": "top-down, straight down",
                      "VERTICAL_UP": "worm's-eye, straight up", "LEVEL": "level"}[cam["angle"]])
    elif cam.get("height") == "EYE" and cam.get("angle") == "LEVEL":
        p.append("eye level")
    else:
        if cam.get("height") in HEIGHT_EN and HEIGHT_EN[cam["height"]]:
            p.append({"GROUND": "camera at ground level", "ANKLE": "camera at ankle height", "KNEE": "camera at knee height",
                      "HIP": "camera at waist height", "CHEST": "camera at chest height", "SHOULDER": "camera at shoulder height",
                      "ELEVATED": "elevated camera above head height", "AERIAL": "aerial, high above"}[cam["height"]])
        if cam.get("angle"):
            p.append({"LOW": "low angle looking up", "HIGH": "high angle looking down", "VERTICAL_DOWN": "top-down, straight down",
                      "VERTICAL_UP": "worm's-eye, straight up", "LEVEL": "level"}[cam["angle"]])
    if cam.get("orientation") == "DUTCH":
        p.append("Dutch angle, tilted horizon")
    L = st["lens"]
    if L.get("focal_length"):
        p.append(f"{int(L['focal_length'])}mm")
    elif L.get("lens_type"):
        p.append({"ULTRAWIDE": "ultra-wide lens", "WIDE": "wide-angle lens", "NORMAL": "normal lens",
                  "PORTRAIT": "85mm portrait lens", "TELE": "telephoto long lens"}[L["lens_type"]])
    for t in L.get("types", []):
        p.append(t.lower() + " lens")
    F = st["focus"]
    if F.get("depth_of_field"):
        p.append("shallow depth of field, background soft" if F["depth_of_field"] == "SHALLOW" else "deep focus, everything sharp")
    if F.get("target"):
        p.append({"FG": "focus stays on the foreground", "MG": "focus stays on the midground", "BG": "focus stays on the background"}[F["target"]])
    if F.get("special"):
        p.append("split diopter, near and far both sharp")
    if F.get("transition"):
        p.append(f"focus shifts from {_plane(F['transition'].get('from'))} to {_plane(F['transition'].get('to'))}")
    R = st["rig"]
    if R.get("stability") == "LOCKED" and not R.get("type") and not st["movement"]:
        p.append("locked-off static camera")
    elif R.get("type"):
        if R.get("locked") and not st["movement"]:
            p.append("locked-off static camera")
        p.append({"TRIPOD": "on a tripod", "HANDHELD": "handheld" + (", strong shake" if R.get("intensity") == "STRONG" else ""),
                  "SHOULDER": "shoulder-mounted", "STEADICAM": "steadicam", "GIMBAL": "smooth gimbal", "SLIDER": "slider",
                  "DRONE": "drone", "FPV": "FPV drone"}[R["type"]])
        if "GIMBAL" in (R.get("types") or []) and R["type"] != "GIMBAL":
            p.append("on a gimbal")
    for mv, prefix in zip(st["movement"], _step_prefixes(st)):
        c, d = mv["canonical"], mv.get("direction")
        prefix = prefix.rstrip(":, ").lower() + " " if prefix else ""
        g = _guards(mv, st)
        inplace = ", camera stays in place" if g["still"] else ""
        zplace = ", camera stays in place" if g["nomove"] else ""
        sp = {"IMPERCEPTIBLE": "barely perceptible ", "VSLOW": "very slow ", "SLOW": "slow ", "STEADY": "steady ",
              "BRISK": "brisk ", "FAST": "fast "}.get(mv.get("speed") or "", "")
        dd = DIR_EN.get(d or "", "")
        phrase = ({"DOLLYIN": f"{sp}push-in toward {subj}, camera moves forward", "DOLLYOUT": f"{sp}pull-back, camera moves backward",
                  "ZOOMIN": f"{sp}lens zoom in{zplace}", "ZOOMOUT": f"{sp}lens zoom out{zplace}",
                  "CRASHZOOM": "crash zoom", "PAN": f"{sp}pan {dd}{inplace}", "WHIPPAN": f"whip pan {dd}",
                  "TILT": f"{sp}tilt {dd}{inplace}", "ROLL": f"camera roll {dd}", "TRUCK": f"{sp}truck {dd}, camera slides sideways",
                  "PEDESTAL": f"{sp}pedestal {dd}, camera rises straight" if d == "UP" else f"{sp}pedestal {dd}, camera lowers straight",
                  "TRACK": f"{sp}tracking shot", "FOLLOW": f"{sp}tracking shot, the camera follows behind {subj}", "LEAD": f"{sp}leading shot, camera moves backward ahead of {subj}",
                  "TRACKSIDE": f"{sp}side tracking shot beside {subj}" + (f", moving toward frame-{dd}" if dd else ""), "ORBIT": f"{sp}orbit around {subj}, {subj} stays in place",
                  "CRANE": f"{sp}crane {dd}", "FLYTHROUGH": f"fly-through, the camera passes through the {(mv.get('target') or 'opening').lower()}", "DOLLYZOOM": f"dolly zoom, {subj} stays the same size",
                  "FLYOVER": "aerial flyover", "DRONEREVEAL": "aerial reveal", "STATIC": "camera holds still"}.get(c, "").strip())
        if phrase:
            p.append(prefix + phrase)
    p += [x.rstrip(".") for x in composition_en(st, "generic")]
    p += [x.rstrip(".") for x in continuity_en(st, "generic")]
    if st["style"].get("visual_style"):
        p.append("cinematic")
    return ", ".join(x for x in p if x) + "."


def _render_image(st, model, lang, edit=False):
    W = []
    if lang == "zh":
        parts = (["电影感"] if st["style"].get("visual_style") else []) + state_zh(st, image=True)
        R0 = st["rig"]
        if R0.get("locked") and R0.get("type"):
            parts.append("固定镜头，画面锁定")
        for mv in st["movement"]:
            parts.append(_move_image_zh(mv, st))
        parts += continuity_zh(st)
        body = "。".join(p for p in parts if p) + "。"
        if edit:
            return "只改变镜头视角：" + body + "人物、服装、道具、场景和姿势保持完全不变。", W
        return body, W
    lines = []
    if st["style"].get("visual_style"):
        lines.append("Cinematic still.")
    fr = framing_en(st, "generic")
    ang = angle_en(st, "generic") + dutch_en(st, "generic")
    lens = lens_en(st, "generic")
    if model == "flux":
        lines += fr[:1] + ang + lens + fr[1:]
    else:
        lines += fr + ang + lens
    lines += focus_en(st, "generic", image=True)
    lines += composition_en(st, "generic")
    R = st["rig"]
    rig_img = {"HANDHELD": "A slightly off-level, imperfect handheld framing.",
               "SHOULDER": "A slightly off-level framing at an operator's shoulder height, as if shoulder-mounted.",
               "GIMBAL": "A smooth, level, stabilised frame.",
               "STEADICAM": "A smooth, level frame with a floating feel.",
               "SLIDER": "A level frame from a short rail position.",
               "TRIPOD": "A steady, level frame from one fixed spot.",
               "DRONE": "Seen from a drone's position in the air.",
               "FPV": "Seen from an agile FPV drone's position, low and fast."}
    if R.get("type") in rig_img:
        lines.append(rig_img[R["type"]])
        if "GIMBAL" in (R.get("types") or []) and R["type"] != "GIMBAL":
            lines.append(rig_img["GIMBAL"])
        if R.get("locked"):
            lines.append("A still, locked frame.")
    elif R.get("stability") == "LOCKED" or R.get("locked"):
        lines.append("A still, locked frame.")
    for mv in st["movement"]:
        lines.append(move_image_en(mv, st, edit))
    lines += continuity_image_en(st)
    text = " ".join(x for x in lines if x)
    if TEMPORAL_VERBS.search(text):
        W.append("image text contains a motion verb: " + TEMPORAL_VERBS.search(text).group(0))
    if edit:
        text = ("Change only the camera, to this view: " + text +
                " Keep {SUBJECT}, clothing, props, scene and pose exactly the same.")
    return text, W


def _move_image_zh(mv, st):
    c, d = mv["canonical"], mv.get("direction")
    subj = _subj(st["shot"].get("primary_subject"))
    a = mv.get("amount") or {}
    deg = f"约{int(a['value'])}度" if a.get("unit") == "deg" else "一部分"
    side = {"L": "左", "R": "右"}.get(d or "", "")
    return {
        "DOLLYIN": f"机位靠近{subj}，像推镜途中的一刻，近处物体在画面边缘显得很大",
        "DOLLYOUT": f"机位离{subj}更远，像拉镜途中的一刻，画面边缘露出更多环境",
        "ZOOMIN": f"像用更长焦距拍摄，{subj}的透视扁平、背景压缩",
        "ZOOMOUT": "从同一机位以更广的视野取景",
        "CRASHZOOM": f"急速变焦落点的紧凑构图，{subj}很近",
        "PAN": f"横摇途中的一刻，{subj}偏向画面一侧",
        "WHIPPAN": "甩镜的一刻：画面有强烈的水平动态模糊",
        "TILT": "纵摇途中的一刻",
        "ROLL": "旋转镜头途中的一刻：地平线大幅倾斜",
        "TRUCK": "侧面机位，像横移途中的一刻",
        "PEDESTAL": "机位在升降到达的高度，保持水平",
        "TRACK": f"跟拍机位：与{subj}保持同样距离",
        "FOLLOW": f"背后跟拍机位：从{subj}身后看",
        "LEAD": f"前方倒退跟拍机位：从{subj}前方看，面对{subj}",
        "TRACKSIDE": f"侧面跟拍机位：从{subj}身旁看",
        "ORBIT": f"机位绕{subj}{'向' + side if side else ''}{deg}，像环绕路径上的一刻，{subj}保持居中",
        "CRANE": f"机位在摇臂的高处，看向{subj}",
        "FLYTHROUGH": "穿越的一刻：透过开口取景，开口边缘在近前景",
        "DOLLYZOOM": f"滑动变焦的一刻：{subj}大小不变，背景显得异常" + ("压缩逼近" if d == "OUT" else "拉远"),
        "FLYOVER": "飞越途中：从空中俯看地面",
        "DRONEREVEAL": f"航拍揭示的终点：{subj}在下方很小，身处广阔的场景中",
    }.get(c, "")
