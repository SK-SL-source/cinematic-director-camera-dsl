# -*- coding: utf-8 -*-
"""Cinematic Director Camera DSL — parser, alias resolver, validator, camera state, continuity.

Stdlib only. The registry (../registry/*.yaml) is the single home of meaning; this file only
implements it. Usage:

    python camera_dsl.py parse  "/MS /LOWANGLE /DOLLYIN:SLOW"
    python camera_dsl.py render "/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL" --model minimax_h3
    python camera_dsl.py render "/ORBIT:R:45" --model generic_image
    python camera_dsl.py shots  "S1: /WS /TWOSHOT /AXIS:A-B
                                 S2: /OTS:A>B /MCU /EYELINE:B>OFFL"
    python camera_dsl.py explain /PUSHIN
"""
import copy
import difflib
import json
import os
import re
import sys

sys.dont_write_bytecode = True   # keep the skill folder free of __pycache__ (checked by the release gate)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import yaml_lite  # noqa: E402

# --------------------------------------------------------------------------- registry

_REG = None


class Registry:
    def __init__(self, root=ROOT):
        r = os.path.join(root, "registry")
        reg = yaml_lite.load_file(os.path.join(r, "canonical_commands.yaml"))
        self.meta = reg["meta"]
        self.commands = reg["commands"]
        al = yaml_lite.load_file(os.path.join(r, "aliases.yaml"))
        self.aliases = al["aliases"]
        self.out_of_scope = al["out_of_scope"]
        self.cm = yaml_lite.load_file(os.path.join(r, "conflict_matrix.yaml"))
        self.compat = yaml_lite.load_file(os.path.join(r, "compatibility_matrix.yaml"))["combinations"]
        self.exclusive = set(self.cm["exclusive_dims"])
        self.channels = self.cm["channels"]
        self.move_channels = set(self.cm["move_channels"])
        self.size_ladder = self.meta["size_ladder"]
        self.speed_scale = self.meta["speed_scale"]


def registry():
    global _REG
    if _REG is None:
        _REG = Registry()
    return _REG


# fine size order (for "tighter / wider" checks); rung ladder (for cut rules) is in the registry
SIZE_ORDER = {"EWS": 1.0, "WS": 2.0, "FS": 2.3, "MFS": 2.6, "COWBOY": 2.8, "MS": 3.0, "MCU": 4.0, "CU": 5.0, "ECU": 6.0}
LENS_CLASS_RANGE = {"ULTRAWIDE": (0, 18), "WIDE": (18, 35), "NORMAL": (35, 70), "PORTRAIT": (70, 110), "TELE": (110, 10000)}

# --------------------------------------------------------------------------- argument slots

RESERVED = {"L", "R", "LEFT", "RIGHT", "UP", "DOWN", "U", "D", "IN", "OUT", "CW", "CCW", "FWD", "BACK",
            "IMPERCEPTIBLE", "VSLOW", "SLOW", "STEADY", "MED", "MEDIUM", "NORMAL", "BRISK", "FAST", "VFAST",
            "SMALL", "LARGE", "PARTIAL", "FULL", "L2R", "R2L", "TOWARD", "TOWARDS", "AWAY", "SUBTLE", "STRONG",
            "SLIGHT", "STEEP", "TIGHT", "LOOSE", "CAM", "FG", "MG", "BG"}

SLOT_RE = {
    "dir_lr": r"(L|R|LEFT|RIGHT)",
    "dir_ud": r"(UP|DOWN|U|D)",
    "dir_io": r"(IN|OUT|FWD|BACK)",
    "dir_rot": r"(CW|CCW|CLOCKWISE|COUNTERCLOCKWISE|ANTICLOCKWISE)",
    "dir_orbit": r"(L|R|LEFT|RIGHT|CW|CCW|CLOCKWISE|COUNTERCLOCKWISE|ANTICLOCKWISE)",
    "dir_reveal": r"(UP|BACK)",
    "speed": r"(IMPERCEPTIBLE|VSLOW|SLOW|STEADY|MED|MEDIUM|NORMAL|BRISK|FAST|VFAST)",
    "percent": r"\d+(\.\d+)?%",
    "degrees": r"\d+(\.\d+)?(DEG|°)?",
    "distance": r"\d+(\.\d+)?(M|CM)",
    "magnitude": r"(SMALL|MEDIUM|LARGE|PARTIAL|FULL)",
    "size_range": r"(EWS|WS|FS|MFS|COWBOY|MS|MCU|CU|ECU)>(EWS|WS|FS|MFS|COWBOY|MS|MCU|CU|ECU)",
    "relation": r"[A-Z][A-Z0-9_]*>[A-Z][A-Z0-9_]*",
    "axis": r"[A-Z][A-Z0-9_]*-[A-Z][A-Z0-9_]*",
    "screen": r"(L2R|R2L|TOWARD|TOWARDS|AWAY)",
    "subject": r"[A-Z][A-Z0-9_]*",
    "label": r"[A-Z][A-Z0-9_]*",
    "mm": r"\d+(\.\d+)?(MM)?",
    "intensity": r"(SUBTLE|STRONG|SLIGHT)",
    "angle_intensity": r"(SLIGHT|STEEP|MILD|EXTREME)",
    "level": r"(TIGHT|NORMAL|LOOSE)",
    "method": r"(MOVE|NEUTRAL|CUTAWAY|REESTABLISH|BLOCKING)",
    "kind": r"(SHAPE|MOTION|COMPOSITION)",
    "side": r"(L|R|UP|DOWN|LEFT|RIGHT)",
}
SLOT_RE = {k: re.compile("^" + v + "$") for k, v in SLOT_RE.items()}
DIR_SLOTS = {"dir_lr", "dir_ud", "dir_io", "dir_rot", "dir_orbit", "dir_reveal"}
NEEDS_DIRECTION = {"PAN", "TILT", "TRUCK", "PEDESTAL", "CRANE", "ROLL", "WHIPPAN", "TRACKSIDE", "ORBIT"}
# Movement parameters fixed by the command's own definition (registry `definition`), not given by the user and not added
# by an adapter: they are reported as DEFINITION_IMPLIED instead of UNSPECIFIED (CHANGELOG CL-031).
DEFINITION_IMPLIED = {
    "CRASHZOOM": {"speed": "FAST", "amount": "LARGE"},   # "A sudden, very fast zoom ... that snaps between framings"
    "WHIPPAN": {"speed": "FAST"},                        # "A very fast pan ..."
}


def _norm_dir(v):
    return {"LEFT": "L", "RIGHT": "R", "U": "UP", "D": "DOWN", "CLOCKWISE": "CW",
            "COUNTERCLOCKWISE": "CCW", "ANTICLOCKWISE": "CCW", "FWD": "IN", "BACK": "BACK"}.get(v, v)


def _norm_speed(v):
    return {"MED": "STEADY", "MEDIUM": "STEADY", "NORMAL": "STEADY", "VFAST": "FAST"}.get(v, v)


def _slot_value(slot, tok):
    if slot in DIR_SLOTS:
        v = _norm_dir(tok)
        if slot == "dir_io" and v == "BACK":
            v = "OUT"
        return v
    if slot == "speed":
        return _norm_speed(tok)
    if slot == "percent":
        return float(tok[:-1])
    if slot == "degrees":
        return float(re.sub(r"(DEG|°)$", "", tok))
    if slot == "distance":
        return float(tok[:-2]) / 100.0 if tok.endswith("CM") else float(tok[:-1])
    if slot == "mm":
        return float(re.sub(r"MM$", "", tok))
    if slot == "size_range":
        a, b = tok.split(">")
        return [a, b]
    if slot == "screen":
        return "TOWARD" if tok == "TOWARDS" else tok
    if slot == "side":
        return _norm_dir(tok)
    if slot == "angle_intensity":
        return {"MILD": "SLIGHT", "EXTREME": "STEEP"}.get(tok, tok)
    if slot == "intensity":
        return "SUBTLE" if tok == "SLIGHT" else tok
    return tok


# --------------------------------------------------------------------------- data classes


class Diag(dict):
    """A lint record: rule, type, commands, message, fix, evidence."""

    def __init__(self, rule, typ, message, commands=(), fix=None, evidence=(), shot=None, segment=None):
        super().__init__(rule=rule, type=typ, commands=list(commands), message=message)
        if fix:
            self["fix"] = fix
        if evidence:
            self["evidence"] = list(evidence)
        if shot is not None:
            self["shot"] = shot
        if segment is not None:
            self["segment"] = segment


SEVERITY = {"HARD_CONFLICT": "ERROR", "SEQUENTIAL_ONLY": "ERROR", "ERROR": "ERROR",
            "SOFT_CONFLICT": "WARN", "CONTEXT_DEPENDENT": "WARN", "WARNING": "WARN",
            "SPECIAL_TECHNIQUE": "INFO", "INFO": "INFO", "OUT_OF_SCOPE": "WARN",
            "VALID_COMBINATION": "OK", "VALID": "OK", "VALID_SEQUENCE": "OK"}


