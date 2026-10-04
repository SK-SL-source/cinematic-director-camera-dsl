# 16 · Conflict rules

How the validator decides (spec sections 18-20; research/07 D04, D12-D15). "Different commands" is never a conflict by itself.

## Order of evaluation (two commands at the same time)
1. Same command twice, or a command and the general command it refines → **merged** (INFO).
2. Named technique pairs → **SPECIAL_TECHNIQUE** (`/DOLLYIN /ZOOMOUT` = dolly zoom).
3. Same movement channel, opposite directions → **SEQUENTIAL_ONLY** (wrong together, fine in sequence).
4. Explicit pair rules (below) → their type.
5. Group rules (STATIC vs any move; TRIPOD vs any travel).
6. Same exclusive dimension, different value → **HARD_CONFLICT**.
7. Otherwise **VALID** (two moves = VALID_COMBINATION).

Then segment rules run (size ranges, lens classes, thirds/lookroom, tracking vs screen direction, POV owner, motion count, missing directions). Commands in **different time segments never conflict** (VALID_SEQUENCE); a static change between segments needs a move or a cut (R09).

## Types
| Type | Meaning | Severity |
|---|---|---|
| HARD_CONFLICT | cannot be true together | ERROR |
| SEQUENTIAL_ONLY | opposite directions on one channel at once | ERROR (valid in sequence) |
| SOFT_CONFLICT | possible but pulling apart or redundant | WARN |
| CONTEXT_DEPENDENT | valid only in some situations; special wording | WARN |
| SPECIAL_TECHNIQUE | looks contradictory, is a named technique | INFO (normalised) |
| VALID_COMBINATION | different mechanisms | OK |

## Why the motion-count rule only warns
Most sources say one dominant move per clip (SRC-002 camera:297; SRC-004 SKILL:138); two compatible moves are fine (SRC-002 camera:23). SRC-009 measured on H3 that contradiction, not count, breaks a shot: three complementary primitives made the best crane rise. So three or more moves is a SOFT warning, and contradictions are what the validator blocks.

