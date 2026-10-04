# -*- coding: utf-8 -*-
"""Audit the skill (spec section 35) and keep generated files in sync.

    python audit.py            # run all audits, print report, exit 1 on any error
    python audit.py --sync     # regenerate provenance 'commands', registry alias lists, reference tables,
                               # the 'output' part of schemas/examples.yaml and the case blocks in examples/*.md
    python audit.py --json     # machine-readable report
    python audit.py --release  # PUBLIC_RELEASE_GATE: every audit + every test + release checks, one verdict

Audits: RESEARCH, COMMAND, SEMANTIC, CONFLICT, MODEL, SCHEMA, TESTS, FILES, PUBLISH, BASELINE.
PUBLISH = ready for a public repository: LICENSE present and filled in, text files only, no local absolute, home-relative or
network-share paths, no private network addresses, and no private names. The private-name list stays outside the repository:
a local file of SHA-256 hashes named by CAMERA_DSL_PRIVATE_TERMS (add a line with `python audit.py --hash-term "<term>"`).
BASELINE = change control since V2_BASELINE (BASELINE_V2.md, CHANGELOG.md): frozen command/alias/grammar sets,
and every file that differs from the frozen fingerprints must be listed in a complete CHANGELOG entry.
"""
import glob
import hashlib
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
import run_tests  # noqa: E402
import yaml_lite  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REF_MAP = {
    "01_shot_size.md": ["SHOT_SIZE"], "02_subject_framing.md": ["SUBJECT_FRAMING"],
    "03_camera_angle.md": ["CAMERA_ANGLE"], "04_camera_height.md": ["CAMERA_HEIGHT"],
    "05_camera_rotation.md": ["CAMERA_ROTATION"], "06_camera_translation.md": ["CAMERA_TRANSLATION"],
    "07_tracking_complex_motion.md": ["CAMERA_TRACKING", "COMPLEX_MOVEMENT"], "08_camera_rig_behavior.md": ["CAMERA_RIG"],
    "09_lens_optics.md": ["LENS"], "10_zoom.md": ["ZOOM"], "11_focus_depth.md": ["FOCUS"],
    "12_composition.md": ["COMPOSITION"], "13_continuity.md": ["CONTINUITY"], "14_aerial_drone.md": ["AERIAL"],
    "17_prompt_translation_rules.md": ["STYLE"],
}
BEGIN, END = "<!-- BEGIN GENERATED", "<!-- END GENERATED -->"
MIN_TESTS = {"canonical_commands.md": 70, "combinations.md": 50, "conflicts.md": 30, "sequences.md": 20,
             "aliases.md": 15, "continuity.md": 10, "image_mode.md": 10, "video_mode.md": 10}
MODELS = list(adapters.MODELS)


class Report:
    def __init__(self):
        self.sections = {}

    def add(self, section, level, msg):
        self.sections.setdefault(section, {"errors": [], "warnings": [], "info": []})[level].append(msg)

    def counts(self):
        e = sum(len(v["errors"]) for v in self.sections.values())
        w = sum(len(v["warnings"]) for v in self.sections.values())
        return e, w


# ------------------------------------------------------------------ generated content