def _inv(canonical, raw, via, rel, args, origin="USER_SPECIFIED", priority=1):
    return {"canonical": canonical, "raw": raw, "via": via, "relationship": rel, "args": args,
            "origin": origin, "priority": priority}


# --------------------------------------------------------------------------- tokenizing

# ASCII-only lookbehind: a command may follow CJK text directly (中景/MS). Arguments take only
# DSL characters, so trailing punctuation (, . ) ，) is never swallowed; a dot needs a digit after it.
CMD_RE = re.compile(r"(?<![A-Za-z0-9_/])/([A-Za-z0-9][A-Za-z0-9_]*)((?::(?:[A-Za-z0-9_%>°+\-]|\.(?=\d))+)*)")
TIME_RE = re.compile(r"(?:(?<=\s)|^)\[?\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*s\s*\]?\s*:?", re.I)
SHOT_RE = re.compile(r"^\s*(?:S|SHOT\s*)(\d+)\s*:", re.I)
MODE_RE = re.compile(r"\bMODE:(STRICT|DIRECTOR|IMAGE|VIDEO)\b", re.I)


def normalize_width(text):
    """Full-width IME characters next to DSL tokens -> ASCII (／MS, /PAN：R, /OTS:A＞B, S1：)."""
    text = re.sub(r"／(?=[A-Za-z0-9])", "/", text)
    text = re.sub(r"(?<=[A-Za-z0-9%°])：(?=[A-Za-z0-9/\s]|$)", ":", text)
    text = re.sub(r"(?<=[A-Za-z0-9])＞(?=[A-Za-z0-9])", ">", text)
    return text


def split_shots(text):
    """Return list of (label, text, continuous_flag). Shots are separated by 'S1:' labels or CUT."""
    lines = text.replace("\r", "").split("\n")
    shots, cur, label = [], [], None
    for ln in lines:
        m = SHOT_RE.match(ln)
        if m:
            if cur or label is not None:
                shots.append((label, "\n".join(cur)))
            label, cur = "S" + m.group(1), [ln[m.end():]]
        else:
            cur.append(ln)
    if cur or label is not None:
        shots.append((label, "\n".join(cur)))
    out = []
    for lab, body in shots:
        parts = re.split(r"(?<![\w/])/?CUT\b", body)
        for i, p in enumerate(parts):
            if not p.strip() and len(parts) > 1:
                continue
            out.append((lab if i == 0 else None, p))
    if not out:
        out = [(None, text)]
    res = []
    for i, (lab, body) in enumerate(out):
        cont = bool(re.search(r"\bCONTINUOUS\b", body))
        body = re.sub(r"\bCONTINUOUS\b", " ", body)
        res.append((lab or f"S{i + 1}", body, cont))
    return res


def split_segments(body):
    """Split one shot into a global segment and time-coded or THEN-separated segments.
    Returns list of dicts: {index, t0, t1, text, global}."""
    segs = []
    marks = [(m.start(), m.end(), float(m.group(1)), float(m.group(2))) for m in TIME_RE.finditer(body)]
    if marks:
        head = body[:marks[0][0]]
        segs.append({"t0": None, "t1": None, "text": head, "global": True})
        for i, (s, e, a, b) in enumerate(marks):
            end = marks[i + 1][0] if i + 1 < len(marks) else len(body)
            segs.append({"t0": a, "t1": b, "text": body[e:end], "global": False})
    else:
        pieces = re.split(r"\bTHEN\b", body)
        if len(pieces) == 1:
            segs.append({"t0": None, "t1": None, "text": body, "global": True})
        else:
            segs.append({"t0": None, "t1": None, "text": "", "global": True})
            for p in pieces:
                segs.append({"t0": None, "t1": None, "text": p, "global": False, "then": True})
    for i, s in enumerate(segs):
        s["index"] = i
    return segs


# --------------------------------------------------------------------------- resolving


def resolve_token(name, argstr, raw, diags, loc):
    """Resolve one '/NAME:ARG...' token into canonical invocations (list)."""
    reg = registry()
    up = name.upper()
    args = [a for a in argstr.split(":") if a] if argstr else []
    args_up = [a.upper() for a in args]
    via, rel, extra, prefix = up, "canonical", None, []

    m = re.match(r"^LENS(\d+(?:\.\d+)?)$", up) or re.match(r"^(\d+(?:\.\d+)?)MM$", up)
    if up in reg.commands:
        canon = up
    elif m:
        canon, rel, prefix = "LENS", "compact_grammar", [m.group(1)]
    elif up in reg.aliases:
        a = reg.aliases[up]
        rel = a["relationship"]
        if rel == "arg_dependent":
            if not args_up or args_up[0] not in a["by_arg"]:
                diags.append(Diag("A01-ALIAS-NEEDS-ARG", "ERROR",
                                  f"/{up} needs one of: {', '.join(a['by_arg'])}.", [raw],
                                  fix=f"Write e.g. /{up}:{list(a['by_arg'])[0]}.", **loc))
                return []
            key = args_up[0]
            tgt = a["by_arg"][key]
            canon, _, fixed = tgt.partition(":")
            prefix = [fixed] if fixed else []
            args, args_up = args[1:], args_up[1:]
            wmsg = (a.get("warning_on") or {}).get(key)
            if wmsg:
                diags.append(Diag("A02-ALIAS-NOTE", "INFO", wmsg, [raw], evidence=a.get("sources", []), **loc))
        elif rel == "composite":
            out = []
            for c in a["expands"]:
                out.append(_inv(c, raw, up, rel, {}))
            return _type_args_many(out, args_up, raw, diags, loc)
        else:
            canon = a["canonical"]
            prefix = [str(x) for x in a.get("args", [])]
            if a.get("arg_template"):
                sub = args_up[0] if args_up else str(a.get("default_arg", "S"))
                prefix = [a["arg_template"].format(sub)]
                args, args_up = args[1:], args_up[1:]
        if a.get("warning"):
            diags.append(Diag("A03-AMBIGUOUS-LEGACY" if rel == "legacy_ambiguous" else "A02-ALIAS-NOTE",
                              "WARNING" if rel == "legacy_ambiguous" else "INFO", a["warning"], [raw], **loc))
    elif up in reg.out_of_scope:
        o = reg.out_of_scope[up]
        diags.append(Diag("A04-OUT-OF-SCOPE", "OUT_OF_SCOPE", f"/{up}: {o['reason']}", [raw],
                          evidence=o.get("sources", []), **loc))
        return []
    else:
        pool = list(reg.commands) + list(reg.aliases)
        sugg = difflib.get_close_matches(up, pool, n=3, cutoff=0.7)
        diags.append(Diag("A05-UNKNOWN-COMMAND", "ERROR", f"/{up} is not a known camera command.", [raw],
                          fix=("Did you mean " + ", ".join("/" + s for s in sugg) + "?") if sugg else
                          "See references/15_aliases.md for accepted names.", **loc))
        return []
    inv = _inv(canon, raw, via, rel, {})
    return _type_args_many([inv], prefix + args_up, raw, diags, loc)


def _type_args_many(invs, args_up, raw, diags, loc):
    reg = registry()
    for tok in args_up:
        placed = False
        for inv in invs:
            spec = reg.commands[inv["canonical"]].get("params") or []
            for i, slot in enumerate(spec):
                key = f"{slot}#{i}" if spec.count(slot) > 1 else slot
                if key in inv["args"]:
                    continue
                if slot in ("subject", "label") and tok in RESERVED:
                    continue
                if SLOT_RE[slot].match(tok):
                    inv["args"][key] = _slot_value(slot, tok)
                    placed = True
                    break
            if placed:
                break
        if not placed:
            spec = reg.commands[invs[0]["canonical"]].get("params") or []
            diags.append(Diag("A06-BAD-ARGUMENT", "ERROR",
                              f"'{tok}' is not a valid argument for /{invs[0]['canonical']}"
                              + (f" (expects {', '.join(spec)})." if spec else " (takes no arguments)."),
                              [raw], fix="See registry meta.param_slots for argument formats.", **loc))
    return invs


def parse_segment_text(text, diags, loc):
    invs = []
    for m in CMD_RE.finditer(text):
        raw = m.group(0)
        name, argstr = m.group(1), m.group(2)[1:] if m.group(2) else ""
        for inv in resolve_token(name, argstr, raw, diags, loc):
            invs.append(inv)
    free = CMD_RE.sub(" ", text)
    free = MODE_RE.sub(" ", free)
    free = re.sub(r"\b(THEN|CUT|CONTINUOUS)\b", " ", free)
    free = re.sub(r"[;,]+", " ", free)
    free = " ".join(free.split())
    if not re.search(r"[^\W_]", free):
        free = ""  # only punctuation was left around the commands
    return invs, free


