# Tests · Aliases

> Every alias must resolve to exactly one canonical command (or be declared out of scope), with the
> relationship recorded in `registry/aliases.yaml`. Sources: research/04 (terminology conflicts) and
> research/07 D11, D26.

## Legacy 20 (spec section 15)

| ID | Input | Expect | Source |
|---|---|---|---|
| ALIAS-001 | `/DRONEVIEW` | canon=DRONEVIEW; cat=AERIAL; rel=canonical; state.camera.height=AERIAL | 07-D26; 04 #10 |
| ALIAS-002 | `/TOPDOWN` | canon=TOPDOWN; cat=CAMERA_ANGLE; state.camera.angle=VERTICAL_DOWN | 07-D26; 04 #8 |
| ALIAS-003 | `/BIRDSEYE` | canon=BIRDSEYE; cat=CAMERA_ANGLE; state.camera.height=AERIAL | 07-D26; 04 #9 |
| ALIAS-004 | `/OVERHEAD` | canon=TOPDOWN; rel=legacy | 04 #7 |
| ALIAS-005 | `/LOWANGLE` | canon=LOWANGLE; rel=canonical | 07-D26 |
| ALIAS-006 | `/HIGHANGLE` | canon=HIGHANGLE; rel=canonical | 07-D26 |
| ALIAS-007 | `/GROUNDLEVEL` | canon=GROUNDLEVEL; cat=CAMERA_HEIGHT | 04 section 2 |
| ALIAS-008 | `/EYELEVEL` | canon=EYELEVEL; state.camera.height=EYE; state.camera.angle=LEVEL | 04 section 2 EYE LEVEL |
| ALIAS-009 | `/WORMSVIEW` | canon=WORMSEYE; rel=legacy | 07-D26 |
| ALIAS-010 | `/WIDEANGLE` | canon=WIDEANGLE; cat=LENS; hasnot=WS | 04 #1 |
| ALIAS-011 | `/CLOSEUP` | canon=CU; rel=legacy | 07-D26 |
| ALIAS-012 | `/MEDIUMSHOT` | canon=MS; rel=legacy | 07-D26 |
| ALIAS-013 | `/FULLBODY` | canon=FS; rel=legacy | 07-D26 |
| ALIAS-014 | `/TRACKING` | canon=TRACK; rel=legacy | 04 #16 |
| ALIAS-015 | `/ORBIT` | canon=ORBIT; rel=canonical; rule=R08-UNSPECIFIED-DIRECTION | 07-D26 |
| ALIAS-016 | `/PUSHIN` | canon=DOLLYIN; rel=legacy; r[generic_video]!~zoom | 04 #11 |
| ALIAS-017 | `/PULLOUT` | canon=DOLLYOUT; rel=legacy; r[generic_video]!~zoom | 04 #13 |
| ALIAS-018 | `/DUTCHTILT` | canon=DUTCH; cat=CAMERA_ANGLE; hasnot=TILT | 04 #20 |
| ALIAS-019 | `/CINEMATIC` | canon=CINEMATIC; cat=STYLE; strict[generic_video]; strict[minimax_h3] | 04 section 1 O; 07-D26 |
| ALIAS-020 | `/PORTRAIT` | canon=PORTRAITLENS; rel=legacy_ambiguous; rule=A03-AMBIGUOUS-LEGACY; hasnot=SHALLOW; hasnot=CU; strict[generic_video] | 04 #5 |

## Parameter and argument-dependent aliases