def _md(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def reference_table(cats):
    reg = dsl.registry()
    lines = ["| Command | Meaning | Args | Confidence | Sources | Aliases |", "|---|---|---|---|---|---|"]
    for name, c in reg.commands.items():
        if c["category"] not in cats:
            continue
        args = ", ".join(c.get("params") or []) or "-"
        al = ", ".join(c.get("aliases") or []) or "-"
        src = ", ".join(c.get("sources") or []) or "-"
        mean = c["definition"] + (f" **Rule:** {c['critical_rule']}" if c.get("critical_rule") else "")
        lines.append(f"| `/{name}` | {_md(mean)} | {_md(args)} | {c['confidence']} | {src} | {_md(al)} |")
    lines += ["", "| Command | Image mode | Video mode |", "|---|---|---|"]
    for name, c in reg.commands.items():
        if c["category"] in cats:
            lines.append(f"| `/{name}` | {_md(c['image_behavior'])} | {_md(c['video_behavior'])} |")
    return "\n".join(lines)


def alias_table():
    reg = dsl.registry()
    lines = ["| Alias | Resolves to | Relationship | Note |", "|---|---|---|---|"]
    for a, e in sorted(reg.aliases.items()):
        if e["relationship"] == "arg_dependent":
            tgt = "; ".join(f"`:{k}` → `/{v}`" for k, v in e["by_arg"].items())
        elif e["relationship"] == "composite":
            tgt = " + ".join(f"`/{x}`" for x in e["expands"])
        else:
            extra = (":" + ":".join(str(x) for x in e["args"])) if e.get("args") else ""
            if e.get("arg_template"):
                extra = ":" + e["arg_template"].format("X")
            tgt = f"`/{e['canonical']}{extra}`"
        note = e.get("warning") or e.get("note") or ""
        lines.append(f"| `/{a}` | {tgt} | {e['relationship']} | {_md(note)} |")
    lines += ["", "| Word | Why it is not a camera command |", "|---|---|"]
    for a, e in sorted(reg.out_of_scope.items()):
        lines.append(f"| `/{a}` | {_md(e['reason'])} |")
    return "\n".join(lines)


def conflict_tables():
    cm = dsl.registry().cm
    lines = ["| Rule | Commands | Type | Message | Evidence |", "|---|---|---|---|---|"]
    for g in cm["group_rules"]:
        who = f"/{g['a']} + " + (f"any {g['b_kind']}" if "b_kind" in g else "any move on " + ", ".join(g["b_writes_any"]))
        lines.append(f"| {g['id']} | {_md(who)} | {g['type']} | {_md(g['message'])} | {', '.join(g.get('evidence', []))} |")
    for p in cm["pair_rules"]:
        who = (" + ".join("/" + x for x in p["pair"]) if "pair" in p else
               "any of " + ", ".join("/" + x for x in p["pair_any_a"]) + " + any of " + ", ".join("/" + x for x in p["pair_any_b"]))
        lines.append(f"| {p['id']} | {_md(who)} | {p['type']} | {_md(p.get('message', ''))} | {', '.join(p.get('evidence', []))} |")
    for r in cm["semantic_rules"]:
        lines.append(f"| {r['id']} | (segment rule) | {r['type']} | {_md(r['rule'])} | {', '.join(r.get('evidence', []))} |")
    lines += ["", "Exclusive dimensions (same dimension, different value = HARD_CONFLICT): " + ", ".join(f"`{d}`" for d in cm["exclusive_dims"]) + ".",
              "", "Movement channels (opposite values at the same time = SEQUENTIAL_ONLY): " +
              "; ".join(f"`{k}` {'/'.join(v)}" for k, v in cm["channels"].items()) + "."]
    return "\n".join(lines)


def _replace_block(text, tag, content):
    b = f"{BEGIN}: {tag} -->"
    if b not in text:
        return text + f"\n\n{b}\n{content}\n{END}\n"
    pre, rest = text.split(b, 1)
    _, post = rest.split(END, 1)
    return f"{pre}{b}\n{content}\n{END}{post}"


def sync(report=None):
    reg_path = os.path.join(ROOT, "registry", "canonical_commands.yaml")
    txt = io.open(reg_path, encoding="utf-8").read()
    reg = dsl.registry()
    lists = {c: [] for c in reg.commands}
    for name, e in reg.aliases.items():
        if e["relationship"] == "arg_dependent":
            for arg, tgt in e["by_arg"].items():
                lists[tgt.split(":")[0]].append(f"/{name}:{arg}")
        elif e["relationship"] == "composite":
            for c in e["expands"]:
                lists[c].append(f"/{name}")
        else:
            lists[e["canonical"]].append(f"/{name}")
    out, cur = [], None
    for line in txt.split("\n"):
        m = re.match(r"^  ([A-Z0-9]+):\s*$", line)
        if m:
            cur = m.group(1)
        if cur and re.match(r"^    aliases: \[.*\]\s*$", line):
            line = "    aliases: [" + ", ".join(lists[cur]) + "]"
        out.append(line)
    io.open(reg_path, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    dsl._REG = None
    reg = dsl.registry()
    # provenance commands
    pv_path = os.path.join(ROOT, "registry", "provenance.yaml")
    pv = io.open(pv_path, encoding="utf-8").read()
    head, _ = pv.split("# ---- BEGIN GENERATED COMMANDS ----", 1)
    body = ["# ---- BEGIN GENERATED COMMANDS ----", "commands:"]
    for name, c in reg.commands.items():
        body.append(f"  {name}:")
        body.append(f"    category: {c['category']}")
        body.append("    sources: [" + ", ".join(c.get("sources") or []) + "]")
        body.append(f"    confidence: {c['confidence']}")
    body.append("# ---- END GENERATED COMMANDS ----")
    io.open(pv_path, "w", encoding="utf-8", newline="\n").write(head + "\n".join(body) + "\n")
    # reference tables
    for fn, cats in REF_MAP.items():
        p = os.path.join(ROOT, "references", fn)
        if not os.path.exists(p):
            continue
        t = io.open(p, encoding="utf-8").read()
        t = _replace_block(t, "commands", reference_table(cats))
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    for fn, fun in (("15_aliases.md", alias_table), ("16_conflict_rules.md", conflict_tables)):
        p = os.path.join(ROOT, "references", fn)
        if os.path.exists(p):
            t = io.open(p, encoding="utf-8").read()
            io.open(p, "w", encoding="utf-8", newline="\n").write(_replace_block(t, "table", fun()))
    if os.path.exists(EXAMPLES):
        sync_examples()
    sync_cases()
    return True


# ------------------------------------------------------------------ audits


SOURCES_FILE = os.path.join(ROOT, "SOURCES.md")


def sources_md_audit(R):
    """every source id cited in a public file resolves in SOURCES.md (CL-056); research/ and tests/reality/ stay with the
    maintainer and are not public"""
    if not os.path.exists(SOURCES_FILE):
        R.add("RESEARCH", "errors", "SOURCES.md missing (the public list of the researched sources)")
        return
    listed = set(re.findall(r"^\| (SRC-\d{3}[A-D]?|LOCAL-\d{3}|DIR-\d{2}) \|", io.open(SOURCES_FILE, encoding="utf-8").read(), re.M))
    cited = {}
    for rel, text in repo_files():
        if text is None or rel == "SOURCES.md" or rel.startswith(("research/", "tests/reality/")):
            continue
        for sid in SOURCE_ID.findall(text):
            cited.setdefault(sid, rel)
    for sid in sorted(set(cited) - listed):
        R.add("RESEARCH", "errors", f"{cited[sid]} cites {sid}, which SOURCES.md does not list")
    R.add("RESEARCH", "info", f"SOURCES.md: {len(listed)} sources listed, {len(cited)} cited in the public files, all resolved"
          if not set(cited) - listed else f"SOURCES.md: {len(listed)} sources listed, {len(set(cited) - listed)} cited ids unresolved")


def research_audit(R):
    sources_md_audit(R)
    if not os.path.isdir(os.path.join(ROOT, "research")):
        R.add("RESEARCH", "info", "maintainer research notes and license register are not part of this copy: register checks skipped")
        return []
    need = ["01_sources.md", "02_feature_matrix.md", "03_command_inventory.md", "04_terminology_conflicts.md",
            "05_gap_analysis.md", "06_license_notes.md", "07_design_decisions.md"]
    for f in need:
        p = os.path.join(ROOT, "research", f)
        if not os.path.exists(p) or os.path.getsize(p) < 1500:
            R.add("RESEARCH", "errors", f"research/{f} missing or too short")
    src = io.open(os.path.join(ROOT, "research", "01_sources.md"), encoding="utf-8").read()
    blocks = re.split(r"\n## (?=SRC-\d+|LOCAL-\d+)|\n### (?=SRC-\d+)", src)
    ids, open_ok, authors = [], 0, set()
    for b in blocks[1:]:
        sid = re.match(r"(SRC-\d+[A-Z]?|LOCAL-\d+)", b).group(1)
        ids.append(sid)
        url = re.search(r"https://github\.com/[\w.-]+/[\w.-]+", b)
        sha = re.search(r"\b[0-9a-f]{40}\b", b)
        lic = re.search(r"\*\*License\*\*", b)
        if sid.startswith("SRC"):
            if not url:
                R.add("RESEARCH", "errors", f"{sid}: no repository URL")
            if not sha:
                R.add("RESEARCH", "errors", f"{sid}: no commit SHA")
            if not lic:
                R.add("RESEARCH", "errors", f"{sid}: no license line")
            if re.search(r"File Paths?\*\*|\*\*Path\*\*", b) is None:
                R.add("RESEARCH", "warnings", f"{sid}: no explicit file path field")
            if re.search(r"License\*\*[^\n]*(MIT|Apache)", b):
                open_ok += 1
                authors.add(url.group(0).split("/")[3].lower() if url else sid)
    R.add("RESEARCH", "info", f"sources with URL+SHA+license: {len([i for i in ids if i.startswith('SRC')])}; open-source licensed: {open_ok}; distinct owners: {len(authors)}")
    if open_ok < 5:
        R.add("RESEARCH", "errors", "fewer than 5 open-source skills researched")
    if len(authors) < 3:
        R.add("RESEARCH", "errors", "fewer than 3 distinct authors")
    for w in ("SOURCE_UNAVAILABLE", "LICENSE_WARNING"):
        n = len(re.findall(w, src + io.open(os.path.join(ROOT, "research", "06_license_notes.md"), encoding="utf-8").read()))
        R.add("RESEARCH", "info", f"{w} mentions recorded: {n}")
    lic = io.open(os.path.join(ROOT, "research", "06_license_notes.md"), encoding="utf-8").read()
    license_audit(R, lic)
    # every source id used in the registry is registered
    known = set(re.findall(r"\b(SRC-\d+[A-Z]?|LOCAL-\d+|DIR-\d+)\b", src))
    reg = dsl.registry()
    used = {s for c in reg.commands.values() for s in (c.get("sources") or [])}
    for s in sorted(used - known):
        R.add("RESEARCH", "errors", f"registry cites unknown source {s}")
    return ids


LICENSE_REGISTER = os.path.join(ROOT, "research", "license_register.yaml")
LR_FIELDS = ["source", "license", "use_type", "copied_content", "attribution_required", "commercial_reuse", "status"]
LR_USE = {"terminology_reference", "architecture_reference", "evidence_reference", "interface_terms", "copied_content"}
LR_STATUS = {"CLEAR", "CLEAR_REFERENCE_ONLY", "CLEAR_INTERFACE_TERMS", "OWN_WORK", "NOT_USED"}
SOURCE_ID = re.compile(r"\b(SRC-\d{3}[A-D]?|LOCAL-\d{3}|DIR-\d{2})\b")


def license_audit(R, lic_text):
    """research/license_register.yaml: one complete entry per cited source; nothing copied except the author's own work;
    every LICENSE_WARNING in research/06 resolved."""
    if not os.path.exists(LICENSE_REGISTER):
        R.add("RESEARCH", "errors", "research/license_register.yaml missing")
        return
    reg = yaml_lite.load_file(LICENSE_REGISTER)
    entries = reg.get("sources") or {}
    for sid, e in entries.items():
        missing = [f for f in LR_FIELDS if e.get(f) is None or e.get(f) == "" or e.get(f) == []]
        if missing:
            R.add("RESEARCH", "errors", f"license register {sid}: missing {', '.join(missing)}")
        if e.get("status") not in LR_STATUS:
            R.add("RESEARCH", "errors", f"license register {sid}: unknown status {e.get('status')!r}")
        bad = [u for u in (e.get("use_type") or []) if u not in LR_USE]
        if bad:
            R.add("RESEARCH", "errors", f"license register {sid}: unknown use_type {bad}")
        if e.get("copied_content") is True and e.get("status") != "OWN_WORK":
            R.add("RESEARCH", "errors", f"license register {sid}: copied_content is true for another author's source")
        if e.get("copied_content") is not True and "copied_content" in (e.get("use_type") or []):
            R.add("RESEARCH", "errors", f"license register {sid}: use_type says copied_content but copied_content is false")
    cited = set()
    for dp, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git")]
        for fn in files:
            if fn.endswith((".md", ".yaml", ".py")):
                cited |= set(SOURCE_ID.findall(io.open(os.path.join(dp, fn), encoding="utf-8").read()))
    for sid in sorted(cited - set(entries)):
        R.add("RESEARCH", "errors", f"source {sid} is cited in the skill but has no license register entry")
    warns = reg.get("warnings") or {}
    found = sorted(set(re.findall(r"LICENSE_WARNING-\d", lic_text)))
    resolved = 0
    for w in found:
        if str((warns.get(w) or {}).get("status", "")).startswith("RESOLVED"):
            resolved += 1
        else:
            R.add("RESEARCH", "warnings", f"{w} is not resolved in research/license_register.yaml")
    own = sorted(k for k, e in entries.items() if e.get("copied_content") is True)
    R.add("RESEARCH", "info", f"license register: {len(entries)} sources, {len(cited)} cited in the skill; "
                              f"copied_content only in the author's own work {own}; LICENSE_WARNING resolved {resolved}/{len(found)}")


def command_audit(R):
    reg = dsl.registry()
    names, cmds, cnames = set(), set(), set()
    req = ["command", "canonical_name", "category", "kind", "definition", "sources", "confidence", "aliases",
           "conflicts", "compatible_with", "image_behavior", "video_behavior", "markers"]
    for n, c in reg.commands.items():
        for k in req:
            if k not in c:
                R.add("COMMAND", "errors", f"{n}: missing field {k}")
        if c.get("command") != "/" + n:
            R.add("COMMAND", "errors", f"{n}: command field {c.get('command')} != /{n}")
        if c.get("canonical_name") in cnames:
            R.add("COMMAND", "errors", f"{n}: duplicate canonical_name {c.get('canonical_name')}")
        cnames.add(c.get("canonical_name"))
        conf, src = c.get("confidence"), c.get("sources") or []
        if conf == "HIGH" and len(src) < 2:
            R.add("COMMAND", "errors", f"{n}: HIGH with {len(src)} source(s)")
        if conf in ("MEDIUM", "LOW") and len(src) < 1:
            R.add("COMMAND", "errors", f"{n}: {conf} without a source")
        if conf == "PROJECT_DEFINED" and src:
            R.add("COMMAND", "errors", f"{n}: PROJECT_DEFINED but lists sources")
        if not (c.get("markers") or {}).get("en") or not (c.get("markers") or {}).get("zh"):
            R.add("COMMAND", "errors", f"{n}: needs en and zh markers")
        for m in [x for v in (c.get("markers") or {}).values() for x in v] + [x for v in (c.get("anti_markers") or {}).values() for x in v]:
            try:
                re.compile(m)
            except re.error as e:
                R.add("COMMAND", "errors", f"{n}: bad regex {m!r}: {e}")
        if c.get("specializes") and c["specializes"] not in reg.commands:
            R.add("COMMAND", "errors", f"{n}: specializes unknown {c['specializes']}")
    seen = {}
    for a, e in reg.aliases.items():
        if a in reg.commands:
            R.add("COMMAND", "errors", f"alias {a} equals a canonical name")
        tgts = list(e["by_arg"].values()) if e["relationship"] == "arg_dependent" else (e.get("expands") or [e.get("canonical")])
        for t in tgts:
            if t.split(":")[0] not in reg.commands:
                R.add("COMMAND", "errors", f"alias {a} -> unknown {t}")
        seen[a] = tgts
    for a in reg.out_of_scope:
        if a in reg.commands or a in reg.aliases:
            R.add("COMMAND", "errors", f"out-of-scope word {a} is also a command/alias")
    # alias lists in the registry match aliases.yaml
    for n, c in reg.commands.items():
        want = set()
        for a, e in reg.aliases.items():
            if e["relationship"] == "arg_dependent":
                want |= {f"/{a}:{k}" for k, v in e["by_arg"].items() if v.split(":")[0] == n}
            elif e["relationship"] == "composite":
                if n in e["expands"]:
                    want.add(f"/{a}")
            elif e["canonical"] == n:
                want.add(f"/{a}")
        if set(c.get("aliases") or []) != want:
            R.add("COMMAND", "errors", f"{n}: registry aliases out of sync with aliases.yaml (run audit.py --sync)")
    # every alias resolves back to its canonical through the parser
    for a, tgts in seen.items():
        e = reg.aliases[a]
        probe = f"/{a}" + (":" + list(e["by_arg"])[0] if e["relationship"] == "arg_dependent" else "")
        res = dsl.analyze(probe)
        got = {c["canonical"] for s in res["shots"] for seg in s["segments"] for c in seg["commands"]}
        want = {tgts[0].split(":")[0]} if e["relationship"] != "composite" else set(tgts)
        if not want <= got:
            R.add("COMMAND", "errors", f"alias /{a} resolves to {sorted(got)}, expected {sorted(want)}")
    # provenance == registry
    pv = yaml_lite.load_file(os.path.join(ROOT, "registry", "provenance.yaml"))
    for n, c in reg.commands.items():
        p = (pv.get("commands") or {}).get(n)
        if not p or p.get("confidence") != c["confidence"] or (p.get("sources") or []) != (c.get("sources") or []):
            R.add("COMMAND", "errors", f"{n}: provenance.yaml out of sync (run audit.py --sync)")
    for sec in ("grammar", "rules"):
        for k, v in (pv.get(sec) or {}).items():
            if v.get("confidence") == "PROJECT_DEFINED" and v.get("sources") and not v.get("note"):
                R.add("COMMAND", "warnings", f"provenance {sec}.{k}: PROJECT_DEFINED with sources but no note")
    # declared conflicts / compatibles match the validator
    for n, c in reg.commands.items():
        for o in c.get("conflicts") or []:
            t = _pair_type(n, o)
            if t in ("VALID", "VALID_COMBINATION", "INFO"):
                R.add("COMMAND", "errors", f"{n}: declares conflict with {o} but validator says {t}")
        for o in c.get("compatible_with") or []:
            t = _pair_type(n, o)
            if t in ("HARD_CONFLICT", "SEQUENTIAL_ONLY"):
                R.add("COMMAND", "errors", f"{n}: declares compatible with {o} but validator says {t}")
    R.add("COMMAND", "info", f"canonical commands: {len(reg.commands)}; aliases: {len(reg.aliases)}; out-of-scope words: {len(reg.out_of_scope)}")


def _default_arg(n):
    return {"PAN": "R", "TILT": "UP", "ROLL": "CW", "TRUCK": "L", "PEDESTAL": "UP", "CRANE": "UP", "TRACKSIDE": "R",
            "ORBIT": "R", "WHIPPAN": "R", "DUTCH": "L", "LENS": "35", "OTS": "A>B", "DIRTYOTS": "A>B", "CLEANOTS": "A>B",
            "POV": "A", "THIRDS": "L", "LOOKROOM": "R", "SCREEN": "L2R", "AXIS": "A-B", "EYELINE": "A>B"}.get(n)


def _pair_type(a, b):
    ta = f"/{a}" + (":" + _default_arg(a) if _default_arg(a) else "")
    tb = f"/{b}" + (":" + _default_arg(b) if _default_arg(b) else "")
    res = dsl.analyze(f"{ta} {tb}")
    types = [d["type"] for d in res["shots"][0]["diagnostics"] if d["rule"] not in ("R08-UNSPECIFIED-DIRECTION",)]
    for t in ("HARD_CONFLICT", "SEQUENTIAL_ONLY", "SOFT_CONFLICT", "CONTEXT_DEPENDENT", "SPECIAL_TECHNIQUE", "INFO"):
        if t in types:
            return t
    return "VALID"


SEMANTIC_PAIRS = [("/PAN:R", "/TRUCK:R"), ("/TILT:UP", "/PEDESTAL:UP"), ("/DOLLYIN", "/ZOOMIN"), ("/DOLLYOUT", "/ZOOMOUT"),
                  ("/POV:A", "/LOOKCAM:A"), ("/ORBIT:R:90", "/TURNTABLE"), ("/RACKFOCUS:A>B", "/DOLLYIN"),
                  ("/WS", "/WIDEANGLE"), ("/GROUNDLEVEL", "/LOWANGLE"), ("/HIGHANGLE", "/TOPDOWN"),
                  ("/DRONEVIEW", "/BIRDSEYE"), ("/BIRDSEYE", "/TOPDOWN"), ("/DRONEVIEW", "/TOPDOWN"), ("/FPV", "/POV:A"),
                  ("/DUTCH:L", "/TILT:UP")]


def semantic_audit(R):
    reg = dsl.registry()
    for a, b in SEMANTIC_PAIRS:
        ra, rb = dsl.analyze(a), dsl.analyze(b)
        ca = {c["canonical"] for s in ra["shots"] for g in s["segments"] for c in g["commands"]}
        cb = {c["canonical"] for s in rb["shots"] for g in s["segments"] for c in g["commands"]}
        if ca & cb:
            R.add("SEMANTIC", "errors", f"{a} and {b} resolve to the same canonical {sorted(ca & cb)}")
            continue
        for model in ("generic_video", "minimax_h3", "kling"):
            ta = adapters.render(ra, model=model)["text"]
            tb = adapters.render(rb, model=model)["text"]
            lang = adapters.MODELS[model]["lang"]
            if ta.strip() and ta == tb:
                R.add("SEMANTIC", "errors", f"{a} and {b} render identically on {model}")
            for x, tx, other in ((a, ta, cb), (b, tb, ca)):
                mine_c = {c["canonical"] for c in dsl.analyze(x)["shots"][0]["segments"][0]["commands"]}
                for o in other:
                    if any(reg.commands[mc].get("specializes") == o for mc in mine_c):
                        continue  # a refinement may carry its general command's wording (BIRDSEYE contains TOPDOWN)
                    for m in (reg.commands[o].get("markers") or {}).get(lang, []):
                        mine = {c["canonical"] for c in (dsl.analyze(x)["shots"][0]["segments"][0]["commands"])}
                        own = [mm for mc in mine for mm in (reg.commands[mc].get("markers") or {}).get(lang, [])]
                        if any(mm == m for mm in own):
                            continue
                        hit = re.search(m, tx, re.I)
                        if hit and not any(re.search(mm, hit.group(0), re.I) for mm in own):
                            R.add("SEMANTIC", "errors", f"{model}: text for {x} contains {o}'s marker /{m}/")
    R.add("SEMANTIC", "info", f"separation pairs checked: {len(SEMANTIC_PAIRS)} on 3 models")


def conflict_audit(R):
    reg = dsl.registry()
    for c in reg.compat:
        res = dsl.analyze(" ".join("/" + x for x in c["set"]))
        bad = [d for s in res["shots"] for d in s["diagnostics"] if d["type"] in ("HARD_CONFLICT", "SEQUENTIAL_ONLY")]
        if bad:
            R.add("CONFLICT", "errors", f"{c['id']} {c['set']} flagged {bad[0]['type']} ({bad[0]['rule']})")
        if c["expect"] != "SOFT_OK":
            soft = [d for s in res["shots"] for d in s["diagnostics"] if d["type"] == "SOFT_CONFLICT"]
            if soft:
                R.add("CONFLICT", "errors", f"{c['id']} {c['set']} flagged SOFT ({soft[0]['rule']})")
    for p in reg.cm["pair_rules"]:
        pairs = [p["pair"]] if "pair" in p else [[x, y] for x in p["pair_any_a"] for y in p["pair_any_b"]]
        for a, b in pairs:
            t = _pair_type(a, b)
            want = p["type"]
            if want == "VALID_COMBINATION":
                ok = t in ("VALID", "VALID_COMBINATION")
            elif want == "SPECIAL_TECHNIQUE":
                ok = t == "SPECIAL_TECHNIQUE"
            else:
                ok = t == want or (t == "SEQUENTIAL_ONLY" and want in ("SOFT_CONFLICT", "CONTEXT_DEPENDENT"))
            if not ok:
                R.add("CONFLICT", "errors", f"{p['id']} /{a} + /{b}: declared {want}, validator {t}")
    # compound moves from the sources must never be HARD
    for s in ["/CRANE:UP /TILT:DOWN", "/TRACK /PEDESTAL:UP /TILT:DOWN", "/DOLLYOUT /PEDESTAL:UP", "/ORBIT:R /RACKFOCUS:FG>BG",
              "/DOLLYOUT /PAN:L", "/CRANE:UP /DOLLYOUT", "/DOLLYIN /ZOOMOUT", "/PAN:R /TRUCK:R", "/TILT:UP /PEDESTAL:DOWN"]:
        res = dsl.analyze(s)
        if res["status"] == "ERROR":
            R.add("CONFLICT", "errors", f"valid compound move misjudged as ERROR: {s}")
    R.add("CONFLICT", "info", f"compatibility sets: {len(reg.compat)}; pair rules: {len(reg.cm['pair_rules'])}; group rules: {len(reg.cm['group_rules'])}; semantic rules: {len(reg.cm['semantic_rules'])}")


LAB_LINT_DIR = os.environ.get("CAMERA_DSL_H3_LAB", "")   # optional local H3 lab; its lint holds the plain-English rule


def _lab_sentence_check():
    """The lab lint's sentence rules (no similes or literary words, 45 words max). None when the lab is not on this machine."""
    if not LAB_LINT_DIR:
        return None
    try:
        if LAB_LINT_DIR not in sys.path:
            sys.path.insert(0, LAB_LINT_DIR)
        from h3_prompt_lint import _check_sentences
        return _check_sentences
    except Exception:
        return None


def _core_text_sha(dsl_text):
    """sha of the camera text the formal H3 core writes today for a DSL (subjects as <Subject N>); the value recorded in
    results.json provenance when a cell was classified CURRENT_CORE_EXACT_MATCH (CL-036)."""
    out = adapters.render(dsl.analyze(str(dsl_text).replace("\\n", "\n")), model="minimax_h3")
    texts = [s["text"].replace("{SUBJECT}", "<Subject 1>").replace("{A}", "<Subject 1>").replace("{B}", "<Subject 2>") for s in out["shots"]]
    return hashlib.sha256("\n".join(texts).encode("utf-8")).hexdigest()[:16]


def _verdict_hash(results):
    """sha256 of every verdict in tests/reality/minimax_h3/results.json: the file without its top-level scope block and
    without cells[*].provenance (the same rule as tools/h3_reality.py verdict-hash)."""
    import hashlib
    r = {k: v for k, v in results.items() if k != "scope"}
    r["cells"] = {cid: {k: v for k, v in c.items() if k != "provenance"} for cid, c in results.get("cells", {}).items()}
    return hashlib.sha256(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def reality_audit(R):
    """Reality evidence stays bound to its mode + generation profile and the historical verdicts stay frozen
    (PROJECT_GOAL.md; CHANGELOG CL-032)."""
    import yaml_lite
    path = os.path.join(ROOT, "tests", "reality", "minimax_h3", "results.json")
    prof_path = os.path.join(ROOT, "models", "minimax_h3_profile.yaml")
    results = None
    if os.path.exists(path):
        try:
            results = json.load(io.open(path, encoding="utf-8"))
        except Exception as e:
            R.add("REALITY", "errors", f"results.json unreadable: {e}")
            return
    else:   # the matrix records stay with the maintainer (CL-056); the profile checks below still run
        R.add("REALITY", "info", "the reality matrix records (tests/reality/) are not part of this copy: verdict hash and matrix cross-checks skipped")
    try:
        prof = yaml_lite.load_file(prof_path) or {}
    except Exception as e:
        R.add("REALITY", "errors", f"models/minimax_h3_profile.yaml unreadable: {e}")
        return
    gp = prof.get("generation_profiles", {}) or {}
    reg_cmds = (yaml_lite.load_file(os.path.join(ROOT, "registry", "canonical_commands.yaml")) or {}).get("commands", {})
    for pid, g in gp.items():   # a generation profile is the identity of one setup: one mode, every field recorded
        for k in ("mode", "checkpoint", "text_encoder", "accelerator", "steps", "sampler", "cfg", "shift", "resolution", "frames",
                  "reference_configuration", "ref_image_size"):
            if k not in g:
                R.add("REALITY", "errors", f"generation_profiles.{pid}: lacks {k}")
        m = str(g.get("mode", "")).upper()
        if pid.startswith("LOCAL_"):
            if m not in adapters.MODES_H3:
                R.add("REALITY", "errors", f"generation_profiles.{pid}: a local profile has exactly one mode ({', '.join(adapters.MODES_H3)}), got {g.get('mode')!r}")
            elif m not in pid.split("_"):
                R.add("REALITY", "errors", f"generation_profiles.{pid}: the id must name its mode ({m}) so that mode + generation_profile stays unambiguous")
        elif pid in (prof.get("reality_evidence", {}) or {}):
            R.add("REALITY", "errors", f"generation_profiles.{pid}: only a local single-mode profile can hold reality evidence")
    cells, seeds, scope, h = {}, 0, {}, ""
    if results is not None:
        scope = results.get("scope") or {}
        if not scope:
            R.add("REALITY", "errors", "results.json has no scope block (mode, generation_profile, verdict_hash)")
            return
        h = _verdict_hash(results)
        if h != scope.get("verdict_hash"):
            R.add("REALITY", "errors", f"historical verdicts changed: hash {h[:16]} != frozen {str(scope.get('verdict_hash'))[:16]} "
                                       "(HISTORICAL_VERDICT_CHANGES must be 0; a deliberate re-judgement re-freezes the hash with a CHANGELOG entry)")
        cells = results.get("cells", {})
        seeds = sum(len(c.get("seeds", {})) for c in cells.values())
        if len(cells) != scope.get("cells") or seeds != scope.get("seeds"):
            R.add("REALITY", "errors", f"results.json has {len(cells)} cells / {seeds} seeds, scope says {scope.get('cells')} / {scope.get('seeds')}")
        if scope.get("generation_profile") not in gp:
            R.add("REALITY", "errors", f"results.json scope profile {scope.get('generation_profile')} is not a generation profile")
        for cid, c in cells.items():
            p = c.get("provenance")
            if not p:
                R.add("REALITY", "errors", f"{cid}: no provenance (mode, generation_profile, checkpoint, steps, accelerator, resolution, reference_configuration)")
                continue
            for k in ("mode", "generation_profile", "checkpoint", "steps", "accelerator", "resolution", "reference_configuration"):
                if k not in p:
                    R.add("REALITY", "errors", f"{cid}: provenance lacks {k}")
            if p.get("prompt_compatibility") not in adapters.PROMPT_COMPATIBILITY:
                R.add("REALITY", "errors", f"{cid}: provenance lacks prompt_compatibility ({' / '.join(adapters.PROMPT_COMPATIBILITY)})")
            g = gp.get(p.get("generation_profile"))
            if g is None:
                R.add("REALITY", "errors", f"{cid}: provenance profile {p.get('generation_profile')} is not a generation profile")
            elif str(g.get("mode", "")).upper() != str(p.get("mode", "")).upper():
                R.add("REALITY", "errors", f"{cid}: provenance mode {p.get('mode')} differs from the profile's mode {g.get('mode')}")
    ev_all = prof.get("reality_evidence", {}) or {}
    for pid, ev in ev_all.items():
        if pid not in gp:
            R.add("REALITY", "errors", f"reality_evidence.{pid}: not a generation profile")
            continue
        if str(ev.get("mode", "")).upper() != str(gp[pid].get("mode", "")).upper():
            R.add("REALITY", "errors", f"reality_evidence.{pid}: mode {ev.get('mode')} differs from the profile's mode {gp[pid].get('mode')}")
        compat_count = {}
        for tbl in adapters.EVIDENCE_TABLES:
            for e in ((ev.get(tbl, {}) or {}).get("by_command", []) or []):
                if not isinstance(e, dict):
                    continue
                pc = e.get("prompt_compatibility")   # a grade is current-core evidence only when the cell was generated with today's camera text
                cprov = (cells.get(e.get("cell")) or {}).get("provenance") or {}
                if pc not in adapters.PROMPT_COMPATIBILITY:
                    R.add("REALITY", "errors", f"reality_evidence.{pid}.{tbl}: row {e.get('key')} ({e.get('cell')}) has no prompt_compatibility")
                elif results is not None and cprov.get("prompt_compatibility") != pc:
                    R.add("REALITY", "errors", f"reality_evidence.{pid}.{tbl}: row {e.get('key')} says {pc}, results.json provenance of {e.get('cell')} says {cprov.get('prompt_compatibility')}")
                elif results is not None and pc == "CURRENT_CORE_EXACT_MATCH" and _core_text_sha(e.get("dsl", "")) != cprov.get("current_core_text_sha"):
                    R.add("REALITY", "errors", f"reality_evidence.{pid}.{tbl}: the core wording for {e.get('dsl')} changed since the compatibility check; {e.get('cell')} "
                                               "is no longer CURRENT_CORE_EXACT_MATCH (mark it PRE_REFACTOR_WORDING or re-validate it with the current core)")
                compat_count[pc] = compat_count.get(pc, 0) + 1
                if e.get("profile") != pid:
                    R.add("REALITY", "errors", f"reality_evidence.{pid}.{tbl}: row {e.get('key')} carries profile {e.get('profile')}")
                # the framing scope of a matrix row is exactly what its own dsl says (CL-044)
                try:
                    st0 = dsl.analyze(e.get("dsl", ""))["shots"][0]["state"]
                    ends = [m.get("end_position") for m in st0["movement"] if m.get("end_position")]
                    got_scope = (st0["shot"]["size"] or (st0["movement"][0].get("start_position") if st0["movement"] else None), ends[0] if ends else None)
                except Exception as ex:   # noqa: BLE001
                    got_scope = None
                    R.add("REALITY", "errors", f"reality_evidence.{pid}.{tbl}: row {e.get('key')}: dsl {e.get('dsl')!r} does not parse ({ex})")
                if got_scope is not None and (e.get("start_framing"), e.get("end_size")) != got_scope:
                    R.add("REALITY", "errors", f"reality_evidence.{pid}.{tbl}: row {e.get('key')} has start_framing {e.get('start_framing')!r} / end_size "
                                               f"{e.get('end_size')!r}, its dsl {e.get('dsl')!r} says {got_scope}")
                key = str(e.get("key", ""))   # the table follows the registry category of the row's commands, never its name
                want = {"camera_motion"} if key.startswith(("COMBO", "SEQ")) else \
                    {adapters.EVIDENCE_TABLE_OF_CATEGORY.get((reg_cmds.get(p.split(":")[0]) or {}).get("category")) for p in key.split("+")} - {None}
                if want and tbl not in want:
                    R.add("REALITY", "errors", f"reality_evidence.{pid}.{tbl}: row {key} belongs in {sorted(want)} by the registry category of its commands")
        ec = ev.get("evidence_compatibility") or {}
        for pc, n_rows in compat_count.items():
            if pc in adapters.PROMPT_COMPATIBILITY and (ec.get(pc) or {}).get("cells") != n_rows:
                R.add("REALITY", "errors", f"reality_evidence.{pid}.evidence_compatibility.{pc}: says {(ec.get(pc) or {}).get('cells')} cells, the tables hold {n_rows}")
        if compat_count.get("PRE_REFACTOR_WORDING") and (ec.get("PRE_REFACTOR_WORDING") or {}).get("applicable_to_current_core") != "UNVERIFIED":
            R.add("REALITY", "errors", f"reality_evidence.{pid}.evidence_compatibility: PRE_REFACTOR_WORDING must say applicable_to_current_core UNVERIFIED")
        for fid, f in (ev.get("lab_findings", {}) or {}).items():
            sc = f.get("scope") or {}
            if sc.get("generation_profile") != pid or str(sc.get("mode", "")).upper() != str(gp[pid].get("mode", "")).upper():
                R.add("REALITY", "errors", f"reality_evidence.{pid}.lab_findings.{fid}: scope {sc.get('mode')}/{sc.get('generation_profile')} is not this profile")
            if not f.get("finding") or "change_output" not in (f.get("adapter_action") or {}):
                R.add("REALITY", "errors", f"reality_evidence.{pid}.lab_findings.{fid}: needs finding and adapter_action.change_output")
        env = ev.get("environment_only_baseline")   # CL-051: the ENVIRONMENT_ONLY evidence of the profile, kept apart
        if env is not None:
            if not isinstance(env, dict) or adapters._ctx_of(env) != "ENVIRONMENT_ONLY":
                R.add("REALITY", "errors", f"reality_evidence.{pid}.environment_only_baseline: must be a block with subject_context ENVIRONMENT_ONLY")
            elif str(env.get("mode", "")).upper() != str(gp[pid].get("mode", "")).upper():
                R.add("REALITY", "errors", f"reality_evidence.{pid}.environment_only_baseline: mode {env.get('mode')} differs from the profile's mode")
        shots = [(f"production_shots.{sid}", sh) for sid, sh in (ev.get("production_shots", {}) or {}).items()]
        if isinstance(env, dict):
            shots += [(f"environment_only_baseline.production_shots.{sid}", sh) for sid, sh in (env.get("production_shots", {}) or {}).items()]
            for sid, sh in (env.get("production_shots", {}) or {}).items():
                if adapters._ctx_of(sh) != "ENVIRONMENT_ONLY":
                    R.add("REALITY", "errors", f"reality_evidence.{pid}.environment_only_baseline.production_shots.{sid}: subject_context must be ENVIRONMENT_ONLY")
        for sid, shot in shots:
            sid = sid.split("production_shots.", 1)[1] if sid.startswith("production_shots.") else sid
            for k in ("evidence_status", "generation_profile", "mode", "tested_seeds", "verdict"):
                if k not in shot:
                    R.add("REALITY", "errors", f"reality_evidence.{pid}.production_shots.{sid}: lacks {k}")
            if shot.get("evidence_status") not in adapters.EVIDENCE_STATUSES:
                R.add("REALITY", "errors", f"reality_evidence.{pid}.production_shots.{sid}: evidence_status {shot.get('evidence_status')!r} is not one of {adapters.EVIDENCE_STATUSES}")
            if shot.get("evidence_status") == "PROVISIONAL" and "caveat" not in shot:
                R.add("REALITY", "errors", f"reality_evidence.{pid}.production_shots.{sid}: a PROVISIONAL record must say why (caveat)")
            if shot.get("generation_profile") != pid:
                R.add("REALITY", "errors", f"reality_evidence.{pid}.production_shots.{sid}: profile {shot.get('generation_profile')}")
    for cmd, r in (prof.get("production_routes", {}) or {}).items():
        for x in (r.get("routes", []) or []):
            g = gp.get(x.get("generation_profile"))
            if g is None or str(g.get("mode", "")).upper() != str(x.get("mode", "")).upper():
                R.add("REALITY", "errors", f"production_routes.{cmd}: route {x.get('input')} has mode {x.get('mode')} / profile {x.get('generation_profile')} that do not match a generation profile")
            if x.get("evidence_status") not in adapters.EVIDENCE_STATUSES:
                R.add("REALITY", "errors", f"production_routes.{cmd}: route {x.get('input')} has no valid evidence_status")
            if x.get("evidence_status") == "PROVISIONAL" and "caveat" not in x:
                R.add("REALITY", "errors", f"production_routes.{cmd}: route {x.get('input')} is PROVISIONAL without a caveat")
            if _ctx_route(x) not in adapters.SUBJECT_CONTEXTS:
                R.add("REALITY", "errors", f"production_routes.{cmd}: route {x.get('input')} has subject_context {x.get('subject_context')!r}, not one of {adapters.SUBJECT_CONTEXTS}")
            elif _ctx_route(x) == "ENVIRONMENT_ONLY" and not isinstance((ev_all.get(x.get("generation_profile")) or {}).get("environment_only_baseline"), dict):
                R.add("REALITY", "errors", f"production_routes.{cmd}: ENVIRONMENT_ONLY route {x.get('input')} has no environment_only_baseline under {x.get('generation_profile')}")
            if "end_framing" in x and x.get("end_framing") not in adapters.END_FRAMINGS:
                R.add("REALITY", "errors", f"production_routes.{cmd}: route {x.get('input')} has end_framing {x.get('end_framing')!r}, not one of {adapters.END_FRAMINGS}")
            # the framing scope of a route: valid shot sizes, and exactly what its measured_dsl says
            where = f"production_routes.{cmd}: route {x.get('input')}"
            for k in ("start_framing", "end_size"):
                if k in x and x.get(k) not in adapters.SIZE_SHORT_EN and not (k == "start_framing" and x.get(k) == "NONE"):
                    R.add("REALITY", "errors", f"{where} has {k} {x.get(k)!r}, not a shot size")
            if x.get("end_size") and x.get("end_framing") != "SPECIFIED":
                R.add("REALITY", "errors", f"{where} has an end_size without end_framing SPECIFIED")
            if "angle" in x and (isinstance(x["angle"], bool) or not isinstance(x["angle"], (int, float)) or x["angle"] <= 0):
                R.add("REALITY", "errors", f"{where} has angle {x.get('angle')!r}, not a positive number of degrees")
            if any(k in x for k in ("start_framing", "end_framing", "end_size", "angle")):
                if not x.get("measured_dsl"):
                    R.add("REALITY", "errors", f"{where} carries a framing scope without measured_dsl")
                else:
                    several = isinstance(x["measured_dsl"], list)     # a route that sums up several cells (pan left and pan right) names each DSL
                    for one in (x["measured_dsl"] if several else [x["measured_dsl"]]):
                        try:
                            st0 = dsl.analyze(one)["shots"][0]["state"]
                            mv0 = [m for m in st0["movement"] if m["canonical"] == cmd]
                            if cmd == "STATIC" and not st0["movement"] and st0["rig"].get("locked"):   # a locked shot (CL-051)
                                mv0 = [{"canonical": "STATIC", "direction": None, "start_position": None, "end_position": None, "amount": None}]
                        except Exception as e:   # noqa: BLE001
                            st0, mv0 = None, []
                            R.add("REALITY", "errors", f"{where}: measured_dsl {one!r} does not parse ({e})")
                        if st0 is not None and len(mv0) != 1:
                            R.add("REALITY", "errors", f"{where}: measured_dsl {one!r} has no single {cmd} move")
                        elif st0 is not None:
                            got = {"direction": mv0[0].get("direction"), "start_framing": mv0[0].get("start_position") or st0["shot"]["size"] or "NONE",
                                   "end_size": mv0[0].get("end_position"), "end_framing": "SPECIFIED" if mv0[0].get("end_position") else "FREE"}
                            bad = [k for k in ("start_framing", "end_framing") if k in x and x[k] != got[k]]
                            bad += ["direction"] if (x.get("direction") != got["direction"] and not (several and "direction" not in x)) else []
                            bad += ["end_size"] if ("end_framing" in x or "end_size" in x) and x.get("end_size") != got["end_size"] else []
                            # the angle scope (CL-048): a route carries exactly the angle its measured_dsl states; a stated angle may not be left out
                            got["angle"] = adapters._asked_angle(mv0[0])
                            if got["angle"] is not None or "angle" in x:
                                xa = x.get("angle")
                                same_angle = (isinstance(got["angle"], float) and isinstance(xa, (int, float)) and not isinstance(xa, bool)
                                              and float(xa) == got["angle"])
                                bad += [] if same_angle else ["angle"]
                            if bad:
                                R.add("REALITY", "errors", f"{where}: {', '.join(bad)} does not match its measured_dsl {one!r} ({got})")
    scopes = ", ".join(f"{k} ({v.get('evidence_status')})" for k, v in ev_all.items())
    R.add("REALITY", "info", f"results.json: {len(cells)} cells, {seeds} seeds, scope {scope.get('mode')}/{scope.get('generation_profile')}, "
                             f"verdict hash {h[:12]} frozen {scope.get('frozen')}; evidence scopes: {scopes}" if results is not None
          else f"evidence scopes: {scopes}")


def _ctx_route(x):
    return str(x.get("subject_context") or "CHARACTER_ANCHORED").upper()


def model_audit(R):
    reg = dsl.registry()
    lab_check = _lab_sentence_check()
    lab_n = 0
    inputs = []
    for n in reg.commands:
        a = _default_arg(n)
        inputs.append(f"/{n}" + (f":{a}" if a else ""))
    inputs += [" ".join("/" + x for x in c["set"]) for c in reg.compat]
    fails = {m: 0 for m in MODELS}
    total = 0
    for inp in inputs:
        res = dsl.analyze(inp)
        if res["status"] == "ERROR":
            continue
        for m in MODELS:
            for lang in adapters.MODELS[m]["langs"]:
                out = adapters.render(res, model=m, lang=lang)
                total += 1
                probs = run_tests.check_intent(res, out)
                if m == "minimax_h3" and lab_check:
                    E, W = [], []
                    lab_check(out["text"], E, W)
                    lab_n += 1
                    probs += [f"lab lint: {e}" for e in E]
                if adapters.MODELS[m]["kind"] != "video":
                    v = adapters.TEMPORAL_VERBS.search(out["text"])
                    if v:
                        probs.append(f"motion verb '{v.group(0)}'")
                if probs:
                    fails[m] += 1
                    if fails[m] <= 3:
                        R.add("MODEL", "errors", f"{m}/{lang} {inp}: {probs[0]}")
    for m, f in fails.items():
        if f > 3:
            R.add("MODEL", "errors", f"{m}: {f} renders lose camera intent in total")
    R.add("MODEL", "info", f"renders checked for intent preservation: {total} ({len(inputs)} inputs x models x languages)")
    R.add("MODEL", "info", f"H3 renders checked with the lab lint (plain-English rule H3LAB-PLAIN-01): {lab_n}" if lab_check
          else "lab lint not configured (set CAMERA_DSL_H3_LAB): H3 plain-English check skipped")


# ------------------------------------------------------------------ schema

SPEC17 = ["shot.size", "shot.framing", "shot.subject_count", "shot.primary_subject", "shot.foreground_subject",
          "camera.position", "camera.height", "camera.angle", "camera.orientation",
          "movement[].type", "movement[].direction", "movement[].amount", "movement[].speed", "movement[].duration",
          "movement[].start_position", "movement[].end_position", "rig.type", "rig.stability",
          "lens.focal_length", "lens.lens_type", "focus.target", "focus.depth_of_field", "focus.transition",
          "composition.placement", "composition.foreground", "composition.midground", "composition.background",
          "composition.depth_layers", "continuity.axis", "continuity.screen_direction", "continuity.eyeline",
          "continuity.relation_to_previous_shot", "style.visual_style", "constraints.preserve_character",
          "constraints.preserve_clothing", "constraints.preserve_scene", "constraints.preserve_props",
          "constraints.preserve_action"]
EXAMPLES = os.path.join(ROOT, "schemas", "examples.yaml")


def _schema():
    return yaml_lite.load_file(os.path.join(ROOT, "schemas", "camera_dsl_schema.yaml"))


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _children(sec, path):
    if path == "":
        return {k: k for k in sec if "." not in k and "[" not in k}
    pre = path + "."
    return {k[len(pre):]: k for k in sec if k.startswith(pre) and "." not in k[len(pre):]}


def _check_obj(val, secname, path, SC, errs):
    if not isinstance(val, dict):
        errs.append(f"{secname}:{path or '(root)'}: expected an object, got {type(val).__name__}")
        return
    sec = SC[secname]
    kids = _children(sec, path)
    for k in val:
        if k not in kids:
            errs.append(f"{secname}:{(path + '.') if path else ''}{k}: not declared in the schema")
    for k, full in kids.items():
        if k not in val:
            if not sec[full].get("optional"):
                errs.append(f"{secname}:{full}: missing from the parser output")
            continue
        _check_val(val[k], sec[full], full, secname, SC, errs)


def _check_val(val, spec, path, secname, SC, errs):
    t, vals, pat = spec["type"], spec.get("values"), spec.get("pattern")
    if val is None:
        if not spec.get("nullable"):
            errs.append(f"{secname}:{path}: null not allowed")
        return
    bad = None
    if t == "enum":
        bad = val not in vals
    elif t == "enum_or_true":
        bad = not (val is True or val in vals)
    elif t == "number_or_enum":
        bad = not (_is_num(val) or val in vals)
    elif t == "string":
        bad = not isinstance(val, str) or bool(pat and not re.match(pat, val))
    elif t == "number":
        bad = not _is_num(val)
    elif t == "integer":
        bad = not (isinstance(val, int) and not isinstance(val, bool))
    elif t == "boolean":
        bad = not isinstance(val, bool)
    elif t == "scalar":
        bad = isinstance(val, (dict, list))
    elif t == "map":
        bad = not isinstance(val, dict) or bool(vals and any(v not in vals for v in val.values()))
    elif t == "object":
        _check_obj(val, secname, path, SC, errs)
    elif t in ("state", "diagnostic"):
        _check_obj(val, t, "", SC, errs)
    elif t == "list":
        if not isinstance(val, list):
            bad = True
        else:
            it = spec.get("item_type")
            for i, item in enumerate(val):
                if it == "object":
                    _check_obj(item, secname, path + "[]", SC, errs)
                elif it in ("state", "diagnostic"):
                    _check_obj(item, it, "", SC, errs)
                else:
                    _check_val(item, {"type": it, "values": vals, "pattern": pat}, f"{path}[{i}]", secname, SC, errs)
    else:
        errs.append(f"{secname}:{path}: unknown schema type {t!r}")
    if bad:
        errs.append(f"{secname}:{path}: {val!r} does not match type {t}" + (f" {vals}" if vals else "") + (f" /{pat}/" if pat else ""))


def validate_result(res, SC=None):
    """Validate a camera_dsl.analyze() result against schemas/camera_dsl_schema.yaml. Returns a list of errors."""
    errs = []
    _check_obj(res, "result", "", SC or _schema(), errs)
    return errs


def _flat(obj, prefix=""):
    out = {}
    if isinstance(obj, dict) and obj:
        for k, v in obj.items():
            out.update(_flat(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(obj, list) and obj and isinstance(obj[0], dict):
        for i, v in enumerate(obj):
            out.update(_flat(v, f"{prefix}[{i}]"))
    else:
        out[prefix] = obj
    return out


def _fmt(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, list):
        return ">".join(str(x) for x in v)
    return str(v)


def example_output(inp):
    """The generated part of one schemas/examples.yaml entry."""
    res = run_tests._analyze(inp)
    empty = _flat(dsl.analyze("")["shots"][0]["state"])
    out = {"status": res["status"], "modes": res["modes"]}
    if res["diagnostics"]:
        out["diagnostics"] = [f"{d['rule']} [{d['type']}] {d['message']}" for d in res["diagnostics"]]
    shots = []
    for sh in res["shots"]:
        cmds = []
        for seg in sh["segments"]:
            when = "" if seg["global"] else (f"[{_fmt(seg['t0'])}-{_fmt(seg['t1'])}s] " if seg["t0"] is not None else f"[THEN {seg['index']}] ")
            for c in seg["commands"]:
                args = ", ".join(f"{k}={_fmt(v)}" for k, v in c["args"].items())
                extra = [] if c["relationship"] == "canonical" else [c["relationship"]]
                if c["origin"] != "USER_SPECIFIED":
                    extra.append(c["origin"])
                cmds.append(f"{when}{c['raw']} -> {c['canonical']}" + (f" {{{args}}}" if args else "")
                            + (f" ({', '.join(extra)})" if extra else ""))
        item = {"label": sh["label"], "status": sh["status"], "commands": cmds}
        if sh["diagnostics"]:
            item["diagnostics"] = [f"{d['rule']} [{d['type']}] {d['message']}" for d in sh["diagnostics"]]
        missing = object()
        item["state"] = {k: v for k, v in _flat(sh["state"]).items() if empty.get(k, missing) != v}
        shots.append(item)
    out["shots"] = shots
    return out


_PLAIN = re.compile(r"^[A-Za-z_][A-Za-z0-9_.>+%-]*$")


def _y(v):
    if v is None:
        return "null"
    if v is True or v is False:
        return "true" if v else "false"
    if _is_num(v):
        return repr(v)
    if isinstance(v, str):
        if _PLAIN.match(v) and v.lower() not in ("null", "true", "false", "yes", "no", "on", "off"):
            return v
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        return "[" + ", ".join(_y(x) for x in v) + "]"
    if isinstance(v, dict) and not v:
        return "{}"
    raise TypeError(f"cannot write {v!r}")


def _dump_map(d, ind):
    lines = []
    for k, v in d.items():
        key = k if re.match(r"^[A-Za-z_][A-Za-z0-9_.\[\]]*$", k) else json.dumps(k, ensure_ascii=False)
        if isinstance(v, dict) and v:
            lines.append(f"{ind}{key}:")
            lines += _dump_map(v, ind + "  ")
        elif isinstance(v, list) and v and isinstance(v[0], dict):
            lines.append(f"{ind}{key}:")
            for item in v:
                sub = _dump_map(item, ind + "    ")
                sub[0] = ind + "  - " + sub[0].lstrip()
                lines += sub
        elif isinstance(v, list) and len(v) > 1 and len(_y(v)) + len(ind) + len(key) > 110:
            lines.append(f"{ind}{key}:")
            lines += [f"{ind}  - {_y(x)}" for x in v]
        else:
            lines.append(f"{ind}{key}: {_y(v)}")
    return lines


def sync_examples():
    text = io.open(EXAMPLES, encoding="utf-8").read()
    head = text.split("\nexamples:", 1)[0].rstrip("\n") + "\n\n"
    data = yaml_lite.load(text)
    items = []
    for ex in data["examples"]:
        item = {k: ex[k] for k in ("id", "title", "input", "note") if ex.get(k) is not None}
        item["output"] = example_output(ex["input"])
        items.append(item)
    body = _dump_map({"examples": items}, "")
    new = head + "\n".join(body) + "\n"
    if yaml_lite.lite_load(new)["examples"] != [dict(i) for i in items]:
        raise RuntimeError("examples.yaml would not round-trip through yaml_lite")
    io.open(EXAMPLES, "w", encoding="utf-8", newline="\n").write(new)


def schema_audit(R):
    SC = _schema()
    st = SC["state"]
    for f in SPEC17:
        if f not in st:
            R.add("SCHEMA", "errors", f"spec section 17 field {f} is not in the schema")
        elif not st[f].get("spec17"):
            R.add("SCHEMA", "warnings", f"{f}: spec17 flag missing")
    for secname in ("result", "diagnostic", "state"):
        for k in SC[secname]:
            if "." in k:
                parent = k.rsplit(".", 1)[0]
                parent = parent[:-2] if parent.endswith("[]") else parent
                if parent not in SC[secname]:
                    R.add("SCHEMA", "errors", f"{secname}:{k}: parent {parent} not declared")
    # every parser output the audit can generate must validate
    reg = dsl.registry()
    inputs = [f"/{n}" + (f":{_default_arg(n)}" if _default_arg(n) else "") for n in reg.commands]
    inputs += [" ".join("/" + x for x in c["set"]) for c in reg.compat]
    inputs += [r["input"] for f in sorted(glob.glob(os.path.join(ROOT, "tests", "*.md"))) for r in run_tests.parse_tables(f)]
    seen, bad = set(), 0
    for inp in inputs:
        errs = validate_result(run_tests._analyze(inp), SC)
        if errs:
            bad += 1
            for e in errs:
                if e not in seen and len(seen) < 8:
                    seen.add(e)
                    R.add("SCHEMA", "errors", f"{inp!r}: {e}")
    if bad > 8:
        R.add("SCHEMA", "errors", f"{bad} parser outputs do not match the schema")
    R.add("SCHEMA", "info", f"parser outputs validated against the schema: {len(inputs)} "
                            "(every command, every compatible set, every test input)")
    # examples.yaml is real parser output
    if not os.path.exists(EXAMPLES):
        R.add("SCHEMA", "errors", "schemas/examples.yaml missing")
        return
    data = yaml_lite.load_file(EXAMPLES)
    exs = data.get("examples") or []
    for ex in exs:
        if ex.get("output") != example_output(ex["input"]):
            R.add("SCHEMA", "errors", f"examples.yaml {ex.get('id')}: recorded output differs from the parser "
                                      "(check the change, then run audit.py --sync)")
    R.add("SCHEMA", "info", f"examples.yaml entries checked against the parser: {len(exs)}")
    if len(exs) < 8:
        R.add("SCHEMA", "warnings", f"examples.yaml has only {len(exs)} examples")


# ------------------------------------------------------------------ examples/*.md cases

CASE_RE = re.compile(r'^<!-- case models=([^\s"]+) input="([^"\n]*)" -->\n(.*?)^<!-- /case -->', re.M | re.S)
MODEL_LABEL = {"generic_video": "Generic video", "minimax_h3": "MiniMax H3", "kling": "Kling", "veo": "Veo",
               "generic_image": "Generic image", "flux": "FLUX", "qwen_image": "Qwen-Image",
               "qwen_image_edit": "Qwen-Image-Edit"}


def case_block(models, inp):
    """Real parser + adapter output for one example case (examples/*.md)."""
    res = run_tests._analyze(inp)
    lines = ["| | |", "|---|---|", f"| Status | **{res['status']}** · modes {', '.join(res['modes'])} |"]
    for sh in res["shots"]:
        cmds = []
        for seg in sh["segments"]:
            when = "" if seg["global"] else (f"[{_fmt(seg['t0'])}-{_fmt(seg['t1'])}s] " if seg["t0"] is not None else "THEN ")
            for c in seg["commands"]:
                args = ",".join(f"{k}={_fmt(v)}" for k, v in c["args"].items())
                tag = "" if c["origin"] == "USER_SPECIFIED" else f" ({c['origin']})"
                cmds.append(f"{when}`{c['raw']}` → {c['canonical']}" + (f"{{{args}}}" if args else "") + tag)
        label = f"Resolved {sh['label']}" if len(res["shots"]) > 1 else "Resolved"
        lines.append(f"| {label} | " + " · ".join(cmds).replace("|", "\\|") + " |")
    diags = res["diagnostics"] + [d for sh in res["shots"] for d in sh["diagnostics"]]
    for d in diags:
        lines.append(f"| {d['type']} | `{d['rule']}` {d['message']}".replace("|", "\\|").replace("\\| ", "| ", 1) + " |")
    unspec = sorted({u for sh in res["shots"] for u in sh["state"]["meta"]["unspecified"]})
    if unspec:
        lines.append("| Left to the model | " + ", ".join(unspec) + " |")
    if res["status"] == "ERROR":
        lines.append("")
        lines.append("Not rendered: fix the ERROR first (adapters refuse to guess).")
        return "\n".join(lines) + "\n"
    for spec in models.split(","):
        parts = spec.split(":")
        out = adapters.render(res, model=parts[0], mode=next((p for p in parts[1:] if p in ("video", "image")), None),
                              lang=next((p for p in parts[1:] if p in ("en", "zh")), None))
        name = MODEL_LABEL.get(parts[0], parts[0]) + (f" ({out['lang']}, {out['mode']})" if len(parts) > 1 else "")
        lines.append("")
        lines.append(f"**{name}**")
        lines.append("")
        lines += ["> " + ln if ln else ">" for ln in out["text"].split("\n")]
        if out.get("director_suggested"):
            lines.append("")
            lines.append("USER_SPECIFIED: " + " ".join(f"`{x}`" for x in out["user_specified"])
                         + " · DIRECTOR_SUGGESTED: " + " ".join(f"`{x}`" for x in out["director_suggested"]))
        extra = [w for w in out["warnings"] if not re.search(r": \[[A-Z0-9]+-[A-Z0-9-]+\] ", w)]
        for w in extra:
            lines.append("")
            lines.append(f"⚠ {w}")
    return "\n".join(lines) + "\n"


def _cases_expand(text):
    def rep(m):
        models, inp = m.group(1), m.group(2).replace("\\n", "\n")
        return f'<!-- case models={m.group(1)} input="{m.group(2)}" -->\n' + case_block(models, inp) + "<!-- /case -->"
    return CASE_RE.sub(rep, text)


def sync_cases():
    for f in sorted(glob.glob(os.path.join(ROOT, "examples", "*.md"))):
        t = io.open(f, encoding="utf-8").read()
        io.open(f, "w", encoding="utf-8", newline="\n").write(_cases_expand(t))


def cases_audit(R):
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "examples", "*.md"))):
        t = io.open(f, encoding="utf-8").read()
        k = len(CASE_RE.findall(t))
        n += k
        if k == 0:
            R.add("FILES", "warnings", f"examples/{os.path.basename(f)}: no generated cases")
        if _cases_expand(t) != t:
            R.add("FILES", "errors", f"examples/{os.path.basename(f)}: case output differs from the adapters (run audit.py --sync)")
    R.add("FILES", "info", f"example cases checked against real adapter output: {n}")


DOC_EX_RE = re.compile(r"^`([^`]+)`(?: \((zh|en)\))?[^\n]*\n> ([^\n]+)$", re.M)


def model_docs_audit(R):
    """The 'actual adapter output' quoted in models/*.md must be what the adapter prints today."""
    n = 0
    for m in MODELS:
        f = os.path.join(ROOT, "models", f"{m}.md")
        if not os.path.exists(f):
            continue
        for dsl_text, lang, quoted in DOC_EX_RE.findall(io.open(f, encoding="utf-8").read()):
            n += 1
            out = adapters.render(dsl.analyze(dsl_text), model=m, lang=lang or None)
            if out["text"] != quoted.strip():
                R.add("MODEL", "errors", f"models/{m}.md example `{dsl_text}`{' (' + lang + ')' if lang else ''} "
                                         f"differs from the adapter:\n        now: {out['text']}")
    R.add("MODEL", "info", f"model-doc examples checked against the adapters: {n}")


def tests_audit(R):
    counts = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "tests", "*.md"))):
        counts[os.path.basename(f)] = len(run_tests.parse_tables(f))
    for f, n in MIN_TESTS.items():
        if counts.get(f, 0) < n:
            R.add("TESTS", "errors", f"{f}: {counts.get(f, 0)} tests < required {n}")
    if "regression.md" not in counts:
        R.add("TESTS", "errors", "tests/regression.md missing")
    rows = run_tests.parse_tables(os.path.join(ROOT, "tests", "model_adapters.md"))
    for m in MODELS:
        n = sum(1 for r in rows if f"[{m}" in r["expect"])
        if n < 10:
            R.add("TESTS", "errors", f"model {m}: {n} consistency tests < 10")
    R.add("TESTS", "info", "test rows: " + ", ".join(f"{k}={v}" for k, v in counts.items()))
    return counts


