# 14 · Aerial and drone

Camera positions and moves that need the camera in the air. Related commands live elsewhere: `/AERIAL` (height, 04), `/DRONE` and `/FPV` (rigs, 08), `/BIRDSEYE` and `/TOPDOWN` (angles, 03).

## Rules
- **DRONE VIEW ≠ BIRD'S-EYE ≠ TOP DOWN** (REG-10; research/04 #8-10):
  - `/DRONEVIEW` = drone height, looking down at an **oblique** angle (a default an explicit angle can override: `/DRONEVIEW /TOPDOWN` = aerial straight-down).
  - `/BIRDSEYE` = straight down **from far above**; the ground reads like a map.
  - `/TOPDOWN` = straight down, **no height implied**.
- **Position vs movement:** `/DRONEVIEW` is a position. Airborne moves are `/FLYOVER` (forward over the land) and `/DRONEREVEAL:UP|BACK` (rise and/or retreat until the place opens out).
- **"Aerial altitude is not bird's-eye"** (SRC-005 SKILL:121).
- **H3:** SRC-009's measured aerial pull-back combines a pull-out with a rise and ends with the subject tiny below (shots/aerial-pullback.md). Start close and finish on the widest view.
- **Handheld in the air** is context-dependent (only from an aircraft door, P30); an aerial move on a tripod or slider is impossible (P77).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/DRONEVIEW` | An aerial viewpoint from drone altitude looking down at an oblique angle (not straight down). A POSITION, not a movement. **Rule:** DRONEVIEW is not BIRDSEYE and not TOPDOWN. | - | MEDIUM | SRC-001, SRC-002, SRC-004, SRC-005 | /DRONESHOT |
| `/FLYOVER` | The airborne camera travels forward over the landscape or subject. | speed | MEDIUM | SRC-001, SRC-002 | /OVERFLIGHT |
| `/DRONEREVEAL` | An aerial move (rising and/or pulling back) that reveals a large environment around a small subject. /DRONEREVEAL:UP or :BACK. | dir_reveal, speed | MEDIUM | SRC-001, SRC-002, SRC-003, SRC-009 | /AERIALREVEAL, /AERIALPULLBACK |

| Command | Image mode | Video mode |
|---|---|---|
| `/DRONEVIEW` | Seen from drone height, looking down at an angle over the scene. | Seen from drone height, looking down at an angle over the scene. |
| `/FLYOVER` | Seen from the air above the landscape, as a moment in forward flight; no motion verbs. | The camera flies forward high over the landscape; the ground passes underneath. |
| `/DRONEREVEAL` | Render the revealed end state: the subject small far below inside the wide place. | The camera rises and/or retreats until the subject is small far below and the whole place opens out. |
<!-- END GENERATED -->
