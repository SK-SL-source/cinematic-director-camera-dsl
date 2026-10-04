# 11 · Focus and depth of field

Depth of field (`focus.dof`: shallow or deep), the focus target plane (`focus.target`: FG, MG, BG), focus pulls (`/RACKFOCUS`) and the split diopter.

## Rules
- **RACK FOCUS ≠ camera movement** (REG-07). The focal plane moves; the framing does not change. It does not count toward the motion budget (SRC-011 movement-catalog.md:441).
- **Write a rack as an event with a start and an end target:** `/RACKFOCUS:FG>BG` or `/RACKFOCUS:A>B` (SRC-004 cinlang:233-235; SRC-005 SKILL:133-134). `/PULLFOCUS` is the slower form.
- **Describe the optical result, not "bokeh":** what is sharp and what dissolves. "Bokeh" alone invites round highlight balls (SRC-004 cinlang:222-235); `/BOKEH` resolves to `/SHALLOW` with that warning.
- **A still shows one focus state:** image mode renders the start of the rack.
- **Physics sanity:** ultra-wide + shallow and telephoto + deep are context-dependent (SRC-004 cinlang:189-206 depth-of-field arithmetic).
- **H3:** a rack worked first time with a static camera and two depth planes, motivated by a look (SRC-009 shots/rack-focus.md).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/SHALLOW` | A thin plane of focus: the subject is sharp, the foreground and background fall soft. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-006 | /SHALLOWDOF, /SHALLOWFOCUS, /BOKEH |
| `/DEEPFOCUS` | Everything from foreground to background is sharp. | - | HIGH | SRC-001, SRC-003, SRC-004, SRC-005 | /DEEP, /DEEPDOF, /ALLSHARP |
| `/RACKFOCUS` | The plane of focus shifts from one subject/plane to another during the shot; framing is unchanged. /RACKFOCUS:A>B or :FG>BG. **Rule:** RACKFOCUS moves focus, not the camera. It is never a dolly or zoom. | relation, speed | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-005, SRC-007, SRC-009 | /PULLFOCUS, /FOCUSPULL, /RACK |
| `/FGFOCUS` | The plane of focus sits on the foreground. | subject | MEDIUM | SRC-004, SRC-005, SRC-006, SRC-007 | /FOCUSFG, /FOREFOCUS |
| `/MGFOCUS` | The plane of focus sits on the midground. | subject | MEDIUM | SRC-004, SRC-005, SRC-006 | /FOCUSMG |
| `/BGFOCUS` | The plane of focus sits on the background; nearer planes are soft. | subject | MEDIUM | SRC-004, SRC-005, SRC-006 | /FOCUSBG |
| `/SPLITDIOPTER` | A split-field lens keeps two distances in focus together, one close to the camera and one far away, divided by a soft blurred line. | - | HIGH | SRC-001, SRC-004 | /DIOPTER, /SPLITFOCUS |

| Command | Image mode | Video mode |
|---|---|---|
| `/SHALLOW` | Describe what is sharp and what dissolves (not just 'bokeh'). | Subject stays sharp while the background stays soft. |
| `/DEEPFOCUS` | Foreground, midground and background all sharp. | Foreground, midground and background all stay sharp. |
| `/RACKFOCUS` | A still shows one focus state: render the START plane sharp and the target soft, or the END state if the user asks for it. | Focus starts on the first target, then shifts to the second; the framing does not change. |
| `/FGFOCUS` | Foreground sharp; farther planes soft. | Focus stays on the foreground. |
| `/MGFOCUS` | Midground sharp; near and far planes soft. | Focus stays on the midground. |
| `/BGFOCUS` | Background sharp; foreground soft. | Focus stays on the background. |
| `/SPLITDIOPTER` | A near subject on one side and a far subject on the other are both sharp; a soft seam runs between them along a vertical edge. | Both planes stay sharp; neither subject crosses the seam. |
<!-- END GENERATED -->
