# Tests · Model adapters

> Spec section 24: an adapter may change the wording, never the shot. Every row checks that the rendered
> text carries each command's intent markers and none of the conflicting values (`intent[...]`), and image
> models never use motion verbs (`still[...]`). The shared set is rendered on all 8 models (Kling in both
> languages). Model-specific rows check the evidence-based wording in `models/*.md`.

## generic_video

| ID | Input | Expect | Source |
|---|---|---|---|
| MA-GV-01 | `/MS /LOWANGLE /DOLLYIN:SLOW /LENS50` | intent[generic_video] | spec section 24 |
| MA-GV-02 | `/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` | intent[generic_video] | spec section 23 |
| MA-GV-03 | `/CU /SHALLOW /PORTRAITLENS` | intent[generic_video] | SRC-002 camera:244 |
| MA-GV-04 | `/WS /HIGHANGLE /STATIC` | intent[generic_video] | SRC-001 SKILL:189 |
| MA-GV-05 | `/OTS:A>B /MCU /EYELINE:B>OFFL` | intent[generic_video] | SRC-004 cinlang:350-355 |
| MA-GV-06 | `/TOPDOWN /EWS` | intent[generic_video] | SRC-002 camera:99 |
| MA-GV-07 | `/ORBIT:R:90 /LOWANGLE` | intent[generic_video] | SRC-001 SKILL:190 |
| MA-GV-08 | `/POV:A /HANDHELD` | intent[generic_video] | SRC-002 camera:86 |
| MA-GV-09 | `/DRONEVIEW /FLYOVER` | intent[generic_video] | SRC-001 SKILL:77 |
| MA-GV-10 | `/DUTCH:L /MCU` | intent[generic_video] | SRC-002 camera:96 |
| MA-GV-11 | `/RACKFOCUS:FG>BG /MS` | intent[generic_video] | SRC-004 lexicon:149 |
| MA-GV-12 | `/BIRDSEYE /EWS` | intent[generic_video] | SRC-005 SKILL:121 |

## minimax_h3

| ID | Input | Expect | Source |
|---|---|---|---|
| MA-H3-01 | `/MS /LOWANGLE /DOLLYIN:SLOW /LENS50` | intent[minimax_h3] | spec section 24 |
| MA-H3-02 | `/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` | intent[minimax_h3] | spec section 23 |
| MA-H3-03 | `/CU /SHALLOW /PORTRAITLENS` | intent[minimax_h3] | SRC-002 camera:244 |
| MA-H3-04 | `/WS /HIGHANGLE /STATIC` | intent[minimax_h3] | SRC-001 SKILL:189 |
| MA-H3-05 | `/OTS:A>B /MCU /EYELINE:B>OFFL` | intent[minimax_h3] | SRC-004 cinlang:350-355 |
| MA-H3-06 | `/TOPDOWN /EWS` | intent[minimax_h3] | SRC-002 camera:99 |
| MA-H3-07 | `/ORBIT:R:90 /LOWANGLE` | intent[minimax_h3] | SRC-001 SKILL:190 |
| MA-H3-08 | `/POV:A /HANDHELD` | intent[minimax_h3] | SRC-002 camera:86 |
| MA-H3-09 | `/DRONEVIEW /FLYOVER` | intent[minimax_h3] | SRC-001 SKILL:77 |
| MA-H3-10 | `/DUTCH:L /MCU` | intent[minimax_h3] | SRC-002 camera:96 |
| MA-H3-11 | `/RACKFOCUS:FG>BG /MS` | intent[minimax_h3] | SRC-004 lexicon:149 |
| MA-H3-12 | `/BIRDSEYE /EWS` | intent[minimax_h3] | SRC-005 SKILL:121 |

## kling

