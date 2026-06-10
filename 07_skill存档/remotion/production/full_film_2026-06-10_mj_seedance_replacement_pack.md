---
tags: [类型/制作文档, 项目/SkillIsAllYouNeed, 工具/Midjourney, 工具/Seedance, 工具/Remotion, 状态/生产包]
created: 2026-06-10
---

# Skill Is All You Need · 全片 MJ / Seedance 素材替换生产包

## 目标

在已验证通过的 `SkillIsAllYouNeedFullFilm` 框架视频上，用 Midjourney 关键视觉和 Seedance 2.0 五秒机制动效替换一部分 Remotion 原生占位画面。

本轮不改旁白、不改 BGM、不改全片结构。Remotion 继续负责：

- 全片时间线；
- 中文字幕；
- BGM 淡入淡出；
- 静态关键图持帧；
- Seedance 短动效的裁切、淡入、淡出和兜底。

Seedance 不承担整段视频，只承担 5 秒左右的“机制运动”。

## 当前基准

- Composition: `SkillIsAllYouNeedFullFilm`
- 当前全片帧数: `6492`
- FPS: `30`
- 当前成片时长: `216.45s`
- 已完成素材:
  - `scene_04_repeat_to_skill`: MJ + Seedance 已接入；
  - `scene_05_markdown_structure`: MJ + Seedance 已接入；
  - `formal_clip_20260608` 的 01 / 04 / 05 素材可作为风格参考，但不直接等同于全片 scene 资产。

## 全片 Scene 时长参考

| sceneId | startFrame | duration | seconds | 本轮策略 |
|---|---:|---:|---:|---|
| scene_00_intro_question | 0 | 786 | 26.20 | A 批次，新做 MJ + Seedance |
| scene_01_hook | 786 | 260 | 8.67 | B 批次，可新做或保留 Remotion |
| scene_02_forgetful_assistant | 1046 | 265 | 8.83 | A 批次，新做 MJ + Seedance |
| scene_03_skill_as_manual | 1311 | 253 | 8.43 | B 批次，可新做或保留 Remotion |
| scene_04_repeat_to_skill | 1564 | 327 | 10.90 | 已完成，复用 |
| scene_05_markdown_structure | 1891 | 278 | 9.27 | 已完成，复用 |
| scene_06_skill_index | 2169 | 286 | 9.53 | A 批次，新做 MJ + Seedance |
| scene_07_common_mistakes | 2455 | 264 | 8.80 | B 批次，可新做 |
| scene_08_ending_system | 2719 | 239 | 7.97 | B 批次，可新做 |
| author_01_loop_closed | 2958 | 199 | 6.63 | C 批次，可保留 Remotion |
| author_02_ai_made_this | 3157 | 359 | 11.97 | B 批次，可复用工具链图 |
| author_03_motivation | 3516 | 444 | 14.80 | A 批次，新做 MJ + Seedance |
| author_04_stack | 3960 | 776 | 25.87 | A 批次，新做 MJ + Seedance |
| author_05_codex_conductor | 4736 | 240 | 8.00 | B 批次，可新做 |
| author_06_industrialization | 4976 | 447 | 14.90 | A 批次，新做 MJ + Seedance |
| author_07_open_source | 5423 | 742 | 24.73 | C 批次，建议 Remotion 原生宣言卡 |
| author_08_final_words | 6165 | 282 | 9.40 | C 批次，建议 Remotion 原生片尾 |

## 生产批次

### A 批次：优先替换

优先做 6 个最能提升观感和信息表达的场景：

1. `scene_00_intro_question`
2. `scene_02_forgetful_assistant`
3. `scene_06_skill_index`
4. `author_03_motivation`
5. `author_04_stack`
6. `author_06_industrialization`

这些场景信息密度高，当前原生画面容易显得空或重复；用 MJ 建立视觉锚点、Seedance 做短机制动效，收益最大。

### B 批次：可选替换

1. `scene_01_hook`
2. `scene_03_skill_as_manual`
3. `scene_07_common_mistakes`
4. `scene_08_ending_system`
5. `author_02_ai_made_this`
6. `author_05_codex_conductor`

这些 scene 可以继续用 Remotion 原生，但如果 A 批次风格稳定，再补它们会让全片更统一。

### C 批次：保留 Remotion 原生

1. `author_01_loop_closed`
2. `author_07_open_source`
3. `author_08_final_words`

这三段更适合文字、宣言卡、片尾节奏。Seedance 介入反而可能削弱表达。

