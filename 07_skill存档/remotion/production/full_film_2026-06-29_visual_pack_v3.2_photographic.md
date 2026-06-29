# 全片 v3.2 视觉生产包（2026-06-29）· 超现实摄影版 · P1 九场景 MJ + Seedance

> 项目：Skill Is All You Need / SkillIsAllYouNeedFullFilm
> **风格改向（2026-06-29 用户拍板）**：从 v3.1 的「扁平矢量图解」整体改为 **Gregory Crewdson 式超现实概念摄影 + 真实（无脸）人物形象**。**v3.1 视觉包（`full_film_2026-06-27_visual_pack_v3.1.md`）整套作废**，本包替代。
> 文稿源：`production/full_film_2026-06-16_script_v3.1_locked.md`（口播稿/节奏不变，只换视觉皮）
> 配音层：已封口（take3 / 2:28），不动。

---

## 〇、核心约束（先读）

1. **统一世界观**：所有场景都发生在**同一个昏暗机构空间——既是产房又是停尸间**（maieutic↔postmortem 生死母题的实体化）。苍白瓷砖墙、不锈钢台面、体积雾气；光从左侧暖琥珀经中性无缝过渡到右侧冷临床蓝。
2. **人物一律无脸**：助产士/法医/创作者都**背身、逆光或剪影，脸永不可见**（MJ 极易补脸且脸会跨 sref 漂移，正文+`--no` 双重压制）。
3. **画面不承载文字**：语义靠**人物姿态 + 象征实物 + 冷暖光编码**。中文一律交 Remotion 顶/底 Label + 字幕（已在 sceneSpecs 里）。`--no text` 防 MJ 乱印。可数概念用**可数实物**（如 11 张卡 = 数得出的 11 张纸），不写数字。
4. **画幅 16:9**，渲染时素材以 1120×630 居中带框卡片呈现，**下三分之一留白**给字幕——每条 prompt 都带 `generous clean negative space across the lower third`。
5. **禁线**：no gore / no blood / 不血腥；poetic macabre + quiet dread + tender，克制惊悚不恐怖。

---

## 一、统一风格 SPINE（每条 MJ prompt 末尾固定接上）

```
surreal conceptual fine art photograph, Gregory Crewdson-style cinematic tableau, a dim institutional chamber that is at once a delivery room and a morgue, pale tiled walls and stainless steel surfaces, lighting blends seamlessly from warm amber on the left through a soft neutral middle into cold clinical blue on the right with no hard seam, eerie symmetry, poetic macabre, quiet dread, tender and reverent, no gore, no blood, soft chiaroscuro, muted desaturated palette, warm-amber-to-clinical-blue split color grading, volumetric atmospheric haze, medium format film grain, eye-level large-format clarity, deep focus, generous clean negative space across the lower third for subtitles --ar 16:9 --v 8.1 --style raw --sref <SCENE00_ANCHOR> --no text, letters, words, numbers, watermark, logo, visible face, facial features, eye contact, gore, blood, open wound, deformed hands, extra limbs, low quality
```

### sref 锁定协议
1. **scene_00 已定稿为锚**（2026-06-29，Crewdson 生死检验台，暖助产抱发光襁褓→中央覆布遗体→冷法医俯身）。
2. 把 scene_00 定稿图的 **sref code**（或图链）填入上方 SPINE 的 `<SCENE00_ANCHOR>`，其余 8 场景全部复用——保证 9 场景像同一部片子。
3. 每场景出 ≥4 版挑最佳；人物姿态/象征物不对就换 sref code 重抽（sref 编号独立律）。

---

## 二、世界 / 角色物词典（跨场景**逐字复用**，一致性命根）

