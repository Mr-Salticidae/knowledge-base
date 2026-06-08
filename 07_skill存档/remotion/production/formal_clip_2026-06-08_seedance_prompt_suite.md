# 2026-06-08 正式小片段 Seedance 2.0 Prompt 套装

## 使用规则

- 每条 prompt 单独生成一段视频。
- 每次只上传对应分镜的 `@Image1`。
- 推荐生成时长:5s。
- 复盘修正:后续正式片段不应默认统一 5s。应先生成 Eleven v3 分段 TTS,再按每段真实口播时长设置 Seedance 目标时长。
- 推荐画幅:16:9 / 720p。
- 02 / 03 复用旧素材,本轮不重新生成。
- 本轮先生成 Seedance,再进入 Eleven v3 和 Remotion;验证通过后确认更优顺序应改为 Eleven v3 前置。

## 生成状态

| 分镜 | Seedance 状态 | 归档路径 |
|---|---|---|
| 01 | 已生成并归档 | `07_skill存档/remotion/public/assets/formal_clip_20260608/01_ai_forgets_seedance_motion.mp4` |
| 02 | 复用旧视频 | `07_skill存档/remotion/public/assets/scene_04/seedance_prompt_to_skill_motion.mp4` |
| 03 | 复用旧视频 | `07_skill存档/remotion/public/assets/scene_05/seedance_markdown_structure_motion.mp4` |
| 04 | 已生成并归档,中段有近景裁切风险 | `07_skill存档/remotion/public/assets/formal_clip_20260608/04_skill_index_seedance_motion.mp4` |
| 05 | 已生成并归档 | `07_skill存档/remotion/public/assets/formal_clip_20260608/05_tool_loop_seedance_motion.mp4` |

## 01 为什么需要 Skill:AI 会忘记

上传素材:

```text
@Image1 = 07_skill存档/remotion/public/assets/formal_clip_20260608/01_ai_forgets_mj_key_visual.png
```

生成时长:5s

```text
@Image1 as the first frame and visual style reference. Create a 5-second premium flat-vector educational explainer animation based on @Image1. Keep the same warm off-white paper texture, dark ink linework, simple robot assistant, desk, chair, and floating prompt bubbles. 0-1s: the AI assistant sits still at the desk; the surrounding prompt bubbles gently float in place, with subtle breathing motion and tiny line blocks flickering as if many instructions are being repeated. 1-2.5s: several prompt bubbles softly fade out and reappear in nearly the same positions, suggesting the assistant forgets and the user has to explain again; keep the camera locked with only a very slow push-in. 2.5-4s: the repeated bubbles begin to organize into a loose path from left to right, as if the repeated instructions are becoming a pattern instead of scattered messages. 4-5s: the motion settles into a clean final pose: the assistant remains at the desk, the bubbles hold steady, and the left side stays open enough for a transition into the next compression scene. Leave the lower third clean for Remotion subtitles. Style: premium editorial flat-vector science explainer, restrained motion, calm intelligent tone, no photorealism, no anime, no 3D realism, no realistic human faces, no extra readable text, no logo, no watermark.
```

保存目标:

```text
07_skill存档/remotion/public/assets/formal_clip_20260608/01_ai_forgets_seedance_motion.mp4
```

验收标准:

- 气泡必须有"重复出现 / 被重新解释"的感觉。
- 不要让机器人离开座位,不要新增复杂角色。
- 末帧要稳定,方便接入 02 的压缩成 Skill 旧素材。

## 02 反复输入压缩成 Skill

本轮不重新生成,复用旧视频:

```text
07_skill存档/remotion/public/assets/scene_04/seedance_prompt_to_skill_motion.mp4
```

说明:

- 这段已经完成过 Seedance 机制动画。
- 正式片段里只需要在 Remotion 阶段重剪入连续时间线。
- 如果后续发现风格或节奏无法衔接,再单独开新一轮重生成。

## 03 Skill 的文件形态:SKILL.md

本轮不重新生成,复用旧视频:

```text
07_skill存档/remotion/public/assets/scene_05/seedance_markdown_structure_motion.mp4
```

说明:

- 这段已经完成过 Seedance 结构分层动画。
- 正式片段里只需要在 Remotion 阶段重剪入连续时间线。
- 该段开头主体偏上,Remotion 合成时优先从有效中段切入,必要时用 MJ 静态图兜底。

## 04 SKILL_INDEX:AI 查目录取手册

上传素材:

