# -*- coding: utf-8 -*-
"""Tests of the Production Example Library (examples/production_library, scripts/example_library.py; CHANGELOG CL-057).

Run by scripts/run_tests.py as one more group. They live outside tests/*.md on purpose: rows there feed the frozen H3
camera-text snapshot corpus, and the library must not change that snapshot."""
import hashlib
import io
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import camera_dsl as dsl  # noqa: E402
import example_library as lib  # noqa: E402
import yaml_lite  # noqa: E402

# the registry is the authority; the library may not touch it (frozen at the library's build, CL-057)
REGISTRY_SHA256 = {
    "registry/canonical_commands.yaml": "2edf4474a5ae00318f08c05502f313b10b9e24f14f12a30a0316f5e1a45ce5ba",
    "registry/aliases.yaml": "f501d8fd9ac3de7f0d68e598eb292fed9614f4d4884ff87052abb27150881e90",
}
# examples the resolver must never settle on its own (spec 10.3)
MUST_ASK = ["EX-014", "EX-028", "EX-034", "EX-039", "EX-041", "EX-044", "EX-045", "EX-047", "EX-052", "EX-053", "EX-056",
            "EX-057", "EX-058", "EX-059", "EX-060", "EX-063", "EX-064", "EX-065", "EX-066"]
# phrases that stay example labels and may never become aliases (spec 7)
NOT_ALIASES = ["移鏡", "跟鏡", "升鏡", "降鏡", "俯仰", "變焦", "低機位", "遮擋轉場", "慢推近", "急拉遠", "環繞升鏡", "跟跑鏡頭", "搖鏡找人",
               "俯拍孤獨", "仰拍英雄", "前景穿越", "俯仰連接", "軌道運鏡", "滑動運鏡", "變焦運鏡", "升降運鏡", "轉場運鏡", "POV 運鏡", "無人機運鏡"]
QUERIES = [("慢推近", "EX-049"), ("急拉遠", "EX-050"), ("仰拍英雄", "EX-055"), ("俯拍孤獨", "EX-054"), ("橫移揭示", "EX-048"),
           ("過肩跟拍", "EX-043"), ("遮擋轉場", "EX-047"), ("飛升拉鏡", "EX-005"), ("時間凝滯回眸", "EX-022"), ("拉出", "EX-028"),
           ("搖鏡找人", "EX-053"), ("环绕升镜", "EX-051"), ("无人机运镜", "EX-066"), ("dolly zoom", "EX-060"), ("POV運鏡", "EX-065"),
           ("推鏡", "EX-031"), ("移鏡", "EX-034"), ("慢动作挡剑", "EX-023")]
SEED_FIXED = ["EX-002", "EX-005", "EX-007", "EX-009", "EX-017", "EX-027"]
README_EN = "This library maps natural-language filmmaking situations to candidate Camera DSL. It is an example/retrieval layer, not a new camera-language authority."
README_ZH = "這個案例庫負責把自然語言／敘事情境對應到候選 Camera DSL。它不是新的 Camera 語義來源，也不會擴充 canonical commands。"


