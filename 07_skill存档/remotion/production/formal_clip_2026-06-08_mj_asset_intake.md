# 2026-06-08 正式小片段全链路归档包

## 目标

- 项目:`Skill is All You Need`
- 阶段:正式 20-30s 小片段实验 / Midjourney 关键视觉锚接收
- 本轮实际工作流:MJ 关键图 -> Seedance 2.0 分镜运动 -> Eleven v3 分段旁白 -> Remotion 时间线 / 字幕 / 导出
- 复盘后推荐工作流:分镜 + 口播初稿 -> Eleven v3 分段 TTS -> 用真实口播时长反推 Seedance 目标时长 -> MJ / Seedance -> Remotion

本文件冻结本轮正式小片段从 MJ 关键图、Seedance 视频、Eleven v3 分段旁白到 Remotion v3 通过版的完整进度。

## 当前进度自检

| 分镜 | 命题 | 当前素材状态 | 下一步 |
|---|---|---|---|
| 01 | 为什么需要 Skill:AI 会忘记 | 新 MJ 图 + Seedance 视频已归档 | 进入 Eleven / Remotion |
| 02 | 反复输入压缩成 Skill | 复用旧 `scene_04` 素材 | 只在需要连续转场时重剪,不重新出图 |
| 03 | Skill 的文件形态:SKILL.md | 复用旧 `scene_05` 素材 | 只在需要连续转场时重剪,不重新出图 |
| 04 | SKILL_INDEX:AI 查目录取手册 | 新 MJ 图 + Seedance 视频已归档 | 进入 Eleven / Remotion,但 Remotion 中段需避开过近裁切 |
| 05 | 三工具闭环:MJ / Seedance / Eleven / Remotion | 新 MJ 图 + Seedance 视频已归档 | 进入 Eleven / Remotion |

阶段判断:

- MJ 阶段:01 / 04 / 05 新图已接收;02 / 03 明确复用旧资产。
- Seedance 阶段:01 / 04 / 05 视频已接收;02 / 03 明确复用旧视频。
- Eleven v3 阶段:已从连续旁白改为五段分镜旁白,字幕和音频共用同一份 timing。
- Remotion 无声排版草稿:已完成。
- Remotion 正式有声合成:已完成 v3 逐字字幕修正版。
- 当前可报告为"正式 20-30s 小片段实验完成 v3 逐字字幕修正版",用户审看验证通过。

## 本轮归档

### 01 为什么需要 Skill:AI 会忘记

保存目标:

```text
07_skill存档/remotion/public/assets/formal_clip_20260608/01_ai_forgets_mj_key_visual.png
```

来源:

```text
C:\Users\Administrator\Downloads\mr_jumping_spider_premium_flat-vector_educational_explainer_i_42d6d6a2-f058-4450-9563-78f287c65e46_0.png
```

画面记录:

- AI 助手坐在桌前,周围漂浮多组 prompt 气泡。
- 画面适合表达"每次都要重新教 AI"或"输入很多,记忆仍不稳定"。
- 下方留白较多,可供 Remotion 叠字幕。

Seedance 视频:

```text
07_skill存档/remotion/public/assets/formal_clip_20260608/01_ai_forgets_seedance_motion.mp4
```

来源:

```text
C:\Users\Administrator\Downloads\jimeng-2026-06-08-2295- as the first frame and visual style ref....mp4
```

元数据:

- 1280x720
- 约 5.06195s
- 60fps
- 文件大小:2688182 bytes

分析:

- 画面主体稳定,AI 助手保持坐姿。
- prompt 气泡有轻微漂移和重复出现感,适合作为开场运动素材。
- 可直接接入 02 的压缩成 Skill 旧素材。

### 04 SKILL_INDEX:AI 查目录取手册

保存目标:

```text
07_skill存档/remotion/public/assets/formal_clip_20260608/04_skill_index_mj_key_visual.png
```

来源:

```text
C:\Users\Administrator\Downloads\mr_jumping_spider_premium_flat-vector_educational_explainer_i_eeb7feaa-6391-4b12-8afa-da51ef78e17a_3.png
```

画面记录:

- AI 助手拿着 `SKILL_INDEX` 标签,旁边是资料架 / 图书馆隐喻。
- `SKILL_INDEX` 字样清楚,适合承担"索引层"概念。
- 后续 Seedance 运动重点应放在"取标签 -> 查架子 -> 定位手册",不要新增复杂角色。

Seedance 视频:

```text
07_skill存档/remotion/public/assets/formal_clip_20260608/04_skill_index_seedance_motion.mp4
```

来源:

```text
C:\Users\Administrator\Downloads\jimeng-2026-06-08-9393- as the first frame and visual style ref....mp4
```

元数据:

- 1280x720
- 约 5.06195s
- 60fps
- 文件大小:4607717 bytes

分析:

