# -*- coding: utf-8 -*-
"""Tests of the H3 content contract and the evidence relation (scripts/h3_wrappers.py, scripts/adapters.py; CHANGELOG CL-059):
who each subject of the camera text is, the cut times, the required fields, camera text against action, the exit codes of
the wrapper CLI, and EXACT / RELATED routing.

Run by scripts/run_tests.py as one more group. They live outside tests/*.md on purpose: rows there feed the frozen H3
camera-text snapshot corpus, and these inputs must not change that snapshot."""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import adapters  # noqa: E402
import camera_dsl as dsl  # noqa: E402
import h3_wrappers as wr  # noqa: E402

I2VA = "LOCAL_H3_I2VA_PDD8_Q_416"
WRAPPER = os.path.join(ROOT, "scripts", "h3_wrappers.py")
FAKE_LINT = ("def lint(p, n_refs=None, ref_names=(), frames=None, entry=None, mode=None):\n"
             "    return [f'n_refs={n_refs} frames={frames} mode={mode}'], []\n")


def content(mode, **kw):
    c = wr.sample_content(mode)
    c.update(kw)
    return c


def two_shots(cut2, **kw):
    """I2VA content for "S1: /MS /STATIC\\nS2: /CU /STATIC" with the given cut of [Shot 2]."""
    c = content("i2va", **kw)
    c["shots"] = [{"opening": c["opening"], "action": "She looks up.", "cut": ""}, {"opening": "", "action": "She smiles.", "cut": cut2}]
    return c


TWO = "S1: /MS /STATIC\nS2: /CU /STATIC"
THREE_REFS = ["<Subject 1> is the young woman whose facial identity comes from <Picture 1>.",
              "<Subject 2> is the man whose facial identity comes from <Picture 2>.",
              "<Subject 3> is the old woman whose facial identity comes from <Picture 3>."]


def has(items, *words):
    return any(all(w in x for w in words) for x in items)