| ID | Input | Expect | Source |
|---|---|---|---|
| MA-KZ-01 | `/MS /LOWANGLE /DOLLYIN:SLOW /LENS50` | intent[kling] | spec section 24 |
| MA-KZ-02 | `/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` | intent[kling] | spec section 23 |
| MA-KZ-03 | `/CU /SHALLOW /PORTRAITLENS` | intent[kling] | SRC-002 camera:244 |
| MA-KZ-04 | `/WS /HIGHANGLE /STATIC` | intent[kling] | SRC-001 SKILL:189 |
| MA-KZ-05 | `/OTS:A>B /MCU /EYELINE:B>OFFL` | intent[kling] | SRC-004 cinlang:350-355 |
| MA-KZ-06 | `/TOPDOWN /EWS` | intent[kling] | SRC-002 camera:99 |
| MA-KZ-07 | `/ORBIT:R:90 /LOWANGLE` | intent[kling] | SRC-001 SKILL:190 |
| MA-KZ-08 | `/POV:A /HANDHELD` | intent[kling] | SRC-002 camera:86 |
| MA-KZ-09 | `/DRONEVIEW /FLYOVER` | intent[kling] | SRC-001 SKILL:77 |
| MA-KZ-10 | `/DUTCH:L /MCU` | intent[kling] | SRC-002 camera:96 |
| MA-KZ-11 | `/RACKFOCUS:FG>BG /MS` | intent[kling] | SRC-004 lexicon:149 |
| MA-KZ-12 | `/BIRDSEYE /EWS` | intent[kling] | SRC-005 SKILL:121 |

## kling:en

| ID | Input | Expect | Source |
|---|---|---|---|
| MA-KE-01 | `/MS /LOWANGLE /DOLLYIN:SLOW /LENS50` | intent[kling:en] | spec section 24 |
| MA-KE-02 | `/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` | intent[kling:en] | spec section 23 |
| MA-KE-03 | `/CU /SHALLOW /PORTRAITLENS` | intent[kling:en] | SRC-002 camera:244 |
| MA-KE-04 | `/WS /HIGHANGLE /STATIC` | intent[kling:en] | SRC-001 SKILL:189 |
| MA-KE-05 | `/OTS:A>B /MCU /EYELINE:B>OFFL` | intent[kling:en] | SRC-004 cinlang:350-355 |
| MA-KE-06 | `/TOPDOWN /EWS` | intent[kling:en] | SRC-002 camera:99 |
| MA-KE-07 | `/ORBIT:R:90 /LOWANGLE` | intent[kling:en] | SRC-001 SKILL:190 |
| MA-KE-08 | `/POV:A /HANDHELD` | intent[kling:en] | SRC-002 camera:86 |
| MA-KE-09 | `/DRONEVIEW /FLYOVER` | intent[kling:en] | SRC-001 SKILL:77 |
| MA-KE-10 | `/DUTCH:L /MCU` | intent[kling:en] | SRC-002 camera:96 |
| MA-KE-11 | `/RACKFOCUS:FG>BG /MS` | intent[kling:en] | SRC-004 lexicon:149 |
| MA-KE-12 | `/BIRDSEYE /EWS` | intent[kling:en] | SRC-005 SKILL:121 |

## veo

| ID | Input | Expect | Source |
|---|---|---|---|
| MA-VEO-01 | `/MS /LOWANGLE /DOLLYIN:SLOW /LENS50` | intent[veo] | spec section 24 |
| MA-VEO-02 | `/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` | intent[veo] | spec section 23 |
| MA-VEO-03 | `/CU /SHALLOW /PORTRAITLENS` | intent[veo] | SRC-002 camera:244 |
| MA-VEO-04 | `/WS /HIGHANGLE /STATIC` | intent[veo] | SRC-001 SKILL:189 |
| MA-VEO-05 | `/OTS:A>B /MCU /EYELINE:B>OFFL` | intent[veo] | SRC-004 cinlang:350-355 |
| MA-VEO-06 | `/TOPDOWN /EWS` | intent[veo] | SRC-002 camera:99 |
| MA-VEO-07 | `/ORBIT:R:90 /LOWANGLE` | intent[veo] | SRC-001 SKILL:190 |
| MA-VEO-08 | `/POV:A /HANDHELD` | intent[veo] | SRC-002 camera:86 |
| MA-VEO-09 | `/DRONEVIEW /FLYOVER` | intent[veo] | SRC-001 SKILL:77 |
| MA-VEO-10 | `/DUTCH:L /MCU` | intent[veo] | SRC-002 camera:96 |
| MA-VEO-11 | `/RACKFOCUS:FG>BG /MS` | intent[veo] | SRC-004 lexicon:149 |
| MA-VEO-12 | `/BIRDSEYE /EWS` | intent[veo] | SRC-005 SKILL:121 |

