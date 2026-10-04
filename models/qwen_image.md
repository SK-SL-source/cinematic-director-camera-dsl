# Model adapter · Qwen-Image

Stills on Qwen-Image. English by default; Chinese available (`--lang zh`).

## Evidence
| Level | Source | Rule |
|---|---|---|
| CAPABILITY MATRIX | SRC-004 imgadapt:19-42 | Qwen-Image: literal prompt fidelity "best", seed "best", negative prompt "yes", text rendering "best" |
| UNVERIFIED | — | no researched source covers Qwen-Image camera wording or which language it follows better; the Chinese option reuses the SRC-004 trade terms |

## Output rules
1. Same as models/generic_image.md (positions, no motion verbs).
2. `lang=zh`: same order in Chinese trade terms (景别, 机位, 角度…); movements become 「…途中的一刻」.
3. Keep readable text out of the camera prompt (the studio's rule: no AI-written text in frame).

## Examples (actual adapter output)
`/ORBIT:R:45 /FS`
> A full shot framing {SUBJECT} from head to toe. The camera is positioned about 45 degrees around {SUBJECT} toward camera-right, as a moment on an implied orbit path; {SUBJECT} stays centered.

`/ORBIT:R:45 /FS` (zh)
> 全景，{SUBJECT}从头到脚完整入画。机位绕{SUBJECT}向右约45度，像环绕路径上的一刻，{SUBJECT}保持居中。

Tests: tests/model_adapters.md (MA-QI-*), tests/image_mode.md IMG-012.