# --------------------------------------------------------------------------- writes


def _dir_of(inv):
    for k, v in inv["args"].items():
        if k.split("#")[0] in DIR_SLOTS:
            return v
    return None


def writes_of(inv):
    """Return (core, defaults) dicts of dimension -> value for an invocation."""
    reg = registry()
    c = reg.commands[inv["canonical"]]
    a = inv["args"]
    d = _dir_of(inv)
    if inv["canonical"] == "ORBIT" and d in ("CW", "CCW"):
        d = "L" if d == "CW" else "R"
    core, defaults = {}, {}
    dw = c.get("dir_writes")
    if dw:
        key = d if d in dw else c.get("default_dir")
        core.update(dw.get(key, {}))
    for k, v in (c.get("writes") or {}).items():
        v = str(v)
        if "$dir" in v:
            v = v.replace("$dir", d) if d else ("THIRD" if v.startswith("THIRD") else "UNSPECIFIED")
            v = v.replace("THIRD_", "THIRD_") if d else v
        elif v == "$mm":
            v = a.get("mm")
        elif v == "$relation":
            v = a.get("relation", "UNSPECIFIED")
            if k == "cont.eyeline":
                src = v.split(">")[0] if ">" in v else "S"
                k = f"cont.eyeline.{src}"
        elif v.startswith("$"):
            v = a.get(v[1:], "UNSPECIFIED")
        core[k] = v
    for k, v in (c.get("defaults") or {}).items():
        defaults[k] = str(v)
    return core, defaults


def kind_of(inv):
    return registry().commands[inv["canonical"]]["kind"]


def specializes(a, b):
    """True if invocation a refines invocation b (b is the general command)."""
    reg = registry()
    sp = reg.commands[a["canonical"]].get("specializes")
    if sp != b["canonical"]:
        return False
    ca, _ = writes_of(a)
    cb, _ = writes_of(b)
    for ch in reg.channels:
        if ch in ca and ch in cb and "UNSPECIFIED" not in (ca[ch], cb[ch]) and ch != "track.mode" and ca[ch] != cb[ch]:
            return False
    return True


# --------------------------------------------------------------------------- pair logic


def _pair_rule(a, b):
    reg = registry()
    na, nb = a["canonical"], b["canonical"]
    for r in reg.cm["pair_rules"]:
        if "pair" in r:
            p = r["pair"]
            if (na == p[0] and nb == p[1]) or (na == p[1] and nb == p[0]):
                return r
        else:
            A, B = r["pair_any_a"], r["pair_any_b"]
            if (na in A and nb in B) or (nb in A and na in B):
                return r
    return None


def _group_rule(a, b):
    reg = registry()
    for r in reg.cm["group_rules"]:
        for x, y in ((a, b), (b, a)):
            if x["canonical"] != r["a"]:
                continue
            if "b_kind" in r and kind_of(y) == r["b_kind"]:
                return r
            if "b_writes_any" in r:
                cy, _ = writes_of(y)
                if any(k in cy for k in r["b_writes_any"]):
                    return r
    return None


def classify_pair(a, b):
    """Return (type, rule_id, message, fix, evidence) for two simultaneous invocations."""
    reg = registry()
    if a["canonical"] == b["canonical"]:
        ca, _ = writes_of(a)
        cb, _ = writes_of(b)
        opp = [ch for ch in reg.channels if ch in ca and ch in cb and ca[ch] != cb[ch]
               and "UNSPECIFIED" not in (ca[ch], cb[ch])]
        if opp:
            return ("SEQUENTIAL_ONLY", "CH-OPPOSITE", f"/{a['canonical']} in opposite directions at the same time.",
                    "Put them in sequence (THEN or time codes).", [])
        sa, sb = a["args"].get("speed"), b["args"].get("speed")
        if sa and sb and sa != sb:
            return ("SOFT_CONFLICT", "R11-SPEED-MISMATCH", f"/{a['canonical']} given two speeds ({sa}, {sb}).",
                    "Keep one speed.", ["SRC-004"])
        excl = [d for d in reg.exclusive if d in ca and d in cb and ca[d] != cb[d]
                and "UNSPECIFIED" not in (ca[d], cb[d])]
        if excl:
            return ("HARD_CONFLICT", "DIM-EXCLUSIVE", f"/{a['canonical']} given twice with different values ({', '.join(excl)}).",
                    "Keep one.", [])
        return ("INFO", "R12-DUPLICATE", f"/{a['canonical']} given twice; merged.", None, [])
    if specializes(a, b) or specializes(b, a):
        spec, gen = (a, b) if specializes(a, b) else (b, a)
        sg = gen["args"].get("speed")
        if spec["canonical"] == "WHIPPAN" and sg in ("IMPERCEPTIBLE", "VSLOW", "SLOW", "STEADY"):
            return ("SOFT_CONFLICT", "R11-SPEED-MISMATCH", "A whip pan is very fast; the pan was given a slow speed.",
                    "Drop the pan speed or use a normal /PAN.", ["SRC-004"])
        return ("INFO", "R12-DUPLICATE", f"/{spec['canonical']} refines /{gen['canonical']}; merged.", None, [])
    r = _pair_rule(a, b)
    if r and r["type"] in ("SPECIAL_TECHNIQUE", "HARD_CONFLICT"):
        return (r["type"], r["id"], r.get("message", ""), r.get("fix"), r.get("evidence", []))
    ca0, _ = writes_of(a)
    cb0, _ = writes_of(b)
    opp0 = [ch for ch in reg.channels if ch in ca0 and ch in cb0 and ch != "track.mode" and ca0[ch] != cb0[ch]
            and "UNSPECIFIED" not in (ca0[ch], cb0[ch])]
    if opp0:
        return ("SEQUENTIAL_ONLY", "CH-OPPOSITE",
                f"/{a['canonical']} and /{b['canonical']} drive {', '.join(opp0)} in opposite directions at the same time.",
                "Put them in sequence (THEN or time codes).", ["SRC-002 camera:180"])
    if r:
        return (r["type"], r["id"], r.get("message", ""), r.get("fix"), r.get("evidence", []))
    g = _group_rule(a, b)
    if g:
        return (g["type"], g["id"], g.get("message", ""), g.get("fix"), g.get("evidence", []))
    ca, _ = writes_of(a)
    cb, _ = writes_of(b)
    excl = [d for d in sorted(reg.exclusive) if d in ca and d in cb and ca[d] != cb[d]
            and "UNSPECIFIED" not in (ca[d], cb[d]) and d not in reg.channels]
    if excl:
        return ("HARD_CONFLICT", "DIM-EXCLUSIVE",
                f"/{a['canonical']} and /{b['canonical']} set {', '.join(excl)} to different values "
                f"({', '.join(str(ca[d]) + ' vs ' + str(cb[d]) for d in excl)}).",
                "Keep one of them.", [])
    chans = [ch for ch in reg.channels if ch in ca and ch in cb]
    opp = [ch for ch in chans if ca[ch] != cb[ch] and "UNSPECIFIED" not in (ca[ch], cb[ch])]
    if opp:
        if "track.mode" in opp:
            return ("HARD_CONFLICT", "DIM-EXCLUSIVE",
                    f"/{a['canonical']} and /{b['canonical']} put the camera on different sides of the subject.",
                    "Keep one tracking position.", ["SRC-001"])
        return ("SEQUENTIAL_ONLY", "CH-OPPOSITE",
                f"/{a['canonical']} and /{b['canonical']} drive {', '.join(opp)} in opposite directions at the same time.",
                "Put them in sequence (THEN or time codes).", ["SRC-002 camera:180"])
    if chans:
        return ("INFO", "CH-REDUNDANT", f"/{a['canonical']} and /{b['canonical']} drive the same movement ({', '.join(chans)}); merged.",
                None, [])
    if kind_of(a) == "movement" and kind_of(b) == "movement":
        return ("VALID_COMBINATION", "OK", "Different mechanisms.", None, [])
    return ("VALID", "OK", "", None, [])


# --------------------------------------------------------------------------- segment rules


def _args_of(invs, name):
    return [i for i in invs if i["canonical"] == name]