## generic_image

| ID | Input | Expect | Source |
|---|---|---|---|
| MA-GI-01 | `/MS /LOWANGLE /DOLLYIN:SLOW /LENS50` | intent[generic_image]; still[generic_image] | spec section 24 |
| MA-GI-02 | `/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` | intent[generic_image]; still[generic_image] | spec section 23 |
| MA-GI-03 | `/CU /SHALLOW /PORTRAITLENS` | intent[generic_image]; still[generic_image] | SRC-002 camera:244 |
| MA-GI-04 | `/WS /HIGHANGLE /STATIC` | intent[generic_image]; still[generic_image] | SRC-001 SKILL:189 |
| MA-GI-05 | `/OTS:A>B /MCU /EYELINE:B>OFFL` | intent[generic_image]; still[generic_image] | SRC-004 cinlang:350-355 |
| MA-GI-06 | `/TOPDOWN /EWS` | intent[generic_image]; still[generic_image] | SRC-002 camera:99 |
| MA-GI-07 | `/ORBIT:R:90 /LOWANGLE` | intent[generic_image]; still[generic_image] | SRC-001 SKILL:190 |
| MA-GI-08 | `/POV:A /HANDHELD` | intent[generic_image]; still[generic_image] | SRC-002 camera:86 |
| MA-GI-09 | `/DRONEVIEW /FLYOVER` | intent[generic_image]; still[generic_image] | SRC-001 SKILL:77 |
| MA-GI-10 | `/DUTCH:L /MCU` | intent[generic_image]; still[generic_image] | SRC-002 camera:96 |
| MA-GI-11 | `/RACKFOCUS:FG>BG /MS` | intent[generic_image]; still[generic_image] | SRC-004 lexicon:149 |
| MA-GI-12 | `/BIRDSEYE /EWS` | intent[generic_image]; still[generic_image] | SRC-005 SKILL:121 |

## flux

| ID | Input | Expect | Source |
|---|---|---|---|
| MA-FLX-01 | `/MS /LOWANGLE /DOLLYIN:SLOW /LENS50` | intent[flux]; still[flux] | spec section 24 |
| MA-FLX-02 | `/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` | intent[flux]; still[flux] | spec section 23 |
| MA-FLX-03 | `/CU /SHALLOW /PORTRAITLENS` | intent[flux]; still[flux] | SRC-002 camera:244 |
| MA-FLX-04 | `/WS /HIGHANGLE /STATIC` | intent[flux]; still[flux] | SRC-001 SKILL:189 |
| MA-FLX-05 | `/OTS:A>B /MCU /EYELINE:B>OFFL` | intent[flux]; still[flux] | SRC-004 cinlang:350-355 |
| MA-FLX-06 | `/TOPDOWN /EWS` | intent[flux]; still[flux] | SRC-002 camera:99 |
| MA-FLX-07 | `/ORBIT:R:90 /LOWANGLE` | intent[flux]; still[flux] | SRC-001 SKILL:190 |
| MA-FLX-08 | `/POV:A /HANDHELD` | intent[flux]; still[flux] | SRC-002 camera:86 |
| MA-FLX-09 | `/DRONEVIEW /FLYOVER` | intent[flux]; still[flux] | SRC-001 SKILL:77 |
| MA-FLX-10 | `/DUTCH:L /MCU` | intent[flux]; still[flux] | SRC-002 camera:96 |
| MA-FLX-11 | `/RACKFOCUS:FG>BG /MS` | intent[flux]; still[flux] | SRC-004 lexicon:149 |
| MA-FLX-12 | `/BIRDSEYE /EWS` | intent[flux]; still[flux] | SRC-005 SKILL:121 |

