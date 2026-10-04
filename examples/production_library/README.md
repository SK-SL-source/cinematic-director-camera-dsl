# Production Example Library

This library maps natural-language filmmaking situations to candidate Camera DSL. It is an example/retrieval layer, not a new camera-language authority.

這個案例庫負責把自然語言／敘事情境對應到候選 Camera DSL。它不是新的 Camera 語義來源，也不會擴充 canonical commands。

People rarely say `/DOLLYIN:SLOW`. They say 慢推近, 仰拍英雄, 遮擋轉場 or 拉出. This library holds 66 such situations and returns the camera commands each one means:

| Batch | Examples | What they are |
|---|---|---|
| [Narrative examples](narrative_30.md) | 30 | story situations, with effects, editing and time effects kept apart from the camera |
| [Technique examples](technique_36.md) | 36 | everyday camera phrases, one technique each |

## Use

```bash
python scripts/example_library.py search "仰拍英雄"
python scripts/example_library.py search "拉出"
python scripts/example_library.py resolve EX-028 --choose 1
```

A clear phrase returns its DSL (real output, shortened):

```text
query: 仰拍英雄
example_id: EX-055
mapping_class: COMPOSITE
candidate_dsl:
  - /LOWANGLE /MFS
needs_context: false
alternatives:
  - /WORMSEYE /FS   # 更極端的地面仰視
```

A phrase that leaves the camera open returns every candidate and a question, never a guess (real output, shortened):

```text
query: 拉出
example_id: EX-028
mapping_class: AMBIGUOUS
candidate_dsl:
  - /DOLLYOUT:ECU>MS   # 攝影機本體往後退
  - /ZOOMOUT:ECU>MS   # 攝影機不動，只把焦距拉遠
needs_context: true
question_zh: 攝影機本體要向後移動，還是只改變焦距？
```

Search accepts Traditional or Simplified Chinese and English command names. From Python:

```python
import example_library as lib                   # scripts/ on the path
hits = lib.search_examples("环绕升镜", top_k=5)  # ranked matches, ties broken by id
res = lib.resolve_example("EX-051")             # candidate DSL, checks, non-camera layers
```

## Rules

- **The registry stays the authority.** Every command in the library comes from `registry/canonical_commands.yaml`, and every candidate is checked again by the parser and the conflict rules before it is returned.
- **A situation name is not a command.** 慢推近, 仰拍英雄, 移鏡 and the rest are labels for search. None of them is a canonical command, and none is added to the aliases.
- **Open questions stay open.** `CONTEXT_REQUIRED`, `AMBIGUOUS` and `CAMERA_PLUS_EDITING` examples return all their candidates with a question; a default candidate is only marked, never chosen silently.
- **Effects are not camera moves.** Slow motion, freeze time, flashbacks, dissolves, dream distortion, transformations, lighting and colour stay in `non_camera`. An example with no camera instruction returns no camera DSL.

| Mapping class | Meaning |
|---|---|
| DIRECT | one candidate states the whole camera intent |
| COMPOSITE | several commands together state it |
| CONTEXT_REQUIRED | the phrase leaves out what decides between candidates; the resolver asks |
| AMBIGUOUS | two or more readings and no default; the resolver asks |
| DIRECT_PLUS_FX | a camera intent plus visual effects outside the camera |
| CAMERA_PLUS_TEMPORAL | a camera move plus a time effect |
| CAMERA_STATE_PLUS_TEMPORAL | a camera position with no move, plus a time effect |
| NON_CAMERA | no camera instruction; nothing is added |
| NON_CAMERA_EDITING | an editing device; camera only where the situation states it |
| NON_CAMERA_FX | a visual effect; no camera move is implied |
| MULTI_SHOT | several shots with continuity between them |
| CAMERA_PLUS_EDITING | a camera element plus an editing device; the move depends on the scene |

Files: `production_examples.yaml` holds the data, `schema.yaml` its fields. The two lists above are generated from the data with `python scripts/example_library.py docs`. `tests/test_example_library.py` checks the library on every test run.

## 中文說明

大家很少直接說 `/DOLLYIN:SLOW`，比較常說「慢推近」「仰拍英雄」「遮擋轉場」「拉出」。這個案例庫收了 66 個這類情境，查得到每個說法對應的運鏡指令。

- **用法**：`python scripts/example_library.py search "仰拍英雄"`。繁體、簡體都可以查。
- **說法清楚**：直接回傳候選 DSL。
- **說法不清楚**：例如「拉出」可能是推軌後退，也可能是變焦。這時會回傳所有候選，再附上一個要先問清楚的問題，不會用猜的。
- **案例名稱不是指令**：「慢推近」「移鏡」這些只是查詢用的說法，不會變成指令，也不會加進別名。
- **特效不是運鏡**：慢動作、時間凝滯、閃回、疊化、夢境扭曲、變身、光線和色調，都另外放在 `non_camera`。原本沒寫運鏡的情境，不會自己補。
- **每個候選都驗證過**：回傳前都會再經過解析器和衝突檢查。
