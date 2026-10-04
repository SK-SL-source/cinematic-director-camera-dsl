# Model adapter · Qwen-Image-Edit

Changing the **camera view of an existing image** while everything else stays. An edit is not a move: it produces the view the move would reach.

## Evidence
| Level | Source | Rule |
|---|---|---|
| GUIDANCE | SRC-004 imgadapt:38, §4 (hold-plus-change) | name the one change and list the holds; "same everything" is weaker than a list of nameable things |
| CAPABILITY MATRIX | SRC-004 imgadapt:19-42 | Qwen edit-class instruction editing "best" |
| UNVERIFIED | — | no researched source measures camera-viewpoint edits (orbit angles, height changes) on Qwen-Image-Edit |

## Output rules
1. Start with "Change only the camera, to this view:" (zh: 只改变镜头视角：).
2. Describe the new camera state with the generic image rules; movements render where they arrive (`/ORBIT:R:45` = the view 45 degrees around toward camera-right).
3. End with the holds: "Keep {SUBJECT}, clothing, props, scene and pose exactly the same." (zh: 人物、服装、道具、场景和姿势保持完全不变。)
4. One camera change per edit; chain from the master image rather than editing an edit (SRC-004 imgadapt: NanoBanana/Gemini-class rules, same edit class).

## Examples (actual adapter output)
`/ORBIT:R:45 /FS`
> Change only the camera, to this view: A full shot framing {SUBJECT} from head to toe. The camera is positioned about 45 degrees around {SUBJECT} toward camera-right, as a moment on an implied orbit path; {SUBJECT} stays centered. Keep {SUBJECT}, clothing, props, scene and pose exactly the same.

`/ORBIT:R:45 /FS` (zh)
> 只改变镜头视角：全景，{SUBJECT}从头到脚完整入画。机位绕{SUBJECT}向右约45度，像环绕路径上的一刻，{SUBJECT}保持居中。人物、服装、道具、场景和姿势保持完全不变。

Tests: tests/model_adapters.md (MA-QE-*, MS-QE-*).