def files_audit(R):
    need = ["SKILL.md", "README.md", "registry/canonical_commands.yaml", "registry/aliases.yaml", "registry/compatibility_matrix.yaml",
            "registry/conflict_matrix.yaml", "registry/provenance.yaml", "schemas/camera_dsl_schema.md", "schemas/camera_dsl_schema.yaml",
            "schemas/examples.yaml"] + [f"references/{f}" for f in list(REF_MAP) + ["15_aliases.md", "16_conflict_rules.md"]] + \
           [f"models/{m}.md" for m in MODELS] + [f"examples/{e}.md" for e in ("basic", "dialogue", "action", "storyboard", "advanced_combinations")] + \
           ["SOURCES.md", "scripts/example_library.py", "tests/test_example_library.py"] + \
           [f"examples/production_library/{f}" for f in ("README.md", "production_examples.yaml", "schema.yaml", "narrative_30.md", "technique_36.md")]
    for f in need:
        if not os.path.exists(os.path.join(ROOT, f)):
            R.add("FILES", "errors", f"missing {f}")
    # every canonical command in exactly one reference table
    reg = dsl.registry()
    where = {n: [] for n in reg.commands}
    for fn in REF_MAP:
        p = os.path.join(ROOT, "references", fn)
        if os.path.exists(p):
            t = io.open(p, encoding="utf-8").read()
            if BEGIN not in t:
                R.add("FILES", "errors", f"references/{fn}: no generated table")
                continue
            block = t.split(BEGIN, 1)[1].split(END, 1)[0]
            for n in reg.commands:
                if re.search(rf"^\| `/{n}` \|", block, re.M):
                    where[n].append(fn)
            if block.strip() != (": commands -->\n" + reference_table(REF_MAP[fn])).strip():
                R.add("FILES", "errors", f"references/{fn}: generated table out of date (run audit.py --sync)")
    for n, fs in where.items():
        if len(set(fs)) != 1:
            R.add("FILES", "errors", f"/{n} appears in {len(set(fs))} reference files")
    sk = os.path.join(ROOT, "SKILL.md")
    if os.path.exists(sk):
        t = io.open(sk, encoding="utf-8").read()
        if not t.startswith("---\nname: cinematic-director-camera-dsl\n"):
            R.add("FILES", "errors", "SKILL.md frontmatter must start with name: cinematic-director-camera-dsl")
        n = t.count("\n")
        R.add("FILES", "info", f"SKILL.md lines: {n}")
        if n > 200:
            R.add("FILES", "warnings", f"SKILL.md has {n} lines (keep it lean)")
    R.add("FILES", "info", f"YAML backend: {yaml_lite.BACKEND}")
    # yaml_lite vs PyYAML (when available)
    try:
        import yaml  # noqa: F401
        for f in glob.glob(os.path.join(ROOT, "registry", "*.yaml")) + glob.glob(os.path.join(ROOT, "schemas", "*.yaml")):
            t = io.open(f, encoding="utf-8").read()
            if yaml_lite.lite_load(t) != yaml.safe_load(t):
                R.add("FILES", "errors", f"{os.path.basename(f)}: yaml_lite and PyYAML disagree")
    except ImportError:
        R.add("FILES", "info", "PyYAML not installed; yaml_lite parses every registry/schema file")
        for f in glob.glob(os.path.join(ROOT, "registry", "*.yaml")) + glob.glob(os.path.join(ROOT, "schemas", "*.yaml")):
            try:
                yaml_lite.lite_load(io.open(f, encoding="utf-8").read())
            except Exception as e:
                R.add("FILES", "errors", f"{os.path.basename(f)}: {e}")


