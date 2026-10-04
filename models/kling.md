# Model adapter · Kling (可灵)

Two languages, same shot:
- `lang=zh` (default): the whole camera text in simplified Chinese with trade terms — Kling is built around Chinese prompts, so Chinese camera terms reach it without a translation step (after SRC-004 vidadapt:238).
- `lang=en`: short declarative phrases, comma separated, for fal.ai / international API use (SRC-003 fal-prompting/references/kling.md:48-84; SRC-005C). Keep a single-shot prompt within about 30-40 words.

## Evidence
| Level | Source | Rule |
|---|---|---|
| GUIDANCE | SRC-004 vidadapt:234-245 | Chinese prompt incl. craft terms; negatives go in the negative field; using a camera preset and also describing the move in words doubles it, so choose one; staged action with a named end pose |
| GUIDANCE | SRC-004 lexicon:334-384 | 景别 / 机位 / 运镜 terms (推镜, 拉镜, 横摇, 纵摇, 横移, 升降, 摇臂, 环绕, 跟拍, 固定镜头, 变焦推近, 移焦, 甩镜, 滑动变焦); 摇镜头 names no axis, never send it alone; 推近 alone is ambiguous |
| GUIDANCE | SRC-003 kling.md | English: "[subject doing action] in [setting], [camera framing/movement], [lighting]"; describe motion only on image-to-video |
| UNVERIFIED | DIR-05 | Kling API `camera_control` numeric axes (−10..10, single axis in simple mode): the source contradicts itself and Kling's official CLI (DIR-16) exposes no camera parameters → not implemented |

## Output rules
1. zh: 景别 → 主体取景 → 机位高度/角度 → 镜头 → 焦点 → 构图 → 载具 → 运镜 → 连戏, joined with 。.
2. Dolly and zoom stay separate words: 推镜/拉镜 (body) vs 变焦推近/变焦拉远 (lens) (REG-05).
3. Pan is 横摇, tilt is 纵摇, truck is 横移, pedestal is 升降 (REG-03, REG-04).
4. Orbit always states that the subject does not turn (保持在原地不转身, REG-06).
5. If you use Kling's own camera preset (运镜), delete the camera words from the text.

## Examples (actual adapter output)
`/MS /LOWANGLE /DOLLYIN:MS>MCU:SLOW` (zh)
> 中景，{SUBJECT}腰部以上入画。仰拍，镜头从下往上看{SUBJECT}。推镜：镜头缓慢地向前推进靠近{SUBJECT}，最后停在近景，{SUBJECT}在画面中变大，焦距不变。

`/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` (en)
> full shot of {SUBJECT} from head to toe, camera at ground level, smooth gimbal, side tracking shot beside {SUBJECT}, moving toward frame-right.

Tests: tests/model_adapters.md (MA-KZ-*, MA-KE-*, MS-KZ-*, MS-KE-*).
