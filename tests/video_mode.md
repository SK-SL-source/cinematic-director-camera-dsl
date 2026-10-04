# Tests · Video mode

> A video movement must state START, PATH, DIRECTION, SPEED, SUBJECT RELATION, PARALLAX, END (spec section 22;
> SRC-012 SKILL:122; SRC-010 SKILL:33-35) — but in STRICT mode only what was given or is definitional
> (research/07 D16). No "cinematic tracking shot" vagueness.

| ID | Input | Expect | Source |
|---|---|---|---|
| VID-001 | `/MS /DOLLYIN:MS>MCU:SLOW` | r[generic_video]~opening framing; r[generic_video]~moves forward; r[generic_video]~slowly; r[generic_video]~grows larger; r[generic_video]~near objects grow faster; r[generic_video]~ends on a medium close-up | spec section 22 (all seven) |
| VID-002 | `/TRUCK:R:SLOW` | r[generic_video]~slides right; r[generic_video]~foreground passes faster; r[generic_video]~does not turn; r[generic_video]~slowly | SRC-004 lexicon:141 |
| VID-003 | `/PAN:L` | r[generic_video]~pans left; r[generic_video]~no parallax; r[generic_video]!~slides | SRC-004 lexicon:142 |
| VID-004 | `/ORBIT:R:90` | r[generic_video]~about 90 degrees; r[generic_video]~counterclockwise; r[generic_video]~does not turn; r[generic_video]~background sweeps | SRC-004 lexicon:145 |
| VID-005 | `/TRACKSIDE:R` | r[generic_video]~beside; r[generic_video]~background slides past; r[generic_video]~toward frame-right | SRC-001 ref01:87 |
| VID-006 | `/ZOOMIN:MS>CU` | r[generic_video]~zooms in; r[generic_video]~does not move; r[generic_video]!~moves forward | SRC-004 lexicon:140 |
| VID-007 | `/STATIC` | r[generic_video]~stays locked in one position; r[generic_video]!~pans | SRC-004 vidadapt:231 |
| VID-008 | `/DOLLYIN` | unspec=DOLLYIN.speed; unspec=DOLLYIN.end_position; r[generic_video]!~slowly; r[generic_video]!~ends on | STRICT (07-D16) |
| VID-009 | `/CRANE:UP /TILT:DOWN` | r[generic_video]~rises; r[generic_video]~tilts down | SRC-009 shots/crane-rise.md |
| VID-010 | `/DOLLYZOOM:IN` | r[generic_video]~same size; r[generic_video]~zooms out; r[generic_video]~moves forward | SRC-004 lexicon:150 |
| VID-011 | `/FOLLOW /HANDHELD` | r[generic_video]~follows behind; r[generic_video]~handheld | SRC-002 camera:178 |
| VID-012 | `/DOLLYOUT:CU>WS` | r[generic_video]~ends on a wide shot; r[generic_video]~more of the surroundings | SRC-004 lexicon:139 |
| VID-013 | `/PEDESTAL:UP` | r[generic_video]~rises straight up; r[generic_video]!~tilts | SRC-004 lexicon:144 |
| VID-014 | `/WHIPPAN:R` | warn[generic_video]~destination | SRC-009 camera-grammar:78-82 |
| VID-015 | `/LEAD /STEADICAM` | r[generic_video]~backward ahead; r[generic_video]~face stays in the frame | SRC-001 ref01:116 |
| VID-016 | `/DRONEREVEAL:BACK` | r[generic_video]~rises and pulls back; r[generic_video]~small far below | SRC-009 shots/aerial-pullback.md |