| 元素 | 复用描述（嵌进对应场景 prompt） |
|---|---|
| 空间 | `a dim institutional chamber, pale tiled walls, a long stainless steel examination table, volumetric haze` |
| 助产士 | `a faceless midwife in soft pale clothing, seen from a three-quarter back angle, her face never visible, bathed in warm amber light` |
| 法医 | `a faceless coroner in dark clothing, seen from behind or in silhouette, his face never visible, lit by cold clinical blue` |
| 创作者 | `a faceless solitary figure, seen from behind, face never visible, plain clothing` |
| 新生儿(=新作品) | `a swaddled newborn held as a softly glowing white bundle` |
| 遗体(=待复盘的作品/一生) | `a full-length human body lying under a thin luminous sheet` |
| 手册(=Skill) | `a worn hardcover manual with faintly glowing blank pages, no readable text` |
| 标签(=标记/判断) | `a small blank paper tag tied with pale string` |
| 假经验之塔 | `a tall unstable tower of identical pale document-cards rising into the haze` |

---

## 三、九场景逐条（MJ key visual + Seedance motion）

> 资产目录：`public/assets/full_film_20260627/<sceneId>/mj_key_visual.png` + `seedance_motion.mp4`（沿用现有目录骨架，sceneId 不变，只换视觉内容）
> Seedance 一律：以 MJ 图当首帧+风格参考，克制运动、锁定机位为主、底部留字幕区、无额外文字/水印；4–6s；timeRange 入库时按场景本地帧设（覆盖该场景最活跃口播 beat）。

### scene_00_two_partners · 冷开场（≈21s）★已定稿=sref 锚
**画面**：贯穿全宽的不锈钢检验台读作"一生左→右"。左端暖琥珀光，无脸助产士（四分之三背侧、低头）抱发光白襁褓；中央薄发光布下的全身遗体；右端冷蓝光，无脸法医侧身俯向中央遗体、持检验工具、视线沿台面看遗体。暖→中性→冷无缝渐变。
**MJ**：已定稿，无需再出。其 sref code 作全片锚。
**Seedance**：`0-2s very slow push-in toward the warm amber left end, the swaddled bundle glowing softly; 2-4s a slow lateral drift right along the table past the central shrouded body; 4-6s settle on the cold blue coroner end. Locked, gentle, funereal calm.`（左→右扫过"一生"，正好压冷开场旁白）

### scene_01_what_is_skill · 它们是什么=Skill（≈8.6s）
**隐喻**：助产与法医依靠的是**同一本手册**——两端不同的工作，靠同一本"Skill"。
**MJ**：
```
At the exact center of the long stainless steel examination table stands a single worn hardcover manual with faintly glowing blank pages, open on a small steel stand; a faceless midwife in soft pale clothing leans in from the warm amber left and a faceless coroner in dark clothing leans in from the cold clinical blue right, both reading from the same open manual, their faces never visible; the amber and blue light meet exactly on the glowing open pages at center; the shared manual is the clear focal point. <SPINE>
```
**Seedance**：`0-1.5s the two faceless figures lean toward the central manual from each side; 1.5-3s the open pages pulse with one soft glow as both consult it; 3-4.5s settle, the manual holding center. Locked camera, very slow push-in.`

### scene_02_coroner_rule · 法医的铁律（≈6.7s）
**隐喻**：先冻结事实，再写判断——法医先把"事实记录"按住冻结，才提笔。
**MJ**：
```
On the cold clinical blue right side of the steel table, a faceless coroner's gloved hand presses flat and perfectly still on a single pale sheet of paper pinned to the steel, holding it down; thin cold vapor of frost rises around the pinned sheet as if it is being frozen in place; a fountain pen waits untouched beside it, not yet used; one narrow shaft of cold light pins the sheet; authoritative, clinical, restrained, the frozen sheet is the focal point. <SPINE>
```
**Seedance**：`0-1s the gloved hand settles flat onto the sheet; 1-2.5s frost vapor creeps across the paper and it stills, one firm freeze; 2.5-4s the pen lifts slightly but holds, waiting. Locked camera, restrained, cold.`

