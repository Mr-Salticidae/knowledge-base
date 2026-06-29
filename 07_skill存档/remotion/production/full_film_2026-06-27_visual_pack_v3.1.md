> ⚠️ **已作废（2026-06-29）**：风格改向超现实摄影+真实人物，本扁平矢量包不再使用。见 `full_film_2026-06-29_visual_pack_v3.2_photographic.md`。下方内容仅作历史参照。

# 全片 v3.1 视觉生产包（2026-06-27）· P1 九场景 MJ + Seedance

> 项目：Skill Is All You Need / SkillIsAllYouNeedFullFilm
> 阶段：配音层已封口（take3 / 2:28），进入 P1 视觉。决策：**全 9 场景上 MJ/Seedance + sref 统一风格**，不限数量、质量优先。
> 文稿源：`production/full_film_2026-06-16_script_v3.1_locked.md`；方案铁律源：`{知识库}/04_方法论与洞察/04_视频影像与声音/2026-06-09_Remotion全片音频字幕BGM复盘.md`

---

## 〇、核心约束（先读，决定每条 prompt 怎么写）

1. **MJ 图只承载视觉隐喻 + 配色编码，不依赖中文文字。**
   渲染时素材图接管场景 → 原生图形（含中文标签）被隐藏，只剩字幕 + 顶/底 Label。而 MJ 中文成字差。所以：
   - 语义靠 **画面隐喻 + 颜色编码 + 通用符号**（锁、警示三角、箭头、数字 11）。
   - 中文标签由 Remotion 顶/底 Label + 字幕承载（已在 sceneSpecs 里）。
   - **只有英文/数字标识可入图**：`SKILL`、`SKILL.md`、`11`、`TRIGGER`、`RULES`。
2. **画幅 16:9（`--ar 16:9`）。** 渲染时素材以 **1120×630 居中带框卡片** 呈现（深描边+投影+白底，像贴在工作台上的插画），四周露出原生网格背景，字幕浮在卡片下方。
3. **构图自足、留白在下三分之一**：主体居中偏上，底部留干净空间（即使字幕在卡片外，也避免主体压到最底边）。
4. **禁用方向**（全片铁底线）：photorealistic / cinematic live-action / 3D realism / anime / oil painting / dark gritty / fashion editorial / 写实人脸。

---

## 一、统一风格 spine（每条 MJ prompt 末尾固定接上）

```
premium flat-vector educational explainer illustration, original high-end science-explainer style (Kurzgesagt-inspired, not a copy), thick dark ink outlines, simple bold geometric shapes, warm off-white paper background with a faint grid, restrained vivid palette limited to warm yellow / sky blue / soft green / coral red / ink navy, strong clear visual hierarchy, calm intelligent friendly tone, generous clean empty space in the lower third, no photorealism, no anime, no realistic human faces, no 3D realism, no cinematic lighting, no tiny unreadable text, no logo, no watermark --ar 16:9 --style raw --sref <ANCHOR>
```

### sref 锁定协议（保证 9 场景像同一部片子）
1. **先出 `scene_00`**（它一次性确立黄=助产手册、蓝=法医手册、绿=作品三件核心角色物）。
2. 出 4 版，挑审美 + 角色物造型最对的一张，**把它设为全片 `--sref` 锚**（用该图的 sref code 或直接当 sref 参考图）。
3. 其余 8 场景 prompt 里 `<ANCHOR>` 全替换成这个锚；角色物描述**逐字复用**下方词典。
4. 质量优先：每场景出≥4 版，挑最佳再 upscale；不满意就换 sref code 重抽（见 [[aigc-character-consistency]] sref 编号独立律）。

---

## 二、角色物词典（跨场景**逐字复用**，这是一致性的命根）

| 角色物 | 复用描述（嵌进对应场景 prompt） |
|---|---|
| 助产手册 | `a warm yellow handbook with a thick dark ink outline and a small folder tab, soft rounded corners, friendly` |
| 法医手册 | `a cool sky-blue handbook with a thick dark ink outline and a small folder tab, clean clinical look` |
| 作品(creation) | `a soft green rounded glowing abstract shape representing a creative work-in-progress` |
| SKILL 块 | `a single glowing block labeled "SKILL" in clean latin caps, warm gradient` |
| SKILL.md 文件 | `a white document card labeled "SKILL.md" with a dark code-style top bar, thick dark outline` |
| 创作者 | `a simple flat-vector person, calm posture, no facial detail, sky-blue clothing` |
| AI 机器人 | `a friendly cyan rounded robot with a simple smiling screen-face and a small antenna, thick dark outline` |
| 警示(误区) | `a bold warning triangle with thick dark outline` |

---

## 三、九场景逐条（MJ key visual + Seedance motion）