# ------------------------------------------------------------------ V2 baseline (change control)

BASELINE_FILE = os.path.join(ROOT, "BASELINE_V2.md")
CHANGELOG_FILE = os.path.join(ROOT, "CHANGELOG.md")
NOT_FINGERPRINTED = {"BASELINE_V2.md", "CHANGELOG.md"}
CL_FIELDS = ["原因", "修改前", "修改後", "影響 Command", "影響 Adapter", "影響 Test", "是否破壞 backward compatibility", "檔案"]


def current_counts():
    """The six baseline numbers, counted the way BASELINE_V2.md defines them."""
    reg = dsl.registry()
    pv = yaml_lite.load_file(os.path.join(ROOT, "registry", "provenance.yaml"))
    cm = yaml_lite.load_file(os.path.join(ROOT, "registry", "conflict_matrix.yaml"))
    src = io.open(os.path.join(HERE, "camera_dsl.py"), encoding="utf-8").read()
    continuity = len(set(re.findall(r'Diag\("(C\d\d)-', src)))
    tests = sum(len(run_tests.parse_tables(f)) for f in glob.glob(os.path.join(ROOT, "tests", "*.md")))
    return {"canonical_commands": len(reg.commands), "aliases": len(reg.aliases), "grammar_rules": len(pv["grammar"]),
            "compatibility_rules": len(reg.compat),
            "conflict_rules": len(cm["group_rules"]) + len(cm["pair_rules"]) + len(cm["semantic_rules"]) + continuity,
            "tests": tests}


