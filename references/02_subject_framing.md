# 02 · Subject framing

Who is in the frame and from which side: head count (`shot.subject_count`), viewpoint (`shot.viewpoint`: OTS or POV) and subject orientation (`subject.orientation`: frontal, three-quarter, profile, rear).

## Rules
- **POV is the camera being a character's eyes.** `/POV:A` hides A completely (no hands, shadow or reflection unless the user writes them; SRC-005B h3guide:70). It is **not** "A looks into the lens" (`/EYELINE:A>CAM`, REG-02) and **not** FPV (a drone rig).
- **OTS is written A>B:** behind A's shoulder, looking at B. Plain `/OTS` = the foreground shoulder is visible (dirty). `/CLEANOTS` keeps the foreground person out of frame; it cannot also be a two-shot (P73).
- **Orientation describes the subject relative to the camera**, never a camera move. Tracking commands imply one by default (FOLLOW = rear, LEAD = frontal, TRACKSIDE = profile); an explicit contradiction is a conflict (`/FOLLOW /FRONTAL`, P71).
- **POV needs a look.** In a shot list, a POV shot should sit next to a shot of its owner looking (continuity C06; SRC-004 cinlang:30).
- **9:16 note:** two people side by side become slivers; stage them in depth (`/DEEPSTAGING`, SRC-004 cinlang:462-470).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/SINGLE` | Only one person is in frame. | subject | LOW | SRC-004 | /SINGLESHOT, /CLEANSINGLE |
| `/TWOSHOT` | Two subjects share the frame. | subject, subject | HIGH | SRC-002, SRC-004 | /2SHOT |
| `/THREESHOT` | Three subjects share the frame. | - | LOW | SRC-004 | /3SHOT |
| `/GROUPSHOT` | Four or more subjects share the frame. | - | LOW | SRC-001, SRC-005 | /GROUP, /ENSEMBLE |
| `/OTS` | The camera stands behind A's shoulder looking at B; part of A (shoulder/back of head) is in the near foreground. /OTS:A>B. | relation | HIGH | SRC-001, SRC-002, SRC-003, SRC-004 | /OVERTHESHOULDER, /OVERSHOULDER |
| `/DIRTYOTS` | Over-the-shoulder with the foreground person's shoulder and head clearly in frame. | relation | LOW | SRC-004 | /DIRTYSINGLE |
| `/CLEANOTS` | The camera sits at the over-the-shoulder position, but the foreground person is kept out of frame (a clean single from that side). | relation | LOW | SRC-004 | - |
| `/POV` | The camera IS A's eyes; A is not visible (except hands/body parts only if the user writes them). /POV:A. **Rule:** POV is not 'the subject looks at the camera' (that is /EYELINE:X>CAM) and not FPV (a drone rig). | subject | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005B, LOCAL-001 | /FIRSTPERSON, /SUBJECTIVE |
| `/FRONTAL` | The subject faces the camera square-on. | - | MEDIUM | SRC-004, SRC-001 | /FRONT, /FACING |
| `/THREEQUARTER` | The subject is turned about 45 degrees from the camera. | - | HIGH | SRC-001, SRC-002, SRC-004, LOCAL-002 | /3Q, /THREEQUARTERS |
| `/PROFILE` | The subject is seen from the side (about 90 degrees). | - | HIGH | SRC-001, SRC-003, SRC-004 | /SIDEPROFILE, /SIDE |
| `/REAR` | The subject's back is to the camera. | - | MEDIUM | SRC-002, SRC-003, SRC-004 | /BACKVIEW, /FROMBEHIND |

| Command | Image mode | Video mode |
|---|---|---|
| `/SINGLE` | Only one person in the frame. | Only one person in the frame for the whole shot. |
| `/TWOSHOT` | Both subjects in one frame. | Both subjects stay in one frame. |
| `/THREESHOT` | Three subjects in one frame. | Three subjects stay in one frame. |
| `/GROUPSHOT` | The whole group in one frame. | The whole group stays in one frame. |
| `/OTS` | A's shoulder and the back of A's head in the near foreground, B facing the camera beyond. | A's shoulder stays in the near foreground while B is the subject of the shot. |
| `/DIRTYOTS` | The foreground shoulder and part of the head occupy a frame edge. | The foreground shoulder and part of the head stay at a frame edge. |
| `/CLEANOTS` | Seen from over the shoulder, but the foreground person is outside the frame. | The foreground person stays outside the frame for the whole shot. |
| `/POV` | Seen through A's eyes; A is not in the frame. | Seen through A's eyes for the whole shot; A never appears (no hands, shadow or reflection unless written). |
| `/FRONTAL` | The subject faces the camera square-on. | The subject faces the camera square-on. |
| `/THREEQUARTER` | The subject is turned about 45 degrees from the camera. | The subject is turned about 45 degrees from the camera. |
| `/PROFILE` | The subject seen from the side. | The subject seen from the side. |
| `/REAR` | The subject seen from behind. | The subject seen from behind. |
<!-- END GENERATED -->
