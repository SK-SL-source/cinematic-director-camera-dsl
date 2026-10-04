# Model adapter · Generic image

For any still-image model (keyframes, storyboard panels, stills) without its own file. **A still cannot move** (spec section 21; REG-11).

## Evidence
| Source | Rule |
|---|---|
| SRC-006 SKILL:45-62, 159-165 | one frozen instant with no cuts or sequences; the frame description covers size, lens, height, angle, distance and which planes are in focus |
| SRC-003 SKILL:101 | motion words belong to video; a still shows motion only as blur |
| SRC-002 img-shots:350-354 | camera movement in a still = the feeling of motion (blur, implied movement, frozen mid-move) |
| SRC-004 imgadapt:66-83, 199-216 | keyframe slot order (size/angle/lens early); imply motion with physical facts, not adjectives |

## Output rules
1. Framing → angle/height → Dutch → lens → focus → composition → rig look → movement-as-position → continuity-as-pose.
2. **Movements become positions:** where the camera is at that moment, the perspective, and what the frame implies. With an amount, render where the move arrives (`/ORBIT:R:45` → about 45 degrees around the subject toward camera-right). No motion verbs (pans, pushes, tracks, orbits…); the adapter checks this.
3. **Motion blur only when definitional:** whip pan, crash zoom, speed FAST.
4. **Rack focus:** a still shows one focus state — the start of the rack.
5. **Continuity:** screen direction becomes "caught heading from frame-left toward frame-right"; match on action becomes a pose partway through the action.

## Example (actual adapter output)
`/ORBIT:R:45 /FS`
> A full shot framing {SUBJECT} from head to toe. The camera is positioned about 45 degrees around {SUBJECT} toward camera-right, as a moment on an implied orbit path; {SUBJECT} stays centered.

`/PAN:R /WS`
> A wide shot; {SUBJECT} is seen full-body with plenty of surroundings. Composed as a moment within a pan to the right: {SUBJECT} sits toward the left edge with open space to the right.

Tests: tests/image_mode.md, tests/model_adapters.md (MA-GI-*), tests/regression.md REG-11.
