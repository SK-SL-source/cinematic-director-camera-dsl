# -*- coding: utf-8 -*-
"""Production Example Library (CL-057): everyday filmmaking situations mapped to candidate Camera DSL.

An example / retrieval layer, not a camera-language authority. registry/canonical_commands.yaml defines every command;
the library only points to commands, and every candidate is checked again by the parser and the conflict rules before it
is returned. A phrase that leaves the camera open comes back with its candidates and a question, never with a guess, and
effects, editing and time effects stay outside the camera DSL.

  python scripts/example_library.py search "慢推近" [--top 5] [--json]
  python scripts/example_library.py resolve EX-028 [--choose N] [--json]
  python scripts/example_library.py validate      # every example through the parser
  python scripts/example_library.py docs          # rewrite narrative_30.md and technique_36.md from the YAML
"""
import io
import json
import os
import re
import sys
import unicodedata

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import camera_dsl as dsl  # noqa: E402
import yaml_lite  # noqa: E402

LIB_DIR = os.path.join(ROOT, "examples", "production_library")
DATA = os.path.join(LIB_DIR, "production_examples.yaml")
DOCS = {"NARRATIVE_30": "narrative_30.md", "TECHNIQUE_36": "technique_36.md"}
NEEDS_CONTEXT = ("CONTEXT_REQUIRED", "AMBIGUOUS", "CAMERA_PLUS_EDITING")
NON_CAMERA_KEYS = ("action", "temporal", "editing", "fx", "lighting", "color", "style")
# simplified -> traditional for the characters of the library's vocabulary, so a query in either script finds the same example
_S2T_PAIRS = ("镜鏡摇搖环環绕繞变變头頭机機挡擋转轉场場远遠过過视視顶頂横橫动動运運轨軌无無观觀战戰斗鬥结結飞飛开開绪緒写寫"
              "随隨并並时時间間滞滯剑劍忆憶闪閃虚虛实實叠疊梦夢睁睜渐漸独獨连連广廣长長极極进進张張叶葉灯燈风風云雲雾霧泪淚"
              "层層两兩对對侧側庄莊严嚴坠墜惊驚觉覺门門剧劇摄攝迹跡节節围圍级級骤驟递遞势勢压壓尘塵烟煙浓濃稳穩线線范範纵縱"
              "构構图圖点點衬襯亲親双雙后後现現显顯断斷尔爾达達蓝藍银銀红紅绿綠黄黃调調质質气氣体體积積处處边邊墙牆帘簾楼樓"
              "阶階桥橋笼籠摆擺飘飄扬揚乌烏电電疗療愈癒尽盡终終悬懸华華丽麗浅淺宽寬狭狹宫宮书書读讀灭滅举舉扩擴杀殺惨慘壮壯"
              "苍蒼凉涼爱愛恋戀温溫关關键鍵资資讯訊继繼拥擁")
S2T = str.maketrans({_S2T_PAIRS[i]: _S2T_PAIRS[i + 1] for i in range(0, len(_S2T_PAIRS), 2)})
_NOT_WORD = re.compile(r"[^0-9a-z㐀-鿿]")
_cache = {}


def load_examples():
    """the 66 examples, in file order"""
    if "examples" not in _cache:
        _cache["examples"] = (yaml_lite.load_file(DATA) or {}).get("examples") or []
    return _cache["examples"]


def get_example(example_id):
    for ex in load_examples():
        if ex["id"] == example_id.upper():
            return ex
    raise KeyError(f"no example {example_id!r}")


def _norm(text):
    return _NOT_WORD.sub("", unicodedata.normalize("NFKC", str(text)).lower().translate(S2T))


def _bigrams(s):
    return {s[i:i + 2] for i in range(len(s) - 1)}


def candidate_list(ex):
    """[{dsl, when_zh, default}] of an example: the shot list of a multi-shot example, the candidates of a needs-context
    example, the one camera_dsl otherwise, or nothing for an example with no camera instruction"""
    if ex.get("shots"):
        return [{"dsl": "\n".join(f"{s['label']}: {s['dsl']}" for s in ex["shots"]), "when_zh": None, "default": False}]
    if ex.get("candidates"):
        return [{"dsl": c["dsl"], "when_zh": c.get("when_zh"), "default": bool(c.get("default"))} for c in ex["candidates"]]
    if ex.get("camera_dsl"):
        return [{"dsl": " ".join(ex["camera_dsl"]), "when_zh": None, "default": False}]
    return []


