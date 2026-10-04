# PROJECT_GOAL · Cinematic Director Camera DSL

Every change to this skill is checked against this page first. It was fixed on 2026-10-01 from the maintainer's charter and an
architecture audit of the skill.

## Goal

A **model-independent, composable, verifiable** cinematography camera DSL. The DSL states camera intent
(`/MS /EYELEVEL /PAN:R`, `/FS /GROUNDLEVEL /TRACKSIDE:R`, `/MCU /OTS:A>B /DOLLYIN`). No model's limits — MiniMax H3, Kling, Veo,
Qwen or any other — may change the canonical camera semantics.

## Architecture (fixed)

```text
USER CAMERA INTENT → CAMERA DSL → CANONICAL CAMERA IR → MODEL SEMANTIC COMPILER → MODEL PROMPT WRAPPER → GENERATION PROFILE → MODEL
```

For MiniMax H3:

```text
Camera DSL → Canonical Camera IR → ONE shared H3 CAMERA CORE → mode wrapper (T2VA | I2VA | FL2VA | L2VA | Ref2VA) → generation profile
```

- **Canonical IR** keeps shot size, viewpoint (height, angle), movement, lens, focus, composition and rig as separate layers.
- **H3 camera core** (`scripts/adapters.py`, model `minimax_h3`) compiles the IR into H3 camera language once, for every mode, in four
  layers, each with its source:
  - `camera_core` — the official motion vocabulary (SRC-008 base-en 4.3); amplitude and speed tokens only when the DSL gives them
  - `temporal_clarifier` — how the move spreads over the clip (PROJECT_DEFINED, evidence id attached)
  - `derived_visual_constraint` — what the move does to the picture: where the subject ends up, what stays in frame, amounts in
    degrees / percent / metres the official vocabulary cannot carry
  - `negative_clarifier` — what the camera does not do, written only when no simultaneous move contradicts it
- **Mode wrappers** (`scripts/h3_wrappers.py`) only handle the official prompt schema, keyframe alignment lines, reference labels
  (`<Subject N>`, `<Picture N>`, `<Video N>`, `<Audio N>`) and the timeline. Base modes (T2VA / I2VA / FL2VA / L2VA) use
  `integrated_multimodal_description`; Ref2VA uses the six-field full-reference format. **No wrapper defines camera language.**
  There is no "I2VA camera language" or "Ref2VA camera language".
- **Reality profile** (`models/minimax_h3_profile.yaml`) answers one question: is this camera intent reliable in this mode under this
  generation profile. It is not grammar. A reliability figure is always bound to `mode + generation_profile`
  (the 42-cell matrix is `LOCAL_H3_REF2VA_PDD8_Q_416`, not "H3"). A failed test never changes a command's definition.
  A figure also belongs to the prompt wording it was measured with: evidence generated with another sentence split than the core writes
  today is historical (`PRE_REFACTOR_WORDING`), its current-core applicability UNVERIFIED until a production shot re-validates that
  command (CL-036). Validation is production-driven; nothing is re-run to complete a matrix.
  A production route is bound, beyond that, to the direction and to the start and end framing it was measured with: any other
  start / end pair is UNVERIFIED, and the measured route is only named as related evidence, never applied (CL-042).
  A route measured with a stated angle (the arc of an ORBIT) is bound to that angle too: another angle, or no stated angle, is UNVERIFIED (CL-048).
  The rows of the reality matrix follow the same rule: a grade measured at one shot size is not a measured grade at another (CL-044).
- **Production routing** outputs recommendations, warnings and model limitations only. It never changes the IR, the semantics or the
  camera core phrase; the user decides.

## Fidelity rules

1. A user-given amount, direction or speed is never dropped silently and never silently added. If the model has no vocabulary for it, the
   value goes into a clarifier layer or a warning.
2. Official vocabulary first (SRC-008). Project wording is allowed only in the clarifier layers, labelled with its evidence.
3. Wording measured in the lab (LOCAL-002) is evidence for a clarifier, never a reason to alter the core semantics.
4. `steadily over the whole video`, final-frame position clauses, keep-in-frame clauses and similar sentences are clarifiers, not motion
   vocabulary.

## Source priority (H3)

1. MiniMax official h3-prompt-writing: SKILL.md, references/base-en.txt, references/ref-en.txt (SRC-008 / LOCAL-001)
2. This project's reality tests (LOCAL-002)
3. Other open-source cinematography / prompt skills (SRC-009 and the rest)

A third-party skill never overrides the official H3 format.

## Frozen