def current_manifest():
    """SHA-256 of every skill file (not the two change-control files, not bytecode, not the git metadata of a clone)."""
    out = {}
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in ("__pycache__", ".git"))
        for fn in files:
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/")
            if rel in NOT_FINGERPRINTED or fn.endswith(".pyc"):
                continue
            with open(os.path.join(dirpath, fn), "rb") as fh:
                out[rel] = hashlib.sha256(fh.read()).hexdigest()
    return dict(sorted(out.items()))


def _baseline_block(text, tag):
    m = re.search(rf"<!-- BEGIN BASELINE: {tag} -->(.*?)<!-- END BASELINE -->", text, re.S)
    if not m:
        return None
    return [ln.strip() for ln in m.group(1).strip().split("\n") if ln.strip() and not ln.strip().startswith("```")]


def changelog_entries(text):
    """'## CL-NNN · date · title' sections holding '- field：value' items; indented lines continue a value."""
    entries = []
    for m in re.finditer(r"^## (CL-\d{3})[^\n]*\n(.*?)(?=^## CL-\d{3}|\Z)", text, re.M | re.S):
        fields, key = {}, None
        for ln in m.group(2).split("\n"):
            fm = re.match(r"^- ([^：:\n]+)[：:][ \t]*(.*)$", ln)
            if fm:
                key = fm.group(1).strip()
                fields[key] = fm.group(2).strip()
            elif key and ln[:1] in (" ", "\t") and ln.strip():
                fields[key] = (fields[key] + " " + ln.strip()).strip()
            elif ln.strip():
                key = None
        entries.append((m.group(1), fields))
    return entries


