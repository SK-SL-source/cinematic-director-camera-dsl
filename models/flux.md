# Model adapter · FLUX

Stills on FLUX (text-to-image; edit variants follow qwen_image_edit.md's hold-plus-change pattern).

## Evidence
| Level | Source | Rule |
|---|---|---|
| CAPABILITY MATRIX | SRC-004 imgadapt:19-42 | Flux: literal prompt fidelity "best"; negative prompt "part" (so exclusions become positive facts); instruction editing "best" (edit class) |
| ROUTING | SRC-003 SKILL:114-119 | `fal-ai/flux-2/klein/9b` as a fast draft still model |
| GENERAL | SRC-004 imgadapt:66-83 | early tokens weigh more: put size, angle and lens first |
| UNVERIFIED | — | no source measures how FLUX responds to specific camera words; this adapter uses the generic image rules |

## Output rules
1. Same as models/generic_image.md, but the **first sentence is the shot size**, followed immediately by angle and lens, then the rest of the framing.
2. No "no …" lists (negative prompts are only partly supported); state what the frame shows.
3. No motion verbs; moves become positions (spec section 21).

## Example (actual adapter output)
`/MS /LOWANGLE /DOLLYIN:MS>MCU:SLOW`
> A medium shot framing {SUBJECT} from the waist up. The camera looks up at {SUBJECT} from a low angle. The camera is positioned close to {SUBJECT}, at the medium close-up a push-in would reach; near objects look large at the frame edges.

Tests: tests/model_adapters.md (MA-FLX-*, MS-FLX-*).