def cli(args, env_extra=None, drop=("CAMERA_DSL_H3_LAB",)):
    env = {k: v for k, v in os.environ.items() if k not in drop}
    env.update({"PYTHONIOENCODING": "utf-8"}, **(env_extra or {}))
    p = subprocess.run([sys.executable, "-B", WRAPPER] + args, capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, p.stdout + p.stderr


def route(d, profile=I2VA):
    out = adapters.render(dsl.analyze(d), model="minimax_h3", h3_profile_id=profile)
    return out["routing"], adapters.routing_text(out["routing"], "en")


def run():
    """[(test name, [failure, ...])]"""
    rows = []
    tmp = tempfile.mkdtemp(prefix="h3_contracts_")

    def check(name, fn):
        try:
            fails = fn() or []
        except Exception as e:   # noqa: BLE001
            fails = [f"exception {type(e).__name__}: {e}"]
        rows.append((f"h3_contracts: {name}", fails))

    def expect(cond, why):
        return [] if cond else [why]

    # ---- subjects
    def reaction_c_unbound():
        r = wr.wrap_dsl("ref2va", "/CU /REACTION:C", content("ref2va", subjects=THREE_REFS))
        return expect(has(r["errors"], "subject C") and "{C}" in r["prompt"], f"errors {r['errors']}")
    check("REACTION:C with nobody bound to C is an error", reaction_c_unbound)

    def reaction_c_bound():
        r = wr.wrap_dsl("ref2va", "/CU /REACTION:C", content("ref2va", subjects=THREE_REFS, subject_map={"C": "<Subject 3>"}))
        return (expect(not r["errors"], f"errors {r['errors']}")
                + expect("A close-up frames <Subject 3> head and shoulders." in r["prompt"]
                         and "<Subject 3>'s reacting face" in r["prompt"], r["cameras"][0]))
    check("REACTION:C bound to <Subject 3> frames <Subject 3>", reaction_c_bound)

    def ots_undefined():
        r = wr.wrap_dsl("ref2va", "/MCU /OTS:A>B", content("ref2va"))
        return expect(has(r["errors"], "<Subject 2>", "subject_definitions"), f"errors {r['errors']}")
    check("OTS:A>B with only <Subject 1> defined is an error", ots_undefined)

    def reaction_b_frames_b():
        r = wr.wrap_dsl("i2va", "/CU /REACTION:B", content("i2va", subject_name="the woman", subject_name_b="the man"))
        cam = r["cameras"][0]
        return expect(not r["errors"] and "frames the man head and shoulders" in cam and "the man's reacting face" in cam
                      and "the woman" not in cam, f"{cam} | errors {r['errors']}")
    check("REACTION:B frames B, the one who reacts", reaction_b_frames_b)

    def scene_is_subject_1():
        subs = ["<Subject 1> is the stone courtyard shown in <Picture 1>.",
                "<Subject 2> is the young woman whose facial identity comes from <Picture 2>.",
                "<Subject 3> is the man whose facial identity comes from <Picture 3>."]
        r = wr.wrap_dsl("ref2va", "/MCU /OTS:A>B", content("ref2va", subjects=subs, subject_map={"A": "<Subject 2>", "B": "<Subject 3>"},
                                                            opening="<Subject 2> and <Subject 3> stand in <Subject 1>."))
        return (expect(not r["errors"], f"errors {r['errors']}")
                + expect("behind <Subject 2>'s shoulder looking at <Subject 3>" in r["prompt"]
                         and "A medium close-up frames <Subject 3> from the chest up." in r["prompt"], r["cameras"][0]))
    check("a scene as <Subject 1>: subject_map puts the characters on <Subject 2> and <Subject 3>", scene_is_subject_1)

    def base_without_name():
        c = content("i2va")
        del c["subject_name"]
        r = wr.wrap_dsl("i2va", "/MS /PAN:R", c)
        return expect(has(r["errors"], "the shot's subject (A)") and "{SUBJECT}" in r["prompt"], f"errors {r['errors']}")
    check("Base modes: a subject with no name is an error, never the sample name", base_without_name)

    def ref_label_only():
        r = wr.wrap_dsl("ref2va", "/MS /PAN:R", content("ref2va", subject_map={"A": "the woman"}))
        return expect(has(r["errors"], "<Subject N> label"), f"errors {r['errors']}")
    check("Ref2VA: subject_map names a <Subject N> label", ref_label_only)

    def base_no_labels():
        r = wr.wrap_dsl("i2va", "/MS /PAN:R", content("i2va", subject_map={"A": "<Subject 1>"}))
        return expect(has(r["errors"], "Base modes call people by name"), f"errors {r['errors']}")
    check("Base modes: a <Subject N> label is an error", base_no_labels)

    def placeholder_in_content():
        r = wr.wrap_dsl("i2va", "/MS /PAN:R", content("i2va", action="{B} waves."))
        return expect(has(r["errors"], "still holds {B}"), f"errors {r['errors']}")
    check("a placeholder left in the content is an error", placeholder_in_content)

    def pov_owner():
        r = wr.wrap_dsl("i2va", "/MS /POV", content("i2va"))
        return expect(has(r["errors"], "subject VIEWER"), f"errors {r['errors']}")
    check("/POV without an owner names nobody: an error", pov_owner)

    # ---- time line
    def no_cut():
        r = wr.wrap_dsl("i2va", TWO, two_shots(""))
        return expect(has(r["errors"], "[Shot 2] has no cut time"), f"errors {r['errors']}")
    check("[Shot 2] without a cut time is an error", no_cut)

    def late_cut():
        r = wr.wrap_dsl("i2va", TWO, two_shots("At 00:20.000, the camera cuts to"))
        return expect(has(r["errors"], "cuts at 20.000 s", "5.17 s long"), f"errors {r['errors']}")
    check("a cut after the end of the video is an error", late_cut)

    def decreasing():
        c = two_shots("At 00:03.000, the camera cuts to")
        c["shots"].append({"opening": "", "action": "She nods.", "cut": "At 00:02.000, the camera cuts to"})
        r = wr.wrap_dsl("i2va", TWO + "\nS3: /MCU /STATIC", c)
        return expect(has(r["errors"], "[Shot 3]", "not after the cut before it"), f"errors {r['errors']}")
    check("cut times increase", decreasing)

    def good_cut():
        r = wr.wrap_dsl("i2va", TWO, two_shots("At 00:02.500, the camera cuts to"))
        return expect(not r["errors"] and "[Shot 2] At 00:02.500, the camera cuts to" in r["prompt"], f"errors {r['errors']}")
    check("a valid two-shot time line passes", good_cut)

    def first_shot_time():
        c = two_shots("At 00:02.500, the camera cuts to")
        c["shots"][0]["cut"] = "At 00:01.000, the camera cuts to"
        r = wr.wrap_dsl("i2va", TWO, c)
        return expect(has(r["errors"], "[Shot 1] takes no cut time"), f"errors {r['errors']}")
    check("[Shot 1] takes no cut time", first_shot_time)

    def zero_duration():
        r = wr.wrap_dsl("l2va", "/MS /STATIC", content("l2va", duration=0))
        return expect(has(r["errors"], "duration must be a positive number"), f"errors {r['errors']}")
    check("L2VA duration 0 is an error", zero_duration)

    def text_duration():
        a = wr.wrap_dsl("fl2va", "/MS /STATIC", content("fl2va", duration="5.17"))
        b = wr.wrap_dsl("fl2va", "/MS /STATIC", content("fl2va"))
        return expect(a["prompt"] == b["prompt"] and not a["errors"], f"errors {a['errors']}")
    check("a duration written as text works as before", text_duration)

    def length_from_frames():
        c = two_shots("At 00:06.000, the camera cuts to", frames=124)
        del c["duration"]
        r = wr.wrap_dsl("i2va", TWO, c)
        return expect(has(r["errors"], "5.17 s long"), f"errors {r['errors']}")
    check("the video length comes from frames when no duration is given", length_from_frames)

    def unknown_length():
        c = two_shots("At 00:02.500, the camera cuts to")
        del c["duration"]
        r = wr.wrap_dsl("i2va", TWO, c)
        return expect(not r["errors"] and has(r["warnings"], "not checked against the video length"), f"{r['errors']} {r['warnings']}")
    check("an unknown video length is warned about, not an error", unknown_length)

    # ---- required fields
    def ref_empty():
        r = wr.wrap_dsl("ref2va", "/MS /PAN:R", content("ref2va", subjects=[], retention=[], summary="", soundscape=""))
        want = ("subject_definitions", "summary is empty", "retention_analysis", "overall_soundscape")
        return [f"no error for {w}: {r['errors']}" for w in want if not has(r["errors"], w)]
    check("Ref2VA: empty required fields are errors", ref_empty)

    def base_empty_sound():
        r = wr.wrap_dsl("t2va", "/MS /PAN:R", content("t2va", soundscape=""))
        return expect(has(r["errors"], "overall_soundscape is empty"), f"errors {r['errors']}")
    check("Base modes: an empty soundscape is an error", base_empty_sound)

    def sample_clean():
        bad = []
        for mode in wr.MODES:
            for d in ("/MS /PAN:R", "/MS /DOLLYIN:MS>MCU:SLOW", "/MFS /TRACKSIDE:R"):
                r = wr.wrap_dsl(mode, d, wr.sample_content(mode))
                if r["errors"]:
                    bad.append(f"{mode} {d}: {r['errors']}")
        return bad
    check("the sample content has no content error for a one-shot DSL in any mode", sample_clean)

    # ---- camera text against the action (warned, never rewritten)
    def orbit_walk():
        r = wr.wrap_dsl("i2va", "/MS /ORBIT:R:45", content("i2va", subject_name="the woman", action="The woman turns around and walks toward the doorway."))
        return (expect(has(r["warnings"], "/ORBIT", "opposite things") and not r["errors"], f"{r['warnings']} {r['errors']}")
                + expect("The woman stays in place and does not turn." in r["prompt"] and "The woman turns around and walks toward the doorway." in r["prompt"],
                         "the wrapper changed the camera text or the action"))
    check("ORBIT and a subject who turns and walks: warned, nothing rewritten", orbit_walk)

    def trackside_still():
        r = wr.wrap_dsl("i2va", "/MFS /TRACKSIDE:R", content("i2va"))
        return expect(has(r["warnings"], "/TRACKSIDE", "stands still"), f"{r['warnings']}")
    check("TRACKSIDE and a subject who stands still: warned", trackside_still)

    def orbit_still():
        r = wr.wrap_dsl("i2va", "/MS /ORBIT:R:45", content("i2va"))
        return expect(not has(r["warnings"], "opposite things"), f"{r['warnings']}")
    check("ORBIT and a subject who stands still: no warning", orbit_still)

    def eyeline_look_away():
        r = wr.wrap_dsl("i2va", "/MS /EYELINE:A>OFFL", content("i2va", action="She looks away."))
        return expect(has(r["warnings"], "/EYELINE", "looks away"), f"{r['warnings']}")
    check("an eyeline held for the whole video and a subject who looks away: warned", eyeline_look_away)

    def lines_run():
        r = wr.wrap_dsl("i2va", "/MS /ORBIT:R:45", content("i2va", action="The floor lines run toward the far end."))
        return expect(not has(r["warnings"], "opposite things"), f"{r['warnings']}")
    check("lines that run toward the far end are not a walking subject", lines_run)

    # ---- the wrapper CLI
    def cli_pass():
        rc, out = cli(["i2va", "/MS /TILT:DOWN"])
        return expect(rc == 0 and "CHECK: PASS" in out and "NOTE: no content file" in out, f"exit {rc}: {out[-300:]}")
    check("CLI: a prompt with no problem exits 0 (CHECK: PASS)", cli_pass)

    t2va_pic = os.path.join(tmp, "t2va_picture.json")
    io.open(t2va_pic, "w", encoding="utf-8").write(json.dumps(content("t2va", opening="The woman shown in <Picture 1> stands in a courtyard.")))

    def cli_fail():
        rc, out = cli(["t2va", "/MS /STATIC", t2va_pic])
        return expect(rc == 1 and "STRUCTURE: T2VA has no reference pictures" in out and "CHECK: FAIL" in out, f"exit {rc}: {out[-300:]}")
    check("CLI: a problem exits 1 (CHECK: FAIL)", cli_fail)

    def cli_draft():
        rc, out = cli(["t2va", "/MS /STATIC", t2va_pic, "--draft"])
        return expect(rc == 0 and "CHECK: DRAFT" in out, f"exit {rc}: {out[-300:]}")
    check("CLI: --draft reports the problem and exits 0", cli_draft)

    def cli_missing():
        rc, out = cli(["i2va", "/MS /STATIC", os.path.join(tmp, "no_such_content.json")])
        return expect(rc == 2 and "ERROR: cannot read the content file" in out and "Traceback" not in out, f"exit {rc}: {out[-300:]}")
    check("CLI: an unreadable content file exits 2 with one line, no traceback", cli_missing)

    def cli_dsl_error():
        rc, out = cli(["i2va", "/MS /CU"])
        return expect(rc == 2 and "ERROR: DSL errors" in out and "Traceback" not in out, f"exit {rc}: {out[-300:]}")
    check("CLI: a DSL error exits 2", cli_dsl_error)

    def cli_lint_skipped():
        rc, out = cli(["i2va", "/MS /TILT:DOWN", "--lint"])
        return expect(rc == 0 and "LINT: SKIPPED" in out, f"exit {rc}: {out[-300:]}")
    check("CLI: --lint without the lab says SKIPPED", cli_lint_skipped)

    def cli_lint_args():
        lab = os.path.join(tmp, "lab")
        os.makedirs(lab)
        io.open(os.path.join(lab, "h3_prompt_lint.py"), "w", encoding="utf-8").write(FAKE_LINT)
        c3 = os.path.join(tmp, "ref_three.json")
        io.open(c3, "w", encoding="utf-8").write(json.dumps(content("ref2va", n_refs=3)))
        rc, out = cli(["ref2va", "/MS /STATIC", c3, "--lint"], env_extra={"CAMERA_DSL_H3_LAB": lab}, drop=())
        return expect(rc == 1 and "LINT ERROR: n_refs=3 frames=124 mode=ref2va" in out, f"exit {rc}: {out[-300:]}")
    check("CLI: --lint gets n_refs and frames from the content, and a lint error exits 1", cli_lint_args)

    # ---- evidence relation (the review probes: speed, amount, sequence, extra command)
    def exact():
        R, _ = route("/MS /TILT:DOWN")
        r = R[0]
        return expect(r["evidence_relation"] == "EXACT" and r["applicability"] == "VERIFIED" and "TILT" in r["production_routes"], str(r)[:300])
    check("routing: the measured DSL is EXACT and VERIFIED", exact)

    for d, why in (("/MS /TILT:DOWN:FAST", "another speed"), ("/MS /TILT:DOWN:30", "another amount"),
                   ("0-1s: /MS /TILT:DOWN 1-5s: /DOLLYIN", "a time sequence"), ("/MS /EYELEVEL /TILT:DOWN", "an extra command")):
        def related(d=d):
            R, text = route(d)
            r = R[0]
            rel = [x for x in r.get("related_routes", []) if x["canonical"] == "TILT"]
            return (expect(r["evidence_relation"] == "RELATED" and r["applicability"] == "UNVERIFIED", f"{r['evidence_relation']} {r['applicability']}")
                    + expect("TILT" not in r["production_routes"] and rel and rel[0]["measured"] == ["/MS /TILT:DOWN"], str(r.get("related_routes"))[:300])
                    + expect("TILT related evidence (not applied; measured with /MS /TILT:DOWN)" in text and "TILT production route" not in text, text[:400]))
        check(f"routing: {why} ({d}) is RELATED, the validated grade is not applied", related)

    def wrapper_prints_relation():
        r = wr.wrap_dsl("i2va", "/MS /TILT:DOWN:FAST", content("i2va"), profile=I2VA)
        text = adapters.routing_text(r["render"]["routing"], "en")
        return expect("evidence relation: RELATED" in text, text[:300])
    check("routing: the wrapper's routing block carries the relation", wrapper_prints_relation)

    shutil.rmtree(tmp, ignore_errors=True)
    return rows


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    res = run()
    bad = [(n, f) for n, f in res if f]
    for n, f in bad:
        print("FAIL", n, "->", f[:3])
    print(f"{len(res) - len(bad)}/{len(res)} passed")
    sys.exit(1 if bad else 0)
