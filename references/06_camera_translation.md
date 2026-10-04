# 06 · Camera translation

The camera body travels in a straight line: forward or back in its viewing direction (dolly in/out), sideways (truck), or straight up/down (pedestal). Travel produces **parallax** — near things move more than far things.

## Rules
- **DOLLY ≠ ZOOM** (REG-05). A dolly moves the camera; the focal length does not change. Never render a dolly with the word "zoom" (SRC-002 camera:280; SRC-004 lexicon:134-140; SRC-005 SKILL:111).
- **Say what changes in the geometry:** for a push-in, the subject grows faster than the wall behind it, which spreads past the frame edges (SRC-004 lexicon:138).
- **Give the move a range** when the end matters: `/DOLLYIN:MS>MCU`. On H3 this is the measured way to control a push (LOCAL-002 H3LAB-PUSH-01, 3/3); "with small amplitude" is inert (SRC-009 camera-grammar:45-59).
- **A dolly past nothing reads as a zoom:** without something near the lens, travel has no parallax to show (SRC-009 camera-grammar:41-43). The DSL cannot add scene objects (Preserve Rules); the adapter warns instead.
- **Legacy names:** `/PUSHIN` → `/DOLLYIN`, `/PULLOUT` → `/DOLLYOUT`; Higgsfield/fal "Dolly Left/Right" → `/TRUCK` (research/04 #17).
- **Special technique:** `/DOLLYIN /ZOOMOUT` together = `/DOLLYZOOM:IN` (07_tracking_complex_motion.md).
- **Chinese:** 推镜 (dolly in) vs 变焦推近 (zoom in); a bare 推近 is ambiguous (SRC-004 lexicon:384).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/DOLLYIN` | The camera body physically travels forward along the lens axis toward the subject. Near objects grow faster than far ones (parallax). The focal length does not change. **Rule:** Never translate DOLLYIN as a zoom. | size_range, percent, distance, magnitude, speed | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-009, LOCAL-001, LOCAL-002 | /PUSHIN, /PUSH, /DOLLYFORWARD, /SUPERDOLLY, /DOLLY:IN, /DOLLY:FWD |
| `/DOLLYOUT` | The camera body physically travels backward along the lens axis, away from the subject; more of the set comes into view at the edges. Focal length stays fixed. **Rule:** Never translate DOLLYOUT as a zoom out. | size_range, percent, distance, magnitude, speed | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-009, LOCAL-001 | /PULLOUT, /PULLBACK, /PULL, /DOLLYBACK, /DOLLY:OUT, /DOLLY:BACK |
| `/TRUCK` | The camera body slides sideways (left or right), parallel to the scene. Near objects pass faster than far ones. **Rule:** TRUCK is not PAN: the camera travels, it does not turn. | dir_lr, percent, distance, magnitude, speed | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, LOCAL-001 | /DOLLY:L, /DOLLY:R, /TRUCKLEFT, /TRUCKRIGHT, /CRAB, /SLIDE, /LATERAL |
| `/PEDESTAL` | The camera body rises or lowers straight up or down, keeping its angle. **Rule:** PEDESTAL is not TILT: the lens angle stays the same. | dir_ud, distance, magnitude, speed | HIGH | SRC-001, SRC-002, SRC-004, SRC-005, SRC-009, LOCAL-001 | /PEDESTALUP, /PEDESTALDOWN, /PEDUP, /PEDDOWN |

| Command | Image mode | Video mode |
|---|---|---|
| `/DOLLYIN` | Cannot travel in a still. Place the camera close to the subject as a moment in the approach; near objects are large at the frame edges. | State START size, the forward PATH toward the subject, SPEED if given, the subject growing in frame, near-far PARALLAX, and the END size if given. |
| `/DOLLYOUT` | Cannot travel in a still. Place the camera farther back, the subject smaller, more surroundings revealed at the edges. | State START size, the backward PATH, SPEED if given, the subject shrinking and more set appearing at the edges, and the END size if given. |
| `/TRUCK` | Cannot travel in a still. Frame side-on with a foreground element partly passing the edge, implying sideways travel. | The camera slides sideways; foreground passes faster than the background (lateral parallax). |
| `/PEDESTAL` | Cannot rise in a still. Choose the height the move reaches; no motion verbs. | The whole camera rises or lowers straight up or down while staying level. |
<!-- END GENERATED -->
