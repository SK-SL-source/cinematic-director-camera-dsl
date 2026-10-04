# Tests · Sequences

> SIMULTANEOUS = commands in one segment. SEQUENTIAL = time-coded segments (`0-3s:` or `[0-3s]`) or `THEN`.
> A sequence must never be reported as a conflict (spec section 20). Global commands (before the first time
> code) apply to every segment. Sources: SRC-001 SKILL:199-205, SRC-002 camera:182, SRC-004 SKILL:261-273,
> SRC-008 base-en:86-92; source disagreement on moves inside one clip: research/04 section 2.

| ID | Input | Expect | Source |
|---|---|---|---|
| SEQ-001 | `0-3s: /PAN:R 3-7s: /DOLLYIN:SLOW` | seq; notype=HARD_CONFLICT; move.0.canonical=PAN; move.1.canonical=DOLLYIN; move.1.time.0=3.0 | spec section 20 |
| SEQ-002 | `0-3s: /DOLLYIN 4-7s: /DOLLYOUT` | seq; notype=SEQUENTIAL_ONLY | spec section 19 |
| SEQ-003 | `/DOLLYIN THEN /DOLLYOUT` | seq; notype=SEQUENTIAL_ONLY; move.0.canonical=DOLLYIN; move.1.canonical=DOLLYOUT | 07-D10 |
| SEQ-004 | `/MS 0-2s: /STATIC 2-5s: /DOLLYIN:MS>MCU` | seq; notype=HARD_CONFLICT; state.shot.size=MS | SRC-004 failmodes:314 (hold then move) |
| SEQ-005 | `/STATIC 2-5s: /DOLLYIN` | rule=G01-STATIC-MOVE; status=ERROR | global state applies to all segments |
| SEQ-006 | `0-3s: /LOWANGLE 3-6s: /HIGHANGLE` | rule=R09-STATE-JUMP; type=CONTEXT_DEPENDENT | SRC-002 camera:283-287 |
| SEQ-007 | `0-3s: /LOWANGLE 3-6s: /HIGHANGLE /CRANE:UP` | norule=R09-STATE-JUMP | crane explains the change |
| SEQ-008 | `0-3s: /WS 3-6s: /CU` | rule=R09-STATE-JUMP | SRC-009 framing.md |
| SEQ-009 | `0-3s: /WS 3-6s: /CU /DOLLYIN` | norule=R09-STATE-JUMP | push explains the change |
| SEQ-010 | `0-4s: /PAN:R 2-6s: /PAN:L` | type=SEQUENTIAL_ONLY; status=ERROR | overlapping windows are simultaneous |
| SEQ-011 | `0-3s: /PAN:R 3-6s: /TILT:UP` | rule=R10-SEQUENCE-IN-ONE-CLIP; status=WARN | SRC-002 camera:182 vs SRC-004 failmodes:314 |
| SEQ-012 | `[0-3s] /DOLLYIN [3-6s] /ORBIT:R:90` | seq; move.1.canonical=ORBIT | bracket notation (SRC-002 vocab:76-79) |
| SEQ-013 | `0-2s: /CRASHZOOM:IN 2-5s: /STATIC` | seq; notype=HARD_CONFLICT | SRC-009 shots/crash-zoom-in.md |
| SEQ-014 | `/HANDHELD 0-3s: /FOLLOW 3-6s: /STATIC` | type=HARD_CONFLICT; status=ERROR | global handheld vs locked |
| SEQ-015 | `0-3s: /DOLLYIN:MS>MCU 3-6s: /DOLLYIN:MCU>CU` | seq; notype=HARD_CONFLICT | consistent ranges |
| SEQ-016 | `0-3s: /DOLLYIN:MS>MCU 3-6s: /DOLLYOUT:MCU>MS` | seq; notype=HARD_CONFLICT | spec section 19 |
| SEQ-017 | `0-3s: /ZOOMIN 3-6s: /ZOOMOUT` | seq; notype=SEQUENTIAL_ONLY | channels in time |
| SEQ-018 | `0-5s: /ORBIT:R:90 5-8s: /ORBIT:L:90` | seq; notype=SEQUENTIAL_ONLY | channels in time |
| SEQ-019 | `3-6s: /PAN:R 0-3s: /TILT:UP` | rule=S01-TIME-ORDER; status=ERROR | time codes increase |
| SEQ-020 | `0-3s: /TILT:UP 3-6s: /PEDESTAL:UP` | seq; move.0.canonical=TILT; move.1.canonical=PEDESTAL | REG-04 in time |
| SEQ-021 | `/MS 0-3s: /STATIC 3-8s: /DOLLYIN:MS>CU:SLOW` | r[minimax_h3]~For the first 3 seconds, the camera holds a Static Shot; r[minimax_h3]~At about the 3-second mark; warn[minimax_h3]~cannot place events | SRC-009 performance (timing); LOCAL-002 H3LAB-TIME-01 time phrasing (07-D41) |
| SEQ-022 | `0-3s: /PAN:R 3-7s: /DOLLYIN:SLOW` | r[generic_video]~From 0s to 3s; r[generic_video]~From 3s to 7s | SRC-001 SKILL:199-205 |
| SEQ-023 | `/DOLLYIN /ZOOMOUT THEN /STATIC` | has=DOLLYZOOM; notype=HARD_CONFLICT | special technique inside a segment |
| SEQ-024 | `0-3s: /PAN:R 3-7s: /DOLLYIN:SLOW` | r[kling]~横摇; r[kling]~推镜 | Kling zh sequence |
| SEQ-025 | `/MS /PAN:R THEN /DOLLYIN` | seq; move.0.step=1; move.1.step=2; r[generic_video]~First, the camera; r[generic_video]~Then, ; r[minimax_h3]~Then, ; r[kling]~然后; r[kling:en]~then | a THEN sequence reads as an order, not as simultaneous moves (spec section 20; 07-D40) |
| SEQ-026 | `/MS 0-2s: /STATIC 2-5s: /DOLLYIN` | status=OK; move.0.type=hold; state.rig.locked=False; r[generic_video]~From 0s to 2s: The camera holds still; r[generic_video]!~for the whole shot; r[kling]~镜头保持不动 | a hold phase, not a lock for the whole shot (07-D40) |
| SEQ-027 | `/MS 0-2s: /PAN:R /TILT:UP 2-5s: /DOLLYIN` | seq; r[generic_video]~At the same time, the camera; r[kling]~同时 | two moves in one step stay simultaneous (07-D40) |
| SEQ-028 | `/MS /STATIC THEN /DOLLYIN` | move.0.type=hold; move.1.canonical=DOLLYIN; state.rig.stability=None; notype=HARD_CONFLICT | 07-D40 |
| SEQ-029 | `/WS 0-2s: /PAN:R 2-5s: /DOLLYIN:WS>MS` | r[kling]~第0至2秒; r[kling]~第2至5秒; r[kling:en]~from 0s to 2s; r[minimax_h3]~For the first 2 seconds; r[minimax_h3]~At about the 2-second mark | every adapter keeps the time order (07-D40, 07-D41) |
| SEQ-030 | `/MS /STATIC 2-5s: /DOLLYIN` | rule=G01-STATIC-MOVE | a /STATIC for the whole shot still conflicts with a later move |
| SEQ-031 | `/MS 0-3s: /PAN:R 3-7s: /DOLLYIN:SLOW` | r[minimax_h3]~For the first 3 seconds, the camera pans right\. The camera stays in place; r[minimax_h3]~At about the 3-second mark, the camera pushes in at slow speed toward \{SUBJECT\}\. The push continues steadily for the rest of the video; r[minimax_h3]!~over the whole video; r[minimax_h3]!~starts on; r[generic_video]!~From 3s to 7s: From this opening framing | a later step starts where the previous one ended (07-D41); the official speed token is kept |
| SEQ-032 | `/MS /PAN:R THEN /DOLLYIN:MS>MCU` | r[minimax_h3]~Then, the camera pushes in toward \{SUBJECT\}\. The push continues steadily for the rest of the video\. The final frame is a medium close-up; r[minimax_h3]!~over the whole video | 07-D41 |
