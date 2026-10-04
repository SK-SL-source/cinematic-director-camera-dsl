# Tests · Conflicts

> Every conflict type from `registry/conflict_matrix.yaml` (research/07 D12). The validator must
> understand camera semantics: "different commands" is not a conflict by itself (spec section 18).

## HARD_CONFLICT

| ID | Input | Expect | Source |
|---|---|---|---|
| CONF-001 | `/LOWANGLE /HIGHANGLE` | type=HARD_CONFLICT; rule=DIM-EXCLUSIVE; status=ERROR | spec section 18; 07-D04 |
| CONF-002 | `/CU /WS` | type=HARD_CONFLICT; rule=DIM-EXCLUSIVE | spec section 18 |
| CONF-003 | `/STATIC /HANDHELD` | type=HARD_CONFLICT; status=ERROR | spec section 18 |
| CONF-004 | `/STATIC /PAN:R` | rule=G01-STATIC-MOVE; type=HARD_CONFLICT | SRC-005 SKILL:107-109 |
| CONF-005 | `/TRIPOD /DOLLYIN` | rule=G02-TRIPOD-TRAVEL | SRC-004 lexicon:148 |
| CONF-006 | `/HIGHANGLE /TOPDOWN` | type=HARD_CONFLICT; rule=DIM-EXCLUSIVE | 04 section 2 (REG-09) |
| CONF-007 | `/EYELEVEL /HIPLEVEL` | type=HARD_CONFLICT | 04 section 2 EYE LEVEL |
| CONF-008 | `/POV:A /OTS:A>B` | type=HARD_CONFLICT | 03 B |
| CONF-009 | `/SHALLOW /DEEPFOCUS` | type=HARD_CONFLICT | SRC-004 cinlang:178-187 |
| CONF-010 | `/CENTER /THIRDS:L` | type=HARD_CONFLICT | SRC-004 cinlang:416-417 |
| CONF-011 | `/FOLLOW /LEAD` | type=HARD_CONFLICT | SRC-001 ref01:115-116 |
| CONF-012 | `/FOLLOW /FRONTAL` | rule=P71-FOLLOW-FRONTAL | SRC-001 ref01:115 |
| CONF-013 | `/TOPDOWN /GROUNDLEVEL` | rule=P70-TOPDOWN-GROUND | SRC-002 camera:143 |
| CONF-014 | `/MACRO /EWS` | rule=P74-MACRO-WIDE | SRC-002 camera:248 |
| CONF-015 | `/LENS:24 /TELEPHOTO` | rule=R03-LENS-CLASS-RANGE; status=ERROR | SRC-004 cinlang:123-137 |
| CONF-016 | `/DOLLYIN:CU>WS` | rule=R02-SIZE-RANGE-DIRECTION; type=HARD_CONFLICT | SRC-002 camera:283-287 |
| CONF-017 | `/MS /DOLLYIN:CU>ECU` | rule=R01-SIZE-RANGE-START | LOCAL-002 H3LAB-PUSH-01 |
| CONF-018 | `/THIRDS:L /LOOKROOM:L` | rule=R04-THIRDS-LOOKROOM | SRC-004 cinlang:402-406 |
| CONF-019 | `/TRACKSIDE:R /SCREEN:R2L` | rule=R05-TRACK-SCREEN | SRC-004 cinlang:328-338 |
| CONF-020 | `/POV:A /EYELINE:A>CAM` | rule=R06-POV-OWNER-LOOKCAM | SRC-005B h3guide:70 |
| CONF-021 | `/CLEANOTS:A>B /TWOSHOT` | rule=P73-CLEANOTS-TWOSHOT | SRC-004 cinlang:268 |
| CONF-022 | `/DRONEVIEW /GROUNDLEVEL` | type=HARD_CONFLICT | 04 #10 |
| CONF-023 | `/BIRDSEYE /LOWANGLE` | type=HARD_CONFLICT | 04 #9 |
| CONF-024 | `/CRASHZOOM:IN /DOLLYZOOM:IN` | rule=P75-CRASH-DOLLYZOOM | SRC-009 shots/dolly-zoom.md |
| CONF-025 | `/FLYOVER /TRIPOD` | type=HARD_CONFLICT | SRC-001 SKILL:77 |

## SEQUENTIAL_ONLY (opposite directions on one channel)

| ID | Input | Expect | Source |
|---|---|---|---|
| CONF-026 | `/DOLLYIN /DOLLYOUT` | type=SEQUENTIAL_ONLY; status=ERROR | SRC-002 camera:180; spec section 19 |
| CONF-027 | `/PAN:L /PAN:R` | type=SEQUENTIAL_ONLY | SRC-002 camera:180 |
| CONF-028 | `/CRANE:UP /PEDESTAL:DOWN` | type=SEQUENTIAL_ONLY | SRC-002 camera:180 (Crane Up + Down) |
| CONF-029 | `/TRUCK:L /TRACKSIDE:R` | type=SEQUENTIAL_ONLY | 07-D04 channels |
| CONF-030 | `/ZOOMIN /ZOOMOUT` | type=SEQUENTIAL_ONLY | 07-D04 channels |
| CONF-031 | `/TILT:UP /TILT:DOWN` | type=SEQUENTIAL_ONLY | 07-D04 channels |
| CONF-032 | `/ORBIT:L /ORBIT:R` | type=SEQUENTIAL_ONLY | 07-D04 channels |
| CONF-033 | `/ORBIT:CW /ORBIT:R` | type=SEQUENTIAL_ONLY | 07-D06 (CW = camera-left) |