def all_dsl(ex):
    """every DSL string the example names: candidates, alternatives, refinements, shots"""
    out = [c["dsl"] for c in candidate_list(ex)]
    out += [a["dsl"] for a in (ex.get("alternatives") or [])] + [r["dsl"] for r in (ex.get("refinements") or [])]
    if ex.get("camera_dsl") and " ".join(ex["camera_dsl"]) not in out:
        out.append(" ".join(ex["camera_dsl"]))
    return out


def validate_dsl(text):
    """the existing parser and conflict rules on one candidate: status, diagnostics, tokens that are not canonical names"""
    res = dsl.analyze(text)
    reg = dsl.registry()
    diags = [{"rule": x.get("rule"), "type": x.get("type"), "message": x.get("message")}
             for s in res["shots"] for x in (s.get("diagnostics") or [])]
    diags += [{"rule": x.get("rule"), "type": x.get("type"), "message": x.get("message")} for x in (res.get("diagnostics") or [])]
    names, not_canonical, unknown = set(), [], []
    for s in res["shots"]:
        for seg in s.get("segments") or []:
            for c in seg.get("commands") or []:
                if c.get("canonical") not in reg.commands:
                    unknown.append(c.get("raw"))
                    continue
                names.add(c["canonical"])
                if c.get("relationship") != "canonical":
                    not_canonical.append(f"{c.get('raw')} -> /{c['canonical']}")
    return {"dsl": text, "status": res["status"], "diagnostics": diags, "commands": sorted(names),
            "not_canonical": not_canonical, "unknown": unknown}


def _commands_of(ex):
    key = ("cmds", ex["id"])
    if key not in _cache:
        _cache[key] = set().union(*[set(validate_dsl(d)["commands"]) for d in all_dsl(ex)]) if all_dsl(ex) else set()
    return _cache[key]


def search_examples(query, top_k=5):
    """deterministic retrieval: exact title > title phrase > tag > command name > description overlap; ties by id"""
    q = _norm(query)
    qb = _bigrams(q)
    out = []
    for ex in load_examples():
        t = _norm(ex["title_zh"])
        score, why = 0, []
        if q and q == t:
            score, why = score + 100, why + ["exact title"]
        elif len(q) >= 2 and len(t) >= 2 and (q in t or t in q):
            score, why = score + 60 + int(20 * min(len(q), len(t)) / max(len(q), len(t))), why + ["title phrase"]
        for tag in ex.get("tags") or []:
            tn = _norm(tag)
            if tn and tn == q:
                score, why = score + 40, why + [f"tag {tag}"]
            elif len(tn) >= 2 and len(q) >= 2 and (tn in q or q in tn):
                score, why = score + 15, why + [f"tag {tag}"]
        for c in sorted(_commands_of(ex)):
            if len(c) >= 4 and c.lower() in q:
                score, why = score + 20, why + [f"command /{c}"]
        overlap = len(qb & _bigrams(_norm(ex["natural_language_intent_zh"])))
        if overlap:
            score, why = score + min(20, 2 * overlap), why + [f"description overlap {overlap}"]
        if score > 0:
            out.append({"example_id": ex["id"], "title_zh": ex["title_zh"], "mapping_class": ex["mapping_class"],
                        "match_score": score, "matched_by": why})
    out.sort(key=lambda m: (-m["match_score"], m["example_id"]))
    return out[:top_k]


