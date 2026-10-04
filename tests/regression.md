# Tests · Regression (spec section 34 — these errors must never come back)

> Each regression is attacked from several sides: resolution (which canonical command), camera state
> (which dimension), and the rendered text on several models. Evidence: research/04 section 3.
> `scripts/audit.py` fails if this file is missing or any REG row fails.

| ID | Input | Expect | Source |
|---|---|---|---|
| REG-01a | `/WIDEANGLE` | canon=WIDEANGLE; cat=LENS; hasnot=WS; state.shot.size=None; state.lens.lens_type=WIDE | WIDE SHOT ≠ WIDE-ANGLE LENS (04 #1) |
| REG-01b | `/WIDEANGLE` | r[generic_video]!~wide shot; r[minimax_h3]!~wide shot; r[kling]!~(?<!大)远景; r[generic_image]!~wide shot | 04 #1 |
| REG-01c | `/WS` | state.lens.lens_type=None; r[generic_video]!~wide-angle; r[kling]!~广角; r[flux]!~wide-angle | 04 #2 |
| REG-01d | `/WS /WIDEANGLE` | canon=WS,WIDEANGLE; notype=HARD_CONFLICT; intent[generic_video] | both, independently |
| REG-02a | `/POV:A` | canon=POV; state.shot.viewpoint=POV; r[generic_video]!~looks? (directly )?into the lens; r[minimax_h3]!~looks? (directly )?into the lens | POV ≠ LOOK AT CAMERA (04 #6) |
| REG-02b | `/LOOKCAM:A` | canon=EYELINE; hasnot=POV; state.shot.viewpoint=None; r[generic_video]~looks directly into the lens; r[generic_video]!~point of view | 04 #6 |
| REG-02c | `/POV:A /EYELINE:B>CAM` | notype=HARD_CONFLICT; intent[generic_video] | B looks at A (valid) |
| REG-03a | `/PAN:R` | canon=PAN; cat=CAMERA_ROTATION; r[generic_video]!~slides; r[minimax_h3]!~trucks; r[kling]!~横移 | PAN ≠ TRUCK (SRC-005 SKILL:112) |
| REG-03b | `/TRUCK:R` | canon=TRUCK; cat=CAMERA_TRANSLATION; r[generic_video]!~pans; r[minimax_h3]!~pans; r[kling]!~横摇 | 04 #17, #19 |
| REG-04a | `/TILT:UP` | canon=TILT; r[generic_video]!~rises straight; r[minimax_h3]!~pedestal; r[kling]!~升降 | TILT ≠ PEDESTAL (04 #20-21) |
| REG-04b | `/PEDESTAL:UP` | canon=PEDESTAL; r[generic_video]!~tilts; r[minimax_h3]!~tilts; r[kling]!~纵摇 | 04 #21 |
| REG-05a | `/DOLLYIN` | r[generic_video]!~zoom; r[minimax_h3]!~zoom; r[veo]!~zoom; r[kling]!~变焦; r[kling:en]!~zoom | DOLLY ≠ ZOOM (SRC-005 SKILL:111) |
| REG-05b | `/ZOOMIN` | r[generic_video]!~moves forward; r[generic_video]!~push; r[minimax_h3]!~push; r[kling]!~推镜 | 04 #26 |
| REG-05c | `/PUSHIN` | canon=DOLLYIN; hasnot=ZOOMIN | 04 #11 |
| REG-06a | `/ORBIT:R:90` | r[generic_video]!~(turns\|spins\|rotates) (around\|in place); r[generic_video]~does not turn; r[minimax_h3]~does not turn; r[kling]~不转身 | ORBIT ≠ SUBJECT ROTATION (04 #24) |
| REG-06b | `/TURNTABLE` | type=OUT_OF_SCOPE; hasnot=ORBIT | 04 #24 |
| REG-07a | `/RACKFOCUS:A>B` | cat=FOCUS; hasnot=DOLLYIN; r[generic_video]!~moves forward; r[generic_video]!~push; r[generic_video]~framing does not change | RACK FOCUS ≠ DOLLY (04 #27) |
| REG-07b | `/RACKFOCUS:FG>BG /STATIC` | notype=HARD_CONFLICT; r[minimax_h3]!~pushes | SRC-009 shots/rack-focus.md |
| REG-08a | `/GROUNDLEVEL` | state.camera.height=GROUND; state.camera.angle=None; r[generic_video]!~low angle; r[generic_video]!~looks up; r[kling]!~仰拍 | GROUND LEVEL ≠ LOW ANGLE (04 section 2) |
| REG-08b | `/LOWANGLE` | state.camera.angle=LOW; state.camera.height=None; r[generic_video]!~ground level | 04 section 2 |
| REG-09a | `/HIGHANGLE` | state.camera.angle=HIGH; r[generic_video]!~straight down; r[generic_video]!~top-down; r[kling]!~顶拍 | HIGH ANGLE ≠ TOP DOWN (04 section 2) |
| REG-09b | `/TOPDOWN` | state.camera.angle=VERTICAL_DOWN; r[generic_video]!~high angle; r[kling]!~俯拍 | 04 #8 |
| REG-10a | `/DRONEVIEW` | state.camera.angle=HIGH; state.camera.height=AERIAL; r[generic_video]!~straight down; r[generic_video]!~bird's-eye | DRONE VIEW ≠ BIRD'S-EYE ≠ TOP DOWN (04 #8-10) |
| REG-10b | `/BIRDSEYE` | state.camera.angle=VERTICAL_DOWN; state.camera.height=AERIAL; r[generic_video]!~drone; r[generic_video]~like a map | 04 #9 |
| REG-10c | `/TOPDOWN` | state.camera.height=None; r[generic_video]!~drone; r[generic_video]!~bird's-eye | 04 #8 |
| REG-11a | `/ORBIT:R:45 /DOLLYIN` | still[generic_image]; still[flux]; still[qwen_image]; still[qwen_image_edit] | STATIC IMAGE ≠ TEMPORAL MOVEMENT (spec section 21) |
| REG-11b | `/PAN:R /CRANE:UP` | still[generic_image]; still[flux]; still[qwen_image] | spec section 21 |
| REG-11c | `/TRUCK:L /TILT:UP` | still[generic_image]; still[qwen_image_edit] | spec section 21 |
| REG-11d | `/FLYOVER /TRACK` | still[generic_image]; still[flux] | spec section 21 |
| REG-12 | `/FPV` | canon=FPV; cat=CAMERA_RIG; state.shot.viewpoint=None | FPV ≠ POV (04 section 2) |
| REG-13 | `/DUTCHTILT` | canon=DUTCH; hasnot=TILT; state.camera.orientation=DUTCH | DUTCH TILT ≠ TILT (04 section 2) |
| REG-14 | `/ORBIT:R:45` | r[generic_image]!~subject's right; r[generic_video]~camera-right | L/R are camera-relative (07-D06) |
| REG-15a | `中景/MS，低角度/LOWANGLE。` | canon=MS,LOWANGLE; status=OK | a command may follow CJK text directly (tokenizer, 07-D38) |
| REG-15b | `/PAN:R, /TILT:UP.` | canon=PAN,TILT; arg.dir_lr=R; norule=A06-BAD-ARGUMENT | trailing punctuation is not an argument (07-D38) |
| REG-15c | `/DOLLYIN:1.5M:SLOW.` | arg.distance=1.5; norule=A06-BAD-ARGUMENT; move.0.speed=SLOW | decimal dot kept, sentence dot dropped (07-D38) |
| REG-15d | `and/or /MS (/PAN:L)` | canon=MS,PAN; norule=A05-UNKNOWN-COMMAND; norule=A06-BAD-ARGUMENT | 'and/or' is not a command; brackets are not arguments (07-D38) |
| REG-15e | `／MS /PAN：R /OTS:A＞B` | canon=MS,PAN,OTS; status=OK; state.shot.foreground_subject=A; move.0.direction=R | full-width IME characters next to DSL tokens (07-D38) |
| REG-15f | `MODE:IMAGE /PAN:R /WS` | still[generic_video]; r[generic_video]~moment within a pan | MODE:IMAGE in the text renders a still even on a video adapter (07-D38) |
| REG-16a | `/MS /TRUCK:R /PAN:L` | intent[generic_video]; intent[minimax_h3]; intent[kling]; intent[kling:en]; intent[veo]; r[generic_video]!~camera does not turn; r[kling]!~机位不动 | guard sentences never contradict a simultaneous move (07-D39) |
| REG-16b | `/WS /CRANE:UP /TILT:DOWN` | intent[generic_video]; intent[minimax_h3]; intent[kling]; r[generic_video]!~same height; r[minimax_h3]!~stays in place | 07-D39 |
| REG-16c | `/DOLLYIN /PAN:R /TILT:UP /ROLL:CW` | intent[generic_video]; intent[minimax_h3]; intent[kling]; r[generic_video]!~stays in one spot | 07-D39 |
| REG-16d | `/PEDESTAL:UP /PAN:R` | r[generic_video]!~keeps its angle; r[minimax_h3]!~staying level; r[kling]!~角度不变; intent[veo] | 07-D39 |
| REG-16e | `/PAN:R` | r[generic_video]~stays in one spot; r[minimax_h3]~stays in place; r[kling]~机位不动; r[kling:en]~camera stays in place | positive control: a lone move keeps its guard (07-D39) |
| REG-16f | `/DOLLYIN /ZOOMIN` | r[generic_video]!~focal length stays; r[minimax_h3]!~focal length stays; r[kling]!~焦距不变; r[generic_video]!~does not move | 07-D39 |
| REG-16g | `/CU /RACKFOCUS:A>B /DOLLYIN:SLOW` | intent[generic_video]; intent[veo]; intent[minimax_h3]; intent[kling]; r[veo]!~framing does not change | a rack focus with a simultaneous push must not claim a still frame (07-D39) |
| REG-16h | `/CU /RACKFOCUS:A>B` | r[generic_video]~framing does not change; r[minimax_h3]~framing does not change; r[kling]~构图不变 | positive control: RACK FOCUS ≠ camera movement (spec section 34) |
| REG-17 | `/WS /DOLLYOUT:WS>EWS` | r[minimax_h3]~final frame is an extreme wide shot; r[minimax_h3]!~\ba extreme; r[generic_video]~ends on an extreme wide shot | article before a vowel (07-D39) |
| REG-18a | `/WS /PAN:R:SLOW` | r[minimax_h3]~pans right at slow speed | SLOW is kept on H3 with the documented token (SRC-008 base-en:114; 07-D39) |
| REG-18b | `/MS /PAN:R:BRISK` | r[minimax_h3]!~speed; warn[minimax_h3]~BRISK is written as normal speed | H3 has no BRISK token; say so (07-D39) |
| REG-18c | `/MS /DOLLYIN:MS>MCU:SLOW` | r[minimax_h3]~pushes in at slow speed; r[minimax_h3]~steadily over the whole video | official speed token (SRC-008 base-en:114-115) plus the measured pacing clarifier (LOCAL-002 H3LAB-PUSH-01) |
| REG-18d | `/MS /ORBIT:R:FULL:SLOW` | r[minimax_h3]~at slow speed; r[minimax_h3]!~fast speed; warn[minimax_h3]~may stop partway | the user's speed wins; the risk is a warning (spec section 24) |
| REG-19 | `/EWS /DRONEREVEAL:BACK` | r[minimax_h3]!~fast speed; r[minimax_h3]!~large amplitude; r[minimax_h3]~pulls out | STRICT: no speed or amplitude the user did not give (spec section 26; PROJECT_GOAL fidelity rule 1) |
| REG-20 | `/WS /FOLLOW:A` | state.shot.primary_subject=A; r[minimax_h3]!~\{SUBJECT\}; r[kling]!~\{SUBJECT\}; r[generic_video]!~\{SUBJECT\} | one subject name per shot (07-D39) |
| REG-21 | `/EWS /DRONEVIEW` | r[minimax_h3]!~drone; intent[minimax_h3]; r[generic_video]~drone view; r[kling]~无人机视角 | H3 never names gear it could draw into the frame (SRC-009 gear.md); other models keep the trade term |
| REG-22 | `/WS /SCREEN:L2R` | r[kling]~\{SUBJECT\}从左向右移动 | the Chinese screen direction says who moves (07-D39) |
| REG-23 | `/WS /BIRDSEYE` | intent[minimax_h3]; r[minimax_h3]!~like a; r[minimax_h3]~Bird's-eye view: the camera is far above and looks straight down; r[generic_video]~like a map | H3 text follows the plain-English rule (H3LAB-PLAIN-01): no similes (07-D41) |
| REG-24 | `/MS /SHOULDER` | intent[minimax_h3]; r[minimax_h3]!~as if; r[minimax_h3]~carried on a shoulder | 07-D41 |