def baseline_audit(R):
    if not os.path.exists(BASELINE_FILE):
        R.add("BASELINE", "errors", "BASELINE_V2.md missing")
        return
    text = io.open(BASELINE_FILE, encoding="utf-8").read()
    if not os.path.exists(CHANGELOG_FILE):
        R.add("BASELINE", "errors", "CHANGELOG.md missing")
        return
    entries = changelog_entries(io.open(CHANGELOG_FILE, encoding="utf-8").read())
    for cid, f in entries:
        missing = [k for k in CL_FIELDS if not f.get(k)]
        if missing:
            R.add("BASELINE", "errors", f"CHANGELOG {cid}: missing field(s) {', '.join(missing)}")
    ids = [cid for cid, _ in entries]
    if len(ids) != len(set(ids)):
        R.add("BASELINE", "errors", "CHANGELOG: duplicate entry id")
    # frozen sets: no new or removed commands or aliases; grammar only through a declared bug fix
    declared = {t for _, f in entries for t in re.findall(r"[+-][A-Z][A-Z0-9_]*", f.get("文法變更", ""))}
    reg = dsl.registry()
    grammar = set(yaml_lite.load_file(os.path.join(ROOT, "registry", "provenance.yaml"))["grammar"])
    for tag, now, label, can_declare in (("commands", set(reg.commands), "canonical command", False),
                                         ("aliases", set(reg.aliases), "alias", False),
                                         ("grammar", grammar, "grammar rule", True)):
        block = _baseline_block(text, tag)
        if block is None:
            R.add("BASELINE", "errors", f"BASELINE_V2.md: block '{tag}' missing")
            continue
        base = set(" ".join(block).split())
        for sign, names in (("+", now - base), ("-", base - now)):
            for x in sorted(names):
                if can_declare and sign + x in declared:
                    continue
                R.add("BASELINE", "errors", f"V2 frozen: {label} {sign}{x} differs from V2_BASELINE"
                      + (" (allowed only as a bug fix declared in CHANGELOG '文法變更')" if can_declare else " (not allowed)"))
    # the six numbers
    counts = dict(ln.split(":", 1) for ln in (_baseline_block(text, "counts") or []))
    cur = current_counts()
    R.add("BASELINE", "info", "now vs V2_BASELINE: " + ", ".join(
        f"{k} {v}" + (f" (baseline {counts[k].strip()})" if k in counts and int(counts[k]) != v else "") for k, v in cur.items()))
    # every changed file is logged
    base_man = {}
    for ln in _baseline_block(text, "manifest") or []:
        h, rel = ln.split(None, 1)
        base_man[rel.strip()] = h
    if not base_man:
        R.add("BASELINE", "errors", "BASELINE_V2.md: manifest block missing")
        return
    cur_man = current_manifest()
    changed = sorted(p for p in set(base_man) | set(cur_man) if base_man.get(p) != cur_man.get(p))
    logged = {x.strip("`") for _, f in entries for x in re.split(r"[,，、;；\s]+", f.get("檔案", "")) if x.strip("`")}
    for p in changed:
        if p not in logged:
            state = "added" if p not in base_man else "removed" if p not in cur_man else "changed"
            R.add("BASELINE", "errors", f"{p} {state} since V2_BASELINE but no CHANGELOG entry lists it under 檔案")
    R.add("BASELINE", "info", f"files differing from V2_BASELINE: {len(changed)}; CHANGELOG entries: {len(entries)}")