def resolve_example(example_id, context=None, query=None, match_score=None):
    """the candidate DSL of an example, validated. A needs-context example returns every candidate and its question; it
    is resolved to one candidate only when context names it: {"candidate": N} (1-based) or {"dsl": "<one candidate>"}"""
    ex = get_example(example_id)
    cls = ex["mapping_class"]
    cands = candidate_list(ex)
    needs = cls in NEEDS_CONTEXT
    chosen = None
    if needs and context:
        if context.get("candidate"):
            n = int(context["candidate"])
            if not 1 <= n <= len(cands):
                raise ValueError(f"{ex['id']} has {len(cands)} candidates, not {n}")
            chosen = cands[n - 1]
        elif context.get("dsl"):
            chosen = next((c for c in cands if c["dsl"] == context["dsl"]), None)
            if chosen is None:
                raise ValueError(f"{context['dsl']!r} is not a candidate of {ex['id']}")
    use = cands if chosen is None else [chosen]
    checks = [validate_dsl(c["dsl"]) for c in use]
    warnings = [f"{v['dsl']}: [{d['rule']}] {d['message']}" for v in checks for d in v["diagnostics"]]
    return {
        "query": query,
        "example_id": ex["id"],
        "title_zh": ex["title_zh"],
        "match_score": match_score,
        "mapping_class": cls,
        "candidate_dsl": [c["dsl"] for c in use],
        "candidate_notes_zh": [c["when_zh"] for c in use],
        "default_candidate": next((c["dsl"] for c in cands if c["default"]), None) if needs and chosen is None else None,
        "needs_context": needs and chosen is None,
        "question_zh": ex.get("question_zh") if needs and chosen is None else None,
        "camera": {"dsl": [c["dsl"] for c in use], "semantics": list(ex.get("camera_semantics") or [])},
        "non_camera": {k: list(v) for k, v in (ex.get("non_camera") or {}).items()},
        "ambiguity": list(ex.get("ambiguity") or []),
        "alternatives": [dict(a) for a in (ex.get("alternatives") or [])],
        "refinements": [dict(r) for r in (ex.get("refinements") or [])],
        "validation": [{"dsl": v["dsl"], "status": v["status"]} for v in checks],
        "warnings": warnings,
    }


def search_and_resolve(query, top_k=5):
    """the best match resolved, plus the other matches"""
    hits = search_examples(query, top_k)
    if not hits:
        return {"query": query, "example_id": None, "needs_context": True,
                "question_zh": "案例庫裡沒有相近的情境；請直接寫 Camera DSL，或換個說法。", "other_matches": []}
    res = resolve_example(hits[0]["example_id"], query=query, match_score=hits[0]["match_score"])
    res["other_matches"] = [{"example_id": h["example_id"], "title_zh": h["title_zh"], "match_score": h["match_score"]} for h in hits[1:]]
    return res


# ------------------------------------------------------------------ text output and docs

def _text(res):
    lines = []
    for k in ("query", "example_id", "title_zh", "match_score", "mapping_class"):
        if res.get(k) is not None:
            lines.append(f"{k}: {res[k]}")
    if res.get("candidate_dsl") == []:
        lines.append("candidate_dsl: []   # 沒有運鏡指令，不自動補")
    elif res.get("candidate_dsl") is not None:
        lines.append("candidate_dsl:")
        for d, note in zip(res["candidate_dsl"], res.get("candidate_notes_zh") or [None] * len(res["candidate_dsl"])):
            mark = "  (default)" if d == res.get("default_candidate") else ""
            text = d.replace("\n", " | ")
            lines.append(f"  - {text}" + (f"   # {note}" if note else "") + mark)
    lines.append(f"needs_context: {str(res.get('needs_context')).lower()}")
    if res.get("question_zh"):
        lines.append(f"question_zh: {res['question_zh']}")
    if res.get("camera", {}).get("semantics"):
        lines.append("camera_semantics:")
        lines += [f"  - {s}" for s in res["camera"]["semantics"]]
    if res.get("non_camera"):
        lines.append("non_camera:")
        lines += [f"  {k}: {', '.join(v)}" for k, v in res["non_camera"].items()]
    for key in ("alternatives", "refinements"):
        if res.get(key):
            lines.append(f"{key}:")
            lines += [f"  - {a['dsl']}   # {a.get('when_zh', '')}" for a in res[key]]
    if res.get("ambiguity"):
        lines.append("ambiguity:")
        lines += [f"  - {a}" for a in res["ambiguity"]]
    if res.get("validation"):
        lines.append("validation: " + ", ".join(f"{v['status']}" for v in res["validation"]))
    if res.get("warnings"):
        lines.append("warnings:")
        lines += [f"  - {w}" for w in res["warnings"]]
    if res.get("other_matches"):
        lines.append("other_matches: " + ", ".join(f"{m['example_id']} {m['title_zh']} ({m['match_score']})" for m in res["other_matches"]))
    return "\n".join(lines)