> 资产目录：`public/assets/full_film_20260627/<sceneId>/mj_key_visual.png` + `seedance_motion.mp4`
> Seedance 一律：以 MJ 图当首帧 + 风格参考，克制运动，底部留字幕区，无额外文字/水印；时长 4–6s；timeRange 入库时按场景本地帧设（覆盖该场景最活跃的口播 beat）。

### scene_00_two_partners · 冷开场（≈21s）★先出，定 sref
**隐喻**：左暖助产、右冷尸检，中间被托付"一生"的作品；一条淡淡的生命线把两端连起来。
**MJ**：
```
A symmetrical opening composition: on the left, [助产手册]; on the right, [法医手册]; in the exact center, [作品]; a faint thin life-thread arcs from the yellow side through the center work to the blue side, suggesting a whole lifespan from birth to closure; balanced, calm, iconic, lots of clean space below. <SPINE>
```
**Seedance**：`0-1s the yellow handbook on the left and the blue handbook on the right gently settle in with a soft paper bounce; 1-3s the central green work softly pulses and the faint life-thread draws itself from left through center to right; 3-4.5s everything settles into a stable balanced final pose. Locked camera with a very subtle slow push-in.`

### scene_01_what_is_skill · 它们是什么=Skill（≈8.6s）
**隐喻**：两本手册并列 → 合成一个发光 SKILL 块。
**MJ**：
```
Two handbooks side by side — [助产手册] and [法医手册] — converging toward the center where they merge into [SKILL 块]; clean arrows or light streams hint the two becoming one; the SKILL block is the clear focal point. <SPINE>
```
**Seedance**：`0-1.5s the two handbooks drift toward center; 1.5-3s light streams flow from both into the middle and a glowing SKILL block forms with one clean pulse; 3-4s stable final pose. Restrained, locked camera.`

### scene_02_coroner_rule · 法医的铁律（≈6.7s）
**隐喻**：法医手册旁，浮出红色铁律卡"先冻结事实，再写判断"（卡上不写中文，用红色锁定条 + 通用符号示意）。
**MJ**：
```
Focus on [法医手册], open; beside it a single bold coral-red rule card with a small lock icon and a horizontal divider line (a "freeze line"), no readable paragraph text; the blue handbook and red card are the only two elements, high contrast, authoritative, clean lower space. <SPINE>
```
**Seedance**：`0-1s the blue coroner handbook scales up gently at center; 1-2.5s a coral-red rule card with a lock icon slides in from the right and locks into place with one firm snap; 2.5-4s stable. Locked camera, restrained.`

### scene_03_crash_case · 真实翻车（≈23s）★唯一硬演示，最丰富
**隐喻**：白色复盘记录 → 被贴上黄色"获奖"标签（误标）→ AI 把它放大成 11 条绿色"成功经验"卡堆叠膨胀 → 红色警示戳穿"其实没获奖"。
**MJ**：
```
A narrative cross-section in one frame: a white review-document on the left; a yellow mislabel sticker slapped onto it (a small trophy/award icon, no chinese text); from it a rising stack of green cards multiplies upward, each stamped with a small check mark, exaggerated into a tall inflated pile of eleven cards with a clear numeral "11"; on the right a coral-red warning triangle punctures the pile. Cause-and-effect left-to-right flow, dramatic but clean. <SPINE>
```
**Seedance**：`0-1s the white document with the yellow award sticker settles; 1-3s green check-cards rapidly stack and inflate upward into a tall pile labeled 11; 3-4.5s a coral-red warning triangle pushes in from the right and the pile flinches/deflates slightly; 4.5-6s unstable settle. Locked camera, slightly faster energy than other scenes.`

### scene_04_freeze_facts · 修复+payoff（≈19.5s）
**隐喻**：SKILL.md 顶部锁死红色"事实记录·不可修改区"条；橙色关卡门 + 通用问号拦下 AI。
**MJ**：
```
[SKILL.md 文件] centered; pinned across its very top a coral-red locked band with a small padlock icon (a non-editable header zone); to the right an orange gate/checkpoint shape with a large question-mark blocking the flow downward; arrows show writing is stopped until the top is filled. Clean, procedural, authoritative. <SPINE>
```
**Seedance**：`0-1s the SKILL.md document fades/bounces in; 1-2.5s a red locked band snaps across the top with a padlock click; 2.5-4s an orange gate with a question-mark pops in and a small downward arrow is halted at the gate; 4-5s stable. Locked camera with a slow push-in.`

### scene_05_markdown_form · Markdown 形态（≈12s）
**隐喻**：SKILL.md 拆成 cyan"触发(TRIGGER)"头 + green"工作规矩(RULES)"正文，箭头相连。
**MJ**：
```
[SKILL.md 文件] visibly split into two stacked functional cards: a small cyan top card labeled "TRIGGER" (when to call) and a larger green body card labeled "RULES" (what to obey); a thin arrow connects the file to both parts showing structure; only latin labels SKILL.md / TRIGGER / RULES, no chinese, no dense paragraphs. <SPINE>
```
**Seedance**：`0-1s the SKILL.md file settles; 1-2.5s the cyan TRIGGER header lifts up and separates as its own card; 2.5-4s the green RULES body expands downward into a clean card; 4-5s the two reconnect to the file forming a stable two-layer structure. Locked camera, very slow push-in.`

