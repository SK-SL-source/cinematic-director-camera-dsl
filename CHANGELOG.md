# CHANGELOG · cinematic-director-camera-dsl

從 V2_BASELINE（2026-09-30，見 `BASELINE_V2.md`）起，每一次修改都記一筆，**最新的放最上面**。

稽核（`python scripts/audit.py` 的 BASELINE 項）會檢查兩件事：
- 每一筆的欄位是否齊全。
- 所有跟基準不同的檔案，是否都列在某一筆的「檔案」裡。

## 規則

- 不新增 Camera Command、不新增 Alias，稽核會直接擋。
- DSL Grammar 只有發現明確 bug 才改。要增減文法規則時，加一行 `- 文法變更：+規則ID` 或 `-規則ID`。
- 「檔案」要列出這次動到的每一個檔，包括 `audit.py --sync` 重新產生的 `examples/*.md`、`references/*.md` 表格、`schemas/examples.yaml`。
- 值寫不下一行時，下一行縮排續寫。

## 格式（複製這段，編號遞增）

```text
## CL-NNN · YYYY-MM-DD · 一句話標題

- 原因：
- 修改前：
- 修改後：
- 影響 Command：（沒有就寫「無」）
- 影響 Adapter：（沒有就寫「無」）
- 影響 Test：（新增／修改的測試 ID；沒有就寫「無」）
- 是否破壞 backward compatibility：否／是（是的話：哪些舊輸入的結果會變）
- 檔案：scripts/adapters.py, tests/regression.md
```

---

## Release v1.0.0 · 2026-10-04 · first public release

- Camera DSL (104 canonical commands, 244 aliases, 18 grammar rules, frozen as V2_BASELINE) compiled into one Canonical Camera IR, with
    conflict, compatibility and continuity checks.
- One shared H3 Camera Core in four labelled layers (the official H3 motion vocabulary plus project-defined clarifiers, each with its source)
    and five H3 mode wrappers (T2VA, I2VA, FL2VA, L2VA, Ref2VA) that only place the core text into each official prompt structure.
- Adapters for Kling, Veo, FLUX, Qwen-Image, Qwen-Image-Edit and generic image / video models; the camera never changes between models.
- Context-aware H3 production routing: exact-scope reliability (mode, generation profile, command, direction, start and end framing, angle,
    evidence type); outside a measured scope the answer is UNVERIFIED and no grade is borrowed.
- H3 Camera Production Evidence of two types: CONSTRAINED_PRODUCTION (the I2VA production baseline, the multi-mode production baseline and
    the 42-cell Ref2VA matrix, kept as history) and CAMERA_ONLY (the free camera baseline). h3_production_baseline_status COMPLETE;
    h3_full_command_space_validation PARTIAL by design.
- Public release audit: license and source register, private paths and names, secrets, binaries, every regression test and the frozen H3
    camera-text snapshot in one release gate.
- Production Example Library: 66 everyday camera phrases and story situations mapped to candidate DSL; a phrase that leaves the
    camera open comes back with its candidates and a question, and effects, editing and time effects stay out of the camera.
- SOURCES.md lists every project studied as a reference; the maintainer's research notes and raw H3 test records are not part of
    the repository.
- The entries below (CL-001 to CL-057, in Chinese) record every change since V2_BASELINE.

## CL-057 · 2026-10-04 · Production Example Library：66 個常見說法與敘事情境對應到候選 DSL

- 原因：維護者的 CC_PRODUCTION_EXAMPLE_LIBRARY_BUILD_SPEC：使用者常說「慢推近」「仰拍英雄」「遮擋轉場」「拉出」，這些不等於單一指令；
    要一個可檢索、可驗證、可測試的案例層，回傳候選 DSL，說法不清楚時保留歧義，特效、剪輯、時間效果和運鏡分開。不擴充 Camera Core。
