# Tests · Canonical commands

> One row per canonical command (104). Generated from `registry/canonical_commands.yaml`; the Source column
> is that command's research sources (research/03). Each row checks: it resolves to itself, its category,
> no hard conflict on its own, the generic video text carries its intent markers (EN), the Kling text
> carries its Chinese markers (ZH), and movements render as a still without motion verbs.

| ID | Input | Expect | Source |
|---|---|---|---|
| CMD-001 | `/EWS` | canon=EWS; cat=SHOT_SIZE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004 (HIGH) |
| CMD-002 | `/WS` | canon=WS; cat=SHOT_SIZE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004 (HIGH) |
| CMD-003 | `/FS` | canon=FS; cat=SHOT_SIZE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005 (HIGH) |
| CMD-004 | `/MFS` | canon=MFS; cat=SHOT_SIZE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002, SRC-004 (HIGH) |
| CMD-005 | `/COWBOY` | canon=COWBOY; cat=SHOT_SIZE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002 (LOW) |
| CMD-006 | `/MS` | canon=MS; cat=SHOT_SIZE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, LOCAL-002 (HIGH) |
| CMD-007 | `/MCU` | canon=MCU; cat=SHOT_SIZE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, LOCAL-002 (HIGH) |
| CMD-008 | `/CU` | canon=CU; cat=SHOT_SIZE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-006, LOCAL-001 (HIGH) |
| CMD-009 | `/ECU` | canon=ECU; cat=SHOT_SIZE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004 (HIGH) |
| CMD-010 | `/SINGLE` | canon=SINGLE; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004 (LOW) |
| CMD-011 | `/TWOSHOT` | canon=TWOSHOT; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002, SRC-004 (HIGH) |
| CMD-012 | `/THREESHOT` | canon=THREESHOT; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004 (LOW) |
| CMD-013 | `/GROUPSHOT` | canon=GROUPSHOT; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-005 (LOW) |
| CMD-014 | `/OTS:A>B` | canon=OTS; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004 (HIGH) |
| CMD-015 | `/DIRTYOTS:A>B` | canon=DIRTYOTS; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004 (LOW) |
| CMD-016 | `/CLEANOTS:A>B` | canon=CLEANOTS; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004 (LOW) |
| CMD-017 | `/POV:A` | canon=POV; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005B, LOCAL-001 (HIGH) |
| CMD-018 | `/FRONTAL` | canon=FRONTAL; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004, SRC-001 (MEDIUM) |
| CMD-019 | `/THREEQUARTER` | canon=THREEQUARTER; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-004, LOCAL-002 (HIGH) |
| CMD-020 | `/PROFILE` | canon=PROFILE; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004 (HIGH) |
| CMD-021 | `/REAR` | canon=REAR; cat=SUBJECT_FRAMING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002, SRC-003, SRC-004 (MEDIUM) |
| CMD-022 | `/EYELEVEL` | canon=EYELEVEL; cat=CAMERA_ANGLE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-006 (HIGH) |
| CMD-023 | `/LOWANGLE` | canon=LOWANGLE; cat=CAMERA_ANGLE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-006, SRC-007 (HIGH) |
| CMD-024 | `/HIGHANGLE` | canon=HIGHANGLE; cat=CAMERA_ANGLE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-007 (HIGH) |
| CMD-025 | `/TOPDOWN` | canon=TOPDOWN; cat=CAMERA_ANGLE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-004, SRC-005 (HIGH) |
| CMD-026 | `/BIRDSEYE` | canon=BIRDSEYE; cat=CAMERA_ANGLE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-004, SRC-005 (MEDIUM) |
| CMD-027 | `/WORMSEYE` | canon=WORMSEYE; cat=CAMERA_ANGLE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-005 (HIGH) |
| CMD-028 | `/DUTCH:L:15` | canon=DUTCH; cat=CAMERA_ANGLE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-009 (HIGH) |
| CMD-029 | `/GROUNDLEVEL` | canon=GROUNDLEVEL; cat=CAMERA_HEIGHT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002, SRC-004, SRC-005, SRC-001 (HIGH) |
| CMD-030 | `/ANKLELEVEL` | canon=ANKLELEVEL; cat=CAMERA_HEIGHT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | PROJECT_DEFINED (PROJECT_DEFINED) |
| CMD-031 | `/KNEELEVEL` | canon=KNEELEVEL; cat=CAMERA_HEIGHT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004 (LOW) |
| CMD-032 | `/HIPLEVEL` | canon=HIPLEVEL; cat=CAMERA_HEIGHT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-004, SRC-005, SRC-006 (HIGH) |
| CMD-033 | `/CHESTLEVEL` | canon=CHESTLEVEL; cat=CAMERA_HEIGHT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004, LOCAL-002 (MEDIUM) |
| CMD-034 | `/SHOULDERLEVEL` | canon=SHOULDERLEVEL; cat=CAMERA_HEIGHT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003 (MEDIUM) |
| CMD-035 | `/ELEVATED` | canon=ELEVATED; cat=CAMERA_HEIGHT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-004 (HIGH) |
| CMD-036 | `/AERIAL` | canon=AERIAL; cat=CAMERA_HEIGHT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-005 (HIGH) |
| CMD-037 | `/PAN:R` | canon=PAN; cat=CAMERA_ROTATION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-004, SRC-005, LOCAL-001 (HIGH) |
| CMD-038 | `/TILT:UP` | canon=TILT; cat=CAMERA_ROTATION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-004, SRC-005, LOCAL-001 (HIGH) |
| CMD-039 | `/ROLL:CW` | canon=ROLL; cat=CAMERA_ROTATION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-005, LOCAL-001 (HIGH) |
| CMD-040 | `/WHIPPAN:R:DOOR` | canon=WHIPPAN; cat=CAMERA_ROTATION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-004, SRC-005, SRC-009 (HIGH) |
| CMD-041 | `/DOLLYIN` | canon=DOLLYIN; cat=CAMERA_TRANSLATION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-009, LOCAL-001, LOCAL-002 (HIGH) |
| CMD-042 | `/DOLLYOUT` | canon=DOLLYOUT; cat=CAMERA_TRANSLATION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-009, LOCAL-001 (HIGH) |
| CMD-043 | `/TRUCK:L` | canon=TRUCK; cat=CAMERA_TRANSLATION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, LOCAL-001 (HIGH) |
| CMD-044 | `/PEDESTAL:UP` | canon=PEDESTAL; cat=CAMERA_TRANSLATION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-004, SRC-005, SRC-009, LOCAL-001 (HIGH) |
| CMD-045 | `/TRACK` | canon=TRACK; cat=CAMERA_TRACKING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, LOCAL-001, LOCAL-002 (HIGH) |
| CMD-046 | `/FOLLOW` | canon=FOLLOW; cat=CAMERA_TRACKING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-004, LOCAL-002 (HIGH) |
| CMD-047 | `/LEAD` | canon=LEAD; cat=CAMERA_TRACKING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-004 (MEDIUM) |
| CMD-048 | `/TRACKSIDE:R` | canon=TRACKSIDE; cat=CAMERA_TRACKING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-004, SRC-005 (HIGH) |
| CMD-049 | `/ORBIT:R:90` | canon=ORBIT; cat=CAMERA_TRACKING; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-009, LOCAL-001 (HIGH) |
| CMD-050 | `/CRANE:UP` | canon=CRANE; cat=COMPLEX_MOVEMENT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-007, SRC-009 (HIGH) |
| CMD-051 | `/FLYTHROUGH:WINDOW` | canon=FLYTHROUGH; cat=COMPLEX_MOVEMENT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-007 (HIGH) |
| CMD-052 | `/DOLLYZOOM:IN` | canon=DOLLYZOOM; cat=COMPLEX_MOVEMENT; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-004, SRC-005, SRC-009 (HIGH) |
| CMD-053 | `/DRONEVIEW` | canon=DRONEVIEW; cat=AERIAL; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-004, SRC-005 (MEDIUM) |
| CMD-054 | `/FLYOVER` | canon=FLYOVER; cat=AERIAL; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002 (MEDIUM) |
| CMD-055 | `/DRONEREVEAL:UP` | canon=DRONEREVEAL; cat=AERIAL; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-003, SRC-009 (MEDIUM) |
| CMD-056 | `/STATIC` | canon=STATIC; cat=CAMERA_RIG; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-005B, LOCAL-001, LOCAL-002 (HIGH) |
| CMD-057 | `/TRIPOD` | canon=TRIPOD; cat=CAMERA_RIG; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004, SRC-002 (MEDIUM) |
| CMD-058 | `/HANDHELD:SUBTLE` | canon=HANDHELD; cat=CAMERA_RIG; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-009, LOCAL-001 (HIGH) |
| CMD-059 | `/SHOULDER` | canon=SHOULDER; cat=CAMERA_RIG; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001 (LOW) |
| CMD-060 | `/STEADICAM` | canon=STEADICAM; cat=CAMERA_RIG; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-004 (MEDIUM) |
| CMD-061 | `/GIMBAL` | canon=GIMBAL; cat=CAMERA_RIG; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-004 (MEDIUM) |
| CMD-062 | `/SLIDER` | canon=SLIDER; cat=CAMERA_RIG; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-004 (MEDIUM) |
| CMD-063 | `/DRONE` | canon=DRONE; cat=CAMERA_RIG; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004 (HIGH) |
| CMD-064 | `/FPV` | canon=FPV; cat=CAMERA_RIG; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-007 (HIGH) |
| CMD-065 | `/LENS:35` | canon=LENS; cat=LENS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-006 (HIGH) |
| CMD-066 | `/ULTRAWIDE` | canon=ULTRAWIDE; cat=LENS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-003, SRC-004 (HIGH) |
| CMD-067 | `/WIDEANGLE` | canon=WIDEANGLE; cat=LENS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004, SRC-006 (HIGH) |
| CMD-068 | `/NORMAL` | canon=NORMAL; cat=LENS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004 (HIGH) |
| CMD-069 | `/PORTRAITLENS` | canon=PORTRAITLENS; cat=LENS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-006 (HIGH) |
| CMD-070 | `/TELEPHOTO` | canon=TELEPHOTO; cat=LENS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004 (HIGH) |
| CMD-071 | `/MACRO` | canon=MACRO; cat=LENS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004 (HIGH) |
| CMD-072 | `/FISHEYE` | canon=FISHEYE; cat=LENS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002 (HIGH) |
| CMD-073 | `/ANAMORPHIC` | canon=ANAMORPHIC; cat=LENS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-004, SRC-005 (HIGH) |
| CMD-074 | `/ZOOMIN` | canon=ZOOMIN; cat=ZOOM; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-004, SRC-005, SRC-009, LOCAL-001 (HIGH) |
| CMD-075 | `/ZOOMOUT` | canon=ZOOMOUT; cat=ZOOM; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-004, SRC-005, SRC-009, LOCAL-001 (HIGH) |
| CMD-076 | `/CRASHZOOM:IN` | canon=CRASHZOOM; cat=ZOOM; notype=HARD_CONFLICT; intent[generic_video]; intent[kling]; still[generic_image] | SRC-001, SRC-002, SRC-009 (HIGH) |
| CMD-077 | `/SHALLOW` | canon=SHALLOW; cat=FOCUS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-006 (HIGH) |
| CMD-078 | `/DEEPFOCUS` | canon=DEEPFOCUS; cat=FOCUS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004, SRC-005 (HIGH) |
| CMD-079 | `/RACKFOCUS:FG>BG` | canon=RACKFOCUS; cat=FOCUS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-007, SRC-009 (HIGH) |
| CMD-080 | `/FGFOCUS` | canon=FGFOCUS; cat=FOCUS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004, SRC-005, SRC-006, SRC-007 (MEDIUM) |
| CMD-081 | `/MGFOCUS` | canon=MGFOCUS; cat=FOCUS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004, SRC-005, SRC-006 (MEDIUM) |
| CMD-082 | `/BGFOCUS` | canon=BGFOCUS; cat=FOCUS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004, SRC-005, SRC-006 (MEDIUM) |
| CMD-083 | `/SPLITDIOPTER` | canon=SPLITDIOPTER; cat=FOCUS; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-004 (HIGH) |
| CMD-084 | `/CENTER` | canon=CENTER; cat=COMPOSITION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004 (HIGH) |
| CMD-085 | `/THIRDS:L` | canon=THIRDS; cat=COMPOSITION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004, SRC-005, SRC-006 (HIGH) |
| CMD-086 | `/SYMMETRY` | canon=SYMMETRY; cat=COMPOSITION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004 (HIGH) |
| CMD-087 | `/NEGSPACE:L` | canon=NEGSPACE; cat=COMPOSITION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-003, SRC-004 (HIGH) |
| CMD-088 | `/HEADROOM:TIGHT` | canon=HEADROOM; cat=COMPOSITION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-004, SRC-005 (HIGH) |
| CMD-089 | `/LOOKROOM:R` | canon=LOOKROOM; cat=COMPOSITION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-004 (HIGH) |
| CMD-090 | `/LEADLINES` | canon=LEADLINES; cat=COMPOSITION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004, SRC-005 (HIGH) |
| CMD-091 | `/FRAMEINFRAME` | canon=FRAMEINFRAME; cat=COMPOSITION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004 (HIGH) |
| CMD-092 | `/FGLAYER:RAILING` | canon=FGLAYER; cat=COMPOSITION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-003, SRC-004, SRC-005 (HIGH) |
| CMD-093 | `/DEEPSTAGING` | canon=DEEPSTAGING; cat=COMPOSITION; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004, SRC-005 (MEDIUM) |
| CMD-094 | `/AXIS:A-B` | canon=AXIS; cat=CONTINUITY; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002, SRC-004 (HIGH) |
| CMD-095 | `/CROSSAXIS:MOVE` | canon=CROSSAXIS; cat=CONTINUITY; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004, SRC-002 (MEDIUM) |
| CMD-096 | `/EYELINE:A>B` | canon=EYELINE; cat=CONTINUITY; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004, SRC-006, LOCAL-002 (HIGH) |
| CMD-097 | `/SCREEN:L2R` | canon=SCREEN; cat=CONTINUITY; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002, SRC-004, SRC-005B (HIGH) |
| CMD-098 | `/SRS:A>B` | canon=SRS; cat=CONTINUITY; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002, SRC-004 (HIGH) |
| CMD-099 | `/MATCHACTION` | canon=MATCHACTION; cat=CONTINUITY; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002, SRC-004 (HIGH) |
| CMD-100 | `/MATCHCUT:SHAPE` | canon=MATCHCUT; cat=CONTINUITY; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002, SRC-004, SRC-007 (HIGH) |
| CMD-101 | `/REACTION:A` | canon=REACTION; cat=CONTINUITY; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-001, SRC-002, SRC-004, SRC-005 (HIGH) |
| CMD-102 | `/INSERT:LETTER` | canon=INSERT; cat=CONTINUITY; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-002, SRC-004, SRC-005B (HIGH) |
| CMD-103 | `/CUTAWAY:CLOCK` | canon=CUTAWAY; cat=CONTINUITY; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-004, SRC-005B (HIGH) |
| CMD-104 | `/CINEMATIC` | canon=CINEMATIC; cat=STYLE; notype=HARD_CONFLICT; intent[generic_video]; intent[kling] | SRC-003, SRC-004, SRC-005, LOCAL-001 (MEDIUM) |
