# 12 · Composition

Where things sit inside the frame: placement (center or a third), symmetry, negative space, headroom, lookroom, leading lines, frame-within-frame, foreground layer, deep staging.

## Rules
- **Placement is exclusive:** centered or on a third, not both (hard); symmetry with thirds is a soft conflict (SRC-004 cinlang:416-417).
- **Lookroom sits in front of the face:** subject on the left third → open space on the right. `/THIRDS:L /LOOKROOM:L` is impossible (R04; SRC-004 cinlang:402-406).
- **Composition never adds objects.** `/FGLAYER`, `/FRAMEINFRAME` and `/LEADLINES` use what the scene already has; name the thing (`/FGLAYER:RAILING`) or the adapter says "an element of the scene" (Preserve Rules, spec section 28).
- **Headroom:** at MS leave roughly 5-10% above the head; at CU the eyes sit near the upper third line (SRC-004 cinlang:398-400).
- **Power in a two-person frame** follows frame area, height in frame, sharpness, lookroom and obstruction (SRC-004 cinlang:429-432) — useful in Director Mode, not a command.
- **9:16:** stage in depth, scale one step tighter, keep faces in the middle ~60% of the frame height (SRC-004 cinlang:462-500).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/CENTER` | The subject sits at the center of the frame. | - | HIGH | SRC-001, SRC-003, SRC-004 | /CENTERED, /CENTRED, /CENTRE |
| `/THIRDS` | The subject sits on a third line. /THIRDS:L or :R names which third. | dir_lr | HIGH | SRC-001, SRC-003, SRC-004, SRC-005, SRC-006 | /RULEOFTHIRDS, /THIRD |
| `/SYMMETRY` | The frame is balanced as a mirror image around the vertical center line. | - | HIGH | SRC-001, SRC-003, SRC-004 | /SYMMETRIC, /SYMMETRICAL |
| `/NEGSPACE` | A large empty area in the frame around the subject. /NEGSPACE:L\|R\|UP\|DOWN names where. | side | HIGH | SRC-001, SRC-002, SRC-003, SRC-004 | /NEGATIVESPACE, /EMPTYSPACE |
| `/HEADROOM` | How much space sits above the head. /HEADROOM:TIGHT\|NORMAL\|LOOSE. | level | HIGH | SRC-001, SRC-004, SRC-005 | /HEADSPACE |
| `/LOOKROOM` | Open space on the side the subject faces. /LOOKROOM:L\|R = the empty side of the frame. | dir_lr | HIGH | SRC-001, SRC-004 | /LEADROOM, /NOSEROOM, /LOOKSPACE |
| `/LEADLINES` | Lines in the scene (roads, rails, edges) lead the eye to the subject. | - | HIGH | SRC-001, SRC-003, SRC-004, SRC-005 | /LEADINGLINES |
| `/FRAMEINFRAME` | An opening in the scene (door, window, arch) frames the subject inside the frame. | - | HIGH | SRC-001, SRC-003, SRC-004 | /FRAMEWITHINFRAME, /FRAMED |
| `/FGLAYER` | Something sits between the camera and the subject in the near foreground (partially obstructing or framing). | label | HIGH | SRC-001, SRC-003, SRC-004, SRC-005 | /FOREGROUND, /FGOBSTRUCTION, /REPOUSSOIR |
| `/DEEPSTAGING` | Subjects are placed at different depths (foreground, midground, background) instead of side by side. | - | MEDIUM | SRC-004, SRC-005 | /DEPTHSTAGING, /LAYERS |

| Command | Image mode | Video mode |
|---|---|---|
| `/CENTER` | Subject at the center of the frame. | Subject stays at the center of the frame. |
| `/THIRDS` | Subject on the left or right third line. | Subject stays on the stated third line. |
| `/SYMMETRY` | Mirror-balanced frame. | The frame stays mirror-balanced. |
| `/NEGSPACE` | A large empty area on the stated side. | A large empty area stays on the stated side. |
| `/HEADROOM` | The stated amount of space above the head. | The head keeps the stated space above it. |
| `/LOOKROOM` | More open space on the stated side, in front of the face. | More open space stays on the stated side. |
| `/LEADLINES` | Existing lines in the scene run toward the subject. | Existing lines in the scene run toward the subject. |
| `/FRAMEINFRAME` | An existing opening in the scene frames the subject. | An existing opening in the scene frames the subject. |
| `/FGLAYER` | An element from the scene in the near foreground, between camera and subject. | An element from the scene stays in the near foreground. |
| `/DEEPSTAGING` | Subjects at different depths: one near, one farther back. | Subjects stay at different depths. |
<!-- END GENERATED -->
