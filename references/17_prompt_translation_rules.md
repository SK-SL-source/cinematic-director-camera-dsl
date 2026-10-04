# 17 · Prompt translation rules

How a validated camera state becomes model text. The pipeline is fixed:
DSL → aliases → validation → camera state (schemas/) → mode split (image / video) → model adapter (models/) → camera text.

## 1. Camera text only (Preserve Rules, spec section 28)
Adapters write **camera text**. People, faces, age, gender, clothes, set, props, dialogue, story, head count and actions come from the user's own shot description and are never invented or changed. Subjects stay as placeholders (`{SUBJECT}`, `{A}`, `{B}`) until they are joined with that description. The only subject-facing lines an adapter writes are the ones the user asked for with continuity commands (`/EYELINE`, `/SCREEN`, `/AXIS`).

## 1b. Errors stop the render
A result with status ERROR is never turned into camera text. The CLI prints each error with its fix, and the user chooses (research/07 D40). A WARN renders with the warnings shown.

## 2. STRICT mode is the default (spec section 26)
- Render exactly what was given. `/MS /LOWANGLE` never gains a lens, depth of field, a move or a Dutch angle.
- Definitional parts of a command are not additions (a push-in's parallax, a follow's rear view, a drone view's downward look).
- Unspecified parameters (speed, amount, end size, direction) are **left out of the text** and listed under `unspecified`, so the user sees what the model will decide.

## 3. Camera Intent Priority (spec section 29)
1 explicit DSL > 2 natural-language camera words > 3 storyboard fields > 4 shot description > 5 director suggestion > 6 model default. A lower layer never overrides a higher one; overridden items are reported (`P00-OVERRIDDEN`). CLI: `--nl`, `--storyboard`, `--director`.

## 4. Director Mode (spec sections 25, 27)
Only when the user asks ("recommend", "design the shot", "導演模式", `MODE:DIRECTOR`). Director Mode decides **why** (shot function, emotional beat); the Camera DSL decides **how**. Suggestions enter as priority-5 commands and are labelled `DIRECTOR_SUGGESTED` next to the user's `USER_SPECIFIED` commands. Keep it small: pick a shot function (establishing, relation, close-up, insert, reaction, transition, aftermath, POV, reveal — SRC-004 cinlang:18-31), then one dominant move or none.

## 5. Video mode (spec section 22)
Each movement states START (opening framing), PATH and DIRECTION, SPEED (if given), SUBJECT RELATION, PARALLAX (definitional), END (if given). Add the one semantic guard that keeps the move from being misread ("the focal length stays the same" for a dolly; "the subject stays in place and does not turn" for an orbit). Never write vague "cinematic tracking shot". Sequential moves inside one clip are valid DSL, but warn: some models blend them (research/04 section 2). Every adapter writes the order: time windows ("From 0s to 2s:", H3 "At about 2 seconds,"), THEN steps ("First, … Then, …"), and "At the same time," for a second move in the same step. `/STATIC` inside a segment is a hold step, not a lock for the whole shot (research/07 D40).

## 6. Image mode (spec section 21)
A still cannot move. Convert every movement into camera position + perspective + framing + implied motion + a moment within the move, with **no motion verbs**. Moves with an amount render where they arrive (`/ORBIT:R:45` → positioned about 45° around the subject toward camera-right). Motion blur only where it is definitional (whip pan, crash zoom, FAST).

## 7. Model adapters (spec section 24)
Wording may change; the shot may not. Every adapter is tested to keep each command's intent markers and none of the conflicting values (tests/model_adapters.md, `scripts/audit.py` MODEL AUDIT). Model specifics: models/*.md.

## 8. Style words
`/CINEMATIC` is a style word, not a camera setting. It adds nothing in STRICT mode except the word itself (H3 accepts "cinematic" as its style opener, SRC-008 base-en:78).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/CINEMATIC` | A style word only. It sets no camera parameter (no lens, no aspect ratio, no movement, no depth of field). **Rule:** CINEMATIC adds nothing to the camera in STRICT mode. | - | MEDIUM | SRC-003, SRC-004, SRC-005, LOCAL-001 | /FILMIC, /MOVIELOOK |

| Command | Image mode | Video mode |
|---|---|---|
| `/CINEMATIC` | At most one style word ('cinematic'); no camera additions. | At most one style word ('cinematic', which H3 accepts as a style token); no camera additions. |
<!-- END GENERATED -->