104 canonical commands, 244 aliases, 18 grammar rules, V2_BASELINE. Grammar changes (for example amplitude words on a pan) are a
separate, maintainer-approved design step, never a side effect of an adapter fix.

## Status of the parts (audit of 2026-10-01)

Aligned: registry, parser and IR, conflict / compatibility / continuity rules, image and video semantics, multi-model adapters, license and
provenance, public release gate, reality data. Phase 1 (this charter, the layered core, parameter fidelity, the wrappers) is applied
(CL-030). Phase 2 (CL-032) is applied: the generation profiles are structured (`LOCAL_H3_REF2VA_PDD8_Q_416`, `LOCAL_H3_I2VA_PDD8_Q_416`,
`LOCAL_H3_T2VA_PDD8_Q_416`, `LOCAL_H3_FL2VA_PDD8_Q_416`, `LOCAL_H3_L2VA_PDD8_Q_416` (CL-049), `LOCAL_H3_PRODUCTION_REF2VA`, `LOCAL_H3_PRODUCTION_I2VA`, `OFFICIAL_REFERENCE`; one profile is one mode, CL-034), every grade carries its profile, results.json carries provenance and a frozen verdict
hash, the height/angle cells are classified as viewpoint, the pre-audit I2VA production shots are PROVISIONAL, and routing answers
UNVERIFIED outside the scope it is asked about. The I2VA production baseline under `LOCAL_H3_I2VA_PDD8_Q_416` is complete and frozen
(H3_I2VA_PRODUCTION_BASELINE_COMPLETE, 2026-10-02, CL-048): sixteen routes with three seeds each, three PRODUCTION_VALIDATED, two CONDITIONAL, eleven LOW
(the table is in models/minimax_h3.md). The multi-mode production baseline is complete (H3_MULTI_MODE_PRODUCTION_BASELINE_COMPLETE,
2026-10-02, CL-050): the same sixteen routes and seeds in T2VA (0 PRODUCTION_VALIDATED, 0 CONDITIONAL, 16 LOW), FL2VA (11 / 0 / 1, and 4
INSUFFICIENT_EVIDENCE), L2VA (2 / 3 / 11) and Ref2VA with the current core (0 / 1 / 15, kept beside the unchanged 42-cell matrix), each
bound to its own mode and profile; the frozen I2VA baseline was not re-run. The last independent package, the free camera baseline, is
complete (H3_FREE_CAMERA_PRODUCTION_BASELINE_COMPLETE, 2026-10-03, CL-051): twelve routes with no reference target to frame in all five modes
(T2VA 9 / 1 / 2 / 0, I2VA 2 / 6 / 4 / 0, FL2VA 1 / 0 / 0 / 11, L2VA 1 / 2 / 6 / 3, Ref2VA 7 / 2 / 2 / 1 as
PRODUCTION_VALIDATED / CONDITIONAL / LOW / INSUFFICIENT_EVIDENCE). Camera validation stops here: nothing is validated to complete a list; no new
route, seed, angle or shot size is tested and no LOW route is re-tuned; a move or a profile outside the baselines stays UNVERIFIED and is
validated when a production needs it.

## H3 Camera Production Evidence and release status (v1.0.0)

One DSL, one evidence system. The measured H3 results are the **H3 Camera Production Evidence**, of two types:
- **CONSTRAINED_PRODUCTION** — camera motion together with production constraints (start and end shot size, landing, screen position,
  behaviour relative to a reference target): the I2VA production baseline, the multi-mode production baseline and the 42-cell Ref2VA matrix.
  Stored as `subject_context: CHARACTER_ANCHORED`, the default.
- **CAMERA_ONLY** — camera motion itself, measured on a fixed set with nothing to frame: the free camera baseline. Stored as
  `subject_context: ENVIRONMENT_ONLY`; routing reads it with `--h3-subject-context camera_only` (stored name `environment_only`).

The person in the constrained tests is a reference target, a test fixture, not a category of the DSL. The stored names stay as they are, so no
record, test or verdict hash changes (CL-052). A grade holds for its exact scope only (mode, generation profile, command, direction, start and
end framing, angle, evidence type); outside it the answer is UNVERIFIED and no grade is borrowed. LOW does not mean the DSL is wrong, and
INSUFFICIENT_EVIDENCE does not mean the model failed.

```text
h3_production_baseline_status:     COMPLETE   # the v1.0 production baseline: CONSTRAINED_PRODUCTION and CAMERA_ONLY, all five H3 modes
h3_full_command_space_validation:  PARTIAL    # by design: not every command x mode x profile x direction x shot size x landing x angle
```
