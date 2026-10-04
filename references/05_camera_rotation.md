# 05 · Camera rotation

The camera stays in place and turns: pan (yaw), tilt (pitch), roll (around the lens axis), whip pan (a very fast pan). Rotation produces **no parallax** — the whole view sweeps.

## Rules
- **PAN ≠ TRUCK** (REG-03): a pan turns, a truck slides. "Pan left" is never "moves left" (SRC-004 lexicon:142; SRC-005 SKILL:112).
- **TILT ≠ PEDESTAL** (REG-04): a tilt pivots, a pedestal rises with the angle unchanged (SRC-001 ref01:92; SRC-004 lexicon:143-144).
- **Directions are camera-relative:** `/PAN:R` turns toward camera-right (research/07 D06). A pan without a direction is warned (R08).
- **Opposite directions at once are SEQUENTIAL_ONLY** (`/PAN:L /PAN:R`); one after the other is fine (`0-3s: /PAN:L 3-6s: /PAN:R`).
- **Whip pan needs a destination** (`/WHIPPAN:R:DOOR`). On H3, naming the landing point raised the speed about nine times; asking for motion blur alone did nothing (SRC-009 camera-grammar:78-84).
- **Chinese:** write 横摇 for a pan and 纵摇 for a tilt, never the bare 摇镜头, which names no axis (SRC-004 lexicon:384).
- **H3 note:** only Pan Right, Tilt Down and Roll Counterclockwise were rendered in SRC-009; the mirrors are documented but untested (direction.md).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/PAN` | The camera stays in place and rotates horizontally (yaw). No travel, so no parallax between near and far objects. **Rule:** PAN is not TRUCK: the camera body does not move sideways. | dir_lr, degrees, speed | HIGH | SRC-001, SRC-002, SRC-004, SRC-005, LOCAL-001 | /PANLEFT, /PANRIGHT, /PANL, /PANR |
| `/TILT` | The camera stays in place and rotates vertically (pitch). The body does not rise or sink. **Rule:** TILT is not PEDESTAL, and not the 'tilt' in Dutch tilt. | dir_ud, degrees, speed | HIGH | SRC-001, SRC-002, SRC-004, SRC-005, LOCAL-001 | /TILTUP, /TILTDOWN |
| `/ROLL` | The camera rotates around its lens axis during the shot (a moving roll). A static cant is DUTCH. | dir_rot, degrees, speed | HIGH | SRC-001, SRC-002, SRC-005, LOCAL-001 | /BARRELROLL, /ROLLCW, /ROLLCCW |
| `/WHIPPAN` | A very fast pan that smears the image between a starting view and a destination. /WHIPPAN:R:DOOR names where it lands. | dir_lr, label | HIGH | SRC-001, SRC-002, SRC-004, SRC-005, SRC-009 | /WHIP, /SWISHPAN, /SWISH |

| Command | Image mode | Video mode |
|---|---|---|
| `/PAN` | Cannot pan in a still. Place the subject toward the side the pan is leaving, with open space in the pan direction; no motion verbs. | The camera stays in one spot and turns left or right; the view sweeps across the scene without parallax. |
| `/TILT` | Cannot tilt in a still. Compose as a moment in the tilt: the frame favors the end the tilt travels toward; no motion verbs. | The camera stays in one spot and pivots up or down. |
| `/ROLL` | A still can only show the result: a strongly tilted horizon; state it as a position, not a motion. | The image rotates around the center as the camera rolls clockwise or counterclockwise. |
| `/WHIPPAN` | A still can show the smear: strong horizontal motion blur across the frame with the destination starting to resolve. | The camera whips sideways off the first view and lands on the destination; the move has a clear start and end point. |
<!-- END GENERATED -->
