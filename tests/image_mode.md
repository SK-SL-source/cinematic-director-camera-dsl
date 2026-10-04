# Tests · Image mode

> A still cannot pan, tilt, dolly, orbit, track or crane (spec section 21). Movements become camera
> position + perspective + framing + implied motion + a moment within the move, with no motion verbs.
> Sources: SRC-006 (one frozen instant), SRC-003 SKILL:101 (camera motion only for video or blur),
> SRC-002 img-shots:350-354, SRC-004 imgadapt:199-216; research/07 D17.

| ID | Input | Expect | Source |
|---|---|---|---|
| IMG-001 | `/ORBIT:R:45` | still[generic_image]; r[generic_image]~about 45 degrees around; r[generic_image]~camera-right; r[generic_image]!~subject's right | spec section 21; 07-D06 |
| IMG-002 | `/PAN:R` | still[generic_image]; r[generic_image]~moment within a pan to the right | SRC-002 img-shots:361 |
| IMG-003 | `/DOLLYIN:MS>CU` | still[flux]; r[flux]~close-up a push-in would reach | 07-D17 |
| IMG-004 | `/TRACKSIDE:R /FS` | still[qwen_image]; r[qwen_image]~side-on; r[qwen_image]~head to toe | 07-D17 |
| IMG-005 | `/CRANE:UP` | still[generic_image]; r[generic_image]~top of the rise | 07-D17 |
| IMG-006 | `/WHIPPAN:R:DOOR` | still[generic_image]; r[generic_image]~motion blur; r[generic_image]~door | SRC-001 ref01:74 |
| IMG-007 | `/DOLLYIN` | still[generic_image]; r[generic_image]!~motion blur | blur only when definitional (07-D17) |
| IMG-008 | `/RACKFOCUS:FG>BG` | still[generic_image]; r[generic_image]~focus is on the foreground | SRC-004 cinlang:233-235 |
| IMG-009 | `/DOLLYZOOM:IN` | still[generic_image]; r[generic_image]~stretched far away | SRC-002 img-shots:385 |
| IMG-010 | `/MS /LOWANGLE /DOLLYIN:SLOW` | still[generic_video]; r[generic_video:image]~medium shot; r[generic_video:image]!~slowly | video model asked for a still |
| IMG-011 | `/ORBIT:R:45` | r[qwen_image_edit]~Change only the camera; r[qwen_image_edit]~Keep \{SUBJECT\}; still[qwen_image_edit] | SRC-004 imgadapt:38 |
| IMG-012 | `/ORBIT:R:45` | r[qwen_image:zh]~约45度 | zh image |
| IMG-013 | `/STATIC` | still[generic_image]; r[generic_image]!~motion blur | 07-D17 |
| IMG-014 | `/FOLLOW /REAR` | still[generic_image]; r[generic_image]~following position behind | 07-D17 |
| IMG-015 | `/FLYOVER` | still[flux]; r[flux]~over the landscape | 07-D17 |
| IMG-016 | `/TILT:UP /PEDESTAL:DOWN` | still[generic_image]; intent[generic_image] | REG-04 in stills |
