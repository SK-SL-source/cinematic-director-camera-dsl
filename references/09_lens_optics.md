# 09 · Lens and optics

Focal length (always 35mm full-frame equivalent, SRC-004 cinlang:10-15) and lens character (macro, fisheye, anamorphic).

## Rules
- **Wide-angle lens ≠ wide shot** (REG-01). `/WIDEANGLE` changes perspective, not framing.
- **Classes** (boundaries overlap on purpose): ULTRAWIDE ≤18mm, WIDE 18-35, NORMAL 35-70, PORTRAIT 70-110, TELE ≥110. A number outside the stated class is a conflict (R03).
- **Perspective comes from distance, not focal length.** A long lens compresses because you stand far away; a wide lens expands because you stand close (SRC-004 cinlang:139-153). Adapters describe the visible result (compressed background, stretched depth), not only the number.
- **Legacy /PORTRAIT** resolves to the portrait lens class only, with a warning about the other two readings (vertical format, posed portrait). It never adds shallow focus or a close-up (research/04 #5).
- **Anamorphic is a lens look** (oval highlights, horizontal flares), not black bars; asking for bars paints them into the image (SRC-004 cinlang:458).
- **H3 note:** lens and body names are nearly cosmetic on H3 — 8mm rendered like 50mm, 75mm slightly tighter (SRC-009 gear.md). The H3 adapter keeps the lens words (intent) and warns; the shot size carries the framing.

<!-- BEGIN GENERATED: commands -->
| Command | Meaning | Args | Confidence | Sources | Aliases |
|---|---|---|---|---|---|
| `/LENS` | A specific focal length in mm (35mm full-frame equivalent). /LENS:35, /LENS50. Sets the lens class it falls in. | mm | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-006 | /FOCAL, /MM |
| `/ULTRAWIDE` | Ultra-wide lens (about 18mm or wider): strongly expanded depth, stretched edges. | - | HIGH | SRC-003, SRC-004 | /ULTRAWIDELENS, /UWA |
| `/WIDEANGLE` | Wide-angle LENS (about 20-28mm): expanded depth, more of the space in view at a given distance. A lens, never a shot size. **Rule:** WIDEANGLE never becomes a wide shot (/WS). | - | HIGH | SRC-001, SRC-003, SRC-004, SRC-006 | /WIDELENS, /WIDEANGLELENS |
| `/NORMAL` | Normal lens (about 40-55mm): perspective close to human vision. | - | HIGH | SRC-001, SRC-003, SRC-004 | /NORMALLENS, /STANDARDLENS |
| `/PORTRAITLENS` | Short telephoto portrait lens (about 85-105mm): flattering face, softly compressed background. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004, SRC-006 | /PORTRAIT |
| `/TELEPHOTO` | Long lens (about 135mm and longer): strongly compressed depth; background planes stack close behind the subject. | - | HIGH | SRC-001, SRC-003, SRC-004 | /TELE, /LONGLENS |
| `/MACRO` | Macro lens: focuses extremely close for large magnification of small details. A lens; the macro 'shot size' is /ECU /MACRO. | - | HIGH | SRC-001, SRC-002, SRC-003, SRC-004 | /MACROLENS |
| `/FISHEYE` | Fisheye lens: extreme wide field with strong barrel distortion (curved straight lines). | - | HIGH | SRC-001, SRC-002 | /FISHEYELENS |
| `/ANAMORPHIC` | Anamorphic lens character: oval out-of-focus highlights and horizontal lens flares. Does not mean black bars (aspect ratio is out of scope). | - | HIGH | SRC-001, SRC-002, SRC-004, SRC-005 | /ANAMORPHICLENS |

| Command | Image mode | Video mode |
|---|---|---|
| `/LENS` | State the focal length and its visible perspective (compressed or expanded depth). | State the focal length; it does not change during the shot unless a zoom is stated. |
| `/ULTRAWIDE` | Ultra-wide perspective: near things huge, far things tiny, edges stretched. | Ultra-wide perspective; any travel toward the camera looks fast. |
| `/WIDEANGLE` | Wide-angle lens perspective: depth feels expanded; the shot size stays whatever was specified. | Wide-angle lens perspective; the shot size stays whatever was specified. |
| `/NORMAL` | Natural, human-like perspective. | Natural, human-like perspective. |
| `/PORTRAITLENS` | Portrait-lens perspective: face rendered naturally, background compressed. | Portrait-lens perspective: face rendered naturally, background compressed. |
| `/TELEPHOTO` | Telephoto compression: the background looks close and large behind the subject. | Telephoto compression; any camera shake is magnified. |
| `/MACRO` | Macro magnification of a small detail; the focus plane is razor thin. | Macro magnification of a small detail. |
| `/FISHEYE` | Fisheye distortion: straight lines bow outward, the frame looks rounded. | Fisheye distortion for the whole shot. |
| `/ANAMORPHIC` | Oval out-of-focus highlights and horizontal flares; no painted black bars. | Oval out-of-focus highlights and horizontal flares; no painted black bars. |
<!-- END GENERATED -->