## qwen_image

| ID | Input | Expect | Source |
|---|---|---|---|
| MA-QI-01 | `/MS /LOWANGLE /DOLLYIN:SLOW /LENS50` | intent[qwen_image]; still[qwen_image] | spec section 24 |
| MA-QI-02 | `/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` | intent[qwen_image]; still[qwen_image] | spec section 23 |
| MA-QI-03 | `/CU /SHALLOW /PORTRAITLENS` | intent[qwen_image]; still[qwen_image] | SRC-002 camera:244 |
| MA-QI-04 | `/WS /HIGHANGLE /STATIC` | intent[qwen_image]; still[qwen_image] | SRC-001 SKILL:189 |
| MA-QI-05 | `/OTS:A>B /MCU /EYELINE:B>OFFL` | intent[qwen_image]; still[qwen_image] | SRC-004 cinlang:350-355 |
| MA-QI-06 | `/TOPDOWN /EWS` | intent[qwen_image]; still[qwen_image] | SRC-002 camera:99 |
| MA-QI-07 | `/ORBIT:R:90 /LOWANGLE` | intent[qwen_image]; still[qwen_image] | SRC-001 SKILL:190 |
| MA-QI-08 | `/POV:A /HANDHELD` | intent[qwen_image]; still[qwen_image] | SRC-002 camera:86 |
| MA-QI-09 | `/DRONEVIEW /FLYOVER` | intent[qwen_image]; still[qwen_image] | SRC-001 SKILL:77 |
| MA-QI-10 | `/DUTCH:L /MCU` | intent[qwen_image]; still[qwen_image] | SRC-002 camera:96 |
| MA-QI-11 | `/RACKFOCUS:FG>BG /MS` | intent[qwen_image]; still[qwen_image] | SRC-004 lexicon:149 |
| MA-QI-12 | `/BIRDSEYE /EWS` | intent[qwen_image]; still[qwen_image] | SRC-005 SKILL:121 |

## qwen_image_edit

| ID | Input | Expect | Source |
|---|---|---|---|
| MA-QE-01 | `/MS /LOWANGLE /DOLLYIN:SLOW /LENS50` | intent[qwen_image_edit]; still[qwen_image_edit] | spec section 24 |
| MA-QE-02 | `/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` | intent[qwen_image_edit]; still[qwen_image_edit] | spec section 23 |
| MA-QE-03 | `/CU /SHALLOW /PORTRAITLENS` | intent[qwen_image_edit]; still[qwen_image_edit] | SRC-002 camera:244 |
| MA-QE-04 | `/WS /HIGHANGLE /STATIC` | intent[qwen_image_edit]; still[qwen_image_edit] | SRC-001 SKILL:189 |
| MA-QE-05 | `/OTS:A>B /MCU /EYELINE:B>OFFL` | intent[qwen_image_edit]; still[qwen_image_edit] | SRC-004 cinlang:350-355 |
| MA-QE-06 | `/TOPDOWN /EWS` | intent[qwen_image_edit]; still[qwen_image_edit] | SRC-002 camera:99 |
| MA-QE-07 | `/ORBIT:R:90 /LOWANGLE` | intent[qwen_image_edit]; still[qwen_image_edit] | SRC-001 SKILL:190 |
| MA-QE-08 | `/POV:A /HANDHELD` | intent[qwen_image_edit]; still[qwen_image_edit] | SRC-002 camera:86 |
| MA-QE-09 | `/DRONEVIEW /FLYOVER` | intent[qwen_image_edit]; still[qwen_image_edit] | SRC-001 SKILL:77 |
| MA-QE-10 | `/DUTCH:L /MCU` | intent[qwen_image_edit]; still[qwen_image_edit] | SRC-002 camera:96 |
| MA-QE-11 | `/RACKFOCUS:FG>BG /MS` | intent[qwen_image_edit]; still[qwen_image_edit] | SRC-004 lexicon:149 |
| MA-QE-12 | `/BIRDSEYE /EWS` | intent[qwen_image_edit]; still[qwen_image_edit] | SRC-005 SKILL:121 |
## Model-specific wording (evidence in models/*.md)