def render_docs():
    """{file name: text} of narrative_30.md and technique_36.md, generated from production_examples.yaml"""
    heads = {"NARRATIVE_30": ("Narrative examples · 敘事情境", "30 個敘事情境：運鏡寫成 DSL，特效、剪輯與時間效果另外放在 non_camera。"),
             "TECHNIQUE_36": ("Technique examples · 技巧用語", "36 個常見的運鏡說法：每個說法對應的候選 DSL，以及需要補問的地方。")}
    out = {}
    for batch, fname in DOCS.items():
        title, intro = heads[batch]
        lines = [f"# {title}", "", "<!-- generated by scripts/example_library.py docs from production_examples.yaml; do not edit by hand -->", "",
                 intro, "", "案例名稱只是說法，不是指令，也不是別名。每個候選都會再經過解析器與衝突檢查。", ""]
        for ex in [e for e in load_examples() if e["batch"] == batch]:
            lines += [f"## {ex['id']}｜{ex['title_zh']}", "", f"- 類型：`{ex['mapping_class']}`", f"- 情境：{ex['natural_language_intent_zh']}"]
            if ex.get("shots"):
                lines.append("- 鏡頭：")
                lines += [f"  - {s['label']}，{s['role_zh']}：`{s['dsl']}`" for s in ex["shots"]]
            elif ex.get("candidates"):
                if ex.get("camera_dsl"):
                    lines.append(f"- 運鏡元素：`{' '.join(ex['camera_dsl'])}`")
                lines.append("- 候選：")
                lines += [f"  - `{c['dsl']}`：{c.get('when_zh', '')}" + ("，預設" if c.get("default") else "") for c in ex["candidates"]]
                lines.append(f"- 要先問：{ex['question_zh']}")
            elif ex.get("camera_dsl"):
                lines.append(f"- DSL：`{' '.join(ex['camera_dsl'])}`")
            else:
                lines.append("- DSL：沒有運鏡，不自動補")
            for key, label in (("alternatives", "其他寫法"), ("refinements", "知道攝影機位置時")):
                if ex.get(key):
                    lines.append(f"- {label}：")
                    lines += [f"  - `{a['dsl']}`：{a.get('when_zh', '')}" for a in ex[key]]
            if ex.get("camera_semantics"):
                lines.append("- 運鏡說明：" + "；".join(s.rstrip("。") for s in ex["camera_semantics"]) + "。")
            if ex.get("non_camera"):
                lines.append("- 非運鏡：" + "；".join(f"{k} {'、'.join(v)}" for k, v in ex["non_camera"].items()))
            if ex.get("ambiguity"):
                lines.append("- 未定：" + "；".join(a.rstrip("。") for a in ex["ambiguity"]) + "。")
            if ex.get("build_notes"):
                lines.append("- 建置修正：" + "；".join(b.rstrip("。") for b in ex["build_notes"]) + "。")
            lines.append("")
        out[fname] = "\n".join(lines).rstrip("\n") + "\n"
    return out


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    as_json = "--json" in argv
    args = [a for a in argv if not a.startswith("--")]
    opt = {argv[i]: argv[i + 1] for i in range(len(argv) - 1) if argv[i] in ("--top", "--choose")}
    if not args:
        print(__doc__.strip())
        return 2
    cmd = args[0]
    if cmd == "search" and len(args) > 1:
        res = search_and_resolve(" ".join(args[1:]), int(opt.get("--top", 5)))
        print(json.dumps(res, ensure_ascii=False, indent=1) if as_json else _text(res))
        return 0
    if cmd == "resolve" and len(args) > 1:
        try:
            ctx = {"candidate": int(opt["--choose"])} if "--choose" in opt else None
            res = resolve_example(args[1], context=ctx)
        except (KeyError, ValueError) as e:
            print(f"ERROR: {e.args[0] if e.args else e}")
            return 2
        print(json.dumps(res, ensure_ascii=False, indent=1) if as_json else _text(res))
        return 0
    if cmd == "validate":
        bad = 0
        for ex in load_examples():
            for d in all_dsl(ex):
                v = validate_dsl(d)
                problems = (["ERROR " + "; ".join(f"[{x['rule']}] {x['message']}" for x in v["diagnostics"] if x["type"] == "ERROR")]
                            if v["status"] == "ERROR" else []) + [f"not canonical: {x}" for x in v["not_canonical"]] + \
                           [f"unknown: {x}" for x in v["unknown"]]
                bad += bool(problems)
                print(f"{ex['id']}  {v['status']:5s}  {d.replace(chr(10), ' | ')}" + (f"   <- {'; '.join(problems)}" if problems else ""))
        print(f"\n{len(load_examples())} examples; DSL strings with problems: {bad}")
        return 0 if not bad else 1
    if cmd == "docs":
        for fname, text in render_docs().items():
            io.open(os.path.join(LIB_DIR, fname), "w", encoding="utf-8", newline="\n").write(text)
            print("written", fname)
        return 0
    print(__doc__.strip())
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
