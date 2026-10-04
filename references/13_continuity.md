# 13 · Continuity

Cross-shot geometry and shot functions. Each generated clip starts without any memory of the previous one, so every shot has to restate its own continuity (after SRC-004 cinlang:239-243).

## Rules
- **Axis of action (180°):** `/AXIS:A-B` = A screen-left, B screen-right for every shot on this side of the line. A later `/AXIS:B-A` without `/CROSSAXIS:<method>` is an error (C01). Legitimate crossings (SRC-004 cinlang:292-303):
  - the actors re-form the line;
  - a visible camera move;
  - a neutral shot on the line;
  - a cutaway;
  - a re-establishing wide.
- **Crossing by move:**
  - `/CROSSAXIS:MOVE` needs a sideways move (`/TRUCK`, `/ORBIT`, `/TRACKSIDE`). A push along the lens cannot carry the audience over the line (C09; SRC-004 cinlang:295-296).
  - The text then says where each person is **by the end** of the shot, not that they "stay" there.
  - A declared crossing is also not a jump cut (C05 is skipped).
- **Eyelines are vectors:** with `/AXIS:A-B`, A looks off-screen right and B off-screen left (C02). Write gaze as a positive state ("her eyes are on…"); negative gaze sentences failed on H3 (LOCAL-002 H3LAB-GAZE-01).
- **Screen direction survives the cut:** L2R in one shot, R2L in the next reads as a turn-around (C04). Neutral TOWARD/AWAY shots reset it.
- **30° / two-step rule:** consecutive shots of the same subject change size by two rungs or the angle by 30° or more (C05; SRC-004 cinlang:315-326).
- **POV needs a look** from its owner in a neighbouring shot (C06).
- **CONTINUOUS:** a shot marked `CONTINUOUS` starts exactly where the previous one ended — size, angle, height (C07; DIR-08, SRC-010 SKILL:63-65).
- **Shot/reverse-shot keeps lens and distance, mirrored** (C08; SRC-004 cinlang:351-355).
- **Functions, not sizes:** `/INSERT`, `/REACTION`, `/CUTAWAY` pair with any size (research/07 D02).
- **H3:** exact cut points inside one generation are unreliable — one shot per generation (LOCAL-002 H3LAB-CUT-01).

Run a shot list with: `python scripts/camera_dsl.py shots "S1: … \n S2: …"`.

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/AXIS` | The 180-degree line between two subjects. /AXIS:A-B = A stays screen-left, B screen-right for every shot on this side of the line. | axis | HIGH | SRC-002, SRC-004 | /180, /AXIS180, /LINE, /180RULE |
| `/CROSSAXIS` | A declared, intentional crossing of the 180-degree line, with how it is made legible. /CROSSAXIS:MOVE\|NEUTRAL\|CUTAWAY\|REESTABLISH\|BLOCKING. | method | MEDIUM | SRC-004, SRC-002 | /CROSSLINE, /CROSS |
| `/EYELINE` | Where a subject looks. /EYELINE:A>B, A>CAM (into the lens), A>OFFL / A>OFFR (off-screen left/right), A>OFFUP / A>OFFDOWN. **Rule:** A>CAM is 'looking into the lens'; it is not POV. | relation | HIGH | SRC-004, SRC-006, LOCAL-002 | /LOOK, /GAZE, /LOOKCAM, /LOOKATCAMERA |
| `/SCREEN` | Direction of travel on screen. /SCREEN:L2R, R2L, TOWARD (the camera), AWAY. | screen | HIGH | SRC-002, SRC-004, SRC-005B | /SCREENDIRECTION, /DIRECTION |
| `/SRS` | This shot is the reverse of the previous one in a dialogue pair: same lens and distance, mirrored position on the same side of the axis. /SRS:A>B = now looking at B from A's side. | relation | HIGH | SRC-002, SRC-004 | /REVERSE, /SHOTREVERSESHOT, /REVERSESHOT |
| `/MATCHACTION` | Cut on action: this shot starts on the same movement the previous shot ended on. | label | HIGH | SRC-002, SRC-004 | /CUTONACTION, /MATCHONACTION |
| `/MATCHCUT` | A cut linked by matching shape, motion or composition. /MATCHCUT:SHAPE\|MOTION\|COMPOSITION. | kind | HIGH | SRC-002, SRC-004, SRC-007 | /GRAPHICMATCH |
| `/REACTION` | Shot function: shows a character's reaction to an action or line. Pair with any size. /REACTION:A. | subject | HIGH | SRC-001, SRC-002, SRC-004, SRC-005 | /REACT, /REACTIONSHOT |
| `/INSERT` | Shot function: a detail of an object or action that carries story. Pair with a tight size. /INSERT:LETTER. | label | HIGH | SRC-002, SRC-004, SRC-005B | /DETAIL, /INSERTSHOT |
| `/CUTAWAY` | Shot function: a shot away from the main action (another place or thing) used to bridge an edit. /CUTAWAY:CLOCK. | label | HIGH | SRC-004, SRC-005B | /CUTAWAYSHOT, /BRIDGE |

| Command | Image mode | Video mode |
|---|---|---|
| `/AXIS` | A on the left side of the frame, B on the right. | A stays on the left side of the frame, B on the right. |
| `/CROSSAXIS` | Not rendered in a single image; recorded for the shot list. | When METHOD is MOVE the camera visibly travels across the line; other methods are editing notes. |
| `/EYELINE` | State the gaze as a positive fact: whose eyes are on what. | State the gaze as a positive fact that holds for the whole shot. |
| `/SCREEN` | Pose the subject mid-stride heading in the stated screen direction. | The subject moves in the stated screen direction for the whole shot. |
| `/SRS` | Mirror the previous frame's camera position on the same side of the line. | Mirror the previous shot's camera position on the same side of the line; keep lens and distance. |
| `/MATCHACTION` | Pose the subject partway through the same action the previous shot ended on. | Open on the continuation of the previous shot's action. |
| `/MATCHCUT` | Place the matched shape or composition in the same frame position as the previous shot. | Place the matched shape or motion in the same frame position as the previous shot. |
| `/REACTION` | The reacting face is readable in frame. | The reacting face stays readable in frame. |
| `/INSERT` | The named object fills the frame. | The named object fills the frame. |
| `/CUTAWAY` | The named thing or place, away from the main action. | The named thing or place, away from the main action. |
<!-- END GENERATED -->
