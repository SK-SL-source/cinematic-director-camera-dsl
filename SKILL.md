---
name: cinematic-director-camera-dsl
description: Evidence-backed camera DSL for AI image/video prompts. Parses and validates camera commands (/MS /LOWANGLE /DOLLYIN:MS>MCU:SLOW /ORBIT:R:90 /OTS:A>B /RACKFOCUS:A>B, time-coded sequences, shot lists), catches contradictions and continuity errors (axis, eyeline, screen direction), and writes model-ready camera text for MiniMax H3, Kling, Veo, FLUX, Qwen-Image, Qwen-Image-Edit or generic image/video models without changing the camera intent. Use when the user writes slash camera commands, asks to turn camera directions or a storyboard into prompt camera text, asks whether camera moves can be combined, or asks for shot/camera suggestions (Director Mode). Also for 運鏡、鏡頭語言、景別、機位、分鏡運鏡.
---

# Cinematic Director Camera DSL

This skill turns camera intent into exact camera text. The Camera layer says **how** to shoot; the Director layer (optional) says **why**. Every command traces to researched sources (`registry/provenance.yaml`) or is marked PROJECT_DEFINED. The script is the source of truth: run it, never paraphrase the rules from memory.

## Workflow

1. **Collect the DSL.**
   - Take `/COMMAND[:ARG…]` tokens from the user's text; they may sit inside sentences or Chinese text.
   - Natural-language camera wishes: convert them to DSL yourself, show the mapping, and pass it as `--nl` (priority 2). Never add anything the words did not say.
   - Everyday phrases and story situations (慢推近, 仰拍英雄, 遮擋轉場, 拉出…): look them up first with `python scripts/example_library.py search "<phrase>"` (examples/production_library/). Use the candidate DSL it returns; when it says `needs_context`, ask its question instead of picking a candidate. Its `non_camera` items (slow motion, transitions, effects) never become camera commands.
2. **Pick the model.** Use the one the user names: `minimax_h3`, `kling`, `veo`, `generic_video`, `generic_image`, `flux`, `qwen_image` or `qwen_image_edit`. If none is named, use `generic_video` (`generic_image` for stills) and say so.
3. **Run the script.** From this skill's folder:
   ```bash
   python scripts/camera_dsl.py render "/MS /LOWANGLE /DOLLYIN:MS>MCU:SLOW" --model minimax_h3
   ```
4. **Read the status.**
   - **ERROR:** nothing is rendered. Report each error in plain words with its fix and two ways forward, and let the user choose. Never drop or change a command to make the error go away.
   - **WARN:** deliver the text and pass the warnings on.