def segment_rules(invs, static_size, diags, loc):
    reg = registry()
    names = {i["canonical"] for i in invs}
    # R01 / R02 size ranges
    for i in invs:
        rng = i["args"].get("size_range")
        if not rng:
            continue
        s, e = rng
        if static_size and static_size != s:
            diags.append(Diag("R01-SIZE-RANGE-START", "HARD_CONFLICT",
                              f"/{i['canonical']} starts at {s} but the shot size is {static_size}.", [i["raw"]],
                              fix=f"Use /{i['canonical']}:{static_size}>{e} or drop the separate size.",
                              evidence=["LOCAL-002", "SRC-009"], **loc))
        c = i["canonical"]
        d = _dir_of(i)
        tighten = c in ("DOLLYIN", "ZOOMIN", "FLYTHROUGH") or (c == "CRASHZOOM" and d != "OUT")
        widen = c in ("DOLLYOUT", "ZOOMOUT") or (c == "CRASHZOOM" and d == "OUT")
        if SIZE_ORDER[s] == SIZE_ORDER[e]:
            diags.append(Diag("R02-SIZE-RANGE-DIRECTION", "SOFT_CONFLICT",
                              f"/{c} starts and ends at {s}: no visible change.", [i["raw"]], **loc))
        elif tighten and SIZE_ORDER[e] < SIZE_ORDER[s]:
            diags.append(Diag("R02-SIZE-RANGE-DIRECTION", "HARD_CONFLICT",
                              f"/{c} moves closer but its range {s}>{e} gets wider.", [i["raw"]],
                              fix=f"Use /DOLLYOUT or reverse the range ({e}>{s}).", evidence=["SRC-002", "SRC-009"], **loc))
        elif widen and SIZE_ORDER[e] > SIZE_ORDER[s]:
            diags.append(Diag("R02-SIZE-RANGE-DIRECTION", "HARD_CONFLICT",
                              f"/{c} moves away but its range {s}>{e} gets tighter.", [i["raw"]],
                              fix=f"Use /DOLLYIN or reverse the range ({e}>{s}).", evidence=["SRC-002", "SRC-009"], **loc))
    # R03 lens class
    lenses = _args_of(invs, "LENS")
    classes = [(i, writes_of(i)[0].get("lens.focal_class")) for i in invs if writes_of(i)[0].get("lens.focal_class")]
    for L in lenses:
        mm = L["args"].get("mm")
        for ci, cls in classes:
            lo, hi = LENS_CLASS_RANGE[cls]
            if mm is not None and not (lo <= mm <= hi):
                diags.append(Diag("R03-LENS-CLASS-RANGE", "HARD_CONFLICT",
                                  f"{int(mm)}mm is outside the {cls} class ({lo}-{hi if hi < 10000 else '...'} mm).",
                                  [L["raw"], ci["raw"]], fix="Keep the number or the class.",
                                  evidence=["SRC-004", "SRC-003"], **loc))
    # R04 thirds / lookroom
    for t in _args_of(invs, "THIRDS"):
        for lr in _args_of(invs, "LOOKROOM"):
            a, b = t["args"].get("dir_lr"), lr["args"].get("dir_lr")
            if a and b and a == b:
                diags.append(Diag("R04-THIRDS-LOOKROOM", "HARD_CONFLICT",
                                  f"Subject on the {a} third cannot have its open space on the {b} side.",
                                  [t["raw"], lr["raw"]], fix=f"Use /LOOKROOM:{'R' if a == 'L' else 'L'}.",
                                  evidence=["SRC-004"], **loc))
    # R05 tracking vs screen direction
    for sc in _args_of(invs, "SCREEN"):
        s = sc["args"].get("screen")
        for tr in invs:
            c, d = tr["canonical"], _dir_of(tr)
            bad = ((c == "TRACKSIDE" and d == "R" and s == "R2L") or (c == "TRACKSIDE" and d == "L" and s == "L2R")
                   or (c == "FOLLOW" and s == "TOWARD") or (c == "LEAD" and s == "AWAY"))
            if bad:
                diags.append(Diag("R05-TRACK-SCREEN", "HARD_CONFLICT",
                                  f"/{c}{':' + d if d else ''} contradicts screen direction {s}.", [tr["raw"], sc["raw"]],
                                  evidence=["SRC-004", "SRC-001"], **loc))
    # R06 POV owner looking into the lens
    for p in _args_of(invs, "POV"):
        owner = p["args"].get("subject")
        for e in _args_of(invs, "EYELINE"):
            rel = e["args"].get("relation", "")
            if owner and rel == f"{owner}>CAM":
                diags.append(Diag("R06-POV-OWNER-LOOKCAM", "HARD_CONFLICT",
                                  f"In /POV:{owner}, {owner} is the camera and cannot look into the lens.",
                                  [p["raw"], e["raw"]], fix="Another subject can look into the lens (they look at the POV owner).",
                                  evidence=["SRC-002", "SRC-005B"], **loc))
    # R08 unspecified direction
    for i in invs:
        if i["canonical"] in NEEDS_DIRECTION and _dir_of(i) is None:
            diags.append(Diag("R08-UNSPECIFIED-DIRECTION", "WARNING",
                              f"/{i['canonical']} has no direction; the model will choose.", [i["raw"]],
                              fix=f"Add a direction, e.g. /{i['canonical']}:{'R' if i['canonical'] not in ('TILT', 'PEDESTAL', 'CRANE') else 'UP'}.",
                              evidence=["SRC-004", "SRC-012"], **loc))
    # R07 motion count
    chans = set()
    for i in invs:
        core, _ = writes_of(i)
        chans |= {k for k in core if k in reg.move_channels}
    if len(chans) >= 3:
        diags.append(Diag("R07-MOTION-OVERLOAD", "SOFT_CONFLICT",
                          f"{len(chans)} camera moves at the same time ({', '.join(sorted(chans))}).",
                          [i["raw"] for i in invs if kind_of(i) == "movement"],
                          fix="Most sources advise one dominant move (SRC-002, SRC-004); SRC-009 measured complementary stacks working on H3. Keep it only if the moves describe one coherent path.",
                          evidence=["SRC-002", "SRC-004", "SRC-010", "SRC-009"], **loc))
    return chans


# --------------------------------------------------------------------------- validation core


def validate_window(invs, diags, loc):
    """Check all pairs of simultaneous invocations. Returns the merged, normalized invocation list."""
    reg = registry()
    work = list(invs)
    # special techniques first (DOLLYIN + ZOOMOUT -> DOLLYZOOM:IN)
    changed = True
    while changed:
        changed = False
        for i in range(len(work)):
            for j in range(i + 1, len(work)):
                r = _pair_rule(work[i], work[j])
                if r and r["type"] == "SPECIAL_TECHNIQUE":
                    tgt, _, d = r["yields"].partition(":")
                    sp = work[i]["args"].get("speed") or work[j]["args"].get("speed")
                    new = _inv(tgt, f"{work[i]['raw']} {work[j]['raw']}", tgt, "special_technique",
                               {"dir_io": d} if d else {})
                    if sp:
                        new["args"]["speed"] = sp
                    new["origin"] = min(work[i]["origin"], work[j]["origin"])
                    diags.append(Diag(r["id"], "SPECIAL_TECHNIQUE", r.get("message", ""),
                                      [work[i]["raw"], work[j]["raw"]], evidence=r.get("evidence", []), **loc))
                    work = [w for k, w in enumerate(work) if k not in (i, j)] + [new]
                    changed = True
                    break
            if changed:
                break
    keep = [True] * len(work)
    pairs = []
    for i in range(len(work)):
        for j in range(i + 1, len(work)):
            typ, rid, msg, fix, ev = classify_pair(work[i], work[j])
            pairs.append((i, j, typ))
            if typ in ("VALID", "VALID_COMBINATION", "OK"):
                continue
            if typ == "INFO":
                a, b = work[i], work[j]
                drop = j
                if specializes(b, a):
                    drop = i
                keep[drop] = False
                diags.append(Diag(rid, "INFO", msg, [a["raw"], b["raw"]], **loc))
                continue
            diags.append(Diag(rid, typ, msg, [work[i]["raw"], work[j]["raw"]], fix=fix, evidence=ev, **loc))
    merged = [w for k, w in enumerate(work) if keep[k]]
    return merged, pairs


def _static_size(invs):
    for i in invs:
        c, _ = writes_of(i)
        if "shot.size" in c:
            return c["shot.size"]
    return None