### scene_06_three_mistakes · 三个误区（≈18s）清单快切
**隐喻**：三个并排警示 —— 红"当魔法"/橙"漏文件"/黄"不存版本"，用通用图标区分（魔法棒/缺页文件/无备份盘）。
**MJ**：
```
Three [警示(误区)] in a clean horizontal row, color-coded left-to-right: a coral-red one containing a small magic-wand-with-a-cross icon, an orange one containing a document-with-a-missing-page icon, a yellow one containing a no-backup disk icon; evenly spaced, equal weight, checklist feel, generous space below. <SPINE>
```
**Seedance**：`0-1s the three warning icons pop in left to right; 1-3.5s each icon does one short emphatic shake in sequence (red, then orange, then yellow); 3.5-4.5s all three settle in a stable row. Locked camera, crisp staccato timing.`

### scene_07_whole_life_close · 收束·一生（≈20.7s）
**隐喻**：创作者居中，黄助产+蓝法医手册环绕，"出生(绿)"与"落幕(紫)"两端，一条生命闭环把出生→落幕连起来。
**MJ**：
```
A circular system: [创作者] at the very center; [助产手册] orbiting upper-left and [法医手册] orbiting upper-right; a green "birth" marker lower-left and a purple "closure" marker lower-right; a continuous dashed life-loop ring connects birth around through the creator to closure, conveying a complete lifespan. Warm, resolved, slightly emotional, clean. <SPINE>
```
**Seedance**：`0-1.5s the creator pops in at center; 1.5-3s the yellow and blue handbooks zoom into orbit; 3-5s the dashed life-loop draws itself from the green birth marker around to the purple closure marker and the ring closes with a soft glow; 5-6s stable. Locked camera, gentle, emotional restraint.`

### scene_08_author_note · 作者的话（≈16.8s）
**隐喻**：cyan AI 机器人居中，四张卡（画面/配音/剪辑 + 橙色开源手册）网状相连，最后落到"开源"。
**MJ**：
```
A network-map: [AI 机器人] at center; four nodes around it — a yellow "image" card (a picture icon), a green "voice" card (a soundwave icon), a purple "edit" card (a film-strip/scissors icon), and an orange open-source handbook node (a branching/fork icon); thin connection lines link the robot to all four, the orange open-source node slightly emphasized; icons are universal, no chinese text. <SPINE>
```
**Seedance**：`0-1s the cyan robot scales up at center; 1-3s the image, voice, edit nodes pop in one by one and connection lines draw to the robot; 3-4.5s the orange open-source node pops in last with one emphasized pulse and a connection line; 4.5-6s stable. Locked camera, friendly.`

---

## 四、入库 + 接渲染（出图后我来做）

1. MJ 出图挑定 → 落 `public/assets/full_film_20260627/<sceneId>/mj_key_visual.png`；Seedance → `seedance_motion.mp4`。
2. 在 `src/data/sceneAssets.ts` 为每个 v3.1 sceneId 注册：
   - `foreground-image`（key visual，无 timeRange，全程）+ `video-insert`（Seedance，`timeRange` 场景本地帧覆盖活跃 beat），`status:'linked'`。
   - 注意 `.gitignore` 需放行 `public/assets/full_film_20260627/`（镜像现有 assets 白名单）。
3. `npx remotion render src/index.ts SkillIsAllYouNeedFullFilm out/full-film-20260627-visual.mp4` → 渲染自动换上素材。
4. 抽帧 + 跳蛛先生审；按需迭代单场景。

## 五、待跳蛛先生确认 / 开放项
- [ ] scene_00 出图后定 sref 锚（全片风格命根）。
- [ ] 卡片框观感：当前 1120×630 居中带框。若想要**满屏沉浸**（无框 full-bleed），需把 binding 改 `background-image` 或改 `AssetLayer` 样式——这会动渲染，定 sref 时一并拍。
- [ ] 含中文是否真的全交给 Remotion Label？若某场景坚持图内中文，按 [[aigc-tool-default-choice]] 改用 GPT Image 2（但会脱离 MJ sref 体系）。

## 关联
- 文稿：`production/full_film_2026-06-16_script_v3.1_locked.md`
- 工作日志：`production/full_film_2026-06-16_worklog_v3.1_checkpoint.md`
- 旧素材包（旧脚本，作 prompt 风格参照）：`production/full_film_2026-06-10_mj_seedance_replacement_pack.md`
- 铁律：[[2026-06-09_Remotion全片音频字幕BGM复盘]]（TTS 误读换词 / 字幕=口播）
