# -*- coding: utf-8 -*-
"""Run every test table in ../tests/*.md.

A test row is a markdown table row:  | ID | Input | Expect | Source |
Input  : DSL text. '\\n' = new line (multi-shot lists). Extra intent layers:
         '@@director: /DSL', '@@storyboard: /DSL', '@@nl: /DSL'.
Expect : assertions separated by ';' (see ASSERTIONS below). Every assertion must pass.

    python run_tests.py            # all files
    python run_tests.py aliases    # files whose name contains 'aliases'
    python run_tests.py -v         # print every row
"""
import glob
import io
import json
import os
import re
import sys

sys.dont_write_bytecode = True   # keep the skill folder free of __pycache__ (checked by the release gate)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import adapters  # noqa: E402
import camera_dsl as dsl  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ASSERTIONS = """
status=OK|WARN|ERROR          overall status
canon=A,B                     set of resolved canonical commands equals {A,B}
has=X / hasnot=X              canonical X is (not) among the resolved commands
cat=CATEGORY                  category of the first resolved command
rel=RELATIONSHIP              alias relationship of the first resolved command
arg.KEY=VALUE                 argument of the first resolved command
type=T / notype=T             some / no diagnostic of type T (shot + continuity diagnostics)
rule=R / norule=R             some / no diagnostic with rule id R
state.PATH=VALUE              value in the first shot's camera state (dots), 'None' allowed
move.N.KEY=VALUE              key of movement N (0-based) in the first shot's state
shots=N                       number of shots
mode=M                        M is among the result modes (STRICT, DIRECTOR, VIDEO, IMAGE)
seq                           has timed/THEN segments and no ERROR
origin.X=ORIGIN               origin of resolved command X
unspec=C.FIELD                'C.FIELD' is listed as unspecified in the first shot
nounspec=C.FIELD              'C.FIELD' is NOT listed as unspecified
implied=C.FIELD=VALUE         the first shot carries a DEFINITION_IMPLIED value (fixed by the command's definition)
routing[spec]~regex           the H3 routing block for the scope in spec (model[:zh]:h3mode=<mode>:profile=<id>) matches; norouting[...] = does not
                              (spec tokens h3mode= and profile= also work in r[], warn[], nowarn[], layer[])
snapshot                      tests/snapshots/minimax_h3_core.json: the H3 camera text of every test input and the wrapper prompts
                              must be unchanged; --update-snapshot re-freezes it after a CHANGELOG entry
r[MODEL(:MODE)(:LANG)]~RE     rendered text matches regex (case-insensitive)
r[MODEL(:MODE)(:LANG)]!~RE    rendered text does not match regex
intent[MODEL(:MODE)(:LANG)]   every resolved command's markers appear; no anti-markers; no conflicting-value markers
strict[MODEL(:MODE)(:LANG)]   nothing unrequested appears (lens, focus, movement, dutch, rig words)
still[MODEL(:LANG)]           image rendering has no temporal camera verbs
warn[MODEL]~RE                a render warning matches regex
"""