def analyze(text, layers=None, mode=None):
    """Parse + validate a DSL string (one or more shots). Returns a result dict.

    layers: optional extra intent layers [(priority, origin_label, dsl_text), ...] merged under the
    explicit DSL (priority 1). Lower priority never overrides higher (spec section 29)."""
    reg = registry()
    source = text
    text = normalize_width(text)
    mm = MODE_RE.findall(text)
    modes = {m.upper() for m in mm}
    if mode:
        modes.add(mode.upper())
    pre_diags = []
    if layers and any(o == "DIRECTOR_SUGGESTED" for _, o, _ in layers):
        if "STRICT" in modes:  # explicit STRICT: suggestions are not allowed (spec sections 26-27)
            pre_diags.append(Diag("M01-DIRECTOR-IN-STRICT", "WARNING",
                                  "MODE:STRICT is set, so the director suggestions were not applied.",
                                  [v for _, o, v in layers if o == "DIRECTOR_SUGGESTED"],
                                  fix="Remove MODE:STRICT to accept suggestions (they stay labelled DIRECTOR_SUGGESTED).",
                                  evidence=["spec section 26", "spec section 27"]))
            layers = [x for x in layers if x[1] != "DIRECTOR_SUGGESTED"]
        else:  # passing a director layer is the request for Director Mode
            modes.add("DIRECTOR")
    if "DIRECTOR" not in modes:
        modes.add("STRICT")
    if "IMAGE" not in modes:
        modes.add("VIDEO")
    result = {"input": source, "modes": sorted(modes), "shots": [], "diagnostics": []}
    result["strict"] = "DIRECTOR" not in modes
    for si, (label, body, cont) in enumerate(split_shots(text)):
        shot = {"label": label, "continuous": cont, "segments": [], "free_text": []}
        diags = []
        segs = split_segments(body)
        for seg in segs:
            loc = {"shot": label, "segment": seg["index"]}
            invs, free = parse_segment_text(seg["text"], diags, loc)
            if free:
                shot["free_text"].append(free)
            seg["invocations"] = invs
        # intent layers (only for single-segment shots; applied to the global segment)
        if layers:
            _apply_layers(segs, layers, diags, label)
        # validate: global + each segment; overlapping timed segments are simultaneous
        glob = segs[0]["invocations"]
        timed = segs[1:]
        if not timed:
            loc = {"shot": label, "segment": 0}
            merged, _ = validate_window(glob, diags, loc)
            segment_rules(merged, _static_size(merged), diags, loc)
            segs[0]["resolved"] = merged
        else:
            gm, _ = validate_window(glob, diags, {"shot": label, "segment": 0})
            segs[0]["resolved"] = gm
            for s in timed:
                loc = {"shot": label, "segment": s["index"]}
                window = gm + s["invocations"]
                merged, _ = validate_window(window, [], loc)  # pairwise messages reported below
                local_diags = []
                validate_window(window, local_diags, loc)
                # keep only diagnostics that involve this segment's own commands
                own = {i["raw"] for i in s["invocations"]}
                for d in local_diags:
                    if any(c in own for c in d["commands"]) or any(any(o in c for o in own) for c in d["commands"]):
                        diags.append(d)
                segment_rules(merged, _static_size(merged), diags, loc)
                s["resolved"] = [m for m in merged if m in s["invocations"] or m["relationship"] == "special_technique"]
            _sequence_rules(segs, diags, label)
        shot["segments"] = [{"index": s["index"], "t0": s["t0"], "t1": s["t1"], "global": s["global"],
                             "commands": [_public_inv(i) for i in s.get("resolved", [])]} for s in segs]
        shot["state"] = build_state(segs, cont, label)
        shot["diagnostics"] = _dedupe(diags)
        shot["status"] = _status(shot["diagnostics"], has_sequence=bool(timed))
        result["shots"].append(shot)
    if len(result["shots"]) > 1:
        result["diagnostics"] = continuity_check(result["shots"])
    result["diagnostics"] = pre_diags + result["diagnostics"]
    all_d = result["diagnostics"] + [d for s in result["shots"] for d in s["diagnostics"]]
    result["status"] = _status(all_d, has_sequence=any(len(s["segments"]) > 1 for s in result["shots"]))
    return result


def _apply_layers(segs, layers, diags, label):
    """Merge lower-priority intent layers into the global segment without overriding higher ones."""
    top = segs[0]["invocations"] + [i for s in segs[1:] for i in s["invocations"]]
    for prio, origin, dsl in sorted(layers, key=lambda x: x[0]):
        ld = []
        invs, _ = parse_segment_text(dsl, ld, {"shot": label, "segment": 0})
        for inv in invs:
            inv["origin"], inv["priority"] = origin, prio
            clash = None
            for t in top:
                typ, rid, msg, fix, ev = classify_pair(t, inv)
                if typ in ("HARD_CONFLICT", "SEQUENTIAL_ONLY", "SOFT_CONFLICT", "INFO") or t["canonical"] == inv["canonical"]:
                    clash = (t, typ)
                    break
            if clash:
                diags.append(Diag("P00-OVERRIDDEN", "INFO",
                                  f"{origin} {inv['raw']} not applied: {clash[0]['origin']} {clash[0]['raw']} has priority.",
                                  [inv["raw"], clash[0]["raw"]], evidence=["spec section 29"], shot=label))
                continue
            segs[0]["invocations"].append(inv)
            top.append(inv)


def _sequence_rules(segs, diags, label):
    reg = registry()
    timed = [s for s in segs[1:]]
    # overlapping time windows are simultaneous
    for i in range(len(timed)):
        for j in range(i + 1, len(timed)):
            a, b = timed[i], timed[j]
            if a["t0"] is not None and b["t0"] is not None and a["t0"] < b["t1"] and b["t0"] < a["t1"]:
                loc = {"shot": label, "segment": b["index"]}
                for x in a["invocations"]:
                    for y in b["invocations"]:
                        typ, rid, msg, fix, ev = classify_pair(x, y)
                        if typ not in ("VALID", "VALID_COMBINATION", "OK", "INFO"):
                            diags.append(Diag(rid, typ, "Overlapping time windows: " + msg, [x["raw"], y["raw"]],
                                              fix=fix, evidence=ev, **loc))
            if a["t1"] is not None and b["t0"] is not None and b["t0"] < a["t0"]:
                diags.append(Diag("S01-TIME-ORDER", "ERROR", "Time segments must be in increasing order.",
                                  [], shot=label, segment=b["index"]))
    # R09 state jumps between consecutive segments
    glob = segs[0]["invocations"]

    def dims(seg):
        out = {}
        for inv in glob + seg["invocations"]:
            c, _ = writes_of(inv)
            for k in ("shot.size", "camera.pitch", "camera.height"):
                if k in c:
                    out[k] = c[k]
        return out

    def chans(seg):
        s = set()
        for inv in seg["invocations"]:
            c, _ = writes_of(inv)
            s |= set(c)
        return s

    causes = {"shot.size": {"move.z", "zoom.dir", "track.mode"}, "camera.pitch": {"rot.pitch", "move.y", "orbit.dir"},
              "camera.height": {"move.y"}}
    for prev, nxt in zip(timed, timed[1:]):
        dp, dn = dims(prev), dims(nxt)
        moved = chans(prev) | chans(nxt)
        for k in dp:
            if k in dn and dp[k] != dn[k] and not (causes[k] & moved):
                diags.append(Diag("R09-STATE-JUMP", "CONTEXT_DEPENDENT",
                                  f"{k} changes from {dp[k]} to {dn[k]} between segments with no move that could cause it.",
                                  [], fix="Add the move (e.g. /DOLLYIN, /TILT) or split into two shots with a cut.",
                                  evidence=["SRC-002", "SRC-009"], shot=label, segment=nxt["index"]))
    moving = [s for s in timed if any(kind_of(i) == "movement" for i in s["invocations"])]
    if len(moving) >= 2:
        diags.append(Diag("R10-SEQUENCE-IN-ONE-CLIP", "WARNING",
                          "Several moves one after another inside one generated clip. Valid DSL; some models blend them.",
                          [], fix="If the model blends them, split into two clips joined on a cut (SRC-004 failure-modes F6).",
                          evidence=["SRC-002", "SRC-004"], shot=label))


def _dedupe(diags):
    seen, out = set(), []
    for d in diags:
        key = (d["rule"], d["type"], tuple(sorted(d["commands"])), d["message"])
        if key in seen:
            continue
        seen.add(key)
        out.append(d)
    return out


def _status(diags, has_sequence=False):
    sev = [SEVERITY.get(d["type"], "WARN") for d in diags]
    if "ERROR" in sev:
        return "ERROR"
    if "WARN" in sev:
        return "WARN"
    return "OK"


def _public_inv(i):
    return {"canonical": i["canonical"], "raw": i["raw"], "via": i["via"], "relationship": i["relationship"],
            "args": i["args"], "origin": i["origin"]}


# --------------------------------------------------------------------------- camera state


