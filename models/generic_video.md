# Model adapter · Generic video

The reference adapter for any text-to-video or image-to-video model without its own file. Explicit and a little verbose on purpose: it spells out every element a model needs so the camera cannot be misread.

## Evidence
| Source | Rule |
|---|---|
| spec section 22; SRC-012 SKILL:122, 196-199; SRC-010 SKILL:33-35 | a move needs a start frame, path, direction, speed, subject relation, end frame (and what becomes visible) |
| SRC-004 lexicon:134-151 | say what physically changes (parallax for travel, none for rotation or zoom) |
| SRC-002 vocab:94-106 (camera contract) | state the camera behaviour explicitly; silence reads as licence to drift (SRC-004 failmodes F6) |
| SRC-004 SKILL:138, SRC-002 camera:297 | one dominant move per clip; more is warned |

## Output rules
1. Framing → angle/height → Dutch → lens → focus → composition → rig → movement → continuity.
2. **Movement sentence** = START ("From this opening framing") + PATH/DIRECTION + amount + SPEED, then SUBJECT RELATION + PARALLAX, then END (only if given), then one guard sentence.
3. **Strict:** unspecified speed, amount and end are omitted and listed as `unspecified`.
4. **Sequences:** each timed move is prefixed "From Xs to Ys:" (the notation of SRC-001 SKILL:199-205 and SRC-002 vocab:76-79). Add a note that some models blend sequential moves (SRC-004 failmodes:314).
5. **Directions:** camera-relative words (camera-right, frame-left); orbit direction also given as clockwise/counterclockwise seen from above.

## Example (actual adapter output)
`/MS /LOWANGLE /DOLLYIN:MS>MCU:SLOW`
> A medium shot framing {SUBJECT} from the waist up. The camera looks up at {SUBJECT} from a low angle. From this opening framing, the camera moves forward along the lens axis toward {SUBJECT}, slowly. {SUBJECT} grows larger in the frame; near objects grow faster than the background, which spreads past the frame edges. It ends on a medium close-up. The focal length stays the same.

Tests: tests/video_mode.md, tests/model_adapters.md (MA-GV-*).
