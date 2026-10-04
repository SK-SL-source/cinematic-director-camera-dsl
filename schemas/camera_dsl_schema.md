# Camera DSL · Grammar and Structured Camera Schema

**Status: PROJECT_DEFINED.** The grammar and the state layout are this project's own abstraction (spec sections 16–17). The vocabulary inside them comes from the researched sources (`registry/provenance.yaml`). The machine-readable form is `camera_dsl_schema.yaml`, and `schemas/examples.yaml` holds real parser output. `scripts/audit.py` validates every parser output it can generate against the YAML (697 outputs at last run), so this page, the YAML and the code cannot drift apart.

## 1. Grammar

| Form | Example | Meaning |
|---|---|---|
| `/COMMAND` | `/MS` | one canonical command or alias (case-insensitive) |
| `/COMMAND:VALUE` | `/LENS:35`, `/POV:A`, `/OTS:A>B` | one argument |
| `/COMMAND:DIRECTION` | `/PAN:R` | L/R are **camera-relative** (= screen) |
| `/COMMAND:DIRECTION:SPEED` | `/TILT:UP:SLOW` | |
| `/COMMAND:DIRECTION:AMOUNT:SPEED` | `/ORBIT:R:90:SLOW` | |
| size range | `/DOLLYIN:MS>MCU` | the move's start and end framing |
| compact lens | `/LENS50`, `/35MM` | `= /LENS:50` |

**Arguments are typed, not positional.** Each token is matched to the command's slots (`registry/canonical_commands.yaml` → `meta.param_slots`), so `/DOLLYIN:SLOW:20%` = `/DOLLYIN:20%:SLOW`.

| Slot | Tokens |
|---|---|
| direction | `L R UP DOWN IN OUT CW CCW` (LEFT/RIGHT/U/D/FWD/BACK accepted) |
| speed | `IMPERCEPTIBLE < VSLOW < SLOW < STEADY < BRISK < FAST` (MED/NORMAL → STEADY) |
| amount | `20%`, `90` or `90DEG`, `1M` or `30CM`, `SMALL MEDIUM LARGE PARTIAL FULL` |
| relation | `A>B`, `FG>BG`, `A>CAM` (into the lens), `A>OFFL/OFFR/OFFUP/OFFDOWN` |
| axis | `A-B` (A screen-left, B screen-right) |
| screen | `L2R R2L TOWARD AWAY` |

**Tokenizing.** A command starts at a `/` that is not preceded by a letter, digit, `_` or `/`, so `中景/MS` works and `and/or` is not a command. Arguments take only DSL characters, so the commas, full stops and brackets around a command are never swallowed. Full-width `／ ： ＞` next to DSL tokens are read as ASCII.

**Structure.**

| Construct | Syntax | Rule |
|---|---|---|
| simultaneous | commands in one segment | happen together; checked for conflicts |
| sequential | `0-3s: /PAN:R 3-7s: /DOLLYIN` or `/PAN:R THEN /DOLLYIN` | never a conflict; text before the first time code applies to the whole shot |
| shot list | lines `S1:` `S2:` or the token `CUT` | continuity is checked across shots |
| continuous | `CONTINUOUS` in a shot | it must start where the previous shot ended |
| modes | `MODE:STRICT` (default), `MODE:DIRECTOR`, `MODE:IMAGE`, `MODE:VIDEO` | |
| intent layers | CLI `--nl` (priority 2), `--storyboard` (3), `--director` (5) | lower priority never overrides higher (spec section 29) |

## 2. Parse result

```
{input, modes[], strict, status, diagnostics[] (cross-shot),
 shots[]: {label, continuous, status, free_text[], diagnostics[],
           segments[]: {index, t0, t1, global, commands[]: {canonical, raw, via, relationship, args{}, origin}},
           state}}
```
- `status`: `OK` / `WARN` / `ERROR`. ERROR means do not render.
- `relationship`: how the token resolved. Values: `canonical`, `compact_grammar`, `special_technique` (merged, e.g. dolly + opposite zoom), or an alias type from `registry/aliases.yaml` (`abbreviation`, `semantic_alias`, `legacy`, `legacy_ambiguous`, …).
- `origin`: `USER_SPECIFIED` (DSL and natural-language camera), `STORYBOARD`, `DIRECTOR_SUGGESTED`.
- `free_text`: words around the commands. They are kept, but never turned into camera instructions.

**Diagnostic (lint record):**
- Fields: `{rule, type, commands[], message, fix?, evidence[]?, shot?, segment?}`.
- `type`: one of the six spec types (`HARD_CONFLICT`, `SOFT_CONFLICT`, `CONTEXT_DEPENDENT`, `SEQUENTIAL_ONLY`, `VALID_COMBINATION`, `SPECIAL_TECHNIQUE`), or `OUT_OF_SCOPE`, `ERROR`, `WARNING`, `INFO`.
- Rule families:
  - `A..` parsing and aliases
  - `P01–P92` pair rules; `P00` priority override
  - `G..` group rules
  - `DIM-EXCLUSIVE` / `CH-OPPOSITE` dimension logic
  - `R..` segment checks
  - `C..` continuity
  - `S..` sequence order
  - `M..` modes

## 3. Camera state (per shot)

Spec section 17 fields are marked **§17**. Everything else is an extension the adapters need. `null` = not given; STRICT mode never fills it in.