## 统一文件命名

```text
public/assets/full_film_20260610/
  scene_00_intro_question_mj_key_visual.png
  scene_00_intro_question_seedance_motion.mp4
  scene_02_forgetful_assistant_mj_key_visual.png
  scene_02_forgetful_assistant_seedance_motion.mp4
  scene_06_skill_index_mj_key_visual.png
  scene_06_skill_index_seedance_motion.mp4
  author_03_motivation_mj_key_visual.png
  author_03_motivation_seedance_motion.mp4
  author_04_stack_mj_key_visual.png
  author_04_stack_seedance_motion.mp4
  author_06_industrialization_mj_key_visual.png
  author_06_industrialization_seedance_motion.mp4
```

## 全局视觉约束

- 16:9 横版。
- 统一使用 premium flat-vector educational explainer 风格。
- 保持 warm off-white paper background、thick dark ink outlines、clean geometric UI cards。
- 下方 18% 画面必须干净，留给 Remotion 中文字幕。
- 不要真实人脸，不要 photorealism，不要 anime，不要 3D render。
- 画面中的英文只允许少量大标签，不能出现长段小字。
- 字幕、中文解释、标题都由 Remotion 负责，不让 MJ / Seedance 生成。

通用 Midjourney suffix:

```text
--ar 16:9 --style raw --no text paragraph tiny text logo watermark brand signature subtitles caption realistic human face photorealism anime 3d render
```

通用 Seedance 尾部约束:

```text
Keep the lower 18% clean for Remotion Chinese subtitles. No readable extra text, no logo, no watermark, no realistic human faces, no photorealism, no anime, no 3D realism. Use restrained motion, calm educational rhythm, and a stable final pose for Remotion hold-frame.
```

## A 批次 Prompt

### 1. scene_00_intro_question

目的：开场提出“AI 失忆、流程反复解释”的问题，并把散乱流程聚合到 Skill。

Midjourney:

```text
premium flat-vector educational explainer frame, a forgetful AI assistant represented as a friendly simple robot at a desk, chat bubbles from yesterday fading away on the left, a new blank conversation window on the right, scattered workflow cards and preference cards floating between them, a clean SKILL handbook waiting near the bottom-right as the solution, warm off-white paper background, thick dark ink outlines, cyan blue and warm yellow accents, clear cause-and-effect composition, empty lower subtitle-safe area, no long readable text --ar 16:9 --style raw --no text paragraph tiny text logo watermark brand signature subtitles caption realistic human face photorealism anime 3d render
```

Seedance:

```text
@Image1 as the first frame and visual style reference. Create a 5-second premium flat-vector educational explainer animation. 0-1s: the old chat bubbles on the left gently fade and drift apart, showing that the AI forgot yesterday's context. 1-2.5s: the new blank conversation window on the right lights up while scattered workflow and preference cards wobble as if they must be explained again. 2.5-4s: the scattered cards begin moving toward the SKILL handbook, forming a clean path. 4-5s: the SKILL handbook gives one calm pulse and the surrounding cards settle into an ordered workflow arc. Camera mostly locked with a very slow push-in. Keep the lower 18% clean for Remotion Chinese subtitles. No readable extra text, no logo, no watermark, no realistic human faces, no photorealism, no anime, no 3D realism. Use restrained motion, calm educational rhythm, and a stable final pose for Remotion hold-frame.
```

### 2. scene_02_forgetful_assistant

目的：把“聪明但每次新对话会失忆”的矛盾视觉化。

Midjourney:

```text
premium flat-vector educational explainer frame, a smart AI assistant robot with a bright thinking node, surrounded by three memory shelves labeled only with simple icons for preferences, rules, and pitfalls, a reset switch or memory meter dropping back to zero, friendly but slightly frustrating mood, warm off-white paper background, thick dark outlines, simple geometric UI cards, cyan and coral accents, clear bottom subtitle-safe area, no long readable text --ar 16:9 --style raw --no text paragraph tiny text logo watermark brand signature subtitles caption realistic human face photorealism anime 3d render
```

Seedance:

```text
@Image1 as the first frame and visual style reference. Create a 5-second premium flat-vector educational explainer animation. 0-1s: the AI assistant's thinking node lights up quickly, showing intelligence. 1-2.5s: the preference, rule, and pitfall memory shelves glow one by one. 2.5-3.8s: a reset pulse passes across the scene; the shelves dim and the memory meter drops toward zero. 3.8-5s: the assistant remains capable but confused, with the cards softly floating as if the user must teach it again. Camera locked with a subtle push-in. Keep the lower 18% clean for Remotion Chinese subtitles. No readable extra text, no logo, no watermark, no realistic human faces, no photorealism, no anime, no 3D realism. Use restrained motion, calm educational rhythm, and a stable final pose for Remotion hold-frame.
```

