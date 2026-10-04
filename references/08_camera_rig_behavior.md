# 08 · Camera rig behaviour

What carries the camera and how steady it is: locked (`/STATIC`, `/TRIPOD`), handheld family (`/HANDHELD`, `/SHOULDER`), stabilised (`/STEADICAM`, `/GIMBAL`, `/SLIDER`), airborne (`/DRONE`, `/FPV`).

## Rules
- **STATIC means nothing moves:** no travel, rotation or zoom. A locked frame with a focus pull is context-dependent (P12): write "the camera does not move; only the focus shifts", not just "static" (SRC-005 SKILL:107-109 vs SRC-009 shots/rack-focus.md).
- **State stillness positively.** Leaving the camera unspecified is read as licence to drift (SRC-004 failmodes F6); on H3 "The camera holds a Static Shot throughout" is the verified wording (LOCAL-002 H3LAB-STATIC-01).
- **A tripod can pan and tilt** on its head but cannot travel (G02).
- **Handheld vs stabiliser is a soft conflict** (two different looks); a drone on a gimbal and a hovering drone (`/STATIC /DRONE`) are valid.
- **FPV is a rig, not a point of view** (research/04 section 2). `/FPV /POV:A` together = a pilot's view.
- **H3: never name a rig the camera could see.** "Snorricam body rig" made H3 draw the rig; describe the effect (smooth, level, shaking) instead (SRC-009 gear.md). The H3 adapter already does this.
- **Shake needs a reason:** a strongly shaking camera on a standing subject reads as a defect (SRC-009 shots/handheld.md).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/STATIC` | The camera does not move at all: no travel, no rotation, no zoom. (A focus change with a locked frame is CONTEXT_DEPENDENT, see conflict_matrix.) | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-005B, LOCAL-001, LOCAL-002 | /LOCKED, /LOCKEDOFF, /STILL, /FIXED |
| `/TRIPOD` | The camera is on a tripod at a fixed position: no travel. It may pan/tilt on the head if a rotation command is given; otherwise it is locked. | - | MEDIUM | SRC-004, SRC-002 | /STICKS |
| `/HANDHELD` | The camera is hand-held: continuous small organic shake and drift. /HANDHELD:SUBTLE or :STRONG. | intensity | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-009, LOCAL-001 | /SHAKYCAM, /SHAKY, /HANDHELDFOLLOW |
| `/SHOULDER` | Shoulder-mounted camera: a heavier, steadier handheld with a slight rolling sway. | - | LOW | SRC-001 | /SHOULDERMOUNT, /SHOULDERRIG |
| `/STEADICAM` | Body-worn stabilizer: smooth, floating movement that can walk with the actors. | - | MEDIUM | SRC-001, SRC-004 | /STEADI, /FLOATING |
| `/GIMBAL` | Electronic stabilizer: very smooth, level movement. | - | MEDIUM | SRC-001, SRC-004 | /STABILIZER, /STABILISED, /STABILIZED |
| `/SLIDER` | Short rail: small, smooth, straight-line moves (usually sideways or forward), strong foreground parallax. | - | MEDIUM | SRC-001, SRC-004 | /RAIL |
| `/DRONE` | The camera is carried by a drone: smooth airborne platform. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004 | /UAV |
| `/FPV` | An FPV (first-person-view) racing drone: fast, agile, can dive, weave and roll. A rig, not a character's point of view. **Rule:** FPV is not POV. | - | HIGH | SRC-001, SRC-002, SRC-007 | /FPVDRONE, /RACINGDRONE |

| Command | Image mode | Video mode |
|---|---|---|
| `/STATIC` | Nothing to convert: a still is static by nature; do not add motion blur. | Say the stillness as a positive fact: the camera stays locked in one position for the whole shot. |
| `/TRIPOD` | A steady, level frame with no shake. | The camera stays at one fixed spot; only a stated pan or tilt may turn it. |
| `/HANDHELD` | A slightly off-level, imperfect framing; blur only if the speed is FAST. | Small natural shake and drift for the whole shot (strong shake only when STRONG). |
| `/SHOULDER` | Framing at an operator's shoulder height, slightly imperfect. | A slight rolling sway as if carried on an operator's shoulder. |
| `/STEADICAM` | A smooth, level frame. | Smooth, floating movement with no shake. |
| `/GIMBAL` | A smooth, level frame. | Very smooth, level movement with no shake. |
| `/SLIDER` | A smooth, level frame, usually with a foreground element. | A short, smooth, straight-line move on a rail. |
| `/DRONE` | Seen from a drone's position in the air. | Smooth airborne movement. |
| `/FPV` | An agile low-flying drone's view, as a moment in fast flight. | Fast, agile flight that can dive, weave and bank. |
<!-- END GENERATED -->