### scene_03_crash_case · 真实翻车（≈23s）★唯一硬演示，最丰富
**隐喻**：一份普通复盘记录被误别上金色"获奖"绶带 → AI 把它膨胀成 11 张自我表扬的"成功经验"卡，叠成摇摇欲坠的高塔 → 一道冷光戳穿：塔是空的，绶带是假的，其实没获奖。
**MJ**：
```
A faceless solitary figure seen from behind stands dwarfed before the steel table, where instead of a body lies a single small ordinary photographic print pinned with a gaudy golden award rosette ribbon; from that print a tall unstable tower of exactly eleven identical pale document-cards balloons upward into the warm amber haze, glowing self-congratulatory and seductive; from the cold clinical blue right a single hard shaft of light cuts in and the topmost cards are already dissolving into thin smoke, revealing the tower casts no real shadow and the golden ribbon is hollow; dramatic cause-and-effect from warm seduction on the left to cold revelation on the right; eleven countable cards, the inflated hollow tower is the focal point. <SPINE>
```
**Seedance**：`0-1.5s the small print with the gold ribbon sits warmly lit; 1.5-4s the eleven pale cards rapidly stack and inflate upward into a tall glowing tower; 4-5.5s a cold blue shaft cuts in from the right and the top cards dissolve into smoke, the tower flinches and reveals it casts no shadow; 5.5-6s unstable settle. Locked camera, slightly faster nervous energy than other scenes.`

### scene_04_freeze_facts · 修复 + payoff（≈19.5s）
**隐喻**：SKILL 手册顶部那段"事实记录"被钢锁条物理锁死（不可改区）；一道横栏拦下从冷侧伸来要提前下笔的手——填完锁死的事实区前不准写。
**MJ**：
```
At the neutral center of the steel table lies an open worn manual; pinned across its very top third is a heavy steel locking bar with a small padlock, sealing that upper section as an unchangeable record zone; from the cold clinical blue right a faceless figure's hand reaches to write but is halted by a thin taut chain stretched across the table like a checkpoint gate; a pen hovers, stopped; procedural, authoritative, the locked top zone and the halted hand are the focal points. <SPINE>
```
**Seedance**：`0-1s the open manual settles at center; 1-2.5s the steel locking bar snaps across its top with a padlock click; 2.5-4s a hand reaches in from the blue right and is stopped by the taut chain, the pen halts; 4-5s stable. Locked camera, slow push-in.`

### scene_05_markdown_form · 手册的形态（≈12s）
**隐喻**：这本手册拆成两层——小小的"触发头"（什么时候翻开我）+ 厚的"规矩正文"（照着做什么）。
**MJ**：
```
A single worn manual open on a steel stand at the neutral center of the table; its small top leaf lifts and floats slightly upward as a separate translucent glowing page (the trigger: when to open it), while the larger body of pages stays below (the rules to follow); a thin thread of light links the floating top leaf down to the body, showing one file made of two layered parts; clean, structural, two glowing layers, the layered manual is the focal point. <SPINE>
```
**Seedance**：`0-1s the open manual settles; 1-2.5s the small top leaf lifts and separates upward as its own glowing page; 2.5-4s the lower body expands into layered pages and a thread of light connects the two; 4-5s the two parts hold as one stable two-layer structure. Locked camera, very slow push-in.`

### scene_06_three_mistakes · 三个误区（≈18s）清单快切
**隐喻**：长台上并排三个不锈钢托盘=三宗"翻车的案子"，各有一个小红警示灯：①当魔法（魔术手套+一缕烟）②漏文件（空文件夹，纸张不见）③不存版本（一张被涂改覆盖的纸+空抽屉，没有备份）。
**MJ**：
```
Three identical small stainless steel trays placed evenly in a row along the dim examination table, each a separate cautionary still life under its own small red warning light: the LEFT tray holds a magician's white glove and a thin curl of smoke (treating it as magic); the MIDDLE tray holds an open empty file folder with its papers gone (missing referenced files); the RIGHT tray holds a single sheet smudged and overwritten beside an open empty drawer (no saved version, no backup); evenly spaced, equal weight, checklist feel, three universal symbolic objects, no text, generous clean space below. <SPINE>
```
**Seedance**：`0-1s the three trays sit in a row; 1-3.5s each red warning light flicks on in sequence left to right with one short emphatic pulse over its object; 3.5-4.5s all three hold, lit. Locked camera, crisp staccato timing.`