- 运动方向成立:`SKILL_INDEX` 标签指向书架,书架区域被强调。
- 风险:中段推镜过近,`SKILL_INDEX` 标签被裁到左侧,图书馆索引关系不再完整。
- Remotion 合成时优先使用开头/末尾的完整构图,或用 MJ 静态图兜底,不要把中段近景当全段主体。

### 05 三工具闭环:MJ / Seedance / Eleven / Remotion

保存目标:

```text
07_skill存档/remotion/public/assets/formal_clip_20260608/05_tool_loop_mj_key_visual.png
```

来源:

```text
C:\Users\Administrator\Downloads\mr_jumping_spider_premium_flat-vector_educational_explainer_i_efdd6726-5366-4268-9213-adbf2ec70c2a_2.png
```

画面记录:

- 四个生产模块由箭头串联,有明确流程感。
- 适合承接"MJ 建视觉锚 / Seedance 做机制运动 / Eleven 给声音 / Remotion 管时间线"。
- 后续 Seedance 运动重点应放在模块间的数据流,不要变成纯镜头推拉。

Seedance 视频:

```text
07_skill存档/remotion/public/assets/formal_clip_20260608/05_tool_loop_seedance_motion.mp4
```

来源:

```text
C:\Users\Administrator\Downloads\jimeng-2026-06-08-6630- as the first frame and visual style ref....mp4
```

元数据:

- 1280x720
- 约 5.06195s
- 60fps
- 文件大小:4225650 bytes

分析:

- 四个模块的横向关系保持完整。
- 箭头和波形模块有清晰流程感,适合作为结尾工具闭环段。
- 末帧稳定,可用于 Remotion 收束字幕。

## 复用旧素材

### 02 反复输入压缩成 Skill

复用:

```text
07_skill存档/remotion/public/assets/scene_04/mj_prompt_to_skill_key_visual.png
07_skill存档/remotion/public/assets/scene_04/seedance_prompt_to_skill_motion.mp4
```

说明:

- 该段已经完成过 MJ / Seedance / Remotion 单场景验证。
- 在正式连续片段里可以复用为中段机制动画,但必须标注为旧资产复用。

### 03 Skill 的文件形态:SKILL.md

复用:

```text
07_skill存档/remotion/public/assets/scene_05/mj_markdown_structure_key_visual.png
07_skill存档/remotion/public/assets/scene_05/seedance_markdown_structure_motion.mp4
```

说明:

- 该段已经完成过 MJ / Seedance / Remotion 单场景验证。
- 在正式连续片段里可以复用为文件结构解释段,但必须标注为旧资产复用。

## sceneAssets 登记

本轮新增登记:

```text
asset_formal_clip_01_ai_forgets_mj_key_visual
asset_formal_clip_01_ai_forgets_seedance_motion
asset_formal_clip_04_skill_index_mj_key_visual
asset_formal_clip_04_skill_index_seedance_motion
asset_formal_clip_05_tool_loop_mj_key_visual
asset_formal_clip_05_tool_loop_seedance_motion
```

登记文件:

```text
07_skill存档/remotion/src/data/sceneAssets.ts
```

状态约束:

- 三张新图登记为 `linked`。
- 三段新 Seedance 视频登记为 `linked`。
- 不登记为 `verified`,因为还没有对应 Eleven 音频和 Remotion 正式合成。
- 不改写旧 `scene_04` / `scene_05` 的验证资产。

## Remotion 草稿

Composition:

```text
FormalClip20260608
```

代码:

```text
07_skill存档/remotion/src/compositions/FormalClip20260608.tsx
```

Root 挂载:

```text
07_skill存档/remotion/src/Root.tsx
```

输出:

```text
07_skill存档/remotion/out/formal-clip-20260608-silent-draft.mp4
```

输出元数据:

- 1920x1080
- 30fps
- 720 frames
- 约 24.04s
- 文件大小:15421846 bytes

说明:

- 这是无声排版草稿,用于验证五段视频素材的连续性、字幕安全区和外框包装。
- 当前没有 Eleven v3 连续旁白,不能作为正式有声版本。
- 04 的 Seedance 中段存在近景裁切,composition 已在片尾淡回 MJ 静态图兜底。

## Eleven v3 旁白

脚本:

```text
07_skill存档/remotion/src/audio/formalClipVoiceover.ts
```

生成脚本:

```text
07_skill存档/remotion/scripts/generate-formal-clip-voiceover.ts
```

第一版音频:

```text
07_skill存档/remotion/public/audio/formal_clip_20260608/voiceover.mp3
```

Manifest:

```text
07_skill存档/remotion/public/audio/formal_clip_20260608/voiceover.manifest.json
```

音频元数据:

- Provider:ElevenLabs
- Model:`eleven_v3`
- 时长:约 30.56s
- 文件大小:489892 bytes
- 第一版问题:字幕按手工段落估算,没有和旁白音频逐句完全对应;`SKILL_INDEX` 英文口播存在语音崩坏风险。

旁白文本:

```text
[calm] AI 很聪明，但每次新对话，它都会忘记你刚教过的规则。

[slight pause] 所以，反复输入的内容，不该继续堆 prompt，而要压缩成流程。

Skill 本质上是一份可读的工作手册，写清角色、步骤和避坑。

SKILL_INDEX 像目录，告诉 AI 什么时候调用哪一本手册。

[confident] 最后，MJ 建视觉锚，Seedance 让机制动起来，Remotion 负责时间线和字幕。
```

v2 修正:

- 改为五段独立 Eleven v3 音频,每个分镜单独生成 MP3。
- `src/audio/generated/formalClipVoiceoverTiming.ts` 记录每段音频真实时长、起始帧、字幕文案和音频路径。
- `FormalClip20260608` 直接读取 timing 文件生成 Sequence,字幕和旁白不再分开手工估算。
- 第 04 段字幕保留 `SKILL_INDEX`,但 TTS 口播改为"技能索引",避免 Eleven v3 读英文标识时崩坏。
- v2 仍存在问题:字幕是语义对应,但不是逐字等于实际口播。

v3 修正:

- 字幕改为逐字等于实际口播文字,只去掉 Eleven 情绪控制标签如 `[calm]` / `[slight pause]` / `[confident]`。
- 第 04 段字幕同步改为"技能索引像目录,告诉 AI 什么时候调用哪一本手册。",不再保留 `SKILL_INDEX` 摘要字幕。
- 字幕盒改为更宽的逐字字幕样式,避免长句溢出。

v2 / v3 分段音频:

```text
07_skill存档/remotion/public/audio/formal_clip_20260608/formal_clip_01_ai_forgets.mp3
07_skill存档/remotion/public/audio/formal_clip_20260608/formal_clip_02_compress_to_skill.mp3
07_skill存档/remotion/public/audio/formal_clip_20260608/formal_clip_03_markdown_structure.mp3
07_skill存档/remotion/public/audio/formal_clip_20260608/formal_clip_04_skill_index.mp3
07_skill存档/remotion/public/audio/formal_clip_20260608/formal_clip_05_tool_loop.mp3
```

v2 / v3 timing:

```text
01 ai_forgets:0-160,约 4.96s
02 compress_to_skill:161-324,约 5.04s
03 markdown_structure:325-502,约 5.52s
04 skill_index:503-658,约 4.80s
05 tool_loop:659-874,约 6.80s
tail hold:875-904,30 frames
```

## Remotion 正式有声版

### v1 第一版

输出:

```text
07_skill存档/remotion/out/formal-clip-20260608-voiced.mp4
```

输出元数据:

- 1920x1080
- 30fps
- 930 frames
- 视频轨:约 31.00s
- 音频轨:约 31.02s
- 文件大小:18593219 bytes

说明:

- `FormalClip20260608` 已从 720 帧扩展为 930 帧,以适配 Eleven 真实语速。
- 每段 Seedance 视频源结束后淡回对应 MJ 静态图,避免源视频不足导致黑帧。
- 第一版问题:字幕与旁白不是逐段同源 timing,观感不够贴合;04 `SKILL_INDEX` 英文口播有语音崩坏。

### v2 修正版

输出:

```text
07_skill存档/remotion/out/formal-clip-20260608-voiced-v2.mp4
```

输出元数据:

- 1920x1080
- 30fps
- 905 frames
- 视频轨:约 30.17s
- 音频轨:约 30.19s
- 文件大小:17806896 bytes

说明:

- v2 使用五段独立旁白驱动五段字幕和五段画面 Sequence。
- 字幕文案来自每段 voiceover beat,不再和音频手工错开。
- 04 画面仍显示 `SKILL_INDEX`,但旁白说"技能索引",修正英文标识导致的语音崩坏。
- v2 问题:字幕仍是摘要式语义对应,没有逐字等于实际口播。

### v3 逐字字幕修正版

输出:

```text
07_skill存档/remotion/out/formal-clip-20260608-voiced-v3.mp4
```

输出元数据:

- 1920x1080
- 30fps
- 905 frames
- 视频轨:约 30.17s
- 音频轨:约 30.19s
- 文件大小:18068587 bytes

说明:

- 五段字幕均改为实际口播全文。
- 只移除不会被读出的 Eleven 情绪控制标签,不再做语义压缩。
- 已抽帧检查第 05 段最长字幕,文本完整显示,没有明显溢出。

## 下一步

1. 本轮成片 `formal-clip-20260608-voiced-v3.mp4` 已验证通过。
2. 后续同类正式片段应把 Eleven v3 分段 TTS 前置,先锁定每段口播真实时长。
3. Seedance prompt 不再默认统一 5s,而应按每段音频 duration 设置目标时长。

## 关联文档

- [[Remotion正式小片段实验工作流防偏移]]
- [[2026-06-08_Remotion_MJ_Seedance混合动画闭环复盘]]
- [[2026-06-08_Remotion正式小片段v3复盘]]
- [[AIGC_Skill到Remotion视频闭环]]