| ID | Input | Expect | Source |
|---|---|---|---|
| ALIAS-021 | `/PANLEFT` | canon=PAN; rel=parameter_alias; arg.dir_lr=L | 07-D11 |
| ALIAS-022 | `/TILTUP:SLOW` | canon=TILT; arg.dir_ud=UP; state.movement.0.speed=SLOW | 07-D11 |
| ALIAS-023 | `/DOLLY:L` | canon=TRUCK; arg.dir_lr=L; rule=A02-ALIAS-NOTE | 04 #17 (SRC-002 camera:39-40) |
| ALIAS-024 | `/DOLLY:IN:SLOW` | canon=DOLLYIN; arg.speed=SLOW | 07-D11 |
| ALIAS-025 | `/DOLLY` | status=ERROR; rule=A01-ALIAS-NEEDS-ARG | 07-D11 |
| ALIAS-026 | `/ZOOM:OUT` | canon=ZOOMOUT | 07-D11 |
| ALIAS-027 | `/JIBUP` | canon=CRANE; rel=rig_variant_alias; arg.dir_ud=UP | 04 #23 |
| ALIAS-028 | `/ARC:R` | canon=ORBIT; arg.magnitude=PARTIAL; arg.dir_orbit=R | 04 #25 |
| ALIAS-029 | `/ORBIT360` | canon=ORBIT; arg.magnitude=FULL | 04 #25 |
| ALIAS-030 | `/LOOKCAM:A` | canon=EYELINE; arg.relation=A>CAM; hasnot=POV | 04 #6 (REG-02) |
| ALIAS-031 | `/HANDHELDFOLLOW` | canon=HANDHELD,FOLLOW; rel=composite | aliases.yaml composite |
| ALIAS-032 | `/SHAKYCAM` | canon=HANDHELD; arg.intensity=STRONG | SRC-001 SKILL:75 |
| ALIAS-033 | `/PULLFOCUS:A>B` | canon=RACKFOCUS; arg.speed=SLOW; arg.relation=A>B | SRC-005 SKILL:131-132 |
| ALIAS-034 | `/LENS85` | canon=LENS; rel=compact_grammar; arg.mm=85.0 | spec section 24 |
| ALIAS-035 | `/35MM` | canon=LENS; arg.mm=35.0 | 07-D10 |
| ALIAS-036 | `/SUPERDOLLY` | canon=DOLLYIN; arg.magnitude=LARGE; arg.speed=FAST | SRC-009 shots/super-dolly-in.md |
| ALIAS-037 | `/SLIDE:R` | canon=TRUCK; arg.dir_lr=R | 04 #18 |
| ALIAS-038 | `/OBLIQUE` | canon=DUTCH; arg.dir_lr=L; arg.degrees=8.0 | SRC-001 ref01:38 |
| ALIAS-039 | `/180:A-B` | canon=AXIS; arg.axis=A-B | 07-D10 |
| ALIAS-040 | `/pushin` | canon=DOLLYIN | case-insensitive (07-D10) |
| ALIAS-041 | `/AERIALPULLBACK` | canon=DRONEREVEAL; arg.dir_reveal=BACK | SRC-009 shots/aerial-pullback.md |
| ALIAS-042 | `/GRAPHICMATCH` | canon=MATCHCUT; arg.kind=SHAPE | SRC-002 vocab:67 |

## Ambiguous, out-of-scope and unknown words

| ID | Input | Expect | Source |
|---|---|---|---|
| ALIAS-043 | `/WIDE` | canon=WS; rel=legacy_ambiguous; rule=A03-AMBIGUOUS-LEGACY | 04 #1-2 |
| ALIAS-044 | `/LS` | canon=WS; rule=A03-AMBIGUOUS-LEGACY | 04 #3 |
| ALIAS-045 | `/MLS` | canon=MFS; rule=A03-AMBIGUOUS-LEGACY | 04 section 2 MLS |
| ALIAS-046 | `/DRONESHOT` | canon=DRONEVIEW; rule=A03-AMBIGUOUS-LEGACY | 04 #10 |
| ALIAS-047 | `/BOKEH` | canon=SHALLOW; rule=A02-ALIAS-NOTE; r[generic_video]!~bokeh | SRC-004 cinlang:222-235 |
| ALIAS-048 | `/TURNTABLE` | canon=; type=OUT_OF_SCOPE; status=WARN | 04 #24 (REG-06) |
| ALIAS-049 | `/SPIELBERG` | canon=; type=OUT_OF_SCOPE | spec section 1-G |
| ALIAS-050 | `/BULLETTIME` | canon=; type=OUT_OF_SCOPE | SRC-009 shots/bullet-time.md |
| ALIAS-051 | `/DOLLYINN` | status=ERROR; rule=A05-UNKNOWN-COMMAND | 07-D10 |
| ALIAS-052 | `/PAN:SIDEWAYS` | status=ERROR; rule=A06-BAD-ARGUMENT | 07-D10 |
| ALIAS-053 | `/ONESHOT` | canon=; type=OUT_OF_SCOPE | aliases.yaml out_of_scope |