### 3. scene_06_skill_index

目的：把 SKILL_INDEX 表达成“图书馆索引 / 查找层”。

Midjourney:

```text
premium flat-vector educational explainer frame, a friendly AI assistant holding a large clean index card labeled SKILL_INDEX, the card points toward a tidy library shelf of skill handbooks, each handbook represented by simple colored tabs and icons, one highlighted path from the index card to the correct handbook, warm off-white paper background, thick dark ink outlines, cyan, yellow, and green accents, clean lower subtitle-safe area, readable only the label SKILL_INDEX --ar 16:9 --style raw --no paragraph tiny text logo watermark brand signature subtitles caption realistic human face photorealism anime 3d render
```

Seedance:

```text
@Image1 as the first frame and visual style reference. Create a 5-second premium flat-vector educational explainer animation. 0-1s: the AI assistant raises the SKILL_INDEX card slightly, as if opening an index. 1-2.5s: a clean line grows from the card toward the library shelf, scanning across several colored skill handbooks. 2.5-4s: the correct handbook lights up and slides forward a little. 4-5s: the index card, path line, and selected handbook hold in a stable triangle composition. Keep the label SKILL_INDEX readable. Camera mostly locked with a very slow push-in. Keep the lower 18% clean for Remotion Chinese subtitles. No readable extra text, no logo, no watermark, no realistic human faces, no photorealism, no anime, no 3D realism.
```

### 4. author_03_motivation

目的：把作者“想法很多但不会剪辑”的私人动机视觉化。

Midjourney:

```text
premium flat-vector editorial explainer frame, a symbolic creator desk with many colorful idea bubbles floating above it, a difficult editing timeline gate or complex editing interface standing like a barrier, the idea bubbles flow around the barrier into a clean SKILL workflow handbook, personal but not sentimental, warm off-white paper background, thick dark ink outlines, soft cyan and warm orange accents, no realistic human face, clean lower subtitle-safe area --ar 16:9 --style raw --no text paragraph tiny text logo watermark brand signature subtitles caption realistic human face photorealism anime 3d render
```

Seedance:

```text
@Image1 as the first frame and visual style reference. Create a 5-second premium flat-vector editorial explainer animation. 0-1s: colorful idea bubbles gently appear above the creator desk. 1-2.2s: the bubbles try to enter the complex editing timeline gate but bounce back softly. 2.2-3.8s: a clean SKILL workflow handbook opens, creating a simpler path around the barrier. 3.8-5s: the idea bubbles flow into the handbook and settle into ordered cards. Camera locked with a gentle push-in. Keep the lower 18% clean for Remotion Chinese subtitles. No readable extra text, no logo, no watermark, no realistic human faces, no photorealism, no anime, no 3D realism.
```

### 5. author_04_stack

目的：清晰展示 Midjourney / Seedance / Eleven / Remotion / Suno / Codex 的分工。

Midjourney:

```text
premium flat-vector workflow diagram, six clean production modules arranged in a coordinated loop around a central project card labeled Skill, modules represented by simple icons only: image anchor for Midjourney, motion spark for Seedance, microphone waveform for Eleven, timeline for Remotion, music wave for Suno, conductor node for Codex, arrows showing division of labor and coordination, warm off-white paper background, thick dark ink outlines, cyan, yellow, purple, green accents, clean lower subtitle-safe area, no long readable text --ar 16:9 --style raw --no paragraph tiny text logo watermark brand signature subtitles caption realistic human face photorealism anime 3d render
```

Seedance:

```text
@Image1 as the first frame and visual style reference. Create a 5-second premium flat-vector workflow animation. 0-1s: the central Skill project card appears with a soft pulse. 1-2.5s: the six production modules light up in sequence: image anchor, motion spark, microphone waveform, music wave, timeline, conductor node. 2.5-4s: arrows connect the modules into a coordinated loop around Skill. 4-5s: a small pulse travels once around the loop, then the whole workflow settles. Camera locked, no cuts. Keep the lower 18% clean for Remotion Chinese subtitles. No readable extra text, no logo, no watermark, no realistic human faces, no photorealism, no anime, no 3D realism.
```

### 6. author_06_industrialization