def run():
    """[(test name, [failure, ...])]"""
    rows = []

    def check(name, fn):
        try:
            fails = fn() or []
        except Exception as e:   # noqa: BLE001
            fails = [f"exception {type(e).__name__}: {e}"]
        rows.append((f"example_library: {name}", fails))

    exs = lib.load_examples()
    schema = yaml_lite.load_file(os.path.join(lib.LIB_DIR, "schema.yaml"))
    classes = set(schema["mapping_classes"])
    by_id = {e["id"]: e for e in exs}

    # seed integrity
    check("66 examples", lambda: [] if len(exs) == 66 else [f"{len(exs)} examples"])
    check("ids unique", lambda: [] if len(by_id) == len(exs) else ["duplicate ids"])
    check("30 narrative + 36 technique", lambda: [f"{b}: {n}" for b, n in (("NARRATIVE_30", 30), ("TECHNIQUE_36", 36))
                                                  if sum(e["batch"] == b for e in exs) != n])

    def well_formed():
        bad = []
        for e in exs:
            for k in ("id", "title_zh", "batch", "mapping_class", "natural_language_intent_zh", "camera_dsl", "camera_semantics", "tags"):
                if k not in e or (k not in ("camera_dsl",) and not e[k]):
                    bad.append(f"{e.get('id')}: {k} missing or empty")
            if e.get("mapping_class") not in classes:
                bad.append(f"{e['id']}: unknown mapping_class {e.get('mapping_class')}")
            if e["mapping_class"] in schema["needs_context_classes"]:
                if len(e.get("candidates") or []) < 2 or not e.get("question_zh"):
                    bad.append(f"{e['id']}: a needs-context example needs two or more candidates and a question")
            elif e.get("candidates"):
                bad.append(f"{e['id']}: candidates belong to needs-context classes only")
            if (e["mapping_class"] == "MULTI_SHOT") != bool(e.get("shots")):
                bad.append(f"{e['id']}: shots and MULTI_SHOT go together")
            if set(e.get("non_camera") or {}) - set(schema["non_camera_keys"]):
                bad.append(f"{e['id']}: unknown non_camera keys {sorted(set(e['non_camera']) - set(schema['non_camera_keys']))}")
            if any(" " in t or not t.startswith("/") for t in e["camera_dsl"]):
                bad.append(f"{e['id']}: camera_dsl must hold single command tokens")
        return bad
    check("every example well formed", well_formed)

    # DSL validity: every string the example names parses, with canonical names only and no ERROR
    for e in exs:
        def valid(e=e):
            bad = []
            for d in lib.all_dsl(e):
                v = lib.validate_dsl(d)
                if v["status"] == "ERROR":
                    bad.append(f"{d}: ERROR " + "; ".join(f"[{x['rule']}] {x['message']}" for x in v["diagnostics"] if x["type"] == "ERROR"))
                bad += [f"{d}: not a canonical name: {x}" for x in v["not_canonical"]] + [f"{d}: unknown command {x}" for x in v["unknown"]]
            return bad
        check(f"{e['id']} DSL valid", valid)

    # ambiguity preserved
    for eid in MUST_ASK:
        def asks(eid=eid):
            r = lib.resolve_example(eid)
            bad = [] if r["needs_context"] else ["resolved without context"]
            bad += [] if len(r["candidate_dsl"]) >= 2 else [f"only {len(r['candidate_dsl'])} candidate"]
            bad += [] if r["question_zh"] else ["no question"]
            return bad
        check(f"{eid} asks instead of choosing", asks)
    check("every needs-context example asks", lambda: [e["id"] for e in exs if e["mapping_class"] in schema["needs_context_classes"]
                                                       and not lib.resolve_example(e["id"])["needs_context"]])

    def choose():
        r = lib.resolve_example("EX-028", context={"candidate": 2})
        return [] if (not r["needs_context"] and r["candidate_dsl"] == ["/ZOOMOUT:ECU>MS"]) else [str(r["candidate_dsl"])]
    check("a stated choice resolves to that candidate only", choose)

    # non-camera protection
    check("EX-023 adds no camera move", lambda: [] if lib.resolve_example("EX-023")["candidate_dsl"] == [] else ["camera DSL added"])
    check("EX-026 adds no camera move", lambda: [] if lib.resolve_example("EX-026")["candidate_dsl"] == [] else ["camera DSL added"])

    def ex025():
        r = lib.resolve_example("EX-025")
        st = dsl.analyze(r["candidate_dsl"][0])["shots"][0]["state"] if r["candidate_dsl"] else None
        return [] if (r["candidate_dsl"] == ["/CU"] and st and not st["movement"]) else [str(r["candidate_dsl"])]
    check("EX-025 keeps only the closing close-up, no move", ex025)
    check("non_camera never holds camera commands", lambda: [f"{e['id']}: {v}" for e in exs for vs in (e.get("non_camera") or {}).values()
                                                            for v in vs if str(v).startswith("/")])

    # the registry stays the authority
    reg = dsl.registry()
    names = {lib._norm(n) for n in list(reg.commands) + [str(a) for a in reg.aliases]}
    check("24 phrases stay example labels, not aliases", lambda: [p for p in NOT_ALIASES if lib._norm(p) in names])
    check("example titles are not commands or aliases", lambda: [e["title_zh"] for e in exs if lib._norm(e["title_zh"]) in names])
    check("registry files unchanged", lambda: [f for f, h in REGISTRY_SHA256.items()
                                               if hashlib.sha256(open(os.path.join(ROOT, f), "rb").read()).hexdigest() != h])
    check("104 commands and 244 aliases", lambda: [] if (len(reg.commands), len(reg.aliases)) == (104, 244)
          else [f"{len(reg.commands)} commands, {len(reg.aliases)} aliases"])

    # retriever and resolver
    for q, want in QUERIES:
        check(f"search {q!r} finds {want}", lambda q=q, want=want: [] if (lambda h: h and h[0]["example_id"] == want)(lib.search_examples(q))
              else [str([(h["example_id"], h["match_score"]) for h in lib.search_examples(q)])])
    check("search is deterministic", lambda: [] if lib.search_examples("拉鏡", 10) == lib.search_examples("拉鏡", 10) else ["order changed"])

    def fields():
        r = lib.search_and_resolve("慢推近")
        need = ("example_id", "match_score", "mapping_class", "candidate_dsl", "non_camera", "ambiguity", "needs_context", "warnings", "camera")
        return [k for k in need if k not in r] + ([] if set(r["camera"]) >= {"dsl", "semantics"} else ["camera.dsl / camera.semantics"])
    check("resolution carries every field", fields)
    check("every seed change is documented", lambda: [i for i in SEED_FIXED if not by_id[i].get("build_notes")])

    # docs
    def docs():
        return [f for f, text in lib.render_docs().items() if io.open(os.path.join(lib.LIB_DIR, f), encoding="utf-8").read() != text]
    check("narrative_30.md and technique_36.md match the data", docs)

    def readme():
        t = io.open(os.path.join(lib.LIB_DIR, "README.md"), encoding="utf-8").read()
        return [s[:30] for s in (README_EN, README_ZH) if s not in t]
    check("library README states its role in both languages", readme)
    return rows


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    res = run()
    bad = [(n, f) for n, f in res if f]
    for n, f in bad:
        print("FAIL", n, "->", f[:3])
    print(f"{len(res) - len(bad)}/{len(res)} passed")
    sys.exit(1 if bad else 0)
