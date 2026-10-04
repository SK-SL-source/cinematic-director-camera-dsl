# 07 · Tracking and complex motion

Moves defined relative to the subject (track, follow, lead, side-track, orbit) and compound moves (crane, fly-through, dolly zoom).

## Rules
- **Tracking positions are exclusive** (`track.mode`): behind (`/FOLLOW`), in front walking backward (`/LEAD`), beside (`/TRACKSIDE`). `/TRACK` is the generic form and merges with any of them (SRC-001 ref01:115-116; research/04 #15-16).
- **Side tracking and screen direction must agree:** `/TRACKSIDE:R` means the subject travels toward frame-right (`/SCREEN:L2R`); the reverse is a conflict (R05).
- **ORBIT ≠ SUBJECT ROTATION** (REG-06). The camera circles; the subject stays in place and does not turn; the background sweeps behind. "Turntable/Lazy Susan" is subject rotation and out of scope. `/ORBIT:R:90` = 90 degrees toward camera-right = counterclockwise seen from above. `/ARC` = partial orbit.
- **Crane = a large vertical arc with a reframe** (tilting to keep the subject), bigger than a pedestal (SRC-004 lexicon:146). `/JIB` and `/BOOM` are the same picture.
- **Complementary moves compose; contradictory ones fight** (SRC-009 camera-grammar:65-76). Crane rise = tracking + pedestal up + tilt down worked best on H3, so `/CRANE:UP /TILT:DOWN` is valid even though one unlicensed source calls it a conflict (research/04 phase 2).
- **Dolly zoom** = dolly and counter-zoom at matching rates; the subject keeps its size (`/DOLLYZOOM:IN` = forward + zoom out, background recedes; `:OUT` = back + zoom in, background looms). It is the least reliable measured H3 shot; open at the size it keeps (SRC-009 shots/dolly-zoom.md).
- **H3 wordings (measured):** tracking "follows … in a tracking shot, keeping … inside the frame the entire way" (LOCAL-002 H3LAB-TRACK-01); full orbit "arc shot … with large amplitude at fast speed" (SRC-009 shots/orbit-360.md).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/TRACK` | The camera moves with a moving subject, keeping it framed. Generic: the side (behind, front, beside) is not specified. | subject, screen, speed | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, LOCAL-001, LOCAL-002 | /TRACKING, /TRACKINGSHOT, /FOLLOWSHOT |
| `/FOLLOW` | The camera follows BEHIND the moving subject. | subject, speed | HIGH | SRC-001, SRC-002, SRC-004, LOCAL-002 | /FOLLOWING, /FOLLOWBEHIND, /HANDHELDFOLLOW |
| `/LEAD` | The camera moves backward in FRONT of the subject as the subject advances toward it. | subject, speed | MEDIUM | SRC-001, SRC-004 | /LEADING, /LEADINGSHOT, /BACKTRACK |
| `/TRACKSIDE` | The camera travels parallel beside the moving subject. /TRACKSIDE:R = the camera travels toward camera-right with a subject moving that way (screen L2R). | dir_lr, subject, speed | HIGH | SRC-001, SRC-002, SRC-004, SRC-005 | /SIDETRACK, /SIDETRACKING, /PARALLEL |
| `/ORBIT` | The camera travels on a circular path around the subject, keeping it framed. The subject does NOT turn; the background sweeps behind it. /ORBIT:R:90 = 90 degrees toward camera-right (counterclockwise from above). **Rule:** ORBIT is not subject rotation: the subject stays in place and the camera moves. | dir_orbit, degrees, magnitude, speed | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-009, LOCAL-001 | /ARC, /ARCSHOT, /CIRCLE, /ORBIT360 |
| `/CRANE` | A large vertical move on an arm (crane, jib, boom), usually reframing on the way (tilting to keep the subject). Larger and more arcing than a pedestal. | dir_ud, magnitude, speed | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-007, SRC-009 | /JIB, /BOOM, /CRANEUP, /CRANEDOWN, /JIBUP, /JIBDOWN, /BOOMUP, /BOOMDOWN |
| `/FLYTHROUGH` | The camera moves forward through an opening (window, doorway, gap) into a new space. /FLYTHROUGH:WINDOW names the opening. | label, speed | HIGH | SRC-001, SRC-002, SRC-007 | /FLYTHRU, /PASSTHROUGH, /THROUGH |
| `/DOLLYZOOM` | Dolly and zoom in opposite directions at matching rates so the subject keeps its size while the background changes scale. IN = camera moves forward while zooming out (background recedes); OUT = camera moves back while zooming in (background looms). | dir_io, speed | HIGH | SRC-001, SRC-002, SRC-004, SRC-005, SRC-009 | /VERTIGO, /ZOLLY, /CONTRAZOOM |

| Command | Image mode | Video mode |
|---|---|---|
| `/TRACK` | Cannot track in a still. Frame the moving subject mid-stride with the background slightly streaked in the travel direction only if the speed is FAST. | The camera travels with the subject, keeping it in frame the whole way, and comes to rest with it if it stops. |
| `/FOLLOW` | Seen from behind the moving subject, the path ahead of them visible. | The camera stays behind the subject and moves with them; the subject walks away from camera. |
| `/LEAD` | Seen from in front of the advancing subject, the subject walking toward the camera. | The camera moves backward ahead of the subject, keeping the face in frame as they walk toward it. |
| `/TRACKSIDE` | Seen side-on beside the moving subject, mid-stride; the background may streak only if the speed is FAST. | The camera travels beside the subject at the same pace; the subject stays about the same size while the background slides past behind them. |
| `/ORBIT` | Position the camera at the orbit's reached angle around the subject (e.g. about 45 degrees toward camera-right); the subject stays centered. | The camera circles the subject by the stated angle; the subject stays in place and centered while the background sweeps behind it. |
| `/CRANE` | Cannot rise in a still. Place the camera at the height the crane reaches, looking toward the subject. | The camera rises (or descends) in a long arc on an arm, tilting to keep the subject framed; the view opens out (or closes in) as it goes. |
| `/FLYTHROUGH` | Frame through the opening, its edges in the near foreground, the space beyond in view. | The camera moves forward and passes through the named opening into the space beyond. |
| `/DOLLYZOOM` | Cannot show the effect in a still. Render the end state: subject at the same size, the background unusually stretched (IN) or compressed (OUT). | The subject stays the same size and position in frame for the whole shot while the background recedes (IN) or looms closer (OUT). |
<!-- END GENERATED -->
