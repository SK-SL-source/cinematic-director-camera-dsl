# 01 · Shot size

How large the subject appears in the frame. One size per shot (exclusive dimension `shot.size`).

## Rules
- **Size is not lens.** `/WS` is a framing; `/WIDEANGLE` is a lens. Never convert one into the other (REG-01; research/04 #1-2).
- **Cut ladder** (for jump-cut checks): EWS 1 · WS 2 · MS 3 · MCU 4 · CU 5 · ECU 6. FS, MFS and COWBOY sit on the WS rung (SRC-004 cinlang:36, lexicon:341). Adjacent shots of the same subject should differ by two rungs or by a real angle change.
- **With a move, a static size is the opening frame.** `/MS /DOLLYIN` starts on MS. State the end with a range: `/DOLLYIN:MS>MCU` (research/07 D09). The validator blocks ranges that go the wrong way (`/DOLLYIN:CU>WS`).
- **Function is not size.** Insert, reaction and cutaway are shot functions (13_continuity.md); pair them with a size.
- **AI note:** models are most reliable from MS to CU; EWS invents distant faces, ECU melts details (SRC-004 cinlang:54-56). On H3 a wide *framing* must be asked for as framing; a wide lens does nothing (SRC-009 framing.md).

## Traps
| Word | Reads as | Why |
|---|---|---|
| LONG SHOT | `/WS` (warned) | some people mean a full shot (research/04 #3) |
| MLS | `/MFS` knees up (warned) | one source says mid-thigh = `/COWBOY` |
| Macro shot | `/ECU /MACRO` | macro is a lens (09_lens_optics.md) |

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/EWS` | The subject is very small (about an eighth of the frame height or less) inside a vast environment; the place dominates. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004 | /ELS, /EXTREMEWIDE, /EXTREMELONGSHOT, /XWS |
| `/WS` | The whole body is visible and the surroundings take a large share of the frame. A shot SIZE, never a lens. **Rule:** Never resolve WS to a wide-angle lens, and never resolve WIDEANGLE to WS. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004 | /WIDESHOT, /WIDE, /LS, /LONGSHOT |
| `/FS` | The subject fills the frame height from head to toe, with little room above and below. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005 | /FULLBODY, /FULLSHOT |
| `/MFS` | Framed from the knees up. | - | HIGH | SRC-002, SRC-004 | /MEDIUMFULL, /MWS, /MEDIUMWIDE, /MLS |
| `/COWBOY` | Framed from mid-thigh up. | - | LOW | SRC-002 | /COWBOYSHOT, /AMERICANSHOT |
| `/MS` | Framed from the waist up. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, LOCAL-002 | /MEDIUMSHOT, /MEDIUM, /MID |
| `/MCU` | Framed from the chest up. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, LOCAL-002 | /MEDIUMCLOSEUP |
| `/CU` | Head and shoulders; the face carries the frame. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-006, LOCAL-001 | /CLOSEUP, /CLOSE |
| `/ECU` | A single detail fills the frame: an eye, a mouth, a hand, an object part. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004 | /EXTREMECLOSEUP, /XCU, /BCU |

| Command | Image mode | Video mode |
|---|---|---|
| `/EWS` | Frame the subject tiny in a vast space. | Opening or holding frame with the subject tiny in a vast space. |
| `/WS` | Frame the full figure with plenty of surroundings. | Frame the full figure with plenty of surroundings. |
| `/FS` | Frame the subject from head to toe; the feet stay inside the frame. | Keep the subject from head to toe inside the frame; the feet stay in frame for the whole shot unless a movement changes the size. |
| `/MFS` | Frame the subject from the knees up. | Frame the subject from the knees up. |
| `/COWBOY` | Frame the subject from mid-thigh up. | Frame the subject from mid-thigh up. |
| `/MS` | Frame the subject from the waist up. | Frame the subject from the waist up (the opening frame when a movement changes the size). |
| `/MCU` | Frame the subject from the chest up. | Frame the subject from the chest up. |
| `/CU` | Frame the face (head and shoulders). | Frame the face (head and shoulders); the head stays inside the frame. |
| `/ECU` | One detail fills the frame. | One detail fills the frame. |
<!-- END GENERATED -->
