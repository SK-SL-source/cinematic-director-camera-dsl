# Tests · MiniMax H3 mode wrappers

> `scripts/h3_wrappers.py` places the ONE H3 camera core into the official prompt structures (PROJECT_GOAL.md). Every row builds the
> prompt for the mode with the wrapper's neutral sample content and checks the structure (`wrap[mode]~regex`, `nowrap[mode]~regex`;
> the structural self-check of the wrapper must also pass). The camera sentence must appear verbatim in every mode: no mode has its own
> camera language.

## Base modes (SRC-008 base-en 2.1-2.2)

| ID | Input | Expect | Source |
|---|---|---|---|
| WRAP-T2VA-01 | `/MS /PAN:R` | wrap[t2va]~^integrated_multimodal_description: \[Shot 1\]; nowrap[t2va]~fully referenced; nowrap[t2va]~<Picture; wrap[t2va]~overall_soundscape:.*non_diegetic_music: | T2VA: no alignment line, no pictures, three fields |
| WRAP-I2VA-01 | `/MS /PAN:R` | wrap[i2va]~^For the target video, at 0\.00 seconds into the target video, <Picture 1> \(from \[Shot 1\]\) is fully referenced\.\n\nintegrated_multimodal_description: \[Shot 1\] | I2VA alignment line verbatim, blank line, then the fields |
| WRAP-FL2VA-01 | `/MS /PAN:R` | wrap[fl2va]~^How the reference pictures align with the target video — Picture 1 \(from Shot 1\) aligns with the 0\.00-second mark of the target video. Picture 2 \(from Shot 1\) aligns with the 5\.17-second mark of the target video\. | FL2VA alignment line with the duration to two decimals |
| WRAP-L2VA-01 | `/MS /PAN:R` | wrap[l2va]~^How the reference pictures align with the target video — <Picture 1> \(from \[Shot 1\]\) aligns with the 5\.17-second mark of the target video\. | L2VA alignment line |
| WRAP-BASE-02 | `/MS /PAN:R` | nowrap[i2va]~subject_definitions; nowrap[i2va]~retention_analysis; nowrap[fl2va]~detailed_description | Base modes never carry Full-reference fields |
| WRAP-BASE-03 | `/MS /DOLLYIN:MS>MCU:SLOW` | wrap[i2va]~The camera pushes in at slow speed\.; wrap[t2va]~The camera pushes in at slow speed\.; wrap[l2va]~The final frame is a medium close-up | the same camera core in every Base mode |
| WRAP-BASE-04 | `/MS /PAN:R` | wrap[i2va]~\[Shot 1\] .*<Picture 1>.*The camera pans right\. The camera stays in place\. She stands still | opening anchor, then the camera core, then the action |
| WRAP-BASE-05 | `/MFS /TRACKSIDE:R` | wrap[i2va]~\. (?-i:The) young woman shown in <Picture 1> stays about the same size while the background slides past behind\.; nowrap[i2va]~\. (?-i:the) young woman shown in <Picture 1> stays; wrap[t2va]~\. (?-i:The) young woman stays about the same size; wrap[i2va]~The camera travels beside the young woman shown in <Picture 1> in a tracking shot | a subject name that opens a sentence starts with a capital; inside a sentence it is unchanged (CL-037) |

## Full-reference mode (SRC-008 ref-en)

| ID | Input | Expect | Source |
|---|---|---|---|
| WRAP-REF-01 | `/MS /PAN:R` | wrap[ref2va]~^subject_definitions:\n.*\n\nsummary:\n\[reference generation\] .*\n\nretention_analysis:\n.*\n\ndetailed_description:\n.*\n\noverall_soundscape:\n.*\n\nnon_diegetic_music:\n | the six fields in the official order |
| WRAP-REF-02 | `/MS /PAN:R` | wrap[ref2va]~\[Shot 1\] <Subject 1> stands in a stone courtyard\. A medium shot frames <Subject 1> from the waist up\. The camera pans right\. The camera stays in place\.; nowrap[ref2va]~fully referenced | <Subject N> labels; no Base alignment line |
| WRAP-REF-03 | `/MS /DOLLYIN:MS>MCU:SLOW` | wrap[ref2va]~The camera pushes in at slow speed\. The push continues steadily over the whole video\. The final frame is a medium close-up of <Subject 1> from the chest up\. The focal length stays the same\. | the same four-layer core as the Base modes |
| WRAP-REF-04 | `S1: /MS /PAN:R\nS2: /CU /STATIC` | wrap[ref2va]~\[Shot 1\] .*\n\[Shot 2\] .*Static Shot | one [Shot N] line per DSL shot (the H3 cut warning still applies) |
| WRAP-REF-05 | `/MFS /TRACKSIDE:R` | wrap[ref2va]~\. <Subject 1> stays about the same size while the background slides past behind\. | the official label is not altered (CL-037) |