## SOFT_CONFLICT

| ID | Input | Expect | Source |
|---|---|---|---|
| CONF-034 | `/HANDHELD /GIMBAL` | rule=P40-HANDHELD-STABILIZER; type=SOFT_CONFLICT; status=WARN | SRC-001 SKILL:74-76 |
| CONF-035 | `/STEADICAM /GIMBAL` | rule=P41-STEADICAM-GIMBAL | SRC-001 SKILL:76 |
| CONF-036 | `/BIRDSEYE /HIGHANGLE` | rule=P45-BIRDSEYE-HIGHANGLE; notype=HARD_CONFLICT | 04 #9 |
| CONF-037 | `/WORMSEYE /LOWANGLE` | rule=P46-WORMSEYE-LOWANGLE; notype=HARD_CONFLICT | SRC-002 camera:142 |
| CONF-038 | `/INSERT:LETTER /WS` | rule=P51-INSERT-WIDE | SRC-004 lexicon:347 |
| CONF-039 | `/ORBIT:R /PAN:L` | rule=P57-ORBIT-PAN; notype=SEQUENTIAL_ONLY | SRC-004 lexicon:145 |
| CONF-040 | `/DOLLYIN /PAN:R /TILT:UP` | rule=R07-MOTION-OVERLOAD; notype=HARD_CONFLICT; status=WARN | SRC-002 camera:297-304; SRC-009 camera-grammar:65-76 |
| CONF-041 | `/DOLLYIN:SLOW /DOLLYIN:FAST` | rule=R11-SPEED-MISMATCH | SRC-004 lexicon:153-166 |
| CONF-042 | `/FISHEYE /WIDEANGLE` | rule=P60-FISHEYE-WIDE; notype=HARD_CONFLICT | SRC-002 camera:97 |

## CONTEXT_DEPENDENT

| ID | Input | Expect | Source |
|---|---|---|---|
| CONF-043 | `/STATIC /RACKFOCUS:FG>BG` | rule=P12-STATIC-RACK; type=CONTEXT_DEPENDENT; notype=HARD_CONFLICT | SRC-005 vs SRC-009 (04 section 2) |
| CONF-044 | `/DOLLYIN /ZOOMIN` | rule=P10-DOLLYIN-ZOOMIN; type=CONTEXT_DEPENDENT | SRC-004 lexicon:134 |
| CONF-045 | `/GROUNDLEVEL /HIGHANGLE` | rule=P14-GROUND-HIGHANGLE | SRC-004 cinlang:79 |
| CONF-046 | `/DRONEVIEW /HANDHELD` | rule=P30-AERIAL-HANDHELD | SRC-002 |
| CONF-047 | `/SLIDER /ORBIT:R` | rule=P20-SLIDER-ORBIT | SRC-001 ref01:134 |
| CONF-048 | `/DRONEVIEW /LOWANGLE` | rule=P16-DRONEVIEW-LOWANGLE; notype=HARD_CONFLICT | 07-D05 |

## SPECIAL_TECHNIQUE

| ID | Input | Expect | Source |
|---|---|---|---|
| CONF-049 | `/DOLLYIN /ZOOMOUT` | type=SPECIAL_TECHNIQUE; canon=DOLLYZOOM; move.0.direction=IN; status=OK | SRC-002 camera:41; SRC-004 lexicon:150 |
| CONF-050 | `/DOLLYOUT /ZOOMIN` | type=SPECIAL_TECHNIQUE; canon=DOLLYZOOM; move.0.direction=OUT | SRC-002 camera:42 |
| CONF-051 | `/PUSHIN /ZOOMOUT` | canon=DOLLYZOOM; move.0.direction=IN | via alias |
| CONF-052 | `/MS /DOLLYIN:SLOW /ZOOMOUT` | canon=MS,DOLLYZOOM; move.0.speed=SLOW | speed carried over |

## Not conflicts (different mechanisms, spec section 18)

| ID | Input | Expect | Source |
|---|---|---|---|
| CONF-053 | `/PAN:R /TRUCK:R` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; status=OK | spec section 18 |
| CONF-054 | `/TILT:UP /PEDESTAL:UP` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY | 04 #20-21 |
| CONF-055 | `/DOLLYIN /DUTCH:L` | status=OK | SRC-002 camera:175 |
| CONF-056 | `/DRONEVIEW /TOPDOWN` | status=OK; state.camera.angle=VERTICAL_DOWN | 07-D05 (explicit angle overrides default) |
| CONF-057 | `/WORMSEYE /ELEVATED` | rule=P17-ELEVATED-WORMSEYE; notype=HARD_CONFLICT | 07-D05 |
| CONF-058 | `/PAN` | rule=R08-UNSPECIFIED-DIRECTION; status=WARN | SRC-004; SRC-012 |
| CONF-059 | `/TRACK /FOLLOW` | canon=FOLLOW; rule=R12-DUPLICATE; status=OK | specializes (07-D04) |
| CONF-060 | `/TRACKSIDE:R /TRUCK:R` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY | same channel, same direction |
