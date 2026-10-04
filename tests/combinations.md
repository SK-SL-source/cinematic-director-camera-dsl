# Tests · Valid combinations

> Generated from `registry/compatibility_matrix.yaml` (every row has a documented case or a definitional reason).
> A valid combination must never be reported as HARD_CONFLICT or SEQUENTIAL_ONLY (spec section 18, CONFLICT AUDIT),
> and its rendering must keep every command's intent.

| ID | Input | Expect | Source |
|---|---|---|---|
| COMBO-001 | `/DOLLYIN /DUTCH` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C01: SRC-002 camera:175 |
| COMBO-002 | `/CRANE:UP /ORBIT` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C02: SRC-002 camera:176 |
| COMBO-003 | `/FPV /CRASHZOOM` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C03: SRC-002 camera:177 |
| COMBO-004 | `/HANDHELD /FOLLOW` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C04: SRC-002 camera:178; SRC-009 shots/handheld.md |
| COMBO-005 | `/ORBIT /RACKFOCUS:FG>BG` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C05: SRC-007 01 prompt:22 |
| COMBO-006 | `/DOLLYOUT /PAN:L` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C06: SRC-007 01 prompt:24 |
| COMBO-007 | `/CRANE:UP /DOLLYOUT` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C07: SRC-007 01 prompt:28 |
| COMBO-008 | `/CRANE:UP /TILT:DOWN` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C08: SRC-009 shots/crane-rise.md; SRC-005 SKILL:104 |
| COMBO-009 | `/TRACK /PEDESTAL:UP /TILT:DOWN` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; intent[generic_video] | C09: SRC-009 camera-grammar:71 |
| COMBO-010 | `/DOLLYOUT /PEDESTAL:UP` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C10: SRC-009 shots/aerial-pullback.md |
| COMBO-011 | `/HANDHELD:STRONG /TRACK` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C11: SRC-009 shots/handheld.md |
| COMBO-012 | `/DOLLYIN /RACKFOCUS` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C12: SRC-011 movement-catalog.md:436 |
| COMBO-013 | `/ORBIT /TILT:UP` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C13: SRC-011 movement-catalog.md:437 |
| COMBO-014 | `/CRANE:UP /PAN:R` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C14: SRC-011 movement-catalog.md:438; SRC-005 SKILL:104 |
| COMBO-015 | `/DOLLYIN /TILT:UP` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C15: spec section 20 |
| COMBO-016 | `/PAN:R /TRUCK:R` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C16: spec section 18; SRC-005 SKILL:112 |
| COMBO-017 | `/TILT:UP /PEDESTAL:DOWN` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C17: SRC-004 lexicon:143-144; PRJ |
| COMBO-018 | `/DOLLYIN /LOWANGLE` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C18: SRC-001 ref01:114 |
| COMBO-019 | `/TRACKSIDE:R /GIMBAL /FS /GROUNDLEVEL` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C19: spec section 23 |
| COMBO-020 | `/FOLLOW /DOLLYIN` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C20: PRJ |
| COMBO-021 | `/LEAD /STEADICAM` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C21: SRC-004 cinlang:385 |
| COMBO-022 | `/FPV /FLYTHROUGH` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C22: SRC-001 ref01:123 |
| COMBO-023 | `/DRONEVIEW /FLYOVER` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C23: SRC-001 SKILL:77 |
| COMBO-024 | `/DUTCH /HANDHELD` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C24: SRC-001 SKILL:175 |
| COMBO-025 | `/LOWANGLE /WIDEANGLE` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C25: SRC-006 SKILL:94; SRC-004 cinlang:174 |
| COMBO-026 | `/CU /SHALLOW /PORTRAITLENS` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C26: SRC-002 camera:244; SRC-004 cinlang:134 |
| COMBO-027 | `/EWS /HIGHANGLE` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C27: SRC-001 SKILL:189 |
| COMBO-028 | `/WORMSEYE /EWS` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C28: SRC-001 SKILL:193 |
| COMBO-029 | `/TOPDOWN /ROLL:CW` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C29: SRC-001 ref01:127 |
| COMBO-030 | `/FOLLOW /REAR` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C30: SRC-001 ref01:115 |
| COMBO-031 | `/TRACKSIDE:R /PROFILE` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C31: SRC-004 cinlang:386 |
| COMBO-032 | `/STATIC /TRIPOD` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C32: SRC-004 lexicon:148 |
| COMBO-033 | `/GROUNDLEVEL /LOWANGLE` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C33: SRC-001 ref01:26-28 |
| COMBO-034 | `/GROUNDLEVEL /WORMSEYE` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C34: SRC-002 img-shots:261 |
| COMBO-035 | `/BIRDSEYE /DRONE` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C35: SRC-001 ref01:144 |
| COMBO-036 | `/DRONEVIEW /TOPDOWN` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C36: PRJ (research 07 D05) |
| COMBO-037 | `/MACRO /ECU /SHALLOW` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C37: SRC-002 camera:248; SRC-004 cinlang:135 |
| COMBO-038 | `/INSERT /POV` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C38: PRJ |
| COMBO-039 | `/DEEPSTAGING /DEEPFOCUS` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C39: SRC-004 cinlang:180-183 |
| COMBO-040 | `/FGLAYER /BGFOCUS` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C40: SRC-003 shotlang:40; SRC-007 01 prompt:19 |
| COMBO-041 | `/TRUCK:L /FGLAYER` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C41: SRC-004 lexicon:141; SRC-001 ref01:134 |
| COMBO-042 | `/SLIDER /TRUCK:R` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C42: SRC-001 ref01:134 |
| COMBO-043 | `/ORBIT /LOWANGLE` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C43: SRC-001 SKILL:190 |
| COMBO-044 | `/PAN:R /TRIPOD` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C44: SRC-004 lexicon:142 |
| COMBO-045 | `/WHIPPAN:R /HANDHELD` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C45: SRC-001 SKILL:182 |
| COMBO-046 | `/OTS /SHALLOW` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C46: SRC-004 cinlang:67 |
| COMBO-047 | `/EYELEVEL /DUTCH` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C47: SRC-005 SKILL:95; PRJ |
| COMBO-048 | `/ZOOMIN /PAN:L` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C48: PRJ |
| COMBO-049 | `/POV /HANDHELD` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C49: SRC-002 camera:86 |
| COMBO-050 | `/STATIC /DRONE` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C50: SRC-002 cinema:444 |
| COMBO-051 | `/FPV /POV` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C51: PRJ (research 04 section 2 FPV vs POV) |
| COMBO-052 | `/SCREEN:L2R /TRACKSIDE:R` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C52: SRC-004 cinlang:328-338 |
| COMBO-053 | `/BIRDSEYE /TOPDOWN` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C53: SRC-005 SKILL:121 |
| COMBO-054 | `/TRACK /FOLLOW` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C54: SRC-001 ref01:115 |
| COMBO-055 | `/HANDHELD /SHOULDER` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C55: SRC-001 ref01:71 |
| COMBO-056 | `/DRONE /FPV` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C56: SRC-001 SKILL:77 |
| COMBO-057 | `/MS /LOWANGLE /DOLLYIN:SLOW /LENS:50` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C57: spec section 24 |
| COMBO-058 | `/DRONE /GIMBAL` | notype=HARD_CONFLICT; notype=SEQUENTIAL_ONLY; notype=SOFT_CONFLICT; intent[generic_video] | C58: PRJ |
