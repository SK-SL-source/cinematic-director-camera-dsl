# 10 · Zoom

Only the focal length changes; the camera itself stays where it is: everything magnifies (or widens) evenly, with **no parallax**.

## Rules
- **ZOOM ≠ DOLLY** (REG-05). One source even defines "Zoom In — camera slowly moves toward subject" (SRC-002 img-shots:363); this DSL does not (research/04 #26).
- **Zoom + dolly:** opposite directions together = dolly zoom (special technique); same direction together = context-dependent (compounded magnification that models tend to collapse into one move, P10-P11).
- **Crash zoom** = one sudden, violent zoom; the world does not move. On H3: "zooms in with large amplitude at fast speed" (SRC-009 shots/crash-zoom-in.md). You cannot place the snap at an exact second on H3; write the order of events.
- **Give a range for control:** `/ZOOMIN:WS>CU`.
- **Chinese:** 变焦推近 / 变焦拉远 (lens) vs 推镜 / 拉镜 (body) (SRC-004 lexicon:378, 384).

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/ZOOMIN` | The focal length increases while the camera body stays put: everything magnifies equally, no parallax. **Rule:** ZOOMIN is not DOLLYIN: the camera does not move. | size_range, percent, magnitude, speed | HIGH | SRC-001, SRC-002, SRC-004, SRC-005, SRC-009, LOCAL-001 | /ZOOM:IN, /LENSZOOMIN, /ZOOMINLENS |
| `/ZOOMOUT` | The focal length decreases while the camera body stays put: the view widens with no parallax. **Rule:** ZOOMOUT is not DOLLYOUT: the camera does not move. | size_range, percent, magnitude, speed | HIGH | SRC-001, SRC-002, SRC-004, SRC-005, SRC-009, LOCAL-001 | /ZOOM:OUT, /LENSZOOMOUT, /ZOOMOUTLENS |
| `/CRASHZOOM` | A sudden, very fast zoom (default IN) that snaps between framings with flat magnification. | dir_io | HIGH | SRC-001, SRC-002, SRC-009 | /SNAPZOOM, /CRASH |

| Command | Image mode | Video mode |
|---|---|---|
| `/ZOOMIN` | Cannot zoom in a still. Render the zoomed framing with flat, compressed perspective. | The camera stays put while the lens zooms in; everything magnifies by the same amount. |
| `/ZOOMOUT` | Cannot zoom in a still. Render the wider framing with the same camera position. | The camera stays put while the lens zooms out; the view widens evenly. |
| `/CRASHZOOM` | Render the landing framing with a slight radial zoom streak only if the user wants the snap visible. | One sudden, violent zoom from the opening framing to the landing framing; the world itself does not move. |
<!-- END GENERATED -->
