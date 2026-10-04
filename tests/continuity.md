# Tests · Continuity

> Multi-shot lists (`S1: ...` lines, or `CUT`). Checks from research/07 D37 and SRC-004 continuity geometry
> (cinlang:239-376): axis of action, eyeline, screen direction, 30-degree / two-step rule, POV needs a look,
> CONTINUOUS start = previous end, shot/reverse-shot keeps size.

| ID | Input | Expect | Source |
|---|---|---|---|
| CONT-001 | `S1: /WS /TWOSHOT /AXIS:A-B\nS2: /OTS:A>B /MCU /EYELINE:B>OFFL\nS3: /OTS:B>A /MCU /EYELINE:A>OFFR` | shots=3; norule=C02-EYELINE-MISMATCH; norule=C01-AXIS-CROSSED; norule=C05-JUMP-CUT-RISK | SRC-004 cinlang:340-361 |
| CONT-002 | `S1: /WS /TWOSHOT /AXIS:A-B\nS2: /OTS:A>B /MCU /EYELINE:B>OFFL\nS3: /OTS:B>A /MCU /EYELINE:A>OFFL` | rule=C02-EYELINE-MISMATCH; status=ERROR | SRC-004 cinlang:343-346 |
| CONT-003 | `S1: /WS /AXIS:A-B\nS2: /MS /AXIS:B-A` | rule=C01-AXIS-CROSSED; status=ERROR | SRC-004 cinlang:245-290 |
| CONT-004 | `S1: /WS /AXIS:A-B\nS2: /MS /AXIS:B-A /CROSSAXIS:MOVE /ORBIT:R:180` | norule=C01-AXIS-CROSSED; norule=C09-CROSS-NEEDS-MOVE | SRC-004 cinlang:292-303 |
| CONT-005 | `S1: /WS /SCREEN:L2R\nS2: /MS /SCREEN:R2L` | rule=C04-SCREEN-DIRECTION-REVERSED | SRC-004 cinlang:328-338 |
| CONT-006 | `S1: /WS /SCREEN:L2R\nS2: /MS /SCREEN:L2R` | norule=C04-SCREEN-DIRECTION-REVERSED | SRC-004 cinlang:328-338 |
| CONT-007 | `S1: /MS /EYELEVEL\nS2: /MCU /EYELEVEL` | rule=C05-JUMP-CUT-RISK; status=WARN | SRC-004 cinlang:36-42, 315-326 |
| CONT-008 | `S1: /MS\nS2: /CU` | norule=C05-JUMP-CUT-RISK | two size steps |
| CONT-009 | `S1: /MS /EYELEVEL\nS2: /MCU /LOWANGLE` | norule=C05-JUMP-CUT-RISK | angle changed |
| CONT-010 | `S1: /WS\nS2: /POV:A /MS` | rule=C06-POV-WITHOUT-LOOK | SRC-004 cinlang:30 |
| CONT-011 | `S1: /MCU /EYELINE:A>OFFR\nS2: /POV:A /MS` | norule=C06-POV-WITHOUT-LOOK | SRC-004 cinlang:30 |
| CONT-012 | `S1: /MS /DOLLYIN:MS>MCU\nS2: CONTINUOUS /MS` | rule=C07-CONTINUOUS-MISMATCH; status=ERROR | DIR-08; SRC-010 SKILL:63-65 |
| CONT-013 | `S1: /MS /DOLLYIN:MS>MCU\nS2: CONTINUOUS /MCU` | norule=C07-CONTINUOUS-MISMATCH | DIR-08; SRC-010 |
| CONT-014 | `S1: /OTS:A>B /MCU\nS2: /SRS:B>A /CU` | rule=C08-SRS-SIZE | SRC-004 cinlang:351-355 |
| CONT-015 | `S1: /MATCHACTION /MS\nS2: /CU` | rule=C10-NO-PREVIOUS-SHOT | SRC-004 editing:69 |
| CONT-016 | `S1: /WS /AXIS:A-B\nS2: /MS /CROSSAXIS:MOVE` | rule=C09-CROSS-NEEDS-MOVE | SRC-004 cinlang:295 |
| CONT-017 | `/WS /TWOSHOT CUT /CU` | shots=2 | 07-D10 (CUT separator) |
| CONT-018 | `S1: /MCU /EYELINE:A>B\nS2: /MCU /EYELINE:B>A` | norule=C05-JUMP-CUT-RISK; status=OK | eyeline pair (A>B / B>A) |
| CONT-019 | `S1: /MS /AXIS:A-B\nS2: /MS /AXIS:B-A /CROSSAXIS:MOVE /ORBIT:R` | norule=C05-JUMP-CUT-RISK; norule=C01-AXIS-CROSSED; status=OK; r[generic_video]~By the end of the shot; r[generic_video]!~\{B\} stays on the left; r[kling]~镜头结束时 | a declared crossing moves the camera to the other side: not a jump cut (SRC-004 cinlang:295) |
| CONT-020 | `S1: /MS /AXIS:A-B\nS2: /MS /AXIS:A-B` | rule=C05-JUMP-CUT-RISK | same size, same side, same angle (SRC-004 cinlang:36) |
| CONT-021 | `S1: /MS /AXIS:A-B\nS2: /MS /AXIS:B-A /CROSSAXIS:MOVE /DOLLYIN` | rule=C09-CROSS-NEEDS-MOVE | a push along the lens axis does not carry the audience over the line (SRC-004 cinlang:295-296) |
| CONT-022 | `S1: /MS /AXIS:A-B\nS2: /MS /AXIS:B-A /CROSSAXIS:CUTAWAY` | r[generic_video]~stays on the left; r[generic_video]~via a cutaway | an edit-based crossing holds the new sides for the whole shot |