5. **Deliver:**
   - the camera text (copyable, in the adapter's language)
   - `UNSPECIFIED`: what the model will decide; `DEFINITION_IMPLIED`: values fixed by the command's own definition (crash zoom = fast and large, whip pan = fast), neither user-given nor added by the adapter
   - the warnings
   - in Director Mode, the `USER_SPECIFIED` / `DIRECTOR_SUGGESTED` split
   - for `minimax_h3`: the routing block (measured reliability of the shot size, each viewpoint and each move, and whether to start from a real first frame; `--lang zh` prints it in Chinese; models/minimax_h3_profile.yaml). Pass `--h3-mode` and `--h3-profile <generation profile id>` so it reads the evidence of that scope; the evidence is CONSTRAINED_PRODUCTION by default (camera motion plus framing, landing and target-relative constraints); for a move with nothing to frame add `--h3-subject-context camera_only` to read the CAMERA_ONLY evidence (camera motion through a fixed set); neither type's grades are applied to the other; without a matching profile every item is UNVERIFIED and no grade is borrowed from another mode or profile; a grade measured with a pre-refactor prompt wording is shown as historical, current-core applicability UNVERIFIED; a grade applies only to the very shot it was measured with (evidence relation EXACT), and a measurement of another shot, speed, amount, sequence or extra command is RELATED: named, never applied. `--layers` shows each move as camera_core / temporal_clarifier / derived_visual_constraint / negative_clarifier with its source
   - one line in the user's language explaining the shot

   The text is **camera only**: it goes into the model's own prompt next to the user's subject, action and scene (H3: the `[Shot N]` of the prompt; see models/minimax_h3.md). For H3, `python scripts/h3_wrappers.py <t2va|i2va|fl2va|l2va|ref2va> "<dsl>" content.json` builds the whole official prompt around that same camera text (PROJECT_GOAL.md: one camera core, the wrappers only wrap) and checks its content: each subject bound in `subject_map`, the cut times, the required fields; a problem exits 1, `--draft` only reports it.

## Modes and priority

- **STRICT (default).** Render exactly what was given. `/MS /LOWANGLE` gains no lens, move, shallow focus or Dutch angle. Missing speed, amount, end size or direction is listed, never invented.
- **DIRECTOR (only when asked):** "recommend / design the shot / 導演模式 / 推薦鏡頭", or `MODE:DIRECTOR`.
  - Choose the shot function first (establishing, relation, close-up, insert, reaction, reveal…), then at most one dominant move. Give one reason per suggestion.
  - Pass the suggestions with `--director "/CU /DOLLYIN:SLOW"`. They are labelled DIRECTOR_SUGGESTED and can never override the user.
  - With an explicit `MODE:STRICT` they are refused (M01).
- **Priority (spec 29):** explicit DSL > natural-language camera (`--nl`) > storyboard (`--storyboard`) > shot description > director (`--director`) > model default. Dropped lower-priority items are reported (P00).
- **Preserve (spec 28):** the camera layer never changes people, faces, age, clothes, set, props, lines, story, head count or blocking. Subjects stay placeholders: `{SUBJECT}`, `{A}`, `{B}`.

## Grammar (PROJECT_DEFINED, full spec: schemas/camera_dsl_schema.md)

| Form | Examples |
|---|---|
| command, value, direction, speed, amount | `/PAN:R`, `/TILT:UP:SLOW`, `/DOLLYIN:20%:SLOW`, `/ORBIT:R:90:SLOW`, `/LENS50` |
| size range = start>end framing | `/DOLLYIN:MS>MCU`, `/ZOOMOUT:CU>MS` |
| relations | `/OTS:A>B` (over A's shoulder onto B), `/POV:A`, `/RACKFOCUS:A>B`, `/EYELINE:A>CAM`, `/AXIS:A-B`, `/SCREEN:L2R` |
| simultaneous | commands in one segment: `/DOLLYIN /TILT:UP` |
| sequential | `0-3s: /PAN:R 3-7s: /DOLLYIN:SLOW` or `/PAN:R THEN /DOLLYIN` (never a conflict) |
| shot list | lines `S1:` `S2:` (or `CUT`); `CONTINUOUS` = start where the last shot ended |
| modes | `MODE:STRICT` `MODE:DIRECTOR` `MODE:IMAGE` `MODE:VIDEO` |

L/R are **camera-relative**; `ORBIT:R` = toward camera-right = counterclockwise seen from above. Speeds: `IMPERCEPTIBLE VSLOW SLOW STEADY BRISK FAST`. Look up any word: `python scripts/camera_dsl.py explain /WIDE`.

## CLI

```bash
python scripts/camera_dsl.py render "<dsl>" --model <model> [--lang zh|en] [--mode image|video] [--director "<dsl>"] [--storyboard "<dsl>"] [--nl "<dsl>"] [--layers] [--h3-mode <mode>] [--h3-profile <id>] [--h3-subject-context constrained_production|camera_only] [--json]
python scripts/h3_wrappers.py <mode> "<dsl>" [content.json] [--layers camera_core,...] [--profile <id>] [--lint] [--draft]   # H3 only: the official prompt for t2va|i2va|fl2va|l2va|ref2va
python scripts/camera_dsl.py parse  "<dsl>"     # JSON: commands, diagnostics, structured camera state
python scripts/camera_dsl.py shots  "S1: /WS /AXIS:A-B\nS2: /MCU /OTS:A>B"   # a typed \n separates shots
python scripts/camera_dsl.py explain /PORTRAIT
```
- Exit code 2 = ERROR.
- Git Bash turns a lone `/MS` into a Windows path. Prefix `MSYS_NO_PATHCONV=1` (the script also undoes the common cases). PowerShell needs nothing.
- **Slash-command clash:** in Claude Code a message that *starts* with `/MS` is read as a slash command. Invoke this skill with the DSL as its argument (`/cinematic-director-camera-dsl /MS /LOWANGLE`), or put any word before the first command.

## Load only what the question needs

Load one reference and one model file, not the whole folder.

| Question about… | Load |
|---|---|
| sizes · framing (OTS, POV, two-shot) · angle · height | references/01 · 02 · 03 · 04 |
| pan/tilt/roll · dolly/truck/pedestal · tracking, orbit, crane · rig feel | references/05 · 06 · 07 · 08 |
| lens · zoom · focus/DOF · composition | references/09 · 10 · 11 · 12 |
| axis, eyeline, screen direction, cuts · aerial/drone | references/13 · 14 |
| accepted names and old names · why a combination is refused | references/15_aliases.md · 16_conflict_rules.md |
| how text is written (STRICT, image vs video, sequences) | references/17_prompt_translation_rules.md |
| one model's wording and evidence | models/<model>.md |
| worked examples with real output | examples/*.md |
| an everyday camera phrase or a story situation | examples/production_library/ through scripts/example_library.py |

`tests/`, `registry/` and `scripts/` are maintenance material; read them only to change the skill. Source ids such as SRC-004 resolve in SOURCES.md.

**Frozen at V2_BASELINE** (BASELINE_V2.md); the charter is PROJECT_GOAL.md:
- No new camera commands and no new aliases.
- The grammar changes only for a clear bug.
- Every change gets a CHANGELOG.md entry (reason, before, after, commands, adapters, tests, backward compatibility, files).
- After any change run `python scripts/audit.py --sync`, then `python scripts/audit.py` and `python scripts/run_tests.py`; all must end with 0 errors.

## Never

- Resolve `/WS` (wide **shot**) to a wide-angle **lens**, or the reverse; the same goes for POV vs looking into the lens, pan vs truck, tilt vs pedestal, dolly vs zoom, orbit vs subject turning, rack focus vs camera move, and drone view vs bird's-eye vs top-down (tests/regression.md).
- Claim a still image pans, pushes or orbits. Image mode renders the position the move implies.
- Let an adapter change the shot: wording may differ between models, the camera may not.