目的：表达“任意文稿 -> 稳定流程 -> 不同风格视频”的工业化愿景，但避免过度承诺。

Midjourney:

```text
premium flat-vector educational workflow frame, a manuscript document enters a clean production pipeline, inside the pipeline are modular stages for prompt tuning, visual anchor, motion, voice, music, and Remotion timeline, the output side shows several abstract video style thumbnails as symbolic possibilities, not a factory cliché, calm and precise, warm off-white paper background, thick dark ink outlines, cyan, yellow, green and coral accents, clean lower subtitle-safe area, no long readable text --ar 16:9 --style raw --no paragraph tiny text logo watermark brand signature subtitles caption realistic human face photorealism anime 3d render
```

Seedance:

```text
@Image1 as the first frame and visual style reference. Create a 5-second premium flat-vector educational workflow animation. 0-1s: the manuscript document slides gently into the production pipeline. 1-2.5s: modular stages light up one by one, showing prompt tuning, visual anchor, motion, voice, music, and timeline coordination. 2.5-4s: a clean pulse moves through the pipeline toward the output side. 4-5s: several abstract video style thumbnails appear and hold steady, representing possible outputs without overpromising. Camera mostly locked with a subtle lateral track. Keep the lower 18% clean for Remotion Chinese subtitles. No readable extra text, no logo, no watermark, no realistic human faces, no photorealism, no anime, no 3D realism.
```

## B 批次 Brief

### scene_01_hook

视觉目标：用一个“神秘插件误解”被拆开的画面，说明 Skill 不是魔法。

关键词：mystery plugin box, magic illusion fading, simple handbook revealed, Skill as practical workflow manual.

### scene_03_skill_as_manual

视觉目标：岗位手册隐喻。

关键词：job manual, role card, workflow steps, output requirements, clean handbook pages.

### scene_07_common_mistakes

视觉目标：三个误区并列。

关键词：three warning cards, magic wand crossed out, missing attachment file, version archive missing.

### scene_08_ending_system

视觉目标：个人工作流系统开始成形。

关键词：personal workflow system, growing skill library, connected manuals, stable capability map.

### author_02_ai_made_this

视觉目标：图片、动画、配音、配乐、剪辑五个模块点亮。

关键词：five AI production modules, image, motion, voice, music, editing, all feeding into one video timeline.

### author_05_codex_conductor

视觉目标：Codex 位于中心，Skill 是流程，工具节点围绕。

关键词：Codex conductor node, Skill process manual, AI tools coordinated around a central workflow.

## Remotion 回接规则

1. 每个 A 批次 scene 新增两条 `SceneAsset`：
   - MJ key visual: `kind: 'image'`, `binding: 'foreground-image'`, 初始 `status: 'linked'` 或 `verified`；
   - Seedance motion: `kind: 'video'`, `binding: 'video-insert'`, 初始 `status: 'linked'`。
2. `filePath` 使用 `public/assets/full_film_20260610/...` 下的相对路径。
3. Seedance motion 不覆盖整段 scene，只在关键 beat 时间范围内出现。
4. Seedance 片段前后需要能回到 MJ 静态图持帧，避免视频源结束后黑帧。
5. 如果 Seedance 画面裁切、偏上、字幕区不干净，优先：
   - 缩小 `AssetLayer` 中该资产的显示尺寸；
   - 修改该资产的 `timeRange`；
   - 用 MJ 静态图兜底；
   - 不直接重做全片时间轴。

## 生产记录模板

每个素材回收后，在本文件追加：

```text
### Intake - <sceneId>

- MJ selected file:
- Seedance selected file:
- Public path:
- Duration:
- Visual issues:
- Integration decision:
- Verified frame / output:
```

## 下一步

先生成 A 批次的 6 张 Midjourney 关键图。选图通过后，再按对应 6 条 Seedance prompt 生成 5 秒动效。

## Intake - 2026-06-10 A 批次 Midjourney

### Intake - scene_00_intro_question

- MJ selected file: `mr_jumping_spider_premium_flat-vector_educational_explainer_f_215e52a5-09fc-4492-9c9c-726f232ce3ef_0.png`
- Public path: `public/assets/full_film_20260610/scene_00_intro_question_mj_key_visual.png`
- Dimensions: `1456x816`
- Analysis: 画面有 AI 助理、反复对话气泡、散落流程卡和右下角 Skill 手册，叙事对应度高；底部留白足够，适合叠字幕。
- Visual issues: 右侧新对话窗口和 Skill 手册之间的因果关系还可以通过 Seedance 动效加强。
- Integration decision: 归档为 `scene_00_intro_question` 的 MJ key visual，状态 `linked`。
- Seedance direction: 让左侧旧气泡淡出，散落卡片向 Skill 手册聚合，最后 Skill 手册稳定发光。

