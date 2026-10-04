# 15 · Aliases

Every alias resolves to exactly one canonical command (or is declared out of scope). The home of this table is `registry/aliases.yaml`; this page is generated from it.

## How aliases behave
- **Legacy 20** (spec section 15) all still work. Ten are canonical names (`/DRONEVIEW`, `/TOPDOWN`, `/BIRDSEYE`, `/LOWANGLE`, `/HIGHANGLE`, `/GROUNDLEVEL`, `/EYELEVEL`, `/WIDEANGLE`, `/ORBIT`, `/CINEMATIC`); ten are aliases (below).
- **Parameter aliases** fix an argument: `/PANLEFT` = `/PAN:L`, `/ORBIT360` = `/ORBIT:FULL`.
- **Argument-dependent aliases** need their argument: `/DOLLY:IN` = `/DOLLYIN`, `/DOLLY:L` = `/TRUCK:L` (Higgsfield/fal naming), `/ZOOM:OUT` = `/ZOOMOUT`. A bare `/DOLLY` is an error.
- **Ambiguous legacy words resolve to the camera reading and warn:** `/PORTRAIT`, `/WIDE`, `/LS`, `/MLS`, `/DRONESHOT`.
- **Out-of-scope words** are recognised and explained, never silently ignored (director names, time effects, subject rotation, aspect ratio).
- Case does not matter (`/pushin` = `/PUSHIN`). Compact lens forms: `/LENS50`, `/35MM`.
- In Claude Code, a message that **starts** with `/XXX` is read as a slash command. Invoke the skill first (`/cinematic-director-camera-dsl /MS /LOWANGLE`) or put the DSL after some text.

