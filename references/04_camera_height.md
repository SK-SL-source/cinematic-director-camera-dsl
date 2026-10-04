# 04 · Camera height

Where the camera physically sits (`camera.height`), independent of where it points.

## Rules
- **Decide the height before the angle; usually keep the lens level** (after SRC-004 cinlang:72-76). A level lens at a low height reads as status without announcing a "low angle".
- **GROUNDLEVEL ≠ LOWANGLE** (REG-08). `/GROUNDLEVEL` never adds an upward look; write `/LOWANGLE` or `/WORMSEYE` if you want one.
- **Heights are relative to a standing adult** (eyes ≈ 1.6 m): ground 0-0.3 m, ankle ≈ 0.1-0.2 m, knee ≈ 0.5 m, hip/waist ≈ 0.9-1.0 m, chest 1.2-1.4 m, shoulder 1.4-1.5 m, eye (via `/EYELEVEL`) 1.5-1.7 m, elevated 1.8-3 m, aerial = airborne (SRC-004 cinlang:79-90). For a seated subject everything drops about 0.4 m.
- **In shot/reverse-shot, set the height at the off-screen character's eyes** (SRC-004 cinlang:91-95).
- **AI note:** models rarely honour a number; describe what the height makes visible (SRC-004 cinlang:97-100). On H3, a sentence that puts the camera at a named spot was not obeyed (LOCAL-002 H3LAB-POSITION-01).
- **Evidence gaps:** ANKLELEVEL has no source (PROJECT_DEFINED); KNEELEVEL has one (LOW).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/GROUNDLEVEL` | The camera rests on or just above the ground (0-0.3 m). A HEIGHT: the lens can still look level. **Rule:** GROUNDLEVEL is not LOWANGLE; do not add an upward look unless /LOWANGLE or /WORMSEYE is given. | - | HIGH | SRC-002, SRC-004, SRC-005, SRC-001 | /GROUND, /FLOORLEVEL, /FLOOR |
| `/ANKLELEVEL` | The camera sits at about the subject's ankle height (about 10-20 cm). | - | PROJECT_DEFINED | - | /ANKLE |
| `/KNEELEVEL` | The camera sits at about knee height (about 0.5 m). | - | LOW | SRC-004 | /KNEE |
| `/HIPLEVEL` | The camera sits at hip/waist height (about 0.9-1.0 m). | - | HIGH | SRC-001, SRC-004, SRC-005, SRC-006 | /HIP, /WAISTLEVEL, /WAIST |
| `/CHESTLEVEL` | The camera sits at chest height (about 1.2-1.4 m). | - | MEDIUM | SRC-004, LOCAL-002 | /CHEST |
| `/SHOULDERLEVEL` | The camera sits at shoulder height of a standing adult (about 1.4-1.5 m), just below eye height. | - | MEDIUM | SRC-001, SRC-003 | /SHOULDERHEIGHT |
| `/ELEVATED` | The camera is above eye height (about 1.8-3 m, e.g. on a step or small crane) but not airborne. A HEIGHT; the axis can stay level. | - | HIGH | SRC-001, SRC-004 | /ABOVEEYE, /RAISED |
| `/AERIAL` | The camera is airborne, well above the scene (drone or aircraft altitude). | - | HIGH | SRC-001, SRC-002, SRC-005 | /AERIALVIEW |

| Command | Image mode | Video mode |
|---|---|---|
| `/GROUNDLEVEL` | Lens just above the ground; the floor or ground fills the bottom of the frame. | Lens stays just above the ground. |
| `/ANKLELEVEL` | Camera at ankle height. | Camera stays at ankle height. |
| `/KNEELEVEL` | Camera at knee height. | Camera stays at knee height. |
| `/HIPLEVEL` | Camera at waist height. | Camera stays at waist height. |
| `/CHESTLEVEL` | Camera at chest height. | Camera stays at chest height. |
| `/SHOULDERLEVEL` | Camera at shoulder height. | Camera stays at shoulder height. |
| `/ELEVATED` | Camera somewhat above head height. | Camera stays somewhat above head height. |
| `/AERIAL` | Seen from the air, high above the scene. | Seen from the air, high above the scene. |
<!-- END GENERATED -->