### Intake - scene_02_forgetful_assistant

- MJ selected file: `mr_jumping_spider_premium_flat-vector_educational_explainer_f_a6e92681-609d-4695-942e-7b690cb6d545_1.png`
- Public path: `public/assets/full_film_20260610/scene_02_forgetful_assistant_mj_key_visual.png`
- Dimensions: `1456x816`
- Analysis: 中央机器人和周围记忆卡片清楚，适合表达“聪明但需要记忆层”；底部安全区干净。
- Visual issues: 静态图中“失忆 / 重置”不够强，Seedance 需要强化 memory reset 或卡片熄灭。
- Integration decision: 归档为 `scene_02_forgetful_assistant` 的 MJ key visual，状态 `linked`。
- Seedance direction: 先点亮记忆卡片，再出现 reset pulse，让卡片变暗或错位，机器人保持困惑。

### Intake - scene_06_skill_index

- MJ selected file: `mr_jumping_spider_premium_flat-vector_educational_explainer_f_6cef656e-641a-4051-8f11-2d40c9690a39_2.png`
- Public path: `public/assets/full_film_20260610/scene_06_skill_index_mj_key_visual.png`
- Dimensions: `1456x816`
- Analysis: 机器人持卡和书架关系清楚，图书馆索引隐喻成立；`SKILL` 标签可读但不喧宾夺主。
- Visual issues: 原 prompt 目标是 `SKILL_INDEX`，当前图只显示 `SKILL`；Remotion 字幕可补足“技能索引”的语义。
- Integration decision: 归档为 `scene_06_skill_index` 的 MJ key visual，状态 `linked`。
- Seedance direction: 卡片指向书架，扫描并选中一本手册，强化“索引找到对应 Skill”的动作。

### Intake - author_03_motivation

- MJ selected file: `mr_jumping_spider_premium_flat-vector_editorial_explainer_fra_50b02dd3-0f23-4363-b65c-f12d46771028_2.png`
- Public path: `public/assets/full_film_20260610/author_03_motivation_mj_key_visual.png`
- Dimensions: `1456x816`
- Analysis: 创作者桌面、想法云、文稿/输出流向明确，个人动机氛围成立；右侧留白非常适合字幕。
- Visual issues: “不会剪辑的门槛”在静态图中偏弱，Seedance 需要补充时间线门槛或阻挡感。
- Integration decision: 归档为 `author_03_motivation` 的 MJ key visual，状态 `linked`。
- Seedance direction: 想法云从屏幕溢出，先被剪辑门槛挡住，再流入 Skill 或文稿路径。

### Intake - author_04_stack

- MJ selected file: `mr_jumping_spider_premium_flat-vector_workflow_diagram_six_cl_a1a3baf0-8113-4a98-99a7-c2a5e8619084_0.png`
- Public path: `public/assets/full_film_20260610/author_04_stack_mj_key_visual.png`
- Dimensions: `1456x816`
- Analysis: 六模块和中心项目卡清楚，图标化程度高，不依赖小字；非常适合作为工具链分工段的主视觉。
- Visual issues: 中央卡片没有明确 `Skill` 标签，但可以由旁白和字幕承担语义。
- Integration decision: 归档为 `author_04_stack` 的 MJ key visual，状态 `linked`。
- Seedance direction: 六模块依次点亮，连线形成环路，最后一圈 pulse 表达 Codex 调度。

### Intake - author_06_industrialization

- MJ selected file: `mr_jumping_spider_premium_flat-vector_educational_workflow_fr_06571a20-40a3-4845-aa18-478cc4e9a2c0_1.png`
- Public path: `public/assets/full_film_20260610/author_06_industrialization_mj_key_visual.png`
- Dimensions: `1456x816`
- Analysis: 文稿进入模块流水线、输出多种视频缩略图的关系明确，适合“工业化地生产成任意风格视频”的段落。
- Visual issues: 画面线条较细，Seedance 动效不宜过快，否则流程关系会变乱。
- Integration decision: 归档为 `author_06_industrialization` 的 MJ key visual，状态 `linked`。
- Seedance direction: 文稿进入管线，模块逐个发光，右侧输出缩略图依次出现并稳定。