<!-- BEGIN GENERATED: table -->
| Alias | Resolves to | Relationship | Note |
|---|---|---|---|
| `/180` | `/AXIS` | abbreviation |  |
| `/180RULE` | `/AXIS` | semantic_alias |  |
| `/2SHOT` | `/TWOSHOT` | abbreviation |  |
| `/3Q` | `/THREEQUARTER` | abbreviation |  |
| `/3SHOT` | `/THREESHOT` | abbreviation |  |
| `/ABOVEEYE` | `/ELEVATED` | semantic_alias |  |
| `/AERIALPULLBACK` | `/DRONEREVEAL:BACK` | parameter_alias | SRC-009 shots/aerial-pullback.md. |
| `/AERIALREVEAL` | `/DRONEREVEAL` | semantic_alias |  |
| `/AERIALVIEW` | `/AERIAL` | semantic_alias |  |
| `/ALLSHARP` | `/DEEPFOCUS` | semantic_alias |  |
| `/AMERICANSHOT` | `/COWBOY` | semantic_alias |  |
| `/ANAMORPHICLENS` | `/ANAMORPHIC` | semantic_alias |  |
| `/ANKLE` | `/ANKLELEVEL` | abbreviation |  |
| `/ARC` | `/ORBIT:PARTIAL` | semantic_alias | Arc = partial orbit (SRC-002 camera:63-64). |
| `/ARCSHOT` | `/ORBIT:PARTIAL` | semantic_alias |  |
| `/AXIS180` | `/AXIS` | semantic_alias |  |
| `/BACKTRACK` | `/LEAD` | semantic_alias |  |
| `/BACKVIEW` | `/REAR` | semantic_alias |  |
| `/BARRELROLL` | `/ROLL:CW:360` | parameter_alias |  |
| `/BCU` | `/ECU` | abbreviation | British 'big close-up'. |
| `/BIRDS` | `/BIRDSEYE` | abbreviation |  |
| `/BIRDSEYEVIEW` | `/BIRDSEYE` | semantic_alias |  |
| `/BOKEH` | `/SHALLOW` | semantic_alias | 'Bokeh' alone tends to add round highlight balls; the adapters describe what is sharp and what dissolves instead (SRC-004 cinlang:222-235). |
| `/BOOM` | `/CRANE` | rig_variant_alias |  |
| `/BOOMDOWN` | `/CRANE:DOWN` | rig_variant_alias |  |
| `/BOOMUP` | `/CRANE:UP` | rig_variant_alias |  |
| `/BRIDGE` | `/CUTAWAY` | semantic_alias |  |
| `/CANTED` | `/DUTCH` | semantic_alias |  |
| `/CANTEDANGLE` | `/DUTCH` | semantic_alias |  |
| `/CENTERED` | `/CENTER` | spelling_variant |  |
| `/CENTRE` | `/CENTER` | spelling_variant |  |
| `/CENTRED` | `/CENTER` | spelling_variant |  |
| `/CHEST` | `/CHESTLEVEL` | abbreviation |  |
| `/CIRCLE` | `/ORBIT` | semantic_alias |  |
| `/CLEANSINGLE` | `/SINGLE` | semantic_alias |  |
| `/CLOSE` | `/CU` | abbreviation |  |
| `/CLOSEUP` | `/CU` | legacy |  |
| `/CONTRAZOOM` | `/DOLLYZOOM` | semantic_alias |  |
| `/COWBOYSHOT` | `/COWBOY` | semantic_alias |  |
| `/CRAB` | `/TRUCK` | semantic_alias |  |
| `/CRANEDOWN` | `/CRANE:DOWN` | parameter_alias |  |
| `/CRANEUP` | `/CRANE:UP` | parameter_alias |  |
| `/CRASH` | `/CRASHZOOM` | abbreviation |  |
| `/CROSS` | `/CROSSAXIS` | abbreviation |  |
| `/CROSSLINE` | `/CROSSAXIS` | semantic_alias |  |
| `/CUTAWAYSHOT` | `/CUTAWAY` | semantic_alias |  |
| `/CUTONACTION` | `/MATCHACTION` | semantic_alias |  |
| `/DEEP` | `/DEEPFOCUS` | abbreviation |  |
| `/DEEPDOF` | `/DEEPFOCUS` | semantic_alias |  |
| `/DEPTHSTAGING` | `/DEEPSTAGING` | semantic_alias |  |
| `/DETAIL` | `/INSERT` | semantic_alias |  |
| `/DIOPTER` | `/SPLITDIOPTER` | abbreviation |  |
| `/DIRECTION` | `/SCREEN` | abbreviation |  |
| `/DIRTYSINGLE` | `/DIRTYOTS` | semantic_alias |  |
| `/DOLLY` | `:IN` → `/DOLLYIN`; `:OUT` → `/DOLLYOUT`; `:FWD` → `/DOLLYIN`; `:BACK` → `/DOLLYOUT`; `:L` → `/TRUCK:L`; `:R` → `/TRUCK:R` | arg_dependent |  |
| `/DOLLYBACK` | `/DOLLYOUT` | semantic_alias |  |
| `/DOLLYFORWARD` | `/DOLLYIN` | semantic_alias |  |
| `/DOWNSHOT` | `/HIGHANGLE` | semantic_alias |  |
| `/DRONESHOT` | `/DRONEVIEW` | legacy_ambiguous | 'Drone shot' is read as the drone VIEWPOINT. For drone movement add /FLYOVER or /DRONEREVEAL. |
| `/DUTCHANGLE` | `/DUTCH` | semantic_alias |  |
| `/DUTCHTILT` | `/DUTCH` | legacy | A roll offset, not a TILT (research 04 #20). |
| `/ELS` | `/EWS` | abbreviation |  |
| `/EMPTYSPACE` | `/NEGSPACE` | semantic_alias |  |
| `/ENSEMBLE` | `/GROUPSHOT` | semantic_alias |  |
| `/EXTREMECLOSEUP` | `/ECU` | semantic_alias |  |
| `/EXTREMELONGSHOT` | `/EWS` | semantic_alias |  |
| `/EXTREMEWIDE` | `/EWS` | semantic_alias |  |
| `/EYE` | `/EYELEVEL` | abbreviation |  |
| `/FACING` | `/FRONTAL` | semantic_alias |  |
| `/FGOBSTRUCTION` | `/FGLAYER` | semantic_alias |  |
| `/FILMIC` | `/CINEMATIC` | semantic_alias |  |
| `/FIRSTPERSON` | `/POV` | semantic_alias |  |
| `/FISHEYELENS` | `/FISHEYE` | semantic_alias |  |
| `/FIXED` | `/STATIC` | semantic_alias |  |
| `/FLATLAY` | `/TOPDOWN` | semantic_alias |  |
| `/FLOATING` | `/STEADICAM` | semantic_alias |  |
| `/FLOOR` | `/GROUNDLEVEL` | abbreviation |  |
| `/FLOORLEVEL` | `/GROUNDLEVEL` | semantic_alias |  |
| `/FLYTHRU` | `/FLYTHROUGH` | spelling_variant |  |
| `/FOCAL` | `/LENS` | semantic_alias |  |
| `/FOCUSBG` | `/BGFOCUS` | spelling_variant |  |
| `/FOCUSFG` | `/FGFOCUS` | spelling_variant |  |
| `/FOCUSMG` | `/MGFOCUS` | spelling_variant |  |
| `/FOCUSPULL` | `/RACKFOCUS:SLOW` | semantic_alias |  |
| `/FOLLOWBEHIND` | `/FOLLOW` | semantic_alias |  |
| `/FOLLOWING` | `/FOLLOW` | semantic_alias |  |
| `/FOLLOWSHOT` | `/TRACK` | semantic_alias |  |
| `/FOREFOCUS` | `/FGFOCUS` | semantic_alias |  |
| `/FOREGROUND` | `/FGLAYER` | semantic_alias | Composition layer. For focus on the foreground use /FGFOCUS. |
| `/FPVDRONE` | `/FPV` | semantic_alias |  |
| `/FRAMED` | `/FRAMEINFRAME` | semantic_alias |  |
| `/FRAMEWITHINFRAME` | `/FRAMEINFRAME` | semantic_alias |  |
| `/FROMBEHIND` | `/REAR` | semantic_alias |  |
| `/FRONT` | `/FRONTAL` | abbreviation |  |
| `/FULLBODY` | `/FS` | legacy |  |
| `/FULLSHOT` | `/FS` | semantic_alias |  |
| `/GAZE` | `/EYELINE` | semantic_alias |  |
| `/GODSEYE` | `/TOPDOWN` | semantic_alias |  |
| `/GRAPHICMATCH` | `/MATCHCUT:SHAPE` | parameter_alias |  |
| `/GROUND` | `/GROUNDLEVEL` | abbreviation |  |
| `/GROUP` | `/GROUPSHOT` | abbreviation |  |
| `/HANDHELDFOLLOW` | `/HANDHELD` + `/FOLLOW` | composite |  |
| `/HEADSPACE` | `/HEADROOM` | semantic_alias |  |
| `/HEROANGLE` | `/LOWANGLE` | semantic_alias |  |
| `/HIGH` | `/HIGHANGLE` | abbreviation |  |
| `/HIP` | `/HIPLEVEL` | abbreviation |  |
| `/INSERTSHOT` | `/INSERT` | semantic_alias |  |
| `/JIB` | `/CRANE` | rig_variant_alias |  |
| `/JIBDOWN` | `/CRANE:DOWN` | rig_variant_alias |  |
| `/JIBUP` | `/CRANE:UP` | rig_variant_alias |  |
| `/KNEE` | `/KNEELEVEL` | abbreviation |  |
| `/LATERAL` | `/TRUCK` | semantic_alias |  |
| `/LAYERS` | `/DEEPSTAGING` | semantic_alias |  |
| `/LEADING` | `/LEAD` | semantic_alias |  |
| `/LEADINGLINES` | `/LEADLINES` | semantic_alias |  |
| `/LEADINGSHOT` | `/LEAD` | semantic_alias |  |
| `/LEADROOM` | `/LOOKROOM` | semantic_alias |  |
| `/LENSZOOMIN` | `/ZOOMIN` | semantic_alias |  |
| `/LENSZOOMOUT` | `/ZOOMOUT` | semantic_alias |  |
| `/LEVEL` | `/EYELEVEL` | abbreviation |  |
| `/LINE` | `/AXIS` | abbreviation |  |
| `/LOCKED` | `/STATIC` | semantic_alias |  |
| `/LOCKEDOFF` | `/STATIC` | semantic_alias |  |
| `/LONGLENS` | `/TELEPHOTO` | semantic_alias |  |
| `/LONGSHOT` | `/WS` | legacy_ambiguous | LONG SHOT is read as a wide shot; some people use it for a full shot (/FS). Research 04 #3. |
| `/LOOK` | `/EYELINE` | abbreviation |  |
| `/LOOKATCAMERA` | `/EYELINE:X>CAM` | parameter_alias |  |
| `/LOOKCAM` | `/EYELINE:X>CAM` | parameter_alias | The subject looks into the lens. Not POV (REG-02). |
| `/LOOKSPACE` | `/LOOKROOM` | semantic_alias |  |
| `/LOW` | `/LOWANGLE` | abbreviation |  |
| `/LS` | `/WS` | legacy_ambiguous | LONG SHOT is read as a wide shot; some people use it for a full shot (/FS). Research 04 #3. |
| `/MACROLENS` | `/MACRO` | semantic_alias |  |
| `/MATCHONACTION` | `/MATCHACTION` | semantic_alias |  |
| `/MEDIUM` | `/MS` | semantic_alias |  |
| `/MEDIUMCLOSEUP` | `/MCU` | semantic_alias |  |
| `/MEDIUMFULL` | `/MFS` | semantic_alias |  |
| `/MEDIUMSHOT` | `/MS` | legacy |  |
| `/MEDIUMWIDE` | `/MFS` | semantic_alias |  |
| `/MID` | `/MS` | abbreviation |  |
| `/MLS` | `/MFS` | legacy_ambiguous | MLS means knees-up here; one source uses it for mid-thigh (/COWBOY). Research 04 section 2. |
| `/MM` | `/LENS` | abbreviation |  |
| `/MOVIELOOK` | `/CINEMATIC` | semantic_alias |  |
| `/MWS` | `/MFS` | abbreviation |  |
| `/NEGATIVESPACE` | `/NEGSPACE` | semantic_alias |  |
| `/NEUTRALANGLE` | `/EYELEVEL` | semantic_alias |  |
| `/NORMALLENS` | `/NORMAL` | semantic_alias |  |
| `/NOSEROOM` | `/LOOKROOM` | semantic_alias |  |
| `/OBLIQUE` | `/DUTCH:L:8` | semantic_alias | SRC-001: an oblique angle is a lighter Dutch tilt. |
| `/ORBIT360` | `/ORBIT:FULL` | parameter_alias |  |
| `/OVERFLIGHT` | `/FLYOVER` | semantic_alias |  |
| `/OVERHEAD` | `/TOPDOWN` | legacy | Most sources use overhead = straight down; some list it as a height (research 04 #7). |
| `/OVERSHOULDER` | `/OTS` | semantic_alias |  |
| `/OVERTHESHOULDER` | `/OTS` | semantic_alias |  |
| `/PANL` | `/PAN:L` | parameter_alias |  |
| `/PANLEFT` | `/PAN:L` | parameter_alias |  |
| `/PANR` | `/PAN:R` | parameter_alias |  |
| `/PANRIGHT` | `/PAN:R` | parameter_alias |  |
| `/PARALLEL` | `/TRACKSIDE` | semantic_alias |  |
| `/PASSTHROUGH` | `/FLYTHROUGH` | semantic_alias |  |
| `/PEDDOWN` | `/PEDESTAL:DOWN` | parameter_alias |  |
| `/PEDESTALDOWN` | `/PEDESTAL:DOWN` | parameter_alias |  |
| `/PEDESTALUP` | `/PEDESTAL:UP` | parameter_alias |  |
| `/PEDUP` | `/PEDESTAL:UP` | parameter_alias |  |
| `/PORTRAIT` | `/PORTRAITLENS` | legacy_ambiguous | PORTRAIT has three readings: portrait LENS (~85mm, used here), vertical 9:16 FORMAT (aspect ratio is out of scope in v1), or a POSED portrait framing (use /CU or /MCU). Only the lens class is set; no shallow focus or close-up is added. |
| `/PULL` | `/DOLLYOUT` | semantic_alias |  |
| `/PULLBACK` | `/DOLLYOUT` | semantic_alias |  |
| `/PULLFOCUS` | `/RACKFOCUS:SLOW` | semantic_alias | SRC-005: pull focus = the same shift, slower than a rack. |
| `/PULLOUT` | `/DOLLYOUT` | legacy |  |
| `/PUSH` | `/DOLLYIN` | semantic_alias |  |
| `/PUSHIN` | `/DOLLYIN` | legacy | A physical move, never a zoom (research 04 #11). |
| `/RACINGDRONE` | `/FPV` | semantic_alias |  |
| `/RACK` | `/RACKFOCUS` | abbreviation |  |
| `/RAIL` | `/SLIDER` | semantic_alias |  |
| `/RAISED` | `/ELEVATED` | semantic_alias |  |
| `/REACT` | `/REACTION` | abbreviation |  |
| `/REACTIONSHOT` | `/REACTION` | semantic_alias |  |
| `/REPOUSSOIR` | `/FGLAYER` | semantic_alias |  |
| `/REVERSE` | `/SRS` | abbreviation |  |
| `/REVERSESHOT` | `/SRS` | semantic_alias |  |
| `/ROLLCCW` | `/ROLL:CCW` | parameter_alias |  |
| `/ROLLCW` | `/ROLL:CW` | parameter_alias |  |
| `/RULEOFTHIRDS` | `/THIRDS` | semantic_alias |  |
| `/SCREENDIRECTION` | `/SCREEN` | semantic_alias |  |
| `/SHAKY` | `/HANDHELD:STRONG` | parameter_alias |  |
| `/SHAKYCAM` | `/HANDHELD:STRONG` | parameter_alias |  |
| `/SHALLOWDOF` | `/SHALLOW` | semantic_alias |  |
| `/SHALLOWFOCUS` | `/SHALLOW` | semantic_alias |  |
| `/SHOTREVERSESHOT` | `/SRS` | semantic_alias |  |
| `/SHOULDERHEIGHT` | `/SHOULDERLEVEL` | semantic_alias |  |
| `/SHOULDERMOUNT` | `/SHOULDER` | semantic_alias |  |
| `/SHOULDERRIG` | `/SHOULDER` | semantic_alias |  |
| `/SIDE` | `/PROFILE` | abbreviation |  |
| `/SIDEPROFILE` | `/PROFILE` | semantic_alias |  |
| `/SIDETRACK` | `/TRACKSIDE` | semantic_alias |  |
| `/SIDETRACKING` | `/TRACKSIDE` | semantic_alias |  |
| `/SINGLESHOT` | `/SINGLE` | semantic_alias |  |
| `/SLIDE` | `/TRUCK` | semantic_alias | The movement. The rig is /SLIDER (research 04 #18). |
| `/SNAPZOOM` | `/CRASHZOOM` | semantic_alias |  |
| `/SPLITFOCUS` | `/SPLITDIOPTER` | semantic_alias |  |
| `/STABILISED` | `/GIMBAL` | spelling_variant |  |
| `/STABILIZED` | `/GIMBAL` | spelling_variant |  |
| `/STABILIZER` | `/GIMBAL` | semantic_alias |  |
| `/STANDARDLENS` | `/NORMAL` | semantic_alias |  |
| `/STEADI` | `/STEADICAM` | abbreviation |  |
| `/STICKS` | `/TRIPOD` | semantic_alias |  |
| `/STILL` | `/STATIC` | semantic_alias |  |
| `/SUBJECTIVE` | `/POV` | semantic_alias |  |
| `/SUPERDOLLY` | `/DOLLYIN:LARGE:FAST` | parameter_alias | Higgsfield preset name (SRC-002); measured on H3 as Push In + large + fast (SRC-009 shots/super-dolly-in.md). |
| `/SWISH` | `/WHIPPAN` | abbreviation |  |
| `/SWISHPAN` | `/WHIPPAN` | semantic_alias |  |
| `/SYMMETRIC` | `/SYMMETRY` | spelling_variant |  |
| `/SYMMETRICAL` | `/SYMMETRY` | spelling_variant |  |
| `/TELE` | `/TELEPHOTO` | abbreviation |  |
| `/THIRD` | `/THIRDS` | spelling_variant |  |
| `/THREEQUARTERS` | `/THREEQUARTER` | spelling_variant |  |
| `/THROUGH` | `/FLYTHROUGH` | abbreviation |  |
| `/TILTDOWN` | `/TILT:DOWN` | parameter_alias |  |
| `/TILTUP` | `/TILT:UP` | parameter_alias |  |
| `/TOPSHOT` | `/TOPDOWN` | semantic_alias |  |
| `/TRACKING` | `/TRACK` | legacy | Generic tracking. For a side-by-side tracking shot use /TRACKSIDE (research 04 #16). |
| `/TRACKINGSHOT` | `/TRACK` | semantic_alias |  |
| `/TRUCKLEFT` | `/TRUCK:L` | parameter_alias |  |
| `/TRUCKRIGHT` | `/TRUCK:R` | parameter_alias |  |
| `/UAV` | `/DRONE` | semantic_alias |  |
| `/ULTRAWIDELENS` | `/ULTRAWIDE` | semantic_alias |  |
| `/UPSHOT` | `/LOWANGLE` | semantic_alias |  |
| `/UWA` | `/ULTRAWIDE` | abbreviation |  |
| `/VERTIGO` | `/DOLLYZOOM` | semantic_alias |  |
| `/WAIST` | `/HIPLEVEL` | abbreviation |  |
| `/WAISTLEVEL` | `/HIPLEVEL` | semantic_alias |  |
| `/WHIP` | `/WHIPPAN` | abbreviation |  |
| `/WIDE` | `/WS` | legacy_ambiguous | WIDE is read as a wide SHOT. For a wide-angle LENS use /WIDEANGLE (REG-01). |
| `/WIDEANGLELENS` | `/WIDEANGLE` | semantic_alias |  |
| `/WIDELENS` | `/WIDEANGLE` | semantic_alias |  |
| `/WIDESHOT` | `/WS` | semantic_alias |  |
| `/WORMS` | `/WORMSEYE` | abbreviation |  |
| `/WORMSEYEVIEW` | `/WORMSEYE` | semantic_alias |  |
| `/WORMSVIEW` | `/WORMSEYE` | legacy |  |
| `/XCU` | `/ECU` | abbreviation |  |
| `/XWS` | `/EWS` | abbreviation |  |
| `/ZOLLY` | `/DOLLYZOOM` | semantic_alias |  |
| `/ZOOM` | `:IN` → `/ZOOMIN`; `:OUT` → `/ZOOMOUT` | arg_dependent |  |
| `/ZOOMINLENS` | `/ZOOMIN` | semantic_alias |  |
| `/ZOOMOUTLENS` | `/ZOOMOUT` | semantic_alias |  |

| Word | Why it is not a camera command |
|---|---|
| `/ASPECT` | Aspect ratio is out of scope in v1 (set it in the model, not in camera text; SRC-004 cinlang:442-460). |
| `/BUCKLEUP` | Higgsfield platform preset. |
| `/BULLETTIME` | Time-freeze effect plus camera sweep; not a single camera parameter. Measured as not achievable on H3 (SRC-009 shots/bullet-time.md). |
| `/CARGRIP` | Vehicle rig preset (single source). |
| `/HEADTRACKING` | Higgsfield platform preset. |
| `/HITCHCOCK` | Director names are not camera commands. For the Vertigo effect use /DOLLYZOOM. |
| `/HYPERLAPSE` | Playback speed / time manipulation is out of scope in v1. |
| `/KUBRICK` | Director names are not camera commands (spec section 1-G). |
| `/LAZYSUSAN` | Subject on a turntable = subject rotation, not a camera move (REG-06). |
| `/LETTERBOX` | Aspect ratio is out of scope; asking for bars paints them into the image (SRC-004 cinlang:458). |
| `/LEVITATION` | Higgsfield platform preset. |
| `/LOWSHUTTER` | Shutter / motion-blur setting, not camera placement. |
| `/MOUTHIN` | Higgsfield platform preset (surreal transition). |
| `/NOLAN` | Director names are not camera commands (spec section 1-G). |
| `/ONESHOT` | Ambiguous: a single-person shot (/SINGLE) or a one-take oner. Say which. |
| `/ROBOARM` | Higgsfield platform preset. |
| `/SCOPE` | 'Scope' usually means a 2.39:1 aspect ratio (out of scope). For the lens look use /ANAMORPHIC. |
| `/SELFIE` | Composite of height + angle + rig + eyeline; write the parts (e.g. /HIGHANGLE /HANDHELD /EYELINE:A>CAM). |
| `/SLOWMO` | Playback speed is out of scope in v1. |
| `/SNORRICAM` | Body-mounted rig; single-source platform preset. Measured on H3 only as a described result, never by naming the rig (SRC-009). |
| `/SPEEDRAMP` | Playback speed is out of scope in v1. |
| `/SPIELBERG` | Director names are not camera commands (spec section 1-G). Write the camera parameters instead. |
| `/SPIN` | Ambiguous subject spin. Use /ORBIT (camera circles) or /ROLL (camera rolls). |
| `/TARANTINO` | Director names are not camera commands (spec section 1-G). |
| `/TIMELAPSE` | Playback speed is out of scope in v1. |
| `/TURNTABLE` | Subject rotation, not a camera move. Use /ORBIT if the camera should circle (REG-06). |
<!-- END GENERATED -->