def parse_tables(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.startswith("|"):
                continue
            body = line.strip()
            body = body[1:] if body.startswith("|") else body
            body = body[:-1] if body.endswith("|") and not body.endswith("\\|") else body
            cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", body)]
            if len(cells) < 3 or cells[0] in ("ID", "") or set(cells[0]) <= set("-: "):
                continue
            rows.append({"id": cells[0], "input": cells[1].strip("`"), "expect": cells[2], "source": cells[3] if len(cells) > 3 else "",
                         "file": os.path.basename(path), "line": n})
    return rows


def _analyze(inp):
    layers = []
    m = re.split(r"@@(director|storyboard|nl):", inp)
    base = m[0]
    prios = {"nl": (2, "USER_SPECIFIED"), "storyboard": (3, "STORYBOARD"), "director": (5, "DIRECTOR_SUGGESTED")}
    for i in range(1, len(m), 2):
        p, o = prios[m[i]]
        layers.append((p, o, m[i + 1].strip()))
    return dsl.analyze(base.replace("\\n", "\n"), layers=layers or None)


def _resolved(res):
    return [c for s in res["shots"] for seg in s["segments"] for c in seg["commands"]]


def _all_diags(res):
    return res["diagnostics"] + [d for s in res["shots"] for d in s["diagnostics"]]


def _get(d, path):
    for part in path.split("."):
        if isinstance(d, list):
            d = d[int(part)]
        elif isinstance(d, dict):
            d = d.get(part)
        else:
            return None
    return d


_RENDER_CACHE = {}


def _render(res, spec):
    """spec = model[:video|image][:en|zh][:h3mode=<mode>][:profile=<generation profile id>][:ctx=env|char] (the last three:
    minimax_h3 routing scope; ctx = the subject context ENVIRONMENT_ONLY / CHARACTER_ANCHORED, CL-051)."""
    parts = spec.split(":")
    model = parts[0]
    mode = next((p for p in parts[1:] if p in ("video", "image")), None)
    lang = next((p for p in parts[1:] if p in ("en", "zh")), None)
    h3mode = next((p[7:] for p in parts[1:] if p.startswith("h3mode=")), None)
    profile = next((p[8:] for p in parts[1:] if p.startswith("profile=")), None)
    ctx = next(({"env": "ENVIRONMENT_ONLY", "char": "CHARACTER_ANCHORED"}.get(p[4:], p[4:]) for p in parts[1:] if p.startswith("ctx=")), None)
    key = (id(res), model, mode, lang, h3mode, profile, ctx)
    hit = _RENDER_CACHE.get(key)
    if hit is None or hit[0] is not res:  # id() can be reused once an old result is freed
        hit = _RENDER_CACHE[key] = (res, adapters.render(res, model=model, mode=mode, lang=lang, h3_mode=h3mode, h3_profile_id=profile,
                                                         h3_subject_context=ctx))
    return hit[1]


def _lang_of(out):
    return "zh" if out["lang"] == "zh" else "en"


def check_intent(res, out):
    reg = dsl.registry()
    lang = _lang_of(out)
    text = out["text"]
    present = {c["canonical"] for c in _resolved(res)}
    problems = []
    for name in present:
        c = reg.commands[name]
        mk = (c.get("markers") or {}).get(lang) or []
        if not mk and lang == "zh":
            mk = []
        if mk and not any(re.search(m, text, re.I) for m in mk):
            problems.append(f"missing marker for {name} ({lang}): {mk}")
        for am in (c.get("anti_markers") or {}).get(lang, []) or []:
            # an anti-marker is allowed only where another present command's marker covers that exact text
            cover = [m.span() for o in present if o != name
                     for x in (reg.commands[o].get("markers") or {}).get(lang, []) or []
                     for m in re.finditer(x, text, re.I)]
            for m in re.finditer(am, text, re.I):
                a0, a1 = m.span()
                if not any(c0 < a1 and a0 < c1 for c0, c1 in cover):
                    problems.append(f"anti-marker for {name}: /{am}/ found ('{m.group(0)}')")
                    break
    # conflicting-value markers: other commands writing the same exclusive dimension
    for name in present:
        core, _ = dsl.writes_of({"canonical": name, "args": {}})
        for dim, val in core.items():
            if dim not in reg.exclusive or dim in ("rig.stability",):
                continue
            for other, oc in reg.commands.items():
                if other in present or other == name:
                    continue
                ocore = (oc.get("writes") or {})
                if dim in ocore and str(ocore[dim]) != str(val) and not str(ocore[dim]).startswith("$"):
                    if (oc.get("specializes") in present) or (reg.commands[name].get("specializes") == other):
                        continue
                    owned = present | {reg.commands[p].get("specializes") for p in present if reg.commands[p].get("specializes")}
                    for m in (oc.get("markers") or {}).get(lang, []) or []:
                        # skip markers that are substrings of a present (or implied) command's own markers
                        mine = [x for p in owned for x in (reg.commands[p].get("markers") or {}).get(lang, [])]
                        if any(m.lower() in x.lower() or x.lower() in m.lower() for x in mine):
                            continue
                        if re.search(m, text, re.I):
                            problems.append(f"{name} ({dim}={val}) but text matches {other}'s marker /{m}/")
    problems += check_contradictions(res, out)
    return problems


# Guard sentences about the CAMERA and the channels that make them false (adapters.MOVE_CHANNELS).
GUARDS = [
    (r"camera stays in one spot|camera stays in place|camera itself does not move|机位不动", {"travel"}),
    (r"camera (slides sideways and )?does not turn|keeps its angle|, staying level|camera stays level|机位不转动|角度不变", {"yaw", "pitch"}),
    (r"camera stays at the same height", {"height"}),
    (r"focal length stays the same|焦距不变", {"zoom"}),
]


def check_contradictions(res, out):
    """A render must not say the camera holds still on a channel that a simultaneous move uses."""
    problems = []
    for sh, so in zip(res["shots"], out["shots"]):
        moves = sh["state"]["movement"]
        if not moves or any(m.get("time") for m in moves) or out["mode"] != "video":
            continue
        used = set()
        for m in moves:
            used |= adapters.MOVE_CHANNELS.get(m["canonical"], set())
        m = re.search(r"framing does not change|构图不变", so["text"], re.I)
        if m:
            problems.append(f"self-contradiction: '{m.group(0)}' while {'/'.join(x['canonical'] for x in moves)} moves")
        for rx, chans in GUARDS:
            for mt in re.finditer(rx, so["text"], re.I):
                owners = [m["canonical"] for m in moves if not (adapters.MOVE_CHANNELS.get(m["canonical"], set()) & chans)]
                breakers = [m["canonical"] for m in moves if adapters.MOVE_CHANNELS.get(m["canonical"], set()) & chans]
                if owners and breakers:
                    problems.append(f"self-contradiction: '{mt.group(0)}' while {'/'.join(breakers)} moves ({'/'.join(sorted(chans))})")
                    break
    return problems


STRICT_GROUPS = [
    ("LENS", r"\b\d+ ?mm\b|wide-angle|telephoto|portrait lens|fisheye|macro|anamorphic|ultra-wide|normal lens|长焦|广角|微距|鱼眼"),
    ("FOCUS", r"shallow|deep focus|depth of field|bokeh|浅景深|深焦|移焦|focus (shifts|racks)"),
    ("MOVE", r"push(es)? in|pull(s)? (out|back)|\bpans\b|\btilts\b|trucks|zooms|circles|\borbit|tracking|crane|whip|推镜|拉镜|横摇|纵摇|环绕|跟拍"),
    ("DUTCH", r"dutch|tilted horizon|canted|斜角"),
    ("RIG", r"handheld|gimbal|steadicam|\bdrone\b|tripod|slider|手持|稳定器|无人机|三脚架"),
]
STRICT_OWNER = {"LENS": {"LENS"}, "FOCUS": {"FOCUS"}, "DUTCH": {"CAMERA_ANGLE:DUTCH"}, "RIG": {"CAMERA_RIG", "AERIAL"},
                "MOVE": {"CAMERA_ROTATION", "CAMERA_TRANSLATION", "CAMERA_TRACKING", "COMPLEX_MOVEMENT", "ZOOM", "AERIAL"}}


def check_strict(res, out):
    reg = dsl.registry()
    present = {c["canonical"] for c in _resolved(res)}
    cats = {reg.commands[p]["category"] for p in present} | {f"{reg.commands[p]['category']}:{p}" for p in present}
    problems = []
    for grp, rx in STRICT_GROUPS:
        if STRICT_OWNER[grp] & cats:
            continue
        m = re.search(rx, out["text"], re.I)
        if m:
            problems.append(f"unrequested {grp} wording: '{m.group(0)}'")
    return problems


def evaluate(row):
    _RENDER_CACHE.clear()
    res = _analyze(row["input"])
    fails = []
    for a in [x.strip() for x in row["expect"].split(";") if x.strip()]:
        ok, why = True, ""
        try:
            if a.startswith("status="):
                ok, why = res["status"] == a[7:], f"status is {res['status']}"
            elif a.startswith("canon="):
                want = set(filter(None, a[6:].split(",")))
                got = {c["canonical"] for c in _resolved(res)}
                ok, why = want == got, f"got {sorted(got)}"
            elif a.startswith("has="):
                ok, why = a[4:] in {c["canonical"] for c in _resolved(res)}, f"got {sorted({c['canonical'] for c in _resolved(res)})}"
            elif a.startswith("hasnot="):
                ok, why = a[7:] not in {c["canonical"] for c in _resolved(res)}, "present"
            elif a.startswith("cat="):
                r = _resolved(res)
                got = dsl.registry().commands[r[0]["canonical"]]["category"] if r else None
                ok, why = got == a[4:], f"got {got}"
            elif a.startswith("rel="):
                r = _resolved(res)
                got = r[0]["relationship"] if r else None
                ok, why = got == a[4:], f"got {got}"
            elif a.startswith("arg."):
                k, v = a[4:].split("=", 1)
                r = _resolved(res)
                got = r[0]["args"].get(k) if r else None
                ok, why = str(got) == v or (isinstance(got, float) and str(got) == v + ".0") or (isinstance(got, list) and ">".join(got) == v), f"got {got}"
            elif a.startswith("type=") or a.startswith("notype="):
                neg = a.startswith("no")
                t = a.split("=", 1)[1]
                found = any(d["type"] == t for d in _all_diags(res))
                ok, why = (found != neg), f"types {sorted({d['type'] for d in _all_diags(res)})}"
            elif a.startswith("rule=") or a.startswith("norule="):
                neg = a.startswith("no")
                t = a.split("=", 1)[1]
                found = any(d["rule"] == t for d in _all_diags(res))
                ok, why = (found != neg), f"rules {sorted({d['rule'] for d in _all_diags(res)})}"
            elif a.startswith("state."):
                k, v = a[6:].split("=", 1)
                got = _get(res["shots"][0]["state"], k)
                ok, why = str(got) == v or (got is None and v == "None"), f"got {got}"
            elif a.startswith("move."):
                k, v = a[5:].split("=", 1)
                got = _get(res["shots"][0]["state"]["movement"], k)
                ok, why = str(got) == v or (got is None and v == "None"), f"got {got}"
            elif a.startswith("mode="):
                ok, why = a[5:] in res["modes"], f"modes {res['modes']}"
            elif a.startswith("shots="):
                ok, why = len(res["shots"]) == int(a[6:]), f"got {len(res['shots'])}"
            elif a == "seq":
                has = any(not s["global"] and s["commands"] for sh in res["shots"] for s in sh["segments"])
                ok, why = has and res["status"] != "ERROR", f"segments={has} status={res['status']}"
            elif a.startswith("origin."):
                k, v = a[7:].split("=", 1)
                got = [c["origin"] for c in _resolved(res) if c["canonical"] == k]
                ok, why = v in got, f"got {got}"
            elif a.startswith("unspec="):
                got = res["shots"][0]["state"]["meta"]["unspecified"]
                ok, why = a[7:] in got, f"got {got}"
            elif a.startswith("nounspec="):
                got = res["shots"][0]["state"]["meta"]["unspecified"]
                ok, why = a[9:] not in got, f"got {got}"
            elif a.startswith("implied="):
                # implied=C.FIELD=VALUE : fixed by the command's definition (meta.definitional, source COMMAND_DEFINITION)
                got = [f"{d['from']}.{d['dimension']}={d['value']}" for d in res["shots"][0]["state"]["meta"]["definitional"]
                       if d.get("source") == "COMMAND_DEFINITION"]
                ok, why = a[8:] in got, f"got {got}"
            elif a.startswith("routing[") or a.startswith("norouting["):
                # routing[minimax_h3:profile=ID]~regex : the routing block (adapters.routing_text) for that evidence scope
                neg = a.startswith("no")
                m = re.match(r"(?:no)?routing\[([^\]]+)\]~(.*)$", a)
                out = _render(res, m.group(1))
                text = adapters.routing_text(out.get("routing") or [], "zh" if "zh" in m.group(1).split(":") else "en")
                hit = re.search(m.group(2), text, re.I) is not None
                ok, why = (not hit) if neg else hit, f"routing: {text[:500]!r}"
            elif a.startswith("r["):
                m = re.match(r"r\[([^\]]+)\](!?~)(.*)$", a)
                out = _render(res, m.group(1))
                hit = re.search(m.group(3), out["text"], re.I) is not None
                ok = hit if m.group(2) == "~" else not hit
                why = f"text: {out['text'][:300]}"
            elif a.startswith("intent["):
                out = _render(res, a[7:-1])
                probs = check_intent(res, out)
                ok, why = not probs, "; ".join(probs) + f" | text: {out['text'][:240]}"
            elif a.startswith("strict["):
                out = _render(res, a[7:-1])
                probs = check_strict(res, out)
                ok, why = not probs, "; ".join(probs) + f" | text: {out['text'][:240]}"
            elif a.startswith("still["):
                out = _render(res, a[6:-1].split(":")[0] + ":image" + (":" + a[6:-1].split(":")[1] if ":" in a[6:-1] else ""))
                m = adapters.TEMPORAL_VERBS.search(out["text"])
                ok, why = m is None, f"motion verb '{m.group(0) if m else ''}' in: {out['text'][:240]}"
            elif a.startswith("warn["):
                m = re.match(r"warn\[([^\]]+)\]~(.*)$", a)
                out = _render(res, m.group(1))
                ok, why = any(re.search(m.group(2), w, re.I) for w in out["warnings"]), f"warnings: {out['warnings']}"
            elif a.startswith("nowarn["):
                m = re.match(r"nowarn\[([^\]]+)\]~(.*)$", a)
                out = _render(res, m.group(1))
                ok, why = not any(re.search(m.group(2), w, re.I) for w in out["warnings"]), f"warnings: {out['warnings']}"
            elif a.startswith("layer[") or a.startswith("nolayer["):
                # layer[minimax_h3:camera_core]~regex : the named layer of the first shot's first movement (or a group: framing, rig, ...)
                neg = a.startswith("no")
                m = re.match(r"(?:no)?layer\[([^:\]]+):([^\]]+)\]~(.*)$", a)
                out = _render(res, m.group(1))
                h3 = out["shots"][0].get("h3") or {}
                if m.group(2) in adapters.H3_LAYERS:
                    mv = (h3.get("movements") or [{}])[0]
                    text = (mv.get(m.group(2)) or {}).get("text", "")
                else:
                    text = " ".join(h3.get(m.group(2)) or [])
                hit = re.search(m.group(3), text, re.I) is not None
                ok, why = (not hit) if neg else hit, f"{m.group(2)}: {text!r}"
            elif a.startswith("wrap[") or a.startswith("nowrap["):
                # wrap[i2va]~regex : the official prompt built by scripts/h3_wrappers.py with its sample content
                import h3_wrappers
                neg = a.startswith("no")
                m = re.match(r"(?:no)?wrap\[([^\]]+)\]~(.*)$", a)
                r = h3_wrappers.wrap_dsl(m.group(1), row["input"], h3_wrappers.sample_content(m.group(1)))
                probs = h3_wrappers.structure_check(m.group(1), r["prompt"])
                hit = re.search(m.group(2), r["prompt"], re.I | re.S) is not None
                ok = ((not hit) if neg else hit) and not probs
                why = f"structure: {probs}; prompt: {r['prompt'][:300]!r}"
            else:
                ok, why = False, "unknown assertion"
        except Exception as e:  # a crash is a failure, with the reason
            ok, why = False, f"exception {type(e).__name__}: {e}"
        if not ok:
            fails.append(f"{a}  -> {why}")
    return fails


SNAPSHOT = os.path.join(ROOT, "tests", "snapshots", "minimax_h3_core.json")


def snapshot_corpus():
    """Every distinct test input of tests/*.md, and the inputs of tests/h3_wrappers.md for the five wrapper modes."""
    inputs, wrap_inputs = [], []
    for f in sorted(glob.glob(os.path.join(ROOT, "tests", "*.md"))):
        for r in parse_tables(f):
            if r["input"] not in inputs:
                inputs.append(r["input"])
            if os.path.basename(f) == "h3_wrappers.md" and r["input"] not in wrap_inputs:
                wrap_inputs.append(r["input"])
    return inputs, wrap_inputs


def snapshot_build():
    """The H3 camera core text of every corpus input that renders without errors, and the wrapper prompt of every mode."""
    import h3_wrappers
    inputs, wrap_inputs = snapshot_corpus()
    cam, wraps = {}, {}
    for inp in inputs:
        out = adapters.render(_analyze(inp), model="minimax_h3")
        if not out["errors"]:
            cam[inp] = out["text"]
    for inp in wrap_inputs:
        for mode in h3_wrappers.MODES:
            wraps[f"{mode}|{inp}"] = h3_wrappers.wrap_dsl(mode, inp, h3_wrappers.sample_content(mode))["prompt"]
    return {"camera_text": cam, "wrappers": wraps}


def snapshot_check():
    """Two tests: the camera text and the wrapper prompts must equal the frozen snapshot (CAMERA_CORE_CHANGES = 0,
    WRAPPER_PROMPT_CHANGES = 0). A deliberate wording change is logged in CHANGELOG and re-frozen with --update-snapshot."""
    names = (("snapshot: camera text", "camera_text"), ("snapshot: wrapper prompts", "wrappers"))
    if not os.path.exists(SNAPSHOT):
        return [(n, ["tests/snapshots/minimax_h3_core.json missing (run --update-snapshot)"]) for n, _ in names]
    ref = json.load(io.open(SNAPSHOT, encoding="utf-8"))
    cur = snapshot_build()
    rows = []
    for name, part in names:
        fails = [f"{k!r}: now {cur[part].get(k)!r}, frozen {v!r}" for k, v in ref[part].items() if cur[part].get(k) != v]
        new = [k for k in cur[part] if k not in ref[part]]
        if new:
            fails.append(f"{len(new)} input(s) not in the snapshot (run --update-snapshot after logging the change): {new[:3]}")
        rows.append((f"{name} ({len(ref[part])})", fails))
    return rows


def example_library_check():
    """The Production Example Library tests (tests/test_example_library.py, CL-057): one row per test."""
    sys.path.insert(0, os.path.join(ROOT, "tests"))
    import test_example_library
    return test_example_library.run()


def h3_contracts_check():
    """The H3 content-contract and evidence-relation tests (tests/test_h3_contracts.py, CL-059): one row per test."""
    sys.path.insert(0, os.path.join(ROOT, "tests"))
    import test_h3_contracts
    return test_h3_contracts.run()


def main(argv):
    verbose = "-v" in argv
    if "--update-snapshot" in argv:
        snap = snapshot_build()
        os.makedirs(os.path.dirname(SNAPSHOT), exist_ok=True)
        io.open(SNAPSHOT, "w", encoding="utf-8", newline="\n").write(json.dumps(snap, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
        print(f"snapshot written: {len(snap['camera_text'])} camera texts, {len(snap['wrappers'])} wrapper prompts")
        return 0
    filt = [a for a in argv if not a.startswith("-")]
    files = sorted(glob.glob(os.path.join(ROOT, "tests", "*.md")))
    if filt:
        files = [f for f in files if any(x in os.path.basename(f) for x in filt)]
    total = passed = 0
    per_file = []
    failures = []
    ids = {}
    for f in files:
        rows = parse_tables(f)
        fp = 0
        for r in rows:
            if r["id"] in ids:
                failures.append((r, [f"duplicate test id (also {ids[r['id']]})"]))
                total += 1
                continue
            ids[r["id"]] = r["file"]
            total += 1
            fl = evaluate(r)
            if fl:
                failures.append((r, fl))
            else:
                passed += 1
                fp += 1
            if verbose:
                print(("PASS " if not fl else "FAIL ") + r["id"], r["input"])
        per_file.append((os.path.basename(f), len(rows), fp))
    if not filt:
        snap_rows, ok = snapshot_check(), 0
        for name, fl in snap_rows:
            total += 1
            if fl:
                failures.append(({"id": name, "file": "snapshots/minimax_h3_core.json", "line": 0, "input": "(test corpus)"}, fl))
            else:
                passed += 1
                ok += 1
        per_file.append(("snapshots/minimax_h3_core.json", len(snap_rows), ok))
    for key, fn, label in (("example_library", example_library_check, "(example library)"),
                           ("h3_contracts", h3_contracts_check, "(H3 content contract)")):
        if filt and not any(key in x for x in filt):
            continue
        lib_rows, ok = fn(), 0
        for name, fl in lib_rows:
            total += 1
            if fl:
                failures.append(({"id": name, "file": f"test_{key}.py", "line": 0, "input": label}, fl))
            else:
                passed += 1
                ok += 1
        per_file.append((f"test_{key}.py", len(lib_rows), ok))
    print("file".ljust(28), "tests", "passed")
    for name, n, p in per_file:
        print(name.ljust(28), str(n).rjust(5), str(p).rjust(6))
    print("TOTAL".ljust(28), str(total).rjust(5), str(passed).rjust(6), " failed:", total - passed)
    for r, fl in failures:
        print(f"\nFAIL {r['id']} ({r['file']}:{r['line']})  input: {r['input']}")
        for x in fl:
            print("   -", x)
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