# ------------------------------------------------------------------ publishing (public repository)

# The private-name list is never stored in the repository: the SHA-256 of a short name or word can be recovered by trying
# candidates (CL-052). The maintainer keeps it in a local file outside the repository, one SHA-256 per line ('#' starts a
# comment; add a line with `python audit.py --hash-term "<term>"`), and points CAMERA_DSL_PRIVATE_TERMS at it.
PRIVATE_TERMS_FILE = os.environ.get("CAMERA_DSL_PRIVATE_TERMS", "")
LOCAL_PATH = re.compile(r"(?<![A-Za-z0-9\\])[A-Za-z]:[\\/](?=[A-Za-z0-9._~\u0080-\uffff])|/(?:Users|home)/[A-Za-z0-9._-]+/")
OTHER_LOCAL = [   # (label, pattern) machine-specific locations and addresses that a public file must not carry
    ("home-relative path", re.compile(r"(?:^|(?<=[\s`'\"(=]))~/[A-Za-z0-9._-]+")),     # a path under the home folder, not the ~ of a test row
    ("network share path", re.compile(r"(?<![\w\\])\\\\[A-Za-z0-9._-]+\\[A-Za-z0-9$._-]+")),
    ("user profile folder", re.compile("(?i)[\\\\/]appdata[\\\\/]|" + "|".join("%" + v + "%" for v in ("userprofile", "appdata", "localappdata")))),
    ("private network address", re.compile(r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01])|169\.254)\.\d{1,3}\.\d{1,3}\b")),
]
BINARY_EXT = re.compile(r"\.(mp4|mov|webm|avi|mkv|png|jpe?g|webp|gif|bmp|tiff?|wav|mp3|flac|zip|7z|rar|tar|gz|safetensors|ckpt|pt|pth|bin|"
                        r"onnx|gguf|npy|npz|pkl)$", re.I)


def _private_term_hashes():
    """the maintainer's private-name list from CAMERA_DSL_PRIVATE_TERMS: None when the variable is not set on this machine,
    an empty set when it is set but no SHA-256 line can be read (a broken setup must not pass as a checked one)"""
    if not PRIVATE_TERMS_FILE:
        return None
    out = set()
    try:
        for ln in io.open(PRIVATE_TERMS_FILE, encoding="utf-8"):
            h = ln.split("#", 1)[0].strip().lower()
            if re.fullmatch(r"[0-9a-f]{64}", h):
                out.add(h)
    except (OSError, UnicodeDecodeError):
        pass
    return out


def _private_terms(text, hashes):
    """SHA-256 of every lowercase word, word pair and 2-6 character CJK run; returns the hashes that are private."""
    t = text.lower()
    cands = set()
    words = re.findall(r"[a-z0-9]+", t)
    cands |= set(words)
    cands |= {a + " " + b for a, b in zip(words, words[1:])}
    for run in re.findall(r"[\u3400-\u9fff]+", t):
        for n in range(2, 7):
            for i in range(len(run) - n + 1):
                cands.add(run[i:i + n])
    return {h for h in (hashlib.sha256(c.encode("utf-8")).hexdigest() for c in cands) if h in hashes}


def repo_files():
    """every file of the repository (hidden files included; .git and caches skipped) as (relative path, text or None):
    None for a binary file (a NUL byte, or not UTF-8)"""
    out = []
    for dp, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in (".git", "__pycache__"))
        for fn in sorted(files):
            path = os.path.join(dp, fn)
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            raw = open(path, "rb").read()
            try:
                text = None if b"\x00" in raw else raw.decode("utf-8")
            except UnicodeDecodeError:
                text = None
            out.append((rel, text))
    return out


