# 03 · Camera angle

Which way the lens axis points relative to the subject (`camera.pitch`: straight up, low, level, high, straight down) plus a static roll offset (`camera.roll_offset`: Dutch).

## Rules
- **Angle is not height** (SRC-004 cinlang:70-100; SRC-005 SKILL:117-125). A ground-level camera can look level; an elevated camera can look level. Set height in 04_camera_height.md.
- **HIGH ANGLE is oblique; TOPDOWN is 90 degrees** (REG-09). They conflict.
- **TOPDOWN implies no height** (a table flat-lay is top-down). **BIRDSEYE = top-down from far above**, the ground like a map; it refines TOPDOWN. **DRONEVIEW is oblique** by default (14_aerial_drone.md). DRONE VIEW ≠ BIRD'S-EYE ≠ TOP DOWN (REG-10).
- **EYELEVEL sets two things:** eye height and a level axis. `/EYELEVEL /HIPLEVEL` is therefore a conflict (research/04 section 2).
- **DUTCH is a roll offset, not a TILT** (`/DUTCHTILT` → `/DUTCH`). A rolling Dutch is `/DUTCH` + `/ROLL` (context-dependent).
- **WORMSEYE** = straight up, normally from the ground (default height). From higher up it is context-dependent (P17).
- **AI note:** state the visible consequence, not degrees ("the ceiling is visible behind her"); models honour described geometry better than numbers (SRC-004 cinlang:97-100). On H3, SRC-009 got a held cant by describing a counterclockwise roll that stops at a tilted horizon and stays there (shots/dutch-angle.md).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/EYELEVEL` | The camera sits at the subject's eye height with a level lens axis: the neutral angle. Sets both height (EYE) and pitch (LEVEL). | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-006 | /EYE, /LEVEL, /NEUTRALANGLE |
| `/LOWANGLE` | The camera looks UP at the subject (lens axis tilted upward). An angle, independent of camera height. | angle_intensity | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-006, SRC-007 | /LOW, /HEROANGLE, /UPSHOT |
| `/HIGHANGLE` | The camera looks DOWN at the subject at an oblique angle. Not straight down (that is TOPDOWN). **Rule:** HIGHANGLE is oblique; it never becomes a 90-degree top-down view. | angle_intensity | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-007 | /HIGH, /DOWNSHOT |
| `/TOPDOWN` | The lens axis points straight down (about 90 degrees). Height is not implied: a table flat-lay is top-down. | - | HIGH | SRC-001, SRC-002, SRC-004, SRC-005 | /OVERHEAD, /TOPSHOT, /FLATLAY, /GODSEYE |
| `/BIRDSEYE` | Looking straight down from very high above, so the ground reads like a map and people look small. Top-down angle PLUS great height. **Rule:** BIRDSEYE is not DRONEVIEW (oblique aerial) and not plain TOPDOWN (no height implied). | - | MEDIUM | SRC-001, SRC-002, SRC-004, SRC-005 | /BIRDSEYEVIEW, /BIRDS |
| `/WORMSEYE` | Looking (nearly) straight up at the subject; usually from the ground. | - | HIGH | SRC-001, SRC-002, SRC-005 | /WORMSVIEW, /WORMSEYEVIEW, /WORMS |
| `/DUTCH` | The camera is rolled so the horizon is tilted (a static cant). /DUTCH:L\|R names which way the frame leans; degrees optional. **Rule:** DUTCH is a roll offset, not a TILT. | dir_lr, degrees | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-009 | /DUTCHTILT, /DUTCHANGLE, /CANTED, /CANTEDANGLE, /OBLIQUE |

| Command | Image mode | Video mode |
|---|---|---|
| `/EYELEVEL` | Camera at the subject's eye height, looking straight across. | Camera at the subject's eye height, looking straight across. |
| `/LOWANGLE` | Camera below the subject looking up; the subject towers. | Camera below the subject looking up. |
| `/HIGHANGLE` | Camera above the subject looking down at an angle (not straight down). | Camera above the subject looking down at an angle (not straight down). |
| `/TOPDOWN` | Looking straight down at the subject. | Looking straight down at the subject. |
| `/BIRDSEYE` | From far above, straight down; the ground looks like a map. | From far above, straight down; the ground looks like a map. |
| `/WORMSEYE` | From the ground looking straight up; the subject towers against the sky or ceiling. | From the ground looking straight up. |
| `/DUTCH` | The horizon is tilted; verticals lean. | The horizon stays tilted for the whole shot. |
<!-- END GENERATED -->