def build_state(segs, continuous=False, label=None):
    """Structured camera state (schemas/camera_dsl_schema.yaml)."""
    reg = registry()
    st = {
        "shot": {"size": None, "framing": [], "subject_count": None, "primary_subject": None,
                 "foreground_subject": None, "viewpoint": None, "pov_owner": None, "ots_variant": None,
                 "orientation": None, "function": None, "function_target": None},
        "camera": {"position": None, "height": None, "angle": None, "angle_intensity": None,
                   "orientation": "LEVEL", "dutch": None},
        "movement": [],
        "rig": {"type": None, "types": [], "stability": None, "intensity": None, "locked": False},
        "lens": {"focal_length": None, "lens_type": None, "types": []},
        "focus": {"target": None, "depth_of_field": None, "transition": None, "special": None},
        "composition": {"placement": None, "foreground": None, "midground": None, "background": None,
                        "depth_layers": False, "symmetry": False, "negative_space": None, "headroom": None,
                        "lookroom": None, "leading_lines": False, "frame_in_frame": False},
        "continuity": {"axis": None, "screen_direction": None, "eyeline": [], "relation_to_previous_shot": [],
                       "cross_axis": None, "continuous": continuous},
        "style": {"visual_style": None},
        "constraints": {"preserve_story": True, "preserve_character": True, "preserve_clothing": True,
                        "preserve_scene": True, "preserve_props": True, "preserve_action": True},
        "meta": {"origins": {}, "unspecified": [], "definitional": [], "label": label},
    }
    glob = segs[0].get("resolved", segs[0].get("invocations", []))

    def setv(path, val, origin):
        sec, key = path
        st[sec][key] = val
        st["meta"]["origins"][f"{sec}.{key}"] = origin

    all_static = list(glob) + [i for s in segs[1:] for i in s.get("resolved", s.get("invocations", [])) if kind_of(i) != "movement"]
    applied_core = set()
    for inv in all_static + [i for s in segs for i in s.get("resolved", s.get("invocations", [])) if kind_of(i) == "movement"]:
        core, _ = writes_of(inv)
        applied_core |= set(core)
    # /STATIC inside a sequence segment is a hold phase (a movement step), not a lock for the whole shot
    seq_static = {id(i) for s in segs[1:] for i in s.get("resolved", s.get("invocations", [])) if i["canonical"] == "STATIC"}
    for inv in glob + [i for s in segs[1:] for i in s.get("resolved", s.get("invocations", []))]:
        if id(inv) in seq_static:
            continue
        c, a, o = inv["canonical"], inv["args"], inv["origin"]
        core, defaults = writes_of(inv)
        for k, v in defaults.items():
            if k not in applied_core:
                st["meta"]["definitional"].append({"from": c, "dimension": k, "value": v})
        cat = reg.commands[c]["category"]
        if cat == "SHOT_SIZE" and st["shot"]["size"] is None:
            setv(("shot", "size"), c, o)
        elif cat == "SUBJECT_FRAMING":
            st["shot"]["framing"].append(c)
            if "shot.subject_count" in core:
                setv(("shot", "subject_count"), core["shot.subject_count"], o)
            if c in ("OTS", "DIRTYOTS", "CLEANOTS"):
                setv(("shot", "viewpoint"), "OTS", o)
                rel = a.get("relation")
                if rel:
                    fg, pr = rel.split(">")
                    st["shot"]["foreground_subject"], st["shot"]["primary_subject"] = fg, pr
                st["shot"]["ots_variant"] = core.get("shot.ots_variant", "DIRTY")
            if c == "POV":
                setv(("shot", "viewpoint"), "POV", o)
                st["shot"]["pov_owner"] = a.get("subject")
            if "subject.orientation" in core:
                setv(("shot", "orientation"), core["subject.orientation"], o)
            if c == "SINGLE" and a.get("subject"):
                st["shot"]["primary_subject"] = a.get("subject")
        elif cat == "CAMERA_ANGLE":
            if "camera.pitch" in core:
                setv(("camera", "angle"), core["camera.pitch"], o)
            if "camera.height" in core:
                setv(("camera", "height"), core["camera.height"], o)
            if c == "BIRDSEYE":
                st["camera"]["position"] = "FAR_ABOVE"
            if c == "DUTCH":
                st["camera"]["orientation"] = "DUTCH"
                st["camera"]["dutch"] = {"direction": a.get("dir_lr"), "degrees": a.get("degrees")}
            if c in ("LOWANGLE", "HIGHANGLE") and a.get("angle_intensity"):
                st["camera"]["angle_intensity"] = a["angle_intensity"]
            if c == "WORMSEYE" and "camera.height" not in applied_core:
                st["camera"]["height"] = "GROUND"
                st["meta"]["origins"]["camera.height"] = "DEFINITIONAL"
        elif cat == "CAMERA_HEIGHT":
            setv(("camera", "height"), core["camera.height"], o)
        elif cat == "AERIAL" and c == "DRONEVIEW":
            setv(("camera", "height"), "AERIAL", o)
            st["camera"]["position"] = "DRONE"
            if "camera.pitch" not in applied_core:
                st["camera"]["angle"] = "HIGH"
                st["meta"]["origins"]["camera.angle"] = "DEFINITIONAL"
        elif cat == "CAMERA_RIG":
            if c == "STATIC":
                st["rig"]["locked"] = True
                if st["rig"]["stability"] is None:
                    setv(("rig", "stability"), "LOCKED", o)
            else:
                rt = core.get("rig.type")
                st["rig"]["types"].append(rt)
                if st["rig"]["type"] in (None, "GIMBAL") or (rt in ("DRONE", "FPV") and st["rig"]["type"] != "FPV"):
                    if not (st["rig"]["type"] == "FPV" and rt == "DRONE"):
                        setv(("rig", "type"), rt, o)
                        st["rig"]["stability"] = core.get("rig.stability")
                if a.get("intensity"):
                    st["rig"]["intensity"] = a["intensity"]
        elif cat == "LENS":
            if c == "LENS":
                setv(("lens", "focal_length"), a.get("mm"), o)
            if "lens.focal_class" in core:
                setv(("lens", "lens_type"), core["lens.focal_class"], o)
            if c in ("MACRO", "FISHEYE", "ANAMORPHIC"):
                st["lens"]["types"].append(c)
        elif cat == "FOCUS":
            if c == "SHALLOW":
                setv(("focus", "depth_of_field"), "SHALLOW", o)
            elif c == "DEEPFOCUS":
                setv(("focus", "depth_of_field"), "DEEP", o)
            elif c in ("FGFOCUS", "MGFOCUS", "BGFOCUS"):
                setv(("focus", "target"), c[:2], o)
            elif c == "SPLITDIOPTER":
                setv(("focus", "special"), "SPLIT_DIOPTER", o)
            elif c == "RACKFOCUS":
                rel = a.get("relation", "")
                fr, _, to = rel.partition(">")
                st["focus"]["transition"] = {"type": "RACK", "from": fr or None, "to": to or None,
                                             "speed": a.get("speed")}
                st["meta"]["origins"]["focus.transition"] = o
        elif cat == "COMPOSITION":
            comp = st["composition"]
            if c == "CENTER":
                comp["placement"] = "CENTER"
            elif c == "THIRDS":
                comp["placement"] = "THIRD_" + a["dir_lr"] if a.get("dir_lr") else "THIRD"
            elif c == "SYMMETRY":
                comp["symmetry"] = True
            elif c == "NEGSPACE":
                comp["negative_space"] = a.get("side") or True
            elif c == "HEADROOM":
                comp["headroom"] = a.get("level", "NORMAL")
            elif c == "LOOKROOM":
                comp["lookroom"] = a.get("dir_lr") or True
            elif c == "LEADLINES":
                comp["leading_lines"] = True
            elif c == "FRAMEINFRAME":
                comp["frame_in_frame"] = True
            elif c == "FGLAYER":
                comp["foreground"] = a.get("label") or "FOREGROUND_ELEMENT"
            elif c == "DEEPSTAGING":
                comp["depth_layers"] = True
            st["meta"]["origins"][f"composition.{c.lower()}"] = o
        elif cat == "CONTINUITY":
            cont = st["continuity"]
            if c == "AXIS":
                cont["axis"] = a.get("axis")
            elif c == "CROSSAXIS":
                cont["cross_axis"] = a.get("method", "UNSPECIFIED")
            elif c == "EYELINE":
                cont["eyeline"].append(a.get("relation", "S>UNSPECIFIED"))
            elif c == "SCREEN":
                cont["screen_direction"] = a.get("screen")
            elif c in ("SRS", "MATCHACTION", "MATCHCUT"):
                cont["relation_to_previous_shot"].append({"type": c, "value": a.get("relation") or a.get("kind") or a.get("label")})
            elif c in ("REACTION", "INSERT", "CUTAWAY"):
                st["shot"]["function"] = c
                st["shot"]["function_target"] = a.get("subject") or a.get("label")
        elif cat == "STYLE":
            st["style"]["visual_style"] = "cinematic"
    # movements (in time order)
    for s in segs:
        for inv in s.get("resolved", s.get("invocations", [])):
            if id(inv) in seq_static:
                st["movement"].append({"type": "hold", "canonical": "STATIC", "direction": None, "amount": None, "speed": None,
                                       "duration": (s["t1"] - s["t0"]) if s["t0"] is not None else None,
                                       "time": [s["t0"], s["t1"]] if s["t0"] is not None else None,
                                       "start_position": None, "end_position": None, "target": None,
                                       "origin": inv["origin"], "sequential": True, "step": s["index"]})
                continue
            if kind_of(inv) != "movement":
                continue
            c, a = inv["canonical"], inv["args"]
            d = _dir_of(inv)
            if c == "ORBIT" and d in ("CW", "CCW"):
                d = "L" if d == "CW" else "R"
            if c in ("DOLLYZOOM", "CRASHZOOM", "DRONEREVEAL") and not d:
                d = reg.commands[c].get("default_dir")
            rng = a.get("size_range")
            mv = {"type": reg.commands[c]["canonical_name"], "canonical": c, "direction": d,
                  "amount": _amount(a), "speed": a.get("speed"),
                  "duration": (s["t1"] - s["t0"]) if s["t0"] is not None else None,
                  "time": [s["t0"], s["t1"]] if s["t0"] is not None else None,
                  "start_position": rng[0] if rng else st["shot"]["size"],
                  "end_position": rng[1] if rng else None,
                  "target": a.get("label") or a.get("subject"), "origin": inv["origin"],
                  "sequential": not s["global"], "step": s["index"]}
            st["movement"].append(mv)
            implied = DEFINITION_IMPLIED.get(c, {})
            for f in ("speed", "amount", "end_position", "direction"):
                key = f"{c}.{f}"
                if mv[f] is None and f in implied:
                    if not any(d["from"] == c and d["dimension"] == f for d in st["meta"]["definitional"]):
                        st["meta"]["definitional"].append({"from": c, "dimension": f, "value": implied[f], "source": "COMMAND_DEFINITION"})
                    continue
                if mv[f] is None and not (f == "direction" and c not in NEEDS_DIRECTION) and key not in st["meta"]["unspecified"]:
                    st["meta"]["unspecified"].append(key)
    if st["shot"]["primary_subject"] is None and st["continuity"]["eyeline"]:
        src = st["continuity"]["eyeline"][0].split(">")[0]
        if src not in ("S", st["shot"].get("pov_owner")):
            st["shot"]["primary_subject"] = src
            st["meta"]["origins"]["shot.primary_subject"] = "INFERRED_FROM_EYELINE"
    if st["shot"]["primary_subject"] is None:
        for mv in st["movement"]:
            if mv["canonical"] in ("TRACK", "FOLLOW", "LEAD", "TRACKSIDE") and mv["target"]:
                st["shot"]["primary_subject"] = mv["target"]
                st["meta"]["origins"]["shot.primary_subject"] = "INFERRED_FROM_MOVE"
                break
    if st["shot"]["size"] is None:
        for mv in st["movement"]:
            if mv["start_position"]:
                st["shot"]["size"] = mv["start_position"]
                st["meta"]["origins"]["shot.size"] = mv["origin"]
                break
    return st