- 修改前：沒有從常見說法到 DSL 的案例層；SKILL.md 只寫「自己把自然語言轉成 DSL」。
- 修改後：新增 examples/production_library/：production_examples.yaml 66 筆（敘事 30、技巧 36）、schema.yaml、README.md（中英說明，
    含規格要求的定位句）、narrative_30.md 與 technique_36.md（由資料產生）。新增 scripts/example_library.py：search_examples 依完全相同標題、
    標題片語、標籤、指令名稱、描述重疊計分，同分依編號，繁簡都可查；resolve_example 回傳候選 DSL、預設候選、needs_context、要問的問題、
    non_camera、ambiguity、alternatives、refinements、驗證結果與警告，需要補問的類別一律不自動選；CLI 有 search、resolve --choose、
    validate、docs。每個候選都重跑現有的解析器與衝突檢查。規格種子只改兩類，都記在該例的 build_notes：EX-002、EX-017 拿掉 /TELEPHOTO
    （85mm 不在 TELE 範圍，保留 /LENS:85），EX-005、EX-007、EX-009 拿掉 /ULTRAWIDE（24mm 不在 ULTRAWIDE 範圍，保留 /LENS:24）；EX-027 的
    /SRS 移到反打那一鏡，寫成 /SRS:A>B。第二批 36 筆的說明用自己的話重寫。tests/test_example_library.py 122 項，run_tests 與 Release Gate
    都會跑；它放在 tests/*.md 之外，不會進到 H3 鏡頭文字快照的語料。SKILL.md 加查詢步驟與載入表一列；README.md、README.zh-TW.md 加用途、
    快速開始與範例連結，測試數改為 866；audit 的 FILES 檢查加上這些檔案。
- 影響 Command：無（104 個指令、244 個別名與 registry 雜湊都不變，測試會擋）
- 影響 Adapter：無
- 影響 Test：新增 tests/test_example_library.py 122 項；run_tests 總數 744 改為 866
- 是否破壞 backward compatibility：否
- 檔案：examples/production_library/README.md, examples/production_library/production_examples.yaml, examples/production_library/schema.yaml,
    examples/production_library/narrative_30.md, examples/production_library/technique_36.md, scripts/example_library.py,
    tests/test_example_library.py, scripts/run_tests.py, scripts/audit.py, SKILL.md, README.md, README.zh-TW.md, CHANGELOG.md

## CL-056 · 2026-10-04 · research 與實驗紀錄移出 repository；新增 SOURCES.md；稽核在沒有這兩個資料夾的副本照常運作

- 原因：維護者要求把 research 和實驗紀錄從 repo 拿掉；公開的是 skill 本身，研究筆記和 H3 實測的原始紀錄留在維護者本機。
- 修改前：research/（11 個檔：來源、授權登記、設計決策、實驗索引、根因調查等）和 tests/reality/（42 格 Ref2VA 矩陣的紀錄、results.json、
    歷史版本與兩支工具，共 23 個檔）都在 repository 裡；稽核的 RESEARCH 與 REALITY 項少了它們就會報錯；公開檔案裡的 SRC、DIR、LOCAL
    來源編號要到 research/01_sources.md 才查得到；models/minimax_h3.md、SKILL.md、PROJECT_GOAL.md 有幾處直接指向這些檔案。
- 修改後：這 34 個檔從 git 移除追蹤並寫進 .gitignore，本機檔案保留，維護者照常使用。新增 SOURCES.md：40 個來源的編號、repository、授權與
    用途，公開檔案裡引用的來源編號都查得到。scripts/audit.py：RESEARCH 項先檢查每個公開檔案引用的來源編號都在 SOURCES.md；research/ 不在時
    略過登記檢查並註明，在時照舊全部檢查；REALITY 項在 results.json 不在時略過 verdict hash 與矩陣交叉比對並註明，profile 的其餘檢查照跑；
    Release Gate 的 THIRD_PARTY_CONTENT 與 42 格狀態行在副本裡註明由維護者保存。models/minimax_h3.md、SKILL.md、PROJECT_GOAL.md 拿掉指向
    已移除檔案的路徑，意思不變。registry、schemas、references、tests 表頭裡的 research/0x 引用與 profile 的註解不改（凍結或屬於證據），
    SOURCES.md 說明它們指向維護者的設計筆記。
- 影響 Command：無
- 影響 Adapter：無
- 影響 Test：無（42 格 verdict hash 仍由維護者本機的稽核檢查）
- 是否破壞 backward compatibility：否（維護者本機的結果不變；公開副本的稽核不再因為少了這兩個資料夾而報錯）
- 檔案：SOURCES.md, .gitignore, scripts/audit.py, SKILL.md, PROJECT_GOAL.md, models/minimax_h3.md, CHANGELOG.md,
    research/01_sources.md, research/02_feature_matrix.md, research/03_command_inventory.md, research/04_terminology_conflicts.md,
    research/05_gap_analysis.md, research/06_license_notes.md, research/07_design_decisions.md, research/h3_lab_findings.md,
    research/h3_root_cause_investigation.md, research/license_register.yaml, research/project_goal_and_h3_architecture_audit.md,
    tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/02_angle_height.md,
    tests/reality/minimax_h3/03_tracking.md, tests/reality/minimax_h3/04_complex_motion.md, tests/reality/minimax_h3/05_focus.md,
    tests/reality/minimax_h3/06_combinations.md, tests/reality/minimax_h3/07_sequences.md,
    tests/reality/minimax_h3/08_negative_cases.md, tests/reality/minimax_h3/09_storyboard_cases.md,
    tests/reality/minimax_h3/10_results.md, tests/reality/minimax_h3/11_crane_validator_v2.md,
    tests/reality/minimax_h3/12_pedestal_revalidation_v1.md, tests/reality/minimax_h3/history/01_single_movement_before_ped_v1.md,
    tests/reality/minimax_h3/history/04_complex_motion_before_crane_v2.md,
    tests/reality/minimax_h3/history/04_complex_motion_before_ped_v1.md,
    tests/reality/minimax_h3/history/06_combinations_before_crane_v2.md,
    tests/reality/minimax_h3/history/06_combinations_before_ped_v1.md,
    tests/reality/minimax_h3/history/10_results_before_crane_v2.md, tests/reality/minimax_h3/history/10_results_before_ped_v1.md,
    tests/reality/minimax_h3/history/11_crane_validator_v2_before_ped_v1.md, tests/reality/minimax_h3/results.json,
    tests/reality/minimax_h3/tools/crane_validator_v2.py, tests/reality/minimax_h3/tools/h3_reality.py

## CL-055 · 2026-10-03 · README 改寫成產品首頁：英文 README.md 加完整繁體中文 README.zh-TW.md

- 原因：維護者的 GITHUB_README_PRODUCT_REWRITE：README 太像技術規格；要先讓使用者想用、再快速理解、再安裝、最後才給技術細節；
    H3 實測證據要放在明顯的位置；中英文分成兩份。
- 修改前：README（CL-054）只有簡短的用途、範例、安裝、指令表與 H3 小技巧，H3 實測證據只有一句提示；中文只有底部摘要。
- 修改後：README.md 依產品順序重寫：定位句與示範指令、支援模型與數字、30 秒示範（程式實際輸出與 routing）、為什麼不直接寫
    提示詞、差異、MiniMax H3 實測、兩種證據與等級意義、範圍規則（三個實際 routing 例子）、各模式結果表、用途、支援模型（分開
    「有轉接器」與「有實測」）、安裝、快速開始、H3 用法、指令速查、分鏡與連戲、範例、架構圖、實測方法、已知限制、專案狀態、授權；
    新增 README.zh-TW.md，完整繁體中文版、結構相同，兩份頂部互相連結。所有指令實際跑過，數字與等級敘述對照
    models/minimax_h3.md 與 models/minimax_h3_profile.yaml。
- 影響 Command：無
- 影響 Adapter：無
- 影響 Test：無
- 是否破壞 backward compatibility：否
- 檔案：README.md, README.zh-TW.md, CHANGELOG.md

## CL-054 · 2026-10-03 · README 改寫成給使用者看的說明

- 原因：維護者要求 GitHub 上的說明寫給使用者看：怎麼用、優點、能解決什麼問題；研究、實驗筆記與規範內容不寫進 README。
- 修改前：README 是給維護者看的技術報告：架構、證據類型、等級、狀態、來源表、維護指令與環境變數。
- 修改後：README 只寫一句話介紹、真實輸出範例、解決的問題、優點、安裝、使用、常用指令表、H3 小技巧與授權，另附中文說明；
    裡面的每一個指令都實際跑過。
- 影響 Command：無
- 影響 Adapter：無
- 影響 Test：無
- 是否破壞 backward compatibility：否
- 檔案：README.md, CHANGELOG.md

## CL-053 · 2026-10-03 · 建立 Git repository 前的修正：稽核不把 .git 算進檔案指紋、所有檔案原樣存取不轉換換行

- 原因：維護者要求 git init 並發佈 v1.0.0。建立 repository 前檢查發現兩件事會讓 clone 下來的副本稽核失敗：BASELINE 稽核的檔案指紋
    會把 .git 資料夾裡的檔案也算進去，每一個都會被當成「新增但沒有記在 CHANGELOG」；指紋逐位元組比對，而 Windows 版 git 預設會在
    checkout 時轉換換行符號，clone 下來的檔案就和凍結指紋不同。
- 修改前：scripts/audit.py 的 current_manifest 與 RESEARCH 的來源編號掃描只略過 __pycache__；repository 沒有 .gitattributes。
- 修改後：兩處都略過 .git；新增 .gitattributes（`* -text`）：所有檔案原樣存進 repository、原樣 checkout，任何系統 clone 下來都和
    這份逐位元組相同；repository 的本機設定另關掉 core.autocrlf。在有 .git 的資料夾重跑稽核與 Release Gate 驗證。
- 影響 Command：無
- 影響 Adapter：無
- 影響 Test：無（run_tests 744/744）
- 是否破壞 backward compatibility：否（沒有 .git 的資料夾結果完全一樣）
- 檔案：.gitattributes, CHANGELOG.md, scripts/audit.py

## CL-052 · 2026-10-03 · v1.0.0 發佈前收尾：對外術語統一為 CONSTRAINED_PRODUCTION／CAMERA_ONLY、H3 狀態分成兩項、從零重做隱私與機密清查

- 原因：維護者的 PUBLIC_RELEASE_FINALIZATION_AND_PRIVACY_AUDIT：GitHub v1.0.0 發佈前，對外文件統一用一套證據（H3 Camera Production
    Evidence）的兩種類型描述實測，不再以「有人物／沒人物」把兩輪證據講成兩套；H3 狀態要分成「v1.0 生產基線已完成」與「全部組合沒有、
    也不需要窮舉驗證」；把準備公開的整個資料夾從零重新清查私人資訊、本機環境、秘密與二進位檔；重跑既有的來源文字比對。不生成影片、
    不改 Camera Core 與 wrapper 語義、不改任何 verdict、等級或證據內容。
- 修改前：scripts/audit.py 內含 12 個私人名稱的 SHA-256：短字的雜湊可以用猜測或窮舉還原，實測還原出其中幾個（包括個人名字與私人專案名），
    等於把私人名稱公開；公開檢查只掃 .md／.py／.yaml／.json／.txt 與 LICENSE，不擋二進位檔、家目錄相對路徑、網路分享路徑、使用者設定資料夾、
    私人網段位址、.env；秘密檢查只認 sk-、ghp_、github_pat_、hf_、AKIA、xox、私鑰開頭與 key／secret／password／token 的賦值；
    REPO_HYGIENE 不擋 .old、.dmp、coverage 輸出與 IDE workspace 檔；Release Gate 的 OPEN_ITEMS 只寫「MiniMax H3 reality validation:
    PARTIAL」，容易被讀成 v1.0 沒完成。
    README 是 2026-10-01 的中文版：已知限制過期（還列著之後已實測的運鏡），沒有說明證據類型、exact scope、LOW 與 INSUFFICIENT_EVIDENCE
    的意思、FL2VA 的 endpoint 限制與 H3 狀態；對外文件以 character-anchored／environment-only、free camera 描述兩輪證據。
    research/01_sources.md 與 06_license_notes.md 寫了本機技能副本的家目錄路徑與私人實驗室的資料夾名；research/h3_lab_findings.md
    有一個內部編號是私人製作的鏡號；research/h3_root_cause_investigation.md 留有一筆本機 ComfyUI 的執行編號（prompt_id 前 8 碼）。
    research/license_register.yaml 的來源比對紀錄停在 2026-09-30；LICENSE_WARNING-2、SRC-008／LOCAL-001 與 interface_terms 的說明只寫
    格式標籤，沒寫到 wrapper 逐字輸出的官方固定格式句（I2VA 的關鍵幀句、FL2VA／L2VA 的參考圖對齊句）。
    CLI：未知的 --model 直接丟 Python traceback（含本機安裝路徑）；--h3-subject-context 只收 character_anchored／environment_only。
    .gitignore 只有 __pycache__ 與 *.pyc。
- 修改後：
    scripts/audit.py：私人名稱清單移出 repository，改讀 CAMERA_DSL_PRIVATE_TERMS 指向的本機檔（一行一個 SHA-256，放在 repository 之外；
    沒設定時略過名稱比對、報告註明；設了卻讀不到任何 SHA-256 行時是 PUBLISH ERROR，不會被當成已經檢查過，訊息也不印出路徑）；
    公開檢查掃 repository 的每一個檔案（含隱藏檔、不論副檔名），另擋二進位檔、家目錄相對路徑、網路分享路徑、使用者設定資料夾與私人網段位址；
    release checks 的秘密與 e-mail 掃描改成全部檔案，秘密格式另加 GitLab、Google API、npm、PyPI、OpenAI project key、JWT、
    Bearer／Authorization／x-api-key 標頭、Azure AccountKey、GCP service account 金鑰檔；REPO_HYGIENE 另擋 .mypy_cache、.ruff_cache、
    .vscode、.idea、node_modules、htmlcov、.env（.env.example 除外）、.old、.dmp、.code-workspace、.coverage、coverage.xml 與媒體／模型檔；
    Release Gate 新增 STATUS 三行：h3_production_baseline_status（由 profile 計算：五個 mode 都有 CONSTRAINED_PRODUCTION 與 CAMERA_ONLY
    證據＝COMPLETE）、h3_full_command_space_validation PARTIAL（設計上如此）、42 格 Ref2VA 矩陣（歷史、凍結，FINAL PARTIAL）；
    OPEN_ITEMS 只留不擋發佈的兩項。新檢查用 29 個故意做錯的樣本驗證（家目錄路徑、網路分享、私人位址、使用者資料夾、二進位檔、秘密、e-mail、
    .env、10 種 token 格式、6 種快取／暫存／dump 檔、私人名稱清單不存在、清單裡沒有雜湊、真清單對乾淨資料夾、真清單對私人名稱樣本、
    乾淨資料夾），29/29 符合預期；私人名稱的錯誤訊息只印雜湊前 10 碼。
    術語：README 重寫（英文主文＋中文摘要：用途、Canonical Camera IR、共用 H3 Camera Core、五個 mode、Production Routing、兩種證據類型、
    exact scope、不跨範圍借等級、LOW 不代表 DSL 錯、INSUFFICIENT_EVIDENCE 不等於模型失敗、FL2VA endpoint 限制、運鏡語義不為模型讓步、
    STRICT／DIRECTOR、MIT、版本號說明、狀態、已知限制、來源表、維護與環境變數）；PROJECT_GOAL.md 新增「H3 Camera Production Evidence
    and release status (v1.0.0)」一段與兩個狀態鍵；SKILL.md 的 routing 說明與 CLI 改用新名稱；models/minimax_h3.md 新增
    「H3 Camera Production Evidence (v1.0)」一段（兩種證據類型與資料裡的名稱對照、exact scope、等級意義、LOW／IE、FL2VA、狀態），
    三個基線的標題標上證據類型、CL-051 那幾段改用新名稱；research/h3_lab_findings.md 開頭加證據類型說明。人物只是測試用的 reference
    target，不是 DSL 的分類，也沒有加進任何 reliability key。資料裡的 subject_context 名稱（CHARACTER_ANCHORED／ENVIRONMENT_ONLY）、
    routing 印出的文字、profile 與 results.json 的內容、verdict hash 一律不動。
    routing：scripts/adapters.py 加 SUBJECT_CONTEXT_ALIASES（CONSTRAINED_PRODUCTION＝CHARACTER_ANCHORED、CAMERA_ONLY＝ENVIRONMENT_ONLY）；
    scripts/camera_dsl.py 的 --h3-subject-context 多收 constrained_production、camera_only（說明文字改用新名稱），未知的 --model 改成
    一行 ERROR、exit 2。
    隱私：research/01_sources.md、06_license_notes.md 的本機副本路徑改成「本機副本（與 SRC-008 相同，路徑不公開）」，LOCAL-002 的標題不寫
    資料夾名；research/h3_lab_findings.md 的私人鏡號改成 production test shot；research/h3_root_cause_investigation.md 拿掉 prompt_id。
    CHANGELOG 最上方加 v1.0.0 發佈摘要；.gitignore 補快取、暫存、coverage 輸出、dump、IDE、.env、媒體與模型檔。
    來源比對：用 2026-09-30 的同一支腳本、同一個方法、同一批來源副本重跑（skill 97 個文字檔對 3,546 個來源檔）。維護者自己的實驗室
    以外有 106 段相同文字，逐條人工複核：官方 H3 提示詞格式（五個 wrapper 逐字輸出的段落標籤、關鍵幀句、參考圖對齊句、retention 格式、
    只用官方運鏡詞組成的句子；DIR-03 與 SRC-009 引用同一套官方格式所以也對到）、標準術語、研究筆記裡最多 11 個 token 的 MIT 來源短引文、
    程式慣用寫法、網址、repo 名、來源檔路徑與公開的模型檔名。沒有新的照抄段落，CL-003 改寫過的句子沒有回來（SRC-004 仍是同樣 21 段、
    最長是 14 個 token 的景別階梯；SRC-009 最長是 13 個 token 的 retention 格式句）。research/license_register.yaml 記一筆 recheck_2，
    LICENSE_WARNING-2、SRC-008／LOCAL-001 的說明與 interface_terms 的定義補上「固定格式句」，結論不變（RESOLVED、CLEAR_INTERFACE_TERMS、
    copied_content false）；research/06_license_notes.md 同步。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照 406 個輸入逐字相同，tests/snapshots/minimax_h3_core.json sha 1c0c713b80207e0a；h3_wrappers.py
    f8533fb5c8adc02a 不變）；routing：subject context 多兩個別名，既有輸入的路線、等級與文字不變
- 影響 Test：tests/h3_routing.md 新增 RT-N-16–18（CAMERA_ONLY、CONSTRAINED_PRODUCTION 別名與 STATIC）；既有測試一條都沒改；
    快照沒有新增輸入；run_tests 744/744
- 是否破壞 backward compatibility：否（character_anchored／environment_only 照常可用，既有查詢的輸出不變；公開檢查變嚴，只多擋本來就
    不該公開的內容；沒設 CAMERA_DSL_PRIVATE_TERMS 的機器略過私人名稱比對，設錯的機器會看到 ERROR）
- 檔案：.gitignore, CHANGELOG.md, PROJECT_GOAL.md, README.md, SKILL.md, models/minimax_h3.md, research/01_sources.md,
    research/06_license_notes.md, research/h3_lab_findings.md, research/h3_root_cause_investigation.md, research/license_register.yaml,
    scripts/adapters.py, scripts/audit.py, scripts/camera_dsl.py, tests/h3_routing.md

## CL-051 · 2026-10-03 · 自由鏡頭／純環境基線登記（12 條路線 × 五個 mode × 3 seeds，subject_context ENVIRONMENT_ONLY）；routing 分開 CHARACTER_ANCHORED 與 ENVIRONMENT_ONLY；H3_FREE_CAMERA_PRODUCTION_BASELINE_COMPLETE

- 原因：維護者的 H3 FREE CAMERA / ENVIRONMENT-ANCHORED CORE BASELINE：畫面完全沒有人物時，同一套 Canonical Camera DSL 在 H3 五個 mode
    能不能可靠控制純環境的攝影機運動（測攝影機幾何，不測人物追蹤）；新證據一律帶 subject_context = ENVIRONMENT_ONLY，不與既有
    CHARACTER_ANCHORED 證據合併、不互相覆蓋；routing 要能分開兩種情境；既有基線與 verdict 一個都不改。
    實驗室流程（預登記、manifest 180 筆、preflight 與 14 種壞 manifest、18 種已知運鏡校準 81/81、主畫面 28/28、五個 block 連續生成、
    逐支目視、生成前登記的 validator 缺陷與唯一一次修補批次、runner 事件）記在實驗室；對外摘要在 research/h3_lab_findings.md（H3LAB-FC-*）。
- 修改前：證據與路線都沒有 subject context（全部是有人物的情境）；production_routes 沒有 STATIC；鎖定鏡頭（/STATIC）在 routing 只查矩陣列；
    LOCAL_H3_T2VA／FL2VA／L2VA_PDD8_Q_416 在 generation_profiles 的 evidence 欄仍寫 CL-049 的「NONE（nothing generated yet）」。
- 修改後：
    profile（models/minimax_h3_profile.yaml；只新增，另外 3 行修正）：五個 profile 的 reality_evidence 各加一個 environment_only_baseline
    （subject_context ENVIRONMENT_ONLY、scope、input、validator_notes、12 支 production_shots：DSL、各 seed 判定、PASS 數、機制數、reliability、
    repeated／variable failure 或 FL2VA 的 input_limitation、failing_items、defects、prompt／core／wrapper sha）；production_routes 新增 60 條
    （每個 mode 12 條，subject_context ENVIRONMENT_ONLY、start_framing NONE、推拉 end_framing FREE、ORBIT angle 45、input environment_*），
    新增 STATIC 指令鍵（canonical_semantics camera_locked）。等級（PV／COND／LOW／IE）：T2VA 9／1／2／0、I2VA 2／6／4／0、
    FL2VA 1／0／0／11（主畫面同時當首尾幀＝ENDPOINT_CONSTRAINED，11 條移動路線依預登記記 IE）、L2VA 1／2／6／3、Ref2VA 7／2／2／1。
    generation_profiles 三個 evidence 欄改成指向各自的 reality_evidence（CL-050 已在這三個 profile 下量測，CL-049 的 NONE 過期）。
    既有每一行（含 42 格、I2VA 基線、多模式基線）逐字不變：difflib 0 刪除、3 替換（就是上面三個 evidence 欄）、其餘全是新增。
    routing（scripts/adapters.py routing 區段；鏡頭核心區段不變）：h3_scope 加 subject context（不指定＝CHARACTER_ANCHORED；ENVIRONMENT_ONLY
    只讀該 profile 的 environment_only_baseline；不認得的情境＝UNVERIFIED）；路線比對多一層情境，另一個情境的路線一律不套用，只說
    「這個 profile 只量過 subject context X」；start_framing NONE 的路線只套用到沒有景別的運鏡；鎖定鏡頭查 STATIC 路線；
    其他範圍清單把 ENVIRONMENT_ONLY 範圍排在原有範圍之後；路線摘要多印 input_limitation（只有 FL2VA 自由鏡頭路線有）；
    scope 行在指定情境時多寫「subject context X」。CLI：camera_dsl.py render 加 --h3-subject-context character_anchored|environment_only；
    run_tests.py 的 spec 加 ctx=env|char。audit.py：environment_only_baseline 必須是 ENVIRONMENT_ONLY 且與 profile 同 mode、
    裡面每支 production_shot 必須是 ENVIRONMENT_ONLY、ENVIRONMENT_ONLY 路線必須有對應 block、情境只能是兩種之一、start_framing 可為 NONE、
    STATIC 路線的 measured_dsl 以鎖定鏡頭比對（8 個故意做錯的樣本 8/8 擋下，未修改的 profile 0 錯）。
    文件：models/minimax_h3.md 新增自由鏡頭基線一段與 12×5 表、與有人物情境的差異、validator 限制，routing 說明加 subject context；
    research/h3_lab_findings.md 新增 H3LAB-FC-METHOD-01、-T2VA-01、-I2VA-01、-FL2VA-01、-L2VA-01、-REF2VA-01、-REVIEW-01；
    PROJECT_GOAL.md 狀態加 H3_FREE_CAMERA_PRODUCTION_BASELINE_COMPLETE 與各 mode 等級；SKILL.md 的 routing 說明與 CLI 加 --h3-subject-context。
    examples/*.md 由 --sync 重新產生：只有「Evidence exists under」清單多列五個 ENVIRONMENT_ONLY 範圍。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照 406 個輸入逐字相同，tests/snapshots/minimax_h3_core.json sha 1c0c713b80207e0a 不變；
    h3_wrappers.py f8533fb5c8adc02a 不變）；routing：subject context、STATIC 路線、情境不符的說明行、其他範圍排序、input_limitation
- 影響 Test：tests/h3_routing.md 新增 RT-N-01–15（ENVIRONMENT_ONLY 路線只在指定情境套用、預設情境不套用、景別／角度／方向／落幅範圍、
    STATIC 與情境說明行、FL2VA 輸入限制不寫成失敗、Ref2VA 環境範圍不顯示矩陣、其他範圍排序、中文、不認得的情境）；既有測試一條都沒改；
    快照沒有新增輸入；run_tests 741/741
- 是否破壞 backward compatibility：否（不指定 subject context 時一律是 CHARACTER_ANCHORED，既有查詢的路線、等級與鏡頭文字不變；
    只在其他範圍清單末尾多列 ENVIRONMENT_ONLY 範圍，鎖定鏡頭在有自由鏡頭證據的 profile 下多一行「只量過 ENVIRONMENT_ONLY」）
- 檔案：CHANGELOG.md, PROJECT_GOAL.md, SKILL.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md,
    examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, research/h3_lab_findings.md, scripts/adapters.py,
    scripts/audit.py, scripts/camera_dsl.py, scripts/run_tests.py, tests/h3_routing.md

## CL-050 · 2026-10-02 · 多模式生產基線登記（T2VA／FL2VA／L2VA／Ref2VA current core，16 條路線 × 3 seeds）；H3_MULTI_MODE_PRODUCTION_BASELINE_COMPLETE

- 原因：維護者的 H3 MULTI-MODE PRODUCTION BASELINE FINALIZATION：I2VA 基線凍結不重跑；同一套 16 條路線、seed 1001–1003，在 T2VA、FL2VA、L2VA、
    Ref2VA（current core）各生成 48 支（共 192 支），用凍結的 I2VA validator 判定，結果寫進 reality profile 與 production routes；
    證據範圍＝mode＋generation profile＋指令＋方向＋起幅＋落幅＋角度，其他一律 UNVERIFIED；Ref2VA 的 42 格不動，current core 的結果另存，兩者不同時都保留。
    實驗室流程（預登記、manifest 192 筆、preflight、validator 移植與校準 46/48、四個 block、一支 GPU 搶用的同 spec 同 seed 補生成、逐支目視、
    事後撤回 58 個切點否決與 8 個突波否決）記在實驗室，對外摘要在 research/h3_lab_findings.md（H3LAB-MM-*）。
- 修改前：LOCAL_H3_T2VA／FL2VA／L2VA_PDD8_Q_416 只有設定（CL-049），routing 一律 UNVERIFIED；Ref2VA profile 只有 42 格矩陣；
    production_routes 只有 Ref2VA 歷史路線與 I2VA 路線（19 條）。T2VA 的 profile 若有 text-only 景別紀錄，routing 會印出 Ref2VA 專用的建議
    （「If Ref2VA is kept, describe what environment…」）並在警告裡引用 Ref2VA 的證據 H3LAB-FRAMING-SCENE-01。
- 修改後：
    profile（models/minimax_h3_profile.yaml；只新增、既有每一行逐字不變——difflib 比對 0 行刪除、0 行替換，I2VA 與 42 格紀錄不動）：
    reality_evidence 新增 LOCAL_H3_T2VA／FL2VA／L2VA_PDD8_Q_416 三個 block（scope、16 支 production_shots：DSL、input、各 seed 判定、PASS 數、機制數、
    reliability、repeated／variable failure、failing_items、input／validator limitation、defects、prompt sha、core 與 wrapper 快照 sha）；
    T2VA 加 framing.text_only_shot_size LOW（strict MFS／MS／MCU；起幅 4/48，失手 44 支全部偏寬，其中 27 支寬兩級以上）；
    FL2VA 加 framing.first_frame_framing HIGH（第 0 幀＝首幀 48/48、最後一幀＝尾幀 48/48）；L2VA 只記 start_framing_result（34/48），不登記景別可靠度。
    Ref2VA block 末尾新增 current_core_production_baseline（evidence_set CURRENT_CORE_PRODUCTION_BASELINE，16 支，start_framing_result 6/48），42 格與 verdict hash 不動。
    production_routes 新增 64 條（每個 mode 16 條；input text_only／first_and_last_keyframes／last_keyframe／face_and_outfit_reference_pictures，
    推拉三條加 _with_foreground_motion_anchor、physical_depth_geometry NOT_VERIFIED；direction、start_framing、end_framing、end_size、ORBIT angle 45；
    reliability、mechanism、confidence、failure_behavior、limitation；Ref2VA 的路線帶 evidence_set）。等級：T2VA 0／0／16 LOW；
    FL2VA 11 PRODUCTION_VALIDATED、1 LOW、4 INSUFFICIENT_EVIDENCE（FOLLOW、PAN:R、TRUCK:R、TRUCK:L 的尾幀是代用片，生成前就規定記 IE）；
    L2VA 2／3／11；Ref2VA 0／1／15。FL2VA DOLLYOUT 的 limitation 寫 input_anchor_fixed_on_screen（兩張關鍵幀的錨點在同一個畫面位置，近景物不可能往內移）。
    routing（scripts/adapters.py 的 routing 區段；鏡頭核心區段不變）：text-only 景別紀錄的建議與警告依 mode 分開——Ref2VA 照舊一字不變；
    其他 mode 寫「If <mode> is kept, a <size> frame is not guaranteed.」、中文「若仍用 <mode>：不保證維持<景別>構圖。」，不再印 Ref2VA 的環境建議、不引用 Ref2VA 的證據。
    文件：models/minimax_h3.md——mode 列表三列換成 T2VA／FL2VA／L2VA 的實測、新增「Multi-mode production baseline」一段與 16×5 表
    （ROUTE／T2VA／I2VA／FL2VA／L2VA／Ref2VA）、跨 mode 的重複失敗、各 mode 的長處與限制、validator 限制；routing 說明加多模式路線。
    research/h3_lab_findings.md——新增 H3LAB-MM-METHOD-01、H3LAB-MM-T2VA-01、-FL2VA-01、-L2VA-01、-REF2VA-01、H3LAB-MM-REVIEW-01。
    PROJECT_GOAL.md——狀態段落加 H3_MULTI_MODE_PRODUCTION_BASELINE_COMPLETE 與各 mode 等級，Camera Validation 到此為止
    （不新增路線、seed、角度、景別，不重新優化 LOW 路線）。examples/*.md 由 --sync 重新產生：只有「Evidence exists under」清單多列三個 mode 的 scope；
    references／registry／schemas 也由 --sync 重寫，內容不變（不含 routing 文字）。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照 406 個輸入逐字相同，tests/snapshots/minimax_h3_core.json sha 1c0c713b80207e0a 不變；h3_wrappers.py f8533fb5c8adc02a 不變）；
    routing：三個多模式 profile 讀到自己的 16 條路線與 framing 紀錄；T2VA 的 text-only 景別建議改寫成 T2VA 自己的句子
- 影響 Test：tests/h3_routing.md——RT-B-07／08／09 改用新 profile 仍沒有證據的指令（/MS /ROLL:CW、/MS /PAN:L、/MS /DOLLYIN:MS>CU），照樣檢查不借用；
    RT-E-12／15／27／32 的 norouting 改成只比對 I2VA 的 input 名稱（\bwith_foreground_motion_anchor、subject_camera_speed_matching），並檢查 Ref2VA
    current-core 路線有顯示；新增 RT-M-01–15（各 mode 自己的路線、FL2VA 首幀景別、L2VA 景別 UNVERIFIED、FL2VA 的 IE、90 度與 FS 不套用、
    Ref2VA 兩套證據並列、I2VA 不受影響、FL2VA 的輸入限制、T2VA 建議寫自己的 mode、中文）；快照沒有新增輸入；run_tests 726/726
- 是否破壞 backward compatibility：否（routing：T2VA／FL2VA／L2VA profile 原本對 16 條基線路線回 UNVERIFIED，現在回實測等級；Ref2VA profile 在 42 格之外
    多顯示 current-core 基線路線；其他 mode 與指令的輸出不變；鏡頭文字不變）
- 檔案：CHANGELOG.md, PROJECT_GOAL.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, research/h3_lab_findings.md, schemas/examples.yaml, scripts/adapters.py, tests/h3_routing.md

## CL-049 · 2026-10-02 · 多模式生產基線的三個 generation profile（T2VA／FL2VA／L2VA，只寫設定）

- 原因：維護者的 H3 MULTI-MODE PRODUCTION BASELINE FINALIZATION：每個 mode 要有含 mode 名稱的 generation profile；已有的沿用，缺的只建設定、
    不帶證據；provenance 要列出每一個設定，不可寫「same as I2VA」。Ref2VA 沿用 LOCAL_H3_REF2VA_PDD8_Q_416；I2VA 已凍結、不生成；
    T2VA、FL2VA、L2VA 沒有 profile，在生成前補上。
- 修改前：generation_profiles 有 LOCAL_H3_REF2VA_PDD8_Q_416、LOCAL_H3_I2VA_PDD8_Q_416、LOCAL_H3_PRODUCTION_REF2VA、LOCAL_H3_PRODUCTION_I2VA、
    OFFICIAL_REFERENCE；T2VA、FL2VA、L2VA 只能用 OFFICIAL_REFERENCE（沒有生成設定）或不給 profile，routing 一律 UNVERIFIED。
- 修改後：新增 LOCAL_H3_T2VA_PDD8_Q_416、LOCAL_H3_FL2VA_PDD8_Q_416、LOCAL_H3_L2VA_PDD8_Q_416，每個都逐項寫 checkpoint
    （minimax_h3_fl2va_pruned_int8_convrot）、text encoder（Qwen3-VL-32B nvfp4 awq）、video VAE fp16、audio VAE fp32、8 步、euler（PDD 的 sigmas）、
    cfg 1.0、shift 12／3、24 fps、accelerator PDD-Acc MiniMax-H3-FL2VA-Acc-8Step、416x736、124 幀、reference configuration、ref_image_size、
    input_asset_configuration、evidence NONE。三者共用 MiniMaxH3ImageToVideo（節點本身就是 t2va 與 fl2va 的入口）：T2VA 不接關鍵幀、
    FL2VA 首幀在第 0 幀＋尾幀在第 123 幀、L2VA 只有尾幀在第 123 幀；圖都剛好 416x736，不會被拉伸或裁切。
    文件：models/minimax_h3.md 與 PROJECT_GOAL.md 列 profile 的地方補上三個 id。
    沒有任何 reality evidence、production route、等級；routing 對這三個 profile 都是 UNVERIFIED，其他 profile 的等級不套用，profile 與 mode 不合會擋。
- 影響 Command：無
- 影響 Adapter：無（鏡頭文字、wrapper、routing 程式都沒動；routing 讀到三個新 profile，回 UNVERIFIED）
- 影響 Test：新增 RT-B-07／08／09（三個新 profile 都是 UNVERIFIED，I2VA 的 PRODUCTION_VALIDATED 不套用）
- 是否破壞 backward compatibility：否（只新增 profile；既有 profile 與輸出不變）
- 檔案：CHANGELOG.md, PROJECT_GOAL.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, tests/h3_routing.md

## CL-048 · 2026-10-02 · ORBIT 路線的證據範圍加入角度（完全相符才套用）；TILT:DOWN 保留 PRODUCTION_VALIDATED 並寫明兩個限制；H3_I2VA_PRODUCTION_BASELINE_COMPLETE 凍結

- 原因：維護者驗收 CL-047 並選 A——production route 的證據範圍再加角度，和已經固定的 mode／profile／direction／起幅／落幅是同一原則，不是新的架構。
    目前的證據只支持 /MS /ORBIT:R:45；/MS /ORBIT:R:90、/MS /ORBIT:R:FULL、沒寫角度的 /MS /ORBIT:R 都必須是 UNVERIFIED，可以列出相近證據，但不得把 LOW 套過去。
    同時定案三件事：（1）TILT:DOWN 依事先寫好的規則是 3/3 PASS，保留 PRODUCTION_VALIDATED，不因看片後發現臉出畫而事後改判；但路線要寫明
    framing_retention_not_guaranteed 與 large_downward_tilt_may_move_subject_face_out_of_frame——下搖機制可靠，不等於人物一定保持理想構圖。
    （2）ORBIT 的 RULE_DEFECT 定性為 VALIDATOR_GEOMETRY_DEFECT：validator 的缺陷，不是模型失敗、也不是提示詞失敗；受污染的背景點不計分、原始量測保留、
    正式判定不重判、不為它重跑。（3）H3_I2VA_PRODUCTION_BASELINE_COMPLETE 正式凍結，停止新的 Camera Validation；特殊鏡頭等實際專案需要時再測。
- 修改前：production route 的範圍是 mode＋generation profile＋direction＋起幅＋落幅；ORBIT 路線沒有角度欄位，/MS /ORBIT:R:90、/MS /ORBIT:R:FULL、/MS /ORBIT:R
    在 I2VA profile 也顯示 45 度那條 LOW（CL-047 記下的已知限制）。TILT:DOWN 路線的 limitation 是 tilt_amount_uncontrolled。PROD_17 的 rule_defect 只有 seeds 與 handling。
    PROJECT_GOAL.md 的狀態段落寫「Next: post-refactor production validation under the production profiles」。
- 修改後：
    routing（scripts/adapters.py 的 routing 區段；鏡頭核心區段逐位元組相同）：新增 _asked_angle，讀出鏡頭寫的角度（度數、FULL 這類關鍵字、或沒寫）。
    路線帶 angle 時只套用到角度完全相同的鏡頭；別的角度、FULL、沒寫角度都走既有的「這個範圍沒有量過」分支——UNVERIFIED，相近證據只列實測 DSL、不帶等級
    （和 CL-042 的寫法相同），並多寫出問的是哪個角度（英文 ", angle 90 degrees"／", angle FULL"／", no stated angle"；中文「、角度 90 度」／「、沒有指定角度」）。
    方向不同照舊回「measured under this scope for direction R only」。沒有帶 angle 的路線（其他所有指令）輸出一字不變。
    audit（scripts/audit.py）：路線的 angle 必須是正數；measured_dsl 寫了角度，路線就必須帶同一個角度；measured_dsl 沒寫角度的路線不可以帶 angle。
    用壞樣本驗證 7 種都會報 REALITY 錯誤，未修改的 profile 0 錯誤。
    profile：ORBIT 路線加 angle: 45（等級 LOW、機制、confidence、evidence 不變）；TILT:DOWN 路線與 PROD_12 的 limitation 改成
    framing_retention_not_guaranteed, large_downward_tilt_may_move_subject_face_out_of_frame，note 開頭加一句「PRODUCTION_VALIDATED 說的是下搖機制可靠，
    不是人物保持理想構圖」（reliability PRODUCTION_VALIDATED、3/3 PASS 不變）；PROD_17 的 rule_defect 加 classification VALIDATOR_GEOMETRY_DEFECT、meaning、handling；
    ORBIT 路線與 PROD_17 的 note 裡「範圍沒有角度欄位」那句改成現況，並補一句定性；檔頭註解同步。所有 verdict、等級、各 seed 的數字逐欄比對不變。
    文件：models/minimax_h3.md——範圍說明加角度、ORBIT 與 TILT:DOWN 兩列同步、新增「I2VA production baseline（H3_I2VA_PRODUCTION_BASELINE_COMPLETE，2026-10-02 凍結）」
    一段與 16 條路線的表（PRODUCTION_VALIDATED 3、CONDITIONAL 2、LOW 11；寫明 PRODUCTION_VALIDATED 指的是實測的機制可靠，不保證每個構圖細節）；
    research/h3_lab_findings.md——H3LAB-PROD-SHOT-12、17 兩列同步；PROJECT_GOAL.md——Reality profile 那段加一句角度範圍，狀態段落把
    「Next: …production validation…」換成「I2VA 生產基線完成並凍結；Camera Validation 到此為止，基線以外的鏡頭或 profile 維持 UNVERIFIED，等製作需要時才驗證」。
    examples／references／registry／schemas 底下的檔是 --sync 重新產生的，內容和修改前逐字相同（另外產生一份比對過）。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照既有 403 個輸入與 20 個 wrapper 提示詞逐字相同；h3_wrappers.py 沒動）；只有 routing：帶 angle 的 production route 依角度完全相符才套用
- 影響 Test：新增 RT-E-50–55（90 度、沒寫角度、FULL、別的起幅都是 UNVERIFIED＋相近證據；45 度照常套用；沒有角度範圍的指令輸出不變）與 RT-Z-07／08（中文）；
    RT-E-38 的 limitation 字串、RT-E-46 的說明同步；快照新增 3 個輸入（403 → 406，舊的逐字不變）；run_tests 708/708
- 是否破壞 backward compatibility：否（routing：I2VA 下角度和實測不同或沒寫角度的 ORBIT:R，原本會顯示 45 度那條路線的等級，現在顯示 UNVERIFIED＋相近證據；
    TILT:DOWN 路線的 limitation 字串改成維護者指定的兩個名稱；鏡頭文字不變）
- 檔案：CHANGELOG.md, PROJECT_GOAL.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, research/h3_lab_findings.md, schemas/examples.yaml, scripts/adapters.py, scripts/audit.py, tests/h3_routing.md, tests/snapshots/minimax_h3_core.json

## CL-047 · 2026-10-02 · 生產驗證最後一批登記：PROD-09–17（TRUCK:R／L、TILT:UP／DOWN、PEDESTAL:UP／DOWN、ZOOMIN:MS>MCU、ZOOMOUT:MCU>MS、ORBIT:R:45）九條 I2VA 路線

- 原因：維護者指示把 H3 I2VA 生產驗證剩下的 27 支（九條路線 × seed 1001–1003）一次跑完：送出前把首幀、spec、prompt sha、validator、PASS／PARTIAL／FAIL 門檻
    全部預登記並凍結；不得因前一組結果修改 Camera Core、Wrapper、prompt、補 clarifier、改首幀、改 validator 門檻或停下等批准；validator 有缺陷記 RULE_DEFECT、
    歷史 seed 不事後重判。27 支用正式 Camera Core＋正式 I2VA wrapper 原樣生成（skill CL-046、鏡頭文字快照 44863b51bda6a866；mode I2VA、
    generation profile LOCAL_H3_I2VA_PDD8_Q_416），一個指令連續送完；全部生成後才量測與判定。DSL 和 42 格矩陣那九格逐字相同，人物站定。
    validator 的背景點一律只取離人物輪廓 13 px 以上的點（PROD-08 的教訓），門檻全部沿用既有標準，生成前用首幀合成的已知答案片與有人工紀錄的舊片校準（38 項）。
- 修改前：production_shots 到 PROD_08；production_routes 沒有 TRUCK、TILT、PEDESTAL、ZOOMIN、ZOOMOUT、ORBIT；這九個 DSL 在 I2VA 範圍是 UNVERIFIED。
- 修改後：production_shots 新增 PROD_09–PROD_17。每筆：POST_REFACTOR_VALIDATION、CURRENT_CORE_EXACT_MATCH、tested_seeds 3、criteria（各項的正式 PASS 數）、
    mechanism_pass_count、shot_verdict、reliability、failure_behavior（LOW 才有）、repeated／variable failure、limitation、每個 seed 的正式結果／各項／數字／失敗標籤、
    note、input_quality_note、batch、measurement_note、generated_with（skill CL-046＋各自的 prompt sha）。結果（seed 1001／1002／1003）：
    TRUCK:R LOW（PARTIAL／FAIL／FAIL）、TRUCK:L LOW（PARTIAL／PARTIAL／FAIL）、TILT:UP LOW（PASS／FAIL／PARTIAL）、
    TILT:DOWN PRODUCTION_VALIDATED（PASS／PASS／PASS；limitation tilt_amount_uncontrolled：幅度 21–40% 畫面高，2/3 臉出畫）、
    PEDESTAL:UP LOW（PARTIAL／FAIL／FAIL）、PEDESTAL:DOWN LOW（PASS／PARTIAL／FAIL）、ZOOMIN:MS>MCU CONDITIONAL（PARTIAL／PASS／PASS；等比放大 3/3、落幅 2/3）、
    ZOOMOUT:MCU>MS LOW（FAIL／FAIL／FAIL；LANDING_OVERSHOOT 3/3）、ORBIT:R:45 LOW（PASS／PARTIAL／PARTIAL；三條都記 rule_defect：人物輪廓在視角轉了以後蓋不到後腦，
    另有視角目視規則沒涵蓋「轉過頭」的缺口；數字與判定照算出來的留著、沒有重判）。
    production_routes 新增 TRUCK（direction R、L 各一條）、TILT（UP、DOWN）、PEDESTAL（UP、DOWN）、ZOOMIN（起幅 MS、落幅 SPECIFIED MCU）、
    ZOOMOUT（起幅 MCU、落幅 SPECIFIED MS）、ORBIT（direction R、起幅 MS、input 標籤 ms_first_frame_arc_45_degrees）；每條帶 measured_dsl，照既有的範圍規則只套用到完全相符的 DSL。
    profile 檔頭註解：direction 的例子補上 UP／DOWN，並加一行說明路線範圍沒有角度欄位。models/minimax_h3.md：支援表加九列、routing 說明的路線清單加六個指令與一句角度說明、
    「左橫移穩定、右橫移不穩」那句註明是 Ref2VA 矩陣的結果（I2VA 兩個方向都是 LOW）。research/h3_lab_findings.md：新增 H3LAB-PROD-SHOT-09–17。
    先前所有紀錄、路線、等級逐欄比對不變；鏡頭文字與 wrapper 沒動。examples／references／registry／schemas 底下的檔是 --sync 重新產生的，內容和修改前逐字相同（另外產生一份比對過）。
- 已知限制（沒有自行改 routing，留給維護者決定）：production route 的範圍欄位沒有角度。ORBIT 路線只量了 45 度，但 /MS /ORBIT:R:90 或沒寫角度的 /MS /ORBIT:R
    在 I2VA profile 也會顯示這條 LOW；目前用路線標籤（ms_first_frame_arc_45_degrees）與 note 標明只量 45 度。
- 影響 Command：無
- 影響 Adapter：無（adapters.py、h3_wrappers.py、audit.py 一個字都沒動；routing 由 profile 資料驅動）
- 影響 Test：新增 RT-E-34–49（九條路線各自顯示；別的起幅／落幅／方向不套用；Ref2VA 範圍不顯示 I2VA 路線；TRACKSIDE、PAN、DOLLYOUT 的既有路線不受影響）；
    RT-B-01 的輸入由 /MS /TRUCK:L 改成 /MS /ROLL:CW（它檢查「I2VA 沒有證據時不借 Ref2VA 的等級」，TRUCK:L 現在在 I2VA 有路線了；檢查的內容不變）；
    快照新增 10 個輸入（393 → 403，舊的逐字不變）；run_tests 700/700
- 是否破壞 backward compatibility：否（九個 DSL 在 I2VA profile 的 routing 由 UNVERIFIED 變成顯示各自的 production route；鏡頭文字不變）
- 檔案：CHANGELOG.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, research/h3_lab_findings.md, schemas/examples.yaml, tests/h3_routing.md, tests/snapshots/minimax_h3_core.json

## CL-046 · 2026-10-01 · PROD-08 登記：I2VA 的 LEAD（/MFS，正面膝上首幀）＝LOW（1 PASS／1 PARTIAL／1 FAIL；機制大致成立、人物與相機的速度配合不準）

- 原因：維護者要建立 forward-follow 對 backward-lead 的方向對照（FOLLOW 已是 LOW），並驗證短劇常用的「人物朝鏡頭走、相機同步後退」。生產鏡頭 08
    （/MFS /LEAD，I2VA，LOCAL_H3_I2VA_PDD8_Q_416，正式 Camera Core＋正式 I2VA wrapper 原樣、不補字；首幀＝同一個庭院的正面膝上幀、沒有前景物）。
    六項分開記錄：subject locomotion、camera backward translation、screen-position stability、subject-scale stability、backward-translation geometry、continuity；
    規則在生成前凍結，並用首幀合成的已知答案片與倒放的 FOLLOW 片校準。seed 1001：預登記的左側地面量測區從第 0 幀就蓋到人物的袖子，中位數量到的是袖子，
    第①項數值 FAIL；照規則停下回報，正式結果保留、不重判（reason preregistered_ROI_contamination）。維護者決定補跑 1002／1003，並在生成前凍結兩件事：
    （1）只改第①項地面流動的取點——原量測區不變、只算離人物輪廓 13 px 以上的地面點、13 px 固定不再調、方向與門檻不變、其他五項不改，並用分層合成的已知答案片校準；
    （2）聚合——seed 1001 的 FAIL 計入，2/3 PASS＝CONDITIONAL、0–1 PASS＝LOW，不可能 PRODUCTION_VALIDATED。
- 修改前：production_shots 沒有 PROD_08；production_routes 沒有 LEAD；LEAD 在 I2VA 範圍是 UNVERIFIED。
- 修改後：production_shots.PROD_08（POST_REFACTOR_VALIDATION、CURRENT_CORE_EXACT_MATCH、tested_seeds 3、shot_verdict pass 1／partial 1／fail 1、reliability LOW、
    failure_behavior VARIABLE；criteria 六項的正式 PASS 數：subject_locomotion 2/3、camera_backward_translation 2/3、screen_position_stability 3/3、
    subject_scale_stability 1/3、backward_translation_geometry 2/3、continuity 3/3；每個 seed 記正式結果、六項、尺度診斷、結尾的人物／近景／遠景尺度與中心漂移；
    seed_1001：formal FAIL、reason preregistered_ROI_contamination、posthoc_diagnostic.corrected_ground_mask.result consistent_forward_walking_motion
    （used_for_the_formal_result false）；aggregation_rule；descriptive_observation「the lead mechanism mostly works, but the subject-camera speed matching is imperfect」
    （維護者的描述，不改任何正式結果）；measurement_note；second_region_note：第②⑤項沿用原近景區（含袖子上的點），seed 1002 有一個檢查點差 0.0003 沒過門檻，
    只記錄、不改判定；generated_with skill CL-045）。production_routes.LEAD 新增 I2VA 路線（start_framing MFS、measured_dsl /MFS /LEAD、reliability LOW、
    failure_behavior VARIABLE、mechanism 六項正式 PASS 數、limitation subject_camera_speed_matching、confidence 1/3 tested seeds PASS, 1 PARTIAL, 1 FAIL）。
    research/h3_lab_findings.md 新增 H3LAB-PROD-SHOT-08；models/minimax_h3.md 支援表加一列、routing 說明的路線清單加 LEAD。
    鏡頭文字（含 LEAD 用字）、wrapper、先前所有判定與等級都沒有動。examples／references／registry／schemas 底下的檔是 --sync 重新產生的，內容和修改前逐字相同（另外產生一份比對過）。
- 影響 Command：無
- 影響 Adapter：無（adapters.py、h3_wrappers.py、audit.py 一個字都沒動；routing 由 profile 資料驅動，LEAD 的路線照既有的起幅／落幅範圍規則套用）
- 影響 Test：新增 RT-E-30–33（/MFS /LEAD 顯示 LOW 路線；/FS /LEAD:A 與 Ref2VA 範圍不套用；FOLLOW 路線不受影響）；快照新增 2 個輸入（391 → 393，舊的逐字不變）；run_tests 684/684
- 是否破壞 backward compatibility：否（/MFS /LEAD 在 I2VA profile 的 routing 由 UNVERIFIED 變成顯示 LOW 的 production route；鏡頭文字不變）
- 檔案：CHANGELOG.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, research/h3_lab_findings.md, schemas/examples.yaml, tests/h3_routing.md, tests/snapshots/minimax_h3_core.json

## CL-045 · 2026-10-01 · 名詞更正：foreground_depth_anchor 改稱 foreground_motion_anchor（physical_depth_geometry NOT_VERIFIED）；只改命名與文件

- 原因：維護者驗收 CL-043／CL-044 時固定一個結論——左側近柱不能再稱為「已驗證的 depth anchor」。它在 Push In（9 條）與 Pull Out（3 條）都往畫面外滑，
    代表它確實能製造前景運動與遮擋變化，但沒有證據證明 H3 是依正確的 3D 深度幾何處理它。文件不可以再暗示「近柱滑動＝已證明真實視差」。
    這是一個只改命名與文件的小 CL：不改 Prompt、不改等級。DOLLYOUT 的兩個 repeated failure 用正式名稱保留，結論限定在實測的範圍。
- 修改前：profile 的路線標籤是 with_foreground_depth_anchor／without_foreground_depth，欄位 foreground_depth_anchor；文件稱它 foreground depth anchor；
    PROD_07 的標籤是 FOREGROUND_MOVES_OUTWARD；沒有寫 DOLLYOUT 結論的適用範圍。
- 修改後：profile 新增 definitions.foreground_motion_anchor（description：A near-camera foreground object used to provide visible occlusion and
    differential foreground motion；physical_depth_geometry NOT_VERIFIED；former_term foreground_depth_anchor；evidence；consequence）。路線標籤改成
    with_foreground_motion_anchor／without_foreground_motion_anchor，欄位改名 foreground_motion_anchor，三條有錨點的路線（DOLLYIN 兩條、DOLLYOUT）加
    physical_depth_geometry NOT_VERIFIED。PROD_07：repeated_failure 改成 FOREGROUND_PARALLAX_DIRECTION_WRONG、LANDING_OVERSHOOT（各 3/3，另記 repeated_failure_counts），
    新增 scope_note——只適用 I2VA、LOCAL_H3_I2VA_PDD8_Q_416、MCU→MS、這張帶 foreground motion anchor 的首幀，不泛化成「H3 所有 Pull Out 都不行」；
    DOLLYOUT 路線的 limitation 與 note 同步。PROD_01、PROD_02_R2 的 input 描述只換名詞。
    DOLLYIN 的結果完全保留：PARALLAX_ASSISTED_PUSH_IN、physical_fidelity PARTIAL、PRODUCTION_VALIDATED／CONDITIONAL，每一條路線的等級、狀態、範圍欄位、
    evidence 文字逐欄比對不變。models/minimax_h3.md 支援表換名詞並加一段名詞定義；research/h3_lab_findings.md 四列換名詞、H3LAB-PROD-SHOT-07 加範圍與正式標籤
    （H3LAB-PROD-SHOT-02 保留「當時稱為 foreground depth anchor」這個歷史說明）。CHANGELOG 舊條目、凍結的實測矩陣檔與判定都沒有動。
- 影響 Command：無
- 影響 Adapter：無（adapters.py、h3_wrappers.py、audit.py 一個字都沒動；routing 顯示的路線標籤來自 profile 資料，跟著改名）
- 影響 Test：RT-E 與 MS-H3-24 的 regex 只換標籤名稱；新增 RT-E-29（routing 不再出現舊名詞，結果名稱與等級不變）；快照不變；run_tests 680/680
- 是否破壞 backward compatibility：否（routing 文字裡的路線標籤改名：with_foreground_depth_anchor → with_foreground_motion_anchor、
    without_foreground_depth → without_foreground_motion_anchor）
- 檔案：CHANGELOG.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, research/h3_lab_findings.md, tests/h3_routing.md, tests/model_adapters.md

## CL-044 · 2026-10-01 · 42 格矩陣的查表加入景別 scope：只套用到實測的起幅（與落幅），其他景別 UNVERIFIED＋相近證據

- 原因：維護者決定 42 格 Ref2VA evidence routing 也要加景別 scope，和 CL-042 的 production evidence 原則一致——已有證據顯示 shot size／人物大小會影響鏡頭行為
    （PAN:R 在 Ref2VA 小人物構圖和 I2VA 中景大人物表現完全不同），不能只靠 command＋direction。lookup key 至少是
    mode＋generation_profile＋command＋direction＋start_shot_size；實測 DSL 有 end_shot_size 的也必須 exact match；不相符＝UNVERIFIED，
    可以列 related evidence、但不得套用 grade。不得修改歷史 grade、歷史 verdict、Camera Core、Wrapper、Prompt wording。
- 修改前：矩陣五張表（viewpoint／focus／lens／continuity／camera_motion）的列只用指令與方向當 key，不看景別：/FS /PAN:R 會顯示 /MS /PAN:R 那一格的 B、
    /MS /EYELEVEL 會顯示 /FS /EYELEVEL 那一格的 D、/MS /DOLLYIN（沒有落幅）會顯示 MS>MCU 那一格的 D；Ref2VA 的 text_only 路線也不分景別。
- 修改後：42 列各自多了 start_framing（景別代碼），dsl 有落幅的 6 列再多 end_size（DOLLY-IN、DOLLY-OUT、ZOOM-IN、ZOOM-OUT 與兩格 COMBO）；
    欄位由每一列自己的 dsl 解析而來，grade、cell、dsl、四項分數、prompt_compatibility 逐欄不變。routing 查表命中之後再比範圍：
    起幅（運鏡的 start_position，沒有就用景別）要相同、落幅要相同（兩邊都沒有也算相同）才顯示該列的等級；不相符時不顯示等級，改顯示一行
    「PAN:R: no row measured under this scope for start framing FS — UNVERIFIED; related evidence (not applied): /MS /PAN:R = B (historical, H3R-PAN-R)」
    （中文：PAN:R：這個範圍沒有量過 起幅 FS——UNVERIFIED；相近證據（不套用）：/MS /PAN:R = B（歷史，H3R-PAN-R）），並列進 UNVERIFIED；
    相近證據標明是 historical 還是 current。機位／對焦／鏡頭光學／連戲的列與固定鏡頭用「shot size」描述範圍。
    Ref2VA 的兩條 text_only 路線補上實測範圍（DOLLYIN：MS、SPECIFIED、MCU、/MS /DOLLYIN:MS>MCU；PAN：MS、measured_dsl 列出 /MS /PAN:R 與 /MS /PAN:L），
    和 CL-042 的 I2VA 路線同一套規則。稽核：矩陣每一列的 start_framing／end_size 必須等於它自己的 dsl 解析結果（缺欄位也擋）；路線的 measured_dsl 可以是清單。
    models/minimax_h3.md 的路由說明、PROJECT_GOAL.md 的 Reality profile 條目、profile 檔頭註解同步。
    沒有動任何 grade、verdict（判定雜湊不變）、鏡頭文字、wrapper、提示詞用字。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照既有 388 個輸入與 20 個 wrapper 提示詞逐字相同）；只有 routing：矩陣列與 Ref2VA text_only 路線依起幅／落幅完全相符才套用，
    新增矩陣列的「相近證據（不套用）」一行
- 影響 Test：改寫 7 列（RT-D-04、RT-E-12、RT-E-21、RT-F-05、MS-H3-19、MS-H3-21、MS-H3-22：原本在實測景別以外的景別拿到等級，現在改成檢查 UNVERIFIED＋相近證據）；
    新增 RT-K-01–08、MS-H3-36、MS-H3-37（原本那幾列要驗的事，改用實測景別驗）；快照新增 3 個輸入（388 → 391，舊的逐字不變）；run_tests 679/679
- 是否破壞 backward compatibility：否（routing：Ref2VA 下景別或落幅和該格實測不同的查詢，原本會顯示那一格的等級，現在顯示 UNVERIFIED＋相近證據）
- 檔案：CHANGELOG.md, PROJECT_GOAL.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, scripts/adapters.py, scripts/audit.py, tests/h3_routing.md, tests/model_adapters.md, tests/snapshots/minimax_h3_core.json

## CL-043 · 2026-10-01 · PROD-07 登記：I2VA 的 DOLLYOUT（MCU>MS＋近景錨點）＝LOW（0/3；近景物往外滑 3/3、落幅拉過頭 3/3）

- 原因：維護者要驗證反方向——「指定落幅＋depth anchor」是只對 Push In 有效，還是 Pull Out 也能形成可靠路線。生產鏡頭 07
    （/MCU /EYELEVEL /DOLLYOUT:MCU>MS，I2VA，LOCAL_H3_I2VA_PDD8_Q_416，正式 Camera Core＋正式 I2VA wrapper 原樣；首幀＝PROD_02_R2 seed 1001 的落幅幀
    ＋和 PROD_02 同一個近柱圖層）。判定規則是 Push In 規則的鏡像（門檻相同），生成前凍結，並用倒放的 Push In 片與首幀圖層合成的已知答案片校準。
    seed 1001 FAIL 後停下回報；維護者決定同條件補跑 1002／1003，補跑前凍結「落幅不可拉過頭」的規則（直接用既有景別標準：中景＝全身高 ≥ 1.5 畫面高，
    不另外發明百分比）與近景物方向標籤；seed 1001 不重判（② 記 historical formal result＝PASS、note＝overshoot observed / criterion gap）。
- 修改前：production_shots 沒有 PROD_07；production_routes 沒有 DOLLYOUT；DOLLYOUT 在 I2VA 範圍是 UNVERIFIED。
- 修改後：production_shots.PROD_07（POST_REFACTOR_VALIDATION、CURRENT_CORE_EXACT_MATCH、tested_seeds 3、shot_verdict fail 3、reliability LOW、
    failure_behavior REPEATED、repeated_failure FOREGROUND_MOVES_OUTWARD／LANDING_OVERSHOOT；foreground_parallax_direction expected inward／observed outward／
    repeated 3/3；landing_overshoot 3/3（結尾膝上級／全景／全景，全身高 1.2／0.943／0.994 畫面高，1.7–2.5 秒就經過中景大小）；
    mechanism 起幅保留 3/3、後退且人物比遠景變得快 3/3、人物站定 3/3、落幅到位 0/3、近景物往內 0/3；每個 seed 記正式結果、未成立的項目、結尾尺度與景別級、
    近景物出畫時間；continuity_note：首幀看不到腰，模型每條畫出不同的腰帶；interpretation_note：同一根近柱在 9 條 Push In 也是往外滑，
    所以它的滑出不是「依深度算出視差」的證據；generated_with skill CL-042）。
    production_routes.DOLLYOUT 新增 I2VA 路線（start_framing MCU、end_framing SPECIFIED、end_size MS、measured_dsl、reliability LOW、failure_behavior REPEATED、
    limitation landing_overshoot, foreground_moves_outward、physical_fidelity LOW）。DOLLYIN 兩條近景錨點路線各加一個 related_finding 欄位指向 PROD_07
    （等級、文字、狀態完全不動）。research/h3_lab_findings.md 新增 H3LAB-PROD-SHOT-07；models/minimax_h3.md 支援表加一列。
    鏡頭文字、wrapper、pull-out 用字、先前所有判定與等級都沒有動。
- 影響 Command：無
- 影響 Adapter：無（routing 由 profile 資料驅動；鏡頭文字與快照既有輸入不變）
- 影響 Test：新增 RT-E-25–28；快照新增 3 個輸入（385 → 388，舊的逐字不變）；run_tests 669/669
- 是否破壞 backward compatibility：否
- 檔案：CHANGELOG.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, research/h3_lab_findings.md, tests/h3_routing.md, tests/snapshots/minimax_h3_core.json

## CL-042 · 2026-10-01 · Production route 的證據範圍加上起幅與落幅：只套用到完全相同的 start／end，其他組合 UNVERIFIED＋相近證據

- 原因：維護者驗收 CL-041 時指出 routing scope 還不夠嚴格——/DOLLYIN:MS>MCU 的 3/3 只證明 start＝MS、end＝MCU，不能支援 /MS /DOLLYIN:MS>CU、
    /MS /DOLLYIN:MS>ECU、/FS /DOLLYIN:FS>MS；CL-041 只分「有沒有寫落幅」，別的落幅也會顯示 PRODUCTION_VALIDATED（只在 confidence 文字印出實測 DSL）。
    原則和先前修 mode＋profile＋direction 相同，現在再加 start framing＋end framing 作為 evidence scope：可以顯示「有相近 evidence」，
    但不能把等級套到不同的起幅／落幅。
- 修改前：production route 依 mode＋generation profile＋direction＋end_framing（FREE／SPECIFIED）篩選；I2VA 的路線沒有記起幅，
    /FS /TRACKSIDE:R、/FS /PAN:R、/MS /DOLLYIN:MS>CU 都會顯示 MFS／MS／MS>MCU 那一輪的等級。
- 修改後：路線可以帶 start_framing、end_framing、end_size、measured_dsl；routing 只把路線套用到每一個欄位都相符的運鏡
    （起幅＝運鏡的 start_position，沒有就用景別）。同一 mode＋profile＋方向下有量過、但起幅或落幅不同時：不顯示任何等級，
    多一行「no production route measured under this scope for MS>CU — UNVERIFIED; related evidence (not applied): /MS /EYELEVEL /DOLLYIN:MS>MCU」
    （中文：這個範圍沒有量過 MS>CU——UNVERIFIED；相近證據（不套用）：…），並照舊列進 UNVERIFIED；相近證據優先列同一種落幅型態的路線，只列實測 DSL、不列等級。
    profile：I2VA 的六條路線補上實測範圍（資料來源是各自的 production shot，等級與文字一個字都沒改）——DOLLYIN without_foreground_depth
    （MS、SPECIFIED、MCU、/MS /EYELEVEL /DOLLYIN:MS>MCU）、DOLLYIN 近景錨點 FREE（MS、/MS /DOLLYIN）、DOLLYIN 近景錨點 SPECIFIED（MS、MCU）、
    PAN（R、MS、/MS /PAN:R）、TRACKSIDE（R、MFS、/MFS /TRACKSIDE:R）、FOLLOW（MFS、/MFS /FOLLOW）；CL-041 的欄位 dsl 改名 measured_dsl。
    Ref2VA 的 text_only 路線沒有加範圍欄位，照舊對所有景別顯示（42 格矩陣的查表本來就只看指令與方向，這次沒有動，另行請維護者決定）。
    稽核：start_framing／end_size 必須是景別代碼、end_size 只能配 SPECIFIED、有範圍欄位就要有 measured_dsl，而且把 measured_dsl 解析後
    方向／起幅／落幅／落幅型態要和欄位一致。PROJECT_GOAL.md 的 Reality profile 條目補一句這個原則；models/minimax_h3.md 的路由說明同步。
    鏡頭文字、wrapper、任何判定與等級都沒有動。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照既有 380 個輸入與 20 個 wrapper 提示詞逐字相同）；只有 routing：production route 依起幅／落幅完全相符才套用，
    新增「相近證據（不套用）」一行
- 影響 Test：RT-E-11 改（沒有落幅的查詢不再顯示用落幅量的 without_foreground_depth 路線）；新增 RT-E-16–24；快照新增 5 個輸入（380 → 385，舊的逐字不變）；
    run_tests 665/665
- 是否破壞 backward compatibility：否（routing：I2VA 下起幅或落幅和實測不同的查詢，原本會顯示那條路線的等級，現在顯示 UNVERIFIED＋相近證據）
- 檔案：CHANGELOG.md, PROJECT_GOAL.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, scripts/adapters.py, scripts/audit.py, tests/h3_routing.md, tests/snapshots/minimax_h3_core.json

## CL-041 · 2026-10-01 · PROD-02-R2 登記＋DOLLYIN 拆成兩條路線：沒有落幅（PROD_06）與指定落幅（PROD_02_R2），互不覆蓋

- 原因：維護者定案——PROD_06 回答的是 /MS /DOLLYIN（沒有落幅），保留、不重判，但不能取代 PROD_02 的「指定落幅 Dolly」證據；CL-040 把兩者併在同一條
    with_foreground_depth_anchor 路線，會讓 /DOLLYIN:MS>MCU 的查詢顯示沒有落幅那一輪的結果。另開 current-core revalidation
    H3R-PROD-MS-DOLLYIN-MSTOMCU-R2：DSL 逐字用舊 PROD_02 的 /MS /EYELEVEL /DOLLYIN:MS>MCU，同首幀、同近景深度錨點、同 seed 1001–1003、
    同模型／PDD／解析度／幀數，唯一差異是 compiler／wrapper（舊的一句推鏡句 → 正式 Core 的三句）。判定沿用 PROD_02 五項，機制門檻直接用 PROD_06 凍結的
    量測程式（未修改），落幅檢查（最後一幀腰帶出畫＝胸上）與聚合（3 PASS＝PRODUCTION_VALIDATED、2＝CONDITIONAL、0–1＝LOW）在生成前寫進預登記；
    用 skill CL-040 生成，生成前沒有改任何東西。
- 修改前：production_shots 沒有 PROD_02_R2；production_routes.DOLLYIN 的 I2VA 近景錨點路線只有一條（PROD_06 的結果，confidence 文字提到 PROD_02）；
    路線只依 mode＋profile＋direction 篩選，不分有沒有落幅。
- 修改後：production_shots.PROD_02_R2（POST_REFACTOR_VALIDATION、CURRENT_CORE_EXACT_MATCH、tested_seeds 3、shot_verdict pass 3、
    result PARALLAX_ASSISTED_PUSH_IN、reliability PRODUCTION_VALIDATED、visual_usability HIGH、physical_fidelity PARTIAL；mechanism 起幅保留／落幅到位／
    人物站定／近柱快於人物／人物快於遠景各 3/3；每個 seed 記結尾尺度、落幅到位時間、近柱出畫時間與成對標籤，並列同 seed 的 PROD_02、PROD_06 人物結尾倍率；
    landing_adherence：R2 1.38／1.503／1.53，PROD_02 1.378／1.497／1.575，PROD_06（沒有落幅）1.301／1.408／1.286，到 MCU 3/3）。
    結論（生成前寫死的句子）：明確落幅在 Current Core 下把推近拉回指定終點，plain /DOLLYIN 與 /DOLLYIN:MS>MCU 是兩種不同的 production behavior。
    事實記錄：1001、1002 幾乎和舊片相同；1003 舊片是人物和背景一起放大（PARTIAL），R2 分開（1.53 對 1.036）；只有 3 個 seed，不宣稱新寫法讓機制變好。
    遠牆三條都幾乎不放大（1.001／1.016／1.036），所以物理真實度仍是 PARTIAL、名稱仍是 PARALLAX_ASSISTED_PUSH_IN。
    production_routes.DOLLYIN 的近景錨點路線拆成兩條：end_framing FREE（dsl /MS /DOLLYIN，PROD_06，CONDITIONAL，等級與 CL-040 完全相同）與
    end_framing SPECIFIED（dsl /MS /EYELEVEL /DOLLYIN:MS>MCU，PROD_02_R2，PRODUCTION_VALIDATED，historical_evidence PROD_02）；PROD_06 與先前所有紀錄逐欄不變。兩條的 confidence 文字都寫出量測用的 DSL（routing 那一行看得到：指定落幅只量過 MS>MCU）。
    routing：路線帶 end_framing 時只顯示給同一種推拉（有沒有寫落幅），沒有帶的照舊兩種都顯示；without_foreground_depth 與 Ref2VA 路線沒有動。
    稽核：end_framing 只能是 FREE／SPECIFIED。research/h3_lab_findings.md 新增 H3LAB-PROD-SHOT-02-R2；models/minimax_h3.md 支援表把該列拆成兩列，
    並寫明路線依方向與落幅套用。鏡頭文字、wrapper、push 用字都沒有動。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照既有 379 個輸入與 20 個 wrapper 提示詞逐字相同）；只有 routing：production route 多一個 end_framing 篩選
- 影響 Test：RT-E-02、RT-E-11 改成檢查各自的路線且不出現另一條的證據；新增 RT-E-13、RT-E-14、RT-E-15；快照新增一個輸入 /MS /DOLLYIN:SLOW
    （379 → 380，舊的逐字不變）；run_tests 656/656
- 是否破壞 backward compatibility：否（routing：/DOLLYIN 有寫落幅時，I2VA 近景錨點路線改顯示 PROD_02_R2 的結果，不再顯示 PROD_06 的結果）
- 檔案：CHANGELOG.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, research/h3_lab_findings.md, scripts/adapters.py, scripts/audit.py, tests/h3_routing.md, tests/snapshots/minimax_h3_core.json

## CL-040 · 2026-10-01 · PROD-06 登記：I2VA 近景深度錨點的 DOLLYIN 有了 current-core 證據（2 PASS＋1 PARTIAL＝CONDITIONAL）

- 原因：維護者要把「DOLLYIN＋近景深度錨點」這條路線從舊 wording／PROVISIONAL 升級成 current-core evidence。生產鏡頭 06（/MS /DOLLYIN，I2VA，
    LOCAL_H3_I2VA_PDD8_Q_416，沿用 PROD_02 的首幀，正式 Camera Core＋正式 I2VA wrapper 原樣、不補字）跑了 seed 1001–1003。Dolly 五項的數值規則、
    局部尺度診斷（near_scale／subject_scale／far_scale）、聚合規則都在生成前凍結並寫進實驗室預登記，先用舊 PROD_02 三條校準（重現 PASS／PASS／PARTIAL）；
    看片後沒有改任何門檻。不修改 Adapter、Wrapper、正式 push 用字。
- 修改前：production_shots 沒有 PROD_06；production_routes.DOLLYIN 的 with_foreground_depth_anchor 路線是 PROVISIONAL＋PRE_REFACTOR_WORDING
    （applicable_to_current_core UNVERIFIED），只靠 PROD_02。
- 修改後：production_shots.PROD_06（POST_REFACTOR_VALIDATION、CURRENT_CORE_EXACT_MATCH、tested_seeds 3、shot_verdict pass 2／partial 1／fail 0、
    result PARALLAX_ASSISTED_PUSH_IN、reliability CONDITIONAL、visual_usability HIGH、physical_fidelity PARTIAL、limitation far_layer_scaling_inconsistent；
    mechanism push_in 3/3、near_layer_faster_than_subject 3/3、subject_faster_than_far_background 2/3；每個 seed 記正式結果、人物與遠景的結尾尺度、
    近柱出畫時間與當時的尺度下限、兩組成對標籤；generated_with skill CL-039）。三條：人物 1.30／1.41／1.29，遠景 1.00（凍結）／1.12／1.31（和人物一起放大），
    近柱 2.6／0.6／1.4 秒滑出（都遠快於等比放大）；1003 是 ZOOM_LIKE_BEHIND_FOREGROUND，型態和 PROD_02 的 1003 相同。
    production_routes.DOLLYIN 的 with_foreground_depth_anchor 路線改成 POST_REFACTOR_VALIDATION＋CURRENT_CORE_EXACT_MATCH，confidence 同時寫明
    「PROD_06 的 DSL 沒有落幅；有落幅的只有 pre-refactor 的 PROD_02」；without_foreground_depth 路線沒有重測，維持 PROVISIONAL。
    事實記錄（dsl_note／end_framing_note）：PROD_06 的 DSL 是維護者寫的 /MS /DOLLYIN，比 PROD_02 的 /MS /EYELEVEL /DOLLYIN:MS>MCU 少平視句與落幅句，
    所以不是單一變數對照；推近幅度比 PROD_02 小（用同一支程式重量：1.38／1.50／1.58），胸上構圖 2/3，不歸因到單一原因。
    research/h3_lab_findings.md 新增 H3LAB-PROD-SHOT-06；models/minimax_h3.md 支援表更新該列，並把「I2VA 路線每一行都標 PROVISIONAL」那句改成符合現況
    （DOLLYIN、PAN、TRACKSIDE、FOLLOW 各自顯示自己的狀態）。鏡頭文字、wrapper、push 用字都沒有動。
- 影響 Command：無
- 影響 Adapter：無（routing 由 profile 資料驅動；鏡頭文字與快照既有輸入不變）
- 影響 Test：RT-E-02 改成檢查新的狀態（POST_REFACTOR_VALIDATION、confidence 寫明沒有落幅）；新增 RT-E-11、RT-E-12；快照新增一個輸入 /MS /DOLLYIN
    （378 → 379，舊的逐字不變）；run_tests 653/653
- 是否破壞 backward compatibility：否
- 檔案：CHANGELOG.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, research/h3_lab_findings.md, tests/h3_routing.md, tests/snapshots/minimax_h3_core.json

## CL-039 · 2026-10-01 · PROD-05 登記：I2VA 背後跟拍 FOLLOW＝LOW（0/3；人物走遠變小 3/3，攝影機行為 VARIABLE）

- 原因：生產鏡頭 05（/MFS /FOLLOW，I2VA，LOCAL_H3_I2VA_PDD8_Q_416，正式 Camera Core 原樣）seed 1001 機制錯誤；維護者決定同條件補跑 1002、1003，
    並在生成前凍結一個輔助診斷（近景與遠景的尺度變化比較），聚合規則也事先給定：兩條都 PASS 才是 CONDITIONAL，否則 LOW，不可能 PRODUCTION_VALIDATED；
    另外記錄失敗型態是否一致。不修改 Adapter、Wrapper、正式 FOLLOW wording。
- 修改前：production_shots 沒有 PROD_05；production_routes 沒有 FOLLOW；FOLLOW 在 I2VA 範圍是 UNVERIFIED。
- 修改後：production_shots.PROD_05（POST_REFACTOR_VALIDATION、CURRENT_CORE_EXACT_MATCH、tested_seeds 3、shot_verdict pass 0／fail 3、reliability LOW、
    failure_behavior VARIABLE、repeated_failure SUBJECT_RECEDES／SUBJECT_SCALE_LOSS；每個 seed 記正式結果、未成立的項目、輔助診斷、人物與近／遠景的結尾尺度、
    失敗型態標籤；mechanism subject_walks_forward 3/3、camera_forward_translation 1/3、subject_size_held 0/3；input_quality_note derived_frame／
    crop_and_1.6x_resize／soft_first_frame；generated_with skill CL-038）。三條的人物結尾尺度 0.652／0.706／0.735（膝上變全身）；
    攝影機：1001 幾乎不動（背景均勻放大 1.09）、1002 真的前進（近處地面 1.51、遠牆 1.09）但比她慢、1003 像變焦（1.26，近＝遠）。
    production_routes.FOLLOW 新增 I2VA 路線（reliability LOW、failure_behavior VARIABLE、limitation subject_scale_loss）。
    量法註記：預登記的第⑤項（近／遠像素流速比）分不出前進與變焦，沒有事後改；輔助診斷在 1002／1003 生成前凍結，seed 1001 的正式結果沒有重判。
    research/h3_lab_findings.md 新增 H3LAB-PROD-SHOT-05；models/minimax_h3.md 支援表加一列。鏡頭文字、wrapper、FOLLOW 用字都沒有動。
- 影響 Command：無
- 影響 Adapter：無（routing 由 profile 資料驅動；鏡頭文字與快照既有輸入不變）
- 影響 Test：新增 RT-E-09、RT-E-10；快照若有新測試輸入則重凍（舊的不變）；run_tests 651/651
- 是否破壞 backward compatibility：否
- 檔案：CHANGELOG.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, research/h3_lab_findings.md, schemas/examples.yaml, tests/h3_routing.md, tests/snapshots/minimax_h3_core.json

## CL-038 · 2026-10-01 · PROD-04 登記：I2VA 側跟拍 TRACKSIDE:R＝PRODUCTION_VALIDATED（附位置漂移限制）

- 原因：生產鏡頭 04（/MFS /TRACKSIDE:R，I2VA，LOCAL_H3_I2VA_PDD8_Q_416，正式 Camera Core 原樣、seed 1001–1003）機制 3/3 成立：人物向右走、
    相機同步橫移、背景近快遠慢地往左滑；位置穩定 1 PASS、2 PARTIAL。維護者定案登記為 Post-refactor Production Evidence：TRACKSIDE 機制記
    PRODUCTION_VALIDATED，但不把整體寫成 3/3 完美，正式限制是「相機與人物速度匹配有 seed 敏感性，人物可能逐漸往畫面一側漂移」。
- 修改前：production_shots 沒有 PROD_04；production_routes 沒有 TRACKSIDE；路線不分方向（量過 PAN:R 的結果也會顯示在 PAN:L）；
    I2VA 證據區塊整塊標 PROVISIONAL。
- 修改後：production_shots.PROD_04（command TRACKSIDE_R、shot_size MFS、mode I2VA、generation_profile、evidence_status POST_REFACTOR_VALIDATION、
    tested_seeds 3、mechanism camera_side_tracking／subject_walk_direction／background_parallax 各 3/3、shot_verdict pass 1＋
    basic_usable_with_partial_position_drift 2、reliability PRODUCTION_VALIDATED、limitation subject_screen_position_drift、
    input_quality_note derived_frame／crop_and_2x_resize／soft_first_frame；另記量測數字與生成版本）。
    production_routes.TRACKSIDE 新增 I2VA 路線（direction R、PRODUCTION_VALIDATED、mechanism 3/3、limitation、CURRENT_CORE_EXACT_MATCH）；
    PAN 的 I2VA 路線補 direction R。routing：路線有 direction 時只套用到同方向，另一方向顯示「這個範圍只量過方向 R」並列為 UNVERIFIED；
    路線行多顯示 mechanism 與 limitation；I2VA 證據區塊改標 MIXED（同時有 PROVISIONAL 與 POST_REFACTOR_VALIDATION 的紀錄），
    每個項目顯示自己的狀態。research/h3_lab_findings.md 新增 H3LAB-PROD-SHOT-04；models/minimax_h3.md 支援表加一列。
    鏡頭文字、wrapper、歷史判定都沒有動。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照既有輸入逐字相同）；只有 routing 顯示（方向限定、MIXED、mechanism／limitation）
- 影響 Test：修改 RT-B-01、RT-Z-04；新增 RT-E-05–08；快照重凍（多新測試輸入，舊的不變）；run_tests 649/649
- 是否破壞 backward compatibility：否（routing：I2VA 區塊狀態由 PROVISIONAL 改顯示 MIXED；PAN:L 在 I2VA 不再顯示 PAN:R 的結果）
- 檔案：CHANGELOG.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, research/h3_lab_findings.md, schemas/examples.yaml, scripts/adapters.py, tests/h3_routing.md, tests/snapshots/minimax_h3_core.json

## CL-037 · 2026-10-01 · wrapper bug：句首的主體名稱要大寫（Base modes）

- 原因：準備生產鏡頭 04（/MFS /TRACKSIDE:R，I2VA）時，正式 wrapper 產出的提示詞有一句以小寫開頭：「the young woman stays about the same size …」。
    Camera Core 的句子以 {SUBJECT} 開頭時，wrapper 直接把呼叫端的主體名稱（小寫開頭）代進去，沒有處理句首。這是 wrapper 的格式 bug，不是補字；
    在生成前修掉，避免用有瑕疵的提示詞產生證據（之後再修就會變成和正式輸出不相符的舊用字）。
- 修改前：h3_wrappers._fill 在 Base modes 一律原樣代入主體名稱；以 {SUBJECT}／{A}／{B} 開頭的句子（側跟拍的「{SUBJECT} stays about the same size …」、
    環繞的「{SUBJECT} stays in place …」、跟拍的「{SUBJECT}'s … stays inside the frame …」）句首變成小寫。
- 修改後：主體名稱出現在句首（文字開頭或句號／問號／驚嘆號之後）時第一個字母大寫，句中不變；Ref2VA 的 <Subject N> 不受影響。
    Camera Core 的用字、四層、wrapper 結構都沒有改。
- 影響 Command：無
- 影響 Adapter：無（Camera Core 文字不變）；wrapper 的 Base modes 輸出只有句首大小寫改變
- 影響 Test：新增 WRAP-BASE-05、WRAP-REF-05；快照重凍（多一個 wrapper 測試輸入，既有的逐字相同）；run_tests 645/645
- 是否破壞 backward compatibility：否（只有以主體名稱開頭的句子首字母由小寫變大寫）
- 檔案：CHANGELOG.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, schemas/examples.yaml, scripts/h3_wrappers.py, tests/h3_wrappers.md, tests/snapshots/minimax_h3_core.json

## CL-036 · 2026-10-01 · H3LAB-PAN-NEGATIVE-CLARIFIER-01 登記＋42 格提示詞相容性（17 格 current-core、25 格歷史證據）

- 原因：Core-only ablation 證實在 PAN:R／I2VA／MS／LOCAL_H3_I2VA_PDD8_Q_416 下，獨立成句的「The camera stays in place.」會壓掉運動幅度（3/3），
    但拿掉後仍不是真正的搖（0/3）。維護者選 A：只登記，不改 Adapter／Wrapper／正式 PAN wording，不改任何歷史 verdict／grade；並要求把 42 格逐格標
    prompt_compatibility——同一語義換一種拆句，H3 行為可能明顯不同，用重構前句子量的等級不能再當作目前 Core 的實測結果。不重跑 25 格、
    不開新的 prompt ablation；之後採 production-driven validation。
- 修改前：42 格等級在 profile 與 routing 都被當作目前 Core 的 measured grade；ablation 的發現沒有登記在 skill 裡。
- 修改後：（1）profile 的 I2VA 證據區新增 lab_findings.H3LAB_PAN_NEGATIVE_CLARIFIER_01（scope：mode I2VA、generation_profile LOCAL_H3_I2VA_PDD8_Q_416、
    shot_size MS、command PAN_R；finding negative_clarifier_interference VERIFIED；evidence independent_sentence motion_suppressed、
    core_only motion_restored＋pan_semantics FAIL；adapter_action.change_output false）；PAN 的 I2VA 路線維持 reliability LOW、failure_behavior VARIABLE，只加 related_finding。
    （2）逐格比對「當時送出的提示詞（片子內嵌）」與「現在正式 Core 對該格 DSL 寫出的鏡頭句」：17 格 CURRENT_CORE_EXACT_MATCH（STATIC、ROLL 兩格、機位 7 格、
    TRK-SIDE 兩格、FOC-RACK、NEG-WIDEANGLE、SB-S1／S2、CMB-FS-GROUND-SIDE）、25 格 PRE_REFACTOR_WORDING；profile 每列加 prompt_compatibility，
    證據區加 evidence_compatibility（PRE_REFACTOR：historical_grade_valid true、applicable_to_current_core UNVERIFIED）；results.json 每格 provenance 加
    prompt_compatibility、executed_prompt_sha、current_core_text_sha，25 格另列「目前 Core 有、當時提示詞沒有」的句子；production_shots 與相關路線同樣標記。
    grade／verdict／四項一字未動（verdict hash 不變）。（3）routing：PRE_REFACTOR 的列顯示「historical grade … — prompt wording: PRE_REFACTOR;
    current-core applicability: UNVERIFIED」，警告寫 has a historical grade only，不再出現 measured H3_RELIABILITY；路線行加 [pre-refactor prompt wording; …]；中文版同步。
    （4）audit REALITY：每列／每格必須有 prompt_compatibility 且 profile 與 results.json 一致；CURRENT_CORE_EXACT_MATCH 的格會重算目前 Core 文字的 sha，
    Core 用字一改就報錯，要求改標或重驗；lab_findings 的 scope 必須等於所在 profile。（5）10_results.md 由工具重生，多一節「提示詞相容性」；
    research/h3_lab_findings.md 新增 H3LAB-PAN-NEGATIVE-CLARIFIER-01；models/minimax_h3.md、PROJECT_GOAL.md、SKILL.md 補上原則。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照既有輸入逐字相同）；只有 routing 的顯示與警告文字
- 影響 Test：修改 RT-A-01–03、RT-D-04、RT-E-03、RT-Z-03、MS-H3-20、MS-H3-22；新增 RT-H-01–07；快照重凍（多新測試輸入，舊的不變）；run_tests 643/643
- 是否破壞 backward compatibility：否（routing 對 25 格的顯示由 measured 改為 historical；profile 每列多 prompt_compatibility 欄位）
- 檔案：CHANGELOG.md, PROJECT_GOAL.md, SKILL.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, research/h3_lab_findings.md, schemas/examples.yaml, scripts/adapters.py, scripts/audit.py, tests/h3_routing.md, tests/model_adapters.md, tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/02_angle_height.md, tests/reality/minimax_h3/03_tracking.md, tests/reality/minimax_h3/04_complex_motion.md, tests/reality/minimax_h3/05_focus.md, tests/reality/minimax_h3/06_combinations.md, tests/reality/minimax_h3/07_sequences.md, tests/reality/minimax_h3/08_negative_cases.md, tests/reality/minimax_h3/09_storyboard_cases.md, tests/reality/minimax_h3/10_results.md, tests/reality/minimax_h3/11_crane_validator_v2.md, tests/reality/minimax_h3/12_pedestal_revalidation_v1.md, tests/reality/minimax_h3/results.json, tests/reality/minimax_h3/tools/h3_reality.py, tests/snapshots/minimax_h3_core.json

## CL-035 · 2026-10-01 · PROD-03-R2 登記（Post-refactor Revalidation）：I2VA 中景 PAN 的失敗型態改記 VARIABLE

- 原因：維護者指定乾淨 A/B 重跑 PROD-03（DSL `/MS /PAN:R`、原首幀、seed 1001–1003、模型、PDD、416x736、generation profile
    LOCAL_H3_I2VA_PDD8_Q_416 全部相同，只換正式 H3 Camera Core＋I2VA wrapper）。結果 0/3，但失敗型態從「背景滑、人物鎖住」變成「幾乎不動」。
    維護者定案：R2 寫進 profile、不覆蓋舊 PROD_03；seed 1003 正式判定維持 FAIL（不事後補第④項的 PARTIAL 規則）；
    SUBJECT_LOCKED_BACKGROUND_SLIDE 不再當作 I2VA PAN 的固定失敗型態。
- 修改前：production_shots 只有 PROD_01–03（PROVISIONAL）；production_routes.PAN 的 I2VA 路線記 result SUBJECT_LOCKED_BACKGROUND_SLIDE、PROVISIONAL。
- 修改後：PROD_03 保留（evidence_status PROVISIONAL、verdict FAIL、caveat tested_before_mode_wrapper_audit；欄位 result 改名 failure_mode，值不變）；
    新增 PROD_03_R2（evidence_status POST_REFACTOR_VALIDATION、verdict FAIL、tested_seeds 3、observed_failure NEAR_STATIC_CAMERA／
    INSUFFICIENT_PAN_AMPLITUDE、generation_profile LOCAL_H3_I2VA_PDD8_Q_416；seed 1003 的描述性註記 closest to threshold / partial-like motion）。
    production_routes.PAN 的 I2VA 路線改為 reliability LOW、failure_behavior VARIABLE（不再有固定的 result），confidence 與 evidence 同時列兩次測試。
    routing 的路線行顯示 failure behavior 與 [POST_REFACTOR_VALIDATION]；adapters.EVIDENCE_STATUSES＝MEASURED／PROVISIONAL／POST_REFACTOR_VALIDATION，
    audit REALITY 用它檢查，PROVISIONAL 仍必須有 caveat。research/h3_lab_findings.md 新增 H3LAB-PROD-SHOT-03-R2；models/minimax_h3.md 支援表該列更新。
    兩版提示詞只差一句的拆法（「The camera stays in place and pans right.」→「The camera pans right. The camera stays in place.」）；
    照生成前寫死的解讀規則記「部分改變、不下因果結論」。鏡頭文字、wrapper、歷史判定都沒有動。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照不變）；只有 routing 的路線行多顯示 failure behavior 與狀態
- 影響 Test：修改 MS-H3-25、RT-E-01；run_tests 636/636
- 是否破壞 backward compatibility：否（profile 的 PROD_03 欄位 result 改名 failure_mode；I2VA PAN 路線不再有 result 欄位）
- 檔案：CHANGELOG.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, research/h3_lab_findings.md, schemas/examples.yaml, scripts/adapters.py, scripts/audit.py, tests/h3_routing.md, tests/model_adapters.md

## CL-034 · 2026-10-01 · 一個 generation profile 對一個 mode：LOCAL_H3_PRODUCTION 拆成 _REF2VA 與 _I2VA

- 原因：維護者指出 LOCAL_H3_PRODUCTION 不能同時代表 Ref2VA／I2VA／FL2VA，否則 mode＋generation_profile 又會模糊；Post-refactor 的
    Production Validation 要用明確的 I2VA production profile。
- 修改前：generation_profiles 有 LOCAL_H3_PRODUCTION（mode REF2VA，但 id 沒有寫出 mode）；沒有 I2VA 的 production profile。
- 修改後：LOCAL_H3_PRODUCTION 改名 LOCAL_H3_PRODUCTION_REF2VA（欄位不變：768x1344、ref_image_size match、1–3 張參考圖＋聲音參考、無證據）；
    新增 LOCAL_H3_PRODUCTION_I2VA（mode I2VA、fl2va int8 convrot、PDD FL2VA-Acc-8Step、8 步、euler、CFG 1.0、shift 12/3、768x1344、124 幀、
    一張 768x1344 首幀；和 LOCAL_H3_I2VA_PDD8_Q_416 同一張節點圖，只差解析度；產線自己的工作流檔只有 Ref2VA，所以這個 profile 走實驗室 runner；
    尚無證據）。audit REALITY 新增規則：每個 profile 必須有規格要求的 12 個欄位；LOCAL_ 開頭的 profile 只能有一個 mode，而且 id 要寫出 mode；
    只有本地單一 mode 的 profile 能掛 reality evidence（用舊 id 當壞樣本驗證會被擋）。舊 id LOCAL_H3_PRODUCTION 現在是 unknown profile。
    其他 profile、reality_evidence、production_routes 逐值驗證不變。
- 影響 Command：無
- 影響 Adapter：無（routing 是資料驅動；鏡頭文字與快照不變）
- 影響 Test：修改 RT-B-02（改用 LOCAL_H3_PRODUCTION_REF2VA）；新增 RT-B-05、RT-B-06；run_tests 636/636
- 是否破壞 backward compatibility：是——profile id LOCAL_H3_PRODUCTION 不再存在（改用 LOCAL_H3_PRODUCTION_REF2VA）；其餘不變
- 檔案：CHANGELOG.md, PROJECT_GOAL.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, schemas/examples.yaml, scripts/audit.py, tests/h3_routing.md

## CL-033 · 2026-10-01 · 證據分類修正（focus／lens／continuity 表）＋中文 routing 說明＋--h3-profile 提示

- 原因：維護者定案：RACKFOCUS、WIDEANGLE、storyboard（AXIS+EYELINE+OTS）留在 camera_motion 不合理，要依 registry／IR 的實際定義分類
    （不准只因名稱硬塞）；不指定 profile 維持 UNVERIFIED、CLI 最多補一句提示、不准自動猜；中文 routing 的說明句要翻譯，enum／profile ID 不翻。
    只改 evidence taxonomy、測試、文件；不改 Prompt、不改歷史 grade。
- 修改前：reality_evidence 只有 viewpoint 與 camera_motion 兩張表，RACKFOCUS（registry FOCUS）、WIDEANGLE（registry LENS）、
    AXIS+EYELINE+OTS（CONTINUITY）共 4 列在 camera_motion；routing 查表時同一個 key 只取最後一列（AXIS+EYELINE+OTS 有 H3R-SB-S1 F 與
    H3R-SB-S2 C 兩格，S1 的 DSL 只顯示 S2 的 C）；--lang zh 的範圍說明是英文；沒給 profile 時沒有提示。
- 修改後：models/minimax_h3_profile.yaml 的 LOCAL_H3_REF2VA_PDD8_Q_416 證據分五張表：viewpoint 7、focus 1（RACKFOCUS）、lens 1（WIDEANGLE：
    registry category LENS、IR lens.lens_type WIDE，是鏡頭不是景別）、continuity 2（AXIS+EYELINE+OTS 兩格）、camera_motion 31；歸表規則＝該列
    指令的 registry category（adapters.EVIDENCE_TABLE_OF_CATEGORY），audit REALITY 逐列檢查；42 列的 key／cell／dsl／grade／四項逐值驗證不變。
    routing 查五張表、同 key 的每一列都回報；routing_text 中文版把範圍說明、無證據清單、其他範圍描述翻成中文（UNVERIFIED／PROVISIONAL／MEASURED、
    profile ID、等級、格號不翻）；沒給 generation profile 時區塊最後加一行「Specify --h3-profile to query measured evidence.」
    （中文：「指定 --h3-profile 才會查詢實測證據。」），不設任何預設 profile；h3_wrappers.py 的 --profile 也接受 --h3-profile。
- 影響 Command：無
- 影響 Adapter：鏡頭文字零變動（快照既有 367 條逐字相同）；routing 區塊：focus／lens／continuity 列用自己的標籤、AXIS+EYELINE+OTS 兩格都顯示、
    中文說明、提示行
- 影響 Test：新增 RT-S-03、RT-F-01–05、RT-Z-01–06；快照重凍（多 4 個新測試輸入，舊的不變）；run_tests 634/634
- 是否破壞 backward compatibility：否（只有 routing 輸出的標籤、語言與同 key 多列的顯示改變；鏡頭文字、DSL、IR、等級不變）
- 檔案：CHANGELOG.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, schemas/examples.yaml, scripts/adapters.py, scripts/audit.py, scripts/h3_wrappers.py, scripts/run_tests.py, tests/h3_routing.md, tests/snapshots/minimax_h3_core.json

## CL-032 · 2026-10-01 · H3_REFACTOR_PHASE_2：generation profile 結構化、Reality 證據綁 mode＋profile、provenance 回填、viewpoint 重分類、PROD 標 PROVISIONAL、routing 範圍化

- 原因：維護者批准 Phase 2，只處理 Reality evidence 屬於哪個 mode／generation profile、routing 如何引用它；不碰 Camera Core、wrapper 結構、
    歷史判定與等級、影片、提示詞用字。
- 修改前：profile 只有一個 minimax_h3_ref2va 區塊，等級寫成「H3 PAN:R = B」沒有綁 profile；機位高度／角度 7 格混在 camera_motion；
    results.json 沒有 provenance；PROD-01/02/03 的 I2VA 結果沒有標示是 wrapper 稽核前的證據；routing 不管 mode 一律套 Ref2VA 證據
    （T2VA 也印「Ref2VA text-only shot size reliability LOW」）。
- 修改後：（1）generation_profiles：LOCAL_H3_REF2VA_PDD8_Q_416、LOCAL_H3_I2VA_PDD8_Q_416、LOCAL_H3_PRODUCTION、OFFICIAL_REFERENCE，每個記
    mode／checkpoint／text encoder／accelerator／steps／sampler／cfg／shift／resolution／frames／reference configuration／ref_image_size
    （來源：lab_run.py、lab specs、results.jsonl 126/126 matrix clips sampler pdd8、根因報告的節點稽核、產線工作流；官方指南只記載 prompt 結構與 4–15 秒）；
    沒有任何本地 profile 稱為 H3 default。（2）reality_evidence 以 profile 為 key、每列 by_command 帶 profile；42 格的 key／cell／dsl／grade／四項
    逐值比對不變（產生器重讀舊檔驗證）。（3）results.json 每格回填 provenance（mode、generation_profile、checkpoint、text_encoder、accelerator、
    steps、sampler、cfg、shift、resolution、frames、fps、reference_configuration、spec；從生成該格的 lab spec 讀出），頂層 scope 記 verdict_hash
    （去掉 scope 與 provenance 後的 sha256，等於回填前整檔的 1e88dc33…）、42 格／126 seed；grade、seed verdict、目視、四項、validators 一字未動。
    （4）EYELEVEL、GROUNDLEVEL、GROUNDLEVEL+LOWANGLE、HIGHANGLE+SHOULDERLEVEL、ELEVATED、TOPDOWN、BIRDSEYE 7 列移到 viewpoint 表，等級不變。
    （5）PROD-01/02/03 記進 reality_evidence.LOCAL_H3_I2VA_PDD8_Q_416.production_shots（verdict、tested_seeds、evidence_status PROVISIONAL、
    caveat tested_before_mode_wrapper_audit、generation_profile）；production_routes 每條 route 綁 mode＋generation_profile，I2VA 路線標 PROVISIONAL。
    （6）routing：adapters.h3_scope(h3_mode, h3_profile_id) 決定證據範圍，只讀該 profile 的證據；查 viewpoint 表→camera_motion 表→production_routes；
    沒有證據＝UNVERIFIED，只指出其他範圍有證據、不套用；輸出第一行印範圍與狀態（MEASURED／PROVISIONAL／UNVERIFIED）；CLI --h3-mode／--h3-profile，
    wrapper --profile（wrapper 自動帶 mode）；不給 profile 一律 UNVERIFIED。（7）文件：profile yaml 標頭、models/minimax_h3.md（範圍句、支援表帶 profile、
    routing 節）、10_results.md（工具 report 重生，標頭帶 profile）、01–09／11／12 報告加範圍行、research/h3_lab_findings.md PROD 三列標 PROVISIONAL、
    PROJECT_GOAL.md 狀態、SKILL.md。（8）測試：tests/h3_routing.md 22 列（A 歷史等級、B UNVERIFIED、C T2VA/FL2VA/L2VA 不收 Ref2VA 警告、
    D viewpoint 表、E PROVISIONAL、S 無範圍）；MS-H3-18–25 改為指定 profile；run_tests 新增 h3mode=／profile= 範圍 token、routing[]／norouting[] 斷言、
    凍結快照 tests/snapshots/minimax_h3_core.json（367 條鏡頭文字＋15 份 wrapper prompt，--update-snapshot 重凍）；audit 新增 REALITY 項
    （verdict hash／格數／provenance／profile 一致性／PROVISIONAL 欄位）；tools/h3_reality.py 加 verdict-hash [--check]、新格自動帶 provenance。
- 影響 Command：無（104／244／18 不變）
- 影響 Adapter：鏡頭文字零變動（快照 363 條與 Phase 2 前逐字相同、wrapper 15 份相同）；只有 routing 區塊與 H3 ROUTING 警告改為帶範圍
- 影響 Test：修改 MS-H3-18–25；新增 RT-A-01–04、RT-B-01–04、RT-C-01–05、RT-D-01–04、RT-E-01–03、RT-S-01–02 與快照 2 項；run_tests 622/622
- 是否破壞 backward compatibility：是——routing 的輸出格式與語義改變：不給 --h3-profile（wrapper 不給 --profile）時全部 UNVERIFIED，舊的
    「H3 Ref2VA routing」區塊不再無條件出現；adapters.render 新增參數 h3_mode／h3_profile_id；profile yaml 結構改變（舊 key minimax_h3_ref2va 移除）；
    鏡頭文字、DSL、IR 不變
- 檔案：CHANGELOG.md, PROJECT_GOAL.md, SKILL.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, models/minimax_h3_profile.yaml, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, research/h3_lab_findings.md, schemas/examples.yaml, scripts/adapters.py, scripts/audit.py, scripts/camera_dsl.py, scripts/h3_wrappers.py, scripts/run_tests.py, tests/h3_routing.md, tests/model_adapters.md, tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/02_angle_height.md, tests/reality/minimax_h3/03_tracking.md, tests/reality/minimax_h3/04_complex_motion.md, tests/reality/minimax_h3/05_focus.md, tests/reality/minimax_h3/06_combinations.md, tests/reality/minimax_h3/07_sequences.md, tests/reality/minimax_h3/08_negative_cases.md, tests/reality/minimax_h3/09_storyboard_cases.md, tests/reality/minimax_h3/10_results.md, tests/reality/minimax_h3/11_crane_validator_v2.md, tests/reality/minimax_h3/12_pedestal_revalidation_v1.md, tests/reality/minimax_h3/results.json, tests/reality/minimax_h3/tools/h3_reality.py, tests/snapshots/minimax_h3_core.json

## CL-031 · 2026-10-01 · 定義性參數標記：/CRASHZOOM、/WHIPPAN 的速度（與幅度）不再列為 UNSPECIFIED

- 原因：維護者指出 /CRASHZOOM 的 metadata 列 speed／amount 為 UNSPECIFIED，輸出卻寫 at fast speed，稽核資料前後矛盾；要求只修標記，
    不改輸出文字、不改 DSL，且不混進 Phase 2。
- 修改前：parse 把 CRASHZOOM.speed、CRASHZOOM.amount、WHIPPAN.speed 列進 unspecified；meta.definitional 只收 registry defaults。
- 修改後：scripts/camera_dsl.py 新增 DEFINITION_IMPLIED（CRASHZOOM：speed FAST、amount LARGE；WHIPPAN：speed FAST——依 registry definition
    「A sudden, very fast zoom … that snaps between framings」「A very fast pan」）；這些欄位不進 unspecified，改記在 meta.definitional
    （source COMMAND_DEFINITION）；render() 輸出新增 definition_implied 清單，CLI 在 UNSPECIFIED 後印一行 DEFINITION_IMPLIED；
    run_tests 新增 nounspec=、implied= 斷言。鏡頭文字、四層與 wrapper 完全不變：對照 Phase 1 結案時凍結的快照，357 條鏡頭文字與 15 份
    wrapper prompt 的雜湊相同。
- 影響 Command：無（定義未改，只把定義裡既有的語義做成可讀的標記）
- 影響 Adapter：無文字變動；render 輸出多 definition_implied 欄位
- 影響 Test：新增 MS-H3-33、MS-H3-34、MS-H3-35；run_tests 598/598
- 是否破壞 backward compatibility：否（文字相同；parse／render 的 metadata 多一個欄位、unspecified 少三個鍵）
- 檔案：scripts/camera_dsl.py, scripts/adapters.py, scripts/run_tests.py, tests/model_adapters.md, SKILL.md, README.md, models/minimax_h3.md, CHANGELOG.md, schemas/camera_dsl_schema.yaml, schemas/camera_dsl_schema.md

## CL-030 · 2026-10-01 · H3_REFACTOR_PHASE_1：專案憲章、H3 Camera Core 四層化、參數忠實度、五種 mode wrapper

- 原因：維護者批准依 CL-029 的稽核重構，Phase 1 只做四件事：PROJECT_GOAL.md、H3 Camera Core 分層、參數忠實度修正、H3 mode wrapper 正式進 skill；
    不改 104 指令／244 別名／18 文法、不改歷史 Reality 判定與等級、不生成影片、不重跑矩陣、不做 PAN/TILT 幅度的文法擴充。
- 修改前：H3 轉接器把官方運鏡詞、時間澄清句、派生畫面約束、否定句混成一個不可拆的字串；/PAN:R:45、/TILT:UP:30、/ROLL:CW:15 的度數靜默丟掉；
    /DOLLYIN:…:SLOW 不輸出官方速度詞；/ORBIT:R:FULL 自動加 with large amplitude at fast speed、/DRONEREVEAL 自動加 large amplitude；
    wrapper 不在 skill 裡（Ref2VA 在實測工具、I2VA 在私人腳本、T2VA/FL2VA/L2VA 缺）。
- 修改後：新增 PROJECT_GOAL.md（目標、固定架構、四層定義與來源、忠實度規則、來源優先序、凍結項、各部分狀態）。
    scripts/adapters.py 的 H3 編譯器改成 `_move_h3_layers`：每個運鏡輸出 camera_core（MINIMAX_OFFICIAL）、temporal_clarifier、derived_visual_constraint、
    negative_clarifier（後三者 PROJECT_DEFINED，附證據編號）；平文字＝四層句子依序相接；render() 每鏡多帶 "h3" 結構；CLI `render --layers` 印 h3_camera_output。
    忠實度：度數／百分比／公尺一律寫成派生約束句（The pan turns about 45 degrees.）；SLOW/VSLOW/IMPERCEPTIBLE → at slow speed、FAST → at fast speed 一律輸出（含推拉）；
    ORBIT FULL 不再自動加 token，改發 SRC-009 orbit-360 警告（/ORBIT:R:FULL:FAST 才寫速度）；DRONEREVEAL 不再自動加 large amplitude；
    CRASHZOOM 的 token 來自指令定義（a sudden, very fast zoom）保留。
    新增 scripts/h3_wrappers.py：T2VA/I2VA/FL2VA/L2VA → 官方 Base 結構（對齊句逐字照 SRC-008 base-en 2.1）、Ref2VA → 六欄 Full-reference 結構；
    五種 mode 吃同一份 camera core，wrapper 不寫任何運鏡語言；sample_content(mode) 是測試夾具；CLI `h3_wrappers.py <mode> "<dsl>" [content.json] [--layers …] [--lint]`。
    scripts/run_tests.py 新增 layer[]/nolayer[]/wrap[]/nowrap[] 斷言、GUARDS 納入分層後的否定句；models/minimax_h3.md 加「Four layers」節，規則 3／3b／4／12／13 與範例改成實際輸出；
    SKILL.md 加 --layers 與 h3_wrappers 一行、指向 PROJECT_GOAL.md。
- 影響 Command：無（104／244／18 不變）
- 影響 Adapter：minimax_h3 的運鏡句分層輸出。用字變動：推拉拆成「starts on …／pushes in[ at slow speed]／The push continues steadily …／The final frame is …／The focal length stays the same.」；
    搖、俯仰、滾轉、橫移、升降的否定句獨立成句（The camera stays in place.）；度數句新增；ORBIT FULL 與 DRONEREVEAL 不再自動加 token；序列中的靜止鏡寫 holds a Static Shot。
    其他模型轉接器與 routing 不變。
- 影響 Test：修改 MS-H3-04、REG-18c、REG-19、SEQ-021、SEQ-031、SEQ-032；新增 MS-H3-26–32，tests/h3_wrappers.md 的 WRAP-T2VA-01、WRAP-I2VA-01、WRAP-FL2VA-01、WRAP-L2VA-01、
    WRAP-BASE-02–04、WRAP-REF-01–04；run_tests 595/595
- 是否破壞 backward compatibility：是——minimax_h3 的輸出文字改變（句子拆分與 token 規則如上：/ORBIT:R:FULL、/EWS /DRONEREVEAL:BACK 少了自動 token，
    /DOLLYIN:…:SLOW 多了 at slow speed，/PAN:R:45 等多了度數句）；DSL、IR、其他模型、歷史 Reality 判定與等級不變
- 檔案：PROJECT_GOAL.md, SKILL.md, CHANGELOG.md, models/minimax_h3.md, scripts/adapters.py, scripts/camera_dsl.py, scripts/h3_wrappers.py, scripts/run_tests.py,
    tests/h3_wrappers.md, tests/model_adapters.md, tests/regression.md, tests/sequences.md, examples/action.md, examples/advanced_combinations.md, examples/basic.md,
    examples/dialogue.md, examples/storyboard.md, references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md,
    references/05_camera_rotation.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md,
    references/09_lens_optics.md, references/10_zoom.md, references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md,
    references/15_aliases.md, references/16_conflict_rules.md, references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml,
    schemas/examples.yaml

## CL-029 · 2026-10-01 · 專案目標與 H3 架構稽核報告（只稽核，不重構）

- 原因：維護者對照官方 h3-prompt-writing、根因報告與專案資料後指出：Camera DSL Core 方向正確，H3 Adapter 架構需要整併成「一套 H3 Camera Core＋各 mode wrapper」，
    Reality Profile 不得泛化成 H3 全域能力；要求本階段只稽核、不改程式、不改提示詞、不生成影片、不改歷史結果，只建立一份稽核報告。
- 修改前：沒有專案目標定稿與架構稽核；H3 的能力等級在 profile／routing／報告裡沒有綁 generation profile。
- 修改後：新增 research/project_goal_and_h3_architecture_audit.md：A 專案目標（待寫成 PROJECT_GOAL.md）、C 15 項現況稽核、D 官方結構對照、E 逐指令 Camera Core 檢查
    （motion type／方向沒有漂移；三個參數忠實度缺陷、澄清句與派生約束和核心句混寫）、F Reality Profile 範圍稽核（42 格＝LOCAL_H3_REF2VA_PDD8_Q_416；PROD I2VA 結果應標 PROVISIONAL）、
    G 判定與 REQUIRED／OPTIONAL fixes，STATUS READY_FOR_REFACTOR。
- 影響 Command：無
- 影響 Adapter：無
- 影響 Test：無（577/577 不變）
- 是否破壞 backward compatibility：否
- 檔案：research/project_goal_and_h3_architecture_audit.md, CHANGELOG.md

## CL-028 · 2026-10-01 · 生產鏡頭 03：/MS /PAN:R 走路由（I2VA，3 seed）→ 0/3，PAN 路徑寫進能力設定

- 原因：維護者指定下一個常用鏡頭 `/MS /PAN:R`，一樣走路由跑 3 seed。
- 修改前：production_routes 只有 DOLLYIN；PAN 在中景 I2VA 下的行為未測。
- 修改後：路由→ MS 只靠文字 LOW → I2VA 真實中景首幀（同 PROD-01 的首幀，不加近景物）；PAN:R 實測 B。結果 0/3：三條方向都對（背景往左滑 8%／9%／18% 畫面寬），
    但人物被鎖在畫面裡（+0.2%／+2.5%／−5.5%），各層沒有一起動＝自動重新取景，不是搖；矩陣裡全身小人物的 PAN-R 是 2/3，差別在人物大小／置中，不在文字。沒有改提示詞。
    profile 新增 production_routes.PAN（canonical_semantics.physical_camera_rotation true；minimax_h3_ref2va.text_only MEDIUM；minimax_h3_i2va.medium_shot_first_frame → SUBJECT_LOCKED_BACKGROUND_SLIDE，reliability LOW，confidence 0/3）；
    tests/model_adapters.md 新增 MS-H3-25（577 測試）；research/h3_lab_findings.md 新增 H3LAB-PROD-SHOT-03；models/minimax_h3.md 支援表加一列；實驗室 matrix.md／results.md 各一段、spec H3R-PROD-MS-PAN-R-01。
- 影響 Command：無
- 影響 Adapter：無新程式（routing 對 PAN 印既有格式的路徑行）；鏡頭句不變
- 影響 Test：新增 MS-H3-25；run_tests 577/577
- 是否破壞 backward compatibility：否
- 檔案：models/minimax_h3_profile.yaml, tests/model_adapters.md, research/h3_lab_findings.md, models/minimax_h3.md, CHANGELOG.md

## CL-027 · 2026-10-01 · 生產鏡頭 02 補跑 2 個 seed；DOLLYIN 路徑定名 PARALLAX_ASSISTED_PUSH_IN、可靠度 CONDITIONAL

- 原因：維護者定案 02 的 seed 1001 是「有視差輔助的推近」而不是物理推軌，給了路徑的最終結構
    （canonical_semantics.physical_camera_translation true；minimax_h3_i2va.without_foreground_depth → ZOOM_LIKE_PUSH_IN／physical_fidelity LOW；with_foreground_depth_anchor → PARALLAX_ASSISTED_PUSH_IN／visual_usability HIGH／physical_fidelity PARTIAL），
    並指定只補跑 seed 1002、1003（首幀、提示詞、設定全同）：3/3 PASS 才升 PRODUCTION_VALIDATED，否則保留 PENDING 或降 CONDITIONAL，不再補字。/DOLLYIN 的 DSL 定義不改。
- 修改前：production_routes.DOLLYIN 是上一版的扁平結構，reliability PENDING_PRODUCTION_CONFIRMATION（只有 seed 1001）。
- 修改後：profile 改成維護者的結構（另保留 minimax_h3_ref2va.text_only LOW）；補跑結果 2 PASS＋1 PARTIAL：近柱在三條裡都比等比放大快得多地出畫（近景層視差 3/3），
    人物與遠景分離 2/3（1001 遠景凍結 1.00、1002 遠景 1.04–1.07、1003 人物後面每一層一起放大約 1.2×）→ reliability CONDITIONAL、confidence「2/3 PASS、1/3 PARTIAL」，physical_fidelity 仍 PARTIAL。
    scripts/adapters.py：routing 改用 _routes_summary 印巢狀路徑（mode.branch: result reliability (usability, fidelity, confidence)＋做法）；tests/model_adapters.md MS-H3-24 改對新名稱（576 測試）；
    research/h3_lab_findings.md、models/minimax_h3.md 同步；實驗室 matrix.md／results.md 各一段；spec H3R-PROD-MS-EYE-DOLLYIN-02 的 seeds 記為 1001–1003。路徑到此凍結。
- 影響 Command：無（/DOLLYIN 定義不變）
- 影響 Adapter：minimax_h3 routing 的路徑行格式；鏡頭句不變
- 影響 Test：MS-H3-24 斷言更新；run_tests 576/576
- 是否破壞 backward compatibility：否
- 檔案：models/minimax_h3_profile.yaml, scripts/adapters.py, tests/model_adapters.md, research/h3_lab_findings.md, models/minimax_h3.md, CHANGELOG.md

## CL-026 · 2026-10-01 · 生產鏡頭 02（近景深度錨點）＋DOLLYIN 生產路徑寫進能力設定

- 原因：維護者定案生產鏡頭 01（FRAMING／IDENTITY／CONTINUITY／TEMPORAL／PUSH-IN VISUAL PASS，PHYSICAL DOLLY PARTIAL / NOT VERIFIED，PRODUCTION_USABLE YES；不拿它證明 /DOLLYIN 可靠），
    並指定只跑 PROD-MS-EYE-DOLLYIN-02（seed 1001）：唯一改變是首幀加一個偏離中心、占畫面寬 15–25%、不擋臉的近景深度錨點，驗證能不能把 zoom-like push 變成有視差的推軌；
    成功就把 DOLLYIN 的路徑寫成 text_only_ref2va LOW／i2va_without_foreground_depth zoom_like_push_in／i2va_with_foreground_depth_anchor PENDING_PRODUCTION_CONFIRMATION。
- 修改前：能力設定沒有各輸入路徑的結果；01 的正式判定未登記。
- 修改後：02 的五項標準全部符合（近柱 0.75 秒內滑出、人物 1.40 倍、遠景 1.00；柱子與人物間隙 16 → 50 px；不是等比放大），但遠景凍結而非小幅放大 → PHYSICAL DOLLY PARTIAL，
    路徑照規則記 PENDING_PRODUCTION_CONFIRMATION。models/minimax_h3_profile.yaml 新增 production_routes.DOLLYIN（維護者格式＋證據＋做法）；scripts/adapters.py 的 routing 對有 production_routes 的運鏡多印一行；
    tests/model_adapters.md 新增 MS-H3-24（576 測試）；research/h3_lab_findings.md 新增 H3LAB-PROD-SHOT-02、01 列補維護者定案；models/minimax_h3.md 的支援表加一列。
    實驗室：首幀 CHARACTER_A_MS_FIRSTFRAME_FGANCHOR.png（同一幀最左柱子放大、模糊、稍暗合成，沒有 AI 修圖）、spec H3R-PROD-MS-EYE-DOLLYIN-02、matrix.md／results.md 各一段。
- 影響 Command：無
- 影響 Adapter：minimax_h3 routing 多一行（有 production_routes 的運鏡）；鏡頭句不變
- 影響 Test：新增 MS-H3-24；run_tests 576/576
- 是否破壞 backward compatibility：否
- 檔案：models/minimax_h3_profile.yaml, scripts/adapters.py, tests/model_adapters.md, research/h3_lab_findings.md, models/minimax_h3.md, CHANGELOG.md

## CL-025 · 2026-10-01 · 第一個生產鏡頭走完路由（H3LAB-PROD-SHOT-01）

- 原因：維護者：不再跑實驗矩陣，拿真正要做的一鏡 `/MS /EYELEVEL /DOLLYIN:MS>MCU` 走完整流程（解析 → 查能力設定 → 發現 MS 只靠文字 LOW → 建議 I2VA → 輸出提示詞 → 實際生成一鏡 → 判可用素材）。
- 修改前：路由只有規則，沒有實鏡驗證。
- 修改後：1 條 I2VA（真實中景首幀、場景句只寫她在哪）：首幀保留（平均差 4.4）、起幅腰上中景（約 1.8 畫面高）、落幅胸上中近景（1.31 倍）、長相服裝一致、無跳接；
    推近平穩但視差 0＝像變焦（轉接器事先已警告）。判可用但註記；由維護者看片定案。research/h3_lab_findings.md 新增 H3LAB-PROD-SHOT-01；models/minimax_h3.md 的 I2VA 列補證據。
- 影響 Command：無
- 影響 Adapter：無（文字與路由都不變）
- 影響 Test：無（575/575）
- 是否破壞 backward compatibility：否
- 檔案：research/h3_lab_findings.md, models/minimax_h3.md, CHANGELOG.md

## CL-024 · 2026-10-01 · H3 能力規則（Capability Profile）＋生產路由（Production Routing）

- 原因：維護者決定停止根因實驗，把實測結果轉成 skill 的 H3 能力規則：不改 104 個 canonical command、不改攝影語義，只更新 H3 轉接器與能力設定；
    遇到 /MS、/MCU、/CU 這類嚴格景別時不能假裝 Ref2VA 文字一定做得到，要輸出可靠度與建議（真實首幀／I2VA；仍用 Ref2VA 就少寫和景別競爭的環境描述）；
    場景提示詞的規則：近景、中景不要在同一鏡頭要求畫面展示大量環境元素，改寫「人物所在的是什麼環境」。
- 修改前：轉接器只輸出鏡頭句與零散警告；實測等級只存在 tests/reality 的報告裡，寫提示詞時查不到；沒有輸入模式（Ref2VA／I2VA）的建議。
- 修改後：
    新增 models/minimax_h3_profile.yaml（維護者給的欄位：framing.text_only_shot_size LOW、environment_description_effect VERIFIED、strict_medium_shot → I2VA_FIRST_FRAME、
    camera_motion COMMAND_DEPENDENT、seed_sensitivity framing／camera_mechanism HIGH、reference_image_size max_vs_match NOT_SUPPORTED_AS_ROOT_CAUSE），
    加上 camera_motion.by_command：42 個矩陣格的修正後 H3_RELIABILITY 等級與四項通過數（由 results.json 產生），每條附證據編號。
    scripts/adapters.py：讀取 profile；minimax_h3 影片輸出新增 routing（每鏡）：景別比全景緊（MFS、COWBOY、MS、MCU、CU、ECU，含推拉範圍的起幅）時給「可靠度 LOW → 若景別必須精確用真實首幀（I2VA）；仍用 Ref2VA 則描述人物所在環境、不列畫面必須看到的元素；不保證維持該景別」；
    每個運鏡／機位指令查 by_command 給實測等級（C、D、F 時另發警告）；seed 敏感度提示。routing 另以 warnings 形式帶出（H3 ROUTING: …），鏡頭句本身一字不改。routing_text(lang) 產生英文或中文（--lang zh）區塊。
    scripts/camera_dsl.py：render 在警告後印出 routing 區塊。scripts/run_tests.py：新增 nowarn[model]~regex 斷言。
    tests/model_adapters.md：新增 MS-H3-18–23（嚴格景別有路由、全景／遠景沒有、範圍起幅算景別、場景規則與 seed 提示、DOLLYIN／TRUCK:R 的等級、其他模型不受影響）；569 → 575。
    models/minimax_h3.md：新增「Capability profile and production routing」與場景規則；景別偏移一節補 H3LAB-FRAMING-SCENE-01、-REFSIZE-01 與根因調查結論。SKILL.md：交付清單加一行 routing 區塊。
    audit.py --sync 重新產生 examples/*.md（H3 案例多了 H3 ROUTING 警告）、references/*.md 表格、registry/provenance.yaml 的 commands、registry/canonical_commands.yaml、schemas/examples.yaml（內容由同一份 registry 重生，104／244／18／58／83 不變）。
- 影響 Command：無（104 個 canonical command、244 個 alias、18 條文法都沒動；--sync 只重生衍生欄位）
- 影響 Adapter：minimax_h3 新增 routing 輸出與 H3 ROUTING 警告；鏡頭句文字不變（既有 MS-H3-01–17 全部照舊通過）
- 影響 Test：新增 MS-H3-18–23；run_tests 575/575
- 是否破壞 backward compatibility：否（render() 的既有鍵不變，新增 routing 鍵；其他模型輸出不變）
- 檔案：models/minimax_h3_profile.yaml, scripts/adapters.py, scripts/camera_dsl.py, scripts/run_tests.py, tests/model_adapters.md, models/minimax_h3.md, SKILL.md,
    examples/action.md, examples/advanced_combinations.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md,
    references/01_shot_size.md, references/02_subject_framing.md, references/03_camera_angle.md, references/04_camera_height.md, references/05_camera_rotation.md,
    references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/09_lens_optics.md, references/10_zoom.md,
    references/11_focus_depth.md, references/12_composition.md, references/13_continuity.md, references/14_aerial_drone.md, references/15_aliases.md, references/16_conflict_rules.md,
    references/17_prompt_translation_rules.md, registry/canonical_commands.yaml, registry/provenance.yaml, schemas/examples.yaml, CHANGELOG.md

## CL-023 · 2026-10-01 · H3LAB-FRAMING-REFSIZE-01（景別：參考圖尺寸 max → match，3 條）

- 原因：維護者的決定：先做參考圖預處理檢查，max 和 match 對實際輸入有差異才跑 3 seed 對照；正式轉接器、歷史判定、Canonical DSL 維持凍結。
- 修改前：實測矩陣 155 條片都用節點的 ref_image_size=max（參考圖原尺寸），產線工作流用 match；兩者對景別的影響沒有測過。
- 修改後：預處理檢查（節點程式：max 以 2048 短邊上限、不放大 → 兩張參考圖原尺寸 1440×1088／1536×1024，VAE latent 6120＋6144 格、DiT 2×2 patch 後 3066 個參考 token、Qwen 視覺 token 3066；
    match 縮到 416×736 的像素量 → 640×480／672×448，latent 1200＋1176、594 個 token）→ 有差異，依決定執行。實驗室 runner 新增可選 spec 鍵 ref_image_size（不寫＝max；既有 158 條片的圖重建後和執行紀錄逐節點相同）。
    結果 0/3（0.30／0.38／0.61 畫面高，對照 0.30／0.42／0.98）：參考圖尺寸不是景別變寬的原因；運鏡機制 3/3、時間 3/3、連續性 2 PARTIAL＋1 FAIL（seed 1003 全程往鏡頭走）。
    登記：research/h3_lab_findings.md 新增一列；research/h3_root_cause_investigation.md CASE 02「後續 2」；實驗室 matrix.md／results.md 各一段。轉接器沒動。
- 影響 Command：無（104 個 canonical command、244 個 alias、18 條文法都沒動）
- 影響 Adapter：無
- 影響 Test：無（run_tests 569/569 不變；矩陣與歷史判定不變；新片是實驗，不進 results.json）
- 是否破壞 backward compatibility：否
- 檔案：research/h3_lab_findings.md, research/h3_root_cause_investigation.md, CHANGELOG.md

## CL-022 · 2026-10-01 · H3LAB-FRAMING-SCENE-01（景別：環境視野描述消融實驗，3 條）

- 原因：ROOT_CAUSE_GATE_02——維護者批准只生成 3 條，驗證共用提示詞裡的環境視野描述（兩排柱子、遠牆月洞門、開闊天空）是不是讓 H3 忽略指定的腰上中景。
    對照組用 H3R-STATIC 既有 seed 1001–1003（不重生）；實驗組只拿掉那三句，其他逐字不動，參考圖、seed、模型、取樣全同（runner 圖逐節點核對，只差 prompt 與輸出檔名）；
    判定沿用凍結的景別與四項標準，成功＝景別 PASS，事先登記 3/3、2/3、0–1/3 的解讀。
- 修改前：場景句對景別的影響從未被單獨隔離（四個既有景別實驗都保留整段場景句）。
- 修改後：結果 0/3（頭頂到腰帶 ÷ 0.38：約 0.93、1.00、1.02 畫面高，都是全身級）→ 拿掉環境描述不足以解決。但 2/3 seed 的人物大了 2.4–3 倍（0.3／0.4 → 約 1.0），
    三個 seed 收斂到同一種「頭頂靠上緣、下緣切裙襬」構圖；運鏡機制 2 PASS＋1 PARTIAL（scale 1.031 剛超過凍結門檻）、時間 3/3、連續性 1 PASS＋2 PARTIAL（前 1–2 秒略放大 3%）。
    登記：research/h3_lab_findings.md 新增 H3LAB-FRAMING-SCENE-01；research/h3_root_cause_investigation.md CASE 02 加「後續」；實驗室 matrix.md／results.md 各一段。
    沒有因此改轉接器，也沒有宣稱模型完全不支援文字景別。
- 影響 Command：無（104 個 canonical command、244 個 alias、18 條文法都沒動）
- 影響 Adapter：無
- 影響 Test：無（run_tests 569/569 不變；矩陣 42 格與歷史判定不變；新片是實驗，不進 results.json）
- 是否破壞 backward compatibility：否
- 檔案：research/h3_lab_findings.md, research/h3_root_cause_investigation.md, CHANGELOG.md

## CL-021 · 2026-09-30 · H3 根因調查報告（ROOT_CAUSE_GATE_01，只讀取與比較）

- 原因：維護者要求確認 H3 實測的問題發生在哪一個系統層級（不是提高成功率）：三組既有案例（機位高度／角度同 seed 三格、指定 MS 卻變全身、右橫移 seed 1001）
    做完整流程稽核（DSL → 解析器 → 轉接器 → 提示詞檢查 → ComfyUI API prompt → 文字編碼節點 → conditioning → 參考圖順序 → 模型／LoRA／CFG／步數／seed／解析度 → 輸出檔與執行紀錄），
    用當時真正執行的資料，記錄雜湊，每項發現只標 VERIFIED／SUSPECTED／EXCLUDED／INSUFFICIENT_EVIDENCE，無法證實就不指定根因。
- 修改前：沒有流程層級的根因報告；失敗原因只記在 MODEL_LIMITATIONS 與實驗室紀錄。
- 修改後：新增 research/h3_root_cause_investigation.md。歷史真本來源：本機 ComfyUI 的 /history（155 條 H3R 片各 1 筆、全部 success）、每支 MP4 內嵌的執行 API prompt
    （155/155 和 history 相同）、runner 紀錄、執行 log；解析器／轉接器／lint 輸出用現版重新產生並標 RECONSTRUCTED，逐句和執行提示詞比對。
    結果：三個案例的編譯、傳遞、判定都排除（指令逐字送達、conditioning 各自重新編碼、無截斷、文字編碼器正確、參考圖順序與內容雜湊正確、無快取或輸出重用）；
    VERIFIED：Ref2VA 下只靠文字指定機位高度／角度、景別在這組條件下沒有可量到的效果，構圖由 seed 決定；右橫移的機制由 seed 決定、對取樣與句子變體穩定，沒有被換成 pan 的指令。
    SUSPECTED（未分離）：模型控制極限、共用模板場景句和景別／機位的 conditioning 衝突、否定句被忽略。INSUFFICIENT_EVIDENCE：量化權重、換取樣的影響。
    建議下一步 12 條片的單變數實驗（場景句隔離、右橫移新 seed、機位 20 步對照），尚未執行。
- 影響 Command：無（104 個 canonical command、244 個 alias、18 條文法都沒動）
- 影響 Adapter：無
- 影響 Test：無（run_tests 569/569 不變；沒有生成影片、沒有改歷史判定）
- 是否破壞 backward compatibility：否
- 檔案：research/h3_root_cause_investigation.md, CHANGELOG.md

## CL-020 · 2026-09-30 · 升降機重新檢查（PEDESTAL_REVALIDATION_V1）＋搖臂 CRANE-UP 1002 複核

- 原因：維護者要求（H3 PEDESTAL REVALIDATION）用修正後的量測方法重新檢查 PED-UP、PED-DOWN 共 6 條歷史影片，確認有沒有因量測方法錯誤造成的誤判；
    升降機＝攝影機整台垂直移動、朝向原則上不變，高度變化不能用俯仰代替。先處理搖臂證據：CRANE-UP seed 1002 結尾有一個取樣的地平線抓錯，
    凍結規則沒有事先允許排除，應記為證據不足，不得為了維持通過數放寬規則。規定：不重新生成、不改原始提示詞、不改 Camera DSL Core 與 H3 Adapter；
    先凍結判定方式再檢查；攝影機高度、朝向、幅度、時間、景別、連續性分開確認；V2 高度量測只當輔助，必須做疊圖檢查與人工目視，
    無法確認記 INSUFFICIENT_EVIDENCE；歷史判定全部保留、另外記修正判定；等級有變就重算 42 個唯一測試 ID 的統計。
- 修改前：CRANE-UP 1002 的疊圖記 ok（理由是結尾值取中位數、不受錯誤取樣影響）。PED-UP、PED-DOWN 只有 V1 判定（ty＋視差指數，各 C）。
    搖臂修正後合計 A5 B2 C10 D16 F9，四項的運鏡機制 57。
- 修改後：
    CRANE-UP 1002：疊圖改記 bad → V2 量測 EVIDENCE_INSUFFICIENT；修正結果仍是 PARTIAL、CRANE-UP 仍是 D。開頭／結尾窗口每個原始取樣與 Δr 都保留，
    先前那次檢查存在 verify_history 並顯示在 11。搖臂修正後的四項運鏡機制 57 → 56。
    PEDESTAL_REVALIDATION_V1（2026-09-30 21:50 凍結，之後才量 6 條片）：攝影機高度＝人工讀數必做（第一幀／最後一幀的參考線與身體長度）＋V2 輔助
    （窗口內每個取樣都要通過疊圖檢查，不可排除）；朝向＝V2 地平線在畫面裡的移動，≤5% 畫面高 PASS、≤12% PARTIAL、更多 FAIL
    （門檻來自非升降機格的校準片：不俯仰的片最多 2.8 px、上搖 163 px）；幅度、時間沿用原本標準；景別、連續性分開記錄、不算進 seed 判定；
    INSUFFICIENT_EVIDENCE 不算通過、計分時當 PARTIAL。
    結果：6 條都有真的垂直位移（人工讀數確認；PED-UP 1001 的 V2 也有效，Δr +0.91）。朝向量得到的 2 條都混了俯仰（PED-UP 1001 上仰 8.7%、
    PED-DOWN 1002 下俯 11.6% 畫面高），另外 4 條照凍結規則朝向證據不足。逐條：PED-UP 1001 FAIL → PARTIAL、1002 PASS → PARTIAL、1003 PASS → PARTIAL；
    PED-DOWN 1001 PARTIAL → PARTIAL、1002 PASS → PARTIAL、1003 PARTIAL → PARTIAL。等級 PED-UP C → D、PED-DOWN C → D（歷史 C 保留）。
    42 個唯一 ID：歷史 A4 B2 C10 D15 F11；搖臂修正後 A5 B2 C10 D16 F9；加升降機後 A5 B2 C8 D18 F9。四項（126 條）加升降機後：
    運鏡機制 52、景別 31、時間 101、連續性 96。各區與 FINAL 修正前後都是 PARTIAL。
    報告：新增 12_pedestal_revalidation_v1.md；01 的升降機兩格加「修正」列；10 的修正段合併兩個修正；11 顯示 1002 的複核與先前紀錄；
    04、06 的搖臂修正列同步（疊圖 bad）；改動前的 01、04、06、10、11 存在 history/。MODEL_LIMITATIONS 第 3、12、16 條更新、新增第 17 條；H3 說明檔的總結同步。
- 影響 Command：無（104 個 canonical command、244 個 alias、18 條文法都沒動）
- 影響 Adapter：無（H3 轉接器輸出不變）
- 影響 Test：實測工具新增 crane-v2-samples、ped-v1-freeze、ped-v1、ped-v1-verify、ped-v1-refresh；PED-UP、PED-DOWN 另有修正後等級；run_tests 569/569 不變
- 是否破壞 backward compatibility：否（歷史紀錄與既有指令不變）
- 檔案：tests/reality/minimax_h3/tools/h3_reality.py, tests/reality/minimax_h3/results.json,
    tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/04_complex_motion.md, tests/reality/minimax_h3/06_combinations.md,
    tests/reality/minimax_h3/10_results.md, tests/reality/minimax_h3/11_crane_validator_v2.md, tests/reality/minimax_h3/12_pedestal_revalidation_v1.md,
    tests/reality/minimax_h3/history/01_single_movement_before_ped_v1.md, tests/reality/minimax_h3/history/04_complex_motion_before_ped_v1.md,
    tests/reality/minimax_h3/history/06_combinations_before_ped_v1.md, tests/reality/minimax_h3/history/10_results_before_ped_v1.md,
    tests/reality/minimax_h3/history/11_crane_validator_v2_before_ped_v1.md, models/minimax_h3.md, CHANGELOG.md

## CL-019 · 2026-09-30 · 搖臂升降量測器修正（CRANE_VALIDATOR_V2）

- 原因：維護者要求修正搖臂升降量測器的判定缺陷（H3 CRANE VALIDATOR CORRECTION）：V1 用整個畫面的光流方向判升降，分不出搖臂和原地俯仰，
    而且因為搖臂同時俯仰把人物留在畫面裡，正確的片會量到相反的方向。規定：不改 DSL、轉接器、提示詞、生成參數、原始影片與歷史判定；先凍結新標準再重判原本 6 條片；
    無法區分搖臂和俯仰時標記證據不足；保留歷史 F、另外記修正結果；用 42 個唯一測試 ID 重算等級總表並找出合計 43 的原因；重算受影響的統計，不覆寫舊報告。
- 修改前：CRANE-UP、CRANE-DOWN 用 ty 的正負號判（6 條量測全 FAIL、等級 F，目視 6/6 符合）。等級合計 A4 B2 C10 D15 F12＝43。
- 修改後：
    新增 tests/reality/minimax_h3/tools/crane_validator_v2.py：地平線（地面直線的消失點）穿過站在地上的東西、在和攝影機一樣高的位置，不受俯仰影響；
    用地平線切在她身上的位置（以黑色圍裙為身體參考、逐幀追蹤）量攝影機相對她的高度，分開判攝影機高度、角度補償（只記錄）、時間；景別與連續性目視；
    疊圖檢查（每個開頭／結尾取樣的地平線與圍裙框）必做，抓錯或量不到＝證據不足、不算通過。規則與門檻 20:58 凍結（results.json 的 validators），之後才重判。
    校準（非搖臂格 27 條）：量得到 13 條，疊圖正確的 9 條全部和預期一致；4 條圍裙框抓錯，由疊圖檢查擋下。附帶發現：PED-UP 1001 量到真的升高，和第 1 波判定不同（不改，待維護者決定）。
    重判：CRANE-DOWN 3/3 PASS → 修正後 A；CRANE-UP 量得到的 2 條都真的升高但 2 秒只完成 24.9%／23.8%（PARTIAL），1 條結尾量不到地平線（證據不足）→ 修正後 D。
    歷史 F 保留（results.json 的 cells 原封不動、報告原內容不變）；修正結果存在 validators 並顯示在 04、06、10 的新增列與新報告 11_crane_validator_v2.md；改動前的 04、06、10 存在 history/。
    合計 43 的原因：別名列 H3R-CMB-WS-CRANEUP 沒有自己的片、沿用 H3R-CRANE-UP，被算了兩次（CL-018 的 F12）。42 個唯一 ID：歷史 A4 B2 C10 D15 F11；修正後 A5 B2 C10 D16 F9。
    四項合計（126 條）修正後 運鏡機制 57、景別 31、時間 101、連續性 96；各區與 FINAL 修正前後都是 PARTIAL。MODEL_LIMITATIONS 第 12 條與 H3 說明檔的總結同步更正。
- 影響 Command：無（104 個 canonical command、244 個 alias、18 條文法都沒動）
- 影響 Adapter：無（H3 轉接器輸出不變）
- 影響 Test：實測工具新增 crane-v2-freeze／crane-v2-calibrate／crane-v2／crane-v2-verify；CRANE-UP、CRANE-DOWN 另有修正後等級；run_tests 569/569 不變
- 是否破壞 backward compatibility：否（歷史紀錄與既有指令不變）
- 檔案：tests/reality/minimax_h3/tools/crane_validator_v2.py, tests/reality/minimax_h3/tools/h3_reality.py, tests/reality/minimax_h3/results.json,
    tests/reality/minimax_h3/04_complex_motion.md, tests/reality/minimax_h3/06_combinations.md, tests/reality/minimax_h3/10_results.md,
    tests/reality/minimax_h3/11_crane_validator_v2.md, tests/reality/minimax_h3/history/04_complex_motion_before_crane_v2.md,
    tests/reality/minimax_h3/history/06_combinations_before_crane_v2.md, tests/reality/minimax_h3/history/10_results_before_crane_v2.md,
    models/minimax_h3.md, CHANGELOG.md

## CL-018 · 2026-09-30 · H3 實測第 3、4 波（25 格）結果：42 格全部完成

- 原因：維護者要求 I2VA 對照之後，用原本凍結的 Ref2VA 條件跑完剩下 25 格，建立 Ref2VA 的 Camera Reality Profile。
- 修改前：25 格 NOT_RUN，FINAL 不下結論。
- 修改後：
    25 格 × 3 seed＝75 條（H3-PDD 8 步），全部用各格事先寫死的目視標準判（等級用這個，和前 17 格同一基準），另外記四項。
    全部 42 格：A 4、B 2、C 10、D 15、F 12；七區都是 PARTIAL，FINAL：PARTIAL。四項（126 條）：運鏡機制 58、景別 31、時間 103、連續性 96。
    MODEL_LIMITATIONS 補上第 3、4 波的發現（機位高度角度被忽略、環繞方向角度不可靠、移焦 0/3、廣角被當遠景、兩人鏡頭多出重複人物），
    並更正第 8 條（第 3 波出現方向相反的環繞）。H3 說明檔的實測段落補上總結。
    搖臂升降 CRANE-UP／DOWN：目視 6/6 符合，但事先寫的量測方向錯了，正式等級照規則是 F；差異與證據寫在各 seed 的備註，是否更正待維護者決定。
- 影響 Command：無
- 影響 Adapter：無（轉接器輸出不變）
- 影響 Test：實測第 3、4 波 25 格的狀態；run_tests 569/569 不變
- 是否破壞 backward compatibility：否
- 檔案：tests/reality/minimax_h3/results.json, tests/reality/minimax_h3/02_angle_height.md, tests/reality/minimax_h3/03_tracking.md,
    tests/reality/minimax_h3/04_complex_motion.md, tests/reality/minimax_h3/05_focus.md, tests/reality/minimax_h3/06_combinations.md,
    tests/reality/minimax_h3/08_negative_cases.md, tests/reality/minimax_h3/09_storyboard_cases.md, tests/reality/minimax_h3/10_results.md,
    models/minimax_h3.md, CHANGELOG.md

## CL-017 · 2026-09-30 · I2VA 首幀對照、輸入模式支援表、判定基準統一

- 原因：維護者要求停止調 Ref2VA 景別、改驗真的首幀（I2VA），並把模型支援依輸入模式分開登記、不動 104 個 canonical command；剩下 25 格照原本凍結的 Ref2VA 條件跑，兩批要能比較。
- 修改前：H3 說明檔只有三級景別控制表（KEYFRAME_LOCK 未測）。判定工具記四項時，目視結果＝四項最差（和前 17 格的基準不同）。
- 修改後：
    新增公開結論 H3LAB-FRAMING-KEYFRAME-01（I2VA，控制方案對照）：景別 3/3（首幀保住、1 秒內不重新構圖、結尾中近景），但推鏡做成接近變焦的整張放大（量測視差 0/3）→ 本測試無效。
    H3 說明檔改成「依輸入模式的支援表」：Ref2VA 文字景別 LOW、Ref2VA 構圖參考 LOW、I2VA 首幀景別 HIGH（單次推近測試）、I2VA 運鏡保真 LOW、FL2VA 未測。
    判定工具改成維護者選的 A：judge <id> <seed> <目視結果> [mech= framing= temporal= continuity=]——等級照各格原本寫死的目視標準（前後兩批同一基準），四項另外記；四項最差和目視不同時記差異。10_results 的分項表多列「對照等級」（若改用四項最差當目視）只供比較。已用結果檔複本測過，正式紀錄沒動。
- 影響 Command：無
- 影響 Adapter：無（轉接器輸出不變）
- 影響 Test：實測工具的判定紀錄格式；run_tests 569/569 不變
- 是否破壞 backward compatibility：否
- 檔案：research/h3_lab_findings.md, models/minimax_h3.md, tests/reality/minimax_h3/tools/h3_reality.py, tests/reality/minimax_h3/01_single_movement.md,
    tests/reality/minimax_h3/02_angle_height.md, tests/reality/minimax_h3/03_tracking.md, tests/reality/minimax_h3/04_complex_motion.md,
    tests/reality/minimax_h3/05_focus.md, tests/reality/minimax_h3/06_combinations.md, tests/reality/minimax_h3/07_sequences.md,
    tests/reality/minimax_h3/08_negative_cases.md, tests/reality/minimax_h3/09_storyboard_cases.md, tests/reality/minimax_h3/10_results.md, CHANGELOG.md

## CL-016 · 2026-09-30 · 構圖參考圖測試與 H3 景別控制分級

- 原因：維護者判斷景別應由畫面錨點控制、不是文字（官方 ref-en §2.2：構圖／分鏡用獨立 <Picture>），要求只加一張構圖參考圖跑 3 條；並建議把景別控制分成 TEXT_ONLY／COMPOSITION_REFERENCE／KEYFRAME_LOCK 三級、不改 canonical command。
- 修改前：景別偏寬只記了文字和參考圖裁切的結果，沒有控制分級。
- 修改後：
    新增公開結論 H3LAB-FRAMING-COMPOSITION-ANCHOR-01：灰色中景人形當 storyboard <Picture>（官方寫法）→ 起幅景別 0/3（仍是全身），推鏡 3/3、長相服裝不受影響、灰色人形沒有漏進影片。
    H3 說明檔加「景別控制分級」：TEXT_ONLY＝LOW（0/51）、COMPOSITION_REFERENCE＝LOW（0/3）、KEYFRAME_LOCK＝UNVERIFIED；轉接器照舊寫景別（那是意圖），但在 H3 上當作盡力而為。
    MODEL_LIMITATIONS 同步。轉接器程式不變。
- 影響 Command：無
- 影響 Adapter：無（轉接器輸出不變；只改說明檔）
- 影響 Test：實測紀錄（MODEL_LIMITATIONS）；run_tests 569/569 不變
- 是否破壞 backward compatibility：否
- 檔案：research/h3_lab_findings.md, models/minimax_h3.md, tests/reality/minimax_h3/results.json, tests/reality/minimax_h3/10_results.md, CHANGELOG.md

## CL-015 · 2026-09-30 · 已完成 17 格補登四項判定

- 原因：維護者選 B：先把已完成的 17 格（51 條基準片）補上四項判定再跑剩下 25 格，才能分開「運鏡控制失敗」和「構圖控制失敗」。規則：不重新生成；原判定與等級保留；新舊不同只記差異與證據；時間項要看原始影片；對照實驗不混進統計。
- 修改前：這 51 條只有一個目視結果；左橫移 CL-009 之前的 3 條已不在 results.json。
- 修改後：
    51 條都補上運鏡機制、景別、時間、連續性四項和各項證據（標記為補登）。原目視、量測、等級一條都沒變（已和補登前的備份逐欄比對）。
    合計 PASS：運鏡機制 35/51、景別 0/51、時間 37/51、連續性 48/51。42 條的四項最差和原目視不同，其中 41 條是景別（原目視標準只有推拉變焦格列了景別），差異已逐條記錄。
    景別規則看片後修正一次：從「看下緣切在哪」改成「看人物大小（全身高度相對畫面高度）」，因為俯仰／升降的起幅人物在畫面下方、很多片頭頂空間很大；51 條一體適用，修正原因寫進 10_results。
    時間項用原始影片逐秒光流；51 條逐幀差異都沒有跳接突波。
    左橫移 CL-009 之前舊句子的 3 條從原片復原為「歷史」（等級 C），不算進統計。報告顯示補登分項、差異、歷史與補登規則。
- 影響 Command：無
- 影響 Adapter：無（轉接器輸出不變）
- 影響 Test：實測紀錄（results.json 與 01–10 的顯示）；run_tests 569/569 不變
- 是否破壞 backward compatibility：否
- 檔案：tests/reality/minimax_h3/tools/h3_reality.py, tests/reality/minimax_h3/results.json, tests/reality/minimax_h3/01_single_movement.md,
    tests/reality/minimax_h3/07_sequences.md, tests/reality/minimax_h3/10_results.md, CHANGELOG.md

## CL-014 · 2026-09-30 · 四項目視判定、參考圖裁切測試（H3LAB-FRAMING-REFERENCE-01）

- 原因：維護者選先做參考圖對照（只批准 3 條），並批准實測工具改成四項獨立判定，讓景別失敗的片子仍保留運鏡資料；剩下 25 格暫緩。
- 修改前：每個 seed 只有一個目視結果（PASS／PARTIAL／FAIL）。景別偏寬只試過裁切句（CL-013）。
- 修改後：
    h3_reality.py 的 judge 可記四項：mech=、framing=、temporal=、continuity=（各 PASS／PARTIAL／FAIL）；目視結果＝四項中最差的，分級規則不變（量測和目視取較差）。
    舊的單一目視寫法照舊可用；缺項或寫錯值會被擋（已用複本測過）。01–10 的說明、每個 seed 的列、10_results 的「分項」表都會顯示四項。已判過的 seed 內容不變。
    新增公開結論 H3LAB-FRAMING-REFERENCE-01：服裝參考圖裁到腰部 → 景別 0/3 沒改善、服裝 0/3 變差、推鏡 3/3 → 保留全身參考圖。H3 說明檔與 MODEL_LIMITATIONS 補上。
- 影響 Command：無
- 影響 Adapter：無（轉接器輸出不變）
- 影響 Test：實測工具的判定紀錄格式；run_tests 569/569 不變
- 是否破壞 backward compatibility：否（舊的單一目視寫法與既有紀錄都照舊有效）
- 檔案：tests/reality/minimax_h3/tools/h3_reality.py, tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/02_angle_height.md,
    tests/reality/minimax_h3/03_tracking.md, tests/reality/minimax_h3/04_complex_motion.md, tests/reality/minimax_h3/05_focus.md,
    tests/reality/minimax_h3/06_combinations.md, tests/reality/minimax_h3/07_sequences.md, tests/reality/minimax_h3/08_negative_cases.md,
    tests/reality/minimax_h3/09_storyboard_cases.md, tests/reality/minimax_h3/10_results.md, tests/reality/minimax_h3/results.json,
    research/h3_lab_findings.md, models/minimax_h3.md, CHANGELOG.md

## CL-013 · 2026-09-30 · 景別裁切錨點測試（H3LAB-FRAMING-ANCHOR-01）

- 原因：第 2 波推拉變焦 12 條機制都對、景別都偏寬。維護者選先做景別小實驗（只批准 3 條、不批准改正式轉接器），並要求判定分成運鏡機制、景別、時間、連續性四項。
- 修改前：景別偏寬只有現象紀錄。
- 修改後：
    新增公開結論 H3LAB-FRAMING-ANCHOR-01：推近那格多一句「第一格畫面下緣切在她的腰」→ 景別 0/3（只從全身收緊到腳踝／小腿），運鏡機制 3/3 不受影響。
    H3 說明檔「失敗類型」加「景別偏寬」。轉接器不變。
- 影響 Command：無
- 影響 Adapter：無（轉接器輸出不變）
- 影響 Test：無（run_tests 569/569）
- 是否破壞 backward compatibility：否
- 檔案：research/h3_lab_findings.md, models/minimax_h3.md, CHANGELOG.md

## CL-012 · 2026-09-30 · H3 實測第 2 波（9 格）結果

- 原因：維護者選先跑第 2 波 9 格（主要是第 1 波的反方向，加上固定、推拉、變焦），再決定剩下 25 格。
- 修改前：這 9 格都是 NOT_RUN。
- 修改後：
    9 格 × 3 seed＝27 條（H3-PDD 8 步），量測和目視都判完，寫進 results.json 和 01、10。
    STATIC、TILT-DOWN：PASS（A）。PAN-R：PARTIAL（B）。PED-UP：PARTIAL（C）。DOLLY-IN、DOLLY-OUT、ZOOM-IN、ZOOM-OUT、ROLL-CCW：PARTIAL（D）。
    推拉與變焦的機制分得出來（推拉視差 0.79–1.00、變焦 0.00–0.37），但起止景別沒照寫（推近與放大起點太寬、拉遠與縮小終點拉過頭），所以都是 D。
    BASIC_MOVEMENT、DOLLY_VS_ZOOM 兩區跑完，都是 PARTIAL；其他區仍 NOT_RUN，FINAL 不下結論。
    MODEL_LIMITATIONS 補上：方向不對稱只出現在橫移，其他反方向格子沒有同樣落差；滾轉兩個方向都只有 1/3、都是從斜的轉回水平；景別起止點的偏差。
- 影響 Command：無
- 影響 Adapter：無（轉接器用字沒改）
- 影響 Test：實測第 2 波 9 格的狀態；run_tests 569/569 不變
- 是否破壞 backward compatibility：否
- 檔案：tests/reality/minimax_h3/results.json, tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/10_results.md, CHANGELOG.md

## CL-011 · 2026-09-30 · 右橫移深度參照測試（H3LAB-RTRUCK-DEPTH-01）

- 原因：維護者選 A：只改深度參照（EXPLICIT_DEPTH_CUES OFF → ON），看右橫移被拍成搖是不是因為場景缺少視差參照。判定與判讀在生成前寫死。
- 修改前：右橫移的失敗只排除了 PDD（CL-010）。
- 修改後：
    新增公開結論 H3LAB-RTRUCK-DEPTH-01：場景多一句近景石燈籠／中景人物／遠景建築，運鏡句不動 → 0/3（沒加時 1/3）；
    近景物有出現，但 H3 讓整個畫面一起滑（旋轉），沒有差速視差。照事先的判讀：明確深度參照沒有解決運鏡機制替換，停止修提示詞。
    H3 說明檔「失敗類型」與 10_results 的 MODEL_LIMITATIONS 補上這一條。轉接器不變。
- 影響 Command：無
- 影響 Adapter：無（轉接器輸出不變）
- 影響 Test：實測紀錄（MODEL_LIMITATIONS）；run_tests 569/569 不變
- 是否破壞 backward compatibility：否
- 檔案：research/h3_lab_findings.md, models/minimax_h3.md, tests/reality/minimax_h3/results.json, tests/reality/minimax_h3/10_results.md, CHANGELOG.md

## CL-010 · 2026-09-30 · 根因測試（PDD 對 20 步）與失敗分類

- 原因：維護者要求先不改提示詞、先分離原因（ROOT_CAUSE_GATE_01），並把正式紀錄改成失敗分類、原因未分離的就寫未分離。
- 修改前：限制寫成「人物在中景時會被鎖在中央」等現象描述，沒有分類，也沒有 PDD 對照。
- 修改後：
    新增公開結論 H3LAB-TRUCK-03：右橫移同提示詞改用正式 20 步（無加速 LoRA），PDD 失敗的兩個 seed 仍不是橫移（0/2）→ 大致排除 PDD。
    H3 說明檔加「失敗類型」：運鏡機制被替換（平移變旋轉）、人物補位／自動重新構圖、時間執行不穩；左右不對稱的原因未分離。
    10_results 的 MODEL_LIMITATIONS 改用這個分類，並寫明 CAUSE＝NOT YET ISOLATED。
- 影響 Command：無
- 影響 Adapter：無（轉接器輸出不變）
- 影響 Test：實測紀錄（MODEL_LIMITATIONS）；run_tests 569/569 不變
- 是否破壞 backward compatibility：否
- 檔案：research/h3_lab_findings.md, models/minimax_h3.md, tests/reality/minimax_h3/results.json, tests/reality/minimax_h3/10_results.md, CHANGELOG.md

## CL-009 · 2026-09-30 · H3 左橫移加結尾人物位置句（實測 3/3）

- 原因：第 1 波左橫移 2/3（seed 1003 人物被鎖在畫面中央）。維護者選先做小實驗：運鏡句加「結尾畫面裡人物在右邊」，同樣 3 個 seed 全過。
    維護者裁定：左橫移 VERIFIED、不重跑；右橫移要鏡像句另外實測 3/3 才算；左搖試到第二輪仍 2/3 就停止調整。
- 修改前：H3 的 /TRUCK:L 是「The camera trucks left, sliding sideways. The camera does not turn.」，並警告「未驗證」。
- 修改後：
    左橫移單獨一鏡時寫「The camera trucks left, sliding sideways, so that in the final frame {SUBJECT} is on the right side of the frame. The camera does not turn.」，不再警告未驗證。
    組合運鏡、分段運鏡、右橫移、左搖都維持原句（右橫移鏡像句 1/3，左搖三種寫法都 2/3）。
    公開實驗結論新增 H3LAB-TRUCK-01、H3LAB-TRUCK-02、H3LAB-PAN-01；H3 說明檔加第 13 條。
    實測：H3R-TRUCK-L 改成新句子，結果沿用實驗那 3 條（提示詞、seed、設定完全相同）→ PASS（A）；MODEL_LIMITATIONS、ADAPTER_CHANGES 更新。
- 影響 Command：無
- 影響 Adapter：minimax_h3（只有單獨一鏡的 /TRUCK:L）
- 影響 Test：新增 MS-H3-15、MS-H3-16、MS-H3-17（run_tests 569/569）；實測 H3R-TRUCK-L
- 是否破壞 backward compatibility：是。H3 轉接器對「單獨一鏡的 /TRUCK:L」多一句、少一個「未驗證」警告；DSL 輸入和其他模型的輸出都不變。
- 檔案：scripts/adapters.py, models/minimax_h3.md, research/h3_lab_findings.md, tests/model_adapters.md,
    tests/reality/minimax_h3/results.json, tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/10_results.md, CHANGELOG.md

## CL-008 · 2026-09-30 · H3 實測第 1 波（8 格）結果

- 原因：維護者指示先跑 A 方案（第 1 波 8 格），用 H3-PDD 8 步。
- 修改前：8 格都是 NOT_RUN，沒有 results.json。
- 修改後：
    8 格 × 3 seed＝24 條，量測和目視都判完，寫進 results.json 和 01、07、10。
    TILT-UP：PASS（A）。PAN-L、TRUCK-L、PED-DOWN：PARTIAL（C）。TRUCK-R、ROLL-CW、SEQ-PAN-DOLLY：PARTIAL（D）。SEQ-FOLLOW-ORBIT：FAIL（F）。
    SEQUENTIAL_MOVEMENT：PARTIAL；SEQUENCE_RELIABILITY：LOW；其他區仍是 NOT_RUN，FINAL 不下結論。
    MODEL_LIMITATIONS 依第 1 波實測填寫。量測有兩條被目視推翻（TRUCK-L seed 1003、ROLL-CW seed 1001），原因寫在該 seed 的備註。
- 影響 Command：無
- 影響 Adapter：無（轉接器用字沒改）
- 影響 Test：實測第 1 波 8 格的狀態；run_tests 566/566 不變
- 是否破壞 backward compatibility：否
- 檔案：tests/reality/minimax_h3/results.json, tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/07_sequences.md,
    tests/reality/minimax_h3/10_results.md, CHANGELOG.md

## CL-007 · 2026-09-30 · H3 實測改用 H3-PDD 8 步

- 原因：維護者指定 H3 實測用 H3-PDD 8 步跑，不用 20 步。
- 修改前：實測設定寫「草稿檔位 416×736／8 步」，走實驗室原本的取樣（res_multistep、simple 排程），沒有加速 LoRA。
- 修改後：
    實測的 runner spec 多一個 `"sampler": "pdd8"`：Ref2VA 8 步加速 LoRA（Ref2VA-Acc-8Step）、euler、CFG 1.0、shift 12/3，
    其餘（Ref2VA pruned int8、416×736、3 seed、送出前 lint）不變。01–10 的說明與 10_results.md 開頭寫明生成設定，並註明結果只代表這個設定。
    runner 那邊的 PDD 接法照加速外掛的官方範例工作流；runner 不在 repository 裡。
- 影響 Command：無
- 影響 Adapter：無
- 影響 Test：實測（tests/reality/minimax_h3）的生成設定；run_tests 566/566 不變
- 是否破壞 backward compatibility：否
- 檔案：tests/reality/minimax_h3/tools/h3_reality.py, tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/02_angle_height.md,
    tests/reality/minimax_h3/03_tracking.md, tests/reality/minimax_h3/04_complex_motion.md, tests/reality/minimax_h3/05_focus.md,
    tests/reality/minimax_h3/06_combinations.md, tests/reality/minimax_h3/07_sequences.md, tests/reality/minimax_h3/08_negative_cases.md,
    tests/reality/minimax_h3/09_storyboard_cases.md, tests/reality/minimax_h3/10_results.md, research/07_design_decisions.md, CHANGELOG.md

## CL-006 · 2026-09-30 · PUBLIC_RELEASE_GATE 指令

- 原因：維護者要求重新跑 PUBLIC_RELEASE_GATE。之前沒有這個名稱的可重複指令，這次做成正式指令，以後每次公開前都能照跑。
- 修改前：公開檢查分散在各項稽核裡。沒有密鑰、email、repository 整潔、SKILL.md 格式的檢查。實測結果檔會記錄影片的本機完整路徑。
- 修改後：
    `python scripts/audit.py --release` 一次跑完全部稽核、全部測試和公開專用檢查，輸出 PUBLIC_RELEASE_GATE。
    公開專用檢查：LICENSE、隱私、第三方內容、密鑰與 email、repository 整潔、SKILL.md 格式、DSL 基準。已用樣本驗證會擋。
    實測結果只記檔名。
    授權登記檔補上 CL-005 之後的重新比對紀錄（Skill 本體 0 段無法解釋的相同文字）。
    所有入口腳本不再寫 `__pycache__`，並新增 `.gitignore`：在沒設任何環境變數的乾淨機器上跑閘門，也不會被自己產生的快取判成不整潔。
- 影響 Command：無
- 影響 Adapter：無
- 影響 Test：無（run_tests 566/566）
- 是否破壞 backward compatibility：否
- 檔案：scripts/audit.py, scripts/run_tests.py, scripts/camera_dsl.py, tests/reality/minimax_h3/tools/h3_reality.py, research/license_register.yaml, README.md, CHANGELOG.md, .gitignore

## CL-005 · 2026-09-30 · LICENSE 填入著作權人

- 原因：維護者提供 MIT 授權的正式權利人名稱。
- 修改前：LICENSE 的著作權行是 `Copyright (c) 2026 <COPYRIGHT_HOLDER>`，公開檢查（PUBLISH）持續警告。
- 修改後：`Copyright (c) 2026 Sidekick Animation Studio Ltd.`；README 授權段落與 research/06 公開清單同步更新。
- 影響 Command：無
- 影響 Adapter：無
- 影響 Test：無（run_tests 566/566；稽核 0 錯誤、0 警告）
- 是否破壞 backward compatibility：否
- 檔案：LICENSE, README.md, research/06_license_notes.md, CHANGELOG.md

## CL-004 · 2026-09-30 · 公開準備：MIT 授權、去除本機路徑與私人資訊、實驗室結論公開索引

- 原因：維護者決定採 MIT 並準備公開（GitHub、MiniMax 投稿）。公開前要清掉本機路徑、真實作品的角色與素材、散落的人名，以及私人實驗室的行號與條目編號。
- 修改前：
    沒有 LICENSE。
    實測工具寫死本機路徑（實驗室、ComfyUI）；實測用真實作品的角色與參考圖檔名。
    規則、測試、研究紀錄、程式註解裡散落人名，約 60 處。
    約 55 處用私人實驗室的行號、條目編號引用結論，外人看不懂。
    README 有一段私人工作室的內部規則。
- 修改後：
    新增 LICENSE（MIT）；著作權人留 `<COPYRIGHT_HOLDER>` 佔位字，等維護者提供正式權利人名稱。
    實測工具改讀環境變數：CAMERA_DSL_H3_LAB、CAMERA_DSL_H3_OUTPUT、CAMERA_DSL_TEST_ASSET_ROOT、CAMERA_DSL_COMFY_PYTHON。
    參考圖改用中性素材 CHARACTER_A_FACE.png、CHARACTER_A_OUTFIT.png、CHARACTER_B_FACE.png、CHARACTER_B_FULLBODY.png。
    提示詞的角色改成 the young woman／the young man；風格句拿掉作品題材。
    人名換成「維護者」或規則名稱，包括 BASELINE_V2.md 的一句（凍結的數字、清單、指紋都沒改）。
    私人實驗室引用改成公開編號 H3LAB-*，並新增公開索引 research/h3_lab_findings.md。
    README 刪除私人工作室段落，新增授權段落與環境變數說明。實驗室 lint 的位置也改讀環境變數。
    稽核新增 PUBLISH 項：檢查 LICENSE、本機絕對路徑、私人名稱（名稱清單只存雜湊值）。已用 7 個樣本驗證。
- 影響 Command：無。DSL、解析、驗證都不變。
- 影響 Adapter：minimax_h3 的警告句把引用改成公開編號、白話規則改用規則名稱；運鏡句本身不變。
- 影響 Test：
    Source 欄與 REG-18c、REG-23 的說明改用公開編號，斷言不變；run_tests 566/566 PASS。
    H3 實測 42 格的提示詞改用中性素材重建（尚未生成，沒有結果受影響）。
- 是否破壞 backward compatibility：否
- 檔案：LICENSE, BASELINE_V2.md, CHANGELOG.md, README.md, examples/action.md, examples/basic.md, examples/dialogue.md, examples/storyboard.md, models/minimax_h3.md, references/04_camera_height.md, references/06_camera_translation.md, references/07_tracking_complex_motion.md, references/08_camera_rig_behavior.md, references/13_continuity.md, registry/provenance.yaml, research/01_sources.md, research/03_command_inventory.md, research/04_terminology_conflicts.md, research/05_gap_analysis.md, research/06_license_notes.md, research/07_design_decisions.md, research/h3_lab_findings.md, research/license_register.yaml, scripts/adapters.py, scripts/audit.py, scripts/camera_dsl.py, tests/conflicts.md, tests/model_adapters.md, tests/regression.md, tests/sequences.md, tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/02_angle_height.md, tests/reality/minimax_h3/03_tracking.md, tests/reality/minimax_h3/04_complex_motion.md, tests/reality/minimax_h3/05_focus.md, tests/reality/minimax_h3/06_combinations.md, tests/reality/minimax_h3/07_sequences.md, tests/reality/minimax_h3/08_negative_cases.md, tests/reality/minimax_h3/09_storyboard_cases.md, tests/reality/minimax_h3/10_results.md, tests/reality/minimax_h3/tools/h3_reality.py

## CL-003 · 2026-09-30 · 授權清理：逐字比對、改寫、授權登記、License Warning 結案

- 原因：維護者要把 Skill 放上 GitHub、投稿 MiniMax。授權模糊的來源只能是研究參考，不能把別人的 skill 內容搬進來。
- 修改前：
    5 個 LICENSE_WARNING 未結案（稽核 5 個警告）。
    逐字比對發現約 20 句從 SRC-004、SRC-009（都是 MIT）原樣進到 Skill 本體：分屈光鏡定義、連戲參考開頭句、Kling 的預設＋運鏡詞、H3 整圈環繞句與甩鏡句、Veo／通用靜止句、滑動變焦句、拉鏡句。
    研究筆記有幾段長引文；README 沒有真正列出來源。
- 修改後：
    上述句子全部改寫成自己的話，語意與標記詞不變。研究筆記的長引文，以及授權不清楚來源的引文，改成意譯並標出處。
    新增 research/license_register.yaml：40 個來源逐一登記 source、license、use_type、copied_content、attribution_required、commercial_reuse、status，並附比對方法與結果。
    5 個警告全部結案。稽核改為依登記檔檢查（已用 6 種做壞的登記驗證會擋）。
    README 新增「來源與授權」；research/06 新增結案紀錄與公開前清單。
- 影響 Command：輸出文字改變：/STATIC、/DOLLYZOOM、/DOLLYOUT、/WHIPPAN（H3）、/ORBIT 整圈（H3）。只改登錄表文字、語意不變：/SPLITDIOPTER 定義、/STATIC 的 video_behavior、/DOLLYOUT 定義。指令、別名、文法都沒有增減。
- 影響 Adapter：generic_video、veo（靜止、滑動變焦、拉鏡）；minimax_h3（整圈環繞、甩鏡）；kling 中文（靜止句）
- 影響 Test：修改 MS-H3-04、MS-H3-06、MS-VEO-02、VID-007 的斷言（改成新句子）；run_tests 566/566 PASS；稽核 0 錯誤、0 警告
- 是否破壞 backward compatibility：否。DSL 輸入、解析、驗證結果都不變；只有上列指令的輸出用字改變。
- 檔案：README.md, registry/canonical_commands.yaml, scripts/adapters.py, scripts/camera_dsl.py, scripts/audit.py, models/generic_image.md, models/kling.md, models/veo.md, models/minimax_h3.md, references/01_shot_size.md, references/03_camera_angle.md, references/04_camera_height.md, references/06_camera_translation.md, references/08_camera_rig_behavior.md, references/10_zoom.md, references/11_focus_depth.md, references/13_continuity.md, references/14_aerial_drone.md, research/03_command_inventory.md, research/04_terminology_conflicts.md, research/06_license_notes.md, research/07_design_decisions.md, research/license_register.yaml, examples/action.md, examples/advanced_combinations.md, examples/basic.md, tests/model_adapters.md, tests/video_mode.md

## CL-002 · 2026-09-30 · V2.1 H3 實測矩陣與工具（尚未生成）

- 原因：維護者指示進入 V2.1 MINIMAX_H3_REALITY_VALIDATION，驗證 H3 轉接器是否忠實保留 Camera Intent。
- 修改前：H3 轉接器只有官方文件與第三方實測佐證。左搖、上搖、降機、順時針滾轉、左右橫移、一次生成內的先後運鏡，沒有本機實測。
- 修改後：新增 tests/reality/minimax_h3/。
    01–10 測試矩陣：42 格×3 seed，判定標準在生成前寫死。
    tools/h3_reality.py：組提示詞並跑實驗室 lint；光流量測，含合成影片自我檢驗與既有片校準；判定與報告。
    稽核的 MODEL 項目加上實驗室 lint 的句子檢查。
    實際生成尚未執行：出片要維護者明確同意。
- 影響 Command：無
- 影響 Adapter：無（只新增檢查）
- 影響 Test：新增實測矩陣 42 格（不在 run_tests 範圍，由 h3_reality.py 判定）；run_tests 566/566 不變
- 是否破壞 backward compatibility：否
- 檔案：tests/reality/minimax_h3/01_single_movement.md, tests/reality/minimax_h3/02_angle_height.md, tests/reality/minimax_h3/03_tracking.md, tests/reality/minimax_h3/04_complex_motion.md, tests/reality/minimax_h3/05_focus.md, tests/reality/minimax_h3/06_combinations.md, tests/reality/minimax_h3/07_sequences.md, tests/reality/minimax_h3/08_negative_cases.md, tests/reality/minimax_h3/09_storyboard_cases.md, tests/reality/minimax_h3/10_results.md, tests/reality/minimax_h3/tools/h3_reality.py, scripts/audit.py

## CL-001 · 2026-09-30 · H3 轉接器：序列時間用語與白話修正（生成前檢查）

- 原因：生成前逐句檢查 H3 提示詞，發現兩個問題。
    (1) `/MS 0-3s: /PAN:R 3-7s: /DOLLYIN:SLOW` 的 H3 句子寫推軌「over the whole video」，還在 3 秒處重述開場景別，和 DSL 的時間段矛盾；一般轉接器的後段也寫「From this opening framing」。
    (2) 鳥瞰、肩扛的 H3 句子有比喻（like a、as if），違反白話規則（H3LAB-PLAIN-01），被實驗室 lint 擋下。
- 修改前：H3 序列句：「At about 3 seconds, the camera starts on a medium shot … It pushes in steadily over the whole video.」
    鳥瞰：「the ground looks like a map」。肩扛：「as if carried on a shoulder」。
- 修改後：H3 序列句：「For the first 3 seconds, the camera stays in place and pans right. At about the 3-second mark, the camera pushes in toward <Subject> steadily for the rest of the video.」（實驗室 H3LAB-TIME-01 驗證過的時間句型）。
    鳥瞰：「the camera is far above and looks straight down. The ground fills the frame, and … is small in it.」
    肩扛：「sways slightly, carried on a shoulder」。一般轉接器序列後段：不再寫「From this opening framing」。
- 影響 Command：時間段或 THEN 序列裡的所有運鏡（只影響序列）；/BIRDSEYE、/SHOULDER（只影響 H3）
- 影響 Adapter：minimax_h3（序列、鳥瞰、肩扛）；generic_video 與 veo（序列後段的開場句）
- 影響 Test：新增 SEQ-031、SEQ-032、REG-23、REG-24；修改 SEQ-021、SEQ-029 的 H3 時間用語斷言；run_tests 566/566 PASS
- 是否破壞 backward compatibility：否。DSL 輸入、解析、驗證結果都不變；只有上述情況的輸出文字改變。
- 檔案：scripts/adapters.py, tests/sequences.md, tests/regression.md, models/minimax_h3.md, research/07_design_decisions.md, examples/action.md

## CL-000 · 2026-09-30 · 凍結 V2 為 V2_BASELINE

- 原因：維護者指示把 CINEMATIC_DIRECTOR_CAMERA_DSL_V2 凍結為基準，之後所有修改都要可追溯。
- 修改前：開發版，沒有基準也沒有變更紀錄。V2 開發期間的設計決策記在 `research/07_design_decisions.md` D01–D40。
- 修改後：V2_BASELINE。
    數字：Canonical Commands 104、Aliases 244、Grammar Rules 18、Compatibility Rules 58、Conflict Rules 83、Tests 562/562 PASS。
    檔案指紋記在 BASELINE_V2.md。
    凍結時一併做了：registry 版本字串 1.0.0 → 2.0.0；SKILL.md、README.md 加凍結規則；audit.py 加 BASELINE 稽核。
- 影響 Command：無
- 影響 Adapter：無（輸出文字不變）
- 影響 Test：無（562/562 維持）
- 是否破壞 backward compatibility：否
- 檔案：BASELINE_V2.md, CHANGELOG.md
