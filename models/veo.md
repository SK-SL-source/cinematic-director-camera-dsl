# Model adapter · Veo

English sentences describing the shot, placed after the subject/action/setting the user wrote.

## Evidence
| Level | Source | Rule |
|---|---|---|
| GUIDANCE | SRC-005D SKILL:68-75 | order: subject → action → setting → shot size, angle, lens, camera movement, focus behaviour → lighting/style → a separate audio sentence |
| GUIDANCE | SRC-004 vidadapt:222-232 | write prompts as a real shot description; say stillness as a positive fact (for example, that the camera stays locked in place); the negative field exists only on some surfaces, so turn exclusions into positive facts; say "no music" when you will score in the edit |
| GUIDANCE | SRC-005D SKILL:83-86 | on image-to-video describe motion and the end state, not the frame again; reference images do not define a timeline |

## Output rules
1. Order: size/framing → angle/height → lens → rig → **movement → focus** → composition → continuity (SRC-005D).
2. Every movement carries start, path, speed (if given), subject relation, parallax and end (if given) — the generic video rules (models/generic_video.md).
3. Stillness is always positive: "The camera stays locked in one position for the whole shot."
4. No exclusion lists in the camera text. The one guard per move is written as a fact ("the focal length stays the same"), and only when no simultaneous move breaks it (research/07 D39): a rack focus during a push no longer claims "the framing does not change".

## Example (actual adapter output)
`/CU /RACKFOCUS:A>B /DOLLYIN:SLOW`
> A close-up of {SUBJECT}'s face, head and shoulders. From this opening framing, the camera moves forward along the lens axis toward {SUBJECT}, slowly. {SUBJECT} grows larger in the frame; near objects grow faster than the background, which spreads past the frame edges. The focal length stays the same. The focus shifts from {A} to {B}.

Tests: tests/model_adapters.md (MA-VEO-*, MS-VEO-*).