def _amount(a):
    for k in ("degrees", "percent", "distance", "magnitude"):
        if k in a:
            v = a[k]
            unit = {"degrees": "deg", "percent": "%", "distance": "m", "magnitude": ""}[k]
            return {"value": v, "unit": unit}
    return None


# --------------------------------------------------------------------------- continuity


def _rung(size):
    return registry().size_ladder.get(size) if size else None


def continuity_check(shots):
    """Cross-shot checks (research 07 D37; SRC-004 continuity geometry)."""
    diags = []
    axis = None
    for idx, sh in enumerate(shots):
        st, label = sh["state"], sh["label"]
        cmds = {c["canonical"]: c for seg in sh["segments"] for c in seg["commands"]}
        # C01 axis crossing
        if st["continuity"]["axis"]:
            new = st["continuity"]["axis"]
            if axis and new != axis:
                a1, b1 = axis.split("-")
                a2, b2 = new.split("-")
                crossed = (a1 == b2 and b1 == a2)
                declared = st["continuity"]["cross_axis"] or (idx > 0 and shots[idx - 1]["state"]["continuity"]["cross_axis"])
                if crossed and not declared:
                    diags.append(Diag("C01-AXIS-CROSSED", "ERROR",
                                      f"{label}: the line flips ({axis} -> {new}) without a declared crossing.",
                                      ["/AXIS:" + new], fix="Add /CROSSAXIS:MOVE|NEUTRAL|CUTAWAY|REESTABLISH|BLOCKING, or keep /AXIS:" + axis,
                                      evidence=["SRC-004 cinlang:245-303", "SRC-002 vocab:64"], shot=label))
            axis = new
        # C02 eyeline direction vs axis
        if axis:
            left, right = axis.split("-")
            for rel in st["continuity"]["eyeline"]:
                src, _, tgt = rel.partition(">")
                if tgt in ("OFFL", "OFFR"):
                    want = "OFFR" if src == left else ("OFFL" if src == right else None)
                    if want and tgt != want:
                        diags.append(Diag("C02-EYELINE-MISMATCH", "ERROR",
                                          f"{label}: {src} is screen-{'left' if src == left else 'right'} on the line {axis}, "
                                          f"so {src} should look {want}, not {tgt}.", ["/EYELINE:" + rel],
                                          fix=f"/EYELINE:{src}>{want}", evidence=["SRC-004 cinlang:340-361"], shot=label))
            # C03 OTS consistent with the axis
            if st["shot"]["viewpoint"] == "OTS" and st["shot"]["foreground_subject"]:
                fg, pr = st["shot"]["foreground_subject"], st["shot"]["primary_subject"]
                if {fg, pr} - {left, right} == set() and fg == pr:
                    diags.append(Diag("C03-OTS-SELF", "ERROR", f"{label}: OTS over and toward the same person.", [], shot=label))
        # C04 screen direction continuity
        if idx > 0:
            prev = shots[idx - 1]["state"]["continuity"]["screen_direction"]
            cur = st["continuity"]["screen_direction"]
            if prev in ("L2R", "R2L") and cur in ("L2R", "R2L") and prev != cur and not st["continuity"]["cross_axis"]:
                diags.append(Diag("C04-SCREEN-DIRECTION-REVERSED", "ERROR",
                                  f"{label}: travel reverses ({prev} -> {cur}); the audience reads a turn-around.",
                                  ["/SCREEN:" + cur], fix="Keep the same direction, insert a neutral TOWARD/AWAY shot, or declare /CROSSAXIS.",
                                  evidence=["SRC-004 cinlang:328-338"], shot=label))
        # C05 jump cut risk (two rungs or a real angle change)
        if idx > 0:
            p = shots[idx - 1]["state"]
            r1, r2 = _rung(p["shot"]["size"]), _rung(st["shot"]["size"])
            same_angle = (p["camera"]["angle"] == st["camera"]["angle"] and p["camera"]["height"] == st["camera"]["height"]
                          and p["shot"]["orientation"] == st["shot"]["orientation"] and p["shot"]["viewpoint"] == st["shot"]["viewpoint"])
            ps, cs = p["shot"].get("primary_subject"), st["shot"].get("primary_subject")
            pa, ca = p["continuity"]["axis"], st["continuity"]["axis"]
            side_changed = bool(st["continuity"]["cross_axis"]) or bool(pa and ca and pa != ca)  # camera went to the other side
            exempt = st["shot"]["function"] in ("INSERT", "CUTAWAY") or st["shot"]["viewpoint"] == "POV" or any(
                r["type"] == "MATCHCUT" for r in st["continuity"]["relation_to_previous_shot"]) or (ps and cs and ps != cs) \
                or side_changed
            if r1 and r2 and abs(r1 - r2) < 2 and same_angle and not exempt and not st["continuity"]["continuous"]:
                diags.append(Diag("C05-JUMP-CUT-RISK", "WARNING",
                                  f"{label}: {p['shot']['size']} -> {st['shot']['size']} is less than two size steps with no angle change.",
                                  [], fix="Change the size by two steps or move the camera 30 degrees or more (same side of the line).",
                                  evidence=["SRC-004 cinlang:36-42", "SRC-004 cinlang:315-326"], shot=label))
        # C06 POV needs a look
        if st["shot"]["viewpoint"] == "POV":
            owner = st["shot"]["pov_owner"]
            near = [shots[k]["state"] for k in (idx - 1, idx + 1) if 0 <= k < len(shots)]
            looked = any(any(e.startswith(f"{owner}>") for e in n["continuity"]["eyeline"]) or
                         (n["shot"]["function"] == "REACTION" and n["shot"]["function_target"] == owner) for n in near) if owner else False
            if not looked:
                diags.append(Diag("C06-POV-WITHOUT-LOOK", "WARNING",
                                  f"{label}: POV{':' + owner if owner else ''} has no neighbouring shot of {owner or 'the viewer'} looking.",
                                  [], fix=f"Add /EYELINE:{owner or 'A'}>... to the shot before or after.",
                                  evidence=["SRC-004 cinlang:30"], shot=label))
        # C07 continuous start == previous end
        if st["continuity"]["continuous"] and idx > 0:
            p = shots[idx - 1]["state"]
            pend = p["shot"]["size"]
            for mv in p["movement"]:
                if mv["end_position"]:
                    pend = mv["end_position"]
            cstart = st["shot"]["size"]
            if pend and cstart and pend != cstart:
                diags.append(Diag("C07-CONTINUOUS-MISMATCH", "ERROR",
                                  f"{label} is CONTINUOUS but starts at {cstart} while the previous shot ends at {pend}.",
                                  [], fix=f"Start {label} at {pend}.", evidence=["DIR-08", "SRC-010", "SRC-004 failure-modes F7"], shot=label))
            for k in ("angle", "height"):
                if p["camera"][k] and st["camera"][k] and p["camera"][k] != st["camera"][k] and not p["movement"]:
                    diags.append(Diag("C07-CONTINUOUS-MISMATCH", "ERROR",
                                      f"{label} is CONTINUOUS but the camera {k} changes ({p['camera'][k]} -> {st['camera'][k]}).",
                                      [], evidence=["DIR-08", "SRC-010"], shot=label))
        # C08 shot/reverse-shot keeps the size
        if any(r["type"] == "SRS" for r in st["continuity"]["relation_to_previous_shot"]) and idx > 0:
            p = shots[idx - 1]["state"]
            if p["shot"]["size"] and st["shot"]["size"] and _rung(p["shot"]["size"]) != _rung(st["shot"]["size"]):
                diags.append(Diag("C08-SRS-SIZE", "WARNING",
                                  f"{label}: the reverse changes size ({p['shot']['size']} -> {st['shot']['size']}); matched pairs keep lens and distance.",
                                  [], evidence=["SRC-004 cinlang:351-355"], shot=label))
        # C09 crossing by move needs a sideways move: the audience must see the camera travel across (SRC-004 cinlang:295-296)
        if st["continuity"]["cross_axis"] == "MOVE" and not any(m["canonical"] in ("TRUCK", "ORBIT", "TRACKSIDE") for m in st["movement"]):
            diags.append(Diag("C09-CROSS-NEEDS-MOVE", "WARNING",
                              f"{label}: /CROSSAXIS:MOVE but no sideways camera move (truck, arc/orbit, side tracking) carries the audience across.",
                              [], fix="Add /ORBIT or /TRUCK, or use another crossing method.", evidence=["SRC-004 cinlang:292-303"], shot=label))
        # C10 match on action needs a previous shot
        if idx == 0 and any(r["type"] in ("MATCHACTION", "SRS") for r in st["continuity"]["relation_to_previous_shot"]):
            diags.append(Diag("C10-NO-PREVIOUS-SHOT", "WARNING", f"{label}: relates to a previous shot but it is the first shot.",
                              [], shot=label))
    return diags