| Field | Values | Set by |
|---|---|---|
| **shot.size** §17 | EWS WS FS MFS COWBOY MS MCU CU ECU | SHOT_SIZE commands; else the start of a size range |
| **shot.framing** §17 | list: SINGLE TWOSHOT THREESHOT GROUPSHOT OTS DIRTYOTS CLEANOTS POV FRONTAL THREEQUARTER PROFILE REAR | SUBJECT_FRAMING |
| **shot.subject_count** §17 | "1" "2" "3" GROUP | SINGLE…GROUPSHOT |
| **shot.primary_subject** §17 / **foreground_subject** §17 | subject id | `OTS:A>B` → B / A; else the first eyeline's looker |
| shot.viewpoint · pov_owner · ots_variant | OTS POV · id · DIRTY CLEAN | OTS, POV |
| shot.orientation | FRONTAL THREEQUARTER PROFILE REAR | which side faces the camera |
| shot.function · function_target | REACTION INSERT CUTAWAY · id | editorial role |
| **camera.position** §17 | FAR_ABOVE DRONE | BIRDSEYE, DRONEVIEW |
| **camera.height** §17 | GROUND ANKLE KNEE HIP CHEST SHOULDER EYE ELEVATED AERIAL | CAMERA_HEIGHT, EYELEVEL |
| **camera.angle** §17 | VERTICAL_UP LOW LEVEL HIGH VERTICAL_DOWN | CAMERA_ANGLE (lens-axis pitch) |
| camera.angle_intensity | SLIGHT STEEP | `/LOWANGLE:STEEP` |
| **camera.orientation** §17 · dutch | LEVEL DUTCH · {direction, degrees} | DUTCH (a held roll, not a move) |
| **movement[]** §17 | one entry per move, in time order | movement commands |
| · **type** §17 · canonical | pan tilt … crash_zoom · PAN TILT … | registry canonical_name |
| · **direction** §17 | L R UP DOWN IN OUT CW CCW BACK | ORBIT CW/CCW stored as L/R |
| · **amount** §17 | {value, unit: deg % m ""} | `90`, `20%`, `1M`, `LARGE` |
| · **speed** §17 | speed scale | |
| · **duration** §17 · time | seconds · [t0, t1] | time-coded segment |
| · **start_position** §17 · **end_position** §17 | shot sizes | size range; else the shot size / null |
| · target · origin · sequential · step | id · origin · bool · segment index | step 0 = whole shot; 1, 2 … = sequence segments. `/STATIC` inside a segment becomes a `hold` step |
| **rig.type** §17 · types · **stability** §17 · intensity · locked | TRIPOD HANDHELD SHOULDER STEADICAM GIMBAL SLIDER DRONE FPV · … · LOCKED HANDHELD STABILIZED AERIAL · SUBTLE STRONG · bool | CAMERA_RIG, STATIC |
| **lens.focal_length** §17 · **lens_type** §17 · types | mm (35mm FF equiv.) · ULTRAWIDE WIDE NORMAL PORTRAIT TELE · MACRO FISHEYE ANAMORPHIC | LENS |
| **focus.target** §17 · **depth_of_field** §17 · **transition** §17 · special | FG MG BG · SHALLOW DEEP · {type RACK, from, to, speed} · SPLIT_DIOPTER | FOCUS |
| **composition.placement** §17 · **foreground** §17 · **midground** §17 · **background** §17 · **depth_layers** §17 | CENTER THIRD THIRD_L THIRD_R · label · reserved · reserved · bool | COMPOSITION |
| composition.symmetry · negative_space · headroom · lookroom · leading_lines · frame_in_frame | bool · side or true · TIGHT NORMAL LOOSE · L R or true · bool · bool | COMPOSITION |
| **continuity.axis** §17 · **screen_direction** §17 · **eyeline** §17 · **relation_to_previous_shot** §17 | `A-B` · L2R R2L TOWARD AWAY · list of `A>B` · list of {type SRS MATCHACTION MATCHCUT, value} | CONTINUITY |
| continuity.cross_axis · continuous | MOVE NEUTRAL CUTAWAY REESTABLISH BLOCKING UNSPECIFIED · bool | CROSSAXIS, CONTINUOUS |
| **style.visual_style** §17 | cinematic | CINEMATIC (a style word only) |
| constraints.preserve_story · **character** · **clothing** · **scene** · **props** · **action** §17 | always true | spec section 28: the camera layer never edits these |
| meta.origins · unspecified · definitional · label | which layer set each field · movement parameters left to the model · implied values (source COMMAND_DEFINITION when fixed by the command definition, CL-031) | |

`composition.midground` and `composition.background` are reserved. No v1 command writes them, because scene content belongs to the prompt, not the camera.

## 4. Example (EX-01, real output)

`/MS /LOWANGLE /DOLLYIN:SLOW /LENS50`
- **Commands:** `MS`, `LOWANGLE`, `DOLLYIN {speed=SLOW}`, `LENS {mm=50}` (compact grammar).
- **State:**
  - shot.size MS; camera.angle LOW; lens.focal_length 50.
  - movement[0] = dolly_in, speed SLOW, start MS, end null.
  - unspecified = DOLLYIN.amount, DOLLYIN.end_position.
- **Status:** OK.

More examples in `examples.yaml`: dialogue, POV, sequence, conflicts, legacy names, director layer, shot-list continuity, image mode.