```text
@Image1 = 07_skill存档/remotion/public/assets/formal_clip_20260608/04_skill_index_mj_key_visual.png
```

生成时长:5s

```text
@Image1 as the first frame and visual style reference. Create a 5-second premium flat-vector educational explainer animation based on @Image1. Keep the same warm paper background, thick dark outlines, simple robot assistant, SKILL_INDEX tag, library shelf, binders, books, and clean minimal composition. 0-1s: the robot assistant holds the SKILL_INDEX tag steady; the tag gives one subtle paper-like lift and settles, while the camera stays locked with a very slow push-in. 1-2.3s: a soft highlight travels from the SKILL_INDEX tag toward the shelf, as if the index is pointing to where the correct skill manual is located. 2.3-3.8s: one or two books or binder tabs on the shelf gently slide forward a few centimeters, not leaving the shelf, showing that the right manual has been found. 3.8-5s: the highlighted book and the SKILL_INDEX tag hold in a stable final pose, forming a clear lookup relationship between index and library. Leave the lower third clean for Remotion subtitles. Style: premium editorial flat-vector science explainer, restrained motion, calm intelligent tone, no photorealism, no anime, no 3D realism, no realistic human faces, no extra readable text beyond SKILL_INDEX if already present, no logo, no watermark.
```

保存目标:

```text
07_skill存档/remotion/public/assets/formal_clip_20260608/04_skill_index_seedance_motion.mp4
```

验收标准:

- `SKILL_INDEX` 标签必须保持清楚。
- 运动要表达"查索引 -> 定位手册",不是单纯推镜。
- 不要新增大段文字,不要让书架变成复杂背景。

## 05 三工具闭环:MJ / Seedance / Eleven / Remotion

上传素材:

```text
@Image1 = 07_skill存档/remotion/public/assets/formal_clip_20260608/05_tool_loop_mj_key_visual.png
```

生成时长:5s

```text
@Image1 as the first frame and visual style reference. Create a 5-second premium flat-vector educational explainer animation based on @Image1. Keep the same warm off-white paper texture, dark ink outlines, four connected production modules, arrows, browser-like panels, waveform panel, and timeline-like final panel. 0-1s: all four modules hold in a clean stable layout; the first arrow gives a subtle pulse, introducing the workflow direction. 1-2s: the first module gently activates with a small image-card flicker, then the arrow pulse travels to the second module, suggesting the key visual becomes animated motion. 2-3s: the second module shows a restrained internal motion, such as small gears or marks rotating once, then the pulse moves to the waveform module. 3-4s: the waveform panel softly animates with vertical bars rising and falling, suggesting Eleven voice or sound entering the workflow. 4-5s: the pulse reaches the final timeline panel; the bottom timeline line fills slightly from left to right, then all modules settle into a clear final production loop. Leave the lower third clean for Remotion subtitles. Style: premium editorial flat-vector science explainer, restrained motion, calm intelligent tone, no photorealism, no anime, no 3D realism, no realistic human faces, no extra readable text, no logo, no watermark.
```

保存目标:

```text
07_skill存档/remotion/public/assets/formal_clip_20260608/05_tool_loop_seedance_motion.mp4
```

验收标准:

- 必须保留四个模块的横向流程关系。
- 箭头 / 数据流要从左到右推进。
- 不要变成快速转场合集,末帧必须稳定,方便做结尾字幕和收束。

## 生成后回填

生成完成后,把三个 MP4 放到:

```text
07_skill存档/remotion/public/assets/formal_clip_20260608/
```

并回填:

```text
07_skill存档/remotion/src/data/sceneAssets.ts
```

推荐新增资产 ID:

```text
asset_formal_clip_01_ai_forgets_seedance_motion
asset_formal_clip_04_skill_index_seedance_motion
asset_formal_clip_05_tool_loop_seedance_motion
```

完成三段 Seedance 后,本轮进入 Eleven v3 分段旁白和 Remotion 合成,最终 v3 验证通过。

## 复盘修正

本轮三段新 Seedance 视频统一按 5s 生成,后续由 Remotion 用静态 MJ 图兜底音频时长。这条链路可用,但不应作为下一轮默认流程。

更优流程:

```text
逐段口播初稿
→ Eleven v3 分段 TTS
→ 读取每段真实 duration
→ Seedance prompt 按该 duration 设置目标时长
→ Remotion 按同一份 timing 合成字幕和音频
```

核心规则:旁白驱动的解释视频里,口播时长是时间线主轴。Seedance 应跟随 TTS timing,不是 Remotion 后期再硬补。