<!-- BEGIN GENERATED: table -->
| Rule | Commands | Type | Message | Evidence |
|---|---|---|---|---|
| G01-STATIC-MOVE | /STATIC + any movement | HARD_CONFLICT | STATIC means the camera does not move, rotate or zoom. | SRC-005, SRC-004, SRC-005B, LOCAL-001 |
| G02-TRIPOD-TRAVEL | /TRIPOD + any move on move.z, move.x, move.y, orbit.dir, track.mode | HARD_CONFLICT | A tripod stays at one spot; it can pan or tilt but cannot travel. | SRC-004 |
| P01-DOLLYZOOM-IN | /DOLLYIN + /ZOOMOUT | SPECIAL_TECHNIQUE | Push in while zooming out = dolly zoom (subject keeps its size, background recedes). | SRC-002, SRC-004, SRC-001, SRC-009 |
| P02-DOLLYZOOM-OUT | /DOLLYOUT + /ZOOMIN | SPECIAL_TECHNIQUE | Pull out while zooming in = dolly zoom (subject keeps its size, background looms). | SRC-002, SRC-004, SRC-001, SRC-009 |
| P10-DOLLYIN-ZOOMIN | /DOLLYIN + /ZOOMIN | CONTEXT_DEPENDENT | Push and zoom in together compound the magnification; many models collapse them into one move. | SRC-004, SRC-009 |
| P11-DOLLYOUT-ZOOMOUT | /DOLLYOUT + /ZOOMOUT | CONTEXT_DEPENDENT | Pull and zoom out together compound the widening; models may collapse them. | SRC-004, SRC-009 |
| P12-STATIC-RACK | /STATIC + /RACKFOCUS | CONTEXT_DEPENDENT | A locked frame with a focus change. Valid, but write it as 'the camera does not move; only the focus shifts', not just 'static'. | SRC-005, SRC-009, SRC-011 |
| P13-DUTCH-ROLL | /DUTCH + /ROLL | CONTEXT_DEPENDENT | A rolling Dutch angle: the cant changes during the shot. State where it starts and ends. | SRC-005 |
| P14-GROUND-HIGHANGLE | /GROUNDLEVEL + /HIGHANGLE | CONTEXT_DEPENDENT | Looking down from ground level only works if the subject is lower than the camera (in a hole, lying down, a small animal). | SRC-004 |
| P15-AERIAL-LOWANGLE | /AERIAL + /LOWANGLE | CONTEXT_DEPENDENT | Looking up from the air only works at something taller than the camera (a tower, a cliff). | SRC-004 |
| P16-DRONEVIEW-LOWANGLE | /DRONEVIEW + /LOWANGLE | CONTEXT_DEPENDENT | DRONEVIEW normally looks down; an explicit low angle overrides that and needs a taller subject. | SRC-001 |
| P17-ELEVATED-WORMSEYE | any of /WORMSEYE + any of /ELEVATED, /AERIAL | CONTEXT_DEPENDENT | A worm's-eye view is normally from the ground; from higher up it needs something far above the camera. | SRC-002 |
| P18-ULTRAWIDE-SHALLOW | /ULTRAWIDE + /SHALLOW | CONTEXT_DEPENDENT | Very wide lenses give deep focus; shallow focus needs the subject very close to the lens. | SRC-004 |
| P19-TELE-DEEP | /TELEPHOTO + /DEEPFOCUS | CONTEXT_DEPENDENT | Long lenses give shallow focus; deep focus needs a far subject and a small aperture. | SRC-004, SRC-001 |
| P20-SLIDER-ORBIT | /SLIDER + /ORBIT | CONTEXT_DEPENDENT | Only a curved slider can orbit; a straight rail cannot. | SRC-001 |
| P21-DEEPSTAGING-SHALLOW | /DEEPSTAGING + /SHALLOW | CONTEXT_DEPENDENT | Staging in depth with shallow focus leaves only one layer sharp; say which. | SRC-004 |
| P22-OTS-ECU | /OTS + /ECU | CONTEXT_DEPENDENT | An over-the-shoulder at extreme close-up leaves little room for the foreground shoulder. | SRC-004 |
| P23-EWS-OTS | /EWS + /OTS | CONTEXT_DEPENDENT | An over-the-shoulder onto a vast view: the foreground person frames a distant scene. | SRC-004 |
| P24-CU-TWOSHOT | /CU + /TWOSHOT | CONTEXT_DEPENDENT | Two faces at close-up distance only fit in a wide frame; in 9:16 stage them in depth. | SRC-004 |
| P25-FGFOCUS-RACK | /FGFOCUS + /RACKFOCUS | CONTEXT_DEPENDENT | A fixed focus target plus a rack: read as the rack's starting plane. | SRC-005 |
| P26-MGFOCUS-RACK | /MGFOCUS + /RACKFOCUS | CONTEXT_DEPENDENT | A fixed focus target plus a rack: read as the rack's starting plane. | SRC-005 |
| P27-BGFOCUS-RACK | /BGFOCUS + /RACKFOCUS | CONTEXT_DEPENDENT | A fixed focus target plus a rack: read as the rack's starting plane. | SRC-005 |
| P28-SYMMETRY-DUTCH | /SYMMETRY + /DUTCH | CONTEXT_DEPENDENT | A tilted horizon breaks mirror symmetry unless the symmetry is intentionally canted. | SRC-004 |
| P29-MACRO-FISHEYE | /MACRO + /FISHEYE | CONTEXT_DEPENDENT | Wide macro (probe) lenses exist but are rare; expect the model to pick one look. |  |
| P30-AERIAL-HANDHELD | any of /DRONEVIEW, /FLYOVER, /DRONEREVEAL, /AERIAL + any of /HANDHELD, /SHOULDER | CONTEXT_DEPENDENT | Handheld in the air only from an aircraft door; a drone cannot be handheld. | SRC-002 |
| P40-HANDHELD-STABILIZER | any of /HANDHELD, /SHOULDER + any of /GIMBAL, /STEADICAM | SOFT_CONFLICT | Handheld shake and stabilised smoothness pull against each other. | SRC-001, SRC-002 |
| P41-STEADICAM-GIMBAL | /STEADICAM + /GIMBAL | SOFT_CONFLICT | Two stabilisers; the picture is the same. Keep one. | SRC-001 |
| P42-GIMBAL-SLIDER | /GIMBAL + /SLIDER | SOFT_CONFLICT | Gimbal on a slider is unusual; both mean smooth movement. Keep the one that describes the move. |  |
| P43-STATIC-STABILIZER | any of /STATIC + any of /GIMBAL, /STEADICAM, /SLIDER | SOFT_CONFLICT | A stabiliser implies movement; for a locked camera /STATIC alone is enough. | SRC-004 |
| P44-FPV-GIMBAL | /FPV + /GIMBAL | SOFT_CONFLICT | FPV drones usually fly without a stabilising gimbal; the looks conflict. | SRC-002 |
| P45-BIRDSEYE-HIGHANGLE | /BIRDSEYE + /HIGHANGLE | SOFT_CONFLICT | Bird's-eye is steeper than a high angle (straight down). Keep one. | SRC-001, SRC-002, SRC-005 |
| P46-WORMSEYE-LOWANGLE | /WORMSEYE + /LOWANGLE | SOFT_CONFLICT | Worm's-eye is the extreme of a low angle (straight up). Keep one. | SRC-002, SRC-005 |
| P47-SYMMETRY-THIRDS | /SYMMETRY + /THIRDS | SOFT_CONFLICT | Mirror symmetry wants a centered subject; thirds wants it off-center. | SRC-004 |
| P48-DEEP-TARGET | any of /DEEPFOCUS + any of /FGFOCUS, /MGFOCUS, /BGFOCUS | SOFT_CONFLICT | With deep focus everything is sharp; a single focus target adds nothing. | SRC-004 |
| P49-SPLIT-DEEP | /SPLITDIOPTER + /DEEPFOCUS | SOFT_CONFLICT | Deep focus already holds both planes; a split diopter is redundant. | SRC-004 |
| P50-SPLIT-RACK | /SPLITDIOPTER + /RACKFOCUS | SOFT_CONFLICT | A split diopter is the rack-free two-plane frame; racking defeats it. | SRC-004 |
| P51-INSERT-WIDE | any of /INSERT + any of /EWS, /WS, /FS, /MFS | SOFT_CONFLICT | An insert is a detail; a wide size cannot isolate it. | SRC-004, SRC-002 |
| P52-REACTION-EWS | /REACTION + /EWS | SOFT_CONFLICT | A reaction needs a readable face; at extreme wide it is lost. | SRC-004 |
| P53-REACTION-INSERT | /REACTION + /INSERT | SOFT_CONFLICT | Two different shot functions; a reaction shown only through an object detail must be stated. | SRC-004 |
| P54-OTS-SINGLE | any of /OTS, /DIRTYOTS + any of /SINGLE | SOFT_CONFLICT | A (dirty) over-the-shoulder shows part of a second person; for only one person use /CLEANOTS. | SRC-004 |
| P55-OTS-TWOSHOT | any of /OTS, /DIRTYOTS + any of /TWOSHOT | SOFT_CONFLICT | An OTS already holds both people (one as a foreground shoulder); a two-shot usually means both fully framed. | SRC-004, SRC-002 |
| P56-ORBIT-TRUCK | /ORBIT + /TRUCK | SOFT_CONFLICT | An orbit already travels sideways around the subject; an extra truck blurs the path. | SRC-004, SRC-011 |
| P57-ORBIT-PAN | /ORBIT + /PAN | SOFT_CONFLICT | An orbit already turns the camera to keep the subject centered; an extra pan fights it. | SRC-004 |
| P58-CRANE-PEDESTAL | /CRANE + /PEDESTAL | SOFT_CONFLICT | Both are vertical travel; a crane already includes the rise or fall. | SRC-004 |
| P59-CRANE-HANDHELD | /CRANE + /HANDHELD | SOFT_CONFLICT | A crane is a smooth arm move; handheld shake contradicts it. | SRC-004 |
| P60-FISHEYE-WIDE | /FISHEYE + /WIDEANGLE | SOFT_CONFLICT | A fisheye is an ultra-wide lens; keep one lens description. | SRC-002 |
| P61-TRACKSIDE-FRONTAL | /TRACKSIDE + /FRONTAL | SOFT_CONFLICT | Side tracking normally shows a profile; a subject facing the camera would be walking sideways. | SRC-004 |
| P70-TOPDOWN-GROUND | any of /TOPDOWN + any of /GROUNDLEVEL, /ANKLELEVEL | HARD_CONFLICT | A camera on the ground cannot look straight down at a subject. | SRC-002, SRC-004 |
| P71-FOLLOW-FRONTAL | /FOLLOW + /FRONTAL | HARD_CONFLICT | Following from behind shows the subject's back, not the face. | SRC-001, SRC-002 |
| P72-LEAD-REAR | /LEAD + /REAR | HARD_CONFLICT | Leading in front shows the subject's face, not the back. | SRC-001 |
| P73-CLEANOTS-TWOSHOT | /CLEANOTS + /TWOSHOT | HARD_CONFLICT | A clean over-the-shoulder keeps the foreground person out of frame; it cannot be a two-shot. | SRC-004 |
| P74-MACRO-WIDE | any of /MACRO + any of /EWS, /WS | HARD_CONFLICT | A macro lens magnifies a tiny detail; it cannot frame a wide view. | SRC-002, SRC-004 |
| P75-CRASH-DOLLYZOOM | /CRASHZOOM + /DOLLYZOOM | HARD_CONFLICT | A dolly zoom needs a zoom that exactly cancels the travel; a crash zoom cannot. | SRC-009 |
| P76-CRANE-SLIDER | /CRANE + /SLIDER | HARD_CONFLICT | A slider cannot make a crane move. | SRC-001 |
| P77-AERIAL-TRIPOD | any of /DRONEVIEW, /FLYOVER, /DRONEREVEAL + any of /TRIPOD, /SLIDER | HARD_CONFLICT | An aerial camera cannot be on a tripod or slider. | SRC-001, SRC-002 |
| P78-ECU-MANY | any of /ECU + any of /TWOSHOT, /THREESHOT, /GROUPSHOT | HARD_CONFLICT | An extreme close-up shows one detail; it cannot hold two or more people. | SRC-004, SRC-002 |
| P79-CU-MANY | any of /CU + any of /THREESHOT, /GROUPSHOT | HARD_CONFLICT | A close-up cannot hold three or more faces. | SRC-004 |
| P80-INSERT-PEOPLE | any of /INSERT + any of /TWOSHOT, /THREESHOT, /GROUPSHOT | HARD_CONFLICT | An insert is an object or action detail, not a frame of several people. | SRC-004, SRC-002 |
| P90-STATIC-DRONE | /STATIC + /DRONE | VALID_COMBINATION | A hovering drone: locked aerial frame. | SRC-002 |
| P91-DRONE-GIMBAL | /DRONE + /GIMBAL | VALID_COMBINATION | Drone cameras sit on a gimbal; smooth aerial movement. |  |
| P92-INSERT-CUTAWAY | /INSERT + /CUTAWAY | VALID_COMBINATION | An insert used as a cutaway (a detail away from the main action). | SRC-004 |
| R01-SIZE-RANGE-START | (segment rule) | HARD_CONFLICT | If a move gives a size range (MS>MCU) and a static size is also given, the static size must equal the range start. | LOCAL-002, SRC-009 |
| R02-SIZE-RANGE-DIRECTION | (segment rule) | HARD_CONFLICT | DOLLYIN, ZOOMIN and CRASHZOOM:IN must end tighter than they start; DOLLYOUT, ZOOMOUT and CRASHZOOM:OUT must end wider. Equal start and end = SOFT (no visible change). | SRC-002, SRC-009 |
| R03-LENS-CLASS-RANGE | (segment rule) | HARD_CONFLICT | A focal length must fall in the stated lens class: ULTRAWIDE <=18, WIDE 18-35, NORMAL 35-70, PORTRAIT 70-110, TELE >=110 mm (boundaries overlap on purpose). | SRC-004, SRC-003, SRC-001 |
| R04-THIRDS-LOOKROOM | (segment rule) | HARD_CONFLICT | THIRDS:X with LOOKROOM:X is impossible: the open space is on the side opposite the subject. | SRC-004 |
| R05-TRACK-SCREEN | (segment rule) | HARD_CONFLICT | TRACKSIDE:R needs SCREEN:L2R, TRACKSIDE:L needs SCREEN:R2L; FOLLOW needs AWAY (not TOWARD); LEAD needs TOWARD (not AWAY). | SRC-004, SRC-001 |
| R06-POV-OWNER-LOOKCAM | (segment rule) | HARD_CONFLICT | In /POV:A, A cannot look into the lens (/EYELINE:A>CAM): A is the camera. Another subject looking into the lens is valid (they look at A). | SRC-002, SRC-005B |
| R07-MOTION-OVERLOAD | (segment rule) | SOFT_CONFLICT | Three or more camera moves at the same time (after merges; focus pulls not counted). Warned, not blocked: SRC-009 measured three complementary moves working on H3. | SRC-002, SRC-004, SRC-010, SRC-009 |
| R08-UNSPECIFIED-DIRECTION | (segment rule) | WARNING | A directional move without a direction (PAN, TILT, TRUCK, PEDESTAL, CRANE, ROLL, WHIPPAN, TRACKSIDE, ORBIT) leaves the choice to the model. | SRC-004, SRC-012 |
| R09-STATE-JUMP | (segment rule) | CONTEXT_DEPENDENT | In a sequence, a size or angle change between segments needs a move that can cause it (or a cut). | SRC-002, SRC-009 |
| R10-SEQUENCE-IN-ONE-CLIP | (segment rule) | WARNING | Sequential moves inside one generated clip are valid DSL but risky: SRC-004 says split into two clips; SRC-002 says time-code them. Adapters add a model-specific note. | SRC-002, SRC-004 |
| R11-SPEED-MISMATCH | (segment rule) | SOFT_CONFLICT | The same channel given two different speeds at the same time. | SRC-004 |
| R12-DUPLICATE | (segment rule) | INFO | The same command (or a command and the one it specializes) twice at the same time is merged. |  |

Exclusive dimensions (same dimension, different value = HARD_CONFLICT): `shot.size`, `shot.subject_count`, `shot.viewpoint`, `shot.ots_variant`, `subject.orientation`, `camera.pitch`, `camera.height`, `camera.roll_offset`, `rig.type`, `rig.stability`, `lens.focal_class`, `focus.dof`, `focus.target`, `comp.placement`, `comp.headroom`, `cont.function`, `track.mode`.

Movement channels (opposite values at the same time = SEQUENTIAL_ONLY): `move.z` IN/OUT; `move.x` L/R; `move.y` UP/DOWN; `rot.yaw` L/R; `rot.pitch` UP/DOWN; `rot.roll` CW/CCW; `zoom.dir` IN/OUT; `orbit.dir` L/R; `track.mode` TRACK/FOLLOW/LEAD/SIDE; `focus.pull` RACK.
<!-- END GENERATED -->