# --------------------------------------------------------------------------- explain


def explain(token):
    reg = registry()
    t = token.lstrip("/").split(":")[0].upper()
    if t in reg.commands:
        c = reg.commands[t]
        return {"canonical": t, **{k: c.get(k) for k in ("category", "definition", "critical_rule", "params",
                                                          "sources", "confidence", "aliases", "image_behavior", "video_behavior")}}
    if t in reg.aliases:
        return {"alias": t, **reg.aliases[t]}
    if t in reg.out_of_scope:
        return {"out_of_scope": t, **reg.out_of_scope[t]}
    return {"unknown": t, "suggestions": difflib.get_close_matches(t, list(reg.commands) + list(reg.aliases), n=5)}


# --------------------------------------------------------------------------- CLI


def _undo_msys(arg):
    """Git Bash (MSYS) rewrites a lone '/MS' argument into a path under the Git install folder ('<Git>/MS'). Undo that.
    (Or run with MSYS_NO_PATHCONV=1.)"""
    m = re.match(r"^[A-Za-z]:[\\/](?:.*[\\/])?Git[\\/](?:usr[\\/])?([A-Za-z0-9].*)$", arg)
    return "/" + m.group(1).replace(";", ":") if m else arg


def _cli(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    import argparse
    ap = argparse.ArgumentParser(description="Cinematic Director Camera DSL")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("parse", help="parse + validate, print JSON")
    p.add_argument("dsl")
    p.add_argument("--director", help="DIRECTOR_SUGGESTED layer (priority 5)")
    p.add_argument("--storyboard", help="storyboard metadata layer (priority 3)")
    p.add_argument("--nl", help="camera instructions already converted from natural language (priority 2)")
    r = sub.add_parser("render", help="render for a model")
    r.add_argument("dsl")
    r.add_argument("--model", default="generic_video")
    r.add_argument("--mode", choices=["video", "image"], default=None)
    r.add_argument("--lang", default=None)
    r.add_argument("--director", help="DIRECTOR_SUGGESTED layer (priority 5)")
    r.add_argument("--storyboard", help="storyboard metadata layer (priority 3)")
    r.add_argument("--nl", help="camera instructions already converted from natural language (priority 2)")
    r.add_argument("--json", action="store_true")
    r.add_argument("--layers", action="store_true", help="minimax_h3: print the camera core in its four layers with sources")
    r.add_argument("--h3-mode", choices=["t2va", "i2va", "fl2va", "l2va", "ref2va"], help="minimax_h3: the prompt mode the shot will be generated in (routing evidence scope)")
    r.add_argument("--h3-profile", help="minimax_h3: generation profile id from models/minimax_h3_profile.yaml; without one every routing item is UNVERIFIED")
    r.add_argument("--h3-subject-context", choices=["character_anchored", "environment_only", "constrained_production", "camera_only"],
                   help="minimax_h3: the evidence context. constrained_production (default; stored as character_anchored) = camera motion "
                        "plus framing, landing and target-relative constraints; camera_only (stored as environment_only) = camera motion "
                        "through a fixed set with nothing to frame")
    s = sub.add_parser("shots", help="validate a multi-shot list (continuity)")
    s.add_argument("dsl")
    e = sub.add_parser("explain", help="explain a command or alias")
    e.add_argument("token")
    a = ap.parse_args([_undo_msys(x) for x in argv])
    for k in ("dsl", "director", "storyboard", "nl"):  # a typed backslash-n separates shot-list lines
        if getattr(a, k, None):
            setattr(a, k, getattr(a, k).replace("\\n", "\n"))
    layers = []
    for prio, name, val in ((2, "USER_SPECIFIED", getattr(a, "nl", None)), (3, "STORYBOARD", getattr(a, "storyboard", None)),
                            (5, "DIRECTOR_SUGGESTED", getattr(a, "director", None))):
        if val:
            layers.append((prio, name, val))
    if a.cmd in ("parse", "shots"):
        res = analyze(a.dsl, layers=layers or None)
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0 if res["status"] != "ERROR" else 2
    if a.cmd == "render":
        import adapters
        if a.model not in adapters.MODELS:   # a usage error, not a crash
            print(f"ERROR: unknown model {a.model!r}; choose from {', '.join(adapters.MODELS)}")
            return 2
        res = analyze(a.dsl, layers=layers or None)
        out = adapters.render(res, model=a.model, mode=a.mode, lang=a.lang, h3_mode=a.h3_mode, h3_profile_id=a.h3_profile,
                              h3_subject_context=a.h3_subject_context)
        if a.json:
            print(json.dumps(out, ensure_ascii=False, indent=1))
        elif out["errors"]:  # never hand a contradictory or broken camera to a model
            for e in out["errors"]:
                print("ERROR:", e)
            for w in out["warnings"]:
                print("WARNING:", w)
            print("NOT RENDERED: fix the errors above first.")
        else:
            print(out["text"])
            if out.get("director_suggested"):
                print("USER_SPECIFIED:", " ".join(out["user_specified"]) or "-")
                print("DIRECTOR_SUGGESTED:", " ".join(out["director_suggested"]))
            for w in out["warnings"]:
                print("WARNING:", w)
            if out.get("unspecified"):
                print("UNSPECIFIED (left to the model):", ", ".join(out["unspecified"]))
            if out.get("definition_implied"):
                print("DEFINITION_IMPLIED (fixed by the command's definition, not added by the adapter):", ", ".join(out["definition_implied"]))
            if a.layers and a.model == "minimax_h3":
                print(adapters.h3_layers_text(out))
            if out.get("routing"):   # H3: measured reliability of what was asked, and the input mode to use
                print(adapters.routing_text(out["routing"], "zh" if a.lang == "zh" else "en"))
        return 0 if res["status"] != "ERROR" else 2
    if a.cmd == "explain":
        print(json.dumps(explain(a.token), ensure_ascii=False, indent=1))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