def publish_audit(R):
    lic = os.path.join(ROOT, "LICENSE")
    if not os.path.exists(lic):
        R.add("PUBLISH", "errors", "LICENSE missing")
    elif "<COPYRIGHT_HOLDER>" in io.open(lic, encoding="utf-8").read():
        R.add("PUBLISH", "warnings", "LICENSE: fill in the copyright holder (the legal name of the rights owner) before publishing")
    hashes = _private_term_hashes()
    n = 0
    for rel, text in repo_files():
        if text is None:
            R.add("PUBLISH", "errors", f"{rel}: binary file (a public release carries text files only)")
            continue
        n += 1
        for i, line in enumerate(text.split("\n"), 1):
            m = LOCAL_PATH.search(line)
            if m:
                R.add("PUBLISH", "errors", f"{rel}:{i}: local absolute path '{line[max(0, m.start() - 10):m.end() + 20].strip()}'")
                break
        for label, pat in OTHER_LOCAL:
            for i, line in enumerate(text.split("\n"), 1):
                m = pat.search(line)
                if m:
                    R.add("PUBLISH", "errors", f"{rel}:{i}: {label} '{line[max(0, m.start() - 10):m.end() + 20].strip()}'")
                    break
        if hashes:
            for h in sorted(_private_terms(text, hashes)):
                R.add("PUBLISH", "errors", f"{rel}: private name or term (hash {h[:10]})")
    R.add("PUBLISH", "info", f"files checked for local paths, home and share paths and private addresses: {n}")
    if hashes is None:
        R.add("PUBLISH", "info", "private-name list not configured on this machine (CAMERA_DSL_PRIVATE_TERMS): names not checked")
    elif not hashes:   # the value itself is never printed: it is a local path
        R.add("PUBLISH", "errors", "CAMERA_DSL_PRIVATE_TERMS is set, but no SHA-256 line could be read from that file: private names not checked")
    else:
        R.add("PUBLISH", "info", f"private-name list: {len(hashes)} terms checked (CAMERA_DSL_PRIVATE_TERMS)")


def h3_status():
    """(h3_production_baseline_status, detail): COMPLETE when every local baseline profile holds its CONSTRAINED_PRODUCTION
    record (production shots) and its CAMERA_ONLY record (environment_only_baseline, 12 routes)"""
    import yaml_lite
    prof = yaml_lite.load_file(os.path.join(ROOT, "models", "minimax_h3_profile.yaml")) or {}
    ev = prof.get("reality_evidence", {}) or {}
    rows = []
    for pid in ("LOCAL_H3_T2VA_PDD8_Q_416", "LOCAL_H3_I2VA_PDD8_Q_416", "LOCAL_H3_FL2VA_PDD8_Q_416", "LOCAL_H3_L2VA_PDD8_Q_416",
                "LOCAL_H3_REF2VA_PDD8_Q_416"):
        e = ev.get(pid, {}) or {}
        cc = e.get("current_core_production_baseline") or {}
        constrained = len(e.get("production_shots", {}) or {}) + len((cc.get("production_shots", {}) or {}) if isinstance(cc, dict) else {})
        env = e.get("environment_only_baseline") or {}
        camera_only = len((env.get("production_shots", {}) or {}) if isinstance(env, dict) else {})
        rows.append(constrained >= 16 and camera_only == 12)
    return ("COMPLETE" if all(rows) else "INCOMPLETE"), f"{sum(rows)}/5 H3 modes hold CONSTRAINED_PRODUCTION and CAMERA_ONLY evidence"


# ------------------------------------------------------------------ PUBLIC_RELEASE_GATE

SECRET_RE = re.compile(r"sk-[A-Za-z0-9]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}"
                       r"|glpat-[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{30,}|AIza[0-9A-Za-z_-]{35}|npm_[A-Za-z0-9]{36}|pypi-[A-Za-z0-9_-]{50,}"
                       r"|AKIA[0-9A-Z]{16}|xox[abprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
                       r"|eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"     # a JSON web token
                       r"|AccountKey=[A-Za-z0-9+/=]{40,}|\"private_key_id\"\s*:"
                       r"|(?i:bearer\s+[A-Za-z0-9._~+/-]{20,}=*)|(?i:(?:authorization|x-api-key)\s*:\s*['\"]?[A-Za-z0-9._~+/-]{12,})"
                       r"|(?i:(?:api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][^'\"\s]{12,}['\"])")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
JUNK = re.compile(r"(\.pyc|\.pyo|\.tmp|\.bak|\.old|\.log|\.dmp|\.code-workspace|~)$|^(\.DS_Store|Thumbs\.db|desktop\.ini"
                  r"|\.coverage(\..+)?|coverage\.xml)$", re.I)


def release_checks():
    """Checks only a public release needs (the audits cover the rest). Returns {name: (ok, detail)}."""
    out = {}
    lic = os.path.join(ROOT, "LICENSE")
    txt = io.open(lic, encoding="utf-8").read() if os.path.exists(lic) else ""
    holder = re.search(r"^Copyright \(c\) \d{4} (.+)$", txt, re.M)
    ok = txt.startswith("MIT License") and bool(holder) and "<COPYRIGHT_HOLDER>" not in txt
    out["LICENSE"] = (ok, f"MIT, {holder.group(0)}" if holder else "missing or not filled in")
    secrets, emails, junk, big, media = [], [], [], [], []
    for dp, dirs, files in os.walk(ROOT):
        for d in dirs:
            if d in ("__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints", ".vscode", ".idea", "node_modules",
                     "htmlcov"):
                junk.append(os.path.relpath(os.path.join(dp, d), ROOT))
        dirs[:] = [d for d in dirs if d != ".git"]
        for fn in files:
            path = os.path.join(dp, fn)
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            if JUNK.search(fn) or (fn.startswith(".env") and fn != ".env.example"):
                junk.append(rel)
            if os.path.getsize(path) > 1_000_000:
                big.append(rel)
            if BINARY_EXT.search(fn):
                media.append(rel)
    for rel, t in repo_files():   # every file, whatever its extension
        if t is None:
            media.append(rel)
            continue
        if SECRET_RE.search(t):
            secrets.append(rel)
        if EMAIL_RE.search(t):
            emails.append(rel)
    media = sorted(set(media))
    out["SECRETS_AND_EMAILS"] = (not secrets and not emails, f"secrets in {secrets}, e-mail addresses in {emails}"
                                 if secrets or emails else "none found")
    out["REPO_HYGIENE"] = (not junk and not big and not media, f"junk {junk}, files over 1 MB {big}, binary or media files {media}"
                           if junk or big or media else "no caches, temp files, environment files, binaries or oversized files")
    sk = io.open(os.path.join(ROOT, "SKILL.md"), encoding="utf-8").read()
    fm = re.match(r"^---\nname: ([^\n]+)\ndescription: ([^\n]+)\n", sk)
    ok = bool(fm) and fm.group(1).strip() == os.path.basename(ROOT) and 0 < len(fm.group(2)) <= 1024
    out["SKILL_MANIFEST"] = (ok, f"name {fm.group(1).strip()}, description {len(fm.group(2))} chars" if fm else "bad frontmatter")
    return out


def release_gate():
    R = Report()
    for audit_fn in (research_audit, command_audit, semantic_audit, conflict_audit, model_audit, model_docs_audit, reality_audit,
                     schema_audit, tests_audit, files_audit, cases_audit, publish_audit, baseline_audit):
        audit_fn(R)
    e, w = R.counts()
    total = passed = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "tests", "*.md"))):
        for row in run_tests.parse_tables(f):
            total += 1
            passed += not run_tests.evaluate(row)
    for _name, fl in run_tests.snapshot_check():   # the frozen H3 camera text and wrapper prompts (CAMERA_CORE_CHANGES = 0)
        total += 1
        passed += not fl
    for _name, fl in run_tests.example_library_check():   # the Production Example Library (CL-057)
        total += 1
        passed += not fl
    sec = lambda name: R.sections.get(name, {"errors": [], "warnings": []})
    extra = release_checks()
    names = next((x for x in sec("PUBLISH").get("info", []) if x.startswith("private-name list")), "")
    gate = [
        ("LICENSE", *extra["LICENSE"]),
        ("PRIVACY", not sec("PUBLISH")["errors"], "no local, home or share paths, no private addresses; " + names if not sec("PUBLISH")["errors"]
         else "; ".join(sec("PUBLISH")["errors"][:3])),
        ("THIRD_PARTY_CONTENT", not sec("RESEARCH")["errors"] and not sec("RESEARCH")["warnings"],
         next((x for x in sec("RESEARCH").get("info", []) if x.startswith("license register")),
              "license register kept by the maintainer, not in this copy; " + next((x for x in sec("RESEARCH").get("info", []) if x.startswith("SOURCES.md")), ""))),
        ("SECRETS_AND_EMAILS", *extra["SECRETS_AND_EMAILS"]),
        ("REPO_HYGIENE", *extra["REPO_HYGIENE"]),
        ("SKILL_MANIFEST", *extra["SKILL_MANIFEST"]),
        ("DSL_BASELINE", not sec("BASELINE")["errors"],
         next((x for x in sec("BASELINE").get("info", []) if x.startswith("now vs")), "")),
        ("AUDIT", e == 0 and w == 0, f"{e} errors, {w} warnings"),
        ("TESTS", passed == total, f"{passed}/{total}"),
    ]
    reality = os.path.join(ROOT, "tests", "reality", "minimax_h3", "10_results.md")
    rf = re.search(r"^FINAL: (.+)$", io.open(reality, encoding="utf-8").read(), re.M) if os.path.exists(reality) else None
    print("PUBLIC_RELEASE_GATE\n")
    for name, ok, detail in gate:
        print(f"{name + ':':22s}{'PASS' if ok else 'FAIL'}  ({detail})")
    status, status_detail = h3_status()
    print("\nSTATUS:")
    print(f"  - h3_production_baseline_status: {status} ({status_detail}; the v1.0 production baseline)")
    print("  - h3_full_command_space_validation: PARTIAL (by design: not every command x mode x profile x direction x shot size x "
          "landing x angle is measured; anything outside a measured scope is UNVERIFIED)")
    print(f"  - 42-cell Ref2VA reality matrix (historical, frozen): FINAL {rf.group(1) if rf else 'records kept by the maintainer, not in this copy'}")
    print("\nOPEN_ITEMS (not blocking):")
    print("  - README Maintainer line: optional (left out; no personal name or address is published)")
    print("  - Submission terms of the target platform: check them against LICENSE and the source register")
    final = all(ok for _, ok, _ in gate)
    print(f"\nFINAL: {'PASS' if final else 'FAIL'}")
    for sec_name, v in R.sections.items():
        for x in v["errors"]:
            print(f"  {sec_name} ERROR: {x}")
    return 0 if final else 1


def main(argv):
    if "--release" in argv:
        return release_gate()
    if "--hash-term" in argv:
        term = argv[argv.index("--hash-term") + 1].lower()
        print(hashlib.sha256(term.encode("utf-8")).hexdigest())
        return 0
    if "--sync" in argv:
        sync()
        print("synced: registry alias lists, provenance commands, reference tables, schema examples, example cases")
        dsl._REG = None
    R = Report()
    research_audit(R)
    command_audit(R)
    semantic_audit(R)
    conflict_audit(R)
    model_audit(R)
    model_docs_audit(R)
    reality_audit(R)
    schema_audit(R)
    tests_audit(R)
    files_audit(R)
    cases_audit(R)
    publish_audit(R)
    baseline_audit(R)
    e, w = R.counts()
    if "--json" in argv:
        print(json.dumps({"errors": e, "warnings": w, "sections": R.sections}, ensure_ascii=False, indent=1))
    else:
        for sec, v in R.sections.items():
            print(f"== {sec} AUDIT: {len(v['errors'])} error(s), {len(v['warnings'])} warning(s)")
            for x in v["info"]:
                print("   info:", x)
            for x in v["errors"]:
                print("   ERROR:", x)
            for x in v["warnings"]:
                print("   warning:", x)
        print(f"\nAUDIT_ERRORS: {e}\nAUDIT_WARNINGS: {w}")
    return 1 if e else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