### scene_07_whole_life_close · 收束·一生（≈20.7s）
**隐喻**：呼应 scene_00，但创作者现在**完整地站在台中央**；暖助产在一端、冷法医在另一端环绕；一条连续光环从暖"出生"端绕过创作者到冷"落幕"端，闭合成完整的一生。温暖、释然、略动情。
**MJ**：
```
A faceless solitary figure seen from behind stands whole and calm at the exact center of the long steel table; to the warm amber left a faceless midwife with a softly glowing swaddled bundle, to the cold clinical blue right a faceless coroner bowing gently; a single continuous loop of soft light runs from the warm birth end, around through the central figure, to the cold closure end, closing into a complete circle of one whole life; warm, resolved, quietly emotional, the closed loop of light and the central figure are the focal points. <SPINE>
```
**Seedance**：`0-1.5s the central figure stands settled; 1.5-3.5s the loop of light draws itself from the warm birth end around through the figure to the cold closure end; 3.5-5s the ring closes with a soft warm glow; 5-6s stable, gentle. Locked camera, slow push-in, emotional restraint.`

### scene_08_author_note · 作者的话（≈16.8s）
**隐喻**：夜工坊感。无脸创作者在钢台前，四样微光物绕着他——画面（一张照片冲印）/ 配音（发光声波/小喇叭）/ 剪辑（一截胶片）/ **开源手册（发光手册，最亮、最强调）**——细光线把四样连到创作者手上，最后落到"开源"。
**MJ**：
```
A faceless solitary figure seen from behind works at the steel table in the dim chamber at night; four faint glowing objects float in an arc around the figure's hands: a single photographic print (image), a small glowing speaker with a soft soundwave (voice), a short strip of film (editing), and a worn open manual glowing brightest of all (open source); thin threads of light connect all four objects to the figure's hands, the bright open manual slightly emphasized as the final node; warm, intimate, night-workshop mood, the glowing open manual is the focal point. <SPINE>
```
**Seedance**：`0-1s the figure settles at the table; 1-3s the print, speaker, and film strip fade in one by one with threads of light drawing to the hands; 3-4.5s the open manual glows up last and brightest with one emphasized pulse; 4.5-6s stable, warm. Locked camera, intimate, gentle.`

---

## 四、入库 + 接渲染（出图后我来做）

1. MJ 出图挑定 → 落 `public/assets/full_film_20260627/<sceneId>/mj_key_visual.png`；Seedance → `seedance_motion.mp4`。（目录骨架 2026-06-29 已建好）
2. 在 `src/data/sceneAssets.ts` 为每个 sceneId 注册：`foreground-image`（key visual，无 timeRange，全程）+ `video-insert`（Seedance，`timeRange` 场景本地帧覆盖活跃 beat），`status:'linked'`。
3. `public/assets/` 默认被 git 跟踪（无忽略规则），无需改 .gitignore。
4. `npx remotion render src/index.ts SkillIsAllYouNeedFullFilm out/full-film-20260629-photographic.mp4` → 渲染自动换上素材。
5. 抽帧 + 跳蛛先生审；按需迭代单场景。

## 五、待跳蛛先生确认 / 开放项
- [ ] 把 scene_00 定稿图存入资产目录 + 取 **sref code** 回填 SPINE 的 `<SCENE00_ANCHOR>`。
- [ ] 逐场景出图（建议顺序：先 scene_07/scene_01 这类构图接近 scene_00 的，验证 sref 一致性最稳；scene_03 最难放最后多迭代）。
- [ ] 卡片框 vs 满屏：当前 1120×630 居中带框。若想满屏沉浸需改 `AssetLayer` 样式（动渲染）。
- [ ] scene_06 三托盘/scene_03 假经验塔 是符号最重的两场，若摄影出不来再考虑局部退回图形或 GPT Image 2。

## 关联
- 文稿：`production/full_film_2026-06-16_script_v3.1_locked.md`
- 工作日志：`production/full_film_2026-06-16_worklog_v3.1_checkpoint.md`
- 作废前身：`production/full_film_2026-06-27_visual_pack_v3.1.md`（扁平矢量版，已被本包替代）
- 铁律：`{知识库}/04_方法论与洞察/04_视频影像与声音/2026-06-09_Remotion全片音频字幕BGM复盘.md`（TTS 误读换词 / 字幕=口播 / 图不承载中文）