| ID | Input | Expect | Source |
|---|---|---|---|
| MS-H3-01 | `/MS /DOLLYIN:MS>MCU` | r[minimax_h3]~starts on a medium shot; r[minimax_h3]~final frame is a medium close-up; r[minimax_h3]!~small amplitude | LOCAL-002 H3LAB-PUSH-01 |
| MS-H3-02 | `/STATIC /MS` | r[minimax_h3]~holds a Static Shot throughout | LOCAL-002 H3LAB-STATIC-01 |
| MS-H3-03 | `/TRACK /MS` | r[minimax_h3]~inside the frame the entire way | LOCAL-002 H3LAB-TRACK-01 |
| MS-H3-04 | `/ORBIT:R:FULL /MS` | r[minimax_h3]~all the way around in an arc shot; r[minimax_h3]!~large amplitude; r[minimax_h3]!~fast speed; warn[minimax_h3]~orbit-360 | PROJECT_GOAL fidelity rule 1: no unrequested modifier; SRC-009 orbit-360 stays a warning |
| MS-H3-05 | `/TRACKSIDE:R /GIMBAL /FS` | r[minimax_h3]!~gimbal; r[minimax_h3]~feet included | SRC-009 gear.md (never name the rig); spec section 23 |
| MS-H3-06 | `/WHIPPAN:R:DOOR` | r[minimax_h3]~lands on the door; r[minimax_h3]~holds on the door until the end | SRC-009 shots/whip-pan.md |
| MS-H3-07 | `/DUTCH:L /MS` | r[minimax_h3]~horizon is tilted | SRC-009 shots/dutch-angle.md |
| MS-H3-08 | `/STATIC /RACKFOCUS:A>B /MS` | r[minimax_h3]~racks from; r[minimax_h3]~framing does not change; notype=HARD_CONFLICT | SRC-009 shots/rack-focus.md |
| MS-H3-09 | `/LENS:24 /MS` | warn[minimax_h3]~cosmetic | SRC-009 gear.md |
| MS-H3-10 | `/CRASHZOOM:IN /CU` | r[minimax_h3]~large amplitude at fast speed on | SRC-009 shots/crash-zoom-in.md |
| MS-H3-11 | `/DOLLYIN` | warn[minimax_h3]~no end size; warn[minimax_h3]~reads as a zoom | LOCAL-002 H3LAB-PUSH-01; SRC-009 camera-grammar:41-43 |
| MS-H3-12 | `/PAN:L` | warn[minimax_h3]~untested | SRC-009 direction.md |
| MS-H3-13 | `S1: /WS\nS2: /CU` | warn[minimax_h3]~one shot per generation | LOCAL-002 H3LAB-CUT-01 |
| MS-H3-14 | `/FS /GROUNDLEVEL /TRACKSIDE:R /GIMBAL` | r[minimax_h3]~ground level; r[minimax_h3]~side the whole time; r[minimax_h3]~background slides past | spec section 23 |
| MS-H3-15 | `/MS /TRUCK:L` | r[minimax_h3]~in the final frame .* is on the right side of the frame; r[minimax_h3]~does not turn | LOCAL-002 H3LAB-TRUCK-01 |
| MS-H3-16 | `/MS /TRUCK:R` | r[minimax_h3]!~final frame; warn[minimax_h3]~untested | LOCAL-002 H3LAB-TRUCK-02 |
| MS-H3-17 | `/MS /TRUCK:L /TILT:UP` | r[minimax_h3]!~final frame; warn[minimax_h3]~truck left is a documented primitive | LOCAL-002 H3LAB-TRUCK-01 (verified alone only) |
| MS-H3-18 | `/MS /STATIC` | warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~ROUTING \[REF2VA/LOCAL_H3_REF2VA_PDD8_Q_416\]: shot size MEDIUM SHOT.*reliability LOW; warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~real first frame \(I2VA\); r[minimax_h3]~medium shot frames | models/minimax_h3_profile.yaml reality_evidence.LOCAL_H3_REF2VA_PDD8_Q_416.framing (H3LAB-FRAMING-SCENE-01; reality matrix framing 0/51) |
| MS-H3-19 | `/FS /STATIC` | nowarn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~text-only shot size reliability; warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~STATIC has no row measured under this scope for shot size FS. related evidence \(/MS /STATIC = A\) is not applied; nowarn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~H3_RELIABILITY | profile: a full shot is not a strict size; the locked-shot row was measured on a medium shot, so it is named and not applied to a full shot (CL-044) |
| MS-H3-20 | `/DOLLYIN:MS>MCU` | warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~ROUTING.*shot size MEDIUM SHOT; warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~DOLLYIN has a historical grade only: D | profile: the range start is the opening size; H3R-DOLLY-IN D is pre-refactor evidence |
| MS-H3-21 | `/MS /EYELEVEL /DOLLYIN:MS>MCU` | warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~what environment .* is in; warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~seed sensitivity HIGH; warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~viewpoint EYELEVEL has no row measured under this scope for shot size MS. related evidence \(/FS /EYELEVEL = D\) is not applied; nowarn[generic_video]~ROUTING | profile scene rule; the viewpoint row was measured on a full shot and is not applied to a medium shot (CL-044); other adapters untouched |
| MS-H3-22 | `/WS /TRUCK:R` | warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~TRUCK:R has no row measured under this scope for start framing WS. related evidence \(/MS /TRUCK:R = D\) is not applied; nowarn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~has a historical grade only; nowarn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~text-only shot size reliability | profile: H3R-TRUCK-R was a medium shot, so its D is named and not applied to a wide shot (CL-044); a wide shot is not a strict size |
| MS-H3-23 | `/CU /STATIC` | warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~ROUTING.*shot size CLOSE-UP.*reliability LOW | profile strict_sizes |
| MS-H3-25 | `/MS /PAN:R` | warn[minimax_h3:profile=LOCAL_H3_I2VA_PDD8_Q_416]~PAN production route.*medium_shot_first_frame: LOW \(failure behavior VARIABLE.*POST_REFACTOR_VALIDATION; warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~PAN production route.*text_only: MEDIUM; nowarn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~failure behavior VARIABLE; nowarn[minimax_h3:profile=LOCAL_H3_I2VA_PDD8_Q_416]~medium_shot_first_frame: SUBJECT_LOCKED | production_routes.PAN, each route under its own scope; the I2VA failure is not one fixed mode (H3LAB-PROD-SHOT-03, -03-R2) |
| MS-H3-26 | `/MS /PAN:R:45` | r[minimax_h3]~about 45 degrees; layer[minimax_h3:derived_visual_constraint]~turns about 45 degrees; layer[minimax_h3:camera_core]~^The camera pans right\.$ | PROJECT_GOAL fidelity rule 1: degrees are never dropped |
| MS-H3-27 | `/MS /DOLLYIN:MS>MCU:SLOW` | layer[minimax_h3:camera_core]~pushes in at slow speed; layer[minimax_h3:temporal_clarifier]~steadily over the whole video; layer[minimax_h3:derived_visual_constraint]~final frame is a medium close-up; layer[minimax_h3:negative_clarifier]~focal length stays the same | the four layers of a push |
| MS-H3-28 | `/MS /PAN:R` | layer[minimax_h3:camera_core]~^The camera pans right\.$; layer[minimax_h3:negative_clarifier]~^The camera stays in place\.$; nolayer[minimax_h3:camera_core]~stays in place | PROJECT_GOAL: core = official vocabulary; clarifier separate |
| MS-H3-29 | `/MS /TRUCK:L` | layer[minimax_h3:camera_core]~^The camera trucks left\.$; layer[minimax_h3:derived_visual_constraint]~final frame .* right side of the frame; nolayer[minimax_h3:camera_core]~final frame | the measured final-position clause is a derived constraint (LOCAL-002 H3LAB-TRUCK-01) |
| MS-H3-30 | `/MS /TILT:UP:30:FAST` | r[minimax_h3]~tilts up at fast speed; r[minimax_h3]~turns about 30 degrees | fidelity: speed token and degrees both kept |
| MS-H3-31 | `/MS /ORBIT:R:FULL:FAST` | r[minimax_h3]~at fast speed; r[minimax_h3]!~large amplitude; nowarn[minimax_h3]~orbit-360 | a requested speed is written; FULL fills the magnitude slot |
| MS-H3-32 | `/MS /PEDESTAL:UP:SMALL` | r[minimax_h3]~pedestals up with small amplitude; warn[minimax_h3]~small amplitude | fidelity: a requested amplitude is written (with the inertness warning) |
| MS-H3-33 | `/CRASHZOOM:IN /CU` | implied=CRASHZOOM.speed=FAST; implied=CRASHZOOM.amount=LARGE; nounspec=CRASHZOOM.speed; nounspec=CRASHZOOM.amount; unspec=CRASHZOOM.end_position; r[minimax_h3]~large amplitude at fast speed on | CL-031: the crash zoom's speed and amplitude come from its definition (registry: a sudden, very fast zoom that snaps between framings); the text is unchanged |
| MS-H3-34 | `/WHIPPAN:R:DOOR` | implied=WHIPPAN.speed=FAST; nounspec=WHIPPAN.speed; r[minimax_h3]~whip pans right | CL-031: a whip pan is a very fast pan by definition |
| MS-H3-35 | `/MS /ZOOMIN:MS>MCU` | unspec=ZOOMIN.speed; nounspec=ZOOMIN.end_position; r[minimax_h3]!~fast speed | an ordinary zoom still leaves its speed to the model |
| MS-H3-36 | `/MS /TRUCK:R` | warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~TRUCK:R has a historical grade only: D; nowarn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~no row measured | profile: H3R-TRUCK-R D (pre-refactor wording) at the shot size it was measured with |
| MS-H3-37 | `/FS /EYELEVEL` | warn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~viewpoint EYELEVEL measured H3_RELIABILITY D; nowarn[minimax_h3:profile=LOCAL_H3_REF2VA_PDD8_Q_416]~no row measured | the viewpoint table at the shot size the cell was measured with |
| MS-H3-24 | `/MS /DOLLYIN:MS>MCU` | warn[minimax_h3:profile=LOCAL_H3_I2VA_PDD8_Q_416]~DOLLYIN production route.*without_foreground_motion_anchor: ZOOM_LIKE_PUSH_IN.*with_foreground_motion_anchor: PARALLAX_ASSISTED_PUSH_IN; warn[minimax_h3:profile=LOCAL_H3_I2VA_PDD8_Q_416]~physical fidelity PARTIAL; warn[minimax_h3:profile=LOCAL_H3_I2VA_PDD8_Q_416]~PROVISIONAL: tested before mode wrapper audit; nowarn[minimax_h3:profile=LOCAL_H3_I2VA_PDD8_Q_416]~PAN production route | production_routes.DOLLYIN under the I2VA profile (H3LAB-PROD-SHOT-01, -02) |
| MS-KZ-01 | `/MS /LOWANGLE /DOLLYIN:SLOW` | r[kling]~中景; r[kling]~仰拍; r[kling]~推镜; r[kling]!~变焦推近 | SRC-004 lexicon:334-381 |
| MS-KZ-02 | `/PAN:R` | r[kling]~横摇; r[kling]!~横移 | SRC-004 lexicon:369-371 |
| MS-KZ-03 | `/TRUCK:L` | r[kling]~横移; r[kling]!~横摇 | SRC-004 lexicon:369-371 |
| MS-KE-01 | `/MS /LOWANGLE /DOLLYIN:SLOW` | r[kling:en]~slow push-in; r[kling:en]~low angle | SRC-003 fal-prompting/references/kling.md:80-84 |
| MS-VEO-01 | `/CU /RACKFOCUS:A>B /DOLLYIN:SLOW` | r[veo]~moves forward.*focus shifts | SRC-005D SKILL:68-75 (movement, then focus) |
| MS-VEO-02 | `/STATIC /WS` | r[veo]~stays locked in one position | SRC-004 vidadapt:231 |
| MS-QE-01 | `/LOWANGLE` | r[qwen_image_edit]~Change only the camera; r[qwen_image_edit]~exactly the same | SRC-004 imgadapt:38 |
| MS-QE-02 | `/LOWANGLE` | r[qwen_image_edit:zh]~只改变镜头; r[qwen_image_edit:zh]~保持完全不变 | SRC-004 imgadapt:38 |
| MS-FLX-01 | `/MS /LOWANGLE /LENS:85 /SHALLOW` | r[flux]~^A medium shot | SRC-004 imgadapt:66-83 (size and angle first) |

## STRICT mode (spec section 26)

| ID | Input | Expect | Source |
|---|---|---|---|
| STRICT-01 | `/MS /LOWANGLE` | strict[generic_video]; strict[minimax_h3]; strict[kling]; strict[kling:en]; strict[veo] | spec section 26 |
| STRICT-02 | `/MS /LOWANGLE` | strict[generic_image]; strict[flux]; strict[qwen_image]; strict[qwen_image_edit] | spec section 26 |
| STRICT-03 | `/CINEMATIC /MS` | strict[generic_video]; strict[minimax_h3]; strict[kling] | 07-D26 |
| STRICT-04 | `/PORTRAIT` | strict[generic_video]; hasnot=SHALLOW; hasnot=CU | 04 #5 |
| STRICT-05 | `/WS /EYELEVEL` | strict[generic_video]; strict[minimax_h3] | spec section 26 |
| STRICT-06 | `/DOLLYIN` | strict[generic_video]; r[generic_video]!~\d+ ?mm | spec section 26 |

## Camera Intent Priority and Director Mode (spec sections 27, 29)

| ID | Input | Expect | Source |
|---|---|---|---|
| PRI-01 | `/STATIC @@director: /DOLLYIN:SLOW` | hasnot=DOLLYIN; rule=P00-OVERRIDDEN; has=STATIC | spec section 29 |
| PRI-02 | `/MS @@director: /SHALLOW` | has=SHALLOW; origin.SHALLOW=DIRECTOR_SUGGESTED; origin.MS=USER_SPECIFIED | spec section 27 |
| PRI-03 | `/LOWANGLE @@director: /EYELEVEL` | hasnot=EYELEVEL; state.camera.angle=LOW | spec section 29 |
| PRI-04 | `/MS @@storyboard: /CU` | hasnot=CU; state.shot.size=MS | spec section 29 (1 beats 3) |
| PRI-05 | `/DOLLYIN @@nl: /DOLLYOUT` | hasnot=DOLLYOUT | spec section 29 (1 beats 2) |
| PRI-06 | `@@director: /CU /SHALLOW` | has=CU; origin.CU=DIRECTOR_SUGGESTED | spec section 27 |
| PRI-07 | `/CU @@storyboard: /LOWANGLE @@director: /HIGHANGLE` | has=LOWANGLE; hasnot=HIGHANGLE; origin.LOWANGLE=STORYBOARD | spec section 29 (3 beats 5) |
| PRI-08 | `/MS @@director: /DOLLYIN:SLOW` | origin.DOLLYIN=DIRECTOR_SUGGESTED; intent[minimax_h3] | spec section 27 |
| PRI-09 | `/MS @@director: /SHALLOW` | mode=DIRECTOR; has=SHALLOW | a director layer is the request for Director Mode (spec section 27) |
| PRI-10 | `MODE:STRICT /MS @@director: /SHALLOW` | mode=STRICT; hasnot=SHALLOW; rule=M01-DIRECTOR-IN-STRICT; status=WARN | explicit STRICT refuses suggestions (spec section 26) |
| PRI-11 | `/MS /LOWANGLE` | mode=STRICT; mode=VIDEO | STRICT is the default (spec section 26) |
